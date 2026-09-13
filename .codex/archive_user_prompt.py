#!/usr/bin/env python3
"""UserPromptSubmit：立即保存当前用户消息，等待 Stop 钩子配对助手回复。"""

from __future__ import annotations

import sys

from conversation_archive_common import (
    date_from_iso,
    load_event,
    now_iso,
    pending_root,
    prompt_key,
    safe_part,
    write_json_atomic,
)


def main() -> None:
    try:
        event = load_event()
        prompt = event.get("prompt", "")
        if not isinstance(prompt, str) or not prompt.strip():
            return

        submitted_at = now_iso()
        session_id = str(event.get("session_id") or "unknown")
        turn_id = str(event.get("turn_id") or "")
        key = prompt_key(session_id, turn_id, prompt)
        record = {
            "version": 1,
            "session_id": session_id,
            "turn_id": turn_id,
            "record_key": key,
            "submitted_at": submitted_at,
            "date": date_from_iso(submitted_at),
            "cwd": str(event.get("cwd") or ""),
            "model": str(event.get("model") or ""),
            "prompt": prompt,
        }
        target = pending_root() / f"{safe_part(key)}.json"
        write_json_atomic(target, record)
    except Exception as exc:  # 归档失败不得阻断用户正常提问
        print(f"conversation archive capture skipped: {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
