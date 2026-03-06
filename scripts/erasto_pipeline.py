#!/usr/bin/env python3
"""Erasto Pipeline v1.0 — Fetch→Score→Allocate→Format→Send"""
import urllib.request, json, time, sys, os
from datetime import datetime, timezone

CG = "https://api.coingecko.com/api/v3"
HDR = {"User-Agent":"Erasto/2.0","Accept":"application/json"}
D = 4; ATH = 126080
ALLOC = [(4.5,5.01,50,40,10,"MAX OFFENSE"),(3.5,4.5,45,30,25,"LEAN AGGRESSIVE"),
         (2.5,3.5,35,10,55,"CAUTIOUS"),(1.5,2.5,20,0,80,"DEFENSIVE"),(1.0,1.5,5,0,95,"PRESERVATION")]

def f(url, r=2):
    for i in range(r+1):
        try:
            req=urllib.request.Request(url,headers=HDR)
            return json.loads(urllib.request.urlopen(req,timeout=15).read())
        except: 
            if i<r: time.sleep(D*(i+2))
    return None

def get_data():
    d={}
    p=f(f"{CG}/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true&include_market_cap=true")
    if p:
        d["btc"]=p.get("bitcoin",{}).get("usd",0);d["btc_24h"]=p.get("bitcoin",{}).get("usd_24h_change",0)
        d["eth"]=p.get("ethereum",{}).get("usd",0);d["sol"]=p.get("solana",{}).get("usd",0)
    time.sleep(D)
    fg=f("https://api.alternative.me/fng/?limit=1")
    d["fng"]=int(fg["data"][0]["value"]) if fg and "data" in fg else 0
    d["fng_l"]=fg["data"][0]["value_classification"] if fg and "data" in fg else "?"
    time.sleep(D)
    g=f(f"{CG}/global")
    if g and "data" in g:
        d["mcap"]=g["data"]["total_market_cap"].get("usd",0)
        d["btc_dom"]=g["data"].get("market_cap_percentage",{}).get("btc",0)
        d["vol24h"]=g["data"]["total_volume"].get("usd",0)
    time.sleep(D)
    s=f("https://stablecoins.llama.fi/stablecoins?includePrices=false")
    d["stb"]=sum(float(x.get("circulating",{}).get("peggedUSD",0) or 0) for x in s.get("peggedAssets",[])) if s else 0
    time.sleep(D)
    t=f("https://api.llama.fi/v2/historicalChainTvl")
    d["tvl"]=t[-1].get("tvl",0) if t else 0
    time.sleep(D)
    mc=f(f"{CG}/coins/bitcoin/market_chart?vs_currency=usd&days=30")
    if mc and "prices" in mc:
        pr=mc["prices"];d["btc_7d"]=(pr[-1][1]/pr[max(0,len(pr)-168)][1]-1)*100;d["btc_30d"]=(pr[-1][1]/pr[0][1]-1)*100
    time.sleep(D)
    sc=f(f"{CG}/coins/markets?vs_currency=usd&ids=aave,uniswap,maker,chainlink,render-token,ondo-finance,dogecoin,pepe,arbitrum,immutable-x&order=market_cap_desc&sparkline=false&price_change_percentage=7d,30d")
    d["sec"]=[]
    if sc and isinstance(sc,list):
        for c in sc:
            d["sec"].append({"s":c.get("symbol","?").upper(),"p":c.get("current_price",0),
                "d7":c.get("price_change_percentage_7d_in_currency",0) or 0,
                "d30":c.get("price_change_percentage_30d_in_currency",0) or 0})
    return d

PREV_STB = 271.8e9

def score(d):
    dp=(d["stb"]-PREV_STB)/PREV_STB*100 if PREV_STB else 0
    l1=4.0 if dp>10 else 3.5 if dp>5 else 3.0 if dp>0 else 2.0 if dp>-5 else 1.0
    fg=d.get("fng",25)
    l2=4.0 if fg>=75 else 3.5 if fg>=50 else 2.5 if fg>=25 else 2.0 if fg>=10 else 1.0
    ar=d.get("btc",70000)/ATH
    s1=4.5 if ar>0.9 else 3.5 if ar>0.75 else 2.5 if ar>0.6 else 1.5 if ar>0.4 else 1.0
    m=d.get("btc_30d",0)
    s2=4.0 if m>15 else 3.0 if m>5 else 2.5 if m>0 else 2.0 if m>-10 else 1.5
    l3=round((s1+s2)/2,2)
    sec=d.get("sec",[])
    pos=sum(1 for s in sec if s["d30"]>0)/len(sec) if sec else 0
    l4=3.5 if pos>0.7 else 3.0 if pos>0.5 else 2.5 if pos>0.3 else 2.0 if pos>0.1 else 1.5
    comp=round((l1+l2+l3+l4)/4,2)
    return l1,l2,l3,l4,comp,dp

def alloc(comp):
    for lo,hi,b,a,s,p in ALLOC:
        if lo<=comp<hi: return b,a,s,p
    return 5,0,95,"PRESERVATION"

def fmt(d,l1,l2,l3,l4,comp,al,dp,lang="en"):
    ts=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    btc=d.get("btc",0);eth=d.get("eth",0);fg=d.get("fng",0);fl=d.get("fng_l","?")
    sb=d["stb"]/1e9;tv=d["tvl"]/1e9;bd=d.get("btc_dom",0);sd=(d["stb"]-PREV_STB)/1e9
    ap=btc/ATH*100-100;b,a,s,ph=al
    sl=""
    for x in sorted(d.get("sec",[]),key=lambda x:x["d30"],reverse=True)[:8]:
        ic="🟢" if x["d30"]>0 else "🔴" if x["d30"]<-10 else "🟡"
        sl+=f"  {ic} {x['s']:5s} {x['d30']:+.1f}%\n"
    bar=lambda v: "█"*int(v)+"░"*(5-int(v))
    if lang=="es":
        ph2={"MAX OFFENSE":"OFENSIVA","LEAN AGGRESSIVE":"AGRESIVO","CAUTIOUS":"CAUTELOSO","DEFENSIVE":"DEFENSIVO","PRESERVATION":"PRESERVACIÓN"}.get(ph,ph)
        return f"📊 ERASTO | {ts}\n⚡ {comp}/5.0 — {ph2}\n📍 {b}% BTC | {a}% Alts | {s}% Stables\n\n₿ ${btc:,.0f} ({ap:+.0f}% ATH)\nΞ ${eth:,.0f}\n😱 {fg} ({fl})\n🏦 ${sb:.1f}B ({sd:+.1f}B)\n🔒 ${tv:.1f}B | 👑 {bd:.1f}%\n\nL1 {bar(l1)} {l1}\nL2 {bar(l2)} {l2}\nL3 {bar(l3)} {l3}\nL4 {bar(l4)} {l4}\n\n{sl}💡 +${sd:.0f}B stables = polvorín\n🤖 Erasto v3"
    return f"📊 ERASTO | {ts}\n⚡ {comp}/5.0 — {ph}\n📍 {b}% BTC | {a}% Alts | {s}% Stables\n\n₿ ${btc:,.0f} ({ap:+.0f}% ATH)\nΞ ${eth:,.0f}\n😱 {fg} ({fl})\n🏦 ${sb:.1f}B ({sd:+.1f}B)\n🔒 ${tv:.1f}B | 👑 {bd:.1f}%\n\nL1 Liquidity  {bar(l1)} {l1}/5\nL2 Macro      {bar(l2)} {l2}/5\nL3 Cycle      {bar(l3)} {l3}/5\nL4 Sectors    {bar(l4)} {l4}/5\n\n{sl}💡 +${sd:.0f}B stables = powder keg. Patience.\n🤖 Erasto v3 | Not financial advice"

def send_tg(text):
    tk=os.environ.get("TELEGRAM_BOT_TOKEN","");ci=os.environ.get("TELEGRAM_CHAT_ID","")
    if not tk or not ci: return None
    url=f"https://api.telegram.org/bot{tk}/sendMessage"
    pl=json.dumps({"chat_id":ci,"text":text}).encode()
    req=urllib.request.Request(url,data=pl,headers={"Content-Type":"application/json"})
    try:
        r=json.loads(urllib.request.urlopen(req,timeout=15).read())
        return r["result"]["message_id"] if r.get("ok") else None
    except: return None

if __name__=="__main__":
    mode=sys.argv[1] if len(sys.argv)>1 else "--dry-run"
    print("🔄 Erasto Pipeline v1.0")
    d=get_data()
    l1,l2,l3,l4,comp,dp=score(d)
    al=alloc(comp)
    print(f"✅ L1={l1} L2={l2} L3={l3} L4={l4} → {comp} → {al[3]}")
    en=fmt(d,l1,l2,l3,l4,comp,al,dp,"en")
    es=fmt(d,l1,l2,l3,l4,comp,al,dp,"es")
    os.makedirs("data",exist_ok=True)
    json.dump({"ts":datetime.now(timezone.utc).isoformat(),"btc":d.get("btc"),"eth":d.get("eth"),
        "fng":d.get("fng"),"stb":d["stb"],"tvl":d["tvl"],
        "scores":{"l1":l1,"l2":l2,"l3":l3,"l4":l4,"c":comp},
        "alloc":{"btc":al[0],"alts":al[1],"stb":al[2],"phase":al[3]}},
        open("data/current_market.json","w"),indent=2)
    print(en)
    if mode=="--send":
        m1=send_tg(en);m2=send_tg(es)
        print(f"📬 TG: {[m1,m2]}")
