# .codex（项目级钩子与脚本）

> 本目录保存项目级 hooks 与脚本。脚本以 `$PROJECT_ROOT` 或脚本自身位置解析路径，可直接移植到其他项目。
> 使用前请把 `.codex/hooks.json` 里的 `$PROJECT_ROOT` 替换为实际项目路径，并在客户端钩子管理界面重新确认信任。

## 文件与事件

| 文件 | 事件 | 行为 |
| --- | --- | --- |
| `hooks.json` | 全部 | 5 组事件钩子声明：时间注入、工作流触发、表达优化、用户消息保存、压缩快照、修改留痕、危险命令闸门 |
| `inject_time.sh` | UserPromptSubmit | 每轮注入北京时间与时间规则两行，无副作用 |
| `diary_workflow_trigger.sh` | UserPromptSubmit | 命中标准触发语或长篇日记产出请求后注入处理流程 |
| `expression_optimizer_trigger.py` | UserPromptSubmit | 普通提问且非引用占多数时注入轻量表达优化规则 |
| `archive_user_prompt.py` | UserPromptSubmit | 立即保存当前用户消息，供归档脚本配对；无 stdout、无模型调用 |
| `archive_turn.py` | Stop | 保存助手可见回复并更新索引 |
| `conversation_archive_common.py` | 由归档脚本调用 | 提供本地时间、引用占比、长度校验、并发追加和索引调用等共享逻辑 |
| `pre_compact.sh` | PreCompact | 压缩前机械写交接快照至 `会话日志与摘要/交接文件/` |
| `post_tool_use.sh` | PostToolUse（apply_patch/Edit/Write） | 写操作后追加一行修改记录至 `会话日志与摘要/修改清单/` |
| `pre_tool_use_gate.sh` | PreToolUse（exec_command/Shell） | 危险命令窄黑名单（9 条），随后调用 `doom_loop.sh` |
| `doom_loop.sh` | 由 pre_tool_use_gate 调用 | 反循环闸门：25 秒窗口内同一命令连续 3 次记事件，当前为 dry-run 不拦截 |
| `config.toml` | — | 项目级模型与压缩参数示例，不含任何凭据 |

## 钩子计数与信任边界

1. 客户端设置页按配置组显示数量，不按组内命令处理器数量显示。本项目实际为 5 组、8 个命令处理器。
2. 截图里的钩子计数可能来自其他目录的配置文件，不能用来判断本项目的处理器数量是否减少。
3. 修改 `hooks.json` 后须重新确认信任；信任按文件内容哈希绑定，配置项见全局 `~/.codex/config.toml` 的 `hooks.state`。

## 变更纪律

1. 脚本修改前先备份 `.bak-时间戳`；改后用 `bash -n` 与模拟场景验证，再按正常节奏运行。
2. 新增钩子必须通过哈希信任确认，避免未审计脚本自动执行。
3. 脚本只输出文本，不写文件、不联网，保持无副作用。

## 会话归档边界

1. 归档只覆盖当前项目；每轮保存用户可见的用户消息和助手回复，不保存思维链、系统提示词或工具原始输出。
2. 表达优化内容一般不超过 250 字，写入 `会话日志与摘要/口语化表达/` 下按日期命名的文件。
3. 临时归档目录已加入 `.gitignore`；生成的 Markdown 与 HTML 作为可阅读备份。
4. 归档过程不把历史记录重新注入模型；表达建议由当前回复产生，归档脚本只做提取、保存和页面生成。
