"""
非洲商用车战情情报室
Africa Commercial Vehicle Intelligence Dashboard
"""

import streamlit as st
import feedparser
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="非洲商用车战情情报室",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS – deep-tech dark theme ────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Source+Code+Pro:wght@400;600&family=Noto+Sans+SC:wght@300;400;700&display=swap');

:root {
    --bg-primary:   #080d14;
    --bg-card:      #0d1522;
    --bg-panel:     #111b2a;
    --accent:       #00d4ff;
    --accent2:      #00ff9d;
    --accent3:      #ff6b35;
    --warn:         #ffd93d;
    --text-main:    #c8dff0;
    --text-dim:     #5a7a96;
    --border:       rgba(0,212,255,0.18);
    --glow:         0 0 18px rgba(0,212,255,0.25);
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-primary) !important;
    color: var(--text-main);
    font-family: 'Noto Sans SC', 'Rajdhani', sans-serif;
}

[data-testid="stSidebar"] {
    background: #090e18 !important;
    border-right: 1px solid var(--border);
}

.cv-header {
    background: linear-gradient(135deg, #0d1a2e 0%, #091420 60%, #0a1f35 100%);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--glow);
}
.cv-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), var(--accent2), transparent);
}
.cv-header-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: 4px;
    color: var(--accent);
    text-transform: uppercase;
    margin: 0;
    text-shadow: 0 0 20px rgba(0,212,255,0.5);
}
.cv-header-sub {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.72rem;
    color: var(--text-dim);
    letter-spacing: 2px;
    margin-top: 4px;
}
.cv-header-ts {
    position: absolute;
    right: 32px; top: 50%;
    transform: translateY(-50%);
    font-family: 'Source Code Pro', monospace;
    font-size: 0.7rem;
    color: var(--accent2);
    text-align: right;
}
.status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--accent2);
    box-shadow: 0 0 8px var(--accent2);
    margin-right: 6px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%,100% { opacity:1; } 50% { opacity:.3; }
}

[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 18px 22px !important;
    box-shadow: var(--glow) !important;
    position: relative;
    overflow: hidden;
}
[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
[data-testid="stMetricLabel"] {
    font-family: 'Source Code Pro', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 1.5px !important;
    color: var(--text-dim) !important;
    text-transform: uppercase;
}
[data-testid="stMetricValue"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.7rem !important;
    font-weight: 700 !important;
    color: var(--accent) !important;
}

.section-label {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    color: var(--accent);
    text-transform: uppercase;
    border-bottom: 1px solid var(--border);
    padding-bottom: 6px;
    margin-bottom: 12px;
}

.news-col-header {
    background: linear-gradient(180deg, #0f1e30 0%, #0a1520 100%);
    border: 1px solid var(--border);
    border-top: 2px solid var(--accent);
    border-radius: 8px 8px 0 0;
    padding: 12px 16px;
}
.news-col-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--accent2);
    letter-spacing: 1px;
    margin: 0;
}
.news-col-query {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.6rem;
    color: var(--text-dim);
    margin-top: 3px;
    word-break: break-word;
}

.news-item {
    background: var(--bg-card);
    border: 1px solid rgba(0,212,255,0.1);
    border-top: none;
    padding: 12px 16px;
    transition: border-color 0.2s;
}
.news-item:hover {
    border-color: rgba(0,212,255,0.35);
    background: #0f1c2e;
}
.news-item:last-child {
    border-radius: 0 0 8px 8px;
}
.news-title a {
    font-family: 'Noto Sans SC', sans-serif;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text-main) !important;
    text-decoration: none;
    line-height: 1.4;
}
.news-title a:hover { color: var(--accent) !important; }
.news-meta {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.62rem;
    color: var(--text-dim);
    margin-top: 5px;
    display: flex;
    gap: 10px;
}
.news-tag {
    display: inline-block;
    background: rgba(0,212,255,0.08);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 3px;
    padding: 1px 6px;
    font-size: 0.58rem;
    color: var(--accent);
    font-family: 'Source Code Pro', monospace;
    letter-spacing: 1px;
}
.no-news {
    background: var(--bg-card);
    border: 1px dashed rgba(0,212,255,0.15);
    border-radius: 0 0 8px 8px;
    padding: 24px;
    text-align: center;
    font-family: 'Source Code Pro', monospace;
    font-size: 0.72rem;
    color: var(--text-dim);
}

.sidebar-section {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.65rem;
    letter-spacing: 2px;
    color: var(--accent);
    text-transform: uppercase;
    margin: 18px 0 8px 0;
    border-bottom: 1px solid var(--border);
    padding-bottom: 5px;
}
.sidebar-link {
    display: block;
    padding: 8px 12px;
    margin: 4px 0;
    background: rgba(0,212,255,0.04);
    border: 1px solid rgba(0,212,255,0.1);
    border-radius: 5px;
    font-size: 0.78rem;
    color: var(--text-main) !important;
    text-decoration: none !important;
    font-family: 'Noto Sans SC', sans-serif;
    transition: all 0.2s;
}
.sidebar-link:hover {
    background: rgba(0,212,255,0.12);
    border-color: var(--accent);
    color: var(--accent) !important;
}

hr { border-color: var(--border) !important; }

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding-top: 1.5rem !important; }
</style>
""",
    unsafe_allow_html=True,
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def fetch_news(query: str, limit: int = 5) -> list:
    encoded = query.replace(" ", "+").replace('"', "%22")
    url = f"https://news.google.com/rss/search?q={encoded}&hl=en-US&gl=US&ceid=US:en"
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries[:limit]:
            pub = entry.get("published", "")
            try:
                dt = datetime(*entry.published_parsed[:6])
                pub = dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                pass
            source = entry.get("source", {}).get("title", "Unknown")
            items.append({
                "title": entry.get("title", "No title"),
                "link":  entry.get("link", "#"),
                "published": pub,
                "source": source,
            })
        return items
    except Exception:
        return []


def render_news_column(col, icon: str, title: str, query: str):
    with col:
        st.markdown(
            f"""
            <div class="news-col-header">
                <div class="news-col-title">{icon} {title}</div>
                <div class="news-col-query">
                    <span class="news-tag">RSS</span>&nbsp;{query}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.spinner(""):
            news = fetch_news(query)

        if not news:
            st.markdown(
                '<div class="no-news">⚠ 暂无数据 / No data fetched<br>请检查网络连接</div>',
                unsafe_allow_html=True,
            )
        else:
            for item in news:
                st.markdown(
                    f"""
                    <div class="news-item">
                        <div class="news-title">
                            <a href="{item['link']}" target="_blank">{item['title']}</a>
                        </div>
                        <div class="news-meta">
                            <span>📅 {item['published']}</span>
                            <span>| 📰 {item['source']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem;font-weight:700;
                    color:#00d4ff;letter-spacing:3px;padding:8px 0;
                    border-bottom:1px solid rgba(0,212,255,0.2);margin-bottom:4px;">
            🛰 工具链接中心
        </div>
        <div style="font-family:'Source Code Pro',monospace;font-size:0.6rem;
                    color:#5a7a96;letter-spacing:1px;margin-bottom:16px;">
            INTELLIGENCE RESOURCE HUB
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-section">🇳🇬 尼日利亚</div>', unsafe_allow_html=True)
    for label, url in [
        ("🏛 尼日利亚海关总署", "https://www.customs.gov.ng"),
        ("🚛 尼日利亚公路运输协会", "https://www.narto.com.ng"),
        ("📊 Central Bank of Nigeria – 汇率", "https://www.cbn.gov.ng/rates/exchratebycurrency.asp"),
        ("🏗 Dangote Industries", "https://www.dangote.com"),
    ]:
        st.markdown(f'<a class="sidebar-link" href="{url}" target="_blank">{label}</a>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">🇿🇦 南非</div>', unsafe_allow_html=True)
    for label, url in [
        ("🚗 AutoTrader 南非 – 商用车", "https://www.autotrader.co.za/trucks"),
        ("🚂 Transnet Freight Rail", "https://www.transnet.net"),
        ("📈 SARB – 兰特汇率", "https://www.resbank.co.za"),
        ("🏭 NAAMSA 汽车协会", "https://www.naamsa.co.za"),
    ]:
        st.markdown(f'<a class="sidebar-link" href="{url}" target="_blank">{label}</a>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">🇲🇦 摩洛哥</div>', unsafe_allow_html=True)
    for label, url in [
        ("🤝 AIVAM 汽车进口商协会", "https://www.aivam.ma"),
        ("⛽ ONHYM – 能源监管", "https://www.onhym.com"),
        ("🌾 OCP Group", "https://www.ocpgroup.ma"),
        ("🛃 摩洛哥海关总署", "https://www.douane.gov.ma"),
    ]:
        st.markdown(f'<a class="sidebar-link" href="{url}" target="_blank">{label}</a>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">🌐 行业情报</div>', unsafe_allow_html=True)
    for label, url in [
        ("📡 FleetAfrica 行业媒体", "https://www.fleetafrica.co.za"),
        ("🚛 Truck & Freight Africa", "https://www.trucksandfreight.co.za"),
        ("🌍 AfDB – 非洲开发银行", "https://www.afdb.org"),
        ("📰 African Business Magazine", "https://african.business"),
    ]:
        st.markdown(f'<a class="sidebar-link" href="{url}" target="_blank">{label}</a>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 刷新所有情报", use_container_width=True):
        st.cache_data.clear()
        st.rerun()


# ── Main ──────────────────────────────────────────────────────────────────────

now_str = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
st.markdown(
    f"""
    <div class="cv-header">
        <div class="cv-header-title">🌍 非洲商用车战情情报室</div>
        <div class="cv-header-sub">AFRICA COMMERCIAL VEHICLE INTELLIGENCE COMMAND CENTER</div>
        <div class="cv-header-ts">
            <div><span class="status-dot"></span>LIVE FEED</div>
            <div style="margin-top:4px;">{now_str} CST</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# KPI Metrics
st.markdown('<div class="section-label">📊 核心市场指标 &nbsp;|&nbsp; KEY MARKET INDICATORS</div>', unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric(
        label="🇳🇬 尼日利亚关税（纯电动）",
        value="0 %",
        delta="免税政策 · 2023年起",
        help="Nigeria 2023 EV import tariff rate – zero-rated to encourage EV adoption",
    )
with k2:
    st.metric(
        label="🇲🇦 摩洛哥柴油均价",
        value="13.5 MAD",
        delta="≈ $1.34 USD/L",
        delta_color="inverse",
        help="Average retail diesel price in Morocco (MAD per litre)",
    )
with k3:
    st.metric(
        label="💱 奈拉兑美元汇率",
        value="NGN/USD",
        delta="实时数据请查 CBN 官网",
        delta_color="off",
        help="Nigerian Naira to US Dollar – check CBN live rate",
    )
with k4:
    st.metric(
        label="💱 兰特兑美元汇率",
        value="ZAR/USD",
        delta="实时数据请查 SARB 官网",
        delta_color="off",
        help="South African Rand to US Dollar – check SARB live rate",
    )

st.markdown("<br>", unsafe_allow_html=True)

# News Intelligence Feed
st.markdown(
    '<div class="section-label">📡 实时情报监控 &nbsp;|&nbsp; REAL-TIME INTELLIGENCE FEED</div>',
    unsafe_allow_html=True,
)

MONITORS = [
    {"icon": "🏗", "title": "大客户动态",  "query": "Morocco OCP Group tender OR Dangote trucks"},
    {"icon": "🚛", "title": "竞品追踪",    "query": "Sinotruk Africa OR Volvo trucks Africa"},
    {"icon": "⚡", "title": "政策与新能源", "query": "Nigeria EV tariff OR Africa green energy"},
    {"icon": "🔗", "title": "物流与基建",  "query": "South Africa logistics OR Transnet"},
]

cols = st.columns(4)
for col, m in zip(cols, MONITORS):
    render_news_column(col, m["icon"], m["title"], m["query"])

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align:center;font-family:'Source Code Pro',monospace;
                font-size:0.62rem;color:#2a4a5e;letter-spacing:2px;
                border-top:1px solid rgba(0,212,255,0.08);padding-top:16px;">
        ⚡ 非洲商用车战情情报室 · AFRICA CV INTELLIGENCE COMMAND &nbsp;|&nbsp;
        数据来源: Google News RSS · 仅供内部商业参考使用
    </div>
    """,
    unsafe_allow_html=True,
)
