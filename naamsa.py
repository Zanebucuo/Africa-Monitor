from __future__ import annotations
import re
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
from .common import get, clean_space, int_num, float_num, utc_now, absolute, source_id

LANDING="https://naamsa.net/press-releases/"
MONTHS={m:i for i,m in enumerate(["January","February","March","April","May","June","July","August","September","October","November","December"],1)}

def _discover_latest_release():
    r=get(LANDING); soup=BeautifulSoup(r.text,"lxml"); candidates=[]
    for a in soup.find_all("a",href=True):
        txt=clean_space(a.get_text(" ",strip=True))
        m=re.search(r"Media Release on the\s+([A-Za-z]+)\s+(20\d{2})\s+New Vehicle Sales stats",txt,re.I)
        if m and m.group(1).title() in MONTHS:
            candidates.append((int(m.group(2)),MONTHS[m.group(1).title()],absolute(r.url,a["href"]),txt))
    if not candidates:
        raise RuntimeError("Could not discover a naamsa monthly sales release link")
    return max(candidates,key=lambda x:(x[0],x[1]))

def _release_text(url):
    r=get(url)
    ctype=r.headers.get("content-type","").lower()
    if "pdf" in ctype or r.url.lower().endswith(".pdf"):
        from .common import pdf_text_bytes
        return clean_space(pdf_text_bytes(r.content)),r.url
    soup=BeautifulSoup(r.text,"lxml")
    # Prefer an official PDF linked from the article when present.
    for a in soup.find_all("a",href=True):
        href=absolute(r.url,a["href"])
        if href.lower().endswith(".pdf") and ("sales" in href.lower() or "naamsa" in href.lower()):
            try:
                rr=get(href,timeout=45)
                from .common import pdf_text_bytes
                return clean_space(pdf_text_bytes(rr.content)),rr.url
            except Exception:
                pass
    return clean_space(soup.get_text(" ",strip=True)),r.url

def _one(pattern,text,name,lo,hi):
    m=re.search(pattern,text,re.I)
    if not m: raise ValueError(f"Missing naamsa field: {name}")
    v=int_num(m.group(1))
    if v is None or not lo <= v <= hi: raise ValueError(f"Implausible {name}: {v}")
    return v

def collect(existing: pd.DataFrame|None=None) -> pd.DataFrame:
    year,month,url,title=_discover_latest_release(); text,source_url=_release_text(url)
    month_name=[k for k,v in MONTHS.items() if v==month][0]; period=f"{year}-{month:02d}"
    total=_one(r"Aggregate domestic new vehicle sales.*?reached\s+([0-9, ]+)\s+units",text,"total",20000,100000)
    passenger=_one(r"new passenger car market at\s+([0-9, ]+)\s+units",text,"passenger",10000,70000)
    lcv=_one(r"light commercial vehicles.*?at\s+([0-9, ]+)\s+units",text,"LCV",3000,30000)
    mcv=_one(r"medium commercial vehicles.*?to\s+([0-9, ]+)\s+units",text,"MCV",50,4000)
    heavy=_one(r"heavy trucks and buses at\s+([0-9, ]+)\s+units",text,"heavy trucks+buses",300,7000)
    if abs((passenger+lcv+mcv+heavy)-total)>100:
        raise ValueError(f"Cross-check failed: segments={passenger+lcv+mcv+heavy}, total={total}")
    sid=source_id("ZA-NAAMSA",source_url,period); now=utc_now()
    vals=[
        ("Industry total vehicle sales",total),("Passenger vehicle sales",passenger),
        ("Light CV <3501kg sales",lcv),("Medium CV 3501-8500kg sales",mcv),
        ("Heavy trucks and buses sales",heavy),
    ]
    rows=[]
    for metric,value in vals:
        rows.append(["South Africa",period,metric,value,"units",sid,"naamsa | The Automotive Business Council",source_url,"Industry official","A","VERIFIED",now,"naamsa_media_release_v1",title])
    # NEV disclosure can lag the vehicle-sales month; preserve its own period.
    nev=re.search(r"during\s+([A-Za-z]+)\s+(20\d{2}),\s+with\s+([0-9, ]+)\s+NEVs sold.*?penetration rate of\s+([0-9.,]+)%",text,re.I)
    if nev and nev.group(1).title() in MONTHS:
        np=f"{int(nev.group(2))}-{MONTHS[nev.group(1).title()]:02d}"; nv=int_num(nev.group(3)); pen=float_num(nev.group(4))
        rows += [
            ["South Africa",np,"NEV sales",nv,"units",sid,"naamsa | The Automotive Business Council",source_url,"Industry official","A","VERIFIED",now,"naamsa_media_release_v1","NEV disclosure may lag main sales month"],
            ["South Africa",np,"NEV penetration",pen,"%",sid,"naamsa | The Automotive Business Council",source_url,"Industry official","A","VERIFIED",now,"naamsa_media_release_v1","Share of domestic new light vehicle sales"],
        ]
        for label,pat in [("HEV sales",r"HEVs.*?([0-9, ]+)\s+units"),("PHEV sales",r"PHEVs.*?([0-9, ]+)\s+units"),("BEV sales",r"Battery Electric Vehicles \(BEVs\).*?([0-9, ]+)\s+units")]:
            mm=re.search(pat,text,re.I)
            if mm:
                rows.append(["South Africa",np,label,int_num(mm.group(1)),"units",sid,"naamsa | The Automotive Business Council",source_url,"Industry official","A","VERIFIED",now,"naamsa_media_release_v1",""])
    return pd.DataFrame(rows,columns=["Country","Period","Metric","Value","Unit","Source ID","Source Name","Source URL","Evidence Type","Confidence","Status","Retrieved At","Parser","Notes"])
