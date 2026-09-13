# Codex 智能体工作原理与工程实践：万字总结

> 本文基于三份材料整合撰写：①《从 Codex 源码带你了解智能体的工作方式》（用户提供原文，下称「源码文」）；②阿里云开发者《Codex 实践系列 Vol.01：从跑通 CLI 开始，看懂 Codex 怎么工作》（2026-06-08）；③腾讯云开发者《Codex 使用最佳实践：把它当成工程队友，而不是代码生成器》（2026-05-27，正文经 CSDN 转载补全）。三份材料分别回答三个问题：智能体「内部怎么转」（①）、「第一次怎么上手」（②）、「长期怎么用才稳」（③）。

## 材料与核心命题

| 编号 | 材料 | 核心命题 |
| --- | --- | --- |
| ① | 源码文（Agent Loop、工具系统、六层安全、扩展能力） | 代码级拆解：循环怎么驱动、工具怎么组织、安全怎么保障、能力怎么扩展 |
| ② | 阿里云实践 Vol.01 | 从 CLI 安装到最小任务，观察 Codex 实际读了什么、跑了什么、改了什么 |
| ③ | 腾讯云最佳实践 | 把它当工程队友：给上下文→先计划→再执行→验证→沉淀 |

三份材料的重合点集中在「循环、工具、安全、上下文」四个主题：①是底层原理，②③是上层用法。第九章专门做重合点对照，第十章给出落地路线图。

## 一、Agent Loop：智能体的核心循环

### 1.1 一个请求的完整旅程

用户在终端输入「帮我把 src/main.rs 里的 TODO 注释清理掉」，请求会经历：

用户输入 → `Codex::submit()` → `submission_loop()` → `run_turn()` → [构建 Prompt → 调用 LLM → 解析响应 → 执行工具 → 结果送回 LLM → 循环] → Turn 结束

方括号里的部分就是 Agent Loop 的核心。它不是「调用一次 LLM 拿到答案」的单发过程，而是多轮循环：模型可能先调用工具查看文件内容，再决定怎么修改，然后调用另一个工具写入文件，最后给出完成回复。每一步工具调用的结果都会被送回模型，驱动下一轮决策。

### 1.2 入口：Codex 结构体与 Channel 通信

核心会话由 `Codex` 结构体管理（codex-rs/core/src/session/mod.rs:370）：

```rust
pub struct Codex {
    pub(crate) tx_sub: Sender<Submission>,      // 发送操作的有界通道（容量 512）
    pub(crate) rx_event: Receiver<Event>,       // 接收事件的无界通道
    pub(crate) agent_status: watch::Receiver<AgentStatus>,
    pub(crate) session: Arc<Session>,
    pub(crate) session_loop_termination: SessionLoopTermination,
}
```

关键设计：Codex 通过一对 Channel 与外部通信。`tx_sub` 是有界通道（容量 512），外部通过它发送指令（Submission），包括用户输入、审批响应、中断请求等；`rx_event` 是无界通道，核心通过它向外发送事件（Event），包括模型回复、工具执行状态、错误信息等。这种设计把 UI 层与核心逻辑完全解耦——TUI、headless 执行模式、App Server 等不同前端都可以通过同一对通道与核心交互。

用户输入时，前端调用 `Codex::submit()`（mod.rs:693），把 Op 包装成带 UUID 的 Submission 经 `tx_sub` 发送。

### 1.3 调度中心：submission_loop

初始化时，系统启动一个后台 Tokio 任务运行 `submission_loop()`（handlers.rs:733）。它不断从 `rx_sub` 接收 Submission，再按 Op 类型分发：`Op::UserTurn` / `UserInput` 走 `user_input_or_turn`；`Op::Interrupt` 走中断处理；`Op::ExecApproval` 走审批响应；`Op::Compact` 走压缩；`Op::Shutdown` 走关闭。Op 枚举定义了所有可能的操作类型。

这里需要解释 Turn（轮次）：指「从用户发出一条消息开始，到模型完成所有工具调用并给出最终回复为止」的完整交互周期。一个 Turn 内部可能包含多轮 LLM 调用和工具执行（这就是 Agent Loop），但从用户视角看，他只发了一条消息、收到一个完整回复。

### 1.4 Turn 启动：user_input_or_turn 与 RegularTask

`user_input_or_turn()`（handlers.rs:99）做两件事：从 Op 中提取用户输入与配置更新（模型、审批策略、沙箱策略等），创建新的 Turn 上下文；尝试把输入「引导」到已在运行的 Turn（steer_input）。若当前没有活跃 Turn，就创建 RegularTask。

`RegularTask::run()`（tasks/regular.rs:40）先发送 TurnStarted 事件，然后进入外层循环：

```rust
let mut next_input = input;
loop {
    let last_agent_message = run_turn(...).await;
    if !sess.has_pending_input().await {
        return last_agent_message;
    }
    next_input = Vec::new();
}
```

这个外层 loop 处理 Turn 内连续轮次：如果一个 Turn 执行完毕又有新的用户输入进来（比如模型运行时用户又发消息），就用空输入继续调用 run_turn。

### 1.5 核心循环：run_turn

`run_turn()`（turn.rs:141）是 Agent Loop 的心脏。函数注释写得很清楚：接收用户消息，进入循环；每次采样请求，模型要么返回函数调用请求，要么返回纯文本回复；函数调用就执行并把输出送回模型继续循环；纯文本则记录并结束 Turn。

run_turn 分两个阶段：

阶段一（准备工作）：预采样压缩检查（`run_pre_sampling_compact`，Token 接近上限先压缩腾空间）；构建工具路由 ToolRouter（收集内置工具、MCP 工具、扩展工具）；加载 Skill 与插件；运行 `session_start` 和 `user_prompt_submit` Hook；把用户输入写入对话历史。

阶段二（主循环，turn.rs:387 起）：

Step 1：获取完整对话历史，按模型输入模态裁剪后作为采样输入。

Step 2：`run_sampling_request` 通过 ModelClientSession 向 LLM 发送请求（WebSocket 或 HTTPS/SSE 流式）。

Step 3：处理返回的 `SamplingRequestResult { needs_follow_up, last_agent_message }`。`needs_follow_up == true`（模型发起了工具调用）就继续循环；为 false（纯文本）就跳出循环，Turn 结束。

Step 4：Token 超限检查：`total_usage_tokens >= auto_compact_limit` 且仍需跟随时，执行自动压缩（`run_auto_compact`）后 continue。

### 1.6 模型调用：run_sampling_request 的重试与降级

`run_sampling_request()`（turn.rs:1013）内部有重试循环：构建 Prompt → `try_run_sampling_request` → 成功则返回；`ContextWindowExceeded` 等错误不可重试；可重试错误按指数退避（`backoff(retries)`）等待后重试；重试次数用尽时尝试把传输方式从 WebSocket 降级到 HTTPS/SSE。

三个值得注意的设计：双传输通道（优先 WebSocket 低延迟，失败自动降级）；指数退避（避免服务端出问题时疯狂重试）；错误分类（流断开等可重试，上下文超限、用量上限不可重试）。

### 1.7 流式响应处理

`try_run_sampling_request()`（turn.rs:1840）打开流后进入事件循环：`OutputItemAdded`（新输出项开始）、`OutputTextDelta`（流式文本增量实时推给 UI）、`OutputItemDone`（工具调用则派发执行并置 needs_follow_up；消息则记录进历史）、`Completed`（记录 Token 用量，返回结果）。

`handle_output_item_done`（stream_events_utils.rs:342）是工具调度入口：通过 `ToolRouter::build_tool_call()` 判断输出项是否为工具调用。是则创建异步 Future，经 ToolCallRuntime 分发执行；不是则作为普通助手消息记录。

### 1.8 并行工具执行

模型一次响应可能返回多个工具调用。`ToolCallRuntime`（parallel.rs:27）用一把 `RwLock` 控制并发：支持并行的工具获取读锁（多读锁可同时持有，多个工具并行运行）；不支持并行的工具获取写锁（排他，必须等其他工具执行完）。每个工具调用被 `tokio::spawn` 为独立异步任务，并通过 `tokio::select!` 监听取消令牌——用户中断时返回 aborted 响应。所有 Future 收集到 FuturesOrdered 队列，按完成顺序处理。

### 1.9 上下文管理：自动压缩

复杂任务中对话历史不断增长。压缩触发条件（turn.rs:498）：Token 总量达到 `auto_compact_limit`（由模型上下文窗口决定）且仍需跟随时，在循环中插入一次压缩。压缩的本质是让模型把旧对话总结成更简洁的表示，用总结替代原始记录，释放 Token 空间，从而保证长任务可持续执行。

### 1.10 小结（人话版）

Agent Loop 一句话：LLM 决策 → 工具执行 → 结果反馈 → LLM 继续决策，直到任务完成。四个特征：LLM 是决策中心（返回 FunctionCall 就执行工具，返回纯文本就结束）；工具是执行手臂（模型本身不能读写文件、执行命令，靠工具间接操控外部世界）；对话历史是状态（所有输入、回复、工具调用与结果都被记录，作为下一轮决策依据）；循环受安全约束且有终止条件（自然结束、Token 超限且无法压缩、用户中断）。

### 1.11 一个完整的工具调用回合（示例）

假设模型收到「统计这个项目有多少个源文件」：第一轮采样，模型返回 FunctionCall 调用 shell，参数是 `{"command": "find src -name '*.rs' | wc -l", "workdir": "my-project"}`。系统经 ToolRouter 识别、dispatch_any 派发，Orchestrator 检查审批策略（在 workspace 权限下这类只读命令通常 Skip），沙箱内执行，返回 JSON（output 为数字、exit_code 0、耗时）。结果写入对话历史。第二轮采样，模型看到输出后，可能再调 shell 验证文件类型分布，也可能直接给出文本结论；若直接给文本，needs_follow_up 为 false，Turn 结束。整个过程对用户只表现为「发了一条消息、收到一个回答」，内部可能已经完成多次工具往返。这就是源码里 needs_follow_up 标记的实际意义。

## 二、工具系统：智能体如何与外部世界交互

### 2.1 工具的本质

LLM 本身只是文本生成模型，不能读文件、跑命令、调 API。工具就是赋予它「行动能力」的桥梁：每次调用 LLM 时，系统把所有可用工具的定义（名称、描述、参数格式）一起发给模型；模型决定调用哪个工具、传什么参数；系统找到对应 Handler 执行；结果格式化后送回模型。模型是「调用方」，工具是「被调用的函数」，只不过执行发生在真实环境中。

### 2.2 定义与注册：ToolName、ToolSpec、ToolRegistry

每个工具都有 ToolSpec 定义。工具名由 `ToolName` 表示：

```rust
pub struct ToolName {
    pub namespace: Option<String>,  // 命名空间，如 "container"
    pub name: String,               // 工具名，如 "exec"
}
```

namespace 可选：内置 shell 没有命名空间，container.exec 的命名空间是 container。这种设计让不同来源的工具（内置、MCP、扩展）共存而不冲突。

所有工具注册进 `ToolRegistry`（本质是 `HashMap<ToolName, Arc<dyn CoreToolRuntime>>`，registry.rs:244）。`CoreToolRuntime` trait（registry.rs:41）在基础 ToolExecutor 之上扩展了 search_info（工具搜索）、matches_kind、telemetry_tags（埋点）、pre/post_tool_use_payload（给 Hook 系统暴露信息）、with_updated_hook_input、create_diff_consumer 等能力。

注册发生在 `build_tool_router()`（spec_plan.rs:92）：`collect_tool_executors()` 实例化所有内置 Handler。常见内置工具：

| 工具名 | Handler | 作用 |
| --- | --- | --- |
| shell | ShellCommandHandler | 执行 Shell 命令 |
| apply_patch | ApplyPatchHandler | 对文件应用 diff 补丁 |
| container.exec | ExecCommandHandler | 后台终端执行 |
| mcp | McpHandler | 调用 MCP 服务器工具 |
| tool_search | ToolSearchHandler | 搜索可用工具 |
| plan | PlanHandler | 结构化规划 |
| request_user_input | RequestUserInputHandler | 向用户提问 |
| view_image | ViewImageHandler | 查看图片 |
| multi_agents | SpawnAgentHandler 等 | 多智能体协作 |

MCP 工具经 McpConnectionManager 从外部服务器发现获取，扩展工具经 ExtensionRegistry 的 tool_contributors() 获取。

### 2.3 路由：ToolRouter

ToolRouter（router.rs:34）是「模型响应」与「工具执行」的桥梁，由注册表 + 模型可见工具定义列表组成。两个核心职责：`model_visible_specs()` 返回发给模型的工具定义列表；`build_tool_call()`（router.rs:77）解析模型返回的 ResponseItem——FunctionCall、ToolSearchCall、CustomToolCall 统一转换为内部 ToolCall（工具名、调用 ID、参数载荷）；普通消息返回 None，进入历史记录分支。

### 2.4 派发：dispatch_any 的五步

`ToolRegistry::dispatch_any()`（registry.rs:305）是工具执行总入口：

Step 1：活跃 Turn 工具调用计数（记录每个 Turn 执行了多少工具调用）。

Step 2：按工具名查找；找不到返回 `FunctionCallError::RespondToModel`——错误消息写入对话历史，模型可以看到并调整策略。

Step 3：运行 pre-tool-use Hook：放行（Continue，无修改）、修改输入（Continue 带 updated_input）、拦截（Blocked，返回消息给模型）。

Step 4：`handle_any_tool` 调用具体工具的 handle() 执行实际逻辑。

Step 5：运行 post-tool-use Hook：可检查结果、修改输出，甚至阻止结果返回模型。

### 2.5 两个具体工具：shell 与 apply_patch

shell 是最常用工具。模型传入类似 `{"command": "ls -la src/", "workdir": "my-project"}` 的参数，Handler 解析参数后经 ToolOrchestrator 走审批与沙箱流程，在沙箱中执行，捕获 stdout/stderr 和退出码，返回结构化 JSON：

```json
{"output": "file1.rs\nfile2.rs\n", "metadata": {"exit_code": 0, "duration_seconds": 0.3}}
```

apply_patch 让模型修改文件，参数是 unified diff 格式：

```
*** Begin Patch
*** Update File: src/main.rs
- let x = 1;
+ let x = 2;
*** End Patch
```

流程：解析 diff → 检查路径是否在允许写入范围 → 应用补丁 → 返回变更结果。它支持流式参数解析：模型流式生成 diff 时，ApplyPatchArgumentDiffConsumer 实时解析并推给 UI，用户能看到「正在修改什么」。

### 2.6 编排器：审批 → 沙箱 → 执行 → 重试

`ToolOrchestrator`（orchestrator.rs:42）的 run() 实现四阶段：审批检查（Skip 自动放行 / Forbidden 直接拒绝 / NeedsApproval 请求用户或 Guardian 审批；结果缓存于 ApprovalStore，「批准并记住」后同命令不再询问）；选择沙箱（`select_initial` 依据文件系统策略、网络策略、工具偏好等）；沙箱内执行；若沙箱拒绝且工具支持 `escalate_on_failure`，请求用户批准「无沙箱执行」后用 SandboxType::None 重试。这是安全的降级路径：默认沙箱内执行，沙箱拒绝才请求更高权限。

### 2.7 结果格式化与截断

Shell 结果经 `format_exec_output_for_model_structured()` 转 JSON（output + metadata）；MCP 结果经 McpToolOutput 包装。所有工具结果统一转为 FunctionCallOutput 写入对话历史，供下一轮决策。超大输出按 TruncationPolicy 截断，避免撑爆上下文。

### 2.8 小结（人话版）

工具系统是清晰的分层架构：Router 负责路由、Runtime 负责并发、Registry 负责派发与 Hook、Orchestrator 负责安全编排、Handler 负责实际逻辑。好处：新增工具只实现一个 Handler 并注册，其他层不用改；改安全策略只调 Orchestrator；加全局行为用 Hook 在 Registry 层拦截。

### 2.9 一次工具调用的完整调用链

把 2.3 到 2.7 串起来看：模型返回 `ResponseItem::FunctionCall` → `build_tool_call` 转换为 ToolCall（含工具名、call_id、参数）→ `dispatch_any` 计数并查注册表 → 命中后跑 pre-tool-use Hook（可拦截或改写）→ `handle_any_tool` 进入 Orchestrator（审批三态 → 沙箱选择 → 执行 → 失败升级）→ Handler 实际执行（shell 捕获输出与退出码，apply_patch 校验路径后落盘）→ post-tool-use Hook 检查结果 → 格式化写入历史 → 模型下一轮决策。任一层都可能提前终止：Hook 拦截返回消息给模型，审批 Forbidden 直接报错，沙箱拒绝且不允许升级则失败。这条链路解释了为什么「工具执行」在源码里不是一个简单函数调用，而是一整套可观察、可干预、可审计的流程。

## 三、六层安全机制：给智能体套上缰绳

能执行任意 Shell 命令的智能体，本质是拥有你电脑权限的程序，可能删除重要文件、执行 `rm -rf /`、外传敏感数据、安装恶意软件。Codex 的安全模型不是事后补救，而是在每次工具执行前多层拦截。

### 3.1 第一层：权限配置（Permission Profile）

内置三个配置（config/permissions.rs:42）：

`:read_only`（默认）：只能读文件，不能写入，不能访问网络。最安全，适合初次使用或不信任的项目。

`:workspace`：允许在项目目录内写入，允许访问 `~/.codex/memories`；网络默认受限但可配置。开发场景常用。

`:danger_full_access`：完全放开文件系统与网络。只在完全信任智能体时使用。

还可自定义权限配置，精确控制可读路径、可写路径、可访问域名。权限配置决定沙箱选择：read-only / workspace 触发平台沙箱，danger-full-access 跳过沙箱。

### 3.2 第二层：平台沙箱（Platform Sandbox）

平台沙箱是操作系统级隔离，在工具执行时包裹子进程，限制文件系统与网络访问。三种平台实现：

macOS Seatbelt：用 `/usr/bin/sandbox-exec`，SBPL 策略动态生成，限制子进程可访问的路径与网络；路径硬编码防止 PATH 注入恶意版本。

Linux Landlock + seccomp + bubblewrap：Landlock 限制目录访问、seccomp 过滤系统调用、bwrap 提供命名空间隔离；由独立可执行文件 codex-linux-sandbox 实现，权限配置序列化为 JSON 传入；不支持 WSL1。

Windows Restricted Token：用受限令牌限制进程特权级别与可访问资源。

`SandboxManager::transform()`（manager.rs:168）把原始命令包装成沙箱化命令。

### 3.3 第三层：执行策略（Exec Policy）

平台沙箱限制「能访问什么资源」，执行策略补充「命令本身允不允许」。`.rules` 文件（配置目录 rules/ 子目录）定义命令前缀与决策：`Allow` 放行、`Prompt` 询问、`Forbidden` 拒绝。未命中规则时用启发式：已知安全命令（git status、ls、cat）自动放行；可能危险的命令（rm、chmod）询问；被禁止前缀（sudo）直接拒绝。

系统维护禁止建议列表（BANNED_PREFIX_SUGGESTIONS），防止模型建议过宽规则——比如不能建议「允许所有 python3 命令」，因为 `python3 -c "import os; os.system('rm -rf /')"` 很危险。用户批准命令时可生成 ExecPolicyAmendment，把决策持久化到 default.rules。

### 3.4 第四层：审批系统（Approval System）

审批策略由 AskForApproval 枚举定义：

Never：从不询问，完全依赖沙箱与执行策略，沙箱拒绝直接报错。

OnFailure：先在沙箱内尝试，沙箱拒绝后再询问是否无沙箱执行。

OnRequest：按执行策略判断，Allow 直接执行，Prompt 才询问。

UnlessTrusted：除已知安全列表外都询问（最严格）。

Granular：细粒度分别控制沙箱审批、规则审批、MCP 审批等。

审批结果缓存在 `ApprovalStore`（sandboxing.rs:39）；「批准并记住」（ApprovedForSession）后，相同命令不再询问。

### 3.5 第五层：Guardian 自动审查

Guardian 是「用 AI 审查 AI」的设计：审批策略为 OnRequest 或 Granular 且配置 `approvals_reviewer = "auto"` 时，审批请求不弹窗，而是路由给独立 Guardian 审查会话。它从当前对话提取用户意图与最近工具调用历史，构建压缩摘要，返回 JSON 结构化评估：risk_level（low/medium/high/critical）、user_authorization、outcome（approve/deny）、rationale（决策理由）。

关键原则：失败即拒绝（Fail Closed）——Guardian 超时（90 秒）、执行失败、输出无法解析，一律视为拒绝，宁可误拦不可误放。另有熔断器：一个 Turn 内连续拒绝 3 次，或最近 50 次审查中拒绝 10 次，就中断整个 Turn，防止模型反复尝试被拒操作。

### 3.6 第六层：网络访问控制

网络代理基于白名单：只允许列表内域名。工具需要网络访问时走 tools/network_approval 流程：先查会话级已拒绝主机缓存（命中直接拦截）、已批准主机缓存（命中直接放行）；未命中则创建审批请求路由到用户或 Guardian；批准/拒绝决策可持久化为 .rules 网络规则。

### 3.7 一次工具执行的多层拦截

以 `rm -rf /tmp/old_builds` 为例：权限配置判定能否执行 → 平台沙箱包裹进程 → 执行策略匹配规则 → 需要时弹审批（用户或 Guardian）→ 涉及外联则过网络白名单 → 沙箱拒绝则按策略请求无沙箱重试。整个流程保证：默认安全（没有明确批准不执行）、最小权限（批准了也在沙箱内）、渐进升级（沙箱拒绝才升权）、用户知情（每个风险操作都通知）。

### 3.8 小结（人话版）

六层不是互相替代，而是互相补充：权限配置定义「能做什么」，平台沙箱限制进程能力，执行策略补命令级判断，审批系统引入人的决策，Guardian 在人不方便时自动化审查，网络控制约束信息流出。这是纵深防御（Defense in Depth）：任何单一机制都可能被绕过，但多层叠加后攻击者需要同时突破所有层。

### 3.9 权限模式与界面字段对照

把源码概念映射到用户实际看到的界面（以②的 /status 截图为例）：`:read_only` 对应只读模式，适合探索与不信任的项目；`:workspace` 对应 Workspace 权限，用户可选是否询问批准（截图里是 Workspace (Ask for approval)，即项目内可写、风险动作先问）；`:danger_full_access` 对应完全访问模式，界面明确提示风险。审批弹窗的三个选项也对应源码三种结果：Yes, proceed 对应单次批准；Yes, and don't ask again 对应 ApprovalStore 缓存（ApprovedForSession）；No, and tell Codex what to do differently 对应拒绝并把指示反馈给模型。理解这层对应关系后，看界面就不会只把它当「点按钮」，而是知道每次批准都在改写一个可持久化的决策。

## 四、扩展能力与设计哲学

### 4.1 MCP：连接外部工具世界

MCP（Model Context Protocol）是开放协议，让智能体连接外部工具服务器。核心思想是工具提供者与使用者分离：Codex 不需要知道数据库怎么操作、Slack 怎么发消息，只要会 MCP 协议就能调用任何符合协议的服务器。

Codex 作为客户端：配置中声明多个服务器，每个可以是本地进程（stdio）或远程服务（HTTP）。McpConnectionManager 管理生命周期：启动（AsyncManagedClient + RMCP 建连）、握手（list_tools 发现工具）、运行（等待调用）、关闭（断开）。工具名规范化（字母数字下划线、最长 64 字节），冲突时加 SHA1 哈希后缀去重。

调用链：模型返回 `FunctionCall(name="mcp__my-database__query")` → ToolRouter 路由到 McpHandler → McpConnectionManager::call_tool → MCP 服务器 → 结果格式化写入历史。对模型来说，内置工具与 MCP 工具没有区别。

Codex 也可以作为 MCP 服务器（`codex mcp-server`），把自己的能力暴露给其他智能体。双向设计让它既能调用别人，也能被别人调用。

### 4.2 多智能体协作

复杂任务（如「重构整个项目目录结构，同时更新所有 import 路径并确保测试通过」）可能超出单智能体上下文。多智能体把大任务拆成子任务，交给独立子智能体。`AgentControl`（agent/control.rs:130）是控制平面，持有全局线程管理器弱引用（避免循环引用）与 AgentRegistry。限制：最大并发子智能体默认 6、最大嵌套深度默认 1、路径与昵称唯一。

spawn_agent 流程：解析参数（任务描述、名称、模型、审批策略）→ 从父配置叠加覆盖项构建子配置 → 注册分配昵称与路径 → 发送初始任务（Op::InterAgentCommunication）→ 持久化父子关系。fork 模式三种：none（不继承）、all（继承全部历史）、last_n_turns（最近 n 轮）。

子智能体之间通过 Mailbox（mpsc 异步消息队列 + 序号 watch）通信，用 AgentPath（如 /root/worker）定位；完成时向父智能体发通知。

### 4.3 配置系统：分层叠加

配置分层：内置默认值 → 全局配置（~/.codex/config.toml）→ 项目配置（.codex/config.toml）→ 命名配置（profiles）→ CLI 覆盖 → 云端强制约束。越往下优先级越高。`Constrained<T>` 类型区分「用户设置的值」与「系统强制的值」，防止用户配置覆盖系统级安全约束。

### 4.4 Skill 系统

Skill 是 Markdown 文件（SKILL.md），包含领域指令、工具依赖与策略；元数据含 name、description、dependencies、policy、scope（User/Repo/System/Admin）。来源：用户级 ~/.codex/skills、仓库级 .codex/skills、系统内置、插件。Turn 开始时根据输入自动注入相关 Skill，也可 `$skill_name` 显式引用；依赖未满足时提示安装。

### 4.5 Hook 系统

Hook 在关键节点插入自定义逻辑，共 8 种事件：

| Hook | 触发时机 | 能否拦截 | 能否修改 |
| --- | --- | --- | --- |
| SessionStart | 会话开始 | 能（停止） | 注入上下文 |
| UserPromptSubmit | 用户发消息 | 能（停止） | 注入上下文 |
| PreToolUse | 工具执行前 | 能（阻止） | 改写工具输入 |
| PermissionRequest | 审批弹窗前 | 能（允许/拒绝） | — |
| PostToolUse | 工具成功后 | 能（停止） | 替换输出 |
| PreCompact | 压缩前 | 能（停止） | — |
| PostCompact | 压缩后 | 能（停止） | — |
| Stop | 会话结束 | — | — |

Hook 通过外部命令实现（hooks.json 配置脚本，stdin 接收上下文、stdout 返回决策）。PreToolUse 位于工具查找之后、实际执行之前，可审查参数、改写输入、阻止执行；PermissionRequest 可在弹窗前自动决策，比如匹配 git commit 时自动批准。

### 4.6 设计哲学与工程严谨性

1. Channel 解耦：核心逻辑可被 TUI、headless、App Server 复用。
2. 安全内建：纵深防御渗透架构每一层，不是外挂功能。
3. 可扩展工具体系：实现 Handler 并注册即可加工具；MCP 让工具外部化；Hook 让行为可运行时拦截。
4. 事件驱动流式架构：ResponseEvent 让用户在模型思考时就看到中间结果。
5. 平台抽象：Seatbelt / Landlock+bwrap / Restricted Token 给上层一致体验。
6. 工程严谨性：全量 Snapshot 测试防 UI 意外变化、Clippy Lint 强制风格、Bazel 保证跨平台可重现构建。

## 五、实践一：从跑通 CLI 到最小任务（阿里云）

### 5.1 为什么先 CLI

Codex 入口有三种：CLI、桌面端、VS Code 插件。桌面端更像任务工作台，适合同时管理多个会话；VS Code 插件贴近日常编码（解释逻辑、改代码、补测试）；CLI 最适合第一次实践：进入项目目录、启动 Codex、发出任务，直接在终端观察它读了什么、跑了什么命令、生成了什么。

### 5.2 安装与启动

macOS 用 Homebrew：

```bash
brew install --cask codex
codex --version
```

注意 `--cask`：brew formula 用于命令行软件包，cask 用于 macOS 应用；Codex 走 cask 路线。升级用 `brew upgrade --cask codex`。首次运行 codex 进入登录/授权流程。关键认知：在哪个目录启动，Codex 就围绕哪个目录工作，所以新手先建干净练习目录（mkdir codex-usage && cd codex-usage）再启动。

### 5.3 /status：最该先学的命令

`/status` 显示当前会话状态，重点字段：Model（模型与推理强度、summaries 策略）、Directory（当前目录）、Permission（权限模式，如 Workspace (Ask for approval)——可在工作区操作但风险动作先请求批准，适合第一次上手）、AGENTS.md（有无项目规则文件）、Account（账号与套餐）、5h limit（5 小时窗口余量，判断接下来几小时）、weekly limit（1 周窗口余量）。`/statusline` 可把余量常驻显示。

### 5.4 最小任务：本地余量记录器

需求：做一个 record_usage.py，尽量「一次命令完成查看和记录」，解析 5h/weekly limit 写入 usage_log.csv 并打印余量；summary.py 显示最近一次记录、历史最低余量、余量下降最快的相邻两次记录；全部用 Python 标准库。Prompt 里明确边界：不读取或修改 Codex 登录凭据、配置文件、缓存文件；不访问隐藏目录内部文件；先验证是否有安全公开方式（codex status / codex usage / codex exec 能否拿到 /status 输出）；无法安全获取就说明原因并提供 fallback 版本。

### 5.5 观察 Codex 的实际行为

Codex 没有一上来就写脚本，而是先试 codex status、codex usage，再看 codex exec --help、codex doctor --help，又试 codex help status/usage，用 codex exec 测试能否拿到 /status 输出——先判断工具链有没有现成接口，再决定是否自己实现，很像真实开发的第一步。

期间出现命令授权提示：Codex 准备运行 `node ... fetch-codex-manual.mjs`（联网获取 OpenAI 官方 Codex manual，确认有无公开支持的 status/usage 读取方式），Reason 写明目的。选项：Yes, proceed（仅这一次）、Yes, and don't ask again...（同命令不再询问）、No, and tell Codex what to do differently（拒绝并给指示）。第一次使用建议只允许一次，保留后续确认。

验证结论：当前版本 /status 只能在 CLI 交互界面查看，没有稳定结构化的外部读取接口——「执行 /status 自动写 CSV」暂不可行。这不算失败，而是摸清了版本边界；于是进入 fallback 方案，创建 record_usage.py、summary.py、usage_log.csv；运行 python3 record_usage.py 录入、cat usage_log.csv 检查、python3 summary.py 输出分析。

完整流程：提出需求 → 检查当前环境 → 尝试验证已有命令 → 遇到限制转向 fallback → 创建本地文件 → 运行脚本 → 生成可检查的结果。第一次上手不必做复杂功能，用一个安全小任务观察它怎么判断工具能力、怎么请求授权、怎么处理限制，比单纯问「你能做什么」更有价值。

说明：原文末尾「哪些任务更耗用量」的回复内容在截图中，正文未提供文字清单，此处如实标注信息缺口，以原文图片为准。

### 5.6 从实践回看源码：三个观察点

第一次跑 Codex 时，可以把看到的现象与源码机制对上号：第一，授权弹窗不是「额外步骤」，而是 Orchestrator 审批阶段（NeedsApproval）的用户界面，选择「批准并记住」就是在写 ApprovalStore 缓存；第二，Codex 先试 codex status/usage 再决定写脚本，对应 Agent Loop 里「先工具后结论」的决策模式——它每次都在用 shell 工具收集信息，再决定下一步；第三，创建 record_usage.py、summary.py 时用到的不是 shell 重定向，而是 apply_patch 类工具（带路径校验与 diff 流式展示），这正是「工具是执行手臂、模型只做决策」的直观体现。带着这三个观察点再看②的截图，会发现每个界面元素背后都有一条源码链路。

## 六、实践二：把它当工程队友（腾讯云）

核心观点：Codex 不是更强的代码聊天机器人（描述需求→等生成→跑不通再追问），而是可配置、可验证、可沉淀经验的工程队友。工作流：给它清楚的上下文，让它先计划，再执行，再验证，最后把经验沉淀下来。

### 6.1 Prompt 不花哨，但上下文要完整

稳定的任务描述包含四件事：目标（到底想改什么）；上下文（相关文件、错误日志、接口文档在哪里）；约束（哪些目录不能碰、哪些行为不能变）；完成标准（测试通过、bug 不再复现、页面行为符合预期）。

反例：「帮我修一下登录问题」。正例：「修复用户登录后偶尔跳回首页的问题。登录逻辑在 src/auth，路由守卫在 src/router。不要改数据库结构，不要重写登录流程。完成后补充测试，并确认登录后能回到原访问页面。」这不是教模型写代码，而是减少它乱猜。

### 6.2 复杂任务先 Plan 再动手

小改动可直接做；涉及多模块、需求不清、可能影响架构时，先进入计划状态：先读代码复述理解 → 列出风险点 → 给出修改方案 → 说明验证方式 → 确认后再实现。可直接说：「先不要写代码。请先阅读相关文件，给出你的理解、修改计划、风险点和验证方式，等我确认后再实现。」这一步能少改很多无关代码，提前暴露风险。

### 6.3 重复要求写进 AGENTS.md

经常提醒的事——不要改无关文件、改完要跑测试、提交前先看 diff、这个项目用 pnpm 不用 npm、API 返回格式不能变——不该每次都写进 prompt，而应沉淀到 AGENTS.md：它是「给 AI Agent 看的项目说明书」，适合写项目结构、启动方式、测试命令、代码风格、禁止事项、完成标准。一个短而准确的 AGENTS.md，通常比一堆临场提醒更有用。

### 6.4 配置决定稳定性，也决定成本

很多使用问题本质是配置没固定：默认模型不合适、权限策略不清楚、MCP 没配、工作目录不对、每次临时改参数。建议固化到 ~/.codex/config.toml。原文示例：

```toml
[model_providers.apitoken]
name = "API Token"
base_url = "https://apitoken.fun/v1"
env_key = "APITOKEN_API_KEY"
wire_api = "chat"

[profiles.gpt55]
model_provider = "apitoken"
model = "gpt-5.5"
```

易错点：base_url 填到 `/v1` 截止，不要写成 `/v1/chat/completions`，也不要漏掉 /v1。

### 6.5 写代码也要验证代码

工程里真正的完成不是「代码写出来了」，而是：测试补了没有、相关测试跑了没有、lint/type check 过了没有、diff 有没有异常、有没有引入回归、最终行为是否符合需求。可把验证要求写进任务：「实现后请运行相关测试，并检查 git diff，确认没有无关修改。如果测试无法运行，请说明原因和已经做过的验证。」Codex 也能补测试、跑测试、看日志、review diff。

### 6.6 MCP、Skill、Automation 三件套

有些上下文不在代码仓库里（issue、PR、CI、内部文档、日志系统、监控平台），每次复制粘贴既麻烦又易过期，适合用 MCP 接入稳定读取最新上下文；但不建议一上来把所有工具都接进去，先接一个最高频信息源，用顺了再扩展。反复做的流程（日志排查、发布说明生成、PR checklist、事故复盘）适合做成 Skill。

简单理解：MCP 解决「信息从哪里来」；Skill 解决「这类任务怎么做」；Automation 解决「什么时候自动做」。顺序很重要：先手动跑通，再沉淀 Skill，最后自动化。

### 6.7 长任务要管理 session

Session 会积累上下文、决策和中间状态，所以不要一个项目永远用同一个巨大线程：上下文越堆越多，后面越容易跑偏。原则：一个 session 对应一个相对完整的任务；任务分叉就开新线程或子任务（代码探索、日志分析、测试补充、方案对比）；主线程负责判断，子线程消化局部信息。

结语：Codex 的最佳实践不是某个神奇 prompt，而是工程化工作流：清晰上下文启动任务 → 复杂需求先计划 → AGENTS.md 沉淀规则 → 配置固定模型与权限 → 测试和 review 闭环 → MCP 接外部上下文 → Skill 固化重复流程 → Automation 放大稳定工作流 → session 管理保持上下文干净。当成代码生成器只能省一点时间；当成可配置、可验证、可沉淀的工程队友，效率提升才稳定、才适合长期高频使用。

## 七、三份材料的重合与互补

重合点对照：

| 主题 | 源码文（①） | 阿里云实践（②） | 腾讯云最佳实践（③） |
| --- | --- | --- | --- |
| 循环与终止 | run_turn 主循环、needs_follow_up、自动压缩 | 观察到「先验证→遇限→fallback→再实现」的多步决策 | 先计划→执行→验证→沉淀的工作流 |
| 工具 | ToolRouter/Registry、shell、apply_patch、MCP | 探测 codex status/usage/exec 命令、创建脚本文件 | MCP 接高频信息源、Skill 固化流程 |
| 安全 | 权限配置、沙箱、执行策略、审批、Guardian、网络白名单 | Permission=Workspace (Ask for approval)、命令授权弹窗 | 配置固定权限策略；验证闭环 |
| 上下文 | 对话历史是状态；自动压缩腾空间 | /status 看目录、模型、额度；目录即边界 | Prompt 四要素、AGENTS.md、session 管理 |
| 沉淀/复用 | Skill、Hook、配置分层叠加 | 小工具文件落地、可复查结果 | AGENTS.md + Skill + Automation 三层沉淀 |

互补关系：①解释「为什么」——审批、沙箱、压缩都是架构内建约束，不是临时开关；②示范「第一次怎么上手」——最小任务、先验证公开接口、fallback 是正常路径而非失败；③给出「长期怎么用」——把上下文、计划、验证、沉淀变成习惯。三份材料共同结论：Codex 的价值不在单次生成，而在「可观察、可约束、可复用的持续工作流」。

### 7.1 一个例子走完三份材料

以「清理 src/main.rs 的 TODO」为例串联：源码视角（①），用户消息进入 run_turn 主循环，模型先调 shell 读文件（grep TODO），把结果写回历史，再决定用 apply_patch 删除或改写，最后给文本回复；期间每次 shell 调用都过权限与沙箱。实践视角（②），用户在 CLI 里能看到每一步命令与结果，遇到危险命令（如 rm）会看到授权弹窗，目录里出现的是补丁后的真实文件。工程视角（③），用户应先在 prompt 里写清目标、约束（只动 main.rs，不碰其他文件）与完成标准（编译通过、无 TODO 残留），实现后要求运行测试与检查 git diff。同一个任务，三份材料分别解释了「内部怎么转」「外部怎么观察」「怎么定义才算好」。

## 八、落地路线图与风险

可操作路线：

1. 安装与边界：按②建干净目录跑通 CLI，用 /status 确认模型、目录、权限、额度；先在 Workspace + 询问权限下练习。
2. 最小任务：选一个边界清楚的小需求（如余量记录器），主动写明禁止项与 fallback 要求，观察它先验证再实现。
3. 理解内部循环：对照①的 Agent Loop 流程，观察每个工具调用前后模型如何决策、结果如何反馈、何时自动压缩。
4. 工程化：按③把重复要求写入 AGENTS.md，复杂任务先计划，实现后要求测试与 diff 检查。
5. 沉淀复用：手动跑通 → Skill → Automation；MCP 只接最高频信息源，不贪多。
6. 保持上下文干净：一任务一会话，任务分叉开子线程；主线程判断、子线程消化信息。

风险与边界：权限模式决定破坏面，danger_full_access 只在完全信任时使用；Guardian 等自动审查不是万能，关键操作仍需人核验；自动压缩会改写历史，极端长任务存在信息损失风险；工具输出可能截断；模型建议的「允许规则」可能过宽；第三方 MCP、插件、Hook 扩大攻击面；额度按 5 小时/1 周窗口管理，长任务注意用量。

### 8.1 每次交付的验收清单

把③的验证要求固化成清单：任务开始前确认目标、上下文、约束、完成标准四要素齐备；实现后确认测试已补、相关测试已跑、lint/type check 已过、git diff 无无关修改、无回归、行为符合预期；若某项无法验证，要求 Codex 说明原因与已做的替代验证；最后把本次踩坑与修正写回 AGENTS.md 或 Skill，让下一次更稳。这条清单同时服务于人：用户核验的是「定义是否正确」，而不是逐行审查代码。

## 九、代码选读：五个最值得看的片段

看不懂全部源码没关系，下面五个片段对应全文最重要的五个机制，每段附一句「看什么」。

### 9.1 调度分发：一切操作都有明确入口

```rust
while let Ok(sub) = rx_sub.recv().await {
    match sub.op.clone() {
        Op::UserTurn { .. } | Op::UserInput { .. } => user_input_or_turn(&sess, sub.id, sub.op).await,
        Op::Interrupt => interrupt(&sess).await,
        Op::ExecApproval { .. } => exec_approval(&sess, ...).await,
        Op::Compact => compact(&sess, sub.id).await,
        Op::Shutdown => shutdown(&sess, sub.id).await,
    }
}
```

看什么：用户输入、中断、审批响应、压缩、关闭都走同一个循环，按 Op 类型分发。这让任何前端（TUI、headless、App）都能用同一套操作原语，也让「用户中断一个长任务」与「提交新任务」在核心层有同等地位。

### 9.2 Token 检查与自动压缩：长任务的续命机制

```rust
let total_usage_tokens = sess.get_total_token_usage().await;
let token_limit_reached = total_usage_tokens >= auto_compact_limit;

if token_limit_reached && needs_follow_up {
    run_auto_compact(..., CompactionReason::ContextLimit, CompactionPhase::MidTurn).await;
    continue;
}
```

看什么：压缩不是「上下文满了报错」，而是插在 Agent Loop 中间的正常步骤。两个条件缺一不可——Token 达到阈值，且任务还没完成（needs_follow_up）。这意味着系统优先保证任务连续性，代价是旧对话被总结改写。

### 9.3 工具调用识别：一切响应先分类

```rust
pub fn build_tool_call(item: ResponseItem) -> Result<Option<ToolCall>, FunctionCallError> {
    match item {
        ResponseItem::FunctionCall { name, namespace, arguments, call_id, .. } => {
            Ok(Some(ToolCall { tool_name: ToolName::new(namespace, name), call_id,
                payload: ToolPayload::Function { arguments } }))
        }
        ResponseItem::ToolSearchCall { .. } => { /* 工具搜索 */ }
        ResponseItem::CustomToolCall { .. } => { /* 自定义工具 */ }
        _ => Ok(None),
    }
}
```

看什么：模型返回的输出项不止「文本」一种，系统先分类再分流。返回 None 的普通消息进入历史；返回 Some 的工具调用进入执行管线。needs_follow_up 的分叉就发生在这里。

### 9.4 工具派发与 Hook：执行前的最后一关

```rust
let tool = match self.tool(&tool_name) {
    Some(tool) => tool,
    None => return Err(FunctionCallError::RespondToModel(unsupported_tool_call_message(...))),
};
if let Some(payload) = tool.pre_tool_use_payload(&invocation) {
    match run_pre_tool_use_hooks(...).await {
        PreToolUseHookResult::Blocked(message) => return Err(FunctionCallError::RespondToModel(message)),
        PreToolUseHookResult::Continue { updated_input: Some(updated_input) } => {
            invocation = tool.with_updated_hook_input(invocation, updated_input)?;
        }
        PreToolUseHookResult::Continue { updated_input: None } => {}
    }
}
```

看什么：工具不存在时错误要「还给模型」而不是直接崩溃——模型能读到错误并改策略；Hook 能在执行前拦截或改写参数。这两点共同体现了「智能体系统把模型当对等参与者，而不是被调用的黑盒」。

### 9.5 并行控制：一把锁决定串行还是并行

```rust
let _guard = if supports_parallel {
    Either::Left(lock.read().await)    // 读锁：多个并行工具同时执行
} else {
    Either::Right(lock.write().await)  // 写锁：串行执行，互斥
};
```

看什么：并行不是「所有工具一起跑」。声明支持并行的工具共享读锁（可同时执行），不支持的工具拿写锁（排他）。一段简单的 RwLock 逻辑，同时保证了吞吐与正确性——比如两个只读命令可以并行，一个写文件的操作必须等前面的读完。

## 十、常见问题：原理与实践对照问答

Q1：Turn 和普通聊天轮次有什么区别？

普通聊天一次问一次答；Turn 是「一次用户消息到最终完整回复」的完整周期，内部可能包含多轮 LLM 调用与工具执行。源码里 RegularTask 的外层 loop 还处理「执行中又有新输入」的情况，用空输入继续下一轮。

Q2：为什么模型不能自己执行命令，非要走工具？

模型是文本生成器，没有操作系统权限。工具把「决策」与「执行」分离：模型只决定调用什么、传什么参数，执行与安全约束由系统负责。这也是安全机制能生效的前提——如果模型直接执行命令，审批、沙箱、Hook 都无处安放。

Q3：工具结果为什么要格式化？

模型需要稳定、结构化的输入。JSON（output + exit_code + duration）比原始终端文本更可靠，且能配合截断策略控制上下文占用。MCP 工具同样被统一包装，所以模型无需区分工具来源。

Q4：自动压缩会不会丢信息？

会改写。压缩把旧对话总结成更简洁的表示，本质上是有损的。设计上它在 Token 阈值触发、任务未完成时执行，保证长任务能继续；代价是极端长任务中早期细节可能被概括掉。实践上对应③的「一个 session 对应一个完整任务」，别让上下文无限堆积。

Q5：沙箱拒绝后为什么不直接放开？

因为「拒绝」本身就是安全信号。正确的路径是：默认沙箱内执行 → 沙箱拒绝 → 若工具支持升级且策略允许，请求用户批准无沙箱重试。这样高风险操作每次都需要人知情，而不是被静默放行。

Q6：Guardian 和用户审批是什么关系？

Guardian 是「auto」审查模式下的替代审批者：用户在配置里选择自动审查后，风险操作由独立 AI 会话判断。它失败即拒绝（超时 90 秒算拒绝），且有熔断器防止模型反复试探。关键操作仍建议保留人工审批，Guardian 适合信任度较高的自动化场景。

Q7：MCP、Skill、Automation 有什么区别？

MCP 解决「信息从哪里来」（外部系统接入）；Skill 解决「这类任务怎么做」（流程与领域知识）；Automation 解决「什么时候自动做」（定时触发）。顺序是手动跑通 → Skill → Automation。

Q8：为什么权限模式这么重要？

权限模式决定整个安全链路的起点：read_only 下写操作直接 Forbidden；workspace 下项目内可写、风险动作询问；danger_full_access 下沙箱被跳过。③的「配置决定稳定性」和②的「第一次用 Workspace 询问模式」都是同一个道理。

Q9：额度（5 小时/1 周窗口）和源码有什么关系？

额度是使用层限制，源码里对应 token 用量跟踪与不可重试错误（UsageLimitReached）。实践上：5 小时窗口判断「接下来几小时能不能用」，1 周窗口看整体；长任务、并行工具、高推理强度都会加速消耗。

Q10：看不懂源码怎么用这份总结？

直接读每章「小结」和第十章的落地路线图；遇到界面上的权限弹窗、自动压缩、MCP 配置时，再回到对应章节查原理。源码细节是「为什么」，实践步骤是「怎么做」，两者对照使用即可。

Q11：什么时候该用多智能体（子任务）？

当一个 Turn 装不下、或任务可以清晰切分时：比如探索代码库、分析日志、补测试、对比方案可以并行。源码层的限制是最大并发 6、嵌套深度默认 1；实践层的原则是③说的「主线程判断、子线程消化局部信息」。子任务结果要回到主线程汇总，而不是各自散落。

Q12：AGENTS.md、Hook、Skill 有什么区别？

AGENTS.md 是「项目说明书」，每次会话都会被读取，适合写静态规则；Skill 是「可复用的任务方法」，按需或自动注入，适合写流程；Hook 是「行为拦截器」，在事件点执行外部脚本，适合做自动化审查与改写。三者都服务于同一个目的：把临时指令变成持久约束。新手从 AGENTS.md 开始，用熟了再加 Skill，最后才考虑 Hook。

Q13：为什么说「安全不是功能，是约束」？

功能是「让智能体能做更多」，安全约束是「让它在边界内做」。源码把约束内建在每一层：权限配置划边界、沙箱锁能力、执行策略管命令、审批引入人、Guardian 自动审查、网络代理管出口。安全的价值不在拦截了多少次，而在默认状态下系统不会越界；这也是为什么「完全访问模式」必须由用户显式选择。

## 附录

关键术语：Agent Loop、Turn、Submission/Event、ToolSpec/ToolName、ToolRouter/ToolRegistry、SandboxType、ExecPolicy、ApprovalStore、Guardian、MCP、Skill、Hook、Compaction、SessionTask、fork 模式。

术语一句话释义：Agent Loop（决策-执行-反馈循环）；Turn（一次消息到完整回复的周期）；Submission/Event（操作指令与状态事件的通道消息）；ToolSpec/ToolName（工具定义与带命名空间的工具名）；ToolRouter（模型响应到工具执行的桥梁）；ToolRegistry（工具注册表）；SandboxType（平台沙箱类型）；ExecPolicy（命令级执行规则）；ApprovalStore（审批结果缓存）；Guardian（AI 自动审批审查）；MCP（外部工具协议）；Skill（领域知识包）；Hook（事件拦截脚本）；Compaction（历史压缩）；SessionTask（Turn 任务实现）；fork 模式（子智能体继承历史的方式）。

来源：①用户提供原文（已存档 raw_data/Codex/2026-08-03-Codex源码万字长文-原文.txt）；②阿里云开发者文章 1740159（2026-06-08）；③腾讯云开发者文章 2674885（2026-05-27，正文经 CSDN 转载 161455726 补全）。
