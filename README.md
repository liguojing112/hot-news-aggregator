# 🛡️ JARVIS 热搜雷达 · 你的全网情报中心

> **Tony Stark 专属 · 钢铁侠级信息聚合系统**  
> 每天自动抓取微博 + 百度热搜，智能去重合并，生成日报、推送微信、网页搜索、语音播报、趋势图 —— 一个属于你自己的 Jarvis。

![Status](https://img.shields.io/badge/Status-Online-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ 它能做什么？

- **自动抓取**：每天 08:00 定时爬取微博热搜榜 + 百度热搜榜，去重合并  
- **日报生成**：将当天热点保存为 Markdown 文件（`output/`），方便阅读  
- **实时推送**：命中你关注的关键词时，通过企业微信机器人立刻通知你  
- **网页交互**：Streamlit 搭建的酷炫面板，支持按日期筛选、关键词搜索、趋势图表  
- **语音播报**：点击按钮，Jarvis 亲口念出当天的热点新闻  
- **一键导出**：搜索结果可导出为 Markdown 或 Excel 文件  
- **自动清理**：只保留最近 7 天的数据，不占空间  
- **双击启动**：两个 `.bat` 脚本，小白也能轻松运行  

---

## 🚀 快速开始

### 1. 下载 / 克隆项目
```bash
git clone https://github.com/你的名字/hot-news-aggregator.git
cd hot-news-aggregator
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置企业微信机器人（可选，用于推送）
- 在企业微信群里添加机器人，获取 Webhook URL  
- 打开 `config.py`，将 URL 填入 `ENTERPRISE_WECHAT_WEBHOOK`（不填也不影响其他功能）

### 4. 选择你的运行模式

#### 🌐 网页模式（推荐）
双击 `start_web.bat`，或手动运行：
```bash
streamlit run app.py
```
浏览器自动打开，你可以搜索、看趋势、听语音、导出结果。

#### ⏰ 后台定时模式
双击 `start_background.bat`，程序将在后台运行，每天 08:00 自动抓取并推送。  
（窗口可最小化，不要关闭）

---

## 📸 功能截图

> *（建议你放几张截图：网页主界面、趋势图、语音播报按钮、推送示例）*

---

## 🛠️ 项目结构

```
hot_news_aggregator/
├── crawlers/               # 采集模块
│   ├── weibo.py            # 微博热搜爬虫
│   └── baidu.py            # 百度热搜爬虫
├── data/                   # 每日原始数据（JSON）
├── output/                 # 生成的日报（Markdown）
├── utils/                  # 工具函数
│   └── cleaner.py          # 自动清理旧文件
├── app.py                  # Streamlit 网页应用
├── main.py                 # 定时调度核心
├── config.py               # 配置文件（关键词、Webhook等）
├── start_web.bat           # 一键启动网页脚本
├── start_background.bat    # 一键启动后台定时脚本
├── requirements.txt        # 依赖列表
└── README.md               # 就是你现在看到的文件
```

---

## ⚙️ 配置说明

所有个性化设置都在 `config.py` 里：

```python
# 你关注的关键词（命中即推送）
KEYWORDS = ["特斯拉", "SpaceX", "马斯克"]

# 企业微信机器人 Webhook（留空则不推送）
ENTERPRISE_WECHAT_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxx"

# 数据保留天数
KEEP_DAYS = 7
```

---

## 📜 许可证

本项目采用 MIT 许可证 —— 你可以自由使用、修改、分发，只需保留原作者声明。  
详情见 [LICENSE](LICENSE) 文件。

---

## 🧠 致敬

**Made with ❤️ by 小海波 & Grok**  
从最初的一个小想法，到如今这个能看、能听、能推的全功能情报系统，感谢一路的探索和折腾。

**现在，去启动你的 Jarvis 吧！** 🛡️

--- 

*注：本项目仅供个人学习与使用，请合理抓取数据，尊重目标网站的 robots.txt 规则。*