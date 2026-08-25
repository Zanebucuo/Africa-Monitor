"""
Africa Commercial Vehicle Market Governance & Intelligence Platform
Enterprise BI Engine v16.0
McKinsey UX Refactor — Narrative-Flow Layout · Zero Text Overlap · Collapsed Intel Feed
"""

import streamlit as st
import feedparser
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import copy
import re
import io
import html as html_lib
from urllib.request import Request, urlopen
from urllib.parse import urljoin
from datetime import datetime, timedelta

APP_VERSION = "16.2.0"
DATA_VERSION = "2026-08-25"
SCHEMA_VERSION = "1.0"
MODEL_NOTICE_EN = "Model estimate or internal judgement; not official market statistics."
MODEL_NOTICE_ZH = "模型估算或内部判断，不代表官方市场统计。"

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


# ─────────────────────────────────────────────────────────────────────────────
# V15 GLOBAL LANGUAGE LAYER
# Internal keys remain English to protect charts/data logic. Display labels
# and all new executive-governance content use this single language state.
# ─────────────────────────────────────────────────────────────────────────────
if "v15_lang" not in st.session_state:
    st.session_state.v15_lang = "zh"
V15_LANG = st.session_state.v15_lang


def tr(en: str, zh: str) -> str:
    return zh if V15_LANG == "zh" else en


V15_MODE_ZH = {
    "Scale CBU": "规模化CBU",
    "Controlled CBU": "受控CBU",
    "Project-Based CBU": "项目型CBU",
    "Validation CBU": "验证型CBU",
}


def v15_mode_label(mode: str) -> str:
    return V15_MODE_ZH.get(mode, mode) if V15_LANG == "zh" else mode


V15_PORTFOLIO = {
    "Nigeria":      {"zh":"尼日利亚","attract":82,"execute":42,"size":45200,"mode":"Project-Based CBU","role":["FX-controlled scale opportunity","外汇约束下的规模机会"]},
    "South Africa": {"zh":"南非","attract":88,"execute":55,"size":33100,"mode":"Controlled CBU","role":["Premium fleet validation","高价值车队验证"]},
    "Morocco":      {"zh":"摩洛哥","attract":78,"execute":66,"size":18200,"mode":"Controlled CBU","role":["Industrial ecosystem reference","工业生态标杆"]},
    "Egypt":        {"zh":"埃及","attract":86,"execute":38,"size":39800,"mode":"Project-Based CBU","role":["High-volume constrained market","高容量高约束市场"]},
    "Kenya":        {"zh":"肯尼亚","attract":74,"execute":61,"size":16800,"mode":"Controlled CBU","role":["East Africa urban gateway","东非城市入口"]},
    "Ethiopia":     {"zh":"埃塞俄比亚","attract":73,"execute":45,"size":14200,"mode":"Project-Based CBU","role":["Policy-led institutional EV","政策驱动机构电动车市场"]},
    "Algeria":      {"zh":"阿尔及利亚","attract":72,"execute":36,"size":20500,"mode":"Project-Based CBU","role":["Regulation-gated institution","监管门槛型机构市场"]},
    "Tunisia":      {"zh":"突尼斯","attract":65,"execute":70,"size":7600,"mode":"Validation CBU","role":["EU-standard reference","欧标合规参考"]},
    "Rwanda":       {"zh":"卢旺达","attract":58,"execute":82,"size":2800,"mode":"Validation CBU","role":["Policy showcase","政策样板"]},
    "Djibouti":     {"zh":"吉布提","attract":60,"execute":64,"size":1600,"mode":"Project-Based CBU","role":["Port-corridor niche","港口走廊细分市场"]},
    "Mauritius":    {"zh":"毛里求斯","attract":55,"execute":84,"size":1900,"mode":"Validation CBU","role":["Premium green showcase","高端绿色样板"]},
    "Madagascar":   {"zh":"马达加斯加","attract":52,"execute":30,"size":4200,"mode":"Project-Based CBU","role":["Infrastructure-constrained niche","基础设施约束型细分市场"]},
}


def v15_country_label(country: str) -> str:
    return V15_PORTFOLIO[country]["zh"] if V15_LANG == "zh" else country


# ─────────────────────────────────────────────────────────────────────────────
# V16 COMMERCIAL OPERATING LAYER
# Additive only: original market, TCO, policy, risk, triangulation and visual
# components below remain untouched. These structured tables close the loop from
# country insight to dealer, customer, opportunity and action management.
# ─────────────────────────────────────────────────────────────────────────────
V16_DEALERS = pd.DataFrame([
    ["Tunisia","Loukil Group","Target",78,"National automotive group; validate EV-CV mandate and investment appetite.","Confirm management sponsor and service investment plan","2026-09-15","Judgement","SRC-MOD-01"],
    ["Tunisia","Aures Auto / UADH","Target",70,"Potential channel case; legal-entity relationship and portfolio conflicts require verification.","Complete entity, brand and conflict map","2026-09-30","Judgement","SRC-MOD-01"],
    ["South Africa","National CV Partner","Qualified",76,"National fleet and aftersales capability subject to SLA validation.","Agree anchor-fleet pilot SLA","2026-10-15","Judgement","SRC-MOD-01"],
    ["Egypt","Institutional Import Partner","Target",64,"Importer capability depends on licence, FX access and secured settlement.","Validate licence and bank route","2026-10-31","Judgement","SRC-MOD-01"],
    ["Rwanda","EV Mobility Partner","Qualified",74,"Strong EV orientation; fleet scale and technical capacity remain gating items.","Select pilot accounts and charging scope","2026-09-30","Judgement","SRC-MOD-01"],
], columns=["Country","Dealer / Group","Relationship Stage","Partner Score","Commercial Assessment","Next Action","Deadline","Data Type","Source ID"])

V16_CUSTOMERS = pd.DataFrame([
    ["Tunisia","Tunis Urban Logistics Prospect","3PL",120,"Last-mile delivery",150,"Medium",78,"Collect route and depot-power data","Judgement","SRC-MOD-01"],
    ["Tunisia","Public Utility Prospect","Utility",200,"Service fleet",90,"High",72,"Confirm tender and replacement cycle","Judgement","SRC-MOD-01"],
    ["South Africa","National Parcel Fleet Prospect","3PL",850,"Parcel delivery",180,"Medium",88,"Build 20-unit pilot TCO and SLA","Judgement","SRC-MOD-01"],
    ["Egypt","State-linked Fleet Prospect","Institutional",500,"Service fleet",120,"Low",65,"Verify funding and import pathway","Judgement","SRC-MOD-01"],
    ["Rwanda","Kigali Delivery Prospect","Delivery",80,"Urban delivery",100,"High",80,"Confirm depot charging design","Judgement","SRC-MOD-01"],
], columns=["Country","Customer","Type","Fleet Size","Application","Daily km","Charging Readiness","Fit Score","Next Action","Data Type","Source ID"])

V16_OPPORTUNITIES = pd.DataFrame([
    ["Tunisia","Tunis last-mile pilot","Electric LCV","Pilot",20,38000,.55,"2027-03-31","Medium","Complete route TCO","2026-09-30"],
    ["Tunisia","Utility fleet validation","Electric LCV","Qualified",30,39000,.25,"2027-06-30","Medium","Confirm tender calendar","2026-10-15"],
    ["South Africa","National parcel pilot","Large electric van","Proposal",50,52000,.40,"2027-04-30","Medium","Submit pilot SLA","2026-10-15"],
    ["Egypt","Institutional fleet project","Electric LCV","Research",100,35000,.05,"2027-12-31","High","Validate FX allocation","2026-10-31"],
    ["Rwanda","Kigali showcase","Compact electric van","Negotiation",15,32000,.70,"2027-02-28","Low","Close charging scope","2026-09-15"],
], columns=["Country","Project","Vehicle","Stage","Expected Units","Unit Value USD","Probability","Expected Close","Risk","Next Action","Next Action Date"])

V16_ACTIONS = pd.DataFrame([
    ["Tunisia","Regulation","Obtain written homologation checklist","P0","Homologation","2026-09-15","Open","Approved document checklist"],
    ["Tunisia","Channel","Complete Loukil / Aures scorecard","P0","Country Manager","2026-09-30","Open","Partner recommendation"],
    ["Tunisia","Customer","Collect duty cycle from two anchor fleets","P0","Country Manager","2026-10-15","Open","Route-based TCO"],
    ["South Africa","Customer","Define national parcel pilot","P0","Country Manager","2026-10-15","Open","Vehicle SLA and trial plan"],
    ["Egypt","Finance","Validate secured FX and payment route","P0","Finance","2026-10-31","Open","Written payment structure"],
    ["Rwanda","Pilot","Close depot charging scope","P1","Country Manager","2026-09-15","Open","Charging BOQ"],
], columns=["Country","Workstream","Action","Priority","Owner","Deadline","Status","Expected Output"])

V16_SOURCES = pd.DataFrame([
    ["SRC-TN-01","Tunisia","Institut National de la Statistique","https://www.ins.tn/statistiques/117","Government","2024-12-31","A","Transport statistics","Exact downloadable table preferred"],
    ["SRC-TN-02","Tunisia","Tunisian Customs — vehicle taxation","https://www.douane.gov.tn/taxationveh/","Government","2026-01-01","A","Tax and customs","Confirm HS code and treatment in writing"],
    ["SRC-TN-03","Tunisia","OCT — rolling-equipment concessionaires","https://www.oct.gov.tn/fr/concessionnaire-materiels-roulants","Government","2026-01-01","A","Dealer authorisation","Confirm licence scope"],
    ["SRC-TN-04","Tunisia","ATTT","https://www.attt.com.tn/","Government","2026-01-01","A","Registration and homologation","Replace homepage with exact procedure when obtained"],
    ["SRC-TN-05","Tunisia","Automobile.tn — 2024 VUL market","https://www.automobile.tn/fr/magazine/actu/2025-02-03-le-marche-des-vehicules-utilitaires-legers-en-tunisie-en-2024.html","Media","2025-02-03","B","VUL market","Secondary source"],
    ["SRC-TN-06","Tunisia","Fiat Professional Tunisia 2024","https://www.media.stellantis.com/me-en/fiat-professional/press/fiat-professional-achieves-record-market-share-in-tunisia-in-2024","OEM","2025-02-01","B","Brand registrations","OEM-reported"],
    ["SRC-MCK-01","Cross-market","McKinsey — EV adoption in LCV","https://www.mckinsey.com/industries/automotive-and-assembly/our-insights/built-for-purpose-ev-adoption-in-light-commercial-vehicles","Consulting","2022-09-01","B","TCO duty-cycle method","Method only; not a country statistic"],
    ["SRC-MOD-01","Cross-market","Internal V16 planning model","","Internal","2026-07-30","D","Commercial assumptions","Not official statistics"],
], columns=["Source ID","Country","Source Name","Source URL","Source Type","Publication Date","Confidence","Scope","Audit Note"])

V16_METRIC_AUDIT = pd.DataFrame([
    ["Tunisia","VUL registration growth",14,"%","2024","Reported","B","SRC-TN-05","2026-07-29"],
    ["Tunisia","Fiat Professional registrations",1596,"units","2024","Reported","B","SRC-TN-06","2026-07-29"],
    ["Tunisia","Fiat Professional share",21,"%","2024","Reported","B","SRC-TN-06","2026-07-29"],
    ["Tunisia","Addressable annual CBU EV volume",150,"units","2027","Modelled","D","SRC-MOD-01","2026-07-29"],
    ["South Africa","Commercial-vehicle opportunity pool",33100,"units","2025","Estimated","C","SRC-MOD-01","2026-07-29"],
    ["Egypt","Commercial-vehicle opportunity pool",39800,"units","2025","Estimated","D","SRC-MOD-01","2026-07-29"],
    ["Rwanda","Addressable EV-van pilot",20,"units","2027","Modelled","D","SRC-MOD-01","2026-07-29"],
], columns=["Country","Metric","Value","Unit","Period","Data Type","Confidence","Source ID","Updated At"])



# ─────────────────────────────────────────────────────────────────────────────
# V16.2 AUTO MARKET DATA ENGINE — trial deployment
# Purpose: refresh selected authoritative market metrics without allowing a failed
# scraper to overwrite management data. Auto data is displayed separately and can
# later be promoted into the audited metric register after validation.
# ─────────────────────────────────────────────────────────────────────────────
AUTO_MARKET_SOURCE_CONFIG = {
    "South Africa": {
        "frequency": "Monthly",
        "source_name": "naamsa | The Automotive Business Council",
        "landing_url": "https://naamsa.net/newsroom/?nocache=1",
        "confidence": "A",
        "mode": "auto",
    },
    "Tunisia": {
        "frequency": "Annual",
        "source_name": "Automobile.tn (ATTT registration data)",
        "landing_url": "https://www.automobile.tn/fr/magazine/enquetes/2026-01-09-statistiques-des-immatriculations-2025.html",
        "confidence": "B",
        "mode": "auto",
    },
    "Kenya": {
        "frequency": "Annual",
        "source_name": "Kenya National Bureau of Statistics — Economic Survey",
        "landing_url": "https://www.knbs.or.ke/wp-content/uploads/2026/04/2026-Economic-Survey.pdf",
        "confidence": "A",
        "mode": "auto",
    },
}

_AUTO_COLUMNS = [
    "Country", "Metric", "Value", "Unit", "Period", "Data Type", "Confidence",
    "Source Name", "Source URL", "Retrieved At", "Auto Status"
]


def _auto_empty(country: str, status: str, source_url: str = "", source_name: str = "") -> pd.DataFrame:
    return pd.DataFrame([{
        "Country": country,
        "Metric": "Auto refresh status",
        "Value": None,
        "Unit": "",
        "Period": "",
        "Data Type": "System",
        "Confidence": "—",
        "Source Name": source_name,
        "Source URL": source_url,
        "Retrieved At": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "Auto Status": status,
    }], columns=_AUTO_COLUMNS)


def _http_bytes(url: str, timeout: int = 18) -> bytes:
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; AfricaCVMonitor/16.2; +market-intelligence)",
        "Accept": "text/html,application/pdf,application/xhtml+xml,*/*;q=0.8",
    })
    with urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _html_to_text(raw: bytes) -> str:
    text = raw.decode("utf-8", errors="ignore")
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", text)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = html_lib.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def _int_token(token: str) -> int:
    return int(re.sub(r"[^0-9]", "", token))


def _pdf_text(raw: bytes) -> str:
    """PDF extraction is optional so the app still runs if pypdf is not installed."""
    try:
        from pypdf import PdfReader
    except Exception as exc:
        raise RuntimeError("pypdf dependency missing; add pypdf>=4.0 to requirements.txt") from exc
    reader = PdfReader(io.BytesIO(raw))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def _metric_row(country, metric, value, unit, period, confidence, source_name, source_url, status="Live parsed"):
    return {
        "Country": country,
        "Metric": metric,
        "Value": value,
        "Unit": unit,
        "Period": period,
        "Data Type": "Reported",
        "Confidence": confidence,
        "Source Name": source_name,
        "Source URL": source_url,
        "Retrieved At": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "Auto Status": status,
    }


def _fetch_tunisia_auto() -> pd.DataFrame:
    country = "Tunisia"
    cfg = AUTO_MARKET_SOURCE_CONFIG[country]
    url = cfg["landing_url"]
    try:
        text = _html_to_text(_http_bytes(url))
        rows = []
        patterns = [
            ("Camionnettes / utility registrations", r"Camionnettes\s*\(VU\).*?([0-9][0-9\s]{2,})\s+([0-9][0-9\s]{2,})\s*\+?([0-9,.]+)%"),
            ("Total VU market", r"Total\s+March[eé]\s+VU\s+([0-9][0-9\s]{2,})\s+([0-9][0-9\s]{2,})\s*\+?([0-9,.]+)%"),
            ("Total vehicle market", r"Total\s+March[eé]\s+([0-9][0-9\s]{2,})\s+([0-9][0-9\s]{2,})\s*\+?([0-9,.]+)%"),
        ]
        for metric, pat in patterns:
            m = re.search(pat, text, flags=re.I)
            if not m:
                continue
            cur, prev = _int_token(m.group(1)), _int_token(m.group(2))
            rows.append(_metric_row(country, metric, cur, "units", "2025", cfg["confidence"], cfg["source_name"], url))
            rows.append(_metric_row(country, metric + " — previous", prev, "units", "2024", cfg["confidence"], cfg["source_name"], url))
        if not rows:
            return _auto_empty(country, "Source reachable but expected registration fields were not parsed; review parser.", url, cfg["source_name"])
        return pd.DataFrame(rows, columns=_AUTO_COLUMNS)
    except Exception as exc:
        return _auto_empty(country, f"Refresh failed: {type(exc).__name__}: {exc}", url, cfg["source_name"])


def _discover_naamsa_latest_pdf() -> str:
    landing = AUTO_MARKET_SOURCE_CONFIG["South Africa"]["landing_url"]
    raw = _http_bytes(landing)
    html_text = raw.decode("utf-8", errors="ignore")
    # Prefer FLASH standard monthly file. The YYYYMM portion makes lexical max reliable.
    candidates = re.findall(r'href=["\']([^"\']*FLASH_STD_20\d{4}\.pdf)["\']', html_text, flags=re.I)
    if not candidates:
        # Some WordPress pages expose absolute URLs without a quoted href in cached markup.
        candidates = re.findall(r'https?://[^\s"\']*FLASH_STD_20\d{4}\.pdf', html_text, flags=re.I)
    if not candidates:
        raise RuntimeError("Latest naamsa monthly FLASH PDF was not discovered on newsroom page")
    abs_urls = [urljoin(landing, c) for c in candidates]
    def key(u: str):
        m = re.search(r"FLASH_STD_(20\d{4})\.pdf", u, flags=re.I)
        return m.group(1) if m else "000000"
    return max(abs_urls, key=key)


def _fetch_south_africa_auto() -> pd.DataFrame:
    country = "South Africa"
    cfg = AUTO_MARKET_SOURCE_CONFIG[country]
    try:
        pdf_url = _discover_naamsa_latest_pdf()
        ym = re.search(r"FLASH_STD_(20\d{4})\.pdf", pdf_url, flags=re.I)
        period = ym.group(1) if ym else "Latest month"
        raw = _http_bytes(pdf_url)
        text = re.sub(r"\s+", " ", _pdf_text(raw))
        rows = []
        # Parse current-month local volumes from the Market-at-a-Glance table.
        specs = [
            ("Passenger vehicle sales", r"Passenger\s+([0-9][0-9\s]{2,})\s+[0-9][0-9\s]{2,}"),
            ("Light CV <3501kg sales", r"Light\s+CV\s*<\s*3501kg\s+([0-9][0-9\s]{2,})\s+[0-9][0-9\s]{1,}"),
            ("Medium CV 3501-8500kg sales", r"Medium\s+CV\s+3501\s*[-–]\s*8500kg\s+([0-9][0-9\s]{1,})\s+[0-9][0-9\s]{0,}"),
            ("Industry total vehicle sales", r"Industry\s+Total\s+([0-9][0-9\s]{2,})\s+[0-9][0-9\s]{2,}"),
        ]
        for metric, pat in specs:
            m = re.search(pat, text, flags=re.I)
            if m:
                rows.append(_metric_row(country, metric, _int_token(m.group(1)), "units", period, cfg["confidence"], cfg["source_name"], pdf_url))
        # Heavy CV family: add three sub-segments if present.
        for metric, pat in [
            ("Heavy CV 8501-16500kg sales", r"Heavy\s+CV\s+8501\s*[-–]\s*16500kg\s+([0-9][0-9\s]{1,})"),
            ("Extra Heavy CV >16500kg sales", r"Extra\s+Heavy\s+CV\s*>\s*16500kg\s+([0-9][0-9\s]{1,})"),
            ("Bus >8500kg sales", r"Bus\s*>\s*8500kg\s+([0-9][0-9\s]{1,})"),
        ]:
            m = re.search(pat, text, flags=re.I)
            if m:
                rows.append(_metric_row(country, metric, _int_token(m.group(1)), "units", period, cfg["confidence"], cfg["source_name"], pdf_url))
        if not rows:
            return _auto_empty(country, "Latest naamsa report discovered, but expected sales rows were not parsed.", pdf_url, cfg["source_name"])
        return pd.DataFrame(rows, columns=_AUTO_COLUMNS)
    except Exception as exc:
        return _auto_empty(country, f"Refresh failed: {type(exc).__name__}: {exc}", cfg["landing_url"], cfg["source_name"])


def _fetch_kenya_auto() -> pd.DataFrame:
    country = "Kenya"
    cfg = AUTO_MARKET_SOURCE_CONFIG[country]
    url = cfg["landing_url"]
    try:
        raw = _http_bytes(url, timeout=25)
        text = re.sub(r"\s+", " ", _pdf_text(raw))
        rows = []
        # 2026 Economic Survey table 13.4 contains 2021–2025 columns; the last
        # numeric token in each row is the latest (2025 provisional) value.
        specs = [
            ("Panel vans & pick-ups registrations", r"Panel\s+Vans,?\s*Pick-ups,?\s*etc\s+((?:[0-9,]+\s+){3,6}[0-9,]+)"),
            ("Lorries / trucks registrations", r"Lorries/Trucks\s+((?:[0-9,]+\s+){3,6}[0-9,]+)"),
            ("Buses & coaches registrations", r"Buses\s+and\s+Coaches\s+((?:[0-9,]+\s+){3,6}[0-9,]+)"),
            ("Mini-buses / Matatu registrations", r"Mini-Buses/Matatu\s+((?:[0-9,]+\s+){3,6}[0-9,]+)"),
            ("Total motor vehicle registrations", r"Total\s+Motor\s+Vehicles\s+((?:[0-9,]+\s+){3,6}[0-9,]+)"),
        ]
        for metric, pat in specs:
            m = re.search(pat, text, flags=re.I)
            if not m:
                continue
            nums = re.findall(r"[0-9][0-9,]*", m.group(1))
            if nums:
                rows.append(_metric_row(country, metric, _int_token(nums[-1]), "units", "2025*", cfg["confidence"], cfg["source_name"], url))
        if not rows:
            return _auto_empty(country, "KNBS survey downloaded but Table 13.4 could not be parsed; review parser.", url, cfg["source_name"])
        return pd.DataFrame(rows, columns=_AUTO_COLUMNS)
    except Exception as exc:
        return _auto_empty(country, f"Refresh failed: {type(exc).__name__}: {exc}", url, cfg["source_name"])


@st.cache_data(ttl=21600, show_spinner=False)
def fetch_auto_market_data(country: str) -> pd.DataFrame:
    """Return live-parsed market metrics for supported trial countries.

    Safety rule: this function never mutates V15_PORTFOLIO, TIER1 or V16_METRIC_AUDIT.
    Auto data remains a separate evidence layer until reviewed.
    """
    if country == "South Africa":
        return _fetch_south_africa_auto()
    if country == "Tunisia":
        return _fetch_tunisia_auto()
    if country == "Kenya":
        return _fetch_kenya_auto()
    return _auto_empty(country, "No automatic market-sales adapter configured for this country yet.")


def _auto_market_health(df: pd.DataFrame) -> tuple[str, int, int]:
    if df.empty:
        return "Unavailable", 0, 0
    usable = df[(df["Data Type"] == "Reported") & pd.to_numeric(df["Value"], errors="coerce").notna()]
    errors = df[df["Metric"] == "Auto refresh status"]
    if not usable.empty:
        return "Live", len(usable), len(errors)
    return "Needs attention", 0, len(errors)


def render_auto_market_data_panel(country: str):
    """Small trial panel used inside Data Governance; does not disturb legacy pages."""
    cfg = AUTO_MARKET_SOURCE_CONFIG.get(country)
    _sdiv(tr("Auto Market Data — Trial", "自动市场数据 — 试运行"))
    if cfg is None:
        st.info(tr(
            "No automatic registration/sales source has been configured for this market yet.",
            "该市场尚未配置自动销量/注册量数据源。",
        ))
        return

    top = st.columns([1.2, 1, 1, 1.2])
    with top[0]:
        st.caption(tr("Primary source", "主要来源"))
        st.markdown(f"**{cfg['source_name']}**")
    with top[1]:
        st.caption(tr("Refresh cadence", "刷新频率"))
        st.markdown(f"**{cfg['frequency']}**")
    with top[2]:
        st.caption(tr("Confidence", "可信度"))
        st.markdown(f"**{cfg['confidence']}**")
    with top[3]:
        if st.button(tr("Refresh auto data", "刷新自动数据"), key=f"auto_refresh_{country}"):
            fetch_auto_market_data.clear()
            st.rerun()

    with st.spinner(tr("Checking authoritative market source…", "正在检查权威市场数据源…")):
        auto_df = fetch_auto_market_data(country)
    health, metric_count, error_count = _auto_market_health(auto_df)
    c1, c2, c3 = st.columns(3)
    c1.metric(tr("Auto status", "自动状态"), health)
    c2.metric(tr("Live metrics", "实时指标"), metric_count)
    c3.metric(tr("Parser alerts", "解析提醒"), error_count)

    if metric_count:
        st.success(tr(
            "Live values were parsed from the source. They remain separate from audited management metrics until reviewed.",
            "已从来源实时解析数据；在人工复核前，不会覆盖正式管理指标。",
        ))
    else:
        st.warning(tr(
            "No live metric was promoted. Existing dashboard values remain unchanged.",
            "本次未获得可用实时指标，现有看板数据不会被覆盖。",
        ))

    st.dataframe(
        auto_df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Source URL": st.column_config.LinkColumn(
                tr("Source URL", "来源链接"), display_text=tr("Open source", "打开来源")
            )
        },
    )
    st.caption(tr(
        "Trial rule: auto-refresh is an evidence layer, not an automatic write-back. Promote into V16_METRIC_AUDIT only after the source, scope and period are verified.",
        "试运行规则：自动刷新仅作为证据层，不自动回写正式指标。确认来源、口径和数据期后，再迁移至 V16_METRIC_AUDIT。",
    ))

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
# 7. LIVE INTELLIGENCE ENGINE v2 — recency-first, scored, no stale fallback
# ══════════════════════════════════════════════════════════════════════════════
# Design rule:
#   0–30d  -> Current Intelligence (default feed)
#   31–90d -> Watchlist / Context only
#   >90d   -> Never shown as "recent news"
# No hard-coded curated fallback is injected into the live feed. Empty is safer
# than stale: if nothing relevant is found, the UI says so explicitly.
# ══════════════════════════════════════════════════════════════════════════════
AUTHORITY_DOMAINS = [
    "reuters","bloomberg","ft.com","engineeringnews","businessday",
    "zawya","theafricareport","africanews","afdb","apanews",
    "naamsa","naddc","statssa","moti.gov","finances.gov.tn","anme.tn",
    "rdb.rw","rura.rw","newtimes.co.rw","ktpress.rw",
    "dpfza.gov.dj","mra.mu","jirama.mg","gov.","gouv.","customs",
    "ministry","ministere","ministère","revenue authority","statistics",
]
NOISE_WORDS = {
    "rumor","rumour","unconfirmed","alleged","shocking","viral",
    "leaked","clickbait","celebrity","football","soccer","music",
}

INTEL_CATEGORY_KEYWORDS = {
    "Regulation": [
        "regulation","policy","law","tax","duty","vat","customs","import",
        "homologation","certification","standard","quota","licence","license",
        "registration","tariff","subsidy","incentive","ban","emission",
    ],
    "Tender": [
        "tender","rfp","procurement","bid","contract award","purchase order",
        "fleet renewal","government purchase","public procurement",
    ],
    "Dealer": [
        "dealer","distributor","distribution agreement","agency","agent",
        "showroom","service centre","service center","exclusive distributor",
        "partner","dealership",
    ],
    "Competitor": [
        "foton","jac","maxus","saic","dongfeng","byd","sinotruk","yutong",
        "toyota","ford","nissan","mercedes","isuzu","iveco","renault",
        "geely","farizon","zeekr","changan","chery","great wall","gwm",
    ],
    "Fleet Customer": [
        "fleet","logistics","delivery","parcel","courier","mining","utility",
        "airport","hotel","bus operator","transport company","last mile",
    ],
    "Infrastructure": [
        "charging","charger","charging station","grid","electricity","depot",
        "renewable","power supply","ev infrastructure",
    ],
    "FX & Economy": [
        "exchange rate","forex","fx","currency","inflation","interest rate",
        "central bank","foreign exchange","devaluation","import financing",
    ],
    "Automotive Market": [
        "vehicle sales","registrations","automotive market","commercial vehicle",
        "light commercial","truck sales","van sales","vehicle market",
    ],
}

INTEL_ACTIONS = {
    "Regulation": (
        "Confirm the exact legal text / effective date and update market-access assumptions.",
        "核对法规原文、生效日期及适用车型，并同步更新准入假设。",
    ),
    "Tender": (
        "Qualify buyer, deadline, technical specification and procurement route; decide bid/no-bid.",
        "核实采购主体、截止时间、技术规格与采购路径，并形成投标/不投标判断。",
    ),
    "Dealer": (
        "Update partner/conflict map and assess whether this changes channel priority or exclusivity risk.",
        "更新渠道及品牌冲突图谱，判断是否影响合作伙伴优先级或排他风险。",
    ),
    "Competitor": (
        "Update competitor PVA, local price/channel evidence and the affected customer segment.",
        "更新竞品PVA、当地价格/渠道证据，并识别受影响客户场景。",
    ),
    "Fleet Customer": (
        "Check fleet size, replacement cycle and duty cycle; convert the signal into a named opportunity if qualified.",
        "核实车队规模、换车周期与工况；若成立则转为实名项目机会。",
    ),
    "Infrastructure": (
        "Re-test depot-charging feasibility and TCO assumptions for the affected route or customer.",
        "重新验证相关客户/线路的充电可行性及TCO假设。",
    ),
    "FX & Economy": (
        "Re-test landed cost, payment security and FX sensitivity before quoting or stocking.",
        "重新验证落地成本、付款安全及汇率敏感性，再决定报价或备库。",
    ),
    "Automotive Market": (
        "Validate the data scope and update market sizing / competitor share only if the source is sufficiently robust.",
        "先核实数据口径与来源强度，再决定是否更新市场规模或竞品份额。",
    ),
    "General": (
        "Review relevance with the country owner before changing any market assumption.",
        "由国家负责人确认业务相关性后，再调整任何市场假设。",
    ),
}

COUNTRY_INTEL_TERMS = {
    "Tunisia": [
        'automobile registration OR vehicle registration OR immatriculation',
        'commercial vehicle OR light commercial vehicle OR véhicule utilitaire',
        'electric vehicle OR véhicule électrique OR charging',
        'vehicle import OR customs OR douane OR homologation OR ATTT OR OCT',
        'Loukil OR UADH OR Aures Auto OR Ennakl OR Automobile.tn',
        'fleet tender OR appel offres vehicle OR marché public véhicule',
        'Foton OR JAC OR Maxus OR BYD OR Dongfeng OR Farizon',
    ],
    "South Africa": [
        'commercial vehicle OR light commercial vehicle OR truck market',
        'electric commercial vehicle OR electric van OR fleet electrification',
        'NAAMSA OR vehicle sales OR vehicle registration',
        'fleet tender OR logistics fleet OR parcel fleet',
        'Foton OR JAC OR Maxus OR BYD OR Dongfeng OR Farizon',
        'charging infrastructure OR Eskom OR electricity tariff',
    ],
    "Egypt": [
        'commercial vehicle OR truck market OR van market',
        'electric vehicle OR electric commercial vehicle',
        'vehicle import OR customs OR automotive regulation OR AIDP',
        'fleet tender OR public procurement vehicle',
        'Foton OR JAC OR Maxus OR BYD OR Dongfeng OR Farizon',
        'foreign exchange OR vehicle import financing',
    ],
    "Rwanda": [
        'electric vehicle OR electric commercial vehicle OR e-mobility',
        'RURA OR RDB OR vehicle tax OR vehicle import',
        'fleet tender OR public transport OR logistics fleet',
        'charging infrastructure OR electricity tariff',
        'BYD OR Foton OR Yutong OR Farizon',
    ],
    "Morocco": [
        'commercial vehicle OR véhicule utilitaire OR truck market',
        'electric vehicle OR véhicule électrique',
        'vehicle import OR homologation OR customs OR douane',
        'AIVAM OR vehicle registration',
        'dealer OR distributor OR automobile group',
        'Foton OR JAC OR Maxus OR BYD OR Dongfeng OR Farizon',
        'fleet tender OR appel offres véhicule',
    ],
}


def _intel_queries(country: str, base_query: str = "") -> list[str]:
    """Build a country-specific query portfolio instead of one generic RSS query."""
    terms = COUNTRY_INTEL_TERMS.get(country, [
        'commercial vehicle OR truck OR van',
        'electric vehicle OR fleet electrification',
        'vehicle import OR customs OR homologation',
        'fleet tender OR vehicle procurement',
        'Foton OR JAC OR Maxus OR BYD OR Dongfeng OR Farizon',
    ])
    queries = []
    if base_query:
        queries.append(base_query)
    queries.extend(f'"{country}" ({term})' for term in terms)
    # Deduplicate while preserving order; cap calls to protect page latency.
    return list(dict.fromkeys(q.strip() for q in queries if q.strip()))[:7]


def _intel_category(title: str) -> str:
    low = title.lower()
    scores = {
        cat: sum(1 for kw in kws if kw in low)
        for cat, kws in INTEL_CATEGORY_KEYWORDS.items()
    }
    best = max(scores, key=scores.get) if scores else "General"
    return best if scores.get(best, 0) > 0 else "General"


def _intel_relevance(title: str) -> int:
    low = title.lower()
    strong = [
        "commercial vehicle","truck","van","fleet","vehicle","automotive",
        "electric","ev","dealer","distributor","tender","procurement",
        "customs","homologation","charging","logistics",
    ]
    hits = sum(1 for kw in strong if kw in low)
    return min(100, 35 + hits * 13) if hits else 20


def _intel_authority(item: dict) -> int:
    hay = f"{item.get('link','')} {item.get('source','')}".lower()
    if any(d in hay for d in AUTHORITY_DOMAINS):
        return 100
    if any(x in hay for x in ["official", "ministry", "authority", "government", "group", "motors"]):
        return 80
    return 55


def _intel_recency(pub_dt: datetime | None, now: datetime) -> int:
    if pub_dt is None:
        return 0
    age = max(0, (now - pub_dt).days)
    if age <= 7:
        return 100
    if age <= 14:
        return 90
    if age <= 30:
        return 78
    if age <= 60:
        return 55
    if age <= 90:
        return 40
    return 0


def _intel_impact(category: str, title: str) -> int:
    high = {"Regulation", "Tender", "Dealer"}
    medium = {"Competitor", "Fleet Customer", "Infrastructure", "FX & Economy"}
    score = 90 if category in high else 75 if category in medium else 55
    low = title.lower()
    if any(x in low for x in ["ban", "exclusive", "award", "tender", "tax", "duty", "homologation", "subsidy"]):
        score = min(100, score + 10)
    return score


def _intel_business_implication(category: str) -> str:
    pair = INTEL_ACTIONS.get(category, INTEL_ACTIONS["General"])
    return pair[1 if V15_LANG == "zh" else 0]


def _intel_score(item: dict, now: datetime) -> int:
    recency = _intel_recency(item.get("pub_dt"), now)
    relevance = _intel_relevance(item.get("title", ""))
    authority = _intel_authority(item)
    impact = _intel_impact(item.get("category", "General"), item.get("title", ""))
    return round(recency * .30 + relevance * .30 + authority * .20 + impact * .20)


def _parse_google_news(url: str) -> list[dict]:
    try:
        feed = feedparser.parse(url)
        out = []
        for e in feed.entries:
            title = (e.get("title", "") or "").strip()
            if not title or any(n in title.lower() for n in NOISE_WORDS):
                continue
            pub_dt = None
            if getattr(e, "published_parsed", None):
                pub_dt = datetime(*e.published_parsed[:6])
            # Unknown publication dates are intentionally rejected from the live feed.
            if pub_dt is None:
                continue
            source = e.get("source", {}) or {}
            source_name = source.get("title", "–") if isinstance(source, dict) else "–"
            out.append({
                "title": title,
                "link": e.get("link", "#"),
                "published": pub_dt.strftime("%Y-%m-%d"),
                "pub_dt": pub_dt,
                "source": source_name,
            })
        return out
    except Exception:
        return []


@st.cache_data(ttl=900, show_spinner=False)
def fetch_news(query: str, country: str = "", limit: int = 8) -> dict:
    """Fetch and score business intelligence. Never backfills stale hard-coded news."""
    from urllib.parse import quote_plus

    now = datetime.utcnow()
    cutoff_30 = now - timedelta(days=30)
    cutoff_90 = now - timedelta(days=90)
    collected = []

    for q in _intel_queries(country, query):
        encoded = quote_plus(f"{q} when:90d")
        url = f"https://news.google.com/rss/search?q={encoded}&hl=en-US&gl=US&ceid=US:en"
        collected.extend(_parse_google_news(url))

    # De-duplicate syndication / repeated Google News entries by normalized title.
    unique = {}
    for item in collected:
        key = re.sub(r"[^a-z0-9]+", " ", item["title"].lower()).strip()
        if not key:
            continue
        old = unique.get(key)
        if old is None or item["pub_dt"] > old["pub_dt"]:
            unique[key] = item

    scored = []
    for item in unique.values():
        item = item.copy()
        item["category"] = _intel_category(item["title"])
        item["score"] = _intel_score(item, now)
        item["authority_score"] = _intel_authority(item)
        item["implication"] = _intel_business_implication(item["category"])
        scored.append(item)

    current = [
        x for x in scored
        if x["pub_dt"] >= cutoff_30 and x["score"] >= 58
    ]
    watch = [
        x for x in scored
        if cutoff_90 <= x["pub_dt"] < cutoff_30 and x["score"] >= 65
    ]
    current.sort(key=lambda x: (x["score"], x["pub_dt"]), reverse=True)
    watch.sort(key=lambda x: (x["score"], x["pub_dt"]), reverse=True)

    return {
        "items": current[:limit],
        "watch_items": watch[:5],
        "is_authority": bool(current) and all(x["authority_score"] >= 80 for x in current[:3]),
        "is_fallback": False,
        "as_of": now.strftime("%Y-%m-%d %H:%M UTC"),
        "queries_run": len(_intel_queries(country, query)),
    }


def _is_auth(item):
    return _intel_authority(item) >= 80


def render_news_panel(query: str, country: str):
    with st.spinner(tr(f"Fetching live intelligence for {country}...", f"正在获取 {country} 最新市场情报...")):
        result = fetch_news(query, country=country)

    items = result["items"]
    watch_items = result.get("watch_items", [])

    current_label = tr("CURRENT · ≤30D", "最新 · ≤30天")
    st.markdown('<div class="news-wrap">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="news-hdr"><span class="news-hdr-title">📡 &nbsp;{country} — '
        f'{tr("Live Commercial Intelligence", "实时商业情报")}</span>'
        f'<span class="news-badge">{current_label}</span></div>',
        unsafe_allow_html=True,
    )

    if not items:
        st.markdown(
            '<div class="news-empty">'
            + tr(
                "No high-value intelligence published in the last 30 days met the quality threshold. "
                "The system will not backfill old curated stories as current news.",
                "过去30天未检索到达到质量阈值的高价值新增情报。系统不会再用旧的人工整理信息冒充近期新闻。",
            )
            + '</div>',
            unsafe_allow_html=True,
        )
    else:
        for item in items:
            sc = "news-src" if _is_auth(item) else "news-fb-src"
            category = item.get("category", "General")
            score = item.get("score", 0)
            st.markdown(
                f'<div class="news-item">'
                f'<a class="news-title-a" href="{item["link"]}" target="_blank">{item["title"]}</a>'
                f'<div class="news-meta"><span class="{sc}">{item["source"]}</span>'
                f'{item["published"]} &nbsp;·&nbsp; {category} &nbsp;·&nbsp; Intel {score}/100</div>'
                f'<div style="font-family:Inter;font-size:.72rem;color:#5A6070;margin-top:7px;line-height:1.55;">'
                f'<b>{tr("Action:", "建议动作：")}</b> {item["implication"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption(
        tr(
            f"As of {result['as_of']} · {result['queries_run']} country-specific query groups · "
            "30-day live feed only · scores combine recency, relevance, source authority and business impact.",
            f"更新时间 {result['as_of']} · 已运行 {result['queries_run']} 组国家定向检索 · "
            "主情报流仅保留30天内内容 · 评分综合时效性、相关性、来源权威性与业务影响。",
        )
    )

    if watch_items:
        with st.expander(tr("Watchlist · 31–90 days (context only)", "观察列表 · 31–90天（仅作背景）"), expanded=False):
            watch_df = pd.DataFrame([{
                tr("Date", "日期"): x["published"],
                tr("Category", "类别"): x["category"],
                tr("Headline", "事件"): x["title"],
                tr("Source", "来源"): x["source"],
                tr("Score", "情报评分"): x["score"],
            } for x in watch_items])
            st.dataframe(watch_df, hide_index=True, use_container_width=True)
            st.caption(tr(
                "Watchlist items are intentionally excluded from the current-news feed.",
                "观察列表内容不会进入“最新新闻”主情报流。",
            ))
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
# ══════════════════════════════════════════════════════════════════════════════
# EXECUTIVE GOVERNANCE LAYER
# These fields are merged into every TIER1 country record so all downstream
# renderers consume one consistent country object.
# CBU is the group-wide primary export mode. CKD is never the default verdict;
# it is retained only as a staged risk-mitigation option where conditions justify it.
# ══════════════════════════════════════════════════════════════════════════════
GOVERNANCE_DATA = {
    "Nigeria": {
        "strategic_guardrails": {
            "red_lines": [
                "Do not treat the 0% EV tariff as proof of bankable demand. No unsecured NGN-denominated receivables, open-ended price validity, or shipment without verified hard-currency settlement.",
                "Do not scale CBU inventory through Apapa before confirming port dwell time, homologation responsibility, spare-parts readiness, and a named fleet off-taker.",
                "Do not position long-haul electric tractors as a nationwide solution while grid reliability and route charging remain unproven."
            ],
            "green_zone": "CBU remains the primary entry route: use controlled batches for USD-funded corporate fleets on closed urban or depot-return routes. Release each batch only against secured payment, service capacity, and verified utilisation."
        },
        "market_mechanics": {
            "market_access": "SON/NAFDAC requirements and Form M discipline matter, but foreign-exchange access is the real gate. A tariff advantage has no value if the buyer cannot obtain USD or clear the vehicle predictably.",
            "channel_ecosystem": "Demand is concentrated in large industrial groups, distributors and public-linked fleets. Dealer reach matters for service, yet creditworthy anchor fleets—not fragmented retail—should determine market entry.",
            "value_pool": "The bankable EV pool sits in high-mileage, depot-return FMCG and industrial distribution. Long-haul economics remain exposed to charging availability, road quality and downtime.",
            "governance_test": "Approve only where payment currency, port plan, off-taker, charging responsibility and aftersales ownership are documented before shipment."
        },
        "farizon_alignment": {
            "portfolio_rule": "Lead with a controlled CBU programme; preserve CKD as a later localisation option after repeatable volume and partner governance are demonstrated.",
            "models": [
                {"model": "V6E / V7E", "role": "Urban FMCG and industrial distribution", "mode": "CBU primary", "logic": "Depot-return duty cycle and high utilisation create the clearest operating-cost case."},
                {"model": "F1E", "role": "Closed industrial and port-adjacent routes", "mode": "CBU pilot", "logic": "Deploy only with captive charging and a USD-funded anchor fleet."},
                {"model": "CKD readiness", "role": "Volume localisation reserve", "mode": "Future option", "logic": "Evaluate only after stable CBU sell-through, quality governance and hard-currency settlement are proven."}
            ]
        }
    },
    "South Africa": {
        "strategic_guardrails": {
            "red_lines": [
                "Do not assume South Africa is EV-import friendly: the CBU EV tariff disadvantage versus ICE vehicles must be reflected in every investment case.",
                "Do not enter on product price alone without a national-grade parts, warranty and technical-support model; established OEM networks define the service benchmark.",
                "Do not overstate ESG intent as purchase demand. Fleet conversion requires route-level uptime, payload and residual-value evidence."
            ],
            "green_zone": "Use CBU as the primary market-validation route for selected LCV and controlled fleet programmes. Scale only where premium fleet customers accept the tariff burden and service coverage is contractually credible."
        },
        "market_mechanics": {
            "market_access": "Homologation and NRCS compliance are demanding but transparent. The larger structural barrier is the tariff architecture and the credibility gap faced by a new brand on residual value and aftersales.",
            "channel_ecosystem": "The market is institutionally mature and network-led. Large fleet tenders are influenced by leasing companies, body builders, service coverage and total uptime—not solely by the vehicle buyer.",
            "value_pool": "Urban logistics, municipal and ESG-accountable fleets can support early EV adoption; broad-market expansion requires financing and used-vehicle confidence.",
            "governance_test": "No national rollout before homologation, parts fill-rate, response-time SLA, residual-value assumptions and priority fleet pipeline pass executive review."
        },
        "farizon_alignment": {
            "portfolio_rule": "CBU is the primary route for proof and brand establishment. CKD/local contract assembly may be assessed later as a tariff and scale response, never as a precondition to entering.",
            "models": [
                {"model": "V6E", "role": "Urban courier and service fleets", "mode": "CBU primary", "logic": "Best fit for predictable city routes and return-to-base charging."},
                {"model": "V7E", "role": "Higher-volume parcel and retail distribution", "mode": "CBU primary", "logic": "Payload and cargo-volume proposition must be validated against mature ICE incumbents."},
                {"model": "F1E", "role": "Corporate and municipal closed-loop duty", "mode": "Selective CBU", "logic": "Use only where charging and fleet uptime governance are controlled."},
                {"model": "CKD readiness", "role": "Tariff mitigation at scale", "mode": "Future option", "logic": "Trigger assessment after repeatable demand and a qualified industrial partner are evidenced."}
            ]
        }
    },
    "Morocco": {
        "strategic_guardrails": {
            "red_lines": [
                "Do not model OCP as a simple direct truck buyer; procurement is distributed across contractors, logistics operators and project ecosystems.",
                "Do not extrapolate mining-sector visibility into nationwide EV readiness. Route ownership, charging power and contractor economics must be verified separately.",
                "Do not concede control of pricing, customer data or service standards to a distributor without measurable performance obligations."
            ],
            "green_zone": "CBU-led entry is appropriate for demonstrator fleets, urban logistics and contractor-operated closed routes. Use evidence from these deployments to build a broader institutional account strategy."
        },
        "market_mechanics": {
            "market_access": "European-oriented homologation and technical expectations favour disciplined product documentation. Industrial policy is sophisticated, so incentives are tied to local value creation rather than import status alone.",
            "channel_ecosystem": "The market combines powerful industrial groups, contractor ecosystems and established distributor networks. Access to OCP-linked demand depends on mapping the contractors that actually own and operate vehicles.",
            "value_pool": "Casablanca urban logistics, industrial estates and selected phosphate-related fixed routes are more actionable than generic national fleet claims.",
            "governance_test": "Approve deployment only when the real asset owner, tender path, duty cycle, charging site and service operator are identified."
        },
        "farizon_alignment": {
            "portfolio_rule": "Use CBU as the primary route to validate products and accounts. Local assembly is a later industrial-policy option if sustained volume and partner economics justify it.",
            "models": [
                {"model": "V6E / V7E", "role": "Casablanca urban and industrial distribution", "mode": "CBU primary", "logic": "Return-to-base routes offer the cleanest entry and reference-building path."},
                {"model": "F1E", "role": "Contractor-operated industrial corridors", "mode": "CBU project deployment", "logic": "Proceed where route and charging assets are captive and procurement authority is clear."},
                {"model": "CKD readiness", "role": "Industrial policy response", "mode": "Future option", "logic": "Evaluate after CBU demand reaches a stable, auditable scale."}
            ]
        }
    },
    "Egypt": {
        "strategic_guardrails": {
            "red_lines": [
                "Absolute prohibition on unsecured CBU credit exposure while hard-currency availability and EGP volatility remain material. No shipment without secured settlement and a defined repatriation path.",
                "Do not use subsidised diesel or headline EV policy to claim automatic TCO superiority; financing, import approvals and currency conversion can reverse the result.",
                "Do not let a future CKD discussion become a reason to reject CBU. CKD is a contingency reserve, not the primary entry verdict."
            ],
            "green_zone": "CBU remains the primary route for tightly controlled, hard-currency-funded fleets and government-backed or multinational projects. Keep batch size, payment security and inventory exposure under executive limits."
        },
        "market_mechanics": {
            "market_access": "Import registration, foreign-currency allocation and evolving industrial policy create a multi-layer gate. Formal compliance alone does not guarantee the ability to pay for or release vehicles.",
            "channel_ecosystem": "The market is relationship- and institution-led, with influential assemblers, agents, banks and public bodies. A credible local operator is needed for approvals and service, but counterparty risk must remain visible.",
            "value_pool": "Closed urban fleets and hard-currency-backed operators are more defensible than broad retail. Subsidised diesel weakens the pure energy-cost argument.",
            "governance_test": "Board approval requires secured currency, credit protection, import responsibility, inventory ceiling and a service plan; any one missing item stops shipment."
        },
        "farizon_alignment": {
            "portfolio_rule": "CBU is the primary controlled-entry mode. CKD/local contract assembly is a future FX and tariff hedge once demand, partner governance and quality control are proven.",
            "models": [
                {"model": "V6E / V7E", "role": "Urban delivery and multinational fleets", "mode": "CBU primary", "logic": "Target hard-currency-funded, depot-return operations with visible ESG mandates."},
                {"model": "F1E", "role": "Closed industrial or public fleet projects", "mode": "Selective CBU", "logic": "Require sovereign, bank or parent-company payment protection."},
                {"model": "CKD readiness", "role": "FX/tariff resilience", "mode": "Future option", "logic": "Activate assessment only when volume, partner quality and local-content economics clear formal gates."}
            ]
        }
    },
    "Kenya": {
        "strategic_guardrails": {
            "red_lines": [
                "Do not confuse Nairobi pilot visibility with national charging readiness or mass-market affordability.",
                "Do not grant nationwide exclusivity to a dealer without service-capacity milestones and named fleet access.",
                "Do not finance fragmented SME demand on unsecured local-currency terms."
            ],
            "green_zone": "CBU-led deployment should focus on Nairobi and Mombasa anchor fleets with depot charging, measurable route utilisation and a service partner able to support uptime."
        },
        "market_mechanics": {
            "market_access": "Standards and import processes are manageable, but tax interpretation and EV policy execution can change. Compliance evidence and landed-cost assumptions require periodic refresh.",
            "channel_ecosystem": "Established Japanese brands and dealer networks shape trust. Corporate fleets, leasing firms and logistics operators are the practical gateways for a new EV brand.",
            "value_pool": "Urban FMCG, courier and selected port logistics routes have the strongest utilisation and charging control.",
            "governance_test": "Scale only after a named anchor fleet, depot power study, parts stocking plan and dealer service KPI are approved."
        },
        "farizon_alignment": {
            "portfolio_rule": "CBU is the default entry and scaling route; localisation is considered only after repeat fleet demand is established.",
            "models": [
                {"model": "V6E", "role": "Nairobi courier and service fleets", "mode": "CBU primary", "logic": "Compact urban duty and return-to-base charging fit the market's early adoption pattern."},
                {"model": "V7E", "role": "FMCG and retail distribution", "mode": "CBU primary", "logic": "Use high-mileage fleets where energy savings are measurable."},
                {"model": "F1E", "role": "Mombasa closed logistics routes", "mode": "CBU pilot", "logic": "Proceed only with controlled charging and a contracted operator."}
            ]
        }
    },
    "Ethiopia": {
        "strategic_guardrails": {
            "red_lines": [
                "Do not equate restrictions on new ICE imports with electrification of the operating fleet; affordability, power availability and aftersales remain binding constraints.",
                "No unsecured exposure to ETB or assumptions of unrestricted USD conversion.",
                "Do not deploy vehicles beyond service and charging corridors merely to capture policy headlines."
            ],
            "green_zone": "Use CBU for institutionally funded Addis Ababa fleets and controlled corridors where payment currency, charging and maintenance are secured. Treat policy as an access catalyst, not proof of commercial viability."
        },
        "market_mechanics": {
            "market_access": "Policy strongly favours EV registration, but FX allocation and administrative execution determine actual importability. Product compliance must be matched by payment and release capability.",
            "channel_ecosystem": "Public institutions, large local groups and development-finance-backed programmes dominate bankable demand. Dealer-led retail is secondary until service and finance mature.",
            "value_pool": "Addis Ababa urban fleets and fixed institutional routes are the near-term pool; nationwide freight electrification is not yet a valid base case.",
            "governance_test": "Require hard-currency funding, route power confirmation, parts inventory and clear government/import approvals before CBU shipment."
        },
        "farizon_alignment": {
            "portfolio_rule": "CBU is the primary response to the immediate EV import window. Local assembly may be examined later if volumes and industrial policy create a controlled case.",
            "models": [
                {"model": "V6E / V7E", "role": "Addis Ababa institutional delivery", "mode": "CBU primary", "logic": "Urban fixed routes align with present charging and service concentration."},
                {"model": "F1E", "role": "Municipal and large-enterprise closed fleets", "mode": "Selective CBU", "logic": "Use only where funding and depot power are contractually secured."},
                {"model": "CKD readiness", "role": "Long-term industrial option", "mode": "Future option", "logic": "Do not delay viable CBU projects while localisation conditions remain unproven."}
            ]
        }
    },
    "Algeria": {
        "strategic_guardrails": {
            "red_lines": [
                "Do not rely on an import-only volume thesis where licensing and industrial-policy changes can abruptly constrain CBU quotas.",
                "Do not commit capital to a local partner without governance rights, quality accountability and auditable localisation economics.",
                "Do not frame CKD as mandatory from day one; controlled CBU entry remains the preferred proof mechanism whenever licences permit."
            ],
            "green_zone": "Pursue CBU projects selectively under confirmed import permissions and institutional demand. Maintain a staged localisation file as a contingency, not as a substitute for commercial validation."
        },
        "market_mechanics": {
            "market_access": "Administrative quotas, homologation and industrial-policy objectives dominate access. Regulatory timing can matter more than underlying demand.",
            "channel_ecosystem": "The market is concentrated around licensed importers, industrial partners and public-linked buyers. Partner political and execution capability require separate assessment.",
            "value_pool": "Institutional fleets, utilities and controlled industrial applications are more governable than speculative dealer inventory.",
            "governance_test": "No shipment or localisation commitment without written import authority, payment security, service responsibility and partner-control provisions."
        },
        "farizon_alignment": {
            "portfolio_rule": "CBU remains the primary controlled-entry route when legally available. CKD is a later regulatory-risk option subject to volume and partner-quality gates.",
            "models": [
                {"model": "V7E", "role": "Urban institutional distribution", "mode": "Selective CBU", "logic": "Use approved fleet projects rather than speculative channel stock."},
                {"model": "F1E", "role": "Utility and industrial fleets", "mode": "CBU project mode", "logic": "Best suited to closed operations with accountable infrastructure."},
                {"model": "CKD readiness", "role": "Industrial-policy contingency", "mode": "Future option", "logic": "Advance only through formal investment-gate review."}
            ]
        }
    },
    "Tunisia": {
        "strategic_guardrails": {
            "red_lines": [
                "Do not ship a configuration without documented UN-ECE conformity and confirmation that all type-approval evidence is accepted locally.",
                "Do not treat fiscal incentives as sufficient demand; charging, financing and distributor service capability must be proven.",
                "Do not dilute product specification to chase price if it compromises European-standard compliance or residual-value credibility."
            ],
            "green_zone": "Use compliant CBU vehicles as the primary entry route for urban and depot-return fleets. Tunisia should function as a standards-validation market and North African reference case."
        },
        "market_mechanics": {
            "market_access": "UN-ECE-oriented homologation is a high technical gate but creates defensibility once passed. Documentation quality and configuration discipline are non-negotiable.",
            "channel_ecosystem": "The market is relatively concentrated among established importers and European-aligned brands. Distributor technical competence is more important than nominal outlet count.",
            "value_pool": "Urban logistics, service fleets and corporate operators benefit most from the policy-TCO gap; long-distance applications remain charging constrained.",
            "governance_test": "Release only homologated configurations through a technically qualified channel with parts, diagnostics and warranty ownership."
        },
        "farizon_alignment": {
            "portfolio_rule": "CBU is the natural primary mode for a standards-led, moderate-volume market. CKD is not a near-term requirement and should be considered only if scale materially changes.",
            "models": [
                {"model": "V6E", "role": "Urban service and last-mile fleets", "mode": "CBU primary", "logic": "Strong fit with depot-return routes and a compliance-led premium proposition."},
                {"model": "V7E", "role": "Retail and parcel distribution", "mode": "CBU primary", "logic": "Use UN-ECE-compliant specification as a trust and resale-value anchor."},
                {"model": "F1E", "role": "Closed municipal/industrial duty", "mode": "Selective CBU", "logic": "Deploy only where charging responsibility is explicit."}
            ]
        }
    },
    "Rwanda": {
        "strategic_guardrails": {
            "red_lines": [
                "Do not mistake regulatory openness and 0% duties for a large addressable volume; market size and public-procurement concentration cap scale.",
                "Do not build the case on a single government or bus tender. Private fleet proof is required to avoid policy-dependent demand.",
                "Do not sell dispersed retail EVs without confirmed charging access and service coverage outside Kigali."
            ],
            "green_zone": "Use CBU as the primary mode for Kigali fleet references, taking advantage of clear EV policy and explicit GB/T recognition. Keep inventory lean and tie scale to repeat orders."
        },
        "market_mechanics": {
            "market_access": "Certification is comparatively pragmatic and the 2026 charging framework explicitly recognises GB/T, reducing technical uncertainty. Licensing and operator obligations still require local execution.",
            "channel_ecosystem": "Demand is small and concentrated around government, development organisations, bus operators and a limited group of formal fleets. Direct key-account governance is more effective than a broad dealer push.",
            "value_pool": "Kigali delivery, hospitality, institutional and scheduled fleet operations offer the clearest fit; national volume remains structurally limited.",
            "governance_test": "Judge Rwanda on policy reference value and reproducible fleet use cases—not on absolute revenue contribution."
        },
        "farizon_alignment": {
            "portfolio_rule": "CBU is decisively preferred for this low-volume policy showcase. CKD would add complexity without a sufficient scale base.",
            "models": [
                {"model": "V6E", "role": "Kigali delivery, hospitality and service fleets", "mode": "CBU primary", "logic": "Compact market, supportive policy and GB/T recognition enable a controlled reference fleet."},
                {"model": "V7E", "role": "Institutional distribution", "mode": "CBU selective", "logic": "Match deployment to committed depot charging and repeatable routes."},
                {"model": "F1E", "role": "Public or scheduled fleet demonstration", "mode": "CBU project", "logic": "Treat as a policy and product reference, not a volume forecast."}
            ]
        }
    },
    "Djibouti": {
        "strategic_guardrails": {
            "red_lines": [
                "Do not evaluate Djibouti on domestic registrations alone; the strategic asset is the Ethiopia trade corridor and port-drainage system.",
                "Do not deploy electric tractors on uncontrolled long-haul corridor duty before heat, payload, charging and uptime are validated.",
                "Do not rely on a single port stakeholder without clarifying concession, operator and fleet-ownership boundaries."
            ],
            "green_zone": "Use CBU for controlled port and free-zone drayage pilots with captive charging and a named terminal or logistics operator. Scale by corridor productivity evidence."
        },
        "market_mechanics": {
            "market_access": "Formal market size is small, but port concessions and free-zone rules shape access. Technical success depends more on operator permission and site power than national retail regulation.",
            "channel_ecosystem": "A small number of port, terminal, free-zone and corridor logistics actors control the bankable demand. Direct institutional engagement is essential.",
            "value_pool": "Short, repetitive port-to-yard and port-to-rail movements create a distinctive electrification case; general domestic distribution does not.",
            "governance_test": "Require route telemetry, charging-site rights, heat-management validation and operator accountability before fleet expansion."
        },
        "farizon_alignment": {
            "portfolio_rule": "CBU project deployment is the primary route. CKD is economically unjustified at current domestic scale.",
            "models": [
                {"model": "F1E", "role": "Port and free-zone drayage", "mode": "CBU pilot/primary", "logic": "Short captive cycles can support high utilisation and central charging."},
                {"model": "V7E", "role": "Free-zone and urban distribution", "mode": "Selective CBU", "logic": "Secondary opportunity tied to formal logistics operators."}
            ]
        }
    },
    "Mauritius": {
        "strategic_guardrails": {
            "red_lines": [
                "Do not pursue volume-led inventory in a structurally small market.",
                "Do not enter through a weak service partner merely because EV policy is favourable; island reputation effects are immediate.",
                "Do not ignore cyclone resilience, coastal corrosion and charging-site continuity in fleet specifications."
            ],
            "green_zone": "Use CBU as the primary and appropriate mode for premium, visible fleet references with disciplined inventory and high service standards."
        },
        "market_mechanics": {
            "market_access": "Import rules are relatively transparent and EV economics benefit from fuel import dependence. Product quality, warranty execution and island-specific durability are the true barriers.",
            "channel_ecosystem": "The market is compact, relationship-driven and concentrated among established distributors, hospitality groups, logistics operators and public bodies.",
            "value_pool": "Hospitality, airport, municipal and premium corporate fleets value visibility and decarbonisation alongside operating cost.",
            "governance_test": "Prioritise reference quality, uptime and brand reputation over unit volume; cap inventory to contracted demand."
        },
        "farizon_alignment": {
            "portfolio_rule": "CBU is the clear primary mode. The market is too small to justify CKD complexity.",
            "models": [
                {"model": "V6E", "role": "Hospitality, service and municipal fleets", "mode": "CBU primary", "logic": "Compact routes and visible sustainability value support a premium reference case."},
                {"model": "V7E", "role": "Airport and formal logistics", "mode": "CBU selective", "logic": "Deploy with corrosion protection and strong uptime support."}
            ]
        }
    },
    "Madagascar": {
        "strategic_guardrails": {
            "red_lines": [
                "Prohibit dispersed retail EV selling and down-market dealer inventory where grid access, road quality and service reach cannot support the product.",
                "Do not present EV as a nationwide answer; outside controlled compounds, infrastructure and recovery risk can overwhelm energy savings.",
                "Do not grant credit or ship specialised vehicles without an anchor operator, service plan and secure payment."
            ],
            "green_zone": "CBU remains valid and must not be rejected: focus on rugged, specification-led vehicles for mining, utilities and controlled urban compounds. EV CBU is limited to captive routes with dedicated charging."
        },
        "market_mechanics": {
            "market_access": "Regulatory certification is less demanding than physical operating conditions. Road degradation, grid weakness, parts logistics and recovery time are the real barriers.",
            "channel_ecosystem": "Formal demand is concentrated among mining companies, utilities, NGOs and a small number of large operators; fragmented retail is high-cost to serve.",
            "value_pool": "Rugged commercial vehicles for mining and infrastructure are the core pool. Electric LCVs are relevant only inside controlled Antananarivo or industrial compounds.",
            "governance_test": "No EV deployment without captive charging, route inspection, recovery capability and a named technical operator."
        },
        "farizon_alignment": {
            "portfolio_rule": "CBU remains the primary export mode. Use product segmentation—not a countrywide CBU rejection—to control risk; CKD has no near-term scale rationale.",
            "models": [
                {"model": "V6E", "role": "Controlled urban/industrial compound duty", "mode": "Highly selective CBU", "logic": "Only where charging, roads and service are captive."},
                {"model": "F1E", "role": "Closed mining or utility operations", "mode": "Project-specific CBU", "logic": "Proceed after terrain, payload and energy-infrastructure validation."},
                {"model": "ICE/rugged portfolio", "role": "Mining and poor-road operations", "mode": "CBU primary", "logic": "Infrastructure reality—not ideology—determines the near-term powertrain mix."}
            ]
        }
    }
}

for _country_name, _governance_fields in GOVERNANCE_DATA.items():
    if _country_name not in TIER1:
        raise KeyError(f"Governance data references unknown country: {_country_name}")
    TIER1[_country_name].update(_governance_fields)

_missing_governance = [
    _name for _name, _data in TIER1.items()
    if not all(_field in _data for _field in (
        "strategic_guardrails", "market_mechanics", "farizon_alignment"
    ))
]
if _missing_governance:
    raise ValueError(f"Missing executive governance fields: {_missing_governance}")

# Chinese executive narratives are deliberately separated from the analytical
# keys. Switching language never changes country scores, chart data or formulas.
V15_GOV_ZH = {
    "Nigeria": {
        "red": ["禁止无担保的奈拉计价CBU应收账款。", "未确认终端车队、硬通货结算与港口方案前，禁止投放投机性库存。", "未具备封闭线路和专属充电前，禁止把重型纯电车型作为全国方案。"],
        "green": "允许面向有美元资金支持的城市及工业车队开展受控批次CBU业务。",
        "mechanics": ["SON与Form M合规可管理，但美元可得性决定进口能否兑现。", "大型工业集团和物流运营商掌握可融资需求，分散渠道库存风险较高。", "真实价值池集中在高里程、回场充电的城市快消和工业配送。"],
        "gate": "只有付款币种、港口方案、终端用户、充电与售后责任全部明确后，才扩大CBU投入。",
        "portfolio": "以受控CBU作为主进入路径；只有形成可重复销量和合作伙伴治理后，才评估CKD。",
    },
    "South Africa": {
        "red": ["禁止把南非视为纯电CBU关税友好市场。", "未建立全国级备件、质保和技术响应体系前，禁止全国铺开。", "禁止把ESG意愿直接等同于采购订单。"],
        "green": "允许面向城市物流、市政和优质企业车队开展CBU标杆项目。",
        "mechanics": ["NRCS与认证规则透明但严格，纯电CBU存在关税劣势。", "租赁公司、上装企业和服务网络共同影响车队采购。", "城市物流和承担ESG责任的车队是最现实的早期价值池。"],
        "gate": "认证、备件满足率、服务时效、残值假设和重点车队管道必须同时通过验证。",
        "portfolio": "CBU用于产品与品牌验证；形成可重复车队需求后，再把CKD/本地代工作为关税与规模备选。",
    },
    "Morocco": {
        "red": ["禁止把OCP简单视为直接购车主体。", "禁止把矿业曝光度直接推导为全国电动化成熟度。", "未设定服务与客户开发指标前，禁止授予经销商无条件独家权。"],
        "green": "允许在城市物流和承运商运营的封闭工业线路开展CBU示范。",
        "mechanics": ["欧洲导向的技术标准要求严格的认证资料和配置纪律。", "工业集团、承运商与成熟经销商共同控制市场入口。", "实际拥有并运营车辆的承运商比名义项目发起方更重要。"],
        "gate": "必须识别真实资产所有者、招标路径、线路、充电场地和服务运营者。",
        "portfolio": "先以CBU建立产品和客户标杆；只有持续销量达到门槛后，才讨论本地化。",
    },
    "Egypt": {
        "red": ["禁止任何无担保的CBU信用敞口。", "禁止在柴油补贴环境下宣称电动车天然具备TCO优势。", "禁止把CKD讨论变成否定CBU进入的理由。"],
        "green": "允许面向跨国企业、公共支持或硬通货车队开展有付款保障的项目型CBU。",
        "mechanics": ["进口审批与外汇分配共同构成准入门槛。", "代理商、银行、组装企业和公共机构共同塑造市场。", "有硬通货保障的封闭城市车队比广泛零售更可执行。"],
        "gate": "必须具备有保障结算、信用保护、明确进口责任、库存上限和服务方案。",
        "portfolio": "CBU是受控进入模式；CKD仅在需求、伙伴治理与质量体系成熟后作为外汇和关税对冲。",
    },
    "Kenya": {
        "red": ["禁止把内罗毕试点曝光度等同于全国成熟度。", "未达到服务里程碑前，禁止授予全国独家代理。", "禁止为分散中小企业需求提供无担保融资。"],
        "green": "允许向具备场站充电和正式合同的内罗毕、蒙巴萨核心车队投放CBU。",
        "mechanics": ["标准和进口流程可管理，但税费与落地成本需持续更新。", "日系品牌和成熟经销商构成市场信任基准。", "城市快消、快递和受控港口物流是主要价值池。"],
        "gate": "必须具备核心车队、场站电力研究、备件计划和经销商服务能力。",
        "portfolio": "CBU是默认进入和扩张路径，本地化只在重复车队需求形成后考虑。",
    },
    "Ethiopia": {
        "red": ["禁止把燃油车进口限制等同于存量车队已经电动化。", "禁止形成无保障的比尔或美元转换敞口。", "禁止在服务与充电走廊之外盲目投放。"],
        "green": "允许向有机构资金支持的亚的斯亚贝巴车队和固定线路投放CBU。",
        "mechanics": ["电动车政策有利，但外汇执行决定实际进口能力。", "公共机构、大型集团和发展金融项目主导可兑现需求。", "短期价值集中在亚的斯亚贝巴与固定机构线路。"],
        "gate": "发运前必须确认硬通货资金、线路电力、备件和进口许可。",
        "portfolio": "利用当前政策窗口以CBU进入；本地化仅作为长期产业选项。",
    },
    "Algeria": {
        "red": ["没有书面进口许可时，禁止投机性CBU发运。", "未取得治理权和质量责任前，禁止承诺本地化。", "禁止因监管不确定性把CKD设为进入前提。"],
        "green": "允许在进口许可明确且需求有保障的机构项目中选择性开展CBU。",
        "mechanics": ["行政配额、进口许可与产业政策主导准入。", "持证进口商、产业伙伴和公共关联买家集中掌握需求。", "公用事业和封闭工业项目比经销商库存更可治理。"],
        "gate": "必须具备书面进口权、付款保障、服务责任和合作伙伴控制条款。",
        "portfolio": "许可允许时，CBU仍是受控验证路径；CKD是经过正式门槛评估后的后续选项。",
    },
    "Tunisia": {
        "red": ["未确认UN-ECE型式认证材料被接受前，禁止发运。", "禁止把财政激励直接等同于市场需求。", "禁止为追求低价降低欧洲标准合规配置。"],
        "green": "允许以合规CBU进入城市配送和回场车队，把突尼斯作为认证与标准标杆。",
        "mechanics": ["UN-ECE认证门槛高，但通过后具备防御性。", "市场信任集中在成熟进口商与欧洲品牌。", "城市物流、服务车队和企业运营商是主要价值池。"],
        "gate": "必须使用已认证配置，并由具备技术能力的渠道承担备件、诊断和质保。",
        "portfolio": "中等容量、标准导向的市场天然适合CBU，短期没有CKD必要性。",
    },
    "Rwanda": {
        "red": ["禁止把政策开放和零关税误判为巨大市场容量。", "禁止把业务建立在单一政府或公交项目上。", "未确认充电与服务覆盖前，禁止基加利以外的分散零售。"],
        "green": "允许利用GB/T认可，在基加利开展轻库存CBU标杆车队。",
        "mechanics": ["认证务实，GB/T认可显著降低技术不确定性。", "政府、发展机构、公交和少数正式车队集中掌握需求。", "基加利配送、酒店和机构车队是主要价值池。"],
        "gate": "以政策标杆价值和可重复车队场景判断市场，而不是以绝对营收判断。",
        "portfolio": "低容量政策样板市场应坚持CBU，CKD会增加不必要复杂度。",
    },
    "Djibouti": {
        "red": ["禁止仅依据国内注册量判断吉布提机会。", "未经高温、载荷和线路验证，禁止开放走廊电动牵引车投放。", "未厘清港口特许权、运营商和车队所有权前，禁止扩大投入。"],
        "green": "允许与明确码头或物流运营商开展具备专属充电的CBU港口倒短试点。",
        "mechanics": ["港口特许权、运营许可和场地电力比零售法规更重要。", "少数港口、码头和走廊运营商控制可兑现需求。", "短距离高频港到堆场、港到铁路循环构成独特价值池。"],
        "gate": "必须具备线路数据、充电场地权利、高温验证和明确运营责任。",
        "portfolio": "以CBU项目交付为主，当前国内容量不足以支持CKD。",
    },
    "Mauritius": {
        "red": ["禁止在结构性小市场进行规模化投机库存。", "禁止通过服务能力薄弱的伙伴进入。", "禁止忽略气旋、海岸腐蚀和充电连续性。"],
        "green": "允许以CBU开展高质量、可见的优质车队标杆，并严格控制库存。",
        "mechanics": ["进口规则透明，海岛耐久与质保执行才是真正门槛。", "成熟经销商、酒店、物流和公共机构集中掌握需求。", "酒店、机场、市政和优质企业车队同时重视品牌可见度与运营成本。"],
        "gate": "优先保证标杆质量、出勤率和品牌声誉，库存必须与合同需求挂钩。",
        "portfolio": "CBU是明确主模式，市场容量不足以支持CKD复杂度。",
    },
    "Madagascar": {
        "red": ["禁止向基础设施与服务无法覆盖的分散客户销售电动车。", "禁止把电动车描述为全国性解决方案。", "没有核心运营商、服务方案和付款保障时，禁止发运专用车辆。"],
        "green": "不能否定CBU；允许面向矿业、公用事业和受控园区投放符合工况的CBU产品。",
        "mechanics": ["道路、电网、备件与救援比形式认证构成更大门槛。", "矿业企业、公用事业、NGO和少数大型运营商集中掌握正式需求。", "矿业与基建是核心价值池，电动车仅适用于封闭园区。"],
        "gate": "电动车项目必须具备专属充电、线路勘察、救援能力和明确技术运营者。",
        "portfolio": "CBU仍是主出口模式，通过产品和场景分层控制风险，而不是否定整个国家。",
    },
}



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
#       Level 2 → Segment Heatmap (L) + immutable macro TCO baseline (R)
#       Level 3 → Brand Share (L) + Country-Exclusive Chart (R)
#       Level 4 → Evidence & Confidence
#     V15 adds Signals, Guardrails and Farizon Alignment without deleting
#     any country-exclusive analytical chart.
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
        _chdr(
            tr("60-Month Market TCO Baseline", "60个月市场TCO基准"),
            tr("ICE vs. EV Cumulative Cost", "燃油与纯电累计成本"),
            tr(
                f"Controlled baseline · ICE ${p['ICE_Capex']:,.0f} vs EV ${p['EV_Capex']:,.0f} · "
                f"interest {p['Interest_Rate']*100:.0f}% · residual ICE {p['ICE_Residual_Pct']:.0%} / EV {p['EV_Residual_Pct']:.0%}",
                f"受控基准 · 燃油车 ${p['ICE_Capex']:,.0f} 对比纯电 ${p['EV_Capex']:,.0f} · "
                f"利率 {p['Interest_Rate']*100:.0f}% · 五年残值 燃油 {p['ICE_Residual_Pct']:.0%} / 纯电 {p['EV_Residual_Pct']:.0%}",
            ),
            p["source_name"], p["source_url"],
        )
        st.plotly_chart(
            chart_tco_breakeven(country),
            use_container_width=True,
            config=PLOTLY_CFG,
            key=f"{country}_tco_baseline",
        )
        breakeven_month, _ = calc_tco_breakeven(country)
        if breakeven_month is None:
            be_text = tr("Not reached within 60 months", "60个月内未达到平衡")
        else:
            be_text = tr(
                f"Month {breakeven_month:.1f} ({breakeven_month/12:.1f} years)",
                f"第 {breakeven_month:.1f} 个月（{breakeven_month/12:.1f} 年）",
            )
        ice_per_km = p["Diesel_Price_per_L"] * p["ICE_Consumption_L_per_100km"] / 100
        ev_per_km = p["Charging_Tariff_per_kWh"] * p["EV_Consumption_kWh_per_100km"] / 100
        st.caption(
            tr(
                f"Baseline parity: {be_text} · ICE ${ice_per_km:.3f}/km · EV ${ev_per_km:.3f}/km",
                f"基准平衡点：{be_text} · 燃油 ${ice_per_km:.3f}/公里 · 纯电 ${ev_per_km:.3f}/公里",
            )
        )
        st.info(
            tr(
                "Approved country benchmark. This is not a customer quotation and cannot be overwritten on the page.",
                "这是受控的国家市场基准，不是客户报价，页面端不能覆盖底层假设。",
            )
        )

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


def _render_signals_tab(country: str, cdata: dict):
    """Structured signals: raw events become management implications."""
    mechanics = cdata["market_mechanics"]
    guardrails = cdata["strategic_guardrails"]
    zh = V15_GOV_ZH[country] if V15_LANG == "zh" else None
    st.markdown(f"""
<div class="gtm-mission-banner">
  <div class="gtm-mission-title">📡 {country} · {tr("Signals & Strategic Triggers", "市场信号与战略触发器")}</div>
  <div class="gtm-mission-sub">{tr("What changed · why it matters · what would change the CBU mode", "发生了什么 · 为什么重要 · 什么条件会改变CBU模式")}</div>
</div>
""", unsafe_allow_html=True)
    _sdiv(tr("Structured Signal Feed", "结构化信号"))
    signal_rows = [
        {
            tr("Signal", "信号"): cdata["policy"]["risk"],
            tr("Implication", "战略含义"): zh["gate"] if zh else mechanics["governance_test"],
            tr("Importance", "重要度"): tr("High", "高"),
        },
        {
            tr("Signal", "信号"): tr("Evidence quality requires periodic refresh", "证据质量需要定期复核"),
            tr("Implication", "战略含义"): tr(
                "Do not upgrade market commitment on stale assumptions.",
                "不能依据过期假设升级市场投入。",
            ),
            tr("Importance", "重要度"): tr("Medium", "中"),
        },
    ]
    st.dataframe(pd.DataFrame(signal_rows), hide_index=True, use_container_width=True)
    _sdiv(tr("Strategic Trigger Monitor", "战略触发器监控"))
    st.warning(
        f"**{tr('Decision trigger', '决策触发条件')}**\n\n"
        f"{zh['gate'] if zh else mechanics['governance_test']}"
    )
    st.info(
        tr(
            "Future automation will populate FX, tariff, registration, competitor and infrastructure signals. "
            "The current version establishes the governed data structure.",
            "未来将自动接入汇率、关税、注册量、竞品与基础设施信号。当前版本先建立受治理的数据骨架。",
        )
    )
    _sdiv(tr("What Changed Since Last Review", "较上次复核的变化"))
    st.dataframe(pd.DataFrame([{
        tr("Previous view", "上次判断"): tr("Baseline retained", "维持基准判断"),
        tr("Current view", "当前判断"): tr("Baseline retained", "维持基准判断"),
        tr("Reason", "原因"): cdata["policy"]["risk"],
        tr("Mode changed?", "模式是否变化"): tr("No", "否"),
    }]), hide_index=True, use_container_width=True)


def _render_guardrails_tab(country: str, cdata: dict):
    """Board-level market mechanics and behavioural boundaries."""
    guardrails = cdata["strategic_guardrails"]
    mechanics = cdata["market_mechanics"]
    zh = V15_GOV_ZH[country] if V15_LANG == "zh" else None
    st.markdown(f"""
<div class="gtm-mission-banner">
  <div class="gtm-mission-title">🚦 {country} · {tr("Market Mechanics & Guardrails", "市场机制与战略边界")}</div>
  <div class="gtm-mission-sub">{tr("Objective market logic and non-negotiable decision boundaries", "客观市场逻辑与不可突破的决策边界")}</div>
</div>
""", unsafe_allow_html=True)
    _sdiv(tr("Absolute Red Lines", "绝对红线"))
    for red_line in (zh["red"] if zh else guardrails["red_lines"]):
        st.error(red_line)
    _sdiv(tr("Permitted Strategic Zone", "当前允许区间"))
    st.success(zh["green"] if zh else guardrails["green_zone"])
    _sdiv(tr("Market Operating Logic", "市场运作逻辑"))
    labels = [
        (tr("Access & Compliance", "准入与合规"), "market_access"),
        (tr("Supply Chain & Channel", "供应链与渠道"), "channel_ecosystem"),
        (tr("Addressable Value Pool", "真实价值池"), "value_pool"),
    ]
    cols = st.columns(3, gap="medium")
    mechanic_values = zh["mechanics"] if zh else [
        mechanics["market_access"],
        mechanics["channel_ecosystem"],
        mechanics["value_pool"],
    ]
    for col, (label, key), body in zip(cols, labels, mechanic_values):
        with col:
            st.markdown(f"""
<div class="gtm-card">
  <div class="gtm-card-hdr product"><div class="gtm-card-title">{label}</div></div>
  <div class="gtm-card-body">{body}</div>
</div>
""", unsafe_allow_html=True)
    _sdiv(tr("Invalid Assumptions", "无效假设"))
    st.info(
        tr(
            "Tariff support is not demand; policy intent is not fleet electrification; market size is not executability; "
            "a headline group is not always the vehicle buyer.",
            "关税支持不等于真实需求；政策意愿不等于车队已经电动化；市场容量不等于可执行性；"
            "大型集团也不一定是车辆的实际采购主体。",
        )
    )


def _render_alignment_tab(country: str, cdata: dict):
    """Farizon product placement without frontline sales calculation."""
    alignment = cdata["farizon_alignment"]
    zh = V15_GOV_ZH[country] if V15_LANG == "zh" else None
    st.markdown(f"""
<div class="gtm-mission-banner">
  <div class="gtm-mission-title">🎯 {country} · {tr("Farizon Strategic Alignment", "远程战略与车型落位")}</div>
  <div class="gtm-mission-sub">{tr("Where the product fits · what must be true · where it must not be used", "产品适合哪里 · 成立条件是什么 · 什么场景不能使用")}</div>
</div>
""", unsafe_allow_html=True)
    st.info(
        f"**{tr('Portfolio rule', '产品组合规则')}**\n\n"
        f"{zh['portfolio'] if zh else alignment['portfolio_rule']}"
    )
    rows = []
    for item in alignment["models"]:
        rows.append({
            tr("Farizon model / capability", "远程车型/能力"): item["model"],
            tr("Market role", "市场角色"): item["role"],
            tr("Entry mode", "进入模式"): item["mode"],
            tr("Strategic rationale", "战略依据"): item["logic"],
        })
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
    _sdiv(tr("Product & Capability Gaps", "产品与能力缺口"))
    st.warning(
        tr(
            "Validate homologation, charging interface, payload, aftersales coverage and residual-value support "
            "before upgrading the country commitment.",
            "升级国家投入前，必须验证认证、充电接口、载荷、售后覆盖和残值支持。",
        )
    )
    st.caption(
        tr(
            "Group boundary: CBU is the primary export mode. CKD/local assembly is a staged future option only.",
            "集团边界：CBU是当前主力出口模式，CKD/本地化组装仅为分阶段的未来选项。",
        )
    )


def render_country_dashboard(country: str, cdata: dict):
    """Original country analytics plus V15 executive-governance layers."""
    tab_market, tab_dd, tab_signals, tab_guardrails, tab_alignment, tab_intel = st.tabs([
        tr("📊 Market & Risk Analytics", "📊 市场与风险分析"),
        tr("🔎 Evidence & Confidence", "🔎 证据与可信度"),
        tr("📡 Signals & Triggers", "📡 信号与触发器"),
        tr("🚦 Strategic Guardrails", "🚦 战略边界"),
        tr("🎯 Farizon Alignment", "🎯 远程车型落位"),
        tr("🕵️ Competitive Intelligence", "🕵️ 竞争情报"),
    ])
    with tab_market:
        _render_market_risk_tab(country, cdata)
    with tab_dd:
        _render_due_diligence_tab(country, cdata)
    with tab_signals:
        _render_signals_tab(country, cdata)
    with tab_guardrails:
        _render_guardrails_tab(country, cdata)
    with tab_alignment:
        _render_alignment_tab(country, cdata)
    with tab_intel:
        _render_competitive_intel_tab(country, cdata)


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
# 12B. V16 COMMERCIAL WORKSPACE & DATA GOVERNANCE
# Uses the existing V15 visual primitives; no new colour system or page skin.
# ══════════════════════════════════════════════════════════════════════════════
STAGE_BASE_PROBABILITY = {
    "Research": 0.05,
    "Contacted": 0.10,
    "Qualified": 0.25,
    "Technical Fit": 0.35,
    "Proposal": 0.40,
    "Pilot": 0.55,
    "Commercial Fit": 0.60,
    "Negotiation": 0.70,
    "Tender": 0.60,
    "PO": 0.95,
    "Won": 1.00,
    "Lost": 0.00,
}


def _effective_pipeline_probability(row: pd.Series) -> float:
    """Stage-led probability with a controlled ±10pp manual override."""
    stage_base = STAGE_BASE_PROBABILITY.get(str(row.get("Stage", "")), 0.10)
    raw = row.get("Probability", stage_base)
    try:
        manual = float(raw)
    except (TypeError, ValueError):
        manual = stage_base
    lower = max(0.0, stage_base - 0.10)
    upper = min(1.0, stage_base + 0.10)
    return min(max(manual, lower), upper)


def _prepare_opportunity_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    out = df.copy()
    out["Stage Base Probability"] = out["Stage"].map(STAGE_BASE_PROBABILITY).fillna(0.10)
    out["Manual Probability"] = pd.to_numeric(out["Probability"], errors="coerce")
    out["Effective Probability"] = out.apply(_effective_pipeline_probability, axis=1)
    out["Weighted Units"] = out["Expected Units"] * out["Effective Probability"]
    out["Weighted Value USD"] = out["Expected Units"] * out["Unit Value USD"] * out["Effective Probability"]
    return out


def _v16_country_frame(df: pd.DataFrame, country: str) -> pd.DataFrame:
    if "Country" not in df.columns:
        return df.copy()
    return df[df["Country"].eq(country)].copy()


def render_v16_commercial_workspace(country: str):
    dealers = _v16_country_frame(V16_DEALERS, country)
    customers = _v16_country_frame(V16_CUSTOMERS, country)
    opportunities = _prepare_opportunity_pipeline(_v16_country_frame(V16_OPPORTUNITIES, country))
    actions = _v16_country_frame(V16_ACTIONS, country)

    _level_hdr(
        1,
        tr("Commercial Decision Snapshot", "销售决策快照"),
        tr(
            "Dealer coverage, account access, weighted pipeline and immediate actions.",
            "渠道覆盖、客户触达、加权项目管道与近期行动。",
        ),
    )
    weighted_units = opportunities["Weighted Units"].sum() if not opportunities.empty else 0
    weighted_value = opportunities["Weighted Value USD"].sum() if not opportunities.empty else 0
    due_dates = pd.to_datetime(actions["Deadline"], errors="coerce") if not actions.empty else pd.Series(dtype="datetime64[ns]")
    due_actions = int(due_dates.le(pd.Timestamp.now() + pd.Timedelta(days=60)).sum())

    cards = [
        (tr("Dealer candidates", "候选渠道"), len(dealers)),
        (tr("Mapped customers", "已识别客户"), len(customers)),
        (tr("Pipeline units", "项目台数"), int(opportunities["Expected Units"].sum()) if not opportunities.empty else 0),
        (tr("Weighted units", "加权台数"), round(weighted_units, 1)),
        (tr("Weighted value", "加权金额"), f"${weighted_value/1_000_000:.2f}m"),
        (tr("Actions due ≤60d", "60天内到期行动"), due_actions),
    ]
    for col, (label, value) in zip(st.columns(6), cards):
        with col:
            st.metric(label, value)

    if dealers.empty and customers.empty and opportunities.empty:
        st.info(
            tr(
                "Commercial records are not yet migrated for this market. The country analytics remain available; add named dealer, customer and project records before an investment decision.",
                "该市场的销售记录尚未迁移。国家分析仍可使用，但投资决策前必须补充实名渠道、客户和项目记录。",
            ),
            icon="ℹ️",
        )
        return

    _sdiv(tr("Opportunity Pipeline", "项目管道"))
    if opportunities.empty:
        st.info(tr("No opportunity has been recorded.", "尚未录入项目机会。"))
    else:
        stage_order = ["Research","Contacted","Qualified","Technical Fit","Proposal","Pilot","Commercial Fit","Negotiation","Tender","PO","Won","Lost"]
        stage_units = (
            opportunities.groupby("Stage")["Expected Units"].sum()
            .reindex(stage_order, fill_value=0)
            .reset_index()
        )
        fig = px.bar(
            stage_units,
            x="Stage",
            y="Expected Units",
            color="Expected Units",
            color_continuous_scale=["#D9E5F5", "#295BA5"],
            text_auto=True,
        )
        fig.update_layout(
            **{
                **CHART_BASE,
                "height": 300,
                "margin": dict(l=25, r=20, t=20, b=25),
                "showlegend": False,
                "coloraxis_showscale": False,
            }
        )
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CFG, key=f"v16_pipe_{country}")
        st.dataframe(opportunities, hide_index=True, use_container_width=True)

    _sdiv(tr("Dealer and Customer Coverage", "渠道与客户覆盖"))
    st.markdown("**" + tr("Dealer candidates", "候选渠道") + "**")
    if dealers.empty:
        st.caption(tr("No dealer record.", "暂无渠道记录。"))
    else:
        st.dataframe(dealers, hide_index=True, use_container_width=True)
    st.markdown("**" + tr("Target accounts", "目标客户") + "**")
    if customers.empty:
        st.caption(tr("No customer record.", "暂无客户记录。"))
    else:
        st.dataframe(customers, hide_index=True, use_container_width=True)

    st.caption(
        tr(
            "Commercial records shown here are internal planning inputs. Named prospects, scores, expected units and probabilities require country-manager verification.",
            "本页客户、渠道、评分、预计台数及成交概率均为内部业务输入，须由国家经理核验。",
        )
    )


def render_v16_data_governance(country: str):
    metrics = _v16_country_frame(V16_METRIC_AUDIT, country)
    sources = V16_SOURCES[
        V16_SOURCES["Country"].isin([country, "Cross-market"])
    ].copy()
    known_sources = set(V16_SOURCES["Source ID"].dropna())
    referenced_sources = set(metrics["Source ID"].dropna()) if not metrics.empty else set()
    orphan_sources = sorted(referenced_sources - known_sources)
    sourced_share = metrics["Source ID"].notna().mean() if not metrics.empty else 0
    reported_share = metrics["Data Type"].isin(["Actual", "Reported"]).mean() if not metrics.empty else 0
    weak_count = int(metrics["Confidence"].isin(["D", "E"]).sum()) if not metrics.empty else 0
    def _source_ttl_days(row: pd.Series) -> int:
        scope = str(row.get("Scope", "")).lower()
        source_type = str(row.get("Source Type", "")).lower()
        if any(k in scope for k in ["fx", "exchange", "fuel", "diesel"]):
            return 30
        if any(k in scope for k in ["electricity", "charging", "price", "dealer", "brand"]):
            return 90
        if any(k in scope for k in ["tax", "customs", "homologation", "policy", "regulation", "authorisation", "authorization"]):
            return 180
        if any(k in scope for k in ["registration", "market", "transport statistics", "sales"]):
            return 450
        if "method" in scope or source_type == "consulting":
            return 1095
        if source_type == "internal":
            return 90
        return 365

    if not sources.empty:
        pub_dates = pd.to_datetime(sources["Publication Date"], errors="coerce")
        source_age = (pd.Timestamp.now().normalize() - pub_dates).dt.days
        sources["TTL Days"] = sources.apply(_source_ttl_days, axis=1)
        sources["Age Days"] = source_age
        sources["Freshness"] = np.where(
            pub_dates.isna(),
            "Missing date",
            np.where(source_age > sources["TTL Days"], "Stale", "Current"),
        )
        stale_count = int(sources["Freshness"].eq("Stale").sum())
    else:
        stale_count = 0

    _level_hdr(
        1,
        tr("Data Audit Snapshot", "数据审计快照"),
        tr(
            "Separates reported facts, estimates, model outputs and management judgement.",
            "明确分离实际/报告数据、估算、模型结果与管理判断。",
        ),
    )
    cards = [
        (tr("Audited metrics", "审计指标"), len(metrics)),
        (tr("Actual / reported", "实际/报告占比"), f"{reported_share:.0%}"),
        (tr("Source linkage", "来源关联率"), f"{sourced_share:.0%}"),
        (tr("Low-confidence", "低可信指标"), weak_count),
        (tr("Stale sources", "过期来源"), stale_count),
        (tr("Orphan IDs", "孤立来源ID"), len(orphan_sources)),
    ]
    for col, (label, value) in zip(st.columns(6), cards):
        with col:
            st.metric(label, value)

    if orphan_sources:
        st.error(
            tr("Unresolved source IDs: ", "未解析来源ID：") + ", ".join(orphan_sources)
        )
    elif metrics.empty:
        st.warning(
            tr(
                "No structured metric audit has been migrated for this country.",
                "该国家尚未迁移结构化指标审计数据。",
            )
        )
    else:
        st.success(tr("Source-ID integrity check passed.", "Source ID完整性检查通过。"))

    _sdiv(tr("Metric Register", "指标登记表"))
    if not metrics.empty:
        st.dataframe(metrics, hide_index=True, use_container_width=True)
    else:
        st.caption(tr("Pending migration.", "待迁移。"))

    _sdiv(tr("Source Register", "来源登记表"))
    if not sources.empty:
        st.dataframe(
            sources,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Source URL": st.column_config.LinkColumn(
                    tr("Source URL", "来源链接"),
                    display_text=tr("Open source", "打开来源"),
                )
            },
        )

    render_auto_market_data_panel(country)

    _sdiv(tr("Governance Rules", "数据治理规则"))
    rules = [
        tr("Actual / Reported: may support management decisions when the exact source and period are recorded.",
           "Actual / Reported：记录具体来源与数据期后，可用于管理判断。"),
        tr("Estimated / Modelled: must display the model notice and cannot be presented as official statistics.",
           "Estimated / Modelled：必须显示模型标识，不得作为官方统计表述。"),
        tr("Judgement: must include an owner, next validation action and deadline.",
           "Judgement：必须对应责任人、下一验证动作与截止时间。"),
        tr("Confidence C requires triangulation; D–E are hypothesis-only.",
           "可信度C需交叉验证；D–E仅可作为假设。"),
        tr("Freshness uses metric-specific TTLs instead of one 730-day rule: FX/fuel 30d, prices/dealers 90d, policy/access 180d, annual market data 450d.",
           "数据时效按类型设置TTL，不再统一使用730天：汇率/油价30天，价格/渠道90天，政策准入180天，年度市场数据450天。"),
    ]
    st.markdown("\n".join(f"- {rule}" for rule in rules))
    st.caption(tr(MODEL_NOTICE_EN, MODEL_NOTICE_ZH))


def render_v16_executive_brief(country: str, cdata: dict):
    portfolio = V15_PORTFOLIO[country]
    governance = cdata["strategic_guardrails"]
    alignment = cdata["farizon_alignment"]
    zh = V15_GOV_ZH[country] if V15_LANG == "zh" else None
    allowed = zh["green"] if zh else governance["green_zone"]
    portfolio_rule = zh["portfolio"] if zh else alignment["portfolio_rule"]
    model_names = " / ".join(item["model"] for item in alignment["models"][:3])
    opps = _v16_country_frame(V16_OPPORTUNITIES, country)
    actions = _v16_country_frame(V16_ACTIONS, country)
    pipeline_units = int(opps["Expected Units"].sum()) if not opps.empty else 0
    next_action = actions.iloc[0]["Action"] if not actions.empty else tr(
        "Complete named-account and partner validation.",
        "完成实名客户与合作伙伴验证。",
    )
    deadline = actions.iloc[0]["Deadline"] if not actions.empty else "—"
    decision = (
        tr("Prioritise", "优先投入") if portfolio["attract"] >= 75 and portfolio["execute"] >= 60
        else tr("Conditional Go", "有条件进入") if portfolio["execute"] >= 55
        else tr("Project Only / Hold", "仅项目制 / 暂缓")
    )
    st.markdown(f"""
<div class="gtm-mission-banner">
  <div class="gtm-mission-title">🎯 {country} · {tr("Executive Brief", "管理层决策摘要")}</div>
  <div class="gtm-mission-sub">{tr("Decision first · evidence below · owner and deadline attached", "先给结论 · 下接证据 · 明确责任与期限")}</div>
</div>
""", unsafe_allow_html=True)
    brief_rows = pd.DataFrame([
        [tr("Current decision", "当前结论"), decision],
        [tr("CBU mode", "CBU模式"), v15_mode_label(portfolio["mode"])],
        [tr("Recommended models", "推荐车型"), model_names],
        [tr("Permitted zone", "允许区间"), allowed],
        [tr("Portfolio rule", "产品组合规则"), portfolio_rule],
        [tr("Recorded pipeline", "已录入项目"), f"{pipeline_units} {tr('units', '台')}"],
        [tr("Immediate action", "近期行动"), next_action],
        [tr("Deadline", "截止时间"), deadline],
    ], columns=[tr("Decision field", "决策字段"), tr("Management view", "管理判断")])
    st.dataframe(brief_rows, hide_index=True, use_container_width=True)


def render_v16_portfolio_home():
    opportunities = _prepare_opportunity_pipeline(V16_OPPORTUNITIES.copy())
    actions = V16_ACTIONS.copy()
    weighted_units = opportunities["Weighted Units"].sum()
    weighted_value = opportunities["Weighted Value USD"].sum()
    due = pd.to_datetime(actions["Deadline"], errors="coerce")
    due_60 = int(due.le(pd.Timestamp.now() + pd.Timedelta(days=60)).sum())
    high_risk = sum(1 for name, item in V15_PORTFOLIO.items() if item["attract"] - item["execute"] >= 25)
    weak_data = int(V16_METRIC_AUDIT["Confidence"].isin(["D", "E"]).sum())

    _level_hdr(
        1,
        tr("Executive Operating KPIs", "核心经营指标"),
        tr("Portfolio, pipeline, channel, risk and data health in one row.", "市场组合、项目、渠道、风险和数据健康度总览。"),
    )
    cards = [
        (tr("Tier 1 markets", "Tier 1市场"), sum(1 for x in V15_PORTFOLIO.values() if x["attract"] >= 75)),
        (tr("Active countries", "活跃机会国家"), opportunities["Country"].nunique()),
        (tr("Pipeline units", "潜在项目台数"), int(opportunities["Expected Units"].sum())),
        (tr("Weighted units", "加权台数"), round(weighted_units, 1)),
        (tr("Weighted value", "加权订单金额"), f"${weighted_value/1_000_000:.2f}m"),
        (tr("Mapped dealers", "已覆盖渠道"), len(V16_DEALERS)),
        (tr("High-risk gaps", "高风险市场"), high_risk),
        (tr("Low-confidence data", "低可信数据"), weak_data),
    ]
    for col, (label, value) in zip(st.columns(8), cards):
        with col:
            st.metric(label, value)

    _level_hdr(
        2,
        tr("Country Priority Matrix", "国家优先级矩阵"),
        tr("Attractiveness × CBU executability; bubble size = addressable segment.", "市场吸引力 × CBU可执行性；气泡大小代表目标细分市场。"),
    )
    portfolio_rows = [{
        tr("Country", "国家"): v15_country_label(name),
        "Country Key": name,
        tr("Market Attractiveness", "市场吸引力"): item["attract"],
        tr("CBU Executability", "CBU可执行性"): item["execute"],
        tr("Addressable Segment", "目标细分市场"): item["size"],
        tr("CBU Mode", "CBU模式"): v15_mode_label(item["mode"]),
        tr("Strategic Role", "战略角色"): item["role"][1 if V15_LANG == "zh" else 0],
    } for name, item in V15_PORTFOLIO.items()]
    portfolio_df = pd.DataFrame(portfolio_rows)
    fig = px.scatter(
        portfolio_df,
        x=tr("CBU Executability", "CBU可执行性"),
        y=tr("Market Attractiveness", "市场吸引力"),
        size=tr("Addressable Segment", "目标细分市场"),
        color=tr("CBU Mode", "CBU模式"),
        text=tr("Country", "国家"),
        color_discrete_map={
            v15_mode_label("Scale CBU"): "#1A8C5B",
            v15_mode_label("Controlled CBU"): "#295BA5",
            v15_mode_label("Project-Based CBU"): "#B45309",
            v15_mode_label("Validation CBU"): "#7A5AF8",
        },
        size_max=46,
        hover_data=[tr("Strategic Role", "战略角色")],
    )
    fig.add_vline(x=60, line_dash="dot", line_color="#9BA3B2")
    fig.add_hline(y=70, line_dash="dot", line_color="#9BA3B2")
    fig.update_traces(textposition="top center")
    fig.update_layout(**{**CHART_BASE, "height": 470, "margin": dict(l=35,r=20,t=25,b=25)})
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CFG, key="v16_home_matrix")

    _level_hdr(3, tr("Map & Management Attention", "地图与管理层关注"), tr("Geography on the left; opportunity, risk and data gaps on the right.", "左侧看区域分布，右侧看机会、风险和数据缺口。"))
    map_col, attention_col = st.columns([1.55, 1], gap="large")
    with map_col:
        st.plotly_chart(build_map(st.session_state.selected_country), use_container_width=True, config={"displayModeBar":False,"scrollZoom":False}, key="v16_home_map")
    with attention_col:
        st.markdown("**" + tr("Top opportunity markets", "Top机会市场") + "**")
        top_opportunity = sorted(V15_PORTFOLIO.items(), key=lambda x: (x[1]["attract"] + x[1]["execute"]), reverse=True)[:5]
        st.dataframe(pd.DataFrame([
            [v15_country_label(name), item["attract"], item["execute"], v15_mode_label(item["mode"])]
            for name, item in top_opportunity
        ], columns=[tr("Country","国家"),tr("Attract.","吸引力"),tr("Execute","执行性"),tr("Mode","模式")]), hide_index=True, use_container_width=True)
        st.markdown("**" + tr("Largest execution gaps", "最大执行缺口") + "**")
        gaps = sorted(V15_PORTFOLIO.items(), key=lambda x: x[1]["attract"]-x[1]["execute"], reverse=True)[:4]
        st.dataframe(pd.DataFrame([
            [v15_country_label(name), item["attract"]-item["execute"], v15_mode_label(item["mode"])]
            for name, item in gaps
        ], columns=[tr("Country","国家"),tr("Gap","缺口"),tr("Mode","模式")]), hide_index=True, use_container_width=True)

    _level_hdr(4, tr("Actions & Changes", "行动与变化"), tr("Current deadlines and recorded portfolio movement.", "当前行动期限和已记录组合变化。"))
    left, right = st.columns(2, gap="large")
    with left:
        st.markdown("**" + tr("Priority actions", "重点行动") + f" · {due_60} ≤60d**")
        st.dataframe(actions.sort_values(["Priority","Deadline"]), hide_index=True, use_container_width=True)
    with right:
        changes = opportunities[["Country","Project","Stage","Expected Units","Expected Close","Next Action"]].copy()
        st.markdown("**" + tr("Opportunity changes / review queue", "项目变化与复核队列") + "**")
        st.dataframe(changes, hide_index=True, use_container_width=True)

    _level_hdr(5, tr("Country Portfolio Table", "国家组合总表"), tr("One row per market; use the sidebar to enter the country war room.", "每个市场一行；通过侧栏进入国家作战室。"))
    st.dataframe(portfolio_df.drop(columns=["Country Key"]), hide_index=True, use_container_width=True)
    st.caption(tr(MODEL_NOTICE_EN, MODEL_NOTICE_ZH))


def render_v16_global_commercial():
    _level_hdr(1, tr("Customer & Channel Database", "客户与渠道数据库"), tr("Cross-country dealer, account and opportunity management.", "跨国家管理渠道、客户和项目机会。"))
    countries = sorted(set(V16_DEALERS["Country"]) | set(V16_CUSTOMERS["Country"]) | set(V16_OPPORTUNITIES["Country"]))
    selected = st.multiselect(tr("Country filter", "国家筛选"), countries, default=countries)
    dealers = V16_DEALERS[V16_DEALERS["Country"].isin(selected)]
    customers = V16_CUSTOMERS[V16_CUSTOMERS["Country"].isin(selected)]
    opps = V16_OPPORTUNITIES[V16_OPPORTUNITIES["Country"].isin(selected)].copy()
    opps["Weighted Units"] = opps["Expected Units"] * opps["Probability"]
    opps["Weighted Value USD"] = opps["Expected Units"] * opps["Unit Value USD"] * opps["Probability"]
    tabs = st.tabs([tr("Opportunity Pipeline","项目管道"),tr("Dealers","渠道数据库"),tr("Customers","客户数据库")])
    with tabs[0]:
        st.dataframe(opps, hide_index=True, use_container_width=True)
    with tabs[1]:
        st.dataframe(dealers, hide_index=True, use_container_width=True)
    with tabs[2]:
        st.dataframe(customers, hide_index=True, use_container_width=True)
    st.caption(tr(MODEL_NOTICE_EN, MODEL_NOTICE_ZH))


def render_v16_global_competitor():
    _level_hdr(1, tr("Competitive Intelligence", "竞品情报"), tr("Facts, field observations and strategic inference must remain separate.", "严格分离市场事实、一线观察和战略推断。"))
    rows = []
    for country, intel_data in INTERNAL_COMPETITOR_DATA.items():
        for record in intel_data.get("competitors", []):
            rows.append({
                tr("Country","国家"): v15_country_label(country),
                tr("Evidence layer","证据层级"): record.get(
                    "Evidence_Type",
                    "Observation" if record.get("Source_ID") else "Pending Verification"
                ),
                tr("Brand","品牌"): record.get("Brand_Type",""),
                tr("Observation","观察"): (
                    f"{record.get('Model','')} · ${record.get('Price_USD',0):,.0f} · "
                    f"{record.get('Channel_Count',0)} channels"
                ),
                tr("Implication","业务影响"): record.get("Channel_Strategy",""),
                tr("Source","来源"): record.get("Source_ID", "Internal BD Intelligence · source pending"),
            })
    intel = pd.DataFrame(rows)
    if intel.empty:
        st.info(tr("No structured competitor record.", "暂无结构化竞品记录。"))
        return
    for layer, title in [
        ("Fact", tr("Layer 1 · Market Facts","第一层 · 市场事实")),
        ("Observation", tr("Layer 2 · Channel Observations","第二层 · 渠道观察")),
        ("Pending Verification", tr("Layer 3 · Pending Verification / Inference","第三层 · 待验证与战略推断")),
    ]:
        _sdiv(title)
        subset = intel[intel[tr("Evidence layer","证据层级")].astype(str).str.contains(layer, case=False, na=False)]
        st.dataframe(subset if not subset.empty else intel.head(0), hide_index=True, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
def render_v16_logic_audit(country: str):
    """Surface textual contradictions that should be fixed before management use."""
    issues = []
    cdata = TIER1.get(country, {})
    text_blob = str(cdata).lower()
    # The platform states Pure-EV only; flag legacy diesel recommendations.
    legacy_terms = ["diesel-only", "lead exclusively with rugged", "diesel rigid", "diesel mining"]
    if any(term in text_blob for term in legacy_terms):
        issues.append(tr(
            "Legacy strategy text recommends diesel products while the platform states a Pure-EV-only product boundary.",
            "旧战略文本仍在推荐柴油车型，但平台已明确我司仅销售纯电商用车，存在战略口径冲突。",
        ))
    if country in V15_PORTFOLIO and V15_PORTFOLIO[country].get("size"):
        issues.append(tr(
            "Portfolio 'addressable segment' is still a planning-model input unless linked to V16_METRIC_AUDIT / a source ID.",
            "Portfolio中的“目标细分市场规模”目前仍属于规划模型输入，除非已关联V16_METRIC_AUDIT及Source ID。",
        ))
    if issues:
        _sdiv(tr("Logic & Evidence Warnings", "逻辑与证据预警"))
        for issue in issues:
            st.warning(issue)


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
        McKinsey UX Refactor · v16.0 · 12 Markets
    </div>
</div>
""", unsafe_allow_html=True)
    st.markdown('<div class="sb-hdr">Business Workspace</div>', unsafe_allow_html=True)
    _view_options = [
        tr("Market Portfolio", "市场组合"),
        tr("Country War Room", "国家作战室"),
        tr("Customer & Channel", "客户与渠道"),
        tr("Competitive Intelligence", "竞品情报"),
    ]
    V16_VIEW = st.radio(
        tr("Workspace", "业务工作区"),
        _view_options,
        index=1,
        label_visibility="collapsed",
        key="v16_workspace",
    )
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
    Africa CV Governance & Intelligence v{APP_VERSION}<br>
    {datetime.now().strftime('%Y-%m-%d %H:%M')} · Internal use only
</div>
""", unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════════════════════
# 15. PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
h1, h2, h3 = st.columns([3, 1, 1])
with h3:
    if st.button(
        "🌐 " + tr("切换至中文", "Switch to English"),
        key="v15_language_switch",
        use_container_width=True,
    ):
        st.session_state.v15_lang = "en" if V15_LANG == "zh" else "zh"
        st.rerun()

with h1:
    st.markdown("""
<div style="padding:18px 0 6px 0;">
    <div style="font-family:'Inter';font-size:1.28rem;font-weight:700;color:#2D3142;letter-spacing:-.3px;">
        Africa Commercial Vehicle Market & Sales Intelligence
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
        ● Intelligence Monitor
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('<hr style="margin:0 0 18px 0;border-color:#E2E5EB;">', unsafe_allow_html=True)

# V16 top-level workspaces. Country War Room deliberately falls through to the
# original map and country renderer below, preserving the established page skin.
if V16_VIEW == tr("Market Portfolio", "市场组合"):
    render_v16_portfolio_home()
    st.stop()
if V16_VIEW == tr("Customer & Channel", "客户与渠道"):
    render_v16_global_commercial()
    st.stop()
if V16_VIEW == tr("Competitive Intelligence", "竞品情报"):
    render_v16_global_competitor()
    st.stop()

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

# ─────────────────────────────────────────────────────────────────────────────
# V15 EXECUTIVE PORTFOLIO COCKPIT — retained as migration reference.
# V16 renders the live portfolio as a dedicated top-level workspace.
# ─────────────────────────────────────────────────────────────────────────────
if False:  # disabled duplicate; kept temporarily until the data-governance refactor
    portfolio_rows = []
    for country_name, item in V15_PORTFOLIO.items():
        portfolio_rows.append({
            tr("Country", "国家"): v15_country_label(country_name),
            "_country_key": country_name,
            tr("Market Attractiveness", "市场吸引力"): item["attract"],
            tr("CBU Executability", "CBU可执行性"): item["execute"],
            tr("Addressable Segment", "目标细分市场"): item["size"],
            tr("CBU Mode", "CBU模式"): v15_mode_label(item["mode"]),
            tr("Strategic Role", "战略角色"): item["role"][1 if V15_LANG == "zh" else 0],
        })
    portfolio_df = pd.DataFrame(portfolio_rows)
    portfolio_colors = {
        v15_mode_label("Scale CBU"): "#1A8C5B",
        v15_mode_label("Controlled CBU"): "#295BA5",
        v15_mode_label("Project-Based CBU"): "#B45309",
        v15_mode_label("Validation CBU"): "#7A5AF8",
    }
    portfolio_fig = px.scatter(
        portfolio_df,
        x=tr("CBU Executability", "CBU可执行性"),
        y=tr("Market Attractiveness", "市场吸引力"),
        size=tr("Addressable Segment", "目标细分市场"),
        color=tr("CBU Mode", "CBU模式"),
        text=tr("Country", "国家"),
        color_discrete_map=portfolio_colors,
        size_max=46,
        hover_data=[tr("Strategic Role", "战略角色")],
    )
    portfolio_fig.add_vline(x=60, line_dash="dot", line_color="#9BA3B2")
    portfolio_fig.add_hline(y=70, line_dash="dot", line_color="#9BA3B2")
    portfolio_fig.update_traces(textposition="top center")
    portfolio_fig.update_layout(
        **{
            **CHART_BASE,
            "height": 480,
            "margin": dict(l=35, r=20, t=25, b=25),
            "xaxis": {
                **CHART_BASE["xaxis"],
                "range": [20, 95],
                "title": tr("CBU Executability", "CBU可执行性"),
            },
            "yaxis": {
                **CHART_BASE["yaxis"],
                "range": [45, 95],
                "title": tr("Market Attractiveness", "市场吸引力"),
            },
            "legend_title_text": tr("CBU Mode", "CBU模式"),
        }
    )
    st.plotly_chart(
        portfolio_fig,
        use_container_width=True,
        config=PLOTLY_CFG,
        key="v15_portfolio_matrix",
    )
    st.dataframe(
        portfolio_df.drop(columns=["_country_key"]),
        hide_index=True,
        use_container_width=True,
    )
    attention = sorted(
        V15_PORTFOLIO.items(),
        key=lambda pair: (
            pair[1]["attract"] - pair[1]["execute"],
            pair[1]["attract"],
        ),
        reverse=True,
    )[:4]
    st.warning(
        "**" + tr("Strategic Attention", "战略关注") + "**\n\n" +
        " · ".join(
            f"{v15_country_label(name)}: {v15_mode_label(item['mode'])}"
            for name, item in attention
        )
    )

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
    render_v16_executive_brief(sel, cdata)
    tab_market, tab_customer, tab_product, tab_policy, tab_intel = st.tabs([
        tr("📊 Market & Segment", "📊 市场与场景"),
        tr("🤝 Customer & Channel", "🤝 客户与渠道"),
        tr("🎯 Product, Price & TCO", "🎯 产品、价格与TCO"),
        tr("📋 Policy, Risk & Actions", "📋 政策、风险与行动"),
        tr("🕵️ Competition & Sources", "🕵️ 竞品与来源"),
    ])

    with tab_market:
        _render_market_risk_tab(sel, cdata)
        _render_signals_tab(sel, cdata)

    with tab_customer:
        render_v16_commercial_workspace(sel)

    with tab_product:
        _render_alignment_tab(sel, cdata)
        st.info(
            tr(
                "The route-based TCO engine remains in Market & Segment in this framework release. "
                "It will be moved here when vehicle and price master data are governed.",
                "当前框架版本中，线路TCO模型仍保留在“市场与场景”。完成车型和价格主数据治理后，将整体迁移至本模块。",
            )
        )

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
        _render_due_diligence_tab(sel, cdata)
        _render_guardrails_tab(sel, cdata)
        _sdiv(tr("Action Register", "行动管理"))
        country_actions = _v16_country_frame(V16_ACTIONS, sel)
        if country_actions.empty:
            st.info(tr("No structured action has been recorded.", "尚未录入结构化行动。"))
        else:
            st.dataframe(country_actions, hide_index=True, use_container_width=True)

    with tab_intel:
        _render_competitive_intel_tab(sel, cdata)
        render_v16_data_governance(sel)
        render_v16_logic_audit(sel)

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
    &nbsp;·&nbsp; Automated RSS + curated inputs · 30-day primary / 90-day fallback
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
            <strong style="color:#5A6070;">Africa CV Market Governance & Intelligence Platform v{APP_VERSION}</strong>
            &nbsp;·&nbsp; Internal strategic use only
            &nbsp;·&nbsp; +DJ/MU/MG Strategic Expansion · Immutable TCO · Signals · Guardrails · Farizon Alignment
        </div>
        <div style="text-align:right;">
            RDB · RURA · NAAMSA · Stats SA · National Treasury ZA · ANME TN · OCP · DPFZA · MRA · JIRAMA · Reuters · Bloomberg · AfDB
            &nbsp;·&nbsp; {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

