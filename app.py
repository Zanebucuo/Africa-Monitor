"""
See Africa – Commercial Vehicle Intelligence Command Center v3.0
非洲商用车战情情报室 · FULL REBUILD
"""

import streamlit as st
import feedparser
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="See Africa · CV Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS – 彻底修复排版 + BI 暗色主题
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@300;400;600;700&family=Source+Code+Pro:wght@400;600&family=Noto+Sans+SC:wght@300;400;700&display=swap');

/* ── 根变量 ── */
:root {
    --bg:       #05090f;
    --bg-card:  #0b1420;
    --bg-panel: #0f1d2e;
    --acc:      #00c8f0;
    --acc2:     #00e8a0;
    --acc3:     #ff6b35;
    --warn:     #ffd93d;
    --txt:      #cce0f0;
    --dim:      #4a6a86;
    --border:   rgba(0,200,240,0.15);
    --glow:     0 0 24px rgba(0,200,240,0.18);
}

/* ── 全局背景 ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main { background: var(--bg) !important; color: var(--txt); }

[data-testid="stSidebar"] {
    background: #060b14 !important;
    border-right: 1px solid var(--border);
}

/* ── Tabs 样式 ── */
[data-testid="stTabs"] { background: transparent; }
[data-testid="stTabsTabList"] {
    background: var(--bg-card) !important;
    border-bottom: 2px solid var(--border) !important;
    border-radius: 10px 10px 0 0;
    gap: 4px;
    padding: 6px 8px 0 8px;
}
button[data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    color: var(--dim) !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    padding: 10px 22px !important;
    border-radius: 8px 8px 0 0 !important;
    transition: all 0.2s !important;
}
button[data-baseweb="tab"]:hover {
    color: var(--acc) !important;
    background: rgba(0,200,240,0.06) !important;
}
button[aria-selected="true"][data-baseweb="tab"] {
    color: var(--acc) !important;
    background: rgba(0,200,240,0.1) !important;
    border-bottom: 2px solid var(--acc) !important;
}
[data-testid="stTabPanel"] {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-top: none;
    border-radius: 0 0 10px 10px;
    padding: 24px !important;
}

/* ── Metric 卡片 ── */
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 18px 20px !important;
    box-shadow: var(--glow) !important;
    position: relative; overflow: hidden;
}
[data-testid="metric-container"]::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--acc), var(--acc2));
}
[data-testid="stMetricLabel"] {
    font-family: 'Source Code Pro', monospace !important;
    font-size: 0.62rem !important; letter-spacing: 2px !important;
    color: var(--dim) !important; text-transform: uppercase;
}
[data-testid="stMetricValue"] {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 1.9rem !important; font-weight: 700 !important;
    color: var(--acc) !important; letter-spacing: 1px;
}

/* ── Hero Header ── */
.hero {
    background: linear-gradient(135deg, #0a1828 0%, #071020 50%, #0c2035 100%);
    border: 1px solid var(--border); border-radius: 12px;
    padding: 22px 36px; margin-bottom: 20px;
    position: relative; overflow: hidden;
    box-shadow: 0 0 40px rgba(0,200,240,0.2);
}
.hero::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--acc), var(--acc2), transparent);
}
.hero-brand {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2.8rem; font-weight: 700; letter-spacing: 8px;
    color: #fff; text-transform: uppercase; margin: 0; line-height: 1;
}
.hero-brand span { color: var(--acc); }
.hero-sub {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.65rem; color: var(--dim);
    letter-spacing: 3px; margin-top: 6px; text-transform: uppercase;
}
.hero-ts {
    position: absolute; right: 36px; top: 50%; transform: translateY(-50%);
    font-family: 'Source Code Pro', monospace;
    font-size: 0.68rem; color: var(--acc2); text-align: right; line-height: 1.9;
}
.dot {
    display: inline-block; width: 7px; height: 7px; border-radius: 50%;
    background: var(--acc2); box-shadow: 0 0 10px var(--acc2);
    margin-right: 6px; animation: blink 2s infinite;
}
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:.2;} }

/* ── Section label ── */
.slabel {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.72rem; font-weight: 600; letter-spacing: 4px;
    color: var(--acc); text-transform: uppercase;
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px; margin-bottom: 18px;
}

/* ── Chart card ── */
.chart-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 10px; padding: 20px; margin-bottom: 20px;
    box-shadow: var(--glow); position: relative; overflow: hidden;
}
.chart-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--acc), var(--acc2));
}
.chart-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1rem; font-weight: 700; letter-spacing: 2px;
    color: var(--acc2); text-transform: uppercase; margin-bottom: 4px;
}
.chart-sub {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.6rem; color: var(--dim); letter-spacing: 1px; margin-bottom: 14px;
}

/* ══ 新闻卡片 – 排版彻底修复 ══ */
.news-col-wrap {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-top: 2px solid var(--acc);
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 8px;
}
.news-col-hdr {
    background: linear-gradient(180deg, #0f1e32 0%, #091520 100%);
    padding: 12px 16px; border-bottom: 1px solid var(--border);
}
.news-col-hdr-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.95rem; font-weight: 700; letter-spacing: 2px;
    color: var(--acc2); text-transform: uppercase; margin: 0;
    /* 防止标题溢出 */
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.news-col-hdr-badge {
    display: inline-block;
    background: rgba(0,200,240,0.1); border: 1px solid rgba(0,200,240,0.25);
    border-radius: 3px; padding: 1px 7px;
    font-size: 0.55rem; color: var(--acc);
    font-family: 'Source Code Pro', monospace; letter-spacing: 1.5px;
    margin-top: 5px;
}
.news-item {
    padding: 12px 16px;
    border-bottom: 1px solid rgba(0,200,240,0.07);
    transition: background 0.2s;
}
.news-item:last-child { border-bottom: none; }
.news-item:hover { background: rgba(0,200,240,0.04); }

/* ★ 核心修复：强制换行，禁止溢出 ★ */
.news-item-title {
    font-family: 'Noto Sans SC', sans-serif;
    font-size: 0.82rem; font-weight: 600; line-height: 1.55;
    color: var(--txt);
    /* 强制自动换行 */
    word-wrap: break-word;
    overflow-wrap: break-word;
    word-break: break-word;
    white-space: normal;
    display: block;
    text-decoration: none;
}
.news-item-title:hover { color: var(--acc); }
.news-item-meta {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.58rem; color: var(--dim);
    margin-top: 5px;
    /* meta 也强制换行 */
    word-wrap: break-word; overflow-wrap: break-word;
    white-space: normal;
}
.news-empty {
    padding: 24px 16px; text-align: center;
    font-family: 'Source Code Pro', monospace;
    font-size: 0.68rem; color: var(--dim); line-height: 2;
}

/* ── Map container ── */
.map-wrap {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; overflow: hidden; box-shadow: var(--glow);
    position: relative;
}
.map-wrap::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--acc), var(--acc2), transparent);
    z-index: 10;
}

/* ── Sidebar ── */
.sb-section {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.7rem; font-weight: 600; letter-spacing: 3px;
    color: var(--acc); text-transform: uppercase;
    margin: 18px 0 7px 0;
    border-bottom: 1px solid var(--border); padding-bottom: 4px;
}
.sb-link {
    display: block; padding: 8px 12px; margin: 3px 0;
    background: rgba(0,200,240,0.03); border: 1px solid rgba(0,200,240,0.08);
    border-radius: 6px; font-size: 0.78rem; color: var(--txt) !important;
    text-decoration: none !important;
    font-family: 'Noto Sans SC', sans-serif; transition: all 0.2s;
    /* 防止侧边栏链接文字溢出 */
    word-wrap: break-word; overflow-wrap: break-word; white-space: normal;
}
.sb-link:hover {
    background: rgba(0,200,240,0.1); border-color: var(--acc);
    color: var(--acc) !important; padding-left: 16px;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding-top: 1.2rem !important; }

/* ── Plotly 图表背景透明 ── */
.js-plotly-plot .plotly, .js-plotly-plot .plotly .plot-container {
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PLOTLY CHART THEME – 全局暗色风格
# ══════════════════════════════════════════════════════════════════════════════
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Barlow Condensed, Source Code Pro, sans-serif",
              color="#cce0f0", size=12),
    legend=dict(
        bgcolor="rgba(11,20,32,0.85)",
        bordercolor="rgba(0,200,240,0.2)",
        borderwidth=1,
        font=dict(size=11, color="#cce0f0"),
    ),
    xaxis=dict(
        gridcolor="rgba(0,200,240,0.08)",
        linecolor="rgba(0,200,240,0.2)",
        tickfont=dict(size=10, color="#4a6a86"),
        title_font=dict(size=11, color="#4a6a86"),
    ),
    yaxis=dict(
        gridcolor="rgba(0,200,240,0.08)",
        linecolor="rgba(0,200,240,0.2)",
        tickfont=dict(size=10, color="#4a6a86"),
        title_font=dict(size=11, color="#4a6a86"),
    ),
    margin=dict(l=48, r=20, t=20, b=48),
    hoverlabel=dict(
        bgcolor="#0b1828", bordercolor="#00c8f0",
        font=dict(family="Noto Sans SC, Source Code Pro", size=12, color="#cce0f0"),
    ),
)


# ══════════════════════════════════════════════════════════════════════════════
# SIMULATED BUSINESS DATA（模拟数据，时间线至 2026）
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def get_za_hcv_data() -> pd.DataFrame:
    """南非重型商用车月度销量 2025-01 至 2026-05"""
    np.random.seed(42)
    months = pd.date_range("2025-01-01", "2026-05-01", freq="MS")
    n = len(months)
    # ICE：基本盘 + 轻微下滑趋势 + 季节性
    ice_base = np.linspace(3200, 2850, n)
    ice_seasonal = 180 * np.sin(np.linspace(0, 2.5 * np.pi, n))
    ice = (ice_base + ice_seasonal + np.random.normal(0, 60, n)).astype(int).clip(min=800)
    # EV：从低基数指数上升
    ev_base = np.linspace(120, 680, n)
    ev = (ev_base + np.random.normal(0, 30, n)).astype(int).clip(min=0)
    return pd.DataFrame({"月份": months, "ICE 传统燃油": ice, "EV 纯电动": ev})


@st.cache_data
def get_ng_brand_share() -> pd.DataFrame:
    """尼日利亚 2026 Q1 重卡品牌市场份额"""
    data = {
        "品牌": ["Sinotruk\n中国重汽", "FAW\n一汽", "Foton\n福田", "Volvo", "Scania", "MAN", "Mercedes\nActros", "Others"],
        "销量": [1840, 1420, 980, 560, 410, 320, 275, 390],
        "国家": ["中国", "中国", "中国", "瑞典", "瑞典", "德国", "德国", "其他"],
    }
    df = pd.DataFrame(data)
    df["份额%"] = (df["销量"] / df["销量"].sum() * 100).round(1)
    return df


@st.cache_data
def get_ocp_throughput() -> pd.DataFrame:
    """摩洛哥 OCP 及矿业集团公路运输吞吐量 2023-2026"""
    months = pd.date_range("2023-01-01", "2026-05-01", freq="MS")
    np.random.seed(7)
    n = len(months)
    trend = np.linspace(820, 1380, n)
    seasonal = 90 * np.sin(np.linspace(0, 6.5 * np.pi, n))
    noise = np.random.normal(0, 35, n)
    throughput = (trend + seasonal + noise).clip(min=500)
    return pd.DataFrame({"月份": months, "吞吐量(千吨)": throughput.round(1)})


# ══════════════════════════════════════════════════════════════════════════════
# AFRICA MAP DATA
# ══════════════════════════════════════════════════════════════════════════════
MARKET_DATA = {
    "Morocco":       {"iso":"MAR","score":95,"tier":"战略核心","lines":["🏷 纯电关税：2.5%","⛽ 柴油：13.5 MAD/L","🚛 年需求：~18,000辆","🏭 OCP磷酸盐物流主力","📋 UN-ECE R49认证"]},
    "Nigeria":       {"iso":"NGA","score":92,"tier":"战略核心","lines":["🏷 纯电关税：0%（2023免税）","🔧 KD散件：0%","🚛 年需求：~45,000辆","🏗 Dangote最大采购方","📋 SON强制认证"]},
    "South Africa":  {"iso":"ZAF","score":88,"tier":"战略核心","lines":["🏷 进口关税：25%","⛽ 柴油：21.6 ZAR/L","🚛 年需求：~30,000辆","🚂 Transnet核心买家","📋 NRCS强制认证"]},
    "Egypt":         {"iso":"EGY","score":78,"tier":"战略新兴","lines":["🏷 CBU整车关税：40%","🔧 KD组装（国产化>40%）：5%","🚛 年需求：~25,000辆","🏗 苏伊士经济区物流","📋 EOS埃及标准局"]},
    "Tunisia":       {"iso":"TUN","score":72,"tier":"战略新兴","lines":["🏷 进口关税：10%（欧盟协定）","⛽ 柴油：2.1 TND/L（补贴价）","🚛 年需求：~8,000辆","🌐 欧非走廊枢纽","📋 INNORPI技术标准"]},
    "Rwanda":        {"iso":"RWA","score":65,"tier":"战略新兴","lines":["🏷 进口关税：0%（EAC协议）","⛽ 柴油：1,650 RWF/L","🚛 年需求：~3,500辆（高速增长）","🌿 2035禁售燃油车","📋 RSB卢旺达标准局"]},
}

ALL_AFRICA_ISO = [
    "DZA","AGO","BEN","BWA","BFA","BDI","CPV","CMR","CAF","TCD",
    "COM","COD","COG","CIV","DJI","EGY","GNQ","ERI","SWZ","ETH",
    "GAB","GMB","GHA","GIN","GNB","KEN","LSO","LBR","LBY","MDG",
    "MWI","MLI","MRT","MUS","MAR","MOZ","NAM","NER","NGA","RWA",
    "STP","SEN","SLE","SOM","ZAF","SSD","SDN","TZA","TGO","TUN",
    "UGA","ZMB","ZWE",
]


# ══════════════════════════════════════════════════════════════════════════════
# NEWS FETCHER – 时间强制过滤 + 权威来源
# ══════════════════════════════════════════════════════════════════════════════
TRUSTED = (
    "site:reuters.com OR site:bloomberg.com OR site:ft.com "
    "OR site:engineeringnews.co.za OR site:businessday.ng "
    "OR site:zawya.com OR site:afdb.org OR site:gov.ma OR site:customs.gov.ng"
)
NOISE = {"rumor","rumour","unconfirmed","alleged","shocking","viral","leaked","clickbait"}

@st.cache_data(ttl=1800)   # 30 分钟缓存
def fetch_news(query: str, limit: int = 5) -> list:
    # ★ when:30d 强制只取近 30 天
    full_q = f"({query}) ({TRUSTED}) when:30d"
    encoded = full_q.replace(" ", "+").replace('"', "%22")
    url = (
        f"https://news.google.com/rss/search"
        f"?q={encoded}&hl=en-US&gl=US&ceid=US:en"
    )
    now = datetime.utcnow()
    cutoff = now - timedelta(days=30)   # 二次校验：30 天内
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries:
            if len(items) >= limit:
                break
            title = entry.get("title", "")
            if any(n in title.lower() for n in NOISE):
                continue
            # 解析发布时间
            pub_str = "–"
            pub_dt  = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                pub_dt = datetime(*entry.published_parsed[:6])
                pub_str = pub_dt.strftime("%Y-%m-%d %H:%M")
            # ★ 时间二次过滤：剔除 30 天前的文章
            if pub_dt and pub_dt < cutoff:
                continue
            items.append({
                "title":     title or "No title",
                "link":      entry.get("link", "#"),
                "published": pub_str,
                "pub_dt":    pub_dt,
                "source":    entry.get("source", {}).get("title", "–"),
            })
        # ★ 按时间倒序排列
        items.sort(key=lambda x: x["pub_dt"] or datetime.min, reverse=True)
        return items
    except Exception:
        return []


def render_news_col(col, icon: str, title: str, badge: str, query: str):
    with col:
        st.markdown(f"""
        <div class="news-col-wrap">
          <div class="news-col-hdr">
            <div class="news-col-hdr-title">{icon} &nbsp;{title}</div>
            <span class="news-col-hdr-badge">{badge} · 近30天 · 权威来源</span>
          </div>
        """, unsafe_allow_html=True)

        with st.spinner(""):
            news = fetch_news(query)

        if not news:
            st.markdown("""
            <div class="news-empty">
              ⚠ 权威来源暂无近期结果<br>
              <span style="font-size:.58rem;">No recent results from authority sources</span>
            </div>""", unsafe_allow_html=True)
        else:
            for item in news:
                st.markdown(f"""
                <div class="news-item">
                  <a class="news-item-title"
                     href="{item['link']}" target="_blank">{item['title']}</a>
                  <div class="news-item-meta">
                    🕐 {item['published']} &nbsp;·&nbsp; 📰 {item['source']}
                  </div>
                </div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CHART BUILDERS
# ══════════════════════════════════════════════════════════════════════════════

def chart_za_hcv(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["月份"], y=df["ICE 传统燃油"],
        name="ICE 传统燃油",
        mode="lines+markers",
        line=dict(color="#00c8f0", width=2.5),
        marker=dict(size=5, color="#00c8f0"),
        fill="tozeroy",
        fillcolor="rgba(0,200,240,0.07)",
        hovertemplate="<b>%{x|%Y-%m}</b><br>ICE销量: <b>%{y:,}</b> 辆<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df["月份"], y=df["EV 纯电动"],
        name="EV 纯电动",
        mode="lines+markers",
        line=dict(color="#00e8a0", width=2.5, dash="solid"),
        marker=dict(size=6, color="#00e8a0", symbol="diamond"),
        fill="tozeroy",
        fillcolor="rgba(0,232,160,0.1)",
        hovertemplate="<b>%{x|%Y-%m}</b><br>EV销量: <b>%{y:,}</b> 辆<extra></extra>",
    ))
    # 标注 EV 关键时间点
    fig.add_annotation(
        x="2026-01-01", y=df[df["月份"]=="2026-01-01"]["EV 纯电动"].values[0] if not df[df["月份"]=="2026-01-01"].empty else 450,
        text="▲ 2026 EV加速渗透",
        showarrow=True, arrowhead=2, arrowcolor="#00e8a0",
        font=dict(size=10, color="#00e8a0"), ax=40, ay=-35,
    )
    layout = dict(**CHART_LAYOUT)
    layout["xaxis"]["title"] = "月份"
    layout["yaxis"]["title"] = "销量（辆）"
    layout["legend"]["orientation"] = "h"
    layout["legend"]["y"] = -0.18
    fig.update_layout(**layout)
    return fig


def chart_ng_brand(df: pd.DataFrame) -> go.Figure:
    colors = [
        "#00c8f0","#00a8cc","#0088a8",  # 中国品牌
        "#00e8a0","#00c080",             # 北欧品牌
        "#ffd93d","#ffb820",             # 欧洲品牌
        "#4a6a86",                        # 其他
    ]
    fig = go.Figure(go.Bar(
        x=df["品牌"],
        y=df["销量"],
        text=[f"{v:,}辆<br>{s}%" for v, s in zip(df["销量"], df["份额%"])],
        textposition="outside",
        textfont=dict(size=11, color="#cce0f0"),
        marker=dict(
            color=colors[:len(df)],
            line=dict(color="rgba(0,200,240,0.3)", width=1),
        ),
        hovertemplate="<b>%{x}</b><br>销量: <b>%{y:,}</b> 辆<br>市场份额: <b>%{text}</b><extra></extra>",
        customdata=df["份额%"],
    ))
    layout = dict(**CHART_LAYOUT)
    layout["xaxis"]["title"] = "品牌"
    layout["yaxis"]["title"] = "Q1销量（辆）"
    layout["yaxis"]["range"] = [0, df["销量"].max() * 1.22]
    layout["showlegend"] = False
    layout["bargap"] = 0.35
    fig.update_layout(**layout)
    # 中国品牌占比标注
    cn_share = df[df["国家"]=="中国"]["份额%"].sum()
    fig.add_annotation(
        text=f"🇨🇳 中国品牌合计: {cn_share:.1f}% 市场份额",
        xref="paper", yref="paper", x=0.98, y=0.97,
        showarrow=False,
        bgcolor="rgba(0,200,240,0.1)", bordercolor="rgba(0,200,240,0.3)",
        borderwidth=1, borderpad=6,
        font=dict(size=10, color="#00c8f0"),
    )
    return fig


def chart_ocp_area(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["月份"], y=df["吞吐量(千吨)"],
        name="公路运输吞吐量",
        mode="lines",
        line=dict(color="#ff6b35", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(255,107,53,0.12)",
        hovertemplate="<b>%{x|%Y-%m}</b><br>吞吐量: <b>%{y:.0f}</b> 千吨<extra></extra>",
    ))
    # 趋势线
    x_num = np.arange(len(df))
    z = np.polyfit(x_num, df["吞吐量(千吨)"], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=df["月份"], y=p(x_num),
        name="增长趋势线",
        mode="lines",
        line=dict(color="#ffd93d", width=1.5, dash="dot"),
        hovertemplate="趋势: <b>%{y:.0f}</b> 千吨<extra></extra>",
    ))
    # 计算增长率
    growth = (df["吞吐量(千吨)"].iloc[-1] / df["吞吐量(千吨)"].iloc[0] - 1) * 100
    fig.add_annotation(
        text=f"↑ 3年累计增长 {growth:.1f}%",
        xref="paper", yref="paper", x=0.02, y=0.95,
        showarrow=False,
        bgcolor="rgba(255,107,53,0.15)", bordercolor="rgba(255,107,53,0.4)",
        borderwidth=1, borderpad=6,
        font=dict(size=11, color="#ff6b35"),
    )
    layout = dict(**CHART_LAYOUT)
    layout["xaxis"]["title"] = "月份"
    layout["yaxis"]["title"] = "吞吐量（千吨）"
    layout["legend"]["orientation"] = "h"
    layout["legend"]["y"] = -0.18
    fig.update_layout(**layout)
    return fig


def build_africa_map() -> go.Figure:
    rows = []
    for iso in ALL_AFRICA_ISO:
        matched = next(((c, d) for c, d in MARKET_DATA.items() if d["iso"] == iso), None)
        if matched:
            name, d = matched
            tip = (f"<b style='color:#00e8a0;font-size:13px;'>★ {name}</b><br>"
                   f"<span style='color:#4a8fa8;font-size:10px;letter-spacing:2px;'>{d['tier']}</span><br><br>"
                   + "<br>".join(d["lines"]))
            rows.append({"iso": iso, "score": d["score"], "tooltip": tip, "hl": 1})
        else:
            rows.append({"iso": iso, "score": 12, "tooltip": f"<b>{iso}</b><br><span style='color:#4a6a86;'>暂无覆盖计划</span>", "hl": 0})
    df = pd.DataFrame(rows)

    fig = go.Figure()
    # 底层（暗色）
    fig.add_trace(go.Choropleth(
        locations=df[df.hl==0]["iso"], z=df[df.hl==0]["score"],
        text=df[df.hl==0]["tooltip"], hovertemplate="%{text}<extra></extra>",
        colorscale=[[0,"#0a1a28"],[1,"#152a40"]], showscale=False,
        marker_line_color="rgba(0,200,240,0.12)", marker_line_width=0.5,
        zmin=0, zmax=100,
    ))
    # 高亮层
    fig.add_trace(go.Choropleth(
        locations=df[df.hl==1]["iso"], z=df[df.hl==1]["score"],
        text=df[df.hl==1]["tooltip"], hovertemplate="%{text}<extra></extra>",
        colorscale=[[0,"#0d3a5c"],[0.4,"#0a6090"],[0.7,"#00a0d0"],[1.0,"#00c8f0"]],
        showscale=True,
        colorbar=dict(
            title=dict(text="战略优先级", font=dict(color="#4a6a86", size=9, family="Source Code Pro")),
            tickfont=dict(color="#4a6a86", size=8), bgcolor="rgba(5,9,15,0.8)",
            bordercolor="rgba(0,200,240,0.2)", borderwidth=1,
            thickness=8, len=0.45, x=0.98,
        ),
        marker_line_color="rgba(0,200,240,0.45)", marker_line_width=1.2,
        zmin=0, zmax=100,
    ))
    fig.update_layout(
        geo=dict(
            scope="africa", showframe=False,
            showcoastlines=True, coastlinecolor="rgba(0,200,240,0.18)", coastlinewidth=0.7,
            showland=True, landcolor="#080e18",
            showocean=True, oceancolor="#030710",
            showcountries=True, countrycolor="rgba(0,200,240,0.1)", countrywidth=0.4,
            bgcolor="#05090f", projection_type="natural earth",
        ),
        paper_bgcolor="#05090f", plot_bgcolor="#05090f",
        margin=dict(l=0, r=55, t=8, b=0), height=500,
        hoverlabel=dict(
            bgcolor="#0b1828", bordercolor="#00c8f0",
            font=dict(family="Noto Sans SC, Source Code Pro", size=12, color="#cce0f0"),
        ),
        dragmode=False,
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Barlow Condensed',sans-serif;font-size:1.25rem;font-weight:700;
                color:#00c8f0;letter-spacing:4px;padding:10px 0 4px 0;
                border-bottom:1px solid rgba(0,200,240,0.18);">
        🛰️ &nbsp;INTEL HUB
    </div>
    <div style="font-family:'Source Code Pro',monospace;font-size:0.57rem;
                color:#4a6a86;letter-spacing:2px;margin:4px 0 14px 0;">
        工具 & 资源链接中心
    </div>
    """, unsafe_allow_html=True)

    for section, links in [
        ("🇳🇬 Nigeria", [
            ("🏛️ 尼日利亚海关总署", "https://www.customs.gov.ng"),
            ("🏦 Central Bank of Nigeria", "https://www.cbn.gov.ng/rates/exchratebycurrency.asp"),
            ("🚛 NARTO 公路运输协会", "https://www.narto.com.ng"),
            ("🏗️ Dangote Group", "https://www.dangote.com"),
        ]),
        ("🇿🇦 South Africa", [
            ("🚗 AutoTrader ZA – Trucks", "https://www.autotrader.co.za/trucks"),
            ("🚂 Transnet Freight Rail", "https://www.transnet.net"),
            ("📈 SARB 兰特汇率", "https://www.resbank.co.za"),
            ("🏭 NAAMSA 汽车协会", "https://www.naamsa.co.za"),
        ]),
        ("🇲🇦 Morocco", [
            ("🤝 AIVAM 汽车进口商协会", "https://www.aivam.ma"),
            ("🌾 OCP Group", "https://www.ocpgroup.ma"),
            ("🛃 摩洛哥海关总署", "https://www.douane.gov.ma"),
            ("⛽ ONHYM 能源监管", "https://www.onhym.com"),
        ]),
        ("🇪🇬 🇹🇳 🇷🇼 新兴市场", [
            ("🏛️ 埃及工业部 MoTI", "https://www.moti.gov.eg"),
            ("📋 EOS 埃及标准局", "https://www.eos.org.eg"),
            ("🇹🇳 INNORPI 突尼斯标准", "https://www.innorpi.tn"),
            ("🇷🇼 RSB 卢旺达标准局", "https://www.rsb.gov.rw"),
        ]),
        ("🌐 行业情报", [
            ("📡 Engineering News ZA", "https://www.engineeringnews.co.za"),
            ("🚛 Truck & Freight Africa", "https://www.trucksandfreight.co.za"),
            ("🌍 AfDB 非洲开发银行", "https://www.afdb.org"),
            ("📊 Zawya 中东非洲财经", "https://www.zawya.com"),
            ("📰 African Business Magazine", "https://african.business"),
        ]),
    ]:
        st.markdown(f'<div class="sb-section">{section}</div>', unsafe_allow_html=True)
        for label, url in links:
            st.markdown(f'<a class="sb-link" href="{url}" target="_blank">{label}</a>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄  刷新全部情报", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.markdown("""
    <div style="font-family:'Source Code Pro',monospace;font-size:0.56rem;
                color:#1e3a50;text-align:center;margin-top:16px;line-height:2.2;">
        SEE AFRICA · CV INTEL v3.0<br>情报数据每30分钟刷新<br>仅供内部商业参考使用
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════════

# ── Hero ──
now_str = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
st.markdown(f"""
<div class="hero">
  <div class="hero-brand">SEE <span>AFRICA</span></div>
  <div class="hero-sub">
    ◆ &nbsp;Commercial Vehicle Intelligence Command Center &nbsp;◆ &nbsp;非洲商用车战情情报室 · v3.0
  </div>
  <div class="hero-ts">
    <div><span class="dot"></span>LIVE &nbsp;·&nbsp; ALL SYSTEMS NOMINAL</div>
    <div>{now_str} CST</div>
    <div style="color:#4a6a86;font-size:.58rem;">6 MARKETS · 3 MODULES · 30min REFRESH</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ──
st.markdown('<div class="slabel">📊 &nbsp;核心市场指标 &nbsp;·&nbsp; KEY MARKET INDICATORS</div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("🇳🇬 尼日利亚纯电关税", "0 %", "✦ 免税 · 2023起", help="Nigeria EV import tariff – zero-rated")
with c2:
    st.metric("🇲🇦 摩洛哥柴油均价", "13.5 MAD", "≈ $1.34/L", delta_color="inverse", help="Morocco avg diesel retail price")
with c3:
    st.metric("🇿🇦 南非 HCV 月销", "~3,100 辆", "▼ YoY -4.2%", delta_color="inverse", help="South Africa HCV monthly sales est.")
with c4:
    st.metric("🇪🇬 埃及 KD 关税", "5 %", "国产化率>40%", help="Egypt KD assembly preferential tariff")
with c5:
    st.metric("🌍 非洲CV市场规模", "$8.4B", "▲ CAGR 6.8%", help="Africa commercial vehicle market size 2025 est.")

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS – 三大板块
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs([
    "📈  市场与销量数据",
    "📡  实时情报雷达",
    "🌍  宏观与地图",
])


# ──────────────────────────────────────────────────────────────────────────────
# TAB 1 · 市场与销量数据
# ──────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="slabel">📈 &nbsp;深度市场数据 &nbsp;·&nbsp; DEEP MARKET ANALYTICS · 模拟数据仅供参考</div>', unsafe_allow_html=True)

    # ── Chart 1: 南非 HCV 折线图 ──
    st.markdown("""
    <div class="chart-card">
      <div class="chart-title">📊 南非重型商用车月度销量走势 &nbsp;2025–2026</div>
      <div class="chart-sub">SOUTH AFRICA HCV MONTHLY SALES · ICE vs EV · SIMULATED DATA</div>
    </div>
    """, unsafe_allow_html=True)

    za_df = get_za_hcv_data()
    col_l, col_r = st.columns([3, 1])
    with col_l:
        st.plotly_chart(chart_za_hcv(za_df), use_container_width=True, config={"displayModeBar": False})
    with col_r:
        latest = za_df.iloc[-1]
        ev_share = latest["EV 纯电动"] / (latest["ICE 传统燃油"] + latest["EV 纯电动"]) * 100
        st.metric("最新月 ICE 销量", f"{latest['ICE 传统燃油']:,} 辆")
        st.metric("最新月 EV 销量", f"{latest['EV 纯电动']:,} 辆", f"渗透率 {ev_share:.1f}%")
        total_ev = za_df["EV 纯电动"].sum()
        st.metric("统计期 EV 合计", f"{total_ev:,} 辆")
        with st.expander("📌 数据说明"):
            st.markdown("""
            - 统计周期：2025-01 至 2026-05
            - HCV 定义：GVW > 16吨
            - EV 含燃料电池商用车
            - 数据来源：NAAMSA 模拟
            """)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chart 2: 尼日利亚品牌份额条形图 ──
    st.markdown("""
    <div class="chart-card">
      <div class="chart-title">🏆 尼日利亚 2026 Q1 重卡品牌市场份额</div>
      <div class="chart-sub">NIGERIA 2026 Q1 HEAVY TRUCK BRAND MARKET SHARE · SIMULATED DATA</div>
    </div>
    """, unsafe_allow_html=True)

    ng_df = get_ng_brand_share()
    col_l2, col_r2 = st.columns([3, 1])
    with col_l2:
        st.plotly_chart(chart_ng_brand(ng_df), use_container_width=True, config={"displayModeBar": False})
    with col_r2:
        st.markdown("**🏅 Top 3 品牌**")
        top3 = ng_df.nlargest(3, "销量")
        for _, row in top3.iterrows():
            brand_name = row['品牌'].replace('\n', ' ')
            st.metric(brand_name, f"{row['销量']:,} 辆", f"{row['份额%']}%")
        with st.expander("📌 数据说明"):
            st.markdown("""
            - 统计周期：2026 Q1
            - 含 Lagos + Kano 核心市场
            - KD组装 + CBU 进口合并计
            - 数据来源：NARTO 模拟
            """)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chart 3: 摩洛哥 OCP 面积图 ──
    st.markdown("""
    <div class="chart-card">
      <div class="chart-title">⛏️ 摩洛哥矿业集团公路运输吞吐量 &nbsp;2023–2026</div>
      <div class="chart-sub">MOROCCO OCP GROUP ROAD FREIGHT THROUGHPUT TREND · SIMULATED DATA</div>
    </div>
    """, unsafe_allow_html=True)

    ocp_df = get_ocp_throughput()
    col_l3, col_r3 = st.columns([3, 1])
    with col_l3:
        st.plotly_chart(chart_ocp_area(ocp_df), use_container_width=True, config={"displayModeBar": False})
    with col_r3:
        latest_ocp = ocp_df.iloc[-1]["吞吐量(千吨)"]
        first_ocp  = ocp_df.iloc[0]["吞吐量(千吨)"]
        growth_pct = (latest_ocp / first_ocp - 1) * 100
        st.metric("最新月吞吐量", f"{latest_ocp:.0f} 千吨")
        st.metric("3年累计增长", f"+{growth_pct:.1f}%", "强劲增长趋势")
        peak = ocp_df["吞吐量(千吨)"].max()
        st.metric("历史峰值", f"{peak:.0f} 千吨")
        with st.expander("📌 数据说明"):
            st.markdown("""
            - OCP Group 磷酸盐运输为主
            - 含 Khouribga → Jorf Lasfar 走廊
            - 吞吐量单位：千公吨
            - 数据来源：OCP IR 模拟
            """)


# ──────────────────────────────────────────────────────────────────────────────
# TAB 2 · 实时情报雷达
# ──────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown(
        '<div class="slabel">📡 &nbsp;实时情报监控 &nbsp;·&nbsp; AUTHORITY SOURCES ONLY &nbsp;·&nbsp; 近30天 &nbsp;·&nbsp; 自动过滤噪声</div>',
        unsafe_allow_html=True
    )
    st.info(
        "📌 情报来源限定：Reuters · Bloomberg · FT · Engineering News · BusinessDay · Zawya · AfDB · 政府官网  |  "
        "每30分钟自动刷新  |  仅显示近30天内容  |  按时间倒序排列",
        icon="🛡️"
    )

    MONITORS = [
        {"icon": "🏗️", "title": "大客户动态",  "badge": "TENDER",     "query": "Morocco OCP Group tender OR Dangote trucks"},
        {"icon": "🚛",  "title": "竞品追踪",    "badge": "COMPETITOR", "query": "Sinotruk Africa OR Volvo trucks Africa"},
        {"icon": "⚡",  "title": "政策·新能源", "badge": "POLICY",     "query": "Nigeria EV tariff OR Africa electric vehicle policy"},
        {"icon": "🔗",  "title": "物流·基建",   "badge": "LOGISTICS",  "query": "South Africa logistics OR Transnet freight rail"},
    ]
    cols = st.columns(4, gap="medium")
    for col, m in zip(cols, MONITORS):
        render_news_col(col, m["icon"], m["title"], m["badge"], m["query"])


# ──────────────────────────────────────────────────────────────────────────────
# TAB 3 · 宏观与地图
# ──────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="slabel">🌍 &nbsp;非洲战略地图 &nbsp;·&nbsp; AFRICA STRATEGIC MARKET MAP</div>', unsafe_allow_html=True)

    st.markdown('<div class="map-wrap">', unsafe_allow_html=True)
    st.plotly_chart(
        build_africa_map(), use_container_width=True,
        config={"displayModeBar": False, "scrollZoom": False}
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 国家图例卡
    legend_cols = st.columns(6)
    for col, (flag, country, tier, iso) in zip(legend_cols, [
        ("🇲🇦", "摩洛哥", "战略核心", "MAR"),
        ("🇳🇬", "尼日利亚", "战略核心", "NGA"),
        ("🇿🇦", "南非", "战略核心", "ZAF"),
        ("🇪🇬", "埃及", "战略新兴", "EGY"),
        ("🇹🇳", "突尼斯", "战略新兴", "TUN"),
        ("🇷🇼", "卢旺达", "战略新兴", "RWA"),
    ]):
        color = "#00c8f0" if tier == "战略核心" else "#00e8a0"
        score = MARKET_DATA.get(next((k for k, v in MARKET_DATA.items() if v["iso"]==iso), ""), {}).get("score", "–")
        with col:
            st.markdown(f"""
            <div style="background:rgba(0,200,240,0.04);border:1px solid {color}40;
                        border-top:2px solid {color};border-radius:8px;
                        padding:12px 10px;text-align:center;">
              <div style="font-size:1.5rem;">{flag}</div>
              <div style="font-family:'Barlow Condensed',sans-serif;font-size:.95rem;
                          font-weight:700;color:{color};letter-spacing:1px;margin-top:4px;">{country}</div>
              <div style="font-family:'Source Code Pro',monospace;font-size:.55rem;
                          color:#4a6a86;letter-spacing:1px;margin-top:3px;">{tier}</div>
              <div style="font-family:'Barlow Condensed',sans-serif;font-size:1.1rem;
                          font-weight:700;color:{color};margin-top:6px;">
                  优先级 {score}/100
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 宏观环境说明
    st.markdown('<div class="slabel">📋 &nbsp;宏观政策环境速览</div>', unsafe_allow_html=True)
    macro_c1, macro_c2 = st.columns(2)
    with macro_c1:
        with st.expander("🇳🇬 尼日利亚 – 政策与市场环境", expanded=True):
            st.markdown("""
            - **关税政策**：纯电动商用车进口关税 **0%**（2023年起，5年有效期）
            - **KD政策**：散件组装享受 0% 关税，鼓励本地制造
            - **市场规模**：年均约 45,000 辆重型商用车需求，非洲第一大市场
            - **主要买家**：Dangote Cement、BUA Group、NNPC 物流部门
            - **风险提示**：奈拉汇率大幅波动，建议美元结算或锁汇操作
            - **认证要求**：SON 强制认证 + NAFDAC（特种车辆）
            """)
        with st.expander("🇿🇦 南非 – 政策与市场环境"):
            st.markdown("""
            - **关税政策**：商用车整车进口税率 25%，AGOA 框架内美国品牌优惠
            - **市场特点**：规范化程度最高，欧标排放要求（Euro 5 等效）
            - **主要买家**：Transnet、Imperial Logistics、Tiger Brands 物流
            - **EV 趋势**：政府 2030 年绿色交通路线图，EV 补贴政策酝酿中
            - **认证要求**：NRCS（南非国家规范委员会）强制 LOA
            - **汇率参考**：1 USD ≈ 18.5 ZAR（2025 年均值）
            """)
    with macro_c2:
        with st.expander("🇲🇦 摩洛哥 – 政策与市场环境", expanded=True):
            st.markdown("""
            - **关税政策**：商用车整车关税 2.5%（欧盟 AA 协议），电动车同等待遇
            - **市场亮点**：OCP 磷酸盐集团年采购重卡 800+ 辆，稳定大客户
            - **基建红利**：卡萨布兰卡–丹吉尔高速走廊建成，物流需求激增
            - **认证要求**：UN-ECE 认证体系（与欧盟互认），门槛相对低
            - **柴油价格**：13.5 MAD/L（约 $1.34），政府部分补贴
            - **战略价值**：欧-非贸易走廊核心枢纽，辐射西非市场
            """)
        with st.expander("🇪🇬 🇹🇳 🇷🇼 – 新兴市场速览"):
            st.markdown("""
            **埃及 🇪🇬**
            - CBU 整车关税 40%，强烈建议寻找本地 KD 合作伙伴
            - KD 组装（国产化率>40%）享受 5% 优惠税率
            - 苏伊士经济区建设拉动大量工程车需求

            **突尼斯 🇹🇳**
            - 欧盟联系国协议，关税 10%，认证与欧标互认
            - 体量较小但采购决策效率高，适合高端品牌切入

            **卢旺达 🇷🇼**
            - EAC 东非共同体内关税 0%，最佳营商环境 Top 3
            - 2035 年禁售燃油商用车路线图，EV 先发优势窗口期
            """)


# ── Footer ──
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;font-family:'Source Code Pro',monospace;
            font-size:0.58rem;color:#1a3248;letter-spacing:2px;
            border-top:1px solid rgba(0,200,240,0.06);padding-top:16px;line-height:2.4;">
  ◆ &nbsp;SEE AFRICA &nbsp;·&nbsp; COMMERCIAL VEHICLE INTELLIGENCE COMMAND CENTER &nbsp;·&nbsp; v3.0 &nbsp;◆<br>
  情报来源：Reuters · Bloomberg · FT · Engineering News ZA · BusinessDay NG · Zawya · AfDB · Gov Sources<br>
  <span style="color:#0f2030;">图表数据为模拟数据，仅供战略参考 &nbsp;·&nbsp; INTERNAL USE ONLY &nbsp;·&nbsp; 情报每30分钟自动刷新</span>
</div>
""", unsafe_allow_html=True)
