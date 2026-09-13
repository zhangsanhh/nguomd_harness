#!/bin/bash
# PreCompact：压缩开始前机械写交接快照（只写文件 + 输出一条系统消息，不做内容总结）
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
input=$(cat)
tmp=$(mktemp)
printf '%s' "$input" > "$tmp"
IFS=$'\t' read -r sid tp cwd <<< "$(node -e "const o=JSON.parse(require('fs').readFileSync(process.argv[1],'utf8'));process.stdout.write([o.session_id||'',o.transcript_path||'',o.cwd||''].join(String.fromCharCode(9)))" "$tmp")"
rm -f "$tmp"

base="$PROJECT_ROOT/会话日志与摘要/交接文件"
mkdir -p "$base"

stamp=$(TZ='Asia/Shanghai' date '+%Y-%m-%d %H:%M')
day=$(TZ='Asia/Shanghai' date '+%Y-%m-%d')
logfile="$PROJECT_ROOT/会话日志与摘要/$day/会话摘要.md"
if [ -f "$logfile" ]; then count=$(grep -c '^| 2026' "$logfile"); else count=0; fi

out="$base/precompact-$day-$(TZ='Asia/Shanghai' date '+%H%M%S')-$sid.md"
{
  echo "# PreCompact 交接快照"
  echo
  echo "- 时间：${stamp}（北京时间）"
  echo "- 会话 ID：$sid"
  echo "- 工作目录：$cwd"
  echo "- 今日日志条数：$count"
  echo "- transcript：$tp"
  echo
  echo "用途：压缩后的审计基线；如需恢复关键路径/数字，先查本文件与本日会话摘要。"
} > "$out"

echo "{\"systemMessage\":\"PreCompact 交接快照已写入：$out\"}"
