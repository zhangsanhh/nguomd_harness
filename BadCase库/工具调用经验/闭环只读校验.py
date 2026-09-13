#!/usr/bin/env python3
"""Bad Case 闭环一致性只读校验。

只检查当前 DSC 项目的失败资产与活动项目钩子，不改状态、不删除文件、不修复链接。
退出码：0=没有结构性错误；1=发现结构性错误。证据不足和逾期项以 WARN 输出。
"""

from __future__ import annotations

import json
import re
import sys
import csv
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BADCASE_ROOT = PROJECT_ROOT / "BadCase库"
MODULE_FILES = sorted(BADCASE_ROOT.glob("[0-9][0-9]_*.md"))
PITFALL_FILE = BADCASE_ROOT / "工具调用经验" / "Pitfall经验库.md"
REGRESSION_FILE = BADCASE_ROOT / "回归集.md"
ACTIVE_CODEX_ROOT = PROJECT_ROOT / ".codex"
OLD_ROOT = os.environ.get("OLD_ROOT", "<OLD_PROJECT_ROOT>")  # 公开版：旧根路径改为可配置
STATES = ("待审核", "已批准", "执行中", "待验证", "已验证", "已关闭")
REGRESSION_STATES = ("待跑", "通过", "失败", "不适用", "阻断", "证据不足")


def emit(bucket: list[str], message: str) -> None:
    bucket.append(message)


def markdown_parts(line: str) -> list[str]:
    return [part.strip() for part in line.strip().strip("|").split("|")]


def parse_module_cases(path: Path) -> tuple[dict[str, str], dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    index: dict[str, str] = {}
    for line in text.splitlines():
        if not line.lstrip().startswith("| BC_"):
            continue
        parts = markdown_parts(line)
        if len(parts) >= 5:
            index[parts[0]] = parts[-1]

    headings = list(re.finditer(r"^##\s+(BC_[^\s]+).*?$", text, re.M))
    bodies: dict[str, str] = {}
    for pos, heading in enumerate(headings):
        end = headings[pos + 1].start() if pos + 1 < len(headings) else len(text)
        bodies[heading.group(1)] = text[heading.start() : end]
    return index, bodies


def extract_state(block: str) -> str | None:
    current = re.search(r"^- 当前处理状态：\s*([^；。\n]+)", block, re.M)
    if current:
        for state in STATES:
            if current.group(1).strip().startswith(state):
                return state
    repair = re.search(r"^- 修复状态：\s*([^（\n；。]+)", block, re.M)
    if repair:
        value = repair.group(1).strip()
        for state in STATES:
            if value.startswith(state):
                return state
    status = re.search(r"^- 当前状态：\s*([^；。\n]+)", block, re.M)
    if status:
        for state in STATES:
            if status.group(1).strip().startswith(state):
                return state
    return None


def check_case_assets(errors: list[str], warnings: list[str], passed: list[str]) -> None:
    all_ids: list[str] = []
    for path in MODULE_FILES:
        index, bodies = parse_module_cases(path)
        all_ids.extend(index)
        body_ids = set(bodies)
        for case_id in sorted(set(index) - body_ids):
            emit(errors, f"{path.relative_to(PROJECT_ROOT)}: 索引有 {case_id}，正文缺失")
        for case_id in sorted(body_ids - set(index)):
            emit(errors, f"{path.relative_to(PROJECT_ROOT)}: 正文有 {case_id}，模块索引缺失")
        for case_id, row_state in index.items():
            if case_id not in bodies:
                continue
            body_state = extract_state(bodies[case_id])
            if body_state is None:
                emit(errors, f"{path.relative_to(PROJECT_ROOT)}:{case_id}: 缺少可解析的当前状态")
            elif row_state != body_state:
                emit(errors, f"{path.relative_to(PROJECT_ROOT)}:{case_id}: 索引状态={row_state}，正文状态={body_state}")
            block = bodies[case_id]
            if body_state == "已验证" and not re.search(r"验证|证据", block):
                emit(warnings, f"{path.relative_to(PROJECT_ROOT)}:{case_id}: 已验证但未找到验证/证据说明")
            if body_state == "待验证" and not re.search(r"待验证|证据不足|下一动作|下一步", block):
                emit(warnings, f"{path.relative_to(PROJECT_ROOT)}:{case_id}: 待验证但缺少下一动作或证据边界")
    duplicates = [case_id for case_id, count in Counter(all_ids).items() if count > 1]
    if duplicates:
        emit(errors, f"BadCase 编号重复：{', '.join(sorted(duplicates))}")
    else:
        emit(passed, f"BadCase 编号唯一：{len(set(all_ids))} 条")


def check_pitfall_ids(errors: list[str], passed: list[str]) -> None:
    text = PITFALL_FILE.read_text(encoding="utf-8")
    ids = re.findall(r"^###\s+Pitfall-(\d{3})\s+", text, re.M)
    duplicates = [f"Pitfall-{key}" for key, count in Counter(ids).items() if count > 1]
    if duplicates:
        emit(errors, f"Pitfall 编号重复：{', '.join(sorted(duplicates))}")
    else:
        emit(passed, f"Pitfall 编号唯一：{len(set(ids))} 条")


def check_links(errors: list[str], passed: list[str]) -> None:
    files = [
        BADCASE_ROOT / "README.md",
        BADCASE_ROOT / "模板_单条badcase.md",
        BADCASE_ROOT / "回归集.md",
        BADCASE_ROOT / "闭环审计与补录台账-2026-09-09.md",
        BADCASE_ROOT / "审计证据" / "README.md",
        PITFALL_FILE,
        *MODULE_FILES,
    ]
    broken: list[str] = []
    pattern = re.compile(r"\]\(<?([^)>]+)>?\)")
    for path in files:
        text = path.read_text(encoding="utf-8")
        for raw in pattern.findall(text):
            target = raw.strip()
            if not target or re.match(r"^(?:https?|mailto|data):", target) or target.startswith("#"):
                continue
            target = target.split("#", 1)[0]
            target = re.sub(r":\d+$", "", target)
            candidate = Path(target).expanduser() if target.startswith("/") else path.parent / target
            if not candidate.exists():
                broken.append(f"{path.relative_to(PROJECT_ROOT)} -> {target}")
    if broken:
        for item in broken:
            emit(errors, f"失效引用：{item}")
    else:
        emit(passed, "BadCase 核心文档相对/绝对链接均存在")


def check_active_hooks(errors: list[str], passed: list[str]) -> None:
    hooks_file = ACTIVE_CODEX_ROOT / "hooks.json"
    data = json.loads(hooks_file.read_text(encoding="utf-8"))
    commands: list[str] = []

    def walk(value: object) -> None:
        if isinstance(value, dict):
            if isinstance(value.get("command"), str):
                commands.append(value["command"])
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(data)
    expected = (
        "inject_time.sh",
        "diary_workflow_trigger.sh",
        "relationship_habit_trigger.py",
        "expression_optimizer_trigger.py",
        "archive_user_prompt.py",
        "pre_compact.sh",
        "post_tool_use.sh",
        "archive_turn.py",
        "pre_tool_use_gate.sh",
    )
    if len(commands) != len(expected):
        emit(errors, f"活动钩子命令数={len(commands)}，预期={len(expected)}")
    for name in expected:
        matches = [command for command in commands if name in command]
        target = ACTIVE_CODEX_ROOT / name
        if len(matches) != 1:
            emit(errors, f"活动钩子缺少唯一入口：{name}")
        elif str(target) not in matches[0] or not target.exists():
            emit(errors, f"活动钩子目标无效：{name}")
    active_sources = [hooks_file, *ACTIVE_CODEX_ROOT.glob("*.sh"), *ACTIVE_CODEX_ROOT.glob("*.py")]
    stale = [path.relative_to(PROJECT_ROOT) for path in active_sources if OLD_ROOT in path.read_text(encoding="utf-8")]
    if stale:
        for path in stale:
            emit(errors, f"活动文件仍含旧项目路径：{path}")
    else:
        emit(passed, "活动钩子 9 个入口均指向当前项目，未发现旧项目路径")


def check_versions(errors: list[str], passed: list[str]) -> None:
    agents = (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    header = re.search(r"版本：([0-9.]+)", agents)
    footer = re.search(r"当前版本：([0-9.]+)", agents)
    changes = (PROJECT_ROOT / "AGENTS版本变更.md").read_text(encoding="utf-8")
    top = re.search(r"^\|\s*([0-9.]+)\s*\|", changes, re.M)
    versions = [m.group(1) for m in (header, footer, top) if m]
    if len(versions) != 3 or len(set(versions)) != 1:
        emit(errors, f"AGENTS 版本不一致：{versions}")
    else:
        emit(passed, f"AGENTS 版本一致：{versions[0]}")


def check_audit_ledger(errors: list[str], warnings: list[str], passed: list[str]) -> None:
    ledger = BADCASE_ROOT / "闭环审计与补录台账-2026-09-09.md"
    text = ledger.read_text(encoding="utf-8")
    ledger_states: dict[str, str] = {}
    for line in text.splitlines():
        if not line.lstrip().startswith("| BC_"):
            continue
        parts = markdown_parts(line)
        if len(parts) >= 5 and parts[1] in STATES:
            ledger_states[parts[0]] = parts[1]
    module_states: dict[str, str] = {}
    for path in MODULE_FILES:
        index, _ = parse_module_cases(path)
        module_states.update(index)
    if ledger_states.keys() != module_states.keys():
        emit(errors, f"审计台账案例集合与模块索引不一致：台账={len(ledger_states)}，模块={len(module_states)}")
    else:
        mismatches = [case_id for case_id in sorted(module_states) if ledger_states[case_id] != module_states[case_id]]
        if mismatches:
            emit(errors, f"审计台账状态不一致：{', '.join(mismatches)}")
        else:
            emit(passed, f"审计台账状态与 30 条模块索引一致")

    tsv = BADCASE_ROOT / "审计证据" / "候选线索逐条台账-2026-09-09.tsv"
    if not tsv.exists():
        emit(warnings, "逐条机械线索 TSV 尚未生成")
        return
    try:
        with tsv.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        if len(rows) != 908:
            emit(warnings, f"逐条机械线索 TSV 行数={len(rows)}，预期=908")
        elif sum(row.get("机械线索") != "无" for row in rows) != 287:
            emit(warnings, "逐条机械线索 TSV 的机械命中数不是 287")
        elif sum(row.get("深审编号", "").startswith("B") for row in rows) != 30:
            emit(warnings, "逐条机械线索 TSV 的深审样本数不是 30")
        else:
            emit(passed, "逐条机械线索 TSV 完整：908 行、287 条机械线索、30 条深审样本")
    except (OSError, csv.Error) as exc:
        emit(warnings, f"逐条机械线索 TSV 无法读取：{exc}")


def check_regression_items(warnings: list[str], passed: list[str]) -> None:
    text = REGRESSION_FILE.read_text(encoding="utf-8")
    ids: list[str] = []
    for line in text.splitlines():
        if not line.lstrip().startswith("| R-"):
            continue
        parts = markdown_parts(line)
        if len(parts) < 4:
            continue
        match = re.match(r"(R-[A-Za-z0-9-]+)", parts[0])
        if match:
            ids.append(match.group(1))
        state = parts[-1]
        if state not in REGRESSION_STATES and not state.startswith("已关闭") and not state.startswith("未通过"):
            emit(warnings, f"回归项 {parts[0]} 使用未登记状态：{state}")
        if "2026-08-19" in line and state in {"待跑", "证据不足", "阻断"}:
            emit(warnings, f"逾期或未闭合回归项：{parts[0]}（保留为 {state}，不可冒充通过）")
    duplicates = [key for key, count in Counter(ids).items() if count > 1]
    if duplicates:
        emit(warnings, f"回归编号重复：{', '.join(sorted(duplicates))}")
    else:
        emit(passed, f"回归编号唯一：{len(set(ids))} 条")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    passed: list[str] = []
    check_case_assets(errors, warnings, passed)
    check_pitfall_ids(errors, passed)
    check_links(errors, passed)
    check_active_hooks(errors, passed)
    check_versions(errors, passed)
    check_audit_ledger(errors, warnings, passed)
    check_regression_items(warnings, passed)

    print(f"范围：{PROJECT_ROOT}")
    for item in passed:
        print(f"[PASS] {item}")
    for item in warnings:
        print(f"[WARN] {item}")
    for item in errors:
        print(f"[FAIL] {item}")
    print(f"结果：PASS={len(passed)} WARN={len(warnings)} FAIL={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
