#!/usr/bin/env python3
"""Cycle 32: Forward Performance Tracker"""
import urllib.request, json, time, sys, os, csv
from datetime import datetime, timezone
sys.path.insert(0, "scripts")
from forward_perf_tracker import add_entry, load, ALLOC

CG="https://api.coingecko.com/api/v3"
HDR={"User-Agent":"Erasto/3.0","Accept":"application/json"}
ATH=126080; PREV_STB=271.8e9; D=4

def fetch(url,r=2):
    for i in range(r+1):
        try:
            req=urllib.request.Request(url,headers=HDR)
            return json.loads(urllib.request.urlopen(req,timeout=15).read())
        except:
            if i<r: time.sleep(D*(i+1))
    return None

def get_data():
    d={}
    p=fetch(f"{CG}/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true")
    if p: d["btc"]=p["bitcoin"]["usd"]; d["eth"]=p["ethereum"]["usd"]
    time.sleep(D)
    fg=fetch("https://api.alternative.me/fng/?limit=1")
    d["fng"]=int(fg["data"][0]["value"]) if fg else 25
    d["fng_l"]=fg["data"][0]["value_classification"] if fg else "?"
    time.sleep(D)
    s=fetch("https://stablecoins.llama.fi/stablecoins?includePrices=false")
    d["stb"]=sum(float(x.get("circulating",{}).get("peggedUSD",0) or 0) for x in s.get("peggedAssets",[])) if s else 0
    time.sleep(D)
    t=fetch("https://api.llama.fi/v2/historicalChainTvl")
    d["tvl"]=t[-1]["tvl"] if t else 0
    time.sleep(D)
    mc=fetch(f"{CG}/coins/bitcoin/market_chart?vs_currency=usd&days=30")
    if mc and "prices" in mc:
        pr=mc["prices"]; d["btc_30d"]=(pr[-1][1]/pr[0][1]-1)*100
    else: d["btc_30d"]=0
    return d

def score(d):
    dp=(d["stb"]-PREV_STB)/PREV_STB*100
    l1=4.0 if dp>10 else 3.5 if dp>5 else 3.0 if dp>0 else 2.0
    fg=d.get("fng",25)
    l2=4.0 if fg>=75 else 3.5 if fg>=50 else 2.5 if fg>=25 else 2.0
    ar=d.get("btc",70000)/ATH
    s1=4.5 if ar>0.9 else 3.5 if ar>0.75 else 2.5 if ar>0.6 else 1.5
    m=d.get("btc_30d",0)
    s2=4.0 if m>15 else 3.0 if m>5 else 2.5 if m>0 else 2.0 if m>-10 else 1.5
    l3=round((s1+s2)/2,2)
    l4=2.75
    comp=round((l1+l2+l3+l4)/4,2)
    return l1,l2,l3,l4,comp

def get_phase(c):
    if c>=4.5: return "MAX OFFENSE"
    if c>=3.5: return "LEAN AGGRESSIVE"
    if c>=2.5: return "CAUTIOUS"
    if c>=1.5: return "DEFENSIVE"
    return "PRESERVATION"

def send_tg(text):
    tk=os.environ.get("TELEGRAM_BOT_TOKEN",""); ci=os.environ.get("TELEGRAM_CHAT_ID","")
    if not tk or not ci: return None
    url=f"https://api.telegram.org/bot{tk}/sendMessage"
    pl=json.dumps({"chat_id":ci,"text":text}).encode()
    req=urllib.request.Request(url,data=pl,headers={"Content-Type":"application/json"})
    try:
        r=json.loads(urllib.request.urlopen(req,timeout=15).read())
        return r.get("ok",False)
    except: return None

def seed_hist(bp,ep):
    hist=load()
    if hist: print(f"  History exists ({len(hist)} entries)"); return
    sh="data/score_history.csv"
    if not os.path.exists(sh): return
    from forward_perf_tracker import save as sv, FIELDS
    entries=[]; seen=set()
    with open(sh) as f:
        for r in csv.DictReader(f):
            key=r.get("date","")+r.get("composite","")
            if key in seen: continue
            seen.add(key)
            ph=r.get("phase","DEFENSIVE"); a=ALLOC.get(ph,(20,0,80))
            e={k:"" for k in FIELDS}
            e.update({"date":r.get("date","?"),"cycle":"seed","phase":ph,
                "score":r.get("composite","2.44"),"btc_price":r.get("btc","68000"),
                "eth_price":r.get("eth","1980"),"fng":r.get("fng","18"),
                "btc_alloc":str(a[0]),"alts_alloc":str(a[1]),"stb_alloc":str(a[2]),
                "portfolio_value":"10000","btc_hodl_value":"10000","dca_value":"10000",
                "port_ret":"0.0","hodl_ret":"0.0","dca_ret":"0.0",
                "alpha_btc":"0.0","alpha_dca":"0.0","max_dd":"0.0","win_streak":"0"})
            entries.append(e)
    sv(entries)
    print(f"  Seeded {len(entries)} entries")

def fmt_msg(e,d,l1,l2,l3,l4,comp,hist,lang="en"):
    ts=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sb=d["stb"]/1e9; sd=(d["stb"]-PREV_STB)/1e9; ap=d["btc"]/ATH*100-100
    pv=float(e["portfolio_value"]); pr=float(e["port_ret"])
    hr=float(e["hodl_ret"]); ab=float(e["alpha_btc"])
    md=float(e["max_dd"]); n=len(hist)
    B=chr(9608); b=chr(9617)
    bar=lambda v: B*int(v)+b*(5-int(v))
    ba=e["btc_alloc"]; aa=e["alts_alloc"]; sa=e["stb_alloc"]
    ph=e["phase"]; ws=e["win_streak"]
    fg=d["fng"]; fl=d["fng_l"]; btc=d["btc"]; eth=d["eth"]
    if lang=="es":
        phe={"CAUTIOUS":"CAUTELOSO","DEFENSIVE":"DEFENSIVO"}.get(ph,ph)
        return (f"ERASTO C32 | {ts}\n"
            f"{comp}/5.0 {phe}\n"
            f"{ba}% BTC | {aa}% Alts | {sa}% Stb\n\n"
            f"BTC  | F&G {fg}\n"
            f"Stables B (+B)\n\n"
            f"RENDIMIENTO ({n} entradas)\n"
            f"Portafolio:  ({pr:+.1f}%)\n"
            f"Alpha vs BTC: {ab:+.1f}%\n"
            f"DD Max: {md:.1f}%\n\n"
            f"+B stables = polvorin\n"
            f"Erasto v3 | No es consejo financiero")
    return (f"ERASTO C32 | {ts}\n"
        f"{comp}/5.0 {ph}\n"
        f"{ba}% BTC | {aa}% Alts | {sa}% Stb\n\n"
        f"BTC  ({ap:+.0f}% ATH)\n"
        f"ETH  | F&G {fg} {fl}\n"
        f"Stables B (+B)\n\n"
        f"FORWARD PERFORMANCE ({n} entries)\n"
        f"Portfolio:  ({pr:+.1f}%)\n"
        f"BTC HODL: ({hr:+.1f}%)\n"
        f"Alpha vs BTC: {ab:+.1f}%\n"
        f"Max DD: {md:.1f}% | Streak: {ws}\n\n"
        f"L1 Liquidity {bar(l1)} {l1}\n"
        f"L2 Macro     {bar(l2)} {l2}\n"
        f"L3 Cycle     {bar(l3)} {l3}\n"
        f"L4 Sectors   {bar(l4)} {l4}\n\n"
        f"+B stables = powder keg\n"
        f"Erasto v3 | Not financial advice")

if __name__=="__main__":
    print("Cycle 32: Forward Performance Tracker")
    d=get_data()
    print(f"  BTC=${d['btc']:,.0f} ETH=${d['eth']:,.0f} F&G={d['fng']} Stb=${d['stb']/1e9:.1f}B")
    l1,l2,l3,l4,comp=score(d)
    phase=get_phase(comp)
    print(f"  L1={l1} L2={l2} L3={l3} L4={l4} -> {comp} {phase}")
    seed_hist(d["btc"],d["eth"])
    entry,hist=add_entry(32,phase,comp,d["btc"],d["eth"],d["fng"],d["btc"],d["eth"])
    print(f"  Portfolio: ${float(entry['portfolio_value']):,.2f} ({entry['port_ret']}%)")
    print(f"  Alpha: {entry['alpha_btc']}% vs BTC | {entry['alpha_dca']}% vs DCA")
    print(f"  Max DD: {entry['max_dd']}% | Streak: {entry['win_streak']}")
    mkt={"date":entry["date"],"btc":d["btc"],"eth":d["eth"],"fng":d["fng"],
         "stb_b":round(d["stb"]/1e9,1),"tvl_b":round(d["tvl"]/1e9,1),
         "score":comp,"phase":phase,"portfolio_value":float(entry["portfolio_value"]),
         "port_ret":float(entry["port_ret"]),"alpha_btc":float(entry["alpha_btc"]),
         "btc_30d":round(d["btc_30d"],1)}
    with open("data/current_market.json","w") as f: json.dump(mkt,f,indent=2)
    with open("data/score_history.csv","a") as f:
        f.write(f"{entry['date']},{d['btc']},{d['eth']},{d['fng']},{d['stb']/1e9:.1f},{d['tvl']/1e9:.1f},{l1},{l2},{l3},{l4},{comp},{phase},{entry['btc_alloc']},{entry['alts_alloc']},{entry['stb_alloc']},,\n")
    en=fmt_msg(entry,d,l1,l2,l3,l4,comp,hist,"en")
    es=fmt_msg(entry,d,l1,l2,l3,l4,comp,hist,"es")
    print(en.replace("\\n","\n"))
    r1=send_tg(en.replace("\\n","\n")); r2=send_tg(es.replace("\\n","\n"))
    print(f"TG: EN={r1} ES={r2}")
    print("Done!")
