#!/usr/bin/env python3
"""Stop：把当前轮的用户消息和助手可见回复写入本地归档，并重建索引。"""

from __future__ import annotations

import hashlib
import fcntl
import json
import re
import sys
from datetime import date as date_type
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from conversation_archive_common import (
    append_jsonl_unique,
    archive_root,
    compact_char_count,
    date_from_iso,
    extract_optimized_phrase,
    extract_section,
    is_diary_trigger,
    is_quote_dominant,
    load_event,
    normal_length_status,
    now_iso,
    pending_root,
    prompt_key,
    run_generator,
    safe_part,
    split_quoted_text,
    write_json_atomic,
)
from relationship_habit import append_relationship_habit_entries


def load_pending(session_id: str, turn_id: str) -> tuple[Path | None, dict[str, Any]]:
    key = prompt_key(session_id, turn_id, "")
    exact = pending_root() / f"{safe_part(key)}.json"
    candidates = [exact] if exact.exists() else []
    if not candidates and not turn_id:
        prefix = f"{safe_part(session_id)}--"
        candidates = sorted(
            (path for path in pending_root().glob(f"{prefix}*.json") if path.is_file()),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
    for path in candidates:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(value, dict):
                return path, value
        except (OSError, json.JSONDecodeError):
            continue
    return None, {}


def record_id(session_id: str, turn_id: str, prompt: str, assistant: str) -> str:
    if turn_id:
        return f"{safe_part(session_id)}--{safe_part(turn_id)}"
    digest = hashlib.sha256(f"{prompt}\n{assistant}".encode("utf-8")).hexdigest()[:20]
    return f"{safe_part(session_id)}--{digest}"


def infer_diary_date(prompt: str, fallback: str) -> str:
    """优先取日记正文中的明确日期，避免次日处理“昨日日记”时归错日期。"""

    match = re.search(
        r"(?:^|[\s\[【#])(?:(\d{4})\s*年\s*)?(\d{1,2})\s*月\s*(\d{1,2})\s*[日号]?",
        prompt or "",
    )
    if match:
        year = int(match.group(1) or fallback[:4])
        month = int(match.group(2))
        day = int(match.group(3))
        try:
            return date_type(year, month, day).isoformat()
        except ValueError:
            pass
    if "昨日日记" in (prompt or ""):
        try:
            return (datetime.strptime(fallback, "%Y-%m-%d").date() - timedelta(days=1)).isoformat()
        except ValueError:
            pass
    return fallback


def append_manual_diary_source(
    conversation: dict[str, Any],
    prompt: str,
    suggestion: str,
) -> None:
    """把日记优化区块追加到当天全天日记手工补录；只追加且按正文去重，保留用户已有内容。"""

    body = suggestion.strip()
    if not body:
        return
    date = infer_diary_date(prompt, str(conversation.get("date") or date_from_iso(None)))
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        return
    source = archive_root() / "口语化表达" / "手工补录全天日记版" / f"{date}.md"
    source.parent.mkdir(parents=True, exist_ok=True)
    lock_path = archive_root() / ".归档数据" / ".write.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    submitted_at = str(conversation.get("submitted_at") or now_iso())
    header = (
        f"<!-- date: {date}; time: {submitted_at}; type: 口述日记 -->\n\n"
        f"# {date} 日记口语化词汇优化建议\n\n"
        "> 处理对象是全天个人日记表达，不处理外部引文整段原文。保留个人语气，并区分事实、判断、计划和待验证内容。\n\n"
    )
    with lock_path.open("a", encoding="utf-8") as lock_handle:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        try:
            existing = source.read_text(encoding="utf-8") if source.exists() else ""
            if body in existing:
                return
            if existing.strip():
                addition = f"\n\n---\n\n## 追加记录｜{submitted_at}\n\n{body}\n"
                with source.open("a", encoding="utf-8") as handle:
                    handle.write(addition)
            else:
                source.write_text(f"{header}{body}\n", encoding="utf-8")
        finally:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)


def build_expression_record(
    conversation: dict[str, Any],
    prompt: str,
    assistant: str,
) -> dict[str, Any] | None:
    diary = is_diary_trigger(prompt)
    if diary:
        suggestion = extract_section(assistant, "口语化词汇优化建议")
        if suggestion:
            append_manual_diary_source(conversation, prompt, suggestion)
        return {
            "version": 1,
            "record_id": conversation["record_id"],
            "date": conversation["date"],
            "time": conversation["submitted_at"],
            "session_id": conversation["session_id"],
            "turn_id": conversation["turn_id"],
            "type": "口述日记",
            "status": "已提取" if suggestion else "未识别到规范标题",
            "source_text": "",
            "source_note": "完整口述日记原文见同一时间的对话归档。",
            "suggestion_text": suggestion,
            "length_policy": "日记专属建议：不受普通提问250字上限限制。",
            "original_chars": None,
            "optimized_chars": None,
            "ratio": None,
            "length_status": "不适用",
        }

    own_text, _, quote_ratio = split_quoted_text(prompt)
    if is_quote_dominant(prompt):
        return None

    suggestion = extract_section(assistant, "本次提问表达优化")
    diary_suggestion = extract_section(assistant, "口语化词汇优化建议")
    if diary_suggestion and "日记" in prompt and compact_char_count(prompt) >= 500:
        append_manual_diary_source(conversation, prompt, diary_suggestion)
    optimized = extract_optimized_phrase(suggestion)
    length = normal_length_status(own_text, optimized, suggestion) if optimized else {
        "original_chars": compact_char_count(own_text),
        "optimized_chars": None,
        "suggestion_chars": compact_char_count(suggestion) if suggestion else None,
        "ratio": None,
        "suggestion_length_status": "通过" if suggestion and compact_char_count(suggestion) <= 250 else "待复核",
        "length_status": "待复核",
    }
    return {
        "version": 1,
        "record_id": conversation["record_id"],
        "date": conversation["date"],
        "time": conversation["submitted_at"],
        "session_id": conversation["session_id"],
        "turn_id": conversation["turn_id"],
        "type": "普通提问",
        "status": "已提取" if suggestion else "未识别到规范标题",
        "source_text": own_text,
        "source_note": f"明确引用占比约 {round(quote_ratio * 100)}%。",
        "suggestion_text": suggestion,
        "length_policy": "普通提问建议：原文40%—110%，通常不超过250字。",
        **length,
    }


def main() -> None:
    pending_path: Path | None = None
    try:
        event = load_event()
        session_id = str(event.get("session_id") or "unknown")
        turn_id = str(event.get("turn_id") or "")
        assistant = event.get("last_assistant_message", "")
        if not isinstance(assistant, str):
            assistant = str(assistant)

        pending_path, pending = load_pending(session_id, turn_id)
        if pending_path is None:
            # 没有匹配到用户消息时，不写入“空 prompt”的助手孤儿记录。
            return
        prompt = pending.get("prompt", "")
        if not isinstance(prompt, str):
            prompt = str(prompt)

        submitted_at = str(pending.get("submitted_at") or "")
        date = str(pending.get("date") or date_from_iso(submitted_at))
        completed_at = now_iso()
        if not submitted_at or not re.match(r"^\d{4}-\d{2}-\d{2}", submitted_at):
            submitted_at = completed_at
        if not date or len(date) != 10:
            date = date_from_iso(None)

        rid = record_id(session_id, turn_id, prompt, assistant)
        conversation = {
            "version": 1,
            "record_id": rid,
            "date": date,
            "submitted_at": submitted_at,
            "completed_at": completed_at,
            "session_id": session_id,
            "turn_id": turn_id,
            "cwd": str(pending.get("cwd") or event.get("cwd") or ""),
            "model": str(pending.get("model") or event.get("model") or ""),
            "prompt": prompt,
            "assistant": assistant,
        }
        conversation_file = archive_root() / ".归档数据" / "对话" / f"{date}.jsonl"
        append_jsonl_unique(conversation_file, conversation)

        expression = build_expression_record(conversation, prompt, assistant) if prompt else None
        if expression is not None and expression.get("type") == "普通提问":
            expression_file = archive_root() / ".归档数据" / "表达" / f"{date}.jsonl"
            append_jsonl_unique(expression_file, expression)

        try:
            source_date = infer_diary_date(prompt, date) if is_diary_trigger(prompt) else date
            append_relationship_habit_entries(conversation, prompt, assistant, source_date)
        except Exception as exc:
            # 关系与惯习沉淀失败不得影响本轮会话归档和正常回复。
            print(f"relationship habit archive skipped: {exc}", file=sys.stderr)

        if pending_path is not None:
            pending_path.unlink(missing_ok=True)
        run_generator(archive_root())
    except Exception as exc:  # 归档失败不得改变已经完成的助手回复
        print(f"conversation archive stop skipped: {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
