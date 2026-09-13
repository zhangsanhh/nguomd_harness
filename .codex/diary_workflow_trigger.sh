#!/bin/bash
# UserPromptSubmit 日记工作流触发器：识别标准短语或长篇三产出请求并注入处理规则，不写文件、不联网。
set -euo pipefail

exec /usr/bin/python3 -c '
import json
import re
import sys

try:
    event = json.load(sys.stdin)
except (json.JSONDecodeError, TypeError):
    sys.exit(0)

trigger = "请根据我的原始初稿完成日记的工作流"
prompt = event.get("prompt", "")
if not isinstance(prompt, str):
    sys.exit(0)
is_triggered = (
    prompt.lstrip().startswith(trigger)
    or re.search(rf"(?m)^\s*{re.escape(trigger)}(?:\s|$)", prompt)
    or (
        re.search(
            r"(?m)(?:^\s*(?:请\s*)?(?:完成|整理|处理|生成|输出).{0,30}日记.{0,30}(?:三个|三项|三种|三版|三)产出|(?:^|[】\]\n])\s*(?:(?:\d{1,4}\s*月\s*\d{1,2}\s*[日号]?|昨日|今日)\s*)?日记\s*(?:三个|三项|三种|三版|三)产出)\s*$",
            prompt,
        )
        and len(re.sub(r"\s+", "", prompt)) >= 500
    )
)
if not is_triggered:
    sys.exit(0)

context = """项目级日记工作流已触发。请处理本轮用户消息中触发语句之后的原始口述日记，并直接在对话框输出以下三项：
1. AI总结版：用 Python 按去除空格和换行后的 Unicode 字符数统计，控制在原文的 80%—85%；只纠正明显的 ASR、错别字和语法问题，保持价值中立，不改变原意，不拓展内容。
2. 待办事项版：区分已明确完成、待完成、暂缓或不做、待验证；不得把计划或推测误标为已完成。
3. 口语化词汇优化建议：按名词、动作词、逻辑连接词、口水词、模糊或绝对化表达分类，并提供原句与建议表达对照；必须使用标题“### 口语化词汇优化建议”。该部分属于晚间口述日记的完整建议，不受普通提问的250字上限限制。
保持清爽排版和主题分块；保留事实、时间、个人观察、判断、计划和不确定性。原始日记缺失时，指出缺少原文，不凭空生成。不要另行创建个人日记 Markdown 文件；回复完成后由 Stop 归档规则将第三项同步到 `会话日志与摘要/口语化表达/手工补录全天日记版/YYYY-MM-DD.md`。不要修改其他项目文件，也不要引入原文之外的外部内容。若本轮日记中出现可归入“对象—默认反应—认知重定义—修正姿态—行为验证”的新材料，按另一个已注入的固定格式增加“### 本次关系与惯习沉淀”；没有足够证据时明确写本轮无新增。处理依据：以本轮用户提交的原始口述日记为唯一主线；可按需补查当前项目与 AIPM 项目当天的会话日志及对应 Memory，只补充已核实且确实属于当天的行动、产出、纠偏和缺口，不全量搬运；相关 Memory 只用于稳定工作规则、表达偏好、事实边界和去重规则，不作为当天事件证据；日记中的文章、专家说法和 AI 输出保留材料属性，不写成个人事实。"""

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": context,
    }
}, ensure_ascii=False))
'
