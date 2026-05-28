"""
See Africa – Commercial Vehicle Intelligence Command Center
非洲商用车战情情报室 · UPGRADED EDITION
"""

import streamlit as st
import feedparser
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="See Africa · CV Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS – Enterprise BI Dark Theme ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Source+Code+Pro:wght@400;600&family=Noto+Sans+SC:wght@300;400;700&family=Barlow+Condensed:wght@300;400;600;700&display=swap');

:root {
    --bg-primary:  #05090f;
    --bg-card:     #0b1420;
    --bg-panel:    #0f1d2e;
    --accent:      #00c8f0;
    --accent2:     #00e8a0;
    --accent3:     #ff6b35;
    --warn:        #ffd93d;
    --text-main:   #cce0f0;
    --text-dim:    #4a6a86;
    --border:      rgba(0,200,240,0.15);
    --glow:        0 0 24px rgba(0,200,240,0.2);
    --glow-strong: 0 0 40px rgba(0,200,240,0.35);
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-primary) !important;
    color: var(--text-main);
    font-family: 'Noto Sans SC', 'Barlow Condensed', sans-serif;
}
[data-testid="stSidebar"] {
    background: #060b14 !important;
    border-right: 1px solid var(--border);
}

/* ── Hero Header ── */
.cv-header {
    background: linear-gradient(135deg, #0a1828 0%, #071020 50%, #0c2035 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--glow-strong);
}
.cv-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent 0%, var(--accent) 30%, var(--accent2) 70%, transparent 100%);
}
.cv-header::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,200,240,0.3), transparent);
}
.cv-brand {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: 8px;
    color: #ffffff;
    text-transform: uppercase;
    margin: 0;
    line-height: 1;
}
.cv-brand span { color: var(--accent); }
.cv-header-sub {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.68rem;
    color: var(--text-dim);
    letter-spacing: 3px;
    margin-top: 6px;
    text-transform: uppercase;
}
.cv-header-ts {
    position: absolute;
    right: 36px; top: 50%;
    transform: translateY(-50%);
    font-family: 'Source Code Pro', monospace;
    font-size: 0.68rem;
    color: var(--accent2);
    text-align: right;
    line-height: 1.8;
}
.status-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--accent2);
    box-shadow: 0 0 10px var(--accent2);
    margin-right: 6px;
    animation: pulse 2s infinite;
}
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:.25;} }

/* ── Section labels ── */
.section-label {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 4px;
    color: var(--accent);
    text-transform: uppercase;
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
    margin-bottom: 16px;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 20px 24px !important;
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
    font-size: 0.65rem !important;
    letter-spacing: 2px !important;
    color: var(--text-dim) !important;
    text-transform: uppercase;
}
[data-testid="stMetricValue"] {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: var(--accent) !important;
    letter-spacing: 1px;
}

/* ── Map container ── */
.map-container {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0;
    overflow: hidden;
    box-shadow: var(--glow);
    margin-bottom: 28px;
    position: relative;
}
.map-container::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), var(--accent2), transparent);
    z-index: 10;
}

/* ── News columns ── */
.news-col-header {
    background: linear-gradient(180deg, #0f1e32 0%, #091520 100%);
    border: 1px solid var(--border);
    border-top: 2px solid var(--accent);
    border-radius: 10px 10px 0 0;
    padding: 14px 18px;
}
.news-col-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--accent2);
    letter-spacing: 2px;
    margin: 0;
    text-transform: uppercase;
}
.news-col-query {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.57rem;
    color: var(--text-dim);
    margin-top: 4px;
    word-break: break-word;
    line-height: 1.5;
}
.news-tag {
    display: inline-block;
    background: rgba(0,200,240,0.1);
    border: 1px solid rgba(0,200,240,0.25);
    border-radius: 3px;
    padding: 1px 7px;
    font-size: 0.55rem;
    color: var(--accent);
    font-family: 'Source Code Pro', monospace;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-right: 4px;
}
.news-source-tag {
    display: inline-block;
    background: rgba(0,232,160,0.08);
    border: 1px solid rgba(0,232,160,0.2);
    border-radius: 3px;
    padding: 1px 6px;
    font-size: 0.55rem;
    color: var(--accent2);
    font-family: 'Source Code Pro', monospace;
    letter-spacing: 1px;
}
.news-item {
    background: var(--bg-card);
    border: 1px solid rgba(0,200,240,0.08);
    border-top: none;
    padding: 14px 18px;
    transition: all 0.2s;
}
.news-item:hover {
    border-color: rgba(0,200,240,0.3);
    background: #0e1d30;
}
.news-item:last-child { border-radius: 0 0 10px 10px; }
.news-title a {
    font-family: 'Noto Sans SC', sans-serif;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text-main) !important;
    text-decoration: none;
    line-height: 1.5;
}
.news-title a:hover { color: var(--accent) !important; }
.news-meta {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.6rem;
    color: var(--text-dim);
    margin-top: 6px;
    display: flex;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
}
.no-news {
    background: var(--bg-card);
    border: 1px dashed rgba(0,200,240,0.12);
    border-radius: 0 0 10px 10px;
    padding: 28px;
    text-align: center;
    font-family: 'Source Code Pro', monospace;
    font-size: 0.7rem;
    color: var(--text-dim);
    line-height: 2;
}

/* ── Sidebar ── */
.sidebar-section {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 3px;
    color: var(--accent);
    text-transform: uppercase;
    margin: 20px 0 8px 0;
    border-bottom: 1px solid var(--border);
    padding-bottom: 5px;
}
.sidebar-link {
    display: block;
    padding: 9px 13px;
    margin: 4px 0;
    background: rgba(0,200,240,0.03);
    border: 1px solid rgba(0,200,240,0.08);
    border-radius: 6px;
    font-size: 0.8rem;
    color: var(--text-main) !important;
    text-decoration: none !important;
    font-family: 'Noto Sans SC', sans-serif;
    transition: all 0.2s;
    line-height: 1.4;
}
.sidebar-link:hover {
    background: rgba(0,200,240,0.1);
    border-color: var(--accent);
    color: var(--accent) !important;
    padding-left: 17px;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding-top: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DATA – Africa Strategic Markets
# ══════════════════════════════════════════════════════════════════════════════

AFRICA_MARKET_DATA = {
    "Morocco": {
        "iso": "MAR",
        "highlight": True,
        "tier": "战略核心",
        "color_score": 95,
        "tooltip_lines": [
            "🏷 纯电动进口关税：2.5%",
            "⛽ 柴油均价：13.5 MAD/L（≈$1.34）",
            "🚛 年商用车需求：~18,000辆",
            "🏭 OCP集团：磷酸盐运输主力买家",
            "📋 认证要求：UN-ECE R49排放标准",
            "💡 政策亮点：2030绿色能源计划",
        ],
    },
    "Nigeria": {
        "iso": "NGA",
        "highlight": True,
        "tier": "战略核心",
        "color_score": 92,
        "tooltip_lines": [
            "🏷 纯电动进口关税：0%（2023起免税）",
            "🔧 KD散件组装关税：0%",
            "🚛 年商用车需求：~45,000辆（非洲第一）",
            "🏗 Dangote集团：水泥物流最大买家",
            "📋 认证：SON强制认证 + NAFDAC",
            "💡 奈拉波动风险：建议美元结算",
        ],
    },
    "South Africa": {
        "iso": "ZAF",
        "highlight": True,
        "tier": "战略核心",
        "color_score": 88,
        "tooltip_lines": [
            "🏷 商用车进口关税：25%（AGOA优惠）",
            "⛽ 柴油均价：21.6 ZAR/L（≈$1.18）",
            "🚛 年商用车需求：~30,000辆",
            "🚂 Transnet：铁路+港口核心运营商",
            "📋 认证：NRCS强制认证",
            "💡 兰特汇率：1USD≈18.5ZAR（浮动）",
        ],
    },
    "Tunisia": {
        "iso": "TUN",
        "highlight": True,
        "tier": "战略新兴",
        "color_score": 72,
        "tooltip_lines": [
            "🏷 商用车进口关税：10%（欧盟协定国）",
            "⛽ 柴油均价：2.1 TND/L（政府补贴）",
            "🚛 年商用车需求：~8,000辆",
            "🌐 地理优势：欧非贸易走廊枢纽",
            "📋 认证：INNORPI技术标准",
            "💡 重点：磷酸盐与农业物流",
        ],
    },
    "Egypt": {
        "iso": "EGY",
        "highlight": True,
        "tier": "战略新兴",
        "color_score": 78,
        "tooltip_lines": [
            "🏷 商用车进口关税：40%（CBU整车）",
            "🔧 KD组装优惠：5%（国产化率>40%）",
            "🚛 年商用车需求：~25,000辆",
            "🏗 苏伊士运河经济区：重点物流需求",
            "📋 认证：EOS埃及标准局",
            "💡 强烈建议本地组装合作",
        ],
    },
    "Rwanda": {
        "iso": "RWA",
        "highlight": True,
        "tier": "战略新兴",
        "color_score": 65,
        "tooltip_lines": [
            "🏷 商用车进口关税：0%（EAC协议内）",
            "⛽ 柴油均价：1,650 RWF/L（≈$1.45）",
            "🚛 年商用车需求：~3,500辆（高速增长）",
            "🌿 政策亮点：2035年禁售燃油车路线图",
            "📋 认证：RSB卢旺达标准局",
            "💡 非洲最佳营商环境 Top 3",
        ],
    },
}

# All African countries for the base map
ALL_AFRICA_ISO = [
    "DZA","AGO","BEN","BWA","BFA","BDI","CPV","CMR","CAF","TCD",
    "COM","COD","COG","CIV","DJI","EGY","GNQ","ERI","SWZ","ETH",
    "GAB","GMB","GHA","GIN","GNB","KEN","LSO","LBR","LBY","MDG",
    "MWI","MLI","MRT","MUS","MAR","MOZ","NAM","NER","NGA","RWA",
    "STP","SEN","SLE","SOM","ZAF","SSD","SDN","TZA","TGO","TUN",
    "UGA","ZMB","ZWE","ESH","SHN","MYT","REU",
]


# ══════════════════════════════════════════════════════════════════════════════
# MAP BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def build_africa_map() -> go.Figure:
    rows = []
    for iso in ALL_AFRICA_ISO:
        matched = None
        for country, data in AFRICA_MARKET_DATA.items():
            if data["iso"] == iso:
                matched = (country, data)
                break
        if matched:
            name, d = matched
            tooltip = f"<b style='color:#00e8a0;font-size:14px;'>{'★ ' if d['highlight'] else ''}{name}</b><br>"
            tooltip += f"<span style='color:#4a8fa8;font-size:10px;letter-spacing:2px;'>{d['tier'].upper()}</span><br><br>"
            tooltip += "<br>".join(d["tooltip_lines"])
            rows.append({
                "iso": iso,
                "name": name,
                "score": d["color_score"],
                "tier": d["tier"],
                "tooltip": tooltip,
                "highlight": 1,
            })
        else:
            rows.append({
                "iso": iso,
                "name": iso,
                "score": 15,
                "tier": "未覆盖市场",
                "tooltip": f"<b>{iso}</b><br><span style='color:#4a6a86;'>暂无覆盖计划</span>",
                "highlight": 0,
            })

    df = pd.DataFrame(rows)

    fig = go.Figure()

    # Base layer – all Africa (dim)
    df_base = df[df["highlight"] == 0]
    fig.add_trace(go.Choropleth(
        locations=df_base["iso"],
        z=df_base["score"],
        text=df_base["tooltip"],
        hovertemplate="%{text}<extra></extra>",
        colorscale=[[0, "#0d1e30"], [1, "#1a3348"]],
        showscale=False,
        marker_line_color="rgba(0,200,240,0.15)",
        marker_line_width=0.5,
        zmin=0, zmax=100,
    ))

    # Highlight layer – strategic markets
    df_hl = df[df["highlight"] == 1]
    fig.add_trace(go.Choropleth(
        locations=df_hl["iso"],
        z=df_hl["score"],
        text=df_hl["tooltip"],
        hovertemplate="%{text}<extra></extra>",
        colorscale=[
            [0.0,  "#0d3a5c"],
            [0.3,  "#0a5a8a"],
            [0.6,  "#0080c0"],
            [0.8,  "#00a8e0"],
            [1.0,  "#00c8f0"],
        ],
        showscale=True,
        colorbar=dict(
            title=dict(text="战略优先级", font=dict(color="#4a6a86", size=10, family="Source Code Pro")),
            tickfont=dict(color="#4a6a86", size=9, family="Source Code Pro"),
            bgcolor="rgba(5,9,15,0.8)",
            bordercolor="rgba(0,200,240,0.2)",
            borderwidth=1,
            thickness=10,
            len=0.5,
            x=0.98,
        ),
        marker_line_color="rgba(0,200,240,0.5)",
        marker_line_width=1.2,
        zmin=0, zmax=100,
    ))

    fig.update_layout(
        geo=dict(
            scope="africa",
            showframe=False,
            showcoastlines=True,
            coastlinecolor="rgba(0,200,240,0.2)",
            coastlinewidth=0.8,
            showland=True,
            landcolor="#080e18",
            showocean=True,
            oceancolor="#040810",
            showlakes=False,
            showrivers=False,
            showcountries=True,
            countrycolor="rgba(0,200,240,0.12)",
            countrywidth=0.4,
            bgcolor="#05090f",
            projection_type="natural earth",
        ),
        paper_bgcolor="#05090f",
        plot_bgcolor="#05090f",
        margin=dict(l=0, r=60, t=0, b=0),
        height=540,
        hoverlabel=dict(
            bgcolor="#0b1828",
            bordercolor="#00c8f0",
            font=dict(
                family="Noto Sans SC, Source Code Pro, monospace",
                size=12,
                color="#cce0f0",
            ),
        ),
        dragmode=False,
    )

    return fig


# ══════════════════════════════════════════════════════════════════════════════
# NEWS FETCHER – Authority-Filtered
# ══════════════════════════════════════════════════════════════════════════════

# Trusted sources injected into every query
TRUSTED_SOURCES = (
    "site:reuters.com OR site:bloomberg.com OR site:ft.com "
    "OR site:africa.com OR site:businessday.ng OR site:engineeringnews.co.za "
    "OR site:zawya.com OR site:afdb.org OR site:gov.ma OR site:customs.gov.ng"
)

NOISE_WORDS = {
    "rumor", "rumour", "unconfirmed", "alleged", "clickbait",
    "shocking", "you won't believe", "viral", "leaked",
}

def fetch_news(query: str, limit: int = 5) -> list:
    full_query = f"({query}) ({TRUSTED_SOURCES})"
    encoded = full_query.replace(" ", "+").replace('"', "%22")
    url = (
        f"https://news.google.com/rss/search"
        f"?q={encoded}&hl=en-US&gl=US&ceid=US:en"
    )
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries:
            if len(items) >= limit:
                break
            title = entry.get("title", "No title")
            # Filter noise
            title_lower = title.lower()
            if any(noise in title_lower for noise in NOISE_WORDS):
                continue
            pub = entry.get("published", "")
            try:
                dt = datetime(*entry.published_parsed[:6])
                pub = dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                pass
            source = entry.get("source", {}).get("title", "–")
            items.append({
                "title": title,
                "link":  entry.get("link", "#"),
                "published": pub,
                "source": source,
            })
        return items
    except Exception:
        return []


def render_news_column(col, icon: str, title: str, badge: str, query: str):
    with col:
        st.markdown(f"""
        <div class="news-col-header">
            <div class="news-col-title">{icon} {title}</div>
            <div class="news-col-query">
                <span class="news-tag">{badge}</span>
                <span class="news-source-tag">REUTERS · BLOOMBERG · FT</span><br>
                <span style="opacity:.6;">{query}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner(""):
            news = fetch_news(query)

        if not news:
            st.markdown("""
            <div class="no-news">
                ⚠ &nbsp;权威来源暂无匹配结果<br>
                <span style="font-size:0.6rem;">Authority sources returned no results · Check network</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            for item in news:
                st.markdown(f"""
                <div class="news-item">
                    <div class="news-title">
                        <a href="{item['link']}" target="_blank">{item['title']}</a>
                    </div>
                    <div class="news-meta">
                        <span>🕐 {item['published']}</span>
                        <span>·</span>
                        <span>📰 {item['source']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="font-family:'Barlow Condensed',sans-serif;font-size:1.3rem;font-weight:700;
                color:#00c8f0;letter-spacing:4px;padding:10px 0 4px 0;
                border-bottom:1px solid rgba(0,200,240,0.18);">
        🛰️ &nbsp;INTEL HUB
    </div>
    <div style="font-family:'Source Code Pro',monospace;font-size:0.58rem;
                color:#4a6a86;letter-spacing:2px;margin-bottom:14px;margin-top:4px;">
        工具与资源链接中心
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">🇳🇬 &nbsp;Nigeria</div>', unsafe_allow_html=True)
    for label, url in [
        ("🏛️ 尼日利亚海关总署 (NCS)", "https://www.customs.gov.ng"),
        ("🏦 Central Bank of Nigeria", "https://www.cbn.gov.ng/rates/exchratebycurrency.asp"),
        ("🚛 NARTO 公路运输协会", "https://www.narto.com.ng"),
        ("🏗️ Dangote Group", "https://www.dangote.com"),
    ]:
        st.markdown(f'<a class="sidebar-link" href="{url}" target="_blank">{label}</a>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">🇿🇦 &nbsp;South Africa</div>', unsafe_allow_html=True)
    for label, url in [
        ("🚗 AutoTrader ZA – Trucks", "https://www.autotrader.co.za/trucks"),
        ("🚂 Transnet Freight Rail", "https://www.transnet.net"),
        ("📈 SARB 兰特汇率", "https://www.resbank.co.za"),
        ("🏭 NAAMSA 汽车行业协会", "https://www.naamsa.co.za"),
    ]:
        st.markdown(f'<a class="sidebar-link" href="{url}" target="_blank">{label}</a>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">🇲🇦 &nbsp;Morocco</div>', unsafe_allow_html=True)
    for label, url in [
        ("🤝 AIVAM 汽车进口商协会", "https://www.aivam.ma"),
        ("🌾 OCP Group", "https://www.ocpgroup.ma"),
        ("🛃 摩洛哥海关总署", "https://www.douane.gov.ma"),
        ("⛽ ONHYM 能源监管", "https://www.onhym.com"),
    ]:
        st.markdown(f'<a class="sidebar-link" href="{url}" target="_blank">{label}</a>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">🇪🇬 &nbsp;Egypt · 🇹🇳 &nbsp;Tunisia · 🇷🇼 &nbsp;Rwanda</div>', unsafe_allow_html=True)
    for label, url in [
        ("🏛️ 埃及工业部 (MoTI)", "https://www.moti.gov.eg"),
        ("📋 EOS 埃及标准局", "https://www.eos.org.eg"),
        ("🇹🇳 INNORPI 突尼斯标准", "https://www.innorpi.tn"),
        ("🇷🇼 RSB 卢旺达标准局", "https://www.rsb.gov.rw"),
    ]:
        st.markdown(f'<a class="sidebar-link" href="{url}" target="_blank">{label}</a>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">🌐 &nbsp;行业情报</div>', unsafe_allow_html=True)
    for label, url in [
        ("📡 Engineering News ZA", "https://www.engineeringnews.co.za"),
        ("🚛 Truck & Freight Africa", "https://www.trucksandfreight.co.za"),
        ("🌍 AfDB 非洲开发银行", "https://www.afdb.org"),
        ("📰 African Business Magazine", "https://african.business"),
        ("📊 Zawya 中东非洲财经", "https://www.zawya.com"),
    ]:
        st.markdown(f'<a class="sidebar-link" href="{url}" target="_blank">{label}</a>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 &nbsp;刷新全部情报", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.markdown("""
    <div style="font-family:'Source Code Pro',monospace;font-size:0.58rem;
                color:#2a4a5e;text-align:center;margin-top:20px;line-height:2;">
        SEE AFRICA · CV INTEL v2.0<br>仅供内部商业参考使用
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════════

# ── Hero Header ──
now_str = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
st.markdown(f"""
<div class="cv-header">
    <div class="cv-brand">SEE <span>AFRICA</span></div>
    <div class="cv-header-sub">
        ◆ &nbsp;Commercial Vehicle Intelligence Command Center &nbsp;◆ &nbsp;非洲商用车战情情报室
    </div>
    <div class="cv-header-ts">
        <div><span class="status-dot"></span>LIVE &nbsp;·&nbsp; ALL SYSTEMS NOMINAL</div>
        <div>{now_str} &nbsp;CST</div>
        <div style="color:#4a6a86;font-size:0.58rem;margin-top:2px;">
            6 MARKETS MONITORED &nbsp;·&nbsp; 4 INTEL STREAMS
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Metrics ──
st.markdown(
    '<div class="section-label">📊 &nbsp;核心市场指标 &nbsp;·&nbsp; KEY MARKET INDICATORS</div>',
    unsafe_allow_html=True
)
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric(
        label="🇳🇬  尼日利亚关税 · 纯电动",
        value="0 %",
        delta="✦ 免税政策 · 2023年起",
        help="Nigeria 2023 EV import tariff – zero-rated to incentivize adoption",
    )
with k2:
    st.metric(
        label="🇲🇦  摩洛哥柴油均价",
        value="13.5 MAD",
        delta="≈ $1.34 USD / Litre",
        delta_color="inverse",
        help="Average retail diesel price in Morocco (MAD per litre, 2024)",
    )
with k3:
    st.metric(
        label="💱  奈拉兑美元汇率",
        value="NGN / USD",
        delta="➜ 实时数据见 CBN 官网",
        delta_color="off",
        help="Nigerian Naira – check Central Bank of Nigeria for live rate",
    )
with k4:
    st.metric(
        label="💱  兰特兑美元汇率",
        value="ZAR / USD",
        delta="➜ 实时数据见 SARB 官网",
        delta_color="off",
        help="South African Rand – check SARB for live rate",
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── Africa Strategic Map ──
st.markdown(
    '<div class="section-label">🗺️ &nbsp;非洲战略地图 &nbsp;·&nbsp; AFRICA STRATEGIC MARKET MAP</div>',
    unsafe_allow_html=True
)
st.markdown('<div class="map-container">', unsafe_allow_html=True)
fig = build_africa_map()
st.plotly_chart(fig, use_container_width=True, config={
    "displayModeBar": False,
    "scrollZoom": False,
})
st.markdown('</div>', unsafe_allow_html=True)

# Legend pills
lc1, lc2, lc3, lc4, lc5, lc6 = st.columns(6)
for col, flag, country, tier in [
    (lc1, "🇲🇦", "摩洛哥", "战略核心"),
    (lc2, "🇳🇬", "尼日利亚", "战略核心"),
    (lc3, "🇿🇦", "南非", "战略核心"),
    (lc4, "🇪🇬", "埃及", "战略新兴"),
    (lc5, "🇹🇳", "突尼斯", "战略新兴"),
    (lc6, "🇷🇼", "卢旺达", "战略新兴"),
]:
    color = "#00c8f0" if tier == "战略核心" else "#00e8a0"
    with col:
        st.markdown(f"""
        <div style="background:rgba(0,200,240,0.05);border:1px solid {color}33;
                    border-radius:6px;padding:8px 10px;text-align:center;">
            <div style="font-size:1.2rem;">{flag}</div>
            <div style="font-family:'Barlow Condensed',sans-serif;font-size:0.85rem;
                        font-weight:600;color:{color};letter-spacing:1px;">{country}</div>
            <div style="font-family:'Source Code Pro',monospace;font-size:0.55rem;
                        color:#4a6a86;letter-spacing:1px;margin-top:2px;">{tier}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── News Intelligence Feed ──
st.markdown(
    '<div class="section-label">📡 &nbsp;实时情报监控 &nbsp;·&nbsp; REAL-TIME INTELLIGENCE FEED &nbsp;·&nbsp; AUTHORITY SOURCES ONLY</div>',
    unsafe_allow_html=True
)

MONITORS = [
    {
        "icon": "🏗️",
        "title": "大客户动态",
        "badge": "TENDER",
        "query": "Morocco OCP Group tender OR Dangote trucks",
    },
    {
        "icon": "🚛",
        "title": "竞品追踪",
        "badge": "COMPETITOR",
        "query": "Sinotruk Africa OR Volvo trucks Africa",
    },
    {
        "icon": "⚡",
        "title": "政策·新能源",
        "badge": "POLICY",
        "query": "Nigeria EV tariff OR Africa electric vehicle",
    },
    {
        "icon": "🔗",
        "title": "物流·基建",
        "badge": "LOGISTICS",
        "query": "South Africa logistics OR Transnet freight",
    },
]

cols = st.columns(4)
for col, m in zip(cols, MONITORS):
    render_news_column(col, m["icon"], m["title"], m["badge"], m["query"])

# ── Footer ──
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;font-family:'Source Code Pro',monospace;
            font-size:0.6rem;color:#1e3a50;letter-spacing:2px;
            border-top:1px solid rgba(0,200,240,0.06);padding-top:18px;line-height:2.2;">
    ◆ &nbsp;SEE AFRICA · COMMERCIAL VEHICLE INTELLIGENCE COMMAND CENTER &nbsp;◆<br>
    数据来源：Reuters · Bloomberg · FT · Engineering News · Gov Sources · Google News RSS<br>
    <span style="color:#152a3a;">INTERNAL USE ONLY · 仅供内部商业参考使用 · v2.0</span>
</div>
""", unsafe_allow_html=True)
