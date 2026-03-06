#!/usr/bin/env python3
import sys,os,json,time,urllib.request
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))
from rebalance_alerts import *
from datetime import datetime,timezone
CG="https://api.coingecko.com/api/v3"
HDR={"User-Agent":"Erasto/2.0","Accept":"application/json"}
D=4;ATH=126080;PREV_STB=271.8e9
mode=sys.argv[1] if len(sys.argv)>1 else "--dry-run"
today=datetime.now(timezone.utc).strftime("%Y-%m-%d")
def api(url):
    for i in range(3):
        try:
            req=urllib.request.Request(url,headers=HDR)
            return json.loads(urllib.request.urlopen(req,timeout=15).read())
        except:
            if i<2:time.sleep(D*(i+2))
    return None
print(f"=== Erasto Rebalance Check {today} ===")
last=load_last()
if last:print(f"Prev: {last['composite']} ({last['phase']}) {last['date']}")
d={}
p=api(CG+"/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true")
if p:d["btc"]=p["bitcoin"]["usd"];d["eth"]=p["ethereum"]["usd"];d["sol"]=p["solana"]["usd"]
time.sleep(D)
fg=api("https://api.alternative.me/fng/?limit=1")
d["fng"]=int(fg["data"][0]["value"]) if fg else 0
d["fng_label"]=fg["data"][0]["value_classification"] if fg else "?"
time.sleep(D)
s=api("https://stablecoins.llama.fi/stablecoins?includePrices=false")
d["stb"]=sum(float(x.get("circulating",{}).get("peggedUSD",0) or 0) for x in s.get("peggedAssets",[])) if s else 0
time.sleep(D)
t=api("https://api.llama.fi/v2/historicalChainTvl")
d["tvl"]=t[-1]["tvl"] if t else 0
time.sleep(D)
mc=api(CG+"/coins/bitcoin/market_chart?vs_currency=usd&days=30")
if mc and "prices" in mc:
    pr=mc["prices"];d["btc_30d"]=(pr[-1][1]/pr[0][1]-1)*100
else:d["btc_30d"]=0
time.sleep(D)
sc=api(CG+"/coins/markets?vs_currency=usd&ids=aave,uniswap,maker,chainlink,render-token,ondo-finance,dogecoin,pepe,arbitrum,immutable-x&order=market_cap_desc&sparkline=false&price_change_percentage=30d")
d["sectors"]=[]
if sc:
    for c in sc:d["sectors"].append({"sym":c.get("symbol","?").upper(),"d30":c.get("price_change_percentage_30d_in_currency",0) or 0})
dp=(d["stb"]-PREV_STB)/PREV_STB*100
l1=4.0 if dp>10 else 3.5 if dp>5 else 3.0 if dp>0 else 2.0 if dp>-5 else 1.0
fv=d.get("fng",25)
l2=4.0 if fv>=75 else 3.5 if fv>=50 else 2.5 if fv>=25 else 2.0 if fv>=10 else 1.0
ar=d.get("btc",70000)/ATH
s1=4.5 if ar>0.9 else 3.5 if ar>0.75 else 2.5 if ar>0.6 else 1.5 if ar>0.4 else 1.0
m=d.get("btc_30d",0)
s2=4.0 if m>15 else 3.0 if m>5 else 2.5 if m>0 else 2.0 if m>-10 else 1.5
l3=round((s1+s2)/2,2)
sec=d.get("sectors",[])
pos=sum(1 for x in sec if x["d30"]>0)/len(sec) if sec else 0
l4=3.5 if pos>0.7 else 3.0 if pos>0.5 else 2.5 if pos>0.3 else 2.0 if pos>0.1 else 1.5
comp=round((l1+l2+l3+l4)/4,2)
scores={"l1":l1,"l2":l2,"l3":l3,"l4":l4,"composite":comp}
al=get_alloc(comp)
old_s=last["composite"] if last else comp
chg=detect_change(old_s,comp)
res=append_hist(today,scores,d,al)
os.makedirs("data",exist_ok=True)
snap={"ts":datetime.now(timezone.utc).isoformat(),"btc":d.get("btc"),"eth":d.get("eth"),
    "fng":d.get("fng"),"stb":d.get("stb"),"tvl":d.get("tvl"),"btc_30d":d.get("btc_30d"),
    "scores":{"l1":l1,"l2":l2,"l3":l3,"l4":l4,"c":comp},"alloc":al,"rebalance":chg}
with open("data/current_market.json","w") as fh:json.dump(snap,fh,indent=2)
btc=d.get("btc",0);sb=d.get("stb",0)/1e9;fng_v=d.get("fng",0)
print(f"BTC:${btc:,.0f} F&G:{fng_v} Stb:${sb:.1f}B TVL:${d['tvl']/1e9:.1f}B")
print(f"L1={l1} L2={l2} L3={l3} L4={l4} => {comp} => {al['phase']}")
print(f"Alloc:{al['btc']}%BTC {al['alts']}%Alts {al['stables']}%Stb")
print(f"Changed:{chg['changed']} Delta:{chg['delta']} Hist:{res}")
if not chg["changed"]:print(f"Dist:{chg['dist']} Near:{chg['nearest']}")
def send_tg(txt):
    tk=os.environ.get("TELEGRAM_BOT_TOKEN","");ci=os.environ.get("TELEGRAM_CHAT_ID","")
    if not tk or not ci:return None
    pl=json.dumps({"chat_id":ci,"text":txt}).encode()
    req=urllib.request.Request(f"https://api.telegram.org/bot{tk}/sendMessage",data=pl,headers={"Content-Type":"application/json"})
    try:return json.loads(urllib.request.urlopen(req,timeout=15).read()).get("result",{}).get("message_id")
    except:return None
if mode=="--send":
    dist=chg.get("dist",0);nb=chg.get("nearest",2.5)
    if chg["changed"]:
        msg=f"REBALANCE {today}\n{chg.get('dir','')}:{chg.get('old_phase','')}->{chg.get('new_phase','')}\nScore:{chg['old_s']}->{chg['new_s']}\n{al['btc']}%BTC|{al['alts']}%Alts|{al['stables']}%Stb\nErasto v3"
    else:
        msg=f"STATUS {today}\n{al['phase']}|{comp}/5.0|d{chg['delta']:+.2f}\n{al['btc']}%BTC|{al['alts']}%Alts|{al['stables']}%Stb\nDist:{dist}pts near {nb}\nBTC${btc:,.0f}|F&G{fng_v}|Stb${sb:.1f}B\nNo rebalance.\nErasto v3"
    m=send_tg(msg);print(f"TG:{m}")
