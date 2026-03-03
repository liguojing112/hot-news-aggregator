import pandas as pd
from difflib import SequenceMatcher
import re

def normalize_title(title):
    """清理标题用于相似度判断"""
    return re.sub(r'[\W\s]+', '', title.lower().strip())

def title_similarity(t1, t2):
    """计算两个标题相似度"""
    return SequenceMatcher(None, normalize_title(t1), normalize_title(t2)).ratio()

def merge_hot_news(weibo_list, baidu_list, similarity_threshold=0.65):
    """合并 微博 + 百度，去重，保留最高热度"""
    all_data = weibo_list + baidu_list
    if not all_data:
        return pd.DataFrame()
    
    df = pd.DataFrame(all_data)
    df['heat'] = pd.to_numeric(df['heat'], errors='coerce').fillna(0)
    
    df['norm'] = df['title'].apply(normalize_title)
    df['cluster'] = -1
    cluster_id = 0
    clusters = {}
    
    for idx in range(len(df)):
        if df.loc[idx, 'cluster'] != -1:
            continue
        current_title = df.loc[idx, 'title']
        df.loc[idx, 'cluster'] = cluster_id
        clusters[cluster_id] = [idx]
        
        for jdx in range(idx + 1, len(df)):
            if df.loc[jdx, 'cluster'] == -1:
                sim = title_similarity(current_title, df.loc[jdx, 'title'])
                if sim > similarity_threshold:
                    df.loc[jdx, 'cluster'] = cluster_id
                    clusters[cluster_id].append(jdx)
        cluster_id += 1
    
    result_rows = []
    for cid, indices in clusters.items():
        group = df.iloc[indices]
        max_idx = group['heat'].idxmax()
        rep = group.loc[max_idx].copy()
        rep['display_title'] = max(group['title'], key=len)
        rep['platforms'] = ' + '.join(sorted(group['platform'].unique()))
        
        for plat in ['X', '百度', '微博']:
            links = group.loc[group['platform'] == plat, 'link']
            if len(links) > 0:
                rep['link'] = links.iloc[0]
                break
        result_rows.append(rep)
    
    result_df = pd.DataFrame(result_rows)
    result_df = result_df.sort_values('heat', ascending=False).reset_index(drop=True)
    result_df['rank'] = range(1, len(result_df) + 1)
    
    print(f"✅ 合并完成！原始 {len(all_data)} 条 → 去重后 {len(result_df)} 条（钢铁侠雷达已扫描）")
    return result_df[['rank', 'display_title', 'platforms', 'heat', 'link', 'timestamp']]

def check_keywords(df, keywords):
    """检查 Musk / RDJ / 钢铁侠 关键词"""
    alerts = []
    kw_lower = [k.lower() for k in keywords]
    for _, row in df.iterrows():
        title_lower = row['display_title'].lower()
        for k in kw_lower:
            if k in title_lower:
                alerts.append({
                    "rank": row['rank'],
                    "title": row['display_title'],
                    "platforms": row['platforms'],
                    "heat": row['heat'],
                    "link": row['link']
                })
                break
    return alerts