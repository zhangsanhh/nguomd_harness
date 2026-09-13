#!/usr/bin/env python3
"""从当前项目日期摘要生成逐条审计线索台账。

这是派生审计文件生成器，不修改会话摘要、BadCase、Pitfall 或状态。
关键词只做机械定位；“去向”是现有资产的候选入口，不是自动语义判定。
"""

from __future__ import annotations

import argparse
import csv
import re
from datetime import date, timedelta
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_ROOT = PROJECT_ROOT / "会话日志与摘要"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "候选线索逐条台账-2026-09-09.tsv"
AUDIT_CUTOFF = "2026-09-09 15:02"
ROW_PATTERN = re.compile(r"^\|\s*(\d{4}-\d\d-\d\d\s+[^|]+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$")
KEYWORDS = (
    "用户指出", "用户纠正", "返工", "失败", "未完成", "未能", "未读", "未覆盖",
    "无法", "不通过", "阻断", "超时", "误判", "漏", "偏题", "报错", "待验证",
    "待确认", "待审核", "待跑", "问题", "异常", "失效", "拒绝", "不可用", "缺口", "错误",
)
BATCHES = (
    ("B1", date(2026, 8, 3), date(2026, 8, 9)),
    ("B2", date(2026, 8, 10), date(2026, 8, 16)),
    ("B3", date(2026, 8, 17), date(2026, 8, 23)),
    ("B4", date(2026, 8, 24), date(2026, 8, 30)),
    ("B5", date(2026, 8, 31), date(2026, 9, 6)),
    ("B6", date(2026, 9, 7), date(2026, 9, 9)),
)

DEEP_REVIEW = {
    ("2026-08-03", "12:31", "BadCase库完善"): "B1-01",
    ("2026-08-03", "19:22", "漏答纠正"): "B1-02",
    ("2026-08-03", "20:00", "技能评估"): "B1-03",
    ("2026-08-03", "22:30", "Typeless授权"): "B1-04",
    ("2026-08-03", "23:20", "词典清理"): "B1-05",
    ("2026-08-10", "10:56", "FlClash深度排查"): "B2-01",
    ("2026-08-10", "17:59", "影评流程归因排查"): "B2-02",
    ("2026-08-10", "21:38", "楚门专题影评（梅莉尔与生育）"): "B2-03",
    ("2026-08-10", "21:44", "子智能体层级规范"): "B2-04",
    ("2026-08-15", "17:58", "Codex 配置体检收尾与修复"): "B2-05",
    ("2026-08-17", "22:03", "代理网络候选实测排序"): "B3-01",
    ("2026-08-17", "22:52", "三份机场配置测试与自动降级配置"): "B3-02",
    ("2026-08-18", "22:37", "子代理模型与移动硬盘状态"): "B3-03",
    ("2026-08-18", "22:23", "《帕特森》影评重构与硬盘素材融合"): "B3-04",
    ("2026-08-23", "20:34", "《极速车王》影评修订"): "B3-05",
    ("2026-08-24", "18:41", "B站整理目录纠正"): "B4-01",
    ("2026-08-25", "22:20", "去魅视频方向纠偏"): "B4-02",
    ("2026-08-29", "08:08", "摄像头复盘阶段整理"): "B4-03",
    ("2026-08-30", "23:08", "电脑采集器桌面权限重复请求"): "B4-04",
    ("2026-08-30", "07:15", "电脑行为日志 LaunchAgent迭代"): "B4-05",
    ("2026-08-31", "21:36", "萤石复盘资源占用与任务暂停"): "B5-01",
    ("2026-08-31", "21:14", "日记库范围核对"): "B5-02",
    ("2026-09-01", "10:16", "日记三产出归档纠正"): "B5-03",
    ("2026-09-02", "22:05", "子代理超时回收协议修复"): "B5-04",
    ("2026-09-06", "20:50", "电影推荐主题纠偏"): "B5-05",
    ("2026-09-07", "23:06", "9月7日日记跨项目融合"): "B6-01",
    ("2026-09-07", "20:37", "本机网络基线诊断"): "B6-02",
    ("2026-09-08", "23:16", "日记工作流补查规则落地"): "B6-03",
    ("2026-09-08", "11:25", "路线B阈值与触发失败"): "B6-04",
    ("2026-09-09", "09:11", "DSH Web 启动修复"): "B6-05",
}


def batch_for(value: date) -> str:
    for name, start, end in BATCHES:
        if start <= value <= end:
            return name
    raise ValueError(value)


def route_for(text: str) -> str:
    if "BadCase" in text or "沉淀" in text or "确认行" in text:
        return "BC_流程_002；R-005；G-008/G-009"
    if "日记" in text or "补录" in text or "三产出" in text:
        return "D-RW-08/D-RW-12；BC_流程_002；R-044/R-046/R-048"
    if "电影" in text or "去魅" in text or "性" in text:
        return "BC_输入_004；D-RW-04/D-RW-11；R-049"
    if "压缩" in text or "writer" in text:
        return "Pitfall-095—097；R-052/R-053"
    if "子代理" in text or "子智能体" in text:
        return "Pitfall-020/049/050；R-041"
    if "FlClash" in text or "网络" in text or "节点" in text:
        return "Pitfall-089/092/093/094；R-043/R-050/R-051"
    if "DSH" in text:
        return "Pitfall-100/101；当前项目路径问题另见 Pitfall-104"
    if "摄像头" in text or "萤石" in text or "录像" in text:
        return "BC_流程_009；Pitfall-105；R-039"
    if "会话" in text or "日志" in text or "Hook" in text or "钩子" in text:
        return "BC_日志_001；R-001/R-020"
    if "影评" in text or "素材" in text or "增量" in text:
        return "BC_内容_007/008；R-040/R-042"
    return "无直接现有映射；仅保留原摘要"


def parse_rows() -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    used_reviews: set[str] = set()
    seen_rows: dict[tuple[str, str, str], int] = {}
    for name, start, end in BATCHES:
        current = start
        while current <= end:
            day = current.isoformat()
            path = LOG_ROOT / day / "会话摘要.md"
            if path.exists():
                for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
                    match = ROW_PATTERN.match(line)
                    if not match:
                        continue
                    stamp, summary, topic = match.groups()
                    if stamp.strip() > AUDIT_CUTOFF:
                        continue
                    text = f"{summary} {topic}"
                    hits = [keyword for keyword in KEYWORDS if keyword in text]
                    # 同一北京时间、主题出现两行时，按重复摘要候选处理；保留两行原始证据，避免重复计数。
                    row_key = (stamp.strip(), topic.strip())
                    duplicate_of = seen_rows.get(row_key)
                    seen_rows[row_key] = len(records) + 2
                    hour_minute = stamp[11:16]
                    review = ""
                    for (review_day, review_time, review_topic), label in DEEP_REVIEW.items():
                        if day == review_day and (not review_time or hour_minute == review_time) and (review_topic in topic or topic in review_topic):
                            if label not in used_reviews:
                                review = label
                                used_reviews.add(label)
                            break
                    records.append({
                        "批次": name,
                        "来源日期": day,
                        "来源时间": stamp,
                        "主题": topic,
                        "摘要": re.sub(r"\s+", " ", summary).strip(),
                        "机械线索": "；".join(hits) if hits else "无",
                        "重复摘要": f"是（第 {duplicate_of} 行）" if duplicate_of else "否",
                        "深审编号": review or "未选入本批五条深审样本",
                        "候选去向": route_for(text) if hits else "非候选线索，保留原摘要",
                        "处理结论": "重复摘要，保留原始行，不重复入库" if duplicate_of else ("已进入深审台账" if review else ("机械线索，不直接入库" if hits else "保留原摘要，不计失败")),
                        "证据边界": "见闭环审计与补录台账；关键词不等于失败" if hits else "未触发机械候选词",
                    })
            current += timedelta(days=1)
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    if output.exists() and not args.force:
        raise SystemExit(f"目标已存在，若要重建请显式使用 --force：{output}")
    records = parse_rows()
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(records)
    hit_count = sum(1 for record in records if record["机械线索"] != "无")
    review_count = sum(1 for record in records if record["深审编号"].startswith("B"))
    print(f"写入：{output}")
    print(f"日期摘要行：{len(records)}；机械线索：{hit_count}；深审样本：{review_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
