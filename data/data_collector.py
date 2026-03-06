#!/usr/bin/env python3
"""
Erasto AI — Automated Data Collector v1.0
Fetches all market data from free APIs, saves to current_market.json.
Cron-ready. Zero API keys required.
Sources: CoinGecko, Alternative.me (F&G), DeFiLlama
Usage:  python3 data_collector.py [--verbose] [--output DIR]
"""
import json, sys, os, time, logging, argparse
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

VERSION = "1.0.0"
RATE_DELAY = 2.5
MAX_RETRIES = 3
TIMEOUT = 15

ENDPOINTS = {
    "prices": "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true",
    "global": "https://api.coingecko.com/api/v3/global",
    "stables": "https://api.coingecko.com/api/v3/simple/price?ids=tether,usd-coin,dai&vs_currencies=usd&include_market_cap=true",
    "fng": "https://api.alternative.me/fng/?limit=7",
    "tvl": "https://api.llama.fi/v2/historicalChainTvl",
}

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("erasto")

def fetch(url, label="", retries=MAX_RETRIES):
    for attempt in range(1, retries + 1):
        try:
            req = Request(url, headers={"User-Agent": "ErastoAI/1.0"})
            with urlopen(req, timeout=TIMEOUT) as r:
                data = json.loads(r.read().decode())
                log.info(f"OK {label}")
                return data
        except HTTPError as e:
            if e.code == 429: time.sleep(5 * attempt)
            log.warning(f"HTTP {e.code} {label} attempt {attempt}")
            time.sleep(3)
        except (URLError, TimeoutError) as e:
            log.error(f"ERR {label}: {e}")
            time.sleep(3)
    log.error(f"FAILED {label}")
    return None

def sg(d, *keys, default=None):
    c = d
    for k in keys:
        if isinstance(c, dict) and k in c: c = c[k]
        else: return default
    return c

def get_prices():
    d = fetch(ENDPOINTS["prices"], "Prices")
    if not d: return None
    r = {}
    for cid, p in [("bitcoin","btc"),("ethereum","eth"),("solana","sol")]:
        c = d.get(cid, {})
        r[f"{p}_price"] = round(c.get("usd",0),2)
        r[f"{p}_24h_change"] = round(c.get("usd_24h_change",0),2)
        r[f"{p}_market_cap"] = round(c.get("usd_market_cap",0))
        r[f"{p}_24h_vol"] = round(c.get("usd_24h_vol",0))
    return r

def get_global():
    d = fetch(ENDPOINTS["global"], "Global")
    if not d: return None
    g = d.get("data",{})
    mp = g.get("market_cap_percentage",{})
    return {"btc_dominance":round(mp.get("btc",0),1),
        "eth_dominance":round(mp.get("eth",0),1),
        "total_mcap_usd":round(sg(g,"total_market_cap","usd",default=0)),
        "total_vol_24h":round(sg(g,"total_volume","usd",default=0)),
        "mcap_chg_24h":round(g.get("market_cap_change_percentage_24h_usd",0),2)}

def get_stables():
    d = fetch(ENDPOINTS["stables"], "Stablecoins")
    if not d: return None
    usdt = sg(d,"tether","usd_market_cap",default=0)
    usdc = sg(d,"usd-coin","usd_market_cap",default=0)
    dai = sg(d,"dai","usd_market_cap",default=0)
    t = usdt+usdc+dai
    return {"usdt_mcap":round(usdt),"usdc_mcap":round(usdc),
            "dai_mcap":round(dai),"total":round(t),"total_b":round(t/1e9,1)}

def get_fng():
    d = fetch(ENDPOINTS["fng"], "F&G")
    if not d or "data" not in d: return None
    e = d["data"]; cur = e[0] if e else {}
    v = [int(x.get("value",0)) for x in e[:7]]
    return {"value":int(cur.get("value",0)),
            "label":cur.get("value_classification","?"),
            "avg_7d":round(sum(v)/len(v),1) if v else 0,"hist_7d":v}

def get_tvl():
    d = fetch(ENDPOINTS["tvl"], "TVL")
    if not d or len(d)<31: return None
    n,w,m = d[-1].get("tvl",0),d[-8].get("tvl",0),d[-31].get("tvl",0)
    return {"tvl":round(n),"tvl_b":round(n/1e9,2),
            "chg_7d":round((n-w)/w*100,2) if w else 0,
            "chg_30d":round((n-m)/m*100,2) if m else 0}

def collect_all(out_dir=None):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    dt = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log.info(f"Collector v{VERSION} — {dt}")
    res = {"meta":{"version":VERSION,"ts":ts,"date":dt,"status":"ok","errors":[]}}
    
    for name, fn, delay in [("prices",get_prices,RATE_DELAY),("global",get_global,RATE_DELAY),
                             ("stablecoins",get_stables,0),("fng",get_fng,0),("defi",get_tvl,0)]:
        data = fn()
        if data: res[name] = data
        else: res["meta"]["errors"].append(name)
        if delay: time.sleep(delay)
    
    p,g,s,f,d = [res.get(k,{}) for k in ["prices","global","stablecoins","fng","defi"]]
    res["summary"] = {"btc":p.get("btc_price",0),"eth":p.get("eth_price",0),
        "sol":p.get("sol_price",0),"btc_chg":p.get("btc_24h_change",0),
        "dom":g.get("btc_dominance",0),"mcap_t":round(g.get("total_mcap_usd",0)/1e12,2),
        "fng":f.get("value",0),"fng_lbl":f.get("label","?"),"fng_7d":f.get("avg_7d",0),
        "stables_b":s.get("total_b",0),"tvl_b":d.get("tvl_b",0),"tvl_7d":d.get("chg_7d",0)}
    
    errs = res["meta"]["errors"]
    if errs: res["meta"]["status"] = "partial" if len(errs)<3 else "degraded"
    
    if not out_dir: out_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(out_dir,"current_market.json"),"w") as f: json.dump(res,f,indent=2)
    snap = os.path.join(out_dir,"snapshots"); os.makedirs(snap,exist_ok=True)
    with open(os.path.join(snap,f"market_{dt}.json"),"w") as f: json.dump(res,f,indent=2)
    log.info(f"Saved. Errors: {errs if errs else 'none'}")
    return res

if __name__ == "__main__":
    pa = argparse.ArgumentParser(); pa.add_argument("--verbose","-v",action="store_true")
    pa.add_argument("--output","-o",type=str,default=None); args = pa.parse_args()
    if args.verbose: logging.getLogger().setLevel(logging.DEBUG)
    r = collect_all(out_dir=args.output); s = r.get("summary",{})
    print(f"\n{'='*50}\n  ERASTO COLLECTOR — {r['meta']['date']}\n{'='*50}")
    print(f"  BTC: ${s['btc']:,.0f} ({s['btc_chg']:+.1f}%)")
    print(f"  ETH: ${s['eth']:,.0f} | SOL: ${s['sol']:,.0f}")
    print(f"  F&G: {s['fng']} ({s['fng_lbl']}) | 7d: {s['fng_7d']}")
    print(f"  Dom: {s['dom']}% | MCap: ${s['mcap_t']}T")
    print(f"  TVL: ${s['tvl_b']}B ({s['tvl_7d']:+.1f}% 7d)")
    print(f"  Stables: ${s['stables_b']}B")
    print(f"  Status: {r['meta']['status'].upper()}\n{'='*50}")
