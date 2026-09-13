# 工具调用 Pitfall 经验库

> 跨场景的通用「工具调用效率与失败应对」经验沉淀库。
> 本库为 BadCase 总库（`BadCase库/`）的「工具调用」模块；库级规则见《BadCase库/README.md》。
> 与《BadCase库/工具调用经验/信息爬取经验与避坑指南》（知乎爬取专项）相互独立：专项文档只覆盖爬取链路，本库覆盖所有工具、命令、搜索、文件与自动化操作。
> 基本认知：调用失败、卡顿、超时是正常现象，不是异常；本库的目的不是「零失败」，而是失败后快速换路、少连续试错。
> 核心主题：每次任务中思考「能否用更少的工具调用完成同一目标」，并沉淀这类少调用经验，从而减少工具调用次数、等待时间与 Token 消耗。
> 查证例外：「少调用」不适用于信息查证与创作——写作、创作、研究时仍要多查来源、多角度认识，必要查找与尝试属正常；衡量标准是失败比例，不是失败绝对次数。
> 表述规范：现象与根因用可核验事实（报错码、返回数量、实测结果、具体命令），不用主观程度词（如「极差」「最稳」「坑多」「大量」）；有量化数据就写数据。

## 一、何时记录（触发条件）

满足以下任一情况，任务中立即追加一条，不等任务结束：

1. 发现新的失败模式（被拦截、报错、超时、返回空/截断/乱码）；
2. 检索失败或结果不可用（搜不到、覆盖差、来源不可信）；
3. 找到新的替代路径、规避方法，或发现旧经验已失效；
4. 任务中发现「可以少调用工具完成同一目标」的新方法；
5. 本次解决不了的失败，记为「待验证」条目，不写结论。

不记流水账：不记录每一步过程，只记「踩了什么坑 + 根因 + 有效路径 + 可复用教训」。
回写前先查重：与现有条目重合则不写（仅旧条目失效或需修正时更新原条目），防止噪音文档与上下文膨胀。

## 二、失败应对原则（失败正常，重试要少）

1. 一次失败先看错误信息：能快速修正（参数、语法、路径）就修正后重试 1 次；不能快速定位就换路。
2. 查库时机（双触发）：动手前先查本库与专项，命中即复用；失败后不立即查——先看报错并快速修正 1 次，修正后仍失败或同一失败持续约 15-20 秒未解决，才 `rg` 检索本库（按「报错特征/触发关键词」字段），命中照做，未命中再自由换路。
3. 换路前先按失败类型定替代路径（换工具、换命令写法、换实现方式、换数据源、降级目标），不做无依据乱换。
4. 同类路径最多尝试 2 次；连续 2 次未成即停，重新评估或向用户说明，不继续盲试第三、四条。
5. 卡顿/超时先判断是正常执行还是已卡死：已卡死立即中断换路，不干等。
6. 闭环回写：命中且解决后，在该条追加「最近复用：YYYY-MM-DD」；连续 2 次命中无效改「状态：已失效，待复核」（删除须用户确认）。
7. 评价用「失败比例」而非「失败次数」：为获取多元信息而做的必要尝试不计为浪费；只有无新增量、同路反复的试错才需要控制。

## 三、效率原则（少调用、少等待、少 Token）

1. 每次任务开始与进行中先问「能否再少调用一点工具就完成同一目标」；能合并、并行、复用就不新增调用。
2. 减少调用次数：无关操作并行执行；一条命令能完成的不拆多条；动手前先查本库与专项文档，命中即复用。
3. 减少等待：长任务挂后台、先做其他步骤；小样本验证通过后再全量执行，避免全量重跑。
4. 减少 Token：失败后不重复粘贴同一错误、不重复输出相似命令；汇报只写结论与必要依据。
5. 检索不到时如实标注「依据不足」，不靠反复搜索硬凑。
6. 查证例外：写作、创作、事实核验与多元认知任务优先多查来源、多角度检索，不因省调用而少查；每次检索应有新增信息，无新增量的重复检索才视为浪费。

## 四、条目格式（模板）

### Pitfall-NNN 一句话标题

- 报错特征/触发关键词：可精确匹配的记号（报错码、命令、URL 片段、现象词），供 `rg` 直接检索
- 最近复用：无 / YYYY-MM-DD（命中并解决后回写）
- 状态：有效 / 已失效，待复核
- 场景：哪个任务/工具/检索场景
- 现象：失败或异常的具体表现（含关键报错）
- 根因：定位到的真实原因（不确定标「待验证」）
- 有效路径：验证过可用的命令/操作/链接
- 教训：下次可复用的判断或操作要点

## 五、现有条目

> 以下四条为初始通用条目，基于用户 2026-08-01 的观察总结与既有《信息爬取经验与避坑指南》提炼，非虚构案例。

### Pitfall-001 失败与卡顿是常态：快速换路，不连续盲试

- 报错特征/触发关键词：超时、卡顿、原样重试
- 最近复用：2026-08-25（视频元数据批量核验：bundled Python 的 urllib 证书校验失败，改用 subprocess 调系统 curl 后端成功）
- 状态：有效
- 场景：任意工具、命令或接口调用
- 现象：调用失败、卡顿或超时，原样重试仍失败
- 根因：权限/沙箱限制、参数错误、目标端防护、环境差异，均属正常可能
- 有效路径：一次修正 → 不行立即换按失败类型确定的替代路径；同类尝试 ≤2 次后停止，重新评估或向用户说明
- 教训：控制连续试错次数比「零失败」更重要；换路前先判断，不做无依据乱换

### Pitfall-002 检索无结果/覆盖差：换关键词、换来源，别反复搜同一组合

- 报错特征/触发关键词：无有效结果、检索无结果、覆盖差
- 最近复用：无
- 状态：有效
- 场景：网络检索、用搜索引擎补全数据
- 现象：同一关键词反复搜索仍无有效结果
- 根因：搜索引擎对目标站点（如知乎）近期内容覆盖差，或关键词组合不当
- 有效路径：换关键词、限定站点、直查官方页面/接口（详见《BadCase库/工具调用经验/信息爬取经验与避坑指南》2.4 节）
- 教训：搜索只作线索；数据类任务优先验证目标站自身接口；检索不到时如实标注「依据不足」

### Pitfall-003 每次任务先问「能否少调用」：合并、并行、复用优先

- 报错特征/触发关键词：调用次数偏多、等待时间偏长、少调用
- 最近复用：无
- 状态：有效
- 场景：任何任务执行前与执行中
- 现象：默认按习惯一步步调用工具，调用次数偏多、等待时间偏长
- 根因：动手前未做「最少调用」规划
- 有效路径：先问「能否再少调用一点工具就完成同一目标」→ 合并命令、并行无关操作、先查本库与专项文档复用已验证路径、小样本验证后再全量
- 教训：调用次数是可规划的；每次任务结束前复盘一次少调用方法，比事后补救更省时间与 Token

### Pitfall-004 「少调用」不等于「少查来源」：查证例外，失败看比例

- 报错特征/触发关键词：减少检索来源、认知片面、查证例外
- 最近复用：无
- 状态：有效
- 场景：写作、创作、研究、事实核验等需要多元信息的任务
- 现象：为避免调用失败而减少检索来源，导致认知片面
- 根因：把「少调用」误用为「少查证」
- 有效路径：多来源、多角度检索照常进行；评价标准是失败/试错比例而非失败次数；每次检索应带来新信息，无新增量的重复检索才叫浪费
- 教训：信息广度与调用效率不矛盾；为多元认识而进行的必要查找与尝试完全正常

### Pitfall-005 官方文档站直连 403：换官方检索或搜索引擎快照，不反复直连

- 报错特征/触发关键词：403、Forbidden、open_page、curl
- 最近复用：2026-09-13（前沿模型系统提示词抓取：help.openai.com 对 curl 浏览器 UA／Googlebot／bingbot 均 403、web_fetch 亦 403，正文确认不可得，改以官方 GitHub raw 与 developers.openai.com 取证；补充——同日 developers.openai.com 在 web_fetch 报 "resolves to a non-public IP" 但 curl 直连成功，故同一官方域应把「网页抓取工具」与「curl」两条通道都试一次再判定不可达）；此前 2026-08-08（Codex 设置问答：developers.openai.com 403、learn.chatgpt.com 超时，改用 site: 官方摘要＋本机 App/CLI 内置定义核对）
- 状态：有效
- 场景：检索 OpenAI 官方文档（developers.openai.com）等有反爬防护的官方站点
- 现象：open_page 与 curl（含浏览器 UA）直连均返回 403 Forbidden；个别官方域名 curl 挂起超时
- 根因：站点对自动化/数据中心流量做防护，直接抓取被拒，属正常防护而非参数错误
- 有效路径：用搜索引擎限定官方域名（site:developers.openai.com）取官方页面摘要与链接，或改用官方文档检索/手册接口；同类直连最多试 2 次后换路；模型元数据可优先取本机 `~/.codex/models_cache.json`（Codex 官方目录缓存）
- 教训：官方文档域对自动化流量返回 403 属已知防护行为，先换路取证并附官方链接，不硬试、不因抓不到就放弃官方来源

### Pitfall-006 多会话并发写同一文件：apply_patch 上下文失配时先重读顶部再插

- 报错特征/触发关键词：Failed to find expected lines、apply_patch、多会话并发
- 最近复用：2026-08-08（会话日志追加：apply_patch 失配，重读文件顶部后以最小上下文插入成功）
- 状态：有效
- 场景：多个 Codex 会话同时向项目文档（如会话摘要、经验库）追加内容
- 现象：apply_patch 报「Failed to find expected lines」，原因是文件顶部已被其他会话改写或整体重生成
- 根因：多会话共享同一工作区并发写文件，按旧上下文打补丁失配（待验证）
- 有效路径：patch 前先 `sed -n '1,10p'` 重读目标文件顶部，用最小上下文（仅表头/分隔行）定位插入点，再打补丁
- 教训：共享文件改前必重读；最小上下文能显著降低并发失配，失配后重读一次即可重试，不盲试

### Pitfall-007 健康信息源被反爬/浏览器验证拦截：换摘要镜像与可直连机构页

- 报错特征/触发关键词：FETCH_TIMEOUT、PROXY_ERROR、Checking your browser、403
- 最近复用：2026-09-09（人体科普：PubMed 出现浏览器验证、Medscape 摘要镜像本轮不可用；改用 Europe PMC 公共书目接口实际读入 PMID 16512313、11370109、41665964 的原论文摘要，核对 DOI 与日期，仅使用摘要支持范围）
- 状态：有效
- 场景：检索权威健康/医学资料（CDC、PubMed、Mayo Clinic 等）
- 现象：archive.cdc.gov 页面 FETCH_TIMEOUT/PROXY_ERROR；PubMed 触发 "Checking your browser" 验证；部分政府健康站 403
- 根因：站点反爬或代理链路不稳定，属正常防护（待验证）
- 有效路径：PubMed 被拦时可尝试摘要镜像，但需当轮验证可达性。2026-09-09 的可用替代为 Europe PMC `https://www.ebi.ac.uk/europepmc/webservices/rest/search`，用 `query=EXT_ID:{PMID} AND SRC:MED`、`format=json`、`resultType=core` 读取题名、DOI、日期与摘要；摘要未覆盖的结论不补写。Medscape MEDLINE `reference.medscape.com/medline/abstract/{PMID}` 为历史候选，本轮未成功。CDC 旧页改试当前机构页；不能把镜像与原论文计作独立来源。
- 教训：健康类权威站有「摘要镜像＋机构直连」两套备选；先并行试摘要源与直连源，同类直连最多 2 次即换路

### Pitfall-008 open_page 报 SSRF_BLOCKED 但同域名 curl 可直连：降级 curl 抓原文

- 报错特征/触发关键词：SSRF_BLOCKED、open_page、error_code
- 最近复用：无
- 状态：有效
- 场景：open_page 读取官方文档站（如 api-docs.deepseek.com）被读取工具侧拦截
- 现象：open_page 返回 `{"error_code":"unavailable","message":"SSRF_BLOCKED"}`；同一域名用 `curl -sL` 可正常抓取页面
- 根因：open_page 的代理层对该域名做了 SSRF 防护，非站点拒绝访问（待验证）
- 有效路径：先 `curl -sL <url> -o /tmp/page.html` 再 `rg -a` 提取关键段落核对原文；curl 成功即继续核验，不再反复试 open_page
- 教训：与官方站 403（Pitfall-005）不同，SSRF_BLOCKED 是读取工具侧拦截，curl 直连常可绕过并拿到一手原文；一次换路即可

### Pitfall-009 结构化文本就地替换别用 perl 一行式：分隔符冲突会破坏文件，改用 apply_patch

- 报错特征/触发关键词：Unknown regexp modifier、perl、-0pi
- 最近复用：无
- 状态：有效
- 场景：给 Markdown 表格（会话摘要、经验库）插入新行或就地替换
- 现象：perl -0pi -e 's/.../.../' 因替换文本含 `/`（如「01/02/03」）报 `Unknown regexp modifier "/0"`；另一次尝试把正则字符类文本 `[-| ]+` 原样写进替换串，导致表格分隔行被写成字面量 `|[-| ]+|`
- 根因：s/// 分隔符与内容冲突未换分隔符；替换串误用模式片段，造成文件内容损坏（待验证）
- 有效路径：结构化小改动直接用 apply_patch（先 `sed -n '1,10p'` 重读顶部），插入点用最小上下文；perl 仅在模式与替换文本均无 `/`、`|` 的简单替换时使用
- 教训：写 perl 替换前先检查分隔符冲突；报错立即停止并换 apply_patch，不做第二次 perl 重试

### Pitfall-010 apply_patch 整行精确匹配且 hunk 须按文件顺序：子串补丁与乱序块会失配

- 报错特征/触发关键词：Failed to find expected lines、apply_patch、hunk
- 最近复用：2026-08-08（真实命中：长中文行失配，改用标题行短锚点插入成功；此前 2026-08-05 受控复测）
- 状态：有效
- 场景：用 apply_patch 批量修改长文档（如 AGENTS.md）
- 现象：补丁行只写长行的片段（如从「信息检索、事实核验…」开始而非整行）报 `Failed to find expected lines`；把靠前章节的 hunk 放在靠后章节之后，同样报失配
- 根因：apply_patch 以整行精确匹配，且 hunk 须按文件出现顺序排列（待验证）
- 有效路径：hunk 行必须与文件整行一致，改长行前先 `sed -n 'Np'` 取出整行再复制；多个 hunk 严格按文件顺序排布；失配后用最小补丁单独验证单行
- 教训：批量补丁前先核对整行文本与 hunk 顺序；失配一次即拆小验证，不连续重试同路径

补充（2026-08-02）：含多个 `|` 的超长表格行（如版本记录表），即使字节级核对一致仍可能整行失配；换用其上方的短锚点行（如表头/分隔线）做上下文、新增行直接插在锚点后即可成功，不必反复重试长行匹配。

### Pitfall-011 Electron 应用 localStorage 数据：strings 搜不到，用 classic-level 按 UTF-16LE 解码 persist 键

- 报错特征/触发关键词：idb_cmp1 does not match existing comparator、classic-level、utf16le、persist:*
- 最近复用：无
- 状态：有效
- 场景：读取 Electron 应用（Cherry Studio 1.9.x）本地存储的助手/配置数据
- 现象：`strings`/`rg -a` 搜中文关键词无结果；classic-level 打开 IndexedDB 报 `idb_cmp1 does not match existing comparator`；persist 值按 utf16le 解码误判为字节序反了，连续两次乱码
- 根因：LevelDB 数据块 Snappy 压缩，strings 抓不到明文；IndexedDB 用 Chromium 自定义 comparator，通用 LevelDB 打不开；localStorage value 格式为「1 字节前缀 + UTF-16LE」，utf16le 本来就是低字节在前，无需 swap（待验证）
- 有效路径：先复制 leveldb 目录到 mktemp 副本 → `npm i classic-level` → 遍历键值，对 `persist:*` 键取 `value.subarray(1).toString('utf16le')` → JSON.parse 后逐层解嵌套 JSON；IndexedDB 打不开就换 Local Storage 目录
- 教训：中文数据 strings 搜不到先假设压缩而非加密；Electron 应用业务数据优先查 localStorage 的 `persist:*` 键；解码前打印头字节 hex 验证假设，不做第二次盲目 swap

### Pitfall-012 拉取 GitHub 源码 raw 直连反复挂起/空文件：改走 api.github.com/contents 取 base64

- 报错特征/触发关键词：raw.githubusercontent.com、api.github.com、0 字节、挂起
- 最近复用：无
- 状态：有效
- 场景：需要核验开源项目（如 openai/codex）当前源码中的配置字段、常量或模板
- 现象：`curl raw.githubusercontent.com/...` 多次返回 0 字节、输出文件不存在或长时间挂起（>10s），重试 2 次仍失败
- 根因：raw.githubusercontent.com 对本机网络链路不稳定/超时（待验证）
- 有效路径：改用 `https://api.github.com/repos/{owner}/{repo}/contents/{path}`，返回 JSON 的 `content` 字段 base64 解码即原文；需要先找路径时用 `git/trees/main?recursive=1` 拉文件清单再定位
- 教训：GitHub 源码优先走 API contents 接口（一次成功率更高）；raw 失败一次即换路，不反复重试同路径

### Pitfall-013 讨论/示例落盘 ≠ 已启用配置：状态断言必须有机械证据

- 报错特征/触发关键词：hooks.json、config.toml、已启用、SessionStart
- 最近复用：无
- 状态：有效
- 场景：核验 Hook、自动化或任何「是否已启用/已配置」的状态
- 现象：用户认为时间注入 Hook 已启用，实际 `~/.codex/hooks.json`、项目 `.codex/`、`config.toml` hooks 表三项全缺；此前仅有讨论与示例文档落盘
- 根因：把「会话讨论/示例文件存在」等同于「运行时配置生效」，未区分文档与实配（待验证：是否因历史会话记忆中示例与启用混谈所致）
- 有效路径：启用类断言一律核验文件存在性、配置键、进程/日志三要素之一，并在回复中给出证据路径
- 补充（2026-08-03 实测）：信任/启用发生在会话中途时，SessionStart 不会对已开会话补跑；验证需新开会话或用 codex exec 起一次性会话，并检查 transcript 首条 developer 注入消息
- 教训：凡说「已启用/已配置」，先给可核验的机械证据，不凭会话记忆；示例文档必须标注「未启用」

### Pitfall-014 Codex Memories 无记忆生成：先查 memories_1.sqlite 的 jobs 表，且归因必须按错误时间戳区分新旧记录

- 报错特征/触发关键词：No raw memories yet.、memory_stage1、memories_1.sqlite、HTTP 400、gpt-5.6-luna
- 最近复用：无
- 状态：有效
- 场景：Codex 全局记忆（Memories）已开启（含 Chronicle 授权），但应用内长期看不到任何记忆/用户画像
- 现象：`~/.codex/memories/raw_memories.md` 恒为「No raw memories yet.」；config.toml 中 `memories=true`、`generate/use_memories=true`，却始终无记忆产出；jobs 表 memory_stage1×33、memory_consolidate_global×1 全部 error，stage1_outputs 为 0
- 根因：记忆管线请求内部模型名 gpt-5.6-luna，而当前 provider 为 DeepSeek 官方直连（base_url=api.deepseek.com，只接受 deepseek-v4-pro/flash），返回 HTTP 400；4 条带「CC Switch local proxy」包装的报错为 08-01 旧记录（当时用 CC Switch），08-01 16:26 起 29 条为直连 DeepSeek 的裸 400——根因相同（模型名不被接受），与是否用 CC Switch 无关
- 有效路径：`sqlite3 ~/.codex/memories_1.sqlite "SELECT CASE WHEN last_error LIKE '%CC Switch%' THEN 'CC包装' ELSE '直连' END, count(*), datetime(min(finished_at),'unixepoch','localtime'), datetime(max(finished_at),'unixepoch','localtime') FROM jobs WHERE kind='memory_stage1' GROUP BY 1;"` 按时间戳区分报错来源；修复须让记忆管线的 gpt-5.6-luna 被后端接受（OpenAI 官方模型或模型名映射），jobs 表有自动重试（retry_at/retry_remaining 可查）
- 教训：功能开关开启/授权 ≠ 数据已产生；定位系统问题必须先核对任务时间戳，避免拿历史报错当当前根因；对用户环境变更（如弃用 CC Switch）要以当前进程、配置与最新报错为准

### Pitfall-015 macOS bash 3.2 变量后紧跟全角字符被吞：脚本内统一用 ${var}

- 报错特征/触发关键词：unbound variable、declare -p、${var}、bash 3.2
- 最近复用：无
- 状态：有效
- 场景：bash 脚本输出「变量＋中文全角字符」组合，如 `echo "时间：$stamp（北京时间）"`
- 现象：输出变为 `时间：<两字节乱码>北京时间）`，变量值（日期数字）整体消失；`declare -p stamp` 显示变量值正常；开启 `set -u` 时同场景报 `stamp�: unbound variable`（变量明明已赋值），是排查「unbound」的重要线索
- 根因：macOS 自带 /bin/bash 3.2（3.2.57）对 `$var` 后紧跟 UTF-8 多字节字符（如全角括号 `（` U+FF08）的解析缺陷——全角字符首字节被当作变量名合法字符并入 `$var` 名称，实际展开的变量名是 `var<字节>`，故空展开/未定义（2026-08-04 实测确认；`echo "A $ctitle（）B"` 报错，`${ctitle}（）` 正常）
- 有效路径：变量后紧跟任何非 ASCII 字符一律写 `${var}`；实测 `${stamp}（北京时间）` 输出正确
- 教训：本机 /bin/bash 为 3.2，脚本含中文输出时优先花括号形式；`set -u` 报「unbound variable」但变量已赋值时，先检查变量名后是否紧跟全角/多字节字符

### Pitfall-016 统计 macOS 磁盘占用别用 `du -x -d 1 /`：APFS firmlink 目录数值虚低

- 报错特征/触发关键词：du -x -d 1 /、firmlink、System/Volumes/Data
- 最近复用：无
- 状态：有效
- 场景：全盘空间分布统计（本机磁盘盘点）
- 现象：`du -x -d 1 /` 与 `du -x -d 1 /System/Volumes/Data` 返回 /Users 仅 455M、/Applications 仅 87M，与真实值（217G、42G）严重不符，浪费两轮定位
- 根因：APFS firmlink（/Users、/Applications）在 du 遍历时不计数其目标内容（待验证）
- 有效路径：直接 `du -d 1 -h /Users/...` 与 `du -d 1 -h /Applications` 分别统计；卷级只信 `df -h`
- 教训：macOS 上做目录空间盘点时跳过 `/` 或 `/System/Volumes/Data` 顶层，直接对真实挂载点统计，避免被虚低数值误导

### Pitfall-017 官网附件下载入口带验证码：改用 pdfjs 视图 file 参数直链 __local 路径，PDF 提取用捆绑 Python 的 pypdf

- 报错特征/触发关键词：请输入验证码下载附件、download.jsp、wbfileid、__local、pdftotext
- 最近复用：无
- 状态：有效
- 场景：从高校/机关官网（如 jxust.edu.cn）下载制度附件（重修办法、公选课管理办法 PDF）
- 现象：详情页正文只有「详情见附件」，附件按钮统一跳 `download.jsp?...&wbfileid=...`，返回「请输入验证码下载附件」HTML 页，无法直接取文件；open_page 打开 pdfjs 查看器显示「Enter the password」且无正文；系统 pdftotext 不存在
- 根因：附件下载入口做了页面级验证码保护；pdfjs 查看器对部分 PDF 显示密码框，但文件本身未加密（pypdf 读取正常），属查看器层限制（待验证）
- 有效路径：从新闻详情页 HTML 中提取附件 `wbfileid`；PDF 类附件在 pdfjs 视图 URL 的 `file=` 参数拿直链（如 `https://域名/__local/{分卷}/{hash}/{文件名}.pdf`），实测 jwc.jxust.edu.cn 可 curl 直下；提取文本用工作区捆绑 Python（`codex_app__load_workspace_dependencies` 返回的 python3，含 pypdf）`PdfReader` 逐页 extract_text
- 教训：验证码下载页不硬绕，优先找同一附件的 PDF 直链或同文多学院站镜像；PDF 处理先用捆绑运行时自带库，不装新依赖

### Pitfall-018 钩子不触发先查触发前提：PermissionRequest 在 approval=never 下无请求可拦

- 报错特征/触发关键词：PermissionRequest、approval=never、hook
- 最近复用：无
- 状态：有效
- 场景：想用 PermissionRequest 钩子做白名单自动放行或风险拦截
- 现象：配置后钩子从未执行（运行日志无 hook: PermissionRequest）
- 根因：该事件只在系统实际产生「审批请求」时触发；approval=never＋全权限/无沙箱下，apply_patch 等工具直接 AutoApprove（openai/codex `core/src/apply_patch.rs` 的 assess_patch_safety），不生成审批请求（待验证：exec 类请求是否完全一致）
- 有效路径：装钩子前先确认当前 approval_policy 与权限配置是否会产生审批请求；命令级白名单/黑名单优先考虑 exec policy（.rules）原生机制
- 教训：钩子不是「装了就有」，先核验触发路径，避免白装与无效维护

### Pitfall-019 子代理创建失败报 agent thread limit reached：并发线程达上限，改主代理并行直接执行

- 报错特征/触发关键词：agent thread limit reached、collab spawn failed、spawn_agent
- 最近复用：无
- 状态：有效
- 场景：用户要求「派两个子代理并行」读两份独立文件；一次并行 spawn 两个 agent
- 现象：两个 spawn_agent 均立即失败，报 `collab spawn failed: agent thread limit reached`
- 根因：当前根线程树活动代理数已达并发上限（4 个并发槽位），spawn 被拒绝（待验证：是否含空闲但未回收的线程）
- 有效路径：放弃子代理，主代理用两个并行 exec_command（cat 两份文件）直接完成同一目标，结果等价且零等待
- 教训：spawn 失败先看是否资源上限而非参数问题；只读并行任务在主代理内并行 exec 即可，不必强求子代理

### Pitfall-020 子代理派生成功但不接任务（只回「待命」）或越权再派生多层链：以最终产物为准，重建而非重发

- 报错特征/触发关键词：待命、fork_turns、无待办任务
- 最近复用：2026-09-02
- 状态：有效（2026-08-15 按有效路径重建验证通过）
- 场景：spawn_agent 派子代理执行明确任务（如独立审查画像），spawn 返回成功
- 现象：子代理最终只回「无待办任务/待命」，任务未执行；followup_task 重发仍回待命；换 fork_turns=2 带上下文派生后正常执行。2026-08-09 复核：给独立审查子代理派发任务时未显式限制其再派生，审查代理 fork_turns=none 再派生孙代理，孙代理只回待命、审查代理挂起等待，最终由用户中断；本次教训为派生审查/子代理时显式写明「不得再派生子代理」，并避免无产出等待。2026-08-10 第三次复核：审查子代理以 fork_turns=all 收到完整任务后完成任务并直接落盘合入，但任务卡未禁止再派生，其自行派生二级审查链（孙代理仍在运行），由根执行体中断；用户明确要求子智能体只保留一层、禁止再派生
- 根因：fork_turns=none 时任务消息未被当作执行指令处理（2026-08-05 实测：派生 3 个受控测试子代理，3/3 仅回待命，任务消息未注入）；并发槽位占满时链内再派生会失败并多层嵌套
- 有效路径：派生子代理带少量最近上下文（如 fork_turns=2）；第一轮只回待命时重建新子代理而非反复重发；验证以最终交付物为准，不以 spawn 成功为准；任务卡首行显式写明「禁止再派生子代理/孙代理，仅本层完成后直接返回」，子智能体只允许一层（2026-08-10 已升级为通用规范：全局/项目 AGENTS 执行规则＋《影评生成范式》《影片分析约束》）
- 教训：子代理「创建成功」≠「接了任务」；关键体验/任务前先确认并发槽位空闲，并核对子代理产出
- 2026-08-09 第二次复核：独立审查子代理以 fork_turns=none 派生并显式写明「禁止再派生子代理、直接输出四块」，运行 10 分钟仍无任何产出，主代理中断后自审交付。结论：本环境审查类子代理稳定性不足，「禁止再派生＋明确任务」未能保证产出；高优先级交付建议主代理自审＋用户复核，或将子代理审查作为可选环节而非硬前置
- 2026-08-15 第四次复核：审查子代理派发再次以 fork_turns=none 卡死（只回「未收到任务内容」），对卡死代理 followup_task 重发两次仍不注入；重建探针代理（fork_turns=2）端到端成功，但 wait_agent 超时未回传 final，报告经 interrupt_agent 的 previous_status 完整取回（与 Pitfall-049 叠加）。结论：根因与有效路径均复现成立，问题在派发参数执行不合规，不在规则本身

### Pitfall-021 PreToolUse 闸门自伤误拦与 node -e 参数下标：模式须限定命令位置，argv 从 1 开始

- 报错特征/触发关键词：ERR_INVALID_ARG_TYPE、node -e、process.argv[1]、git reset --hard
- 最近复用：2026-08-15
- 状态：有效
- 场景：实现危险命令闸门钩子，命令内嵌 node 脚本做模式匹配
- 现象：① 搜索脚本内容含「git reset --hard」字样被自家闸门拦截（字符串级误拦）；② 改写为 node 匹配后所有调用报 `ERR_INVALID_ARG_TYPE: path undefined`，闸门 fail-open 放行
- 根因：① 模式未限定命令位置，命中字符串/脚本内容；② `node -e '脚本' 参数` 时 process.argv[1] 才是首个自定义参数，误用 argv[2]
- 有效路径：模式统一加 `(^|[;&|])\s*` 命令位置前缀；node -e 传参用 process.argv[1]；测试命令含关键字时改用脚本文件载体，避免测试自身触发闸门
- 教训：闸门类钩子先测「自伤」与「误拦」，再测「漏拦」；fail-open 下脚本崩溃=形同虚设，必须把语法/参数错误扼杀在测试阶段

### Pitfall-022 桌面端 MCP 服务器「启用」开关重开不持久：先核 config.toml 是否写入 enabled=true

- 报错特征/触发关键词：mcp_servers、enabled = true、write-config-value、config.toml
- 最近复用：2026-08-15
- 状态：有效
- 场景：ChatGPT/Codex 桌面端设置里启用 computer-use（或其他）MCP 服务器，重启 App 后开关又变关闭
- 现象：`~/.codex/config.toml` 的 `[mcp_servers.computer-use]` 始终是 `enabled = false`（含 8/2 以来全部备份）；UI 开关的写入错误被 `catch{}` 静默吞掉，无任何提示；2026-08-14 手动改全局 `enabled = true` 并加插件级 `plugins."computer-use@openai-bundled".mcp_servers.computer-use.enabled = true`，当日 75 秒内 App 未回写，但 2026-08-15 16:09 App 启动后整文件回写，全局项被重置为 false，插件级配置虽保留，`codex mcp list` 仍显示 disabled
- 根因：App 启动/退出时用内存态回写 config.toml，内存态对插件自带 MCP 默认 false（write-config-value upsert 未成功落盘可能是另一条失效路径）；直接改文件会被下一次 App 写盘覆盖，具体状态源待验证
- 有效路径：开关后立即查看 config.toml 是否出现 `enabled = true`；仅手动改文件不够，需在 App 写盘后由守护/巡检脚本改回（或删除全局项只留插件级开关，未验证）；2026-08-15 已落地守护方案：`~/.codex/scripts/keep_computer_use_enabled.sh`＋LaunchAgent `com.user.codex-computer-use-guard`（每 30 秒巡检，false→true 原子改写），`codex mcp list` 已显示 enabled，重启后是否持久待用户验证；改前备份；官方文档提供插件级持久开关字段但实测未能压制全局 disabled
- 教训：App 内开关状态与配置文件落盘都不可全信，判定以「重启后 `codex mcp list`」为准；排查顺序＝先看配置，再看进程与日志；凡 App 托管配置，先验证重启是否回写再交付修复结论

### Pitfall-023 macOS ps 多列输出 comm 截断致 grep 漏匹配：按进程名统计一律用 args 并加 LC_ALL=C

- 报错特征/触发关键词：ps -axo comm,rss、Illegal byte sequence、multibyte conversion failure、LC_ALL=C
- 最近复用：2026-08-05（受控复测：comm 截断 0 条，改 args+LC_ALL=C 统计成功）
- 状态：有效
- 场景：macOS 上按应用统计进程数与内存占用（如诊断 Chrome/Typeless 常驻开销）
- 现象：`ps -axo comm,rss | grep -i chrome` 返回 0 条；`sort`/`awk` 报 `Illegal byte sequence`、`multibyte conversion failure`；同一机器 `ps -axo args` 却含完整路径
- 根因：macOS ps 多列输出时 comm 列被截断到列宽（"Google Chrome" 只显示 "/Applications/Go"），单列输出不截断；管道含非 UTF-8 字节时，UTF-8 locale 下 sort/awk 报错
- 有效路径：进程名过滤/聚合一律用 `ps -axo pid=,rss=,args=` 取完整参数；统计命令统一前缀 `LC_ALL=C`；按关键词汇总用 `awk '{s+=$2;c++} END{...}'`
- 教训：grep 空结果先怀疑列截断而非「无进程」；macOS 取进程路径优先 args，不依赖 comm

### Pitfall-024 跨模型 API 成本对比不能只比单价：按账单四列逐项计价＋反查实付与列表价偏差

- 报错特征/触发关键词：缓存命中、实付、汇率、tokenizer、49.693M
- 最近复用：无
- 状态：有效
- 场景：用户给某平台账单（分日缓存命中/未命中缓存/输出等列＋实付金额），问同样 tokens 换到 OpenAI/Anthropic 要花多少
- 现象：只按「输入/输出」两档估算严重失真：GPT-5.6 Sol 同一用量（命中 522.29M/未命中 49.69M/写入 4.42M/输出 20.94M）标准档约 ¥7,914、Priority 档 ¥15,827、Batch 档 ¥3,957（三档差 4 倍）；首版曾把未命中 49.693M 误读成 496.9M（多一位数），用户核账单后修正；DeepSeek 该量按官方价全量应收 ¥102+，用户实付仅 ¥39.72
- 根因：账单含缓存命中、未命中、缓存写入、输出四个分项，命中/未命中单价差 50 倍；粘贴文本易多/丢位数，且「Tokens 显示值=命中列之和」只能校验命中列，未命中/输出数量级须与用户或截图二次核对；实付低于列表价多为赠送额度/活动折扣——本次已反向验证：¥39.72 精确等于输出 20.942M×$0.28/M×6.774，即输入命中/未命中均未计费（V4-Flash 公测期输入侧免费/赠送覆盖，官方文档亦注明「赠送余额优先抵扣、先于充值余额」）；汇率须用当日中间价（8/3 为 6.7898），拍脑袋用 7.15 会高估约 5%；不同模型 tokenizer 口径不同（Claude 4.7 代分词同文本可能多 35% token）
- 有效路径：先按账单四列×对应单价逐项汇总，注明服务档位（标准/Priority/Batch）与当日汇率；有峰谷价的平台以「全平峰价」为应扣下限（峰谷只会抬高、不会降低，本次全平峰 ¥102 vs 实付 ¥39.72＝下限的 39%）；再用「实付÷官方单价」逐项反推，能精确对上某列即该列计费、其余免费；偏差大时提示优惠/抵扣而非怀疑模型；同时核官方模型名（本次「DeepSeek-V3 Flash」查无条目，当前 Flash 实际为 V4-Flash）
- 教训：成本对比必须交代口径（token 分项、档位、汇率、缓存策略）；「同样 tokens」≠「同样工作量」

### Pitfall-025 macOS 硬件温度诊断权限边界：免密仅电池温度与热状态，核心温度需 sudo 或 GUI

- 报错特征/触发关键词：a password is required、sudo -n、ioreg、powermetrics
- 最近复用：无
- 状态：有效
- 场景：诊断 Mac 实时温度（CPU/GPU/SSD），未获 sudo 密码
- 现象：`ioreg -c AppleARMPMUTempSensor` 只见类名与 HID 属性、无数值；`ioreg -l -w0` 抓温度撞上 IOKitDiagnostics 巨型字典；`sudo -n` 返回 `a password is required`
- 根因：Apple Silicon 温度值经 root/HID 受限通道，普通用户 ioreg 读不到数值（待验证：是否所有机型一致）；powermetrics 必须 root
- 有效路径：免密可读 `ioreg -rn AppleSmartBattery` 的 `Temperature`/`VirtualTemperature`（0.01°C，实测 3051≈30.5°C）与 `pmset -g therm` 热警告；核心温度让用户自行执行 `sudo powermetrics -n 1 --samplers smc -f text`（密码不经过助手），或读已装 GUI（Macs Fan Control）
- 教训：先分清「免密可读/需 sudo/需 GUI」三档再下结论；为测温度索要密码违反安全边界，改为给用户一条可自跑命令

### Pitfall-026 macOS 无 sudo 硬件诊断工具箱：GPU 利用率/刷新率/Apple NVMe SMART 均免密可读；brew 可能根本没装

- 报错特征/触发关键词：brew、Permission denied、AGXAccelerator、Device Utilization %、smartctl
- 最近复用：无
- 状态：有效
- 场景：Mac 性能诊断（GPU 持续忙、SSD 寿命、屏幕刷新率），不想也不能用 sudo 密码
- 现象：`brew` 命令不存在，但 `~/Library/LaunchAgents` 有 homebrew 残留 plist（redis 等未运行）；`/dev/disk0` 直接读返回 `Permission denied`
- 根因：Homebrew 曾安装后卸载/迁移，残留 LaunchAgent 造成「好像装了」的假象；Apple 设备节点默认不允许普通用户直读
- 有效路径：① GPU 利用率：`ioreg -rc AGXAccelerator -w0 | rg 'Device Utilization %'`（免 sudo，实测空闲态 52–62% 属异常）；② 刷新率/在屏窗口：`swift -e` 调 CoreGraphics（`CGDisplayCopyDisplayMode().refreshRate`、`CGWindowListCopyWindowInfo`）查 120Hz 与悬浮覆盖窗口；③ SSD 健康：有 CommandLineTools 时从官方 GitHub 源码在 /tmp 编译 smartmontools（`./configure && make`，产物为根目录 `smartctl` 文件），`smartctl -a disk0` 经 IOKit 免 sudo 直读 Apple NVMe（实测 Percentage Used 1%、Available Spare 100%、SMART PASSED；Error Log 读取失败是 Apple 固件限制，非故障）；④ 清理临时产物用 `mv` 到 `~/.Trash`（本环境安全策略禁 rm -f）
- 教训：不要因「brew 不在」就放弃测量，先核 CLT 与官方源码；Apple NVMe 的 SMART 免 sudo 可读，先实测再下结论

### Pitfall-027 桌面 App 隐藏配置/参数定位：asar 解包 + rg 关键词，不靠 UI 猜

- 报错特征/触发关键词：app.asar、@electron/asar、enabledOpusCompression、sampleRate、bitrate、opusWorker
- 最近复用：无
- 状态：有效
- 场景：给 Electron 桌面应用（Typeless 2.2.0）调识别/音频配置，UI 无相关开关
- 现象：app-settings.json 只有窗口/快捷键/麦克风等常规键，未见识别相关项；官方文档只讲麦克风与个人词典，无语速/精度设置
- 根因：识别链路参数（Opus 码率 16kbps、帧 20ms、采样率 32kHz、降噪开关）硬编码在打包 JS 内，不经设置 UI 暴露（待验证：仅本次版本）
- 有效路径：`npx --yes @electron/asar extract <App>.app/Contents/Resources/app.asar /tmp/x` 解包；再 `rg` 搜 `enabledOpusCompression|sampleRate|bitrate|opusWorker` 等键与 worker 脚本，即可定位可写配置键与硬编码参数；改 app-settings.json 前先确认应用已退出，避免运行时被覆盖
- 教训：调第三方 App 识别质量，先解包看「上传前音频是否被压缩/采样率/降噪」等链路参数，再决定改配置还是只能改行为习惯；禁止凭 UI 外推「没有这个设置」

### Pitfall-028 macOS CLI 调 Speech 框架触发 TCC 隐私违规直接 abort：无 Bundle/权限声明不可用

- 报错特征/触发关键词：__TCC_CRASHING_DUE_TO_PRIVACY_VIOLATION__、SFSpeechRecognizer、NSSpeechRecognitionUsageDescription
- 最近复用：无
- 状态：有效
- 场景：想用本机 SFSpeechRecognizer 对语音文件做本地转写对比（Typeless 快语速前后效果测试）
- 现象：swift 脚本申请语音识别授权时崩溃，堆栈含 `__TCC_CRASHING_DUE_TO_PRIVACY_VIOLATION__`，无友好报错
- 根因：无 App Bundle 与 `NSSpeechRecognitionUsageDescription` 的 CLI 进程申请语音识别权限，TCC 视为隐私违规直接终止（macOS 15）
- 有效路径：命令行场景改用无权限依赖的客观指标（numpy 频带能量/SNR 对比）；确需 Apple 语音识别须做成带 Info.plist 声明且经用户授权的正规应用
- 教训：本地语音类验证先确认权限载体（Bundle + usage description）；TCC 类权限缺失表现为进程崩溃而非报错提示，不要误判为脚本语法问题

### Pitfall-029 launchd 定时任务里的 osascript 被 TCC 静默拒绝：交互式 exec 正常、后台全 FAIL，且 RC=0

- 报错特征/触发关键词：launchd、osascript、System Events、TCC、-1728、kickstart
- 最近复用：无
- 状态：有效
- 场景：LaunchAgent 每 5 分钟跑 shell 脚本，用 osascript/System Events 枚举并关闭 Codex 闲置线程窗口（2026-08-03 实测）
- 现象：同一脚本在 Codex exec 交互上下文手动运行正常（能列出窗口标题）；launchd 定时运行连续 24 次全 FAIL，日志仅见脚本自记的「无法读取窗口列表」，osascript 自身 RC=0、stderr 为空，外层无法区分 TCC 拒绝与其他错误；用户不在场时无任何弹窗
- 根因：launchd 后台进程（负责进程非终端/App）调用 System Events 未获辅助功能授权，TCC 静默拒绝；脚本的 `on error` 把失败包装成 `__ERR__` 返回，掩盖了真实 -1728
- 有效路径：脚本内 osascript 失败分支必须同时检查退出码与哨兵输出并明确记录「疑似 TCC」；授权对象是 launchd 任务的负责进程 /bin/bash（2026-08-03 实测：用户在辅助功能里勾选 bash 后 kickstart 立即恢复，无需单独授权 osascript）；授权后 `launchctl kickstart -k gui/$(id -u)/<label>` 即时复测，别等 5 分钟周期
- 教训：后台定时任务复用「交互式验证通过」的 UI 自动化代码时，权限上下文不同，必须用 kickstart 强制跑一次并查日志确认；FAIL 类监控任务要能区分「没权限」和「正常无事」，否则会误以为已生效

### Pitfall-030 OneDrive 仅在线文件打不开报「无权限」：dataless 占位读取超时，根因多为代理 TLS 中断

- 报错特征/触发关键词：dataless、compressed、Operation timed out、Error Code -1200、SSL_ERROR_SYSCALL
- 最近复用：无（2026-08-05 曾被跑偏子代理伪回写，未真实解决，已撤销）
- 状态：有效
- 场景：Mac 上 OneDrive 图片/文件双击打开报「未能打开该文件，因为你没有查看它的权限」，且不确定是否所有文件受影响
- 现象：`ls -lO` 显示 `compressed,dataless` 标志；`file`/`sips` 读取该文件返回 `Operation timed out`；已本地化的文件（无 dataless）读取正常；OneDrive SyncEngine 日志出现 `Error Code -1200`、`An SSL error occurred`、`OneAuth ... Network infrastructure failure`
- 根因：dataless 是「仅在线占位文件」，打开需经 File Provider 实时下载；下载通道因代理（如 FlClash）对微软端点的 TLS 握手失败而中断，Finder 把下载失败包装成无权限提示（待验证：官方是否统一此错误映射）
- 有效路径：`stat -f "%Sf" <文件>` 看是否 dataless（本机 522 个文件有 139 个占位）；用 `curl --noproxy '*'` 与 `curl -x http://127.0.0.1:7890` 对比 `https://graph.microsoft.com/`、`https://login.microsoftonline.com/`，直连 200/302、代理 SSL_ERROR_SYSCALL 即定位；修复代理节点或让微软域名绕过代理后，退出并重开 OneDrive，双击文件即自动下载；实测 OneDrive 不读 macOS 代理绕过列表（ExceptionsList 已含微软域名仍走代理），把系统代理关闭后 dataless 文件可立即本地化（0.7s 下载 775KB），说明直连可用
- 教训：占位文件打不开先查 dataless 标志与 File Provider 下载日志，再查网络代理 TLS，不要按提示去改 POSIX 权限；FlClash 订阅地址返回 403 会让启动后 UI 无响应、代理不接管，数据库 `auto_update=0` 可跳过启动拉订阅但会失去自动更新；改第三方代理应用前先备份 plist/db/配置文件

### Pitfall-031 macOS 系统 python3 的 urllib 请求 https 报 SSL 证书错误：统一改 subprocess 调 curl 后端

- 报错特征/触发关键词：SSLCertVerificationError、CERTIFICATE_VERIFY_FAILED、urllib、unable to get local issuer certificate
- 最近复用：无
- 状态：有效
- 场景：2026-08-03 多平台只读探测（B 站/抖音/小红书），python3 `urllib.request.urlopen` 请求 https 接口
- 现象：`SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate`；即使换 `ssl._create_unverified_context()` 也非首选（跳过校验等于把数据完整性交给运气）
- 根因：macOS 自带 python3 未捆绑 CA 证书库，Python 找不到系统证书链（待验证：具体证书路径行为随 Python 版本/安装方式变化）
- 有效路径：`subprocess.run(['curl','-s','-m','20','-A',UA,'--compressed','-w','\n@@%{http_code}',url])`，curl 自带系统证书链；输出按最后 `@@状态码` 切分（`p.stdout.rpartition('@@')`）；或安装 Python 证书/换 brew python（属安装类敏感操作，需先确认，未执行）
- 教训：探测阶段先确认工具链证书可用，不要在 SSL 报错上反复改代码；curl 后端模式跨平台、零依赖、可同时拿状态码，适合做爬虫统一底座

### Pitfall-032 HTTP 200 不代表返回期望格式：B 站 oEmbed 返回 HTML 错误页，解析前必须校验 body

- 报错特征/触发关键词：oembed、json.loads、HTTP 200、bilibili.com
- 最近复用：无
- 状态：有效
- 场景：2026-08-03 B 站 oEmbed 探测 `https://www.bilibili.com/oembed?url=...`
- 现象：HTTP 200，body 是 HTML 错误页而非 JSON，`json.loads` 直接抛异常；同厂 `view`/`popular` 接口正常返回 `code:0` 结构化 JSON
- 根因：oEmbed 端点对当前分享场景不可用或需额外参数（待验证：官方文档/参数组合）；200 只代表请求被受理，不代表格式正确
- 有效路径：解析前先看 body 首字符或 Content-Type；以实测可用的 `view`/`popular` 为准；curl `-w` 状态码与 body 一起看，不单独信状态码
- 教训：接口可用性以「取到预期结构化数据」为判据，状态码和猜测不算；平台接口差异大，未实测不写死结论

### Pitfall-033 Chrome headless --dump-dom 挂起超 90 秒：需要 JS 渲染的页面改 CDP 常驻实例

- 报错特征/触发关键词：--headless=new、--dump-dom、--virtual-time-budget、CDP、user-data-dir
- 最近复用：无
- 状态：有效
- 场景：2026-08-03 抖音视频页（纯 JS 壳，需渲染后取数据），Chrome 150 用 `--headless=new --dump-dom --virtual-time-budget=15000` 抓 DOM
- 现象：进程运行超 90 秒无任何输出，会话无法结束，只能按 `user-data-dir=/tmp/douyin_dump_*` 特征 pkill；改用普通 Chrome＋`--remote-debugging-port`＋CDP 驱动后 12 秒内完成渲染并取到数据
- 根因：待验证（可能 headless 被页面长连接/后台请求拖住，或与已有 Chrome 实例冲突；未深挖）
- 有效路径：需要 JS 渲染的站点统一走 3.4 的专用 Chrome CDP 模式：起普通实例（`--remote-debugging-port=9223 --user-data-dir=/tmp/xxx`）→ Node WebSocket 连 DevTools → `Page.navigate` → 等 8~12 秒 → DOM/Network 取数；headless 挂起即换路，不硬等
- 教训：无头模式不是万能快路径，先小样本验证；挂起后用进程特征精准清理，不误杀用户浏览器与其他测试实例

### Pitfall-034 云转写延迟排查先测链路：lsof 看代理常驻连接＋直连/代理对比耗时＋上行实测

- 报错特征/触发关键词：lsof、127.0.0.1:7890、networkQuality、-1200
- 最近复用：无
- 状态：有效
- 场景：Typeless 口述后「等好多秒才有反应」，需判断是否网络/代理/OneDrive 所致
- 现象：Typeless 常驻 TCP 连接到 127.0.0.1:7890（走 FlClash 代理）；`curl` 对比 api.typeless.com 直连 0.6s vs 代理 6.0–6.6s；`networkQuality` 报 SSL -1200（与 OneDrive 排障同款代理 TLS 故障）；本机直连上行波动 0.2–1.2 MB/s
- 根因：① 无损 WAV 较原 Opus OGG 上传量大约 15 倍（24s 口述≈768KB），慢时上行需 3–4s；② 代理节点慢且 TLS 不稳（21:37 OneDrive 排障期间重启过 FlClash）；③ 本机 swap 3.1GB、load 3.6 放大感知延迟
- 有效路径：`lsof -nP -iTCP -sTCP:ESTABLISHED | rg 应用名` 看是否常驻连代理端口；`curl` 同 URL 直连与 `-x http://127.0.0.1:7890` 各测一次对比耗时；`networkQuality` 失败码 -1200 即代理 TLS 异常佐证；`dd + curl -T` 测上行；最后查会话日志确认近期代理/同步事件时间窗
- 教训：App 云服务延迟先量化「上行体积×速度＋代理 RTT」，再归因内存/App；改无损音频后必须同步评估上传量对延迟的影响

### Pitfall-035 FlClash 改配置文件后规则不生效：核心用缓存配置，需在 UI 重新导入/应用，且强制重启可能让节点变差

- 报错特征/触发关键词：FlClash、config.yaml、DIRECT、7890
- 最近复用：无
- 状态：有效
- 场景：给 FlClash 加 typeless.com→DIRECT 直连规则（改 config.yaml 与活动订阅 YAML）
- 现象：文件语法校验通过、内容确认写入；但 curl 经 7890 访问 api.typeless.com 仍 5s 超时（规则未命中），而既有 DIRECT 规则（baidu）正常；强制重启 FlClash 后同样不生效，且 api 经代理从 6.6s 可通恶化为 5s 超时
- 根因：FlClashCore 运行配置来自 UI 内存/缓存，不直接读磁盘上的 config.yaml（待验证：具体加载链路）；仅改文件不触发重新应用；强制 pkill 重启可能改选节点（selected_map 缓存）导致链路变差
- 有效路径：改规则后在 FlClash UI 里重新导入/应用该订阅，或经 UI 重载；不要仅改 YAML 后强制重启；改动前备份，验证用「同域名 curl 经代理耗时」对照
- 教训：代理类配置「文件已改」≠「运行已生效」；验证以实际链路耗时/命中为准；用户叫停后先还原配置文件，不再反复重启

### Pitfall-036 Electron asar 完整性校验拦截改包：先副本试跑，fuses write off＋重打包＋临时重签名可落地

- 报错特征/触发关键词：EnableEmbeddedAsarIntegrityValidation、@electron/fuses、codesign、ditto、app.asar
- 最近复用：无
- 状态：有效
- 场景：Typeless 无码率设置（Opus 16k 硬编码），需改包提到 64k 实现 4 倍体积
- 现象：`@electron/fuses read` 显示 EnableEmbeddedAsarIntegrityValidation Enabled，直接改 app.asar 会在启动时被完整性校验拦截；安装包原始签名为 Developer ID（arm64，runtime）
- 根因：Electron ≥20 打包应用默认开启 asar 完整性校验，校验哈希内嵌在 Mach-O，改 asar 必失败
- 有效路径：① `ditto` 整包备份到 /tmp；② 副本试跑：`npx @electron/fuses write --app 副本 EnableEmbeddedAsarIntegrityValidation=off` → asar 解包改 opusWorker.js 的 `'bitrate':0x3e80` 为 `0xfa00`（16000→64000）→ 重打包替换 → `codesign --force --deep --sign -` 临时重签名 → 副本启动验证；③ 正式安装同样操作，`open -a` 启动验证无崩溃；④ 用改后 worker 直跑一段 WAV 验证实际码率（实测 64k、压缩比 3.94）
- 教训：改 Electron 应用先查 fuses 再决定路径；高风险改包必须「整包备份＋副本验证＋正式替换＋可回滚」，临时签名会随自动更新失效需重打

### Pitfall-037 临时重签名后 TCC 授权全部失效：系统隐私出现旧「patched」条目，用 tccutil reset 后重新授权

- 报错特征/触发关键词：tccutil reset、patched、adhoc、Designated Requirement
- 最近复用：无
- 状态：有效
- 场景：Typeless 改包后临时 adhoc 重签名，用户发现「隐私与安全性」出现 patched 条目且麦克风/辅助功能授权失效
- 现象：用户给 patched 条目开权限，正式 Typeless 仍提示无权限；因 adhoc 签名改变 Designated Requirement，TCC 按「Bundle ID＋签名要求」匹配，原授权与现签名不匹配
- 有效路径：退出应用后 `tccutil reset Microphone now.typeless.desktop` 与 `tccutil reset Accessibility now.typeless.desktop`，重启应用重新触发授权弹窗；旧 patched 条目同 Bundle ID 一并被重置，可忽略或关闭
- 教训：临时重签名等于换「应用身份」，必须先规划 TCC 重置；改包前把权限失效列入风险清单，避免用户误授权错条目

### Pitfall-038 afconvert 输出扩展 WAV 头（0xFFFE）致 libopusenc 编码返回 -2：先转标准 PCM 头再喂编码器

- 报错特征/触发关键词：afconvert、0xFFFE、WAVE_FORMAT_EXTENSIBLE、libopusenc、-2
- 最近复用：无
- 状态：有效
- 场景：用 macOS afconvert 把 Opus OGG 解码成 WAV 后，再喂 Typeless 的 libopusenc worker 编码，全部返回 -2（缓冲与文件模式均失败）
- 现象：`afconvert -f WAVE -d LEI16@16000` 生成的 WAV fmt chunk 为 40 字节、format tag 0xFFFE（WAVE_FORMAT_EXTENSIBLE）并带 FLLR 附加块；应用自录音频为标准 16 字节 PCM fmt（tag 1）；libopusenc 按标准 WAV 偏移解析得到错误 data 长度→-2
- 有效路径：先按 RIFF 块解析出 PCM 数据，用标准 44 字节 PCM 头重写（`wave` 模块 setnchannels/setsampwidth/setframerate + writeframes），再交给编码器即可；解码侧 afconvert 输出无碍，只有编码侧挑剔
- 教训：跨工具链传 WAV 先核对 fmt tag 与块布局；第三方编码器 -2 类错误优先怀疑「WAV 头非标准」，不要直接怀疑时长/数据问题

### Pitfall-039 语音转写实体名歧义（herness→Harness→Hermes）：深挖研究对象前先做实体消歧

- 报错特征/触发关键词：herness、Harness、Hermes、hermes-agent
- 最近复用：无
- 状态：有效
- 场景：2026-08-03 用户语音列出六个工具名，其中一项转写为「herness」，被误判为 Harness 并展开整支深挖
- 现象：按 Harness 产出「Model+Harness=Agent、DeepSeek Harness、MemHarness」等一整条研究线；用户随后更正第 6 项实为 Hermes（Nous Research hermes-agent），整支研究结论与用户目标不匹配，需撤回重做
- 根因：语音转写名词存在多个相近实体（Harness/Hermes），未在展开前核对「这个名词指哪个具体产品/项目」；相近词的行业概念（Harness 工程）真实存在，更易被当成默认解释
- 有效路径：收到语音转写的对象清单时，先对每个名词做实体消歧——检索官方仓库/官网/官方文档确认「是什么」，无法唯一对应时先向用户确认再深挖；输出按对象名锚定一手来源（本次 Hermes 锚定 NousResearch/hermes-agent 官方 README 与 v0.19.1 发布说明）
- 教训：研究对象清单先消歧、后挖掘；宁可多花一次确认调用，不产出整支可废弃的研究线

### Pitfall-040 Codex 桌面版同事件多钩子组只执行第一组：合并进同一脚本，不依赖多组配置

- 报错特征/触发关键词：hooks.json、PreToolUse、doom_loop、codex_doom_loop_hits.log
- 最近复用：无
- 状态：有效
- 场景：2026-08-04 在项目 `.codex/hooks.json` 的 PreToolUse 事件下追加第二个钩子组（危险闸门之后挂 doom_loop 反循环脚本）
- 现象：第二个钩子组从未被调用（脚本首行无条件写标记文件验证：`/tmp/codex_doom_loop_hits.log` 不存在）；第一个钩子组正常（`diskutil eraseVolume` 探针被拦截）；应用重启后仍不生效；hooks.json 语法与脚本可执行权限均正常
- 根因：当前 Codex 桌面版对同一事件仅执行第一个匹配钩子组（待验证：官方实现细节与版本差异；CLI 行为未测）
- 有效路径：把多组逻辑合并进第一个钩子组的同一脚本（`pre_tool_use_gate.sh` 黑名单通过后调用 `doom_loop.sh`）；单组配置实测生效；脚本内容按次读取、改动立即生效，hooks.json 仅启动时读取、改后需重启
- 教训：hook 能力以真实链路 E2E 为准，不能只信配置 schema；新增钩子先做「无条件标记→跑一条命令→查标记」的最小探针，确认被调用再写业务逻辑

### Pitfall-041 Codex 桌面版 AX 快照不可靠＋面板标签语义易误判：用 JXA 按坐标遍历，禁止按名称猜测“哪个标签是主会话”

- 报错特征/触发关键词：JXA、AppleScript、entire contents、AX、坐标遍历
- 最近复用：无
- 状态：有效
- 场景：2026-08-04 标定右侧面板自动关闭（审阅/文件/浏览器/终端/侧边聊天），需要读取面板开关状态并定位关闭按钮
- 现象：AppleScript `get entire contents of window` 多次返回过期/不完整树——同一时刻 JXA 按坐标遍历能看到会话内容与标签条，AppleScript 快照却显示“无标签、无聊天文本”，曾误判“主会话被关闭”并反复点击恢复；标签名动态（主会话标签=线程标题，文件面板标签=项目文件夹名，浏览器标签=网页标题），按名称猜测“deepseek coding agent 标签”曾误认为主会话
- 根因：待验证（应用渲染树大且变化频繁，AppleScript 全量快照可能截断或走缓存；AX 暴露结构随界面状态变化）
- 有效路径：状态读取统一用 JXA 递归遍历＋位置过滤（角色、名称、描述、坐标、尺寸）；关闭标签=外层标签按钮的子按钮（description 含「关闭…标签页」），点后延迟 2-3 秒再遍历确认；主会话保护以“线程标题（session_index 的 thread_name）”精确匹配，不猜项目名
- 教训：对桌面 App 的 AX 自动化，先做「两个 API 同一时刻对拍」验证快照可信度；读不到状态不要立刻判定“窗口关了”，先换遍历方式复核；标签/按钮名称永远以实测结构为准，不按字面推断

### Pitfall-042 launchd 定时脚本里外部命令依赖交互 PATH：node 找不到导致解析环节静默失效，只留 stderr 痕迹

- 报错特征/触发关键词：node: command not found、launchd、PATH、kickstart、close_idle_codex_panels.sh
- 最近复用：无
- 状态：有效
- 场景：2026-08-04 面板自动关闭脚本 `~/.codex/scripts/close_idle_codex_panels.sh`（LaunchAgent 每 5 分钟运行）用 `node -e` 解析 JXA 输出；交互 shell 手动跑正常，定时跑不出关闭动作
- 现象：`~/.codex/idle-panels-closer.err.log` 出现 `close_idle_codex_panels.sh: line 178: node: command not found`；脚本自记日志仅见「RUN/JSON解析失败」，无 FAIL，用户从主日志看不出故障；交互式 exec 跑同一脚本正常（交互 PATH 含 /usr/local/bin）
- 根因：launchd 默认 PATH 仅 `/usr/bin:/bin:/usr/sbin:/sbin`，不继承交互 shell 的 PATH；node 装在 `/usr/local/bin`，定时运行找不到
- 有效路径：脚本内外部命令一律用绝对路径（本机 `/usr/local/bin/node`），或脚本开头显式 `export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"`；安装时把 `command -v node` 的绝对路径固化为变量；验证用 `launchctl kickstart -k gui/$(id -u)/<label>` 即时复测并同时看 stderr 日志与脚本自记日志
- 已修复（2026-08-04）：面板脚本改为 `NODE="${CODEX_PANEL_NODE:-/usr/local/bin/node}"` 并用 `"$NODE" -e` 调用，无其他非系统命令依赖；手动 FORCE+DRY_RUN 全链路验证 `ROUNDS 1`，launchd kickstart 后 err 日志无新增报错
- 教训：定时任务「手动跑正常」不能证明 launchd 下正常；检查故障必须先看 StandardErrorPath 落盘文件，再对照脚本自记日志，两个通道都干净才能判定健康

### Pitfall-043 Codex 桌面版线程窗口 AX 标题固定为「ChatGPT」：按窗口标题匹配线程名的闲置关窗脚本永久空转

- 报错特征/触发关键词：ChatGPT、AX title、updated_at、session_index.jsonl、mtime
- 最近复用：无
- 状态：有效
- 场景：2026-08-04 复核 `~/.codex/scripts/close_idle_codex_windows.sh`（LaunchAgent 每 5 分钟、闲置 60 分钟关窗、当前 DRY_RUN=1）；Pitfall-029 的 launchd TCC 问题已解决，日志累计 100+ 次 RUN 无 FAIL
- 现象：日志每 5 分钟稳定输出「SKIP 非线程窗口：ChatGPT」「RUN 窗口=1 闲置待关=0 本次处理=0」；osascript 枚举当前在线 ChatGPT/Codex 窗口名唯一为 `ChatGPT`，session_index.jsonl 中当前线程名「确认闲置Codex窗口是否关闭」未出现在窗口 AX 标题；脚本剥掉「ChatGPT」后缀后标题为空，命中非线程分支跳过
- 根因：当前 ChatGPT.app（150.0.7871.182）主窗口 AX title 固定为应用名，线程标题不进入窗口名；脚本以「窗口标题与 thread_name 互为前缀」匹配线程，导致永远无匹配（待验证：是否覆盖所有版本与多窗口场景）
- 有效路径：定位线程不能靠窗口标题，改用 JXA 遍历窗口内元素/标签（复用 Pitfall-041 的坐标遍历法）；若要真正释放内存，空闲超时应直接 quit 整个 ChatGPT 进程——仅点关窗不退出进程，内存释放有限；DRY_RUN 与正式模式均应增加「存在在线会话但每轮处理数为 0」的计数/告警，避免静默空转
- 补充（2026-08-04 实测）：`~/.codex/session_index.jsonl` 的 `updated_at` 是线程创建时间而非最后活动时间——文件 mtime 停在创建时刻 09:54:15，用户 09:58/10:02 发消息后也未刷新；真实的「最后消息时间」在 `~/.codex/sessions/**/*.jsonl` 的文件 mtime（旧线程文件 mtime 停在各自最后写入时刻）。判定闲置应取会话文件最新 mtime，不能用 updated_at
- 教训：监控类脚本「日志无 FAIL、每轮 RUN」不等于任务生效，必须核对每轮处理数是否非零；写 UI 自动化匹配逻辑前，先实测 AX 暴露的窗口标题是否含业务标识

### Pitfall-044 脚本测试覆盖参数未生效＋ps|grep 自匹配：无害「计算器测试」误退出生产应用

- 报错特征/触发关键词：APP_NAME=Calculator、ps ax -o args=、grep、自匹配、DRY_RUN
- 最近复用：无
- 状态：有效
- 场景：2026-08-04 给 `close_idle_codex_windows.sh` 加「退出 ChatGPT 进程」功能，想用环境变量把目标临时改为计算器做端到端测试；脚本头部只把 IDLE_MINUTES/DRY_RUN/INDEX 等写成 `${VAR:-默认}`，APP_NAME/APP_PATH/APP_BUNDLE_ID 仍是硬编码
- 现象：`APP_NAME=Calculator ... bash 脚本` 的日志却显示目标仍是 ChatGPT，10:01 当前 Codex 会话被真实退出、exec 会话中断（输出 aborted），计算器只是被 `open -a` 打开未退出；修复覆盖参数后，`ps ax -o args= | grep -F "$APP_PATH"` 又永远匹配——grep 自身与父 shell 的 argv 都含该路径，进程检测与退出轮询永不跳出，测试跑满 40 秒并误报 ERR
- 根因：1) 声称可测试的参数没真正参与变量展开，测试命令与生产行为不一致；2) 用 `ps | grep -F "$PATH"` 检测进程时，执行 shell 的命令行里若包含同一路径（内联环境变量赋值），grep 必然自匹配；掩码正则 `[/]path` 只挡 grep 自身 argv，挡不住父 shell argv
- 有效路径：所有可覆盖变量统一 `${VAR:-默认}`，测试先跑 DRY_RUN=1 核对日志里的目标名；带副作用的端到端测试用无害应用（计算器）＋环境文件注入（`set -a; . /tmp/test.env; exec bash 脚本`，使路径不出现在任何 argv）；进程存在性检查用掩码正则 `MASKED="[/]${PATH#/}"` 并在 launchd（argv 干净）下验证；trap 同时挂 EXIT INT TERM 防锁目录残留
- 教训：覆盖变量的生效性必须先用 DRY-RUN 日志验证，再执行真实副作用路径；「退出/杀死某进程」类脚本的测试与生产 argv 环境必须一致，任何自匹配都会把「已退出」误判为「仍存活」

### Pitfall-045 Chrome AppleScript 标签级属性不可用（URL/active/pinned/index 取不到）：标签级闲置判定改窗口级＋System Events AXMain 判前台

- 报错特征/触发关键词：tab.URL()、tab.pinned()、frontWindow()、AXMain
- 最近复用：无
- 状态：有效
- 场景：2026-08-04 设计 Chrome 闲置自动关闭（对标 Codex 闲置关窗），原想按「最后使用时间」逐标签关闭，或至少读取 URL/固定标签做保护
- 现象：`tab.URL()`、`tab.active()`、`tab.pinned()`、`tab.index()` 全部报「不能转换类型/不能获取对象」，仅 `title()`/`loading()` 可读；`Application('Google Chrome').frontWindow()` 报「信息无法识别」；System Events 的 `value of attribute "AXMain"` 能正确标记前台窗口（实测返回 true）
- 根因：本机 Chrome 150 的 AppleScript 字典对 tab 属性暴露不全（待验证：具体版本差异与官方支持矩阵）
- 有效路径：标签级只读 title/loading；窗口级用 System Events `{name, value of attribute "AXMain"}` 判前台，Chrome 字典 `windows()[i].id()/title()` 关联；闲置判定用「前台窗口最后出现时间」状态文件，不做逐标签时间戳；关闭用整窗 close，保护前台窗口/最后一个窗口/标题含下载的窗口；先 dry-run 观察再开真关
- 教训：Chrome 自动化先探测 tab 字典再定粒度；读不到就降级到窗口级，不硬做逐标签；前台判定优先 System Events AXMain，不依赖 Chrome 的 frontWindow 属性

### Pitfall-046 Electron CDP Fetch.continueRequest 的 url 改写静默无效；Typeless 词典删除须走 UI 悬停渲染

- 报错特征/触发关键词：Fetch.continueRequest、Network.requestWillBeSent、418、mouseover、mouseenter、user/dictionary/delete
- 最近复用：无
- 状态：有效
- 场景：2026-08-04 批量删除 Typeless 词典 47 条词条。词典数据在云端且 Node/页面内独立 fetch 均被 418 风控拦截，只能驱动 App 自身发请求；先尝试 CDP Fetch 拦截 list 请求并改写 URL 为 delete 接口
- 现象：改写后 `Network.requestWillBeSent`/`responseReceived` 显示请求仍以原 list URL 发出（200/418），delete 一条未生效；之后改走 UI 点击，删除请求实际 URL 为 `POST https://api.typeless.com/user/dictionary/delete`，ID 在 POST body（`{"user_dictionary_id":...}`），不在 URL query
- 根因：Electron 33（Chromium 130）的 `Fetch.continueRequest` 对普通请求的 `url`/`method` 改写静默忽略，仅对已重定向请求生效（待验证：官方行为与版本差异）；Typeless 词卡删除按钮仅在卡片 `onMouseEnter` 后渲染，搜索态/未悬停无按钮；词典顶部筛选 tab（所有/自动添加/手动添加）影响搜索，在「自动添加」下搜手动词返回 0
- 有效路径：JS 向词卡根节点派发 `mouseover`(bubbles)+`mouseenter` 即可触发 React 渲染 `.actions`，再 `.click()` 删除图标与确认弹窗「删除」按钮；逐条先切「所有」再搜索精确词；删除结果以网络响应体 `{"status":"OK","msg":"success",...}` 为准，不要用 `/true/` 判断
- 教训：验证请求改写前先打真实 Network 事件确认 URL 是否变化，不能只信 Fetch 事件；批量删除优先走 App 自身 UI/API 链路，失败时先查请求 URL 与 body 字段，别在 DOM 空态（本地状态被错误响应清空）上做判断

### Pitfall-047 禁用 Electron 应用自动更新：只改更新源不够，已下载的更新缓存必须一并禁用

- 报错特征/触发关键词：update.zip、app-update.yml、typeless-updater、pending
- 最近复用：无
- 状态：有效
- 场景：2026-08-04 用户要求禁止 Typeless 自动更新，避免补丁版被覆盖和反复弹重启提示
- 现象：App 已下载 165MB update.zip 到 `~/Library/Caches/typeless-updater/`，即使更新源不可达，缓存里的 `pending/update.zip` 仍会在启动时触发「更新已就绪」提示
- 根因：electron-updater 下载完成后在缓存目录落盘 pending 状态，启动时优先识别已下载更新；只改 `app-update.yml` 的 `url` 只能阻止未来检查，不能清除既有下载态
- 有效路径：退出 App → 改 `Contents/Resources/app-update.yml` 的 url 为本机无效地址（`http://127.0.0.1:1/`）→ 把缓存目录 `update.zip`/`pending` 重命名（可逆，不删除）→ `codesign --force --deep --sign -` 重新 adhoc 签名（否则修改资源后 bundle 签名失效）→ 重启验证缓存无新包、主进程正常
- 教训：禁 Electron 自动更新要「更新源 + 已下载缓存」双管齐下；改 app 内资源后必须重签；恢复更新＝还原 app-update.yml 的 url（备份到 /tmp）或官网重装

### Pitfall-048 DeepSeek 直连首字慢定位：先拆四段时间线并量化请求体大小，再归因

- 报错特征/触发关键词：feedback_log_body、logs_2.sqlite、api.deepseek.com/responses、首字延迟
- 最近复用：无
- 状态：有效
- 场景：2026-08-04 用户反馈 Codex 用 DeepSeek 直联，每轮发送后要等 6-7 秒（重任务 17-42 秒）才开始；明确不改思考强度、代理与自动压缩限制
- 现象：提交→HTTP 发送 0-3 秒、响应头 1-6 秒，但首文字事件延迟 17-42 秒；同一线程请求体从 65KB 涨到 497KB（input 历史占 91%），首字延迟同步从 17 秒升到 42 秒；小提示直连实测 max 档仅 1.2 秒
- 根因：主因是 `model_reasoning_effort=max`（用户保留不改）；放大因素是线程内工具输出/历史全量重发致请求体膨胀，DeepSeek 大上下文 prefill+推理显著变慢（待验证：服务端是否缓存 prompt 前缀）
- 有效路径：用 `~/.codex/logs_2.sqlite` 的 `feedback_log_body LIKE '%POST to https://api.deepseek.com/responses%'` 量化请求体长度，用 `codex_core::stream_events_utils` 的 reasoning 项创建/完成时间拆分推理段；控制上下文的低成本手段＝新开线程、手动 `/compact`、避免大输出进对话
- 教训：诊断"慢"先拆四段（提交→发送→响应头→首事件→首文字），请求体大小是免费且有效的量化指标；不先量化就归因到网络/代理容易误判

### Pitfall-049 子代理完成但 final 报告未传回主线程：以产物＋主线程同标准复核兜底，不无限重等

- 报错特征/触发关键词：final、子代理、报告未传回、等待超时、followup
- 最近复用：2026-09-02
- 状态：有效
- 场景：2026-08-05 主线程派子代理独立审查《荒岛余生影评》，子代理已完成任务、要求其 final 通道返回四块结论
- 现象：子代理状态显示完成，但详细报告未传到主线程；followup 重发后仍未收到，多次等待超时
- 根因：早期记录待验证；2026-09-02 本次具体根因已确认：父线程把 `wait_agent` 的超时结果当作唯一状态依据，未先调用 `read_thread` 核实仍在运行的线程，就调用了终止性的 `close_agent`。
- 有效路径：每轮等待 120 秒后先查询状态；仍运行则继续等待，已完成但报告未传回则读取 `previous_status`、线程记录或落盘产物；只有明确启动/模型/账户/任务失败才用同一任务卡重试一次，随后由主线程按同一验收标准复核兜底；不反复重发、不无限等待
- 教训：子代理产出必须可核验（落盘文件/输出通道），不能依赖「会传回」；审查类任务把验收标准固化，主线程可独立复跑
- 2026-08-15 复用：wait_agent 连续超时后，interrupt_agent 返回的 previous_status 可完整取回已完成代理的 final 报告，无需重发、无需中断其他任务
- 2026-09-02 复用：本轮 reviewer 连续三轮等待 120 秒均只返回 `timed_out=true`，最终状态回收为 `previous_status=running`；未重发，按主线程同一验收清单兜底
- 2026-09-02 复盘补充：`wait_agent` 的 `timed_out=true` 返回 `status={}`，不能代替线程状态查询；本轮未先读取 `read_thread` 就调用 `close_agent`，其返回 `previous_status=running`，随后代理被 shutdown，证明仍运行任务被提前终止。修复顺序为：`wait_agent(120秒)` → `read_thread` 查询 `thread.status`、`turn.status` 和最新更新时间/最近事件；有进展继续等待；连续两个快照无进展先 `send_input(interrupt=true)` 要求立即返回四块摘要，再等待一次并复查；仅已确认终止或救援失败才 `close_agent`。
- 2026-09-02 任务卡收窄：影评审查只传“影评正文＋事实清单＋验收标准”，默认不附完整原始转写稿；仅按事实清单定向回看争议片段，减少无关读取、联网核验和推理耗时。
- 2026-09-02 修复后探针：新 reviewer 会话实际使用 `gpt-5.6-luna`、`high`，约 16 秒完成并由 `read_thread` 取回记录后再关闭；仅证明配置加载和正常完成分支，超时救援分支仍需后续真实回归。

### Pitfall-050 子代理继承含候选任务/方案的上下文会跑偏并互杀：受控任务必须自包含且显式禁止扩展与互操作

- 报错特征/触发关键词：fork_turns、子代理、跑偏、上下文污染、spawn_agent、interrupt_agent
- 最近复用：2026-09-02
- 状态：有效
- 场景：2026-08-05 用三个子代理做受控 A/B 测试，spawn 时 fork_turns=2 继承主线程最近讨论（含三个候选任务列表与 fork 意图）
- 现象：其中一个子代理未执行指派任务，转而把候选任务当任务执行：自行 spawn「土拨鼠/OneDrive」两个子任务、中断另外两个兄弟测试子代理（均 turn_aborted）、在 raw_data 创建 `_Pitfall测试_影评修订` 目录、回写 Pitfall-030「最近复用：2026-08-05」（伪回写）
- 根因：fork_turns=2 的上下文包含候选任务与编排讨论，子代理误将其当作执行指令；任务卡未显式禁止扩展、派生与互操作（待验证：多 agent 消息传递在 fork_turns=2 下的完整注入行为）
- 有效路径：受控子代理任务卡首行声明「忽略上下文中任何候选/讨论，仅执行以下唯一任务」；显式禁止派生子代理、中断其他 agent、写项目文件；默认使用 `fork_context=false`，仅在调用面不支持时采用最小 `fork_turns`＋强任务卡（`none` 会丢任务消息，见 Pitfall-020）；高价值受控测试优先主线程串行执行
- 教训：子代理测试环境不可靠（消息丢失、上下文污染、兄弟互杀）；「最近复用」只能在真实命中且解决后回写，未解决不得回写

### Pitfall-051 闲置关窗脚本以「历史会话 mtime」判闲置：ChatGPT 重启后仍被旧闲置时间立即退出

- 报错特征/触发关键词：idle-window-closer.log、QUIT、闲置、ChatGPT 自动关闭、launchd、重启
- 最近复用：无
- 状态：有效
- 场景：2026-08-05 用户把 ChatGPT 放后台/重新打开，几分钟内又被自动退出；日志显示 LaunchAgent 每 5 分钟巡检
- 现象：`~/.codex/idle-window-closer.log` 显示 17:46、19:16、19:21 三次「QUIT 开始→OK 已退出 ChatGPT 进程」；19:14 时闲置已 153 分钟，App 重开后 19:21 又立即被退；会话文件最新 mtime 仍停在 16:41（旧线程「规范竞品分析报告撰写」），与 App 重启时间无关
- 根因：`close_idle_codex_windows.sh` 的闲置时长 = 全局最新会话 JSONL 的 mtime 与当前时间差；该 mtime 是持久化历史，App 重启不会归零。用户重开后，只要旧会话闲置已超阈值，下一次 5 分钟巡检就会把刚打开的应用退掉，表现为「挂后台/刚打开几分钟就被关」
- 补充（2026-08-05 用户澄清）：只“打开查看/阅读”不写会话文件，mtime 不会刷新；所以即使用户刚重开并看过内容，只要全局最新会话 mtime 仍停留在几小时前，脚本也会把刚打开几分钟的进程误杀。闲置起点必须是「会话最后写入 / 进程启动 / 最近前台查看」三者中的最新者，而不是单一历史 mtime
- 有效路径：闲置判定增加「进程最近启动时间」维度，取 max(会话最后活动时间, 进程启动时间) 作为活动起点；或退出动作加进程启动时间保护（启动不足阈值不退出）；修复前临时停用可 `launchctl bootout gui/$(id -u)/com.user.codex-idle-close` 或脚本 DRY_RUN=1
- 已修复（2026-08-05，用户批准）：两个 Codex 闲置脚本 IDLE_MINUTES 统一 30；闲置起点改为 max(会话最后写入, 进程启动时间, 最近前台查看时间)，最近查看状态存 `~/.codex/idle-codex-activity`；bash -n、dry-run（重开 10 分钟不杀、0 分钟仅 DRY 记录）、launchctl kickstart 复测均通过
- 教训：用持久化文件时间做「当前进程闲置」时必须与进程生命周期对齐，否则重启后会把历史闲置算到新进程头上；「几分钟被关」先查最近一次 QUIT 日志与进程启动时间对比

### Pitfall-052 双 Codex 入口（ChatGPT 桌面＋VS Code 扩展）同机并发：两套 app-server 共享 ~/.codex 加剧锁与日志竞争

- 报错特征/触发关键词：app-server、双入口、thread-writer-locks、logs_2.sqlite、VS Code 扩展、ChatGPT 桌面、并发
- 最近复用：2026-08-05
- 状态：有效
- 场景：2026-08-05 排查「子代理超过两个就出问题」时发现 ChatGPT.app（PID 84104，运行 3 天）与 VS Code 扩展（PID 86065/86066，运行 12 小时）同时存在，均为 `codex app-server`
- 现象：两台服务读同一 `~/.codex/config.toml`、写同一 `logs_2.sqlite` 与 `thread-writer-locks/.coordination.lock`；当天日志出现 12+ 个不同 app-server 进程实例；多会话同时写「会话摘要.md」时 apply_patch 连续报 Failed to find expected lines（10:11/10:16/13:57/15:55）
- 根因：Codex 桌面版与 VS Code 扩展是两套独立 app-server 进程，各自可派生子代理，却共用同一套用户目录状态；并发槽位与文件写入竞争叠加（待验证：两套服务的槽位是否独立计）
- 有效路径：同一时间只保留一个 Codex 入口（关掉桌面端或 VS Code 扩展其一）；子代理预算按「主线程＋最多 2 个子代理」留余量；不同会话错开写同一文件的时间
- 教训：排查并发问题先 `ps -axo ... | rg 'codex.*app-server'` 数实例；「超过两个就乱」先查入口数，其次才是内存

### Pitfall-053 VS Code CLI 卸载扩展只删清单不删文件夹：磁盘未释放，需 trash 或移目录补清理

- 报错特征/触发关键词：code --uninstall-extension、卸载成功但目录仍在、extensions 磁盘未变小、~/.vscode/extensions
- 最近复用：无
- 状态：有效
- 场景：2026-08-05 批量卸载 32 个 VS Code 扩展，CLI 逐个返回 OK，`--list-extensions` 从 57 降到 24
- 现象：`du -sh ~/.vscode/extensions` 仍为 1.8G（几乎未释放），目标文件夹全部原样保留在目录中
- 根因：本机 VS Code 版本（26.x）的 `code --uninstall-extension` 只移除 extensions.json 元数据，未删除扩展目录（待验证：是否受运行中扩展宿主占用影响）
- 有效路径：卸载后必须复查目录体积；把目标文件夹 `trash`（系统 /usr/bin/trash，可恢复）或移出加载路径；先复制备份再卸载，避免误删
- 教训：验证「卸载成功」要看磁盘和目录，不能只看 CLI 返回 OK；批量清理前先备份、卸载后按文件夹逐项核对

### Pitfall-054 Codex/Computer Use 隔天自动关闭先查本地 LaunchAgent 闲置退出，不是浏览器缓存机制

- 报错特征/触发关键词：MCP Computer Use 自动关闭、浏览器退回空白未登录、com.user.codex-idle-close、close_idle_codex_windows.sh、idle-window-closer.log、整窗关闭
- 最近复用：无
- 状态：有效
- 场景：2026-08-08 用户报告 MCP Computer Use 隔天自动关闭、浏览器操作退回未登录 Chrome，怀疑「占用浏览器缓存被自动关掉」
- 现象：config.toml 中 computer-use/chrome/browser 插件始终 enabled=true（非配置回退）；`~/.codex/idle-window-closer.log` 显示 8/7 22:46「QUIT 开始/OK 已退出 ChatGPT 进程」；`~/.codex/idle-chrome-closer.log` 显示 23:26「已整窗关闭：窗口#0」；Codex 进程退出后 MCP/扩展连接全部终止，次日需重新登录
- 根因：用户自装 LaunchAgent（com.user.codex-idle-close 每 5 分钟、com.user.codex-chrome-idle 每 1 分钟）分别实现「Codex 闲置≥30 分钟退出整个进程」与「Chrome 闲置标签 30 分钟清理、后台窗口整窗关闭」；官方未见「浏览器缓存占用自动关闭 Computer Use」机制，本机插件 skill 无此机制且配置保持 enabled（官方否定结论待验证）
- 有效路径：先查 `~/.codex/idle-window-closer.log`（QUIT/OK 已退出）与 `idle-chrome-closer.log`（整窗关闭/CLOSE），再核对 `~/Library/LaunchAgents/com.user.codex-idle-close.plist`、`com.user.codex-chrome-idle.plist`；保活方案＝脚本白名单关键词（WHITELIST_KEY 默认「日记」）、调大 IDLE_MINUTES 或临时 bootout，属系统级变更须用户确认后执行
- 教训：「MCP 被自动关闭」先区分进程退出（LaunchAgent/内存守卫）与配置回退（Pitfall-022）两类根因；浏览器登录态掉线优先查 Chrome 是否被整窗关闭，再查扩展连接

### Pitfall-055 脚本重组 HTML 章节时，无 id 的散落 section 会被当“尾部”丢掉：重组前必须按深度配对全量块并保留区间外内容

- 报错特征/触发关键词：HTML 重排、section 顺序、block_end、无 id 的 section、ch1 尾部内容丢失、1.8/1.9 消失
- 最近复用：2026-08-08
- 状态：有效
- 场景：2026-08-08 为《人机协作的迭代史（重构版）》HTML 补「行业增量需求」后，发现 ch6/ch7/ch8 章节块在文件中乱序，写脚本重排
- 现象：第一次按「每个章节第一个 </section>」切块，把 ch1 内部嵌套的普通 `<section>` 误判为章节结束，导致 1.8/1.9 所在的「无 id section」掉出重建范围；第二次按「首次出现 id 取块、取最大 end 为尾」重建，尾部仍残留重复的 ch7/ch6，页面出现两个第 7 章和两个第 6 章
- 根因：HTML 章节间存在不带 id 的散落 `<section>`（逻辑上属于上一章，DOM 上平级）；按字符串「第一个闭合标签」或「首次出现 id 的块」切分都覆盖不了这类区间；重排时用「最后一块的 end」当全文尾部，而最后一块并不是最大 end
- 有效路径：重排前先用正则扫描全部 `<section id="chN">`，按标签深度配对每个块的起止；确认「块与块之间还有没有未命名 section」并把它们与前一章绑定；重建时尾部取「全文件最后一个块的 end」而不是“最后一个已收录块的 end”；改完用 `rg '<section id="ch(\d)">'` 数次数并校验 1.8/1.9 等边界内容仍在
- 教训：批量重排 HTML 前先盘点“无 id 的平级 section”，重组输出必须由「前缀 + 全量块 + 后缀」三段拼成，任何一段都不能依赖“刚好碰到”的边界；改完用 id 出现次数与边界锚点双验证

### Pitfall-056 Ollama 官方下载源极慢（ollama.com/GitHub 约 50KB/s），换 ghproxy.net 镜像提速约 13 倍

- 报错特征/触发关键词：Ollama 升级、Ollama-darwin.zip、下载慢、curl 速度 50KB/s、GitHub releases 超时
- 最近复用：2026-08-08
- 状态：有效
- 场景：2026-08-08 升级 Ollama 0.13.5→0.32.6（zip 171MB）
- 现象：官网直连 45-60KB/s（预计 1 小时）；GitHub 官方源直连约 22KB/s（20 秒仅 443KB）；换镜像后 320-612KB/s，7 分钟完成
- 根因：本机网络到 ollama.com 与 GitHub CDN 节点慢（节点/线路未进一步验证）；国内 GitHub 加速镜像对 releases 下载有效
- 有效路径：先用 15 秒并行测速多个镜像再选：ghproxy.net（612KB/s）＞gh-proxy.com（31KB/s）＞ghfast.top/mirror.ghproxy.com（0）；下载后 `unzip -tq` 校验完整性；macOS 替换 /Applications/Ollama.app 流程：kill 旧进程→mv 旧版备份→cp -R 新版→open -a 启动→`ollama --version` 验证（CLI 是符号链接指向 app 内二进制，替换 app 即更新）
- 教训：大文件下载先并行测多源（15 秒内出结果）再决定，不干等慢速官方源；替换 .app 前校验 zip，替换后验证版本与进程

### Pitfall-057 Qwen3.5-2B 默认思考模式输出超长思维链，ollama run 看似卡死；需 think:false + num_predict 上限

- 报错特征/触发关键词：ollama run 无输出、qwen3.5 卡住、n_decoded 持续增长、response 空、OCR 超时、思维链
- 最近复用：2026-08-08
- 状态：有效
- 场景：2026-08-08 在 16GB M4 上用 qwen3.5:2b-q4_K_M 做本地 OCR/视觉兜底
- 现象：ollama run 2 分 38 秒解码 7931 token 仍未结束（client 中断）；/api/generate 不设上限时持续生成；同一请求加 `think:false` + `options.num_predict=500` 后 10 秒返回完整中文 OCR
- 根因：Qwen3.5 默认思考模式开启，先生成超长思维链再输出答案；Ollama CLI 无输出上限参数，默认上下文 128K 进一步放大内存与等待
- 有效路径：调 /api/chat 加顶层 `think:false` 与 `options.num_predict`（OCR 实测 800 token 足够）；上下文按 16GB 内存选 51200 而非 128K；判断“卡死”先看 ~/.ollama/logs/server.log 的 n_decoded 是否增长，增长即正常推理；解析响应时 response 与 thinking 是独立字段
- 教训：集成本地思考型模型前先实测输出结构与默认开关；代码调用必须设输出上限与思考开关，不能依赖 CLI 默认行为

### Pitfall-058 MCP 服务器把 VISION_* 配置写在 ~/.codex/<视觉代理配置文件> 但代码只读 Key，真实进程不加载配置；需启动时解析整个 env 文件

- 报错特征/触发关键词：<视觉代理配置文件>、VISION_LOCAL_MODEL 不生效、VISION_PRIMARY_MODEL 未定义、MCP 配置环境变量、本地兜底未配置
- 最近复用：2026-08-08
- 状态：有效
- 场景：2026-08-08 给视觉代理做「主 GLM-4.6V→Flash→本地」三级降级时，把 VISION_PRIMARY_MODEL/VISION_LOCAL_MODEL/VISION_LOCAL_CONTEXT 追加进 ~/.codex/<视觉代理配置文件>，但 config.toml 的 [mcp_servers.vision_proxy] 无 env 表
- 现象：server.mjs 常量区只读 process.env，loadApiKey 又只解析 env 文件里的 <视觉模型 API Key> 一行；真实 MCP 进程里 LOCAL_MODEL 恒为空，本地兜底永远报「未配置本地兜底模型」；之前 shell 测试全过是因为命令行 export 了同名变量，掩盖了问题
- 根因：env 文件与 process.env 是两套来源，代码只在 Key 读取处解析 env 文件；config.toml 未配置 [mcp_servers.vision_proxy.env]，MCP 子进程没有这些环境变量
- 有效路径：server.mjs 启动时用 readFileSync 解析 ~/.codex/<视觉代理配置文件> 的全部 VISION_* 行写入 process.env（已存在的进程环境变量优先，Key 仍单独走 loadApiKey）；测试时不要只依赖 shell export 验证「文件配置生效」；改后分别验证 mock、真实云端、全失败落本地三条路径
- 教训：MCP 服务器的「env 文件」不是自动环境来源，代码必须显式加载；「shell 里能跑通」不等于「Codex 真实进程能跑通」，两类运行环境都要回归

### Pitfall-059 智谱 GLM-4.6V 图片 token 随分辨率近似线性增长；长边压到 1536px 是「省 token 且不伤质量」甜点，1024px 复杂图会明显错字

- 报错特征/触发关键词：GLM-4.6V prompt tokens 高、视觉计费、图片压缩、sips -Z、1536、1024、OCR 错字
- 最近复用：2026-08-08
- 状态：有效
- 场景：2026-08-08 用 GLM-4.6V 对 1900×1400 级 PPT 截屏做三尺寸（原图/长边1536/长边1024）OCR 对比，验证「压缩图片省 token」假设
- 现象：同图不同分辨率 prompt tokens：1941×1408 原图 3492 → 1536 版 2242（省 36%）→ 1024 版 1041（省 70%）；token 与像素面积近似线性（约 100-130 tokens/10 万像素，另加约 100 文字 token）。效果：1536 与原文一致，1024 在文字密集图有 1 处错字、在复杂架构图出现「记录生活的陈三」「可视测性」等多处错字且输出更长，总成本反超原图（0.0125 vs 0.0114 元）
- 根因：智谱按图片像素折算视觉 token（实测拟合，官方折算规则未公开）；过度压缩使小字/密集结构看不清，模型用更长输出来补猜测
- 有效路径：长边 ≤1536px 作为默认压缩档（省 24-36% token、质量不降）；纯文字简单截图可试 1024，复杂架构图/表格别低于 1536；1600px 比 1536 贵约 6% 且效果无增益，1650px 贵约 14% 仅复杂小字图略准，默认 1536、复杂图按需调 1650；压缩用 macOS 自带 `sips -Z 1536 in.png --out out.png`（已集成进视觉代理：VISION_IMAGE_MAX_DIM 默认 1536，VISION_IMAGE_RESIZE_DISABLE=1 关闭）；对比测试要同时记录 prompt/completion/输出文本，只看 token 会漏掉「输出变长导致总成本反升」的反例
- 教训：视觉 token 优化先实测分辨率映射，不能凭「越小越省」一刀切；质量验证要逐字对比错字，并看 completion 长度变化

### Pitfall-060 智谱 GLM-4.6V 内容审核拦截名画裸体/敏感图（HTTP 400 code 1301 contentFilter），视觉代理无提示词可绕过

- 报错特征/触发关键词：视觉 API 请求失败（HTTP 400）、code 1301、contentFilter、系统检测到输入或生成内容可能包含不安全或敏感内容、describe_image 失败、毕加索、裸体名画
- 最近复用：2026-08-09
- 状态：有效
- 场景：2026-08-09 用 vision-proxy 对毕加索 5 幅名画做 DeepSeek+GLM 伪视觉链路实测，第 2 张《亚维农少女》（Les Demoiselles d'Avignon）触发拦截
- 现象：describe_image 调 GLM-4.6v 与 glm-4.6v-flash 均返回 HTTP 400，错误体 `{"contentFilter":[{"level":2,"role":"user"}],"error":{"code":"1301","message":"系统检测到输入或生成内容可能包含不安全或敏感内容..."}}`；本地 Ollama 兜底也失败（fetch failed，未运行）；同批《格尔尼卡》《哭泣的女人》《镜前的少女》《老吉他手》均正常识别
- 根因：智谱视觉接口对图像内容做安全过滤，名画中的裸露人体命中敏感图像规则（具体规则未公开，待验证）；过滤发生在请求阶段，与提示词是否安全无关，默认「详细描述图片内容」也会被拦
- 有效路径：识别裸体/人体艺术前先预判敏感度；绕过思路（均需实测）：先裁剪局部、加马赛克/遮挡敏感区、换无此过滤的视觉供应商（OpenAI/Gemini/其他兼容端点）；工具层可在 server.mjs 的 describe_image 失败 1301 时返回「图片被智谱内容审核拦截」的明确提示，而不是让上层模型误以为图片内容为空
- 教训：伪视觉链路的可靠性受第三方内容审核约束，「模型不能看图」之外还有「审核不让看」；做艺术识别测试先声明题材敏感度，失败信息保留错误码便于归因

### Pitfall-061 FlClash 0.8.92：覆写规则落库/落文件但运行核心不重载；Flutter UI 自动化须用 AXPress 并在正确分组 Tab 操作

- 报错特征/触发关键词：FlClash、覆写、DIRECT、config.yaml、AXUIElement、AXPress、节点切换不生效、selected_map
- 最近复用：2026-08-10
- 状态：有效
- 场景：2026-08-10 为 happy猫 订阅加 typeless.com/OneDrive 家族 DIRECT 覆写并做节点换优；全程通过 macOS 辅助功能 API 操作 Flutter 界面
- 现象：① 覆写规则经 UI 添加后 sqlite（rules/profile_rule_mapping）与 config.yaml 均正确写入，重新应用订阅（切走再切回）后运行核心仍用旧规则集：新域名请求仍走节点出站（lsof 无 DIRECT 出站），原配置里已有的 DIRECT 规则（zhihu 等）正常；**用户手动重启 FlClash 后新规则立即生效**（typeless 出站直连 166.117.210.238、0.58s）；② 用 CGEvent 全局合成点击 FlClash 卡片/按钮经常无效（被前台 ChatGPT/其他应用窗口遮挡），AXPress 几乎全部有效；③ 代理页顶部有分组 Tab（happy猫 机场/自动选择/故障转移），直接点节点名只改「自动选择」子组 selected_map，根组不变、出口 IP 不变，须切到根组 Tab 再选节点才生效并持久化
- 根因：FlClash 0.8.92 运行中通过 UI「重新应用订阅」不会把新增 rules 推送给已运行核心（热载失效，机制待验证），重启客户端后核心重读 config.yaml 生效；Flutter macOS 语义树默认不完整，需设 AXEnhancedUserInterface=true；合成点击受窗口遮挡/焦点影响
- 有效路径：① Flutter/FlClash 自动化基线：先 AXUIElementSetAttributeValue(AXEnhancedUserInterface=true)，每次动作前重新取完整树；按钮/复选框/规则行/节点卡片用 AXPress；文本输入用「点击字段 + System Events Cmd+A + Delete + keystroke」；窗口被覆盖时先用 AX move 到未被遮挡显示器，操作完还原位置与尺寸；② 节点切换必须确认所在分组 Tab：代理页先点根组 Tab，再 AXPress 目标节点，随后查 sqlite selected_map 与出口 IP（cloudflare trace）双确认；③ 规则类改动以 UI 内可查（覆写列表、sqlite）为准；运行核心不生效时保留配置，重启 FlClash 一次即可生效，勿反复重启
- 教训：GUI 自动化先验证「点击是否真的到达目标窗口」（CGWindowList 层序/前台进程），再谈元素路径；改配置类任务要区分「配置已保存」与「运行进程已生效」两层状态，验收必须测实际流量/出站，不能只看配置文件；「需重启生效」的结论要在重启后复验再沉淀，避免把临时现象写成永久缺陷

### Pitfall-062 素材任务只列目录未深读：把 ls/rg --files 当读取，被用户指出后才补读移动硬盘

- 报错特征/触发关键词：移动硬盘、Elements、素材未读、只列目录、深读、影评素材、用户纠正
- 最近复用：2026-08-10
- 状态：有效
- 场景：2026-08-10《楚门的世界》影评任务。范式要求默认深读本机工作区与已挂载移动硬盘素材，主线程首轮只做了 `/Volumes/Elements` 顶层目录列举与少量文件名检索，未实质读盘即开始准备成稿；用户指出「好像你没读取过移动硬盘里的信息，移动硬盘里面很多东西」，随后补做深读
- 现象：影评首轮素材扫描停留在 ls 顶层目录与文件名列表；关键词 rg 命中文件后未读取正文；用户纠正后才读入「即兴游戏、云监控、元认知、伪退出、决策边界」等正文素材
- 根因：把「扫描素材」误解为「列出素材」；大文件（数百 KB 至 MB 级 md/docx）导致回避全读，误以为文件命中关键词即代表内容已消化（待验证）
- 有效路径：① 素材任务以「读入正文」为完成标准，不把 ls/rg --files 当读取；② 大文件用 rg 关键词上下文抽取＋小文件全文 cat 组合，命中即读上下文；③ docx 用 `textutil -convert txt -stdout` 直接读；④ 成稿前把拟用理念逐条标注来源文件，交付报告列出实际读过的素材清单，防伪读取
- 教训：用户可见的检查点是「实际读过什么」；只列目录等于未执行素材规则，宁可少写不可假读

### Pitfall-063 判断南方夏季局地降雨：中央气象台全国雷达拼图（chinaall.html）看局部外推趋势，优于常规日预报与其他天气站点

- 报错特征/触发关键词：预报无雨却淋雨、雷达回波、组合反射率、dBZ、中央气象台、chinaall.html、分钟级、防雨、电动车出行
- 最近复用：2026-08-11
- 状态：有效
- 场景：2026-08-11 用户多次实测：常规日预报「无雨」时骑电动车被午后局地对流淋雨（约 1.5 小时后放晴）；改用中央气象台全国雷达拼图（http://www.nmc.cn/publish/radar/chinaall.html）后确认其优于中国天气网分钟级、Windy、RainViewer 等同类工具，确认「只用一个雷达图即可」
- 现象：日预报对景德镇/南昌/温州夏季午后局地对流经常漏报；雷达拼图以「组合反射率」产品、dBZ 色标（蓝→紫约 10～70）清晰显示降水系统位置、强度、移动方向与演变，查看华东等局部区域时细节清楚，缩放全国则看不清单体
- 根因：常规日预报为数值模式网格外推，对尺度仅数公里、生消周期约 1～2 小时的局地对流存在时空盲区；雷达拼图是实况产品，约 10 分钟滚动更新并保留近 2 小时回放，动画直接呈现趋势（待验证项：各产品实际更新间隔与延迟）
- 有效路径：① 出门前打开 http://www.nmc.cn/publish/radar/chinaall.html，把视图缩放到本地所在区域（华东等局部，勿看全国）；② 看动画确认 100 公里内有无黄色以上回波（约 30 dBZ 以上、中到大雨量级）向本地移动，有则带雨具或暂缓出发；③ 途中每 20～30 分钟刷新一次；④ 雷达只覆盖「已成形回波」，新生对流有盲区，仍须结合中央气象台暴雨/强对流预警与本地云况（天色骤暗、雷声、风骤凉）兜底
- 教训：判断「会不会下雨」以实况雷达的移动趋势为准，不以日预报的「无雨」为准；同类工具先小成本实测再下结论，用户验证过的单一有效工具优先于工具组合（彩云网页版 app.caiyun.com 已跳转域名出售页，勿再推荐）

### Pitfall-064 程序化获取官方降雨判断数据：中央气象台雷达帧 URL 内嵌 UTC 时间，分钟级降水用 d3.weather.com.cn JSONP 接口

- 报错特征/触发关键词：雷达图 URL 404、SEVP_AOC_RDCP、chinaall、huadong、AZ9798、UTC 时间戳、分钟级降水、webgis/minute、RainViewer 无数据
- 最近复用：2026-08-12
- 状态：有效
- 场景：2026-08-12 用户要求按「雷达+分钟级」流程判断景德镇此刻与未来 2 小时是否下雨，需程序化抓取官方数据而非肉眼看网页
- 现象：中央气象台网页为 JS 渲染，正文不在 HTML；直接用北京时间拼雷达图 URL（20260812160000000）全部 404；RainViewer 瓦片在景德镇周边只返回灰阶占位图（无回波数据）；d1.weather.com.cn 旧接口返回「联系方式」占位页
- 根因：中央气象台雷达产品 URL 内嵌的是 UTC 时间（页面 data-time 显示 15:48 时 URL 是 074800000，即北京-8h），且产品帧非每 6 分钟连续；RainViewer 对中国本地雷达覆盖不完整（待验证）；weather.com.cn 部分旧接口已失效/反爬
- 有效路径：① 从雷达页 HTML 的 data-img 属性直接取最新帧，不自行拼时间：全国 http://www.nmc.cn/publish/radar/chinaall.html、华东 http://www.nmc.cn/publish/radar/huadong.html、景德镇单站 http://m.nmc.cn/publish/radar/jiang-xi/jing-de-zhen.htm（图片 URL 形如 SEVP_AOC_RDCP_SLDAS3_ECREF_ACHN/AECN/AZ9798_L88_PI_YYYYMMDDHHMMSS00000.PNG，时间戳为 UTC）；② 分钟级降水官方 JSONP：`https://d3.weather.com.cn/webgis_rain_new/webgis/minute?lat=<纬度>&lon=<经度>&callback=fc5m`，返回未来 2 小时逐分钟 values（全 0 即无雨）与自然语言 msg，更新约 6 分钟一次；③ 城市当日预报与预警用 https://www.weather.com.cn/weather/101240801.shtml（景德镇）等城市页；④ 官方预警列表看 http://www.nmc.cn/ 首页正文区
- 教训：抓取数据先解析页面 data 属性拿到真实帧再下载，凭模式猜时间极易 404；判断「本地未来 2 小时有雨无雨」优先官方分钟级 JSONP，第三方全球雷达（RainViewer）在中国区不可依赖

### Pitfall-065 zsh 脚本中变量 `path` 会覆盖 PATH，循环内命令全部 command not found

- 报错特征/触发关键词：command not found、PATH、path 变量、zsh、循环内 curl/ls 全失效
- 最近复用：2026-08-12
- 状态：有效
- 场景：2026-08-12 写循环下载 RainViewer 瓦片，把循环路径变量命名为 `path`
- 现象：`path='/v2/radar/xxx'` 赋值后，同一命令内后续 curl、ls、rg、head 全部报 command not found；退出后 shell 恢复正常
- 根因：zsh 中 `path` 是与 `PATH` 绑定的特殊数组，赋单值即破坏 PATH；bash 无此行为，跨 shell 写法不通用
- 有效路径：循环/局部变量命名避开 `path`、`home`、`user`、`status` 等 shell 特殊名，用 `rvp`、`tile_path` 等；出现批量 command not found 先 `echo $PATH` 排查是否被覆盖
- 教训：zsh 脚本默认按 zsh 语义写变量，bash 经验不能直接照搬；特殊变量名要在写循环前规避

### Pitfall-066 VS Code 多标签打字光标乱晃：accessibilitySupport=off 仍复现，08-10 修复未闭环

- 报错特征/触发关键词：VS Code、光标乱晃、指针乱跳、中文输入法被打断、多标签/多窗口、accessibilitySupport
- 最近复用：2026-08-12
- 状态：待闭环
- 场景：2026-08-10 首次报告（多标签打字光标乱晃＋中文输入法被打断，单文件正常），当时改 `editor.accessibilitySupport` on→auto；2026-08-12 用户复报仍乱晃，实测用户设置已是 off
- 现象：文字输入时光标跳到其他位置、中文拼音组合被中断；已排除：闲置关闭编辑器脚本（launchd 60s 巡检，日志仅 DRY/SKIP 未真实执行）、Copilot 写文件（日志 403 unauthorized 未授权）、屏幕阅读器虚拟光标（accessibilitySupport=off）
- 根因：待验证；当前主嫌疑按序：① Typeless 全局 dictation 热键 LeftOption，误触 Option 触发语音转写插入当前光标位；② files.autoSave afterDelay 500ms 在多标签/双窗口（两个 VS Code 窗口均开 md）下引起编辑器状态刷新；③ macOS 15.5 + VS Code 1.132（Electron 42）中文 IME 组合输入在窗口失焦/切换时被打断（待核实具体版本）
- 有效路径：A/B 验证三步——① 退出 Typeless 或改 push-to-talk 热键后打字测试；② `"files.autoSave":"off"` 后打字测试；③ 只保留一个 VS Code 窗口测试；确认主因后改配置并复验；若乱晃的是鼠标指针而非文字光标，转查 SkyComputerUseService/触控板
- 教训：修复类结论必须用户复验闭环才可算完成；「主因」标签要保留候选清单，单一开关改动不足以排除同症状多源

### Pitfall-067 VS Code 卡顿先查内存压力与 CPU 而非 V8 堆上限：js-flags 是上限不是配额

- 报错特征/触发关键词：VS Code 卡、内存不够、max-old-space-size、2048、WindowServer CPU、swap、内存压力、BetterDisplay
- 最近复用：2026-08-12
- 状态：有效（重启/关窗口效果待用户复验）
- 场景：2026-08-12 用户把 08-04 设置的 `--max-old-space-size=2048` 误认为「给 VS Code 的内存配额」，问卡顿是否因内存太少
- 现象：VS Code 17 进程总 RSS 约 2.0-2.4GB，单进程最大约 770MB，离 2GB 远；系统 16GB 空闲 62%、swap 仅 210MB，无内存压力；但 WindowServer 平均 47.5%、WindowManager 32.2%、VS Code 主进程 24.9%（6 小时均值），第二窗口渲染进程瞬时 12.8%
- 根因：V8 `--max-old-space-size` 只限制单进程老生代堆上限，不是预先占用或配额；堆未触顶时调大不会变快，只会放宽内存占用；卡顿源在系统合成层（BetterDisplay/高分辨率外屏叠加）与 VS Code 主进程间歇重负载（双窗口大 md＋内置 Copilot Agent 空转，待验证细分占比）
- 有效路径：排查顺序——① `memory_pressure -Q` 看系统空闲百分比＋`sysctl vm.swapusage`；② `ps` 聚合 VS Code 总 RSS 与单进程峰值，堆未触顶先不调；③ `ps -r` 看 WindowServer/WindowManager/CheatSheet 等高 CPU 后台；④ 先重启 VS Code、关第二窗口、退出不用的全局工具（CheatSheet/BetterDisplay）再谈调参；本机 argv.json 实际路径是 `~/.vscode/argv.json`（不在 Library/Application Support/Code）
- 教训：内存类卡顿先量「压力」而非「上限」；改性能参数前先确认瓶颈维度，避免把 GC 上限当配额调整

### Pitfall-068 Codex 桌面版自定义 provider 的模型选择器空白而 CLI 正常：切换模型改 config.toml 或用 codex --model

- 报错特征/触发关键词：Codex 桌面模型选择器空白 / model picker empty / custom provider / model_catalog_json / #34487 / #15138 / #19694 / deepseek-v4-pro
- 最近复用：2026-08-13
- 状态：有效
- 场景：用户 Codex 桌面版经自定义 provider 接入 DeepSeek，问输入框为何不显示模型选择/模型自定义、当前模型不可见
- 现象：`~/.codex/config.toml` 配置正确（model_provider=custom、model_catalog_json 两个模型 visibility=list），`codex debug models` 能列出 deepseek-v4-flash 与 deepseek-v4-pro，但桌面 app 模型选择器完全空白；CLI 不受影响
- 根因：Codex 桌面版对自定义 provider 的模型选择器存在门控/过滤缺陷，对应 GitHub openai/codex issues #15138、#19694、#34487、#36582；官方/普通配置均无法让桌面 picker 显示第三方模型（#36597 指出社区绕法需本地代理接管官方流量）；具体机制官方未确认，标「待验证」
- 有效路径：诊断用 `codex debug models`；CLI 不在 PATH 时用绝对路径 `/Applications/ChatGPT.app/Contents/Resources/codex --model deepseek-v4-pro`，会话内用 `/model` 查看并切换严格三档 low/high/max；临时切 Pro 改 `~/.codex/config.toml` 的 `model = "deepseek-v4-pro"` 后重启 app（issue #19694 workaround）不推荐长期使用；桌面右下角切换需社区方案——DSCodex 本地路由（127.0.0.1:10110，ChatGPT 桌面端原生模型菜单显示 V4 Flash/Pro，无需改 App）、cc-switch（需 ChatGPT OAuth 登录态＋/v1/models 端点，PR #3503 未合并，v3.19.2 待实测）、Better-Codex-App-Custom-Provider-Support（patch app.asar，更新后需重装补丁）；桌面推理档位可在「智能体默认设置→模型功能→可用推理强度」勾选裁剪（本机 26.812 为 6 档：极低/低/中/高/极高/最高，默认 6 选 5；2026-08-13 截图确认该设置页存在），可按需只留 低/高/最高 三档，属全局显示清单、官方模型同样受限；DeepSeek 官方映射 low→low、medium→high、high→high、xhigh→high、max→max，实际仅三档，minimal 不在官方映射表内
- 教训：桌面 UI 缺模型控件不等于配置错误，先 CLI 验证再下结论；自定义 provider 场景以 CLI 为可靠切换入口；第三方模型在桌面滑杆显示的档位数不代表模型真实支持档位，先查官方 reasoning_effort 映射表；桌面设置里若有「可用推理强度」清单，可裁剪为模型实际档位，先看设置页再下「不可裁剪」结论；改配置前先备份并征得用户同意；codex 命令不存在先查绝对路径，/model 只能在 CLI 会话内输入
- 2026-08-14 更新：App 升级到 26.810.41047（内置 CLI 0.148.0-alpha.9）后，本机桌面模型选择器已能显示 deepseek-v4-flash/pro（models_cache.json 仍是 8/1 官方缓存、不含 DeepSeek，说明新版读取了 model_catalog_json）；config.toml 出现新版写入的 `[desktop] enabled-reasoning-efforts = [low…max]` 段（旧版无此键，桌面设置开始落盘 config）；官方相关 issue #37379/#36597/#29156 仍 open，机制官方未确认，标「待验证」

### Pitfall-069 macOS 桌面版 Codex CLI 不在 PATH 且 /model 不是 shell 命令：用绝对路径别名，斜杠命令仅限 REPL

- 报错特征/触发关键词：command not found: codex / no such file or directory: /model / codex-pro / zsh / ChatGPT.app/Contents/Resources/codex
- 最近复用：2026-08-13
- 状态：有效
- 场景：2026-08-13 用户桌面版 Codex 接入 DeepSeek 后，在终端运行 `codex --model deepseek-v4-pro` 与别名 `codex-pro` 均报 command not found，输入 `/model` 报 no such file or directory
- 现象：`source ~/.zshrc` 后别名仍失效；`which codex` 无结果；桌面 app 正常
- 根因：ChatGPT/Codex 桌面版把 CLI 放在 App 包内 `/Applications/ChatGPT.app/Contents/Resources/codex`，未加入 PATH；`/model` 是 codex 交互会话内的斜杠命令，shell 会把它当文件路径解析
- 有效路径：别名/脚本一律用绝对路径（`alias codex-flash='/Applications/ChatGPT.app/Contents/Resources/codex --model deepseek-v4-flash'`）；`/model` 只在 `codex` 进入 REPL 后输入；验证用 `zsh -ic 'alias codex-flash codex-pro'` 与 `/Applications/ChatGPT.app/Contents/Resources/codex --version`
- 教训：桌面版自带 CLI 不等于 PATH 可用；斜杠命令不是 shell 命令，报错先分清执行环境

### Pitfall-070 Codex CLI 哑终端（TERM=dumb）下 /model 不被识别为斜杠命令：会当普通消息发给模型，模型可能误答“已切换”

- 报错特征/触发关键词：TERM is set to dumb / /model 未生效 / 已切换 / 模型没变 / thread_settings_applied / rollout jsonl
- 最近复用：2026-08-13
- 状态：有效
- 场景：2026-08-13 用自动化 PTY 但 TERM=dumb 启动 `/Applications/ChatGPT.app/Contents/Resources/codex --model deepseek-v4-flash`，会话内输入 `/model deepseek-v4-pro`，验证“同会话切换模型是否保留上下文”
- 现象：TUI 提示 `TERM is set to "dumb"... Continue anyway?`；输入 `/model deepseek-v4-pro` 后模型回复“已切换。”，但 `/status` 仍显示 deepseek-v4-flash；`~/.codex/sessions/2026/08/13/rollout-*.jsonl` 中该输入按 user_message 记录（text_elements 含 placeholder `/model`），thread_settings_applied.model 与全部请求 model 字段均为 deepseek-v4-flash；同一会话下一轮提问仍能答出前一轮记忆的词“哈密瓜”
- 根因：dumb 终端下 Codex TUI 未把 `/model` 解析为斜杠命令，原样作为用户消息发给模型；模型据上下文自行答复“已切换”，造成切换成功假象；斜杠命令解析依赖真实 TTY/交互模式（待官方确认机制，标「待验证」）
- 有效路径：判断切换是否生效不依赖 UI 与模型答复，直接查会话 rollout JSONL 的 thread_settings_applied.model 及各轮 model 字段；真实终端里再用 `/model`；自动化验证用 `codex exec --model deepseek-v4-pro` 或改 config.toml；验证“同会话上下文保留”可看 JSONL 中每轮是否携带完整历史
- 教训：模型对“切换类指令”的确认回复不可信，必须看会话元数据；TUI 自动化测试需真实 TERM/PTY，dumb 模式不构成交互 REPL 语义

### Pitfall-071 macOS 命令行工具调 SFSpeechRecognizer 直接 SIGABRT：TCC 查的是 responsible process 的 Info.plist

- 报错特征/触发关键词：SFSpeechRecognizer / requestAuthorization / SIGABRT / exit 134 / TCC / privacy-sensitive data / NSSpeechRecognitionUsageDescription / DiagnosticReports / mic A/B
- 最近复用：2026-08-13
- 状态：有效
- 场景：2026-08-13 写 Swift 工具做 XISEM Mike Pro 与内置麦克风 A/B 录音，录制正常（麦克风授权通过），随后调 `SFSpeechRecognizer.requestAuthorization` 做转写对比
- 现象：程序立即 SIGABRT（exit 134）且无 stdout；`~/Library/Logs/DiagnosticReports/mic_ab_test-*.ips` 的 termination.details 明确：`Info.plist must contain an NSSpeechRecognitionUsageDescription key`；用 `-Xlinker -sectcreate __TEXT __info_plist` 嵌入 Info.plist 并 ad-hoc 签名后仍崩；打成独立 .app（含完整 Info.plist）经 `open -n` 启动后进程停在授权请求处，对话框未确认/未弹出，未走通
- 根因：TCC 检查的是 responsible process（本环境为 ChatGPT，负责执行 Codex 子进程）的 Info.plist；ChatGPT 的 Info.plist 没有 `NSSpeechRecognitionUsageDescription`，故任何子进程调用语音识别都触发 TCC 崩溃；直接子进程嵌入 `__info_plist` 不影响 responsible process 判定；独立 .app 经 `open` 启动后 responsible 变为自身，理论可绕过，但 CLI 无 GUI 时授权提示是否可见待验证
- 有效路径：语音转写优先走已有授权的宿主 App（如 Typeless 自带的转写链路与历史库 `~/Library/Application Support/Typeless/typeless.db`）；确需命令行转写时，把工具打包成带 `NSSpeechRecognitionUsageDescription` 与 `NSMicrophoneUsageDescription` 的独立 .app 并用 `open -n` 启动、结果写文件后回读；排错先看 DiagnosticReports 最新 .ips 的 termination.details，不要反复重编译猜原因
- 教训：TCC 崩溃先看 .ips 的 termination 段；usage description 校验对象是 responsible process 而非当前二进制；麦克风权限通了不代表语音识别权限也通，两类权限要分别验证

### Pitfall-072 安装刚发布的 GitHub 官方仓库：先核验组织、时间戳、npm 包脚本，慢装看进程而非反复重试

- 报错特征/触发关键词：deepseek-harness / dsh / 刚发布几小时的仓库 / open_page FETCH_TIMEOUT / raw.githubusercontent 超时 / npm install -g 长时间无输出 / npm ping 慢
- 最近复用：2026-08-13
- 状态：有效
- 场景：2026-08-13 用户发来当天 19:56 刚创建的 deepseek-ai/deepseek-harness 仓库链接要求安装，仓库发布仅约 2 小时，用户不确定真伪
- 现象：open_page 打开 GitHub 页面 FETCH_TIMEOUT；raw.githubusercontent 的 README.zh.md 多次 10 秒超时；npm install -g @deepseek-ai/dsh 12 分钟无中间输出，疑似卡死
- 根因：GitHub 页面与 raw 域名访问不稳；npm registry 延迟高（npm ping 4.1 秒），依赖树 531 包逐个拉取；管道 `| tail` 缓冲导致安装期间无输出；新发布仓库信息少、仿冒风险需要单独核验
- 有效路径：安装前核验四步——① GitHub API `repos/{org}/{repo}` 看 owner 是否官方组织、created_at/pushed_at 是否与用户说法吻合、license/default_branch；② `git ls-remote` 确认 HEAD 可访问；③ 读 README 与 package.json 确认安装方式；④ npm registry 查包 `scripts`（null 即无 install/postinstall 脚本）、`bin`、依赖是否全为官方命名空间。慢装时用 `ps -o etime,time` 看进程存活、`ls node_modules/@scope` 看目录增长判断进度，不要盲目 Ctrl+C 重试；装完用 `dsh --version` 与 `curl 127.0.0.1:<port>` 验证服务
- 教训：官方组织仓库仍要先看安装脚本再执行，全新发布项目尤其如此；npm 长安装用日志文件或目录增长观察，管道 tail 会吞掉中间输出；「几小时前发布」不是风险本身，但核验成本很低，先查再装

### Pitfall-073 dsh 与 Codex 直连不共享缓存：缓存命中取决于提示前缀一致，换 harness 后命中率可能下降

- 报错特征/触发关键词：dsh、deepseek-harness、缓存命中、命中率、首 token、token/s、直连对比
- 最近复用：2026-08-14
- 状态：有效（根因待验证）
- 场景：2026-08-14 用户实测 dsh（deepseek-ai/deepseek-harness，0.1.0-rc.6）与 Codex 直连同用 deepseek-v4-flash，个人体验：dsh 缓存命中不如直连，但回复 tok/s 与首字更快
- 现象：dsh settings.yaml 确认为 provider=deepseek-official、model=deepseek-v4-flash、reasoningEffort=max；用户观感 dsh 前置思考摘要与工具调用快，缓存命中低于 Codex 直连
- 根因：待验证；推测缓存命中按提示前缀（system prompt＋历史）一致性计算，dsh 自带系统提示词与工作流封装，与 Codex 直连的前缀不同，两边各自命中各自缓存，不互享；Codex 桌面端 hooks/记忆/会话管理使请求体更重（Pitfall-048 直连 497KB 请求体首字 42s），dsh 本地轻量处理所以首字与吞吐观感更快
- 有效路径：跨 harness 比较缓存/成本时，先核对双方 system prompt 与请求前缀是否一致；缓存命中率不可跨客户端复用；速度观感对比需同提示、同请求体大小才有可比性
- 教训：缓存命中和速度是两套指标，分别受前缀一致性与本地处理开销影响；用户个人体验优先记录为待验证线索，不擅自重测

### Pitfall-074 dsh web_search 返回 DeepSeek API error (HTTP 404)：baseURL 缺 /anthropic/v1 路径段

- 报错特征/触发关键词：`web_search`、`DeepSeek API error (HTTP 404)`、dsh settings、baseURL
- 场景：DSH（deepseek harness）settings.yaml 中 `web-search-deepseek.baseURL` 配为 `https://api.deepseek.com`，web_search 全部 404
- 根因：DSH 搜索插件（dsh-web-search-deepseek）走 DeepSeek **Anthropic 兼容端点**，默认 `https://api.deepseek.com/anthropic/v1`，请求拼成 `${baseURL}/messages`；settings 覆盖掉了 `/anthropic/v1` 路径段 → 请求打到不存在的 `/messages`
- 有效路径：baseURL 改回 `https://api.deepseek.com/anthropic/v1`（或删除该行用默认值）；settings 热生效，无需重启
- 教训：改 DSH 配置前先看插件默认值（`lib/index.js` 的 `DEEPSEEK_DEFAULT_BASE_URL`）；配置覆盖只应改「想改的」部分，路径段缺失是 404 高发根因
- 来源：DSH 工作区 P-DSH-001 ｜ 最近复用：2026-08-14 ｜ 状态：有效

### Pitfall-075 dsh web_fetch 报 "no usable web provider is registered"：平台无内置 fetch provider，非配置错误

- 报错特征/触发关键词：`web_fetch`、`no usable web provider is registered`、`WEB_PROVIDER_UNAVAILABLE`、dsh
- 场景：DSH zh-agent 已开 `tool-web.fetch: true`，但 web_fetch 全部不可用
- 根因：DSH v0.1.0-rc.6 平台**无内置 fetch provider**（`@deepseek-ai/dsh-web` 的 search 与 fetch 是两套独立注册表，互不回退）；`dsh-web-search-deepseek` 只注册了 search。属平台能力缺失，非配置错误
- 有效路径：fetch 不可用时改用 `curl`（bash 工具）抓取；或等平台后续版本补 fetch provider；tool-web 的 fetch 开关保留（对将来版本有效）
- 教训：DSH 工具可用性以「平台插件注册表」为准，配置开关≠能力存在；排查先看插件是否注册了对应 provider
- 来源：DSH 工作区 P-DSH-002 ｜ 最近复用：2026-08-14 ｜ 状态：有效（平台限制）

### Pitfall-076 bash 变量紧跟全角括号报 unbound variable：set -euo pipefail 下中文与 $VAR 拼接

- 报错特征/触发关键词：`unbound variable`、bash 脚本、全角括号、`$PORT）`、`set -u`
- 场景：DSH `start-chrome.sh` 中 `echo "✅ 隔离 Chrome 已启动（端口 $PORT）"`，`set -euo pipefail` 下运行报 `line 31: PORT�: unbound variable` 并中断脚本
- 根因：bash 把 `$` 后紧跟的非 ASCII 字节（全角右括号 `）` 的 UTF-8 首字节 0xEF）吞进变量名，解析为不存在的变量 `PORT<0xEF>`；`set -u` 将其判为未定义。中文文本与 `$VAR` 之间没有分隔时必然触发
- 有效路径：bash 脚本中变量后接中文/全角字符时一律写 `${VAR}`（花括号形式），或与中文之间留空格；echo 输出模板同理。ASCII 场景（`$PORT"`、`$PORT/`、`$PORT `）不受影响
- 教训：凡 `set -euo pipefail` 的脚本，中文＋变量拼接全部用 `${VAR}`，可避免一类隐蔽的启动即崩
- 来源：DSH 工作区 P-DSH-003 ｜ 最近复用：2026-08-14 ｜ 状态：有效

### Pitfall-077 官方 dsh-hooks-codex 桥接插件评估：仅 5/10 事件、PreCompact 不支持，不安装

- 报错特征/触发关键词：`hooks-codex`、`hooks.json`、`PreCompact`、hook 迁移、dsh
- 场景：发现官方 `@deepseek-ai/dsh-hooks-codex`（npm v0.1.0-rc.6，与本地 DSH 同版）可桥接 Codex hooks.json，评估是否安装以迁移 Codex hooks
- 根因/评估：桥接仅支持 5/10 事件（PreToolUse/PostToolUse/SessionStart/UserPromptSubmit/Stop），PreCompact/PostCompact 不支持；PreToolUse 仅 block 无 ask；UserPromptSubmit 不支持 systemMessage。用户现有 4 个 hook 中 3 个与 DSH 现有机制重复（inject_time↔time-context、post_tool_use↔修改清单、pre_tool_use_gate 无 ask 与 danger-full-access 冲突），唯一缺的 pre_compact 恰不支持
- 有效路径：不安装；维持现状（时间注入/防循环/文件记录已有替代）
- 教训：迁移前先评估「新机制与现有机制是否重复」（MECE）；官方插件目录以 `docs/config-catalog.zh.md` 或 npm registry 为准，本地未装≠不存在
- 来源：DSH 工作区 P-DSH-004 ｜ 最近复用：2026-08-14 ｜ 状态：有效

### Pitfall-078 launchd 派生的 bash 清其他 App 容器缓存报 Operation not permitted：需给 /bin/bash 完全磁盘访问

- 报错特征/触发关键词：Operation not permitted、LaunchAgent、/bin/bash、完全磁盘访问、Full Disk Access、~/Library/Containers、有道翻译、youdao、定时清理
- 最近复用：2026-08-15
- 状态：有效（授权后复测待用户确认）
- 场景：2026-08-11 落地网易有道翻译每日清理（LaunchAgent 12:00/00:00，清 WebKit/fsCachedData/崩溃报告三个缓存目录）；交互终端验证通过后，launchd 定时执行连续失败
- 现象：日志出现 `find: ~/Library/Containers/com.youdao.YoudaoDict/...: Operation not permitted`；交互终端同命令可删（Terminal/Codex 已获相关 TCC 权限）；脚本无权限时 `du` 结果为空、旧版日志误记 CLEAN
- 根因：TCC 按 responsible process 授权；launchd 任务的负责进程是 /bin/bash，未获完全磁盘访问时无法进入其他 App 的沙盒容器目录（同族：Pitfall-029 辅助功能、Pitfall-071 语音权限）
- 有效路径：① 系统设置→隐私与安全性→完全磁盘访问→＋→Cmd+Shift+G 输入 /bin/bash→添加并勾选；② `launchctl kickstart -k gui/$(id -u)/com.user.youdao-cleanup` 即时复测（会退出并重启有道翻译）；③ 验收看 ~/.codex/youdao-cleanup.log 出现 CLEAN 且带清理前大小、不再有 Operation not permitted；④ FDA 给 /bin/bash 等于所有 bash 脚本全盘权限，属高影响授权，须用户知情选择
- 教训：launchd 脚本「终端里能跑」不等于「定时能跑」，权限维度以 launchd 负责进程为准；失败分支必须记录 stderr 原文（`find ... 2>&1`），避免把失败误报成 CLEAN

### Pitfall-081 微信 4.x Mac 双开：复制 App 改 Bundle ID 重签名即可，无需第三方分身软件（用户已验证）

- 报错特征/触发关键词：微信双开、微信分身、多开、两个账号、com.tencent.xinWeChat2、Bundle ID、ad-hoc 重签名
- 最近复用：2026-08-16
- 状态：有效（用户已验证）
- 场景：2026-08-16 用户要一台 Mac 同时登两个微信账号、不想频繁切换；第三方“分身”软件有外挂与封号风险
- 现象/路径：复制官方 WeChat.app 到 ~/Applications/WeChat2.app（用户目录免 sudo）；PlistBuddy 改 CFBundleIdentifier=com.tencent.xinWeChat2、显示名=微信2；xattr -cr 后 `codesign --force --deep --sign -` 重签名；open 启动即出现第二个登录窗口；数据容器自动落到 com.tencent.xinWeChat2，与 com.tencent.xinWeChat 完全隔离；验证标准：pgrep 见两个不同路径的 WeChat 主进程、两个容器各自增长
- 根因：WeChat 4.x 单实例检测与数据目录都按 Bundle ID 区分，复制＋改 ID＋重签名后系统视为独立应用
- 有效路径：官方升级后克隆版不自动更新、可能失效，删除后重做一次；官方公告禁止多开、存在封号风险（Mac 端社区实测较低，建议小号先试）；原应用无需改动，删除 WeChat2.app 即可回退
- 教训：用户说“下载分身”不等于必须装第三方软件；本地复制官方 App 改标识是更低风险的可复用路径

## 六、与既有文档的分工

| 文档 | 定位 |
|---|---|
| BadCase 库（BadCase库/） | 总库：通用失败样本、修复闭环与回归集；本库是其「工具调用」模块 |
| 本库（工具调用 Pitfall 经验库） | 通用：所有工具调用、命令、检索、文件、自动化 |
| 《BadCase库/工具调用经验/信息爬取经验与避坑指南》 | 专项：知乎动态爬取（接口、CDP、清洗、校验） |
| 《会话日志与摘要/YYYY-MM-DD/会话摘要.md》 | 流水账：一问一答记录，不承担经验复用 |

专项文档命中时优先专项；专项未覆盖时回查本库。

### Pitfall-102 禁止读取密钥/Token 文件：读取凭据文件既泄密又回传大量输出

- 报错特征/触发关键词：凭据文件、.env、API key、密钥文件、cat 凭据目录
- 最近复用：2026-08-14
- 状态：有效
- 场景：需要核对模型配置/密钥字段名时（DSH 或 Codex 配置排查）
- 现象：2026-08-14 DSH 轨迹复盘发现会话 95d65cd7 直接执行 `cat ~/.dsh/<凭据文件>`，密钥明文进入工具回传（49K 字符），同时违反「密钥需同意」规则
- 根因：规则原表述「读写密钥需同意」在纯读取场景约束不足；排查配置时模型默认 cat 整个文件而非只问字段
- 有效路径：需要密钥信息时只确认字段名/键名（ls 目录、grep 键名不取值）；确需查看内容先向用户说明并征得同意
- 教训：密钥文件内容永不进入工具回传；安全条款用「禁止」而非「需同意」；已同步 DSH 全局 AGENTS §二.5 措辞

### Pitfall-079 分析脚本用完即弃：同一段解压/解析脚本跨会话反复重写

- 报错特征/触发关键词：node -e、python3 -c 内联脚本、解压 jsonl、zstd、脚本重写
- 最近复用：2026-08-14
- 状态：有效
- 场景：会话轨迹/JSONL/配置解析类分析任务
- 现象：2026-08-14 DSH 轨迹复盘：同一会话内 zstd 解压脚本重写 3-4 次、同一段 yaml 解析 node 脚本执行 2 遍、find 全盘扫描跑 2 遍（20K+10K 输出）；跨会话必然重写
- 根因：分析脚本用完即弃无沉淀载体；「少调用」规则只管单会话内，跨会话复用无抓手
- 有效路径：分析类脚本沉淀 `00_系统配置/dsh/scripts/`（DSH 会话解压/统计脚本已入），执行前先查该目录；新脚本用后回写沉淀
- 教训：脚本是资产不是临时品；「先查后用」比「现写现用」省 2-4 次调用/任务

### Pitfall-080 launchd 任务清不掉其他 App 容器缓存：TCC SystemPolicyAppData 权限

- 报错特征/触发关键词：LaunchAgent、~/Library/Containers、Operation not permitted、find: 清理失败、有道缓存
- 最近复用：2026-08-15
- 状态：有效
- 场景：launchd 定时清理另一 App 的沙盒容器缓存（如 `~/Library/Containers/com.youdao.YoudaoDict/Data/Library/Caches/...`）
- 现象：`youdao_daily_cleanup.sh` 每次 12:00/00:00 均 WARN「清理失败」；同一命令在交互 shell 手动执行成功；把 stderr 写入日志后显示 `find: ...: Operation not permitted`；用 `launchctl kickstart` 复现（先放探针文件）确认 launchd 派生进程删不掉
- 根因：`~/Library/Containers/<其他 bundle>/Data` 受 TCC `SystemPolicyAppData` 保护；launchd 直接派生的 `/bin/bash` 无该权限，交互 shell（Terminal/Codex 已授权 AppData）可写；与文件属主、权限位无关
- 有效路径：给 `/bin/bash` 或专用清理助手 App 授予「完全磁盘访问」（系统设置一次性操作）；或调整清理范围绕开容器目录；诊断先复现（launchd kickstart＋探针文件＋stderr 落日志）再判断，别只靠交互 shell 验证
- 教训：launchd 任务权限 ≠ 交互终端权限；清理跨 App 容器前先验证 launchd 上下文是否可写，stderr 必须落日志

### Pitfall-103 第三方 cordis 插件在 DSH tools/pre-execute 上结构不匹配（barricade 全拦 bash）

- 报错特征/触发关键词：Barricade: 工具调用缺少字符串形式的命令字段、cannot get property without inject、tools/pre-execute、arguments.command
- 最近复用：2026-08-20
- 状态：有效
- 场景：给 DSH web profile 挂第三方拦截器插件（dsh-barricade，监听 tools/pre-execute 拦截破坏性命令）
- 现象：安装后所有 bash 工具调用被拦（含 ls/grep）；插件树偶发整体加载失败 `cannot get property "approval" without inject`
- 根因：① Cordis 严格模式禁止访问未 inject 的属性（ctx.approval 未声明即抛错，`??` 兜不住）；② DSH ToolExecution 结构是 `{name, arguments}`（命令在 `arguments.command`），插件按 `args.command` 取必失败，失败安全逻辑变成全拦；③ waterfall listener 契约要求放行时 `return next()`，插件返回 exec 对象破坏链
- 有效路径：inject 声明不全时用 try/catch 包裹访问；命令字段用 `config.commandPath ?? 'arguments.command'` 并加 `obj.arguments?.command` 兜底；listener 签名 `(exec, next)` 且放行 `return next()`（参照 dsh-tool-jobs 写法）
- 教训：挂第三方插件前先对照 DSH 事件类型定义（dsh-tools/lib/types/index.d.ts）核对结构；被插件全拦时用非 shell 工具（read/grep）诊断

### Pitfall-082 link: 插件的依赖必须装进插件自己的目录

- 报错特征/触发关键词：ERR_MODULE_NOT_FOUND、Cannot find module 'mermaid/dist/mermaid.min.js'、link: 协议、MODULE_NOT_FOUND requireStack
- 最近复用：2026-08-20
- 状态：有效
- 场景：profile 用 `link:/path/to/plugin` 安装本地插件（dsh-mermaid、dsh-zagens-office），插件 import 第三方包
- 现象：插件树加载失败 `Cannot find module 'mermaid/dist/mermaid.min.js'`，requireStack 指向工作区真实路径；把依赖装进 profile/node_modules 无效
- 根因：pnpm link 在 node_modules 建 symlink，Node 解析 import 按 symlink 真实路径向上找 node_modules——profile/node_modules 的依赖对 link 插件不可见
- 有效路径：进插件真实目录 `pnpm add <dep>`（依赖落在插件自己目录）；zagens-office 补 @deepseek-ai/schemastery + @deepseek-ai/dsh-tools 即恢复
- 教训：link 插件缺依赖先确认插件目录有无 node_modules，别往 profile 层装

### Pitfall-083 gate_scan 工具 schema 故障：返回未声明字段

- 报错特征/触发关键词：gate_scan、value.summary.categories.network is not a declared property、additionalProperties: false
- 最近复用：2026-08-20
- 状态：有效
- 场景：安装第三方插件前按安全门执行 gate_scan（本地目录）
- 现象：gate_scan 返回 invalid output——输出含 summary.categories.network/permissions/binary/scripts 字段，工具 schema 未声明，重试同样失败
- 根因：gate_scan 工具端 schema 与输出契约不一致（部署故障），与扫描目标无关
- 有效路径：等效人工审查——克隆源码后全量通读（package.json install 钩子、网络回连、eval/exec、写文件路径、密钥读取），重点核 execFile 参数是否经 shell、落盘目录、大小限制
- 教训：安全门工具故障时用等效人工审查并明确告知用户替代路径，不能跳过审查直接装

### Pitfall-084 pkill -f 会匹配自身命令行（自杀）

- 报错特征/触发关键词：pkill -f "dsh web"、EADDRINUSE、进程没被杀、自己 bash 被杀
- 最近复用：2026-08-20
- 状态：有效
- 场景：重启 dsh web 时用 `pkill -f "dsh web"` 杀旧实例
- 现象：pkill 后旧实例未死、新实例 EADDRINUSE 失败；后台 job 丢失（unknown job）
- 根因：pkill -f 按完整命令行匹配，执行命令的 bash -c 命令行本身含 "dsh web" 字样，先杀掉自己导致后续 nohup 未完整执行
- 有效路径：先 `lsof -ti :3080` 拿精确 PID 再 kill；多步重启写脚本一次完成并验证端口释放
- 教训：杀进程用 PID 或精确匹配，别用会匹配自身的宽泛 -f 模式

### Pitfall-085 MCP SDK 1.30 注册 resources/list 前必须先声明 capabilities

- 报错特征/触发关键词：Server does not support resources (required for resources/list)、assertRequestHandlerCapability、MCP SDK 1.30.0、McpServer capabilities
- 最近复用：2026-08-20
- 状态：有效
- 场景：vision-proxy MCP server（stdio）由 DSH/Codex 拉起，SDK 从旧版升到 1.30.0
- 现象：server.mjs 启动即抛 `Server does not support resources (required for resources/list)`，进程退出，MCP 工具（describe_image/ocr_image）不注册；旧 SDK 下同样代码正常
- 根因：MCP SDK 1.30 的 `Server.setRequestHandler(ListResourcesRequestSchema, ...)` 会先校验 server 是否声明了 resources 能力，未声明即抛错（低层 handler 与能力声明绑定）
- 有效路径：`new McpServer(info, { capabilities: { resources: {} } })` 声明能力后再注册空资源处理器（resources/list 与 resourceTemplates/list 均返回空数组）；验证以 MCP 工具是否出现在模型工具列表为准（握手成功才注册），而非只看进程没崩
- 教训：升级 MCP SDK 后低层 handler 注册变严；排查"声称已修复"的同类问题时先核对报错行号对应的是新旧文件哪一版，再判断是否真生效

### Pitfall-086 LaunchAgent 未签名采集器反复请求访问桌面：重编译与后台 TCC 身份变化

- 报错特征/触发关键词：电脑行为采集器、想访问桌面文件夹、LaunchAgent、允许后再次请求、ContentsOfDirectory、未签名二进制
- 最近复用：2026-08-30
- 状态：有效
- 场景：LaunchAgent 常驻运行本地电脑行为采集器，程序启动时读取工作区配置、项目上下文和桌面下的数据目录；实现期间多次重新编译并替换运行副本
- 现象：用户已经允许多次，macOS 仍重复弹出“电脑行为采集器想访问桌面文件夹中的文件”；后台进程可能存在但卡在文件打开或目录枚举阶段，事件不再增长
- 根因：macOS TCC 授权不是“允许次数累加”；未签名命令行二进制被反复替换后，代码身份/请求上下文可能变化，且 LaunchAgent 与交互式终端不是同一权限主体。启动阶段直接访问 Desktop 会把该权限问题变成阻塞或重复弹窗
- 有效路径：不要要求用户无限次重复授权；把启动必需的规则副本和运行态数据放到用户级 Application Support，避免启动阶段枚举 Desktop；保留工作区配置作为可审阅副本，变更后显式同步运行副本；每次改动后同时核对 LaunchAgent 状态、进程栈、数据库事件是否继续增长
- 教训：交互式终端能读写不等于 LaunchAgent 能读写；TCC 弹窗出现时先区分“新二进制身份”“后台权限主体”和“Desktop 目录访问”，不能把重复点击“允许”当作修复

### Pitfall-087 日记日期后置触发语未被识别：Stop 误归类为普通提问

- 报错特征/触发关键词：8月30日日记三个产出、昨日日记三个产出、手工补录缺失、普通提问表达归档
- 最近复用：2026-08-31
- 状态：有效
- 场景：用户把长篇口述日记放在前面，最后只追加“某日＋日记三个产出”，由 UserPromptSubmit 注入日记工作流、Stop 负责把第三项建议写入手工补录本
- 现象：8 月 30 日三个产出已经在对话中生成，但 `手工补录全天日记版/2026-08-30.md` 未创建；该轮进入普通对话归档，原因不是写入权限或索引故障
- 根因：触发器只匹配“完成/整理/处理/生成/输出……日记三个产出”，没有覆盖“日期＋日记三个产出”及“昨日日记/今日日记”后置表达
- 有效路径：共享 `is_diary_trigger` 与 UserPromptSubmit 正则同时支持标准触发语、日期前缀、昨日/今日前缀和无前缀“日记三个产出”；回归时同时验证“长篇真实日记触发”和“普通讨论不误触发”，并从已有对话归档补回漏掉的日期文件
- 教训：日记触发不能只测试标准句式；要覆盖用户实际的尾部短语，并以手工补录文件、类型字段和 HTML 索引三者的真实产物作为验收依据

### Pitfall-088 `codex exec` 不接受 `--ask-for-approval`：子命令参数不能照搬顶层 CLI

- 报错特征/触发关键词：`codex exec --ask-for-approval`、unexpected argument、Codex CLI 0.153.0
- 最近复用：2026-09-05
- 状态：有效
- 场景：用 `codex exec` 启动只读隔离任务时，尝试沿用顶层 `codex` 的审批参数
- 现象：子命令立即返回参数错误，任务未启动；改用 `--sandbox read-only` 后正常运行
- 根因：顶层 CLI 与 `exec` 子命令的参数面不同；当前 `exec --help` 未列出 `--ask-for-approval`，不能假设顶层选项对子命令同样可用
- 有效路径：执行具体子命令前先读取该子命令的 `--help`；本次只读测试使用 `--ephemeral --sandbox read-only --skip-git-repo-check`，并将记忆生成显式关闭
- 教训：命令参数必须按实际子命令帮助核验；参数错误只证明启动方式不兼容，不应误判为模型、网络或记忆功能故障

### Pitfall-089 独立代理端口仍被系统TUN接管：节点排名可能反转

- 报错特征/触发关键词：FlClash、TUN、AnyTLS几乎全失败、香港01好02差、独立Mihomo、403/421、finished.marker与running矛盾
- 最近复用：2026-09-06
- 状态：有效；用户已授权修正监测架构并续跑一周，V6单元与实机烟测通过
- 场景：V5独立核心只更换端口并关闭自身TUN，按未认证OpenAI HTTP响应率推荐三份配置节点，用户反馈排名与真实使用基本相反
- 现象：不绑定物理网卡时香港01/新加坡01反复超时、02可达；只绑定en0（不换DNS）后01恢复；只换DNS不绑定仍失败。新烟测香港01两个HTTPS目标约156/147ms，香港02约4927/6817ms；Happy猫日本JP1、网际快车日本直连也恢复可达，旧0%不可沿用
- 根因：当前FlClash TUN仍可能接管独立核心的上游流量，端口隔离未隔离出口；只查组now未查实际连接链；把curl退出0/HTTP403或421提升为业务可用；同名节点没有订阅指纹；到期只写marker而不更新状态和卸载任务
- 有效路径：逐节点绑定真实网卡＋固定监听入口＋实际chains验证；使用系统CA保持TLS校验；严格204、401JSON、挑战页、403、421分别保存；首测和补测分开、源配置指纹分层；新窗口单独存数；到期先落盘完成状态和报告，再归档plist并卸载自身
- 教训：先验证测量方法与用户实际路径的一致性，再比较节点；任何监测环境异常不得直接判为节点差。旧数据可保留，但失效排名须显式撤回。未测试登录、WebSocket和长会话就不得承诺Codex稳定性
- 证据与回滚：[监测纠偏与验收](../../00_系统配置/网络监测/监测纠偏与验收-2026-09-06.md)；原始旧日志和两个遗留临时目录可恢复归档，原始订阅未改

### Pitfall-090 CUA原生Safari设置操作：完整快照重编号与观察失败后防重复提交

- 报错特征/触发关键词：cua_repl、Safari、disableDiffing、控件编号重建、SCStreamErrorDomain、-3812、-10005
- 最近复用：2026-09-06
- 状态：本次实机验证有效；底层截图失败机制待验证
- 场景：通过CUA原生应用接口复制ChatGPT账号偏好，每次操作后检查可访问性状态。
- 现象：请求完整快照后仍用前一快照编号，原计划点击风格菜单却展开Safari分享菜单；立即取消，未选择收件人或发送。另一次选择绿色后观察接口连续两次返回ScreenCaptureKit参数无效，重新取得Safari应用对象后确认绿色已经保存。
- 根因：完整快照或菜单状态变化可重建编号，编号不是持久标识；动作成功与后续观察成功是两个结果。截图失败的底层原因未确认，不推断为账号保存失败。
- 有效路径：每次观察后从最新返回文本按准确标签重新解析编号，先确认菜单内容再选目标；观察失败不重复执行写入，使用已知bundle ID重新取得应用对象，再只读核对实际值。自定义指令与职业须点击页面保存按钮，最后刷新并逐字比对原文与换行。
- 教训：不能在取得新快照后沿用旧编号；工具报错不等于操作未生效，恢复观察后再决定下一步。不使用应用内部接口、凭据或未经授权的替代控制技术。

### Pitfall-091 官方 Computer Use 不允许操作 Codex 自身设置页：组件存在不等于 Locked use 已启用

- 报错特征/触发关键词：`Computer Use is not allowed to use the app 'com.openai.codex' for safety reasons`、`CUALockScreenGuardian`、`-10005`、Locked use 设置核对
- 最近复用：2026-09-07
- 状态：有效
- 场景：用户批准在 Codex Settings → Computer Use 中核对并开启 Locked use，并要求随后用 Calculator 做一次锁屏续接验证
- 现象：官方 `node_repl` 能列出 ChatGPT/Codex 应用，但对 `com.openai.codex` 按显示名和 Bundle ID 读取界面都被官方安全策略拒绝；对锁屏守护组件的状态读取超时。系统设置中没有对应的 Codex 开关页。未启动 Calculator，也未重复点击或改写配置。
- 根因：当前官方 Computer Use 入口将 Codex 自身窗口列为不可操作目标；本机存在 `SkyComputerUseService`、`CUALockScreenGuardian` 或 `preventSleepWhileRunning` 只能证明组件/保活机制存在，不能证明 Locked use 已开启或可跨锁屏续接。
- 有效路径：停止同一目标的重复调用；要求用户手动打开 Codex Settings → Computer Use 核对开关。开关无法确认或不可用时，任务开始前明确提示“需要保持解锁”，不启动锁屏验证；只有用户确认开关已开启后，才用官方 Computer Use 启动 Calculator 并执行一次不可逆动作之外的短时锁屏观察，失败只记录阻断，不重放上一次操作。
- 教训：官方入口拒绝自身设置页时不能用手动 node_repl 桥接、AppleScript、JXA 或直接改偏好文件绕过；必须区分“官方入口可用性”“设置开关状态”“守护进程存在”和“锁屏续接实测”四层证据。

### Pitfall-094 FlClash 自动选节点切换导致同一故障重复弹窗

- 报错特征/触发关键词：FlClash、自动选择、节点切换、关闭多次、重复提醒、dismissed、alert_triggered
- 最近复用：2026-09-08
- 状态：有效
- 场景：用户手动关闭节点延迟提醒后，FlClash 自动选择在同一网络故障期间连续切换节点
- 现象：日志在约两分钟内连续记录多个配置/节点的 alert_triggered；用户实际需要关闭右上角提示多次，面板不是单实例创建问题，而是故障状态被节点变化重新武装
- 根因：旧逻辑把配置/节点选择键变化当成新状态并重置 active；没有跨选择变化继承同一故障的 dismissed 抑制标记
- 有效路径：节点变化只更新配置、节点和测量字段，保留 active、dismissed 与故障周期；只有连续两轮低于恢复阈值才清除 dismissed；同一故障期间不重复写入 alert_triggered
- 教训：自动选择器的节点变化不是故障边界；告警去重应按故障周期和恢复条件，而不是按节点名称分段

### Pitfall-095 Codex Stop Hook 入队 `/compact` 只生成普通用户消息，未执行压缩

- 报错特征/触发关键词：Codex、Stop Hook、300K、`compact_queued`、队列中出现 `/compact`、没有 `contextCompaction`
- 最近复用：2026-09-08
- 状态：已避开普通消息误入队；自定义300K动作仍未完成
- 场景：希望所有项目主会话在回答完成后，当前上下文超过300000 token时自动压缩；第一版Hook通过 `codex queue --message /compact` 投递命令
- 现象：Hook实际读到327603和364310 token并成功入队，但rollout没有产生 `contextCompaction`；`/compact`被当前执行路径当作普通用户消息，窗口继续增长
- 根因：CLI队列接口只保证提交一条会话消息，不保证把消息解析为桌面端斜杠命令；把“命令文本入队”和“App Server压缩操作”混为一件事
- 有效路径：不再把队列消息当斜杠命令；后续请求改为pending并由独立执行器处理，但是否能取得桌面端writer必须单独验证
- 教训：自动化动作必须验证最终状态事件，不能把“队列写入成功”当作“压缩已完成”；Hook只在用户级配置被信任后才会生效

### Pitfall-096 Stop Hook 内直接压缩被自身 active writer 生命周期阻塞

- 报错特征/触发关键词：Codex、Stop Hook、`thread/compact/start`、`active writer`、`inflight=true`、408K仍未下降
- 最近复用：2026-09-08
- 状态：已避开Stop Hook自身等待环；仍受桌面端writer限制
- 场景：把直接App Server压缩放进异步Stop Hook，期待回答完成后马上压缩
- 现象：Hook确实触发并启动App Server，但`thread/resume`持续返回`thread already has an active writer`；Hook自身的进程未退出，用户界面上下文继续增长
- 根因：Stop Hook仍处在当前turn的writer生命周期内；Hook进程等待writer释放，writer又要等Hook结束，形成等待环
- 有效路径：Stop Hook只写pending请求并立即退出；独立LaunchAgent先判回合边界，拿不到writer时延期并长退避；这只消除自身等待环，不等于当前桌面会话一定可压缩
- 教训：执行压缩的进程不能绑定在触发压缩的turn生命周期内；必须把检测、排队和实际动作拆成两个生命周期

### Pitfall-097 桌面端持有 thread writer 时外部 App Server 不能完成回合后压缩

- 报错特征/触发关键词：`thread already has an active writer`、LaunchAgent、`compact_starting`持续出现、没有`contextCompaction`
- 最近复用：2026-09-08
- 状态：有效
- 场景：Stop Hook 已退出并由独立 LaunchAgent 调用 App Server，仍要求当前桌面打开会话在每次回答后立即压缩
- 现象：LaunchAgent 确实被加载，但`thread/resume`持续返回`active writer`；此前会持续启动外部`codex app-server`并写失败事件，用户界面上下文没有因该自定义动作下降
- 根因：当前桌面会话的 writer 由桌面端持有；公开 App Server 客户端无法接管同一 thread，Stop Hook 也没有可直接调用桌面端内部`thread/compact/start`的受支持接口
- 有效路径：Stop Hook只写pending；执行器先读取 transcript 回合边界和`context_compacted`；活动回合只记录`compact_deferred_active_turn`，外部`active writer`只记录`compact_deferred_active_writer`并长退避，不把失败重试伪装成完成
- 教训：严格“回答完成后且桌面会话仍打开立即压缩”目前没有可验证的公开实现；必须把“已发起”“已观察到内置压缩”和“执行器收到`contextCompaction`”分开报告，或改用受支持的内置阈值/手动 Compact

### Pitfall-093 FlClash 延迟指标混用：HTTPS总耗时不能替代节点原生 delay

- 报错特征/触发关键词：FlClash、400ms、延迟提醒、generate_204、native delay、HTTP总耗时、误报
- 最近复用：2026-09-08
- 状态：有效
- 场景：为当前 FlClash 选中配置和节点增加 400ms 延迟提醒；用户界面显示“网际快车.yaml(1) → 台湾家宽·直连·3倍消耗”约104ms
- 现象：第一版独立探针测得当前有效 HTTPS 总耗时约913.9ms，若直接套用400ms阈值会弹出“节点延迟过高”；该值包含路径建立、协议处理和远端响应，不能等同 FlClash 节点卡片的原生延迟
- 根因：FlClash 卡片使用 Mihomo 节点 delay 测试口径，而 HTTPS 总耗时是业务探针口径；两者测量阶段、连接复用和远端服务因素不同，混用会把业务端点慢误归因于节点原生延迟
- 有效路径：从当前生效配置与只读数据库选择记录匹配配置和节点；在隔离 Mihomo 核心中绑定真实物理接口，对同一节点调用 /proxies/<node>/delay?url=http://www.gstatic.com/generate_204&timeout=5000&expected=204；提醒阈值只作用于 native_delay，业务HTTPS总耗时另行记录，不参与该提醒
- 教训：先固定指标定义再设阈值；“节点原生延迟”“当前业务请求耗时”“Codex长连接稳定性”必须分栏验证，不能用一个数字代表全部网络体验

### Pitfall-092 zsh 诊断脚本使用保留变量导致网络结果无效

- 报错特征/触发关键词：zsh、`read-only variable: status`、`command not found: tr`、`command not found: cut`、网络诊断脚本
- 最近复用：2026-09-07
- 状态：有效
- 场景：macOS zsh 中并行执行 Ping、DNS 和 HTTPS 轻量网络基线采样
- 现象：变量名 `status` 使脚本在 DNS 阶段提前停止；改用变量名 `path` 后，zsh 的特殊 `path` 数组覆盖了命令搜索路径，导致 `tr`、`cut` 等外部命令不可用，HTTPS 结果被错误标为失败。
- 根因：zsh 内置了只读的 `status` 状态变量；`path` 与环境变量 `PATH` 绑定，不能把它当普通局部变量使用。
- 有效路径：退出码使用 `rc`，路由模式使用 `route_mode` 等非保留名称；修正后只采信完整重跑结果，失败轮次不并入统计。
- 教训：网络诊断要把脚本执行完整性与网络证据分开验收；出现命令错误时先丢弃该轮数据，不把脚本失败写成链路失败。

### Pitfall-098 CUA单次CDP大文本导出导致调试管道中断

- 报错特征/触发关键词：`Runtime.evaluate`、`native pipe closed before response`、`Debugger unattached`、大段Markdown、Blob下载
- 最近复用：2026-09-08
- 状态：有效
- 场景：通过认证浏览器读取多期周报正文后，尝试用一次CDP表达式将约43.8万字符的Markdown直接生成本地文件
- 现象：单次大表达式返回`native pipe closed before response`，随后原标签的CDP连接短暂不可用；已提取的正文仍保留在CUA会话变量中，未丢失
- 根因：待验证；更可能是CDP调试管道或参数序列化对单次超大表达式存在大小限制，而非页面正文读取失败
- 有效路径：重新创建同源空白研究标签并先导航到目标页面，确认新CDP连接可用；将正文按约2万字符切块，通过多次`Runtime.evaluate`暂存，再由最后一次小表达式组装Blob下载；导出后用文件大小、字符数、哈希和结构断言复核
- 教训：大文本传输不要一次性塞入CDP命令；读取成功、导出失败和调试器断连必须分开记录，优先保留内存结果并采用分块恢复，不重复抓取已完成页面

### Pitfall-099 引用行号断言未与命中内容比对导致错误定位

- 报错特征/触发关键词：`grep -n`、行号断言、"只写在某文件第 N 行"、引用同步检查、rg 结果核对
- 最近复用：2026-09-08
- 状态：有效
- 场景：核对日记工作流规则落在哪些文件时，用 grep 拿到命中行号后，直接断言"跨项目补查只写在 README 第 10 行"，未回读该行内容
- 现象：README 第 10 行实际是口述日记归档规则，与断言无关；该错误结论已写入回复，需下一轮自我更正
- 根因：把"文件命中"与"指定行号命中"混同，且未把命中内容与断言逐条比对就输出
- 有效路径：给出行号级断言前回读该行并确认语义匹配；命中多条时逐条标注哪条支持结论、哪条只是同词命中；无法回读时只写“某文件出现该表述”，不写行号
- 教训：引用定位属于事实断言，证据是“命中行内容”而非“命中位置”；行号只是索引，不能替代内容核验

### Pitfall-100 DSH Web profile 的本地 link 依赖保留旧工作区路径

- 报错特征/触发关键词：`cannot resolve profile bundle`、`dsh-barricade`、`link:/Users/.../Desktop/deepseek harness/`、`ERR_CONNECTION_REFUSED`、3080
- 最近复用：2026-09-09
- 状态：有效
- 场景：DSH 工作区目录改名后，Web profile 仍引用 `dsh-barricade`、`dsh-mermaid` 的旧绝对路径。
- 现象：两个 `node_modules` 链接目标不存在，`dsh web` 在监听 3080 前退出，浏览器访问 `127.0.0.1:3080` 被拒绝。
- 根因：`~/.dsh/profiles/web/package.json` 与 `pnpm-lock.yaml` 同时保留旧的绝对和相对 link 路径，pnpm 未自动迁移本地链接。
- 有效路径：先确认当前源码目录并备份 profile 清单；同步更新两个 manifest 的 link 路径；运行 `pnpm install --offline --frozen-lockfile --ignore-scripts` 重建链接；再用 `dsh plugin --profile web list`、单实例 `dsh web` 与 `curl 127.0.0.1:3080` 验证。
- 教训：工作区改名后必须同步检查 profile manifest、lockfile 和 `node_modules` 链接；启动验证期间不要并行运行多个会占用 3080 的 DSH 实例。

### Pitfall-101 DSH 安全探针自身未验收：URL 路径残留与无断言假通过

- 报错特征/触发关键词：`new URL(...).pathname`、`fixture-malicious`、百分号编码目录、正常命令 block、退出码 0、扫描探针
- 最近复用：2026-09-09
- 状态：缺陷已复现；仅完成终审与修复建议，未修改探针、护栏或清理残留。
- 场景：复核 DSH-00—05 迁移的安全探针及“全部验收通过”结论。
- 现象：扫描脚本使用 URL.pathname 作为本地路径，含空格和中文的目录被百分号编码后另建；报告称样本已删除，实际编码路径仍有 index.js 与 package.json。另一个判定探针给“正常 bash”传入 args.command，返回 block 却仍退出 0；使用真实 arguments.command 结构进行纯判定对照时正常命令为 allow。
- 根因：URL 路径与文件系统路径混用；测试输入形状与真实工具调用不一致；脚本只打印结果，没有预期值断言及失败退出；静态测试、运行证据和业务验收混为一谈。
- 有效核验路径：只读比对 URL.pathname 与 fileURLToPath 所指的两个目录；纯调用判定函数检查真实与畸形入参，绝不执行其中的命令；逐项对照预期值、实际结果和退出码。上述核验已完成，未运行带写入副作用的扫描探针或样本。
- 修复建议（待批准）：测试输入改用无执行能力的内存数据；需要临时文件时使用受控唯一临时目录和 fileURLToPath，登记并验证生命周期；采用断言驱动退出码；扫描工具须支持明确目标并列出跳过项，不能把固定两个测试对象冒充通用安装检查。
- 教训：探针自身也要验收；看见退出 0、样本 BLOCK 或预期路径为空，均不足以证明完整通过。护栏误报应最小复现并经批准修复，禁止把改换执行载体绕过拦截写成常规操作。
- 证据：[扫描探针](<<HOME>/Desktop/deepseek harness coding agent（DSH）/00_系统配置/dsh/迁移记录/2026-09-09/probe-gate-scan.mjs:40>)、[判定探针](<<HOME>/Desktop/deepseek harness coding agent（DSH）/00_系统配置/dsh/迁移记录/2026-09-09/probe-barricade.mjs:13>)。

### Pitfall-104 项目改名后 Codex 项目钩子仍引用旧绝对路径

- 报错特征/触发关键词：项目改名、`.codex/hooks.json`、旧绝对路径、归档未写入、PreCompact、修改清单、路径不存在
- 最近复用：2026-09-09
- 状态：待验证（本次路径修复的静态检查和隔离运行链已通过；Codex 应用重新信任与后续真实回合仍待验证）
- 场景：当前 DSC 项目目录由旧工作区名称变为含中文括号的实际目录后，项目级 Codex 钩子和两个 Shell 输出脚本仍保留旧目录路径
- 现象：`hooks.json` 的 9 个命令均指向不存在的旧目录；PreCompact 和 PostToolUse 也把输出写向旧位置，导致当前项目钩子不能按配置找到入口，项目归档出现 91 个待归档用户消息积压（积压内容未在本条处理时删除或批量补写）
- 根因：配置文件内的绝对路径不会随项目目录改名自动迁移；脚本内部又重复硬编码旧输出根，未从脚本位置或实际项目根推导
- 有效路径：钩子入口更新为当前真实项目路径；输出脚本用 `dirname "$0"` 推导 `.codex`，再取上级作为项目根；在临时副本中从项目外目录运行 PreCompact，并使用隔离 `CODEX_CONVERSATION_ARCHIVE_ROOT` 完成用户消息→助手回复→JSONL 的最小端到端验证
- 教训：项目复制或改名后先核对活动钩子的命令目标和脚本输出根；历史记录中的旧路径保留为证据，不对历史正文做批量替换；静态路径存在不等于 App 已重新信任，必须分开报告真实回合验证

### Pitfall-105 摄像头批量解码未设资源闸门导致 CPU 与磁盘读写冲高

- 报错特征/触发关键词：多路 `ffmpeg`、CPU 空闲下降、风扇加速、磁盘读写冲高、外置盘、批量解码、低线程
- 最近复用：2026-08-31
- 状态：待验证（已验证停止高负载任务有效；低线程并发上限和长期资源预算仍待复测）
- 场景：2026-08-31 对萤石录像进行高密度关键帧/音频复盘
- 现象：活动监视器显示多个 `ffmpeg` 同时占用约 38%—55% CPU，`kernel_task`、IINA 和外置盘读写同时升高；磁盘页显示读取累计约 208.21 GB、写入约 118.48 GB。停止本轮相关任务后 CPU 空闲回升、读写明显回落。
- 根因：批量解码并发与外置盘 I/O 未在启动前绑定资源预算；具体瓶颈比例和最优并发数尚未单独测量，不能由一次截图推出固定上限。
- 有效路径：先单通道低线程试跑；用户已确认可尝试两路，但以 CPU 空闲率平均不低于 30% 为硬阈值，低于阈值立即停止并退回单路；每块控制时长和读写范围，完成后再扩展。
- 教训：视频任务必须把内容覆盖、资源占用和停止条件分开验收；“进程正在运行”不等于可接受，不能恢复上轮 8 路并发。

### Pitfall-106 并发会话同时改同一文件：edit 报 file changed since read，先重读再改

- 报错特征/触发关键词：`cannot edit ... file changed since it was read`、`re-read the file, then retry`、并发会话、另一 Agent 同时写入
- 最近复用：2026-09-09
- 状态：已验证
- 场景：2026-09-09 在 DSC 项目同步根 `README.md` 结构表时，同一分钟另一会话也修改了该文件
- 现象：`edit` 直接失败并提示文件自上次读取后已变化，此前的读取版本已过期；同一文件的其他位置仍正常
- 根因：同一工作区可能有并行会话或用户手动写入同一文件；读取-修改按文件指纹做乐观锁校验，过期即拒绝，不是权限或路径问题
- 有效路径：不要原样重试旧 old_string；先 `read` 重新读取目标区域确认当前内容，再用新锚点重新 `edit`；改完 `rg` 复核引用；`修改清单` 出现非本人写入行即为并发信号
- 教训：多会话并行的工作区，改共享文件前先重读；一次失败即重读，不重复盲试

### Pitfall-107 关停「服务提供行」会让下游插件全部 pending：inject 是硬依赖

- 报错特征/触发关键词：`Failed to load plugins`、`pending (waiting for service: fileUploads)`、`pending (waiting for service: sidebarRight)`、`did not activate`、profile patch `disabled: true`
- 状态：已验证
- 场景：2026-09-10 给 DSH Web 做「极简化」裁剪，用 `~/.dsh/profiles/web/cordis.patch.yml` 关停自认为的「界面展示行」
- 现象：①关 `file-upload` → `dsh-api-session-controller` 等 20 个插件 pending、页面白屏；②关 `ui-sidebar-right` → `ui-chat`、`ui-sidebar-files`、`ui-sidebar-documentpreview` 三个包 pending，页面只显示错误页。两次都需外部（Codex）回滚配置才恢复
- 根因：cordis 的 `inject` 默认必需。客户端包的 `package.json → dsh.client.inject` 声明它依赖的其它客户端包；被依赖方不在组合里，依赖方就永久 pending。`ui-sidebar-right` 提供 `sidebarRight` 服务（被 3 个包 inject），`file-upload` 被 `ui-conversation` inject —— 它们不是「展示行」
- 有效路径：关停任何行前先跑依赖图检查——`node 00_系统配置/dsh/scripts/inject-graph-ui.mjs`（输出「被依赖包 → 依赖它的包」全景，`--check a,b` 直接校验）；并用 `preflight-ui-trim.mjs` 走过白名单＋保护名单＋inject＋id 存在性四项预检；改完先 `dsh --profile web --patch <file> --dump-config` 离线验证退出码
- 教训：「看起来只是 UI」不等于可关；官方 Web UI 里绝大多数字面展示行都处在被依赖位置。可安全关停的面很窄（本机实测只有 `ui-open-in-app`、`ui-sidebar-documentpreview` 两个），判据是依赖图而非直觉
- 最近复用：2026-09-10

### Pitfall-108 改 UI 样式不要落到参与客户端模块图的插件 JS

- 报错特征/触发关键词：`Failed to load plugins`、`client-modules 清单里的插件加载异常`、`ui-renderer 未注册`、修改 `dsh-client-ui-theme/lib/client.js`、`/plugins/??…&rev=`
- 状态：已验证
- 场景：2026-09-10 给 DSH Web 做「海洋主题」，v1 把自定义 CSS 追加到 `@deepseek-ai/dsh-client-ui-theme/lib/client.js` 末尾（想借它注入 `--dsw-*` 变量）
- 现象：第一次完全无效果（样式块放在 `define(...)` 之后，模块定义后的顶层代码不保证执行，`<style>` 从未插入 DOM）；改为包装插件 `apply()` 后，页面出现整页插件加载错误，用户侧两次崩页、两次由 Codex 回滚
- 根因：该 JS 属于**客户端模块图**，服务端按内容哈希下发 `rev`，「版本化代码不可变、修订号不匹配即拒发」；改动它会让旧页面缓存的 rev 与新组合不一致，进而整页失败。样式改动被卷进模块加载链路，风险与收益完全不成比例
- 有效路径：样式只落**产物样式表** —— 追加到 `…/@deepseek-ai/dsh-web-frontend/dist/assets/index-*.css` 末尾，用 `html body` + `!important` 提权覆盖官方主题变量（前端 CSS 由 `<link>` 加载，不参与模块图）；封装成幂等脚本 `00_系统配置/dsh/scripts/apply-ocean-theme.mjs`（`--check`/`--revert`），自带大括号配平与标记自检
- 教训：改样式前先问「这个文件参与不参与模块加载图」；参与就换落点。纯 CSS 追加可随时 `--revert`，升级 dsh 后重跑一次即可
- 最近复用：2026-09-10

### Pitfall-109 多实例并存会让同一界面看起来不一致（两个回形针）：先查端口与宿主

- 报错特征/触发关键词：`一个窗口两个回形针、另一个一个`、`同样地址表现不同`、`旧页面报错新页面正常`、`自动重连中`、`Failed to fetch`
- 状态：已验证
- 场景：2026-09-10 DSH 排查期间，本机同时跑着 3080 与 3081 两个 `dsh web` 实例，用户两个窗口各连一个
- 现象：Codex 桌面窗口（3081）输入框有两个回形针，Chrome（3080）只有一个；一侧页面报 `waiting for service`，另一侧正常；刷新裸地址只得到 401/拒绝连接
- 根因：①两个实例的组合不同——3081 是旧实例，仍加载着已从 profile 卸载的 `dsh-file-drop`（它的回形针按钮 + 内置附件按钮 = 两个）；②0.1.5 的 cookie 绑定 authority，且每次启动换 launch token，裸地址没有 cookie 必然 401；③`自动重连中` 只是前端在等已经退出的后端进程，重连本身救不回来
- 有效路径：先 `lsof -nP -iTCP:3080 -iTCP:3081 -sTCP:LISTEN` 查清有几个实例；用 `env | grep ^DSH`（`DSH_WEB_URL`/`DSH_SESSION_ID`）或 `ps -o ppid= -p $$` 判断当前会话挂在哪个实例上（**杀掉宿主实例会连带终止该会话**，先确认再动手）；统一只保留一个端口（本机定为 3080，入口 `DSC/启动DSH.command`），并用该次启动打印的完整 `?token=` 地址打开一次换取 cookie
- 教训：界面表现不一致先怀疑「不是同一个后端」，而不是去查主题、缓存或插件；多实例还会互相掩盖真实问题
- 最近复用：2026-09-10
### Pitfall-110 日记三产出的比例是硬约束：不先计数就会反复删改

- 报错特征/触发关键词：`AI 总结版控制在原文的 80%—85%`、`意图还原主正文 60%—80%`、`产出超长需二次压缩`、`日记提示词存在两份副本`
- 状态：已验证
- 场景：2026-09-10 执行 DSC 日记工作流，处理 4,813 个非空白字符的全天口述；前台交 AI 总结版、待办事项版、口语化词汇优化建议，文档层续写 Codex 项目两个总库与两处索引
- 现象：AI 总结版初稿 4,391 字（占原文 91.2%），超出 3,850—4,091 上限，连续删改三轮才落到 4,088 字；同时发现 DSC 侧只有 `00_系统配置/codex/备份-日记工作流-20260908/日记处理提示词.md`，其手工补录路径仍指向旧 DSH 目录
- 根因：①比例口径按「去除空白与换行后的 Unicode 字符数」计算，凭感觉写作必然偏差 5%—10%；②日记提示词有活动版与备份版两份，活动版在 Codex 项目 `提示词文件/日记处理提示词.md`，备份版路径未随 2026-09-10 的日志路由迁移同步
- 有效路径：先把原始口述写入临时文件，用 `python3 -c "import re;print(len(re.sub(r'\s','',open('F').read())))"` 算出 80%—85% 与 60%—80% 的上下界，再按界写作、每轮改完立即复算；取材与落盘以活动提示词为准，手工补录落 DSC `会话日志与摘要/口语化表达/手工补录全天日记版/`，续写后跑 Codex `日记/生成日记索引.mjs` 与 DSC `会话日志与摘要/生成对话与表达索引.mjs`
- 教训：比例类硬约束先计数再写正文，可省掉整轮删改；同名提示词有多份副本时先确认活动版与路径，不按备份版落盘
- 最近复用：2026-09-10
### Pitfall-111 守护脚本的规范副本与实机漂移：按副本回滚会静默改回旧阈值

- 报错特征/触发关键词：`规范副本与实机不一致`、`CHROME_IDLE_MINUTES`、`闲置阈值 30 还是 60`、`按 00_系统配置 副本恢复`
- 状态：已验证（差异经 diff 核对）
- 场景：2026-09-11 核查 Chrome 闲置关闭时，比对 DSC `00_系统配置/codex/scripts/close_idle_chrome_windows.sh` 与实机 `~/.codex/scripts/close_idle_chrome_windows.sh`
- 现象：两处都有听悟保护代码，但默认阈值不同——副本写 `IDLE_MINUTES="${CHROME_IDLE_MINUTES:-30}"`，实机为 `60`，注释与第 5 行说明也随之一致地分叉；按副本恢复会把清理阈值静默改回 30 分钟
- 根因：实机脚本先改、规范副本未同步；该类副本是「实机全局配置的规范副本」，但没有自动比对机制，只能人工 diff
- 有效路径：改动 `~/.codex/scripts/` 下任一脚本后，立即 `diff` 对应 `00_系统配置/codex/scripts/` 副本并同步；核对时不要只看关键功能是否存在（本例听悟保护两边都有），要连带默认值、注释一起比
- 教训：功能一致不等于版本一致；阈值类默认值漂移没有报错，只会在某次回滚或重建时才发现
- 解决记录：2026-09-11 按用户选择把两侧统一为 30 分钟（实机 :-30），并把听悟保护从「全局停摆」改为「按窗口豁免」；diff 复核两侧字节一致，实机 dry-run 已命中真实听悟窗口
- 最近复用：2026-09-11

### Pitfall-112 脚本用标记字符串定位区段时，别在别处写出该标记：一次静默丢来源

- 报错特征/触发关键词：`text.find("## Sources")`、区段解析、引用静默清空、参考文献条数变少、批次文件头部说明行
- 最近复用：无
- 状态：有效
- 场景：2026-09-11《把人体当作一个产品》G4 扩写后重跑 `汇编最终正文.py` 与 `生成全局引用映射.py`
- 现象：汇编报告「正文引用来源」由 65 掉到 62，正文里既没有空引用 `[]` 也没有任何报错；4C 一节的引用标记被静默清空
- 根因：脚本用 `text.find("## Sources")` 定位来源区；为记录净增字数在 18 个批次文件头部的引用块里追加了一行说明，行文含「## Sources」字样，于是 find 提前命中头部；4C 文件原本用「## 来源说明」、靠 `idx < 0` 走特殊分支，被误判成「有来源区但无条目」，其来源全部丢失，脚注映射为空后汇编替换为空字符串
- 有效路径：把头部说明行里的 `## Sources` 改写成「来源区」，重跑两个脚本后引用来源恢复为 65；并把「引用来源条数」纳入每次汇编后的固定校验，与 `[]` 计数、参考文献条数一起看
- 教训：① 定位串要选不会被写进说明文字的标记，或改用行首整行匹配的结构化边界；② 「无报错」不等于「无损失」，静默降级只能靠计数校验兜住，而空引用计数为 0 恰好掩盖了这次丢失

### Pitfall-113 DSC 日志脚本摘要长度有硬校验：超 180 字直接 exit 1 拒绝写入

- 报错特征/触发关键词：`[未追加] 摘要长度`、`超出 80—180 字区间`、`追加摘要.mjs`、exit code 1
- 最近复用：2026-09-13
- 状态：有效
- 场景：2026-09-13 调用 DSC `会话日志与摘要/追加摘要.mjs` 写会话日志
- 现象：传入约 220 字摘要，脚本 stderr 输出「[未追加] 摘要长度 220 字，超出 80—180 字区间」并以 exit code 1 结束，本轮日志未写入
- 根因：脚本内置摘要长度校验（80—180 字），超出区间即拒绝写入，与路径、参数名、权限无关
- 有效路径：把摘要压到 180 字以内、重调同一条命令即写入成功（同轮内一次修正通过）
- 教训：带格式校验的脚本先按已知约束自检输入再调用，可省一次失败调用；报错已给出合法区间时按区间改内容，不要改命令写法或换工具

### Pitfall-114 官方文档站对本机地区返回 307：改用渲染代理 + Wayback 官方快照双路抓同一 URL

- 报错特征/触发关键词：`307`、`app-unavailable-in-region`、`platform.claude.com`、`docs.claude.com`、地区封锁
- 最近复用：2026-09-13
- 状态：有效
- 场景：2026-09-13 抓取 Anthropic 官方 Claude Fable 5.1 系统提示词发布页
- 现象：docs.claude.com / platform.claude.com 直连返回 307，跳转 claude.com/app-unavailable-in-region，页面正文取不到
- 根因：官方文档站按请求来源地区做访问限制，与 UA、语言路径、反爬无关
- 有效路径：走 r.jina.ai 渲染代理读取同一官方 URL；再用 `web.archive.org/web/<时间戳>id_/<原始URL>` 取官方存档快照；两路正文逐字比对（本例 27933 字符完全一致）后交付
- 教训：① 地区封锁不要靠换 UA 或换语言路径硬试，直接换「渲染代理 + 官方存档快照」双路；② 双路一致可作未篡改的交叉证据，比单路可信；③ 交付时写明内容仍出自官方 URL，代理只是通道

### Pitfall-115 校验中译稿完整性别用标签计数比对：正文引用标签名与代码块剥离会造成大量误报

- 报错特征/触发关键词：标签数差、译稿多标签、译稿缺标签、XML 标签计数、代码块剥离
- 最近复用：2026-09-13
- 状态：有效
- 场景：2026-09-13 校验 10 家模型系统提示词的中译稿与官方原文是否逐段对应
- 现象：自写脚本按 `</?(\w+)` 统计标签数、剥离 ``` 代码块后比对，10 家中 8 家报「标签数差」与「译稿多标签 think/function/IMPORTANT」，逐条核查后全部为误报
- 根因：① 译稿末尾的核验说明节会引用标签名（如「官方 `<refusal_handling>` 内的 `<example>` 块…」）并计入标签数；② 官方页面导出瑕疵（正文夹入孤立 ``` 围栏）会让剥离逻辑把大段正文当代码块剔除，反而制造差异；③ 译文首句若以标签名开头（如「`<policy>` 标签内的这些核心政策…」）会被行首正则误命中
- 有效路径：不做跨文件的标签计数比对；改为 ① 同一文件内开闭标签配对校验（`<x>` 对 `</x>`）；② 逐行位置核对代替序列比对；③ 对关键来源做独立抽验——自己重抓一次官方原始文件并与落盘原文比对（本例 xAI 官方 j2 文件逐字一致）
- 教训：机械校验脚本的信噪比取决于语料形态；跨语言、含说明性引用的文档上，计数比对天然高误报。宁可少而准（配对 + 抽验），不要多而假——误报会掩盖真问题并浪费核查时间

### Pitfall-116 合并多源 Markdown 时「统一降一级」会让章内标题与章标题撞级：改为按各源文件最小层级归一

- 报错特征/触发关键词：章节错位、标题层级倒挂、索引编号对不上、多源合并、标题降级
- 最近复用：2026-09-13
- 状态：有效
- 场景：2026-09-13 把 10 份不同来源的中译稿合并为一份文档，每份作为一章
- 现象：v1 规则「章内标题统一 +1 级」交付后，Meta 章出现 7 个 `## ` 标题、Google 章出现 10 个 `## ` 标题，与章标题同级，读者视为并列章节；索引表的 1—10 编号在正文中找不到对应。用户直接指出「章节有点混乱，也有点错位，索引没对上」
- 根因：① 各源文件标题起点层级不同——有的首行 `#` 后紧跟 `##`，有的内部仍用 `#` 作内容标题，统一 +1 无法保证章内标题都低于章标题；② 章标题为程序生成的纯文本、不带编号，与索引表编号脱钩；③ 个别源文件自身层级倒挂（组织标题用 `##`、其辖下内容标题用 `#`）
- 有效路径：① 章标题由程序统一生成且带编号（`## N. 公司｜模型`），直接取代源文件首行标题；② 章内标题用**嵌套栈**推导真实深度——按源文件层级算出每个标题的嵌套层数，再映射为从 `###` 起的连续层级，一步同时解决「与章标题撞级」「3 跳到 5 的跳级」「源文件自身倒挂」三个问题（中途试过的「最小层级归一」仍会跳级，已弃用）；③ 代码块内 `#` 注释一律不动
- 教训：跨源合并不要用「相对偏移」或「最小层级归一」处理标题，要用「嵌套栈推深度 → 连续映射」；并加三条机械断言——「一级标题数 = 1」「二级标题数 = 章数 + 索引」「逐章检查子标题层级 ≤ 父级 + 1（跳级数 = 0）」，再把索引编号与章标题编号逐条比对。这三条断言能在交付前抓住本次全部缺陷，不必等用户指出两轮
