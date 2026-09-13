#!/bin/bash
# PreToolUse 危险命令窄黑名单：只匹配「命令起始或 ;/&&/||/| 之后」的真实命令，字符串/脚本内容中提到关键字不误拦
input=$(cat)
tmp=$(mktemp)
printf '%s' "$input" > "$tmp"
node -e '
const fs=require("fs");
const o=JSON.parse(fs.readFileSync(process.argv[1],"utf8"));
const ti=o.tool_input;let s="";
try{const obj=typeof ti==="object"?ti:JSON.parse(ti);s=obj.cmd||obj.command||obj.input||JSON.stringify(obj)}catch(e){s=typeof ti==="object"?JSON.stringify(ti):String(ti||"")}
const rules=[
  [/(^|[;&|])\s*rm\s+(-[a-zA-Z]*[rf][a-zA-Z]*\s+)?(\/|~)(\s|$)/m,"禁止递归删除根目录/家目录"],
  [/(^|[;&|])\s*sudo\s+(?!-n\b)/m,"禁止交互式 sudo 提权命令（sudo -n 只读查询放行）"],
  [/(^|[;&|])\s*(curl|wget)\s+[^|;]*\|\s*(sh|bash)\b/m,"禁止 curl/wget 管道执行 shell"],
  [/(^|[;&|])\s*git\s+reset\s+--hard/m,"禁止 git reset --hard（不可逆）"],
  [/(^|[;&|])\s*git\s+clean\s+-[a-zA-Z]*[dfx][a-zA-Z]*/m,"禁止 git clean 强制清理"],
  [/(^|[;&|])\s*mkfs(\.\S+)?\s/m,"禁止 mkfs 格式化文件系统（不可逆）"],
  [/(^|[;&|])\s*dd\b[^|;&]*\bof=\/dev\/(r?disk|sd[a-z]|nvme|mmcblk|hda|sda)/m,"禁止 dd 直接写块设备（of=/dev/disk* 等，不可逆）"],
  [/(^|[;&|])\s*:\s*\(\s*\)\s*\{/m,"禁止 fork bomb（:(){...}）"],
  [/(^|[;&|])\s*diskutil\s+(eraseDisk|eraseVolume|eraseDevice|zeroDisk)\b/m,"禁止 diskutil 抹盘（不可逆）"],
];
for(const [re,msg] of rules){if(re.test(s)){process.stderr.write("拦截："+msg+"\n");process.exit(2)}}
' "$tmp"
rc=$?
rm -f "$tmp"
if [ "$rc" -ne 0 ]; then exit "$rc"; fi
# 反循环闸门（默认 dry-run）：黑名单通过后再检查连续重试；只有显式 intercept 模式才以退出码 2 拦截
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
printf '%s' "$input" | bash "$SCRIPT_DIR/doom_loop.sh"
rc=$?
if [ "$rc" -eq 2 ]; then exit 2; fi
exit 0
