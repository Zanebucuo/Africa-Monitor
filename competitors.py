from __future__ import annotations
import re
import pandas as pd
from .common import html_text, int_num, float_num, utc_now, source_id

MODELS=[
    {"brand":"Foton","model":"eView Panel Van","url":"https://fotonsa.co.za/new-models/eview-panel-van/","farizon":["V6E","V7E"],"type":"Direct / adjacent EV van","kind":"foton"},
    {"brand":"Foton","model":"eTruckmate","url":"https://fotonsa.co.za/new-models/etruckmate/","farizon":["F1E"],"type":"Direct / adjacent electric truck","kind":"foton"},
    {"brand":"Foton","model":"eAumark 6 Ton","url":"https://fotonsa.co.za/new-models/eaumark/","farizon":["F1E"],"type":"Upper adjacent electric truck","kind":"foton"},
    {"brand":"Maxus","model":"eDeliver 3","url":"https://maxus.co.za/edeliver3/","farizon":["V6E","V7E"],"type":"Direct / adjacent EV van","kind":"maxus"},
]

def _m(pattern,text,kind="float"):
    x=re.search(pattern,text,re.I)
    if not x: return None
    return int_num(x.group(1)) if kind=="int" else float_num(x.group(1))

def _foton(text):
    price=_m(r"From\s+R\s*([0-9, ]+)",text,"int")
    battery=_m(r"Displacement \(L\)\s*\|?\s*([0-9.]+)\s*kWh",text)
    rng=_m(r"Battery Range \(km\)\s*\|?\s*([0-9.]+)",text)
    payload=_m(r"Load Weight \(kg\)\s*\|?\s*([0-9, ]+)",text,"int")
    cargo=_m(r"Load Space\s*\|?\s*([0-9.]+)\s*Cubic Metres",text)
    length=_m(r"Exterior Dimensions \(L\*W\*H mm\)\s*\|?\s*([0-9]+)",text,"int")
    w=re.search(r"Warranty\s*\|?\s*(.+?)(?:Roadside Assistance|Service Plan)",text,re.I)
    return price,battery,rng,payload,cargo,length,(w.group(1).strip() if w else "")

def _maxus(text):
    price=_m(r"(?:From|Price)\s+R\s*([0-9, ]+)",text,"int")
    battery=_m(r"Battery Capacity:?\s*([0-9.]+)\s*kWh",text)
    rng=_m(r"WLTP Combined Range:?\s*([0-9.]+)\s*km",text)
    payload=_m(r"Maximum Payload\s*:?\s*([0-9, ]+)\s*kg",text,"int")
    cargo=_m(r"Cargo Volume\s*:?\s*([0-9.]+)\s*m",text)
    length=_m(r"Overall Dimensions\s*:?\s*([0-9]+)\s*[x×]",text,"int")
    w=re.search(r"Battery Warranty\s*:?\s*([^\n]{1,100})",text,re.I)
    return price,battery,rng,payload,cargo,length,(w.group(1).strip() if w else "See OEM site")

def collect():
    rows=[]; now=utc_now()
    for cfg in MODELS:
        text,final_url=html_text(cfg["url"])
        vals=_foton(text) if cfg["kind"]=="foton" else _maxus(text)
        price,battery,rng,payload,cargo,length,warranty=vals
        # Require enough independently parseable specs to certify the row.
        known=sum(v is not None for v in [price,battery,rng,payload,cargo,length])
        if known<3: raise ValueError(f"Too few parsed fields for {cfg['brand']} {cfg['model']}: {known}")
        sid=source_id("ZA-OEM",final_url,"current")
        for fm in cfg["farizon"]:
            rows.append(["South Africa",fm,cfg["brand"],cfg["model"],cfg["type"],price,"ZAR",battery,rng,payload,cargo,length,warranty,sid,final_url,"Automated OEM","Current","Approved",now])
    return pd.DataFrame(rows,columns=["Country","Farizon Model","Brand","Model","Benchmark Type","Price Local","Currency","Battery kWh","Range km","Payload kg","Cargo m3","Length mm","Warranty","Source ID","Source URL","Evidence Type","Period","Status","Retrieved At"])
