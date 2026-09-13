#!/usr/bin/env python3
"""UserPromptSubmit：仅在普通提问适合时注入轻量表达优化规则。"""

from __future__ import annotations

import json
import sys

from conversation_archive_common import (
    compact_char_count,
    is_diary_trigger,
    is_quote_dominant,
    load_event,
    split_quoted_text,
)


CONTEXT = """普通提问表达优化已启用。只分析本轮用户自己写的提问或说明，不改写引用、文件粘贴、代码和逐字材料；若引用内容占多数，跳过本区块。回答正文中在固定页脚之前增加标题“### 本次提问表达优化”，内容不超过250字：给出一版更清楚的正确表述和一句修改说明；优化表述按去除空格和换行后的Unicode字符数控制在原始自写内容的40%—110%，不改变原意、不增加外部事实。若没有明显问题，优化表述可保留原句，并说明“无需明显调整”。"""


def main() -> None:
    try:
        event = load_event()
        prompt = event.get("prompt", "")
        if not isinstance(prompt, str) or not prompt.strip():
            return
        if is_diary_trigger(prompt) or is_quote_dominant(prompt):
            return

        own_text, _, _ = split_quoted_text(prompt)
        if compact_char_count(own_text) == 0:
            return

        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "UserPromptSubmit",
                        "additionalContext": CONTEXT,
                    }
                },
                ensure_ascii=False,
            )
        )
    except Exception as exc:  # 注入失败不得阻断用户正常提问
        print(f"expression optimization trigger skipped: {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
