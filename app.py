import streamlit as st
import pandas as pd
import os
import base64
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 页面配置
st.set_page_config(page_title="JARVIS 热搜雷达", page_icon="🛡️", layout="wide")

# ================== 语言字典（完整版）==================
LANG = {
    "zh": {
        "title": "🛡️ JARVIS 热搜雷达",
        "caption": "Tony Stark 专属全网热点扫描仪 | 微博 + 百度",
        "control_panel": "⚙️ 控制面板",
        "select_date": "📅 选择日期",
        "platform_filter": "📡 平台过滤",
        "search_placeholder": "🔍 关键词（空格分隔）",
        "search_help": "输入关键词，空格分隔多个",
        "total_hot": "总热点",
        "current_match": "当前匹配",
        "match_result": "匹配结果",
        "no_match": "暂无匹配结果",
        "no_data": "当前日期无数据",
        "export": "📤 导出当前结果",
        "export_md": "导出为 Markdown",
        "download_md": "下载 Markdown",
        "export_csv": "导出为 Excel",
        "download_csv": "下载 Excel",
        "alert_radar": "🚨 关注雷达",
        "today_signals": "🔥 今日高能信号！总计命中",
        "no_signals": "今天暂无关注关键词命中",
        "trend": "📈 关键词历史趋势",
        "select_kw": "选择关键词查看趋势",
        "voice": "🔊 JARVIS 语音播报",
        "voice_btn": "🎙️ 让 JARVIS 读出今日情报",
        "voice_success": "JARVIS 正在播报...",
        "voice_no_data": "暂无数据",
        "refresh": "🔄 手动刷新",
        "language": "🌐 语言",
        "chinese": "中文",
        "english": "English",
        # 以下为新增的键
        "view": "查看",
        "hit_count": "命中 {count} 条",
        "times": "次",
        "occurrences": "上榜次数",
        "total_heat": "总热度",
        "7day_trend": "近7天趋势",
        "jarvis_online": "JARVIS 已上线。",
        "total_scanned": "今日扫描",
        "hotspots": "条热点",
        "high_energy": "其中高能信号",
        "items": "条",
    },
    "en": {
        "title": "🛡️ JARVIS Hot Radar",
        "caption": "Tony Stark's Exclusive Hotspot Scanner | Weibo + Baidu",
        "control_panel": "⚙️ Control Panel",
        "select_date": "📅 Select Date",
        "platform_filter": "📡 Platform Filter",
        "search_placeholder": "🔍 Keywords (space separated)",
        "search_help": "Enter keywords, space separated",
        "total_hot": "Total Hotspots",
        "current_match": "Current Match",
        "match_result": "Matched Results",
        "no_match": "No matching results",
        "no_data": "No data for this date",
        "export": "📤 Export Current Results",
        "export_md": "Export as Markdown",
        "download_md": "Download Markdown",
        "export_csv": "Export as Excel",
        "download_csv": "Download Excel",
        "alert_radar": "🚨 Alert Radar",
        "today_signals": "🔥 Today's High-Energy Signals! Total hits",
        "no_signals": "No keywords hit today",
        "trend": "📈 Keyword Trend History",
        "select_kw": "Select keyword to view trend",
        "voice": "🔊 JARVIS Voice Broadcast",
        "voice_btn": "🎙️ Let JARVIS read today's intel",
        "voice_success": "JARVIS is broadcasting...",
        "voice_no_data": "No data available",
        "refresh": "🔄 Manual Refresh",
        "language": "🌐 Language",
        "chinese": "Chinese",
        "english": "English",
        # 以下为新增的键
        "view": "View",
        "hit_count": "hit {count} times",
        "times": "times",
        "occurrences": "Occurrences",
        "total_heat": "Total Heat",
        "7day_trend": "7-Day Trend",
        "jarvis_online": "JARVIS online.",
        "total_scanned": "Total scanned",
        "hotspots": "hotspots",
        "high_energy": "High-energy signals",
        "items": "items",
    }
}

# ================== 初始化语言 ==================
if "lang" not in st.session_state:
    st.session_state.lang = "zh"  # 默认中文

def t(key, **kwargs):
    """翻译函数，支持格式化参数"""
    text = LANG[st.session_state.lang].get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text

# ================== 钢铁侠 HUD 样式 ==================

# ================== 尝试加载本地图片，否则用内置SVG ==================
def get_ironman_background():
    # 尝试读取本地图片（支持 png, jpg, jpeg, webp）
    img_paths = [
        "assets/ironman.png",
        "assets/ironman.jpg", 
        "assets/ironman.jpeg",
        "static/ironman.png",
        "ironman.png"  # 根目录
    ]
    
    for path in img_paths:
        if os.path.exists(path):
            with open(path, "rb") as f:
                img_base64 = base64.b64encode(f.read()).decode()
            # 根据扩展名判断类型
            ext = path.split('.')[-1].lower()
            mime = "jpeg" if ext in ["jpg", "jpeg"] else "png" if ext == "png" else "webp"
            return f"data:image/{mime};base64,{img_base64}"
    
    # 如果找不到文件，使用内置的SVG钢铁侠标志（红色发光头盔轮廓）
    # 这个SVG内嵌base64，不需要外部文件
    svg_ironman = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 240">
        <defs>
            <linearGradient id="gold" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#FFD700;stop-opacity:1" />
                <stop offset="50%" style="stop-color:#FF6B00;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#FF0000;stop-opacity:1" />
            </linearGradient>
            <filter id="glow">
                <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
        </defs>
        <!-- 头盔轮廓 -->
        <path d="M100 20 L160 60 L160 140 Q160 200 100 220 Q40 200 40 140 L40 60 Z" fill="url(#gold)" stroke="#FF0000" stroke-width="2" filter="url(#glow)"/>
        <!-- 面罩 -->
        <path d="M60 100 Q80 80 100 90 Q120 80 140 100 L130 150 Q100 170 70 150 Z" fill="#1a1a1a" stroke="#FF3333" stroke-width="2"/>
        <!-- 眼睛 - 发光 -->
        <ellipse cx="80" cy="120" rx="12" ry="8" fill="#00FFFF" filter="url(#glow)"/>
        <ellipse cx="120" cy="120" rx="12" ry="8" fill="#00FFFF" filter="url(#glow)"/>
        <!-- 反应堆核心 -->
        <circle cx="100" cy="180" r="15" fill="none" stroke="#00FFFF" stroke-width="2" filter="url(#glow)"/>
        <circle cx="100" cy="180" r="8" fill="#00FFFF" filter="url(#glow)"/>
    </svg>'''
    
    svg_base64 = base64.b64encode(svg_ironman.encode()).decode()
    return f"data:image/svg+xml;base64,{svg_base64}"

# 获取背景图URL（本地或SVG）
bg_image_url = get_ironman_background()

# ================== 完整样式 ==================
bg_html = f"""
<style>
    [data-testid="stAppViewContainer"] {{
        background: radial-gradient(ellipse at center, #0a0e17 0%, #000000 100%);
        color: #e0e0e0;
    }}

    /* 内容区域 - 半透明黑蓝 + 红色边框微光 */
    .main .block-container {{
        background: rgba(10, 15, 30, 0.85) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 60, 60, 0.3);
        box-shadow: 
            0 0 40px rgba(255, 60, 60, 0.15),
            inset 0 0 30px rgba(0, 0, 0, 0.5);
        border-radius: 20px;
        max-width: 88% !important;
        position: relative;
        z-index: 10;
    }}

    h1, h2, h3 {{
        color: #ff4d4d;
        text-shadow: 0 0 15px rgba(255, 77, 77, 0.8);
        font-family: 'Share Tech Mono', monospace;
        letter-spacing: 2px;
    }}

    .stTextInput input, .stSelectbox, .stMultiSelect, .stDateInput input {{
        background: rgba(5, 10, 20, 0.8) !important;
        border: 1px solid rgba(255, 77, 77, 0.5) !important;
        color: #fff !important;
        box-shadow: 0 0 10px rgba(255, 77, 77, 0.2);
    }}

    .stButton button {{
        background: linear-gradient(135deg, rgba(255,0,0,0.1), rgba(0,0,0,0.2)) !important;
        border: 1px solid #ff4d4d !important;
        color: #ff4d4d !important;
        text-shadow: 0 0 8px rgba(255, 77, 77, 0.8);
        transition: all 0.3s;
    }}

    .stButton button:hover {{
        background: rgba(255, 77, 77, 0.25) !important;
        box-shadow: 0 0 25px rgba(255, 77, 77, 0.6);
        transform: translateY(-2px);
    }}

    /* === 钢铁侠背景核心样式 === */
    .ironman-bg {{
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 75%;           /* 页面宽度的3/4，左右留空 */
        height: 85vh;         /* 占视口85%高度，大图效果 */
        z-index: 0;
        pointer-events: none;
        
        /* 背景图设置 - 使用Base64URL */
        background-image: url('{bg_image_url}');
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
        
        /* 发光效果 - 多层红色阴影 + 呼吸动画 */
        filter: drop-shadow(0 0 20px rgba(255, 0, 0, 0.6))
                drop-shadow(0 0 40px rgba(255, 60, 60, 0.4))
                drop-shadow(0 0 80px rgba(200, 0, 0, 0.3));
        
        /* 呼吸动画：透明度 + 发光强度变化 */
        animation: breathe 4s ease-in-out infinite;
    }}

    @keyframes breathe {{
        0%, 100% {{ 
            opacity: 0.3;      /* 低谷：较淡但可见 */
            filter: drop-shadow(0 0 10px rgba(255, 0, 0, 0.4))
                    drop-shadow(0 0 30px rgba(255, 60, 60, 0.2));
        }}
        50% {{ 
            opacity: 0.7;      /* 峰值：明显可见，强烈发光 */
            filter: drop-shadow(0 0 40px rgba(255, 0, 0, 0.9))
                    drop-shadow(0 0 80px rgba(255, 60, 60, 0.6))
                    drop-shadow(0 0 120px rgba(255, 0, 0, 0.3));
        }}
    }}

    /* 扫描线动画 */
    @keyframes scan {{
        0% {{ top: -10%; opacity: 0; }}
        10% {{ opacity: 1; }}
        90% {{ opacity: 1; }}
        100% {{ top: 110%; opacity: 0; }}
    }}
    .scan-line {{
        position: fixed;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(to right, transparent, #ff4d4d, transparent);
        box-shadow: 0 0 15px #ff4d4d, 0 0 30px rgba(255, 77, 77, 0.5);
        animation: scan 6s linear infinite;
        z-index: 9999;
        pointer-events: none;
    }}

    /* 右下角雷达 */
    @keyframes radar {{
        0% {{ transform: scale(1); opacity: 0.8; border-color: rgba(255,77,77,0.8); }}
        100% {{ transform: scale(2.5); opacity: 0; border-color: rgba(255,77,77,0); }}
    }}
    .radar-pulse {{
        position: fixed;
        bottom: 40px;
        right: 40px;
        width: 60px;
        height: 60px;
        border: 2px solid rgba(255,77,77,0.8);
        border-radius: 50%;
        animation: radar 2s ease-out infinite;
        z-index: 9998;
        pointer-events: none;
    }}
    .radar-pulse::before {{
        content: '';
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        width: 10px; height: 10px;
        background: #ff4d4d;
        border-radius: 50%;
        box-shadow: 0 0 20px #ff4d4d;
    }}
</style>

<!-- 钢铁侠发光背景容器 -->
<div class="ironman-bg"></div>

<!-- HUD元素 -->
<div class="scan-line"></div>
<div class="radar-pulse"></div>
"""

st.html(bg_html)

# ================== 修复 use_container_width 警告 ==================
# 在你代码中搜索所有的 use_container_width=True，替换为 width='stretch'
# 找到这行（大约在显示dataframe的地方）：
# st.dataframe(..., use_container_width=True, ...)
# 改为：
# st.dataframe(..., width='stretch', ...)

# ================== 侧边栏语言选择 ==================
with st.sidebar:
    # 语言切换
    lang_choice = st.radio(t("language"), [t("chinese"), t("english")], index=0 if st.session_state.lang == "zh" else 1)
    if lang_choice == t("english"):
        st.session_state.lang = "en"
    else:
        st.session_state.lang = "zh"

    st.markdown(f"## {t('control_panel')}")
    today = datetime.now().date()
    selected_date = st.date_input(t("select_date"), today, min_value=today - timedelta(days=30), max_value=today)
    platforms = st.multiselect(t("platform_filter"), ["微博", "百度"], default=["微博", "百度"])

# 主标题
st.title(t("title"))
st.caption(t("caption"))

# ================== 数据加载 ==================
@st.cache_data(ttl=300)
def load_data(date_str):
    json_path = f"data/hot_{date_str}.json"
    if not os.path.exists(json_path):
        st.info(f"{date_str} {t('no_data')}")
        return pd.DataFrame()
    try:
        df = pd.read_json(json_path)
        if 'platform' in df.columns:
            df['platforms'] = df['platform']
        if 'title' in df.columns:
            df['display_title'] = df['title']
        return df
    except:
        return pd.DataFrame()

df = load_data(selected_date.strftime("%Y-%m-%d"))

# 搜索
keyword = st.text_input(t("search_placeholder"), placeholder=t("search_placeholder"))

filtered = df.copy() if not df.empty else pd.DataFrame()

if keyword.strip() and not filtered.empty:
    keywords = [k.lower().strip() for k in keyword.split() if k.strip()]
    mask = pd.Series(True, index=filtered.index)
    for k in keywords:
        mask &= filtered['display_title'].str.lower().str.contains(k, na=False)
    filtered = filtered[mask]

if platforms and not filtered.empty:
    platform_mask = filtered['platforms'].astype(str).str.contains('|'.join(platforms), na=False)
    filtered = filtered[platform_mask]

# 显示表格
if not filtered.empty:
    st.subheader(f"{t('match_result')}：{len(filtered)} {t('total_hot')}")
    st.dataframe(
        filtered[['rank', 'platforms', 'display_title', 'heat', 'link']].sort_values('rank'),
        column_config={
            "rank": "排名",
            "platforms": "平台",
            "display_title": "标题",
            "heat": "热度",
            "link": st.column_config.LinkColumn(t("view"))
        },
        width='stretch',
        hide_index=True
    )
elif not df.empty:
    st.info(t("no_match"))
else:
    st.warning(t("no_data"))

# 统计指标
if not df.empty:
    col1, col2 = st.columns(2)
    col1.metric(t("total_hot"), len(df))
    col2.metric(t("current_match"), len(filtered))

# ================== 一键导出 ==================
if not filtered.empty:
    st.subheader(t("export"))
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        if st.button(t("export_md")):
            md_text = filtered.to_markdown(index=False)
            st.download_button(t("download_md"), md_text, f"hot_{selected_date}.md", "text/markdown")
    with col_exp2:
        if st.button(t("export_csv")):
            csv = filtered.to_csv(index=False).encode('utf-8-sig')
            st.download_button(t("download_csv"), csv, f"hot_{selected_date}.csv", "text/csv")

# ================== 关注雷达 ==================
st.markdown("---")
st.subheader(t("alert_radar"))
try:
    from config import KEYWORDS
except ImportError:
    KEYWORDS = ["马斯克", "特斯拉", "钢铁侠"]

if not df.empty and 'display_title' in df.columns:
    hits = []
    total = 0
    for kw in KEYWORDS:
        count = df['display_title'].str.contains(kw, case=False, na=False).sum()
        if count > 0:
            hits.append(f"**{kw}** → {t('hit_count', count=count)}")
            total += count
    if hits:
        st.success(f"{t('today_signals')} {total} {t('times')}")
        for hit in hits:
            st.markdown(hit)
    else:
        st.info(t("no_signals"))

# ================== 历史趋势图 ==================
st.markdown("---")
st.subheader(t("trend"))
selected_kw = st.selectbox(t("select_kw"), KEYWORDS)

if selected_kw:
    dates, counts, heats = [], [], []
    today = datetime.now().date()
    for i in range(7):
        d = today - timedelta(days=i)
        date_str = d.strftime("%Y-%m-%d")
        path = f"data/hot_{date_str}.json"
        if os.path.exists(path):
            try:
                day_df = pd.read_json(path)
                title_col = 'display_title' if 'display_title' in day_df.columns else 'title'
                count = day_df[title_col].str.contains(selected_kw, case=False, na=False).sum() if title_col in day_df.columns else 0
                heat = day_df[day_df[title_col].str.contains(selected_kw, case=False, na=False)]['heat'].sum() if 'heat' in day_df.columns and title_col in day_df.columns else 0
            except:
                count = heat = 0
        else:
            count = heat = 0
        dates.append(d.strftime("%m-%d"))
        counts.append(count)
        heats.append(heat)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=dates[::-1], y=counts[::-1], name=t("occurrences"), marker_color="#ff4d4d"), secondary_y=False)
    fig.add_trace(go.Scatter(x=dates[::-1], y=heats[::-1], name=t("total_heat"), mode="lines+markers", line=dict(color="#ffcc00", width=3)), secondary_y=True)
    fig.update_layout(
        title=f"{selected_kw} {t('7day_trend')}",
        template="plotly_dark",
        height=400,
        font=dict(color="#e0e0e0")
    )
    st.plotly_chart(fig, use_container_width=True)

# ================== JARVIS 语音播报 ==================
st.markdown("---")
st.subheader(t("voice"))
if st.button(t("voice_btn")):
    if not df.empty:
        total = len(df)
        speak_text = f"{t('jarvis_online')} {t('total_scanned')} {total} {t('hotspots')}."
        if 'filtered' in locals() and len(filtered) > 0:
            speak_text += f" {t('high_energy')} {len(filtered)} {t('items')}."
        js = f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{speak_text}");
            msg.lang = "zh-CN";
            msg.rate = 1.05;
            window.speechSynthesis.speak(msg);
        </script>
        """
        st.components.v1.html(js, height=0)
        st.success(t("voice_success"))
    else:
        st.warning(t("voice_no_data"))

if st.button(t("refresh")):
    st.rerun()