"""
Africa Commercial Vehicle Market Intelligence Platform
Enterprise BI Engine v11.0
McKinsey UX Refactor — Narrative-Flow Layout · Zero Text Overlap · Collapsed Intel Feed
"""

import streamlit as st
import feedparser
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import copy
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
# 1. GLOBAL CSS — including mandatory anti text-overlap rule
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
:root{
    --bg:#F4F5F7;--white:#FFFFFF;--orange:#D04A02;--orange2:#EB6C2D;
    --navy:#21325B;--blue:#295BA5;--txt:#2D3142;--mid:#5A6070;
    --dim:#9BA3B2;--border:#E2E5EB;--green:#1A8C5B;--amber:#B45309;--red:#B91C1C;
    --shadow:0 1px 4px rgba(0,0,0,.07),0 4px 16px rgba(0,0,0,.04);--radius:8px;
}
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"],.main{
    background:var(--bg)!important;font-family:'Inter',sans-serif!important;color:var(--txt);
}
[data-testid="stSidebar"]{background:var(--navy)!important;border-right:none!important;}
[data-testid="stSidebar"] *{color:#E8ECF4!important;}
[data-testid="stSidebar"] .stButton>button{
    background:var(--orange)!important;color:#fff!important;
    border:none!important;border-radius:var(--radius)!important;font-weight:600!important;
}
[data-testid="stSidebar"] .stButton>button:hover{background:var(--orange2)!important;}
[data-testid="stTabsTabList"]{
    background:var(--white)!important;border-bottom:2px solid var(--border)!important;
    border-radius:var(--radius) var(--radius) 0 0;padding:0 8px;box-shadow:var(--shadow);
}
button[data-baseweb="tab"]{
    font-family:'Inter',sans-serif!important;font-size:.84rem!important;
    font-weight:500!important;color:var(--mid)!important;
    padding:11px 18px!important;border-bottom:3px solid transparent!important;
    background:transparent!important;border-radius:0!important;
}
button[aria-selected="true"][data-baseweb="tab"]{
    color:var(--orange)!important;border-bottom:3px solid var(--orange)!important;font-weight:700!important;
}
[data-testid="stTabPanel"]{background:transparent!important;padding:22px 0 0 0!important;border:none!important;}
[data-testid="metric-container"]{
    background:var(--white)!important;border:1px solid var(--border)!important;
    border-radius:var(--radius)!important;padding:18px 20px!important;
    box-shadow:var(--shadow)!important;border-top:3px solid var(--orange)!important;
}
[data-testid="stMetricLabel"]{
    font-size:.68rem!important;font-weight:700!important;
    letter-spacing:.8px!important;color:var(--mid)!important;text-transform:uppercase!important;
}
[data-testid="stMetricValue"]{font-size:1.65rem!important;font-weight:700!important;color:var(--txt)!important;}
.section-hdr{
    display:flex;align-items:center;gap:10px;
    margin:30px 0 16px 0;padding-bottom:10px;border-bottom:1px solid var(--border);
}
.section-bar{width:4px;height:20px;background:var(--orange);border-radius:2px;flex-shrink:0;}
.level-badge{
    font-size:.62rem;font-weight:700;letter-spacing:1px;color:#fff;
    background:var(--navy);padding:3px 10px;border-radius:20px;text-transform:uppercase;
    flex-shrink:0;
}
.section-title{font-size:.88rem;font-weight:700;letter-spacing:.4px;color:var(--txt);text-transform:uppercase;}
.section-sub{font-size:.72rem;color:var(--dim);margin-left:4px;}
.chart-card{
    background:var(--white);border:1px solid var(--border);
    border-radius:var(--radius);padding:18px 18px 8px 18px;box-shadow:var(--shadow);margin-bottom:4px;
}
.chart-label{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.7px;color:var(--dim);margin-bottom:2px;}
.chart-title{font-size:.92rem;font-weight:700;color:var(--txt);margin-bottom:2px;}
.chart-sub{font-size:.72rem;color:var(--dim);margin-bottom:10px;}
.source-link{font-size:.68rem;color:var(--blue);margin-top:4px;}
.pol-card{
    background:var(--white);border:1px solid var(--border);
    border-left:4px solid var(--blue);border-radius:var(--radius);
    padding:14px 18px;box-shadow:var(--shadow);margin-bottom:12px;
}
.pol-card.warn{border-left-color:var(--orange);}
.pol-card.ok{border-left-color:var(--green);}
.pol-card-title{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:var(--mid);margin-bottom:7px;}
.sb-hdr{
    font-size:.6rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;
    color:rgba(255,255,255,.38)!important;margin:16px 0 6px 0;
    padding-bottom:4px;border-bottom:1px solid rgba(255,255,255,.1);
}
.sb-link{
    display:block;padding:7px 11px;margin:3px 0;border-radius:6px;font-size:.77rem;
    color:#C8D3E8!important;text-decoration:none!important;
    border:1px solid rgba(255,255,255,.08);background:rgba(255,255,255,.04);
    transition:all .15s;
}
.sb-link:hover{background:rgba(208,74,2,.2);border-color:rgba(208,74,2,.5);color:#fff!important;}
.news-wrap{background:var(--white);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;}
.news-hdr{background:var(--navy);padding:11px 16px;display:flex;align-items:center;gap:10px;}
.news-hdr-title{font-size:.78rem;font-weight:600;color:#fff;letter-spacing:.4px;text-transform:uppercase;}
.news-badge{background:var(--orange);color:#fff;font-size:.58rem;font-weight:700;padding:2px 8px;border-radius:20px;}
.news-fb-badge{background:#F0F3F8;color:var(--mid);font-size:.58rem;font-weight:700;padding:2px 8px;border-radius:20px;}
.news-item{padding:13px 16px;border-bottom:1px solid var(--border);}
.news-item:last-child{border-bottom:none;}
.news-title-a{
    font-size:.83rem;font-weight:500;color:var(--txt)!important;
    text-decoration:none!important;line-height:1.55;display:block;
}
.news-title-a:hover{color:var(--orange)!important;}
.news-meta{font-size:.68rem;color:var(--dim);margin-top:5px;}
.news-src{display:inline-block;background:#F0F3F8;color:var(--navy);font-size:.6rem;font-weight:600;padding:1px 7px;border-radius:4px;margin-right:5px;}
.news-fb-src{display:inline-block;background:#FFF3ED;color:var(--orange);font-size:.6rem;font-weight:600;padding:1px 7px;border-radius:4px;margin-right:5px;}
.news-empty{padding:28px 16px;text-align:center;color:var(--dim);font-size:.8rem;line-height:1.8;}
.action-box{
    background:linear-gradient(135deg,#FFF8F5 0%,#FFF3ED 100%);
    border:2px solid var(--orange);border-radius:var(--radius);
    padding:18px 20px;margin-top:16px;box-shadow:var(--shadow);
}
.action-box-title{
    font-size:.78rem;font-weight:700;letter-spacing:.6px;color:var(--orange);
    text-transform:uppercase;margin-bottom:8px;
}
.gate-index-card{
    background:var(--white);border:1px solid var(--border);border-radius:var(--radius);
    padding:16px 18px;box-shadow:var(--shadow);text-align:center;
}
.gate-index-value{font-size:2.2rem;font-weight:700;font-family:'Inter';}
.gate-index-label{font-size:.65rem;color:var(--dim);text-transform:uppercase;letter-spacing:.6px;margin-top:4px;}

/* ── GTM Playbook cards (Task 3) ── */
.gtm-card{
    background:var(--white);border:1px solid var(--border);border-radius:var(--radius);
    padding:0;box-shadow:var(--shadow);overflow:hidden;margin-bottom:16px;height:100%;
}
.gtm-card-hdr{
    padding:14px 18px;display:flex;align-items:center;gap:10px;
}
.gtm-card-hdr.product{background:linear-gradient(135deg,#FFF3ED 0%,#FFE8DC 100%);border-bottom:2px solid var(--orange);}
.gtm-card-hdr.supply{background:linear-gradient(135deg,#EEF2FA 0%,#E3EAF7 100%);border-bottom:2px solid var(--navy);}
.gtm-card-hdr.persona{background:linear-gradient(135deg,#EAF6F0 0%,#DCF0E6 100%);border-bottom:2px solid var(--green);}
.gtm-card-icon{font-size:1.4rem;flex-shrink:0;}
.gtm-card-title{font-size:.82rem;font-weight:700;color:var(--txt);letter-spacing:.2px;}
.gtm-card-subtitle{font-size:.62rem;color:var(--mid);text-transform:uppercase;letter-spacing:.6px;margin-top:1px;}
.gtm-card-body{padding:16px 18px;font-size:.83rem;line-height:1.75;color:var(--txt);}
.gtm-card-body b{color:var(--orange);}
.gtm-mission-banner{
    background:linear-gradient(135deg,#21325B 0%,#1A2747 100%);
    border-radius:var(--radius);padding:18px 24px;margin-bottom:20px;
    box-shadow:0 4px 16px rgba(33,50,91,.25);
}
.gtm-mission-title{font-size:.95rem;font-weight:700;color:#fff;letter-spacing:.3px;}
.gtm-mission-sub{font-size:.72rem;color:#B8C4DC;margin-top:4px;}
#MainMenu,footer,header{visibility:hidden;}
[data-testid="stToolbar"]{display:none;}
.block-container{padding-top:0!important;}

/* ── MANDATORY ANTI TEXT-OVERLAP RULE (Task 1) ── */
.stMarkdown, p, div {word-wrap: break-word; overflow-wrap: break-word;}

/* ── B2B Pricing & Margin Sandbox (Battle 3) ── */
.b2b-banner{
    background:linear-gradient(135deg,#21325B 0%,#1A2747 100%);
    border-radius:var(--radius);padding:16px 22px;margin:18px 0 16px 0;
    box-shadow:0 4px 16px rgba(33,50,91,.25);
}
.b2b-banner-title{font-size:.92rem;font-weight:700;color:#fff;letter-spacing:.3px;}
.b2b-banner-sub{font-size:.72rem;color:#B8C4DC;margin-top:4px;}
.b2b-output-card{
    background:var(--white);border:2px solid var(--border);border-radius:var(--radius);
    padding:20px 22px;box-shadow:var(--shadow);text-align:center;height:100%;
}
.b2b-output-card.fob{border-color:var(--navy);}
.b2b-output-card.profit-ok{border-color:var(--green);background:linear-gradient(135deg,#F2FBF6 0%,#EAF6F0 100%);}
.b2b-output-card.profit-bad{border-color:var(--red);background:linear-gradient(135deg,#FDF3F2 0%,#FBEAE8 100%);}
.b2b-output-label{font-size:.66rem;font-weight:700;letter-spacing:.8px;color:var(--dim);text-transform:uppercase;}
.b2b-output-value{font-size:2.1rem;font-weight:700;font-family:'Inter';margin-top:6px;}
.b2b-output-sub{font-size:.68rem;color:var(--dim);margin-top:4px;}

/* ── TCO Sandbox lock banner (Battle 2) ── */
.tco-lock-banner{
    display:flex;align-items:center;justify-content:space-between;gap:12px;
    background:#F8F9FB;border:1px solid var(--border);border-radius:var(--radius);
    padding:10px 14px;margin-bottom:10px;
}
.tco-lock-banner.unlocked{background:#FFF8F5;border-color:var(--orange);}

/* ── Internal Competitive Intel (Tab 4) ── */
.intel-banner{
    background:linear-gradient(135deg,#1A1F2E 0%,#2D1B0F 100%);
    border:1px solid #3A2A1A;border-radius:var(--radius);
    padding:16px 22px;margin:6px 0 16px 0;box-shadow:0 4px 16px rgba(0,0,0,.25);
}
.intel-banner-title{font-size:.92rem;font-weight:700;color:#FFD8B8;letter-spacing:.3px;}
.intel-banner-sub{font-size:.7rem;color:#B8A896;margin-top:4px;}
.intel-badge{
    display:inline-block;font-size:.58rem;font-weight:700;letter-spacing:.6px;
    padding:2px 9px;border-radius:20px;text-transform:uppercase;margin-left:8px;
    background:#3A2A1A;color:#FFD8B8;vertical-align:middle;
}
.brand-legend{display:flex;gap:14px;flex-wrap:wrap;margin:6px 0 14px 0;}
.brand-legend-item{display:flex;align-items:center;gap:6px;font-size:.72rem;color:var(--mid);}
.brand-legend-dot{width:10px;height:10px;border-radius:50%;display:inline-block;}
.footprint-card{
    background:var(--white);border:1px solid var(--border);border-left:4px solid #8B3000;
    border-radius:var(--radius);padding:16px 18px;box-shadow:var(--shadow);margin-bottom:12px;
}
.footprint-card-title{font-size:.74rem;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:#8B3000;margin-bottom:7px;}
.footprint-card-body{font-size:.83rem;line-height:1.75;color:var(--txt);}
.footprint-card-body b{color:#D04A02;}
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

def _apply(fig, ov=None):
    layout = dict(**CHART_BASE)
    if ov:
        layout.update(ov)
    fig.update_layout(**layout)
    return fig

PLOTLY_CFG = {"displayModeBar": False}
# ══════════════════════════════════════════════════════════════════════════════
# 3. TRIANGULATION DATA — unchanged structure, reused verbatim
# ══════════════════════════════════════════════════════════════════════════════
TRIANGULATION = {
    "rw_sandbox": {
        "title": "Rwanda Market Size vs. Strategic EAC Value — Small Volume, Outsized Positioning",
        "claim": "Rwanda's total CV market of ~3,200 units/year is too small to justify meaningful commercial investment in fleet sales or local distribution infrastructure for a Chinese commercial vehicle manufacturer.",
        "cross_validation_items": [
            "**[Fact]** Rwanda Development Board (RDB) confirmed: EV commercial vehicles enjoy **0% import duty, 0% VAT, 0% excise tax** — the most comprehensive EV fiscal exemption package in Sub-Saharan Africa (RDB Investment Incentives 2024).",
            "**[Fact]** Rwanda's corporate income tax for qualifying EV/clean energy enterprises is **15%** (vs standard 30%) under the Special Economic Zone and Priority Sector incentive regime (RRA, 2024).",
            "**[Fact]** RURA has established a dedicated **e-mobility electricity tariff** of RWF 115/kWh — approximately **14× cheaper** than diesel-equivalent energy cost.",
            "**[Fact]** Kigali's grid reliability is among Africa's highest: **<2% outage rate** (REG), powered predominantly by hydro, methane, and solar.",
            "**[Structural logic]** Rwanda is the **EAC headquarters hub**: AfDB East Africa Regional Office, AUDA-NEPAD, and 47+ international organisations are based in Kigali.",
            "**[Market trajectory]** Rwanda's 2035 target to transition 100% of public transport and 70% of commercial vehicles to EV creates a **policy-locked demand pipeline**.",
            "**[Counter-evidence]** Absolute unit volume will remain low (<5,000 CVs/yr through 2030). Infrastructure outside Kigali is limited.",
        ],
        "verdict": "Rwanda is **not a volume market** — it is a **strategic sandbox and EAC showcase**. Deploy 20–50 EV commercial units in Kigali via G2G bus programmes and B2B city logistics, generate verifiable performance data, and leverage that proof-of-concept to unlock EAC-wide fleet tenders.",
        "verdict_type": "success",
        "confidence_items": [
            ("🟢 Verified Fact", "0% import duty / 0% VAT for EV CVs (RDB 2024)"),
            ("🟢 Verified Fact", "15% CIT for qualifying clean energy enterprises"),
            ("🟢 Verified Fact", "RURA e-mobility tariff RWF 115/kWh vs RWF 1,600/L diesel"),
            ("🟢 Verified Fact", "<2% grid outage rate (REG Annual Report 2024)"),
            ("🟡 Plausible Estimate", "Kigali EV deployment as EAC-wide proof-of-concept accelerator"),
            ("🟡 Plausible Estimate", "G2G bus programme as lowest-risk entry vehicle"),
            ("🔴 Needs Field Verification", "2035 EV mandate enforcement mechanism and budget allocation"),
        ],
    },
    "rw_eac_gateway": {
        "title": "Rwanda as EAC Gateway — Does the Regulatory Advantage Transfer to Neighbouring Markets?",
        "claim": "A Rwanda-registered EV fleet operation automatically grants preferential access to Kenya, Uganda, and Tanzania markets under the EAC Common Market Protocol.",
        "cross_validation_items": [
            "**[Fact]** The EAC Common Market Protocol establishes free movement of goods — but vehicle registration and homologation requirements remain national, not harmonised.",
            "**[Fact]** KEBS PVoC is required for all vehicles entering Kenya, regardless of EAC origin country.",
            "**[Fact]** TBS maintains separate type-approval requirements; Rwanda registration does not grant automatic TBS homologation.",
            "**[Nuance]** EAC Customs Union eliminates tariffs between Partner States — but technical standards remain independently enforced.",
            "**[Strategic reality]** The gateway value is **reputational and relational**: a Kigali proof-of-concept generates case studies and RDB endorsement letters with significant weight in EAC procurement evaluations.",
        ],
        "verdict": "The EAC gateway thesis is **partially valid**: tariff elimination is confirmed, but technical standards barriers in Kenya and Tanzania require separate homologation investment. The strategic value is primarily proof-of-concept documentation, not automatic regulatory passthrough.",
        "verdict_type": "warning",
        "confidence_items": [
            ("🟢 Verified Fact", "EAC Customs Union: zero tariffs between Partner States"),
            ("🟢 Verified Fact", "KEBS PVoC required for Kenya — Rwanda registration not sufficient"),
            ("🟡 Plausible Estimate", "Kigali proof-of-concept accelerates Kenya/Tanzania procurement"),
            ("🔴 Needs Field Verification", "TBS (Tanzania) type-approval timeline for Chinese EV CVs"),
        ],
    },
    "ma_ocp_modal": {
        "title": "OCP Transport Modal & Road HCV Procurement Potential",
        "claim": "Industry commentators cite OCP Group as a flagship anchor client with annual HCV procurement of **800–1,000 units/year**, driven by the Khouribga–Jorf Lasfar phosphate corridor.",
        "cross_validation_items": [
            "**[Fact]** OCP operates a dedicated **187 km slurry pipeline** — structurally inaccessible to road HCVs (OCP Integrated Annual Report 2023).",
            "**[Fact]** OCP also operates the Benguerir–Jorf Lasfar rail corridor for phosphate concentrate.",
            "**[Structural logic]** Pipeline and rail serve only the primary ore trunk. ~60 contractor companies perform auxiliary logistics — structurally road-dependent.",
            "**[Counter-evidence]** No publicly accessible OCP tender database confirms a recurring 800-unit annual HCV figure.",
            "**[Supportive proxy]** OCP 2023 capex of USD 2.1 billion includes mining fleet renewal.",
        ],
        "verdict": "The slurry pipeline dominates primary ore haulage. The contractor ecosystem represents a real and recurring HCV demand segment. The 800 units/year figure is a bottom-up estimate, not a verified tender disclosure.",
        "verdict_type": "warning",
        "confidence_items": [
            ("🟢 Verified Fact", "Pipeline dominates primary ore trunk (OCP Annual Report)"),
            ("🟢 Verified Fact", "Rail handles phosphate concentrate flows"),
            ("🟡 Plausible Estimate", "Contractor ecosystem is structurally road-dependent"),
            ("🟡 Plausible Estimate", "800 units/yr HCV procurement estimate"),
            ("🔴 Needs Field Verification", "Specific tender volumes & timing via OCP SupplierPortal"),
        ],
    },
    "ma_tariff": {
        "title": "Morocco 2.5% Tariff Advantage — Sustainable Competitive Moat?",
        "claim": "Morocco's EU Association Agreement confers a **2.5% CBU import tariff** — cited as the lowest in Africa and a decisive advantage for EU-origin vehicles.",
        "cross_validation_items": [
            "**[Fact]** EU–Morocco Association Agreement sets preferential tariff rates confirmed by Direction Générale des Douanes.",
            "**[Complication]** The 2.5% applies to vehicles of EU origin (Rules of Origin). Chinese-built trucks face standard MFN rates (~25%) unless locally assembled.",
            "**[Strategic implication]** Structurally advantages European brands. Chinese players must pursue CKD assembly or third-country EU-FTA routing.",
            "**[Risk]** UK–Morocco post-Brexit continuity agreement is periodically renegotiated.",
        ],
        "verdict": "The 2.5% tariff is origin-conditioned, not a blanket benefit. Chinese CBU entrants face a de facto ~22.5pp tariff disadvantage. The rational China entry strategy is local CKD assembly or a Morocco-based JV.",
        "verdict_type": "warning",
        "confidence_items": [
            ("🟢 Verified Fact", "2.5% tariff for EU-origin vehicles (Douane.gov.ma)"),
            ("🟢 Verified Fact", "Chinese CBU faces ~25% MFN rate"),
            ("🟡 Plausible Estimate", "CKD assembly as optimal China entry route"),
            ("🔴 Needs Field Verification", "Specific CKD partner availability & negotiated terms"),
        ],
    },
    "za_transnet": {
        "title": "Transnet Rail Collapse → Road HCV Demand Transfer — Scissors Effect",
        "claim": "Transnet's operational deterioration has structurally transferred freight to road, creating durable demand uplift of **3,000–5,000 incremental HCV units/year**.",
        "cross_validation_items": [
            "**[Fact]** Transnet Freight Rail volumes declined from **228 Mt (FY2018)** to an estimated **122 Mt (FY2026)** — 46% collapse confirmed in Transnet Annual Reports and Stats SA P7162.",
            "**[Fact]** Stats SA P7162 records rising freight income concurrent with declining payload tonnage.",
            "**[Fact]** NAAMSA 2025 data shows HCV segment resilience outperforming overall automotive market.",
            "**[Critical counter-risk]** Durban Container Terminal concession (initiated 2023) could restore rail competitiveness within 5–8 years.",
            "**[Additional risk]** Private rail operators (Grindrod, Traxtion) entering under open-access policy.",
        ],
        "verdict": "The Transnet modal shift is empirically well-supported by multiple independent data sources. However, consensus systematically underweights rail recovery risk. Stress-test models against a 30–40% rail volume recovery scenario within 5 years.",
        "verdict_type": "warning",
        "confidence_items": [
            ("🟢 Verified Fact", "Transnet volume collapse 228→122 Mt (Transnet Annual Reports)"),
            ("🟢 Verified Fact", "Road freight income growth (Stats SA P7162)"),
            ("🟡 Plausible Estimate", "3,000–5,000 incremental HCV units from modal shift"),
            ("🟡 Plausible Estimate", "Rail recovery via port privatisation (5-yr horizon)"),
            ("🔴 Needs Field Verification", "Private rail operator market share trajectory"),
        ],
    },
    "za_ev_loadshed": {
        "title": "EV Fleet Adoption Under Load-Shedding Constraints",
        "claim": "South Africa's load-shedding will delay commercial EV fleet adoption by **5–10 years**.",
        "cross_validation_items": [
            "**[Fact]** Eskom implemented load-shedding for **335 days in 2023** (Eskom operational reports).",
            "**[Fact]** National EV Strategy (SAIT, 2023) acknowledges grid reliability as primary EV barrier.",
            "**[Nuance]** Large fleet operators deploy behind-the-meter solar + battery systems decoupling depot charging from Eskom grid.",
            "**[Counter-trend]** Eskom FY2025 data shows load-shedding days declining sharply as Kusile Unit 5 and private IPPs come online.",
        ],
        "verdict": "Load-shedding is real but potentially transient. The 5–10 year delay thesis is overstated for captive depot fleets with solar/battery backup. EV strategy should be segmented: depot distribution fleets viable now; long-haul intercity EV remains a 2028+ proposition.",
        "verdict_type": "warning",
        "confidence_items": [
            ("🟢 Verified Fact", "335 load-shedding days in 2023 (Eskom reports)"),
            ("🟡 Plausible Estimate", "Solar depot charging feasibility for captive fleets"),
            ("🟡 Plausible Estimate", "Grid recovery via Kusile + private IPPs"),
            ("🔴 Needs Field Verification", "Long-haul public charging availability & rollout pace"),
        ],
    },
    "za_150pct_tax": {
        "title": "2026 New Energy Manufacturing — 150% Tax Allowance Strategic Pivot",
        "claim": "South Africa's 2026 Budget introduced a **150% accelerated tax deduction** on qualifying NEV manufacturing investment, effective 1 March 2026, capped at R500 million in Year 1.",
        "cross_validation_items": [
            "**[Fact]** National Treasury 2026 Budget Review confirmed Section 12V expansion: 150% first-year deduction on qualifying EV/NEV manufacturing capex, R500m annual cap.",
            "**[Fact]** APDP Phase 2 continues to issue Production Rebate Certificates (PRCs) — a parallel, stackable incentive.",
            "**[Structural implication]** On R500m qualifying investment, 150% deduction generates ~R210m tax saving vs ~R140m under standard deduction — net R70m incremental benefit.",
            "**[Strategic consequence]** Pure CBU importers cannot access the 150% deduction or APDP PRCs.",
            "**[Market validation]** Ford, Toyota, and Isuzu cited the combined 150%/APDP stack as primary driver of 2026–2028 EV localization commitments (Reuters, March 2026).",
        ],
        "verdict": "Pure CBU import will structurally lose competitiveness against locally-assembled competitors capturing the 150% deduction + APDP PRC stack. The long-term commercial moat is CKD/local assembly + APDP enrolment.",
        "verdict_type": "warning",
        "confidence_items": [
            ("🟢 Verified Fact", "150% deduction from 1 March 2026 (National Treasury)"),
            ("🟢 Verified Fact", "APDP Phase 2 PRC stackability confirmed"),
            ("🟡 Plausible Estimate", "R70m incremental tax benefit per R500m qualifying investment"),
            ("🟡 Plausible Estimate", "CBU competitiveness erosion vs local assemblers within 3–5 years"),
            ("🔴 Needs Field Verification", "SARS qualifying asset definition for Chinese CKD assembly lines"),
        ],
    },
    "ng_kd_tariff": {
        "title": "Nigeria Zero-Tariff KD Policy — Durable Incentive or Policy Risk?",
        "claim": "Nigeria's 2023 EV and CKD/SKD zero-tariff policy delivers **~$46,000 per-unit** cost advantage over CBU imports.",
        "cross_validation_items": [
            "**[Fact]** Nigeria Customs Service confirmed 0% import duty on EV commercial vehicles and CKD/SKD kits under 2023 Finance Act amendments.",
            "**[Fact]** NADDC's NAIDP explicitly targets local assembly partnerships as a core strategic pillar.",
            "**[Risk: Policy]** Nigeria has modified automotive tariff policy 3 times in 6 years (2013–2019).",
            "**[Risk: FX]** NGN depreciation >60% since 2022 increases USD cost of KD kits.",
            "**[Operational risk]** NADDC assembly licence approval averaging 18–24 months in practice.",
        ],
        "verdict": "The zero-tariff CKD advantage is legally confirmed and financially material. Structure JVs with USD-indexed kit pricing, multi-year FX forwards, and exit clauses. Realistic net savings after FX: **$28,000–$35,000 per unit**.",
        "verdict_type": "warning",
        "confidence_items": [
            ("🟢 Verified Fact", "0% CKD/EV tariff (2023 Finance Act)"),
            ("🟡 Plausible Estimate", "~$46k gross per-unit saving"),
            ("🟡 Plausible Estimate", "Net saving after FX hedge: ~$28k–$35k"),
            ("🔴 Needs Field Verification", "NADDC licence approval timeline"),
            ("🔴 Needs Field Verification", "Policy stability through 2028"),
        ],
    },
    "eth_ev_mandate": {
        "title": "Ethiopia Petroleum Import Ban — EV Transition Reality vs. Headline",
        "claim": "Ethiopia's 2022 petroleum vehicle import ban will drive EV penetration to **>90% of commercial vehicle sales** by 2025.",
        "cross_validation_items": [
            "**[Fact]** ERCA formally suspended import permits for petroleum vehicles mid-2022.",
            "**[Implementation gap]** Enforcement is uneven; grey market imports via Djibouti and South Sudan documented.",
            "**[Infrastructure constraint]** <120 public EV charging points nationwide; Addis–Djibouti corridor has zero public chargers.",
            "**[Fleet reality]** High EV share reflects new registrations only. Existing ICE fleet of ~80,000 CVs operates for its full economic life.",
            "**[Chinese dominance]** BYD, Foton, King Long collectively >75% of new EV commercial vehicle registrations.",
        ],
        "verdict": "The ban is real; its impact on new registration sales is transformative. However, '90% EV' conflates sales share with operational fleet electrification. Chinese EV brands have genuine first-mover advantage in urban fleets; long-haul requires 3–5 year charging build-out.",
        "verdict_type": "warning",
        "confidence_items": [
            ("🟢 Verified Fact", "Petroleum import ban enacted by ERCA (mid-2022)"),
            ("🟢 Verified Fact", "Chinese brands >75% new EV registrations"),
            ("🟡 Plausible Estimate", "EV new sales share >85% (2025 est.)"),
            ("🟡 Plausible Estimate", "Operational fleet electrification <15%"),
            ("🔴 Needs Field Verification", "Addis–Djibouti EV corridor viability"),
        ],
    },
    "ke_sgr": {
        "title": "Kenya SGR — Road Freight Competitor or Demand Complement?",
        "claim": "The SGR Mombasa–Nairobi line will displace **30–40% of long-haul container freight** from road by 2026.",
        "cross_validation_items": [
            "**[Fact]** SGR freight volumes: 1.2 Mt (2018) → 5.8 Mt (2023) (Kenya Railways Corporation).",
            "**[Fact]** Port of Mombasa container throughput grew concurrently — SGR captured incremental freight.",
            "**[Operational limit]** SGR operates Mombasa–Nairobi only (472 km). Last-mile to Kampala, Kigali, Juba remains road-dependent.",
            "**[Financial distress]** SGR debt to Exim Bank China (~KES 500bn); extension to Uganda stalled.",
        ],
        "verdict": "SGR is a complement to, not substitute for, HCV demand in Kenya. Most Kenyan freight — and all EAC cross-border freight — remains road-dependent.",
        "verdict_type": "success",
        "confidence_items": [
            ("🟢 Verified Fact", "SGR volumes 5.8 Mt 2023 (Kenya Railways)"),
            ("🟢 Verified Fact", "Last-mile beyond Nairobi ICD is road-only"),
            ("🟡 Plausible Estimate", "SGR Uganda extension stalled (debt constraints)"),
            ("🔴 Needs Field Verification", "Net HCV demand displacement quantum from SGR"),
        ],
    },
    "eg_kd": {
        "title": "Egypt KD Assembly 5% Tariff — Realistic Entry Path?",
        "claim": "Egypt's KD assembly preferential tariff (**5% vs 40% CBU**) creates a compelling incentive analogous to the Nigerian model.",
        "cross_validation_items": [
            "**[Fact]** 5% KD rate requires verified local content >40% (Egyptian IDA guidelines).",
            "**[Implementation complexity]** Egypt's CV component supply chain is limited; most qualifying content is tyres, glass, wiring harnesses.",
            "**[Precedent]** GB Auto/MAN Trucks Egypt has navigated KD assembly successfully.",
            "**[FX risk]** EGP devaluation >50% since 2022 compresses margins for local assemblers.",
        ],
        "verdict": "The 5% KD tariff is genuine but the 40% local content threshold requires deliberate supply chain engineering. GB Auto/MAN precedent confirms viability.",
        "verdict_type": "warning",
        "confidence_items": [
            ("🟢 Verified Fact", "5% KD rate requires 40% local content (IDA confirmed)"),
            ("🟢 Verified Fact", "GB Auto/MAN proven assembly precedent"),
            ("🟡 Plausible Estimate", "40% local content achievability for Chinese CV platforms"),
            ("🔴 Needs Field Verification", "Net margin after FX and supply chain costs"),
        ],
    },
    "dz_protect": {
        "title": "Algeria Import Protectionism — Navigable or Structural Barrier?",
        "claim": "Algeria's 30% CBU tariff and import licence quota system make direct CV import commercially unviable.",
        "cross_validation_items": [
            "**[Fact]** Algeria's import licence system (reinstated 2022) creates chronic supply uncertainty.",
            "**[Fact]** Renault Trucks operates a proven JV assembly plant in Rouiba (Algiers).",
            "**[Political dynamic]** JV partners committing to technology transfer receive preferential treatment in public procurement.",
            "**[Risk]** Ministerial-level JV licence approval is opaque; typical timeline 24–36 months.",
        ],
        "verdict": "Algeria is high-barrier but not closed. The Renault Rouiba precedent confirms JV manufacturing partnerships can succeed. Realistic timeline from MOU to first unit production: 3–4 years.",
        "verdict_type": "warning",
        "confidence_items": [
            ("🟢 Verified Fact", "30% CBU tariff + quota system confirmed"),
            ("🟢 Verified Fact", "Renault Rouiba JV as proven entry template"),
            ("🟡 Plausible Estimate", "3–4 year JV setup timeline"),
            ("🔴 Needs Field Verification", "Ministerial approval timeline for Chinese brand JVs"),
        ],
    },
    "tn_ev_policy": {
        "title": "Tunisia 2026 EV Policy Arbitrage — TCO Advantage for Chinese Electric CV",
        "claim": "Tunisia's 2026 Finance Law EV incentives create a structural TCO advantage of **~TND 151,000 per unit** for EV commercial vehicles vs conventional diesel imports.",
        "cross_validation_items": [
            "**[Fact]** Tunisia Loi de Finances 2026: BEV commercial vehicles exempt from customs duty (0%), exempt from Taxe de Consommation (0%), eligible for reduced TVA of 7% (vs standard 19%).",
            "**[Fact]** ANME confirmed TND 10,000 direct subsidy for BEV commercial vehicles registered in Tunisia from January 2026.",
            "**[Fact]** Conventional diesel commercial vehicle (≥12t) subject to: 10% customs duty, 19% TVA, Taxe de Consommation 25% on CIF value.",
            "**[Structural advantage]** On a CIF base price of TND 300,000, all-in tax loading for diesel = ~TND 162,000; for BEV = ~TND 11,000.",
            "**[Market readiness risk]** Tunisia has <50 commercial EV charging points as of early 2026 (STEG data).",
        ],
        "verdict": "The Tunisia 2026 EV policy arbitrage is the most clearly quantifiable policy-driven TCO advantage in North Africa. Key risk is operational charging infrastructure — limiting near-term EV suitability to urban distribution and depot-return routes.",
        "verdict_type": "success",
        "confidence_items": [
            ("🟢 Verified Fact", "0% customs + 0% excise + 7% VAT for BEV (Loi de Finances 2026)"),
            ("🟢 Verified Fact", "TND 10,000 ANME direct subsidy confirmed (January 2026)"),
            ("🟢 Verified Fact", "Diesel CV: 10% duty + 19% TVA + 25% excise (standard regime)"),
            ("🟡 Plausible Estimate", "~TND 151,000 per-unit net tax delta on TND 300k CIF base"),
            ("🟡 Plausible Estimate", "Urban depot-return routes viable with current charging infrastructure"),
            ("🔴 Needs Field Verification", "ANME annual programme budget continuity beyond 2026"),
        ],
    },
    "tn_eu": {
        "title": "Tunisia EU-Aligned Market — Gateway Opportunity or Niche?",
        "claim": "Tunisia's EU Association Agreement and UN-ECE certification mutual recognition make it the easiest African market to enter for EU-compliant commercial vehicles.",
        "cross_validation_items": [
            "**[Fact]** INNORPI confirms UN-ECE mutual recognition — EU type-approved vehicles require no additional homologation.",
            "**[Market size]** ~8,000 units/year total CV market — regulatory ease must be weighed against limited scale economics.",
            "**[Chinese brand challenge]** European brands hold >70% share through decades of network investment.",
            "**[Gateway potential]** Tunisia's EU regulatory alignment could serve as a testbed for EU-spec Chinese CV variants.",
        ],
        "verdict": "Tunisia is easiest to enter but hardest to scale. The 2026 EV policy arbitrage fundamentally changes this calculus — making Tunisia potentially the most commercially attractive immediate entry market for Chinese EV commercial vehicles in North Africa.",
        "verdict_type": "success",
        "confidence_items": [
            ("🟢 Verified Fact", "UN-ECE mutual recognition (INNORPI confirmed)"),
            ("🟢 Verified Fact", "European brands >70% market share"),
            ("🟡 Plausible Estimate", "EV policy arbitrage as primary 2026 entry driver"),
            ("🔴 Needs Field Verification", "Chinese brand dealer network viability at 8,000 unit market"),
        ],
    },

    # ══ NEW · Battle 1 additions — Djibouti / Mauritius / Madagascar ══
    "dj_port_gateway": {
        "title": "Djibouti as Ethiopia's Port Throat — Is Drayage Volume Real or a Transit Mirage?",
        "claim": "Djibouti's commercial vehicle market is dismissed by regional planners as 'too small to matter' (<1,000 CV/yr domestic registrations) — implying no dedicated fleet strategy is warranted.",
        "cross_validation_items": [
            "**[Fact]** Over 95% of landlocked Ethiopia's import/export trade transits the Addis–Djibouti corridor via the Port of Djibouti and Doraleh Multipurpose Port (Djibouti Ports & Free Zones Authority).",
            "**[Fact]** Djibouti operates as a free-zone re-export and drayage hub, not a domestic consumption market — the relevant fleet metric is container-drayage truck-days, not local vehicle registrations.",
            "**[Structural logic]** Short, predictable, high-frequency port-to-railhead / port-to-border drayage runs (Djibouti City ⇄ Ethio-Djibouti Railway terminal, <15km) are the single most EV-friendly duty cycle in the entire 12-market portfolio — fixed routes, fixed hours, depot-return every night.",
            "**[Counter-evidence]** Djibouti's own grid remains partially diesel-generator-backed outside the capital; national household electrification is uneven, though the Doraleh/Djibouti City grid segment (Ethiopia-Djibouti interconnector + Ghoubet geothermal pipeline) is comparatively stable.",
            "**[Risk]** Flat, non-EAC-style import duty regime (~33% effective) makes CBU import expensive regardless of powertrain; Djibouti has no dedicated EV duty carve-out today.",
        ],
        "verdict": "Do not evaluate Djibouti on domestic CV sales volume — evaluate it as a **captive drayage asset serving Ethiopia's entire trade volume**. A depot-charged e-drayage tractor fleet based at Doraleh, running fixed <15km port-to-rail legs, is a defensible pilot even without a broad EV duty incentive, because the route profile itself (not policy) is what makes the TCO work.",
        "verdict_type": "warning",
        "confidence_items": [
            ("🟢 Verified Fact", "Djibouti carries >95% of Ethiopia's seaborne trade (DPFZA)"),
            ("🟢 Verified Fact", "Doraleh Multipurpose Port is the primary container gateway"),
            ("🟡 Plausible Estimate", "Port-to-rail drayage leg is <15km — ideal EV depot-return profile"),
            ("🟡 Plausible Estimate", "~33% flat effective import duty, no EV carve-out yet"),
            ("🔴 Needs Field Verification", "Doraleh grid capacity for a multi-unit overnight EV depot charging load"),
        ],
    },
    "mu_green_island": {
        "title": "Mauritius Green Premium — Does 'Small Island' Mean 'Small Opportunity'?",
        "claim": "Mauritius's total commercial vehicle market (~1,800 units/yr) is too small and too EU-brand-loyal for a Chinese OEM to bother building a dedicated go-to-market motion.",
        "cross_validation_items": [
            "**[Fact]** Mauritius has one of the highest EV penetration rates in Sub-Saharan Africa, driven by a government excise-duty exemption on battery-electric vehicles and a national decarbonisation roadmap targeting 60% renewable electricity by 2030 (Mauritius Ministry of Energy).",
            "**[Fact]** The island's entire road network is under 2,000km, and the longest possible single trip (Port Louis to the furthest resort in the south) is under 60km — structurally eliminating range anxiety as an objection for any commercial EV pitch.",
            "**[Structural logic]** Mauritius's economy is disproportionately weighted toward luxury tourism (resorts, hotel groups) and duty-free/import-export logistics at Port Louis — both are premium, brand-conscious buyers willing to pay for an ESG-forward fleet story that they can put in their own sustainability reports.",
            "**[Counter-evidence]** Absolute unit volumes are tiny in isolation; a Chinese OEM cannot justify a dedicated dealer network on Mauritius volume alone.",
            "**[Strategic logic]** Mauritius functions as a **reference-account market**: a fleet of electric resort shuttle buses or light EV trucks photographed at a 5-star resort is a marketing asset reusable across every other Indian Ocean and mainland tourism-economy pitch.",
        ],
        "verdict": "Mauritius is **not a volume play — it is a showcase play**, structurally similar to Rwanda's EAC-sandbox logic but aimed at the luxury hospitality and green-logistics segment instead of G2G. Fund a small EV resort-shuttle and EV light-truck pilot with 2-3 flagship hotel groups, and reuse the case study across every coastal tourism market on the continent.",
        "verdict_type": "success",
        "confidence_items": [
            ("🟢 Verified Fact", "EV excise duty exemption confirmed (Mauritius Ministry of Energy)"),
            ("🟢 Verified Fact", "Entire island road network <2,000km — no range-anxiety objection"),
            ("🟡 Plausible Estimate", "Resort/hospitality groups as premium early-adopter buyer segment"),
            ("🟡 Plausible Estimate", "Reference-case value transferable to other tourism economies"),
            ("🔴 Needs Field Verification", "Actual hotel-group capex appetite and fleet renewal cycle timing"),
        ],
    },
    "mg_infra_reality": {
        "title": "Madagascar Grid & Road Reality — Why 'Just Sell EVs Everywhere' Fails Here",
        "claim": "Madagascar's poor road infrastructure and mining-sector demand make it a natural candidate for the same EV-led strategy being pursued in Rwanda, Tunisia, and Mauritius.",
        "cross_validation_items": [
            "**[Fact]** Madagascar's national electrification rate is among the lowest in Africa (under 35% even in nominal terms), and grid reliability outside Antananarivo is poor-to-nonexistent — most mining and industrial sites run on captive diesel generation, not grid power (World Bank / JIRAMA data).",
            "**[Fact]** Madagascar's core commercial vehicle demand driver is mining and mineral-export logistics (nickel, cobalt, chromite, graphite, and artisanal/industrial gemstone corridors) running on unpaved or badly maintained roads between inland mine sites and the ports of Toamasina and Tuléar.",
            "**[Structural logic]** Long-haul, high-payload, rough-terrain mining logistics on an unreliable-to-absent grid is the single worst possible use case for battery-electric trucks anywhere in the 12-market portfolio — this is a pure diesel-mining-truck opportunity, not an EV one.",
            "**[Counter-evidence]** A handful of urban Antananarivo distribution routes could theoretically support light EVs if grid-connected depot charging is available, but this is a small, low-priority sub-segment relative to the mining corridor volume.",
            "**[Risk]** Political and currency instability (Ariary volatility, periodic political transitions) adds deal-execution risk on top of the infrastructure risk.",
        ],
        "verdict": "Madagascar should be pitched **diesel mining/haulage trucks exclusively** — rugged, high-payload, low-electronics-complexity ICE trucks suited to unreliable fuel supply chains and zero charging infrastructure. Do not lead with EV messaging here under any circumstances; it will read as out-of-touch with the buyer's operating reality and cost credibility with the mining-sector decision maker.",
        "verdict_type": "warning",
        "confidence_items": [
            ("🟢 Verified Fact", "National electrification rate <35%, grid unreliable outside capital (World Bank/JIRAMA)"),
            ("🟢 Verified Fact", "Core CV demand driver is mining/mineral export logistics, not urban distribution"),
            ("🟡 Plausible Estimate", "Rough/unpaved road network structurally favours rugged diesel platforms"),
            ("🔴 Needs Field Verification", "Specific mine-site fleet renewal timelines and tender processes"),
        ],
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 4. TRIANGULATION RENDERER — strictly single-column, top-to-bottom (Task 1 + 2)
# ══════════════════════════════════════════════════════════════════════════════
def render_triangulation(tri_key: str):
    """
    Renders the three-layer Due Diligence logic in a single vertical column.
    No st.columns are used here by design — long-form text must never sit
    side-by-side with another long-form text block (this was the source of
    the text-overlap bug in earlier versions).
    """
    if tri_key not in TRIANGULATION:
        return
    t = TRIANGULATION[tri_key]

    st.markdown("**① Market Claim &nbsp;/&nbsp; 市场观点**")
    st.markdown(f"> {t['claim']}")
    st.markdown("")

    cv_text = "\n\n".join(f"- {item}" for item in t["cross_validation_items"])
    st.info(f"**② Cross-Validation &nbsp;/&nbsp; 交叉验证**\n\n{cv_text}", icon="🔍")

    conf_lines = "\n".join(f"- {badge} — {label}" for badge, label in t["confidence_items"])
    full_verdict = (
        f"**③ Analyst Verdict &nbsp;/&nbsp; 最终研判**\n\n"
        f"{t['verdict']}\n\n---\n"
        f"**Confidence Assessment:**\n\n{conf_lines}"
    )
    if t["verdict_type"] == "success":
        st.success(full_verdict, icon="✅")
    else:
        st.warning(full_verdict, icon="⚠️")


def render_strategic_action(cdata: dict):
    """
    Level 4 closing element — a single, visually distinct action box that
    converts the Due Diligence verdict into a concrete sales instruction.
    Pulled from cdata['action'], which every Tier 1 country dict defines.
    """
    action = cdata.get("action")
    if not action:
        return
    st.markdown(f"""
<div class="action-box">
    <div class="action-box-title">🎯 Strategic Action / 销售行动指令</div>
    <div style="font-size:.86rem;color:#2D3142;line-height:1.7;">
        {action}
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 5. TIER-1 COUNTRY DATABASE
#    v13.0 schema additions (Battle 1 — Strategic Map Expansion):
#      + Djibouti   (DJ)  — "Ethiopia's Port Throat" · Port Drayage focus
#      + Mauritius  (MU)  — "High-End Green Island"  · Pure-EV LCV & bus focus
#      + Madagascar (MG)  — "Brutal Infrastructure & Mining" · Diesel-only mining trucks
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
        "policy":{
            "tariff":      "CBU EV: 0% (2023–2028). CKD/SKD: 0%. Conventional CBU: 35%.",
            "certification":"SON mandatory; NAFDAC for specialist vehicles; Form M import approval required.",
            "key_buyers":  "Dangote Cement, BUA Group (agri & chemicals), NNPC Logistics Division.",
            "risk":        "NGN/USD depreciation >60% over 18 months. Apapa port congestion: 3–6 week clearance delays.",
        },
        "news_query":"Nigeria commercial vehicle logistics truck EV",
        "tri_keys":["ng_kd_tariff"],
        "sources":{
            "trade":  ("NADDC — National Automotive Design & Development Council","https://naddc.gov.ng"),
            "customs":("Nigeria Customs Service","https://customs.gov.ng"),
            "market": ("Nigeria Trade Hub","https://trade.gov.ng"),
        },
        "tco_params": {
            "ICE_Capex":               95000,
            "EV_Capex":                145000,
            "ICE_Energy_Cost_per_km":  0.42,
            "EV_Energy_Cost_per_km":   0.11,
            "Diesel_Price_per_L":          0.74,
            "ICE_Consumption_L_per_100km": 56.8,
            "Charging_Tariff_per_kWh":     0.12,
            "EV_Consumption_kWh_per_100km":91.7,
            "Monthly_km":              8000,
            "Interest_Rate":           0.24,
            "ICE_Residual_Pct":        0.40,
            "EV_Residual_Pct":         0.15,
            "source_name": "NADDC / Nigeria Customs — Tariff & Fuel Price Modelling 2026",
            "source_url":  "https://naddc.gov.ng",
        },
        "segment_apps": {
            "Urban FMCG (城市快消)":      {"volume": 14200, "ev_readiness": 7.0},
            "Port Drayage (港口倒短)":    {"volume": 9800,  "ev_readiness": 4.5},
            "Long-Haul Mining (长途矿业)":{"volume": 21200, "ev_readiness": 0.9},
        },
        "risk_radar": {
            "FX_Liquidity":        1.5,
            "Tariff_Advantage":    9.0,
            "Port_Efficiency":     3.5,
            "Grid_Stability":      4.0,
            "Policy_Consistency":  4.5,
        },
        "action": (
            "FX liquidity is the binding constraint, not tariffs. Structure all contracts in "
            "<b>USD-denominated CKD kits</b> with a Nigerian assembly partner (capturing the 0% CKD "
            "duty) rather than CBU export — this avoids NGN devaluation risk on the bulk of the deal "
            "value. Target Dangote and BUA Group fleet renewal cycles directly; Apapa port delays make "
            "CKD-Lagos-assembly strictly faster to deliver than CBU import in 2026."
        ),
        "gtm_playbook": {
            "product_matrix": (
                "**Lead SKU: 8t e-LCV** for Lagos/Lagos-Ibadan urban FMCG distribution (Dangote, BUA "
                "depot runs) — this is the only segment where EV readiness (7.0/10) clears the bar. "
                "**Secondary SKU: 18t SKD rigid** assembled locally to capture 0% CKD duty, positioned "
                "against Sinotruk/FAW incumbents on landed cost, not on EV narrative — Nigerian buyers "
                "are price-led, not ESG-led. **Do not lead with EHCV/tractor** (0.9/10 readiness) — "
                "diesel tractors remain the only bankable choice for long-haul mining logistics through 2028."
            ),
            "supply_chain_mode": (
                "**CKD assembly via a Lagos-based JV partner, invoiced in USD.** This is non-negotiable "
                "given NGN's >60% two-year depreciation — any naira-denominated contract erodes margin "
                "faster than the 0% duty saves it. Structure milestone payments in USD with a 90-day FX "
                "forward on the naira-denominated local assembly labour component only. Route CBU spares "
                "and high-value components through Lagos Free Trade Zone to defer duty exposure further."
            ),
            "target_persona": (
                "**Primary:** Group Fleet Director at Dangote Cement / BUA Group — KPI-driven on landed "
                "cost per tonne-km, controls multi-year framework agreements, immune to EV sentiment "
                "pitches. **Secondary:** NNPC Logistics Division procurement lead — long sales cycle "
                "(12-18 months) but framework volumes once won are sticky and FX-insulated via dollar "
                "crude revenue. Avoid SME logistics owners — their FX access is worse than the corporates'."
            ),
        },
    },

    "South Africa": {
        "flag":"🇿🇦","iso":"ZAF","region":"Southern Africa","tier":1,
        "kpi":{
            "Total Vehicle Sales 2025": ("596,818","units (+15.7% YoY)","NAAMSA Full Year 2025","https://naamsa.co.za"),
            "NEV Sales 2025":           ("16,716","units (+7.1% YoY)","BEV+PHEV+HEV combined","https://naamsa.co.za"),
            "HCV Import Tariff":        ("25%","CBU standard","KD assembly ~12%","https://itac.org.za"),
            "Diesel Price":             ("R21.60","/litre","≈ $1.18 USD","https://www.energy.gov.za"),
        },
        "brand_share":{"brands":["Mercedes-Benz","Volvo","MAN","Scania","FAW"],"sales":[7200,6100,5800,5200,3100]},
        "policy":{
            "tariff":      "25% CBU import duty. APDP Phase 2: >50% localisation earns PRCs. From 1 March 2026: 150% accelerated tax deduction on qualifying NEV manufacturing capex (cap R500m/yr).",
            "certification":"NRCS mandatory LoA; Euro 5-equivalent emissions; SABS type approval.",
            "key_buyers":  "Transnet, Imperial Logistics, Tiger Brands distribution, Shoprite supply chain.",
            "risk":        "Load-shedding (declining but not resolved). ZAR/USD ~18.5. Port privatisation may revive rail competitiveness within 5 years.",
        },
        "news_query":"South Africa commercial truck NEV NAAMSA 2025 logistics",
        "tri_keys":["za_transnet","za_ev_loadshed","za_150pct_tax"],
        "sources":{
            "trade":  ("NAAMSA — Automotive Business Council","https://naamsa.co.za"),
            "customs":("ITAC — International Trade Administration Commission","https://itac.org.za"),
            "market": ("National Treasury 2026 Budget Review","https://www.treasury.gov.za"),
        },
        "tco_params": {
            "ICE_Capex":               110000,
            "EV_Capex":                168000,
            "ICE_Energy_Cost_per_km":  0.46,
            "EV_Energy_Cost_per_km":   0.09,
            "Diesel_Price_per_L":          1.18,
            "ICE_Consumption_L_per_100km": 39.0,
            "Charging_Tariff_per_kWh":     0.10,
            "EV_Consumption_kWh_per_100km":90.0,
            "Monthly_km":              9500,
            "Interest_Rate":           0.11,
            "ICE_Residual_Pct":        0.40,
            "EV_Residual_Pct":         0.15,
            "source_name": "NAAMSA / Eskom Tariff Schedule 2026",
            "source_url":  "https://naamsa.co.za",
        },
        "segment_apps": {
            "Urban FMCG (城市快消)":      {"volume": 9600,  "ev_readiness": 6.2},
            "Port Drayage (港口倒短)":    {"volume": 8100,  "ev_readiness": 3.8},
            "Long-Haul Mining (长途矿业)":{"volume": 13000, "ev_readiness": 1.2},
        },
        "risk_radar": {
            "FX_Liquidity":        6.5,
            "Tariff_Advantage":    4.0,
            "Port_Efficiency":     5.0,
            "Grid_Stability":      4.5,
            "Policy_Consistency":  7.0,
        },
        "action": (
            "Lead with the <b>150% tax deduction + APDP PRC stack</b> — this is the only durable moat "
            "in this market. Do not pitch CBU export as a long-term strategy; pitch a <b>local assembly "
            "JV</b> structured to qualify for both incentives before the 1 March 2026 deadline. Target "
            "Transnet and Imperial Logistics for the Gauteng-corridor depot fleets where Eskom grid "
            "reliability already supports overnight EV charging."
        ),
        "gtm_playbook": {
            "product_matrix": (
                "**Lead SKU: 12t SKD rigid for Gauteng depot distribution** — Eskom grid reliability in "
                "the metro corridor and APDP-qualifying local content make this the most defensible "
                "near-term play. **Secondary SKU: 8t e-LCV for urban FMCG** (Shoprite/Tiger Brands depot "
                "loops, 6.2/10 readiness) — overnight charging fits existing depot operating hours. "
                "**Do not lead with long-haul EHCV/tractor** (1.2/10 readiness) — Transnet's rail "
                "collapse is creating road HCV demand, but that demand is diesel demand, not EV demand, "
                "given inter-provincial charging infrastructure gaps."
            ),
            "supply_chain_mode": (
                "<b>2026年3月后全面转向本地SKD以获取150%抵税与APDP退税</b> — from 1 March 2026, structure "
                "100% of new South African volume as locally-assembled SKD to simultaneously capture the "
                "150% Section 12V tax deduction (R500m annual cap) and APDP Phase 2 Production Rebate "
                "Certificates. Pure CBU import after this date forfeits both incentives and concedes "
                "structural cost advantage to any competitor who localises. Pricing should be quoted "
                "ZAR-denominated with quarterly FX reset clauses tied to ZAR/USD ~18.5 reference."
            ),
            "target_persona": (
                "**Primary:** Transnet Freight Rail / Imperial Logistics Fleet Procurement Director — "
                "actively seeking road HCV capacity to offset the 46% rail volume collapse since 2018, "
                "decision authority sits at GM level for multi-year framework deals. **Secondary:** "
                "Shoprite/Tiger Brands Supply Chain VP — depot-based urban fleets, EV-receptive given "
                "ESG reporting pressure from JSE-listed parent, but price-sensitive on TCO payback period."
            ),
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
        "policy":{
            "tariff":      "EU AA Agreement: EU-origin CBU 2.5%. Chinese CBU: ~25% MFN. No dedicated KD incentive.",
            "certification":"CNEAT: UN-ECE mutual recognition. EU type-approved vehicles: fast-track.",
            "key_buyers":  "OCP Group (phosphate mining), ONCF (national rail logistics), Casablanca Port operators.",
            "risk":        "Origin rules limit 2.5% to EU-origin only. Chinese CBU at structural tariff disadvantage.",
        },
        "news_query":"Maroc transport logistique camions OCP fret",
        "tri_keys":["ma_ocp_modal","ma_tariff"],
        "sources":{
            "trade":  ("AIVAM — Association des Importateurs de Véhicules au Maroc","http://www.aivam.ma"),
            "customs":("Direction Générale des Douanes","https://www.douane.gov.ma"),
            "market": ("CNEAT — Centre National d'Essais et d'Homologation","https://www.cneat.ma"),
        },
        "tco_params": {
            "ICE_Capex":               92000,
            "EV_Capex":                139000,
            "ICE_Energy_Cost_per_km":  0.38,
            "EV_Energy_Cost_per_km":   0.10,
            "Diesel_Price_per_L":          1.34,
            "ICE_Consumption_L_per_100km": 28.4,
            "Charging_Tariff_per_kWh":     0.11,
            "EV_Consumption_kWh_per_100km":90.9,
            "Monthly_km":              7800,
            "Interest_Rate":           0.06,
            "ICE_Residual_Pct":        0.42,
            "EV_Residual_Pct":         0.15,
            "source_name": "AIVAM / ONHYM Energy Price Bulletin 2026",
            "source_url":  "http://www.aivam.ma",
        },
        "segment_apps": {
            "Urban FMCG (城市快消)":      {"volume": 5400, "ev_readiness": 5.8},
            "Port Drayage (港口倒短)":    {"volume": 5800, "ev_readiness": 4.2},
            "Long-Haul Mining (长途矿业)":{"volume": 7200, "ev_readiness": 1.1},
        },
        "risk_radar": {
            "FX_Liquidity":        7.5,
            "Tariff_Advantage":    7.0,
            "Port_Efficiency":     7.5,
            "Grid_Stability":      6.5,
            "Policy_Consistency":  8.0,
        },
        "action": (
            "Chinese CBU cannot win on tariff — the 2.5% EU-origin rate is structurally closed to "
            "non-EU brands. Pitch a <b>CKD assembly JV</b> co-located near Casablanca Port to access the "
            "2.5% rate via local content rules, and target OCP Group's contractor fleet (road-accessible "
            "segment only — not the slurry pipeline trunk) as the anchor reference customer."
        ),
        "gtm_playbook": {
            "product_matrix": (
                "**Lead SKU: 18t SKD rigid for OCP contractor logistics** — targets the road-accessible "
                "segment of phosphate logistics (finished fertiliser, reagent supply, equipment "
                "mobilisation) explicitly excluded from OCP's slurry pipeline and rail trunk. "
                "**Secondary SKU: 8t e-LCV for Casablanca urban distribution** (5.8/10 readiness) — "
                "best positioned against incumbent Renault Trucks/Mercedes on landed cost once local "
                "content qualifies for the 2.5% EU-equivalent rate. **EHCV/tractor remains a European "
                "brand stronghold** (>65% share) — do not contest this segment head-on; win share "
                "through OCP contractor relationships instead."
            ),
            "supply_chain_mode": (
                "CKD assembly JV co-located in the Casablanca-Tangier industrial corridor, structured to "
                "meet Rules of Origin thresholds under the EU Association Agreement — this is the only "
                "path to the 2.5% tariff for a Chinese-brand vehicle, since direct CBU import faces the "
                "~25% MFN rate with no local content offset. Price in MAD with EUR-indexed input cost "
                "pass-through, since the EU AA Agreement anchors Morocco's trade pricing norms to euro "
                "benchmarks even though the local currency is MAD."
            ),
            "target_persona": (
                "**Primary:** OCP Group Procurement & Logistics Director — controls the largest single "
                "fleet decision in the market (~800 units/yr estimated, unverified against tender data), "
                "values supplier relationships measured in decades, not quarters. **Secondary:** "
                "Tier-1 OCP contractor GMs (CBI, Snef, Cofely) — faster sales cycle than OCP direct, "
                "serve as the practical entry point while building the OCP direct relationship."
            ),
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
        "policy":{
            "tariff":      "CBU: 40%. KD (>40% local content): 5%. SCZone production: 0%.",
            "certification":"EOS mandatory; GOEIC import licence; SCZone simplified clearance.",
            "key_buyers":  "EGPC logistics, SCZone contractors, building materials distributors.",
            "risk":        "EGP depreciated >50% in 2 years; FX controls delay payments 45–90 days.",
        },
        "news_query":"Egypt commercial vehicle logistics Suez Zone truck",
        "tri_keys":["eg_kd"],
        "sources":{
            "trade":  ("EOS — Egyptian Organisation for Standardisation","https://www.eos.org.eg"),
            "customs":("GOEIC — General Organisation for Export & Import Control","https://www.goeic.gov.eg"),
            "market": ("IDSC — Information and Decision Support Center","https://www.idsc.gov.eg"),
        },
        "tco_params": {
            "ICE_Capex":               78000,
            "EV_Capex":                132000,
            "ICE_Energy_Cost_per_km":  0.10,
            "EV_Energy_Cost_per_km":   0.07,
            "Diesel_Price_per_L":          0.20,
            "ICE_Consumption_L_per_100km": 50.0,
            "Charging_Tariff_per_kWh":     0.06,
            "EV_Consumption_kWh_per_100km":116.7,
            "Monthly_km":              7200,
            "Interest_Rate":           0.20,
            "ICE_Residual_Pct":        0.38,
            "EV_Residual_Pct":         0.12,
            "source_name": "EOS / Egypt Ministry of Petroleum Subsidised Fuel Schedule 2026",
            "source_url":  "https://www.mop.gov.eg",
        },
        "segment_apps": {
            "Urban FMCG (城市快消)":      {"volume": 7200, "ev_readiness": 3.2},
            "Port Drayage (港口倒短)":    {"volume": 8400, "ev_readiness": 2.0},
            "Long-Haul Mining (长途矿业)":{"volume": 10200,"ev_readiness": 0.5},
        },
        "risk_radar": {
            "FX_Liquidity":        2.5,
            "Tariff_Advantage":    5.0,
            "Port_Efficiency":     5.5,
            "Grid_Stability":      5.5,
            "Policy_Consistency":  5.0,
        },
        "action": (
            "Subsidised diesel (EGP 9.75/L) makes EV TCO uncompetitive without a KD tariff play. "
            "Pitch <b>SCZone-based KD assembly</b> (0% production tariff) targeting EGPC logistics "
            "contracts, and insist on EGP-indexed pricing with quarterly FX reset clauses — do not "
            "accept fixed EGP pricing given 45-90 day payment delays under current FX controls."
        ),
        "gtm_playbook": {
            "product_matrix": (
                "**Lead SKU: 18t KD rigid for SCZone construction logistics** — this is a tariff-arbitrage "
                "play, not an EV play, given EGP 9.75/L subsidised diesel makes ICE structurally cheap to "
                "run. **Secondary SKU: 8t e-LCV for Cairo urban FMCG** (3.2/10 readiness — the best "
                "available segment, still thin) — only viable for depot-return operators with captive "
                "charging, not as a broad market push. **Avoid EHCV/tractor entirely** (0.5/10 readiness) "
                "— subsidised diesel plus FX constraints make this the least defensible segment in the "
                "entire portfolio."
            ),
            "supply_chain_mode": (
                "KD assembly inside the Suez Canal Economic Zone (SCZone) to access the 0% production "
                "tariff, modelled on the GB Auto / MAN Trucks Egypt precedent — local content must exceed "
                "40% to qualify, which requires sourcing tyres, glass, and wiring harnesses domestically "
                "since Egypt's CV component supply chain cannot support deeper localisation yet. Price in "
                "USD with quarterly EGP conversion at spot rate, and build a 60-90 day payment delay "
                "buffer into cash flow planning given FX controls — do not extend open credit terms."
            ),
            "target_persona": (
                "**Primary:** EGPC Logistics Division Procurement Manager — state-owned, FX-insulated via "
                "dollar oil revenue, slower decision cycle but contracts are durable once signed. "
                "**Secondary:** SCZone-based construction contractor Operations Director — actively "
                "seeking KD-assembled fleet to support Suez Canal economic zone build-out, more "
                "commercially agile than EGPC but exposed to the same EGP payment delay risk."
            ),
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
        "policy":{
            "tariff":      "EAC CET: 25%. COMESA: 0%. EV: currently 25% (policy review underway).",
            "certification":"KEBS mandatory PVoC at origin; NTSA inspection on arrival.",
            "key_buyers":  "Kenya Ports Authority, East African Breweries, Bamburi Cement, SGR feeder.",
            "risk":        "KES depreciation ~20% (2023–24); SGR competition on Mombasa–Nairobi corridor.",
        },
        "news_query":"Kenya commercial vehicle logistics freight Mombasa Nairobi EAC",
        "tri_keys":["ke_sgr"],
        "sources":{
            "trade":  ("KEBS — Kenya Bureau of Standards","https://kebs.org"),
            "customs":("KRA — Kenya Revenue Authority","https://kra.go.ke"),
            "market": ("EPRA — Energy & Petroleum Regulatory Authority","https://www.epra.go.ke"),
        },
        "tco_params": {
            "ICE_Capex":               74000,
            "EV_Capex":                118000,
            "ICE_Energy_Cost_per_km":  0.39,
            "EV_Energy_Cost_per_km":   0.13,
            "Diesel_Price_per_L":          1.42,
            "ICE_Consumption_L_per_100km": 27.5,
            "Charging_Tariff_per_kWh":     0.14,
            "EV_Consumption_kWh_per_100km":92.9,
            "Monthly_km":              6800,
            "Interest_Rate":           0.16,
            "ICE_Residual_Pct":        0.40,
            "EV_Residual_Pct":         0.14,
            "source_name": "EPRA Fuel Price Bulletin / KEBS 2026",
            "source_url":  "https://www.epra.go.ke",
        },
        "segment_apps": {
            "Urban FMCG (城市快消)":      {"volume": 4800, "ev_readiness": 4.8},
            "Port Drayage (港口倒短)":    {"volume": 4400, "ev_readiness": 3.5},
            "Long-Haul Mining (长途矿业)":{"volume": 5000, "ev_readiness": 0.7},
        },
        "risk_radar": {
            "FX_Liquidity":        4.5,
            "Tariff_Advantage":    4.5,
            "Port_Efficiency":     5.5,
            "Grid_Stability":      6.0,
            "Policy_Consistency":  6.0,
        },
        "action": (
            "Mombasa Port drayage is the highest near-term EV-readiness segment (3.5/10, but best in "
            "this market) given short, predictable routes. Target <b>Kenya Ports Authority</b> directly "
            "for a depot-charging pilot before committing to long-haul SGR-feeder routes, where diesel "
            "still dominates structurally."
        ),
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
        "policy":{
            "tariff":      "Petroleum vehicle imports BANNED (2022). EV: 0% duty.",
            "certification":"EthSA; EV charging under national grid expansion.",
            "key_buyers":  "Ethiopian Roads Authority, Ethiopian Airlines cargo, Ethio Telecom fleet.",
            "risk":        "<120 public chargers nationwide; Addis–Djibouti corridor has zero public chargers.",
        },
        "news_query":"Ethiopia EV commercial vehicle petroleum ban transport Addis",
        "tri_keys":["eth_ev_mandate"],
        "sources":{
            "trade":  ("MoTI — Ministry of Trade & Industry Ethiopia","https://www.moti.gov.et"),
            "customs":("ERCA — Ethiopian Revenue & Customs Authority","https://www.erca.gov.et"),
            "market": ("EthSA — Ethiopian Standards Agency","https://www.ethsa.gov.et"),
        },
        "tco_params": {
            "ICE_Capex":               68000,
            "EV_Capex":                102000,
            "ICE_Energy_Cost_per_km":  0.0,
            "EV_Energy_Cost_per_km":   0.02,
            "Diesel_Price_per_L":          0.83,
            "ICE_Consumption_L_per_100km": 0.0,
            "Charging_Tariff_per_kWh":     0.025,
            "EV_Consumption_kWh_per_100km":80.0,
            "Monthly_km":              6200,
            "Interest_Rate":           0.18,
            "ICE_Residual_Pct":        0.35,
            "EV_Residual_Pct":         0.16,
            "source_name": "ERCA Import Ban Notice / EEPCO Tariff Schedule 2026",
            "source_url":  "https://www.erca.gov.et",
        },
        "segment_apps": {
            "Urban FMCG (城市快消)":      {"volume": 3400, "ev_readiness": 8.5},
            "Port Drayage (港口倒短)":    {"volume": 2600, "ev_readiness": 6.0},
            "Long-Haul Mining (长途矿业)":{"volume": 3800, "ev_readiness": 2.0},
        },
        "risk_radar": {
            "FX_Liquidity":        2.0,
            "Tariff_Advantage":    9.5,
            "Port_Efficiency":     4.0,
            "Grid_Stability":      5.5,
            "Policy_Consistency":  5.5,
        },
        "action": (
            "ICE imports are simply illegal — there is no fuel-cost comparison to make, only a sales "
            "execution question. Move fast on <b>Urban FMCG fleets</b> (8.5/10 readiness, Addis Ababa "
            "depot routes) before competitors saturate the market; avoid Addis–Djibouti long-haul "
            "until charging infrastructure is confirmed beyond the capital."
        ),
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
        "policy":{
            "tariff":      "30% CBU. CKD JV partnerships permitted; Renault Rouiba JV as template.",
            "certification":"IANOR; Euro 3 minimum (Euro 4 upgrade underway).",
            "key_buyers":  "Sonatrach (oil & gas), SNVI, Ministry of Public Works.",
            "risk":        "Import quotas; FX controls; JV licence approval 24–36 months.",
        },
        "news_query":"Algérie transport logistique camions Sonatrach véhicule commercial",
        "tri_keys":["dz_protect"],
        "sources":{
            "trade":  ("Ministère du Commerce — Algeria","https://www.commerce.gov.dz"),
            "customs":("Direction Générale des Douanes","https://www.douane.gov.dz"),
            "market": ("IANOR — Institut Algérien de Normalisation","https://www.ianor.dz"),
        },
        "tco_params": {
            "ICE_Capex":               85000,
            "EV_Capex":                136000,
            "ICE_Energy_Cost_per_km":  0.07,
            "EV_Energy_Cost_per_km":   0.06,
            "Diesel_Price_per_L":          0.33,
            "ICE_Consumption_L_per_100km": 21.2,
            "Charging_Tariff_per_kWh":     0.065,
            "EV_Consumption_kWh_per_100km":92.3,
            "Monthly_km":              6500,
            "Interest_Rate":           0.09,
            "ICE_Residual_Pct":        0.40,
            "EV_Residual_Pct":         0.12,
            "source_name": "Ministère de l'Energie — Subsidised Diesel Schedule 2026",
            "source_url":  "https://www.energy.gov.dz",
        },
        "segment_apps": {
            "Urban FMCG (城市快消)":      {"volume": 4200, "ev_readiness": 2.2},
            "Port Drayage (港口倒短)":    {"volume": 3600, "ev_readiness": 1.5},
            "Long-Haul Mining (长途矿业)":{"volume": 4800, "ev_readiness": 0.3},
        },
        "risk_radar": {
            "FX_Liquidity":        2.5,
            "Tariff_Advantage":    3.0,
            "Port_Efficiency":     3.5,
            "Grid_Stability":      6.5,
            "Policy_Consistency":  3.5,
        },
        "action": (
            "Subsidised diesel and FX controls make this a long-game market only. Do not pursue CBU "
            "export — pursue a <b>state-endorsed JV</b> modelled on Renault's Rouiba plant, with a "
            "3-4 year horizon to first production. Defer EV positioning entirely until charging "
            "infrastructure and FX liquidity improve."
        ),
    },

    "Tunisia": {
        "flag":"🇹🇳","iso":"TUN","region":"North Africa","tier":1,
        "kpi":{
            "Annual CV Sales":   ("8,100","units/yr","+3.1% YoY","https://www.innorpi.tn"),
            "EV Policy Saving":  ("~TND 151k","/unit vs diesel import","Loi de Finances 2026","https://www.finances.gov.tn"),
            "EV Import Tariff":  ("0%","BEV (was 10%)","+ 0% excise + 7% VAT","https://www.douane.gov.tn"),
            "ANME EV Subsidy":   ("TND 10,000","direct subsidy/vehicle","ANME 2026 programme","https://www.anme.tn"),
        },
        "brand_share":{"brands":["Mercedes-Benz","Renault Trucks","MAN","Volvo","Sinotruk"],"sales":[2100,1800,1500,1200,900]},
        "policy":{
            "tariff":      "Diesel CV (≥12t): 10% customs + 19% TVA + 25% taxe de consommation. BEV: 0% customs + 0% excise + 7% TVA + TND 10,000 ANME subsidy (Loi de Finances 2026).",
            "certification":"INNORPI; ATTT road transport authority; UN-ECE mutual recognition with EU.",
            "key_buyers":  "CPG (phosphates), Délice Danone (FMCG), Aramex Tunisia (parcels), Port de Tunis logistics.",
            "risk":        "<50 commercial EV charging points nationwide (STEG 2026). Annual ANME budget continuity beyond 2026 not guaranteed.",
        },
        "news_query":"Tunisie transport logistique camion électrique véhicule commercial fret 2026",
        "tri_keys":["tn_ev_policy","tn_eu"],
        "sources":{
            "trade":  ("INNORPI — Institut National de la Normalisation","https://www.innorpi.tn"),
            "customs":("Direction Générale des Douanes — Tunisie","https://www.douane.gov.tn"),
            "market": ("ANME — Agence Nationale pour la Maîtrise de l'Énergie","https://www.anme.tn"),
            "finance":("Ministère des Finances — Loi de Finances 2026","https://www.finances.gov.tn"),
        },
        "tco_params": {
            "ICE_Capex":               95000,
            "EV_Capex":                99000,
            "ICE_Energy_Cost_per_km":  0.32,
            "EV_Energy_Cost_per_km":   0.08,
            "Diesel_Price_per_L":          0.92,
            "ICE_Consumption_L_per_100km": 34.8,
            "Charging_Tariff_per_kWh":     0.09,
            "EV_Consumption_kWh_per_100km":88.9,
            "Monthly_km":              6000,
            "Interest_Rate":           0.08,
            "ICE_Residual_Pct":        0.40,
            "EV_Residual_Pct":         0.16,
            "ANME_Subsidy_TND":        10000,
            "EV_VAT_Pct":              0.07,
            "source_name": "Loi de Finances 2026 / ANME e-Mobility Programme",
            "source_url":  "https://www.finances.gov.tn",
        },
        "segment_apps": {
            "Urban FMCG (城市快消)":      {"volume": 2800, "ev_readiness": 8.0},
            "Port Drayage (港口倒短)":    {"volume": 2400, "ev_readiness": 5.5},
            "Long-Haul Mining (长途矿业)":{"volume": 2900, "ev_readiness": 1.0},
        },
        "risk_radar": {
            "FX_Liquidity":        4.0,
            "Tariff_Advantage":    9.5,
            "Port_Efficiency":     6.0,
            "Grid_Stability":      6.5,
            "Policy_Consistency":  6.5,
        },
        "action": (
            "The TND 151,000 per-unit tax delta is the single strongest B2B argument in North Africa — "
            "lead every sales conversation with this number. Target <b>Délice Danone</b> and <b>Aramex "
            "Tunisia</b> for urban depot fleets first; defer phosphate corridor (Gafsa) pitches until "
            "STEG confirms charging infrastructure beyond the Tunis–Sousse corridor."
        ),
        "gtm_playbook": {
            "product_matrix": (
                "**Lead SKU: 8t e-LCV for Tunis urban FMCG** (Délice Danone, SOTUMAG depot routes — "
                "8.0/10 readiness, the best score in the entire portfolio) — the TND 151,000 "
                "tax delta makes this nearly impossible to lose on price alone. **Secondary SKU: 12t "
                "rigid for Tunis–Sousse port drayage** (5.5/10 readiness) — short predictable routes "
                "suit current charging infrastructure. **Defer EHCV/tractor for Gafsa phosphate corridor** "
                "(1.0/10 readiness) until STEG's 200-charger 2026 rollout plan is confirmed beyond "
                "announcement stage — do not commit inventory against an unconfirmed infrastructure timeline."
            ),
            "supply_chain_mode": (
                "<b>0% 关税 + 0% 消费税 + 7% 增值税 + TND 10,000 ANME 政府补贴</b> 全套组合是北非地区最强的政策套利窗口 — "
                "import as BEV CBU directly (no CKD assembly needed here, unlike ZA/NG/MA) to capture the "
                "full Loi de Finances 2026 exemption stack immediately. Quote in TND with the ANME subsidy "
                "deducted at point of sale to maximise the visible price advantage in the customer's eyes "
                "rather than as a rebate — this materially changes how the deal feels to a price-anchored buyer."
            ),
            "target_persona": (
                "**Primary:** Délice Danone Tunisie Fleet & Logistics Director — FMCG depot fleet, EU "
                "parent company under ESG pressure to electrify, Tunis-based with full charging "
                "infrastructure access. **Secondary:** Aramex Tunisia Country Operations Manager — "
                "urban last-mile parcels, fast decision cycle, MENA regional fleet standards mean a Tunisia "
                "win can become a regional reference case."
            ),
        },
    },

    "Rwanda": {
        "flag":"🇷🇼","iso":"RWA","region":"East Africa (EAC)","tier":1,
        "kpi":{
            "Annual CV Sales":       ("~3,200","units/yr","+12.5% YoY","https://www.rdb.rw"),
            "EV Penetration (CVs)":  ("~6.2%","of new CV registrations","+3.1pp YoY","https://www.rura.rw"),
            "EV Import Tariff":      ("0%","EAC Pioneer — 0% Duty + 0% VAT","Most generous in Sub-Sahara","https://www.rra.gov.rw"),
            "e-Mobility Electricity":("RWF 115","/kWh (RURA e-mobility tariff)","vs RWF 1,600/L diesel","https://www.rura.rw"),
        },
        "brand_share":{
            "brands":["Toyota","Isuzu","Foton","BYD EV","Yutong EV"],
            "sales": [980, 720, 480, 310, 220],
        },
        "policy":{
            "tariff":      "EAC Pioneer: 0% import duty + 0% VAT on all EV commercial vehicles (RDB Investment Code 2024). ICE CVs: 25% EAC CET + 18% VAT. Corporate income tax for qualifying EV enterprises: 15% (vs standard 30%).",
            "certification":"Rwanda Standards Board (RSB) mandatory type-approval; RURA e-mobility operator licence for fleet charging; EAC CoC accepted.",
            "key_buyers":  "Kigali Bus Services (KBS), RwandAir cargo, BRALIRWA (Heineken) distribution, MTN Rwanda fleet, La Colombière construction logistics.",
            "risk":        "Market volume cap (~5,000 CVs/yr through 2030). Charging infrastructure outside Kigali limited. RWF/USD stability depends on foreign aid inflows.",
        },
        "news_query":"Rwanda Kigali electric vehicle commercial transport e-mobility EV bus",
        "tri_keys":["rw_sandbox","rw_eac_gateway"],
        "sources":{
            "trade":   ("RDB — Rwanda Development Board","https://www.rdb.rw"),
            "customs": ("RRA — Rwanda Revenue Authority","https://www.rra.gov.rw"),
            "market":  ("RURA — Rwanda Utilities Regulatory Authority","https://www.rura.rw"),
            "energy":  ("REG — Rwanda Energy Group","https://www.reg.rw"),
        },
        "tco_params": {
            "ICE_Capex":               80000,
            "EV_Capex":                108000,
            "ICE_Energy_Cost_per_km":  0.40,
            "EV_Energy_Cost_per_km":   0.0739,
            "Diesel_Price_per_L":          1.143,
            "ICE_Consumption_L_per_100km": 35.0,
            "Charging_Tariff_per_kWh":     0.0821,
            "EV_Consumption_kWh_per_100km":90.0,
            "Monthly_km":              6700,
            "Interest_Rate":           0.13,
            "ICE_Residual_Pct":        0.40,
            "EV_Residual_Pct":         0.17,
            "EAC_Import_Duty_Pct":     0.0,
            "Kigali_Electricity_RWF_per_kWh": 115,
            "source_name": "RURA e-Mobility Tariff Order 2023 / RDB Investment Incentives 2024",
            "source_url":  "https://www.rura.rw",
        },
        "segment_apps": {
            "Urban FMCG (城市快消)":      {"volume": 1300, "ev_readiness": 9.0},
            "Port Drayage (港口倒短)":    {"volume": 700,  "ev_readiness": 6.5},
            "Long-Haul Mining (长途矿业)":{"volume": 1200, "ev_readiness": 1.8},
        },
        "risk_radar": {
            "FX_Liquidity":        5.0,
            "Tariff_Advantage":    10.0,
            "Port_Efficiency":     6.5,
            "Grid_Stability":      9.5,
            "Policy_Consistency":  9.0,
        },
        "action": (
            "Do not chase volume here — chase <b>proof-of-concept</b>. Propose a 20-50 unit G2G electric "
            "bus pilot with <b>Kigali Bus Services</b>, fully financed against the 0% duty + 15% CIT "
            "stack, and use the resulting performance data as the reference case for EAC-wide tenders "
            "in Kenya and Tanzania within 18 months."
        ),
        "gtm_playbook": {
            "product_matrix": (
                "**Lead SKU: Electric bus for Kigali Bus Services G2G pilot** (9.0/10 readiness, the "
                "highest EV readiness score across all markets and all 3 segments) — Rwanda's grid "
                "reliability (<2% outage) and RURA's RWF 115/kWh e-mobility tariff make this the single "
                "most de-risked EV deployment in the entire portfolio. **Secondary SKU: 8t e-LCV for "
                "BRALIRWA/MTN Rwanda urban distribution** (6.5/10 readiness) — depot-based, fits within "
                "Kigali's emerging charging network. **Long-haul mining/construction remains diesel** "
                "(1.8/10 readiness) — La Colombière and similar contractors should be quoted ICE, not EV."
            ),
            "supply_chain_mode": (
                "<b>0% EAC关税 + 0% 增值税 + 15%企业所得税(较标准30%大幅优惠)</b> 构成全非洲最激进的EV财政组合 — "
                "import as CBU directly through the EAC Pioneer EV exemption (no local assembly needed to "
                "access the incentive, unlike Nigeria/South Africa/Morocco). Structure the deal as a "
                "leasing or G2G financing arrangement rather than an outright municipal purchase, since "
                "Kigali Bus Services' budget cycle favours opex-style financing — this also lets the 15% "
                "CIT rate apply if the financing vehicle is structured as a qualifying Rwandan EV enterprise."
            ),
            "target_persona": (
                "**Primary:** City of Kigali / Kigali Bus Services Transport Directorate — G2G "
                "procurement framework, RDB-endorsed pilots receive expedited approval, low absolute "
                "deal size but outsized reference value across the EAC. **Secondary:** BRALIRWA "
                "(Heineken Rwanda) Supply Chain Director — multinational parent under group-level ESG "
                "mandate, Kigali depot operations are the most charging-infrastructure-ready fleet "
                "segment outside the G2G bus programme."
            ),
        },
    },

    "Djibouti": {
        "flag":"🇩🇯","iso":"DJI","region":"East Africa (Horn)","tier":1,
        "kpi":{
            "Port Transit Share":   ("~95%","of Ethiopia trade via DJ","Djibouti Ports & FZ Authority","https://www.dpfza.gov.dj"),
            "Annual CV Sales":      ("~1,400","units/yr (domestic + drayage fleet)","+7.8% YoY","https://www.commerce.gouv.dj"),
            "CBU Import Duty":      ("~33%","flat effective rate","No EV carve-out yet","https://www.douanes.dj"),
            "Diesel Price":         ("DJF 210","/litre","≈ $1.18 USD","https://www.energie.gouv.dj"),
        },
        "brand_share":{"brands":["Sinotruk","Isuzu","Mercedes-Benz","Foton","Volvo"],"sales":[420,310,260,240,170]},
        "policy":{
            "tariff":      "Flat ~33% effective CBU import duty (no differentiated EV rate today). Free-zone re-export cargo is duty-exempt but the drayage tractor fleet itself is not.",
            "certification":"Djibouti Ministry of Commerce vehicle registration; port operator (SGTD/DP World Djibouti) equipment pre-qualification for terminal access.",
            "key_buyers":  "Djibouti Ports & Free Zones Authority (DPFZA), SGTD (Société de Gestion du Terminal à Conteneurs de Doraleh), Ethio-Djibouti Railway freight partners, Ethiopian Shipping & Logistics Services Enterprise (ESLSE).",
            "risk":        "Grid capacity outside Djibouti City/Doraleh is thin; regional geopolitical volatility (Horn of Africa); Ethiopia-Djibouti relationship is the single point of failure for all volume.",
        },
        "news_query":"Djibouti port logistics Ethiopia corridor truck freight",
        "tri_keys":["dj_port_gateway"],
        "sources":{
            "trade":  ("DPFZA — Djibouti Ports & Free Zones Authority","https://www.dpfza.gov.dj"),
            "customs":("Direction des Douanes de Djibouti","https://www.douanes.dj"),
            "market": ("Ministère du Commerce — Djibouti","https://www.commerce.gouv.dj"),
        },
        "tco_params": {
            "ICE_Capex":               88000,
            "EV_Capex":                132000,
            "ICE_Energy_Cost_per_km":  0.41,
            "EV_Energy_Cost_per_km":   0.10,
            "Diesel_Price_per_L":          1.18,
            "ICE_Consumption_L_per_100km": 34.7,
            "Charging_Tariff_per_kWh":     0.115,
            "EV_Consumption_kWh_per_100km":87.0,
            "Monthly_km":              4200,
            "Interest_Rate":           0.14,
            "ICE_Residual_Pct":        0.38,
            "EV_Residual_Pct":         0.14,
            "source_name": "DPFZA Tariff Schedule / Djibouti Ministry of Energy 2026",
            "source_url":  "https://www.dpfza.gov.dj",
        },
        "segment_apps": {
            "Urban FMCG (城市快消)":      {"volume": 300,  "ev_readiness": 4.0},
            "Port Drayage (港口倒短)":    {"volume": 5200, "ev_readiness": 7.8},
            "Long-Haul Mining (长途矿业)":{"volume": 150,  "ev_readiness": 0.4},
        },
        "risk_radar": {
            "FX_Liquidity":        6.0,
            "Tariff_Advantage":    3.5,
            "Port_Efficiency":     8.0,
            "Grid_Stability":      5.5,
            "Policy_Consistency":  5.5,
        },
        "action": (
            "Do not sell into Djibouti as a domestic market — sell into it as a <b>captive port-drayage "
            "asset serving 100% of Ethiopia's seaborne trade</b>. Pilot a small depot-charged e-drayage "
            "tractor fleet at Doraleh running fixed &lt;15km port-to-rail legs (highest EV readiness "
            "segment in this market at 7.8/10), and use DPFZA/SGTD as the anchor account rather than "
            "chasing thin domestic CBU volume."
        ),
        "gtm_playbook": {
            "product_matrix": (
                "**Lead SKU: e-Drayage tractor for Doraleh port-to-rail short-haul** (7.8/10 readiness — "
                "the single best drayage-specific score outside South Africa) — fixed, short, "
                "depot-return routes are the ideal EV duty cycle regardless of national grid weakness "
                "elsewhere. **Secondary SKU: diesel rigid for general free-zone logistics** — outside the "
                "core port corridor, stick to conventional diesel given the ~33% flat duty and thin "
                "national grid. **Do not pitch long-haul EV or mining trucks** (0.4/10 readiness) — "
                "Djibouti has essentially no domestic mining logistics segment to speak of."
            ),
            "supply_chain_mode": (
                "CBU import via the Djibouti free-zone regime, targeting SGTD/DPFZA as an institutional "
                "buyer rather than a distributed dealer network — a handful of large port-operator "
                "framework deals will move more volume here than retail-style sales ever could. Price in "
                "USD (Djibouti Franc is de facto USD-pegged, removing most FX risk relative to other "
                "markets) and bundle a depot charging infrastructure package into the port-operator "
                "proposal, since DPFZA controls the Doraleh grid connection directly."
            ),
            "target_persona": (
                "**Primary:** DPFZA / SGTD Terminal Operations Director — controls port equipment "
                "procurement and grid capacity allocation at Doraleh, the single highest-leverage decision "
                "maker in this market. **Secondary:** Ethio-Djibouti Railway freight operations lead — "
                "owns the rail-side handoff and can co-sponsor a port-to-rail e-drayage pilot as a joint "
                "corridor-efficiency initiative with Ethiopian counterparts."
            ),
        },
    },

    "Mauritius": {
        "flag":"🇲🇺","iso":"MUS","region":"Southern Africa (Indian Ocean)","tier":1,
        "kpi":{
            "Annual CV Sales":   ("~1,800","units/yr","+5.4% YoY","https://commerce.govmu.org"),
            "EV Penetration":    ("~14.5%","of new CV sales — top-tier in SSA","+6.0pp YoY","https://energy.govmu.org"),
            "EV Excise Duty":    ("0%","BEV commercial vehicles","vs 30-55% ICE excise bands","https://mra.mu"),
            "Grid Renewable Mix":("~40%","targeting 60% by 2030","National Energy Roadmap","https://energy.govmu.org"),
        },
        "brand_share":{"brands":["BYD EV","Toyota","Isuzu","Foton EV","Mercedes-Benz"],"sales":[420,380,310,260,190]},
        "policy":{
            "tariff":      "BEV commercial vehicles: 0% excise duty. Conventional ICE CVs: 30-55% excise duty band depending on engine size. No CBU customs duty under COMESA/SADC/AfCFTA-aligned regime for most origin countries.",
            "certification":"Mauritius Revenue Authority (MRA) vehicle registration; National Transport Authority roadworthiness; National Electrification Grid connection approval for depot charging >50kW.",
            "key_buyers":  "Beachcomber Hotels, LUX* Resorts & Hotels, Constance Hotels, Mauritius Ports Authority, Rogers Logistics.",
            "risk":        "Tiny absolute market size limits dedicated dealer network economics; almost total European/Japanese brand loyalty in the ICE segment; cyclone-season logistics disruption (Jan-Mar).",
        },
        "news_query":"Mauritius electric vehicle commercial fleet resort tourism logistics",
        "tri_keys":["mu_green_island"],
        "sources":{
            "trade":  ("Ministry of Commerce & Consumer Protection — Mauritius","https://commerce.govmu.org"),
            "customs":("Mauritius Revenue Authority (MRA)","https://mra.mu"),
            "market": ("Ministry of Energy & Public Utilities — Mauritius","https://energy.govmu.org"),
        },
        "tco_params": {
            "ICE_Capex":               72000,
            "EV_Capex":                98000,
            "ICE_Energy_Cost_per_km":  0.36,
            "EV_Energy_Cost_per_km":   0.09,
            "Diesel_Price_per_L":          1.46,
            "ICE_Consumption_L_per_100km": 24.7,
            "Charging_Tariff_per_kWh":     0.135,
            "EV_Consumption_kWh_per_100km":66.7,
            "Monthly_km":              4500,
            "Interest_Rate":           0.07,
            "ICE_Residual_Pct":        0.40,
            "EV_Residual_Pct":         0.18,
            "source_name": "MRA Excise Schedule / Ministry of Energy Tariff Bulletin 2026",
            "source_url":  "https://mra.mu",
        },
        "segment_apps": {
            "Urban FMCG (城市快消)":      {"volume": 900, "ev_readiness": 8.8},
            "Port Drayage (港口倒短)":    {"volume": 500, "ev_readiness": 6.5},
            "Long-Haul Mining (长途矿业)":{"volume": 20,  "ev_readiness": 0.2},
        },
        "risk_radar": {
            "FX_Liquidity":        8.0,
            "Tariff_Advantage":    9.0,
            "Port_Efficiency":     7.5,
            "Grid_Stability":      7.5,
            "Policy_Consistency":  8.5,
        },
        "action": (
            "Ignore absolute unit volume — this is a <b>reference-account showcase market</b>. Fund a "
            "small pure-EV pilot (light e-trucks + electric shuttle buses) with 2-3 flagship resort "
            "groups (Beachcomber, LUX*, Constance) whose entire operating radius is under 60km, and reuse "
            "the resulting case study across every coastal tourism economy in the portfolio. There is "
            "effectively no long-haul mining segment here — do not build one into the pitch."
        ),
        "gtm_playbook": {
            "product_matrix": (
                "**Lead SKU: Pure-electric light truck for resort/hospitality distribution** (8.8/10 "
                "readiness, the highest urban-FMCG score in the portfolio outside Rwanda/Tunisia) — "
                "0% excise duty and an island-wide sub-60km operating radius eliminate the two biggest "
                "objections (cost and range) simultaneously. **Secondary SKU: Electric shuttle bus for "
                "resort/airport transfer routes** (6.5/10 readiness) — pairs naturally with hotel groups' "
                "own sustainability reporting needs. **Do not build a mining/long-haul SKU strategy here** "
                "(0.2/10 readiness) — there is essentially no market for it."
            ),
            "supply_chain_mode": (
                "Direct CBU import at 0% excise duty — no CKD/local assembly rationale exists given the "
                "tiny absolute volume; Mauritius is a **margin-rich, low-volume showcase deal**, not a "
                "manufacturing-localisation play. Price in USD or EUR (Mauritius commercial buyers are "
                "accustomed to hard-currency equipment financing via international leasing lines), and "
                "bundle a depot charging installation into the resort-group proposal as a turnkey package "
                "rather than a separate line item."
            ),
            "target_persona": (
                "**Primary:** Group Sustainability / Fleet Director at a flagship resort group (Beachcomber, "
                "LUX*, Constance) — under direct pressure from international tour operators and ESG-linked "
                "financing covenants to decarbonise ground operations, values the marketing/PR value of a "
                "visible EV fleet as much as the TCO case. **Secondary:** Mauritius Ports Authority "
                "logistics lead — smaller volume but adds a non-hospitality reference account to the "
                "showcase portfolio."
            ),
        },
    },

    "Madagascar": {
        "flag":"🇲🇬","iso":"MDG","region":"Southern Africa (Indian Ocean)","tier":1,
        "kpi":{
            "Annual CV Sales":     ("~2,600","units/yr","+3.4% YoY","https://www.commerce.gov.mg"),
            "National Electrification":("<35%","of population, grid unreliable outside capital","World Bank / JIRAMA","https://www.jirama.mg"),
            "CBU Import Duty":     ("~20%","standard rate, no EV carve-out","","https://douanes.gov.mg"),
            "Diesel Price":        ("MGA 5,450","/litre","≈ $1.19 USD","https://www.mines-energie.gov.mg"),
        },
        "brand_share":{"brands":["Sinotruk","Isuzu","Mercedes-Benz","Foton","Volvo"],"sales":[680,540,420,380,260]},
        "policy":{
            "tariff":      "~20% standard CBU import duty, no differentiated EV rate. Mining-sector equipment occasionally qualifies for investment-code duty relief on a project-by-project basis (Code Minier).",
            "certification":"Ministry of Commerce vehicle registration; Ministry of Mines equipment import approval for mine-site-dedicated fleets under the Code Minier investment framework.",
            "key_buyers":  "Ambatovy (nickel/cobalt), Rio Tinto QMM (ilmenite/mineral sands), Kraoma (chromite), independent graphite and artisanal gemstone export logistics operators.",
            "risk":        "National electrification rate <35%, grid unreliable-to-absent outside Antananarivo. Ariary currency volatility. Periodic political transitions add execution risk. Road network largely unpaved outside main corridors.",
        },
        "news_query":"Madagascar mining logistics truck nickel cobalt export transport",
        "tri_keys":["mg_infra_reality"],
        "sources":{
            "trade":  ("Ministère du Commerce — Madagascar","https://www.commerce.gov.mg"),
            "customs":("Direction Générale des Douanes — Madagascar","https://douanes.gov.mg"),
            "market": ("JIRAMA — Jiro sy Rano Malagasy (national utility)","https://www.jirama.mg"),
        },
        "tco_params": {
            "ICE_Capex":               98000,
            "EV_Capex":                158000,
            "ICE_Energy_Cost_per_km":  0.52,
            "EV_Energy_Cost_per_km":   0.16,
            "Diesel_Price_per_L":          1.19,
            "ICE_Consumption_L_per_100km": 43.7,
            "Charging_Tariff_per_kWh":     0.17,
            "EV_Consumption_kWh_per_100km":94.1,
            "Monthly_km":              5200,
            "Interest_Rate":           0.19,
            "ICE_Residual_Pct":        0.42,
            "EV_Residual_Pct":         0.08,
            "source_name": "JIRAMA Tariff Schedule / Ministry of Mines & Energy 2026",
            "source_url":  "https://www.mines-energie.gov.mg",
        },
        "segment_apps": {
            "Urban FMCG (城市快消)":      {"volume": 700,  "ev_readiness": 2.5},
            "Port Drayage (港口倒短)":    {"volume": 600,  "ev_readiness": 1.8},
            "Long-Haul Mining (长途矿业)":{"volume": 6800, "ev_readiness": 0.1},
        },
        "risk_radar": {
            "FX_Liquidity":        3.0,
            "Tariff_Advantage":    2.5,
            "Port_Efficiency":     3.0,
            "Grid_Stability":      1.5,
            "Policy_Consistency":  3.5,
        },
        "action": (
            "Do not pitch EV here under any circumstances — grid reliability (1.5/10) and a mining-led "
            "demand profile make this a <b>diesel-only market</b>. Lead exclusively with rugged, "
            "high-payload diesel mining/haulage trucks targeting Ambatovy, Rio Tinto QMM, and Kraoma "
            "fleet renewal cycles; positioning EV messaging here will cost credibility with mining-sector "
            "buyers who operate on captive diesel generation, not grid power."
        ),
        "gtm_playbook": {
            "product_matrix": (
                "**Lead SKU: Rugged diesel mining/haulage rigid & tipper** for the Ambatovy/Rio Tinto "
                "QMM/Kraoma inland-mine-to-port corridors — this is essentially 100% of the realistic "
                "near-term opportunity (6,800 units/yr segment volume vs 0.1/10 EV readiness). "
                "**Secondary SKU: diesel rigid for Toamasina/Tuléar port logistics** — supports the same "
                "mining-export value chain. **There is no viable EV SKU to lead with in this market** — "
                "even the highest-scoring segment (Urban FMCG, Antananarivo only) sits at just 2.5/10 "
                "readiness, reflecting the capital's own unreliable grid."
            ),
            "supply_chain_mode": (
                "CBU import at the standard ~20% duty, with a case-by-case push for Code Minier "
                "investment-code duty relief when the buyer is a mine operator importing fleet as part "
                "of a registered mining investment project — this can materially reduce the effective "
                "duty rate for the Ambatovy/QMM/Kraoma segment specifically. Price in USD given Ariary "
                "volatility, and build extended lead times into delivery commitments given Madagascar's "
                "port and inland logistics constraints — do not commit to delivery windows shorter than "
                "regional peers can support."
            ),
            "target_persona": (
                "**Primary:** Ambatovy / Rio Tinto QMM Fleet & Logistics Procurement Director — large, "
                "durable multi-year framework volumes tied to mine-life fleet renewal cycles, decision "
                "process runs through the Code Minier investment-project structure rather than standard "
                "commercial import channels. **Secondary:** Independent graphite/gemstone export logistics "
                "operators — smaller individual deal size but a broader base of relationships across the "
                "mineral-export corridor."
            ),
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 5B. B2B PRICING SANDBOX — reference duty table (Battle 3)
#     Standalone lookup dict, deliberately separate from tco_params so the
#     Pricing & Margin calculator can read a single clean "Import Duty & Tax %"
#     figure per country without parsing free-text policy strings. Figures are
#     the headline CBU/BEV duty rate referenced in each country's KPI/policy
#     block above — illustrative, not a substitute for a customs ruling.
# ══════════════════════════════════════════════════════════════════════════════
B2B_IMPORT_DUTY_PCT = {
    "Nigeria":       0.0,
    "South Africa":  25.0,
    "Morocco":       25.0,
    "Egypt":         40.0,
    "Kenya":         25.0,
    "Ethiopia":      0.0,
    "Algeria":       30.0,
    "Tunisia":       0.0,
    "Rwanda":        0.0,
    "Djibouti":      33.0,
    "Mauritius":     0.0,
    "Madagascar":    20.0,
}

DEFAULT_LOGISTICS_COST_USD = 1500

# ══════════════════════════════════════════════════════════════════════════════
# 5C. INTERNAL COMPETITIVE INTELLIGENCE DATABASE — Internal Use Only
#     Strategic ground truth: we ONLY sell pure-electric commercial vehicles.
#     Every country's competitor set therefore always includes exactly one
#     "Ours (我司纯电)" row — even in markets like Madagascar where the fit is
#     structurally poor, because seeing that mismatch on the positioning
#     scatter IS the internal insight leadership needs.
#
#     Schema per competitor row:
#       Model            — vehicle nameplate
#       Brand_Type       — "Ours (我司纯电)" | "Chinese EV Rival" | "ICE Incumbent"
#       Price_USD        — retail terminal price
#       Length_mm        — vehicle length
#       Battery_kWh      — None for diesel/ICE rows
#       Payload_kg       — rated payload
#       Channel_Strategy — dealer/network description
#       Channel_Count    — approximate number of active sales/service points
#
#     "vehicle_class" and "chinese_footprint" sit at the country level:
#     vehicle_class names which LCV/Van segment this comparison set targets;
#     chinese_footprint is the blunt internal-only paragraph on how Chinese
#     rivals (Foton, Maxus/SAIC, DFSK, Sinotruk, etc.) are actually playing
#     this market — written for the BD/channel team, not for a client deck.
# ══════════════════════════════════════════════════════════════════════════════
INTERNAL_COMPETITOR_DATA = {
    "Nigeria": {
        "vehicle_class": "e-LCV / Panel Van (城市快消轻卡·微面)",
        "competitors": [
            {"Model":"Our EV — X1 e-Van","Brand_Type":"Ours (我司纯电)","Price_USD":42000,"Length_mm":5200,"Battery_kWh":75.0,"Payload_kg":1500,"Channel_Strategy":"直营+2家意向经销商，网点建设中","Channel_Count":2},
            {"Model":"Foton iBlue EV","Brand_Type":"Chinese EV Rival","Price_USD":38500,"Length_mm":5100,"Battery_kWh":70.0,"Payload_kg":1400,"Channel_Strategy":"依托Foton尼日利亚CKD组装网络","Channel_Count":12},
            {"Model":"Maxus EV90","Brand_Type":"Chinese EV Rival","Price_USD":40800,"Length_mm":5400,"Battery_kWh":80.0,"Payload_kg":1600,"Channel_Strategy":"SAIC西非代理商Coscharis渠道","Channel_Count":8},
            {"Model":"Toyota Hiace (Diesel)","Brand_Type":"ICE Incumbent","Price_USD":34000,"Length_mm":5380,"Battery_kWh":None,"Payload_kg":1500,"Channel_Strategy":"CFAO集团全国网络，油车心智垄断","Channel_Count":45},
        ],
        "chinese_footprint": (
            "Foton 与 Maxus 已在尼日利亚建立CKD组装+本地渠道双重护城河：Foton 依托拉各斯周边组装线拿到0%CKD关税，"
            "整车成本比我司CBU直接进口低约10%；Maxus 通过 SAIC 与 Coscharis 集团深度绑定，8个网点覆盖拉各斯-伊巴丹主干道。"
            "两者定价均比我司低8-10%，且网点数量是我司的4-6倍。<b>正面打价格战必输</b> —— "
            "应避其锋芒，主攻 Dangote/BUA 大客户直销框架协议，用USD计价CKD方案对冲奈拉贬值风险，"
            "绕开渠道数量劣势，用大客户直签速度差换取先发优势。"
        ),
    },
    "South Africa": {
        "vehicle_class": "e-LCV / Panel Van (Cape Town / Gauteng 仓配轻卡)",
        "competitors": [
            {"Model":"SV-L1H1","Brand_Type":"Ours (我司纯电)","Price_USD":53619,"Length_mm":4990,"Battery_kWh":83.0,"Payload_kg":1245,"Channel_Strategy":"开普敦首店（我司南非首家直营门店）","Channel_Count":1},
            {"Model":"Foton eView Panel Van","Brand_Type":"Chinese EV Rival","Price_USD":38500,"Length_mm":5380,"Battery_kWh":50.23,"Payload_kg":1150,"Channel_Strategy":"依托FAW南非组装厂配套渠道，全国铺开","Channel_Count":60},
            {"Model":"Maxus eDeliver5","Brand_Type":"Chinese EV Rival","Price_USD":57390,"Length_mm":5400,"Battery_kWh":64.0,"Payload_kg":1190,"Channel_Strategy":"SAIC南非独家总代，仅少量旗舰点","Channel_Count":5},
            {"Model":"Toyota Quantum Van (Diesel)","Brand_Type":"ICE Incumbent","Price_USD":45232,"Length_mm":5380,"Battery_kWh":None,"Payload_kg":1155,"Channel_Strategy":"Toyota南非本土化生产近80年，网点密度全国第一","Channel_Count":200},
        ],
        "chinese_footprint": (
            "实测数据显示：Foton eView 定价（$38,500）比我司 SV-L1H1（$53,619）低约 <b>28%</b>，"
            "且网点数量是我司的 60 倍（60+ vs 1家开普敦首店），是南非渠道渗透最深的中资EV玩家；"
            "Maxus eDeliver5 走的是反向路线——定价比我司还高 7%，但网点仅5+，走精品旗舰路线，"
            "证明南非EV市场并非只能靠低价取胜。Toyota Quantum 凭借近80年本土化生产与200+网点，"
            "在电量/续航故事尚未被验证前仍是运营车队的默认选择。<b>我司真正的威胁不是价格战本身，"
            "而是 Foton 的渠道密度</b>——应避免与 Foton 拼网点数量，转而对标 Maxus 的精品旗舰打法，"
            "以开普敦首店为样板店，用整车尺寸(4990mm，全场最短)与83kWh大电量（全场最高）打"
            "'小车身大电量'的差异化产品故事，锁定城市高频短途配送场景的车队直销客户。"
        ),
    },
    "Morocco": {
        "vehicle_class": "e-LCV / Panel Van (卡萨布兰卡城配)",
        "competitors": [
            {"Model":"Our EV — X1 e-Van","Brand_Type":"Ours (我司纯电)","Price_USD":39500,"Length_mm":5200,"Battery_kWh":78.0,"Payload_kg":1500,"Channel_Strategy":"卡萨布兰卡港区合作方，网点筹建中","Channel_Count":1},

            {"Model":"DFSK C35 EV","Brand_Type":"Chinese EV Rival","Price_USD":33800,"Length_mm":4995,"Battery_kWh":58.0,"Payload_kg":1200,"Channel_Strategy":"东风小康与Auto Hall集团深度绑定分销","Channel_Count":22},
            {"Model":"Maxus EV90","Brand_Type":"Chinese EV Rival","Price_USD":41200,"Length_mm":5400,"Battery_kWh":80.0,"Payload_kg":1600,"Channel_Strategy":"SAIC北非独家进口商","Channel_Count":9},
            {"Model":"Renault Trucks Master (Diesel)","Brand_Type":"ICE Incumbent","Price_USD":36500,"Length_mm":5548,"Battery_kWh":None,"Payload_kg":1700,"Channel_Strategy":"欧盟AA协定2.5%关税，欧洲品牌心智垄断","Channel_Count":38},
        ],
        "chinese_footprint": (
            "东风小康(DFSK)与摩洛哥最大汽车经销商集团 <b>Auto Hall</b> 已形成深度独家绑定，22个网点覆盖"
            "卡萨布兰卡-拉巴特-丹吉尔主干道，且DFSK定价比我司低约15%，是当地中资EV份额最大的玩家；"
            "SAIC/Maxus 走独立进口商路线，网点少但主攻高端车队直销。<b>Auto Hall渠道已被DFSK锁死，"
            "正面抢渠道成本极高</b>——应转向OCP承包商车队直销+CKD合资路线，绕开经销商网络卡位战，"
            "用2.5%欧盟关税税率(通过本地化认定)对冲价格劣势。"
        ),
    },
    "Egypt": {
        "vehicle_class": "e-LCV / Panel Van (开罗城配)",
        "competitors": [
            {"Model":"Our EV — X1 e-Van","Brand_Type":"Ours (我司纯电)","Price_USD":37000,"Length_mm":5200,"Battery_kWh":75.0,"Payload_kg":1500,"Channel_Strategy":"SCZone合作方，网点筹建中","Channel_Count":1},
            {"Model":"Foton iBlue EV","Brand_Type":"Chinese EV Rival","Price_USD":32500,"Length_mm":5100,"Battery_kWh":68.0,"Payload_kg":1400,"Channel_Strategy":"依托GB Auto/MAN Trucks Egypt KD产能","Channel_Count":16},
            {"Model":"Maxus EV90","Brand_Type":"Chinese EV Rival","Price_USD":35800,"Length_mm":5400,"Battery_kWh":80.0,"Payload_kg":1600,"Channel_Strategy":"SAIC埃及独家代理","Channel_Count":7},
            {"Model":"Sinotruk Homan (Diesel)","Brand_Type":"ICE Incumbent","Price_USD":24000,"Length_mm":5600,"Battery_kWh":None,"Payload_kg":3000,"Channel_Strategy":"补贴柴油+40%CBU关税壁垒下的性价比之王","Channel_Count":30},
        ],
        "chinese_footprint": (
            "Foton 借道 GB Auto/MAN Trucks Egypt 现成KD产能实现5%关税入市，成本结构对我司CBU路线形成"
            "近乎降维打击；补贴柴油(EGP 9.75/L)又让 Sinotruk 等传统油车在总成本上难以撼动。"
            "<b>埃及是本轮12国中中资EV+本土柴油双重挤压最严重的市场</b>——若不能复制GB Auto式KD合资，"
            "单纯CBU出口在此几乎无胜算，建议列为观察市场，资源优先投向SCZone物流承包商定向直销。"
        ),
    },
    "Kenya": {
        "vehicle_class": "e-LCV / Panel Van (蒙巴萨港区+内罗毕城配)",
        "competitors": [
            {"Model":"Our EV — X1 e-Van","Brand_Type":"Ours (我司纯电)","Price_USD":36000,"Length_mm":5200,"Battery_kWh":75.0,"Payload_kg":1500,"Channel_Strategy":"内罗毕合作方，网点筹建中","Channel_Count":1},
            {"Model":"Foton iBlue EV","Brand_Type":"Chinese EV Rival","Price_USD":32800,"Length_mm":5100,"Battery_kWh":68.0,"Payload_kg":1400,"Channel_Strategy":"东非区域总代，内罗毕-蒙巴萨双网点","Channel_Count":9},
            {"Model":"Maxus EV90","Brand_Type":"Chinese EV Rival","Price_USD":35200,"Length_mm":5400,"Battery_kWh":80.0,"Payload_kg":1600,"Channel_Strategy":"SAIC肯尼亚独立进口商","Channel_Count":5},
            {"Model":"Isuzu NQR (Diesel)","Brand_Type":"ICE Incumbent","Price_USD":29500,"Length_mm":5985,"Battery_kWh":None,"Payload_kg":3500,"Channel_Strategy":"Isuzu东非组装厂+全国网络","Channel_Count":52},
        ],
        "chinese_footprint": (
            "Foton 在东非走区域总代模式，内罗毕-蒙巴萨双枢纽布局精准卡住港口物流与城配两大场景，"
            "定价比我司低约9%；Isuzu 凭借本地组装历史仍是油车心智绝对霸主。<b>肯尼亚渠道竞争尚未固化"
            "（Chinese EV网点均低于10个），是12国中少数仍可正面抢滩的市场</b>——建议以蒙巴萨港口"
            "Drayage试点为切入点，用Kenya Ports Authority框架合同建立第一批直营网点，抢在Foton/Maxus"
            "扩张前占据港区心智。"
        ),
    },
    "Ethiopia": {
        "vehicle_class": "e-LCV / Panel Van (亚的斯亚贝巴城配 — 柴油已禁止进口)",
        "competitors": [
            {"Model":"Our EV — X1 e-Van","Brand_Type":"Ours (我司纯电)","Price_USD":33000,"Length_mm":5200,"Battery_kWh":75.0,"Payload_kg":1500,"Channel_Strategy":"亚的斯亚贝巴直营+代理商网络","Channel_Count":4},
            {"Model":"BYD T3","Brand_Type":"Chinese EV Rival","Price_USD":29500,"Length_mm":4785,"Battery_kWh":50.0,"Payload_kg":1000,"Channel_Strategy":"BYD在埃塞市占率第一，全国经销网络最广","Channel_Count":26},
            {"Model":"Foton EV Van","Brand_Type":"Chinese EV Rival","Price_USD":31200,"Length_mm":5100,"Battery_kWh":68.0,"Payload_kg":1400,"Channel_Strategy":"Foton EV埃塞第二大份额","Channel_Count":15},
            {"Model":"Legacy ICE Fleet (进口已禁)","Brand_Type":"ICE Incumbent","Price_USD":22000,"Length_mm":5380,"Battery_kWh":None,"Payload_kg":1500,"Channel_Strategy":"存量约8万辆在役，无新增进口但仍占路权大头","Channel_Count":0},
        ],
        "chinese_footprint": (
            "BYD 已凭借2022年石油车禁令窗口期抢先建成埃塞俄比亚最大的EV经销网络(26个网点)，"
            "在新车注册份额上稳居第一；Foton EV紧随其后。<b>中资品牌是这场'政策红利战争'的最大赢家，"
            "我司入场已属追赶者</b>——正面拼网点数量已无胜算，应聚焦BYD/Foton尚未覆盖的Addis周边区域"
            "及政企直采(Ethiopian Roads Authority/Ethio Telecom)大宗订单，用差异化车型规格切入。"
        ),
    },
    "Algeria": {
        "vehicle_class": "e-LCV / Panel Van (阿尔及尔城配 — EV早期阶段)",
        "competitors": [
            {"Model":"Our EV — X1 e-Van","Brand_Type":"Ours (我司纯电)","Price_USD":45000,"Length_mm":5200,"Battery_kWh":75.0,"Payload_kg":1500,"Channel_Strategy":"尚无本地网点，依赖跨境试销","Channel_Count":0},
            {"Model":"Maxus EV90","Brand_Type":"Chinese EV Rival","Price_USD":43500,"Length_mm":5400,"Battery_kWh":80.0,"Payload_kg":1600,"Channel_Strategy":"SAIC通过阿尔及尔独立进口商试水","Channel_Count":2},
            {"Model":"Sinotruk Homan (Diesel)","Brand_Type":"ICE Incumbent","Price_USD":26500,"Length_mm":5600,"Battery_kWh":None,"Payload_kg":3000,"Channel_Strategy":"补贴柴油+进口配额制下的实用主义之选","Channel_Count":18},
            {"Model":"Renault Trucks Master (Diesel)","Brand_Type":"ICE Incumbent","Price_USD":38000,"Length_mm":5548,"Battery_kWh":None,"Payload_kg":1700,"Channel_Strategy":"Renault Rouiba合资JV本地生产，政策优先扶持","Channel_Count":25},
        ],
        "chinese_footprint": (
            "阿尔及利亚EV渗透率仅0.4%，中资品牌尚处试水阶段，Maxus通过独立进口商小规模布局，"
            "尚未形成网络护城河。但补贴柴油(DZD 45/L)与进口许可证配额制才是真正的结构性壁垒——"
            "<b>无论我司还是中资友商，在此市场的共同敌人都是政策壁垒本身，而非彼此</b>。建议暂缓渠道投入，"
            "参照Renault Rouiba模式推进国家背书JV，3-4年设厂窗口期内不与中资EV正面竞争。"
        ),
    },
    "Tunisia": {
        "vehicle_class": "e-LCV / Panel Van (突尼斯城配 — 2026 EV政策红利市场)",
        "competitors": [
            {"Model":"Our EV — X1 e-Van","Brand_Type":"Ours (我司纯电)","Price_USD":34000,"Length_mm":5200,"Battery_kWh":75.0,"Payload_kg":1500,"Channel_Strategy":"突尼斯市直营，网点扩张中","Channel_Count":3},
            {"Model":"Foton iBlue EV","Brand_Type":"Chinese EV Rival","Price_USD":31500,"Length_mm":5100,"Battery_kWh":68.0,"Payload_kg":1400,"Channel_Strategy":"Foton北非区域代理，突尼斯-苏塞双枢纽","Channel_Count":10},
            {"Model":"DFSK C35 EV","Brand_Type":"Chinese EV Rival","Price_USD":28800,"Length_mm":4995,"Battery_kWh":58.0,"Payload_kg":1200,"Channel_Strategy":"东风小康低价走量策略，主攻小微车队","Channel_Count":13},
            {"Model":"Mercedes-Benz Sprinter (Diesel)","Brand_Type":"ICE Incumbent","Price_USD":48000,"Length_mm":5926,"Battery_kWh":None,"Payload_kg":1600,"Channel_Strategy":"欧洲品牌高端心智，但2026新政后总成本劣势凸显","Channel_Count":20},
        ],
        "chinese_footprint": (
            "DFSK 以极致低价走量策略在突尼斯快速铺开13个网点，专攻价格敏感的小微车队市场；"
            "Foton 则主打突尼斯市-苏塞双枢纽的中高端定位。<b>TND 151,000的政策套利窗口对所有EV玩家"
            "一视同仁，真正的分水岭是渠道密度而非政策</b>——DFSK的网点数已是我司4倍以上，"
            "必须加快在Délice Danone/Aramex等旗舰客户的直签速度，用大客户样板案例弥补渠道数量差距，"
            "抢在DFSK/Foton把网点优势转化为品牌心智之前建立差异化定位。"
        ),
    },
    "Rwanda": {
        "vehicle_class": "e-Bus / e-LCV (基加利G2G公交+城配)",
        "competitors": [
            {"Model":"Our EV — X1 e-Van","Brand_Type":"Ours (我司纯电)","Price_USD":31000,"Length_mm":5200,"Battery_kWh":75.0,"Payload_kg":1500,"Channel_Strategy":"基加利直营，G2G投标资质已获批","Channel_Count":2},
            {"Model":"BYD e-Bus","Brand_Type":"Chinese EV Rival","Price_USD":185000,"Length_mm":12000,"Battery_kWh":324.0,"Payload_kg":None,"Channel_Strategy":"BYD卢旺达公交标杆项目，RDB重点扶持","Channel_Count":6},
            {"Model":"Yutong e-Bus","Brand_Type":"Chinese EV Rival","Price_USD":172000,"Length_mm":11800,"Battery_kWh":300.0,"Payload_kg":None,"Channel_Strategy":"Yutong基加利公交系统在役车型","Channel_Count":4},
            {"Model":"Toyota Coaster (Diesel)","Brand_Type":"ICE Incumbent","Price_USD":58000,"Length_mm":6990,"Battery_kWh":None,"Payload_kg":None,"Channel_Strategy":"存量柴油中巴，新规下逐步被置换","Channel_Count":15},
        ],
        "chinese_footprint": (
            "BYD 与 Yutong 已在基加利公交电动化项目中建立标杆地位，是 RDB/RURA G2G招标的重点扶持对象，"
            "客车级网点(6个+4个)覆盖全部主干线。<b>大巴细分我司难以正面竞争，但e-LCV城配细分"
            "中资尚未重兵投入</b>——应聚焦BRALIRWA/MTN等企业车队直销，避开BYD/Yutong主导的G2G大巴标段，"
            "用Kigali Bus Services以外的商业车队证明TCO故事，反向争取G2G第二批标段话语权。"
        ),
    },
    "Djibouti": {
        "vehicle_class": "e-Drayage Tractor (多拉雷港口倒短)",
        "competitors": [
            {"Model":"Our EV — X1 e-Tractor","Brand_Type":"Ours (我司纯电)","Price_USD":58000,"Length_mm":6200,"Battery_kWh":150.0,"Payload_kg":25000,"Channel_Strategy":"DPFZA框架谈判中，尚无落地网点","Channel_Count":0},
            {"Model":"Sinotruk e-Tractor","Brand_Type":"Chinese EV Rival","Price_USD":52000,"Length_mm":6100,"Battery_kWh":140.0,"Payload_kg":24000,"Channel_Strategy":"中国重汽通过埃塞-吉布提走廊项目试点","Channel_Count":1},
            {"Model":"Isuzu FVR (Diesel)","Brand_Type":"ICE Incumbent","Price_USD":41000,"Length_mm":6900,"Battery_kWh":None,"Payload_kg":22000,"Channel_Strategy":"SGTD港口在役柴油牵引车主力","Channel_Count":8},
        ],
        "chinese_footprint": (
            "中国重汽(Sinotruk)依托埃塞-吉布提走廊既有工程项目关系，已在多拉雷港区展开e-Tractor试点，"
            "虽仅1个网点但背靠中资承建的铁路/港口基建项目具备天然入场优势。<b>吉布提是纯增量市场"
            "（港口柴油牵引车存量8台起步），谁先拿下DPFZA/SGTD框架协议谁就定义标准</b>——"
            "应加快与DPFZA的框架谈判节奏，避免被Sinotruk的基建项目关系抢先锁定港口运营方入口。"
        ),
    },
    "Mauritius": {
        "vehicle_class": "e-LCV / e-Shuttle (度假村配送+接驳)",
        "competitors": [
            {"Model":"Our EV — X1 e-Van","Brand_Type":"Ours (我司纯电)","Price_USD":33000,"Length_mm":5200,"Battery_kWh":75.0,"Payload_kg":1500,"Channel_Strategy":"路易港直营，度假村集团直销中","Channel_Count":2},
            {"Model":"BYD T3","Brand_Type":"Chinese EV Rival","Price_USD":27500,"Length_mm":4785,"Battery_kWh":50.0,"Payload_kg":1000,"Channel_Strategy":"BYD毛里求斯EV渗透率最高车型","Channel_Count":7},
            {"Model":"Foton EV Shuttle","Brand_Type":"Chinese EV Rival","Price_USD":36000,"Length_mm":6500,"Battery_kWh":90.0,"Payload_kg":None,"Channel_Strategy":"Foton接驳巴士主攻度假村酒店集团","Channel_Count":3},
            {"Model":"Toyota Hiace (Diesel)","Brand_Type":"ICE Incumbent","Price_USD":30000,"Length_mm":5380,"Battery_kWh":None,"Payload_kg":1500,"Channel_Strategy":"存量油车仍占岛内车队大头","Channel_Count":18},
        ],
        "chinese_footprint": (
            "BYD 凭借0%消费税优势与极具性价比的T3车型，已拿下毛里求斯EV渗透率最高的位置(7个网点)，"
            "价格比我司低约17%；Foton则专攻度假村接驳巴士细分。<b>毛里求斯体量虽小，但BYD已建立"
            "价格心智锚点</b>——正面拼低价性价比无优势，应聚焦Beachcomber/LUX*等旗舰度假村集团的"
            "ESG合作叙事与整体解决方案(车辆+充电桩)打包能力，用服务与品牌溢价而非价格差异化取胜。"
        ),
    },
    "Madagascar": {
        "vehicle_class": "e-LCV (仅安塔那那利佛城配试点 — 全国以柴油矿卡为主)",
        "competitors": [
            {"Model":"Our EV — X1 e-Van","Brand_Type":"Ours (我司纯电)","Price_USD":36000,"Length_mm":5200,"Battery_kWh":75.0,"Payload_kg":1500,"Channel_Strategy":"仅安塔那那利佛试点，无矿区覆盖","Channel_Count":1},
            {"Model":"Maxus EV90","Brand_Type":"Chinese EV Rival","Price_USD":39500,"Length_mm":5400,"Battery_kWh":80.0,"Payload_kg":1600,"Channel_Strategy":"SAIC马达加斯加试探性小规模进口","Channel_Count":1},
            {"Model":"Sinotruk Howo (Diesel Mining)","Brand_Type":"ICE Incumbent","Price_USD":68000,"Length_mm":8500,"Battery_kWh":None,"Payload_kg":30000,"Channel_Strategy":"中国重汽柴油矿卡是Ambatovy/QMM矿区绝对主力","Channel_Count":9},
            {"Model":"Isuzu FTR (Diesel)","Brand_Type":"ICE Incumbent","Price_USD":54000,"Length_mm":7200,"Battery_kWh":None,"Payload_kg":12000,"Channel_Strategy":"塔马塔夫-图莱亚尔港口柴油物流主力","Channel_Count":6},
        ],
        "chinese_footprint": (
            "在电网覆盖率不足35%的马达加斯加，中资品牌的真正战场是<b>柴油矿卡</b>而非EV——"
            "Sinotruk Howo 已凭借Code Minier投资法典下的关税减免深度绑定Ambatovy/QMM矿区柴油车队"
            "9个服务网点，是这个市场事实上的基建级供应商。Maxus EV90虽有小规模试探性进口，"
            "但在无电网支撑的矿区场景毫无竞争力。<b>我司作为纯电玩家在马达加斯加不存在结构性胜算</b>——"
            "本国不应投入渠道资源，仅保留安塔那那利佛市区试点用于技术验证，资源应回流至Rwanda/Tunisia/Mauritius三个EV基建条件成熟的市场。"
        ),
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# 6. FULL 54-NATION MAP DATA
# ══════════════════════════════════════════════════════════════════════════════
ALL_AFRICA = {
    "NGA":"Nigeria","ZAF":"South Africa","MAR":"Morocco","EGY":"Egypt",
    "KEN":"Kenya","ETH":"Ethiopia","DZA":"Algeria","TUN":"Tunisia","RWA":"Rwanda",
    "DJI":"Djibouti","MUS":"Mauritius","MDG":"Madagascar",
    "GHA":"Ghana","TZA":"Tanzania","UGA":"Uganda",
    "SEN":"Senegal","CIV":"Côte d'Ivoire","CMR":"Cameroon","ZMB":"Zambia",
    "ZWE":"Zimbabwe","MOZ":"Mozambique","MWI":"Malawi",
    "NAM":"Namibia","BWA":"Botswana","AGO":"Angola","LBY":"Libya",
    "SDN":"Sudan","SSD":"South Sudan","SOM":"Somalia","ERI":"Eritrea",
    "BDI":"Burundi","COM":"Comoros","STP":"São Tomé",
    "SWZ":"Eswatini","LSO":"Lesotho","CPV":"Cabo Verde",
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
    "SEN":{"gdp":32.0,"roads":16,"cv_imports":4200,"flag":"🇸🇳","region":"West Africa"},
    "CIV":{"gdp":73.0,"roads":81,"cv_imports":7800,"flag":"🇨🇮","region":"West Africa"},
    "CMR":{"gdp":48.0,"roads":77,"cv_imports":5200,"flag":"🇨🇲","region":"Central Africa"},
    "ZMB":{"gdp":29.0,"roads":40,"cv_imports":3800,"flag":"🇿🇲","region":"Southern Africa"},
    "ZWE":{"gdp":28.0,"roads":97,"cv_imports":3200,"flag":"🇿🇼","region":"Southern Africa"},
    "MOZ":{"gdp":18.0,"roads":31,"cv_imports":2800,"flag":"🇲🇿","region":"Southern Africa"},
    "MWI":{"gdp":12.6,"roads":16,"cv_imports":1800,"flag":"🇲🇼","region":"Southern Africa"},
    "NAM":{"gdp":12.8,"roads":48,"cv_imports":3400,"flag":"🇳🇦","region":"Southern Africa"},
    "BWA":{"gdp":18.6,"roads":31,"cv_imports":2900,"flag":"🇧🇼","region":"Southern Africa"},
    "AGO":{"gdp":102.0,"roads":76,"cv_imports":6800,"flag":"🇦🇴","region":"Southern Africa"},
    "LBY":{"gdp":52.0,"roads":34,"cv_imports":4100,"flag":"🇱🇾","region":"North Africa"},
    "SDN":{"gdp":45.0,"roads":24,"cv_imports":3600,"flag":"🇸🇩","region":"East Africa"},
    "SSD":{"gdp":4.6,"roads":9,"cv_imports":800,"flag":"🇸🇸","region":"East Africa"},
    "SOM":{"gdp":8.0,"roads":22,"cv_imports":1200,"flag":"🇸🇴","region":"East Africa"},
    "ERI":{"gdp":2.1,"roads":14,"cv_imports":400,"flag":"🇪🇷","region":"East Africa"},
    "BDI":{"gdp":3.1,"roads":14,"cv_imports":500,"flag":"🇧🇮","region":"East Africa"},
    "COM":{"gdp":1.4,"roads":1,"cv_imports":120,"flag":"🇰🇲","region":"East Africa"},
    "STP":{"gdp":0.6,"roads":0.3,"cv_imports":60,"flag":"🇸🇹","region":"Central Africa"},
    "SWZ":{"gdp":4.8,"roads":4,"cv_imports":650,"flag":"🇸🇿","region":"Southern Africa"},
    "LSO":{"gdp":2.9,"roads":6,"cv_imports":420,"flag":"🇱🇸","region":"Southern Africa"},
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
# 7. NEWS FETCHER — wide net, smart filter, guaranteed no blank
#    (logic unchanged; rendering destination moves to a bottom-page expander)
# ══════════════════════════════════════════════════════════════════════════════
AUTHORITY_DOMAINS = [
    "reuters","bloomberg","ft.com","engineeringnews","businessday",
    "zawya","theafricareport","africanews","afdb","apanews",
    "naamsa","naddc","statssa","moti.gov","finances.gov.tn","anme.tn",
    "rdb.rw","rura.rw","newtimes.co.rw","ktpress.rw",
    "dpfza.gov.dj","mra.mu","jirama.mg",
]
NOISE_WORDS = {"rumor","rumour","unconfirmed","alleged","shocking","viral","leaked","clickbait"}

FALLBACK_INSIGHTS = {
    "Tunisia": [
        {"title":"Loi de Finances 2026 : les véhicules électriques bénéficient d'une exonération totale de droits de douane et d'une TVA réduite à 7% — un avantage TCO historique pour les flottes commerciales tunisiennes.",
         "link":"https://www.finances.gov.tn","published":"2026-01-15","source":"Ministère des Finances Tunisie (Curated Insight)"},
        {"title":"ANME confirms TND 10,000 direct subsidy per commercial BEV registered in Tunisia under the 2026 Energy Efficiency Programme — applications open Q1 2026.",
         "link":"https://www.anme.tn","published":"2026-01-20","source":"ANME Tunisia (Curated Insight)"},
        {"title":"CPG (Compagnie des Phosphates de Gafsa) issues tender for 120 heavy logistics vehicles for Gafsa–Sfax corridor — deadline Q2 2026.",
         "link":"https://www.marchespublics.gov.tn","published":"2026-02-01","source":"Marchés Publics Tunisie (Curated Insight)"},
        {"title":"STEG accelerates EV charging station rollout: 200 commercial charging points planned for Tunis–Sousse–Sfax corridor by end 2026.",
         "link":"https://www.steg.com.tn","published":"2026-02-15","source":"STEG Tunisie (Curated Insight)"},
    ],
    "Algeria": [
        {"title":"Sonatrach lance un appel d'offres pour 350 camions-citernes GNL pour la distribution de gaz naturel dans les wilayas du Sud — délai de soumission T2 2026.",
         "link":"https://www.sonatrach.dz","published":"2026-01-28","source":"Sonatrach Algérie (Curated Insight)"},
        {"title":"Ministry of Industry confirms Rouiba automotive cluster to receive DZD 8bn infrastructure upgrade — creates new CKD assembly capacity for Chinese commercial vehicle JV candidates.",
         "link":"https://www.industrie.gov.dz","published":"2026-02-05","source":"Ministère de l'Industrie Algérie (Curated Insight)"},
    ],
    "Morocco": [
        {"title":"OCP Group issues annual strategic logistics tender — phosphate distribution network expansion requires 180 additional heavy trucks for Khouribga contractor fleet refresh (2026–2028 cycle).",
         "link":"https://www.ocpgroup.ma","published":"2026-01-12","source":"OCP Group (Curated Insight)"},
        {"title":"AIVAM: le marché des véhicules utilitaires lourds au Maroc progresse de 8.5% en 2025 — la demande tirée par les grands chantiers d'infrastructure.",
         "link":"http://www.aivam.ma","published":"2026-01-25","source":"AIVAM Maroc (Curated Insight)"},
    ],
    "Rwanda": [
        {"title":"Rwanda Development Board (RDB) confirms: zero import duty and zero VAT on all electric commercial vehicles — most comprehensive EV fiscal package in Sub-Saharan Africa.",
         "link":"https://www.rdb.rw","published":"2026-01-10","source":"RDB Rwanda (Curated Insight)"},
        {"title":"RURA Green Mobility Strategy 2023–2035: Rwanda targets 100% electric public transport and 70% EV commercial vehicle fleet by 2035 — policy-locked demand pipeline for fleet operators.",
         "link":"https://www.rura.rw","published":"2026-01-18","source":"RURA Rwanda (Curated Insight)"},
        {"title":"Kigali Bus Services (KBS) issues RFP for 50 electric buses for Kigali metropolitan routes — delivery expected H2 2026. G2G procurement framework preferred.",
         "link":"https://www.kigalicity.gov.rw","published":"2026-02-03","source":"City of Kigali (Curated Insight)"},
        {"title":"REG (Rwanda Energy Group) reports <2% grid outage rate in 2024 — Kigali's power reliability confirmed as best-in-class in Sub-Saharan Africa for commercial EV depot charging.",
         "link":"https://www.reg.rw","published":"2026-02-08","source":"REG Rwanda (Curated Insight)"},
        {"title":"MINICOM Rwanda: EV commercial vehicle registrations grew 58% in 2025 — Yutong, BYD, and Foton lead market. e-LCV urban logistics segment fastest growing (+82% YoY).",
         "link":"https://www.minicom.gov.rw","published":"2026-02-20","source":"MINICOM Rwanda (Curated Insight)"},
    ],
    "Djibouti": [
        {"title":"DPFZA confirms Doraleh Multipurpose Port container throughput up 11% YoY as Ethiopian transit trade continues to grow — drayage fleet capacity cited as a bottleneck for 2026.",
         "link":"https://www.dpfza.gov.dj","published":"2026-01-22","source":"DPFZA Djibouti (Curated Insight)"},
        {"title":"Ethio-Djibouti Railway freight volumes reach new record as port-to-rail handoff efficiency becomes the corridor's next investment priority.",
         "link":"https://www.edrailway.com","published":"2026-02-10","source":"Ethio-Djibouti Railway (Curated Insight)"},
    ],
    "Mauritius": [
        {"title":"Mauritius Revenue Authority confirms continuation of 0% excise duty on battery-electric commercial vehicles through the 2026/27 fiscal year.",
         "link":"https://mra.mu","published":"2026-01-14","source":"MRA Mauritius (Curated Insight)"},
        {"title":"Beachcomber and LUX* Resorts jointly announce fleet electrification pilot for resort shuttle and light-distribution vehicles ahead of the 2026 peak tourism season.",
         "link":"https://energy.govmu.org","published":"2026-02-06","source":"Ministry of Energy Mauritius (Curated Insight)"},
    ],
    "Madagascar": [
        {"title":"Ambatovy confirms multi-year mining haulage fleet renewal programme for the Moramanga–Toamasina corridor — diesel rigid and tipper trucks specified.",
         "link":"https://www.ambatovy.com","published":"2026-01-30","source":"Ambatovy (Curated Insight)"},
        {"title":"JIRAMA reports continued grid capacity constraints outside Antananarivo, reinforcing captive diesel generation as the operating norm for inland mining and industrial sites.",
         "link":"https://www.jirama.mg","published":"2026-02-12","source":"JIRAMA Madagascar (Curated Insight)"},
    ],
}

@st.cache_data(ttl=1800)
def fetch_news(query: str, country: str = "", limit: int = 7) -> dict:
    cutoff_30 = datetime.utcnow() - timedelta(days=30)
    cutoff_90 = datetime.utcnow() - timedelta(days=90)

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
                    pub_dt  = datetime(*e.published_parsed[:6])
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

    def _recent(item, cutoff):
        return item["pub_dt"] is None or item["pub_dt"] >= cutoff

    enc1 = (query+" when:30d").replace(" ","+").replace('"',"%22")
    raw1 = _parse(f"https://news.google.com/rss/search?q={enc1}&hl=en-US&gl=US&ceid=US:en")
    r30 = [x for x in raw1 if _recent(x, cutoff_30)]
    a30 = [x for x in r30 if _auth(x)]
    if len(a30) >= 3:
        return {"items":a30[:limit],"is_authority":True,"is_fallback":False}
    if len(r30) >= 3:
        return {"items":r30[:limit],"is_authority":False,"is_fallback":False}

    enc2 = (query+" when:90d").replace(" ","+").replace('"',"%22")
    raw2 = _parse(f"https://news.google.com/rss/search?q={enc2}&hl=en-US&gl=US&ceid=US:en")
    r90 = [x for x in raw2 if _recent(x, cutoff_90)]
    if len(r90) >= 3:
        return {"items":r90[:limit],"is_authority":False,"is_fallback":False}

    enc3 = query.replace(" ","+").replace('"',"%22")
    raw3 = _parse(f"https://news.google.com/rss/search?q={enc3}&hl=en-US&gl=US&ceid=US:en")
    if len(raw3) >= 2:
        return {"items":raw3[:limit],"is_authority":False,"is_fallback":False}

    fb = FALLBACK_INSIGHTS.get(country, [])
    if fb:
        return {"items":fb[:limit],"is_authority":False,"is_fallback":True}
    return {"items":[],"is_authority":False,"is_fallback":True}

def _is_auth(item):
    return any(d in (item["link"]+item["source"]).lower() for d in AUTHORITY_DOMAINS)

def render_news_panel(query: str, country: str):
    """
    Renders the news list. This function itself is unchanged from prior
    versions — what changes (Task 3) is WHERE it gets called: now always
    inside a collapsed st.expander at the very bottom of the page.
    """
    with st.spinner(f"Fetching intelligence for {country}..."):
        result = fetch_news(query, country=country)
    items, is_auth, is_fb = result["items"], result["is_authority"], result["is_fallback"]
    badge = ('<span class="news-badge">AUTHORITY · 30D</span>' if is_auth else
             '<span class="news-fb-badge">GENERAL · 90D</span>' if not is_fb else
             '<span class="news-fb-badge">MARKET INSIGHTS · CURATED</span>')
    st.markdown('<div class="news-wrap">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="news-hdr"><span class="news-hdr-title">📡 &nbsp;{country} — Market Intelligence</span>{badge}</div>',
        unsafe_allow_html=True)
    if not items:
        st.markdown('<div class="news-empty">📭 No results found. Try refreshing.</div>', unsafe_allow_html=True)
    else:
        if is_fb:
            st.markdown(
                '<div style="padding:8px 16px;background:#FFF8F5;border-bottom:1px solid #F0C4AC;'
                'font-family:Inter;font-size:.72rem;color:#D04A02;">'
                '⚡ Live news unavailable — showing curated market intelligence for this market.</div>',
                unsafe_allow_html=True)
        for item in items:
            sc = "news-src" if _is_auth(item) else "news-fb-src"
            st.markdown(
                f'<div class="news-item">'
                f'<a class="news-title-a" href="{item["link"]}" target="_blank">{item["title"]}</a>'
                f'<div class="news-meta"><span class="{sc}">{item["source"]}</span>{item["published"]}</div>'
                f'</div>',
                unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════════════════════
# 8. DATA GENERATORS
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def gen_brand_df(country):
    cd = TIER1[country]["brand_share"]
    total = sum(cd["sales"])
    return pd.DataFrame({
        "Brand":     cd["brands"],
        "Units":     cd["sales"],
        "Share_pct": [round(s/total*100,1) for s in cd["sales"]],
    })

# ── South Africa exclusive data ───────────────────────────────────────────────
@st.cache_data
def gen_za_rail_road():
    return pd.DataFrame({
        "Year":      [2018,2019,2020,2021,2022,2023,2024,2025,2026],
        "Rail_Mt":   [228,218,204,189,171,158,142,131,122],
        "HCV_Units": [27500,28200,29800,30400,31200,32500,31800,30900,30900],
    })

@st.cache_data
def gen_za_freight_category():
    """Stats SA P7162 Road Freight Survey — revenue by commodity category."""
    return pd.DataFrame({
        "Category":       ["Mining & Quarrying","Manufactured Food & Beverages",
                           "Agriculture & Forestry","Retail & Wholesale Trade",
                           "Parcels & Express Logistics","Construction Materials",
                           "Petroleum Products","Other"],
        "Revenue_ZAR_bn": [48.2,21.6,14.8,13.2,11.4,9.6,8.8,7.4],
        "Pct":            [35.4,15.9,10.9,9.7,8.4,7.1,6.5,5.4],
        "Color":          ["#D04A02","#21325B","#295BA5","#4C7FA8","#EB6C2D","#8BA7C4","#C0C8D8","#E2E5EB"],
    })

@st.cache_data
def gen_za_payload_income():
    """Stats SA P7162 — Payload volume vs Freight income, the cost-squeeze story."""
    np.random.seed(10)
    q = pd.date_range("2020-01-01","2026-04-01",freq="QS"); n=len(q)
    return pd.DataFrame({
        "Quarter":       q,
        "Payload_Mt":    (np.linspace(2420,1890,n)+np.random.normal(0,30,n)).round(1),
        "Income_ZAR_bn": (np.linspace(58.4,96.8,n)+np.random.normal(0,1.2,n)).round(2),
    })

@st.cache_data
def gen_za_channel():
    """NAAMSA HCV sales channel split."""
    return pd.DataFrame({
        "Channel":   ["Dealer Retail","Corporate Fleets","Government","Rental & Leasing"],
        "Share_pct": [79.5,10.8,5.2,4.5],
        "Color":     ["#D04A02","#21325B","#295BA5","#8BA7C4"],
    })

@st.cache_data
def gen_za_province():
    """NAAMSA HCV sales by province."""
    return pd.DataFrame({
        "Province":  ["Gauteng","KwaZulu-Natal","Western Cape","Eastern Cape",
                      "Limpopo","Mpumalanga","North West","Free State","Northern Cape"],
        "Units":     [14200,5800,4600,2400,1600,1200,800,600,300],
        "Share_pct": [45.1,18.4,14.6,7.6,5.1,3.8,2.5,1.9,1.0],
    })

# ── Nigeria exclusive data ────────────────────────────────────────────────────
@st.cache_data
def gen_ng_waterfall():
    return pd.DataFrame({
        "Label":   ["CBU Base Price","CBU Import Duty\n(35%)","CBU Port &\nClearance",
                    "CBU Total Landed","CKD Base Price","CKD Import Duty\n(0% — EV Policy)",
                    "CKD Assembly Cost","CKD Total Landed"],
        "Value":   [100000,35000,8000,143000,85000,0,12000,97000],
        "Measure": ["absolute","relative","relative","total",
                    "absolute","relative","relative","total"],
    })

# ── Morocco exclusive data ────────────────────────────────────────────────────
@st.cache_data
def gen_ma_modal():
    return pd.DataFrame({
        "Modal":          ["Slurry Pipeline\n(Raw Ore)","Rail\n(Concentrate)","Road HCV\n(Contractor / Finished Goods)"],
        "Volume_Mt_yr":   [38.0,12.0,6.5],
        "Road_Accessible":[False,False,True],
        "Color":          ["#9BA3B2","#4C7FA8","#D04A02"],
        "Note":           ["187 km pipeline Khouribga→Jorf Lasfar (not road-accessible)",
                           "Rail Benguerir–Jorf Lasfar concentrate (not road-accessible)",
                           "Road: contractor logistics, finished fertiliser, reagent supply"],
    })

# ── Ethiopia exclusive data ───────────────────────────────────────────────────
@st.cache_data
def gen_eth_ev():
    np.random.seed(4)
    months = pd.date_range("2021-01-01","2026-05-01",freq="MS"); n=len(months); ban=18
    ev = np.concatenate([np.linspace(0.5,3.0,ban),
                         np.linspace(3.0,92.0,n-ban)+np.random.normal(0,2,n-ban)]).clip(0,100)
    return pd.DataFrame({"Month":months,"EV_Share_pct":ev.round(1)})

# ── Tunisia exclusive data ────────────────────────────────────────────────────
@st.cache_data
def gen_tn_tco_waterfall():
    return pd.DataFrame({
        "Label":   ["Diesel CIF\nBase Price","Customs Duty\n(Diesel 10%)",
                    "Taxe de\nConsommation\n(Diesel 25%)","TVA\n(Diesel 19%)",
                    "Diesel Total\nLanded Cost","BEV CIF\nBase Price",
                    "Customs Duty\n(BEV 0%)","Taxe Consommation\n(BEV 0%)",
                    "TVA\n(BEV 7%)","ANME Subsidy\n(-TND 10,000)","BEV Total\nLanded Cost"],
        "Value":   [300000,30000,75000,57000,462000,300000,0,0,21000,-10000,311000],
        "Measure": ["absolute","relative","relative","relative","total",
                    "absolute","relative","relative","relative","relative","total"],
    })

@st.cache_data
def gen_tn_b2b_targets():
    return pd.DataFrame({
        "Sector":       ["FMCG & Food","FMCG & Food","Parcels & Express","Parcels & Express",
                         "Port & Industrial","Port & Industrial","Phosphate & Mining","Construction"],
        "Company":      ["Délice Danone Tunisie","SOTUMAG (Groupe Poulina)",
                         "Aramex Tunisia","DHL Tunisia",
                         "Port de Sfax Operators","Tunisie Manutention (TM)",
                         "CPG — Cie des Phosphates de Gafsa","CICO (Ciment d'Oum El Kélil)"],
        "Fleet Size Est.":["120–160 units","80–110 units","60–90 units","40–60 units",
                            "80–120 units","50–70 units","100–150 units","60–80 units"],
        "Decision Maker":["Fleet & Logistics Director","Supply Chain VP",
                          "Country Operations Manager","Fleet Manager MENA",
                          "Port Authority Procurement","General Manager",
                          "Direction des Achats","Directeur Technique"],
    })

# ── Rwanda exclusive data ─────────────────────────────────────────────────────
@st.cache_data
def gen_rw_tariff_comparison():
    return pd.DataFrame({
        "Label": [
            "ICE Truck\nCIF Base (USD 80k)","EAC Import Duty\n(ICE: 25%)","VAT\n(ICE: 18%)",
            "ICE Total\nLanded Cost","EV Truck\nCIF Base (USD 80k)","EAC Import Duty\n(EV: 0%)",
            "VAT\n(EV: 0%)","EV Total\nLanded Cost",
        ],
        "Value_USD": [80000,20000,14400,114400,80000,0,0,80000],
        "Measure": ["absolute","relative","relative","total","absolute","relative","relative","total"],
        "Group": ["ice","ice","ice","ice","ev","ev","ev","ev"],
    })

@st.cache_data
def gen_rw_ev_adoption():
    years = [2022, 2023, 2024, 2025, 2026, 2027]
    return pd.DataFrame({
        "Year":     years,
        "Bus_ICE":  [180, 175, 160, 140, 110,  80],
        "Bus_EV":   [  5,  15,  40,  80, 130, 190],
        "eLCV_ICE": [320, 330, 320, 300, 270, 230],
        "eLCV_EV":  [  8,  25,  65, 130, 230, 380],
    })

# ══════════════════════════════════════════════════════════════════════════════
# 8B. CORE v13.0 GENERATORS — TCO w/ Interest + Residual Value, Segment Apps,
#     Risk Radar, Gate Index
#     Battle 2 upgrade: gen_tco_60month_df / calc_tco_breakeven / chart_tco_breakeven
#     now ALSO accept interest_rate_override, ice_residual_override, and
#     ev_residual_override — so the "极限扩容" sandbox sliders (financing rate,
#     residual value %) redraw the curve live, exactly like the existing
#     diesel-price / charging-tariff / consumption / monthly-km overrides.
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def gen_tco_60month_df(
    country: str,
    diesel_price_override: float = None,
    charging_tariff_override: float = None,
    ice_consumption_override: float = None,
    ev_consumption_override: float = None,
    monthly_km_override: float = None,
    interest_rate_override: float = None,
    ice_residual_override: float = None,
    ev_residual_override: float = None,
) -> pd.DataFrame:
    """
    60-month (5-year) cumulative TCO comparison: ICE vs EV.

    Energy cost is derived live from four independent factors:
        ICE OPEX = Monthly_km * Diesel_Price_per_L * ICE_Consumption_L_per_100km / 100
        EV  OPEX = Monthly_km * Charging_Tariff_per_kWh * EV_Consumption_kWh_per_100km / 100
    Any *_override argument, if provided, replaces the country's default
    tco_params value for that one factor only; all other factors keep their
    dictionary defaults (or their own override, independently).

    Three cost layers are modelled, in the order a CFO would actually
    underwrite this deal:
      1. Capex, financed at the (possibly overridden) Interest_Rate
         (straight-line amortisation over 60 months, interest accrued on
         the declining outstanding balance).
      2. Cumulative energy cost (diesel litres vs kWh at the live pricing).
      3. Residual value penalty: at month 60, the vehicle is assumed sold
         into the local 2nd-hand market. (Possibly overridden)
         ICE_Residual_Pct / EV_Residual_Pct determine what fraction of the
         ORIGINAL CAPEX is recovered as a cash inflow, subtracted from
         cumulative cost at month 60 as a discrete liquidity event.
    """
    p = TIER1[country]["tco_params"]
    months = np.arange(0, 61)
    ice_capex = p["ICE_Capex"]
    ev_capex  = p["EV_Capex"]

    diesel_price     = diesel_price_override     if diesel_price_override     is not None else p["Diesel_Price_per_L"]
    charging_tariff  = charging_tariff_override  if charging_tariff_override  is not None else p["Charging_Tariff_per_kWh"]
    ice_consumption  = ice_consumption_override  if ice_consumption_override  is not None else p["ICE_Consumption_L_per_100km"]
    ev_consumption   = ev_consumption_override   if ev_consumption_override   is not None else p["EV_Consumption_kWh_per_100km"]
    km_per_month     = monthly_km_override       if monthly_km_override       is not None else p["Monthly_km"]

    ice_per_km = diesel_price * ice_consumption / 100
    ev_per_km  = charging_tariff * ev_consumption / 100

    annual_rate = interest_rate_override if interest_rate_override is not None else p.get("Interest_Rate", 0.0)
    monthly_rate = annual_rate / 12
    ice_residual_pct = ice_residual_override if ice_residual_override is not None else p.get("ICE_Residual_Pct", 0.40)
    ev_residual_pct  = ev_residual_override  if ev_residual_override  is not None else p.get("EV_Residual_Pct", 0.15)

    def financed_cumulative(capex, per_km_cost, residual_pct):
        # Straight-line amortisation over the full 60-month horizon
        amort_per_month = capex / 60
        balance = capex
        cum_interest = 0.0
        interest_series = [0.0]
        for m in range(1, 61):
            interest_this_month = balance * monthly_rate
            cum_interest += interest_this_month
            balance -= amort_per_month
            interest_series.append(cum_interest)

        energy_series = per_km_cost * km_per_month * months
        gross_cost = capex + np.array(interest_series) + energy_series

        # Residual value penalty: subtract resale proceeds at month 60 only.
        residual_value = capex * residual_pct
        net_cost = gross_cost.copy()
        net_cost[-1] = net_cost[-1] - residual_value
        return net_cost, residual_value

    ice_cumulative, ice_residual_value = financed_cumulative(ice_capex, ice_per_km, ice_residual_pct)
    ev_cumulative,  ev_residual_value  = financed_cumulative(ev_capex,  ev_per_km,  ev_residual_pct)

    df = pd.DataFrame({
        "Month": months,
        "ICE_Cumulative_Cost": ice_cumulative,
        "EV_Cumulative_Cost":  ev_cumulative,
    })
    df.attrs["ice_residual_value"] = ice_residual_value
    df.attrs["ev_residual_value"]  = ev_residual_value
    df.attrs["ice_residual_pct"]   = ice_residual_pct
    df.attrs["ev_residual_pct"]    = ev_residual_pct
    df.attrs["ice_per_km"]         = ice_per_km
    df.attrs["ev_per_km"]          = ev_per_km
    df.attrs["diesel_price"]       = diesel_price
    df.attrs["charging_tariff"]    = charging_tariff
    df.attrs["interest_rate"]      = annual_rate
    return df


def calc_tco_breakeven(
    country: str,
    diesel_price_override: float = None,
    charging_tariff_override: float = None,
    ice_consumption_override: float = None,
    ev_consumption_override: float = None,
    monthly_km_override: float = None,
    interest_rate_override: float = None,
    ice_residual_override: float = None,
    ev_residual_override: float = None,
):
    """
    Returns (breakeven_month, breakeven_cost) or (None, None) if EV never
    reaches cost parity with ICE within the 60-month horizon. Accepts the
    same slider overrides as gen_tco_60month_df so the break-even badge
    updates in lockstep with the chart.

    Handles three cases:
      1. EV starts more expensive and crosses below ICE within 60mo.
      2. EV starts at or below ICE cost from Month 0.
      3. EV never catches up within 60 months -> (None, None).
    """
    df = gen_tco_60month_df(
        country,
        diesel_price_override=diesel_price_override,
        charging_tariff_override=charging_tariff_override,
        ice_consumption_override=ice_consumption_override,
        ev_consumption_override=ev_consumption_override,
        monthly_km_override=monthly_km_override,
        interest_rate_override=interest_rate_override,
        ice_residual_override=ice_residual_override,
        ev_residual_override=ev_residual_override,
    )
    diff = df["EV_Cumulative_Cost"] - df["ICE_Cumulative_Cost"]

    if diff.iloc[0] <= 0:
        return 0.0, df["ICE_Cumulative_Cost"].iloc[0]

    crossing = None
    for i in range(1, len(diff)):
        if diff.iloc[i-1] > 0 and diff.iloc[i] <= 0:
            x0, x1 = df["Month"].iloc[i-1], df["Month"].iloc[i]
            y0, y1 = diff.iloc[i-1], diff.iloc[i]
            if y1 != y0:
                frac = y0 / (y0 - y1)
                crossing = x0 + frac * (x1 - x0)
            else:
                crossing = x1
            break
    if crossing is None:
        return None, None

    cost_at_crossing = np.interp(crossing, df["Month"], df["ICE_Cumulative_Cost"])
    return crossing, cost_at_crossing


@st.cache_data
def gen_segment_apps_df(country: str) -> pd.DataFrame:
    """
    The three application scenarios: Urban FMCG (城市快消) / Port Drayage
    (港口倒短) / Long-Haul Mining (长途矿业).
    """
    seg = TIER1[country]["segment_apps"]
    rows = []
    for label, d in seg.items():
        rows.append({"Application": label, "Volume": d["volume"], "EV_Readiness": d["ev_readiness"]})
    return pd.DataFrame(rows)


@st.cache_data
def gen_risk_radar_df(country: str) -> pd.DataFrame:
    """Operational risk radar — 5 dimensions, 0-10 scale."""
    r = TIER1[country]["risk_radar"]
    labels_map = {
        "FX_Liquidity":       "FX Liquidity",
        "Tariff_Advantage":   "Tariff Advantage",
        "Port_Efficiency":    "Port Efficiency",
        "Grid_Stability":     "Grid Stability",
        "Policy_Consistency": "Policy Consistency",
    }
    rows = [{"Dimension": labels_map[k], "Score": r[k]} for k in labels_map]
    return pd.DataFrame(rows)


def calc_gate_index(country: str) -> float:
    """
    Converts the 5-dimension risk radar into a single 0-100 'Market Access
    Gate Index'. Weights reflect what actually kills deals in practice: FX
    liquidity and policy consistency are weighted heaviest, since a tariff
    advantage is worthless if profits cannot be repatriated or the regime
    reverses policy overnight.
    """
    r = TIER1[country]["risk_radar"]
    weights = {
        "FX_Liquidity":        0.30,
        "Policy_Consistency":  0.25,
        "Tariff_Advantage":    0.20,
        "Port_Efficiency":     0.15,
        "Grid_Stability":      0.10,
    }
    score_0_10 = sum(r[k] * w for k, w in weights.items())
    return round(score_0_10 * 10, 1)  # scale to 0-100

# ══════════════════════════════════════════════════════════════════════════════
# 9. CHART BUILDERS
# ══════════════════════════════════════════════════════════════════════════════
def chart_brand(df, country):
    colors = [PwC_COLORS[i] if i<3 else "#C0C8D8" for i in range(len(df))]
    fig = go.Figure(go.Bar(
        x=df["Brand"], y=df["Units"],
        text=[f"{p}%" for p in df["Share_pct"]], textposition="outside",
        textfont=dict(size=11,color="#2D3142",family="Inter"),
        marker=dict(color=colors,line=dict(color="white",width=1.5)),
        hovertemplate="<b>%{x}</b><br>%{y:,} units · %{text}<extra></extra>"))
    return _apply(fig,{"yaxis":{**CHART_BASE["yaxis"],"title":"Units","range":[0,df["Units"].max()*1.22]},
                        "xaxis":{**CHART_BASE["xaxis"],"title":"Brand"},"showlegend":False,"bargap":.38})


def chart_segment_apps_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    Application Segment Heatmap. Single-country view: 3 rows (applications)
    x 1 column, color = EV readiness, cell text = volume. Tells the "city
    fast-moves electrify, mining haul stays diesel" story at a glance.
    """
    df_sorted = df.copy()
    z_vals = [[row["EV_Readiness"]] for _, row in df_sorted.iterrows()]
    text_vals = [[f"{row['Volume']:,} units/yr<br>EV Readiness: {row['EV_Readiness']:.1f}/10"]
                 for _, row in df_sorted.iterrows()]

    fig = go.Figure(go.Heatmap(
        z=z_vals,
        x=["EV Readiness"],
        y=df_sorted["Application"].tolist(),
        text=text_vals,
        texttemplate="%{text}",
        textfont=dict(size=11, family="Inter", color="#2D3142"),
        colorscale=[
            [0.0, "#F4F5F7"], [0.15, "#E8ECF4"], [0.35, "#C0C8D8"],
            [0.55, "#8BA7C4"], [0.75, "#EB6C2D"], [1.0, "#D04A02"],
        ],
        zmin=0, zmax=10,
        showscale=True,
        colorbar=dict(
            title=dict(text="Readiness", font=dict(size=9, family="Inter", color="#5A6070")),
            tickfont=dict(size=9, family="Inter", color="#9BA3B2"),
            thickness=10, len=0.8,
        ),
        hovertemplate="<b>%{y}</b><br>%{text}<extra></extra>",
    ))
    return _apply(fig, {
        "xaxis": {**CHART_BASE["xaxis"], "title": "", "showticklabels": False},
        "yaxis": {**CHART_BASE["yaxis"], "title": "", "automargin": True},
        "height": 320,
        "margin": dict(l=170, r=20, t=10, b=10),
    })


def chart_tco_breakeven(
    country: str,
    diesel_price_override: float = None,
    charging_tariff_override: float = None,
    ice_consumption_override: float = None,
    ev_consumption_override: float = None,
    monthly_km_override: float = None,
    interest_rate_override: float = None,
    ice_residual_override: float = None,
    ev_residual_override: float = None,
) -> go.Figure:
    """
    60-month (5-year) cumulative TCO comparison with financing cost and
    residual value penalty included. The break-even crossing is marked
    with a dotted vertical line + star marker, and the month-60 residual
    value step-down is separately annotated so the CFO can see exactly
    where in the curve the resale liquidity event lands.

    Accepts live slider overrides (diesel price, charging tariff,
    consumption rates, monthly km, financing rate, residual %) so the
    chart redraws in real time as a sales rep drags the sandbox controls.
    """
    df = gen_tco_60month_df(
        country,
        diesel_price_override=diesel_price_override,
        charging_tariff_override=charging_tariff_override,
        ice_consumption_override=ice_consumption_override,
        ev_consumption_override=ev_consumption_override,
        monthly_km_override=monthly_km_override,
        interest_rate_override=interest_rate_override,
        ice_residual_override=ice_residual_override,
        ev_residual_override=ev_residual_override,
    )
    breakeven_month, breakeven_cost = calc_tco_breakeven(
        country,
        diesel_price_override=diesel_price_override,
        charging_tariff_override=charging_tariff_override,
        ice_consumption_override=ice_consumption_override,
        ev_consumption_override=ev_consumption_override,
        monthly_km_override=monthly_km_override,
        interest_rate_override=interest_rate_override,
        ice_residual_override=ice_residual_override,
        ev_residual_override=ev_residual_override,
    )
    ice_resid = df.attrs.get("ice_residual_value", 0)
    ev_resid  = df.attrs.get("ev_residual_value", 0)
    diesel_price_live    = df.attrs.get("diesel_price", 0)
    charging_tariff_live = df.attrs.get("charging_tariff", 0)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Month"], y=df["ICE_Cumulative_Cost"],
        name=f"ICE — Cumulative TCO (diesel ${diesel_price_live:.2f}/L)",
        mode="lines", line=dict(color="#21325B", width=2.5),
        hovertemplate="<b>Month %{x}</b><br>ICE Cumulative: <b>$%{y:,.0f}</b><extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df["Month"], y=df["EV_Cumulative_Cost"],
        name=f"EV — Cumulative TCO (charging ${charging_tariff_live:.3f}/kWh)",
        mode="lines", line=dict(color="#D04A02", width=2.5),
        hovertemplate="<b>Month %{x}</b><br>EV Cumulative: <b>$%{y:,.0f}</b><extra></extra>",
    ))

    # Month-60 residual value step-down marker (CFO requirement)
    fig.add_vline(x=60, line_dash="dash", line_color="#9BA3B2", line_width=1.2)
    fig.add_annotation(
        x=60, y=df["ICE_Cumulative_Cost"].max()*1.0,
        text=f"↓ Residual cashback at exit:<br>ICE −${ice_resid:,.0f} · EV −${ev_resid:,.0f}",
        showarrow=False, yanchor="top", xanchor="right", xshift=-4,
        bgcolor="rgba(255,255,255,0.92)", bordercolor="#9BA3B2",
        font=dict(size=9, color="#5A6070", family="Inter"),
    )

    if breakeven_month is not None:
        fig.add_vline(x=breakeven_month, line_dash="dot", line_color="#1A8C5B", line_width=2)
        fig.add_trace(go.Scatter(
            x=[breakeven_month], y=[breakeven_cost],
            mode="markers", marker=dict(size=14, color="#1A8C5B", symbol="star",
                                        line=dict(color="white", width=2)),
            name="Break-even Point", showlegend=False,
            hovertemplate=f"<b>TCO Parity</b><br>Month {breakeven_month:.1f}<br>${breakeven_cost:,.0f}<extra></extra>",
        ))
        fig.add_annotation(
            x=breakeven_month, y=df["EV_Cumulative_Cost"].max()*0.10,
            text=f"🟢 Break-even: Month {breakeven_month:.1f}",
            showarrow=False, bgcolor="rgba(26,140,91,0.1)", bordercolor="#1A8C5B",
            font=dict(size=10, color="#1A8C5B", family="Inter"),
        )
    else:
        fig.add_annotation(
            x=28, y=df["EV_Cumulative_Cost"].max()*0.82,
            text="⚠ No TCO parity within 60 months\nat current financing, energy & residual rates",
            showarrow=False, bgcolor="rgba(208,74,2,0.1)", bordercolor="#D04A02",
            font=dict(size=10, color="#D04A02", family="Inter"),
        )

    return _apply(fig, {
        "xaxis": {**CHART_BASE["xaxis"], "title": "Month of Operation (60mo = 5-year exit)"},
        "yaxis": {**CHART_BASE["yaxis"], "title": "Cumulative Cost (USD, incl. financing)"},
        "legend": {**CHART_BASE["legend"], "y": -0.25},
        "height": 380,
    })


def chart_risk_radar(df: pd.DataFrame, country: str) -> go.Figure:
    """Operational risk radar chart — 5 dimensions on 0-10 scale."""
    categories = df["Dimension"].tolist()
    values = df["Score"].tolist()
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_closed, theta=categories_closed, fill="toself",
        fillcolor="rgba(208,74,2,0.15)", line=dict(color="#D04A02", width=2.5),
        marker=dict(size=7, color="#D04A02"), name=country,
        hovertemplate="<b>%{theta}</b><br>Score: %{r:.1f}/10<extra></extra>",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 10],
                           tickfont=dict(size=9, color="#9BA3B2", family="Inter"),
                           gridcolor="#E2E5EB", linecolor="#E2E5EB"),
            angularaxis=dict(tickfont=dict(size=10, color="#2D3142", family="Inter"),
                            gridcolor="#E2E5EB", linecolor="#E2E5EB"),
        ),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#2D3142", size=12),
        showlegend=False, margin=dict(l=40, r=40, t=30, b=30), height=360,
    )
    return fig


# ── South Africa exclusive chart ──────────────────────────────────────────────
def chart_za_scissors():
    df = gen_za_rail_road()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Year"],y=df["Rail_Mt"],name="Transnet Rail (Mt) ←",
        mode="lines+markers",yaxis="y1",line=dict(color="#D04A02",width=2.5),marker=dict(size=6,color="#D04A02"),
        fill="tozeroy",fillcolor="rgba(208,74,2,0.07)",
        hovertemplate="<b>%{x}</b><br>Rail: %{y:.0f} Mt<extra></extra>"))
    fig.add_trace(go.Scatter(x=df["Year"],y=df["HCV_Units"],name="HCV Road Sales (units) →",
        mode="lines+markers",yaxis="y2",line=dict(color="#21325B",width=2.5),marker=dict(size=6,color="#21325B"),
        hovertemplate="<b>%{x}</b><br>HCV: %{y:,} units<extra></extra>"))
    fig.add_annotation(x=2018,y=228,text="Rail peak 2018:\n228 Mt",
        showarrow=True,arrowhead=2,arrowcolor="#D04A02",
        font=dict(size=9,color="#D04A02",family="Inter"),ax=60,ay=-35)
    return _apply(fig,{"yaxis":{**CHART_BASE["yaxis"],"title":"Rail Volume (Mt)","side":"left"},
                        "yaxis2":{**CHART_BASE["yaxis"],"title":"HCV Sales (units)","side":"right","overlaying":"y","showgrid":False},
                        "xaxis":{**CHART_BASE["xaxis"],"title":"Year","tickmode":"array","tickvals":df["Year"].tolist()},
                        "height":380})


def chart_za_freight_cat(df):
    """Stats SA P7162 — horizontal bar of freight revenue by commodity category."""
    ds = df.sort_values("Revenue_ZAR_bn")
    fig = go.Figure(go.Bar(
        x=ds["Revenue_ZAR_bn"], y=ds["Category"], orientation="h",
        text=[f"R{v:.1f}bn ({p:.1f}%)" for v, p in zip(ds["Revenue_ZAR_bn"], ds["Pct"])],
        textposition="outside", textfont=dict(size=10, family="Inter", color="#2D3142"),
        marker=dict(color=ds["Color"], line=dict(color="white", width=1)),
        hovertemplate="<b>%{y}</b><br>R%{x:.1f}bn<extra></extra>"))
    return _apply(fig, {
        "xaxis": {**CHART_BASE["xaxis"], "title": "Freight Revenue (ZAR bn)",
                  "range": [0, df["Revenue_ZAR_bn"].max()*1.3]},
        "yaxis": {**CHART_BASE["yaxis"], "title": "", "automargin": True},
        "showlegend": False, "margin": dict(l=170, r=20, t=20, b=50), "height": 320,
    })


def chart_za_payload_income(df):
    """Stats SA P7162 — Payload vs Income dual-axis, the cost-squeeze story."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Quarter"], y=df["Payload_Mt"], name="Payload (Mt) ←",
        mode="lines+markers", yaxis="y1", line=dict(color="#D04A02", width=2.5),
        marker=dict(size=4, color="#D04A02"), fill="tozeroy", fillcolor="rgba(208,74,2,0.07)",
        hovertemplate="<b>%{x|Q%q %Y}</b><br>%{y:.0f} Mt<extra></extra>"))
    fig.add_trace(go.Scatter(
        x=df["Quarter"], y=df["Income_ZAR_bn"], name="Freight Income (Rbn) →",
        mode="lines+markers", yaxis="y2", line=dict(color="#21325B", width=2.5),
        marker=dict(size=4, color="#21325B"),
        hovertemplate="<b>%{x|Q%q %Y}</b><br>R%{y:.1f}bn<extra></extra>"))
    fig.add_annotation(
        x=df["Quarter"].iloc[-4], y=df["Payload_Mt"].iloc[-4],
        text="▼ Volume falling\n▲ Revenue rising\n= Cost squeeze",
        showarrow=True, arrowhead=2, arrowcolor="#D04A02",
        bgcolor="rgba(208,74,2,0.08)", bordercolor="#D04A02",
        font=dict(size=9, color="#D04A02", family="Inter"), ax=-80, ay=-50)
    return _apply(fig, {
        "yaxis": {**CHART_BASE["yaxis"], "title": "Payload (Mt)", "side": "left"},
        "yaxis2": {**CHART_BASE["yaxis"], "title": "Income (R bn)", "side": "right",
                   "overlaying": "y", "showgrid": False},
        "xaxis": {**CHART_BASE["xaxis"], "title": "Quarter"}, "height": 320,
    })


def chart_za_channel(df):
    """NAAMSA — HCV sales channel donut."""
    fig = go.Figure(go.Pie(
        labels=df["Channel"], values=df["Share_pct"], hole=.58,
        marker=dict(colors=df["Color"].tolist(), line=dict(color="white", width=2)),
        textinfo="label+percent", textfont=dict(size=11, family="Inter"),
        hovertemplate="<b>%{label}</b><br>%{value:.1f}%<extra></extra>"))
    fig.add_annotation(text="Sales\nChannel", x=.5, y=.5,
        font=dict(size=12, family="Inter", color="#5A6070"), showarrow=False)
    return _apply(fig, {
        "showlegend": True,
        "legend": dict(orientation="v", x=1.02, y=.5, font=dict(size=11), bgcolor="rgba(0,0,0,0)"),
        "margin": dict(l=20, r=120, t=20, b=20), "height": 290,
    })


def chart_za_province(df):
    """NAAMSA — HCV sales by province bar chart."""
    colors = ["#D04A02" if i==0 else "#21325B" if i==1 else "#295BA5" if i==2
              else "#8BA7C4" for i in range(len(df))]
    fig = go.Figure(go.Bar(
        x=df["Province"], y=df["Units"],
        text=[f"{v:,}\n({s}%)" for v, s in zip(df["Units"], df["Share_pct"])],
        textposition="outside", textfont=dict(size=10, family="Inter"),
        marker=dict(color=colors, line=dict(color="white", width=1.5)),
        hovertemplate="<b>%{x}</b><br>%{y:,} units<extra></extra>"))
    return _apply(fig, {
        "yaxis": {**CHART_BASE["yaxis"], "title": "Units", "range": [0, df["Units"].max()*1.25]},
        "xaxis": {**CHART_BASE["xaxis"], "title": "Province"},
        "showlegend": False, "bargap": .35, "height": 300,
    })


# ── Nigeria exclusive chart ───────────────────────────────────────────────────
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
                        "margin":dict(l=60,r=20,t=30,b=70),"height":420})


# ── Morocco exclusive chart ───────────────────────────────────────────────────
def chart_ma_modal(df):
    colors=["#C0C8D8" if not r else "#D04A02" for r in df["Road_Accessible"]]
    fig=go.Figure(go.Bar(x=df["Volume_Mt_yr"],y=df["Modal"],orientation="h",
        text=[f"{v:.1f} Mt/yr" for v in df["Volume_Mt_yr"]],
        textposition="outside",textfont=dict(size=11,family="Inter",color="#2D3142"),
        marker=dict(color=colors,line=dict(color="white",width=2)),
        customdata=df["Note"],
        hovertemplate="<b>%{y}</b><br>%{x:.1f} Mt/yr<br>%{customdata}<extra></extra>"))
    fig.add_annotation(x=6.5,y="Road HCV\n(Contractor / Finished Goods)",
        text="● Road-accessible",showarrow=False,xanchor="left",xshift=8,
        font=dict(size=10,color="#D04A02",family="Inter"))
    return _apply(fig,{"xaxis":{**CHART_BASE["xaxis"],"title":"Estimated Volume (Mt/year)",
                                 "range":[0,df["Volume_Mt_yr"].max()*1.35]},
                        "yaxis":{**CHART_BASE["yaxis"],"title":"","automargin":True},
                        "showlegend":False,"margin":dict(l=200,r=20,t=20,b=50),"height":300})


# ── Ethiopia exclusive chart ──────────────────────────────────────────────────
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
                        "yaxis":{**CHART_BASE["yaxis"],"title":"EV Market Share (%)","range":[0,105]},
                        "showlegend":False,"height":380})


# ── Tunisia exclusive chart ───────────────────────────────────────────────────
def chart_tn_tco_waterfall(df):
    fig=go.Figure(go.Waterfall(orientation="v",measure=df["Measure"].tolist(),
        x=df["Label"].tolist(),y=df["Value"].tolist(),
        text=["FREE ✓" if v==0 else f"TND {v:,.0f}" if m=="total" else
              f"−TND {abs(v):,.0f}" if v<0 else f"+TND {v:,.0f}"
              for v,m in zip(df["Value"],df["Measure"])],
        textposition="outside",textfont=dict(size=9,family="Inter",color="#2D3142"),
        connector=dict(line=dict(color="#E2E5EB",width=1,dash="dot")),
        increasing=dict(marker_color="#D04A02"),decreasing=dict(marker_color="#1A8C5B"),
        totals=dict(marker_color="#21325B"),
        hovertemplate="<b>%{x}</b><br>TND %{y:,.0f}<extra></extra>"))
    fig.add_annotation(x="BEV Total\nLanded Cost",y=311000,
        text="💡 BEV saves\n~TND 151,000\nvs Diesel",showarrow=True,arrowhead=2,
        arrowcolor="#1A8C5B",bgcolor="rgba(26,140,91,0.1)",bordercolor="#1A8C5B",
        font=dict(size=10,color="#1A8C5B",family="Inter"),ax=-90,ay=-60)
    fig.add_vline(x=4.5,line_dash="dash",line_color="#9BA3B2",line_width=1)
    return _apply(fig,{"yaxis":{**CHART_BASE["yaxis"],"title":"Cost (TND)","range":[-30000,530000]},
                        "xaxis":{**CHART_BASE["xaxis"],"title":"","tickangle":-15},
                        "showlegend":False,"margin":dict(l=60,r=20,t=50,b=90),"height":460})


# ── Rwanda exclusive charts ───────────────────────────────────────────────────
def chart_rw_tariff_comparison(df):
    fig = go.Figure(go.Waterfall(
        orientation="v", measure=df["Measure"].tolist(),
        x=df["Label"].tolist(), y=df["Value_USD"].tolist(),
        text=["FREE ✓" if v==0 else f"${v:,.0f}" if m=="total" else f"+${v:,.0f}"
              for v, m in zip(df["Value_USD"], df["Measure"])],
        textposition="outside", textfont=dict(size=10, family="Inter", color="#2D3142"),
        connector=dict(line=dict(color="#E2E5EB", width=1, dash="dot")),
        increasing=dict(marker_color="#D04A02"), decreasing=dict(marker_color="#1A8C5B"),
        totals=dict(marker_color="#21325B"),
        hovertemplate="<b>%{x}</b><br>$%{y:,.0f}<extra></extra>",
    ))
    fig.add_annotation(
        x="EV Total\nLanded Cost", y=80000,
        text="✅ EV saves $34,400\nper unit vs ICE (43%)",
        showarrow=True, arrowhead=2, arrowcolor="#1A8C5B",
        bgcolor="rgba(26,140,91,0.1)", bordercolor="#1A8C5B",
        font=dict(size=10, color="#1A8C5B", family="Inter"), ax=-100, ay=-50,
    )
    return _apply(fig, {
        "yaxis":{**CHART_BASE["yaxis"],"title":"All-in Landed Cost (USD)","range":[-5000,135000]},
        "xaxis":{**CHART_BASE["xaxis"],"title":"","tickangle":-10},
        "showlegend":False,"margin":dict(l=60, r=20, t=50, b=90),"height":420,
    })

def chart_rw_ev_adoption(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Year"], y=df["Bus_ICE"], name="Public Buses — ICE",
        mode="lines", stackgroup="buses", line=dict(color="#9BA3B2", width=0),
        fillcolor="rgba(155,163,178,0.35)",
        hovertemplate="<b>%{x}</b><br>Bus ICE: <b>%{y}</b> units<extra></extra>"))
    fig.add_trace(go.Scatter(x=df["Year"], y=df["Bus_EV"], name="Public Buses — EV",
        mode="lines", stackgroup="buses", line=dict(color="#21325B", width=0),
        fillcolor="rgba(33,50,91,0.55)",
        hovertemplate="<b>%{x}</b><br>Bus EV: <b>%{y}</b> units<extra></extra>"))
    fig.add_trace(go.Scatter(x=df["Year"], y=df["eLCV_ICE"], name="Urban LCV — ICE",
        mode="lines", stackgroup="lcv", line=dict(color="#C0C8D8", width=0),
        fillcolor="rgba(192,200,216,0.30)",
        hovertemplate="<b>%{x}</b><br>LCV ICE: <b>%{y}</b> units<extra></extra>"))
    fig.add_trace(go.Scatter(x=df["Year"], y=df["eLCV_EV"], name="Urban LCV — EV",
        mode="lines", stackgroup="lcv", line=dict(color="#D04A02", width=0),
        fillcolor="rgba(208,74,2,0.45)",
        hovertemplate="<b>%{x}</b><br>LCV EV: <b>%{y}</b> units<extra></extra>"))
    return _apply(fig, {
        "xaxis":{**CHART_BASE["xaxis"],"title":"Year","tickmode":"array","tickvals":df["Year"].tolist()},
        "yaxis":{**CHART_BASE["yaxis"],"title":"Units in Fleet / Registered"},
        "legend":{**CHART_BASE["legend"],"y":-0.25}, "height":380,
    })

# ══════════════════════════════════════════════════════════════════════════════
# 10. UI HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════
def _chdr(label, title, sub, src_name, src_url):
    st.markdown(f"""
<div class="chart-card">
    <div class="chart-label">{label}</div>
    <div class="chart-title">{title}</div>
    <div class="chart-sub">{sub}</div>
    <div class="source-link">📌 <a href="{src_url}" target="_blank">{src_name}</a></div>
</div>
""", unsafe_allow_html=True)

def _level_hdr(level_num: int, title: str, sub: str = ""):
    st.markdown(f"""
<div class="section-hdr">
    <div class="section-bar"></div>
    <span class="level-badge">Level {level_num}</span>
    <div class="section-title">{title}</div>
    {"<div class='section-sub'>"+sub+"</div>" if sub else ""}
</div>
""", unsafe_allow_html=True)

def _sdiv(title, sub=""):
    st.markdown(f"""
<div class="section-hdr">
    <div class="section-bar"></div>
    <div class="section-title">{title}</div>
    {"<div class='section-sub'>"+sub+"</div>" if sub else ""}
</div>
""", unsafe_allow_html=True)

def _kpi_row(cdata):
    cols = st.columns(len(cdata["kpi"]))
    for col, (key, (val, lbl, delta, _)) in zip(cols, cdata["kpi"].items()):
        with col:
            dc = "normal" if "+" in delta else "inverse" if "-" in delta else "off"
            st.metric(key, val, delta, delta_color=dc, help=lbl)
    src = list(cdata["sources"].values())[0]
    st.caption(f"Source: [{src[0]}]({src[1]}) · Simulated data unless otherwise stated.")

# ══════════════════════════════════════════════════════════════════════════════
# 11. MASTER NARRATIVE-FLOW RENDERER
#     One function drives all 12 countries top-to-bottom:
#       Level 1 → KPIs + Risk Radar + Gate Index + FX Alert
#       Level 2 → Segment Heatmap (L) + TCO Break-even Sandbox (R) — Battle 2
#       Level 3 → Brand Share (L) + Country-Exclusive Chart (R)
#       Level 4 → Due Diligence (single column) + Strategic Action box
#     Tab 3 → GTM Playbook, now led by the B2B Pricing & Margin Sandbox — Battle 3
# ══════════════════════════════════════════════════════════════════════════════

def _exclusive_chart_nigeria():
    CUSTOMS = "https://customs.gov.ng"
    NADDC = "https://naddc.gov.ng"
    _chdr("Exclusive · Nigeria Customs / NADDC",
          "CBU vs. CKD/SKD Import Cost Waterfall",
          "Per-unit landed cost (30t HCV, base $100k). CKD route saves ~$46k under 2023 EV/assembly tariff.",
          "Nigeria Customs Service", CUSTOMS)
    st.plotly_chart(chart_ng_waterfall(gen_ng_waterfall()), use_container_width=True, config=PLOTLY_CFG, key="ng_excl")
    st.caption(f"Source: [Nigeria Customs]({CUSTOMS}) · [NADDC]({NADDC}) · Figures illustrative.")

def _exclusive_chart_morocco():
    OCP = "https://www.ocpgroup.ma/investor-relations"
    AIVAM = "http://www.aivam.ma"
    _chdr("Exclusive · OCP Group",
          "Phosphate Transport Modal Split — Pipeline vs Rail vs Road",
          "Orange = road-accessible segment only. Pipeline/rail serve the primary ore trunk and are structurally closed to HCVs.",
          "OCP Group Investor Relations", OCP)
    st.plotly_chart(chart_ma_modal(gen_ma_modal()), use_container_width=True, config=PLOTLY_CFG, key="ma_excl")
    st.caption(f"Source: [OCP Group IR]({OCP}) · [AIVAM]({AIVAM}) · Estimated volumes.")

def _exclusive_chart_egypt():
    src = TIER1["Egypt"]["sources"]["trade"]
    _chdr("Market Context · EOS",
          "Subsidised Diesel Erodes EV Cost Case",
          "At EGP 9.75/L subsidised diesel, the ICE energy cost floor is structurally low — "
          "the KD tariff route (5% vs 40% CBU) is the only realistic lever, not EV TCO.",
          src[0], src[1])
    st.info(
        "**No standalone chart for this slot.** Egypt's commercial story is the **KD tariff "
        "waterfall**, already quantified in Level 2's TCO panel — energy subsidy keeps ICE "
        "structurally cheap to run, so the differentiator is assembly tariff, not fuel cost.",
        icon="ℹ️"
    )

def _exclusive_chart_kenya():
    src = TIER1["Kenya"]["sources"]["trade"]
    _chdr("Market Context · KEBS / Kenya Railways",
          "SGR Is a Complement, Not a Competitor, to Road HCV",
          "SGR volumes grew 1.2→5.8 Mt (2018-23) but operate Mombasa–Nairobi only (472 km). "
          "Last-mile to Kampala, Kigali, and Juba remains structurally road-dependent.",
          src[0], src[1])
    st.success(
        "**Net read:** EAC cross-border freight — the majority of Kenyan HCV demand — is "
        "untouched by SGR. Port drayage at Mombasa is the best near-term EV pilot route.",
        icon="✅"
    )

def _exclusive_chart_ethiopia():
    ERCA = "https://www.erca.gov.et"
    MOTI = "https://www.moti.gov.et"
    _chdr("Exclusive · MoTI / ERCA",
          "EV Market Share Trajectory — Post Petroleum Import Ban",
          "From <3% to >85% EV share in 30 months following the July 2022 petroleum import ban.",
          "Ministry of Trade & Industry Ethiopia", MOTI)
    st.plotly_chart(chart_eth_ev(gen_eth_ev()), use_container_width=True, config=PLOTLY_CFG, key="eth_excl")
    st.caption(f"Source: [MoTI Ethiopia]({MOTI}) · [ERCA]({ERCA}) · Simulated data.")

def _exclusive_chart_tunisia():
    FIN = "https://www.finances.gov.tn"
    ANME = "https://www.anme.tn"
    _chdr("Exclusive · Loi de Finances 2026 / ANME",
          "All-in Landed Cost Waterfall: Diesel HCV vs. BEV",
          "CIF base TND 300,000. BEV: 0% customs + 0% excise + 7% TVA + TND 10,000 ANME subsidy.",
          "Ministère des Finances Tunisie", FIN)
    st.plotly_chart(chart_tn_tco_waterfall(gen_tn_tco_waterfall()), use_container_width=True, config=PLOTLY_CFG, key="tn_excl")
    st.caption(f"Source: [Loi de Finances 2026]({FIN}) · [ANME]({ANME}) · Exchange rate TND/USD 3.14 (BCT Q1 2026).")

def _exclusive_chart_algeria():
    src = TIER1["Algeria"]["sources"]["trade"]
    _chdr("Market Context · Ministère du Commerce",
          "Renault Rouiba JV — The Only Proven Entry Template",
          "30% CBU tariff + import licence quotas make direct CV import commercially unviable. "
          "Renault's JV assembly plant in Rouiba is the only durable precedent.",
          src[0], src[1])
    st.warning(
        "**Net read:** This is a JV-or-nothing market. Budget 3-4 years from MOU to first "
        "unit production; do not pursue CBU export here.",
        icon="⚠️"
    )

def _exclusive_chart_rwanda():
    RDB = "https://www.rdb.rw"
    RURA = "https://www.rura.rw"
    _chdr("Exclusive · RURA / MINICOM",
          "Kigali EV Fleet Adoption — Buses & Urban LCV (Stacked Area)",
          "2022–2025 actuals; 2026–2027 RURA Green Mobility forecast. Orange = EV, Grey = ICE.",
          "RURA — Green Mobility Annual Report 2024", RURA)
    st.plotly_chart(chart_rw_ev_adoption(gen_rw_ev_adoption()), use_container_width=True, config=PLOTLY_CFG, key="rw_excl")
    st.caption(f"Source: [RURA]({RURA}) · [RDB]({RDB}) · 2026-27 figures are policy targets, not confirmed actuals.")

def _exclusive_chart_djibouti():
    src = TIER1["Djibouti"]["sources"]["trade"]
    _chdr("Market Context · DPFZA",
          "Djibouti Is a Corridor, Not a Domestic Market",
          "Over 95% of Ethiopia's seaborne trade transits Djibouti. The relevant fleet metric is "
          "port-to-rail drayage truck-days, not domestic vehicle registrations.",
          src[0], src[1])
    st.success(
        "**Net read:** Port Drayage scores 7.8/10 EV readiness — the best drayage-specific score "
        "outside South Africa — because the Doraleh port-to-rail leg is short, fixed, and "
        "depot-return every night. Anchor the account on DPFZA/SGTD, not retail CBU sales.",
        icon="✅"
    )

def _exclusive_chart_mauritius():
    src = TIER1["Mauritius"]["sources"]["trade"]
    _chdr("Market Context · Ministry of Energy Mauritius",
          "Island-Wide Sub-60km Radius Eliminates the Range Objection",
          "Mauritius's entire road network is under 2,000km. With 0% BEV excise duty, this is a "
          "showcase market for pure-EV hospitality and light-distribution fleets.",
          src[0], src[1])
    st.success(
        "**Net read:** Urban FMCG scores 8.8/10 EV readiness — the highest outside Rwanda/Tunisia. "
        "Fund a small resort-fleet pilot with Beachcomber/LUX*/Constance and reuse the case study "
        "across every coastal tourism market in the portfolio.",
        icon="✅"
    )

def _exclusive_chart_madagascar():
    src = TIER1["Madagascar"]["sources"]["market"]
    _chdr("Market Context · JIRAMA",
          "Grid Reliability <35% — This Is a Diesel-Only Market",
          "National electrification is under 35% and unreliable outside Antananarivo. Core CV "
          "demand is mining/mineral-export haulage on unpaved roads, running on captive diesel "
          "generation, not grid power.",
          src[0], src[1])
    st.warning(
        "**Net read:** Long-Haul Mining scores just 0.1/10 EV readiness — the lowest of any "
        "segment in any of the 12 markets. Lead exclusively with rugged diesel mining/haulage "
        "trucks for Ambatovy, Rio Tinto QMM, and Kraoma.",
        icon="⚠️"
    )


EXCLUSIVE_CHART_REGISTRY = {
    "Nigeria":       _exclusive_chart_nigeria,
    "Morocco":       _exclusive_chart_morocco,
    "Egypt":         _exclusive_chart_egypt,
    "Kenya":         _exclusive_chart_kenya,
    "Ethiopia":      _exclusive_chart_ethiopia,
    "Tunisia":       _exclusive_chart_tunisia,
    "Algeria":       _exclusive_chart_algeria,
    "Rwanda":        _exclusive_chart_rwanda,
    "Djibouti":      _exclusive_chart_djibouti,
    "Mauritius":     _exclusive_chart_mauritius,
    "Madagascar":    _exclusive_chart_madagascar,
}


def _render_market_risk_tab(country: str, cdata: dict):
    """
    Tab 1 content: 市场与风控全景.
    Level 1 + Level 2 + Level 3. Level 2's TCO sandbox is the Battle 2
    rebuild: session_state-backed sliders, a 🔒/🔓 lock toggle (default
    locked = baseline curve only), a 🔄 Reset-to-Default button, and
    dramatically widened slider ranges across all 8 tunable factors.
    """
    _level_hdr(1, "Decision Overview · 决策全景", "KPIs, market access gate, and FX risk screen")
    _kpi_row(cdata)
    st.markdown("<br>", unsafe_allow_html=True)

    gate_index = calc_gate_index(country)
    fx_score = cdata["risk_radar"]["FX_Liquidity"]
    gate_color = "#1A8C5B" if gate_index >= 65 else "#B45309" if gate_index >= 45 else "#B91C1C"

    radar_col, gate_col = st.columns([3, 1], gap="large")
    with radar_col:
        _chdr("Market Access Radar", f"5-Dimension Operational Risk Profile — {country}",
              "FX Liquidity · Tariff Advantage · Port Efficiency · Grid Stability · Policy Consistency (0-10 scale)",
              cdata["sources"]["trade"][0], cdata["sources"]["trade"][1])
        st.plotly_chart(chart_risk_radar(gen_risk_radar_df(country), country),
                        use_container_width=True, config=PLOTLY_CFG, key=f"{country}_radar")
    with gate_col:
        st.markdown(f"""
<div class="gate-index-card">
    <div class="gate-index-label">Market Access Gate Index</div>
    <div class="gate-index-value" style="color:{gate_color};">{gate_index:.0f}<span style="font-size:1rem;color:#9BA3B2;">/100</span></div>
    <div class="gate-index-label" style="margin-top:6px;color:{gate_color};">
        {"LOW RISK" if gate_index>=65 else "MODERATE RISK" if gate_index>=45 else "HIGH RISK"}
    </div>
</div>
""", unsafe_allow_html=True)
        st.caption("Weighted: FX 30% · Policy 25% · Tariff 20% · Port 15% · Grid 10%")

    if fx_score <= 3:
        st.error(
            f"🚨 **FATAL RISK ALERT — FX Liquidity Score: {fx_score:.1f}/10**\n\n"
            f"USD/hard-currency access in **{country}** is severely constrained. Any deal structure "
            f"that assumes smooth profit repatriation or stable local-currency pricing carries "
            f"material risk of capital trapping or margin erosion. Structure contracts in "
            f"USD-indexed terms with FX hedging clauses before proceeding.",
            icon="🚨"
        )

    _level_hdr(2, "Commercial Monetisation · 商业变现", "Where EV wins by application, and when it pays for itself")
    seg_col, tco_col = st.columns(2, gap="large")
    with seg_col:
        _chdr("Application Segment Heatmap", "EV Readiness by Use Case",
              "Urban FMCG · Port Drayage · Long-Haul Mining — volume and electrification readiness",
              cdata["sources"]["trade"][0], cdata["sources"]["trade"][1])
        st.plotly_chart(chart_segment_apps_heatmap(gen_segment_apps_df(country)),
                        use_container_width=True, config=PLOTLY_CFG, key=f"{country}_segheat")
        seg_df = gen_segment_apps_df(country)
        st.caption(
            "Volumes: " + " · ".join(f"{r['Application'].split('(')[0].strip()}: {r['Volume']:,}/yr"
                                     for _, r in seg_df.iterrows())
        )
    with tco_col:
        p = cdata["tco_params"]
        _chdr("60-Month TCO Break-even Sandbox", "ICE vs. EV Cumulative Cost (incl. financing & residual)",
              f"Capex ICE ${p['ICE_Capex']:,.0f} vs EV ${p['EV_Capex']:,.0f} · "
              f"financed at {p['Interest_Rate']*100:.0f}% p.a. · "
              f"5-yr residual: ICE {p['ICE_Residual_Pct']:.0%} / EV {p['EV_Residual_Pct']:.0%}",
              p["source_name"], p["source_url"])

        # ── Battle 2: 参数默认值 + session_state 初始化 ──────────────────────
        defaults = {
            "diesel":   float(p["Diesel_Price_per_L"]),
            "charge":   float(p["Charging_Tariff_per_kWh"]),
            "ice_cons": float(p["ICE_Consumption_L_per_100km"]),
            "ev_cons":  float(p["EV_Consumption_kWh_per_100km"]),
            "km":       int(p["Monthly_km"]),
            "interest": round(float(p.get("Interest_Rate", 0.10)) * 100, 1),
            "ice_res":  round(float(p.get("ICE_Residual_Pct", 0.40)) * 100, 1),
            "ev_res":   round(float(p.get("EV_Residual_Pct", 0.15)) * 100, 1),
        }
        skeys = {name: f"{country}_{name}_slider" for name in defaults}
        for name, val in defaults.items():
            st.session_state.setdefault(skeys[name], val)

        lock_key = f"tco_unlocked_{country}"
        st.session_state.setdefault(lock_key, False)

        lock_l, lock_r = st.columns([3, 2])
        with lock_l:
            unlocked = st.toggle(
                "🔓 解锁参数修改 (Unlock to Edit)" if not st.session_state[lock_key]
                else "🔒 点击重新锁定 (Click to Re-lock)",
                key=lock_key,
                help="默认锁定，仅展示基准曲线，防止前线业务员误触打乱基准数据；"
                     "解锁后可自由拖动全部滑块进行现场测算。",
            )
        with lock_r:
            if st.button("🔄 一键恢复默认 (Reset to Default)", key=f"tco_reset_{country}",
                        use_container_width=True):
                for name, val in defaults.items():
                    st.session_state[skeys[name]] = val
                st.rerun()

        locked = not st.session_state[lock_key]
        banner_cls = "tco-lock-banner" if locked else "tco-lock-banner unlocked"
        banner_txt = (
            "🔒 <b>参数已锁定</b> — 当前展示该国基准曲线，防止误触。点击上方开关解锁后方可拖动滑块。 / "
            "Locked — showing baseline curve only. Toggle above to unlock sliders."
            if locked else
            "🔓 <b>参数已解锁</b> — 可自由拖动下方全部滑块进行实时测算，测算完成后建议重新锁定。 / "
            "Unlocked — drag any slider below to re-price the deal live."
        )
        st.markdown(f'<div class="{banner_cls}" style="font-size:.74rem;color:#5A6070;">{banner_txt}</div>',
                    unsafe_allow_html=True)

        if locked:
            # 锁定状态下强制回写基准值，确保滑块显示与图表口径完全一致
            for name, val in defaults.items():
                st.session_state[skeys[name]] = val

        sld_l, sld_r = st.columns(2)
        with sld_l:
            diesel_price_live = st.slider(
                "⛽ Diesel Price (USD/L)",
                min_value=0.0, max_value=5.0, step=0.01,
                key=skeys["diesel"], disabled=locked,
                help="放开至 0–5 USD/L 的极限区间，可模拟补贴取消、价格飙升或跨区域差异。",
            )
        with sld_r:
            charging_tariff_live = st.slider(
                "🔌 Commercial Charging Tariff (USD/kWh)",
                min_value=0.0, max_value=1.0, step=0.005,
                key=skeys["charge"], disabled=locked,
                help="放开至 0–1 USD/kWh，可模拟电网尖峰电价或专属 e-mobility 优惠电价。",
            )

        with st.expander("⚙️ Advanced — 消耗 / 里程 / 融资 / 残值 极限扩容", expanded=False):
            adv_l, adv_r = st.columns(2)
            with adv_l:
                ice_consumption_live = st.slider(
                    "ICE consumption (L/100km)", min_value=0.0, max_value=150.0, step=1.0,
                    key=skeys["ice_cons"], disabled=locked,
                )
                monthly_km_live = st.slider(
                    "Monthly utilisation (km/month)", min_value=0, max_value=50000, step=100,
                    key=skeys["km"], disabled=locked,
                )
                interest_pct_live = st.slider(
                    "💰 Financing Interest Rate (%/yr)", min_value=0.0, max_value=50.0, step=1.0,
                    key=skeys["interest"], disabled=locked,
                    help="按用户要求放开至 0%–50% 的极限融资利率区间。",
                )
            with adv_r:
                ev_consumption_live = st.slider(
                    "EV consumption (kWh/100km)", min_value=0.0, max_value=300.0, step=1.0,
                    key=skeys["ev_cons"], disabled=locked,
                )
                ice_resid_pct_live = st.slider(
                    "ICE Residual Value @ 60mo (%)", min_value=0.0, max_value=100.0, step=1.0,
                    key=skeys["ice_res"], disabled=locked,
                )
                ev_resid_pct_live = st.slider(
                    "EV Residual Value @ 60mo (%)", min_value=0.0, max_value=100.0, step=1.0,
                    key=skeys["ev_res"], disabled=locked,
                )

        interest_rate_live = interest_pct_live / 100
        ice_residual_live  = ice_resid_pct_live / 100
        ev_residual_live   = ev_resid_pct_live / 100

        st.plotly_chart(
            chart_tco_breakeven(
                country,
                diesel_price_override=diesel_price_live,
                charging_tariff_override=charging_tariff_live,
                ice_consumption_override=ice_consumption_live,
                ev_consumption_override=ev_consumption_live,
                monthly_km_override=monthly_km_live,
                interest_rate_override=interest_rate_live,
                ice_residual_override=ice_residual_live,
                ev_residual_override=ev_residual_live,
            ),
            use_container_width=True, config=PLOTLY_CFG, key=f"{country}_tco"
        )
        breakeven_month, _ = calc_tco_breakeven(
            country,
            diesel_price_override=diesel_price_live,
            charging_tariff_override=charging_tariff_live,
            ice_consumption_override=ice_consumption_live,
            ev_consumption_override=ev_consumption_live,
            monthly_km_override=monthly_km_live,
            interest_rate_override=interest_rate_live,
            ice_residual_override=ice_residual_live,
            ev_residual_override=ev_residual_live,
        )
        be_text = f"Month {breakeven_month:.1f} ({breakeven_month/12:.1f} yrs)" if breakeven_month is not None else "Not reached within 60 months"
        ice_per_km_live = diesel_price_live * ice_consumption_live / 100
        ev_per_km_live  = charging_tariff_live * ev_consumption_live / 100
        st.caption(
            f"Break-even: **{be_text}** · ICE energy: ${ice_per_km_live:.3f}/km · "
            f"EV energy: ${ev_per_km_live:.3f}/km · "
            f"Energy delta: ${ice_per_km_live - ev_per_km_live:.3f}/km in EV's favour"
            if ice_per_km_live >= ev_per_km_live else
            f"Break-even: **{be_text}** · ICE energy: ${ice_per_km_live:.3f}/km · "
            f"EV energy: ${ev_per_km_live:.3f}/km · "
            f"⚠ EV energy is now MORE expensive than ICE at these slider settings"
        )
        st.caption(
            "📌 TCO 测算已包含当地高息融资成本及二手车残值惩罚，融资利率与残值比例现已加入实时沙盘 / "
            "TCO modelling includes local financing cost and residual value penalty — both now "
            "part of the live sandbox above."
        )
        st.session_state[f"_tco_live_{country}"] = {
            "breakeven_month": breakeven_month,
            "diesel_price": diesel_price_live,
            "charging_tariff": charging_tariff_live,
            "ice_per_km": ice_per_km_live,
            "ev_per_km": ev_per_km_live,
            "monthly_km": monthly_km_live,
            "interest_rate": interest_rate_live,
            "ice_capex": p["ICE_Capex"],
            "ev_capex": p["EV_Capex"],
        }

    _level_hdr(3, "Market Depth · 市场深度", "Brand competitive set and country-specific structural story")

    if country == "South Africa":
        # South Africa keeps its full 4-chart Stats SA / NAAMSA depth panel —
        # explicitly preserved at the user's request rather than collapsed
        # into a single exclusive chart like the other markets.
        src = cdata["sources"]["trade"]
        STATSSA = "https://www.statssa.gov.za/publications/P7162/P7162.html"
        NAAMSA  = "https://naamsa.co.za"

        row1_l, row1_r = st.columns(2, gap="large")
        with row1_l:
            _chdr("Competitive Set", f"Brand Market Share — {country}",
                  "Top 5 brands by annual CV unit sales", src[0], src[1])
            st.plotly_chart(chart_brand(gen_brand_df(country), country),
                            use_container_width=True, config=PLOTLY_CFG, key=f"{country}_brand")
        with row1_r:
            _chdr("Exclusive · Transnet / NAAMSA",
                  "Rail Collapse → Road HCV Demand Transfer",
                  "Rail freight down 46% from 2018 peak; HCV road sales absorb displaced demand",
                  "Transnet Annual Report",
                  "https://www.transnet.net/InvestorCentre/Pages/AnnualReports.aspx")
            st.plotly_chart(chart_za_scissors(), use_container_width=True, config=PLOTLY_CFG, key="za_scissors")

        st.markdown("<br>", unsafe_allow_html=True)
        row2_l, row2_r = st.columns(2, gap="large")
        with row2_l:
            _chdr("Exclusive · Stats SA P7162", "Road Freight Revenue by Commodity Category",
                  "Mining & Quarrying dominates at 35.4% of total freight revenue", "Stats SA — P7162", STATSSA)
            st.plotly_chart(chart_za_freight_cat(gen_za_freight_category()),
                            use_container_width=True, config=PLOTLY_CFG, key="za_freight_cat")
        with row2_r:
            _chdr("Exclusive · Stats SA P7162", "Payload Volume vs. Freight Income — The Cost Squeeze",
                  "Diverging trends illustrate per-km cost inflation burden on fleet operators",
                  "Stats SA — P7162", STATSSA)
            st.plotly_chart(chart_za_payload_income(gen_za_payload_income()),
                            use_container_width=True, config=PLOTLY_CFG, key="za_payload_income")

        st.markdown("<br>", unsafe_allow_html=True)
        row3_l, row3_r = st.columns(2, gap="large")
        with row3_l:
            _chdr("Exclusive · NAAMSA", "HCV Sales by Channel",
                  "Dealer retail dominates; corporate fleet growing", "NAAMSA", NAAMSA)
            st.plotly_chart(chart_za_channel(gen_za_channel()),
                            use_container_width=True, config=PLOTLY_CFG, key="za_channel")
        with row3_r:
            _chdr("Exclusive · NAAMSA", "HCV Sales by Province",
                  "Gauteng accounts for 45.1% — industrial heartland concentration", "NAAMSA", NAAMSA)
            st.plotly_chart(chart_za_province(gen_za_province()),
                            use_container_width=True, config=PLOTLY_CFG, key="za_province")
        st.caption(f"Sources: [Stats SA P7162]({STATSSA}) · [NAAMSA]({NAAMSA}) · Simulated data modelled on actual report structures.")

    else:
        brand_col, excl_col = st.columns(2, gap="large")
        with brand_col:
            src = cdata["sources"]["trade"]
            _chdr("Competitive Set", f"Brand Market Share — {country}",
                  "Top 5 brands by annual CV unit sales", src[0], src[1])
            st.plotly_chart(chart_brand(gen_brand_df(country), country),
                            use_container_width=True, config=PLOTLY_CFG, key=f"{country}_brand")
        with excl_col:
            renderer = EXCLUSIVE_CHART_REGISTRY.get(country)
            if renderer:
                renderer()


def _render_due_diligence_tab(country: str, cdata: dict):
    """
    Tab 2 content: 尽调交叉验证.
    Single-column Triangulation expanders followed by the Strategic Action box.
    """
    _level_hdr(4, "Due Diligence & Action · 尽调研判与行动",
               "Single-column verdict — converted directly into a sales instruction")
    tri_keys = cdata.get("tri_keys", [])
    if not tri_keys:
        st.info("No Due Diligence triangulation modules registered for this market yet.", icon="ℹ️")
    for tk in tri_keys:
        t = TRIANGULATION.get(tk, {})
        if not t:
            continue
        with st.expander(f"🔍  {t['title']}", expanded=False):
            render_triangulation(tk)

    render_strategic_action(cdata)


def _render_gtm_playbook_tab(country: str, cdata: dict):
    """
    Tab 3 content: 🚀 GTM Playbook (一国一策战术板).

    Battle 3 rebuild: the deprecated 'Target Account Search' company-intel
    lookup (checked against a 4-company hardcoded DB — useless for the vast
    majority of real-world small/mid dealer prospects) has been REMOVED
    entirely and replaced with the 【B2B 落地报价与毛利倒推 (Pricing & Margin
    Sandbox)】 — an interactive calculator any frontline rep or dealer can
    use on any deal, in any market, without needing the customer's name in
    a database first.
    """
    st.markdown(f"""
<div class="gtm-mission-banner">
    <div class="gtm-mission-title">🚀 {country} — GTM Tactical Playbook</div>
    <div class="gtm-mission-sub">一国一策战术板 · Mission brief for frontline sales &amp; channel teams</div>
</div>
""", unsafe_allow_html=True)

    # ══ B2B Pricing & Margin Sandbox (Battle 3 core deliverable) ══════════════
    st.markdown("""
<div class="b2b-banner">
    <div class="b2b-banner-title">💰 B2B 落地报价与毛利倒推沙盘 · Pricing &amp; Margin Sandbox</div>
    <div class="b2b-banner-sub">从当地终端零售价倒推我司必须做到的离岸底价，现场就能算给经销商听</div>
</div>
""", unsafe_allow_html=True)

    p = cdata["tco_params"]
    default_duty = B2B_IMPORT_DUTY_PCT.get(country, 25.0)
    default_retail = int(round(p["ICE_Capex"] * 1.35 / 500.0) * 500)
    cost_floor = p["ICE_Capex"] * 0.68  # illustrative OEM manufacturing cost floor ("红线")

    in_l, in_r = st.columns(2, gap="large")
    with in_l:
        retail_price = st.number_input(
            "🎯 Target Retail Price (当地对标竞品终端售价, USD)",
            min_value=5000, max_value=500000, value=default_retail, step=500,
            key=f"b2b_retail_{country}",
            help="当地市场对标竞品（Isuzu/Foton/Sinotruk 等）的终端到手售价，示例默认值 $45,000 级别。",
        )
        dealer_margin_pct = st.slider(
            "🤝 Dealer Margin % (给当地代理商留的利润率)",
            min_value=0.0, max_value=50.0, value=15.0, step=0.5,
            key=f"b2b_margin_{country}",
        )
    with in_r:
        duty_pct = st.slider(
            "🏛 Import Duty & Tax % (进口关税与税负，默认读取该国关税参数)",
            min_value=0.0, max_value=60.0, value=float(default_duty), step=0.5,
            key=f"b2b_duty_{country}",
            help=f"默认值 {default_duty:.1f}% 取自 {country} 的关税基准（见 Tab 2 政策解读）；可自行调整以测算 CKD/关税优惠情形。",
        )
        logistics_cost = st.number_input(
            "🚢 Logistics Cost (单车海运物流费, USD)",
            min_value=0, max_value=20000, value=DEFAULT_LOGISTICS_COST_USD, step=100,
            key=f"b2b_logi_{country}",
        )

    # ── 倒推逻辑 / Reverse-engineering logic ──
    #   Landed_Cost_to_Dealer = Retail_Price × (1 − Dealer_Margin%)
    #   Landed_Cost_to_Dealer = (FOB + Logistics_Cost) × (1 + Duty%)
    #   ⇒ FOB = Landed_Cost_to_Dealer ÷ (1 + Duty%) − Logistics_Cost
    landed_cost_to_dealer = retail_price * (1 - dealer_margin_pct / 100)
    fob_target = landed_cost_to_dealer / (1 + duty_pct / 100) - logistics_cost
    gross_profit = fob_target - cost_floor
    margin_on_cost = (gross_profit / cost_floor) if cost_floor else 0.0

    out_l, out_r = st.columns(2, gap="large")
    with out_l:
        st.markdown(f"""
<div class="b2b-output-card fob">
    <div class="b2b-output-label">🏭 OEM Target FOB Price · 离岸底价</div>
    <div class="b2b-output-value" style="color:#21325B;">${fob_target:,.0f}</div>
    <div class="b2b-output-sub">在满足经销商 {dealer_margin_pct:.1f}% 利润与 {duty_pct:.1f}% 关税/税负前提下，
    我司必须做到的离岸(FOB)底价</div>
</div>
""", unsafe_allow_html=True)
    with out_r:
        profit_cls = "profit-ok" if gross_profit >= 0 else "profit-bad"
        profit_color = "#1A8C5B" if gross_profit >= 0 else "#B91C1C"
        st.markdown(f"""
<div class="b2b-output-card {profit_cls}">
    <div class="b2b-output-label">📊 Gross Profit per Unit · 单车毛利</div>
    <div class="b2b-output-value" style="color:{profit_color};">${gross_profit:,.0f}</div>
    <div class="b2b-output-sub">对比制造成本红线 ${cost_floor:,.0f}（≈ 该国标杆 Capex 的 68%）
    · 毛利率 {margin_on_cost*100:.1f}%</div>
</div>
""", unsafe_allow_html=True)

    st.caption(
        "计算逻辑 / Formula: Landed Cost to Dealer = Retail × (1 − Dealer Margin%)  →  "
        "FOB = Landed Cost ÷ (1 + Duty%) − Logistics Cost  →  Gross Profit = FOB − 制造成本红线。"
        "制造成本红线为illustrative估算值，实际签单前请以财务口径最终成本为准。"
    )

    if fob_target < cost_floor:
        st.error(
            "🚨 利润击穿警告：在此终端定价下，出海面临亏损！请要求代理商压低利润预期或转为 CKD 模式！"
        )
    elif margin_on_cost >= 0.15:
        st.success("🟢 利润健康，可签单！(毛利率 ≥15%，安全边际充足)")
    else:
        st.warning(
            f"⚠️ 毛利率偏薄（{margin_on_cost*100:.1f}%）——尚可推进，但建议争取更优关税/CKD路径，"
            f"或与代理商协商压缩物流成本以扩大安全边际。"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ══ Existing 3-card country-level playbook ════════════════════════════════
    gtm = cdata.get("gtm_playbook")

    if not gtm:
        st.warning(
            f"**Playbook not yet authored for {country}.**\n\n"
            "This market currently has full Market & Risk Analytics and Due Diligence coverage, "
            "but a GTM tactical playbook has not yet been written by the strategy team. "
            "Request authoring via the GTM Strategy Director before committing sales resources "
            "to this market without a tactical brief. The Pricing & Margin Sandbox above still "
            "works for this market regardless.",
            icon="⚠️"
        )
        return

    pm_col, sc_col, tp_col = st.columns(3, gap="medium")
    with pm_col:
        st.markdown(f"""
<div class="gtm-card">
    <div class="gtm-card-hdr product">
        <div class="gtm-card-icon">🎯</div>
        <div>
            <div class="gtm-card-title">Product Matrix</div>
            <div class="gtm-card-subtitle">产品阵型与应用场景</div>
        </div>
    </div>
    <div class="gtm-card-body">{gtm['product_matrix']}</div>
</div>
""", unsafe_allow_html=True)
    with sc_col:
        st.markdown(f"""
<div class="gtm-card">
    <div class="gtm-card-hdr supply">
        <div class="gtm-card-icon">⚙️</div>
        <div>
            <div class="gtm-card-title">Supply Chain & Pricing</div>
            <div class="gtm-card-subtitle">供应链与定价打法</div>
        </div>
    </div>
    <div class="gtm-card-body">{gtm['supply_chain_mode']}</div>
</div>
""", unsafe_allow_html=True)
    with tp_col:
        st.markdown(f"""
<div class="gtm-card">
    <div class="gtm-card-hdr persona">
        <div class="gtm-card-icon">🧭</div>
        <div>
            <div class="gtm-card-title">Target Persona</div>
            <div class="gtm-card-subtitle">靶向客户画像</div>
        </div>
    </div>
    <div class="gtm-card-body">{gtm['target_persona']}</div>
</div>
""", unsafe_allow_html=True)

    st.caption(
        "📌 战术板基于尽职调查模块的交叉验证结论制定，应配合 Tab 2 的研判结果协同使用 / "
        "Playbook tactics are derived from the Due Diligence cross-validation conclusions in Tab 2 "
        "— review both before committing account resources."
    )


BRAND_TYPE_COLORS = {
    "Ours (我司纯电)":   "#D04A02",
    "Chinese EV Rival":  "#21325B",
    "ICE Incumbent":     "#9BA3B2",
}
BRAND_TYPE_ORDER = ["Ours (我司纯电)", "Chinese EV Rival", "ICE Incumbent"]


def _init_competitor_session_state(country: str) -> str:
    """
    Battle 4 — Step 1: session_state initialisation.
    Checks whether st.session_state already holds a working copy of this
    country's competitor table; if not, deep-copies the default rows out
    of INTERNAL_COMPETITOR_DATA into a fresh DataFrame and stores it under
    a per-country key. Every subsequent read (scatter plot, data_editor,
    positioning verdict) reads ONLY from this session_state key, so the
    chart and table stay in lockstep with any edit the user makes.
    """
    skey = f"competitor_data_{country}"
    if skey not in st.session_state:
        base_rows = INTERNAL_COMPETITOR_DATA.get(country, {}).get("competitors", [])
        st.session_state[skey] = pd.DataFrame(copy.deepcopy(base_rows))
    return skey


def _render_competitive_intel_tab(country: str, cdata: dict):
    """
    Tab 4 content: 🕵️ Internal Competitive Intel (内部竞品靶向分析).
    INTERNAL USE ONLY — never shown in a client-facing deck.

    Layout (per spec):
      Top row, left  → 🔒/🔓 lock toggle + Reset button + st.data_editor
                        (Module B: 核心参数红蓝对决)
      Top row, right → live plotly.express positioning scatter
                        (Module A: 产品价格卡位矩阵) — redraws instantly
                        whenever the left-hand editor is touched, because
                        both read from the same st.session_state DataFrame.
      Bottom          → Chinese rivals channel-footprint insight card
                        (Module C: 中资同行渠道渗透底牌)
    """
    st.markdown(f"""
<div class="intel-banner">
    <div class="intel-banner-title">🕵️ {country} — Internal Competitive Intelligence
        <span class="intel-badge">🔒 Internal Use Only</span>
    </div>
    <div class="intel-banner-sub">内部竞品靶向分析 · 严禁对外分享 · 我司战略底线：仅销售纯电商用车 (Pure-EV Only)</div>
</div>
""", unsafe_allow_html=True)

    intel = INTERNAL_COMPETITOR_DATA.get(country)
    if not intel:
        st.info(
            f"**No internal competitive dataset authored for {country} yet.** "
            "Request the BD/Channel Intelligence team to populate this market before "
            "using it for account planning.",
            icon="ℹ️"
        )
        return

    skey = _init_competitor_session_state(country)

    editor_col, chart_col = st.columns([1.05, 1], gap="large")

    with editor_col:
        _chdr("Module B · 内部专用", "核心参数红蓝对决 (Spec-to-Spec Showdown)",
              f"车型类别：{intel['vehicle_class']} — 我司车型 vs 中国友商 vs 当地油车霸主",
              "Internal BD Intelligence", "#")

        lock_key = f"comp_unlocked_{country}"
        st.session_state.setdefault(lock_key, False)

        lock_l, lock_r = st.columns([3, 2])
        with lock_l:
            st.toggle(
                "🔓 解锁竞品底价与参数编辑 (Unlock Data Editing)" if not st.session_state[lock_key]
                else "🔒 点击重新锁定 (Click to Re-lock)",
                key=lock_key,
                help="默认锁定，仅供展示；解锁后可双击单元格直接修改 Price_USD / Battery_kWh 等竞品参数，"
                     "右侧卡位散点图会实时重绘。",
            )
        with lock_r:
            if st.button("🔄 恢复默认出厂数据", key=f"comp_reset_{country}", use_container_width=True):
                base_rows = INTERNAL_COMPETITOR_DATA.get(country, {}).get("competitors", [])
                st.session_state[skey] = pd.DataFrame(copy.deepcopy(base_rows))
                st.rerun()

        locked = not st.session_state[lock_key]
        banner_cls = "tco-lock-banner" if locked else "tco-lock-banner unlocked"
        banner_txt = (
            "🔒 <b>数据已锁定</b> — 仅供展示，防止误触修改竞品底价。解锁后方可编辑。"
            if locked else
            "🔓 <b>数据已解锁</b> — 双击任意单元格可直接修改数值，右侧散点图将实时联动。"
        )
        st.markdown(f'<div class="{banner_cls}" style="font-size:.74rem;color:#5A6070;">{banner_txt}</div>',
                    unsafe_allow_html=True)

        edited_df = st.data_editor(
            st.session_state[skey],
            key=f"comp_editor_{country}",
            use_container_width=True,
            num_rows="fixed",
            disabled=locked,
            hide_index=True,
            column_config={
                "Model": st.column_config.TextColumn("Model / 车型", width="medium"),
                "Brand_Type": st.column_config.SelectboxColumn(
                    "Brand_Type / 阵营", options=BRAND_TYPE_ORDER, width="medium"),
                "Price_USD": st.column_config.NumberColumn("Price_USD / 终端价", format="$%d"),
                "Length_mm": st.column_config.NumberColumn("Length_mm / 车长", format="%d mm"),
                "Battery_kWh": st.column_config.NumberColumn("Battery_kWh / 电量", format="%.1f kWh"),
                "Payload_kg": st.column_config.NumberColumn("Payload_kg / 载重", format="%d kg"),
                "Channel_Strategy": st.column_config.TextColumn("Channel_Strategy / 渠道布局", width="large"),
                "Channel_Count": st.column_config.NumberColumn("Channel_Count / 网点数", format="%d"),
            },
        )
        # 写回 session_state，确保右侧散点图读取的是编辑后的最新数据
        st.session_state[skey] = edited_df

        st.caption(
            "💡 Battery_kWh 留空 = 传统燃油车（我司战略底线：只卖纯电，此列永远非空）。"
            " Price_USD / Battery_kWh 等数值仅解锁后可编辑，用于现场压力测试竞品降价情形。"
        )

    with chart_col:
        _chdr("Module A · 内部专用", "产品价格卡位矩阵 (Product Positioning Scatter Map)",
              "X = Length_mm 车长 · Y = Price_USD 终端价 · 气泡颜色 = 品牌阵营 · 气泡大小 = 载重(kg)",
              "Internal BD Intelligence", "#")

        df_plot = st.session_state[skey].copy()
        if df_plot.empty:
            st.info("No competitor rows to plot.", icon="ℹ️")
        else:
            df_plot["Payload_Plot"] = df_plot["Payload_kg"].fillna(df_plot["Payload_kg"].median() or 1500)
            df_plot["Battery_Label"] = df_plot["Battery_kWh"].apply(
                lambda v: f"{v:.0f} kWh" if pd.notna(v) else "N/A (Diesel/ICE)"
            )

            fig = px.scatter(
                df_plot, x="Length_mm", y="Price_USD", color="Brand_Type",
                size="Payload_Plot", size_max=38, text="Model",
                color_discrete_map=BRAND_TYPE_COLORS,
                category_orders={"Brand_Type": BRAND_TYPE_ORDER},
                hover_name="Model",
                hover_data={
                    "Length_mm": True, "Price_USD": True, "Battery_Label": True,
                    "Payload_kg": True, "Channel_Count": True,
                    "Payload_Plot": False,
                },
            )
            fig.update_traces(
                textposition="top center",
                textfont=dict(size=10, family="Inter", color="#2D3142"),
                marker=dict(line=dict(color="white", width=1.5), opacity=0.88),
            )
            fig = _apply(fig, {
                "xaxis": {**CHART_BASE["xaxis"], "title": "Length (mm)"},
                "yaxis": {**CHART_BASE["yaxis"], "title": "Retail Price (USD)"},
                "legend": {**CHART_BASE["legend"], "title": {"text": ""}, "y": -0.28},
                "height": 440,
            })
            st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CFG, key=f"{country}_comp_scatter")

            # ── 实时卡位判定 / live positioning verdict ──
            ours = df_plot[df_plot["Brand_Type"] == "Ours (我司纯电)"]
            rivals = df_plot[df_plot["Brand_Type"] != "Ours (我司纯电)"]
            if not ours.empty and not rivals.empty:
                our_price = float(ours["Price_USD"].iloc[0])
                our_length = float(ours["Length_mm"].iloc[0])
                avg_rival_price = float(rivals["Price_USD"].mean())
                avg_rival_length = float(rivals["Length_mm"].mean())
                price_delta_pct = (our_price - avg_rival_price) / avg_rival_price * 100
                length_delta_pct = (our_length - avg_rival_length) / avg_rival_length * 100

                if price_delta_pct > 5 and length_delta_pct <= 0:
                    st.error(
                        f"🔴 **高价低配预警**：我方定价比友商均值高 **{price_delta_pct:+.1f}%**，"
                        f"但车长反而 {length_delta_pct:+.1f}%（更短或相当）—— 正被挤压在'高价低配'象限，"
                        f"需重新审视定价或差异化配置故事。",
                        icon="🔴"
                    )
                elif price_delta_pct <= 0:
                    st.success(
                        f"🟢 **性价比护城河**：我方定价比友商均值低 **{price_delta_pct:.1f}%**，"
                        f"车长 {length_delta_pct:+.1f}%，具备正面卡位竞争力。",
                        icon="🟢"
                    )
                else:
                    st.warning(
                        f"🟡 **定价中性**：我方定价高于友商均值 {price_delta_pct:+.1f}%，车长 {length_delta_pct:+.1f}%，"
                        f"卡位尚可但需关注渠道网点数量差距（见下方中资渠道渗透洞察）。",
                        icon="🟡"
                    )

    st.markdown("<br>", unsafe_allow_html=True)
    _sdiv("Module C · 内部专用", "中资同行渠道渗透底牌 (Chinese Brands Footprint)")
    st.markdown(f"""
<div class="footprint-card">
    <div class="footprint-card-title">🀄 Chinese Rivals Playbook — {country}</div>
    <div class="footprint-card-body">{intel['chinese_footprint']}</div>
</div>
""", unsafe_allow_html=True)
    st.caption(
        "📌 本模块数据为内部模拟情报，仅供招商/BD团队制定狙击策略参考，严禁出现在任何对外客户材料中。"
    )


def render_country_dashboard(country: str, cdata: dict):
    """
    Master renderer. Every Tier 1 country flows through the same
    4-tab structure:
        Tab 1 → 📊 Market & Risk Analytics  (Level 1+2+3; Level 2 = TCO sandbox)
        Tab 2 → 🕵️ Analyst Due Diligence    (Level 4)
        Tab 3 → 🚀 GTM Playbook              (B2B Pricing & Margin Sandbox + tactics)
        Tab 4 → 🕵️ Internal Competitive Intel (Internal Use Only — competitor
                 positioning scatter + editable spec showdown + Chinese
                 rivals channel-footprint insight)
    No country gets a bespoke page structure; only a bespoke Level-3-right
    chart via EXCLUSIVE_CHART_REGISTRY, a bespoke 'action' sentence, and
    (for most markets) bespoke 'gtm_playbook' / 'competitors' data.
    """
    tab_market, tab_dd, tab_gtm, tab_intel = st.tabs([
        "📊 Market & Risk Analytics",
        "🕵️ Analyst Due Diligence",
        "🚀 GTM Playbook",
        "🕵️ Internal Competitive Intel",
    ])

    with tab_market:
        _render_market_risk_tab(country, cdata)

    with tab_dd:
        _render_due_diligence_tab(country, cdata)

    with tab_gtm:
        _render_gtm_playbook_tab(country, cdata)

    with tab_intel:
        _render_competitive_intel_tab(country, cdata)

# ══════════════════════════════════════════════════════════════════════════════
# 12. MAP BUILDER
# ══════════════════════════════════════════════════════════════════════════════
def build_map(selected_name):
    sel_iso = next((d["iso"] for n,d in TIER1.items() if n==selected_name),"") or \
              next((iso for iso,name in ALL_AFRICA.items() if name==selected_name),"")
    rows = []
    for iso in ALL_ISO_LIST:
        name = ISO_TO_NAME.get(iso, iso)
        is_t1 = name in TIER1
        is_sel = iso == sel_iso
        score = 100 if is_sel else 70 if is_t1 else 20
        grp   = "selected" if is_sel else "tier1" if is_t1 else "base"
        if is_t1:
            d = TIER1[name]
            kpi_text = "<br>".join(f"<b>{v[0]}</b> {v[1]}" for v in d["kpi"].values())
            tip = (f"<b style='font-size:13px;'>{d['flag']} {name}</b><br>"
                   f"<span style='color:#9BA3B2;font-size:10px;'>TIER 1 · {d['region']}</span><br><br>"
                   f"{kpi_text}<br><br>"
                   f"<span style='color:#D04A02;font-size:10px;'>● Click to drill down</span>")
        else:
            m = TIER2_MACRO.get(iso, {})
            flag = m.get("flag","🌍"); region = m.get("region","Africa")
            tip = (f"<b style='font-size:13px;'>{flag} {name}</b><br>"
                   f"<span style='color:#9BA3B2;font-size:10px;'>{region}</span><br><br>"
                   f"Est. GDP: <b>${m.get('gdp','N/A')}B</b><br>"
                   f"Est. CV Imports: <b>{m.get('cv_imports','N/A'):,} units/yr</b><br>"
                   f"Road Network: <b>{m.get('roads','N/A')}k km</b><br><br>"
                   f"<span style='color:#295BA5;font-size:10px;'>● Click for live news</span>")
        rows.append({"iso":iso,"score":score,"group":grp,"tooltip":tip})

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
                locations=sub.iso, z=sub.score, text=sub.tooltip,
                hovertemplate="%{text}<extra></extra>",
                colorscale=cs, showscale=False,
                marker_line_color=lc, marker_line_width=lw, zmin=0, zmax=100))
    fig.update_layout(
        geo=dict(scope="africa", showframe=False, showcoastlines=True,
                 coastlinecolor="#C8CDD8", coastlinewidth=0.6,
                 showland=True, landcolor="#F0F2F6",
                 showocean=True, oceancolor="#E4EEF8",
                 showcountries=True, countrycolor="#C8CDD8", countrywidth=0.5,
                 bgcolor="#F4F5F7", projection_type="natural earth"),
        paper_bgcolor="#F4F5F7", plot_bgcolor="#F4F5F7",
        margin=dict(l=0,r=0,t=0,b=0), height=400,
        hoverlabel=dict(bgcolor="white", bordercolor="#E2E5EB",
                        font=dict(family="Inter", size=12, color="#2D3142")),
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
        McKinsey UX Refactor · v13.0 · 12 Markets
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
                st.cache_data.clear(); st.rerun()

    st.markdown('<div class="sb-hdr">Quick Reference</div>', unsafe_allow_html=True)
    for label, url in [
        ("📊 NAAMSA — ZA Auto Stats",    "https://naamsa.co.za"),
        ("💰 SA Treasury Budget 2026",    "https://www.treasury.gov.za"),
        ("🇷🇼 RDB — Rwanda Invest",       "https://www.rdb.rw"),
        ("⚡ ANME Tunisia — EV Subsidy",  "https://www.anme.tn"),
        ("🏛 Loi de Finances TN 2026",    "https://www.finances.gov.tn"),
        ("🌾 OCP Group Morocco",          "https://www.ocpgroup.ma"),
        ("🏛 Nigeria Customs (NCS)",      "https://www.customs.gov.ng"),
        ("⚓ DPFZA — Djibouti Ports",     "https://www.dpfza.gov.dj"),
        ("🌴 MRA — Mauritius Revenue",    "https://mra.mu"),
        ("⛏ JIRAMA — Madagascar Power",  "https://www.jirama.mg"),
        ("🌍 AfDB",                        "https://www.afdb.org"),
        ("📰 The Africa Report",          "https://www.theafricareport.com"),
    ]:
        st.markdown(f'<a class="sb-link" href="{url}" target="_blank">{label}</a>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↺  Refresh Intelligence Feed", use_container_width=True, key="refresh"):
        st.cache_data.clear(); st.rerun()
    st.markdown(f"""
<div style="font-family:'Inter';font-size:.58rem;color:rgba(255,255,255,.22);
            text-align:center;margin-top:16px;line-height:2.1;">
    Africa CV Intelligence v13.0<br>
    {datetime.now().strftime('%Y-%m-%d %H:%M')} · Internal use only
</div>
""", unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════════════════════
# 15. PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
h1, h2 = st.columns([3,1])
with h1:
    st.markdown("""
<div style="padding:18px 0 6px 0;">
    <div style="font-family:'Inter';font-size:1.28rem;font-weight:700;color:#2D3142;letter-spacing:-.3px;">
        Africa Commercial Vehicle Market Intelligence
    </div>
    <div style="font-family:'Inter';font-size:.78rem;color:#9BA3B2;margin-top:3px;">
        12 Tier 1 markets · Decision → Monetisation → Depth → Action narrative flow
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
# 16. MAP SECTION — single-column-friendly, map only (no side metrics card,
#     since all KPIs now live inside Level 1 of the dashboard below — this
#     removes one more source of side-by-side text crowding)
# ══════════════════════════════════════════════════════════════════════════════
sel     = st.session_state.selected_country
is_t1   = sel in TIER1
cdata   = TIER1.get(sel, {})
sel_iso = cdata.get("iso","") if is_t1 else next(
    (iso for iso,name in ALL_AFRICA.items() if name==sel),"")
macro   = TIER2_MACRO.get(sel_iso, {})

st.markdown("""
<div style="font-family:'Inter';font-size:.7rem;font-weight:700;letter-spacing:.8px;
            text-transform:uppercase;color:#5A6070;margin-bottom:8px;">
    Africa Strategic Market Map
    <span style="font-weight:400;color:#9BA3B2;margin-left:8px;">
        · Click any country to drill down · Orange = selected · Blue = Tier 1 (12 markets)
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
            st.cache_data.clear(); st.rerun()

leg_cols = st.columns(len(TIER1))
for lc, (cname, cd) in zip(leg_cols, TIER1.items()):
    active = cname == sel
    color  = "#D04A02" if active else "#295BA5"
    bg     = "rgba(208,74,2,0.08)" if active else "rgba(41,91,165,0.05)"
    with lc:
        st.markdown(f"""
<div style="text-align:center;padding:5px 2px;border-radius:6px;
            background:{bg};border:1px solid {'#D04A02' if active else '#E2E5EB'};">
    <div style="font-size:.85rem;">{cd['flag']}</div>
    <div style="font-family:'Inter';font-size:.55rem;font-weight:{'700' if active else '500'};
                color:{color};margin-top:1px;">{cname.split()[0]}</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 17. COUNTRY DASHBOARD — single narrative-flow tab (Task 2 + Policy tab)
# ══════════════════════════════════════════════════════════════════════════════
flag_display = cdata.get("flag", macro.get("flag","🌍")) if is_t1 else macro.get("flag","🌍")

st.markdown(f"""
<div class="section-hdr" style="margin-top:30px;">
    <div class="section-bar"></div>
    <div class="section-title">{flag_display} &nbsp;{sel} — Country Dashboard</div>
    <div class="section-sub">{"Full Tier 1 narrative-flow analysis" if is_t1 else "Tier 2 — general coverage"}</div>
</div>
""", unsafe_allow_html=True)

if not is_t1:
    st.info(f"**{sel}** is a Tier 2 market. Full narrative-flow analysis available for 12 Tier 1 core markets.", icon="ℹ️")
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Est. GDP",        "${:,.1f}B".format(macro.get("gdp",0)),  help="IMF WEO estimate")
    with m2: st.metric("Road Network",    "{:,}k km".format(macro.get("roads",0)), help="AfDB infrastructure data")
    with m3: st.metric("Est. CV Imports", "{:,} units/yr".format(macro.get("cv_imports",0)), help="Regional trade estimate")
    st.caption("Source: [AfDB](https://www.afdb.org) · [IMF WEO](https://www.imf.org) · Indicative estimates.")
else:
    tab_dashboard, tab_policy = st.tabs(["📊  Market Dashboard", "📋  Policy & Market Access"])

    with tab_dashboard:
        render_country_dashboard(sel, cdata)

    with tab_policy:
        p     = cdata["policy"]
        src_c = cdata["sources"].get("customs",("",""))
        src_m = cdata["sources"].get("market",("",""))
        src_t = cdata["sources"].get("trade",("",""))

        # Single-column policy cards (Task 1: no side-by-side long text)
        st.markdown(f'<div class="pol-card"><div class="pol-card-title">🏷 Tariff & Import Structure</div><p>{p["tariff"]}</p></div>', unsafe_allow_html=True)
        st.caption(f"Source: [{src_c[0]}]({src_c[1]})")

        st.markdown(f'<div class="pol-card ok"><div class="pol-card-title">📋 Certification & Homologation</div><p>{p["certification"]}</p></div>', unsafe_allow_html=True)
        st.caption(f"Source: [{src_m[0]}]({src_m[1]})")

        st.markdown(f'<div class="pol-card"><div class="pol-card-title">🏗 Key Buyers & Procurement Bodies</div><p>{p["key_buyers"]}</p></div>', unsafe_allow_html=True)
        st.caption(f"Source: [{src_t[0]}]({src_t[1]})")

        st.markdown(f'<div class="pol-card warn"><div class="pol-card-title">⚠ Risk Factors & Operational Considerations</div><p>{p["risk"]}</p></div>', unsafe_allow_html=True)

        _sdiv("Market Entry Assessment Scorecard")
        all_sc = {
            "Nigeria":      {"Market Size":9,"EV Readiness":7,"Tariff Advantage":9,"Regulatory Ease":5,"Growth Momentum":7},
            "South Africa": {"Market Size":8,"EV Readiness":5,"Tariff Advantage":4,"Regulatory Ease":8,"Growth Momentum":4},
            "Morocco":      {"Market Size":6,"EV Readiness":6,"Tariff Advantage":8,"Regulatory Ease":8,"Growth Momentum":8},
            "Egypt":        {"Market Size":7,"EV Readiness":3,"Tariff Advantage":5,"Regulatory Ease":5,"Growth Momentum":8},
            "Kenya":        {"Market Size":6,"EV Readiness":6,"Tariff Advantage":6,"Regulatory Ease":7,"Growth Momentum":8},
            "Ethiopia":     {"Market Size":5,"EV Readiness":9,"Tariff Advantage":9,"Regulatory Ease":6,"Growth Momentum":9},
            "Algeria":      {"Market Size":6,"EV Readiness":2,"Tariff Advantage":4,"Regulatory Ease":3,"Growth Momentum":5},
            "Tunisia":      {"Market Size":4,"EV Readiness":8,"Tariff Advantage":9,"Regulatory Ease":7,"Growth Momentum":7},
            "Rwanda":       {"Market Size":2,"EV Readiness":9,"Tariff Advantage":10,"Regulatory Ease":9,"Growth Momentum":8},
            "Djibouti":     {"Market Size":2,"EV Readiness":5,"Tariff Advantage":3,"Regulatory Ease":5,"Growth Momentum":6},
            "Mauritius":    {"Market Size":2,"EV Readiness":9,"Tariff Advantage":9,"Regulatory Ease":9,"Growth Momentum":6},
            "Madagascar":   {"Market Size":4,"EV Readiness":1,"Tariff Advantage":3,"Regulatory Ease":4,"Growth Momentum":5},
        }
        scores = all_sc.get(sel, {d:5 for d in ["Market Size","EV Readiness","Tariff Advantage","Regulatory Ease","Growth Momentum"]})
        for col, (dim, score) in zip(st.columns(5), scores.items()):
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
        <div style="background:{color};width:{min(score*10,100)}%;height:4px;border-radius:3px;"></div>
    </div>
</div>
""", unsafe_allow_html=True)
        st.caption(f"Source: [{src_t[0]}]({src_t[1]}) · Assessment based on simulated and publicly available market intelligence.")

# ══════════════════════════════════════════════════════════════════════════════
# 18. INTELLIGENCE FEED — collapsed expander at the very bottom of the page.
#     No longer a tab, no longer competing for visual attention with the
#     structured dashboard above.
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
news_query = cdata.get("news_query","") if is_t1 else f"{sel} transport logistics commercial vehicle"

with st.expander(f"📡 点击展开：{sel} 近期商业与政策情报流 / Click to expand recent intelligence", expanded=False):
    st.markdown(f"""
<div style="background:#F8F9FB;border:1px solid #E2E5EB;border-radius:8px;
            padding:11px 16px;margin-bottom:14px;font-family:'Inter';
            font-size:.76rem;color:#5A6070;line-height:1.7;">
    Sources: Reuters · Bloomberg · FT · Engineering News · BusinessDay · Zawya · Africa Report
    &nbsp;·&nbsp; Window: 30-day primary / 90-day fallback / curated insights guaranteed
    {"&nbsp;·&nbsp; <span style='color:#D04A02;'>⚠ Tier 2 — general coverage</span>" if not is_t1 else ""}
</div>
""", unsafe_allow_html=True)
    render_news_panel(news_query, sel)
    st.caption(f"Keywords used: `{news_query}` · Cache TTL: 30 minutes")

# ══════════════════════════════════════════════════════════════════════════════
# 19. FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="border-top:1px solid #E2E5EB;padding-top:14px;
            font-family:'Inter';font-size:.68rem;color:#9BA3B2;">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
        <div>
            <strong style="color:#5A6070;">Africa CV Market Intelligence Platform v13.0</strong>
            &nbsp;·&nbsp; Internal strategic use only
            &nbsp;·&nbsp; +DJ/MU/MG Strategic Expansion · TCO Sandbox Lock/Reset · B2B Margin Sandbox
        </div>
        <div style="text-align:right;">
            RDB · RURA · NAAMSA · Stats SA · National Treasury ZA · ANME TN · OCP · DPFZA · MRA · JIRAMA · Reuters · Bloomberg · AfDB
            &nbsp;·&nbsp; {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
