#!/usr/bin/env python3
"""Cycle 34: Multi-Asset Alt Portfolio Tracker"""
import sys,os,json,csv,time
sys.path.insert(0,os.path.dirname(__file__))
from weekly_digest import score,alloc,regime,send
from forward_perf_tracker import add_entry
from alt_basket_tracker import select_basket,build_basket,track_basket
from alt_basket_tracker import save_basket,format_basket_display
from datetime import datetime,timezone
TODAY=datetime.now(timezone.utc).strftime("%Y-%m-%d")
P={"bitcoin":{"usd":68322,"d7":4.3,"d30":-5.9,"mcap":1366e9}}
P["ethereum"]={"usd":1982.82,"d7":3.2,"d30":-6.0,"mcap":239e9}
P["solana"]={"usd":84.7,"d7":4.4,"d30":-6.8,"mcap":48.3e9}
P["sui"]={"usd":0.9015,"d7":0.6,"d30":-16.2,"mcap":3.52e9}
P["arbitrum"]={"usd":0.0999,"d7":0.1,"d30":-22.0,"mcap":0.59e9}
P["celestia"]={"usd":0.3302,"d7":3.8,"d30":-9.1,"mcap":0.29e9}
P["aave"]={"usd":111.9,"d7":-0.0,"d30":-9.9,"mcap":1.7e9}
P["uniswap"]={"usd":3.85,"d7":3.5,"d30":2.3,"mcap":2.44e9}
P["pendle"]={"usd":1.21,"d7":-2.3,"d30":-16.9,"mcap":0.2e9}
P["render-token"]={"usd":1.36,"d7":-3.5,"d30":-10.3,"mcap":0.7e9}
P["hyperliquid"]={"usd":31.01,"d7":14.2,"d30":-11.5,"mcap":7.39e9}
P["ondo-finance"]={"usd":0.2554,"d7":-0.0,"d30":-5.1,"mcap":1.24e9}
P["chainlink"]={"usd":8.78,"d7":1.3,"d30":-4.2,"mcap":6.22e9}
P["immutable-x"]={"usd":0.1564,"d7":-5.3,"d30":-11.1,"mcap":0.13e9}
P["dogecoin"]={"usd":0.0911,"d7":-2.1,"d30":-11.2,"mcap":14.0e9}
P["pepe"]={"usd":3.39e-06,"d7":-8.0,"d30":-19.1,"mcap":1.43e9}
BTC=P["bitcoin"]["usd"];ETH=P["ethereum"]["usd"]
FNG=18;STB=311.7e9;TVL=95.8e9
sec=[{"s":k,"p":v["usd"],"d7":v["d7"],"d30":v["d30"],"ath":-50} for k,v in P.items() if k not in("bitcoin","ethereum")]
d={"btc":BTC,"eth":ETH,"fng":FNG,"stb":STB,"tvl":TVL,"b7":P["bitcoin"]["d7"],"b30":P["bitcoin"]["d30"],"sec":sec}
sc=score(d);al=alloc(sc["c"]);rg=regime(d)
sel=select_basket(P)
PORTF=10000;ab=PORTF*al["a"]/100;paper=ab==0
ab_use=PORTF*0.10 if paper else ab
bsk=build_basket(sel,ab_use);bsk,tnow,bret=track_basket(bsk,P)
bd={"date":TODAY,"cycle":34,"phase":al["p"],"score":sc["c"],
 "alt_pct":al["a"],"alt_budget":ab,"portfolio_value":PORTF,
 "basket_ret":bret,"paper_mode":paper,
 "positions":[{"id":p["id"],"entry_price":p["entry_price"],
  "current_price":p["current_price"],"units":p["units"],
  "usd_alloc":p["usd_alloc"],"weight_pct":p["weight_pct"],
  "pnl_usd":p["pnl_usd"],"pnl_pct":p["pnl_pct"],
  "opp_score":p["opp_score"],"ath_disc":p["ath_disc"],
  "d7":p["d7"],"d30":p["d30"]} for p in bsk],
 "selection_universe":len(P)-2,"method":"opp_score_v1"}
save_basket(bd)
en,_=add_entry(34,al["p"],sc["c"],BTC,ETH,FNG,BTC,ETH,10000)
sf=["date","btc","eth","fng","stb_b","tvl_b","l1","l2","l3","l4","composite","phase","btc_alloc","alts_alloc","stb_alloc","daily_score","monthly_score"]
with open("data/score_history.csv","a",newline="") as f:
 w=csv.DictWriter(f,fieldnames=sf)
 w.writerow({"date":TODAY,"btc":BTC,"eth":ETH,"fng":FNG,"stb_b":311.7,"tvl_b":95.8,"l1":sc["l1"],"l2":sc["l2"],"l3":sc["l3"],"l4":sc["l4"],"composite":sc["c"],"phase":al["p"],"btc_alloc":al["b"],"alts_alloc":al["a"],"stb_alloc":al["s"],"daily_score":sc["c"],"monthly_score":sc["c"]})
mkt={"ts":TODAY,"btc":BTC,"eth":ETH,"sol":P["solana"]["usd"],
 "fng":FNG,"fngl":"Extreme Fear","stb":STB,"tvl":TVL,"bdom":63.0,
 "b7":P["bitcoin"]["d7"],"b30":P["bitcoin"]["d30"],
 "scores":{"l1":sc["l1"],"l2":sc["l2"],"l3":sc["l3"],"l4":sc["l4"],"c":sc["c"]},
 "alloc":{"b":al["b"],"a":al["a"],"s":al["s"],"p":al["p"]},
 "regime":{"r":rg["r"],"cf":rg["cf"]},
 "perf":{"pv":float(en["portfolio_value"]),"hv":float(en["btc_hodl_value"]),
  "ab":float(en["alpha_btc"]),"md":float(en["max_dd"]),"ws":int(en["win_streak"])},
 "alt_basket":{"mode":"paper" if paper else "live",
  "tokens":[p["id"] for p in bsk],"top_pick":sel[0]["id"],"top_score":sel[0]["score"]}}
with open("data/current_market.json","w") as f:json.dump(mkt,f,indent=2)
bdisp=format_basket_display(bd)
NL=chr(10)
bl=NL.join(("G "+p["id"][:8].upper()+" Sc:"+str(int(p["opp_score"]))+" ATH:"+str(int(p["ath_disc"]))+"%") for p in bsk[:5])
tg_en=f"📊 ERASTO C34|{TODAY}\n🆕 Alt Tracker LIVE\n⚡ {sc['c']} {al['p']}|{rg['r']} ({rg['cf']:.0f}%)\n📐 L1:{sc['l1']} L2:{sc['l2']} L3:{sc['l3']} L4:{sc['l4']}\n💼 BTC {al['b']}%|Alts {al['a']}%|Stb {al['s']}%\n\n{bdisp}\n\n📈 Port:${en['portfolio_value']}|HODL:${en['btc_hodl_value']}\nAlpha:{en['alpha_btc']}%|DD:{en['max_dd']}%|W{en['win_streak']}\n🔑 BTC ${BTC:,.0f} F&G {FNG} $312B stables\n{'⚠️ PAPER:0% alts' if paper else '🟢 ALT BASKET LIVE'}\n🤖 Erasto v3.4"
tg_es=f"📊 ERASTO C34|{TODAY}\n🆕 Rastreador Alt\n⚡ {sc['c']} {al['p']}|{rg['r']} ({rg['cf']:.0f}%)\n💼 BTC {al['b']}%|Alts {al['a']}%|Stb {al['s']}%\n🧺 Top 5:\n{bl}\n📈 Port:${en['portfolio_value']}|Alpha:{en['alpha_btc']}%\n{'⚠️ PAPEL:0% alts' if paper else '🟢 CANASTA ACTIVA'}\n🤖 Erasto v3.4"
r1=send(tg_en);time.sleep(1);r2=send(tg_es)
print(f"Score:{sc['c']} {al['p']}|Regime:{rg['r']}({rg['cf']:.0f}%)")
for s in sel:print(f" {s['id']:18s} Sc:{s['score']:5.1f} ATH:{s['ath_disc']:+.0f}%")
pm="paper" if paper else "live"
print(f"Basket:${ab_use:.0f}>{tnow:.2f}({bret:+.2f}%)|Mode:{pm}")
print(f"Port:${en['portfolio_value']}|Alpha:{en['alpha_btc']}%|W{en['win_streak']}")
print(f"TG:EN={'OK' if r1 else 'FAIL'}|ES={'OK' if r2 else 'FAIL'}")
print("CYCLE 34 DONE")
