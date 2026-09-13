# Hook 会话注入最小示例（SessionStart）

> 定位：最小可用的 SessionStart 注入方案，只注入动态信息（实时时间），静态规则交给 AGENTS.md，不重复、不占多余 token。
> 使用原则：本示例只放项目内供查看与自测，未写入 ~/.codex，不修改全局配置。
> 部署状态：2026-08-03 已在本项目启用时间注入、日记工作流、压缩快照、修改记录和危险命令闸门；2026-08-28 新增普通提问表达优化与双来源会话归档（项目级 `.codex/hooks.json`：UserPromptSubmit 每轮时间注入 `.codex/inject_time.sh` + 日记工作流触发 `.codex/diary_workflow_trigger.sh` + 普通提问表达优化 `.codex/expression_optimizer_trigger.py` + 用户消息归档 `.codex/archive_user_prompt.py` + Stop 会话归档 `.codex/archive_turn.py` + PreCompact 压缩快照 `.codex/pre_compact.sh` + PostToolUse 修改记录 `.codex/post_tool_use.sh` + PreToolUse 危险命令窄黑名单 `.codex/pre_tool_use_gate.sh`）；新增或修改钩子需在 App Hook 管理界面确认信任后生效。实际部署已用 UserPromptSubmit 替代 SessionStart（每轮刷新时间、覆盖首条消息），本文件仍保留 SessionStart 作最小示例说明。
> 格式状态：已于 2026-08-28 按 OpenAI 官方 Hooks 文档复核 `UserPromptSubmit`、`Stop`、`additionalContext` 和信任机制；官方文档当前可访问，正式启用前仍需以当前版本行为为准。

## 一、注入内容（最终版）

```
会话注入：
- 当前时间：{实时获取，北京时间}
- 时间规则：以当前时间为基准，不沿用/引用训练截止日期作为默认值。
```

## 二、脚本示例（session_start.sh）

```bash
#!/bin/bash
# 会话开始时的注入脚本：只输出动态信息，无副作用（不写文件、不联网）
echo "会话注入："
echo "- 当前时间：$(TZ='Asia/Shanghai' date '+%Y-%m-%d %H:%M')（北京时间）"
echo "- 时间规则：以当前时间为基准，不沿用/引用训练截止日期作为默认值。"
```

说明：

1. `TZ='Asia/Shanghai'` 强制取北京时间，不依赖系统时区；
2. 脚本只 echo，不写文件、不访问网络，属于低风险注入；
3. 注入内容保持两行，静态规则（AGENTS.md 已有）一律不重复。

## 三、hooks.json 官方格式（已核验）

```json
{
  "description": "会话注入：实时北京时间 + 时间规则",
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/绝对路径/session_start.sh",
            "timeout": 10,
            "statusMessage": "注入实时时间"
          }
        ]
      }
    ]
  }
}
```

字段说明（逐项对照官方源码）：

1. 事件名是 PascalCase 的 `"SessionStart"`（不是 `session_start`），共 11 个事件：`PreToolUse`、`PermissionRequest`、`PostToolUse`、`PreCompact`、`PostCompact`、`SessionStart`、`SessionEnd`、`UserPromptSubmit`、`SubagentStart`、`SubagentStop`、`Stop`；
2. 每个事件的值是「匹配组」数组，每组含可选 `matcher` 与必填 `hooks`；`matcher` 省略/空/`"*"` 匹配全部，纯字母数字或 `|` 分隔为精确匹配（如 `"Edit|Write"`），其余按正则；`UserPromptSubmit` 与 `Stop` 忽略 matcher；
3. 处理器是 `{"type": "command", "command": "..."}`：`command` 为字符串（脚本绝对路径），`timeout` 为秒（省略默认 600 秒；`SessionEnd` 默认 1 秒、上限 3 秒），另有可选 `commandWindows`、`async`、`statusMessage`、`additionalContextLimit`（默认 2500 token 阈值）；
4. `type` 目前只有 `command` 真正执行；`prompt`、`agent` 两种类型源码里能解析但运行时会跳过并告警「not supported yet」，不要用；
5. 顶层 `description` 可选；脚本路径需替换为实际绝对路径。

配置文件位置（三处均可，等价）：

- 项目级：`<项目根>/.codex/hooks.json`（推荐，不动全局；本工作区当前使用该配置文件）；
- 用户级：`~/.codex/hooks.json`；
- 也可写进对应层的 `config.toml` 的 `[hooks]` 表，TOML 写法为 `[[SessionStart]]` + `[[SessionStart.hooks]]` 数组。

运行时协议（SessionStart）：

- stdin 收到一个 JSON 对象，字段含 `cwd`、`hook_event_name`、`model`、`permission_mode`、`session_id`、`source`、`transcript_path` 等；
- stdout 纯文本（非 JSON）会直接作为注入上下文——本示例脚本只 echo 两行即属于此路径；输出合法 JSON 也可结构化指定 `hookSpecificOutput.additionalContext`、`continue`、`systemMessage` 等；输出长得像 JSON 但解析失败会判 hook 失败；空输出不注入。

信任机制：用户级/项目级属「非托管 hook」，放置后需在 Codex 的 Hook 管理界面确认信任（trusted_hash 匹配）后才会真正执行；企业托管 hook 自动放行。

## 四、启用前检查清单

1. 脚本只输出文本，无写入、删除、网络操作；
2. 注入内容仅两行，未夹带 AGENTS.md 已有规则；
3. 未修改全局配置（本示例仅项目内文档）；
4. 启用前先自测脚本输出，确认时间格式正确；
5. 把 hooks.json 放到项目 `.codex/` 后，先在 App 的 Hook 管理界面确认信任，再开始首个会话验证注入是否生效。
