import requests
import pandas as pd
import os
from datetime import datetime

def get_baidu_hot():
    """抓取百度实时热搜 - 官方API"""
    url = "https://top.baidu.com/api/board?tab=realtime"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # 官方结构：data.cards[0].content 是热搜列表
        hot_list = []
        for card in data.get("data", {}).get("cards", []):
            if card.get("component") == "hotList":
                items = card.get("content", [])
                for item in items[:50]:
                    hot_list.append({
                        "platform": "百度",
                        "rank": item.get("index", 0) + 1,
                        "title": item.get("word", ""),
                        "heat": item.get("hotScore", "N/A"),
                        "tag": item.get("hotTag", ""),
                        "link": item.get("url", ""),
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                break
        
        print(f"✅ 成功抓取 {len(hot_list)} 条百度热搜！")
        return hot_list
        
    except Exception as e:
        print(f"❌ 百度抓取失败: {e}")
        return []

# 测试
if __name__ == "__main__":
    hot_data = get_baidu_hot()
    print("\n=== 前10条百度热搜 ===")
    for item in hot_data[:10]:
        print(f"{item['rank']:2d}. {item['title']}  ({item['heat']})")
    
    os.makedirs("output", exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    df = pd.DataFrame(hot_data)
    csv_path = f"output/baidu_{date_str}.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"\n📁 保存到: {csv_path}")