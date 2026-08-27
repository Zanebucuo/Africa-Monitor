from __future__ import annotations
import argparse, sys
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from collectors import naamsa, statssa, competitors
from services.storage import read_csv, write_csv, merge_history
from services.change_detector import detect_changes

P=ROOT/"data"/"processed"
STATUS=P/"crawler_status.csv"; CHANGES=P/"market_changes.csv"

def status_row(name,status,rows,source,error=""):
    from datetime import datetime,timezone
    return [name,status,datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),rows,source,error[:500]]

def run_market():
    statuses=[]; changes=[]; failures=0
    # NAAMSA: append period history; never delete old verified periods.
    path=P/"za_naamsa_sales.csv"; old=read_csv(path)
    try:
        new=naamsa.collect(old)
        changes.append(detect_changes(old,new,["Country","Period","Metric"],["Value"],"Vehicle sales"))
        merged=merge_history(old,new,["Country","Period","Metric"]); write_csv(merged,path)
        statuses.append(status_row("naamsa","OK",len(new),"https://naamsa.net/press-releases/"))
    except Exception as e:
        failures+=1; statuses.append(status_row("naamsa","FAILED",0,"https://naamsa.net/press-releases/",repr(e)))
    # Stats SA: append monthly and commodity histories independently.
    dpath=P/"za_freight_demand.csv"; mpath=P/"za_freight_monthly.csv"; od=read_csv(dpath); om=read_csv(mpath)
    try:
        nd,nm=statssa.collect(od,om)
        if not nd.empty:
            changes.append(detect_changes(od,nd,["Country","Period","Commodity"],["Current Rm","YoY %","Weight %"],"Freight demand"))
            write_csv(merge_history(od,nd,["Country","Period","Commodity"]),dpath)
        write_csv(merge_history(om,nm,["Country","Period"]),mpath)
        statuses.append(status_row("statssa_p7162","OK",len(nd)+len(nm),"https://www.statssa.gov.za/?PPN=P7162&page_id=1854", "Commodity table unavailable in latest PDF" if nd.empty else ""))
    except Exception as e:
        failures+=1; statuses.append(status_row("statssa_p7162","FAILED",0,"https://www.statssa.gov.za/?PPN=P7162&page_id=1854",repr(e)))
    return statuses,changes,failures

def run_competitor():
    statuses=[]; changes=[]; failures=0; path=P/"za_competitor_specs.csv"; old=read_csv(path)
    try:
        new=competitors.collect()
        changes.append(detect_changes(old,new,["Country","Farizon Model","Brand","Model"],["Price Local","Battery kWh","Range km","Payload kg","Cargo m3","Length mm","Warranty"],"Competitor"))
        write_csv(new,path)
        # History stores only changed/current snapshots with retrieval time.
        h=P/"za_competitor_history.csv"; oh=read_csv(h); hist=merge_history(oh,new,["Country","Farizon Model","Brand","Model","Retrieved At"]); write_csv(hist,h)
        statuses.append(status_row("za_competitors","OK",len(new),"Foton SA + Maxus SA"))
    except Exception as e:
        failures+=1; statuses.append(status_row("za_competitors","FAILED",0,"Foton SA + Maxus SA",repr(e)))
    return statuses,changes,failures

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--group",choices=["market","competitor","all"],default="all"); args=ap.parse_args()
    all_status=[]; all_changes=[]; failures=0
    if args.group in {"market","all"}:
        s,c,f=run_market(); all_status+=s; all_changes+=c; failures+=f
    if args.group in {"competitor","all"}:
        s,c,f=run_competitor(); all_status+=s; all_changes+=c; failures+=f
    old_status=read_csv(STATUS)
    new_status=pd.DataFrame(all_status,columns=["Collector","Status","Last Run","Rows","Source URL","Error"])
    if not old_status.empty:
        keep=old_status[~old_status["Collector"].isin(new_status["Collector"])]
        new_status=pd.concat([keep,new_status],ignore_index=True)
    write_csv(new_status,STATUS)
    change_frames=[x for x in all_changes if x is not None and not x.empty]
    if change_frames:
        old=read_csv(CHANGES); add=pd.concat(change_frames,ignore_index=True); combined=pd.concat([old,add],ignore_index=True,sort=False).tail(1000)
        write_csv(combined,CHANGES)
    elif not CHANGES.exists():
        write_csv(pd.DataFrame(columns=["Detected At","Country","Entity Type","Entity","Field","Old Value","New Value","Impact","Source URL"]),CHANGES)
    return 1 if failures else 0

if __name__=="__main__": raise SystemExit(main())
