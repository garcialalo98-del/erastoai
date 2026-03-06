#!/usr/bin/env python3
"""Cycle 28: Score Prediction Model"""
import json,csv,os,urllib.request,datetime
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from score_predictor import predict,triggers,phase_for,ALLOC,LN,ATH
from multi_timeframe import l1_weekly,l2,l3_weekly,l4_weekly,composite

def fetch(url):
    r=urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Erasto/2.0"}),timeout=15)
    return json.loads(r.read())

print("📡 Fetching...")
pr=fetch("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true")
fg=fetch("https://api.alternative.me/fng/?limit=1")
st=fetch("https://stablecoins.llama.fi/stablecoins?includePrices=true")
tv=fetch("https://api.llama.fi/v2/historicalChainTvl")
bd=fetch("https://api.coingecko.com/api/v3/coins/bitcoin?localization=false&tickers=false&community_data=false&developer_data=false&sparkline=false")

btc=pr['bitcoin']['usd'];eth=pr['ethereum']['usd']
btc24=pr['bitcoin'].get('usd_24h_change',0)
fng=int(fg['data'][0]['value'])
stb=sum(float(s.get('circulating',{}).get('peggedUSD',0) or 0) for s in st.get('peggedAssets',[]))
tvl_val=tv[-1]['tvl'] if tv else 0
m30=bd['market_data'].get('price_change_percentage_30d',0)
ath_r=btc/ATH;stb_delta=(stb/1e9)-272
tvl30=(tvl_val-tv[-31]['tvl'])/tv[-31]['tvl']*100 if len(tv)>31 else 0
now=datetime.datetime.now(datetime.timezone.utc)
today=now.strftime("%Y-%m-%d");ts=now.strftime("%Y-%m-%d %H:%M")
print(f"BTC ${btc:,.0f}|ETH ${eth:,.0f}|F&G {fng}|Stb ${stb/1e9:.1f}B|TVL ${tvl_val/1e9:.1f}B")

s1=l1_weekly(stb/1e9,stb_delta);s2=l2(fng)
s3=l3_weekly(m30,ath_r);s4=l4_weekly(tvl30,50)
comp=composite(s1,s2,s3,s4);phase,_,_=phase_for(comp)
ba,aa,sa=ALLOC.get(phase,(5,0,95))
print(f"Score:{comp} {phase}|L1:{s1} L2:{s2} L3:{s3} L4:{s4}")

hpath="../data/score_history.csv";rows=[]
if os.path.exists(hpath):
    with open(hpath) as f: rows=list(csv.DictReader(f))
nr={"date":today,"btc":btc,"eth":eth,"fng":fng,"stb_b":f"{stb/1e9:.1f}",
    "tvl_b":f"{tvl_val/1e9:.1f}","l1":s1,"l2":s2,"l3":s3,"l4":s4,
    "composite":comp,"phase":phase,"btc_alloc":ba,"alts_alloc":aa,
    "stb_alloc":sa,"daily_score":"","monthly_score":""}
if not rows or rows[-1].get('date')!=today: rows.append(nr)
else: rows[-1]=nr
flds=list(nr.keys())
with open(hpath,'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=flds);w.writeheader();w.writerows(rows)

pred=predict(rows[-min(len(rows),5):])
trigs=triggers([s1,s2,s3,s4],btc,fng,stb,tvl_val)
if pred:
    ft=min(pred['scenarios'],key=lambda s:abs(s['chg']) if s['chg']>0 else 99)
    pred['fastest']=ft

def fmt_tg(p):
    b,a,s=p['alloc']
    m=f"🔮 ERASTO PREDICTION MODEL\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    m+=f"📍 {p['score']:.2f} {p['phase']}\n💼 BTC {b}% | Alts {a}% | Stb {s}%\n"
    m+=f"💰 ${btc:,.0f} | F&G {fng} | ${stb/1e9:.0f}B\n\n"
    m+=f"📏 PHASE DISTANCE\n⬆ {p['up']}: {p['du']:.2f}pts\n"
    m+=f"⬇ {p['dn']}: {p['dd']:.2f}pts buffer\n"
    m+=f"⚡ Vel: {p['cv']:+.2f}/period\n\n🎯 LEVEL FORECAST\n"
    for sc in p['scenarios']:
        a2="⬆" if sc['vel']>0.2 else ("↗" if sc['vel']>0 else ("↘" if sc['vel']>-0.2 else "⬇"))
        m+=f"{a2} {sc['level'][:2]}: {sc['cur']:.1f}->{sc['tgt']:.1f} [{sc['feas']}]\n"
    ft=p.get('fastest',p['scenarios'][0])
    m+=f"\n🚀 FASTEST: {ft['level']}\n{ft['cur']:.1f}->{ft['tgt']:.1f} ({ft['feas']})\n"
    m+=f"\n⏰ {ts} UTC\n📊 Research only • NFA"
    return m

def fmt_es(p):
    ph={"CAUTIOUS":"CAUTELOSO","DEFENSIVE":"DEFENSIVO","LEAN AGGRESSIVE":"AGRESIVO"}
    b,a,s=p['alloc']
    m=f"🔮 ERASTO MODELO PREDICTIVO\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    m+=f"📍 {p['score']:.2f} {ph.get(p['phase'],p['phase'])}\n"
    m+=f"💼 BTC {b}% | Alts {a}% | Stb {s}%\n"
    m+=f"💰 ${btc:,.0f} | Miedo {fng} | ${stb/1e9:.0f}B\n\n🎯 PRONOSTICO\n"
    for sc in p['scenarios']:
        a2="⬆" if sc['vel']>0.2 else ("↗" if sc['vel']>0 else ("↘" if sc['vel']>-0.2 else "⬇"))
        fe={"HIGH":"ALTA","MED":"MEDIA","LOW":"BAJA"}.get(sc['feas'],sc['feas'])
        m+=f"{a2} {sc['level'][:2]}: {sc['cur']:.1f}->{sc['tgt']:.1f} [{fe}]\n"
    ft=p.get('fastest',p['scenarios'][0])
    m+=f"\n🚀 VIA RAPIDA: {ft['level']}\n⏰ {ts} UTC\n📊 Solo investigacion"
    return m

def fmt_full(p):
    L=["🔮 ERASTO SCORE PREDICTION MODEL v1.0","━"*44,
       f"📍 Score: {p['score']:.2f} {p['phase']}",
       f"💼 BTC {p['alloc'][0]}% | Alts {p['alloc'][1]}% | Stb {p['alloc'][2]}%",
       f"💰 BTC ${btc:,.0f} | F&G {fng} | Stb ${stb/1e9:.0f}B","",
       "📏 PHASE BOUNDARIES","─"*44]
    L.append(f"⬆ -> {p['up']}: {p['du']:.2f}pts needed")
    if p['up']:
        ub=ALLOC.get(p['up'],(0,0,0))
        L.append(f"   New: BTC {ub[0]}% Alts {ub[1]}% Stb {ub[2]}%")
    L+=[f"⬇ -> {p['dn']}: {p['dd']:.2f}pts buffer","",
        f"⚡ VELOCITY: {p['cv']:+.2f}/period | Avg: {p['av']:+.02f}","",
        "🎯 LEVEL FORECAST","─"*44]
    for sc in p['scenarios']:
        a="⬆" if sc['vel']>0.2 else ("↗" if sc['vel']>0 else ("↘" if sc['vel']>-0.2 else "⬇"))
        L.append(f"{a} {sc['level']}: {sc['cur']:.1f}->{sc['tgt']:.1f} (+{sc['chg']:.1f}) [{sc['feas']}]")
    ft=p.get('fastest',p['scenarios'][0])
    L+=[f"\n🚀 FASTEST: {ft['level']} ({ft['feas']})","",
        "🌍 TRIGGER CATALOG","━"*44]
    for lv,val,ups,dns in trigs:
        L.append(f"\n{lv} ({val:.1f})")
        for u in ups[:2]: L.append(f"  📈 {u}")
        for d in dns[:1]: L.append(f"  📉 {d}")
    return "\n".join(L)

tg_en=fmt_tg(pred);tg_es=fmt_es(pred);full=fmt_full(pred)
print(f"\n{tg_en}")

with open("../outputs/cycle28_score_prediction_model.md",'w') as f:
    f.write(f"# Cycle 28: Score Prediction Model v1.0\n**Date:** {today}\n\n")
    f.write(f"## Market\nBTC ${btc:,.0f} ({btc24:.1f}%) | ETH ${eth:,.0f} | F&G {fng} | Stb ${stb/1e9:.1f}B\n\n")
    f.write(f"## Score: {comp} {phase}\nL1:{s1} L2:{s2} L3:{s3} L4:{s4}\nBTC {ba}% Alts {aa}% Stb {sa}%\n\n")
    f.write(f"## Full Dashboard\n```\n{full}\n```\n\n")
    f.write(f"## TG EN\n```\n{tg_en}\n```\n\n## TG ES\n```\n{tg_es}\n```\n")

def send_tg(msg):
    tok=os.environ.get('TELEGRAM_BOT_TOKEN','')
    cid=os.environ.get('TELEGRAM_CHAT_ID','')
    if not tok or not cid: return "NO_TOKEN"
    data=json.dumps({"chat_id":cid,"text":msg}).encode()
    req=urllib.request.Request(f"https://api.telegram.org/bot{tok}/sendMessage",
        data=data,headers={"Content-Type":"application/json"})
    try: return urllib.request.urlopen(req,timeout=10).status
    except Exception as e: return str(e)

r1=send_tg(tg_en);r2=send_tg(tg_es)
print(f"📱 TG EN:{r1} ES:{r2}")

with open("../data/current_market.json",'w') as f:
    json.dump({"date":today,"btc":btc,"eth":eth,"fng":fng,
        "stb_b":round(stb/1e9,1),"tvl_b":round(tvl_val/1e9,1),
        "score":comp,"phase":phase},f,indent=2)
with open("../data/current_score.json",'w') as f:
    json.dump({"date":today,"composite":comp,"phase":phase,
        "l1":s1,"l2":s2,"l3":s3,"l4":s4,
        "alloc":{"btc":ba,"alts":aa,"stables":sa},
        "pred":{"du":pred['du'],"dd":pred['dd'],"cv":pred['cv']}},f,indent=2)
print("✅ Cycle 28 complete!")
