#!/bin/bash
# PostToolUse：文件写操作后追加一行机械修改记录（只写文件，不向模型注入内容）
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
input=$(cat)
tmp=$(mktemp)
printf '%s' "$input" > "$tmp"
IFS=$'\t' read -r tool_name tool_use_id tool_input cwd <<< "$(node -e "const o=JSON.parse(require('fs').readFileSync(process.argv[1],'utf8'));const ti=(o.tool_input&&typeof o.tool_input==='object')?JSON.stringify(o.tool_input):String(o.tool_input||'');process.stdout.write([o.tool_name||'',o.tool_use_id||'',ti,o.cwd||''].join(String.fromCharCode(9)))" "$tmp")"
rm -f "$tmp"

base="$PROJECT_ROOT/会话日志与摘要/修改清单"
mkdir -p "$base"
day=$(TZ='Asia/Shanghai' date '+%Y-%m-%d')
hhmm=$(TZ='Asia/Shanghai' date '+%H:%M')
file="$base/$day.md"

if [ ! -f "$file" ]; then
  echo "# 修改清单：$day" > "$file"
  echo >> "$file"
  echo "| 时间 | 操作 | 文件 |" >> "$file"
  echo "| --- | --- | --- |" >> "$file"
fi

# 从 apply_patch 输入文本提取文件路径（JSON 字符串内路径后是 \n 转义或引号）
files=$(printf '%s' "$tool_input" | grep -oE '\*\*\* (Update|Add|Delete|Move to) File: [^"\\]+' | sed -E 's/^\*\*\* (Update|Add|Delete|Move to) File: //' | sort -u | tr '\n' ';')
if [ -z "$files" ]; then files="(未提取到路径)"; fi

# 表内竖线转全角，避免破坏 Markdown 表格
files=$(printf '%s' "$files" | tr '|' '｜')
tool=$(printf '%s' "$tool_name" | tr '|' '｜')
printf '| %s | %s | %s |\n' "$hhmm" "$tool" "$files" >> "$file"
exit 0
