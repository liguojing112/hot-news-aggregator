import requests
import pandas as pd
import os
from datetime import datetime

def get_weibo_hot():
    """抓取微博热搜榜 - 修复优化版"""
    url = "https://weibo.com/ajax/side/hotSearch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Referer": "https://weibo.com/",
        "Accept": "application/json, text/plain, */*"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        realtime = data.get("data", {}).get("realtime", [])
        hot_list = []
        
        for i, item in enumerate(realtime, 1):   # 强制排名1-50
            word = item.get("word", "").strip()
            if not word:
                continue
            # 智能提取热度（兼容新老字段）
            heat = item.get("num") or item.get("raw_hot") or item.get("hot") or "N/A"
            label = item.get("label", "") or ""
            link = item.get("scheme") or f"https://s.weibo.com/weibo?q={requests.utils.quote(word)}"
            
            hot_list.append({
                "platform": "微博",
                "rank": i,
                "title": word,
                "heat": str(heat),
                "tag": label,
                "link": link,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        print(f"✅ 成功抓取 {len(hot_list)} 条微博热搜！")
        return hot_list[:50]
        
    except Exception as e:
        print(f"❌ 抓取失败: {e}")
        return []

# 测试运行
if __name__ == "__main__":
    hot_data = get_weibo_hot()
    
    print("\n=== 前10条热搜（修复后） ===")
    for item in hot_data[:10]:
        print(f"{item['rank']:2d}. {item['title']}  ({item['heat']}) {item['tag']}")
    
    os.makedirs("output", exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    df = pd.DataFrame(hot_data)
    csv_path = f"output/weibo_{date_str}.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"\n📁 已保存到: {csv_path}")