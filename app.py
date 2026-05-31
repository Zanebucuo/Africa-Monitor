"""
Africa Commercial Vehicle Market Intelligence Platform
Enterprise BI Engine v7.0
— Intelligence Triangulation · Analyst Due Diligence · Critical Thinking Framework
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
    --dim:#9BA3B2; --border:#E2E5EB; --green:#1A8C5B; --amber:#B45309;
    --red:#B91C1C;
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

/* Section headers */
.section-hdr{
    display:flex; align-items:center; gap:10px;
    margin:26px 0 14px 0; padding-bottom:10px; border-bottom:1px solid var(--border);
}
.section-bar{ width:4px; height:20px; background:var(--orange); border-radius:2px; flex-shrink:0; }
.section-title{ font-size:.88rem; font-weight:700; letter-spacing:.4px; color:var(--txt); text-transform:uppercase; }
.section-sub{ font-size:.72rem; color:var(--dim); margin-left:4px; }

/* Chart card */
.chart-card{
    background:var(--white); border:1px solid var(--border);
    border-radius:var(--radius); padding:18px 18px 8px 18px;
    box-shadow:var(--shadow); margin-bottom:4px;
}
.chart-label{ font-size:.68rem; font-weight:700; text-transform:uppercase; letter-spacing:.7px; color:var(--dim); margin-bottom:2px; }
.chart-title{ font-size:.92rem; font-weight:700; color:var(--txt); margin-bottom:2px; }
.chart-sub  { font-size:.72rem; color:var(--dim); margin-bottom:10px; }
.source-link{ font-size:.68rem; color:var(--blue); margin-top:4px; }

/* ══ TRIANGULATION COMPONENT ══ */
.tri-outer{
    background:var(--white); border:1px solid var(--border);
    border-radius:var(--radius); overflow:hidden;
    box-shadow:var(--shadow); margin-top:12px; margin-bottom:20px;
}
.tri-header{
    background:var(--navy); padding:12px 20px;
    display:flex; align-items:center; gap:10px;
}
.tri-header-title{
    font-family:'Inter',sans-serif; font-size:.8rem; font-weight:700;
    color:#fff; letter-spacing:.6px; text-transform:uppercase;
}
.tri-header-badge{
    background:var(--orange); color:#fff; font-size:.6rem; font-weight:700;
    padding:2px 10px; border-radius:20px; letter-spacing:.5px; text-transform:uppercase;
}
.tri-body{ padding:0; }
.tri-layer{
    padding:14px 20px; border-bottom:1px solid var(--border);
}
.tri-layer:last-child{ border-bottom:none; }
.tri-layer-label{
    font-family:'Inter',sans-serif; font-size:.62rem; font-weight:700;
    text-transform:uppercase; letter-spacing:1.2px; margin-bottom:6px;
    display:flex; align-items:center; gap:8px;
}
.tri-claim-label { color:var(--blue); }
.tri-cross-label { color:var(--amber); }
.tri-verdict-label{ color:var(--green); }
.tri-layer-body{
    font-family:'Inter',sans-serif; font-size:.82rem; color:var(--txt);
    line-height:1.7; word-wrap:break-word; overflow-wrap:break-word; white-space:normal;
}
.tri-layer-body ul{ margin:6px 0 0 0; padding-left:16px; }
.tri-layer-body li{ margin-bottom:4px; }

/* Confidence badges */
.conf-verified{
    display:inline-flex; align-items:center; gap:5px;
    background:#ECFDF5; border:1px solid #6EE7B7; border-radius:4px;
    padding:2px 9px; font-size:.68rem; font-weight:700; color:var(--green);
    font-family:'Inter',sans-serif; white-space:nowrap;
}
.conf-plausible{
    display:inline-flex; align-items:center; gap:5px;
    background:#FFFBEB; border:1px solid #FCD34D; border-radius:4px;
    padding:2px 9px; font-size:.68rem; font-weight:700; color:var(--amber);
    font-family:'Inter',sans-serif; white-space:nowrap;
}
.conf-field{
    display:inline-flex; align-items:center; gap:5px;
    background:#FEF2F2; border:1px solid #FCA5A5; border-radius:4px;
    padding:2px 9px; font-size:.68rem; font-weight:700; color:var(--red);
    font-family:'Inter',sans-serif; white-space:nowrap;
}
.conf-row{
    display:flex; align-items:flex-start; gap:10px; flex-wrap:wrap;
    margin-top:8px; padding-top:8px; border-top:1px solid var(--border);
}
.conf-row-label{
    font-family:'Inter'; font-size:.68rem; font-weight:700;
    color:var(--mid); text-transform:uppercase; letter-spacing:.6px;
    flex-shrink:0; padding-top:3px;
}

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
.news-badge   { background:var(--orange); color:#fff; font-size:.58rem; font-weight:700; padding:2px 8px; border-radius:20px; }
.news-fb-badge{ background:#F0F3F8; color:var(--mid); font-size:.58rem; font-weight:700; padding:2px 8px; border-radius:20px; }
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
.news-src   { display:inline-block; background:#F0F3F8; color:var(--navy); font-size:.6rem; font-weight:600; padding:1px 7px; border-radius:4px; margin-right:5px; }
.news-fb-src{ display:inline-block; background:#FFF3ED; color:var(--orange); font-size:.6rem; font-weight:600; padding:1px 7px; border-radius:4px; margin-right:5px; }
.news-empty{ padding:28px 16px; text-align:center; color:var(--dim); font-size:.8rem; line-height:1.8; }
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
    margin=dict(l=52, r=20, t=24, b=52),
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
# 3. TRIANGULATION CONTENT DATABASE
#    Each entry: {claim, cross_validation (list), verdict, confidence_items}
#    confidence_items: list of {label, badge_type ("verified"|"plausible"|"field")}
# ══════════════════════════════════════════════════════════════════════════════
TRIANGULATION = {

    # ── Morocco: OCP Transport Modal ─────────────────────────────────────────
    "ma_ocp_modal": {
        "title":  "OCP Transport Modal & Road HCV Procurement Potential",
        "claim":  (
            "Industry commentators and several Chinese commercial vehicle exporters "
            "cite OCP Group as a flagship anchor client, estimating annual HCV fleet "
            "procurement at <strong>800–1,000 units/year</strong>, driven by the "
            "Khouribga–Jorf Lasfar phosphate corridor and downstream logistics."
        ),
        "cross_validation": [
            "<strong>[Fact]</strong> OCP Group operates a dedicated <strong>187 km slurry pipeline</strong> "
            "(Khouribga → Jorf Lasfar) that handles the bulk of raw phosphate ore "
            "transport — this segment is structurally inaccessible to road HCVs.",
            "<strong>[Fact]</strong> OCP also operates the <strong>Benguerir–Jorf Lasfar rail corridor</strong> "
            "for phosphate concentrate, confirmed in OCP's 2022 and 2023 Integrated Annual Reports.",
            "<strong>[Structural logic]</strong> However, pipeline and rail serve only the <em>primary ore trunk</em>. "
            "OCP's ecosystem of ~60 contractor companies performs auxiliary logistics: "
            "sulphuric acid deliveries, fertiliser finished goods, equipment mobilisation, "
            "and reagent supply — segments that are <em>structurally road-dependent</em>.",
            "<strong>[Counter-evidence]</strong> No publicly accessible OCP procurement tender database "
            "confirms a recurring 800-unit annual HCV purchase figure. "
            "OCP issues tenders via SupplierPortal (Ariba) with limited public disclosure.",
            "<strong>[Supportive proxy]</strong> OCP's 2023 capex of USD 2.1 billion includes "
            "significant mining fleet renewal — a portion of which flows to road HCVs "
            "based on analogous mining group capex structures in comparable operations.",
        ],
        "verdict": (
            "The slurry pipeline unambiguously dominates primary ore haulage — "
            "framing OCP purely as a 'truck buyer' overstates the road opportunity. "
            "However, the contractor ecosystem and finished-goods distribution network "
            "represent a <em>real and recurring</em> HCV demand segment. "
            "The 800 units/year figure is a bottom-up estimate derived from "
            "contractor fleet modelling, not a verified tender disclosure. "
            "Decision-makers should treat this as a working hypothesis and prioritise "
            "direct engagement with OCP's Procurement & Logistics division "
            "and tier-1 contractors (e.g., CBI, Snef, Cofely) for ground-truth validation."
        ),
        "confidence_items": [
            {"label": "Pipeline dominates primary ore trunk", "badge": "verified"},
            {"label": "Rail handles phosphate concentrate flows", "badge": "verified"},
            {"label": "Contractor ecosystem is road-dependent", "badge": "plausible"},
            {"label": "800 units/yr HCV procurement estimate", "badge": "plausible"},
            {"label": "Specific tender volumes & timing", "badge": "field"},
        ],
    },

    # ── Morocco: Tariff Advantage ─────────────────────────────────────────────
    "ma_tariff": {
        "title":  "Morocco 2.5% Tariff Advantage — Sustainable Competitive Moat?",
        "claim":  (
            "Morocco's EU Association Agreement confers a 2.5% CBU import tariff "
            "on commercial vehicles — cited as the lowest in Africa and a decisive "
            "competitive advantage for European-origin or EU-compliant vehicles."
        ),
        "cross_validation": [
            "<strong>[Fact]</strong> The EU–Morocco Association Agreement (in force since 2000) "
            "does set preferential tariff rates, including on motor vehicles, confirmed "
            "by Direction Générale des Douanes schedules.",
            "<strong>[Complication]</strong> The 2.5% rate applies to vehicles of EU <em>origin</em> "
            "(Rules of Origin apply). Chinese-built trucks — even if EU-spec — do not "
            "automatically qualify; they face standard MFN rates (~25%) unless locally assembled.",
            "<strong>[Strategic implication]</strong> This tariff structure structurally "
            "advantages Renault Trucks, Mercedes-Benz, Volvo, and MAN over Chinese brands "
            "entering via CBU. Chinese players must pursue CKD assembly partnerships "
            "or route through third countries with EU FTAs to access the preferential rate.",
            "<strong>[Risk]</strong> Post-Brexit UK–Morocco trade continuity agreement is "
            "periodically renegotiated — tariff schedules should be verified against "
            "the latest DOUANE.GOV.MA tariff tables before contract commitments.",
        ],
        "verdict": (
            "The 2.5% tariff is a confirmed and material advantage — but it is <em>origin-conditioned</em>, "
            "not a blanket benefit for all importers. Chinese CBU entrants face a de facto "
            "tariff disadvantage of ~22.5 percentage points versus EU-origin competitors. "
            "For Chinese CV manufacturers, the commercially rational entry strategy is "
            "local assembly (CKD) or a Morocco-based JV — not direct CBU import."
        ),
        "confidence_items": [
            {"label": "2.5% tariff for EU-origin vehicles confirmed", "badge": "verified"},
            {"label": "Chinese CBU faces ~25% MFN rate", "badge": "verified"},
            {"label": "CKD assembly as optimal China entry route", "badge": "plausible"},
            {"label": "Specific CKD partner availability & terms", "badge": "field"},
        ],
    },

    # ── South Africa: Transnet Rail Crisis ───────────────────────────────────
    "za_transnet": {
        "title":  "Transnet Rail Collapse → Road HCV Demand Transfer — Scissors Effect",
        "claim":  (
            "Multiple logistics industry analysts and HCV dealers assert that Transnet's "
            "operational deterioration has structurally transferred freight to road, "
            "creating a durable demand uplift of <strong>3,000–5,000 incremental HCV units/year</strong> "
            "that would not exist under a functioning rail network."
        ),
        "cross_validation": [
            "<strong>[Fact]</strong> Transnet Freight Rail volumes declined from <strong>228 Mt (FY2018)</strong> "
            "to an estimated <strong>122 Mt (FY2026)</strong> — a 46% collapse confirmed in "
            "Transnet's own annual reports and corroborated by Stats SA P7162.",
            "<strong>[Fact]</strong> Stats SA P7162 Road Freight Survey records a rising "
            "freight income trend concurrent with declining payload tonnage, consistent "
            "with road operators capturing higher-value diverted freight.",
            "<strong>[Fact]</strong> NAAMSA data shows HCV segment resilience outperforming "
            "overall automotive market during 2022–2024, coinciding with Transnet's "
            "most acute operational crisis.",
            "<strong>[Critical counter-risk]</strong> South Africa's National Logistics Crisis "
            "Response (NLCR) and the <strong>Transnet port privatisation programme</strong> "
            "(Durban Container Terminal concession, initiated 2023) could, if successful, "
            "restore rail competitiveness within 5–8 years — partially reversing "
            "the modal shift and reducing structural HCV demand.",
            "<strong>[Additional risk]</strong> Private rail operators (e.g., Grindrod, "
            "Traxtion) are entering the market under new open-access rail policy — "
            "a further rail recovery vector that is systematically underweighted "
            "in current HCV demand forecasts.",
        ],
        "verdict": (
            "The Transnet-driven freight modal shift is one of the most "
            "<em>empirically well-supported</em> demand drivers in African HCV markets — "
            "the volume collapse is confirmed by multiple independent data sources. "
            "However, the market consensus <em>systematically underweights</em> the "
            "rail recovery risk: port privatisation, open-access rail policy, and "
            "private operator entry are structural variables that could materially "
            "compress road HCV demand within a 5-year horizon. "
            "Buyers planning long-term fleet financing should stress-test models "
            "against a 30–40% rail volume recovery scenario."
        ),
        "confidence_items": [
            {"label": "Transnet volume collapse (228→122 Mt)", "badge": "verified"},
            {"label": "Road freight income growth (Stats SA P7162)", "badge": "verified"},
            {"label": "3,000–5,000 incremental HCV units from modal shift", "badge": "plausible"},
            {"label": "Rail recovery via port privatisation (5-yr horizon)", "badge": "plausible"},
            {"label": "Private rail operator market share trajectory", "badge": "field"},
        ],
    },

    # ── South Africa: EV / Load Shedding ─────────────────────────────────────
    "za_ev_loadshed": {
        "title":  "EV Fleet Adoption Under Load-Shedding Constraints",
        "claim":  (
            "South Africa's severe electricity supply instability (load-shedding Stage 2–6) "
            "is widely cited as a structural barrier that will delay commercial EV "
            "fleet adoption by 5–10 years relative to comparable markets."
        ),
        "cross_validation": [
            "<strong>[Fact]</strong> Eskom implemented load-shedding for <strong>335 days in 2023</strong> "
            "(a national record), with Stage 4–6 outages totalling >1,000 hours — "
            "confirmed by Eskom operational reports.",
            "<strong>[Fact]</strong> South Africa's National EV Strategy (SAIT, 2023) "
            "acknowledges grid reliability as a primary EV barrier and mandates "
            "dedicated charging infrastructure investment as a precondition.",
            "<strong>[Nuance]</strong> Large fleet operators (e.g., Shoprite, Transnet Road Motor "
            "Transport) are deploying <em>behind-the-meter solar + battery</em> systems "
            "that decouple depot charging from Eskom grid — partially negating "
            "the load-shedding constraint for captive fleet applications.",
            "<strong>[Counter-trend]</strong> Eskom's FY2025 operational data shows load-shedding "
            "days declining sharply as new generation capacity (Kusile Unit 5, "
            "private IPPs) comes online — the structural constraint may ease "
            "faster than industry consensus assumes.",
        ],
        "verdict": (
            "Load-shedding is a <em>real but potentially transient</em> constraint on EV adoption. "
            "The 5–10 year delay thesis is overstated for <em>captive depot fleets</em> "
            "with solar/battery backup — the genuine constraint applies to "
            "<em>over-the-road long-haul</em> applications dependent on public charging. "
            "EV strategy for South Africa should be segmented: depot-based distribution "
            "fleets (urban/peri-urban) are viable <em>now</em>; "
            "long-haul intercity EV remains a 2028+ proposition pending charging infrastructure."
        ),
        "confidence_items": [
            {"label": "Load-shedding severity (335 days, 2023)", "badge": "verified"},
            {"label": "Solar depot charging feasibility for fleets", "badge": "plausible"},
            {"label": "Grid recovery timeline (Kusile + IPPs)", "badge": "plausible"},
            {"label": "Long-haul public charging availability", "badge": "field"},
        ],
    },

    # ── Nigeria: KD Tariff Dividend ───────────────────────────────────────────
    "ng_kd_tariff": {
        "title":  "Nigeria Zero-Tariff KD Policy — Durable Incentive or Policy Risk?",
        "claim":  (
            "Nigeria's 2023 EV and CKD/SKD zero-tariff policy creates a compelling "
            "economic case for Chinese CV manufacturers to establish local assembly, "
            "delivering ~$46,000 per-unit cost advantage over CBU imports."
        ),
        "cross_validation": [
            "<strong>[Fact]</strong> Nigeria Customs Service confirmed 0% import duty on "
            "fully electric commercial vehicles and CKD/SKD assembly kits "
            "under the 2023 Finance Act amendments.",
            "<strong>[Fact]</strong> NADDC's National Automotive Industry Development Plan (NAIDP) "
            "explicitly targets local assembly partnerships as a core pillar.",
            "<strong>[Risk: Policy Stability]</strong> Nigeria has a documented history of "
            "retroactive tariff policy reversals — the 2013–2019 automotive tariff "
            "regime was modified three times in six years. "
            "The current 0% window has a stated 2023–2028 horizon but "
            "carries medium political risk given fiscal pressure on import duties.",
            "<strong>[Risk: FX]</strong> CKD assembly economics assume stable USD/NGN rates "
            "for imported kits. With NGN depreciation exceeding 60% since 2022, "
            "the USD cost of kits has effectively risen proportionally for "
            "naira-revenue businesses.",
            "<strong>[Operational risk]</strong> NADDC assembly licence approval has averaged "
            "18–24 months in practice — the regulatory friction offsets some financial advantage.",
        ],
        "verdict": (
            "The zero-tariff CKD advantage is <em>legally confirmed and financially material</em>. "
            "However, it operates within a high-volatility policy and FX environment "
            "that requires hedging strategies and contractual protections. "
            "Manufacturers should structure assembly JVs with "
            "USD-indexed kit pricing, multi-year FX forward contracts, "
            "and clause-based exit provisions triggered by policy reversal. "
            "The $46,000 per-unit saving is the <em>best-case scenario</em> — "
            "realistic net savings after FX and operational costs are closer to $28,000–$35,000."
        ),
        "confidence_items": [
            {"label": "0% CKD/EV tariff legally confirmed (2023 Finance Act)", "badge": "verified"},
            {"label": "~$46,000 gross per-unit CBU vs CKD saving", "badge": "plausible"},
            {"label": "Net saving after FX hedge: ~$28k–$35k", "badge": "plausible"},
            {"label": "NADDC assembly licence approval timeline", "badge": "field"},
            {"label": "Policy stability through 2028", "badge": "field"},
        ],
    },

    # ── Ethiopia: EV Mandate ──────────────────────────────────────────────────
    "eth_ev_mandate": {
        "title":  "Ethiopia Petroleum Import Ban — EV Transition Reality vs. Headline",
        "claim":  (
            "Ethiopia's 2022 petroleum vehicle import ban is heralded as "
            "the most decisive EV fleet mandate in Africa, projected to drive "
            "EV penetration to >90% of commercial vehicle sales by 2025."
        ),
        "cross_validation": [
            "<strong>[Fact]</strong> ERCA (Ethiopian Revenue & Customs Authority) formally "
            "suspended import permits for petroleum-powered vehicles in mid-2022 — "
            "this is confirmed policy, not a proposal.",
            "<strong>[Implementation gap]</strong> Enforcement has been uneven: "
            "legacy ICE vehicles already in-country continue to operate; "
            "grey market imports via Djibouti and South Sudan have been documented "
            "by Ethiopian trade monitoring bodies.",
            "<strong>[Infrastructure constraint]</strong> As of 2024, Ethiopia has "
            "<strong>fewer than 120 public EV charging points</strong> nationwide "
            "(EEPCO data), almost exclusively in Addis Ababa. "
            "Long-haul routes (Addis–Djibouti corridor, 850 km) have zero public chargers.",
            "<strong>[Fleet composition reality]</strong> The high EV share in sales data "
            "reflects <em>new registrations</em>, not operational fleet composition. "
            "The existing ICE fleet of ~80,000 commercial vehicles continues to operate "
            "and will do so for its economic life (10–15 years).",
            "<strong>[Chinese EV dominance]</strong> BYD, Foton, and King Long collectively "
            "hold >75% of new EV commercial vehicle registrations — a confirmed "
            "structural beneficiary dynamic.",
        ],
        "verdict": (
            "The ban is real and its impact on <em>new registration sales</em> is transformative. "
            "However, the '90% EV' narrative conflates new sales share with operational "
            "fleet electrification — the latter remains below 15% given fleet longevity. "
            "The Addis–Djibouti corridor, Ethiopia's most commercially critical freight artery, "
            "is structurally incompatible with current EV range and charging infrastructure. "
            "Chinese EV brands have a genuine first-mover advantage in urban/peri-urban fleets; "
            "long-haul electrification requires a 3–5 year charging infrastructure build-out "
            "before it is commercially viable."
        ),
        "confidence_items": [
            {"label": "Petroleum import ban officially enacted (2022)", "badge": "verified"},
            {"label": "Chinese brands hold >75% new EV registrations", "badge": "verified"},
            {"label": "EV new sales share >85% (2025 est.)", "badge": "plausible"},
            {"label": "Operational fleet electrification <15%", "badge": "plausible"},
            {"label": "Long-haul corridor (Addis–Djibouti) EV viability", "badge": "field"},
        ],
    },

    # ── Kenya: SGR Impact ─────────────────────────────────────────────────────
    "ke_sgr": {
        "title":  "Kenya SGR — Road Freight Competitor or Demand Complement?",
        "claim":  (
            "The Standard Gauge Railway (SGR) Mombasa–Nairobi line is frequently cited "
            "as a structural threat to HCV demand, projected to displace "
            "30–40% of long-haul container freight from road by 2026."
        ),
        "cross_validation": [
            "<strong>[Fact]</strong> SGR freight volumes grew from 1.2 Mt (2018) to "
            "5.8 Mt (2023) — confirmed by Kenya Railways Corporation annual data.",
            "<strong>[Fact]</strong> Port of Mombasa container throughput grew concurrently, "
            "meaning SGR captured incremental freight rather than purely substituting road.",
            "<strong>[Operational limit]</strong> SGR operates Mombasa–Nairobi only (472 km). "
            "The 'last mile' from Nairobi ICD to final destinations (Kampala, Kigali, "
            "Juba) remains structurally road-dependent — HCVs are complementary, "
            "not competitive, for inland distribution.",
            "<strong>[Financial distress]</strong> Kenya's SGR debt obligations to Exim Bank "
            "of China (~KES 500 billion) create fiscal pressure; "
            "extension to Kisumu and Uganda has stalled — limiting SGR's "
            "geographic competitive reach.",
        ],
        "verdict": (
            "SGR is a <em>complement to, not a substitute for</em>, HCV demand "
            "in the Kenyan freight system. The modal shift concern is overstated: "
            "SGR's geographic limitation to the Mombasa–Nairobi corridor means "
            "the vast majority of Kenyan freight — and virtually all EAC cross-border "
            "freight — remains road-dependent. "
            "HCV demand in Kenya is more sensitively correlated with "
            "EAC trade volumes and fuel subsidy policy than with SGR capacity."
        ),
        "confidence_items": [
            {"label": "SGR volumes: 5.8 Mt (2023, Kenya Railways)", "badge": "verified"},
            {"label": "Last-mile beyond Nairobi ICD remains road-only", "badge": "verified"},
            {"label": "SGR extension to Uganda stalled (debt constraints)", "badge": "plausible"},
            {"label": "Net HCV demand displacement from SGR", "badge": "field"},
        ],
    },

    # ── Egypt: KD Assembly ────────────────────────────────────────────────────
    "eg_kd": {
        "title":  "Egypt KD Assembly 5% Tariff — Realistic Entry Path?",
        "claim":  (
            "Egypt's KD assembly preferential tariff (5% vs 40% CBU) "
            "creates a compelling incentive for Chinese CV manufacturers "
            "to establish local assembly operations, analogous to the Nigerian model."
        ),
        "cross_validation": [
            "<strong>[Fact]</strong> The 5% KD preferential rate requires verified "
            "local content/value-added exceeding 40% — confirmed by Egyptian "
            "Industrial Development Authority (IDA) guidelines.",
            "<strong>[Implementation complexity]</strong> Achieving 40% local content "
            "for a commercial vehicle in Egypt requires sourcing engines, chassis "
            "components, or cab assemblies locally — Egypt's CV component supply "
            "chain is limited; most qualifying content is tyres, glass, and wiring.",
            "<strong>[Precedent]</strong> Ghabbour Auto (GB Auto) and MAN Trucks Egypt "
            "have navigated KD assembly successfully, establishing a replicable template.",
            "<strong>[FX risk]</strong> EGP devaluation (>50% since 2022) increases the "
            "USD cost of imported KD kits for local assemblers pricing in EGP — "
            "compressing margins in ways not captured in tariff-only analysis.",
        ],
        "verdict": (
            "The 5% KD tariff is a genuine and material incentive, but achieving "
            "the 40% local content threshold requires deliberate supply chain engineering "
            "— it is not automatically conferred on any assembler. "
            "The GB Auto/MAN precedent confirms viability; "
            "Chinese manufacturers should structure JVs with established "
            "Egyptian assembly partners rather than greenfield operations. "
            "FX hedging and EGP-indexed pricing are non-negotiable risk mitigants."
        ),
        "confidence_items": [
            {"label": "5% KD rate requires 40% local content (IDA confirmed)", "badge": "verified"},
            {"label": "GB Auto/MAN KD assembly as precedent", "badge": "verified"},
            {"label": "40% local content achievability for Chinese CVs", "badge": "plausible"},
            {"label": "Net margin after FX and supply chain costs", "badge": "field"},
        ],
    },

    # ── Algeria: Protectionism ────────────────────────────────────────────────
    "dz_protect": {
        "title":  "Algeria Import Protectionism — Navigable or Structural Barrier?",
        "claim":  (
            "Algeria's 30% CBU tariff and import licence quota system "
            "effectively make direct CV import commercially unviable, "
            "requiring mandatory local assembly JVs for market entry."
        ),
        "cross_validation": [
            "<strong>[Fact]</strong> Algeria's 2016 import licence system (suspended 2019, "
            "partially reinstated 2022) has created chronic supply uncertainty "
            "for importers — confirmed by multiple MENA trade monitoring reports.",
            "<strong>[Fact]</strong> Renault Trucks operates a proven JV assembly plant "
            "in Rouiba (Algiers) — demonstrating that local manufacturing partnerships "
            "are the only sustainable market entry model.",
            "<strong>[Political dynamic]</strong> Algeria's government explicitly prioritises "
            "local industrial development; JV partners who commit to "
            "workforce training and technology transfer receive preferential "
            "treatment in public procurement (Sonatrach, Ministry of Public Works).",
            "<strong>[Risk]</strong> Political and commercial relationship between Algeria "
            "and China is positive at state level, but "
            "ministerial-level approval of new JV licences is opaque and "
            "can take 24–36 months.",
        ],
        "verdict": (
            "Algeria is a <em>high-barrier but not closed</em> market. "
            "The Renault Rouiba precedent confirms that committed long-term JV "
            "manufacturing partnerships can succeed. "
            "For Chinese CV brands, the strategic entry path is a "
            "state-endorsed JV with a local industrialist and a credible "
            "technology transfer commitment. "
            "Timeframe from initial MOU to first unit production: "
            "realistically 3–4 years. Market size does not justify greenfield "
            "investment for volumes below 2,000 units/year."
        ),
        "confidence_items": [
            {"label": "30% CBU tariff + quota system confirmed", "badge": "verified"},
            {"label": "Renault Rouiba JV as viable entry template", "badge": "verified"},
            {"label": "3–4 year JV approval and setup timeline", "badge": "plausible"},
            {"label": "Ministerial JV approval timeline for Chinese brands", "badge": "field"},
        ],
    },

    # ── Tunisia: EU Alignment ─────────────────────────────────────────────────
    "tn_eu": {
        "title":  "Tunisia EU-Aligned Market — Gateway or Niche?",
        "claim":  (
            "Tunisia's EU Association Agreement and UN-ECE certification "
            "mutual recognition make it the easiest African market to enter "
            "for EU-compliant commercial vehicles, with minimal regulatory friction."
        ),
        "cross_validation": [
            "<strong>[Fact]</strong> INNORPI confirms UN-ECE mutual recognition — "
            "EU type-approved vehicles require no additional homologation in Tunisia.",
            "<strong>[Market size constraint]</strong> Total Tunisian CV market of ~8,000 units/year "
            "represents approximately 17% of Nigeria's market — the regulatory ease "
            "must be weighed against limited scale economics.",
            "<strong>[Chinese brand challenge]</strong> European brands (Renault, Mercedes, MAN, Volvo) "
            "hold >70% share through decades of network investment. "
            "Chinese brands entering without a local dealer/service network "
            "face a trust deficit that no tariff advantage compensates.",
            "<strong>[Gateway potential]</strong> Tunisia's geographic position and "
            "EU regulatory alignment could serve as a testbed for "
            "EU-spec Chinese CV variants before broader European or North African expansion.",
        ],
        "verdict": (
            "Tunisia is easiest to enter but hardest to scale. "
            "It should be approached as a <em>strategic beachhead</em> for "
            "EU-spec product validation and brand-building, not as a "
            "primary volume market. "
            "The gateway value — regulatory learning, reference customer development, "
            "EU certification precedent — may exceed the direct revenue opportunity "
            "for Chinese brands in a 3–5 year horizon."
        ),
        "confidence_items": [
            {"label": "UN-ECE mutual recognition confirmed (INNORPI)", "badge": "verified"},
            {"label": "European brands >70% market share", "badge": "verified"},
            {"label": "Tunisia as EU-spec validation gateway", "badge": "plausible"},
            {"label": "Chinese brand dealer network viability at 8,000 unit market", "badge": "field"},
        ],
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 4. TRIANGULATION RENDERER
# ══════════════════════════════════════════════════════════════════════════════
BADGE_HTML = {
    "verified": '<span class="conf-verified">🟢 Verified Fact</span>',
    "plausible":'<span class="conf-plausible">🟡 Plausible Estimate</span>',
    "field":    '<span class="conf-field">🔴 Needs Field Verification</span>',
}

def render_triangulation(tri_key: str):
    """Render the full Intelligence Triangulation component for a given key."""
    if tri_key not in TRIANGULATION:
        return
    t = TRIANGULATION[tri_key]

    st.markdown(f"""
    <div class="tri-outer">
      <div class="tri-header">
        <span class="tri-header-title">🔍 &nbsp;Analyst Due Diligence</span>
        <span class="tri-header-badge">Intelligence Triangulation</span>
      </div>
      <div class="tri-body">

        <!-- Layer 1: Market Claim -->
        <div class="tri-layer">
          <div class="tri-layer-label tri-claim-label">
            <span>①</span>&nbsp;Market Claim &nbsp;/&nbsp; 市场观点
          </div>
          <div class="tri-layer-body">{t['claim']}</div>
        </div>

        <!-- Layer 2: Cross-Validation -->
        <div class="tri-layer">
          <div class="tri-layer-label tri-cross-label">
            <span>②</span>&nbsp;Cross-Validation &nbsp;/&nbsp; 交叉验证
          </div>
          <div class="tri-layer-body">
            <ul>
              {''.join(f'<li>{item}</li>' for item in t['cross_validation'])}
            </ul>
          </div>
        </div>

        <!-- Layer 3: Analyst Verdict -->
        <div class="tri-layer">
          <div class="tri-layer-label tri-verdict-label">
            <span>③</span>&nbsp;Analyst Verdict &nbsp;/&nbsp; 最终研判
          </div>
          <div class="tri-layer-body">
            {t['verdict']}
            <div class="conf-row">
              <span class="conf-row-label">Confidence:</span>
              {''.join(
                f'<span style="display:inline-flex;align-items:center;gap:5px;margin-bottom:4px;">'
                f'{BADGE_HTML[ci["badge"]]}'
                f'<span style="font-family:Inter;font-size:.7rem;color:#5A6070;">{ci["label"]}</span>'
                f'</span> '
                for ci in t['confidence_items']
              )}
            </div>
          </div>
        </div>

      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 5. TIER-1 COUNTRY DATABASE
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
            "tariff":      "CBU EV: 0% (2023–2028). CKD/SKD: 0%. Conventional CBU: 35%.",
            "certification":"SON mandatory; NAFDAC for specialist vehicles; Form M import approval required.",
            "key_buyers":  "Dangote Cement, BUA Group (agri & chemicals), NNPC Logistics Division.",
            "risk":        "NGN/USD depreciation >60% over 18 months. Apapa port congestion: 3–6 week clearance delays.",
        },
        "news_query":"Nigeria commercial vehicle logistics truck",
        "tri_keys":["ng_kd_tariff"],
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
            "Import Tariff":   ("25%","CBU standard","KD assembly ~12%","https://itac.org.za"),
            "Diesel Price":    ("R21.60","/litre","≈ $1.18 USD","https://www.energy.gov.za"),
        },
        "brand_share":{"brands":["Mercedes-Benz","Volvo","MAN","Scania","FAW"],"sales":[7200,6100,5800,5200,3100]},
        "trend":{"years":[2021,2022,2023,2024,2025,2026],"ice":[29800,31200,32500,31800,30900,30900],"ev":[0,0,120,320,540,600]},
        "policy":{
            "tariff":      "25% CBU import duty. APDP incentive: >50% localisation receives production rebates.",
            "certification":"NRCS mandatory LoA; Euro 5-equivalent emissions; SABS type approval.",
            "key_buyers":  "Transnet, Imperial Logistics, Tiger Brands distribution, Shoprite supply chain.",
            "risk":        "Load-shedding (Stage 2–4) disrupts EV charging infrastructure. ZAR/USD ~18.5.",
        },
        "news_query":"South Africa commercial truck logistics freight",
        "tri_keys":["za_transnet","za_ev_loadshed"],
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
            "EV Import Tariff": ("2.5%","EU-origin vehicles","Standard MFN ~25%","https://www.douane.gov.ma"),
            "Diesel Price":     ("MAD 13.50","/litre","≈ $1.34 USD","https://www.onhym.com"),
        },
        "brand_share":{"brands":["Renault Trucks","Mercedes-Benz","Volvo","Sinotruk","MAN"],"sales":[4200,3600,3100,2800,2100]},
        "trend":{"years":[2021,2022,2023,2024,2025,2026],"ice":[14200,15100,16200,17400,18000,18000],"ev":[0,40,120,260,380,400]},
        "policy":{
            "tariff":      "EU AA Agreement: EU-origin CBU 2.5%. Chinese CBU: ~25% MFN. No dedicated KD incentive.",
            "certification":"CNEAT: UN-ECE mutual recognition. EU type-approved vehicles: fast-track.",
            "key_buyers":  "OCP Group (phosphate mining), ONCF (national rail logistics), Casablanca Port operators.",
            "risk":        "Origin rules limit 2.5% benefit to EU-origin vehicles. Chinese CBU at structural tariff disadvantage.",
        },
        "news_query":"Morocco transport logistics trucks OCP freight",
        "tri_keys":["ma_ocp_modal","ma_tariff"],
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
            "tariff":      "CBU: 40%. KD (>40% local content): 5%. SCZone production: 0%.",
            "certification":"EOS mandatory; GOEIC import licence; SCZone simplified clearance.",
            "key_buyers":  "EGPC logistics, SCZone construction contractors, building materials distributors.",
            "risk":        "EGP depreciated >50% in 2 years; FX controls delay payments 45–90 days.",
        },
        "news_query":"Egypt commercial vehicle logistics freight Suez",
        "tri_keys":["eg_kd"],
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
            "Import Duty":     ("25%","EAC CET","COMESA: 0%","https://kra.go.ke"),
            "Diesel Price":    ("KES 188","/litre","≈ $1.42 USD","https://www.epra.go.ke"),
        },
        "brand_share":{"brands":["Isuzu","Toyota","Foton","Sinotruk","Volvo"],"sales":[3800,2900,2400,2100,1200]},
        "trend":{"years":[2021,2022,2023,2024,2025,2026],"ice":[10800,11500,12200,13100,13800,13900],"ev":[0,20,80,210,340,370]},
        "policy":{
            "tariff":      "EAC CET: 25%. COMESA: 0%. EV: currently 25% (policy review underway).",
            "certification":"KEBS mandatory PVoC at origin; NTSA inspection on arrival.",
            "key_buyers":  "Kenya Ports Authority, East African Breweries, Bamburi Cement, SGR feeder.",
            "risk":        "KES depreciation ~20% (2023–24); SGR competition on Mombasa–Nairobi corridor.",
        },
        "news_query":"Kenya commercial vehicle logistics freight Mombasa Nairobi",
        "tri_keys":["ke_sgr"],
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
            "EV Import Duty":    ("0%","Petroleum ban (2022)","ICE imports banned","https://www.erca.gov.et"),
            "Electricity Price": ("ETB 1.42","/kWh","≈ $0.025 USD","https://www.eepco.gov.et"),
        },
        "brand_share":{"brands":["BYD","Foton EV","King Long EV","Sinotruk","Skywell"],"sales":[2800,2100,1600,1200,800]},
        "trend":{"years":[2021,2022,2023,2024,2025,2026],"ice":[7200,6800,5400,3200,1800,1200],"ev":[200,800,2800,5800,7400,8200]},
        "policy":{
            "tariff":      "Petroleum-powered vehicle imports BANNED (2022). EV: 0% duty.",
            "certification":"EthSA; EV charging under national grid expansion programme.",
            "key_buyers":  "Ethiopian Roads Authority, Ethiopian Airlines cargo, Ethio Telecom fleet.",
            "risk":        "<120 public chargers nationwide; Addis–Djibouti corridor has zero public chargers.",
        },
        "news_query":"Ethiopia EV commercial vehicle petroleum ban transport",
        "tri_keys":["eth_ev_mandate"],
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
            "Import Tariff":   ("30%","CBU standard","CKD JV available","https://www.douane.gov.dz"),
            "Diesel Price":    ("DZD 45","/litre (subsidised)","≈ $0.33 USD","https://www.energy.gov.dz"),
        },
        "brand_share":{"brands":["Mercedes-Benz","Renault Trucks","MAN","Sinotruk","Volvo"],"sales":[3200,2800,2400,2000,1400]},
        "trend":{"years":[2021,2022,2023,2024,2025,2026],"ice":[10200,10800,11400,12000,12400,12400],"ev":[0,0,20,40,60,60]},
        "policy":{
            "tariff":      "30% CBU. CKD JV partnerships permitted; Renault Rouiba JV as template.",
            "certification":"IANOR; Euro 3 minimum (Euro 4 upgrade underway).",
            "key_buyers":  "Sonatrach (oil & gas), SNVI, Ministry of Public Works.",
            "risk":        "Import quotas; FX controls; JV licence approval 24–36 months.",
        },
        "news_query":"Algeria commercial vehicle transport logistics Sonatrach",
        "tri_keys":["dz_protect"],
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
            "tariff":      "EU Association Agreement: ~10% tariff. UN-ECE mutual recognition.",
            "certification":"INNORPI; ATTT road transport authority approval.",
            "key_buyers":  "CPG (phosphates), Port of Tunis operators, food & textile logistics.",
            "risk":        "Small total market (~8,000 units); European brands >70% share.",
        },
        "news_query":"Tunisie transport logistique camions freight",
        "tri_keys":["tn_eu"],
        "sources":{
            "trade":  ("INNORPI — Institut National de la Normalisation","https://www.innorpi.tn"),
            "customs":("Direction Générale des Douanes — Tunisie","https://www.douane.gov.tn"),
            "market": ("ATTT — Agence Technique des Transports Terrestres","https://www.attt.tn"),
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 6. FULL 54-NATION MAP DATA
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
# 7. NEWS FETCHER — Wide Net, Smart Filter
# ══════════════════════════════════════════════════════════════════════════════
AUTHORITY_DOMAINS = [
    "reuters","bloomberg","ft.com","engineeringnews","businessday",
    "zawya","theafricareport","africanews","afdb","apanews",
    "businesstimes","naamsa","naddc","statssa","moti.gov",
]
NOISE_WORDS = {"rumor","rumour","unconfirmed","alleged","shocking","viral","leaked","clickbait"}

@st.cache_data(ttl=1800)
def fetch_news(query: str, limit: int = 7) -> dict:
    cutoff = datetime.utcnow() - timedelta(days=30)

    def _parse(url):
        try:
            feed = feedparser.parse(url)
            out = []
            for e in feed.entries:
                t = e.get("title","")
                if not t or any(n in t.lower() for n in NOISE_WORDS):
                    continue
                pub_str, pub_dt = "–", None
                if hasattr(e,"published_parsed") and e.published_parsed:
                    pub_dt = datetime(*e.published_parsed[:6])
                    pub_str = pub_dt.strftime("%Y-%m-%d")
                out.append({"title":t,"link":e.get("link","#"),
                             "published":pub_str,"pub_dt":pub_dt,
                             "source":e.get("source",{}).get("title","–")})
            out.sort(key=lambda x: x["pub_dt"] or datetime.min, reverse=True)
            return out
        except Exception:
            return []

    def _auth(item):
        return any(d in (item["link"]+item["source"]).lower() for d in AUTHORITY_DOMAINS)

    def _recent(item):
        return item["pub_dt"] is None or item["pub_dt"] >= cutoff

    enc = (query+" when:30d").replace(" ","+").replace('"',"%22")
    raw = _parse(f"https://news.google.com/rss/search?q={enc}&hl=en-US&gl=US&ceid=US:en")
    recent = [x for x in raw if _recent(x)]
    auth   = [x for x in recent if _auth(x)]

    if len(auth) >= 3:
        return {"items":auth[:limit],"is_authority":True,"is_fallback":False}
    if len(recent) >= 3:
        return {"items":recent[:limit],"is_authority":False,"is_fallback":False}

    enc2 = query.replace(" ","+").replace('"',"%22")
    raw2 = _parse(f"https://news.google.com/rss/search?q={enc2}&hl=en-US&gl=US&ceid=US:en")
    return {"items":raw2[:3],"is_authority":False,"is_fallback":True} if raw2 else \
           {"items":[],"is_authority":False,"is_fallback":True}

def _is_auth(item):
    return any(d in (item["link"]+item["source"]).lower() for d in AUTHORITY_DOMAINS)

def render_news_panel(query: str, country: str):
    with st.spinner(f"Fetching intelligence for {country}..."):
        result = fetch_news(query)
    items, is_auth, is_fb = result["items"], result["is_authority"], result["is_fallback"]
    badge = ('<span class="news-badge">AUTHORITY · 30D</span>' if is_auth else
             '<span class="news-fb-badge">GENERAL · 30D</span>' if not is_fb else
             '<span class="news-fb-badge">FALLBACK · 90D</span>')
    st.markdown('<div class="news-wrap">', unsafe_allow_html=True)
    st.markdown(f'<div class="news-hdr"><span class="news-hdr-title">📡 &nbsp;{country} — Market Intelligence</span>{badge}</div>',
                unsafe_allow_html=True)
    if not items:
        st.markdown('<div class="news-empty">📭 No results found. Try refreshing.</div>', unsafe_allow_html=True)
    else:
        if is_fb:
            st.markdown('<div style="padding:8px 16px;background:#FFF8F5;border-bottom:1px solid #F0C4AC;font-family:Inter;font-size:.72rem;color:#D04A02;">⚠ Showing best available coverage (90-day fallback).</div>', unsafe_allow_html=True)
        for item in items:
            sc = "news-src" if _is_auth(item) else "news-fb-src"
            st.markdown(f'<div class="news-item"><a class="news-title-a" href="{item["link"]}" target="_blank">{item["title"]}</a><div class="news-meta"><span class="{sc}">{item["source"]}</span>{item["published"]}</div></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 8. SIMULATED DATA GENERATORS
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def gen_brand_df(country):
    cd = TIER1[country]["brand_share"]
    total = sum(cd["sales"])
    return pd.DataFrame({"Brand":cd["brands"],"Units":cd["sales"],
                          "Share_pct":[round(s/total*100,1) for s in cd["sales"]]})

@st.cache_data
def gen_trend_df(country):
    t = TIER1[country]["trend"]
    df = pd.DataFrame({"Year":t["years"],"ICE":t["ice"],"EV":t["ev"]})
    df["Total"] = df["ICE"]+df["EV"]
    df["EV_Share"] = (df["EV"]/df["Total"]*100).round(2)
    return df

@st.cache_data
def gen_za_freight_category():
    return pd.DataFrame({
        "Category":["Mining & Quarrying","Manufactured Food & Beverages",
                    "Agriculture & Forestry","Retail & Wholesale Trade",
                    "Parcels & Express Logistics","Construction Materials",
                    "Petroleum Products","Other"],
        "Revenue_ZAR_bn":[48.2,21.6,14.8,13.2,11.4,9.6,8.8,7.4],
        "Pct":[35.4,15.9,10.9,9.7,8.4,7.1,6.5,5.4],
        "Color":["#D04A02","#21325B","#295BA5","#4C7FA8","#EB6C2D","#8BA7C4","#C0C8D8","#E2E5EB"],
    })

@st.cache_data
def gen_za_payload_income():
    np.random.seed(10)
    q = pd.date_range("2020-01-01","2026-04-01",freq="QS"); n=len(q)
    return pd.DataFrame({"Quarter":q,
                          "Payload_Mt":(np.linspace(2420,1890,n)+np.random.normal(0,30,n)).round(1),
                          "Income_ZAR_bn":(np.linspace(58.4,96.8,n)+np.random.normal(0,1.2,n)).round(2)})

@st.cache_data
def gen_za_channel():
    return pd.DataFrame({"Channel":["Dealer Retail","Corporate Fleets","Government","Rental & Leasing"],
                          "Share_pct":[79.5,10.8,5.2,4.5],
                          "Color":["#D04A02","#21325B","#295BA5","#8BA7C4"]})

@st.cache_data
def gen_za_province():
    return pd.DataFrame({
        "Province":["Gauteng","KwaZulu-Natal","Western Cape","Eastern Cape",
                    "Limpopo","Mpumalanga","North West","Free State","Northern Cape"],
        "Units":[14200,5800,4600,2400,1600,1200,800,600,300],
        "Share_pct":[45.1,18.4,14.6,7.6,5.1,3.8,2.5,1.9,1.0],
    })

@st.cache_data
def gen_za_rail_road():
    return pd.DataFrame({
        "Year":[2018,2019,2020,2021,2022,2023,2024,2025,2026],
        "Rail_Mt":[228,218,204,189,171,158,142,131,122],
        "HCV_Units":[27500,28200,29800,30400,31200,32500,31800,30900,30900],
    })

@st.cache_data
def gen_ng_waterfall():
    return pd.DataFrame({
        "Label":["CBU Base Price","CBU Import Duty\n(35%)","CBU Port &\nClearance",
                 "CBU Total Landed","CKD Base Price","CKD Import Duty\n(0% — EV Policy)",
                 "CKD Assembly Cost","CKD Total Landed"],
        "Value":[100000,35000,8000,143000,85000,0,12000,97000],
        "Measure":["absolute","relative","relative","total","absolute","relative","relative","total"],
    })

@st.cache_data
def gen_ma_modal():
    """Morocco OCP transport modal split — pipeline vs rail vs road (estimated)."""
    return pd.DataFrame({
        "Modal":["Slurry Pipeline\n(Raw Ore)","Rail\n(Concentrate)","Road HCV\n(Contractor / Finished Goods)"],
        "Volume_Mt_yr":[38.0,12.0,6.5],
        "Road_Accessible":[False,False,True],
        "Color":["#9BA3B2","#4C7FA8","#D04A02"],
        "Note":["Pipeline: 187 km Khouribga–Jorf Lasfar (not road-accessible)",
                "Rail: Benguerir–Jorf Lasfar concentrate (not road-accessible)",
                "Road: Contractor logistics, finished fertiliser, reagent supply"],
    })

@st.cache_data
def gen_ocp_throughput():
    np.random.seed(3)
    months = pd.date_range("2023-01-01","2026-05-01",freq="MS"); n=len(months)
    trend=np.linspace(820,1380,n); seasonal=90*np.sin(np.linspace(0,6.5*np.pi,n))
    return pd.DataFrame({"Month":months,"Throughput_kt":(trend+seasonal+np.random.normal(0,35,n)).clip(500).round(1)})

@st.cache_data
def gen_eth_ev():
    np.random.seed(4)
    months=pd.date_range("2021-01-01","2026-05-01",freq="MS"); n=len(months); ban=18
    ev=np.concatenate([np.linspace(0.5,3.0,ban),np.linspace(3.0,92.0,n-ban)+np.random.normal(0,2,n-ban)]).clip(0,100)
    return pd.DataFrame({"Month":months,"EV_Share_pct":ev.round(1)})

# ══════════════════════════════════════════════════════════════════════════════
# 9. CHART BUILDERS
# ══════════════════════════════════════════════════════════════════════════════
def _apply(fig, ov=None):
    layout = dict(**CHART_BASE)
    if ov: layout.update(ov)
    fig.update_layout(**layout)
    return fig

def chart_brand(df, country):
    colors=[PwC_COLORS[i] if i<3 else "#C0C8D8" for i in range(len(df))]
    fig=go.Figure(go.Bar(x=df["Brand"],y=df["Units"],
        text=[f"{p}%" for p in df["Share_pct"]],textposition="outside",
        textfont=dict(size=11,color="#2D3142",family="Inter"),
        marker=dict(color=colors,line=dict(color="white",width=1.5)),
        hovertemplate="<b>%{x}</b><br>%{y:,} units · %{text}<extra></extra>"))
    return _apply(fig,{"yaxis":{**CHART_BASE["yaxis"],"title":"Units","range":[0,df["Units"].max()*1.22]},
                        "xaxis":{**CHART_BASE["xaxis"],"title":"Brand"},"showlegend":False,"bargap":.38})

def chart_trend(df):
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=df["Year"],y=df["ICE"],name="ICE (Conventional)",mode="lines+markers",
        line=dict(color="#21325B",width=2.5),marker=dict(size=6,color="#21325B"),
        fill="tozeroy",fillcolor="rgba(33,50,91,0.08)",
        hovertemplate="<b>%{x}</b><br>ICE: <b>%{y:,}</b><extra></extra>"))
    fig.add_trace(go.Scatter(x=df["Year"],y=df["EV"],name="EV / New Energy",mode="lines+markers",
        line=dict(color="#D04A02",width=2.5),marker=dict(size=7,color="#D04A02",symbol="diamond"),
        fill="tozeroy",fillcolor="rgba(208,74,2,0.10)",
        hovertemplate="<b>%{x}</b><br>EV: <b>%{y:,}</b><extra></extra>"))
    fig.add_vline(x=2025.5,line_dash="dash",line_color="#9BA3B2",line_width=1)
    fig.add_annotation(x=2025.7,y=df["ICE"].max()*.9,text="← Actual | Forecast →",
        showarrow=False,font=dict(size=9,color="#9BA3B2",family="Inter"))
    return _apply(fig,{"xaxis":{**CHART_BASE["xaxis"],"title":"Year","tickmode":"array","tickvals":df["Year"].tolist()},
                        "yaxis":{**CHART_BASE["yaxis"],"title":"Units"}})

def chart_za_freight_cat(df):
    ds=df.sort_values("Revenue_ZAR_bn")
    fig=go.Figure(go.Bar(x=ds["Revenue_ZAR_bn"],y=ds["Category"],orientation="h",
        text=[f"R{v:.1f}bn ({p:.1f}%)" for v,p in zip(ds["Revenue_ZAR_bn"],ds["Pct"])],
        textposition="outside",textfont=dict(size=10,family="Inter",color="#2D3142"),
        marker=dict(color=ds["Color"],line=dict(color="white",width=1)),
        hovertemplate="<b>%{y}</b><br>R%{x:.1f}bn<extra></extra>"))
    return _apply(fig,{"xaxis":{**CHART_BASE["xaxis"],"title":"Freight Revenue (ZAR bn)",
                                 "range":[0,df["Revenue_ZAR_bn"].max()*1.3]},
                        "yaxis":{**CHART_BASE["yaxis"],"title":"","automargin":True},
                        "showlegend":False,"margin":dict(l=170,r=20,t=20,b=50),"height":340})

def chart_za_payload_income(df):
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=df["Quarter"],y=df["Payload_Mt"],name="Payload (Mt) ←",
        mode="lines+markers",yaxis="y1",line=dict(color="#D04A02",width=2.5),marker=dict(size=4,color="#D04A02"),
        fill="tozeroy",fillcolor="rgba(208,74,2,0.07)",
        hovertemplate="<b>%{x|Q%q %Y}</b><br>%{y:.0f} Mt<extra></extra>"))
    fig.add_trace(go.Scatter(x=df["Quarter"],y=df["Income_ZAR_bn"],name="Freight Income (Rbn) →",
        mode="lines+markers",yaxis="y2",line=dict(color="#21325B",width=2.5),marker=dict(size=4,color="#21325B"),
        hovertemplate="<b>%{x|Q%q %Y}</b><br>R%{y:.1f}bn<extra></extra>"))
    fig.add_annotation(x=df["Quarter"].iloc[-4],y=df["Payload_Mt"].iloc[-4],
        text="▼ Volume falling<br>▲ Revenue rising<br>= Cost squeeze",showarrow=True,
        arrowhead=2,arrowcolor="#D04A02",bgcolor="rgba(208,74,2,0.08)",bordercolor="#D04A02",
        font=dict(size=9,color="#D04A02",family="Inter"),ax=-80,ay=-50)
    return _apply(fig,{"yaxis":{**CHART_BASE["yaxis"],"title":"Payload (Mt)","side":"left"},
                        "yaxis2":{**CHART_BASE["yaxis"],"title":"Income (R bn)","side":"right","overlaying":"y","showgrid":False},
                        "xaxis":{**CHART_BASE["xaxis"],"title":"Quarter"}})

def chart_za_channel(df):
    fig=go.Figure(go.Pie(labels=df["Channel"],values=df["Share_pct"],hole=.58,
        marker=dict(colors=df["Color"].tolist(),line=dict(color="white",width=2)),
        textinfo="label+percent",textfont=dict(size=11,family="Inter"),
        hovertemplate="<b>%{label}</b><br>%{value:.1f}%<extra></extra>"))
    fig.add_annotation(text="Sales<br>Channel",x=.5,y=.5,font=dict(size=12,family="Inter",color="#5A6070"),showarrow=False)
    return _apply(fig,{"showlegend":True,"legend":dict(orientation="v",x=1.02,y=.5,font=dict(size=11),bgcolor="rgba(0,0,0,0)"),
                        "margin":dict(l=20,r=120,t=20,b=20),"height":300})

def chart_za_province(df):
    colors=["#D04A02" if i==0 else "#21325B" if i==1 else "#295BA5" if i==2 else "#8BA7C4" for i in range(len(df))]
    fig=go.Figure(go.Bar(x=df["Province"],y=df["Units"],
        text=[f"{v:,}\n({s}%)" for v,s in zip(df["Units"],df["Share_pct"])],
        textposition="outside",textfont=dict(size=10,family="Inter"),
        marker=dict(color=colors,line=dict(color="white",width=1.5)),
        hovertemplate="<b>%{x}</b><br>%{y:,} units<extra></extra>"))
    return _apply(fig,{"yaxis":{**CHART_BASE["yaxis"],"title":"Units","range":[0,df["Units"].max()*1.25]},
                        "xaxis":{**CHART_BASE["xaxis"],"title":"Province"},"showlegend":False,"bargap":.35,"height":320})

def chart_za_scissors():
    df=gen_za_rail_road()
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=df["Year"],y=df["Rail_Mt"],name="Transnet Rail (Mt) ←",
        mode="lines+markers",yaxis="y1",line=dict(color="#D04A02",width=2.5),marker=dict(size=6,color="#D04A02"),
        fill="tozeroy",fillcolor="rgba(208,74,2,0.07)",
        hovertemplate="<b>%{x}</b><br>Rail: %{y:.0f} Mt<extra></extra>"))
    fig.add_trace(go.Scatter(x=df["Year"],y=df["HCV_Units"],name="HCV Road Sales (units) →",
        mode="lines+markers",yaxis="y2",line=dict(color="#21325B",width=2.5),marker=dict(size=6,color="#21325B"),
        hovertemplate="<b>%{x}</b><br>HCV: %{y:,} units<extra></extra>"))
    fig.add_annotation(x=2018,y=228,text="Rail peak 2018:<br>228 Mt",showarrow=True,arrowhead=2,
        arrowcolor="#D04A02",font=dict(size=9,color="#D04A02",family="Inter"),ax=60,ay=-35)
    return _apply(fig,{"yaxis":{**CHART_BASE["yaxis"],"title":"Rail Volume (Mt)","side":"left"},
                        "yaxis2":{**CHART_BASE["yaxis"],"title":"HCV Sales (units)","side":"right","overlaying":"y","showgrid":False},
                        "xaxis":{**CHART_BASE["xaxis"],"title":"Year","tickmode":"array","tickvals":df["Year"].tolist()}})

def chart_ng_waterfall(df):
    fig=go.Figure(go.Waterfall(orientation="v",measure=df["Measure"].tolist(),
        x=df["Label"].tolist(),y=df["Value"].tolist(),
        text=["FREE" if v==0 else f"${v:,.0f}" for v in df["Value"]],
        textposition="outside",textfont=dict(size=10,family="Inter",color="#2D3142"),
        connector=dict(line=dict(color="#E2E5EB",width=1)),
        increasing=dict(marker_color="#D04A02"),decreasing=dict(marker_color="#1A8C5B"),
        totals=dict(marker_color="#21325B"),
        hovertemplate="<b>%{x}</b><br>$%{y:,.0f}<extra></extra>"))
    fig.add_annotation(x=7,y=97000,text="💡 CKD saves ~$46k/unit\nvs CBU",
        showarrow=True,arrowhead=2,arrowcolor="#1A8C5B",bgcolor="rgba(26,140,91,0.1)",
        bordercolor="#1A8C5B",font=dict(size=10,color="#1A8C5B",family="Inter"),ax=-90,ay=-50)
    return _apply(fig,{"yaxis":{**CHART_BASE["yaxis"],"title":"Cost (USD)"},
                        "xaxis":{**CHART_BASE["xaxis"],"title":""},"showlegend":False,
                        "margin":dict(l=60,r=20,t=30,b=70)})

def chart_ma_modal(df):
    """OCP Transport Modal Split — horizontal bar with road-accessible highlight."""
    colors = ["#C0C8D8" if not r else "#D04A02" for r in df["Road_Accessible"]]
    fig = go.Figure(go.Bar(
        x=df["Volume_Mt_yr"], y=df["Modal"], orientation="h",
        text=[f"{v:.1f} Mt/yr" for v in df["Volume_Mt_yr"]],
        textposition="outside",textfont=dict(size=11,family="Inter",color="#2D3142"),
        marker=dict(color=colors,line=dict(color="white",width=2)),
        customdata=df["Note"],
        hovertemplate="<b>%{y}</b><br>Volume: %{x:.1f} Mt/yr<br>%{customdata}<extra></extra>",
    ))
    fig.add_annotation(x=6.5,y="Road HCV\n(Contractor / Finished Goods)",
        text="● Road-accessible segment",showarrow=False,xanchor="left",xshift=8,
        font=dict(size=10,color="#D04A02",family="Inter"))
    return _apply(fig,{
        "xaxis":{**CHART_BASE["xaxis"],"title":"Estimated Annual Volume (Mt/year)",
                 "range":[0,df["Volume_Mt_yr"].max()*1.35]},
        "yaxis":{**CHART_BASE["yaxis"],"title":"","automargin":True},
        "showlegend":False,"margin":dict(l=200,r=20,t=20,b=50),"height":280,
    })

def chart_ocp_throughput(df):
    x_num=np.arange(len(df)); trend=np.poly1d(np.polyfit(x_num,df["Throughput_kt"],1))(x_num)
    growth=(df["Throughput_kt"].iloc[-1]/df["Throughput_kt"].iloc[0]-1)*100
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=df["Month"],y=df["Throughput_kt"],name="Monthly Throughput (kt)",
        mode="lines",line=dict(color="#D04A02",width=2),fill="tozeroy",fillcolor="rgba(208,74,2,0.10)",
        hovertemplate="<b>%{x|%b %Y}</b><br>%{y:.0f} kt<extra></extra>"))
    fig.add_trace(go.Scatter(x=df["Month"],y=trend,name="Growth Trend",mode="lines",
        line=dict(color="#21325B",width=1.5,dash="dot"),hovertemplate="Trend: %{y:.0f} kt<extra></extra>"))
    fig.add_annotation(x=df["Month"].iloc[-1],y=df["Throughput_kt"].iloc[-1],
        text=f"▲ +{growth:.1f}% since Jan 2023",showarrow=True,arrowhead=2,
        arrowcolor="#D04A02",font=dict(size=10,color="#D04A02",family="Inter"),ax=-110,ay=-40)
    return _apply(fig,{"xaxis":{**CHART_BASE["xaxis"],"title":"Month"},
                        "yaxis":{**CHART_BASE["yaxis"],"title":"Throughput (thousand tonnes)"}})

def chart_eth_ev(df):
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=df["Month"],y=df["EV_Share_pct"],name="EV Market Share (%)",
        mode="lines",line=dict(color="#D04A02",width=2.5),fill="tozeroy",fillcolor="rgba(208,74,2,0.12)",
        hovertemplate="<b>%{x|%b %Y}</b><br>%{y:.1f}%<extra></extra>"))
    fig.add_vline(x=pd.Timestamp("2022-07-01"),line_dash="dash",line_color="#21325B",line_width=1.5)
    fig.add_annotation(x=pd.Timestamp("2022-07-01"),y=50,text="⚡ Petroleum ban\nenacted Jul 2022",
        showarrow=False,xanchor="left",xshift=8,bgcolor="rgba(33,50,91,0.08)",bordercolor="#21325B",
        font=dict(size=9,color="#21325B",family="Inter"))
    return _apply(fig,{"xaxis":{**CHART_BASE["xaxis"],"title":"Month"},
                        "yaxis":{**CHART_BASE["yaxis"],"title":"EV Market Share (%)","range":[0,105]},"showlegend":False})

# ══════════════════════════════════════════════════════════════════════════════
# 10. HELPER UI FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════
def _chdr(label,title,sub,src_name,src_url):
    st.markdown(f"""
    <div class="chart-card">
        <div class="chart-label">{label}</div>
        <div class="chart-title">{title}</div>
        <div class="chart-sub">{sub}</div>
        <div class="source-link">📌 <a href="{src_url}" target="_blank">{src_name}</a></div>
    </div>
    """, unsafe_allow_html=True)

def _sdiv(title,sub=""):
    st.markdown(f"""
    <div class="section-hdr" style="margin-top:26px;">
        <div class="section-bar"></div>
        <div class="section-title">{title}</div>
        {"<div class='section-sub'>"+sub+"</div>" if sub else ""}
    </div>
    """, unsafe_allow_html=True)

def _kpi_row(cdata):
    cols = st.columns(len(cdata["kpi"]))
    for col,(key,(val,lbl,delta,_)) in zip(cols,cdata["kpi"].items()):
        with col:
            dc="normal" if "+" in delta else "inverse" if "-" in delta else "off"
            st.metric(key,val,delta,delta_color=dc,help=lbl)
    src = list(cdata["sources"].values())[0]
    st.caption(f"Source: [{src[0]}]({src[1]}) · Simulated data for illustrative purposes.")
    st.markdown("<br>",unsafe_allow_html=True)

def _standard_2col(country,cdata,key_prefix):
    c1,c2=st.columns(2,gap="large")
    src=cdata["sources"]["trade"]
    with c1:
        _chdr("Market Share",f"Brand Rankings — {country}","Top 5 brands by annual HCV unit sales",src[0],src[1])
        st.plotly_chart(chart_brand(gen_brand_df(country),country),use_container_width=True,
                        config={"displayModeBar":False},key=f"{key_prefix}_brand")
    with c2:
        _chdr("Sales Trend 2021–2026",f"ICE vs. EV — {country}","Historical actuals + 2026 forecast",src[0],src[1])
        st.plotly_chart(chart_trend(gen_trend_df(country)),use_container_width=True,
                        config={"displayModeBar":False},key=f"{key_prefix}_trend")

# ══════════════════════════════════════════════════════════════════════════════
# 11. COUNTRY MARKET TAB RENDERERS
# ══════════════════════════════════════════════════════════════════════════════

def render_south_africa(cdata):
    STATSSA = "https://www.statssa.gov.za/publications/P7162/P7162.html"
    NAAMSA  = "https://naamsa.co.za"
    TRANSNET= "https://www.transnet.net/InvestorCentre/Pages/AnnualReports.aspx"
    _kpi_row(cdata)
    _standard_2col("South Africa",cdata,"za")
    _sdiv("Stats SA P7162 — Road Freight Survey","Exclusive Tier 1 · Modelled on Stats SA P7162 report structure")
    _chdr("Exclusive Module 1 · Stats SA P7162","Road Freight Revenue by Commodity Category",
          "Annual freight revenue (ZAR bn) — Mining dominates at 35.4%","Stats SA — Road Freight Survey P7162",STATSSA)
    st.plotly_chart(chart_za_freight_cat(gen_za_freight_category()),use_container_width=True,
                    config={"displayModeBar":False},key="za_fc")
    st.caption(f"Source: [Stats SA P7162]({STATSSA}) · Simulated data modelled on actual report structure.")
    st.markdown("<br>",unsafe_allow_html=True)
    _chdr("Exclusive Module 2 · Stats SA P7162","Payload Volume vs. Freight Income — The Cost Squeeze",
          "Diverging trends illustrate per-km cost inflation burden on fleet operators","Stats SA — P7162",STATSSA)
    st.plotly_chart(chart_za_payload_income(gen_za_payload_income()),use_container_width=True,
                    config={"displayModeBar":False},key="za_pi")
    st.caption(f"Source: [Stats SA P7162]({STATSSA}) · Simulated quarterly data.")
    st.markdown("<br>",unsafe_allow_html=True)
    _sdiv("NAAMSA — Sales Channel & Provincial Distribution","Exclusive Tier 1 · NAAMSA monthly release structure")
    ch_l,ch_r=st.columns([2,3],gap="large")
    with ch_l:
        _chdr("Module 3a · NAAMSA","HCV Sales by Channel","Dealer retail dominates; corporate fleet growing",NAAMSA,NAAMSA)
        st.plotly_chart(chart_za_channel(gen_za_channel()),use_container_width=True,
                        config={"displayModeBar":False},key="za_ch")
        st.caption(f"Source: [NAAMSA]({NAAMSA}) · Simulated data.")
    with ch_r:
        _chdr("Module 3b · NAAMSA","HCV Sales by Province","Gauteng accounts for 45.1% — industrial heartland concentration",NAAMSA,NAAMSA)
        st.plotly_chart(chart_za_province(gen_za_province()),use_container_width=True,
                        config={"displayModeBar":False},key="za_pv")
        st.caption(f"Source: [NAAMSA]({NAAMSA}) · Simulated provincial distribution.")
    _sdiv("Transnet Rail Crisis — Road Transport Demand Driver","Structural shift · Scissors effect analysis")
    _chdr("Exclusive Module 4 · Transnet / NAAMSA",
          "Transnet Rail Volume Collapse vs. HCV Road Sales Surge",
          "Rail freight down 46% from 2018 peak; road HCV absorbs displaced demand — dual-axis scissors effect",
          "Transnet Annual Report",TRANSNET)
    st.plotly_chart(chart_za_scissors(),use_container_width=True,
                    config={"displayModeBar":False},key="za_sc")
    st.caption(f"Source: [Transnet IR]({TRANSNET}) · [NAAMSA]({NAAMSA}) · Simulated data.")
    # Triangulation modules
    _sdiv("Analyst Due Diligence — Intelligence Triangulation","Critical thinking · Cross-validation · Confidence ratings")
    for tk in cdata.get("tri_keys",[]):
        with st.expander(f"🔍 {TRIANGULATION[tk]['title']}", expanded=False):
            render_triangulation(tk)

def render_nigeria(cdata):
    NADDC   = "https://naddc.gov.ng"
    CUSTOMS = "https://customs.gov.ng"
    _kpi_row(cdata)
    _standard_2col("Nigeria",cdata,"ng")
    _sdiv("Tariff Structure Analysis — The Zero-Duty Dividend","Exclusive Tier 1 · Per-unit landed cost comparison")
    _chdr("Exclusive Module · Nigeria Customs / NADDC","CBU vs. CKD/SKD Import Cost Waterfall",
          "Per-unit landed cost (30t HCV, base $100k). CKD route: ~$46k saving under 2023 EV/assembly tariff.",
          "Nigeria Customs Service",CUSTOMS)
    st.plotly_chart(chart_ng_waterfall(gen_ng_waterfall()),use_container_width=True,
                    config={"displayModeBar":False},key="ng_wf")
    st.caption(f"Source: [Nigeria Customs]({CUSTOMS}) · [NADDC]({NADDC}) · Figures illustrative.")
    _sdiv("Analyst Due Diligence — Intelligence Triangulation","Critical thinking · Cross-validation · Confidence ratings")
    for tk in cdata.get("tri_keys",[]):
        with st.expander(f"🔍 {TRIANGULATION[tk]['title']}", expanded=False):
            render_triangulation(tk)

def render_morocco(cdata):
    OCP   = "https://www.ocpgroup.ma/investor-relations"
    AIVAM = "http://www.aivam.ma"
    _kpi_row(cdata)
    _standard_2col("Morocco",cdata,"ma")
    _sdiv("OCP Group Transport Modal Assessment","Exclusive Tier 1 · Phosphate logistics structure analysis")
    _chdr("Exclusive Module 1 · OCP Group",
          "OCP Phosphate Transport Modal Split — Pipeline vs Rail vs Road",
          "Estimated annual volume by transport mode. Orange = road-accessible segment. "
          "Pipeline and rail dominate primary ore; road serves contractor and finished goods logistics.",
          "OCP Group Investor Relations",OCP)
    st.plotly_chart(chart_ma_modal(gen_ma_modal()),use_container_width=True,
                    config={"displayModeBar":False},key="ma_modal")
    st.caption(f"Source: [OCP Group IR]({OCP}) · [AIVAM]({AIVAM}) · Estimated volumes; OCP does not publish modal split data publicly.")
    st.markdown("<br>",unsafe_allow_html=True)
    _chdr("Exclusive Module 2 · OCP Group",
          "OCP Road Freight Throughput — Contractor & Finished Goods Corridor",
          "Monthly road freight throughput (kt) 2023–2026. Represents road-accessible portion only.",
          "OCP Group Investor Relations",OCP)
    st.plotly_chart(chart_ocp_throughput(gen_ocp_throughput()),use_container_width=True,
                    config={"displayModeBar":False},key="ma_ocp")
    st.caption(f"Source: [OCP Group IR]({OCP}) · Simulated data.")
    _sdiv("Analyst Due Diligence — Intelligence Triangulation","Critical thinking · Cross-validation · Confidence ratings")
    for tk in cdata.get("tri_keys",[]):
        with st.expander(f"🔍 {TRIANGULATION[tk]['title']}", expanded=False):
            render_triangulation(tk)

def render_ethiopia(cdata):
    MOTI = "https://www.moti.gov.et"
    ERCA = "https://www.erca.gov.et"
    _kpi_row(cdata)
    _standard_2col("Ethiopia",cdata,"eth")
    _sdiv("EV Penetration Surge — Post Petroleum Import Ban","Exclusive Tier 1 · Fastest EV transition on the continent")
    _chdr("Exclusive Module · MoTI Ethiopia / ERCA",
          "EV Market Share Trajectory — Monthly 2021–2026",
          "From <3% to >85% EV share in 30 months following July 2022 petroleum import ban.",
          "Ministry of Trade & Industry Ethiopia",MOTI)
    st.plotly_chart(chart_eth_ev(gen_eth_ev()),use_container_width=True,
                    config={"displayModeBar":False},key="eth_ev")
    st.caption(f"Source: [MoTI Ethiopia]({MOTI}) · [ERCA]({ERCA}) · Simulated data.")
    _sdiv("Analyst Due Diligence — Intelligence Triangulation","Critical thinking · Cross-validation · Confidence ratings")
    for tk in cdata.get("tri_keys",[]):
        with st.expander(f"🔍 {TRIANGULATION[tk]['title']}", expanded=False):
            render_triangulation(tk)

def render_generic(country, cdata):
    _kpi_row(cdata)
    _standard_2col(country,cdata,country[:2].lower())
    _sdiv("Market Entry Assessment Scorecard")
    scores_db={
        "Egypt":  {"Market Size":7,"EV Readiness":3,"Tariff Advantage":5,"Regulatory Ease":5,"Growth Momentum":8},
        "Kenya":  {"Market Size":6,"EV Readiness":6,"Tariff Advantage":6,"Regulatory Ease":7,"Growth Momentum":8},
        "Algeria":{"Market Size":6,"EV Readiness":2,"Tariff Advantage":4,"Regulatory Ease":3,"Growth Momentum":5},
        "Tunisia":{"Market Size":4,"EV Readiness":5,"Tariff Advantage":7,"Regulatory Ease":7,"Growth Momentum":4},
    }
    scores=scores_db.get(country,{d:5 for d in ["Market Size","EV Readiness","Tariff Advantage","Regulatory Ease","Growth Momentum"]})
    for col,(dim,score) in zip(st.columns(5),scores.items()):
        color="#D04A02" if score>=8 else "#295BA5" if score>=6 else "#9BA3B2"
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
    src=cdata["sources"]["trade"]
    st.caption(f"Source: [{src[0]}]({src[1]}) · Simulated market intelligence.")
    _sdiv("Analyst Due Diligence — Intelligence Triangulation","Critical thinking · Cross-validation · Confidence ratings")
    for tk in cdata.get("tri_keys",[]):
        with st.expander(f"🔍 {TRIANGULATION[tk]['title']}", expanded=False):
            render_triangulation(tk)

# ══════════════════════════════════════════════════════════════════════════════
# 12. MAP BUILDER
# ══════════════════════════════════════════════════════════════════════════════
def build_map(selected_name):
    sel_iso = next((d["iso"] for n,d in TIER1.items() if n==selected_name),"") or \
              next((iso for iso,name in ALL_AFRICA.items() if name==selected_name),"")
    rows=[]
    for iso in ALL_ISO_LIST:
        name=ISO_TO_NAME.get(iso,iso); is_t1=name in TIER1; is_sel=iso==sel_iso
        score=100 if is_sel else 70 if is_t1 else 20
        grp="selected" if is_sel else "tier1" if is_t1 else "base"
        if is_t1:
            d=TIER1[name]
            kpi_text="<br>".join(f"<b>{v[0]}</b> {v[1]}" for v in d["kpi"].values())
            tip=(f"<b style='font-size:13px;'>{d['flag']} {name}</b><br>"
                 f"<span style='color:#9BA3B2;font-size:10px;'>TIER 1 · {d['region']}</span><br><br>"
                 f"{kpi_text}<br><br><span style='color:#D04A02;font-size:10px;'>● Click to drill down</span>")
        else:
            m=TIER2_MACRO.get(iso,{}); flag=m.get("flag","🌍"); region=m.get("region","Africa")
            tip=(f"<b style='font-size:13px;'>{flag} {name}</b><br>"
                 f"<span style='color:#9BA3B2;font-size:10px;'>{region}</span><br><br>"
                 f"Est. GDP: <b>${m.get('gdp','N/A')}B</b><br>"
                 f"Est. CV Imports: <b>{m.get('cv_imports','N/A'):,} units/yr</b><br>"
                 f"Road Network: <b>{m.get('roads','N/A')}k km</b><br><br>"
                 f"<span style='color:#295BA5;font-size:10px;'>● Click for live news</span>")
        rows.append({"iso":iso,"score":score,"group":grp,"tooltip":tip})
    df=pd.DataFrame(rows)
    fig=go.Figure()
    for grp,cs,lw,lc in [
        ("base",    [[0,"#E8ECF4"],[1,"#D0D6E2"]],0.5,"#C8CDD8"),
        ("tier1",   [[0,"#6E90BF"],[1,"#295BA5"]],0.9,"#21325B"),
        ("selected",[[0,"#D04A02"],[1,"#EB6C2D"]],2.0,"#8B3000"),
    ]:
        sub=df[df.group==grp]
        if not sub.empty:
            fig.add_trace(go.Choropleth(
                locations=sub.iso,z=sub.score,text=sub.tooltip,
                hovertemplate="%{text}<extra></extra>",
                colorscale=cs,showscale=False,
                marker_line_color=lc,marker_line_width=lw,zmin=0,zmax=100))
    fig.update_layout(
        geo=dict(scope="africa",showframe=False,showcoastlines=True,
                 coastlinecolor="#C8CDD8",coastlinewidth=0.6,
                 showland=True,landcolor="#F0F2F6",showocean=True,oceancolor="#E4EEF8",
                 showcountries=True,countrycolor="#C8CDD8",countrywidth=0.5,
                 bgcolor="#F4F5F7",projection_type="natural earth"),
        paper_bgcolor="#F4F5F7",plot_bgcolor="#F4F5F7",
        margin=dict(l=0,r=0,t=0,b=0),height=420,
        hoverlabel=dict(bgcolor="white",bordercolor="#E2E5EB",
                        font=dict(family="Inter",size=12,color="#2D3142")),
        dragmode=False)
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# 13. SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if "selected_country" not in st.session_state:
    st.session_state.selected_country = "Nigeria"

# ══════════════════════════════════════════════════════════════════════════════
# 14. SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 4px 12px 4px;border-bottom:1px solid rgba(255,255,255,.12);">
        <div style="font-family:'Inter';font-size:1.05rem;font-weight:700;color:white;letter-spacing:-.2px;">
            Africa CV Intelligence
        </div>
        <div style="font-family:'Inter';font-size:.68rem;color:rgba(255,255,255,.4);margin-top:2px;">
            Enterprise Market Analytics · v7.0
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="sb-hdr">Core Markets (Tier 1)</div>', unsafe_allow_html=True)
    for cname,cd in TIER1.items():
        is_active=st.session_state.selected_country==cname
        if is_active:
            st.markdown(f"""
            <div style="padding:9px 13px;margin:3px 0;border-radius:6px;
                        background:#D04A02;border:1px solid #D04A02;
                        font-family:'Inter';font-size:.81rem;font-weight:700;color:white;">
                {cd['flag']} &nbsp;{cname}
                <span style="opacity:.7;font-size:.65rem;margin-left:6px;">● Active</span>
            </div>""", unsafe_allow_html=True)
        else:
            if st.button(f"{cd['flag']}  {cname}",key=f"sb_{cname}",use_container_width=True):
                st.session_state.selected_country=cname
                st.cache_data.clear(); st.rerun()
    st.markdown('<div class="sb-hdr">Quick Reference</div>', unsafe_allow_html=True)
    for label,url in [
        ("📊 Stats SA — P7162","https://www.statssa.gov.za"),
        ("🏭 NAAMSA","https://naamsa.co.za"),
        ("🏛 Nigeria Customs","https://www.customs.gov.ng"),
        ("🚂 Transnet IR","https://www.transnet.net/InvestorCentre"),
        ("🌾 OCP Group","https://www.ocpgroup.ma"),
        ("🌍 AfDB","https://www.afdb.org"),
        ("📰 The Africa Report","https://www.theafricareport.com"),
        ("📊 Zawya Finance","https://www.zawya.com"),
    ]:
        st.markdown(f'<a class="sb-link" href="{url}" target="_blank">{label}</a>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    if st.button("↺  Refresh Intelligence Feed",use_container_width=True,key="refresh"):
        st.cache_data.clear(); st.rerun()
    st.markdown(f"""
    <div style="font-family:'Inter';font-size:.58rem;color:rgba(255,255,255,.22);
                text-align:center;margin-top:16px;line-height:2.1;">
        Africa CV Intelligence v7.0<br>{datetime.now().strftime('%Y-%m-%d %H:%M')} · Internal use only
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 15. PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
h1,h2=st.columns([3,1])
with h1:
    st.markdown("""
    <div style="padding:18px 0 6px 0;">
        <div style="font-family:'Inter';font-size:1.28rem;font-weight:700;color:#2D3142;letter-spacing:-.3px;">
            Africa Commercial Vehicle Market Intelligence
        </div>
        <div style="font-family:'Inter';font-size:.78rem;color:#9BA3B2;margin-top:3px;">
            54-nation coverage · Tier 1 deep analytics · Intelligence Triangulation · Analyst Due Diligence Framework
        </div>
    </div>""", unsafe_allow_html=True)
with h2:
    st.markdown(f"""
    <div style="padding:18px 0 6px 0;text-align:right;">
        <div style="font-family:'Inter';font-size:.7rem;color:#9BA3B2;">{datetime.now().strftime('%B %d, %Y')}</div>
        <div style="font-family:'Inter';font-size:.74rem;color:#D04A02;font-weight:600;margin-top:2px;">● Live Intelligence Feed</div>
    </div>""", unsafe_allow_html=True)
st.markdown('<hr style="margin:0 0 18px 0;border-color:#E2E5EB;">',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 16. MAP SECTION
# ══════════════════════════════════════════════════════════════════════════════
sel=st.session_state.selected_country
is_t1=sel in TIER1
cdata=TIER1.get(sel,{})
sel_iso=cdata.get("iso","") if is_t1 else next((iso for iso,name in ALL_AFRICA.items() if name==sel),"")
macro=TIER2_MACRO.get(sel_iso,{})

map_col,snap_col=st.columns([5,2],gap="large")
with map_col:
    st.markdown("""
    <div style="font-family:'Inter';font-size:.7rem;font-weight:700;letter-spacing:.8px;
                text-transform:uppercase;color:#5A6070;margin-bottom:8px;">
        Africa Strategic Market Map
        <span style="font-weight:400;color:#9BA3B2;margin-left:8px;">
        · Click any country to drill down · Orange = selected · Blue = Tier 1
        </span>
    </div>""", unsafe_allow_html=True)
    map_fig=build_map(sel)
    map_event=st.plotly_chart(map_fig,use_container_width=True,
        config={"displayModeBar":False,"scrollZoom":False},
        on_select="rerun",selection_mode="points",key="africa_map")
    if map_event and hasattr(map_event,"selection") and map_event.selection:
        pts=map_event.selection.get("points",[])
        if pts:
            clicked_iso=pts[0].get("location","")
            clicked_name=ISO_TO_NAME.get(clicked_iso,"")
            if clicked_name and clicked_name!=st.session_state.selected_country:
                st.session_state.selected_country=clicked_name
                st.cache_data.clear(); st.rerun()
    leg_cols=st.columns(len(TIER1))
    for lc,(cname,cd) in zip(leg_cols,TIER1.items()):
        active=cname==sel; color="#D04A02" if active else "#295BA5"
        bg="rgba(208,74,2,0.08)" if active else "rgba(41,91,165,0.05)"
        with lc:
            st.markdown(f"""
            <div style="text-align:center;padding:5px 3px;border-radius:6px;
                        background:{bg};border:1px solid {'#D04A02' if active else '#E2E5EB'};">
                <div style="font-size:.9rem;">{cd['flag']}</div>
                <div style="font-family:'Inter';font-size:.6rem;font-weight:{'700' if active else '500'};
                            color:{color};margin-top:1px;">{cname.split()[0]}</div>
            </div>""", unsafe_allow_html=True)

with snap_col:
    flag=cdata.get("flag","🌍") if is_t1 else macro.get("flag","🌍")
    region=cdata.get("region","Africa") if is_t1 else macro.get("region","Africa")
    sources=cdata.get("sources",{}) if is_t1 else {}
    main_src=list(sources.values())[0] if sources else ("","")
    st.markdown(f"""
    <div style="background:white;border:1px solid #E2E5EB;border-radius:8px;
                padding:18px;box-shadow:0 1px 4px rgba(0,0,0,.07);border-top:4px solid #D04A02;">
        <div style="font-family:'Inter';font-size:.68rem;font-weight:700;letter-spacing:.8px;
                    text-transform:uppercase;color:#9BA3B2;margin-bottom:10px;">Currently Viewing</div>
        <div style="font-size:1.8rem;margin-bottom:3px;">{flag}</div>
        <div style="font-family:'Inter';font-size:1.05rem;font-weight:700;color:#2D3142;">{sel}</div>
        <div style="font-family:'Inter';font-size:.72rem;color:#9BA3B2;margin-bottom:12px;">{region}</div>
        <div style="border-top:1px solid #F0F2F5;padding-top:12px;">
    """, unsafe_allow_html=True)
    if not is_t1:
        st.markdown('<div class="fallback-badge">⚠ Tier 2 — General Coverage</div>',unsafe_allow_html=True)
        for label,val in [("Est. GDP","${:,.1f}B".format(macro.get("gdp",0))),
                           ("Road Network","{:,}k km".format(macro.get("roads",0))),
                           ("Est. CV Imports","{:,} units/yr".format(macro.get("cv_imports",0)))]:
            st.markdown(f"""
            <div style="margin-bottom:10px;">
                <div style="font-family:'Inter';font-size:.65rem;color:#9BA3B2;text-transform:uppercase;letter-spacing:.5px;">{label}</div>
                <div style="font-family:'Inter';font-size:1.1rem;font-weight:700;color:#2D3142;">{val}</div>
            </div>""", unsafe_allow_html=True)
    else:
        for key,(value,label,delta,_) in cdata["kpi"].items():
            dc="#1A8C5B" if "+" in delta else "#D04A02" if "-" in delta else "#5A6070"
            st.markdown(f"""
            <div style="margin-bottom:11px;padding-bottom:11px;border-bottom:1px solid #F0F2F5;">
                <div style="font-family:'Inter';font-size:.65rem;color:#9BA3B2;text-transform:uppercase;letter-spacing:.5px;">{label}</div>
                <div style="font-family:'Inter';font-size:1.1rem;font-weight:700;color:#2D3142;margin:2px 0;">{value}</div>
                <div style="font-family:'Inter';font-size:.68rem;color:{dc};font-weight:500;">{delta}</div>
            </div>""", unsafe_allow_html=True)
        if main_src[0]:
            st.markdown(f'<div style="font-family:Inter;font-size:.62rem;color:#295BA5;margin-top:4px;">📌 <a href="{main_src[1]}" target="_blank" style="color:#295BA5;">{main_src[0]}</a></div>',unsafe_allow_html=True)
    st.markdown("</div></div>",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 17. COUNTRY DASHBOARD TABS
# ══════════════════════════════════════════════════════════════════════════════
flag_display=cdata.get("flag",macro.get("flag","🌍")) if is_t1 else macro.get("flag","🌍")
tri_count=len(cdata.get("tri_keys",[])) if is_t1 else 0
st.markdown(f"""
<div class="section-hdr">
    <div class="section-bar"></div>
    <div class="section-title">{flag_display} &nbsp;{sel} — Country Dashboard</div>
    <div class="section-sub">
        {"Full Tier 1 · Stats SA P7162 · NAAMSA" if sel=="South Africa" else
         f"Full Tier 1 analytics · {tri_count} Triangulation module{'s' if tri_count!=1 else ''}" if is_t1 else
         "General coverage — live news + macro indicators"}
    </div>
</div>""", unsafe_allow_html=True)

tab_market,tab_policy,tab_news=st.tabs([
    "📊  Market Analytics",
    "📋  Policy & Market Access",
    "📡  Intelligence Feed",
])

with tab_market:
    if not is_t1:
        st.info(f"**{sel}** is a Tier 2 market. Full analytics available for 8 Tier 1 core markets.",icon="ℹ️")
        m1,m2,m3=st.columns(3)
        with m1: st.metric("Est. GDP","${:,.1f}B".format(macro.get("gdp",0)),help="IMF WEO estimate")
        with m2: st.metric("Road Network","{:,}k km".format(macro.get("roads",0)),help="AfDB infrastructure data")
        with m3: st.metric("Est. CV Imports","{:,} units/yr".format(macro.get("cv_imports",0)),help="Regional trade estimate")
        st.caption("Source: [AfDB](https://www.afdb.org) · [IMF WEO](https://www.imf.org) · Indicative estimates.")
    elif sel=="South Africa": render_south_africa(cdata)
    elif sel=="Nigeria":      render_nigeria(cdata)
    elif sel=="Morocco":      render_morocco(cdata)
    elif sel=="Ethiopia":     render_ethiopia(cdata)
    else:                     render_generic(sel,cdata)

with tab_policy:
    if not is_t1:
        st.info(f"Detailed policy brief for **{sel}** not yet available. Showing AfCFTA general framework.",icon="📋")
        st.markdown("""
        <div class="pol-card">
            <div class="pol-card-title">🌍 African Continental Free Trade Area (AfCFTA)</div>
            <p>Member states are progressively eliminating tariffs on 90% of goods.
            Commercial vehicles are classified as sensitive goods with 10–15 year phase-out timelines.
            Check the AfCFTA Secretariat for country-specific schedules.</p>
        </div>""", unsafe_allow_html=True)
        st.caption("Source: [AfCFTA Secretariat](https://au-afcfta.org) · [AfDB](https://www.afdb.org)")
    else:
        p=cdata["policy"]
        src_c=cdata["sources"].get("customs",("",""))
        src_m=cdata["sources"].get("market",("",""))
        src_t=cdata["sources"].get("trade",("",""))
        pl,pr=st.columns(2,gap="large")
        with pl:
            st.markdown(f'<div class="pol-card"><div class="pol-card-title">🏷 Tariff & Import Structure</div><p>{p["tariff"]}</p></div>',unsafe_allow_html=True)
            st.caption(f"Source: [{src_c[0]}]({src_c[1]})")
            st.markdown(f'<div class="pol-card ok"><div class="pol-card-title">📋 Certification & Homologation</div><p>{p["certification"]}</p></div>',unsafe_allow_html=True)
            st.caption(f"Source: [{src_m[0]}]({src_m[1]})")
        with pr:
            st.markdown(f'<div class="pol-card"><div class="pol-card-title">🏗 Key Buyers & Procurement Bodies</div><p>{p["key_buyers"]}</p></div>',unsafe_allow_html=True)
            st.caption(f"Source: [{src_t[0]}]({src_t[1]})")
            st.markdown(f'<div class="pol-card warn"><div class="pol-card-title">⚠ Risk Factors & Operational Considerations</div><p>{p["risk"]}</p></div>',unsafe_allow_html=True)
        _sdiv("Market Entry Assessment Scorecard")
        all_sc={
            "Nigeria":      {"Market Size":9,"EV Readiness":7,"Tariff Advantage":9,"Regulatory Ease":5,"Growth Momentum":7},
            "South Africa": {"Market Size":8,"EV Readiness":5,"Tariff Advantage":4,"Regulatory Ease":8,"Growth Momentum":4},
            "Morocco":      {"Market Size":6,"EV Readiness":6,"Tariff Advantage":8,"Regulatory Ease":8,"Growth Momentum":8},
            "Egypt":        {"Market Size":7,"EV Readiness":3,"Tariff Advantage":5,"Regulatory Ease":5,"Growth Momentum":8},
            "Kenya":        {"Market Size":6,"EV Readiness":6,"Tariff Advantage":6,"Regulatory Ease":7,"Growth Momentum":8},
            "Ethiopia":     {"Market Size":5,"EV Readiness":9,"Tariff Advantage":9,"Regulatory Ease":6,"Growth Momentum":9},
            "Algeria":      {"Market Size":6,"EV Readiness":2,"Tariff Advantage":4,"Regulatory Ease":3,"Growth Momentum":5},
            "Tunisia":      {"Market Size":4,"EV Readiness":5,"Tariff Advantage":7,"Regulatory Ease":7,"Growth Momentum":4},
        }
        scores=all_sc.get(sel,{d:5 for d in ["Market Size","EV Readiness","Tariff Advantage","Regulatory Ease","Growth Momentum"]})
        for col,(dim,score) in zip(st.columns(5),scores.items()):
            color="#D04A02" if score>=8 else "#295BA5" if score>=6 else "#9BA3B2"
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
                </div>""", unsafe_allow_html=True)
        st.caption(f"Source: [{src_t[0]}]({src_t[1]}) · Assessment based on simulated market intelligence.")

with tab_news:
    news_query=cdata.get("news_query","") if is_t1 else f"{sel} transport logistics commercial vehicle"
    st.markdown(f"""
    <div style="background:#F8F9FB;border:1px solid #E2E5EB;border-radius:8px;
                padding:11px 16px;margin-bottom:18px;font-family:'Inter';font-size:.78rem;color:#5A6070;line-height:1.7;">
        <strong style="color:#2D3142;">Intelligence parameters:</strong>
        &nbsp;Focus: <strong style="color:#D04A02;">{sel}</strong>
        &nbsp;·&nbsp; Sources: Reuters · Bloomberg · FT · Engineering News · BusinessDay · Zawya · Africa Report
        &nbsp;·&nbsp; Window: <strong>Last 30 days</strong>
        &nbsp;·&nbsp; Wide-net fetch → authority filter → fallback guarantee
        {"&nbsp;·&nbsp; <span style='color:#D04A02;'>⚠ Tier 2 — general coverage</span>" if not is_t1 else ""}
    </div>""", unsafe_allow_html=True)
    nc,pc=st.columns([3,1],gap="large")
    with nc:
        render_news_panel(news_query,sel)
    with pc:
        st.markdown("""
        <div style="background:white;border:1px solid #E2E5EB;border-radius:8px;
                    padding:16px;box-shadow:0 1px 4px rgba(0,0,0,.06);">
            <div style="font-family:'Inter';font-size:.68rem;font-weight:700;text-transform:uppercase;
                        letter-spacing:.6px;color:#9BA3B2;margin-bottom:12px;">Fetch Strategy</div>""",
        unsafe_allow_html=True)
        for label,val in [("Pass 1","Broad query + when:30d"),("Pass 2","Authority domain filter"),
                           ("Pass 3","All recent results"),("Pass 4","90-day fallback"),("Cache TTL","30 min")]:
            st.markdown(f"""
            <div style="margin-bottom:9px;">
                <div style="font-family:'Inter';font-size:.62rem;color:#9BA3B2;">{label}</div>
                <div style="font-family:'Inter';font-size:.78rem;font-weight:500;color:#2D3142;">{val}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown(f"""
            <div style="margin-top:8px;padding-top:8px;border-top:1px solid #F0F2F5;">
                <div style="font-family:'Inter';font-size:.62rem;color:#9BA3B2;margin-bottom:4px;">Keywords</div>
                <div style="font-family:'Inter';font-size:.72rem;color:#5A6070;line-height:1.6;
                            word-break:break-word;background:#F8F9FB;border-radius:5px;padding:7px 9px;">
                    {news_query}
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown("""
        <div style="background:white;border:1px solid #E2E5EB;border-radius:8px;
                    padding:16px;box-shadow:0 1px 4px rgba(0,0,0,.06);">
            <div style="font-family:'Inter';font-size:.68rem;font-weight:700;text-transform:uppercase;
                        letter-spacing:.6px;color:#9BA3B2;margin-bottom:10px;">Authority Domains</div>""",
        unsafe_allow_html=True)
        for src,url in [("Reuters","https://reuters.com"),("Bloomberg","https://bloomberg.com"),
                         ("Financial Times","https://ft.com"),("Engineering News ZA","https://engineeringnews.co.za"),
                         ("BusinessDay NG","https://businessday.ng"),("Zawya","https://zawya.com"),
                         ("The Africa Report","https://theafricareport.com"),("AfDB","https://afdb.org")]:
            st.markdown(f"""
            <div style="font-family:'Inter';font-size:.72rem;color:#5A6070;
                        padding:4px 0;border-bottom:1px solid #F4F5F7;">
                <span style="display:inline-block;width:6px;height:6px;border-radius:50%;
                             background:#1A8C5B;margin-right:6px;"></span>
                <a href="https://{url}" target="_blank" style="color:#295BA5;text-decoration:none;">{src}</a>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 18. FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<br>",unsafe_allow_html=True)
st.markdown(f"""
<div style="border-top:1px solid #E2E5EB;padding-top:14px;
            font-family:'Inter';font-size:.68rem;color:#9BA3B2;">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
        <div>
            <strong style="color:#5A6070;">Africa CV Market Intelligence Platform v7.0</strong>
            &nbsp;·&nbsp; Internal strategic use only &nbsp;·&nbsp; Simulated data for illustrative purposes
            &nbsp;·&nbsp; Intelligence Triangulation Framework · 54-nation coverage
        </div>
        <div style="text-align:right;">
            Reuters · Bloomberg · FT · NAAMSA · NADDC · Stats SA · AIVAM · OCP · AfDB
            &nbsp;·&nbsp; {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC
        </div>
    </div>
</div>""", unsafe_allow_html=True)
