# Codex 从 0 到 1 学习资源库（50+ 权威来源·非技术版导读）

> 整理日期：2026-08-02（北京时间）
> 适用对象：不搞技术、但想真正理解 Codex「是什么、怎么工作、怎么用得好」的人。
> 使用方式：先读「第 0 节」，再按兴趣进入对应分类；每条来源都附一句话说明，避免枯燥说明书式罗列。

## 0. 先读这 5 条，最快建立全貌

1. [在你的 ChatGPT 套餐中使用 Codex（官方帮助中心·中文）](https://help.openai.com/zh-hans-cn/articles/11369540-codex-in-chatgpt)：官方对 Codex 最直白的定义、套餐额度、插件、数据控制问答。非技术读者从这里开始最合适。
2. [Introducing Codex（OpenAI 官方博客）](https://openai.com/index/introducing-codex/)：Codex 的产品出生证明——发布时的定位、云沙箱、模型能力（codex-1）。
3. [Codex 最佳实践（官方开发者文档）](https://developers.openai.com/codex/learn/best-practices)：官方写给新手的「怎么用得好」，覆盖提示、计划、验证、技能与自动化。
4. [Integrate with Codex（DeepSeek 官方文档）](https://api-docs.deepseek.com/quick_start/agent_integrations/codex/)：与你当前的 DeepSeek 链路直接相关，官方提供一键配置脚本。
5. [OpenAI Codex (AI agent)（维基百科）](https://en.wikipedia.org/wiki/OpenAI_Codex_(AI_agent))：把 2025-04 至今的发布历史、版本演进和关键事件串成一条时间线。

## 1. 官方第一手来源（30 条）

### 1.1 产品公告与官方博客

6. [Introducing upgrades to Codex｜Codex 全面升级](https://openai.com/index/introducing-upgrades-to-codex/)：官方总结 Codex 在终端、IDE、网页、手机四端的能力升级与工作方式。
7. [GPT-5.1-Codex-Max 介绍](https://openai.com/index/gpt-5-1-codex-max/)：长任务模型里程碑，可连续工作 24 小时以上。
8. [Introducing GPT-5.3-Codex](https://openai.com/index/introducing-gpt-5-3-codex/)：Codex 从「编码代理」进化为「能在电脑上完成日常工作」的智能代理。
9. [GPT-5.3-Codex 系统卡](https://openai.com/index/gpt-5-3-codex-system-card/)：官方安全评估与能力边界的权威文档。
10. [Codex for every role, tool, and workflow｜适用于各种角色、工具和工作流的 Codex](https://openai.com/index/codex-for-every-role-tool-workflow/)：官方明说「非技术团队也在用 Codex」——做内部应用、高管材料、仪表板、创意简报。
11. [Running Codex safely at OpenAI｜在 OpenAI 内部安全运行 Codex](https://openai.com/index/running-codex-safely/)：官方亲述沙箱、审批、遥测三层机制怎么配合，是理解「Codex 怎么工作」最好的官方入口。
12. [Building a secure, effective sandbox for Codex on Windows](https://openai.com/index/building-codex-windows-sandbox/)：工程团队自述 Windows 沙箱设计，理解安全边界。
13. [Harness engineering｜工程技术：在智能体优先的世界中利用 Codex](https://openai.com/index/harness-engineering/)：OpenAI 内部「3 人指挥 AI、5 个月交付百万行代码」的实验复盘，是理解「怎么用得好」的官方范本。
14. [Introducing the Codex app](https://openai.com/index/introducing-the-codex-app/)：桌面 App 版发布说明（macOS 首发）。

### 1.2 官方开发者文档（按主题）

15. [Codex 开发者文档总入口](https://developers.openai.com/codex/)：所有官方文档的根目录，含 App、Web、CLI、IDE、SDK。
16. [Codex App 文档](https://developers.openai.com/codex/app)：桌面 App 的完整使用说明（macOS/Windows）。
17. [Codex Web/Cloud 文档](https://developers.openai.com/codex/cloud)：云端并行任务、后台运行的官方说明。
18. [Cloud environments｜云端环境](https://developers.openai.com/codex/cloud/environments)：Codex 云任务如何建容器、跑仓库、控制安装。
19. [Agent internet access｜联网控制](https://developers.openai.com/codex/cloud/internet-access)：域名白名单与网络风险，理解「为什么它有时不联网」。
20. [IDE Web Tasks｜从编辑器发起云任务](https://developers.openai.com/codex/ide/web-tasks)：本地对话如何无缝升级为云端后台任务。
21. [Codex Changelog｜更新日志](https://developers.openai.com/codex/changelog)：官方产品动态，判断「过时信息」最准的标尺。
22. [Developers Changelog｜开发者更新日志](https://developers.openai.com/changelog/)：模型版本（如 GPT-5.2-Codex）官方发布记录。
23. [Codex Manual（官方手册 Markdown 版）](https://developers.openai.com/codex/codex-manual.md)：覆盖配置、技能、插件、MCP、钩子、自动化的官方总手册。
24. [Codex MCP 文档](https://developers.openai.com/codex/mcp)：Codex 如何连接外部工具与服务（理解「插头」机制）。
25. [Codex Hooks 文档](https://developers.openai.com/codex/hooks)：在智能体循环中注入自定义脚本的官方说明。
26. [Subagents 文档](https://developers.openai.com/codex/subagents)：子智能体（多代理协作）官方说明，含 Token 成本提示。
27. [Automations 文档](https://developers.openai.com/codex/app/automations)：定时任务/自动化的官方说明，适合「让 Codex 自己干活」。
28. [Best practices（已列第 3 条，此处归位）](https://developers.openai.com/codex/learn/best-practices)：官方「用好 Codex」核心习惯清单。
29. [Codex 与 Agents SDK 集成](https://developers.openai.com/codex/guides/agents-sdk)：Codex 如何被其他智能体系统调用（进阶）。
30. [PLANS.md：用计划文件解决多小时任务（官方 Cookbook）](https://developers.openai.com/cookbook/articles/codex_exec_plans)：官方示范「先计划再执行」的工作流。
31. [OpenAI 开发者视频中心](https://developers.openai.com/learn/videos)：Codex 官方演示视频。
32. [Codex 开发者说明（API 文档中的 Code 生成指南）](https://developers.openai.com/api/docs/guides/code-generation)：了解 Codex 在 API 层的定位。

### 1.3 帮助中心与学习中心

33. [ChatGPT Work 和 Codex（官方帮助中心）](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex)：厘清 Codex 与 ChatGPT 里「Work」的关系。
34. [迁移到新版 ChatGPT 桌面应用（官方帮助中心）](https://help.openai.com/en/articles/20001276-migrating-to-the-new-chatgpt-desktop-app)：ChatGPT 桌面应用与 Codex 整合后的操作说明。
35. [ChatGPT Learn：Codex Cloud 文档](https://learn.chatgpt.com/docs/cloud)：以 ChatGPT 账号视角讲的云端 Codex 上手文档。
36. [ChatGPT Learn：配置参考](https://learn.chatgpt.com/docs/config-file/config-reference)：`config.toml` 配置项检索表（进阶）。
37. [ChatGPT Learn：Skills & Plugins](https://learn.chatgpt.com/docs/skills-and-plugins)：技能与插件机制的人话版说明。
38. [ChatGPT Learn：Build skills](https://learn.chatgpt.com/docs/build-skills)：如何自己制作可复用技能。
39. [ChatGPT Learn：Record & Replay](https://learn.chatgpt.com/docs/extend/record-and-replay)：把一次操作录制成技能的官方玩法。

### 1.4 官方 GitHub 与学院

40. [openai/codex 官方仓库](https://github.com/openai/codex)：Codex CLI 开源代码、文档、版本发布都在这里。
41. [openai/codex Releases](https://github.com/openai/codex/releases/tag/rust-v0.145.0)：最新版本说明（含子智能体、记忆等功能更新）。
42. [openai/role-specific-plugins 官方仓库](https://github.com/openai/role-specific-plugins)：面向销售、数据分析、产品设计等角色的官方插件模板。
43. [OpenAI Academy：Codex for Builders](https://academy.openai.com/public/clubs/builders-etkn1/resources/codex-for-builders)：官方学习资源总览。
44. [OpenAI Academy：Codex Bootcamp](https://academy.openai.com/public/clubs/builders-etkn1/resources/codex-bootcamp-2026-07-18)：官方三期训练营（101 基础 / 201 团队 / 301 自动化）。
45. [OpenAI Academy：Codex 102 实践工作流](https://academy.openai.com/public/clubs/builders-etkn1/resources/codex-102-practical-workflows-2026-03-18)：官方实操课。
46. [OpenAI Academy：Automations](https://openai.com/academy/codex-automations/)：官方自动化专题课。
47. [OpenAI Academy：Plugins and skills](https://openai.com/academy/codex-plugins-and-skills/)：官方插件与技能专题课。

## 2. 工作原理（不钻研代码也能懂）

48. 《从 Codex 源码带你了解智能体的工作方式》（本地附件，未随本仓库发布）：Agent Loop、工具系统、六层安全机制、扩展能力。看不懂代码没关系，每章末尾的「小结」就是人话版。
49. [Codex 实践系列 Vol.01：从跑通 CLI 开始，看懂 Codex 怎么工作（阿里云开发者）](https://developer.aliyun.com/article/1740159)：用一个最小任务观察 Codex 读了什么、跑了什么、改了什么。
50. [Codex 使用最佳实践：把它当成工程队友，而不是代码生成器（腾讯云开发者）](https://cloud.tencent.com.cn/developer/article/2674885)：讲清楚「给上下文→先计划→再执行→验证→沉淀」的协作姿势。
51. [关于 Codex 和 Claude Code 的取舍（V2EX 社区讨论）](https://global.v2ex.co/t/1227231)：真实用户的优缺点清单，含成本、电脑操作、额度重置等细节。

## 3. DeepSeek 链路（你的特殊场景）

52. [Integrate with Codex｜DeepSeek 官方接入文档](https://api-docs.deepseek.com/quick_start/agent_integrations/codex/)：官方承认 Codex 为可用前端，提供一键脚本。
53. [Codex 接入 DeepSeek：安全平替 Claude Code 的零门槛方案（腾讯云开发者）](https://cloud.tencent.com.cn/developer/article/2707328)：CC-Switch + DeepSeek 的完整配置路径。
54. [Codex 接入第三方模型 DeepSeek、GLM、Kimi 教程：CC-Switch 和 Codex++ 两种方案对比（知乎）](https://zhuanlan.zhihu.com/p/2045207013248995839)：讲清「协议不完全兼容」这个坑，及两种代理方案。
55. [保姆级教程｜Codex 接入 DeepSeek V4，以及更多进阶玩法（CSDN）](https://blog.csdn.net/qimo_ai/article/details/161851381)：解释 Responses API 与 Chat Completions 协议差异，附代理方案演进。
56. [codex-deepseek-guide（GitHub）](https://github.com/zza-830/codex-deepseek-guide)：Windows 桌面版接入 DeepSeek 的完整教程仓库。
57. [codex_deepseek_proxy（GitHub）](https://github.com/Nigel211/codex_deepseek_proxy)：开源流式代理，把 Responses API 请求翻译为 DeepSeek 协议。
58. [Codex App 接入本地模型（Ollama 官方文档）](https://docs.ollama.com/integrations/codex-app)：如果你想在 Codex 里跑本地模型，这是官方集成说明。

> 注意：DeepSeek 链路下，云任务额度、记忆、插件等部分能力以 ChatGPT 账号为前提，API 键链路可能不一致；具体差异以官方文档为准，社区教程仅作配置参考。

## 4. 评测与对比（扬长避短）

59. [Codex CLI vs Claude Code：2026 对比（Tembo）](https://www.tembo.io/blog/codex-cli-vs-claude-code)：价格与 GitHub 集成 Codex 胜，配置深度 Claude Code 胜。
60. [Codex vs Claude Code vs Gemini CLI（Tembo）](https://www.tembo.io/blog/codex-vs-claude-code-vs-gemini-cli)：三工具分工：Codex 强在审查与 CI 原生。
61. [我换用 Codex 一周，权衡出乎意料（XDA）](https://www.xda-developers.com/replaced-claude-code-with-codex-for-week-trade-offs-not-what-expected/)：真实体验：委派型任务 Codex 更好，但离过程更远。
62. [Codex 撞脸 Claude Code，新功能只领先 11 天（36氪）](https://36kr.com/p/3843714346748424)：两大智能体竞品的时间线对照。
63. [深度测评 Codex：编码仅是表现形式，承接任务才是核心本质（36氪）](https://eu.36kr.com/zh/p/3889531105295106)：论证 Codex 适合「判断之后的一连串推进动作」。
64. [被骂了一年的 Codex，怎么突然爆了？（智东西）](https://zhidx.com/p/567244.html)：从存在感不足到 500 万周活的转折复盘。
65. [Claude Code 和 Codex 怎么选？我的分项推荐（腾讯云开发者）](https://cloud.tencent.com.cn/developer/article/2682615)：Claude Code 像「陪我一起干」，Codex 像「派任务后台干」。
66. [Codex 与 Cursor：哪款更契合你的工作流（DataCamp·中文）](https://www.datacamp.com/zh/blog/codex-vs-cursor)：Codex 假设你想委派，Cursor 假设你想协作。
67. [Codex vs. Cursor（Zapier）](https://zapier.com/blog/codex-vs-cursor/)：并行任务、安全默认值、代码库索引方式的差异。
68. [Claude Code vs Codex：实测后不再迷信基准（Bito）](https://bito.ai/ai-tools/claude-code-vs-codex/)：基准分数与真实体验的差距。
69. [When to use Codex vs Claude Code（Unstoppable Domains）](https://unstoppabledomains.com/blog/categories/education/article/codex-vs-claude-when-to-use-both)：含 2026 年 6 月 SWE-bench 实测数据对比。

## 5. 新闻与产品时间线

70. [ChatGPT 的 Codex 大升级（ZDNET）](https://www.zdnet.com/article/chatgpts-codex-just-got-a-huge-upgrade-that-makes-it-more-powerful-than-ever-whats-new/)：2025-10 GA 发布解读。
71. [DevDay 2025 最容易被忽略的重磅消息（VentureBeat）](https://venturebeat.com/ai/the-most-important-openai-announcement-you-probably-missed-at-devday-2025)：Codex GA 与企业化信号。
72. [OpenAI 公布 Harness Engineering（InfoQ）](https://www.infoq.com/news/2026/02/openai-harness-engineering-codex/)：英文权威解读官方实验。
73. [OpenAI 如何为 Codex 构建 Windows 沙箱（InfoQ）](https://www.infoq.com/news/2026/06/codex-windows-sandbox-design/)：安全架构的非官方权威解读。
74. [Codex 扩展为企业工作平台（The Next Web）](https://thenextweb.com/news/openai-codex-enterprise-plugins-sites-non-developers)：Sites、插件、非开发者用户的里程碑。
75. [程序员不许写代码！OpenAI 硬核实验（澎湃新闻）](https://www.thepaper.cn/newsdetail_forward_32618365)：中文媒体对 Harness Engineering 的通俗报道。
76. [OpenAI 发布 GPT-5.1-Codex-Max（量子位）](https://www.qbitai.com/2025/11/354582.html)：中文权威科技媒体报道。
77. [Codex 进入 ChatGPT 手机 App（新智元/网易）](https://m.163.com/dy/article/KT24948D0511ABV6.html)：400 万周活 + 移动端发布。
78. [OpenAI 将 Codex 引入 ChatGPT 移动端（至顶网）](https://ai.zhiding.cn/2026/0528/3188631.shtml)：含远程 SSH、程序化访问令牌、HIPAA 合规等企业功能。
79. [OpenAI announces Codex for mobile devices（SDTimes）](https://sdtimes.com/ai/openai-announces-codex-for-mobile-devices/)：英文权威报道移动端发布。

## 6. 课程与教程（按难度递进）

80. [freeCodeCamp：Codex 主题文章合集](https://www.freecodecamp.org/news/tag/codex/)：含《The Codex Handbook》和官方课程解读，免费。
81. [Introduction to OpenAI Codex（Pluralsight）](https://www.pluralsight.com/courses/introduction-openai-codex)：把 Codex 当「代理编排工具」而不是代码助手来学。
82. [Codex 零基础实战教程：速通 15 种玩法（腾讯云开发者）](https://cloud.tencent.com.cn/developer/article/2687337)：10 多个实战案例，覆盖编程、办公提效与创作。
83. [Codex 保姆级项目实战（腾讯云开发者）](https://cloud.tencent.com.cn/developer/article/2687305)：从 GitHub 仓库到分析报告的完整演示。
84. [Codex CLI 速查表（阿里云开发者）](https://developer.aliyun.com/article/1714675)：安装、配置、沙箱、AGENTS.md、快捷键、避坑。
85. [Codex 新手入门（阿里云开发者）](https://developer.aliyun.com/article/1740183)：Rust 实现、速度与成本的通俗介绍。
86. [CodexGuide（GitHub 中文教程站）](https://github.com/freestylefly/CodexGuide)：社区维护的中文完整教程（快速上手 + 进阶 + 实战）。
87. [Codex 橙皮书（GitHub）](https://github.com/bozhouDev/codex-orange-book)：从安装到实战案例的全链路开源指南，含 PDF。
88. [AI-Coding-Guide-Zh（GitHub）](https://github.com/KimYx0207/AI-Coding-Guide-Zh)：按 2026-06 官方文档修订的中文安装与认证指南。
89. [Codex 自动化与 CI/CD：让 Codex 在你不在的时候自己干活（w3cschool）](https://www.w3cschool.cn/aicodingguide/codex-automation.html)：GitHub Actions + 桌面 App 定时任务两条路。
90. [我为什么把 Codex 接到第三方 API（腾讯云开发者）](https://cloud.tencent.com.cn/developer/article/2668348)：第三方模型与 Codex 的组合玩法。

## 7. 视频与播客

91. [吴恩达发布的 Codex 教程（B站视频）](https://www.bilibili.com/video/BV1FrLs6jE2Q/)：从安装到功能模块详解，中文圈口碑最好的入门视频之一。
92. [Codex 零基础入门（B站视频）](https://www.bilibili.com/video/BV1YBVw6wEY5/)：国内环境安装到项目实战的保姆级教程。
93. [Lenny 播客访谈 Codex 产品与工程负责人（智东西报道）](https://m.zhidx.com/p/571648.html)：做 AI 产品「最后拼的是品味」。
94. [Codex 技术总监访谈：AI 已能写 80% 代码，但 Agent 也有致命短板（InfoQ 中文）](https://www.infoq.cn/article/bycqtv38Ng71KoUjC0bH)：能力边界与使用姿势的第一手观点。
95. [Dev Interrupted 播客：OpenAI Codex 团队谈自主性](https://linearb.io/dev-interrupted/podcast/openai-codex-thibault-sottiaux-agentic-autonomy)：为什么「脚手架是应付而非扩展」。
96. [我用了 Codex 350 小时，它现在替我运营业务（播客）](https://share.transistor.fm/s/feac1c60)：非程序员视角的完整工作流演示。
97. [跨国串门儿计划 #364：Codex 负责人揭秘 18 天打造榜首 App](https://podscan.fm/podcasts/kua-guo-chuan-men-er-ji-hua/episodes/364-jie-mi-openai-gao-xiao-yin-qing18tian-da-zao-bang-shou-appcodex-fu-ze-ren-jie-mi-ai-dui-you-de-jin-hua-zhi-lu)：中文播客深度访谈。

## 8. 书籍（可选进阶）

98. [Vibecoding with Codex: 101 Things to Know（Amazon Kindle）](https://www.amazon.ca/gp/aw/d/B0GQ38PNK9)：101 个短章节覆盖 2026 年 4 月版的云端、CLI、桌面 App 与 IDE 扩展。
99. [The Codex Automation Handbook（Bookshop）](https://bookshop.org/p/books/the-codex-automation-handbook-hand-off-repetitive-work-to-an-ai-coding-agent-and-reclaim-your-time-lucas-d-reiner/59c9fadb80d1f5c2)：教你从「干活的人」变成「把任务定义清楚的人」。

## 9. 社区、基准与安全

100. [Codex CLI 网络访问问答（Stack Overflow）](https://stackoverflow.com/questions/79970154/how-to-allow-codex-cli-to-execute-shell-commands-with-internet-access-from-withi/79970156)：沙箱默认断网、白名单机制的实测问答。
101. [Hacker News 讨论区](https://news.ycombinator.com/)：搜「Codex」可看开发者真实吐槽与赞美（含 2026-06 日志写入 Bug 等争议）。
102. [Gemini CLI vs Codex（MorphLLM）](https://www.morphllm.com/comparisons/gemini-cli-vs-codex)：2026 年 6 月公开基准（SWE-bench 88.7%、Terminal-Bench 82.7%）。
103. [7 个 CLI 编程代理排名（Security Boulevard）](https://securityboulevard.com/2026/06/7-cli-coding-agents-ranked-by-real-terminal-bench-scores/)：以 Terminal-Bench 2.0 实测数据排名。
104. [OpenAI 称 Codex Security 一个月发现 11000 个高危漏洞（CSO Online）](https://www.csoonline.com/article/4142354/openai-says-codex-security-found-11000-high-impact-bugs-in-a-month.html)：安全代理方向的权威报道。
105. [OpenAI 发布 Codex Security 研究预览（Bloomberg）](https://www.bloomberg.com/news/articles/2026-03-06/openai-releases-ai-agent-security-tool-for-research-preview)：财经媒体视角。
106. [Codex for non-coders（牛津大学 OERC）](https://oerc.ox.ac.uk/ai-centre/ai-centre-news/codex-for-non-coders-and-for-those-who-can)：高校面向非技术人员的实操活动记录。

## 10. 建议的学习顺序（针对你的两套环境）

第一步（今天）：读第 0 节 5 条 + 官方帮助中心文章，回答「Codex 是什么、我订阅里有什么」。
第二步（本周）：看第 2 节工作原理（先读你手头源码文章的每章小结，再看官方安全文章），建立「LLM 决策→工具执行→结果反馈→继续」的心智模型。
第三步（本两周）：按第 6 节挑一套课程（推荐 OpenAI Academy Bootcamp 或 CodexGuide），在你的 DeepSeek 链路上做一次真实小任务，同时对比 ChatGPT 原生链路的体验差异。
第四步（长期）：用第 1.2 节官方文档当字典按需查；用第 4 节评测指导「什么任务交给 Codex、什么任务自己盯」；用第 3 节维护好 DeepSeek 链路。

> 一句话结论：Codex 不是「更聪明的 ChatGPT」，而是「会动手干活的智能体」；官方文档 + 官方博客是唯一不会过时的权威源，其余来源用于补体验和避坑。
