#!/bin/bash
# 时间注入脚本（UserPromptSubmit 每轮触发）：只输出动态信息，无副作用（不写文件、不联网）
echo "会话注入："
echo "- 当前时间：$(TZ='Asia/Shanghai' date '+%Y-%m-%d %H:%M')（北京时间）"
echo "- 时间规则：以当前时间为基准，不沿用/引用训练截止日期作为默认值。"
