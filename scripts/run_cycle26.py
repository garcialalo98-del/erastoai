#!/usr/bin/env python3
"""Cycle 26: Multi-Timeframe Analysis — Run with live data"""
import sys,os,csv,json
sys.path.insert(0,os.path.dirname(__file__))
from multi_timeframe import *

D={"date":"2026-03-07","btc":67849,"eth":1973,
   "btc_24h":-4.83,"btc_7d":3.4,"btc_30d":7.9,"btc_90d":-24.0,
   "btc_1d":-4.6,"pos_7d":44.5,"pos_90d":14.6,
   "fng":18,"fng7":14.1,"fng30":10.3,
   "stb":311.8,"stb_delta":40.0,"tvl":95.8,
   "tvl30":5.8,"tvl90":((95.8-119.3)/119.3)*100,"sec_pos":0.0}

dl1=l1_daily(D["stb"],D["btc_24h"]); dl2=l2(D["fng"])
dl3=l3_daily(D["btc_1d"],D["btc_7d"],D["pos_7d"]); dl4=l4_daily(D["sec_pos"])
ds=composite(dl1,dl2,dl3,dl4); dp=phase_for(ds)

wl1=l1_weekly(D["stb"],D["stb_delta"]); wl2=l2(D["fng7"])
wl3=l3_weekly(D["btc_30d"],D["btc"]/ATH); wl4=l4_weekly(D["tvl30"],D["sec_pos"])
ws=composite(wl1,wl2,wl3,wl4); wp=phase_for(ws)

ml1=l1_monthly(D["stb"],D["tvl90"]); ml2=l2(D["fng30"])
ml3=l3_monthly(D["btc_90d"],D["pos_90d"]); ml4=l4_monthly(D["tvl90"])
ms=composite(ml1,ml2,ml3,ml4); mp=phase_for(ms)

divs=divergences(ds,ws,ms); ba,aa,sa=ALLOC[wp]

print(f"DAILY:   {ds:.2f} {dp} | L1:{dl1} L2:{dl2} L3:{dl3} L4:{dl4}")
print(f"WEEKLY:  {ws:.2f} {wp} | L1:{wl1} L2:{wl2} L3:{wl3} L4:{wl4}")
print(f"MONTHLY: {ms:.2f} {mp} | L1:{ml1} L2:{ml2} L3:{ml3} L4:{ml4}")
print(f"ALLOC: BTC {ba}% | Alts {aa}% | Stables {sa}%")
for s in divs: print(f"  {s}")

hp=os.path.join(os.path.dirname(__file__),"..","data","score_history.csv")
hist=[]
if os.path.exists(hp):
    with open(hp) as f: hist=list(csv.DictReader(f))
fields=["date","btc","eth","fng","stb_b","tvl_b","l1","l2","l3","l4",
    "composite","phase","btc_alloc","alts_alloc","stb_alloc","daily_score","monthly_score"]
if D["date"] not in [h.get("date") for h in hist]:
    hist.append({"date":D["date"],"btc":D["btc"],"eth":D["eth"],"fng":D["fng"],
        "stb_b":D["stb"],"tvl_b":D["tvl"],"l1":wl1,"l2":wl2,"l3":wl3,"l4":wl4,
        "composite":ws,"phase":wp,"btc_alloc":ba,"alts_alloc":aa,"stb_alloc":sa,
        "daily_score":ds,"monthly_score":ms})
    with open(hp,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore')
        w.writeheader()
        for h in hist: w.writerow(h)
    print(f"History: {len(hist)} entries")
