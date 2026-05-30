"""
Africa Commercial Vehicle Market Intelligence Platform
Enterprise BI Engine v5.0 — Full 54-Nation Coverage + Tiered Fallback
"""

import streamlit as st
import feedparser
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

:root {
    --bg:         #F4F5F7;
    --white:      #FFFFFF;
    --orange:     #D04A02;
    --orange2:    #EB6C2D;
    --navy:       #21325B;
    --blue:       #295BA5;
    --txt:        #2D3142;
    --mid:        #5A6070;
    --dim:        #9BA3B2;
    --border:     #E2E5EB;
    --shadow:     0 1px 4px rgba(0,0,0,0.07), 0 4px 16px rgba(0,0,0,0.04);
    --radius:     8px;
}
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
    background: var(--bg) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--txt);
}
[data-testid="stSidebar"] {
    background: var(--navy) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: #E8ECF4 !important; }
[data-testid="stSidebar"] .stButton > button {
    background: var(--orange) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--orange2) !important;
}

/* Tabs */
[data-testid="stTabsTabList"] {
    background: var(--white) !important;
    border-bottom: 2px solid var(--border) !important;
    border-radius: var(--radius) var(--radius) 0 0;
    padding: 0 8px;
    box-shadow: var(--shadow);
}
button[data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.84rem !important;
    font-weight: 500 !important;
    color: var(--mid) !important;
    padding: 11px 18px !important;
    border-bottom: 3px solid transparent !important;
    background: transparent !important;
    border-radius: 0 !important;
}
button[aria-selected="true"][data-baseweb="tab"] {
    color: var(--orange) !important;
    border-bottom: 3px solid var(--orange) !important;
    font-weight: 700 !important;
}
[data-testid="stTabPanel"] {
    background: transparent !important;
    padding: 22px 0 0 0 !important;
    border: none !important;
}

/* Metrics */
[data-testid="metric-container"] {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 18px 20px !important;
    box-shadow: var(--shadow) !important;
    border-top: 3px solid var(--orange) !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.8px !important;
    color: var(--mid) !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.65rem !important;
    font-weight: 700 !important;
    color: var(--txt) !important;
}

/* Cards */
.pwc-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 22px;
    box-shadow: var(--shadow);
    margin-bottom: 14px;
}
.section-hdr {
    display: flex; align-items: center; gap: 10px;
    margin: 26px 0 14px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}
.section-bar { width:4px; height:20px; background:var(--orange); border-radius:2px; flex-shrink:0; }
.section-title { font-size:.88rem; font-weight:700; letter-spacing:.4px; color:var(--txt); text-transform:uppercase; }
.section-sub { font-size:.72rem; color:var(--dim); margin-left:4px; }

.chart-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 18px 18px 8px 18px;
    box-shadow: var(--shadow);
    margin-bottom: 4px;
}
.chart-label { font-size:.68rem; font-weight:700; text-transform:uppercase; letter-spacing:.7px; color:var(--dim); margin-bottom:2px; }
.chart-title { font-size:.92rem; font-weight:700; color:var(--txt); margin-bottom:2px; }
.chart-sub   { font-size:.72rem; color:var(--dim); margin-bottom:10px; }
.source-link { font-size:.68rem; color:var(--blue); margin-top:4px; }

/* Policy cards */
.pol-card {
    background: var(--white); border: 1px solid var(--border);
    border-left: 4px solid var(--blue); border-radius: var(--radius);
    padding: 14px 18px; box-shadow: var(--shadow); margin-bottom: 12px;
}
.pol-card.warn  { border-left-color: var(--orange); }
.pol-card.ok    { border-left-color: #1A8C5B; }
.pol-card-title { font-size:.7rem; font-weight:700; text-transform:uppercase; letter-spacing:.6px; color:var(--mid); margin-bottom:7px; }
.pol-card p, .pol-card li {
    font-size:.82rem; color:var(--txt); line-height:1.65; margin:0;
    word-wrap:break-word; overflow-wrap:break-word; white-space:normal;
}
.pol-card ul { margin:5px 0 0 0; padding-left:15px; }

/* Sidebar links */
.sb-hdr {
    font-size:.6rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase;
    color:rgba(255,255,255,0.38) !important; margin:16px 0 6px 0;
    padding-bottom:4px; border-bottom:1px solid rgba(255,255,255,0.1);
}
.sb-link {
    display:block; padding:7px 11px; margin:3px 0;
    border-radius:6px; font-size:.77rem;
    color:#C8D3E8 !important; text-decoration:none !important;
    border:1px solid rgba(255,255,255,0.08);
    background:rgba(255,255,255,0.04);
    word-wrap:break-word; overflow-wrap:break-word; white-space:normal;
    transition:all .15s;
}
.sb-link:hover {
    background:rgba(208,74,2,0.2); border-color:rgba(208,74,2,0.5);
    color:#fff !important;
}

/* News */
.news-wrap { background:var(--white); border:1px solid var(--border); border-radius:var(--radius); overflow:hidden; box-shadow:var(--shadow); }
.news-hdr  { background:var(--navy); padding:11px 16px; display:flex; align-items:center; gap:10px; }
.news-hdr-title { font-size:.78rem; font-weight:600; color:#fff; letter-spacing:.4px; text-transform:uppercase; }
.news-badge { background:var(--orange); color:#fff; font-size:.58rem; font-weight:700; padding:2px 8px; border-radius:20px; letter-spacing:.5px; text-transform:uppercase; }
.news-item  { padding:13px 16px; border-bottom:1px solid var(--border); transition:background .15s; }
.news-item:last-child { border-bottom:none; }
.news-item:hover { background:#FAFBFC; }
.news-title-a {
    font-size:.83rem; font-weight:500; color:var(--txt) !important;
    text-decoration:none !important; line-height:1.55; display:block;
    word-wrap:break-word; overflow-wrap:break-word; word-break:break-word; white-space:normal;
}
.news-title-a:hover { color:var(--orange) !important; }
.news-meta  { font-size:.68rem; color:var(--dim); margin-top:5px; word-wrap:break-word; white-space:normal; }
.news-src   { display:inline-block; background:#F0F3F8; color:var(--navy); font-size:.6rem; font-weight:600; padding:1px 7px; border-radius:4px; margin-right:5px; }
.news-empty { padding:28px 16px; text-align:center; color:var(--dim); font-size:.8rem; line-height:1.8; }

/* Fallback badge */
.fallback-badge {
    display:inline-flex; align-items:center; gap:6px;
    background:#FFF3ED; border:1px solid #F0C4AC; border-radius:20px;
    padding:4px 14px; font-size:.72rem; font-weight:600; color:var(--orange);
    margin-bottom:14px;
}

#MainMenu, footer, header { visibility:hidden; }
[data-testid="stToolbar"] { display:none; }
.block-container { padding-top:0 !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 2. CHART THEME
# ══════════════════════════════════════════════════════════════════════════════
PwC_COLORS = ["#D04A02","#21325B","#295BA5","#EB6C2D","#4C7FA8","#8BA7C4","#C0C8D8","#F0C4AC"]

CHART_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#2D3142", size=12),
    margin=dict(l=50, r=16, t=20, b=50),
    legend=dict(bgcolor="rgba(255,255,255,.9)", bordercolor="#E2E5EB", borderwidth=1,
                font=dict(size=11), orientation="h", y=-0.22),
    xaxis=dict(gridcolor="#F0F2F5", linecolor="#E2E5EB",
               tickfont=dict(size=10, color="#9BA3B2"),
               title_font=dict(size=11, color="#5A6070")),
    yaxis=dict(gridcolor="#F0F2F5", linecolor="#E2E5EB",
               tickfont=dict(size=10, color="#9BA3B2"),
               title_font=dict(size=11, color="#5A6070")),
    hoverlabel=dict(bgcolor="white", bordercolor="#E2E5EB",
                    font=dict(family="Inter", size=12, color="#2D3142")),
)

# ══════════════════════════════════════════════════════════════════════════════
# 3. TIER-1 COUNTRY DATABASE — Top 8 Core Markets
# ══════════════════════════════════════════════════════════════════════════════
TIER1 = {
    # ── Nigeria ──────────────────────────────────────────────────────────────
    "Nigeria": {
        "flag":"🇳🇬","iso":"NGA","region":"West Africa","tier":1,
        "kpi": {
            "Annual CV Sales":    ("45,200","units/yr","+6.2% YoY","https://naddc.gov.ng"),
            "EV Penetration":     ("3.8%","of total sales","+1.2pp YoY","https://trade.gov.ng"),
            "EV Import Tariff":   ("0%","CBU EV (2023–28)","Zero-rated","https://customs.gov.ng"),
            "Diesel Price":       ("₦1,180","/litre","≈ $0.74 USD","https://pppra.gov.ng"),
        },
        "brand_share": {
            "brands":["Sinotruk","FAW","Foton","Volvo","Scania"],
            "sales": [1840,1420,980,560,410],
        },
        "trend": {
            "years":[2021,2022,2023,2024,2025,2026],
            "ice":  [38200,39500,40100,41800,43200,43800],
            "ev":   [0,80,320,820,1640,1400],
        },
        "policy": {
            "tariff":       "CBU EV commercial vehicles: 0% (2023–2028). CKD/SKD assembly: 0%. Conventional CBU: 35%.",
            "certification":"SON mandatory certification; NAFDAC for specialist vehicles; Form M import approval required.",
            "key_buyers":   "Dangote Cement (cement logistics), BUA Group (agri & chemicals), NNPC Logistics Division.",
            "risk":         "NGN/USD depreciation >60% over 18 months. Port congestion at Apapa delays clearance 3–6 weeks.",
        },
        "news_query":"Nigeria commercial vehicle OR Dangote logistics OR Nigeria EV tariff",
        "sources": {
            "trade": ("NADDC — National Automotive Design & Development Council","https://naddc.gov.ng"),
            "customs":("Nigeria Customs Service","https://customs.gov.ng"),
            "market": ("Nigeria Trade Hub","https://trade.gov.ng"),
        },
    },

    # ── South Africa ─────────────────────────────────────────────────────────
    "South Africa": {
        "flag":"🇿🇦","iso":"ZAF","region":"Southern Africa","tier":1,
        "kpi": {
            "Annual CV Sales":  ("31,500","units/yr","-2.8% YoY","https://naamsa.co.za"),
            "EV Penetration":   ("1.9%","of total sales","+0.7pp YoY","https://naamsa.co.za"),
            "Import Tariff":    ("25%","CBU standard rate","KD assembly ~12%","https://itac.org.za"),
            "Diesel Price":     ("R21.60","/litre","≈ $1.18 USD","https://www.energy.gov.za"),
        },
        "brand_share": {
            "brands":["Mercedes-Benz","Volvo","MAN","Scania","FAW"],
            "sales": [7200,6100,5800,5200,3100],
        },
        "trend": {
            "years":[2021,2022,2023,2024,2025,2026],
            "ice":  [29800,31200,32500,31800,30900,30900],
            "ev":   [0,0,120,320,540,600],
        },
        "policy": {
            "tariff":       "25% CBU import duty. APDP incentive scheme: manufacturers achieving >50% localisation receive production rebates.",
            "certification":"NRCS (National Regulator for Compulsory Specifications) mandatory LoA. Euro 5-equivalent emissions. SABS type approval.",
            "key_buyers":   "Transnet (rail + ports), Imperial Logistics, Tiger Brands distribution, Shoprite supply chain.",
            "risk":         "Load-shedding (Stage 2–4) disrupts EV charging infrastructure rollout. ZAR/USD pressure at ~18.5.",
        },
        "news_query":"South Africa commercial truck OR Transnet logistics OR South Africa HCV sales",
        "sources": {
            "trade": ("NAAMSA — Automotive Business Council","https://naamsa.co.za"),
            "customs":("ITAC — International Trade Administration Commission","https://itac.org.za"),
            "market": ("NRCS — National Regulator for Compulsory Specifications","https://www.nrcs.org.za"),
        },
    },

    # ── Morocco ──────────────────────────────────────────────────────────────
    "Morocco": {
        "flag":"🇲🇦","iso":"MAR","region":"North Africa","tier":1,
        "kpi": {
            "Annual CV Sales":  ("18,400","units/yr","+8.5% YoY","http://www.aivam.ma"),
            "EV Penetration":   ("2.1%","of total sales","+0.9pp YoY","http://www.aivam.ma"),
            "EV Import Tariff": ("2.5%","EU AA Agreement","Lowest in region","https://www.douane.gov.ma"),
            "Diesel Price":     ("MAD 13.50","/litre","≈ $1.34 USD","https://www.onhym.com"),
        },
        "brand_share": {
            "brands":["Renault Trucks","Mercedes-Benz","Volvo","Sinotruk","MAN"],
            "sales": [4200,3600,3100,2800,2100],
        },
        "trend": {
            "years":[2021,2022,2023,2024,2025,2026],
            "ice":  [14200,15100,16200,17400,18000,18000],
            "ev":   [0,40,120,260,380,400],
        },
        "policy": {
            "tariff":       "EU Association Agreement: CBU tariff 2.5%. EV treated equally. No dedicated KD incentive scheme.",
            "certification":"CNEAT (Centre National d'Essais et d'Homologation): UN-ECE mutual recognition. EU-certified vehicles fast-track approval.",
            "key_buyers":   "OCP Group (phosphate mining, 800+ units/yr), ONCF (national rail logistics), Casablanca Port operators.",
            "risk":         "Market limited vs Sub-Sahara; European brands hold >65% share; Chinese brands need local after-sales investment.",
        },
        "news_query":"Morocco OCP Group trucks OR Morocco transport logistics OR AIVAM véhicules utilitaires",
        "sources": {
            "trade": ("AIVAM — Association des Importateurs de Véhicules au Maroc","http://www.aivam.ma"),
            "customs":("Direction Générale des Douanes","https://www.douane.gov.ma"),
            "market": ("CNEAT — Centre National d'Essais et d'Homologation","https://www.cneat.ma"),
        },
    },

    # ── Egypt ─────────────────────────────────────────────────────────────────
    "Egypt": {
        "flag":"🇪🇬","iso":"EGY","region":"North Africa","tier":1,
        "kpi": {
            "Annual CV Sales":  ("25,800","units/yr","+11.2% YoY","https://www.eos.org.eg"),
            "EV Penetration":   ("0.8%","of total sales","+0.3pp YoY","https://www.eos.org.eg"),
            "CBU Tariff":       ("40%","standard rate","KD at 5% (>40% local)","https://www.goeic.gov.eg"),
            "Diesel Price":     ("EGP 9.75","/litre (subsidised)","≈ $0.20 USD","https://www.mop.gov.eg"),
        },
        "brand_share": {
            "brands":["Sinotruk","SAIC Maxus","Foton","Mercedes-Benz","MAN"],
            "sales": [6200,4800,3900,3500,2800],
        },
        "trend": {
            "years":[2021,2022,2023,2024,2025,2026],
            "ice":  [18000,20500,22100,24800,25600,25600],
            "ev":   [0,0,60,130,200,200],
        },
        "policy": {
            "tariff":       "CBU standard: 40%. KD assembly with >40% localisation: 5%. SCZone (Suez Canal Zone) production: 0%.",
            "certification":"EOS (Egyptian Organisation for Standardisation) mandatory; GOEIC import licence; SCZone investors get simplified clearance.",
            "key_buyers":   "EGPC (Egyptian General Petroleum Corp) logistics, SCZone construction contractors, private building materials distributors.",
            "risk":         "EGP depreciated >50% in 2 years; FX controls delay import payments 45–90 days; bureaucratic KD approval process.",
        },
        "news_query":"Egypt commercial vehicle market OR Egypt logistics EV OR Suez Economic Zone trucks",
        "sources": {
            "trade": ("EOS — Egyptian Organisation for Standardisation","https://www.eos.org.eg"),
            "customs":("GOEIC — General Organisation for Export & Import Control","https://www.goeic.gov.eg"),
            "market": ("IDSC — Information and Decision Support Center","https://www.idsc.gov.eg"),
        },
    },

    # ── Kenya ─────────────────────────────────────────────────────────────────
    "Kenya": {
        "flag":"🇰🇪","iso":"KEN","region":"East Africa","tier":1,
        "kpi": {
            "Annual CV Sales":  ("14,200","units/yr","+9.4% YoY","https://kebs.org"),
            "EV Penetration":   ("2.6%","of total sales","+1.1pp YoY","https://kebs.org"),
            "Import Duty":      ("25%","EAC CET standard","COMESA preference 0%","https://kra.go.ke"),
            "Diesel Price":     ("KES 188","/litre","≈ $1.42 USD","https://www.epra.go.ke"),
        },
        "brand_share": {
            "brands":["Isuzu","Toyota","Foton","Sinotruk","Volvo"],
            "sales": [3800,2900,2400,2100,1200],
        },
        "trend": {
            "years":[2021,2022,2023,2024,2025,2026],
            "ice":  [10800,11500,12200,13100,13800,13900],
            "ev":   [0,20,80,210,340,370],
        },
        "policy": {
            "tariff":       "EAC Common External Tariff: 25%. COMESA member states: 0%. EV import: currently 25% (policy review underway).",
            "certification":"KEBS (Kenya Bureau of Standards) mandatory PVoC inspection at origin; NTSA vehicle inspection on arrival.",
            "key_buyers":   "Kenya Ports Authority (Mombasa logistics), East African Breweries, Bamburi Cement, SGR (Standard Gauge Railway feeder).",
            "risk":         "KES depreciation ~20% (2023–2024); SGR freight competition reducing some long-haul truck demand.",
        },
        "news_query":"Kenya commercial vehicle OR Kenya logistics truck OR Nairobi freight transport",
        "sources": {
            "trade": ("KEBS — Kenya Bureau of Standards","https://kebs.org"),
            "customs":("KRA — Kenya Revenue Authority","https://kra.go.ke"),
            "market": ("EPRA — Energy & Petroleum Regulatory Authority","https://www.epra.go.ke"),
        },
    },

    # ── Ethiopia ──────────────────────────────────────────────────────────────
    "Ethiopia": {
        "flag":"🇪🇹","iso":"ETH","region":"East Africa","tier":1,
        "kpi": {
            "Annual CV Sales":  ("9,800","units/yr","+22.1% YoY","https://www.moti.gov.et"),
            "EV Penetration":   ("8.4%","of total sales","+4.2pp YoY","https://www.moti.gov.et"),
            "EV Import Duty":   ("0%","Petroleum vehicle ban","ICE ban since 2022","https://www.erca.gov.et"),
            "Electricity Price":("ETB 1.42","/kWh","≈ $0.025 USD","https://www.eepco.gov.et"),
        },
        "brand_share": {
            "brands":["BYD","Foton EV","King Long EV","Sinotruk","Skywell"],
            "sales": [2800,2100,1600,1200,800],
        },
        "trend": {
            "years":[2021,2022,2023,2024,2025,2026],
            "ice":  [7200,6800,5400,3200,1800,1200],
            "ev":   [200,800,2800,5800,7400,8200],
        },
        "policy": {
            "tariff":       "Ethiopia BANNED petroleum-powered vehicle imports (2022). EV import duty: 0%. Strict enforcement by ERCA.",
            "certification":"EthSA (Ethiopian Standards Agency); EV charging infrastructure under national grid expansion programme.",
            "key_buyers":   "Ethiopian Roads Authority (infrastructure logistics), Ethiopian Airlines cargo, Ethio Telecom fleet.",
            "risk":         "Limited charging infrastructure outside Addis Ababa; internal conflict (Tigray) disrupts northern supply routes.",
        },
        "news_query":"Ethiopia EV commercial vehicle OR Ethiopia petroleum ban trucks OR Addis Ababa logistics",
        "sources": {
            "trade": ("MoTI — Ministry of Trade & Industry Ethiopia","https://www.moti.gov.et"),
            "customs":("ERCA — Ethiopian Revenue & Customs Authority","https://www.erca.gov.et"),
            "market": ("EthSA — Ethiopian Standards Agency","https://www.ethsa.gov.et"),
        },
    },

    # ── Algeria ───────────────────────────────────────────────────────────────
    "Algeria": {
        "flag":"🇩🇿","iso":"DZA","region":"North Africa","tier":1,
        "kpi": {
            "Annual CV Sales":  ("12,600","units/yr","+4.8% YoY","https://www.dz.gov.dz"),
            "EV Penetration":   ("0.4%","of total sales","Early-stage","https://www.dz.gov.dz"),
            "Import Tariff":    ("30%","CBU standard","CKD benefits available","https://www.douane.gov.dz"),
            "Diesel Price":     ("DZD 45","/litre (subsidised)","≈ $0.33 USD","https://www.energy.gov.dz"),
        },
        "brand_share": {
            "brands":["Mercedes-Benz","Renault Trucks","MAN","Sinotruk","Volvo"],
            "sales": [3200,2800,2400,2000,1400],
        },
        "trend": {
            "years":[2021,2022,2023,2024,2025,2026],
            "ice":  [10200,10800,11400,12000,12400,12400],
            "ev":   [0,0,20,40,60,60],
        },
        "policy": {
            "tariff":       "30% CBU tariff. Government permits CKD/SKD assembly partnerships; Renault Trucks has existing JV in Rouiba.",
            "certification":"IANOR (Institut Algérien de Normalisation); Euro 3 minimum emission standard (upgrade to Euro 4 underway).",
            "key_buyers":   "Sonatrach (oil & gas logistics), SNVI (national vehicle manufacturer), Ministry of Public Works infrastructure.",
            "risk":         "Heavy protectionism; foreign exchange controls; import licence quotas create supply uncertainty.",
        },
        "news_query":"Algeria commercial vehicle market OR Algérie transport logistique OR Sonatrach fleet",
        "sources": {
            "trade": ("Ministère du Commerce — Algeria","https://www.commerce.gov.dz"),
            "customs":("Direction Générale des Douanes","https://www.douane.gov.dz"),
            "market": ("IANOR — Institut Algérien de Normalisation","https://www.ianor.dz"),
        },
    },

    # ── Tunisia ───────────────────────────────────────────────────────────────
    "Tunisia": {
        "flag":"🇹🇳","iso":"TUN","region":"North Africa","tier":1,
        "kpi": {
            "Annual CV Sales":  ("8,100","units/yr","+3.1% YoY","https://www.innorpi.tn"),
            "EV Penetration":   ("1.2%","of total sales","+0.4pp YoY","https://www.innorpi.tn"),
            "Import Tariff":    ("10%","EU Association Agreement","Lowest tier","https://www.douane.gov.tn"),
            "Diesel Price":     ("TND 2.10","/litre (subsidised)","≈ $0.67 USD","https://www.industrie.gov.tn"),
        },
        "brand_share": {
            "brands":["Mercedes-Benz","Renault Trucks","MAN","Volvo","Sinotruk"],
            "sales": [2100,1800,1500,1200,900],
        },
        "trend": {
            "years":[2021,2022,2023,2024,2025,2026],
            "ice":  [6800,7100,7400,7800,8000,8000],
            "ev":   [0,20,40,70,100,100],
        },
        "policy": {
            "tariff":       "EU Association Agreement: ~10% tariff. UN-ECE mutual recognition removes need for re-certification of EU-approved vehicles.",
            "certification":"INNORPI (Institut National de la Normalisation et de la Propriété Industrielle); ATTT road transport authority approval.",
            "key_buyers":   "CPG (Compagnie des Phosphates de Gafsa), Port of Tunis operators, private food & textile logistics.",
            "risk":         "Small total market; European brands dominate >70% share; Chinese brands need strong local after-sales presence.",
        },
        "news_query":"Tunisie transport logistique camions OR Tunisia freight commercial vehicle",
        "sources": {
            "trade": ("INNORPI — Institut National de la Normalisation","https://www.innorpi.tn"),
            "customs":("Direction Générale des Douanes — Tunisie","https://www.douane.gov.tn"),
            "market": ("ATTT — Agence Technique des Transports Terrestres","https://www.attt.tn"),
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 4. FULL 54-NATION ISO MAPPING + METADATA
# ══════════════════════════════════════════════════════════════════════════════
ALL_AFRICA = {
    # Tier 1 (full data above)
    "NGA":"Nigeria","ZAF":"South Africa","MAR":"Morocco","EGY":"Egypt",
    "KEN":"Kenya","ETH":"Ethiopia","DZA":"Algeria","TUN":"Tunisia",
    # Tier 2 — fallback
    "GHA":"Ghana","TZA":"Tanzania","UGA":"Uganda","RWA":"Rwanda",
    "SEN":"Senegal","CIV":"Côte d'Ivoire","CMR":"Cameroon","ZMB":"Zambia",
    "ZWE":"Zimbabwe","MOZ":"Mozambique","MDG":"Madagascar","MWI":"Malawi",
    "NAM":"Namibia","BWA":"Botswana","AGO":"Angola","LBY":"Libya",
    "SDN":"Sudan","SSD":"South Sudan","SOM":"Somalia","ERI":"Eritrea",
    "DJI":"Djibouti","BDI":"Burundi","COM":"Comoros","STP":"São Tomé & Príncipe",
    "SWZ":"Eswatini","LSO":"Lesotho","MUS":"Mauritius","CPV":"Cabo Verde",
    "SLE":"Sierra Leone","LBR":"Liberia","GIN":"Guinea","GNB":"Guinea-Bissau",
    "GMB":"Gambia","GNQ":"Equatorial Guinea","GAB":"Gabon","COG":"Congo",
    "COD":"DR Congo","CAF":"Central African Republic","TCD":"Chad",
    "NER":"Niger","MLI":"Mali","BFA":"Burkina Faso","BEN":"Benin",
    "TGO":"Togo","NGA2":"Nigeria","MRT":"Mauritania","ESH":"Western Sahara",
}
# Remove duplicate
ALL_AFRICA.pop("NGA2", None)

# Tier-2 macro estimates (GDP USD bn, road km '000, CV imports est.)
TIER2_MACRO = {
    "GHA": {"gdp":75.5,"roads":72,"cv_imports":8200,"flag":"🇬🇭","region":"West Africa"},
    "TZA": {"gdp":80.0,"roads":87,"cv_imports":9100,"flag":"🇹🇿","region":"East Africa"},
    "UGA": {"gdp":51.0,"roads":21,"cv_imports":5400,"flag":"🇺🇬","region":"East Africa"},
    "RWA": {"gdp":13.8,"roads":15,"cv_imports":3600,"flag":"🇷🇼","region":"East Africa"},
    "SEN": {"gdp":32.0,"roads":16,"cv_imports":4200,"flag":"🇸🇳","region":"West Africa"},
    "CIV": {"gdp":73.0,"roads":81,"cv_imports":7800,"flag":"🇨🇮","region":"West Africa"},
    "CMR": {"gdp":48.0,"roads":77,"cv_imports":5200,"flag":"🇨🇲","region":"Central Africa"},
    "ZMB": {"gdp":29.0,"roads":40,"cv_imports":3800,"flag":"🇿🇲","region":"Southern Africa"},
    "ZWE": {"gdp":28.0,"roads":97,"cv_imports":3200,"flag":"🇿🇼","region":"Southern Africa"},
    "MOZ": {"gdp":18.0,"roads":31,"cv_imports":2800,"flag":"🇲🇿","region":"Southern Africa"},
    "MDG": {"gdp":14.5,"roads":32,"cv_imports":2100,"flag":"🇲🇬","region":"Southern Africa"},
    "MWI": {"gdp":12.6,"roads":16,"cv_imports":1800,"flag":"🇲🇼","region":"Southern Africa"},
    "NAM": {"gdp":12.8,"roads":48,"cv_imports":3400,"flag":"🇳🇦","region":"Southern Africa"},
    "BWA": {"gdp":18.6,"roads":31,"cv_imports":2900,"flag":"🇧🇼","region":"Southern Africa"},
    "AGO": {"gdp":102.0,"roads":76,"cv_imports":6800,"flag":"🇦🇴","region":"Southern Africa"},
    "LBY": {"gdp":52.0,"roads":34,"cv_imports":4100,"flag":"🇱🇾","region":"North Africa"},
    "SDN": {"gdp":45.0,"roads":24,"cv_imports":3600,"flag":"🇸🇩","region":"East Africa"},
    "SSD": {"gdp":4.6,"roads":9,"cv_imports":800,"flag":"🇸🇸","region":"East Africa"},
    "SOM": {"gdp":8.0,"roads":22,"cv_imports":1200,"flag":"🇸🇴","region":"East Africa"},
    "ERI": {"gdp":2.1,"roads":14,"cv_imports":400,"flag":"🇪🇷","region":"East Africa"},
    "DJI": {"gdp":3.9,"roads":3,"cv_imports":600,"flag":"🇩🇯","region":"East Africa"},
    "BDI": {"gdp":3.1,"roads":14,"cv_imports":500,"flag":"🇧🇮","region":"East Africa"},
    "COM": {"gdp":1.4,"roads":1,"cv_imports":120,"flag":"🇰🇲","region":"East Africa"},
    "STP": {"gdp":0.6,"roads":0.3,"cv_imports":60,"flag":"🇸🇹","region":"Central Africa"},
    "SWZ": {"gdp":4.8,"roads":4,"cv_imports":650,"flag":"🇸🇿","region":"Southern Africa"},
    "LSO": {"gdp":2.9,"roads":6,"cv_imports":420,"flag":"🇱🇸","region":"Southern Africa"},
    "MUS": {"gdp":14.2,"roads":2,"cv_imports":1800,"flag":"🇲🇺","region":"Southern Africa"},
    "CPV": {"gdp":2.2,"roads":1.5,"cv_imports":280,"flag":"🇨🇻","region":"West Africa"},
    "SLE": {"gdp":4.0,"roads":11,"cv_imports":620,"flag":"🇸🇱","region":"West Africa"},
    "LBR": {"gdp":3.8,"roads":10,"cv_imports":540,"flag":"🇱🇷","region":"West Africa"},
    "GIN": {"gdp":16.0,"roads":44,"cv_imports":1800,"flag":"🇬🇳","region":"West Africa"},
    "GNB": {"gdp":1.7,"roads":4,"cv_imports":200,"flag":"🇬🇼","region":"West Africa"},
    "GMB": {"gdp":2.1,"roads":4,"cv_imports":320,"flag":"🇬🇲","region":"West Africa"},
    "GNQ": {"gdp":10.7,"roads":3,"cv_imports":840,"flag":"🇬🇶","region":"Central Africa"},
    "GAB": {"gdp":19.0,"roads":9,"cv_imports":1400,"flag":"🇬🇦","region":"Central Africa"},
    "COG": {"gdp":12.0,"roads":17,"cv_imports":980,"flag":"🇨🇬","region":"Central Africa"},
    "COD": {"gdp":65.0,"roads":152,"cv_imports":5800,"flag":"🇨🇩","region":"Central Africa"},
    "CAF": {"gdp":2.5,"roads":24,"cv_imports":380,"flag":"🇨🇫","region":"Central Africa"},
    "TCD": {"gdp":11.2,"roads":40,"cv_imports":1200,"flag":"🇹🇩","region":"Central Africa"},
    "NER": {"gdp":16.5,"roads":19,"cv_imports":1400,"flag":"🇳🇪","region":"West Africa"},
    "MLI": {"gdp":19.2,"roads":22,"cv_imports":1800,"flag":"🇲🇱","region":"West Africa"},
    "BFA": {"gdp":20.4,"roads":15,"cv_imports":1600,"flag":"🇧🇫","region":"West Africa"},
    "BEN": {"gdp":17.8,"roads":16,"cv_imports":2100,"flag":"🇧🇯","region":"West Africa"},
    "TGO": {"gdp":9.0,"roads":11,"cv_imports":1200,"flag":"🇹🇬","region":"West Africa"},
    "GHA": {"gdp":75.5,"roads":72,"cv_imports":8200,"flag":"🇬🇭","region":"West Africa"},
    "MRT": {"gdp":9.9,"roads":12,"cv_imports":800,"flag":"🇲🇷","region":"West Africa"},
    "ESH": {"gdp":2.4,"roads":6,"cv_imports":180,"flag":"🏳","region":"North Africa"},
}

# Canonical ISO→name
ISO_TO_NAME = {d["iso"]: name for name, d in TIER1.items()}
# Add tier2
for iso, name in ALL_AFRICA.items():
    if iso not in ISO_TO_NAME:
        ISO_TO_NAME[iso] = name

ALL_ISO_LIST = list(dict.fromkeys(list(ISO_TO_NAME.keys())))

# ══════════════════════════════════════════════════════════════════════════════
# 5. NEWS FETCHER
# ══════════════════════════════════════════════════════════════════════════════
TRUSTED = (
    "site:reuters.com OR site:bloomberg.com OR site:ft.com "
    "OR site:engineeringnews.co.za OR site:businessday.ng "
    "OR site:zawya.com OR site:afdb.org OR site:apanews.net "
    "OR site:theafricareport.com OR site:africanews.com"
)
NOISE = {"rumor","rumour","unconfirmed","alleged","shocking","viral","leaked","clickbait"}

@st.cache_data(ttl=1800)
def fetch_news(query: str, limit: int = 7) -> list:
    full_q = f"({query}) ({TRUSTED}) when:30d"
    encoded = full_q.replace(" ", "+").replace('"', "%22")
    url = (f"https://news.google.com/rss/search"
           f"?q={encoded}&hl=en-US&gl=US&ceid=US:en")
    cutoff = datetime.utcnow() - timedelta(days=30)
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries:
            if len(items) >= limit:
                break
            title = entry.get("title", "")
            if not title or any(n in title.lower() for n in NOISE):
                continue
            pub_str, pub_dt = "–", None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                pub_dt  = datetime(*entry.published_parsed[:6])
                pub_str = pub_dt.strftime("%Y-%m-%d")
            if pub_dt and pub_dt < cutoff:
                continue
            items.append({"title": title, "link": entry.get("link","#"),
                           "published": pub_str, "pub_dt": pub_dt,
                           "source": entry.get("source",{}).get("title","–")})
        items.sort(key=lambda x: x["pub_dt"] or datetime.min, reverse=True)
        return items
    except Exception:
        return []

# ══════════════════════════════════════════════════════════════════════════════
# 6. SIMULATED DATA GENERATORS
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def gen_za_rail_road():
    """South Africa: Transnet rail decline vs HCV road surge — Scissors Effect"""
    np.random.seed(1)
    years = list(range(2018, 2027))
    rail  = [228,218,204,189,171,158,142,131,122]  # Mt
    road  = [27500,28200,29800,30400,31200,32500,31800,30900,30900]
    return pd.DataFrame({"Year":years,"Transnet Rail (Mt)":rail,"HCV Road Sales (units)":road})

@st.cache_data
def gen_ng_tariff_waterfall():
    """Nigeria: CBU vs SKD vs CKD cost waterfall"""
    np.random.seed(2)
    categories = ["CBU\nBase Price","CBU\nImport Duty\n(35%)","CBU\nPort &\nClearance","CBU\nTotal Cost",
                  "CKD\nBase Price","CKD\nImport Duty\n(0%)","CKD\nAssembly\nCost","CKD\nTotal Cost"]
    values     = [100000, 35000, 8000, 143000,
                  85000,  0,     12000, 97000]
    types      = ["base","positive","positive","total",
                  "base","zero","positive","total"]
    return pd.DataFrame({"Category":categories,"Value":values,"Type":types})

@st.cache_data
def gen_ocp_throughput():
    """Morocco: OCP phosphate road freight throughput"""
    np.random.seed(3)
    months = pd.date_range("2023-01-01","2026-05-01",freq="MS")
    n = len(months)
    trend    = np.linspace(820,1380,n)
    seasonal = 90*np.sin(np.linspace(0,6.5*np.pi,n))
    noise    = np.random.normal(0,35,n)
    return pd.DataFrame({"Month":months,"Throughput (kt)":(trend+seasonal+noise).clip(min=500).round(1)})

@st.cache_data
def gen_eth_ev_surge():
    """Ethiopia: EV penetration surge post petroleum ban"""
    np.random.seed(4)
    months = pd.date_range("2021-01-01","2026-05-01",freq="MS")
    n = len(months)
    ban_idx = 18  # mid-2022
    ev_pct  = np.concatenate([
        np.linspace(0.5, 3.0, ban_idx),
        np.linspace(3.0,92.0, n-ban_idx) + np.random.normal(0,2,n-ban_idx)
    ]).clip(0,100)
    return pd.DataFrame({"Month":months,"EV Share (%)":ev_pct.round(1)})

# ══════════════════════════════════════════════════════════════════════════════
# 7. MAP BUILDER — Full 54-nation, click-anywhere
# ══════════════════════════════════════════════════════════════════════════════
def build_map(selected_name: str) -> go.Figure:
    selected_iso = next((d["iso"] for d in TIER1.values()
                         if list(TIER1.keys())[list(TIER1.values()).index(d)] == selected_name), "")
    # Also check tier2
    for iso, name in ALL_AFRICA.items():
        if name == selected_name:
            selected_iso = iso
            break

    rows = []
    for iso in ALL_ISO_LIST:
        name = ISO_TO_NAME.get(iso, iso)
        is_t1   = name in TIER1
        is_sel  = (iso == selected_iso)

        if is_sel:
            score, color_group = 100, "selected"
        elif is_t1:
            score, color_group = 70, "tier1"
        else:
            score, color_group = 20, "base"

        # Tooltip
        if is_t1:
            d = TIER1[name]
            kpi_text = "<br>".join(
                f"<b>{v[0]}</b> {v[1]}" for v in d["kpi"].values()
            )
            tip = (f"<b style='font-size:13px;'>{d['flag']} {name}</b><br>"
                   f"<span style='color:#9BA3B2;font-size:10px;'>TIER 1 · {d['region']}</span><br><br>"
                   f"{kpi_text}<br><br>"
                   f"<span style='color:#D04A02;font-size:10px;'>● Click to drill down</span>")
        else:
            m = TIER2_MACRO.get(iso, {})
            flag = m.get("flag","🏳")
            region = m.get("region","Africa")
            gdp  = m.get("gdp","N/A")
            cvs  = m.get("cv_imports","N/A")
            roads= m.get("roads","N/A")
            tip = (f"<b style='font-size:13px;'>{flag} {name}</b><br>"
                   f"<span style='color:#9BA3B2;font-size:10px;'>{region}</span><br><br>"
                   f"Est. GDP: <b>${gdp}B</b><br>"
                   f"Est. CV Imports: <b>{cvs:,} units/yr</b><br>"
                   f"Road Network: <b>{roads}k km</b><br><br>"
                   f"<span style='color:#295BA5;font-size:10px;'>● Click for live news</span>")

        rows.append({"iso":iso,"name":name,"score":score,
                     "group":color_group,"tooltip":tip})

    df = pd.DataFrame(rows)

    fig = go.Figure()

    # Layer 1: base countries
    dfb = df[df.group=="base"]
    if not dfb.empty:
        fig.add_trace(go.Choropleth(
            locations=dfb.iso, z=dfb.score,
            text=dfb.tooltip, hovertemplate="%{text}<extra></extra>",
            colorscale=[[0,"#E8ECF4"],[1,"#D0D6E2"]],
            showscale=False,
            marker_line_color="#C8CDD8", marker_line_width=0.5,
            zmin=0, zmax=100,
        ))

    # Layer 2: Tier-1 non-selected
    dft = df[df.group=="tier1"]
    if not dft.empty:
        fig.add_trace(go.Choropleth(
            locations=dft.iso, z=dft.score,
            text=dft.tooltip, hovertemplate="%{text}<extra></extra>",
            colorscale=[[0,"#6E90BF"],[1,"#295BA5"]],
            showscale=False,
            marker_line_color="#21325B", marker_line_width=0.9,
            zmin=0, zmax=100,
        ))

    # Layer 3: selected country (orange)
    dfs = df[df.group=="selected"]
    if not dfs.empty:
        fig.add_trace(go.Choropleth(
            locations=dfs.iso, z=dfs.score,
            text=dfs.tooltip, hovertemplate="%{text}<extra></extra>",
            colorscale=[[0,"#D04A02"],[1,"#EB6C2D"]],
            showscale=False,
            marker_line_color="#8B3000", marker_line_width=2.0,
            zmin=0, zmax=100,
        ))

    fig.update_layout(
        geo=dict(
            scope="africa", showframe=False,
            showcoastlines=True, coastlinecolor="#C8CDD8", coastlinewidth=0.6,
            showland=True, landcolor="#F0F2F6",
            showocean=True, oceancolor="#E4EEF8",
            showcountries=True, countrycolor="#C8CDD8", countrywidth=0.5,
            bgcolor="#F4F5F7", projection_type="natural earth",
        ),
        paper_bgcolor="#F4F5F7", plot_bgcolor="#F4F5F7",
        margin=dict(l=0,r=0,t=0,b=0), height=420,
        hoverlabel=dict(bgcolor="white", bordercolor="#E2E5EB",
                        font=dict(family="Inter", size=12, color="#2D3142")),
        dragmode=False,
    )
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# 8. CHART BUILDERS
# ══════════════════════════════════════════════════════════════════════════════
def chart_brand_bar(cdata: dict, country: str) -> go.Figure:
    brands = cdata["brand_share"]["brands"]
    sales  = cdata["brand_share"]["sales"]
    total  = sum(sales)
    pcts   = [round(s/total*100,1) for s in sales]
    colors = [PwC_COLORS[0] if i==0 else PwC_COLORS[1] if i==1
              else PwC_COLORS[2] if i==2 else "#C0C8D8" for i in range(len(brands))]
    fig = go.Figure(go.Bar(
        x=brands, y=sales,
        text=[f"{p}%" for p in pcts], textposition="outside",
        textfont=dict(size=11, color="#2D3142", family="Inter"),
        marker=dict(color=colors, line=dict(color="white",width=1.5)),
        hovertemplate="<b>%{x}</b><br>Sales: <b>%{y:,}</b><br>Share: <b>%{text}</b><extra></extra>",
    ))
    layout = {**CHART_BASE}
    layout["yaxis"] = {**CHART_BASE["yaxis"],"title":"Units","range":[0,max(sales)*1.22]}
    layout["xaxis"] = {**CHART_BASE["xaxis"],"title":"Brand"}
    layout["showlegend"] = False
    layout["bargap"] = 0.38
    fig.update_layout(**layout)
    return fig

def chart_trend_area(cdata: dict) -> go.Figure:
    years = cdata["trend"]["years"]
    ice   = cdata["trend"]["ice"]
    ev    = cdata["trend"]["ev"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=ice, name="ICE (Conventional)",
        mode="lines+markers",
        line=dict(color="#21325B",width=2.5), marker=dict(size=6,color="#21325B"),
        fill="tozeroy", fillcolor="rgba(33,50,91,0.08)",
        hovertemplate="<b>%{x}</b><br>ICE: <b>%{y:,}</b> units<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=years, y=ev, name="EV / New Energy",
        mode="lines+markers",
        line=dict(color="#D04A02",width=2.5), marker=dict(size=7,color="#D04A02",symbol="diamond"),
        fill="tozeroy", fillcolor="rgba(208,74,2,0.10)",
        hovertemplate="<b>%{x}</b><br>EV: <b>%{y:,}</b> units<extra></extra>",
    ))
    fig.add_vline(x=2025.5, line_dash="dash", line_color="#9BA3B2", line_width=1)
    fig.add_annotation(x=2025.7, y=max(ice)*0.92, text="← Actual | Forecast →",
                       showarrow=False, font=dict(size=9,color="#9BA3B2",family="Inter"))
    layout = {**CHART_BASE}
    layout["xaxis"] = {**CHART_BASE["xaxis"],"title":"Year",
                       "tickmode":"array","tickvals":years}
    layout["yaxis"] = {**CHART_BASE["yaxis"],"title":"Units"}
    fig.update_layout(**layout)
    return fig

def chart_za_scissors() -> go.Figure:
    df = gen_za_rail_road()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.Year, y=df["Transnet Rail (Mt)"], name="Transnet Rail Volume (Mt)",
        mode="lines+markers", yaxis="y1",
        line=dict(color="#D04A02",width=2.5,dash="solid"),
        marker=dict(size=6,color="#D04A02"),
        fill="tozeroy", fillcolor="rgba(208,74,2,0.07)",
        hovertemplate="<b>%{x}</b><br>Rail: <b>%{y:.0f} Mt</b><extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df.Year, y=df["HCV Road Sales (units)"], name="HCV Road Sales (units)",
        mode="lines+markers", yaxis="y2",
        line=dict(color="#21325B",width=2.5),
        marker=dict(size=6,color="#21325B"),
        fill="tozeroy", fillcolor="rgba(33,50,91,0.06)",
        hovertemplate="<b>%{x}</b><br>HCV Sales: <b>%{y:,}</b> units<extra></extra>",
    ))
    # Annotate crossover
    fig.add_annotation(x=2021, y=228,
        text="Rail peak (2018: 228 Mt)", showarrow=True, arrowhead=2,
        arrowcolor="#D04A02", font=dict(size=9,color="#D04A02"), ax=60, ay=-30)
    layout = {**CHART_BASE}
    layout["xaxis"] = {**CHART_BASE["xaxis"],"title":"Year",
                       "tickmode":"array","tickvals":df.Year.tolist()}
    layout["yaxis"]  = {**CHART_BASE["yaxis"],"title":"Rail Volume (Mt)","side":"left"}
    layout["yaxis2"] = {**CHART_BASE["yaxis"],"title":"HCV Road Sales (units)",
                        "side":"right","overlaying":"y","showgrid":False}
    layout["legend"]["y"] = -0.22
    fig.update_layout(**layout)
    return fig

def chart_ng_waterfall() -> go.Figure:
    data = [
        ("CBU Base\nPrice",    100000, "absolute"),
        ("CBU Import\nDuty 35%", 35000,"relative"),
        ("CBU Port &\nClearance", 8000,"relative"),
        ("CBU Total\nLanded",   143000,"total"),
        ("CKD Base\nPrice",     85000, "absolute"),
        ("CKD Duty\n(0% EV)",       0,"relative"),
        ("CKD Assembly\nCost",  12000, "relative"),
        ("CKD Total\nCost",     97000, "total"),
    ]
    cats   = [d[0] for d in data]
    vals   = [d[1] for d in data]
    types  = [d[2] for d in data]
    colors = []
    for t, v in zip(types, vals):
        if t == "total":    colors.append("#21325B")
        elif t == "absolute": colors.append("#295BA5")
        elif v == 0:        colors.append("#1A8C5B")
        else:               colors.append("#D04A02")

    fig = go.Figure(go.Waterfall(
        orientation="v", measure=types,
        x=cats, y=vals,
        text=[f"${v:,.0f}" if v>0 else "FREE" for v in vals],
        textposition="outside",
        textfont=dict(size=10, family="Inter", color="#2D3142"),
        connector=dict(line=dict(color="#E2E5EB",width=1)),
        increasing=dict(marker_color="#D04A02"),
        decreasing=dict(marker_color="#1A8C5B"),
        totals=dict(marker_color="#21325B"),
        hovertemplate="<b>%{x}</b><br>Value: <b>$%{y:,.0f}</b><extra></extra>",
    ))
    # Saving annotation
    fig.add_annotation(
        x=7, y=97000,
        text="💡 CKD saves ~$46,000<br>per unit vs CBU",
        showarrow=True, arrowhead=2, arrowcolor="#1A8C5B",
        bgcolor="rgba(26,140,91,0.1)", bordercolor="#1A8C5B",
        font=dict(size=10, color="#1A8C5B", family="Inter"),
        ax=-80, ay=-50,
    )
    layout = {**CHART_BASE}
    layout["yaxis"]  = {**CHART_BASE["yaxis"],"title":"Cost (USD)"}
    layout["xaxis"]  = {**CHART_BASE["xaxis"],"title":""}
    layout["showlegend"] = False
    layout["margin"] = dict(l=60,r=20,t=30,b=60)
    fig.update_layout(**layout)
    return fig

def chart_ocp_throughput() -> go.Figure:
    df = gen_ocp_throughput()
    growth = (df["Throughput (kt)"].iloc[-1]/df["Throughput (kt)"].iloc[0]-1)*100
    # Trend line
    x_num = np.arange(len(df))
    z = np.polyfit(x_num, df["Throughput (kt)"], 1)
    trend = np.poly1d(z)(x_num)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.Month, y=df["Throughput (kt)"],
        name="Monthly Throughput",
        mode="lines", line=dict(color="#D04A02",width=2),
        fill="tozeroy", fillcolor="rgba(208,74,2,0.10)",
        hovertemplate="<b>%{x|%b %Y}</b><br>%{y:.0f} kt<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df.Month, y=trend,
        name="Growth Trend",
        mode="lines", line=dict(color="#21325B",width=1.5,dash="dot"),
        hovertemplate="Trend: %{y:.0f} kt<extra></extra>",
    ))
    fig.add_annotation(
        x=df.Month.iloc[-1], y=df["Throughput (kt)"].iloc[-1],
        text=f"▲ +{growth:.1f}% since Jan 2023",
        showarrow=True, arrowhead=2, arrowcolor="#D04A02",
        font=dict(size=10, color="#D04A02", family="Inter"), ax=-100, ay=-40)
    layout = {**CHART_BASE}
    layout["xaxis"] = {**CHART_BASE["xaxis"],"title":"Month"}
    layout["yaxis"] = {**CHART_BASE["yaxis"],"title":"Throughput (thousand tonnes)"}
    fig.update_layout(**layout)
    return fig

def chart_eth_ev_surge() -> go.Figure:
    df = gen_eth_ev_surge()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.Month, y=df["EV Share (%)"],
        name="EV Market Share (%)",
        mode="lines", line=dict(color="#D04A02",width=2.5),
        fill="tozeroy", fillcolor="rgba(208,74,2,0.12)",
        hovertemplate="<b>%{x|%b %Y}</b><br>EV Share: <b>%{y:.1f}%</b><extra></extra>",
    ))
    # Ban annotation
    ban_date = pd.Timestamp("2022-07-01")
    fig.add_vline(x=ban_date, line_dash="dash", line_color="#21325B", line_width=1.5)
    fig.add_annotation(
        x=ban_date, y=50,
        text="⚡ Petroleum import ban<br>enacted July 2022",
        showarrow=False, xanchor="left",
        bgcolor="rgba(33,50,91,0.08)", bordercolor="#21325B",
        font=dict(size=9, color="#21325B", family="Inter"),
        xshift=8,
    )
    layout = {**CHART_BASE}
    layout["xaxis"] = {**CHART_BASE["xaxis"],"title":"Month"}
    layout["yaxis"] = {**CHART_BASE["yaxis"],"title":"EV Market Share (%)","range":[0,105]}
    layout["showlegend"] = False
    fig.update_layout(**layout)
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# 9. SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if "selected_country" not in st.session_state:
    st.session_state.selected_country = "Nigeria"

# ══════════════════════════════════════════════════════════════════════════════
# 10. SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 4px 12px 4px;border-bottom:1px solid rgba(255,255,255,0.12);">
        <div style="font-family:'Inter';font-size:1.05rem;font-weight:700;color:white;letter-spacing:-.2px;">
            Africa CV Intelligence
        </div>
        <div style="font-family:'Inter';font-size:.68rem;color:rgba(255,255,255,.4);margin-top:2px;">
            Enterprise Market Analytics · v5.0
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-hdr">Core Markets (Tier 1)</div>', unsafe_allow_html=True)
    for cname, cd in TIER1.items():
        is_active = st.session_state.selected_country == cname
        if is_active:
            st.markdown(f"""
            <div style="padding:9px 13px;margin:3px 0;border-radius:6px;
                        background:#D04A02;border:1px solid #D04A02;
                        font-family:'Inter';font-size:.81rem;font-weight:700;color:white;">
                {cd['flag']} &nbsp;{cname}
                <span style="opacity:.7;font-size:.65rem;margin-left:6px;">● Active</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.button(f"{cd['flag']}  {cname}", key=f"sb_{cname}", use_container_width=True):
                st.session_state.selected_country = cname
                st.cache_data.clear()
                st.rerun()

    st.markdown('<div class="sb-hdr">Quick Reference Links</div>', unsafe_allow_html=True)
    for label, url in [
        ("🏛 Nigeria Customs (NCS)","https://www.customs.gov.ng"),
        ("🏦 Central Bank Nigeria","https://www.cbn.gov.ng"),
        ("🚗 AutoTrader ZA – Trucks","https://www.autotrader.co.za/trucks"),
        ("🚂 Transnet Freight Rail","https://www.transnet.net"),
        ("🌾 OCP Group Morocco","https://www.ocpgroup.ma"),
        ("🌍 AfDB — African Dev. Bank","https://www.afdb.org"),
        ("📊 Zawya Africa Finance","https://www.zawya.com"),
        ("📰 The Africa Report","https://www.theafricareport.com"),
    ]:
        st.markdown(f'<a class="sb-link" href="{url}" target="_blank">{label}</a>',
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↺  Refresh Intelligence Feed", use_container_width=True, key="refresh"):
        st.cache_data.clear()
        st.rerun()

    st.markdown(f"""
    <div style="font-family:'Inter';font-size:.58rem;color:rgba(255,255,255,.22);
                text-align:center;margin-top:16px;line-height:2.1;">
        Africa CV Market Intelligence<br>
        {datetime.now().strftime('%Y-%m-%d %H:%M')} · Internal use only
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 11. PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
hdr_l, hdr_r = st.columns([3,1])
with hdr_l:
    st.markdown("""
    <div style="padding:18px 0 6px 0;">
        <div style="font-family:'Inter';font-size:1.28rem;font-weight:700;color:#2D3142;letter-spacing:-.3px;">
            Africa Commercial Vehicle Market Intelligence
        </div>
        <div style="font-family:'Inter';font-size:.78rem;color:#9BA3B2;margin-top:3px;">
            54-nation coverage · Tier 1 deep analytics + full continent click-through · Updated monthly
        </div>
    </div>
    """, unsafe_allow_html=True)
with hdr_r:
    st.markdown(f"""
    <div style="padding:18px 0 6px 0;text-align:right;">
        <div style="font-family:'Inter';font-size:.7rem;color:#9BA3B2;">{datetime.now().strftime('%B %d, %Y')}</div>
        <div style="font-family:'Inter';font-size:.74rem;color:#D04A02;font-weight:600;margin-top:2px;">
            ● Live Intelligence Feed
        </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('<hr style="margin:0 0 18px 0;border-color:#E2E5EB;">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 12. MAP SECTION
# ══════════════════════════════════════════════════════════════════════════════
sel     = st.session_state.selected_country
is_t1   = sel in TIER1
cdata   = TIER1.get(sel, {})
sel_iso = cdata.get("iso","") if is_t1 else next(
    (iso for iso, name in ALL_AFRICA.items() if name == sel), "")
macro   = TIER2_MACRO.get(sel_iso, {})

map_col, snap_col = st.columns([5,2], gap="large")

with map_col:
    st.markdown("""
    <div style="font-family:'Inter';font-size:.7rem;font-weight:700;letter-spacing:.8px;
                text-transform:uppercase;color:#5A6070;margin-bottom:8px;">
        Africa Strategic Market Map
        <span style="font-weight:400;color:#9BA3B2;margin-left:8px;">
            · Click any country to drill down
        </span>
    </div>
    """, unsafe_allow_html=True)

    map_fig   = build_map(sel)
    map_event = st.plotly_chart(
        map_fig, use_container_width=True,
        config={"displayModeBar":False,"scrollZoom":False},
        on_select="rerun", selection_mode="points",
        key="africa_map",
    )

    # Handle click
    if map_event and hasattr(map_event,"selection") and map_event.selection:
        pts = map_event.selection.get("points",[])
        if pts:
            clicked_iso  = pts[0].get("location","")
            clicked_name = ISO_TO_NAME.get(clicked_iso,"")
            if clicked_name and clicked_name != st.session_state.selected_country:
                st.session_state.selected_country = clicked_name
                st.cache_data.clear()
                st.rerun()

    # Mini legend row
    leg_cols = st.columns(len(TIER1))
    for lc, (cname, cd) in zip(leg_cols, TIER1.items()):
        active = cname == sel
        color  = "#D04A02" if active else "#295BA5"
        bg     = "rgba(208,74,2,0.08)" if active else "rgba(41,91,165,0.05)"
        with lc:
            st.markdown(f"""
            <div style="text-align:center;padding:5px 3px;border-radius:6px;
                        background:{bg};border:1px solid {'#D04A02' if active else '#E2E5EB'};">
                <div style="font-size:.9rem;">{cd['flag']}</div>
                <div style="font-family:'Inter';font-size:.6rem;font-weight:{'700' if active else '500'};
                            color:{color};margin-top:1px;">{cname.split()[0]}</div>
            </div>
            """, unsafe_allow_html=True)

with snap_col:
    # Country snapshot card
    if is_t1:
        flag   = cdata.get("flag","🌍")
        region = cdata.get("region","Africa")
        sources = cdata.get("sources",{})
        main_src = list(sources.values())[0] if sources else ("","")
    else:
        flag   = macro.get("flag","🌍")
        region = macro.get("region","Africa")
        main_src = ("","")

    st.markdown(f"""
    <div style="background:white;border:1px solid #E2E5EB;border-radius:8px;
                padding:18px;box-shadow:0 1px 4px rgba(0,0,0,0.07);
                border-top:4px solid #D04A02;">
        <div style="font-family:'Inter';font-size:.68rem;font-weight:700;
                    letter-spacing:.8px;text-transform:uppercase;color:#9BA3B2;
                    margin-bottom:10px;">Currently Viewing</div>
        <div style="font-size:1.8rem;margin-bottom:3px;">{flag}</div>
        <div style="font-family:'Inter';font-size:1.05rem;font-weight:700;color:#2D3142;">{sel}</div>
        <div style="font-family:'Inter';font-size:.72rem;color:#9BA3B2;margin-bottom:12px;">{region}</div>
    """, unsafe_allow_html=True)

    if not is_t1:
        st.markdown(f"""
        <div class="fallback-badge">⚠ Tier 2 — General Coverage</div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="border-top:1px solid #F0F2F5;padding-top:12px;">
        """, unsafe_allow_html=True)
        for label, val in [
            ("Est. GDP","${:,.1f}B".format(macro.get("gdp",0))),
            ("Road Network","{:,}k km".format(macro.get("roads",0))),
            ("Est. CV Imports","{:,} units/yr".format(macro.get("cv_imports",0))),
        ]:
            st.markdown(f"""
            <div style="margin-bottom:10px;">
                <div style="font-family:'Inter';font-size:.65rem;color:#9BA3B2;
                            text-transform:uppercase;letter-spacing:.5px;">{label}</div>
                <div style="font-family:'Inter';font-size:1.1rem;font-weight:700;color:#2D3142;">{val}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown('<div style="border-top:1px solid #F0F2F5;padding-top:12px;">', unsafe_allow_html=True)
        for key, (value, label, delta, src_url) in cdata["kpi"].items():
            delta_color = "#1A8C5B" if "+" in delta else "#D04A02" if "-" in delta else "#5A6070"
            st.markdown(f"""
            <div style="margin-bottom:11px;padding-bottom:11px;border-bottom:1px solid #F0F2F5;">
                <div style="font-family:'Inter';font-size:.65rem;color:#9BA3B2;
                            text-transform:uppercase;letter-spacing:.5px;">{label}</div>
                <div style="font-family:'Inter';font-size:1.1rem;font-weight:700;color:#2D3142;margin:2px 0;">{value}</div>
                <div style="font-family:'Inter';font-size:.68rem;color:{delta_color};font-weight:500;">{delta}</div>
            </div>
            """, unsafe_allow_html=True)
        if main_src[0]:
            st.markdown(f"""
            <div style="font-family:'Inter';font-size:.62rem;color:#295BA5;margin-top:4px;">
                📌 <a href="{main_src[1]}" target="_blank"
                   style="color:#295BA5;">{main_src[0]}</a>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 13. COUNTRY DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
flag_display = cdata.get("flag", macro.get("flag","🌍")) if is_t1 else macro.get("flag","🌍")
st.markdown(f"""
<div class="section-hdr">
    <div class="section-bar"></div>
    <div class="section-title">{flag_display} &nbsp;{sel} — Country Dashboard</div>
    <div class="section-sub">
        {"Full Tier 1 analytics" if is_t1 else "General coverage — live news + macro indicators"}
    </div>
</div>
""", unsafe_allow_html=True)

tab_market, tab_policy, tab_news = st.tabs([
    "📊  Market Analytics",
    "📋  Policy & Market Access",
    "📡  Intelligence Feed",
])

# ── TAB 1: Market Analytics ───────────────────────────────────────────────────
with tab_market:
    if not is_t1:
        st.info(
            f"**{sel}** is a Tier 2 market. Detailed market analytics are available "
            "for our 8 core Tier 1 markets. Showing macroeconomic indicators and live intelligence feed.",
            icon="ℹ️"
        )
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Est. GDP", "${:,.1f}B".format(macro.get("gdp",0)),
                      help="IMF World Economic Outlook estimate")
        with m2:
            st.metric("Road Network", "{:,}k km".format(macro.get("roads",0)),
                      help="African Development Bank infrastructure data")
        with m3:
            st.metric("Est. CV Imports", "{:,} units/yr".format(macro.get("cv_imports",0)),
                      help="Estimated from regional trade flow modelling")
        st.caption("Source: [AfDB — African Development Bank](https://www.afdb.org) · [IMF World Economic Outlook](https://www.imf.org/en/Publications/WEO) · Estimated data for indicative purposes only.")
        st.markdown("---")
        st.markdown("**💡 Upgrade to Tier 1 coverage** — Contact your account manager for full market analytics on this country.")

    else:
        # KPI row
        kpi_keys = list(cdata["kpi"].keys())
        kpi_vals = list(cdata["kpi"].values())
        km_cols  = st.columns(len(kpi_vals))
        for col, key, (val, lbl, delta, src_url) in zip(km_cols, kpi_keys, kpi_vals):
            with col:
                dc = "normal" if "+" in delta else "inverse" if "-" in delta else "off"
                st.metric(label=key, value=val, delta=delta, delta_color=dc, help=lbl)
        st.caption(f"Source: [{list(cdata['sources'].values())[0][0]}]({list(cdata['sources'].values())[0][1]}) · Simulated data for illustrative purposes.")

        st.markdown("<br>", unsafe_allow_html=True)

        # Standard charts
        ch_l, ch_r = st.columns(2, gap="large")
        with ch_l:
            src_trade = cdata["sources"].get("trade",("",""))
            st.markdown(f"""
            <div class="chart-card">
                <div class="chart-label">Market Share</div>
                <div class="chart-title">Brand Rankings — {sel}</div>
                <div class="chart-sub">Top 5 brands by annual unit sales</div>
                <div class="source-link">📌 <a href="{src_trade[1]}" target="_blank">{src_trade[0]}</a></div>
            </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(chart_brand_bar(cdata, sel),
                            use_container_width=True,
                            config={"displayModeBar":False}, key=f"brand_{sel}")
            with st.expander("Data table"):
                df_b = pd.DataFrame({
                    "Brand": cdata["brand_share"]["brands"],
                    "Units": cdata["brand_share"]["sales"],
                    "Share (%)": [round(s/sum(cdata["brand_share"]["sales"])*100,1)
                                  for s in cdata["brand_share"]["sales"]],
                })
                st.dataframe(df_b, use_container_width=True, hide_index=True)

        with ch_r:
            src_mkt = cdata["sources"].get("market",("",""))
            st.markdown(f"""
            <div class="chart-card">
                <div class="chart-label">Sales Trend 2021–2026</div>
                <div class="chart-title">ICE vs. EV — {sel}</div>
                <div class="chart-sub">Historical actuals + 2026 forecast</div>
                <div class="source-link">📌 <a href="{src_mkt[1]}" target="_blank">{src_mkt[0]}</a></div>
            </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(chart_trend_area(cdata),
                            use_container_width=True,
                            config={"displayModeBar":False}, key=f"trend_{sel}")
            with st.expander("Data table"):
                df_t = pd.DataFrame({
                    "Year": cdata["trend"]["years"],
                    "ICE (units)": cdata["trend"]["ice"],
                    "EV (units)":  cdata["trend"]["ev"],
                })
                df_t["EV Share (%)"] = (df_t["EV (units)"] /
                    (df_t["ICE (units)"]+df_t["EV (units)"])*100).round(2)
                st.dataframe(df_t, use_container_width=True, hide_index=True)

        # ── Country-specific exclusive modules ──────────────────────────────
        st.markdown("""
        <div class="section-hdr" style="margin-top:28px;">
            <div class="section-bar"></div>
            <div class="section-title">Country-Specific Deep Analysis</div>
            <div class="section-sub">Exclusive intelligence module</div>
        </div>
        """, unsafe_allow_html=True)

        # ── South Africa: Rail Crisis / Scissors Effect ──
        if sel == "South Africa":
            st.markdown("""
            <div class="chart-card">
                <div class="chart-label">Exclusive Module · South Africa</div>
                <div class="chart-title">Transnet Rail Crisis → Road Transport Surge ("Scissors Effect")</div>
                <div class="chart-sub">
                    As Transnet rail volume collapses, HCV road sales absorb displaced freight demand.
                    Dual-axis view: Rail Mt (left) vs HCV units sold (right).
                </div>
                <div class="source-link">
                    📌 <a href="https://naamsa.co.za" target="_blank">NAAMSA — Automotive Business Council</a>
                    &nbsp;·&nbsp;
                    <a href="https://www.transnet.net/InvestorCentre/Pages/AnnualReports.aspx" target="_blank">Transnet Annual Report</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(chart_za_scissors(), use_container_width=True,
                            config={"displayModeBar":False}, key="za_scissors")
            st.caption(
                "⚠️ Transnet rail volumes declined from 228 Mt (2018) to an estimated 122 Mt (2026), "
                "a 46% collapse. This structural shift is a primary demand driver for South Africa's "
                "HCV segment. Source: [Transnet Investor Relations](https://www.transnet.net) · "
                "[NAAMSA](https://naamsa.co.za) · Simulated data for illustrative purposes."
            )

        # ── Nigeria: Tariff Waterfall ──
        elif sel == "Nigeria":
            st.markdown("""
            <div class="chart-card">
                <div class="chart-label">Exclusive Module · Nigeria</div>
                <div class="chart-title">CBU vs. CKD/SKD Import Cost Waterfall — The Zero-Tariff Dividend</div>
                <div class="chart-sub">
                    Per-unit landed cost comparison: Full CBU at 35% duty vs. CKD assembly at 0%.
                    Illustrative for a 30-tonne heavy truck base price of $100,000.
                </div>
                <div class="source-link">
                    📌 <a href="https://customs.gov.ng" target="_blank">Nigeria Customs Service</a>
                    &nbsp;·&nbsp;
                    <a href="https://naddc.gov.ng" target="_blank">NADDC — National Automotive Design & Development Council</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(chart_ng_waterfall(), use_container_width=True,
                            config={"displayModeBar":False}, key="ng_waterfall")
            st.caption(
                "💡 The CKD route delivers approximately **$46,000 per-unit cost saving** vs CBU "
                "under Nigeria's 2023 EV/assembly tariff regime. "
                "Source: [Nigeria Customs Service](https://customs.gov.ng) · "
                "[NADDC](https://naddc.gov.ng) · Figures illustrative."
            )

        # ── Morocco: OCP Throughput ──
        elif sel == "Morocco":
            st.markdown("""
            <div class="chart-card">
                <div class="chart-label">Exclusive Module · Morocco</div>
                <div class="chart-title">OCP Group Road Freight Throughput — Phosphate Corridor</div>
                <div class="chart-sub">
                    Monthly road transport throughput (thousand tonnes) on the
                    Khouribga–Jorf Lasfar mining corridor, 2023–2026.
                </div>
                <div class="source-link">
                    📌 <a href="https://www.ocpgroup.ma/investor-relations" target="_blank">OCP Group Investor Relations</a>
                    &nbsp;·&nbsp;
                    <a href="http://www.aivam.ma" target="_blank">AIVAM</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(chart_ocp_throughput(), use_container_width=True,
                            config={"displayModeBar":False}, key="ma_ocp")
            st.caption(
                "OCP Group accounts for ~800 heavy commercial vehicle units per year, "
                "representing the single largest fleet procurement decision in Morocco. "
                "Source: [OCP Group IR](https://www.ocpgroup.ma) · "
                "[AIVAM](http://www.aivam.ma) · Simulated data for illustrative purposes."
            )

        # ── Ethiopia: EV Surge ──
        elif sel == "Ethiopia":
            st.markdown("""
            <div class="chart-card">
                <div class="chart-label">Exclusive Module · Ethiopia</div>
                <div class="chart-title">EV Penetration Surge — Post Petroleum Import Ban</div>
                <div class="chart-sub">
                    Monthly EV market share (%) of commercial vehicle sales. Vertical line marks
                    July 2022 petroleum vehicle import ban implementation.
                </div>
                <div class="source-link">
                    📌 <a href="https://www.moti.gov.et" target="_blank">Ministry of Trade & Industry — Ethiopia</a>
                    &nbsp;·&nbsp;
                    <a href="https://www.erca.gov.et" target="_blank">ERCA — Ethiopian Revenue & Customs Authority</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(chart_eth_ev_surge(), use_container_width=True,
                            config={"displayModeBar":False}, key="eth_ev")
            st.caption(
                "Ethiopia's petroleum-powered vehicle import ban (2022) triggered the fastest EV "
                "fleet transition on the African continent. EV share grew from <3% to >85% within "
                "30 months. Source: [MoTI Ethiopia](https://www.moti.gov.et) · "
                "[ERCA](https://www.erca.gov.et) · Simulated data for illustrative purposes."
            )

        # ── Egypt / Kenya / Algeria / Tunisia: Assessment Scorecard ──
        else:
            scores_db = {
                "Egypt":   {"Market Size":7,"EV Readiness":3,"Tariff Advantage":5,"Regulatory Ease":5,"Growth Momentum":8},
                "Kenya":   {"Market Size":6,"EV Readiness":6,"Tariff Advantage":6,"Regulatory Ease":7,"Growth Momentum":8},
                "Algeria": {"Market Size":6,"EV Readiness":2,"Tariff Advantage":4,"Regulatory Ease":3,"Growth Momentum":5},
                "Tunisia": {"Market Size":4,"EV Readiness":5,"Tariff Advantage":7,"Regulatory Ease":7,"Growth Momentum":4},
            }
            scores = scores_db.get(sel, {dim:5 for dim in ["Market Size","EV Readiness","Tariff Advantage","Regulatory Ease","Growth Momentum"]})
            sc_cols = st.columns(5)
            for col, (dim, score) in zip(sc_cols, scores.items()):
                bar_w = score * 10
                color = "#D04A02" if score>=8 else "#295BA5" if score>=6 else "#9BA3B2"
                with col:
                    st.markdown(f"""
                    <div style="background:white;border:1px solid #E2E5EB;border-radius:8px;
                                padding:14px 12px;box-shadow:0 1px 4px rgba(0,0,0,0.06);">
                        <div style="font-family:'Inter';font-size:.62rem;font-weight:700;
                                    text-transform:uppercase;letter-spacing:.6px;color:#9BA3B2;
                                    margin-bottom:7px;">{dim}</div>
                        <div style="font-family:'Inter';font-size:1.5rem;font-weight:700;color:{color};">
                            {score}<span style="font-size:.75rem;color:#9BA3B2;">/10</span>
                        </div>
                        <div style="background:#F0F2F5;border-radius:3px;height:4px;margin-top:7px;">
                            <div style="background:{color};width:{bar_w}%;height:4px;border-radius:3px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            src_t = cdata.get("sources",{}).get("trade",("",""))
            if src_t[0]:
                st.caption(f"Source: [{src_t[0]}]({src_t[1]}) · Assessment based on simulated market intelligence.")

# ── TAB 2: Policy & Market Access ─────────────────────────────────────────────
with tab_policy:
    if not is_t1:
        st.info(
            f"Detailed policy analysis for **{sel}** is not yet available in Tier 1 coverage. "
            "Showing general EAC/AU framework guidance. "
            "Contact your account manager to commission a dedicated country policy brief.",
            icon="📋"
        )
        st.markdown("""
        <div class="pol-card">
            <div class="pol-card-title">🌍 African Union — General Trade Framework</div>
            <p>Under the African Continental Free Trade Area (AfCFTA), member states have committed to
            progressively eliminating tariffs on 90% of goods. Commercial vehicles are classified as
            sensitive goods with longer phase-out timelines (10–15 years). Check the AfCFTA Secretariat
            for country-specific schedules.</p>
        </div>
        """, unsafe_allow_html=True)
        st.caption("Source: [AfCFTA Secretariat](https://au-afcfta.org) · [AfDB Trade Finance](https://www.afdb.org)")
    else:
        p = cdata["policy"]
        src_customs = cdata["sources"].get("customs",("",""))
        src_market  = cdata["sources"].get("market",("",""))
        src_trade   = cdata["sources"].get("trade",("",""))

        st.markdown(f"""
        <div style="font-family:'Inter';font-size:.76rem;color:#5A6070;margin-bottom:18px;line-height:1.7;">
            Regulatory intelligence for <strong>{sel}</strong> — covering tariff structure,
            certification requirements, procurement landscape, and operational risk factors.
            Data represents current intelligence as of the reporting period.
        </div>
        """, unsafe_allow_html=True)

        pl, pr = st.columns(2, gap="large")
        with pl:
            st.markdown(f"""
            <div class="pol-card">
                <div class="pol-card-title">🏷 Tariff & Import Structure</div>
                <p>{p['tariff']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"Source: [{src_customs[0]}]({src_customs[1]})")

            st.markdown(f"""
            <div class="pol-card ok">
                <div class="pol-card-title">📋 Certification & Homologation Requirements</div>
                <p>{p['certification']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"Source: [{src_market[0]}]({src_market[1]})")

        with pr:
            st.markdown(f"""
            <div class="pol-card">
                <div class="pol-card-title">🏗 Key Buyers & Procurement Bodies</div>
                <p>{p['key_buyers']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"Source: [{src_trade[0]}]({src_trade[1]})")

            st.markdown(f"""
            <div class="pol-card warn">
                <div class="pol-card-title">⚠ Risk Factors & Operational Considerations</div>
                <p>{p['risk']}</p>
            </div>
            """, unsafe_allow_html=True)

        # Market entry scorecard
        st.markdown("""
        <div class="section-hdr" style="margin-top:24px;">
            <div class="section-bar"></div>
            <div class="section-title">Market Entry Assessment Scorecard</div>
        </div>
        """, unsafe_allow_html=True)

        all_scores = {
            "Nigeria":      {"Market Size":9,"EV Readiness":7,"Tariff Advantage":9,"Regulatory Ease":5,"Growth Momentum":7},
            "South Africa": {"Market Size":8,"EV Readiness":5,"Tariff Advantage":4,"Regulatory Ease":8,"Growth Momentum":4},
            "Morocco":      {"Market Size":6,"EV Readiness":6,"Tariff Advantage":8,"Regulatory Ease":8,"Growth Momentum":8},
            "Egypt":        {"Market Size":7,"EV Readiness":3,"Tariff Advantage":5,"Regulatory Ease":5,"Growth Momentum":8},
            "Kenya":        {"Market Size":6,"EV Readiness":6,"Tariff Advantage":6,"Regulatory Ease":7,"Growth Momentum":8},
            "Ethiopia":     {"Market Size":5,"EV Readiness":9,"Tariff Advantage":9,"Regulatory Ease":6,"Growth Momentum":9},
            "Algeria":      {"Market Size":6,"EV Readiness":2,"Tariff Advantage":4,"Regulatory Ease":3,"Growth Momentum":5},
            "Tunisia":      {"Market Size":4,"EV Readiness":5,"Tariff Advantage":7,"Regulatory Ease":7,"Growth Momentum":4},
        }
        scores = all_scores.get(sel, {d:5 for d in ["Market Size","EV Readiness","Tariff Advantage","Regulatory Ease","Growth Momentum"]})
        sc_cols = st.columns(5)
        for col, (dim, score) in zip(sc_cols, scores.items()):
            color = "#D04A02" if score>=8 else "#295BA5" if score>=6 else "#9BA3B2"
            with col:
                st.markdown(f"""
                <div style="background:white;border:1px solid #E2E5EB;border-radius:8px;
                            padding:14px 12px;box-shadow:0 1px 4px rgba(0,0,0,0.06);text-align:center;">
                    <div style="font-family:'Inter';font-size:.6rem;font-weight:700;
                                text-transform:uppercase;letter-spacing:.6px;color:#9BA3B2;
                                margin-bottom:8px;">{dim}</div>
                    <div style="font-family:'Inter';font-size:1.5rem;font-weight:700;color:{color};">
                        {score}<span style="font-size:.72rem;color:#9BA3B2;">/10</span></div>
                    <div style="background:#F0F2F5;border-radius:3px;height:4px;margin-top:8px;">
                        <div style="background:{color};width:{score*10}%;height:4px;border-radius:3px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ── TAB 3: Intelligence Feed ───────────────────────────────────────────────────
with tab_news:
    news_query = cdata.get("news_query","") if is_t1 else f"{sel} transport logistics commercial vehicle"

    st.markdown(f"""
    <div style="background:#F8F9FB;border:1px solid #E2E5EB;border-radius:8px;
                padding:11px 16px;margin-bottom:18px;font-family:'Inter';
                font-size:.78rem;color:#5A6070;line-height:1.7;">
        <strong style="color:#2D3142;">Intelligence parameters:</strong>
        &nbsp;Focus: <strong style="color:#D04A02;">{sel}</strong>
        &nbsp;·&nbsp; Sources: Reuters · Bloomberg · FT · Engineering News · BusinessDay · Zawya · Africa Report
        &nbsp;·&nbsp; Window: <strong>Last 30 days</strong>
        &nbsp;·&nbsp; Noise-filtered · Sorted by recency
        {"&nbsp;·&nbsp; <span style='color:#D04A02;'>⚠ Tier 2 market — general news coverage</span>" if not is_t1 else ""}
    </div>
    """, unsafe_allow_html=True)

    news_col, params_col = st.columns([3,1], gap="large")

    with news_col:
        with st.spinner(f"Fetching intelligence for {sel}..."):
            news_items = fetch_news(news_query, limit=8)

        st.markdown('<div class="news-wrap">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="news-hdr">
            <span class="news-hdr-title">📡 &nbsp;{sel} — Market Intelligence</span>
            <span class="news-badge">LIVE · 30D</span>
        </div>
        """, unsafe_allow_html=True)

        if not news_items:
            st.markdown("""
            <div class="news-empty">
                📭 &nbsp;No recent results from authority sources.<br>
                <span style="font-size:.7rem;">Try refreshing or check connectivity.</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            for item in news_items:
                st.markdown(f"""
                <div class="news-item">
                    <a class="news-title-a" href="{item['link']}" target="_blank">{item['title']}</a>
                    <div class="news-meta">
                        <span class="news-src">{item['source']}</span>
                        {item['published']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with params_col:
        st.markdown("""
        <div style="background:white;border:1px solid #E2E5EB;border-radius:8px;
                    padding:16px;box-shadow:0 1px 4px rgba(0,0,0,0.06);">
            <div style="font-family:'Inter';font-size:.68rem;font-weight:700;
                        text-transform:uppercase;letter-spacing:.6px;color:#9BA3B2;
                        margin-bottom:12px;">Search Configuration</div>
        """, unsafe_allow_html=True)
        for label, val in [
            ("Country", sel),
            ("Time Window", "Last 30 days"),
            ("Cache TTL", "30 minutes"),
            ("Coverage", "Tier 1 Deep" if is_t1 else "Tier 2 General"),
        ]:
            st.markdown(f"""
            <div style="margin-bottom:10px;">
                <div style="font-family:'Inter';font-size:.65rem;color:#9BA3B2;">{label}</div>
                <div style="font-family:'Inter';font-size:.82rem;font-weight:600;color:#2D3142;">{val}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f"""
            <div style="margin-bottom:0;">
                <div style="font-family:'Inter';font-size:.65rem;color:#9BA3B2;margin-bottom:4px;">Keywords</div>
                <div style="font-family:'Inter';font-size:.72rem;color:#5A6070;
                            line-height:1.6;word-break:break-word;background:#F8F9FB;
                            border-radius:5px;padding:8px 10px;">{news_query}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:white;border:1px solid #E2E5EB;border-radius:8px;
                    padding:16px;box-shadow:0 1px 4px rgba(0,0,0,0.06);">
            <div style="font-family:'Inter';font-size:.68rem;font-weight:700;
                        text-transform:uppercase;letter-spacing:.6px;color:#9BA3B2;
                        margin-bottom:10px;">Authority Sources</div>
        """, unsafe_allow_html=True)
        for src, url in [
            ("Reuters","https://www.reuters.com"),
            ("Bloomberg","https://www.bloomberg.com"),
            ("Financial Times","https://www.ft.com"),
            ("Engineering News ZA","https://www.engineeringnews.co.za"),
            ("BusinessDay Nigeria","https://businessday.ng"),
            ("Zawya","https://www.zawya.com"),
            ("The Africa Report","https://www.theafricareport.com"),
            ("AfDB","https://www.afdb.org"),
        ]:
            st.markdown(f"""
            <div style="font-family:'Inter';font-size:.72rem;color:#5A6070;
                        padding:4px 0;border-bottom:1px solid #F4F5F7;">
                <span style="display:inline-block;width:7px;height:7px;border-radius:50%;
                             background:#1A8C5B;margin-right:7px;"></span>
                <a href="{url}" target="_blank"
                   style="color:#295BA5;text-decoration:none;">{src}</a>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 14. FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="border-top:1px solid #E2E5EB;padding-top:14px;
            font-family:'Inter';font-size:.68rem;color:#9BA3B2;">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
        <div>
            <strong style="color:#5A6070;">Africa CV Market Intelligence Platform v5.0</strong>
            &nbsp;·&nbsp; Internal strategic use only
            &nbsp;·&nbsp; Simulated data for illustrative purposes
            &nbsp;·&nbsp; 54-nation coverage
        </div>
        <div style="text-align:right;">
            Intelligence sources: Reuters · Bloomberg · FT · NAAMSA · NADDC · AIVAM · AfDB
            &nbsp;·&nbsp; Refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
