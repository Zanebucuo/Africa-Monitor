"""
Africa Commercial Vehicle Market Governance & Intelligence
V15.0 — Executive decision skeleton

Audience: Group executives and overseas country general managers.
Purpose: understand market mechanics, monitor strategic signals, constrain
decision boundaries and align Farizon products with country opportunities.

CBU is the primary export mode. CKD/local assembly is a staged future option,
never a blanket reason to reject CBU in any country.
"""

from __future__ import annotations

from datetime import datetime
from urllib.parse import quote_plus

import feedparser
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ─────────────────────────────────────────────────────────────────────────────
# 0. PAGE AND LANGUAGE
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Africa CV Market Governance & Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
:root{
  --navy:#17243F;--orange:#D04A02;--blue:#315B8A;--ink:#252B36;
  --muted:#667085;--line:#E3E7ED;--bg:#F5F6F8;--white:#FFFFFF;
  --green:#18794E;--amber:#A15C00;--red:#B42318;
}
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"],.main{
  background:var(--bg)!important;font-family:'Inter',sans-serif!important;color:var(--ink);
}
.block-container{max-width:1500px;padding-top:1.2rem;padding-bottom:3rem;}
*{overflow-wrap:anywhere;word-break:normal;box-sizing:border-box;}
h1,h2,h3,p,div,span,label,td,th{line-height:1.45;}
[data-testid="stMetric"]{
  background:var(--white);border:1px solid var(--line);border-radius:10px;
  padding:14px 16px;box-shadow:0 2px 10px rgba(23,36,63,.04);
}
[data-testid="stMetricLabel"]{color:var(--muted);}
[data-testid="stMetricValue"]{color:var(--navy);}
.hero{
  background:linear-gradient(120deg,#17243F 0%,#243A64 72%,#D04A02 140%);
  color:white;border-radius:12px;padding:22px 28px;margin-bottom:16px;
}
.hero-title{font-size:1.45rem;font-weight:700;letter-spacing:-.02em;}
.hero-sub{font-size:.8rem;color:#D7DEEA;margin-top:6px;}
.section{
  border-left:4px solid var(--orange);padding:2px 0 2px 12px;
  margin:28px 0 14px;color:var(--navy);font-size:1rem;font-weight:700;
}
.section small{display:block;color:var(--muted);font-size:.7rem;font-weight:500;margin-top:2px;}
.card{
  background:white;border:1px solid var(--line);border-radius:10px;
  padding:16px 18px;height:100%;box-shadow:0 2px 10px rgba(23,36,63,.035);
}
.card-kicker{font-size:.65rem;font-weight:700;color:var(--orange);text-transform:uppercase;letter-spacing:.07em;}
.card-title{font-size:.88rem;font-weight:700;color:var(--navy);margin:5px 0 7px;}
.card-body{font-size:.78rem;color:#475467;}
.status{
  display:inline-block;border-radius:999px;padding:3px 9px;font-size:.66rem;
  font-weight:700;border:1px solid currentColor;
}
.data-note{
  background:#F9FAFB;border:1px solid var(--line);border-radius:8px;
  padding:9px 12px;color:var(--muted);font-size:.7rem;
}
.stTabs [data-baseweb="tab-list"]{gap:4px;flex-wrap:wrap;}
.stTabs [data-baseweb="tab"]{
  background:white;border:1px solid var(--line);border-radius:8px 8px 0 0;
  padding:8px 13px;white-space:normal;
}
div[data-testid="stDataFrame"],div[data-testid="stTable"]{background:white;border-radius:8px;}
.footer{font-size:.68rem;color:#98A2B3;text-align:center;padding:30px 0 8px;}
</style>
""",
    unsafe_allow_html=True,
)

if "lang" not in st.session_state:
    st.session_state.lang = "zh"

LANG = st.session_state.lang


def B(en: str, zh: str) -> dict[str, str]:
    return {"en": en, "zh": zh}


def L(value):
    if isinstance(value, dict) and "en" in value and "zh" in value:
        return value[LANG]
    return value


UI = {
    "switch": B("切换至中文", "Switch to English"),
    "title": B("Africa Commercial Vehicle Market Governance & Intelligence", "非洲商用车市场治理与情报看板"),
    "subtitle": B(
        "Executive decision system · market mechanics, signals, guardrails and portfolio alignment",
        "高管决策系统 · 市场机制、变化信号、战略边界与产品落位",
    ),
    "data_notice": B(
        "V15 skeleton: country figures are controlled baseline assumptions. Official/customs data automation will be connected later.",
        "V15骨架版本：国家数值为受控基准假设，官方数据与海关数据自动更新将在后续接入。",
    ),
    "country": B("Country", "国家"),
    "updated": B("Baseline date", "基准日期"),
    "confidence": B("Data confidence", "数据可信度"),
    "executive": B("Executive Portfolio", "管理层市场组合"),
    "mechanics": B("Country Mechanics", "国家市场机制"),
    "signals": B("Signals & Triggers", "信号与触发器"),
    "guardrails": B("Strategic Guardrails", "战略边界"),
    "alignment": B("Farizon Alignment", "远程车型落位"),
    "competitive": B("Competitive Intelligence", "竞争情报"),
    "market_attract": B("Market Attractiveness", "市场吸引力"),
    "cbu_exec": B("CBU Executability", "CBU可执行性"),
    "addressable": B("Addressable Segment", "目标细分市场"),
    "role": B("Strategic Role", "战略角色"),
    "cbu_mode": B("CBU Mode", "CBU模式"),
    "ckd_option": B("CKD Option", "CKD选项"),
    "direction": B("Direction", "变化方向"),
    "opportunity": B("Core Opportunity", "核心机会"),
    "constraint": B("Binding Constraint", "关键约束"),
    "attention": B("Strategic Attention List", "战略关注清单"),
    "snapshot": B("Executive Snapshot", "管理层快照"),
    "structure": B("Market Structure", "市场结构"),
    "operating": B("Market Operating Logic", "市场运作逻辑"),
    "access": B("Access & Compliance", "准入与合规"),
    "channel": B("Supply Chain & Channel", "供应链与渠道"),
    "decision": B("Purchase Decision Logic", "采购决策逻辑"),
    "scenario": B("Macro TCO Scenarios", "宏观TCO情景"),
    "evidence": B("Evidence & Confidence", "证据与可信度"),
    "signal_feed": B("Structured Signal Feed", "结构化市场信号"),
    "trigger_monitor": B("Strategic Trigger Monitor", "战略触发器"),
    "news": B("Authoritative News Input", "权威新闻输入"),
    "changed": B("What Changed Since Last Review", "较上次复核的变化"),
    "red_lines": B("Absolute Red Lines", "绝对红线"),
    "boundaries": B("Conditional Boundaries", "条件边界"),
    "permitted": B("Permitted Strategic Zone", "当前允许区间"),
    "invalid": B("Invalid Assumptions", "无效假设"),
    "products": B("Product–Market Alignment", "产品与市场落位"),
    "gaps": B("Product & Capability Gaps", "产品与能力缺口"),
    "position": B("Competitive Positioning", "竞品定位"),
    "moat": B("Competitive Moat", "竞争壁垒"),
    "winloss": B("Win / Loss Logic", "胜负逻辑"),
    "baseline": B("Baseline", "基准"),
    "stress": B("Stress", "压力"),
    "upside": B("Upside", "向上"),
    "source": B("Source", "来源"),
    "period": B("Period", "周期"),
    "status": B("Status", "状态"),
    "impact": B("Strategic implication", "战略含义"),
    "all": B("All", "全部"),
}


def T(key: str) -> str:
    return L(UI[key])


# ─────────────────────────────────────────────────────────────────────────────
# 1. CONTROLLED COUNTRY BASELINE
# ─────────────────────────────────────────────────────────────────────────────
COUNTRIES = {
    "Nigeria": {
        "label": B("Nigeria", "尼日利亚"), "iso": "NGA", "flag": "🇳🇬",
        "role": B("Scale opportunity under FX control", "外汇约束下的规模机会市场"),
        "cbu_mode": "Project-Based CBU", "ckd": "Evaluate Later",
        "attract": 82, "execute": 42, "addressable": 45200, "direction": "→",
        "confidence": "Medium", "market_cv": 45200, "ev_share": 3.8,
        "opportunity": B("High-mileage Lagos FMCG and industrial fleets", "拉各斯高里程快消与工业车队"),
        "constraint": B("Hard-currency access and port predictability", "硬通货获取与港口可预测性"),
        "summary": B(
            "Large addressable demand, but tariffs are not the binding constraint. CBU must be tied to secured USD settlement, named fleets and controlled batches.",
            "市场容量较大，但关税并非决定性约束。CBU必须绑定硬通货结算、明确终端车队和受控批次。",
        ),
        "mechanics": [
            B("SON/Form M compliance is manageable; USD availability determines whether imports are bankable.", "SON/Form M合规可管理，但美元可得性决定进口是否真正可执行。"),
            B("Large industrial groups and logistics operators control bankable demand; fragmented dealer stock is risky.", "大型工业集团与物流运营商掌握可融资需求，分散经销商库存风险较高。"),
            B("Fleet directors optimise cost per tonne-km and uptime, not EV narrative.", "车队决策者关注吨公里成本与出勤率，而不是新能源叙事。"),
        ],
        "red": [
            B("No unsecured NGN-denominated CBU receivables.", "禁止无担保的奈拉计价CBU应收账款。"),
            B("No speculative CBU inventory before off-taker and port plan are confirmed.", "未确认终端用户与港口方案前，禁止投放投机性CBU库存。"),
        ],
        "conditional": B("F1E only on captive routes with dedicated charging; CKD only after repeatable CBU volume.", "F1E仅用于具备专属充电的封闭线路；CKD仅在CBU形成可重复销量后评估。"),
        "permitted": B("Controlled CBU batches for USD-funded urban and industrial fleets.", "面向美元资金支持的城市及工业车队，采用受控批次CBU。"),
        "invalid": B("0% EV tariff does not equal bankable demand.", "零电动车关税不等于可兑现需求。"),
        "tco": [95000, 145000, .74, .12, 56.8, 91.7, 8000, .24, .40, .15],
        "products": [("V6E / V7E", "Urban FMCG", "CBU", "High"), ("F1E", "Captive industrial routes", "Project CBU", "Medium")],
        "gap": B("National aftersales reach and hard-currency fleet finance", "全国售后覆盖与硬通货车队融资"),
        "signal": B("FX remains the dominant gate despite EV tariff support.", "尽管电动车关税有利，外汇仍是主导性门槛。"),
        "trigger": B("Move to Controlled CBU only when secured USD pipeline covers two import cycles.", "只有在有担保美元订单覆盖两个进口周期后，才可升级为Controlled CBU。"),
        "competitors": [("Sinotruk", 7.5, 8.0), ("FAW", 7.2, 7.4), ("Foton", 7.0, 6.8), ("Farizon", 8.2, 3.2)],
    },
    "South Africa": {
        "label": B("South Africa", "南非"), "iso": "ZAF", "flag": "🇿🇦",
        "role": B("Premium validation and institutional fleet market", "高价值验证与机构车队市场"),
        "cbu_mode": "Controlled CBU", "ckd": "Strategic Option",
        "attract": 88, "execute": 55, "addressable": 33100, "direction": "↑",
        "confidence": "High", "market_cv": 33100, "ev_share": 1.2,
        "opportunity": B("Urban logistics and ESG-accountable fleets", "城市物流与承担ESG责任的车队"),
        "constraint": B("EV tariff disadvantage, service network and residual value", "电动车关税劣势、服务网络与残值"),
        "summary": B(
            "A mature and valuable market, but not an EV tariff haven. CBU entry should build fleet references and service credibility before national scale.",
            "这是成熟且高价值的市场，但并非电动车关税洼地。CBU应先建立车队标杆和服务信誉，再考虑全国扩张。",
        ),
        "mechanics": [
            B("NRCS and homologation are transparent but demanding; EV CBU bears a tariff disadvantage.", "NRCS与认证规则透明但严格，纯电CBU存在关税劣势。"),
            B("Leasing firms, body builders and national service networks influence fleet awards.", "租赁公司、上装企业和全国服务网络共同影响车队采购。"),
            B("Buyers require uptime, payload and residual evidence before ESG intent converts to orders.", "ESG意愿转化为订单前，客户要求出勤率、载荷与残值证据。"),
        ],
        "red": [
            B("Do not price as if EV CBU enjoys an import advantage.", "禁止按照纯电CBU享受进口优势进行定价。"),
            B("No national rollout without parts, warranty and response-time coverage.", "未建立备件、质保与响应时效覆盖前，禁止全国铺开。"),
        ],
        "conditional": B("CKD/local contract assembly may be assessed after repeatable CBU fleet demand.", "只有形成可重复的CBU车队需求后，才评估CKD或本地代工。"),
        "permitted": B("CBU reference fleets in urban logistics, municipal and premium corporate duty.", "允许在城市物流、市政及优质企业车队开展CBU标杆项目。"),
        "invalid": B("ESG commitments do not automatically become EV purchase orders.", "ESG承诺不会自动转化为电动车订单。"),
        "tco": [52000, 72000, 1.25, .16, 13.5, 32, 5500, .12, .42, .24],
        "products": [("V6E", "Courier / service fleets", "CBU", "High"), ("V7E", "Retail distribution", "CBU", "High"), ("F1E", "Closed corporate duty", "Project CBU", "Medium")],
        "gap": B("Residual-value support, right-hand-drive validation and national parts coverage", "残值支持、右舵验证与全国备件覆盖"),
        "signal": B("Fleet decarbonisation interest is rising while tariff disadvantage persists.", "车队脱碳兴趣上升，但关税劣势仍然存在。"),
        "trigger": B("Scale only after two reference fleets achieve uptime and residual milestones.", "只有两支标杆车队达到出勤率和残值里程碑后，才进入规模化。"),
        "competitors": [("Toyota", 8.4, 9.5), ("Foton", 7.2, 7.0), ("Maxus", 7.8, 5.5), ("Farizon", 8.5, 2.8)],
    },
    "Morocco": {
        "label": B("Morocco", "摩洛哥"), "iso": "MAR", "flag": "🇲🇦",
        "role": B("Industrial ecosystem and North Africa reference", "工业生态与北非标杆市场"),
        "cbu_mode": "Controlled CBU", "ckd": "Evaluate Later",
        "attract": 78, "execute": 66, "addressable": 18200, "direction": "↑",
        "confidence": "Medium", "market_cv": 18200, "ev_share": 2.5,
        "opportunity": B("Casablanca logistics and contractor-operated industrial routes", "卡萨布兰卡物流与承运商运营的工业线路"),
        "constraint": B("Identifying the real asset owner and procurement path", "识别真实资产所有者与采购路径"),
        "summary": B("OCP-linked opportunity sits in the contractor ecosystem, not only direct group procurement. CBU references should precede localisation discussion.", "OCP相关机会主要存在于承运商生态，而非仅看集团直接采购。应先建立CBU标杆，再讨论本地化。"),
        "mechanics": [
            B("European-oriented compliance rewards disciplined documentation.", "欧洲导向的合规体系要求严格的技术文件管理。"),
            B("Industrial groups, contractors and established distributors jointly control access.", "工业集团、承运商和成熟经销商共同控制市场入口。"),
            B("The operating fleet owner matters more than the headline project sponsor.", "实际车队运营者比项目名义发起方更重要。"),
        ],
        "red": [B("Do not model OCP as a simple direct truck buyer.", "禁止把OCP简单视为直接购车主体。"), B("No exclusive distributor without measurable service and account access.", "未具备可衡量服务能力与客户入口前，禁止授予独家代理。")],
        "conditional": B("Heavy EV deployment requires captive route and charging evidence.", "重型电动车投放必须具备封闭线路和充电证据。"),
        "permitted": B("CBU demonstrators for urban logistics and controlled industrial fleets.", "允许在城市物流与受控工业车队投放CBU示范项目。"),
        "invalid": B("Large mining output does not imply equally large road-truck procurement.", "矿业产量大不等于公路卡车采购量同样大。"),
        "tco": [50000, 69000, 1.35, .14, 14, 31, 6000, .08, .42, .22],
        "products": [("V6E / V7E", "Urban distribution", "CBU", "High"), ("F1E", "Industrial closed routes", "Project CBU", "Medium")],
        "gap": B("Contractor map, Arabic/French technical support and industrial account access", "承运商地图、阿拉伯语/法语技术支持与工业客户入口"),
        "signal": B("Industrial decarbonisation creates references, but procurement remains ecosystem-led.", "工业脱碳创造标杆机会，但采购仍由生态体系主导。"),
        "trigger": B("Expand after five qualified fleet owners—not only sponsors—enter the pipeline.", "只有销售管道中进入五家合格车队业主，而非仅有项目发起方后，才扩大投入。"),
        "competitors": [("Renault", 8.0, 8.5), ("Isuzu", 7.3, 7.8), ("Foton", 7.0, 6.0), ("Farizon", 8.3, 3.0)],
    },
    "Egypt": {
        "label": B("Egypt", "埃及"), "iso": "EGY", "flag": "🇪🇬",
        "role": B("High-volume, high-constraint project market", "高容量、高约束的项目型市场"),
        "cbu_mode": "Project-Based CBU", "ckd": "Strategic Option",
        "attract": 86, "execute": 38, "addressable": 39800, "direction": "→",
        "confidence": "Medium", "market_cv": 39800, "ev_share": 1.0,
        "opportunity": B("Hard-currency-funded urban and institutional fleets", "硬通货支持的城市与机构车队"),
        "constraint": B("FX allocation, payment security and subsidised diesel", "外汇分配、付款安全与柴油补贴"),
        "summary": B("CBU remains valid, but only under secured project structures. CKD is a future FX/tariff hedge, not the entry prerequisite.", "CBU仍然可行，但只能采用有付款保障的项目结构。CKD是未来外汇与关税对冲选项，而非进入前提。"),
        "mechanics": [
            B("Import approval and FX allocation jointly determine actual access.", "进口审批与外汇分配共同决定实际准入。"),
            B("Agents, banks, assemblers and public institutions shape the channel.", "代理商、银行、组装企业和公共机构共同塑造渠道。"),
            B("Payment security matters more than headline fleet demand.", "付款安全比表面车队需求更重要。"),
        ],
        "red": [B("No unsecured CBU credit exposure.", "禁止无担保的CBU信用敞口。"), B("Do not claim automatic EV TCO superiority under subsidised diesel.", "柴油受补贴时，禁止宣称电动车天然具备TCO优势。")],
        "conditional": B("CKD assessment starts only after demand, partner governance and quality gates are proven.", "只有需求、合作伙伴治理与质量门槛得到验证后，才启动CKD评估。"),
        "permitted": B("Secured CBU projects for multinational, public-backed or hard-currency fleets.", "允许面向跨国企业、公共支持或硬通货车队开展有保障的CBU项目。"),
        "invalid": B("A large market is not automatically an executable market.", "市场容量大不等于市场可执行。"),
        "tco": [54000, 76000, .31, .11, 19, 37, 6500, .28, .38, .16],
        "products": [("V6E / V7E", "Urban institutional fleets", "Project CBU", "High"), ("F1E", "Closed industrial fleets", "Project CBU", "Medium")],
        "gap": B("Payment protection, homologation partner and local technical governance", "付款保障、认证伙伴与本地技术治理"),
        "signal": B("FX availability remains more decisive than nominal policy support.", "外汇可得性仍比名义政策支持更具决定性。"),
        "trigger": B("CBU exposure contracts immediately when secured settlement falls below 100%.", "一旦有保障结算比例低于100%，立即收缩CBU敞口。"),
        "competitors": [("Chevrolet", 7.2, 8.8), ("Isuzu", 7.4, 8.0), ("Foton", 6.9, 6.8), ("Farizon", 8.2, 2.5)],
    },
    "Kenya": {
        "label": B("Kenya", "肯尼亚"), "iso": "KEN", "flag": "🇰🇪",
        "role": B("East Africa urban fleet gateway", "东非城市车队入口市场"),
        "cbu_mode": "Controlled CBU", "ckd": "Monitor",
        "attract": 74, "execute": 61, "addressable": 16800, "direction": "↑",
        "confidence": "Medium", "market_cv": 16800, "ev_share": 4.5,
        "opportunity": B("Nairobi FMCG, courier and Mombasa controlled logistics", "内罗毕快消、快递与蒙巴萨受控物流"),
        "constraint": B("Dealer service strength and fleet financing", "经销商服务能力与车队融资"),
        "summary": B("A credible East African entry market when anchored by formal fleets and depot charging; avoid confusing pilot visibility with national readiness.", "在正式车队和场站充电支持下，这是可信的东非入口市场；不能把试点曝光度误当成全国成熟度。"),
        "mechanics": [B("Standards are manageable but landed-cost assumptions need regular refresh.", "标准可管理，但落地成本假设需定期更新。"), B("Japanese brands and dealer networks set the trust benchmark.", "日系品牌和经销商网络构成信任基准。"), B("Formal fleets and leasing firms are the practical purchase gateways.", "正式车队与租赁公司是实际采购入口。")],
        "red": [B("No nationwide dealer exclusivity without service milestones.", "未达到服务里程碑前，禁止授予全国独家代理。"), B("No unsecured financing of fragmented SME demand.", "禁止为分散中小企业需求提供无担保融资。")],
        "conditional": B("Scale beyond Nairobi/Mombasa only after service and charging coverage are proven.", "只有服务与充电覆盖得到验证后，才可超出内罗毕/蒙巴萨扩张。"),
        "permitted": B("CBU deployment for anchor fleets with depot charging.", "允许向具备场站充电的核心车队投放CBU。"),
        "invalid": B("Visible pilots do not prove mass-market affordability.", "可见试点不能证明大众市场可负担性。"),
        "tco": [48000, 67000, 1.12, .18, 14, 33, 6000, .16, .40, .20],
        "products": [("V6E", "Courier", "CBU", "High"), ("V7E", "FMCG", "CBU", "High"), ("F1E", "Port logistics", "Project CBU", "Medium")],
        "gap": B("Fleet finance and service coverage outside Nairobi", "车队融资与内罗毕以外的服务覆盖"),
        "signal": B("Formal fleet electrification is rising faster than mass-market readiness.", "正式车队电动化增长快于大众市场成熟度。"),
        "trigger": B("Scale when two anchor fleets and one service hub operate above target uptime.", "两支核心车队及一个服务中心达到目标出勤率后方可扩张。"),
        "competitors": [("Isuzu", 7.5, 9.0), ("Toyota", 7.8, 8.7), ("Foton", 7.0, 6.5), ("Farizon", 8.3, 3.0)],
    },
    "Ethiopia": {
        "label": B("Ethiopia", "埃塞俄比亚"), "iso": "ETH", "flag": "🇪🇹",
        "role": B("Policy-led institutional EV market", "政策驱动的机构型电动车市场"),
        "cbu_mode": "Project-Based CBU", "ckd": "Evaluate Later",
        "attract": 73, "execute": 45, "addressable": 14200, "direction": "↑",
        "confidence": "Medium", "market_cv": 14200, "ev_share": 18.0,
        "opportunity": B("Addis Ababa institutional and fixed-route fleets", "亚的斯亚贝巴机构及固定线路车队"),
        "constraint": B("FX, charging concentration and aftersales", "外汇、充电集中度与售后"),
        "summary": B("Strong policy does not mean the operating fleet is already electrified. CBU should target funded institutional fleets and controlled corridors.", "强政策不代表存量运营车队已经电动化。CBU应聚焦有资金支持的机构车队与受控走廊。"),
        "mechanics": [B("EV import policy is favourable; FX execution is the practical gate.", "电动车进口政策有利，但外汇执行才是实际门槛。"), B("Public institutions and major groups dominate bankable demand.", "公共机构与大型集团主导可融资需求。"), B("Funding, power and service must be solved as one system.", "资金、电力与服务必须作为一个系统解决。")],
        "red": [B("Do not equate new-EV registration policy with fleet electrification.", "禁止把新能源注册政策等同于存量车队电动化。"), B("No deployment beyond service and charging corridors.", "禁止在服务和充电走廊之外投放。")],
        "conditional": B("CBU shipment requires hard-currency funding and route power confirmation.", "CBU发运必须具备硬通货资金与线路电力确认。"),
        "permitted": B("Institutionally funded CBU fleets in Addis Ababa and fixed routes.", "允许在亚的斯亚贝巴及固定线路投放机构资金支持的CBU车队。"),
        "invalid": B("An ICE import restriction does not remove affordability and uptime constraints.", "限制燃油车进口不会消除可负担性和出勤率约束。"),
        "tco": [47000, 65000, 1.05, .06, 16, 34, 6500, .20, .38, .15],
        "products": [("V6E / V7E", "Addis institutional delivery", "Project CBU", "High"), ("F1E", "Closed fleet", "Project CBU", "Medium")],
        "gap": B("Hard-currency funding, field service and charging redundancy", "硬通货资金、现场服务与充电冗余"),
        "signal": B("Policy window is open, but operational readiness remains concentrated.", "政策窗口已经打开，但运营成熟度仍高度集中。"),
        "trigger": B("Upgrade only after route power and service uptime are independently verified.", "只有线路电力与服务出勤率得到独立验证后，才升级投入。"),
        "competitors": [("Isuzu", 7.2, 8.0), ("Sinotruk", 7.0, 7.5), ("BYD", 8.4, 4.5), ("Farizon", 8.2, 2.8)],
    },
    "Algeria": {
        "label": B("Algeria", "阿尔及利亚"), "iso": "DZA", "flag": "🇩🇿",
        "role": B("Regulation-gated institutional market", "受监管门槛控制的机构市场"),
        "cbu_mode": "Project-Based CBU", "ckd": "Strategic Option",
        "attract": 72, "execute": 36, "addressable": 20500, "direction": "→",
        "confidence": "Low", "market_cv": 20500, "ev_share": .5,
        "opportunity": B("Utilities and controlled institutional fleets", "公用事业与受控机构车队"),
        "constraint": B("Import licensing and industrial policy volatility", "进口许可与产业政策波动"),
        "summary": B("Underlying demand exists, but administrative timing dominates. CBU remains the proof route whenever licences permit.", "潜在需求存在，但行政节奏占主导。只要许可允许，CBU仍是市场验证路径。"),
        "mechanics": [B("Quotas and import licences dominate formal access.", "配额与进口许可主导正式准入。"), B("Licensed importers and public-linked buyers concentrate demand.", "持证进口商与公共关联买家集中掌握需求。"), B("Partner governance matters as much as market volume.", "合作伙伴治理与市场容量同等重要。")],
        "red": [B("No speculative shipment without written import authority.", "没有书面进口许可时禁止投机性发运。"), B("No localisation commitment without governance and quality control.", "未具备治理权与质量控制前，禁止承诺本地化。")],
        "conditional": B("CKD is evaluated only through formal volume and partner gates.", "CKD只能通过正式销量与合作伙伴门槛后评估。"),
        "permitted": B("Selective CBU for licensed institutional projects.", "允许面向有许可的机构项目选择性开展CBU。"),
        "invalid": B("Large latent demand does not guarantee an open import window.", "潜在需求大不代表进口窗口开放。"),
        "tco": [53000, 76000, .28, .08, 20, 39, 5500, .10, .42, .18],
        "products": [("V7E", "Institutional distribution", "Project CBU", "Medium"), ("F1E", "Utility fleets", "Project CBU", "Medium")],
        "gap": B("Current licensing evidence and qualified industrial partner", "最新许可证据与合格产业伙伴"),
        "signal": B("Regulatory timing remains more important than underlying demand.", "监管节奏仍比潜在需求更重要。"),
        "trigger": B("No change in CBU mode without written import-window evidence.", "没有书面进口窗口证据，不改变CBU模式。"),
        "competitors": [("Renault", 7.6, 8.0), ("Mercedes", 8.0, 7.2), ("Foton", 6.8, 5.5), ("Farizon", 8.1, 2.0)],
    },
    "Tunisia": {
        "label": B("Tunisia", "突尼斯"), "iso": "TUN", "flag": "🇹🇳",
        "role": B("EU-standard compliance reference", "欧标合规参考市场"),
        "cbu_mode": "Validation CBU", "ckd": "Not Relevant",
        "attract": 65, "execute": 70, "addressable": 7600, "direction": "↑",
        "confidence": "Medium", "market_cv": 7600, "ev_share": 2.8,
        "opportunity": B("Compliant urban and depot-return fleets", "合规的城市及回场车队"),
        "constraint": B("UN-ECE homologation and technical channel quality", "UN-ECE认证与渠道技术质量"),
        "summary": B("Moderate volume but high strategic value as a compliance reference. CBU is the natural mode for homologated configurations.", "市场容量中等，但作为合规标杆具有较高战略价值。认证配置天然适合CBU模式。"),
        "mechanics": [B("UN-ECE compliance is demanding and defensible once passed.", "UN-ECE合规严格，但一旦通过便形成壁垒。"), B("Established importers and European brands concentrate trust.", "成熟进口商和欧洲品牌集中掌握市场信任。"), B("Technical competence matters more than outlet count.", "渠道技术能力比网点数量更重要。")],
        "red": [B("No shipment without accepted type-approval evidence.", "未确认型式认证证据被接受前禁止发运。"), B("Do not dilute specification to chase price.", "禁止为了追求低价而降低合规配置。")],
        "conditional": B("Heavy EV only where charging responsibility is explicit.", "重型电动车仅在充电责任明确时投放。"),
        "permitted": B("Homologated CBU for urban and depot-return reference fleets.", "允许面向城市及回场标杆车队投放已认证CBU。"),
        "invalid": B("Fiscal incentives alone do not create charging readiness.", "财政激励本身不会创造充电成熟度。"),
        "tco": [50000, 68000, .82, .12, 15, 32, 5000, .11, .40, .22],
        "products": [("V6E", "Urban service", "Validation CBU", "High"), ("V7E", "Parcel distribution", "CBU", "High")],
        "gap": B("UN-ECE dossier completeness and French technical support", "UN-ECE资料完整性与法语技术支持"),
        "signal": B("Policy advantage is improving the urban-fleet case.", "政策优势正在改善城市车队商业逻辑。"),
        "trigger": B("Move beyond validation after homologation and one full duty-cycle reference.", "完成认证并形成一个完整工况标杆后，才超越验证阶段。"),
        "competitors": [("Iveco", 7.8, 8.0), ("Renault", 7.7, 8.2), ("Foton", 6.8, 5.2), ("Farizon", 8.3, 2.4)],
    },
    "Rwanda": {
        "label": B("Rwanda", "卢旺达"), "iso": "RWA", "flag": "🇷🇼",
        "role": B("Policy showcase and standards reference", "政策样板与标准参考市场"),
        "cbu_mode": "Validation CBU", "ckd": "Not Relevant",
        "attract": 58, "execute": 82, "addressable": 2800, "direction": "↑",
        "confidence": "High", "market_cv": 2800, "ev_share": 6.5,
        "opportunity": B("Kigali institutional, hospitality and scheduled fleets", "基加利机构、酒店与定班车队"),
        "constraint": B("Small absolute market size", "绝对市场容量较小"),
        "summary": B("Policy and GB/T recognition make Rwanda a strong reference market, but inventory and revenue expectations must remain disciplined.", "政策与GB/T认可使卢旺达成为优质参考市场，但库存和营收预期必须保持克制。"),
        "mechanics": [B("Certification is pragmatic and GB/T recognition reduces technical uncertainty.", "认证务实，GB/T认可降低技术不确定性。"), B("Government, development organisations and formal fleets concentrate demand.", "政府、发展机构与正式车队集中掌握需求。"), B("Direct key-account governance is superior to broad dealer inventory.", "重点客户直管优于广泛经销商库存。")],
        "red": [B("Do not mistake policy openness for large volume.", "禁止把政策开放误判为巨大市场容量。"), B("No dispersed EV retail outside confirmed charging/service coverage.", "未确认充电与服务覆盖前，禁止分散零售电动车。")],
        "conditional": B("Scale only through repeat fleet orders, not policy headlines.", "只能依靠重复车队订单扩张，不能依靠政策新闻扩张。"),
        "permitted": B("Lean CBU reference fleets in Kigali.", "允许在基加利开展轻库存CBU标杆车队。"),
        "invalid": B("0% duty does not create a large revenue pool.", "零关税不会创造巨大的收入池。"),
        "tco": [46000, 62000, 1.22, .15, 13, 30, 4500, .15, .38, .18],
        "products": [("V6E", "Hospitality / delivery", "Validation CBU", "High"), ("V7E", "Institutional fleet", "CBU", "Medium")],
        "gap": B("Sustained private-fleet demand beyond public pilots", "公共试点之外的持续私营车队需求"),
        "signal": B("GB/T recognition lowers charging-standard risk.", "GB/T认可降低了充电标准风险。"),
        "trigger": B("Inventory remains capped until private repeat orders exceed public pilots.", "在私营重复订单超过公共试点前，库存保持上限。"),
        "competitors": [("Toyota", 7.8, 8.5), ("Isuzu", 7.3, 7.5), ("BYD", 8.3, 4.0), ("Farizon", 8.4, 2.5)],
    },
    "Djibouti": {
        "label": B("Djibouti", "吉布提"), "iso": "DJI", "flag": "🇩🇯",
        "role": B("Ethiopia corridor and port-drainage niche", "埃塞走廊与港口倒短细分市场"),
        "cbu_mode": "Project-Based CBU", "ckd": "Not Relevant",
        "attract": 60, "execute": 64, "addressable": 1600, "direction": "↑",
        "confidence": "Low", "market_cv": 1600, "ev_share": 1.0,
        "opportunity": B("Captive port-to-yard and port-to-rail cycles", "封闭的港到堆场与港到铁路循环"),
        "constraint": B("Operator access, heat and charging-site rights", "运营商入口、高温与充电场地权利"),
        "summary": B("Domestic volume is small; strategic value comes from Ethiopia-linked port logistics. F1E is relevant only on captive, measured routes.", "国内容量较小，战略价值来自与埃塞相关的港口物流。F1E只适用于封闭且可测量的线路。"),
        "mechanics": [B("Port concessions and site power matter more than retail regulation.", "港口特许权与场地电力比零售监管更重要。"), B("A few terminal and corridor operators control demand.", "少数码头及走廊运营商控制需求。"), B("Route productivity and heat management decide procurement.", "线路生产率与热管理决定采购。")],
        "red": [B("Do not judge opportunity by domestic registrations alone.", "禁止仅依据国内注册量判断机会。"), B("No open-corridor EV tractor deployment before route validation.", "线路验证前禁止投放开放走廊电动牵引车。")],
        "conditional": B("Requires captive charging, telemetry and operator accountability.", "必须具备封闭充电、车联网数据与明确运营责任。"),
        "permitted": B("CBU port-drainage pilot with named terminal operator.", "允许与明确码头运营商开展CBU港口倒短试点。"),
        "invalid": B("Small national market does not mean zero strategic corridor value.", "国家市场小不代表走廊战略价值为零。"),
        "tco": [98000, 155000, 1.15, .20, 55, 95, 9000, .09, .42, .15],
        "products": [("F1E", "Port drayage", "Project CBU", "High"), ("V7E", "Free-zone logistics", "CBU", "Medium")],
        "gap": B("High-temperature validation and terminal charging agreement", "高温验证与码头充电协议"),
        "signal": B("Corridor value is rising with Ethiopia-linked throughput.", "随着埃塞相关吞吐增长，走廊价值上升。"),
        "trigger": B("Scale only after pilot telemetry proves uptime and energy performance.", "只有试点车联网数据证明出勤率与能耗表现后才扩张。"),
        "competitors": [("Mercedes", 8.0, 7.5), ("Sinotruk", 7.0, 8.0), ("Volvo", 8.3, 6.0), ("Farizon", 8.5, 1.8)],
    },
    "Mauritius": {
        "label": B("Mauritius", "毛里求斯"), "iso": "MUS", "flag": "🇲🇺",
        "role": B("Premium low-volume green showcase", "高端低容量绿色样板市场"),
        "cbu_mode": "Validation CBU", "ckd": "Not Relevant",
        "attract": 55, "execute": 84, "addressable": 1900, "direction": "↑",
        "confidence": "Medium", "market_cv": 1900, "ev_share": 8.0,
        "opportunity": B("Hospitality, airport, municipal and premium fleets", "酒店、机场、市政与优质车队"),
        "constraint": B("Small volume and reputation-sensitive service", "容量较小且服务声誉敏感"),
        "summary": B("CBU is the natural mode. Value comes from high-quality visible references, not inventory-led volume.", "CBU是天然模式。价值来自高质量可见标杆，而非库存驱动的规模。"),
        "mechanics": [B("Import rules are transparent; island durability is the product gate.", "进口规则透明，海岛耐久性是产品门槛。"), B("Established distributors and formal fleets concentrate demand.", "成熟经销商与正式车队集中掌握需求。"), B("Reputation and uptime outweigh discount-led selling.", "品牌声誉与出勤率比折扣销售更重要。")],
        "red": [B("No volume-led speculative inventory.", "禁止以规模为导向的投机库存。"), B("No entry through a weak service partner.", "禁止通过服务能力弱的合作伙伴进入。")],
        "conditional": B("Specification must address corrosion, cyclone and charging continuity.", "配置必须应对腐蚀、气旋与充电连续性。"),
        "permitted": B("Premium CBU reference fleets with disciplined inventory.", "允许开展库存克制的高端CBU标杆车队。"),
        "invalid": B("A favourable EV market does not imply large unit volume.", "电动车环境友好不代表销量巨大。"),
        "tco": [52000, 68000, 1.40, .19, 12, 29, 4000, .09, .44, .25],
        "products": [("V6E", "Hospitality / service", "Validation CBU", "High"), ("V7E", "Airport logistics", "CBU", "Medium")],
        "gap": B("Island durability package and premium service partner", "海岛耐久配置与优质服务伙伴"),
        "signal": B("Corporate decarbonisation supports visible reference fleets.", "企业脱碳推动可见标杆车队。"),
        "trigger": B("Keep stock linked to contracted demand and service capacity.", "库存必须与已签约需求和服务能力挂钩。"),
        "competitors": [("Toyota", 8.0, 9.0), ("Isuzu", 7.4, 7.5), ("BYD", 8.4, 4.5), ("Farizon", 8.5, 2.2)],
    },
    "Madagascar": {
        "label": B("Madagascar", "马达加斯加"), "iso": "MDG", "flag": "🇲🇬",
        "role": B("Infrastructure-constrained mining niche", "基础设施约束下的矿业细分市场"),
        "cbu_mode": "Project-Based CBU", "ckd": "Not Relevant",
        "attract": 52, "execute": 30, "addressable": 4200, "direction": "→",
        "confidence": "Low", "market_cv": 4200, "ev_share": .3,
        "opportunity": B("Mining, utilities and controlled compounds", "矿业、公用事业与受控园区"),
        "constraint": B("Roads, grid, recovery and service reach", "道路、电网、救援与服务覆盖"),
        "summary": B("CBU must not be rejected, but product and scenario selection must be strict. EV is limited to captive operations with dedicated charging.", "不能全盘否定CBU，但必须严格选择产品和场景。电动车仅限具备专属充电的封闭作业。"),
        "mechanics": [B("Physical infrastructure is a larger barrier than formal certification.", "物理基础设施比正式认证构成更大门槛。"), B("Mining firms, utilities and NGOs concentrate formal demand.", "矿业企业、公用事业与NGO集中掌握正式需求。"), B("Recovery capability and parts lead time determine purchase risk.", "救援能力与备件周期决定采购风险。")],
        "red": [B("No dispersed retail EV selling.", "禁止分散零售电动车。"), B("No specialised shipment without anchor operator and recovery plan.", "没有核心运营商与救援方案时，禁止发运专用车辆。")],
        "conditional": B("EV requires captive power, inspected routes and technical operator.", "电动车必须具备封闭电力、已勘察线路和技术运营方。"),
        "permitted": B("CBU for mining, utilities and controlled urban compounds.", "允许面向矿业、公用事业及受控城市园区开展CBU。"),
        "invalid": B("Country infrastructure weakness does not justify blanket CBU rejection.", "国家基础设施薄弱不能成为全盘否定CBU的理由。"),
        "tco": [62000, 88000, 1.18, .24, 20, 42, 4500, .18, .35, .12],
        "products": [("V6E", "Controlled compounds", "Project CBU", "Low"), ("F1E", "Closed mining duty", "Project CBU", "Medium")],
        "gap": B("Ruggedisation, recovery network and captive charging", "强化适应性、救援网络与封闭充电"),
        "signal": B("Mining investment creates selective demand; national EV readiness remains low.", "矿业投资创造选择性需求，但全国电动车成熟度仍低。"),
        "trigger": B("No EV project without route, power and recovery validation.", "没有线路、电力与救援验证，不开展电动车项目。"),
        "competitors": [("Toyota", 8.0, 8.5), ("Mercedes", 8.1, 6.5), ("Sinotruk", 6.9, 5.5), ("Farizon", 8.2, 1.5)],
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# 2. SHARED HELPERS AND MODELS
# ─────────────────────────────────────────────────────────────────────────────
PLOT = {
    "displayModeBar": False,
    "responsive": True,
}

MODE_COLORS = {
    "Scale CBU": "#18794E",
    "Controlled CBU": "#315B8A",
    "Project-Based CBU": "#A15C00",
    "Validation CBU": "#7A5AF8",
}

MODE_LABELS = {
    "Scale CBU": B("Scale CBU", "规模化CBU"),
    "Controlled CBU": B("Controlled CBU", "受控CBU"),
    "Project-Based CBU": B("Project-Based CBU", "项目型CBU"),
    "Validation CBU": B("Validation CBU", "验证型CBU"),
    "CBU": B("CBU", "CBU整车"),
    "Project CBU": B("Project CBU", "项目型CBU"),
}
CKD_LABELS = {
    "Not Relevant": B("Not Relevant", "暂不相关"),
    "Monitor": B("Monitor", "持续观察"),
    "Evaluate Later": B("Evaluate Later", "后续评估"),
    "Strategic Option": B("Strategic Option", "战略备选"),
}
CONFIDENCE_LABELS = {
    "High": B("High", "高"),
    "Medium": B("Medium", "中"),
    "Low": B("Low", "低"),
    "Open": B("Open", "待验证"),
}
FIT_LABELS = {
    "High": B("High", "高"),
    "Medium": B("Medium", "中"),
    "Low": B("Low", "低"),
}
APPLICATION_LABELS = {
    "Urban FMCG": B("Urban FMCG", "城市快消"),
    "Captive industrial routes": B("Captive industrial routes", "封闭工业线路"),
    "Courier / service fleets": B("Courier / service fleets", "快递/服务车队"),
    "Retail distribution": B("Retail distribution", "零售配送"),
    "Closed corporate duty": B("Closed corporate duty", "企业封闭工况"),
    "Urban distribution": B("Urban distribution", "城市配送"),
    "Industrial closed routes": B("Industrial closed routes", "封闭工业线路"),
    "Urban institutional fleets": B("Urban institutional fleets", "城市机构车队"),
    "Closed industrial fleets": B("Closed industrial fleets", "封闭工业车队"),
    "Courier": B("Courier", "快递"),
    "FMCG": B("FMCG", "快消"),
    "Port logistics": B("Port logistics", "港口物流"),
    "Addis institutional delivery": B("Addis institutional delivery", "亚的斯机构配送"),
    "Closed fleet": B("Closed fleet", "封闭车队"),
    "Institutional distribution": B("Institutional distribution", "机构配送"),
    "Utility fleets": B("Utility fleets", "公用事业车队"),
    "Urban service": B("Urban service", "城市服务"),
    "Parcel distribution": B("Parcel distribution", "包裹配送"),
    "Hospitality / delivery": B("Hospitality / delivery", "酒店/配送"),
    "Institutional fleet": B("Institutional fleet", "机构车队"),
    "Port drayage": B("Port drayage", "港口倒短"),
    "Free-zone logistics": B("Free-zone logistics", "自贸区物流"),
    "Hospitality / service": B("Hospitality / service", "酒店/服务"),
    "Airport logistics": B("Airport logistics", "机场物流"),
    "Controlled compounds": B("Controlled compounds", "受控园区"),
    "Closed mining duty": B("Closed mining duty", "封闭矿区工况"),
}


def local_mode(value: str) -> str:
    return L(MODE_LABELS.get(value, B(value, value)))


def local_ckd(value: str) -> str:
    return L(CKD_LABELS.get(value, B(value, value)))


def local_confidence(value: str) -> str:
    return L(CONFIDENCE_LABELS.get(value, B(value, value)))


def local_fit(value: str) -> str:
    return L(FIT_LABELS.get(value, B(value, value)))


def local_application(value: str) -> str:
    return L(APPLICATION_LABELS.get(value, B(value, value)))


def section(title: str, subtitle: str = ""):
    st.markdown(
        f'<div class="section">{title}<small>{subtitle}</small></div>',
        unsafe_allow_html=True,
    )


def card(kicker: str, title: str, body: str):
    st.markdown(
        f"""
<div class="card">
  <div class="card-kicker">{kicker}</div>
  <div class="card-title">{title}</div>
  <div class="card-body">{body}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def local_country(name: str) -> str:
    return L(COUNTRIES[name]["label"])


def portfolio_df() -> pd.DataFrame:
    return pd.DataFrame([
        {
            T("country"): local_country(name),
            "country_key": name,
            T("market_attract"): d["attract"],
            T("cbu_exec"): d["execute"],
            T("addressable"): d["addressable"],
            T("cbu_mode"): local_mode(d["cbu_mode"]),
            T("direction"): d["direction"],
            "iso": d["iso"],
        }
        for name, d in COUNTRIES.items()
    ])


def cumulative_tco(country: str, scenario: str) -> tuple[pd.DataFrame, float | None]:
    p = COUNTRIES[country]["tco"]
    ice_capex, ev_capex, diesel, power, ice_cons, ev_cons, monthly_km, interest, ice_res, ev_res = p
    factors = {
        "Baseline": (1.00, 1.00, 1.00),
        "Stress": (.90, 1.15, 1.25),
        "Upside": (1.20, .90, .80),
    }
    diesel_f, power_f, finance_f = factors[scenario]
    diesel *= diesel_f
    power *= power_f
    interest *= finance_f
    months = np.arange(0, 61)
    ice_energy = diesel * ice_cons / 100 * monthly_km
    ev_energy = power * ev_cons / 100 * monthly_km
    ice_financed = ice_capex * (1 + interest * months / 12)
    ev_financed = ev_capex * (1 + interest * months / 12)
    ice_cost = ice_financed + ice_energy * months
    ev_cost = ev_financed + ev_energy * months
    ice_cost[-1] -= ice_capex * ice_res
    ev_cost[-1] -= ev_capex * ev_res
    delta = ice_cost - ev_cost
    idx = np.where(delta >= 0)[0]
    breakeven = float(idx[0]) if len(idx) and idx[0] > 0 else None
    df = pd.DataFrame({
        "Month": months,
        "ICE": ice_cost,
        "EV": ev_cost,
    }).melt("Month", var_name="Powertrain", value_name="Cost")
    return df, breakeven


def mode_implication(mode: str) -> str:
    mapping = {
        "Scale CBU": B("Repeatable CBU import and channel scale", "可重复的CBU进口与渠道规模化"),
        "Controlled CBU": B("Limit batch, inventory, geography and customer type", "限制批次、库存、区域与客户类型"),
        "Project-Based CBU": B("Only named projects with secured conditions", "仅开展条件有保障的明确项目"),
        "Validation CBU": B("Certification, samples and reference fleets", "认证、样车与标杆车队验证"),
    }
    return L(mapping[mode])


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_news(query: str, limit: int = 5) -> list[dict]:
    authoritative = (
        "(site:reuters.com OR site:worldbank.org OR site:afdb.org OR "
        "site:gov.za OR site:gov.ng OR site:gov.ma OR site:gov.rw) when:30d"
    )
    url = (
        "https://news.google.com/rss/search?q="
        + quote_plus(f"{query} {authoritative}")
        + "&hl=en&gl=US&ceid=US:en"
    )
    try:
        feed = feedparser.parse(url)
        result = []
        for item in feed.entries[:limit]:
            result.append({
                T("period"): item.get("published", "")[:16],
                "Headline" if LANG == "en" else "新闻标题": item.get("title", ""),
                T("source"): item.get("source", {}).get("title", "Google News"),
                "URL": item.get("link", ""),
            })
        return result
    except Exception:
        return []


# ─────────────────────────────────────────────────────────────────────────────
# 3. GLOBAL HEADER AND NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────
top_left, top_right = st.columns([8, 1.6])
with top_right:
    if st.button(f"🌐 {T('switch')}", use_container_width=True):
        st.session_state.lang = "en" if LANG == "zh" else "zh"
        st.rerun()

st.markdown(
    f"""
<div class="hero">
  <div class="hero-title">🌍 {T("title")}</div>
  <div class="hero-sub">{T("subtitle")} · V15.0</div>
</div>
""",
    unsafe_allow_html=True,
)
st.markdown(f'<div class="data-note">ℹ️ {T("data_notice")}</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"### {T('country')}")
    selected_country = st.selectbox(
        T("country"),
        list(COUNTRIES),
        format_func=local_country,
        label_visibility="collapsed",
    )
    sd = COUNTRIES[selected_country]
    st.markdown(f"## {sd['flag']} {local_country(selected_country)}")
    st.markdown(
        f'<span class="status" style="color:{MODE_COLORS[sd["cbu_mode"]]}">{local_mode(sd["cbu_mode"])}</span>',
        unsafe_allow_html=True,
    )
    st.caption(mode_implication(sd["cbu_mode"]))
    st.divider()
    st.metric(T("market_attract"), f"{sd['attract']}/100")
    st.metric(T("cbu_exec"), f"{sd['execute']}/100")
    st.metric(T("addressable"), f"{sd['addressable']:,}")
    st.divider()
    st.caption(f"{T('updated')}: 2026-07-29")
    st.caption(f"{T('confidence')}: {local_confidence(sd['confidence'])}")
    st.caption(B("CBU = primary · CKD = staged option", "CBU为主力 · CKD为分阶段备选")[LANG])

tabs = st.tabs([
    f"01 · {T('executive')}",
    f"02 · {T('mechanics')}",
    f"03 · {T('signals')}",
    f"04 · {T('guardrails')}",
    f"05 · {T('alignment')}",
    f"06 · {T('competitive')}",
])


# ─────────────────────────────────────────────────────────────────────────────
# 4. TAB 1 — EXECUTIVE PORTFOLIO
# ─────────────────────────────────────────────────────────────────────────────
with tabs[0]:
    section(T("executive"), B("Where to play · how strongly to enter · what needs attention", "去哪里投入 · 以何种强度进入 · 当前关注什么")[LANG])
    pdf = portfolio_df()
    fig = px.scatter(
        pdf,
        x=T("cbu_exec"),
        y=T("market_attract"),
        size=T("addressable"),
        color=T("cbu_mode"),
        text=T("country"),
        color_discrete_map={local_mode(k): v for k, v in MODE_COLORS.items()},
        size_max=48,
        hover_data=[T("addressable"), T("direction")],
    )
    fig.add_vline(x=60, line_dash="dot", line_color="#98A2B3")
    fig.add_hline(y=70, line_dash="dot", line_color="#98A2B3")
    fig.update_traces(textposition="top center")
    fig.update_layout(
        height=520, paper_bgcolor="white", plot_bgcolor="white",
        margin=dict(l=30, r=20, t=30, b=20), legend_title_text=T("cbu_mode"),
        xaxis=dict(range=[20, 95], gridcolor="#EEF1F4"),
        yaxis=dict(range=[45, 95], gridcolor="#EEF1F4"),
    )
    st.plotly_chart(fig, use_container_width=True, config=PLOT)

    table = pd.DataFrame([
        {
            T("country"): f"{d['flag']} {local_country(n)}",
            T("role"): L(d["role"]),
            T("cbu_mode"): local_mode(d["cbu_mode"]),
            T("ckd_option"): local_ckd(d["ckd"]),
            T("direction"): d["direction"],
            T("opportunity"): L(d["opportunity"]),
            T("constraint"): L(d["constraint"]),
        }
        for n, d in COUNTRIES.items()
    ])
    st.dataframe(table, use_container_width=True, hide_index=True, height=450)

    section(T("attention"), B("Markets where opportunity, constraint or evidence requires renewed judgement", "机会、约束或证据变化需要重新判断的市场")[LANG])
    attention = sorted(
        COUNTRIES.items(),
        key=lambda x: (x[1]["attract"] - x[1]["execute"], x[1]["attract"]),
        reverse=True,
    )[:4]
    cols = st.columns(4)
    for col, (name, d) in zip(cols, attention):
        with col:
            card(
                local_mode(d["cbu_mode"]),
                f"{d['flag']} {local_country(name)}",
                f"<b>{L(d['constraint'])}</b><br>{L(d['trigger'])}",
            )


# ─────────────────────────────────────────────────────────────────────────────
# 5. TAB 2 — COUNTRY MECHANICS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[1]:
    d = COUNTRIES[selected_country]
    section(f"{d['flag']} {local_country(selected_country)} · {T('snapshot')}", L(d["role"]))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(T("cbu_mode"), local_mode(d["cbu_mode"]))
    c2.metric(T("ckd_option"), local_ckd(d["ckd"]))
    c3.metric(T("market_attract"), f"{d['attract']}/100")
    c4.metric(T("cbu_exec"), f"{d['execute']}/100")
    st.info(L(d["summary"]))

    section(T("structure"), B("Controlled baseline — replace with customs and registration feeds later", "受控基准——后续接入海关与注册数据")[LANG])
    s1, s2, s3 = st.columns(3)
    s1.metric(B("Annual CV market", "商用车年度市场")[LANG], f"{d['market_cv']:,}")
    s2.metric(B("EV share proxy", "电动车份额估算")[LANG], f"{d['ev_share']:.1f}%")
    s3.metric(T("addressable"), f"{d['addressable']:,}")

    section(T("operating"), B("How access, channels and purchase decisions actually work", "准入、渠道与采购决策如何真实运作")[LANG])
    cols = st.columns(3)
    labels = [T("access"), T("channel"), T("decision")]
    for col, label, body in zip(cols, labels, d["mechanics"]):
        with col:
            card(B("MARKET MECHANIC", "市场机制")[LANG], label, L(body))

    section(T("scenario"), B("Fixed management scenarios — no customer quotation variables", "固定管理情景——不包含客户报价变量")[LANG])
    scenario_labels = {"Baseline": T("baseline"), "Stress": T("stress"), "Upside": T("upside")}
    scenario_tabs = st.tabs(list(scenario_labels.values()))
    for scenario, stab in zip(scenario_labels, scenario_tabs):
        with stab:
            tdf, be = cumulative_tco(selected_country, scenario)
            fig_tco = px.line(
                tdf, x="Month", y="Cost", color="Powertrain",
                color_discrete_map={"ICE": "#667085", "EV": "#D04A02"},
                labels={
                    "Month": B("Month", "月份")[LANG],
                    "Cost": B("Cumulative cost", "累计成本")[LANG],
                    "Powertrain": B("Powertrain", "动力类型")[LANG],
                },
            )
            fig_tco.update_layout(
                height=390, paper_bgcolor="white", plot_bgcolor="white",
                margin=dict(l=20, r=20, t=20, b=20),
                yaxis_title="USD", xaxis_title=B("Month", "月份")[LANG],
                legend_title_text="",
            )
            st.plotly_chart(fig_tco, use_container_width=True, config=PLOT)
            be_text = (
                B(f"Month {be:.0f}", f"第{be:.0f}个月")[LANG]
                if be is not None else B("No parity within 60 months", "60个月内未达到平衡")[LANG]
            )
            st.caption(f"{scenario_labels[scenario]} · {B('TCO parity', 'TCO平衡点')[LANG]}: {be_text}")

    section(T("evidence"), B("Facts, assumptions and known gaps are kept separate", "事实、假设与已知缺口分开呈现")[LANG])
    evidence_df = pd.DataFrame([
        {
            B("Evidence type", "证据类型")[LANG]: B("Controlled baseline", "受控基准")[LANG],
            B("Item", "项目")[LANG]: B("Market and TCO parameters", "市场与TCO参数")[LANG],
            T("source"): B("Existing TIER1 research", "现有TIER1研究")[LANG],
            T("confidence"): local_confidence(d["confidence"]),
            T("period"): "2026",
        },
        {
            B("Evidence type", "证据类型")[LANG]: B("Strategic judgement", "战略判断")[LANG],
            B("Item", "项目")[LANG]: L(d["summary"]),
            T("source"): B("Management synthesis", "管理判断综合")[LANG],
            T("confidence"): local_confidence("Medium"),
            T("period"): "2026-07",
        },
        {
            B("Evidence type", "证据类型")[LANG]: B("Known gap", "已知缺口")[LANG],
            B("Item", "项目")[LANG]: L(d["gap"]),
            T("source"): B("Requires validation", "需要验证")[LANG],
            T("confidence"): local_confidence("Open"),
            T("period"): "Next review",
        },
    ])
    st.dataframe(evidence_df, hide_index=True, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# 6. TAB 3 — SIGNALS & TRIGGERS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[2]:
    d = COUNTRIES[selected_country]
    section(T("signal_feed"), B("Events translated into strategic meaning", "把事件转化为战略含义")[LANG])
    signal_df = pd.DataFrame([
        {
            T("period"): "2026-07",
            B("Signal type", "信号类型")[LANG]: B("Policy / Market", "政策/市场")[LANG],
            B("What happened", "发生了什么")[LANG]: L(d["signal"]),
            T("impact"): L(d["trigger"]),
            B("Importance", "重要度")[LANG]: local_confidence("High"),
        },
        {
            T("period"): "2026-07",
            B("Signal type", "信号类型")[LANG]: B("Evidence Gap", "证据缺口")[LANG],
            B("What happened", "发生了什么")[LANG]: L(d["gap"]),
            T("impact"): B("Do not upgrade market commitment until validated.", "在验证完成前，不升级市场投入。")[LANG],
            B("Importance", "重要度")[LANG]: local_confidence("Medium"),
        },
    ])
    st.dataframe(signal_df, hide_index=True, use_container_width=True)

    section(T("trigger_monitor"), B("The condition that changes the strategic mode", "能够改变战略模式的条件")[LANG])
    tc1, tc2 = st.columns([1, 2])
    with tc1:
        st.metric(T("status"), local_mode(d["cbu_mode"]), d["direction"])
        st.caption(mode_implication(d["cbu_mode"]))
    with tc2:
        st.warning(f"**{T('impact')}**\n\n{L(d['trigger'])}")

    section(T("changed"), B("Skeleton baseline for future review-to-review comparison", "为后续逐次复核比较预留的骨架")[LANG])
    changed_df = pd.DataFrame([
        {
            B("Previous view", "上次判断")[LANG]: local_mode(d["cbu_mode"]),
            B("Current view", "当前判断")[LANG]: local_mode(d["cbu_mode"]),
            B("Reason", "变化原因")[LANG]: L(d["signal"]),
            B("Mode changed?", "模式是否变化")[LANG]: B("No", "否")[LANG],
        }
    ])
    st.dataframe(changed_df, hide_index=True, use_container_width=True)

    section(T("news"), B("Raw input only — structured signals above remain the management output", "仅作为原始输入——上方结构化信号才是管理输出")[LANG])
    if st.button(B("Refresh authoritative news", "刷新权威新闻")[LANG], key=f"news_{selected_country}"):
        st.cache_data.clear()
    news = fetch_news(f"{selected_country} commercial vehicle EV logistics")
    if news:
        st.dataframe(pd.DataFrame(news), hide_index=True, use_container_width=True)
    else:
        st.info(B("No live feed available. The strategic skeleton remains usable offline.", "当前无法获取实时新闻，战略骨架仍可离线使用。")[LANG])


# ─────────────────────────────────────────────────────────────────────────────
# 7. TAB 4 — STRATEGIC GUARDRAILS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[3]:
    d = COUNTRIES[selected_country]
    section(T("guardrails"), B("Boundaries that prevent strategy drift and false confidence", "防止战略漂移与错误自信的判断边界")[LANG])
    section(T("red_lines"))
    for item in d["red"]:
        st.error(L(item))
    section(T("boundaries"))
    st.warning(L(d["conditional"]))
    section(T("permitted"))
    st.success(L(d["permitted"]))
    section(T("invalid"))
    st.info(L(d["invalid"]))
    st.markdown(
        f"""
<div class="data-note">
<b>{B("CBU group boundary", "CBU集团战略边界")[LANG]}:</b> {B(
    "CBU is the primary export mode. Country risk changes the intensity and structure of CBU—not its blanket validity. CKD is a staged future option.",
    "CBU是当前主力出口模式。国家风险改变的是CBU的投入强度和结构，而不是全盘否定其有效性。CKD仅为分阶段的未来选项。",
)[LANG]}
</div>
""",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# 8. TAB 5 — FARIZON ALIGNMENT
# ─────────────────────────────────────────────────────────────────────────────
with tabs[4]:
    d = COUNTRIES[selected_country]
    section(T("products"), L(d["role"]))
    product_rows = []
    for model, application, mode, fit in d["products"]:
        product_rows.append({
            B("Farizon model", "远程车型")[LANG]: model,
            B("Target application", "目标场景")[LANG]: local_application(application),
            B("Entry mode", "进入模式")[LANG]: local_mode(mode) if mode in MODE_LABELS else mode,
            B("Fit", "适配度")[LANG]: local_fit(fit),
            B("Must be true", "成立条件")[LANG]: L(d["permitted"]),
            B("Do not use when", "不适用条件")[LANG]: L(d["conditional"]),
        })
    st.dataframe(pd.DataFrame(product_rows), hide_index=True, use_container_width=True)

    section(T("gaps"), B("What the portfolio or operating model cannot yet cover", "当前产品或运营模式尚不能覆盖什么")[LANG])
    g1, g2 = st.columns(2)
    with g1:
        card(B("CAPABILITY GAP", "能力缺口")[LANG], B("Current gap", "当前缺口")[LANG], L(d["gap"]))
    with g2:
        card(
            B("PORTFOLIO RULE", "产品组合规则")[LANG],
            local_mode(d["cbu_mode"]),
            f"{mode_implication(d['cbu_mode'])}<br><br><b>CKD:</b> {local_ckd(d['ckd'])}",
        )


# ─────────────────────────────────────────────────────────────────────────────
# 9. TAB 6 — COMPETITIVE INTELLIGENCE
# ─────────────────────────────────────────────────────────────────────────────
with tabs[5]:
    d = COUNTRIES[selected_country]
    section(T("position"), B("Product proposition vs. local channel strength", "产品主张与本地渠道实力对比")[LANG])
    comp = pd.DataFrame(d["competitors"], columns=[
        B("Brand", "品牌")[LANG],
        B("Product proposition", "产品竞争力")[LANG],
        B("Channel strength", "渠道实力")[LANG],
    ])
    fig_comp = px.scatter(
        comp,
        x=B("Channel strength", "渠道实力")[LANG],
        y=B("Product proposition", "产品竞争力")[LANG],
        text=B("Brand", "品牌")[LANG],
        color=B("Brand", "品牌")[LANG],
    )
    fig_comp.update_traces(marker_size=18, textposition="top center")
    fig_comp.update_layout(
        height=430, showlegend=False, paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(range=[0, 10], gridcolor="#EEF1F4"),
        yaxis=dict(range=[5, 10], gridcolor="#EEF1F4"),
        margin=dict(l=30, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_comp, use_container_width=True, config=PLOT)

    section(T("moat"))
    m1, m2, m3 = st.columns(3)
    with m1:
        card(B("PRODUCT", "产品")[LANG], B("Our potential edge", "我司潜在优势")[LANG], B("Purpose-built EV platform and urban operating economics", "正向电动平台与城市运营经济性")[LANG])
    with m2:
        card(B("CHANNEL", "渠道")[LANG], B("Incumbent moat", "既有品牌壁垒")[LANG], L(d["gap"]))
    with m3:
        card(B("DECISION", "决策")[LANG], B("What price cannot solve", "降价无法解决什么")[LANG], L(d["constraint"]))

    section(T("winloss"))
    winloss = pd.DataFrame([
        {
            B("Outcome", "结果")[LANG]: B("Win", "赢")[LANG],
            B("Logic", "逻辑")[LANG]: L(d["opportunity"]),
            B("Evidence required", "所需证据")[LANG]: L(d["permitted"]),
        },
        {
            B("Outcome", "结果")[LANG]: B("Lose", "输")[LANG],
            B("Logic", "逻辑")[LANG]: L(d["constraint"]),
            B("Evidence required", "所需证据")[LANG]: L(d["gap"]),
        },
    ])
    st.dataframe(winloss, hide_index=True, use_container_width=True)


st.markdown(
    f'<div class="footer">{T("title")} · V15.0 · '
    f'{datetime.now().strftime("%Y-%m-%d")} · '
    f'{B("CBU primary / CKD staged option", "CBU主力 / CKD分阶段备选")[LANG]}</div>',
    unsafe_allow_html=True,
)
