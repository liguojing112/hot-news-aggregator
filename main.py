import schedule
import time
import json
import os
import requests
from datetime import datetime

from crawlers.weibo import get_weibo_hot
from crawlers.baidu import get_baidu_hot
from utils.cleaner import merge_hot_news, check_keywords
from config import KEYWORDS, ENTERPRISE_WECHAT_WEBHOOK  # 这里统一导入


def generate_markdown(df, alerts, date_str):
    md = f"""# 🛡️ JARVIS 热搜雷达 - {date_str}

**Tony Stark 模式已激活** | 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**数据来源**：微博 + 百度（已智能去重合并）

## 🚨 你的关注雷达（Musk / RDJ / 钢铁侠 / 马斯克 / 特斯拉）
"""
    if alerts:
        md += f"**🔥 Jarvis 警报！今日捕获 {len(alerts)} 条高能信号！**\n\n"
        md += "| 排名 | 标题 | 平台 | 热度 | 链接 |\n|------|------|------|------|------|\n"
        for a in alerts:
            md += f"| {a['rank']} | {a['title']} | {a['platforms']} | {a['heat']} | [直达]({a['link']}) |\n"
    else:
        md += "**今天雷达暂无 Musk/RDJ/马斯克/特斯拉 信号，继续保持扫描状态！** 🛠️\n"

    md += f"""
---

## 🔥 全网Top 15 热搜

| 排名 | 热点标题 | 平台 | 热度 | 链接 |
|------|----------|------|------|------|
"""
    for _, row in df.head(15).iterrows():
        md += f"| {row['rank']} | {row['display_title']} | {row['platforms']} | {row['heat']} | [查看]({row['link']}) |\n"

    md += f"""
---
**统计**：共 {len(df)} 条热点 · Jarvis 已为你过滤重复  
**明天同一时间见**，Stark Industries 出品！  

*by 你的钢铁侠个人雷达 | v1.0*
"""
    return md


def save_to_json(df, date_str):
    os.makedirs("data", exist_ok=True)
    json_path = f"data/hot_{date_str}.json"
    df.to_json(json_path, orient="records", force_ascii=False, indent=2)
    print(f"💾 已保存 JSON 数据 → {json_path} ({len(df)} 条)")


def send_enterprise_wechat_push(title, content):
    if not ENTERPRISE_WECHAT_WEBHOOK:
        print("⚠️ 未配置企业微信 Webhook，跳过推送")
        return
    
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": f"**{title}**\n\n{content}\n\n> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        }
    }
    
    try:
        resp = requests.post(ENTERPRISE_WECHAT_WEBHOOK, json=payload, timeout=10)
        if resp.status_code == 200 and resp.json().get("errcode") == 0:
            print("✅ 企业微信推送成功！")
        else:
            print(f"推送失败：{resp.json()}")
    except Exception as e:
        print(f"推送异常：{e}")


def job():
    print(f"\n=== JARVIS 扫描启动 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
    
    weibo = get_weibo_hot()
    baidu = get_baidu_hot()
    
    merged_df = merge_hot_news(weibo, baidu)
    alerts = check_keywords(merged_df, KEYWORDS)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    save_to_json(merged_df, date_str)
    
    md_content = generate_markdown(merged_df, alerts, date_str)
    md_path = f"output/{date_str}_ironman_daily.md"
    os.makedirs("output", exist_ok=True)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"🎉 日报生成完成 → {md_path}")
    print(f"📊 今日热点总数：{len(merged_df)} 条")
    
    # 企业微信推送
    alerts_summary = f"今日捕获 **{len(alerts)}** 条高能信号！" if alerts else "今天暂无高能信号，继续保持扫描状态。"
    push_title = f"JARVIS 热搜雷达 - {date_str}"
    push_content = f"{alerts_summary}\n\n日报路径：{md_path}\n\n命中详情：\n" + "\n".join([f"- {a['title']} ({a['platforms']})" for a in alerts]) if alerts else "无关键词命中"
    
    send_enterprise_wechat_push(push_title, push_content)


# ================== 定时设置 ==================
# 正式
# schedule.every().day.at("08:00").do(job)

# 测试：每2分钟跑一次
schedule.every(2).minutes.do(job)


print("🛡️ JARVIS 定时系统已启动，每天 08:00 自动扫描...")
print("按 Ctrl+C 退出程序")

while True:
    schedule.run_pending()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if schedule.jobs:
        next_time = schedule.jobs[0].next_run.strftime("%H:%M:%S")
        print(f"[{now}] 等待中... 下次扫描：{next_time}", end="\r")
    time.sleep(30)

    # ================== 自动清理旧文件（保留最近7天） ==================
def clean_old_files(days=7):
    now = datetime.now()
    for folder in ["data", "output"]:
        if os.path.exists(folder):
            for f in os.listdir(folder):
                file_path = os.path.join(folder, f)
                if os.path.isfile(file_path):
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if (now - file_time).days > days:
                        os.remove(file_path)
                        print(f"🗑️ 已清理旧文件: {f}")

clean_old_files(days=7)   # 保留最近7天，改成30也可以