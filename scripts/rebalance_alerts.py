#!/usr/bin/env python3
"""Erasto Rebalance Alerts v1.0"""
import os,json,csv

PHASES=[(4.5,5.01,50,40,10,"MAX OFFENSE"),(3.5,4.5,45,30,25,"LEAN AGGRESSIVE"),
        (2.5,3.5,35,10,55,"CAUTIOUS"),(1.5,2.5,20,0,80,"DEFENSIVE"),(1.0,1.5,5,0,95,"PRESERVATION")]
BOUNDS=[1.5,2.5,3.5,4.5]
HIST="data/score_history.csv"
CURR="data/current_market.json"
FLDS=["date","btc","eth","fng","stb_b","tvl_b","l1","l2","l3","l4","composite","phase","btc_alloc","alts_alloc","stb_alloc"]

def get_phase(s):
    for lo,hi,b,a,st,nm in PHASES:
        if lo<=s<hi: return nm,b,a,st
    return "PRESERVATION",5,0,95

def get_alloc(s):
    nm,b,a,st=get_phase(s)
    return {"btc":b,"alts":a,"stables":st,"phase":nm}

def load_last():
    if os.path.exists(HIST):
        with open(HIST) as fh:
            rows=list(csv.DictReader(fh))
            if rows:
                r=rows[-1]
                return {"date":r["date"],"composite":float(r["composite"]),"phase":r["phase"]}
    if os.path.exists(CURR):
        with open(CURR) as fh:
            cm=json.load(fh)
            return {"date":cm.get("ts","?")[:10],"composite":cm["scores"]["c"],"phase":cm["alloc"]["phase"]}
    return None

def detect_change(old_s,new_s):
    op=get_phase(old_s)[0];np_=get_phase(new_s)[0]
    delta=round(new_s-old_s,2)
    if op!=np_:
        d="UPGRADE" if new_s>old_s else "DOWNGRADE"
        return {"changed":True,"dir":d,"old_phase":op,"new_phase":np_,"old_s":old_s,"new_s":new_s,"delta":delta}
    nb=min(BOUNDS,key=lambda b:abs(new_s-b))
    return {"changed":False,"phase":op,"old_s":old_s,"new_s":new_s,"delta":delta,
            "nearest":nb,"dist":round(min(abs(new_s-b) for b in BOUNDS),2)}

def append_hist(date,sc,d,al):
    os.makedirs("data",exist_ok=True)
    exists=os.path.exists(HIST)
    row={"date":date,"btc":round(d.get("btc",0)),"eth":round(d.get("eth",0),2),
         "fng":d.get("fng",0),"stb_b":round(d.get("stb",0)/1e9,1),
         "tvl_b":round(d.get("tvl",0)/1e9,1),"l1":sc["l1"],"l2":sc["l2"],
         "l3":sc["l3"],"l4":sc["l4"],"composite":sc["composite"],
         "phase":al["phase"],"btc_alloc":al["btc"],"alts_alloc":al["alts"],"stb_alloc":al["stables"]}
    if exists:
        with open(HIST) as fh:
            rows=list(csv.DictReader(fh))
        if rows and rows[-1].get("date")==date:
            rows[-1]=row
            with open(HIST,"w",newline="") as wf:
                w=csv.DictWriter(wf,fieldnames=FLDS);w.writeheader();w.writerows(rows)
            return "updated"
    with open(HIST,"a",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=FLDS)
        if not exists:w.writeheader()
        w.writerow(row)
    return "appended"
