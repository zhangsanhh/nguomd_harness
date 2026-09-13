#!/usr/bin/env python3
"""项目级会话归档钩子的共享函数。

本模块只做本地数据整理，不调用模型、不访问网络，也不向 stdout 输出内容。
"""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARCHIVE_ROOT = PROJECT_ROOT / "会话日志与摘要"
DIARY_TRIGGER = "请根据我的原始初稿完成日记的工作流"
DIARY_FALLBACK_PATTERN = re.compile(
    r"(?m)(?:^\s*(?:请\s*)?(?:完成|整理|处理|生成|输出).{0,30}日记.{0,30}(?:三个|三项|三种|三版|三)产出|(?:^|[】\]\n])\s*(?:(?:\d{1,4}\s*月\s*\d{1,2}\s*[日号]?|昨日|今日)\s*)?日记\s*(?:三个|三项|三种|三版|三)产出)\s*$"
)
BEIJING = ZoneInfo("Asia/Shanghai")


def archive_root() -> Path:
    configured = os.environ.get("CODEX_CONVERSATION_ARCHIVE_ROOT")
    return Path(configured).expanduser().resolve() if configured else DEFAULT_ARCHIVE_ROOT


def data_root() -> Path:
    return archive_root() / ".归档数据"


def pending_root() -> Path:
    return archive_root() / ".待归档"


def now() -> datetime:
    return datetime.now(BEIJING)


def now_iso() -> str:
    return now().isoformat(timespec="seconds")


def date_from_iso(value: str | None) -> str:
    if isinstance(value, str):
        match = re.match(r"^(\d{4}-\d{2}-\d{2})", value)
        if match:
            return match.group(1)
    return now().strftime("%Y-%m-%d")


def load_event() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        event = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return {}
    return event if isinstance(event, dict) else {}


def safe_part(value: Any, fallback: str = "unknown") -> str:
    text = str(value or "").strip()
    text = re.sub(r"[^0-9A-Za-z._-]+", "_", text)
    return (text[:120] or fallback)


def prompt_key(session_id: Any, turn_id: Any, prompt: str) -> str:
    session = safe_part(session_id)
    turn = str(turn_id or "").strip()
    if not turn:
        turn = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]
    return f"{session}--{safe_part(turn)}"


def write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
    finally:
        temp_path.unlink(missing_ok=True)


def append_jsonl_unique(path: Path, value: dict[str, Any], key: str = "record_id") -> bool:
    """在跨会话并发时安全追加，并按 record_id 去重。"""

    path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = path.parent.parent / ".write.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    target_key = value.get(key)
    with lock_path.open("a+", encoding="utf-8") as lock_handle:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        try:
            if path.exists():
                with path.open("r", encoding="utf-8") as handle:
                    for line in handle:
                        try:
                            existing = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if target_key and existing.get(key) == target_key:
                            return False
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            return True
        finally:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)


def is_diary_trigger(prompt: str) -> bool:
    if not isinstance(prompt, str):
        return False
    if (
        prompt.lstrip().startswith(DIARY_TRIGGER)
        or re.search(rf"(?m)^\s*{re.escape(DIARY_TRIGGER)}(?:\s|$)", prompt)
    ):
        return True
    # 次日补做日记时，允许“完成昨日日记的三个产出”这类明确请求触发；
    # 设置长度门槛，避免普通的规则讨论被误判为全天日记。
    return bool(DIARY_FALLBACK_PATTERN.search(prompt) and compact_char_count(prompt) >= 500)


def compact_char_count(text: str) -> int:
    return len(re.sub(r"\s+", "", text or ""))


def split_quoted_text(text: str) -> tuple[str, str, float]:
    """剥离常见明确引用区，返回自写部分、引用部分和引用占比。

    这是保守的本地筛选，不声称能理解所有语义引用；最终规则仍要求模型复核。
    """

    if not text:
        return "", "", 0.0

    own_lines: list[str] = []
    quoted_parts: list[str] = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            quoted_parts.append(line)
            continue
        if in_fence or stripped.startswith(">"):
            quoted_parts.append(line)
        else:
            own_lines.append(line)

    own = "".join(own_lines)

    patterns = (
        r"【[\s\S]{40,}?】",
        r"“[\s\S]{40,}?”",
        r"「[\s\S]{40,}?」",
        r"『[\s\S]{40,}?』",
        r"<blockquote\b[^>]*>[\s\S]*?</blockquote>",
    )
    for pattern in patterns:
        def collect(match: re.Match[str]) -> str:
            quoted_parts.append(match.group(0))
            return ""

        own = re.sub(pattern, collect, own)

    total = compact_char_count(text)
    quoted = compact_char_count("\n".join(quoted_parts))
    ratio = quoted / total if total else 0.0
    return own.strip(), "\n".join(quoted_parts).strip(), ratio


def is_quote_dominant(text: str) -> bool:
    own, quoted, ratio = split_quoted_text(text)
    return bool(quoted and compact_char_count(quoted) >= 40 and ratio >= 0.5)


def heading_level(line: str) -> int | None:
    match = re.match(r"^\s*(#{1,6})\s+", line)
    return len(match.group(1)) if match else None


def section_line_matches(line: str, title: str) -> bool:
    normalized = re.sub(r"[*_`]", "", line).strip()
    if title not in normalized:
        return False
    return bool(
        normalized.startswith("#")
        or re.match(r"^\s*\d+[.)、]\s*", normalized)
        or normalized.startswith("-")
        or normalized.startswith("**")
    )


def extract_section(message: str, title: str) -> str:
    if not message:
        return ""
    lines = message.splitlines()
    start = None
    start_level = 2
    for index, line in enumerate(lines):
        if section_line_matches(line, title):
            start = index
            start_level = heading_level(line) or 2
            break
    if start is None:
        return ""

    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith(("📌", "📝")):
            end = index
            break
        level = heading_level(lines[index])
        if level is not None and level <= start_level:
            end = index
            break
    return "\n".join(lines[start + 1 : end]).strip()


def extract_optimized_phrase(section: str) -> str:
    for line in (section or "").splitlines():
        match = re.search(r"(?:优化表述|建议改写|改写版本)\s*[：:]\s*(.+)$", line.strip())
        if match:
            return match.group(1).strip().strip("`")
    return ""


def normal_length_status(original: str, optimized: str, suggestion: str = "") -> dict[str, Any]:
    original_chars = compact_char_count(original)
    optimized_chars = compact_char_count(optimized)
    suggestion_chars = compact_char_count(suggestion)
    ratio = optimized_chars / original_chars if original_chars else None
    passed = bool(
        ratio is not None
        and 0.4 <= ratio <= 1.1
        and optimized_chars <= 250
        and suggestion_chars <= 250
    )
    return {
        "original_chars": original_chars,
        "optimized_chars": optimized_chars,
        "suggestion_chars": suggestion_chars,
        "ratio": round(ratio, 3) if ratio is not None else None,
        "suggestion_length_status": "通过" if suggestion_chars <= 250 else "需复核",
        "length_status": "通过" if passed else "需复核",
    }


def run_generator(root: Path | None = None) -> None:
    root = root or archive_root()
    node = shutil.which("node")
    if not node:
        for candidate in ("/opt/homebrew/bin/node", "/usr/local/bin/node"):
            if Path(candidate).exists():
                node = candidate
                break
    if not node:
        return
    generator = PROJECT_ROOT / "会话日志与摘要" / "生成对话与表达索引.mjs"
    if not generator.exists():
        return
    env = os.environ.copy()
    env["CODEX_CONVERSATION_ARCHIVE_ROOT"] = str(root)
    try:
        subprocess.run(
            [node, str(generator)],
            cwd=PROJECT_ROOT,
            env=env,
            timeout=20,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return
