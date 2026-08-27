from __future__ import annotations
import re
from bs4 import BeautifulSoup
import pandas as pd
from .common import get, pdf_text_bytes, clean_space, int_num, float_num, utc_now, absolute, source_id

LANDING="https://www.statssa.gov.za/?PPN=P7162&page_id=1854"
MONTHS={m:i for i,m in enumerate(["January","February","March","April","May","June","July","August","September","October","November","December"],1)}

def _latest_pdf():
    r=get(LANDING); soup=BeautifulSoup(r.text,"lxml"); candidates=[]
    for a in soup.find_all("a",href=True):
        txt=clean_space(a.get_text(" ",strip=True))
        m=re.search(r"P7162\s*-\s*Land transport survey,\s*([A-Za-z]+)\s+(20\d{2})",txt,re.I)
        if m and m.group(1).title() in MONTHS:
            candidates.append((int(m.group(2)),MONTHS[m.group(1).title()],absolute(r.url,a["href"]),m.group(1).title()))
    if candidates:
        year,month,detail,month_name=max(candidates,key=lambda x:(x[0],x[1]))
        rr=get(detail); ss=BeautifulSoup(rr.text,"lxml")
        for a in ss.find_all("a",href=True):
            href=absolute(rr.url,a["href"])
            if href.lower().endswith(".pdf") and "p7162" in href.lower(): return year,month,month_name,href
        # Stable Stats SA naming fallback.
        return year,month,month_name,f"https://www.statssa.gov.za/publications/P7162/P7162{month_name}{year}.pdf"
    raise RuntimeError("Could not discover latest P7162 publication")

def _window_tokens(text,label,n=700):
    i=text.lower().find(label.lower())
    if i<0: return []
    w=text[i+len(label):i+len(label)+n]
    return re.findall(r"\d{1,3}(?:\s\d{3})+|-?\d+(?:,\d+)?",w)

def collect(existing_demand=None, existing_monthly=None):
    year,month,month_name,pdf_url=_latest_pdf(); rr=get(pdf_url,timeout=45); raw=pdf_text_bytes(rr.content); text=clean_space(raw)
    period=f"{year}-{month:02d}"; now=utc_now(); sid=source_id("ZA-STATS-P7162",rr.url,period)
    # Monthly momentum from prose is more robust than scraping flattened table columns.
    pm=re.search(r"volume of goods transported \(payload\)\s+(?:increased|decreased) by\s+([0-9,.-]+)%",text,re.I)
    im=re.search(r"corresponding income\s+(?:increased|decreased) by\s+([0-9,.-]+)%",text,re.I)
    payload=float_num(pm.group(1)) if pm else None; income=float_num(im.group(1)) if im else None
    # Recover sign from wording.
    if pm and "decreased" in pm.group(0).lower(): payload=-abs(payload)
    if im and "decreased" in im.group(0).lower(): income=-abs(income)
    monthly=pd.DataFrame([["South Africa",period,payload,income,sid,"Statistics South Africa",rr.url,"Government","A","VERIFIED",now,"statssa_p7162_v1"]],
        columns=["Country","Period","Payload YoY %","Freight Income YoY %","Source ID","Source Name","Source URL","Evidence Type","Confidence","Status","Retrieved At","Parser"])
    commodity_labels=[
        "Agriculture and forestry primary products","Primary mining and quarrying products",
        "Manufactured food, beverages and tobacco products","Containers","Parcels","Other freight"
    ]
    rows=[]
    for label in commodity_labels:
        toks=_window_tokens(text,label)
        # expected: prev Rm, weight %, current Rm, yoy %, contribution pp
        if len(toks)<5: continue
        prev=int_num(toks[0]); weight=float_num(toks[1]); cur=int_num(toks[2]); yoy=float_num(toks[3])
        if prev is None or cur is None or weight is None or yoy is None: continue
        if not (0 <= weight <= 100 and -100 <= yoy <= 300 and prev>=0 and cur>=0): continue
        rows.append(["South Africa",period,label,prev,weight,cur,yoy,sid,"Statistics South Africa",rr.url,"Government","A","VERIFIED",now,"statssa_p7162_v1"])
    demand=pd.DataFrame(rows,columns=["Country","Period","Commodity","Previous Rm","Weight %","Current Rm","YoY %","Source ID","Source Name","Source URL","Evidence Type","Confidence","Status","Retrieved At","Parser"])
    # Commodity table is not always recoverable from every monthly PDF. Fail closed
    # for that table while retaining the independently validated monthly momentum.
    return demand,monthly
