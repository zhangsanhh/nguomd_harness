#!/bin/bash
# nguomd_harness 一键安装
#
# 用法：
#   ./install.sh                    就地激活（在 harness 仓库内试用）
#   ./install.sh /path/to/project   安装到你自己的项目
#   ./install.sh --check            只做环境自检，不改任何文件
#
# 做的事：检查依赖 → 写入绝对路径 → 补执行权限 → 建运行时目录 → 自检拦截能力

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$SCRIPT_DIR"
CHECK_ONLY=0

while [ $# -gt 0 ]; do
  case "$1" in
    --check) CHECK_ONLY=1; shift ;;
    -h|--help)
      sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'
      exit 0 ;;
    -*) echo "未知参数：$1"; exit 1 ;;
    *) TARGET="$1"; shift ;;
  esac
done

pass() { printf '  \033[32m✓\033[0m %s\n' "$1"; }
warn() { printf '  \033[33m!\033[0m %s\n' "$1"; }
fail() { printf '  \033[31m✗\033[0m %s\n' "$1"; }

echo
echo "nguomd_harness 安装程序"
echo "目标目录：$TARGET"
echo

# ---------- 1. 依赖检查 ----------
echo "[1/5] 检查依赖"
missing=0

if command -v node >/dev/null 2>&1; then
  pass "node $(node -v)"
else
  fail "未找到 node —— 危险命令闸门与反循环监测依赖它"
  missing=1
fi

PY=""
for c in python3 /usr/bin/python3 /usr/local/bin/python3; do
  if command -v "$c" >/dev/null 2>&1; then PY="$(command -v "$c")"; break; fi
done
if [ -n "$PY" ]; then
  pass "python $PY"
else
  fail "未找到 python3 —— 会话归档与表达优化钩子依赖它"
  missing=1
fi

if [ "$missing" = "1" ]; then
  echo
  echo "依赖不全，先装齐再运行。macOS 可用：brew install node python3"
  exit 1
fi

# ---------- 2. 复制到目标目录（非就地时） ----------
if [ "$TARGET" != "$SCRIPT_DIR" ]; then
  echo
  echo "[2/5] 复制文件到目标目录"
  mkdir -p "$TARGET"
  for item in AGENTS.md AGENTS版本变更.md 回归集.md .codex 提示词库 BadCase库 人机协作的迭代史; do
    [ -e "$SCRIPT_DIR/$item" ] || continue
    if [ -e "$TARGET/$item" ]; then
      cp -R "$SCRIPT_DIR/$item" "$TARGET/${item}.harness-new"
      warn "$item 已存在，未覆盖；新版放在 ${item}.harness-new，请自行合并"
    else
      cp -R "$SCRIPT_DIR/$item" "$TARGET/$item"
      pass "$item"
    fi
  done
else
  echo
  echo "[2/5] 就地激活，跳过复制"
fi

HOOKS="$TARGET/.codex/hooks.json"
[ -f "$HOOKS" ] || { fail "找不到 $HOOKS"; exit 1; }

# ---------- 3. 写入绝对路径 ----------
echo
echo "[3/5] 写入绝对路径并补执行权限"
if [ "$CHECK_ONLY" = "1" ]; then
  warn "--check 模式，跳过写入"
else
  if grep -q 'PROJECT_ROOT' "$HOOKS" 2>/dev/null; then
    cp "$HOOKS" "$HOOKS.bak-$(date '+%Y%m%d-%H%M%S')"
  fi
  "$PY" - "$HOOKS" "$TARGET" <<'PYEOF'
import json, sys, pathlib
hooks_path, target = sys.argv[1], sys.argv[2]
p = pathlib.Path(hooks_path)
data = json.loads(p.read_text(encoding="utf-8"))

def fix(v):
    if isinstance(v, str):
        if v.startswith('"'):                      # 形如 "…/x.sh"
            return '"' + fix(v[1:-1]) + '"'
        if v.startswith('/usr/bin/python3') or v.startswith('python3'):
            rest = v.split(' ', 1)[1] if ' ' in v else ''
            return f'{sys.executable} {fix(rest)}'.strip()
        return v.replace('$PROJECT_ROOT', target)
    if isinstance(v, list):
        return [fix(i) for i in v]
    if isinstance(v, dict):
        return {k: fix(x) for k, x in v.items()}
    return v

p.write_text(json.dumps(fix(data), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PYEOF
  pass "hooks.json 路径已指向 $TARGET"

  chmod +x "$TARGET/.codex/"*.sh 2>/dev/null || true
  pass "钩子脚本已补执行权限"

  mkdir -p "$TARGET/会话日志与摘要/交接文件" "$TARGET/会话日志与摘要/修改清单"
  pass "运行时目录已创建"
fi

# ---------- 4. 自检 ----------
echo
echo "[4/5] 自检"
ok=1

if out=$("$TARGET/.codex/inject_time.sh" 2>&1); then
  pass "时间注入正常：$(echo "$out" | sed -n '2p' | sed 's/^- //')"
else
  fail "时间注入脚本执行失败"; ok=0
fi

if printf '%s' '{"tool_input":{"cmd":"ls -la"},"session_id":"selftest"}' | "$TARGET/.codex/pre_tool_use_gate.sh" >/dev/null 2>&1; then
  pass "正常命令放行"
else
  fail "正常命令被误拦"; ok=0
fi

if printf '%s' '{"tool_input":{"cmd":"rm -rf /"},"session_id":"selftest"}' | "$TARGET/.codex/pre_tool_use_gate.sh" >/dev/null 2>&1; then
  fail "危险命令未被拦截 —— 闸门失效"; ok=0
else
  pass "危险命令已拦截"
fi

if [ "$ok" = "1" ]; then
  pass "闸门工作正常"
else
  warn "自检未全通过，请查看上方 ✗ 项"
fi

# ---------- 5. 后续步骤 ----------
echo
echo "[5/5] 还差一步：让客户端加载钩子"
cat <<EOF

  这套钩子按 Codex 的 .codex/hooks.json 格式声明。
  在 Codex 里打开 Hooks 设置页，确认信任本项目的钩子即可生效
  （信任按文件内容哈希绑定，改过 hooks.json 后需重新确认）。

  其他客户端只要能执行命令式钩子，也能接：把 hooks.json 里
  8 条 command 按其格式重新声明一遍即可，脚本本身不用改。

  日常维护：
    ./install.sh --check          复查环境与闸门
    git checkout .codex/hooks.json   还原就地激活写入的绝对路径

EOF
