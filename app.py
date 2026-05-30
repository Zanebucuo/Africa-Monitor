"""
Africa Commercial Vehicle Market Intelligence Platform
Enterprise BI Engine v6.0
— Robust News Feed · Deep ZA Stats SA/NAAMSA Modules · Modular Architecture
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
# 1. GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg:#F4F5F7; --white:#FFFFFF; --orange:#D04A02; --orange2:#EB6C2D;
    --navy:#21325B; --blue:#295BA5; --txt:#2D3142; --mid:#5A6070;
    --dim:#9BA3B2; --border:#E2E5EB; --green:#1A8C5B;
    --shadow:0 1px 4px rgba(0,0,0,.07),0 4px 16px rgba(0,0,0,.04);
    --radius:8px;
}
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"],.main {
    background:var(--bg) !important;
    font-family:'Inter',sans-serif !important;
    color:var(--txt);
}
[data-testid="stSidebar"]{ background:var(--navy) !important; border-right:none !important; }
[data-testid="stSidebar"] * { color:#E8ECF4 !important; }
[data-testid="stSidebar"] .stButton>button {
    background:var(--orange) !important; color:#fff !important;
    border:none !important; border-radius:var(--radius) !important; font-weight:600 !important;
}
[data-testid="stSidebar"] .stButton>button:hover{ background:var(--orange2) !important; }

/* Tabs */
[data-testid="stTabsTabList"]{
    background:var(--white) !important;
    border-bottom:2px solid var(--border) !important;
    border-radius:var(--radius) var(--radius) 0 0;
    padding:0 8px; box-shadow:var(--shadow);
}
button[data-baseweb="tab"]{
    font-family:'Inter',sans-serif !important; font-size:.84rem !important;
    font-weight:500 !important; color:var(--mid) !important;
    padding:11px 18px !important; border-bottom:3px solid transparent !important;
    background:transparent !important; border-radius:0 !important;
}
button[aria-selected="true"][data-baseweb="tab"]{
    color:var(--orange) !important; border-bottom:3px solid var(--orange) !important;
    font-weight:700 !important;
}
[data-testid="stTabPanel"]{
    background:transparent !important; padding:22px 0 0 0 !important; border:none !important;
}

/* Metrics */
[data-testid="metric-container"]{
    background:var(--white) !important; border:1px solid var(--border) !important;
    border-radius:var(--radius) !important; padding:18px 20px !important;
    box-shadow:var(--shadow) !important; border-top:3px solid var(--orange) !important;
}
[data-testid="stMetricLabel"]{
    font-size:.68rem !important; font-weight:700 !important;
    letter-spacing:.8px !important; color:var(--mid) !important; text-transform:uppercase !important;
}
[data-testid="stMetricValue"]{
    font-size:1.65rem !important; font-weight:700 !important; color:var(--txt) !important;
}

/* Cards */
.section-hdr{
    display:flex; align-items:center; gap:10px;
    margin:26px 0 14px 0; padding-bottom:10px; border-bottom:1px solid var(--border);
}
.section-bar{ width:4px; height:20px; background:var(--orange); border-radius:2px; flex-shrink:0; }
.section-title{ font-size:.88rem; font-weight:700; letter-spacing:.4px; color:var(--txt); text-transform:uppercase; }
.section-sub{ font-size:.72rem; color:var(--dim); margin-left:4px; }

.chart-card{
    background:var(--white); border:1px solid var(--border);
    border-radius:var(--radius); padding:18px 18px 8px 18px;
    box-shadow:var(--shadow); margin-bottom:4px;
}
.chart-label{ font-size:.68rem; font-weight:700; text-transform:uppercase; letter-spacing:.7px; color:var(--dim); margin-bottom:2px; }
.chart-title{ font-size:.92rem; font-weight:700; color:var(--txt); margin-bottom:2px; }
.chart-sub  { font-size:.72rem; color:var(--dim); margin-bottom:10px; }
.source-link{ font-size:.68rem; color:var(--blue); margin-top:4px; }

/* Policy cards */
.pol-card{
    background:var(--white); border:1px solid var(--border);
    border-left:4px solid var(--blue); border-radius:var(--radius);
    padding:14px 18px; box-shadow:var(--shadow); margin-bottom:12px;
}
.pol-card.warn{ border-left-color:var(--orange); }
.pol-card.ok  { border-left-color:var(--green); }
.pol-card-title{ font-size:.7rem; font-weight:700; text-transform:uppercase; letter-spacing:.6px; color:var(--mid); margin-bottom:7px; }
.pol-card p,.pol-card li{
    font-size:.82rem; color:var(--txt); line-height:1.65; margin:0;
    word-wrap:break-word; overflow-wrap:break-word; white-space:normal;
}
.pol-card ul{ margin:5px 0 0 0; padding-left:15px; }

/* Sidebar */
.sb-hdr{
    font-size:.6rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase;
    color:rgba(255,255,255,.38) !important; margin:16px 0 6px 0;
    padding-bottom:4px; border-bottom:1px solid rgba(255,255,255,.1);
}
.sb-link{
    display:block; padding:7px 11px; margin:3px 0; border-radius:6px; font-size:.77rem;
    color:#C8D3E8 !important; text-decoration:none !important;
    border:1px solid rgba(255,255,255,.08); background:rgba(255,255,255,.04);
    word-wrap:break-word; overflow-wrap:break-word; white-space:normal; transition:all .15s;
}
.sb-link:hover{ background:rgba(208,74,2,.2); border-color:rgba(208,74,2,.5); color:#fff !important; }

/* News */
.news-wrap{ background:var(--white); border:1px solid var(--border); border-radius:var(--radius); overflow:hidden; box-shadow:var(--shadow); }
.news-hdr { background:var(--navy); padding:11px 16px; display:flex; align-items:center; gap:10px; }
.news-hdr-title{ font-size:.78rem; font-weight:600; color:#fff; letter-spacing:.4px; text-transform:uppercase; }
.news-badge{ background:var(--orange); color:#fff; font-size:.58rem; font-weight:700; padding:2px 8px; border-radius:20px; letter-spacing:.5px; text-transform:uppercase; }
.news-fb-badge{ background:#F0F3F8; color:var(--mid); font-size:.58rem; font-weight:700; padding:2px 8px; border-radius:20px; letter-spacing:.5px; text-transform:uppercase; }
.news-item { padding:13px 16px; border-bottom:1px solid var(--border); transition:background .15s; }
.news-item:last-child{ border-bottom:none; }
.news-item:hover{ background:#FAFBFC; }
.news-title-a{
    font-size:.83rem; font-weight:500; color:var(--txt) !important;
    text-decoration:none !important; line-height:1.55; display:block;
    word-wrap:break-word; overflow-wrap:break-word; word-break:break-word; white-space:normal;
}
.news-title-a:hover{ color:var(--orange) !important; }
.news-meta{ font-size:.68rem; color:var(--dim); margin-top:5px; word-wrap:break-word; white-space:normal; }
.news-src { display:inline-block; background:#F0F3F8; color:var(--navy); font-size:.6rem; font-weight:600; padding:1px 7px; border-radius:4px; margin-right:5px; }
.news-fb-src{ display:inline-block; background:#FFF3ED; color:var(--orange); font-size:.6rem; font-weight:600; padding:1px 7px; border-radius:4px; margin-right:5px; }
.news-empty{ padding:28px 16px; text-align:center; color:var(--dim); font-size:.8rem; line-height:1.8; }

/* Fallback badge */
.fallback-badge{
    display:inline-flex; align-items:center; gap:6px;
    background:#FFF3ED; border:1px solid #F0C4AC; border-radius:20px;
    padding:4px 14px; font-size:.72rem; font-weight:600; color:var(--orange); margin-bottom:14px;
}

#MainMenu,footer,header{ visibility:hidden; }
[data-testid="stToolbar"]{ display:none; }
.block-container{ padding-top:0 !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 2. CHART THEME
# ══════════════════════════════════════════════════════════════════════════════
PwC_COLORS = ["#D04A02","#21325B","#295BA5","#EB6C2D","#4C7FA8","#8BA7C4","#C0C8D8","#F0C4AC"]

CHART_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#2D3142", size=12),
    margin=dict(l=50, r=20, t=24, b=50),
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
# 3. TIER-1 COUNTRY DATABASE
# ══════════════════════════════════════════════════════════════════════════════
TIER1 = {
    "Nigeria": {
        "flag":"🇳🇬","iso":"NGA","region":"West Africa","tier":1,
        "kpi":{
            "Annual CV Sales":  ("45,200","units/yr","+6.2% YoY","https://naddc.gov.ng"),
            "EV Penetration":   ("3.8%","of total sales","+1.2pp YoY","https://trade.gov.ng"),
            "EV Import Tariff": ("0%","CBU EV (2023–28)","Zero-rated","https://customs.gov.ng"),
            "Diesel Price":     ("₦1,180","/litre","≈ $0.74 USD","https://pppra.gov.ng"),
        },
        "brand_share":{"brands":["Sinotruk","FAW","Foton","Volvo","Scania"],"sales":[1840,1420,980,560,410]},
        "trend":{"years":[2021,2022,2023,2024,2025,2026],"ice":[38200,39500,40100,41800,43200,43800],"ev":[0,80,320,820,1640,1400]},
        "policy":{
            "tariff":      "CBU EV commercial vehicles: 0% (2023–2028). CKD/SKD assembly: 0%. Conventional CBU: 35%.",
            "certification":"SON mandatory certification; NAFDAC for specialist vehicles; Form M import approval required.",
            "key_buyers":  "Dangote Cement (cement logistics), BUA Group (agri & chemicals), NNPC Logistics Division.",
            "risk":        "NGN/USD depreciation >60% over 18 months. Port congestion at Apapa delays clearance 3–6 weeks.",
        },
        "news_query":"Nigeria commercial vehicle logistics truck",
        "sources":{
            "trade":  ("NADDC — National Automotive Design & Development Council","https://naddc.gov.ng"),
            "customs":("Nigeria Customs Service","https://customs.gov.ng"),
            "market": ("Nigeria Trade Hub","https://trade.gov.ng"),
        },
    },
    "South Africa": {
        "flag":"🇿🇦","iso":"ZAF","region":"Southern Africa","tier":1,
        "kpi":{
            "Annual CV Sales": ("31,500","units/yr","-2.8% YoY","https://naamsa.co.za"),
            "EV Penetration":  ("1.9%","of total sales","+0.7pp YoY","https://naamsa.co.za"),
            "Import Tariff":   ("25%","CBU standard rate","KD assembly ~12%","https://itac.org.za"),
            "Diesel Price":    ("R21.60","/litre","≈ $1.18 USD","https://www.energy.gov.za"),
        },
        "brand_share":{"brands":["Mercedes-Benz","Volvo","MAN","Scania","FAW"],"sales":[7200,6100,5800,5200,3100]},
        "trend":{"years":[2021,2022,2023,2024,2025,2026],"ice":[29800,31200,32500,31800,30900,30900],"ev":[0,0,120,320,540,600]},
        "policy":{
            "tariff":      "25% CBU import duty. APDP incentive scheme: manufacturers achieving >50% localisation receive production rebates.",
            "certification":"NRCS (National Regulator for Compulsory Specifications) mandatory LoA. Euro 5-equivalent emissions. SABS type approval.",
            "key_buyers":  "Transnet (rail + ports), Imperial Logistics, Tiger Brands distribution, Shoprite supply chain.",
            "risk":        "Load-shedding (Stage 2–4) disrupts EV charging infrastructure rollout. ZAR/USD pressure at ~18.5.",
        },
        "news_query":"South Africa commercial truck logistics freight",
        "sources":{
            "trade":  ("NAAMSA — Automotive Business Council","https://naamsa.co.za"),
            "customs":("ITAC — International Trade Administration Commission","https://itac.org.za"),
            "market": ("NRCS — National Regulator for Compulsory Specifications","https://www.nrcs.org.za"),
        },
    },
    "Morocco": {
        "flag":"🇲🇦","iso":"MAR","region":"North Africa","tier":1,
        "kpi":{
            "Annual CV Sales":  ("18,400","units/yr","+8.5% YoY","http://www.aivam.ma"),
            "EV Penetration":   ("2.1%","of total sales","+0.9pp YoY","http://www.aivam.ma"),
            "EV Import Tariff": ("2.5%","EU AA Agreement","Lowest in region","https://www.douane.gov.ma"),
            "Diesel Price":     ("MAD 13.50","/litre","≈ $1.34 USD","https://www.onhym.com"),
        },
        "brand_share":{"brands":["Renault Trucks","Mercedes-Benz","Volvo","Sinotruk","MAN"],"sales":[4200,3600,3100,2800,2100]},
        "trend":{"years":[2021,2022,2023,2024,2025,2026],"ice":[14200,15100,16200,17400,18000,18000],"ev":[0,40,120,260,380,400]},
        "policy":{
            "tariff":      "EU Association Agreement: CBU tariff 2.5%. EV treated equally. No dedicated KD incentive scheme.",
            "certification":"CNEAT UN-ECE mutual recognition. EU-certified vehicles fast-track approval.",
            "key_buyers":  "OCP Group (phosphate mining, 800+ units/yr), ONCF (national rail logistics), Casablanca Port operators.",
            "risk":        "Market limited vs Sub-Sahara; European brands hold >65% share; Chinese brands need local after-sales investment.",
        },
        "news_query":"Morocco transport logistics trucks OCP freight",
        "sources":{
            "trade":  ("AIVAM — Association des Importateurs de Véhicules au Maroc","http://www.aivam.ma"),
            "customs":("Direction Générale des Douanes","https://www.douane.gov.ma"),
            "market": ("CNEAT — Centre National d'Essais et d'Homologation","https://www.cneat.ma"),
        },
    },
    "Egypt": {
        "flag":"🇪🇬","iso":"EGY","region":"North Africa","tier":1,
        "kpi":{
            "Annual CV Sales": ("25,800","units/yr","+11.2% YoY","https://www.eos.org.eg"),
            "EV Penetration":  ("0.8%","of total sales","+0.3pp YoY","https://www.eos.org.eg"),
            "CBU Tariff":      ("40%","standard rate","KD at 5% (>40% local)","https://www.goeic.gov.eg"),
            "Diesel Price":    ("EGP 9.75","/litre (subsidised)","≈ $0.20 USD","https://www.mop.gov.eg"),
        },
        "brand_share":{"brands":["Sinotruk","SAIC Maxus","Foton","Mercedes-Benz","MAN"],"sales":[6200,4800,3900,3500,2800]},
        "trend":{"years":[2021,2022,2023,2024,2025,2026],"ice":[18000,20500,22100,24800,25600,25600],"ev":[0,0,60,130,200,200]},
        "policy":{
            "tariff":      "CBU standard: 40%. KD assembly with >40% localisation: 5%. SCZone production: 0%.",
            "certification":"EOS mandatory; GOEIC import licence; SCZone investors get simplified clearance.",
            "key_buyers":  "EGPC logistics, SCZone construction contractors, private building materials distributors.",
            "risk":        "EGP depreciated >50% in 2 years; FX controls delay import payments 45–90 days.",
        },
        "news_query":"Egypt commercial vehicle logistics freight Suez",
        "sources":{
            "trade":  ("EOS — Egyptian Organisation for Standardisation","https://www.eos.org.eg"),
            "customs":("GOEIC — General Organisation for Export & Import Control","https://www.goeic.gov.eg"),
            "market": ("IDSC — Information and Decision Support Center","https://www.idsc.gov.eg"),
        },
    },
    "Kenya": {
        "flag":"🇰🇪","iso":"KEN","region":"East Africa","tier":1,
        "kpi":{
            "Annual CV Sales": ("14,200","units/yr","+9.4% YoY","https://kebs.org"),
            "EV Penetration":  ("2.6%","of total sales","+1.1pp YoY","https://kebs.org"),
            "Import Duty":     ("25%","EAC CET standard","COMESA preference 0%","https://kra.go.ke"),
            "Diesel Price":    ("KES 188","/litre","≈ $1.42 USD","https://www.epra.go.ke"),
        },
        "brand_share":{"brands":["Isuzu","Toyota","Foton","Sinotruk","Volvo"],"sales":[3800,2900,2400,2100,1200]},
        "trend":{"years":[2021,2022,2023,2024,2025,2026],"ice":[10800,11500,12200,13100,13800,13900],"ev":[0,20,80,210,340,370]},
        "policy":{
            "tariff":      "EAC Common External Tariff: 25%. COMESA member states: 0%. EV import: currently 25%.",
            "certification":"KEBS mandatory PVoC inspection at origin; NTSA vehicle inspection on arrival.",
            "key_buyers":  "Kenya Ports Authority (Mombasa), East African Breweries, Bamburi Cement, SGR feeder.",
            "risk":        "KES depreciation ~20% (2023–2024); SGR freight competition reducing some long-haul demand.",
        },
        "news_query":"Kenya commercial vehicle logistics freight Nairobi",
        "sources":{
            "trade":  ("KEBS — Kenya Bureau of Standards","https://kebs.org"),
            "customs":("KRA — Kenya Revenue Authority","https://kra.go.ke"),
            "market": ("EPRA — Energy & Petroleum Regulatory Authority","https://www.epra.go.ke"),
        },
    },
    "Ethiopia": {
        "flag":"🇪🇹","iso":"ETH","region":"East Africa","tier":1,
        "kpi":{
            "Annual CV Sales":   ("9,800","units/yr","+22.1% YoY","https://www.moti.gov.et"),
            "EV Penetration":    ("8.4%","of total sales","+4.2pp YoY","https://www.moti.gov.et"),
            "EV Import Duty":    ("0%","Petroleum vehicle ban","ICE ban since 2022","https://www.erca.gov.et"),
            "Electricity Price": ("ETB 1.42","/kWh","≈ $0.025 USD","https://www.eepco.gov.et"),
        },
        "brand_share":{"brands":["BYD","Foton EV","King Long EV","Sinotruk","Skywell"],"sales":[2800,2100,1600,1200,800]},
        "trend":{"years":[2021,2022,2023,2024,2025,2026],"ice":[7200,6800,5400,3200,1800,1200],"ev":[200,800,2800,5800,7400,8200]},
        "policy":{
            "tariff":      "Ethiopia BANNED petroleum-powered vehicle imports (2022). EV import duty: 0%.",
            "certification":"EthSA (Ethiopian Standards Agency); EV charging under national grid expansion.",
            "key_buyers":  "Ethiopian Roads Authority, Ethiopian Airlines cargo, Ethio Telecom fleet.",
            "risk":        "Limited charging infrastructure outside Addis Ababa; internal conflict disrupts northern routes.",
        },
        "news_query":"Ethiopia EV commercial vehicle petroleum ban transport",
        "sources":{
            "trade":  ("MoTI — Ministry of Trade & Industry Ethiopia","https://www.moti.gov.et"),
            "customs":("ERCA — Ethiopian Revenue & Customs Authority","https://www.erca.gov.et"),
            "market": ("EthSA — Ethiopian Standards Agency","https://www.ethsa.gov.et"),
        },
    },
    "Algeria": {
        "flag":"🇩🇿","iso":"DZA","region":"North Africa","tier":1,
        "kpi":{
            "Annual CV Sales": ("12,600","units/yr","+4.8% YoY","https://www.commerce.gov.dz"),
            "EV Penetration":  ("0.4%","of total sales","Early-stage","https://www.commerce.gov.dz"),
            "Import Tariff":   ("30%","CBU standard","CKD benefits available","https://www.douane.gov.dz"),
            "Diesel Price":    ("DZD 45","/litre (subsidised)","≈ $0.33 USD","https://www.energy.gov.dz"),
        },
        "brand_share":{"brands":["Mercedes-Benz","Renault Trucks","MAN","Sinotruk","Volvo"],"sales":[3200,2800,2400,2000,1400]},
        "trend":{"years":[2021,2022,2023,2024,2025,2026],"ice":[10200,10800,11400,12000,12400,12400],"ev":[0,0,20,40,60,60]},
        "policy":{
            "tariff":      "30% CBU tariff. CKD/SKD assembly partnerships permitted; Renault Trucks has existing JV in Rouiba.",
            "certification":"IANOR (Institut Algérien de Normalisation); Euro 3 minimum (upgrade to Euro 4 underway).",
            "key_buyers":  "Sonatrach (oil & gas logistics), SNVI, Ministry of Public Works infrastructure.",
            "risk":        "Heavy protectionism; FX controls; import licence quotas create supply uncertainty.",
        },
        "news_query":"Algeria commercial vehicle transport logistics Sonatrach",
        "sources":{
            "trade":  ("Ministère du Commerce — Algeria","https://www.commerce.gov.dz"),
            "customs":("Direction Générale des Douanes","https://www.douane.gov.dz"),
            "market": ("IANOR — Institut Algérien de Normalisation","https://www.ianor.dz"),
        },
    },
    "Tunisia": {
        "flag":"🇹🇳","iso":"TUN","region":"North Africa","tier":1,
        "kpi":{
            "Annual CV Sales": ("8,100","units/yr","+3.1% YoY","https://www.innorpi.tn"),
            "EV Penetration":  ("1.2%","of total sales","+0.4pp YoY","https://www.innorpi.tn"),
            "Import Tariff":   ("10%","EU Association Agreement","Lowest tier","https://www.douane.gov.tn"),
            "Diesel Price":    ("TND 2.10","/litre (subsidised)","≈ $0.67 USD","https://www.industrie.gov.tn"),
        },
        "brand_share":{"brands":["Mercedes-Benz","Renault Trucks","MAN","Volvo","Sinotruk"],"sales":[2100,1800,1500,1200,900]},
        "trend":{"years":[2021,2022,2023,2024,2025,2026],"ice":[6800,7100,7400,7800,8000,8000],"ev":[0,20,40,70,100,100]},
        "policy":{
            "tariff":      "EU Association Agreement: ~10% tariff. UN-ECE mutual recognition removes re-certification need.",
            "certification":"INNORPI; ATTT road transport authority approval.",
            "key_buyers":  "CPG (Compagnie des Phosphates de Gafsa), Port of Tunis operators, food & textile logistics.",
            "risk":        "Small total market; European brands dominate >70% share.",
        },
        "news_query":"Tunisie transport logistique camions freight",
        "sources":{
            "trade":  ("INNORPI — Institut National de la Normalisation","https://www.innorpi.tn"),
            "customs":("Direction Générale des Douanes — Tunisie","https://www.douane.gov.tn"),
            "market": ("ATTT — Agence Technique des Transports Terrestres","https://www.attt.tn"),
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 4. FULL 54-NATION MAP DATA
# ══════════════════════════════════════════════════════════════════════════════
ALL_AFRICA = {
    "NGA":"Nigeria","ZAF":"South Africa","MAR":"Morocco","EGY":"Egypt",
    "KEN":"Kenya","ETH":"Ethiopia","DZA":"Algeria","TUN":"Tunisia",
    "GHA":"Ghana","TZA":"Tanzania","UGA":"Uganda","RWA":"Rwanda",
    "SEN":"Senegal","CIV":"Côte d'Ivoire","CMR":"Cameroon","ZMB":"Zambia",
    "ZWE":"Zimbabwe","MOZ":"Mozambique","MDG":"Madagascar","MWI":"Malawi",
    "NAM":"Namibia","BWA":"Botswana","AGO":"Angola","LBY":"Libya",
    "SDN":"Sudan","SSD":"South Sudan","SOM":"Somalia","ERI":"Eritrea",
    "DJI":"Djibouti","BDI":"Burundi","COM":"Comoros","STP":"São Tomé",
    "SWZ":"Eswatini","LSO":"Lesotho","MUS":"Mauritius","CPV":"Cabo Verde",
    "SLE":"Sierra Leone","LBR":"Liberia","GIN":"Guinea","GNB":"Guinea-Bissau",
    "GMB":"Gambia","GNQ":"Equatorial Guinea","GAB":"Gabon","COG":"Congo",
    "COD":"DR Congo","CAF":"Central African Republic","TCD":"Chad",
    "NER":"Niger","MLI":"Mali","BFA":"Burkina Faso","BEN":"Benin",
    "TGO":"Togo","MRT":"Mauritania","ESH":"Western Sahara",
}

TIER2_MACRO = {
    "GHA":{"gdp":75.5,"roads":72,"cv_imports":8200,"flag":"🇬🇭","region":"West Africa"},
    "TZA":{"gdp":80.0,"roads":87,"cv_imports":9100,"flag":"🇹🇿","region":"East Africa"},
    "UGA":{"gdp":51.0,"roads":21,"cv_imports":5400,"flag":"🇺🇬","region":"East Africa"},
    "RWA":{"gdp":13.8,"roads":15,"cv_imports":3600,"flag":"🇷🇼","region":"East Africa"},
    "SEN":{"gdp":32.0,"roads":16,"cv_imports":4200,"flag":"🇸🇳","region":"West Africa"},
    "CIV":{"gdp":73.0,"roads":81,"cv_imports":7800,"flag":"🇨🇮","region":"West Africa"},
    "CMR":{"gdp":48.0,"roads":77,"cv_imports":5200,"flag":"🇨🇲","region":"Central Africa"},
    "ZMB":{"gdp":29.0,"roads":40,"cv_imports":3800,"flag":"🇿🇲","region":"Southern Africa"},
    "ZWE":{"gdp":28.0,"roads":97,"cv_imports":3200,"flag":"🇿🇼","region":"Southern Africa"},
    "MOZ":{"gdp":18.0,"roads":31,"cv_imports":2800,"flag":"🇲🇿","region":"Southern Africa"},
    "MDG":{"gdp":14.5,"roads":32,"cv_imports":2100,"flag":"🇲🇬","region":"Southern Africa"},
    "MWI":{"gdp":12.6,"roads":16,"cv_imports":1800,"flag":"🇲🇼","region":"Southern Africa"},
    "NAM":{"gdp":12.8,"roads":48,"cv_imports":3400,"flag":"🇳🇦","region":"Southern Africa"},
    "BWA":{"gdp":18.6,"roads":31,"cv_imports":2900,"flag":"🇧🇼","region":"Southern Africa"},
    "AGO":{"gdp":102.0,"roads":76,"cv_imports":6800,"flag":"🇦🇴","region":"Southern Africa"},
    "LBY":{"gdp":52.0,"roads":34,"cv_imports":4100,"flag":"🇱🇾","region":"North Africa"},
    "SDN":{"gdp":45.0,"roads":24,"cv_imports":3600,"flag":"🇸🇩","region":"East Africa"},
    "SSD":{"gdp":4.6,"roads":9,"cv_imports":800,"flag":"🇸🇸","region":"East Africa"},
    "SOM":{"gdp":8.0,"roads":22,"cv_imports":1200,"flag":"🇸🇴","region":"East Africa"},
    "ERI":{"gdp":2.1,"roads":14,"cv_imports":400,"flag":"🇪🇷","region":"East Africa"},
    "DJI":{"gdp":3.9,"roads":3,"cv_imports":600,"flag":"🇩🇯","region":"East Africa"},
    "BDI":{"gdp":3.1,"roads":14,"cv_imports":500,"flag":"🇧🇮","region":"East Africa"},
    "COM":{"gdp":1.4,"roads":1,"cv_imports":120,"flag":"🇰🇲","region":"East Africa"},
    "STP":{"gdp":0.6,"roads":0.3,"cv_imports":60,"flag":"🇸🇹","region":"Central Africa"},
    "SWZ":{"gdp":4.8,"roads":4,"cv_imports":650,"flag":"🇸🇿","region":"Southern Africa"},
    "LSO":{"gdp":2.9,"roads":6,"cv_imports":420,"flag":"🇱🇸","region":"Southern Africa"},
    "MUS":{"gdp":14.2,"roads":2,"cv_imports":1800,"flag":"🇲🇺","region":"Southern Africa"},
    "CPV":{"gdp":2.2,"roads":1.5,"cv_imports":280,"flag":"🇨🇻","region":"West Africa"},
    "SLE":{"gdp":4.0,"roads":11,"cv_imports":620,"flag":"🇸🇱","region":"West Africa"},
    "LBR":{"gdp":3.8,"roads":10,"cv_imports":540,"flag":"🇱🇷","region":"West Africa"},
    "GIN":{"gdp":16.0,"roads":44,"cv_imports":1800,"flag":"🇬🇳","region":"West Africa"},
    "GNB":{"gdp":1.7,"roads":4,"cv_imports":200,"flag":"🇬🇼","region":"West Africa"},
    "GMB":{"gdp":2.1,"roads":4,"cv_imports":320,"flag":"🇬🇲","region":"West Africa"},
    "GNQ":{"gdp":10.7,"roads":3,"cv_imports":840,"flag":"🇬🇶","region":"Central Africa"},
    "GAB":{"gdp":19.0,"roads":9,"cv_imports":1400,"flag":"🇬🇦","region":"Central Africa"},
    "COG":{"gdp":12.0,"roads":17,"cv_imports":980,"flag":"🇨🇬","region":"Central Africa"},
    "COD":{"gdp":65.0,"roads":152,"cv_imports":5800,"flag":"🇨🇩","region":"Central Africa"},
    "CAF":{"gdp":2.5,"roads":24,"cv_imports":380,"flag":"🇨🇫","region":"Central Africa"},
    "TCD":{"gdp":11.2,"roads":40,"cv_imports":1200,"flag":"🇹🇩","region":"Central Africa"},
    "NER":{"gdp":16.5,"roads":19,"cv_imports":1400,"flag":"🇳🇪","region":"West Africa"},
    "MLI":{"gdp":19.2,"roads":22,"cv_imports":1800,"flag":"🇲🇱","region":"West Africa"},
    "BFA":{"gdp":20.4,"roads":15,"cv_imports":1600,"flag":"🇧🇫","region":"West Africa"},
    "BEN":{"gdp":17.8,"roads":16,"cv_imports":2100,"flag":"🇧🇯","region":"West Africa"},
    "TGO":{"gdp":9.0,"roads":11,"cv_imports":1200,"flag":"🇹🇬","region":"West Africa"},
    "MRT":{"gdp":9.9,"roads":12,"cv_imports":800,"flag":"🇲🇷","region":"West Africa"},
    "ESH":{"gdp":2.4,"roads":6,"cv_imports":180,"flag":"🏳","region":"North Africa"},
}

ISO_TO_NAME = {d["iso"]: n for n, d in TIER1.items()}
for iso, name in ALL_AFRICA.items():
    if iso not in ISO_TO_NAME:
        ISO_TO_NAME[iso] = name
ALL_ISO_LIST = list(dict.fromkeys(ISO_TO_NAME.keys()))

# ══════════════════════════════════════════════════════════════════════════════
# 5. NEWS FETCHER — "Wide Net, Smart Filter" Architecture
# ══════════════════════════════════════════════════════════════════════════════
AUTHORITY_DOMAINS = [
    "reuters","bloomberg","ft.com","engineeringnews","businessday",
    "zawya","theafricareport","africanews","afdb","apanews",
    "businesstimes","naamsa","naddc","statssa","moti.gov",
]
NOISE_WORDS = {"rumor","rumour","unconfirmed","alleged","shocking","viral","leaked","clickbait"}

@st.cache_data(ttl=1800)
def fetch_news(query: str, limit: int = 7) -> dict:
    """
    'Wide Net, Smart Filter' news fetcher.
    Returns: {"items": [...], "is_authority": bool, "is_fallback": bool}
    Each item: {title, link, published, pub_dt, source}
    """
    cutoff = datetime.utcnow() - timedelta(days=30)

    def _parse_feed(url: str) -> list:
        try:
            feed = feedparser.parse(url)
            results = []
            for entry in feed.entries:
                title = entry.get("title","")
                if not title or any(n in title.lower() for n in NOISE_WORDS):
                    continue
                pub_str, pub_dt = "–", None
                if hasattr(entry,"published_parsed") and entry.published_parsed:
                    pub_dt  = datetime(*entry.published_parsed[:6])
                    pub_str = pub_dt.strftime("%Y-%m-%d")
                results.append({
                    "title":     title,
                    "link":      entry.get("link","#"),
                    "published": pub_str,
                    "pub_dt":    pub_dt,
                    "source":    entry.get("source",{}).get("title","–"),
                })
            results.sort(key=lambda x: x["pub_dt"] or datetime.min, reverse=True)
            return results
        except Exception:
            return []

    def _is_authority(item: dict) -> bool:
        combined = (item["link"] + " " + item["source"]).lower()
        return any(d in combined for d in AUTHORITY_DOMAINS)

    def _is_recent(item: dict) -> bool:
        return item["pub_dt"] is None or item["pub_dt"] >= cutoff

    # ── Pass 1: Broad query + time filter (when:30d)
    encoded = (query + " when:30d").replace(" ","+").replace('"',"%22")
    url1 = f"https://news.google.com/rss/search?q={encoded}&hl=en-US&gl=US&ceid=US:en"
    raw = _parse_feed(url1)
    recent = [x for x in raw if _is_recent(x)]

    # ── Pass 2: Authority filter
    authority_items = [x for x in recent if _is_authority(x)]
    if len(authority_items) >= 3:
        return {"items": authority_items[:limit], "is_authority": True, "is_fallback": False}

    # ── Pass 3: All recent (non-authority) up to limit
    if len(recent) >= 3:
        return {"items": recent[:limit], "is_authority": False, "is_fallback": False}

    # ── Pass 4: Fallback — broaden to 90 days, no time param
    encoded_fb = query.replace(" ","+").replace('"',"%22")
    url_fb = f"https://news.google.com/rss/search?q={encoded_fb}&hl=en-US&gl=US&ceid=US:en"
    raw_fb = _parse_feed(url_fb)
    if raw_fb:
        return {"items": raw_fb[:3], "is_authority": False, "is_fallback": True}

    return {"items": [], "is_authority": False, "is_fallback": True}


def render_news_panel(query: str, country: str):
    """Render the full news panel with authority/fallback badging."""
    with st.spinner(f"Fetching intelligence for {country}..."):
        result = fetch_news(query)

    items       = result["items"]
    is_auth     = result["is_authority"]
    is_fallback = result["is_fallback"]

    badge_html = (
        '<span class="news-badge">AUTHORITY · 30D</span>' if is_auth else
        '<span class="news-fb-badge">GENERAL · 30D</span>' if not is_fallback else
        '<span class="news-fb-badge">FALLBACK · 90D</span>'
    )

    st.markdown('<div class="news-wrap">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="news-hdr">
        <span class="news-hdr-title">📡 &nbsp;{country} — Market Intelligence</span>
        {badge_html}
    </div>
    """, unsafe_allow_html=True)

    if is_fallback and not items:
        st.markdown("""
        <div class="news-empty">
            📭 &nbsp;No results found.<br>
            <span style="font-size:.7rem;">Try refreshing or check network connectivity.</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        if is_fallback:
            st.markdown("""
            <div style="padding:8px 16px;background:#FFF8F5;border-bottom:1px solid #F0C4AC;
                        font-family:'Inter';font-size:.72rem;color:#D04A02;">
                ⚠ Authority sources returned no results. Showing best available recent coverage.
            </div>
            """, unsafe_allow_html=True)
        elif not is_auth:
            st.markdown("""
            <div style="padding:8px 16px;background:#F8F9FB;border-bottom:1px solid #E2E5EB;
                        font-family:'Inter';font-size:.72rem;color:#5A6070;">
                ℹ Showing recent industry coverage. Authority source articles highlighted where available.
            </div>
            """, unsafe_allow_html=True)

        for item in items:
            auth = _is_authority_display(item)
            src_class = "news-src" if auth else "news-fb-src"
            st.markdown(f"""
            <div class="news-item">
                <a class="news-title-a" href="{item['link']}" target="_blank">{item['title']}</a>
                <div class="news-meta">
                    <span class="{src_class}">{item['source']}</span>
                    {item['published']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def _is_authority_display(item: dict) -> bool:
    combined = (item["link"] + " " + item["source"]).lower()
    return any(d in combined for d in AUTHORITY_DOMAINS)

# ══════════════════════════════════════════════════════════════════════════════
# 6. SIMULATED DATA GENERATORS — Modular, CSV-ready
# ══════════════════════════════════════════════════════════════════════════════

# ── Universal generators ──────────────────────────────────────────────────────
@st.cache_data
def gen_brand_share_df(country: str) -> pd.DataFrame:
    cdata = TIER1[country]
    brands = cdata["brand_share"]["brands"]
    sales  = cdata["brand_share"]["sales"]
    total  = sum(sales)
    return pd.DataFrame({
        "Brand":     brands,
        "Units":     sales,
        "Share_pct": [round(s/total*100,1) for s in sales],
    })

@st.cache_data
def gen_trend_df(country: str) -> pd.DataFrame:
    cdata = TIER1[country]
    t = cdata["trend"]
    df = pd.DataFrame({"Year":t["years"],"ICE":t["ice"],"EV":t["ev"]})
    df["Total"]    = df["ICE"] + df["EV"]
    df["EV_Share"] = (df["EV"]/df["Total"]*100).round(2)
    return df

# ── South Africa exclusive generators ────────────────────────────────────────
@st.cache_data
def gen_za_freight_category() -> pd.DataFrame:
    """
    Stats SA P7162 Road Freight Survey — Category breakdown.
    Future: replace with pd.read_csv('statssa_p7162.csv')
    """
    return pd.DataFrame({
        "Category": [
            "Mining & Quarrying",
            "Manufactured Food & Beverages",
            "Agriculture & Forestry",
            "Retail & Wholesale Trade",
            "Parcels & Express Logistics",
            "Construction Materials",
            "Petroleum Products",
            "Other",
        ],
        "Revenue_ZAR_bn": [48.2, 21.6, 14.8, 13.2, 11.4, 9.6, 8.8, 7.4],
        "Pct": [35.4, 15.9, 10.9, 9.7, 8.4, 7.1, 6.5, 5.4],
        "Color": [
            "#D04A02","#21325B","#295BA5","#4C7FA8",
            "#EB6C2D","#8BA7C4","#C0C8D8","#E2E5EB",
        ],
    })

@st.cache_data
def gen_za_payload_vs_income() -> pd.DataFrame:
    """
    Stats SA P7162 — Payload (tonnes) vs Freight Income (ZAR bn).
    Diverging trends illustrate per-km cost squeeze.
    Future: replace with pd.read_csv('statssa_p7162_timeseries.csv')
    """
    np.random.seed(10)
    quarters = pd.date_range("2020-01-01","2026-04-01",freq="QS")
    n = len(quarters)
    payload = (np.linspace(2420,1890,n) + np.random.normal(0,30,n)).round(1)
    income  = (np.linspace(58.4,96.8,n) + np.random.normal(0,1.2,n)).round(2)
    return pd.DataFrame({"Quarter":quarters,"Payload_Mt":payload,"Income_ZAR_bn":income})

@st.cache_data
def gen_za_sales_channel() -> pd.DataFrame:
    """
    NAAMSA sales channel breakdown.
    Future: replace with pd.read_csv('naamsa_channel.csv')
    """
    return pd.DataFrame({
        "Channel":["Dealer Retail","Corporate Fleets","Government Procurement","Rental & Leasing"],
        "Share_pct":[79.5,10.8,5.2,4.5],
        "Color":["#D04A02","#21325B","#295BA5","#8BA7C4"],
    })

@st.cache_data
def gen_za_province_sales() -> pd.DataFrame:
    """
    NAAMSA provincial HCV sales distribution.
    Future: replace with pd.read_csv('naamsa_province.csv')
    """
    return pd.DataFrame({
        "Province":["Gauteng","KwaZulu-Natal","Western Cape","Eastern Cape",
                    "Limpopo","Mpumalanga","North West","Free State","Northern Cape"],
        "Units":[14200,5800,4600,2400,1600,1200,800,600,300],
        "Share_pct":[45.1,18.4,14.6,7.6,5.1,3.8,2.5,1.9,1.0],
    })

@st.cache_data
def gen_za_rail_road() -> pd.DataFrame:
    """Transnet rail decline vs HCV road sales — Scissors Effect."""
    return pd.DataFrame({
        "Year":   [2018,2019,2020,2021,2022,2023,2024,2025,2026],
        "Rail_Mt":[228,218,204,189,171,158,142,131,122],
        "HCV_Units":[27500,28200,29800,30400,31200,32500,31800,30900,30900],
    })

# ── Nigeria exclusive generators ──────────────────────────────────────────────
@st.cache_data
def gen_ng_tariff_waterfall() -> pd.DataFrame:
    """CBU vs CKD landed cost per unit (USD). Future: pd.read_csv('ng_tariff.csv')"""
    return pd.DataFrame({
        "Label":   ["CBU Base Price","CBU Import Duty\n(35%)","CBU Port &\nClearance",
                    "CBU Total Landed","CKD Base Price","CKD Import Duty\n(0% — EV Policy)",
                    "CKD Assembly Cost","CKD Total Landed"],
        "Value":   [100000,35000,8000,143000,85000,0,12000,97000],
        "Measure": ["absolute","relative","relative","total",
                    "absolute","relative","relative","total"],
    })

# ── Morocco exclusive generators ──────────────────────────────────────────────
@st.cache_data
def gen_ocp_throughput() -> pd.DataFrame:
    """OCP phosphate road freight throughput. Future: pd.read_csv('ocp_throughput.csv')"""
    np.random.seed(3)
    months = pd.date_range("2023-01-01","2026-05-01",freq="MS")
    n = len(months)
    trend    = np.linspace(820,1380,n)
    seasonal = 90*np.sin(np.linspace(0,6.5*np.pi,n))
    noise    = np.random.normal(0,35,n)
    return pd.DataFrame({"Month":months,"Throughput_kt":(trend+seasonal+noise).clip(500).round(1)})

# ── Ethiopia exclusive generators ─────────────────────────────────────────────
@st.cache_data
def gen_eth_ev_surge() -> pd.DataFrame:
    """Ethiopia EV market share post petroleum ban. Future: pd.read_csv('eth_ev.csv')"""
    np.random.seed(4)
    months = pd.date_range("2021-01-01","2026-05-01",freq="MS")
    n = len(months)
    ban_idx = 18
    ev_pct = np.concatenate([
        np.linspace(0.5,3.0,ban_idx),
        np.linspace(3.0,92.0,n-ban_idx) + np.random.normal(0,2,n-ban_idx)
    ]).clip(0,100)
    return pd.DataFrame({"Month":months,"EV_Share_pct":ev_pct.round(1)})

# ══════════════════════════════════════════════════════════════════════════════
# 7. MODULAR CHART BUILDERS
# ══════════════════════════════════════════════════════════════════════════════

def _apply_base(fig, overrides: dict = None) -> go.Figure:
    layout = dict(**CHART_BASE)
    if overrides:
        layout.update(overrides)
    fig.update_layout(**layout)
    return fig

# ── Universal charts ──────────────────────────────────────────────────────────
def chart_brand_bar(df: pd.DataFrame, country: str) -> go.Figure:
    colors = [PwC_COLORS[i] if i < 3 else "#C0C8D8" for i in range(len(df))]
    fig = go.Figure(go.Bar(
        x=df["Brand"], y=df["Units"],
        text=[f"{p}%" for p in df["Share_pct"]], textposition="outside",
        textfont=dict(size=11,color="#2D3142",family="Inter"),
        marker=dict(color=colors,line=dict(color="white",width=1.5)),
        hovertemplate="<b>%{x}</b><br>Sales: <b>%{y:,}</b><br>Share: <b>%{text}</b><extra></extra>",
    ))
    return _apply_base(fig, {
        "yaxis":{**CHART_BASE["yaxis"],"title":"Units","range":[0,df["Units"].max()*1.22]},
        "xaxis":{**CHART_BASE["xaxis"],"title":"Brand"},
        "showlegend":False,"bargap":0.38,
    })

def chart_trend_area(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Year"],y=df["ICE"],name="ICE (Conventional)",
        mode="lines+markers",line=dict(color="#21325B",width=2.5),marker=dict(size=6,color="#21325B"),
        fill="tozeroy",fillcolor="rgba(33,50,91,0.08)",
        hovertemplate="<b>%{x}</b><br>ICE: <b>%{y:,}</b><extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df["Year"],y=df["EV"],name="EV / New Energy",
        mode="lines+markers",line=dict(color="#D04A02",width=2.5),
        marker=dict(size=7,color="#D04A02",symbol="diamond"),
        fill="tozeroy",fillcolor="rgba(208,74,2,0.10)",
        hovertemplate="<b>%{x}</b><br>EV: <b>%{y:,}</b><extra></extra>",
    ))
    fig.add_vline(x=2025.5,line_dash="dash",line_color="#9BA3B2",line_width=1)
    fig.add_annotation(x=2025.7,y=df["ICE"].max()*0.92,
        text="← Actual | Forecast →",showarrow=False,
        font=dict(size=9,color="#9BA3B2",family="Inter"))
    return _apply_base(fig, {
        "xaxis":{**CHART_BASE["xaxis"],"title":"Year","tickmode":"array","tickvals":df["Year"].tolist()},
        "yaxis":{**CHART_BASE["yaxis"],"title":"Units"},
    })

# ── South Africa exclusive charts ─────────────────────────────────────────────
def chart_za_freight_category(df: pd.DataFrame) -> go.Figure:
    df_s = df.sort_values("Revenue_ZAR_bn")
    fig = go.Figure(go.Bar(
        x=df_s["Revenue_ZAR_bn"], y=df_s["Category"],
        orientation="h",
        text=[f"R{v:.1f}bn  ({p:.1f}%)" for v,p in zip(df_s["Revenue_ZAR_bn"],df_s["Pct"])],
        textposition="outside",
        textfont=dict(size=10,family="Inter",color="#2D3142"),
        marker=dict(color=df_s["Color"],line=dict(color="white",width=1)),
        hovertemplate="<b>%{y}</b><br>Revenue: <b>R%{x:.1f}bn</b><br>Share: <b>%{text}</b><extra></extra>",
    ))
    return _apply_base(fig, {
        "xaxis":{**CHART_BASE["xaxis"],"title":"Freight Revenue (ZAR billion)",
                 "range":[0,df["Revenue_ZAR_bn"].max()*1.28]},
        "yaxis":{**CHART_BASE["yaxis"],"title":"","automargin":True},
        "showlegend":False,
        "margin":dict(l=160,r=20,t=20,b=50),
        "height":360,
    })

def chart_za_payload_income(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Quarter"],y=df["Payload_Mt"],name="Total Payload (Mt) ← Left axis",
        mode="lines+markers",yaxis="y1",
        line=dict(color="#D04A02",width=2.5),marker=dict(size=5,color="#D04A02"),
        fill="tozeroy",fillcolor="rgba(208,74,2,0.07)",
        hovertemplate="<b>%{x|Q%q %Y}</b><br>Payload: <b>%{y:.0f} Mt</b><extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df["Quarter"],y=df["Income_ZAR_bn"],name="Freight Income (R bn) → Right axis",
        mode="lines+markers",yaxis="y2",
        line=dict(color="#21325B",width=2.5),marker=dict(size=5,color="#21325B"),
        hovertemplate="<b>%{x|Q%q %Y}</b><br>Income: <b>R%{y:.1f}bn</b><extra></extra>",
    ))
    # Divergence annotation
    fig.add_annotation(
        x=df["Quarter"].iloc[-3],y=df["Payload_Mt"].iloc[-3],
        text="▼ Volume falling<br>▲ Revenue rising<br>= Cost squeeze",
        showarrow=True,arrowhead=2,arrowcolor="#D04A02",
        bgcolor="rgba(208,74,2,0.08)",bordercolor="#D04A02",
        font=dict(size=9,color="#D04A02",family="Inter"),ax=-80,ay=-50,
    )
    return _apply_base(fig, {
        "yaxis": {**CHART_BASE["yaxis"],"title":"Payload (million tonnes)","side":"left"},
        "yaxis2":{**CHART_BASE["yaxis"],"title":"Freight Income (R billion)",
                  "side":"right","overlaying":"y","showgrid":False},
        "xaxis": {**CHART_BASE["xaxis"],"title":"Quarter"},
        "legend":{**CHART_BASE["legend"],"y":-0.22},
    })

def chart_za_channel_donut(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure(go.Pie(
        labels=df["Channel"], values=df["Share_pct"],
        hole=0.58,
        marker=dict(colors=df["Color"].tolist(),line=dict(color="white",width=2)),
        textinfo="label+percent",
        textfont=dict(size=11,family="Inter",color="#2D3142"),
        hovertemplate="<b>%{label}</b><br>Share: <b>%{value:.1f}%</b><extra></extra>",
    ))
    fig.add_annotation(
        text="Sales<br>Channel", x=0.5,y=0.5,font=dict(size=12,family="Inter",color="#5A6070"),
        showarrow=False,
    )
    return _apply_base(fig, {
        "showlegend":True,
        "legend":dict(orientation="v",x=1.02,y=0.5,font=dict(size=11),bgcolor="rgba(0,0,0,0)"),
        "margin":dict(l=20,r=120,t=20,b=20),
        "height":300,
    })

def chart_za_province_bar(df: pd.DataFrame) -> go.Figure:
    colors = ["#D04A02" if i==0 else "#21325B" if i==1 else "#295BA5" if i==2
              else "#8BA7C4" for i in range(len(df))]
    fig = go.Figure(go.Bar(
        x=df["Province"],y=df["Units"],
        text=[f"{v:,}\n({s}%)" for v,s in zip(df["Units"],df["Share_pct"])],
        textposition="outside",textfont=dict(size=10,family="Inter"),
        marker=dict(color=colors,line=dict(color="white",width=1.5)),
        hovertemplate="<b>%{x}</b><br>Units: <b>%{y:,}</b><extra></extra>",
    ))
    return _apply_base(fig, {
        "yaxis":{**CHART_BASE["yaxis"],"title":"Units","range":[0,df["Units"].max()*1.25]},
        "xaxis":{**CHART_BASE["xaxis"],"title":"Province"},
        "showlegend":False,"bargap":0.35,
        "height":320,
    })

def chart_za_scissors() -> go.Figure:
    df = gen_za_rail_road()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Year"],y=df["Rail_Mt"],name="Transnet Rail Volume (Mt) ← Left",
        mode="lines+markers",yaxis="y1",
        line=dict(color="#D04A02",width=2.5),marker=dict(size=6,color="#D04A02"),
        fill="tozeroy",fillcolor="rgba(208,74,2,0.07)",
        hovertemplate="<b>%{x}</b><br>Rail: <b>%{y:.0f} Mt</b><extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df["Year"],y=df["HCV_Units"],name="HCV Road Sales (units) → Right",
        mode="lines+markers",yaxis="y2",
        line=dict(color="#21325B",width=2.5),marker=dict(size=6,color="#21325B"),
        hovertemplate="<b>%{x}</b><br>HCV Sales: <b>%{y:,} units</b><extra></extra>",
    ))
    fig.add_annotation(x=2018,y=228,text="Rail peak 2018:<br>228 Mt",
        showarrow=True,arrowhead=2,arrowcolor="#D04A02",
        font=dict(size=9,color="#D04A02",family="Inter"),ax=60,ay=-35)
    return _apply_base(fig, {
        "yaxis": {**CHART_BASE["yaxis"],"title":"Rail Volume (Mt)","side":"left"},
        "yaxis2":{**CHART_BASE["yaxis"],"title":"HCV Sales (units)",
                  "side":"right","overlaying":"y","showgrid":False},
        "xaxis": {**CHART_BASE["xaxis"],"title":"Year",
                  "tickmode":"array","tickvals":df["Year"].tolist()},
        "legend":{**CHART_BASE["legend"],"y":-0.22},
    })

# ── Nigeria exclusive charts ──────────────────────────────────────────────────
def chart_ng_waterfall(df: pd.DataFrame) -> go.Figure:
    inc_color = "#D04A02"
    dec_color = "#1A8C5B"
    tot_color = "#21325B"
    zer_color = "#1A8C5B"

    colors = []
    for m, v in zip(df["Measure"], df["Value"]):
        if m == "total":     colors.append(tot_color)
        elif v == 0:         colors.append(zer_color)
        elif m == "absolute":colors.append("#295BA5")
        else:                colors.append(inc_color)

    fig = go.Figure(go.Waterfall(
        orientation="v", measure=df["Measure"].tolist(),
        x=df["Label"].tolist(), y=df["Value"].tolist(),
        text=["FREE" if v==0 else f"${v:,.0f}" for v in df["Value"]],
        textposition="outside",
        textfont=dict(size=10,family="Inter",color="#2D3142"),
        connector=dict(line=dict(color="#E2E5EB",width=1)),
        increasing=dict(marker_color=inc_color),
        decreasing=dict(marker_color=dec_color),
        totals=dict(marker_color=tot_color),
        hovertemplate="<b>%{x}</b><br>Value: <b>$%{y:,.0f}</b><extra></extra>",
    ))
    fig.add_annotation(x=7,y=97000,
        text="💡 CKD saves ~$46,000<br>per unit vs CBU",
        showarrow=True,arrowhead=2,arrowcolor=dec_color,
        bgcolor="rgba(26,140,91,0.1)",bordercolor=dec_color,
        font=dict(size=10,color=dec_color,family="Inter"),ax=-90,ay=-50)
    return _apply_base(fig, {
        "yaxis":{**CHART_BASE["yaxis"],"title":"Cost (USD)"},
        "xaxis":{**CHART_BASE["xaxis"],"title":""},
        "showlegend":False,
        "margin":dict(l=60,r=20,t=30,b=70),
    })

# ── Morocco exclusive charts ──────────────────────────────────────────────────
def chart_ocp_throughput(df: pd.DataFrame) -> go.Figure:
    x_num = np.arange(len(df))
    trend = np.poly1d(np.polyfit(x_num, df["Throughput_kt"], 1))(x_num)
    growth = (df["Throughput_kt"].iloc[-1]/df["Throughput_kt"].iloc[0]-1)*100
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Month"],y=df["Throughput_kt"],name="Monthly Throughput (kt)",
        mode="lines",line=dict(color="#D04A02",width=2),
        fill="tozeroy",fillcolor="rgba(208,74,2,0.10)",
        hovertemplate="<b>%{x|%b %Y}</b><br>%{y:.0f} kt<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df["Month"],y=trend,name="Growth Trend",
        mode="lines",line=dict(color="#21325B",width=1.5,dash="dot"),
        hovertemplate="Trend: %{y:.0f} kt<extra></extra>",
    ))
    fig.add_annotation(x=df["Month"].iloc[-1],y=df["Throughput_kt"].iloc[-1],
        text=f"▲ +{growth:.1f}% since Jan 2023",showarrow=True,arrowhead=2,
        arrowcolor="#D04A02",font=dict(size=10,color="#D04A02",family="Inter"),ax=-110,ay=-40)
    return _apply_base(fig, {
        "xaxis":{**CHART_BASE["xaxis"],"title":"Month"},
        "yaxis":{**CHART_BASE["yaxis"],"title":"Throughput (thousand tonnes)"},
    })

# ── Ethiopia exclusive charts ─────────────────────────────────────────────────
def chart_eth_ev_surge(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Month"],y=df["EV_Share_pct"],name="EV Market Share (%)",
        mode="lines",line=dict(color="#D04A02",width=2.5),
        fill="tozeroy",fillcolor="rgba(208,74,2,0.12)",
        hovertemplate="<b>%{x|%b %Y}</b><br>EV Share: <b>%{y:.1f}%</b><extra></extra>",
    ))
    fig.add_vline(x=pd.Timestamp("2022-07-01"),line_dash="dash",line_color="#21325B",line_width=1.5)
    fig.add_annotation(x=pd.Timestamp("2022-07-01"),y=50,
        text="⚡ Petroleum ban<br>enacted Jul 2022",
        showarrow=False,xanchor="left",xshift=8,
        bgcolor="rgba(33,50,91,0.08)",bordercolor="#21325B",
        font=dict(size=9,color="#21325B",family="Inter"))
    return _apply_base(fig, {
        "xaxis":{**CHART_BASE["xaxis"],"title":"Month"},
        "yaxis":{**CHART_BASE["yaxis"],"title":"EV Market Share (%)","range":[0,105]},
        "showlegend":False,
    })

# ══════════════════════════════════════════════════════════════════════════════
# 8. MAP BUILDER
# ══════════════════════════════════════════════════════════════════════════════
def build_map(selected_name: str) -> go.Figure:
    selected_iso = next(
        (d["iso"] for n,d in TIER1.items() if n == selected_name), ""
    ) or next(
        (iso for iso,name in ALL_AFRICA.items() if name == selected_name), ""
    )
    rows = []
    for iso in ALL_ISO_LIST:
        name    = ISO_TO_NAME.get(iso, iso)
        is_t1   = name in TIER1
        is_sel  = iso == selected_iso
        score   = 100 if is_sel else 70 if is_t1 else 20
        group   = "selected" if is_sel else "tier1" if is_t1 else "base"

        if is_t1:
            d = TIER1[name]
            kpi_text = "<br>".join(f"<b>{v[0]}</b> {v[1]}" for v in d["kpi"].values())
            tip = (f"<b style='font-size:13px;'>{d['flag']} {name}</b><br>"
                   f"<span style='color:#9BA3B2;font-size:10px;'>TIER 1 · {d['region']}</span><br><br>"
                   f"{kpi_text}<br><br>"
                   f"<span style='color:#D04A02;font-size:10px;'>● Click to drill down</span>")
        else:
            m = TIER2_MACRO.get(iso,{})
            flag = m.get("flag","🌍"); region = m.get("region","Africa")
            tip = (f"<b style='font-size:13px;'>{flag} {name}</b><br>"
                   f"<span style='color:#9BA3B2;font-size:10px;'>{region}</span><br><br>"
                   f"Est. GDP: <b>${m.get('gdp','N/A')}B</b><br>"
                   f"Est. CV Imports: <b>{m.get('cv_imports','N/A'):,} units/yr</b><br>"
                   f"Road Network: <b>{m.get('roads','N/A')}k km</b><br><br>"
                   f"<span style='color:#295BA5;font-size:10px;'>● Click for live news</span>")
        rows.append({"iso":iso,"score":score,"group":group,"tooltip":tip})

    df = pd.DataFrame(rows)
    fig = go.Figure()

    for grp, cs, lw, lc in [
        ("base",    [[0,"#E8ECF4"],[1,"#D0D6E2"]], 0.5, "#C8CDD8"),
        ("tier1",   [[0,"#6E90BF"],[1,"#295BA5"]], 0.9, "#21325B"),
        ("selected",[[0,"#D04A02"],[1,"#EB6C2D"]], 2.0, "#8B3000"),
    ]:
        sub = df[df.group==grp]
        if not sub.empty:
            fig.add_trace(go.Choropleth(
                locations=sub.iso, z=sub.score,
                text=sub.tooltip, hovertemplate="%{text}<extra></extra>",
                colorscale=cs, showscale=False,
                marker_line_color=lc, marker_line_width=lw,
                zmin=0, zmax=100,
            ))

    fig.update_layout(
        geo=dict(scope="africa",showframe=False,showcoastlines=True,
                 coastlinecolor="#C8CDD8",coastlinewidth=0.6,
                 showland=True,landcolor="#F0F2F6",
                 showocean=True,oceancolor="#E4EEF8",
                 showcountries=True,countrycolor="#C8CDD8",countrywidth=0.5,
                 bgcolor="#F4F5F7",projection_type="natural earth"),
        paper_bgcolor="#F4F5F7",plot_bgcolor="#F4F5F7",
        margin=dict(l=0,r=0,t=0,b=0),height=420,
        hoverlabel=dict(bgcolor="white",bordercolor="#E2E5EB",
                        font=dict(family="Inter",size=12,color="#2D3142")),
        dragmode=False,
    )
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# 9. COUNTRY PANEL RENDERERS — Modular, one function per country group
# ══════════════════════════════════════════════════════════════════════════════

def _chart_header(label: str, title: str, sub: str, source_name: str, source_url: str):
    st.markdown(f"""
    <div class="chart-card">
        <div class="chart-label">{label}</div>
        <div class="chart-title">{title}</div>
        <div class="chart-sub">{sub}</div>
        <div class="source-link">📌 <a href="{source_url}" target="_blank">{source_name}</a></div>
    </div>
    """, unsafe_allow_html=True)

def _section_divider(title: str, sub: str = ""):
    st.markdown(f"""
    <div class="section-hdr" style="margin-top:28px;">
        <div class="section-bar"></div>
        <div class="section-title">{title}</div>
        {"<div class='section-sub'>"+sub+"</div>" if sub else ""}
    </div>
    """, unsafe_allow_html=True)


def render_market_tab_south_africa(cdata: dict):
    """Full Market Analytics panel for South Africa."""
    src_trade   = cdata["sources"]["trade"]
    src_customs = cdata["sources"]["customs"]
    src_market  = cdata["sources"]["market"]
    STATSSA_URL = "https://www.statssa.gov.za/publications/P7162/P7162.html"
    NAAMSA_URL  = "https://naamsa.co.za"
    TRANSNET_URL= "https://www.transnet.net/InvestorCentre/Pages/AnnualReports.aspx"

    # ── KPIs
    kpi_items = list(cdata["kpi"].items())
    for col, (key,(val,lbl,delta,src_url)) in zip(st.columns(len(kpi_items)), kpi_items):
        with col:
            dc = "normal" if "+" in delta else "inverse" if "-" in delta else "off"
            st.metric(key, val, delta, delta_color=dc, help=lbl)
    st.caption(f"Source: [{src_trade[0]}]({src_trade[1]}) · Simulated data for illustrative purposes.")
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 1: Brand share + Trend
    c1, c2 = st.columns(2, gap="large")
    with c1:
        _chart_header("Market Share","Brand Rankings — South Africa",
                      "Top 5 brands by annual HCV unit sales",src_trade[0],src_trade[1])
        st.plotly_chart(chart_brand_bar(gen_brand_share_df("South Africa"),"South Africa"),
                        use_container_width=True,config={"displayModeBar":False},key="za_brand")
    with c2:
        _chart_header("Sales Trend 2021–2026","ICE vs. EV — South Africa",
                      "Historical actuals + 2026 forecast",src_trade[0],src_trade[1])
        st.plotly_chart(chart_trend_area(gen_trend_df("South Africa")),
                        use_container_width=True,config={"displayModeBar":False},key="za_trend")

    # ── Section: Stats SA Deep Modules
    _section_divider("Stats SA P7162 — Road Freight Survey Deep Dive",
                     "Exclusive Tier 1 analytics · Modelled on Stats SA P7162 report structure")

    # ── Module 1: Freight Category Horizontal Bar
    _chart_header(
        "Exclusive Module 1 · Stats SA P7162",
        "Road Freight Revenue by Commodity Category",
        "Annual freight revenue breakdown (ZAR billion) — Mining dominates at 35.4% of total",
        "Stats SA — Road Freight Survey P7162", STATSSA_URL,
    )
    st.plotly_chart(chart_za_freight_category(gen_za_freight_category()),
                    use_container_width=True,config={"displayModeBar":False},key="za_freight_cat")
    st.caption(
        "Mining & Quarrying accounts for 35.4% of total road freight revenue, driven by iron ore, "
        "coal, and platinum group metals. Parcels & Express is the fastest-growing segment (+12% YoY). "
        f"Source: [Stats SA — P7162 Road Freight Survey]({STATSSA_URL}) · "
        "Simulated data modelled on actual report structure."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Module 2: Payload vs Income (dual-axis)
    _chart_header(
        "Exclusive Module 2 · Stats SA P7162",
        "Payload Volume vs. Freight Income — The Cost Squeeze",
        "Left axis: total payload (Mt) falling. Right axis: freight income (R bn) rising. "
        "Divergence = per-km cost inflation burden on fleet operators.",
        "Stats SA — Road Freight Survey P7162", STATSSA_URL,
    )
    st.plotly_chart(chart_za_payload_income(gen_za_payload_vs_income()),
                    use_container_width=True,config={"displayModeBar":False},key="za_payload")
    st.caption(
        "⚠ Fleet operators carried **22% fewer tonnes** in 2026 vs 2020, yet freight income grew "
        "by 66% over the same period — driven by diesel cost pass-through and toll escalation. "
        f"Source: [Stats SA P7162]({STATSSA_URL}) · Simulated quarterly data for illustrative purposes."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Module 3: Sales Channel Donut + Province Bar
    _section_divider("NAAMSA — Sales Channel & Provincial Distribution",
                     "Exclusive Tier 1 analytics · NAAMSA monthly release structure")

    ch_l, ch_r = st.columns([2,3], gap="large")
    with ch_l:
        _chart_header(
            "Exclusive Module 3a · NAAMSA",
            "HCV Sales by Channel",
            "Dealer retail dominates; corporate fleet growing",
            "NAAMSA — Automotive Business Council", NAAMSA_URL,
        )
        st.plotly_chart(chart_za_channel_donut(gen_za_sales_channel()),
                        use_container_width=True,config={"displayModeBar":False},key="za_channel")
        st.caption(f"Source: [NAAMSA]({NAAMSA_URL}) · Simulated data.")
    with ch_r:
        _chart_header(
            "Exclusive Module 3b · NAAMSA",
            "HCV Sales by Province",
            "Gauteng accounts for 45.1% of all HCV sales — industrial heartland concentration",
            "NAAMSA — Automotive Business Council", NAAMSA_URL,
        )
        st.plotly_chart(chart_za_province_bar(gen_za_province_sales()),
                        use_container_width=True,config={"displayModeBar":False},key="za_province")
        st.caption(f"Source: [NAAMSA]({NAAMSA_URL}) · Simulated provincial distribution.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Module 4: Rail Crisis Scissors
    _section_divider("Transnet Rail Crisis — Road Transport Demand Driver",
                     "Structural shift analysis · Dual-axis scissors effect")
    _chart_header(
        "Exclusive Module 4 · Transnet / NAAMSA",
        "Transnet Rail Volume Collapse vs. HCV Road Sales Surge",
        "Rail freight down 46% from 2018 peak; road HCV absorbs displaced demand",
        "Transnet Annual Report", TRANSNET_URL,
    )
    st.plotly_chart(chart_za_scissors(),use_container_width=True,
                    config={"displayModeBar":False},key="za_scissors")
    st.caption(
        f"Source: [Transnet Investor Relations]({TRANSNET_URL}) · "
        f"[NAAMSA]({NAAMSA_URL}) · Simulated data for illustrative purposes."
    )


def render_market_tab_nigeria(cdata: dict):
    """Full Market Analytics panel for Nigeria."""
    src_trade   = cdata["sources"]["trade"]
    NADDC_URL   = "https://naddc.gov.ng"
    CUSTOMS_URL = "https://customs.gov.ng"

    kpi_items = list(cdata["kpi"].items())
    for col, (key,(val,lbl,delta,src_url)) in zip(st.columns(len(kpi_items)), kpi_items):
        with col:
            dc = "normal" if "+" in delta else "inverse" if "-" in delta else "off"
            st.metric(key, val, delta, delta_color=dc, help=lbl)
    st.caption(f"Source: [{src_trade[0]}]({src_trade[1]}) · Simulated data for illustrative purposes.")
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        _chart_header("Market Share","Brand Rankings — Nigeria",
                      "Top 5 brands by annual HCV unit sales",src_trade[0],src_trade[1])
        st.plotly_chart(chart_brand_bar(gen_brand_share_df("Nigeria"),"Nigeria"),
                        use_container_width=True,config={"displayModeBar":False},key="ng_brand")
    with c2:
        _chart_header("Sales Trend 2021–2026","ICE vs. EV — Nigeria",
                      "Historical actuals + 2026 forecast",src_trade[0],src_trade[1])
        st.plotly_chart(chart_trend_area(gen_trend_df("Nigeria")),
                        use_container_width=True,config={"displayModeBar":False},key="ng_trend")

    _section_divider("Tariff Structure Analysis — The Zero-Duty Dividend",
                     "Exclusive Tier 1 module · Per-unit landed cost comparison")
    _chart_header(
        "Exclusive Module · Nigeria Customs / NADDC",
        "CBU vs. CKD/SKD Import Cost Waterfall",
        "Per-unit landed cost for a 30-tonne HCV (base price $100,000). "
        "CKD route saves ~$46,000 per unit under 2023 EV/assembly tariff regime.",
        "Nigeria Customs Service", CUSTOMS_URL,
    )
    st.plotly_chart(chart_ng_waterfall(gen_ng_tariff_waterfall()),
                    use_container_width=True,config={"displayModeBar":False},key="ng_waterfall")
    st.caption(
        f"Source: [Nigeria Customs Service]({CUSTOMS_URL}) · "
        f"[NADDC]({NADDC_URL}) · Figures illustrative; actual costs vary by port and broker."
    )


def render_market_tab_morocco(cdata: dict):
    """Full Market Analytics panel for Morocco."""
    src_trade = cdata["sources"]["trade"]
    OCP_URL   = "https://www.ocpgroup.ma/investor-relations"
    AIVAM_URL = "http://www.aivam.ma"

    kpi_items = list(cdata["kpi"].items())
    for col, (key,(val,lbl,delta,src_url)) in zip(st.columns(len(kpi_items)), kpi_items):
        with col:
            dc = "normal" if "+" in delta else "inverse" if "-" in delta else "off"
            st.metric(key, val, delta, delta_color=dc, help=lbl)
    st.caption(f"Source: [{src_trade[0]}]({src_trade[1]}) · Simulated data for illustrative purposes.")
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        _chart_header("Market Share","Brand Rankings — Morocco",
                      "Top 5 brands by annual HCV unit sales",src_trade[0],src_trade[1])
        st.plotly_chart(chart_brand_bar(gen_brand_share_df("Morocco"),"Morocco"),
                        use_container_width=True,config={"displayModeBar":False},key="ma_brand")
    with c2:
        _chart_header("Sales Trend 2021–2026","ICE vs. EV — Morocco",
                      "Historical actuals + 2026 forecast",src_trade[0],src_trade[1])
        st.plotly_chart(chart_trend_area(gen_trend_df("Morocco")),
                        use_container_width=True,config={"displayModeBar":False},key="ma_trend")

    _section_divider("OCP Group Road Freight Corridor",
                     "Exclusive Tier 1 module · Phosphate mining logistics")
    _chart_header(
        "Exclusive Module · OCP Group",
        "OCP Phosphate Road Freight Throughput — Khouribga–Jorf Lasfar Corridor",
        "Monthly throughput (thousand tonnes) 2023–2026. OCP accounts for ~800 HCV units/yr procurement.",
        "OCP Group Investor Relations", OCP_URL,
    )
    df_ocp = gen_ocp_throughput()
    st.plotly_chart(chart_ocp_throughput(df_ocp),use_container_width=True,
                    config={"displayModeBar":False},key="ma_ocp")
    st.caption(
        f"Source: [OCP Group IR]({OCP_URL}) · [AIVAM]({AIVAM_URL}) · "
        "Simulated data modelled on OCP annual report structure."
    )


def render_market_tab_ethiopia(cdata: dict):
    """Full Market Analytics panel for Ethiopia."""
    src_trade = cdata["sources"]["trade"]
    MOTI_URL  = "https://www.moti.gov.et"
    ERCA_URL  = "https://www.erca.gov.et"

    kpi_items = list(cdata["kpi"].items())
    for col, (key,(val,lbl,delta,src_url)) in zip(st.columns(len(kpi_items)), kpi_items):
        with col:
            dc = "normal" if "+" in delta else "inverse" if "-" in delta else "off"
            st.metric(key, val, delta, delta_color=dc, help=lbl)
    st.caption(f"Source: [{src_trade[0]}]({src_trade[1]}) · Simulated data for illustrative purposes.")
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        _chart_header("Market Share","Brand Rankings — Ethiopia",
                      "Post-ban EV brand landscape",src_trade[0],src_trade[1])
        st.plotly_chart(chart_brand_bar(gen_brand_share_df("Ethiopia"),"Ethiopia"),
                        use_container_width=True,config={"displayModeBar":False},key="eth_brand")
    with c2:
        _chart_header("Sales Trend 2021–2026","ICE vs. EV — Ethiopia",
                      "Dramatic ICE decline post petroleum ban",src_trade[0],src_trade[1])
        st.plotly_chart(chart_trend_area(gen_trend_df("Ethiopia")),
                        use_container_width=True,config={"displayModeBar":False},key="eth_trend")

    _section_divider("EV Penetration Surge — Post Petroleum Import Ban",
                     "Exclusive Tier 1 module · Fastest EV transition on the continent")
    _chart_header(
        "Exclusive Module · MoTI Ethiopia / ERCA",
        "EV Market Share Trajectory — Monthly, 2021–2026",
        "From <3% to >85% EV share in 30 months following July 2022 petroleum import ban.",
        "Ministry of Trade & Industry — Ethiopia", MOTI_URL,
    )
    df_eth = gen_eth_ev_surge()
    st.plotly_chart(chart_eth_ev_surge(df_eth),use_container_width=True,
                    config={"displayModeBar":False},key="eth_ev")
    st.caption(
        f"Source: [MoTI Ethiopia]({MOTI_URL}) · [ERCA]({ERCA_URL}) · "
        "Simulated data for illustrative purposes."
    )


def render_market_tab_generic(country: str, cdata: dict):
    """Generic Market Analytics panel for Egypt, Kenya, Algeria, Tunisia."""
    src_trade = cdata["sources"]["trade"]
    kpi_items = list(cdata["kpi"].items())
    for col, (key,(val,lbl,delta,src_url)) in zip(st.columns(len(kpi_items)), kpi_items):
        with col:
            dc = "normal" if "+" in delta else "inverse" if "-" in delta else "off"
            st.metric(key, val, delta, delta_color=dc, help=lbl)
    st.caption(f"Source: [{src_trade[0]}]({src_trade[1]}) · Simulated data for illustrative purposes.")
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        _chart_header("Market Share",f"Brand Rankings — {country}",
                      "Top 5 brands by annual HCV unit sales",src_trade[0],src_trade[1])
        st.plotly_chart(chart_brand_bar(gen_brand_share_df(country),country),
                        use_container_width=True,config={"displayModeBar":False},key=f"{country}_brand")
    with c2:
        _chart_header("Sales Trend 2021–2026",f"ICE vs. EV — {country}",
                      "Historical actuals + 2026 forecast",src_trade[0],src_trade[1])
        st.plotly_chart(chart_trend_area(gen_trend_df(country)),
                        use_container_width=True,config={"displayModeBar":False},key=f"{country}_trend")

    # Market entry scorecard
    _section_divider("Market Entry Assessment Scorecard")
    all_scores = {
        "Egypt":   {"Market Size":7,"EV Readiness":3,"Tariff Advantage":5,"Regulatory Ease":5,"Growth Momentum":8},
        "Kenya":   {"Market Size":6,"EV Readiness":6,"Tariff Advantage":6,"Regulatory Ease":7,"Growth Momentum":8},
        "Algeria": {"Market Size":6,"EV Readiness":2,"Tariff Advantage":4,"Regulatory Ease":3,"Growth Momentum":5},
        "Tunisia": {"Market Size":4,"EV Readiness":5,"Tariff Advantage":7,"Regulatory Ease":7,"Growth Momentum":4},
    }
    scores = all_scores.get(country,{d:5 for d in ["Market Size","EV Readiness","Tariff Advantage","Regulatory Ease","Growth Momentum"]})
    for col,(dim,score) in zip(st.columns(5), scores.items()):
        color = "#D04A02" if score>=8 else "#295BA5" if score>=6 else "#9BA3B2"
        with col:
            st.markdown(f"""
            <div style="background:white;border:1px solid #E2E5EB;border-radius:8px;
                        padding:14px 12px;box-shadow:0 1px 4px rgba(0,0,0,.06);text-align:center;">
                <div style="font-family:'Inter';font-size:.6rem;font-weight:700;
                            text-transform:uppercase;letter-spacing:.6px;color:#9BA3B2;margin-bottom:7px;">{dim}</div>
                <div style="font-family:'Inter';font-size:1.5rem;font-weight:700;color:{color};">
                    {score}<span style="font-size:.72rem;color:#9BA3B2;">/10</span></div>
                <div style="background:#F0F2F5;border-radius:3px;height:4px;margin-top:8px;">
                    <div style="background:{color};width:{score*10}%;height:4px;border-radius:3px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.caption(f"Source: [{src_trade[0]}]({src_trade[1]}) · Assessment based on simulated market intelligence.")

# ══════════════════════════════════════════════════════════════════════════════
# 10. SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if "selected_country" not in st.session_state:
    st.session_state.selected_country = "Nigeria"

# ══════════════════════════════════════════════════════════════════════════════
# 11. SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 4px 12px 4px;border-bottom:1px solid rgba(255,255,255,.12);">
        <div style="font-family:'Inter';font-size:1.05rem;font-weight:700;color:white;letter-spacing:-.2px;">
            Africa CV Intelligence
        </div>
        <div style="font-family:'Inter';font-size:.68rem;color:rgba(255,255,255,.4);margin-top:2px;">
            Enterprise Market Analytics · v6.0
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

    st.markdown('<div class="sb-hdr">Quick Reference</div>', unsafe_allow_html=True)
    for label, url in [
        ("🏛 Nigeria Customs (NCS)","https://www.customs.gov.ng"),
        ("📊 Stats SA — P7162","https://www.statssa.gov.za"),
        ("🏭 NAAMSA","https://naamsa.co.za"),
        ("🚂 Transnet Annual Reports","https://www.transnet.net/InvestorCentre"),
        ("🌾 OCP Group Morocco","https://www.ocpgroup.ma"),
        ("🌍 AfDB","https://www.afdb.org"),
        ("📰 The Africa Report","https://www.theafricareport.com"),
        ("📊 Zawya Finance","https://www.zawya.com"),
    ]:
        st.markdown(f'<a class="sb-link" href="{url}" target="_blank">{label}</a>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↺  Refresh Intelligence Feed", use_container_width=True, key="refresh"):
        st.cache_data.clear()
        st.rerun()
    st.markdown(f"""
    <div style="font-family:'Inter';font-size:.58rem;color:rgba(255,255,255,.22);
                text-align:center;margin-top:16px;line-height:2.1;">
        Africa CV Market Intelligence v6.0<br>
        {datetime.now().strftime('%Y-%m-%d %H:%M')} · Internal use only
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 12. PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
h1, h2 = st.columns([3,1])
with h1:
    st.markdown("""
    <div style="padding:18px 0 6px 0;">
        <div style="font-family:'Inter';font-size:1.28rem;font-weight:700;color:#2D3142;letter-spacing:-.3px;">
            Africa Commercial Vehicle Market Intelligence
        </div>
        <div style="font-family:'Inter';font-size:.78rem;color:#9BA3B2;margin-top:3px;">
            54-nation coverage · Tier 1 deep analytics · Stats SA P7162 · NAAMSA · Click any country on the map
        </div>
    </div>
    """, unsafe_allow_html=True)
with h2:
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
# 13. MAP SECTION
# ══════════════════════════════════════════════════════════════════════════════
sel   = st.session_state.selected_country
is_t1 = sel in TIER1
cdata = TIER1.get(sel, {})
sel_iso = cdata.get("iso","") if is_t1 else next(
    (iso for iso, name in ALL_AFRICA.items() if name == sel), "")
macro = TIER2_MACRO.get(sel_iso, {})

map_col, snap_col = st.columns([5,2], gap="large")

with map_col:
    st.markdown("""
    <div style="font-family:'Inter';font-size:.7rem;font-weight:700;letter-spacing:.8px;
                text-transform:uppercase;color:#5A6070;margin-bottom:8px;">
        Africa Strategic Market Map
        <span style="font-weight:400;color:#9BA3B2;margin-left:8px;">
            · Click any country to drill down · Orange = selected · Blue = Tier 1 coverage
        </span>
    </div>
    """, unsafe_allow_html=True)

    map_fig   = build_map(sel)
    map_event = st.plotly_chart(
        map_fig, use_container_width=True,
        config={"displayModeBar":False,"scrollZoom":False},
        on_select="rerun", selection_mode="points", key="africa_map",
    )

    if map_event and hasattr(map_event,"selection") and map_event.selection:
        pts = map_event.selection.get("points",[])
        if pts:
            clicked_iso  = pts[0].get("location","")
            clicked_name = ISO_TO_NAME.get(clicked_iso,"")
            if clicked_name and clicked_name != st.session_state.selected_country:
                st.session_state.selected_country = clicked_name
                st.cache_data.clear()
                st.rerun()

    # Legend
    leg_cols = st.columns(len(TIER1))
    for lc,(cname,cd) in zip(leg_cols, TIER1.items()):
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
    flag   = cdata.get("flag","🌍") if is_t1 else macro.get("flag","🌍")
    region = cdata.get("region","Africa") if is_t1 else macro.get("region","Africa")
    sources = cdata.get("sources",{}) if is_t1 else {}
    main_src = list(sources.values())[0] if sources else ("","")

    st.markdown(f"""
    <div style="background:white;border:1px solid #E2E5EB;border-radius:8px;
                padding:18px;box-shadow:0 1px 4px rgba(0,0,0,.07);border-top:4px solid #D04A02;">
        <div style="font-family:'Inter';font-size:.68rem;font-weight:700;
                    letter-spacing:.8px;text-transform:uppercase;color:#9BA3B2;margin-bottom:10px;">
            Currently Viewing
        </div>
        <div style="font-size:1.8rem;margin-bottom:3px;">{flag}</div>
        <div style="font-family:'Inter';font-size:1.05rem;font-weight:700;color:#2D3142;">{sel}</div>
        <div style="font-family:'Inter';font-size:.72rem;color:#9BA3B2;margin-bottom:12px;">{region}</div>
        <div style="border-top:1px solid #F0F2F5;padding-top:12px;">
    """, unsafe_allow_html=True)

    if not is_t1:
        st.markdown('<div class="fallback-badge">⚠ Tier 2 — General Coverage</div>', unsafe_allow_html=True)
        for label,val in [
            ("Est. GDP","${:,.1f}B".format(macro.get("gdp",0))),
            ("Road Network","{:,}k km".format(macro.get("roads",0))),
            ("Est. CV Imports","{:,} units/yr".format(macro.get("cv_imports",0))),
        ]:
            st.markdown(f"""
            <div style="margin-bottom:10px;">
                <div style="font-family:'Inter';font-size:.65rem;color:#9BA3B2;text-transform:uppercase;letter-spacing:.5px;">{label}</div>
                <div style="font-family:'Inter';font-size:1.1rem;font-weight:700;color:#2D3142;">{val}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        for key,(value,label,delta,src_url) in cdata["kpi"].items():
            delta_color = "#1A8C5B" if "+" in delta else "#D04A02" if "-" in delta else "#5A6070"
            st.markdown(f"""
            <div style="margin-bottom:11px;padding-bottom:11px;border-bottom:1px solid #F0F2F5;">
                <div style="font-family:'Inter';font-size:.65rem;color:#9BA3B2;text-transform:uppercase;letter-spacing:.5px;">{label}</div>
                <div style="font-family:'Inter';font-size:1.1rem;font-weight:700;color:#2D3142;margin:2px 0;">{value}</div>
                <div style="font-family:'Inter';font-size:.68rem;color:{delta_color};font-weight:500;">{delta}</div>
            </div>
            """, unsafe_allow_html=True)
        if main_src[0]:
            st.markdown(f"""
            <div style="font-family:'Inter';font-size:.62rem;color:#295BA5;margin-top:4px;">
                📌 <a href="{main_src[1]}" target="_blank" style="color:#295BA5;">{main_src[0]}</a>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 14. COUNTRY DASHBOARD TABS
# ══════════════════════════════════════════════════════════════════════════════
flag_display = cdata.get("flag", macro.get("flag","🌍")) if is_t1 else macro.get("flag","🌍")
st.markdown(f"""
<div class="section-hdr">
    <div class="section-bar"></div>
    <div class="section-title">{flag_display} &nbsp;{sel} — Country Dashboard</div>
    <div class="section-sub">
        {"Full Tier 1 analytics · Stats SA P7162 · NAAMSA" if sel=="South Africa" else
         "Full Tier 1 analytics" if is_t1 else
         "General coverage — live news + macro indicators"}
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
            f"**{sel}** is a Tier 2 market. Full analytics available for 8 Tier 1 core markets. "
            "Showing macroeconomic overview and live intelligence.", icon="ℹ️"
        )
        m1,m2,m3 = st.columns(3)
        with m1: st.metric("Est. GDP","${:,.1f}B".format(macro.get("gdp",0)),help="IMF WEO estimate")
        with m2: st.metric("Road Network","{:,}k km".format(macro.get("roads",0)),help="AfDB infrastructure data")
        with m3: st.metric("Est. CV Imports","{:,} units/yr".format(macro.get("cv_imports",0)),help="Regional trade flow estimate")
        st.caption("Source: [AfDB](https://www.afdb.org) · [IMF WEO](https://www.imf.org) · Indicative estimates only.")
    elif sel == "South Africa":
        render_market_tab_south_africa(cdata)
    elif sel == "Nigeria":
        render_market_tab_nigeria(cdata)
    elif sel == "Morocco":
        render_market_tab_morocco(cdata)
    elif sel == "Ethiopia":
        render_market_tab_ethiopia(cdata)
    else:
        render_market_tab_generic(sel, cdata)

# ── TAB 2: Policy & Market Access ─────────────────────────────────────────────
with tab_policy:
    if not is_t1:
        st.info(
            f"Detailed policy brief for **{sel}** not yet available. "
            "Showing AfCFTA general framework.", icon="📋"
        )
        st.markdown("""
        <div class="pol-card">
            <div class="pol-card-title">🌍 African Continental Free Trade Area (AfCFTA)</div>
            <p>Under AfCFTA, member states are progressively eliminating tariffs on 90% of goods.
            Commercial vehicles are classified as sensitive goods with 10–15 year phase-out timelines.
            Check the AfCFTA Secretariat for country-specific schedules.</p>
        </div>
        """, unsafe_allow_html=True)
        st.caption("Source: [AfCFTA Secretariat](https://au-afcfta.org) · [AfDB Trade Finance](https://www.afdb.org)")
    else:
        p = cdata["policy"]
        src_customs = cdata["sources"].get("customs",("",""))
        src_market  = cdata["sources"].get("market",("",""))
        src_trade   = cdata["sources"].get("trade",("",""))

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
                <div class="pol-card-title">📋 Certification & Homologation</div>
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

        _section_divider("Market Entry Assessment Scorecard")
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
        for col,(dim,score) in zip(st.columns(5),scores.items()):
            color = "#D04A02" if score>=8 else "#295BA5" if score>=6 else "#9BA3B2"
            with col:
                st.markdown(f"""
                <div style="background:white;border:1px solid #E2E5EB;border-radius:8px;
                            padding:14px 12px;box-shadow:0 1px 4px rgba(0,0,0,.06);text-align:center;">
                    <div style="font-family:'Inter';font-size:.6rem;font-weight:700;text-transform:uppercase;
                                letter-spacing:.6px;color:#9BA3B2;margin-bottom:7px;">{dim}</div>
                    <div style="font-family:'Inter';font-size:1.5rem;font-weight:700;color:{color};">
                        {score}<span style="font-size:.72rem;color:#9BA3B2;">/10</span></div>
                    <div style="background:#F0F2F5;border-radius:3px;height:4px;margin-top:8px;">
                        <div style="background:{color};width:{score*10}%;height:4px;border-radius:3px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.caption(f"Source: [{src_trade[0]}]({src_trade[1]}) · Assessment based on simulated market intelligence.")

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
        &nbsp;·&nbsp; Wide-net fetch → authority filter → fallback guarantee
        {"&nbsp;·&nbsp; <span style='color:#D04A02;'>⚠ Tier 2 — general coverage</span>" if not is_t1 else ""}
    </div>
    """, unsafe_allow_html=True)

    news_col, params_col = st.columns([3,1], gap="large")

    with news_col:
        render_news_panel(news_query, sel)

    with params_col:
        st.markdown("""
        <div style="background:white;border:1px solid #E2E5EB;border-radius:8px;
                    padding:16px;box-shadow:0 1px 4px rgba(0,0,0,.06);">
            <div style="font-family:'Inter';font-size:.68rem;font-weight:700;text-transform:uppercase;
                        letter-spacing:.6px;color:#9BA3B2;margin-bottom:12px;">Fetch Strategy</div>
        """, unsafe_allow_html=True)
        for label, val in [
            ("Pass 1","Broad query + when:30d"),
            ("Pass 2","Authority domain filter"),
            ("Pass 3","All recent results"),
            ("Pass 4","90-day fallback"),
            ("Cache TTL","30 minutes"),
        ]:
            st.markdown(f"""
            <div style="margin-bottom:9px;">
                <div style="font-family:'Inter';font-size:.62rem;color:#9BA3B2;">{label}</div>
                <div style="font-family:'Inter';font-size:.78rem;font-weight:500;color:#2D3142;">{val}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f"""
            <div style="margin-top:8px;padding-top:8px;border-top:1px solid #F0F2F5;">
                <div style="font-family:'Inter';font-size:.62rem;color:#9BA3B2;margin-bottom:4px;">Keywords</div>
                <div style="font-family:'Inter';font-size:.72rem;color:#5A6070;line-height:1.6;
                            word-break:break-word;background:#F8F9FB;border-radius:5px;padding:7px 9px;">
                    {news_query}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:white;border:1px solid #E2E5EB;border-radius:8px;
                    padding:16px;box-shadow:0 1px 4px rgba(0,0,0,.06);">
            <div style="font-family:'Inter';font-size:.68rem;font-weight:700;text-transform:uppercase;
                        letter-spacing:.6px;color:#9BA3B2;margin-bottom:10px;">Authority Domains</div>
        """, unsafe_allow_html=True)
        for src, url in [
            ("Reuters","https://reuters.com"),("Bloomberg","https://bloomberg.com"),
            ("Financial Times","https://ft.com"),("Engineering News ZA","https://engineeringnews.co.za"),
            ("BusinessDay NG","https://businessday.ng"),("Zawya","https://zawya.com"),
            ("The Africa Report","https://theafricareport.com"),("AfDB","https://afdb.org"),
        ]:
            st.markdown(f"""
            <div style="font-family:'Inter';font-size:.72rem;color:#5A6070;
                        padding:4px 0;border-bottom:1px solid #F4F5F7;">
                <span style="display:inline-block;width:6px;height:6px;border-radius:50%;
                             background:#1A8C5B;margin-right:6px;"></span>
                <a href="https://{url}" target="_blank" style="color:#295BA5;text-decoration:none;">{src}</a>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 15. FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="border-top:1px solid #E2E5EB;padding-top:14px;
            font-family:'Inter';font-size:.68rem;color:#9BA3B2;">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
        <div>
            <strong style="color:#5A6070;">Africa CV Market Intelligence Platform v6.0</strong>
            &nbsp;·&nbsp; Internal strategic use only
            &nbsp;·&nbsp; Simulated data for illustrative purposes
            &nbsp;·&nbsp; 54-nation coverage · Stats SA P7162 · NAAMSA
        </div>
        <div style="text-align:right;">
            Reuters · Bloomberg · FT · NAAMSA · NADDC · Stats SA · AIVAM · AfDB
            &nbsp;·&nbsp; {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
