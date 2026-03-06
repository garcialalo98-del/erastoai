#!/usr/bin/env python3
"""Erasto Alt Basket Tracker v1.0
Transforms 'X% alts' into specific tracked positions."""
import json,os
BASKET_PATH="data/alt_basket.json"
MAX_TOKENS=5
ATH_DB={
 "solana":294.33,"sui":5.35,"arbitrum":2.39,"celestia":20.91,
 "aave":661.69,"uniswap":44.92,"pendle":7.52,"render-token":13.53,
 "hyperliquid":59.34,"ondo-finance":2.14,"chainlink":52.7,
 "immutable-x":9.52,"dogecoin":0.7316,"pepe":0.00002803}

def opp_score(tid,price,d7,d30,mcap):
 ath=ATH_DB.get(tid,price*2)
 disc=min(100,max(0,(1-price/ath)*100))
 mom=min(30,max(0,d7+15))
 bounce=min(20,max(0,(-d30-5))) if d7>-3 else 0
 size=10 if mcap>1e9 else 5 if mcap>500e6 else 0
 return round(min(100,disc*0.4+mom*1.0+bounce*1.0+size),1)

def select_basket(mkt,exclude=["bitcoin","ethereum"]):
 scored=[]
 for tid,info in mkt.items():
  if tid in exclude:continue
  sc=opp_score(tid,info["usd"],info.get("d7",0),info.get("d30",0),info.get("mcap",0))
  scored.append({"id":tid,"price":info["usd"],"score":sc,"d7":info.get("d7",0),"d30":info.get("d30",0),"mcap":info.get("mcap",0),"ath_disc":round((1-info["usd"]/ATH_DB.get(tid,info["usd"]*2))*100,1)})
 scored.sort(key=lambda x:x["score"],reverse=True)
 return scored[:MAX_TOKENS]

def build_basket(selected,budget):
 n=len(selected)
 if n==0:return[]
 per=budget/n
 return[{"id":t["id"],"entry_price":t["price"],"units":per/t["price"] if t["price"]>0 else 0,"usd_alloc":round(per,2),"weight_pct":round(100/n,1),"opp_score":t["score"],"ath_disc":t["ath_disc"],"d7":t["d7"],"d30":t["d30"]} for t in selected]

def track_basket(basket,prices):
 te=sum(p["usd_alloc"] for p in basket);tn=0
 for p in basket:
  cp=prices.get(p["id"],{}).get("usd",p["entry_price"])
  p["current_price"]=cp;p["current_value"]=round(p["units"]*cp,2)
  p["pnl_usd"]=round(p["current_value"]-p["usd_alloc"],2)
  p["pnl_pct"]=round((cp/p["entry_price"]-1)*100,2) if p["entry_price"]>0 else 0
  tn+=p["current_value"]
 return basket,tn,round((tn/te-1)*100,2) if te>0 else 0

def save_basket(data,path=BASKET_PATH):
 os.makedirs(os.path.dirname(path),exist_ok=True)
 with open(path,"w") as f:json.dump(data,f,indent=2)

def format_basket_display(bd):
 lines=[f"🧺 ALT BASKET v1.0 | {bd['date']}"]
 lines.append(f"Budget: ${bd['alt_budget']:.0f} ({bd['alt_pct']}% of portfolio)")
 if bd["paper_mode"]:lines.append("⚠️ PAPER MODE (tracking only)")
 lines.append(f"Basket Return: {bd['basket_ret']:+.2f}%")
 lines.append("")
 lines.append("Token      Price     Wt%  Score  ATH")
 lines.append("─"*42)
 for p in bd["positions"]:
  sym=p["id"].upper()[:6]
  ic="🟢" if p["pnl_pct"]>=0 else "🔴"
  lines.append(f"{ic} {sym:6s} ${p['current_price']:>8.4g} {p['weight_pct']:4.0f}% {p['opp_score']:5.1f} {p['ath_disc']:+.0f}%")
 lines.append("─"*42)
 top=max(bd["positions"],key=lambda x:x["opp_score"])
 lines.append(f"⭐ Top: {top['id'].upper()} (score {top['opp_score']:.0f})")
 return"\n".join(lines)
