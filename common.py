from __future__ import annotations
import io, re, hashlib
from datetime import datetime, timezone
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

UA = "AfricaCVMonitor/21.0 (+public market research; contact repository owner)"

def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

def get(url: str, timeout: int = 30) -> requests.Response:
    r=requests.get(url,timeout=timeout,headers={"User-Agent":UA,"Accept":"text/html,application/pdf;q=0.9,*/*;q=0.8"})
    r.raise_for_status(); return r

def html_text(url: str) -> tuple[str,str]:
    r=get(url); soup=BeautifulSoup(r.text,"lxml")
    return soup.get_text(" ",strip=True), r.url

def pdf_text_bytes(raw: bytes) -> str:
    reader=PdfReader(io.BytesIO(raw))
    return "\n".join((p.extract_text() or "") for p in reader.pages)

def pdf_text(url: str) -> tuple[str,str]:
    r=get(url,timeout=45)
    return pdf_text_bytes(r.content), r.url

def clean_space(s: str) -> str:
    return re.sub(r"\s+"," ",s or "").strip()

def int_num(s):
    if s is None: return None
    x=re.sub(r"[^0-9-]","",str(s))
    return int(x) if x not in {"","-"} else None

def float_num(s):
    if s is None: return None
    x=str(s).strip().replace(" ","").replace(",",".")
    x=re.sub(r"[^0-9.\-]","",x)
    try: return float(x)
    except: return None

def source_id(prefix: str, url: str, period: str="") -> str:
    return f"{prefix}-{hashlib.sha1((url+period).encode()).hexdigest()[:10].upper()}"

def absolute(base, href): return urljoin(base, href)
