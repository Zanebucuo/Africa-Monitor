"""
Africa Commercial Vehicle Market Intelligence
PwC-style BI Dashboard · v4.0
"""

import streamlit as st
import feedparser
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ══════════════════════════════════════════════════════════════════════════════
# 0. PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Africa CV Market Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# 1. GLOBAL CSS — PwC Clean Light Style
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Reset & Base ── */
:root {
    --bg:          #F4F5F7;
    --white:       #FFFFFF;
    --pwc-orange:  #D04A02;
    --pwc-orange2: #EB6C2D;
    --pwc-navy:    #21325B;
    --pwc-blue:    #295BA5;
    --txt-main:    #2D3142;
    --txt-mid:     #5A6070;
    --txt-dim:     #9BA3B2;
    --border:      #E2E5EB;
    --shadow:      0 1px 4px rgba(0,0,0,0.07), 0 4px 16px rgba(0,0,0,0.05);
    --shadow-hover: 0 4px 16px rgba(0,0,0,0.12);
    --radius:      8px;
    --accent:      var(--pwc-orange);
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
    background: var(--bg) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--txt-main);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--pwc-navy) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: #E8ECF4 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.12) !important; }
[data-testid="stSidebar"] .stButton button {
    background: var(--pwc-orange) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: var(--pwc-orange2) !important;
}

/* ── Tabs ── */
[data-testid="stTabsTabList"] {
    background: var(--white) !important;
    border-bottom: 2px solid var(--border) !important;
    border-radius: var(--radius) var(--radius) 0 0;
    padding: 0 8px;
    gap: 0;
    box-shadow: var(--shadow);
}
button[data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: var(--txt-mid) !important;
    padding: 12px 20px !important;
    border-bottom: 3px solid transparent !important;
    background: transparent !important;
    border-radius: 0 !important;
    letter-spacing: 0.2px;
}
button[aria-selected="true"][data-baseweb="tab"] {
    color: var(--pwc-orange) !important;
    border-bottom: 3px solid var(--pwc-orange) !important;
    font-weight: 600 !important;
}
[data-testid="stTabPanel"] {
    background: transparent !important;
    padding: 24px 0 0 0 !important;
    border: none !important;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 20px 22px !important;
    box-shadow: var(--shadow) !important;
    border-top: 3px solid var(--pwc-orange) !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.8px !important;
    color: var(--txt-mid) !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: var(--txt-main) !important;
}
[data-testid="stMetricDelta"] svg { display: none; }

/* ── Cards / Panels ── */
.pwc-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 22px 24px;
    box-shadow: var(--shadow);
    margin-bottom: 16px;
}
.pwc-card-title {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: var(--txt-mid);
    margin-bottom: 4px;
}
.pwc-card-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--txt-main);
}

/* ── Section headers ── */
.section-hdr {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 28px 0 14px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}
.section-hdr-bar {
    width: 4px; height: 20px;
    background: var(--pwc-orange);
    border-radius: 2px;
    flex-shrink: 0;
}
.section-hdr-text {
    font-size: 0.9rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: var(--txt-main);
    text-transform: uppercase;
}
.section-hdr-sub {
    font-size: 0.75rem;
    color: var(--txt-dim);
    font-weight: 400;
    margin-left: 4px;
}

/* ── Page header ── */
.page-header {
    background: var(--white);
    border-bottom: 1px solid var(--border);
    padding: 18px 0 14px 0;
    margin-bottom: 24px;
}
.page-header-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--txt-main);
    letter-spacing: -0.2px;
}
.page-header-sub {
    font-size: 0.78rem;
    color: var(--txt-dim);
    margin-top: 2px;
}
.pwc-logo-bar {
    display: flex;
    align-items: center;
    gap: 10px;
}
.pwc-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--pwc-orange);
    display: inline-block;
}

/* ── Country badge (sidebar) ── */
.country-btn {
    display: block;
    width: 100%;
    padding: 10px 14px;
    margin: 4px 0;
    border-radius: var(--radius);
    border: 1px solid rgba(255,255,255,0.15);
    background: rgba(255,255,255,0.06);
    color: #E8ECF4 !important;
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
    font-weight: 500;
    text-decoration: none !important;
    cursor: pointer;
    transition: all 0.15s;
}
.country-btn:hover {
    background: rgba(208,74,2,0.25);
    border-color: var(--pwc-orange);
}
.country-btn.active {
    background: var(--pwc-orange);
    border-color: var(--pwc-orange);
    font-weight: 600;
}
.country-flag { margin-right: 8px; font-size: 1rem; }

/* ── News cards ── */
.news-wrap {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    box-shadow: var(--shadow);
}
.news-hdr {
    background: var(--pwc-navy);
    padding: 12px 18px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.news-hdr-title {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    font-weight: 600;
    color: #FFFFFF;
    letter-spacing: 0.4px;
    text-transform: uppercase;
}
.news-badge {
    background: var(--pwc-orange);
    color: white;
    font-size: 0.6rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 20px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.news-item {
    padding: 14px 18px;
    border-bottom: 1px solid var(--border);
    transition: background 0.15s;
}
.news-item:last-child { border-bottom: none; }
.news-item:hover { background: #FAFBFC; }
.news-item-title {
    font-family: 'Inter', sans-serif;
    font-size: 0.84rem;
    font-weight: 500;
    color: var(--txt-main) !important;
    text-decoration: none !important;
    line-height: 1.55;
    display: block;
    word-wrap: break-word;
    overflow-wrap: break-word;
    word-break: break-word;
    white-space: normal;
}
.news-item-title:hover { color: var(--pwc-orange) !important; }
.news-meta {
    font-size: 0.7rem;
    color: var(--txt-dim);
    margin-top: 5px;
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: normal;
}
.news-source-tag {
    display: inline-block;
    background: #F0F3F8;
    color: var(--pwc-navy);
    font-size: 0.62rem;
    font-weight: 600;
    padding: 1px 7px;
    border-radius: 4px;
    margin-right: 6px;
    letter-spacing: 0.3px;
}
.news-empty {
    padding: 30px 18px;
    text-align: center;
    color: var(--txt-dim);
    font-size: 0.82rem;
    line-height: 1.8;
}

/* ── Policy cards ── */
.policy-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-left: 4px solid var(--pwc-blue);
    border-radius: var(--radius);
    padding: 16px 20px;
    box-shadow: var(--shadow);
    margin-bottom: 12px;
}
.policy-card.warning {
    border-left-color: var(--pwc-orange);
}
.policy-card.success {
    border-left-color: #1A8C5B;
}
.policy-card-title {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: var(--txt-mid);
    margin-bottom: 8px;
}
.policy-card p, .policy-card li {
    font-size: 0.83rem;
    color: var(--txt-main);
    line-height: 1.65;
    margin: 0;
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: normal;
}
.policy-card ul {
    margin: 6px 0 0 0;
    padding-left: 16px;
}

/* ── Map selection highlight ── */
.selected-country-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: var(--pwc-orange);
    color: white;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    margin-bottom: 12px;
    letter-spacing: 0.3px;
}

/* ── Chart card ── */
.chart-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 20px 10px 20px;
    box-shadow: var(--shadow);
}
.chart-label {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: var(--txt-mid);
    margin-bottom: 2px;
}
.chart-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--txt-main);
    margin-bottom: 2px;
}
.chart-sub {
    font-size: 0.75rem;
    color: var(--txt-dim);
    margin-bottom: 12px;
}

/* ── Sidebar resource links ── */
.sb-link {
    display: block;
    padding: 7px 12px;
    margin: 3px 0;
    border-radius: 6px;
    font-size: 0.78rem;
    color: #C8D3E8 !important;
    text-decoration: none !important;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.04);
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: normal;
    transition: all 0.15s;
}
.sb-link:hover {
    background: rgba(208,74,2,0.2);
    border-color: rgba(208,74,2,0.5);
    color: #FFFFFF !important;
}
.sb-section-hdr {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.4) !important;
    margin: 18px 0 6px 0;
    padding-bottom: 4px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }
.block-container { padding-top: 0 !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 2. CHART THEME — PwC Light
# ══════════════════════════════════════════════════════════════════════════════
CHART_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#2D3142", size=12),
    margin=dict(l=48, r=16, t=16, b=48),
    legend=dict(
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#E2E5EB", borderwidth=1,
        font=dict(size=11, color="#2D3142"),
        orientation="h", y=-0.2,
    ),
    xaxis=dict(
        gridcolor="#F0F2F5", linecolor="#E2E5EB",
        tickfont=dict(size=10, color="#9BA3B2"),
        title_font=dict(size=11, color="#5A6070"),
    ),
    yaxis=dict(
        gridcolor="#F0F2F5", linecolor="#E2E5EB",
        tickfont=dict(size=10, color="#9BA3B2"),
        title_font=dict(size=11, color="#5A6070"),
    ),
    hoverlabel=dict(
        bgcolor="white", bordercolor="#E2E5EB",
        font=dict(family="Inter", size=12, color="#2D3142"),
    ),
)
PwC_COLORS = ["#D04A02", "#21325B", "#295BA5", "#EB6C2D", "#4C7FA8", "#8BA7C4", "#C0C8D8"]


# ══════════════════════════════════════════════════════════════════════════════
# 3. COUNTRY DATA STORE — Simulated BI Database
# ══════════════════════════════════════════════════════════════════════════════
COUNTRIES = {
    "Nigeria": {
        "flag": "🇳🇬", "iso": "NGA", "region": "West Africa",
        "kpi": {
            "total_sales":    ("45,200", "辆/年", "+6.2% YoY"),
            "ev_penetration": ("3.8%",   "EV 渗透率", "+1.2pp YoY"),
            "ev_tariff":      ("0%",     "纯电进口关税", "2023年起免税"),
            "fuel_price":     ("₦1,180", "柴油/升", "≈ $0.74 USD"),
        },
        "brand_share": {
            "brands": ["Sinotruk", "FAW", "Foton", "Volvo", "Scania"],
            "sales":  [1840, 1420, 980, 560, 410],
        },
        "trend": {
            "years": [2021, 2022, 2023, 2024, 2025, 2026],
            "ice":   [38200, 39500, 40100, 41800, 43200, 43800],
            "ev":    [0,     80,    320,   820,   1640,  1400],
        },
        "policy": {
            "tariff": "CBU整车纯电动商用车：0%关税（2023–2028优惠期）；KD散件组装：0%；传统燃油CBU：35%",
            "certification": "SON（尼日利亚标准局）强制认证；NAFDAC（特种车辆）；进口须取得Form M批文",
            "key_buyers": "Dangote Cement（水泥物流）、BUA Group（粮食与化工）、NNPC旗下物流公司",
            "risk": "奈拉汇率剧烈波动（近18个月贬值超60%），建议合同使用美元计价并锁定汇率；港口清关效率存在延误风险",
        },
        "news_query": "Nigeria commercial vehicle OR Dangote logistics OR Nigeria EV tariff",
    },
    "South Africa": {
        "flag": "🇿🇦", "iso": "ZAF", "region": "Southern Africa",
        "kpi": {
            "total_sales":    ("31,500", "辆/年", "-2.8% YoY"),
            "ev_penetration": ("1.9%",   "EV 渗透率", "+0.7pp YoY"),
            "ev_tariff":      ("25%",    "整车进口关税", "KD组装可降至12%"),
            "fuel_price":     ("R21.6",  "柴油/升", "≈ $1.18 USD"),
        },
        "brand_share": {
            "brands": ["Mercedes-Benz", "Volvo", "MAN", "Scania", "FAW"],
            "sales":  [7200, 6100, 5800, 5200, 3100],
        },
        "trend": {
            "years": [2021, 2022, 2023, 2024, 2025, 2026],
            "ice":   [29800, 31200, 32500, 31800, 30900, 30900],
            "ev":    [0,     0,     120,   320,   540,   600],
        },
        "policy": {
            "tariff": "CBU整车进口税25%；APDP国产化激励计划（国产化>50%可获补贴）；EV进口暂无优惠",
            "certification": "NRCS（南非国家规范委员会）强制LoA认证；需符合Euro 5等效排放标准；SABS型式认证",
            "key_buyers": "Transnet（铁路与港口）、Imperial Logistics、Tiger Brands物流、Shoprite配送",
            "risk": "兰特汇率承压（1USD≈18.5ZAR）；电力供应不稳（负荷削减）影响EV充电基建推进",
        },
        "news_query": "South Africa commercial truck OR Transnet logistics OR South Africa EV fleet",
    },
    "Morocco": {
        "flag": "🇲🇦", "iso": "MAR", "region": "North Africa",
        "kpi": {
            "total_sales":    ("18,400", "辆/年", "+8.5% YoY"),
            "ev_penetration": ("2.1%",   "EV 渗透率", "+0.9pp YoY"),
            "ev_tariff":      ("2.5%",   "纯电进口关税", "欧盟AA协议优惠"),
            "fuel_price":     ("13.5",   "MAD/升柴油", "≈ $1.34 USD"),
        },
        "brand_share": {
            "brands": ["Renault Trucks", "Mercedes-Benz", "Volvo", "Sinotruk", "MAN"],
            "sales":  [4200, 3600, 3100, 2800, 2100],
        },
        "trend": {
            "years": [2021, 2022, 2023, 2024, 2025, 2026],
            "ice":   [14200, 15100, 16200, 17400, 18000, 18000],
            "ev":    [0,     40,    120,   260,   380,   400],
        },
        "policy": {
            "tariff": "欧盟联系国AA协议：商用车CBU关税2.5%；纯电与传统车同等对待；无KD专项激励",
            "certification": "CNEAT（摩洛哥道路运输技术认证中心）；与UN-ECE体系互认，欧标车辆无需重复认证",
            "key_buyers": "OCP集团（磷酸盐矿业年采购800+辆）、ONCF国铁、卡萨布兰卡港物流运营商",
            "risk": "市场规模相对有限；竞争对手以欧洲品牌为主，中国品牌品牌认知度仍需提升",
        },
        "news_query": "Morocco OCP Group truck OR Morocco logistics transport OR AIVAM véhicules",
    },
    "Egypt": {
        "flag": "🇪🇬", "iso": "EGY", "region": "North Africa",
        "kpi": {
            "total_sales":    ("25,800", "辆/年", "+11.2% YoY"),
            "ev_penetration": ("0.8%",   "EV 渗透率", "+0.3pp YoY"),
            "ev_tariff":      ("40%",    "CBU整车关税", "KD组装降至5%"),
            "fuel_price":     ("EGP 9.7","柴油/升 (补贴价)", "≈ $0.20 USD"),
        },
        "brand_share": {
            "brands": ["Sinotruk", "SAIC Maxus", "Foton", "Mercedes-Benz", "MAN"],
            "sales":  [6200, 4800, 3900, 3500, 2800],
        },
        "trend": {
            "years": [2021, 2022, 2023, 2024, 2025, 2026],
            "ice":   [18000, 20500, 22100, 24800, 25600, 25600],
            "ev":    [0,     0,     60,    130,   200,   200],
        },
        "policy": {
            "tariff": "CBU整车关税40%；KD散件组装（国产化率>40%）可享5%优惠税率；强烈建议寻找本地组装合作方",
            "certification": "EOS（埃及标准局）强制认证；需取得GOEIC进口许可；苏伊士经济区内生产可享免税",
            "key_buyers": "苏伊士运河经济区建设承包商、埃及国家石油公司（EGPC）运输部门、私营建材物流",
            "risk": "埃及镑大幅贬值风险（近2年贬值超50%）；外汇管制影响进口付款周期",
        },
        "news_query": "Egypt commercial vehicle market OR Egypt logistics EV OR Suez Economic Zone trucks",
    },
    "Tunisia": {
        "flag": "🇹🇳", "iso": "TUN", "region": "North Africa",
        "kpi": {
            "total_sales":    ("8,100",  "辆/年", "+3.1% YoY"),
            "ev_penetration": ("1.2%",   "EV 渗透率", "+0.4pp YoY"),
            "ev_tariff":      ("10%",    "进口关税", "欧盟联系协议"),
            "fuel_price":     ("2.1",    "TND/升柴油", "≈ $0.67 USD"),
        },
        "brand_share": {
            "brands": ["Mercedes-Benz", "Renault Trucks", "MAN", "Volvo", "Sinotruk"],
            "sales":  [2100, 1800, 1500, 1200, 900],
        },
        "trend": {
            "years": [2021, 2022, 2023, 2024, 2025, 2026],
            "ice":   [6800, 7100, 7400, 7800, 8000, 8000],
            "ev":    [0,    20,   40,   70,   100,  100],
        },
        "policy": {
            "tariff": "欧盟联系协议框架内：商用车关税约10%；与欧盟认证体系高度互认，准入门槛相对低",
            "certification": "INNORPI（突尼斯国家标准局）；欧标Euro 5车辆基本免二次认证",
            "key_buyers": "突尼斯磷酸盐集团（CPG）、港口管理局、私营食品及纺织品物流",
            "risk": "市场总量偏小；欧洲品牌市场份额超70%，中国品牌需强本地化服务体系",
        },
        "news_query": "Tunisia transport logistics truck OR Tunisie transport commercial OR CPG phosphate logistics",
    },
    "Rwanda": {
        "flag": "🇷🇼", "iso": "RWA", "region": "East Africa",
        "kpi": {
            "total_sales":    ("3,600",  "辆/年", "+18.4% YoY"),
            "ev_penetration": ("4.5%",   "EV 渗透率", "+2.1pp YoY"),
            "ev_tariff":      ("0%",     "EAC协议内关税", "东非共同体免税"),
            "fuel_price":     ("RWF 1,650","柴油/升", "≈ $1.45 USD"),
        },
        "brand_share": {
            "brands": ["Toyota Dyna", "Sinotruk", "ISUZU", "Foton", "Yutong"],
            "sales":  [980, 760, 620, 480, 340],
        },
        "trend": {
            "years": [2021, 2022, 2023, 2024, 2025, 2026],
            "ice":   [1800, 2100, 2500, 2900, 3300, 3450],
            "ev":    [0,    20,   60,   110,  150,  160],
        },
        "policy": {
            "tariff": "EAC东非共同体内0%关税；非EAC国家进口适用25%标准税率；EV有额外激励讨论中",
            "certification": "RSB（卢旺达标准局）认证；监管透明度高，流程相对高效（全球营商便利度前50名）",
            "key_buyers": "卢旺达发展局（RDB）基建项目、私营农业物流、科技园区配送",
            "risk": "市场体量仍小；2035年禁售燃油商用车路线图带来长期不确定性，但EV先发机遇窗口明确",
        },
        "news_query": "Rwanda transport logistics truck OR Rwanda EV commercial vehicle OR East Africa freight",
    },
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
# 4. NEWS FETCHER — Authority-filtered, time-constrained
# ══════════════════════════════════════════════════════════════════════════════
TRUSTED_SOURCES = (
    "site:reuters.com OR site:bloomberg.com OR site:ft.com "
    "OR site:engineeringnews.co.za OR site:businessday.ng "
    "OR site:zawya.com OR site:afdb.org OR site:apanews.net"
)
NOISE_WORDS = {
    "rumor","rumour","unconfirmed","alleged","shocking","viral",
    "leaked","clickbait","you won't believe",
}

@st.cache_data(ttl=1800)
def fetch_news(query: str, country: str, limit: int = 6) -> list:
    full_q = f"({query}) ({TRUSTED_SOURCES}) when:30d"
    encoded = full_q.replace(" ", "+").replace('"', "%22")
    url = (
        f"https://news.google.com/rss/search"
        f"?q={encoded}&hl=en-US&gl=US&ceid=US:en"
    )
    cutoff = datetime.utcnow() - timedelta(days=30)
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries:
            if len(items) >= limit:
                break
            title = entry.get("title", "")
            if not title:
                continue
            if any(n in title.lower() for n in NOISE_WORDS):
                continue
            pub_str, pub_dt = "–", None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                pub_dt  = datetime(*entry.published_parsed[:6])
                pub_str = pub_dt.strftime("%Y-%m-%d")
            if pub_dt and pub_dt < cutoff:
                continue
            items.append({
                "title":     title,
                "link":      entry.get("link", "#"),
                "published": pub_str,
                "pub_dt":    pub_dt,
                "source":    entry.get("source", {}).get("title", "–"),
            })
        items.sort(key=lambda x: x["pub_dt"] or datetime.min, reverse=True)
        return items
    except Exception:
        return []


# ══════════════════════════════════════════════════════════════════════════════
# 5. SESSION STATE INIT
# ══════════════════════════════════════════════════════════════════════════════
if "selected_country" not in st.session_state:
    st.session_state.selected_country = "Nigeria"


# ══════════════════════════════════════════════════════════════════════════════
# 6. MAP BUILDER
# ══════════════════════════════════════════════════════════════════════════════
def build_map(selected: str) -> go.Figure:
    rows = []
    selected_iso = COUNTRIES.get(selected, {}).get("iso", "")

    for iso in ALL_AFRICA_ISO:
        matched_name = next(
            (c for c, d in COUNTRIES.items() if d["iso"] == iso), None
        )
        if matched_name:
            d = COUNTRIES[matched_name]
            kpi_lines = "<br>".join([
                f"<b>{v[0]}</b> {v[1]}"
                for v in d["kpi"].values()
            ])
            tip = (
                f"<b style='font-size:13px;'>{d['flag']} {matched_name}</b><br>"
                f"<span style='color:#9BA3B2;font-size:10px;'>{d['region']}</span><br><br>"
                f"{kpi_lines}<br><br>"
                f"<span style='color:#D04A02;font-size:10px;'>● Click to drill down</span>"
            )
            score = (95 if matched_name == selected else 75)
            rows.append({"iso": iso, "score": score,
                         "tooltip": tip, "hl": 1, "name": matched_name})
        else:
            rows.append({"iso": iso, "score": 10,
                         "tooltip": f"<b>{iso}</b><br><span style='color:#9BA3B2;'>No coverage data</span>",
                         "hl": 0, "name": iso})

    df = pd.DataFrame(rows)

    fig = go.Figure()

    # Base layer
    df_base = df[df.hl == 0]
    fig.add_trace(go.Choropleth(
        locations=df_base["iso"], z=df_base["score"],
        text=df_base["tooltip"],
        hovertemplate="%{text}<extra></extra>",
        colorscale=[[0, "#E8ECF4"], [1, "#D0D6E2"]],
        showscale=False,
        marker_line_color="#C8CDD8", marker_line_width=0.5,
        zmin=0, zmax=100,
    ))

    # Highlight: non-selected tracked countries
    df_hl_other = df[(df.hl == 1) & (df["name"] != selected)]
    if not df_hl_other.empty:
        fig.add_trace(go.Choropleth(
            locations=df_hl_other["iso"], z=df_hl_other["score"],
            text=df_hl_other["tooltip"],
            hovertemplate="%{text}<extra></extra>",
            colorscale=[[0, "#8BA7C4"], [1, "#295BA5"]],
            showscale=False,
            marker_line_color="#21325B", marker_line_width=0.8,
            zmin=0, zmax=100,
        ))

    # Selected country
    df_sel = df[df["name"] == selected]
    if not df_sel.empty:
        fig.add_trace(go.Choropleth(
            locations=df_sel["iso"], z=df_sel["score"],
            text=df_sel["tooltip"],
            hovertemplate="%{text}<extra></extra>",
            colorscale=[[0, "#D04A02"], [1, "#EB6C2D"]],
            showscale=False,
            marker_line_color="#A03800", marker_line_width=2,
            zmin=0, zmax=100,
        ))

    fig.update_layout(
        geo=dict(
            scope="africa", showframe=False,
            showcoastlines=True, coastlinecolor="#C8CDD8", coastlinewidth=0.7,
            showland=True, landcolor="#F0F2F6",
            showocean=True, oceancolor="#E8F0F8",
            showcountries=True, countrycolor="#C8CDD8", countrywidth=0.5,
            bgcolor="#F4F5F7",
            projection_type="natural earth",
        ),
        paper_bgcolor="#F4F5F7",
        plot_bgcolor="#F4F5F7",
        margin=dict(l=0, r=0, t=0, b=0),
        height=420,
        hoverlabel=dict(
            bgcolor="white", bordercolor="#E2E5EB",
            font=dict(family="Inter", size=12, color="#2D3142"),
        ),
        dragmode=False,
        coloraxis_showscale=False,
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# 7. CHART BUILDERS — Country-specific
# ══════════════════════════════════════════════════════════════════════════════
def chart_brand_bar(country_data: dict) -> go.Figure:
    brands = country_data["brand_share"]["brands"]
    sales  = country_data["brand_share"]["sales"]
    total  = sum(sales)
    pcts   = [round(s / total * 100, 1) for s in sales]
    colors = [PwC_COLORS[0] if i == 0 else PwC_COLORS[1] if i == 1
              else PwC_COLORS[2] if i == 2 else "#C0C8D8"
              for i in range(len(brands))]

    fig = go.Figure(go.Bar(
        x=brands, y=sales,
        text=[f"{p}%" for p in pcts],
        textposition="outside",
        textfont=dict(size=11, color="#2D3142", family="Inter"),
        marker=dict(color=colors, line=dict(color="white", width=1.5)),
        hovertemplate="<b>%{x}</b><br>Sales: <b>%{y:,}</b> units<br>Share: <b>%{text}</b><extra></extra>",
    ))
    layout = {**CHART_BASE}
    layout["yaxis"] = {**layout.get("yaxis", {}), "title": "Units", "range": [0, max(sales) * 1.2]}
    layout["xaxis"] = {**layout.get("xaxis", {}), "title": "Brand"}
    layout["showlegend"] = False
    layout["bargap"] = 0.38
    fig.update_layout(**layout)
    return fig


def chart_trend_area(country_data: dict) -> go.Figure:
    years = country_data["trend"]["years"]
    ice   = country_data["trend"]["ice"]
    ev    = country_data["trend"]["ev"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=ice, name="ICE (Conventional)",
        mode="lines+markers",
        line=dict(color="#21325B", width=2.5),
        marker=dict(size=6, color="#21325B"),
        fill="tozeroy", fillcolor="rgba(33,50,91,0.08)",
        hovertemplate="<b>%{x}</b><br>ICE: <b>%{y:,}</b> units<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=years, y=ev, name="EV / New Energy",
        mode="lines+markers",
        line=dict(color="#D04A02", width=2.5),
        marker=dict(size=7, color="#D04A02", symbol="diamond"),
        fill="tozeroy", fillcolor="rgba(208,74,2,0.1)",
        hovertemplate="<b>%{x}</b><br>EV: <b>%{y:,}</b> units<extra></extra>",
    ))
    # 2026 forecast annotation
    fig.add_vline(
        x=2025.5, line_dash="dash", line_color="#9BA3B2", line_width=1,
    )
    fig.add_annotation(
        x=2025.7, y=max(ice) * 0.95,
        text="← Actual  |  Forecast →",
        showarrow=False,
        font=dict(size=10, color="#9BA3B2", family="Inter"),
    )
    layout = {**CHART_BASE}
    layout["xaxis"] = {**layout.get("xaxis", {}), "title": "Year",
                       "tickmode": "array", "tickvals": years}
    layout["yaxis"] = {**layout.get("yaxis", {}), "title": "Units"}
    fig.update_layout(**layout)
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# 8. SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo / Brand
    st.markdown("""
    <div style="padding: 16px 4px 12px 4px; border-bottom: 1px solid rgba(255,255,255,0.12);">
        <div style="font-family:'Inter',sans-serif;font-size:1.1rem;font-weight:700;
                    color:white;letter-spacing:-0.3px;">
            Africa CV Intelligence
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:0.7rem;
                    color:rgba(255,255,255,0.45);margin-top:3px;letter-spacing:0.3px;">
            Market Analytics Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Country selector
    st.markdown("""
    <div style="font-family:'Inter',sans-serif;font-size:0.65rem;font-weight:700;
                letter-spacing:1.5px;text-transform:uppercase;
                color:rgba(255,255,255,0.4);margin:18px 0 8px 0;">
        Focus Market
    </div>
    """, unsafe_allow_html=True)

    for country_name, cdata in COUNTRIES.items():
        is_active = st.session_state.selected_country == country_name
        btn_label = f"{cdata['flag']}  {country_name}"
        if is_active:
            # Active state — shown as disabled styled button
            st.markdown(f"""
            <div style="padding:9px 14px;margin:3px 0;border-radius:6px;
                        background:#D04A02;border:1px solid #D04A02;
                        font-family:'Inter',sans-serif;font-size:0.82rem;
                        font-weight:600;color:white;">
                {btn_label} &nbsp;<span style="opacity:.7;font-size:.7rem;">● Selected</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.button(btn_label, key=f"btn_{country_name}", use_container_width=True):
                st.session_state.selected_country = country_name
                st.cache_data.clear()
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sb-section-hdr">Quick Links</div>', unsafe_allow_html=True)

    QUICK_LINKS = [
        ("🏛 Nigeria Customs (NCS)", "https://www.customs.gov.ng"),
        ("🏦 Central Bank Nigeria",  "https://www.cbn.gov.ng"),
        ("🚗 AutoTrader ZA – Trucks","https://www.autotrader.co.za/trucks"),
        ("🚂 Transnet Freight",      "https://www.transnet.net"),
        ("🌾 OCP Group Morocco",     "https://www.ocpgroup.ma"),
        ("🤝 AIVAM Morocco",        "https://www.aivam.ma"),
        ("🌍 AfDB",                  "https://www.afdb.org"),
        ("📊 Zawya Finance",         "https://www.zawya.com"),
    ]
    for label, url in QUICK_LINKS:
        st.markdown(f'<a class="sb-link" href="{url}" target="_blank">{label}</a>',
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↺  Refresh Intelligence", use_container_width=True, key="refresh"):
        st.cache_data.clear()
        st.rerun()

    st.markdown(f"""
    <div style="font-family:'Inter',monospace;font-size:0.6rem;
                color:rgba(255,255,255,0.25);text-align:center;
                margin-top:20px;line-height:2;">
        Africa CV Market Intelligence<br>
        Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}<br>
        For internal use only
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 9. PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
col_hdr_l, col_hdr_r = st.columns([3, 1])
with col_hdr_l:
    st.markdown("""
    <div style="padding: 20px 0 8px 0;">
        <div style="font-family:'Inter',sans-serif;font-size:1.35rem;font-weight:700;
                    color:#2D3142;letter-spacing:-0.3px;">
            Africa Commercial Vehicle Market Intelligence
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:0.8rem;color:#9BA3B2;margin-top:3px;">
            Strategic market analysis across 6 key African economies · Updated monthly
        </div>
    </div>
    """, unsafe_allow_html=True)
with col_hdr_r:
    st.markdown(f"""
    <div style="padding:20px 0 8px 0;text-align:right;">
        <div style="font-family:'Inter',sans-serif;font-size:0.7rem;
                    color:#9BA3B2;letter-spacing:0.3px;">
            {datetime.now().strftime('%B %d, %Y')}
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:0.75rem;
                    color:#D04A02;font-weight:600;margin-top:3px;">
            ● Live Intelligence Feed
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr style="margin: 0 0 20px 0; border-color: #E2E5EB;">', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 10. MAP + COUNTRY SELECTOR (Top Section)
# ══════════════════════════════════════════════════════════════════════════════
sel = st.session_state.selected_country
cdata = COUNTRIES[sel]

map_col, info_col = st.columns([5, 2], gap="large")

with map_col:
    st.markdown("""
    <div style="font-family:'Inter',sans-serif;font-size:0.72rem;font-weight:700;
                letter-spacing:0.8px;text-transform:uppercase;color:#5A6070;
                margin-bottom:8px;">
        Africa Strategic Market Map
        <span style="font-weight:400;color:#9BA3B2;margin-left:8px;">
            · Click a highlighted country to drill down
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Map with click selection
    map_fig = build_map(sel)
    map_event = st.plotly_chart(
        map_fig,
        use_container_width=True,
        config={"displayModeBar": False, "scrollZoom": False},
        on_select="rerun",
        selection_mode="points",
        key="africa_map",
    )

    # Handle map click
    if map_event and hasattr(map_event, "selection") and map_event.selection:
        pts = map_event.selection.get("points", [])
        if pts:
            clicked_iso = pts[0].get("location", "")
            clicked_name = next(
                (c for c, d in COUNTRIES.items() if d["iso"] == clicked_iso),
                None
            )
            if clicked_name and clicked_name != st.session_state.selected_country:
                st.session_state.selected_country = clicked_name
                st.cache_data.clear()
                st.rerun()

    # Legend
    legend_cols = st.columns(len(COUNTRIES))
    for lc, (cname, cd) in zip(legend_cols, COUNTRIES.items()):
        is_sel = cname == sel
        with lc:
            color = "#D04A02" if is_sel else "#295BA5"
            bg    = "rgba(208,74,2,0.08)" if is_sel else "rgba(41,91,165,0.06)"
            st.markdown(f"""
            <div style="text-align:center;padding:6px 4px;border-radius:6px;
                        background:{bg};border:1px solid {'#D04A02' if is_sel else '#E2E5EB'};">
                <div style="font-size:1rem;">{cd['flag']}</div>
                <div style="font-family:'Inter',sans-serif;font-size:0.65rem;
                            font-weight:{'700' if is_sel else '500'};
                            color:{color};margin-top:2px;">{cname.split()[0]}</div>
            </div>
            """, unsafe_allow_html=True)

with info_col:
    st.markdown(f"""
    <div style="background:white;border:1px solid #E2E5EB;border-radius:8px;
                padding:20px;box-shadow:0 1px 4px rgba(0,0,0,0.07);
                border-top:4px solid #D04A02;height:100%;">
        <div style="font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:700;
                    letter-spacing:0.8px;text-transform:uppercase;color:#9BA3B2;
                    margin-bottom:12px;">
            Currently Viewing
        </div>
        <div style="font-size:2rem;margin-bottom:4px;">{cdata['flag']}</div>
        <div style="font-family:'Inter',sans-serif;font-size:1.1rem;font-weight:700;
                    color:#2D3142;">{sel}</div>
        <div style="font-family:'Inter',sans-serif;font-size:0.75rem;color:#9BA3B2;
                    margin-bottom:16px;">{cdata['region']}</div>
        <hr style="border-color:#F0F2F5;margin:12px 0;">
        <div style="font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:700;
                    letter-spacing:0.6px;text-transform:uppercase;color:#9BA3B2;
                    margin-bottom:10px;">
            Market Snapshot
        </div>
    """, unsafe_allow_html=True)

    for key, (value, label, delta) in cdata["kpi"].items():
        delta_color = "#1A8C5B" if "+" in delta else "#D04A02" if "-" in delta else "#5A6070"
        st.markdown(f"""
        <div style="margin-bottom:12px;padding-bottom:12px;
                    border-bottom:1px solid #F0F2F5;">
            <div style="font-family:'Inter',sans-serif;font-size:0.68rem;
                        color:#9BA3B2;text-transform:uppercase;letter-spacing:0.5px;">
                {label}
            </div>
            <div style="font-family:'Inter',sans-serif;font-size:1.15rem;
                        font-weight:700;color:#2D3142;margin:2px 0;">
                {value}
            </div>
            <div style="font-family:'Inter',sans-serif;font-size:0.7rem;
                        color:{delta_color};font-weight:500;">
                {delta}
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 11. COUNTRY DASHBOARD — Tabs
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="section-hdr">
    <div class="section-hdr-bar"></div>
    <div class="section-hdr-text">{cdata['flag']} &nbsp;{sel} — Country Dashboard</div>
    <div class="section-hdr-sub">Simulated data for illustrative purposes</div>
</div>
""", unsafe_allow_html=True)

tab_market, tab_policy, tab_news = st.tabs([
    "📊  Market Analytics",
    "📋  Policy & Market Access",
    "📡  Intelligence Feed",
])


# ── Tab 1: Market Analytics ───────────────────────────────────────────────────
with tab_market:
    # KPI metrics row
    km1, km2, km3, km4 = st.columns(4)
    kpi_items = list(cdata["kpi"].items())
    metric_labels = {
        "total_sales":    "Annual CV Sales",
        "ev_penetration": "EV Penetration Rate",
        "ev_tariff":      "EV Import Tariff",
        "fuel_price":     "Fuel / Energy Price",
    }
    for col, (key, (val, lbl, delta)) in zip([km1, km2, km3, km4], kpi_items):
        with col:
            delta_val = delta if delta else None
            dcolor = "normal"
            if delta and "-" in delta:
                dcolor = "inverse"
            elif delta and ("免税" in delta or "0%" in delta or "EAC" in delta):
                dcolor = "normal"
            st.metric(
                label=metric_labels.get(key, lbl),
                value=val,
                delta=delta,
                delta_color=dcolor,
                help=lbl,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts row
    chart_l, chart_r = st.columns(2, gap="large")

    with chart_l:
        st.markdown(f"""
        <div class="chart-card">
            <div class="chart-label">Market Share</div>
            <div class="chart-title">Brand Rankings — {sel}</div>
            <div class="chart-sub">Top 5 brands by annual unit sales (simulated)</div>
        </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(
            chart_brand_bar(cdata),
            use_container_width=True,
            config={"displayModeBar": False},
            key=f"brand_{sel}",
        )
        with st.expander("View data table"):
            df_brand = pd.DataFrame({
                "Brand":      cdata["brand_share"]["brands"],
                "Units":      cdata["brand_share"]["sales"],
                "Share (%)":  [
                    round(s / sum(cdata["brand_share"]["sales"]) * 100, 1)
                    for s in cdata["brand_share"]["sales"]
                ],
            })
            st.dataframe(df_brand, use_container_width=True, hide_index=True)

    with chart_r:
        st.markdown(f"""
        <div class="chart-card">
            <div class="chart-label">Sales Trend 2021–2026</div>
            <div class="chart-title">ICE vs. EV/New Energy — {sel}</div>
            <div class="chart-sub">Historical actuals + 2026 forecast (simulated)</div>
        </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(
            chart_trend_area(cdata),
            use_container_width=True,
            config={"displayModeBar": False},
            key=f"trend_{sel}",
        )
        with st.expander("View data table"):
            df_trend = pd.DataFrame({
                "Year": cdata["trend"]["years"],
                "ICE (units)": cdata["trend"]["ice"],
                "EV (units)":  cdata["trend"]["ev"],
            })
            df_trend["EV Share (%)"] = (
                df_trend["EV (units)"] /
                (df_trend["ICE (units)"] + df_trend["EV (units)"]) * 100
            ).round(2)
            st.dataframe(df_trend, use_container_width=True, hide_index=True)


# ── Tab 2: Policy & Market Access ─────────────────────────────────────────────
with tab_policy:
    p = cdata["policy"]

    st.markdown("""
    <div style="font-family:'Inter',sans-serif;font-size:0.78rem;color:#5A6070;
                margin-bottom:20px;line-height:1.7;">
        This section outlines the key regulatory, certification, and commercial access
        requirements for the selected market. Data represents current intelligence
        as of the reporting period.
    </div>
    """, unsafe_allow_html=True)

    pol_l, pol_r = st.columns(2, gap="large")

    with pol_l:
        st.markdown(f"""
        <div class="policy-card">
            <div class="policy-card-title">🏷 Tariff & Import Structure</div>
            <p>{p['tariff']}</p>
        </div>
        <div class="policy-card success">
            <div class="policy-card-title">📋 Certification Requirements</div>
            <p>{p['certification']}</p>
        </div>
        """, unsafe_allow_html=True)

    with pol_r:
        st.markdown(f"""
        <div class="policy-card">
            <div class="policy-card-title">🏗 Key Buyers & Procurement Bodies</div>
            <p>{p['key_buyers']}</p>
        </div>
        <div class="policy-card warning">
            <div class="policy-card-title">⚠ Risk Factors & Operational Considerations</div>
            <p>{p['risk']}</p>
        </div>
        """, unsafe_allow_html=True)

    # Summary scorecard
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-hdr">
        <div class="section-hdr-bar"></div>
        <div class="section-hdr-text">Market Entry Assessment</div>
    </div>
    """, unsafe_allow_html=True)

    score_cols = st.columns(5)
    scores = {
        "Market Size":     {"Nigeria":9,"South Africa":8,"Morocco":6,"Egypt":7,"Tunisia":4,"Rwanda":3},
        "EV Readiness":    {"Nigeria":7,"South Africa":5,"Morocco":6,"Egypt":3,"Tunisia":5,"Rwanda":8},
        "Tariff Advantage":{"Nigeria":9,"South Africa":4,"Morocco":8,"Egypt":5,"Tunisia":7,"Rwanda":9},
        "Regulatory Ease": {"Nigeria":5,"South Africa":8,"Morocco":8,"Egypt":5,"Tunisia":7,"Rwanda":9},
        "Growth Momentum": {"Nigeria":7,"South Africa":4,"Morocco":8,"Egypt":8,"Tunisia":5,"Rwanda":9},
    }
    for col, (dim, vals) in zip(score_cols, scores.items()):
        score = vals.get(sel, 5)
        bar_w = score * 10
        color = "#D04A02" if score >= 8 else "#295BA5" if score >= 6 else "#9BA3B2"
        with col:
            st.markdown(f"""
            <div style="background:white;border:1px solid #E2E5EB;border-radius:8px;
                        padding:16px 14px;box-shadow:0 1px 4px rgba(0,0,0,0.07);">
                <div style="font-family:'Inter',sans-serif;font-size:0.65rem;font-weight:700;
                            text-transform:uppercase;letter-spacing:0.6px;color:#9BA3B2;
                            margin-bottom:8px;">{dim}</div>
                <div style="font-family:'Inter',sans-serif;font-size:1.6rem;font-weight:700;
                            color:{color};">{score}<span style="font-size:.8rem;color:#9BA3B2;">/10</span></div>
                <div style="background:#F0F2F5;border-radius:4px;height:5px;margin-top:8px;">
                    <div style="background:{color};width:{bar_w}%;height:5px;border-radius:4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ── Tab 3: Intelligence Feed ───────────────────────────────────────────────────
with tab_news:
    st.markdown(f"""
    <div style="background:#F8F9FB;border:1px solid #E2E5EB;border-radius:8px;
                padding:12px 18px;margin-bottom:20px;
                font-family:'Inter',sans-serif;font-size:0.8rem;color:#5A6070;
                line-height:1.7;">
        <strong style="color:#2D3142;">Intelligence parameters:</strong>
        &nbsp;Country focus: <strong style="color:#D04A02;">{sel}</strong>
        &nbsp;·&nbsp; Sources: Reuters, Bloomberg, FT, Engineering News, BusinessDay, Zawya
        &nbsp;·&nbsp; Time window: <strong>Last 30 days</strong>
        &nbsp;·&nbsp; Noise-filtered &amp; sorted by recency
    </div>
    """, unsafe_allow_html=True)

    news_l, news_r = st.columns([3, 1], gap="large")

    with news_l:
        with st.spinner(f"Fetching latest intelligence for {sel}..."):
            news_items = fetch_news(cdata["news_query"], sel, limit=8)

        st.markdown('<div class="news-wrap">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="news-hdr">
            <span class="news-hdr-title">📡 &nbsp;{sel} — Commercial Vehicle Intelligence</span>
            <span class="news-badge">LIVE · 30D</span>
        </div>
        """, unsafe_allow_html=True)

        if not news_items:
            st.markdown("""
            <div class="news-empty">
                <div style="font-size:1.5rem;margin-bottom:8px;">📭</div>
                No recent results found from authority sources.<br>
                <span style="font-size:0.72rem;color:#C0C8D8;">
                Try refreshing, or check network connectivity.
                </span>
            </div>
            """, unsafe_allow_html=True)
        else:
            for item in news_items:
                st.markdown(f"""
                <div class="news-item">
                    <a class="news-item-title"
                       href="{item['link']}" target="_blank">{item['title']}</a>
                    <div class="news-meta">
                        <span class="news-source-tag">{item['source']}</span>
                        {item['published']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with news_r:
        st.markdown("""
        <div style="background:white;border:1px solid #E2E5EB;border-radius:8px;
                    padding:18px;box-shadow:0 1px 4px rgba(0,0,0,0.07);">
            <div style="font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:700;
                        text-transform:uppercase;letter-spacing:0.6px;color:#9BA3B2;
                        margin-bottom:14px;">Search Parameters</div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="margin-bottom:12px;">
                <div style="font-size:.68rem;color:#9BA3B2;font-family:'Inter';">Country</div>
                <div style="font-size:.85rem;font-weight:600;color:#2D3142;
                            font-family:'Inter';">{sel}</div>
            </div>
            <div style="margin-bottom:12px;">
                <div style="font-size:.68rem;color:#9BA3B2;font-family:'Inter';">Keywords</div>
                <div style="font-size:.75rem;color:#5A6070;font-family:'Inter';
                            line-height:1.6;word-break:break-word;">
                    {cdata['news_query']}
                </div>
            </div>
            <div style="margin-bottom:12px;">
                <div style="font-size:.68rem;color:#9BA3B2;font-family:'Inter';">Time Window</div>
                <div style="font-size:.85rem;font-weight:600;color:#2D3142;font-family:'Inter';">
                    Last 30 days
                </div>
            </div>
            <div style="margin-bottom:0;">
                <div style="font-size:.68rem;color:#9BA3B2;font-family:'Inter';">Cache TTL</div>
                <div style="font-size:.85rem;font-weight:600;color:#2D3142;font-family:'Inter';">
                    30 minutes
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:white;border:1px solid #E2E5EB;border-radius:8px;
                    padding:18px;box-shadow:0 1px 4px rgba(0,0,0,0.07);">
            <div style="font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:700;
                        text-transform:uppercase;letter-spacing:0.6px;color:#9BA3B2;
                        margin-bottom:12px;">Authority Sources</div>
        """, unsafe_allow_html=True)
        for src in ["Reuters", "Bloomberg", "Financial Times", "Engineering News ZA",
                    "BusinessDay NG", "Zawya", "AfDB", "APANews"]:
            st.markdown(f"""
            <div style="font-family:'Inter';font-size:.75rem;color:#5A6070;
                        padding:5px 0;border-bottom:1px solid #F4F5F7;
                        display:flex;align-items:center;gap:8px;">
                <div style="width:6px;height:6px;border-radius:50%;
                            background:#1A8C5B;flex-shrink:0;"></div>
                {src}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 12. FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="border-top:1px solid #E2E5EB;padding-top:16px;
            font-family:'Inter',sans-serif;font-size:0.7rem;color:#9BA3B2;
            display:flex;justify-content:space-between;align-items:center;">
    <div>
        <strong style="color:#5A6070;">Africa CV Market Intelligence Platform</strong>
        &nbsp;·&nbsp; For internal strategic use only
        &nbsp;·&nbsp; Market data is simulated for illustrative purposes
    </div>
    <div style="text-align:right;">
        News: Reuters · Bloomberg · FT · Authority Sources
        &nbsp;·&nbsp; Refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M')} CST
    </div>
</div>
""", unsafe_allow_html=True)
