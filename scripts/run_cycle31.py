#!/usr/bin/env python3
"""Cycle 31: Market Regime Classifier + Dashboard"""
import json,os,sys
from datetime import datetime,timezone
from urllib.request import urlopen,Request
def fetch(u):
    return json.loads(urlopen(Request(u,headers={"User-Agent":"Erasto/3.1"}),timeout=15).read())
def tg(tk,ch,txt,la="EN"):
    d=json.dumps({"chat_id":ch,"text":txt,"parse_mode":"Markdown"}).encode()
    print(f"  TG {la}: {urlopen(Request(f'https://api.telegram.org/bot{tk}/sendMessage',data=d,headers={'Content-Type':'application/json'}),timeout=10).getcode()}")
print("ERASTO CYCLE 31\n")
p=fetch("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true")
btc,eth,sol=p['bitcoin']['usd'],p['ethereum']['usd'],p['solana']['usd']
b24=p['bitcoin'].get('usd_24h_change',0)
fng=int(fetch("https://api.alternative.me/fng/?limit=1")['data'][0]['value'])
sd=fetch("https://stablecoins.llama.fi/stablecoins?includePrices=true")
stb=sum(float(s.get('circulating',{}).get('peggedUSD',0) or 0) for s in sd.get('peggedAssets',[]))/1e9
ta=fetch("https://api.llama.fi/v2/historicalChainTvl")
tvl=ta[-1]['tvl']/1e9; tvlp=ta[-8]['tvl']/1e9
bh=fetch("https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30")
bp=[x[1] for x in bh['prices']]; b30a,b30h,b30l=bp[0],max(bp),min(bp)
print(f"BTC ${btc:,.0f} ({b24:+.1f}%) ETH ${eth:,.0f} SOL ${sol:.0f} F&G {fng} Stb ${stb:.1f}B TVL ${tvl:.1f}B")
# Score
sp=270.0; ath=122000.0
l1=min(5.0,2.0+(stb-sp)/15); l2=2.0 if fng<=20 else(2.5 if fng<=40 else 3.0)
mom=((btc/b30a)-1)*100; l3=min(5.0,max(1.0,1.0+(btc/ath)*2.5+(0.5 if mom>0 else 0)))
l4=2.0+(0.5 if stb>300 else 0)+(0.25 if tvl>90 else 0)
c=(l1*0.30+l2*0.25+l3*0.25+l4*0.20)
ph="AGGRESSIVE" if c>=3.5 else("CAUTIOUS" if c>=2.5 else "DEFENSIVE")
# Regime
sys.path.insert(0,os.path.dirname(__file__))
from market_regime import classify_regime
R=classify_regime(btc,ath,b30a,b30l,b30h,fng,stb,sp,tvl,tvlp,"outflow")
S=R['signals']; e=R['guide']['e']; ad=R['ath_d']
now=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
print(f"Score {c:.2f} {ph} | Regime {R['regime']} ({R['conf']:.0f}%)")
en=f"""{e} *ERASTO Cycle 31*
{now}

*REGIME: {R['regime']}* ({R['conf']:.0f}%)
{R['guide']['s']}

📊 *{c:.2f}/5.0 → {ph}*
L1={l1:.1f} L2={l2:.1f} L3={l3:.1f} L4={l4:.1f}
💰 *{R['guide']['a']}*

📈 BTC ${btc:,.0f} ({b24:+.1f}%) -{ad:.0f}% ATH
ETH ${eth:,.0f} | SOL ${sol:.0f}
F&G {fng} | Stb ${stb:.1f}B | TVL ${tvl:.1f}B

🔬 *Signals*
ATH: {S['ath']['l']}→{S['ath']['r']}
Mom: {S['mom']['l']}→{S['mom']['r']}
F&G: {S['fng']['l']}→{S['fng']['r']}
Stb: {S['stb']['l']}→{S['stb']['r']}
TVL: {S['tvl']['l']}→{S['tvl']['r']}
ETF: {S['etf']['l']}→{S['etf']['r']}

⚡ ${stb:.0f}B powder keg + Extreme Fear = accumulation zone. DCA, don't FOMO.
_Research only_"""
es=f"""{e} *ERASTO Ciclo 31*\n{now}\n*RÉGIMEN: {R['regime']}* ({R['conf']:.0f}%)\n📊 *{c:.2f}/5.0 → {ph}*\n💰 {R['guide']['a']}\nBTC ${btc:,.0f} | F&G {fng} | Stb ${stb:.1f}B\n⚡ Zona de acumulación. Paciencia.\n_Solo investigación_"""
tk,ch=os.environ.get("TELEGRAM_BOT_TOKEN",""),os.environ.get("TELEGRAM_CHAT_ID","")
if tk and ch: tg(tk,ch,en,"EN"); tg(tk,ch,es,"ES")
# Save
dd=os.path.join(os.path.dirname(__file__),'..','data'); os.makedirs(dd,exist_ok=True)
td=datetime.now(timezone.utc).strftime("%Y-%m-%d")
with open(os.path.join(dd,'score_history.csv'),'a') as f:
    f.write(f"{td},{int(btc)},{int(eth)},{fng},{stb:.1f},{tvl:.1f},{l1:.2f},{l2:.1f},{l3:.2f},{l4:.2f},{c:.2f},{ph},30,5,65,{c:.2f},{c:.2f}\n")
with open(os.path.join(dd,'current_market.json'),'w') as f:
    json.dump({'date':td,'btc':btc,'eth':eth,'fng':fng,'stb_b':round(stb,1),'tvl_b':round(tvl,1),'score':round(c,2),'phase':ph,'regime':R['regime'],'regime_conf':round(R['conf']),'ath_dist':round(ad,1),'mom_30d':round(R['mom'],1)},f,indent=2)
print("DONE")
