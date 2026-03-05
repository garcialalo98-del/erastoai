#!/usr/bin/env python3
"""
Erasto Data Collector v1.0
Fetches live market data from free APIs: CoinGecko, Fear&Greed, DeFiLlama
Rate limit: 10-30 calls/min free tier. Use delays between calls.
Usage: python3 data_collector.py [--live|--test]
"""
import urllib.request, json, time, sys
from datetime import datetime, timezone

BASE = "https://api.coingecko.com/api/v3"
HDR = {"User-Agent": "Erasto/1.0", "Accept": "application/json"}
DELAY = 6

def fetch(url, retries=2):
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=HDR)
            return json.loads(urllib.request.urlopen(req, timeout=15).read())
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < retries:
                time.sleep(DELAY * (i + 2))
            else: raise
    return None

def prices():
    return fetch(f"{BASE}/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true&include_market_cap=true")

def fear_greed():
    d = fetch("https://api.alternative.me/fng/?limit=1")
    return int(d["data"][0]["value"]) if d and "data" in d else None

def global_data():
    d = fetch(f"{BASE}/global")
    if d and "data" in d:
        return {"market_cap": d["data"]["total_market_cap"].get("usd",0),
                "btc_dom": d["data"].get("market_cap_percentage",{}).get("btc",0)}
    return None

def defi_tvl():
    d = fetch("https://api.llama.fi/v2/historicalChainTvl")
    return d[-1].get("tvl",0) if d else None

def snapshot():
    s = {"ts": datetime.now(timezone.utc).isoformat()}
    p = prices(); time.sleep(DELAY)
    if p:
        s["btc"] = p.get("bitcoin",{}).get("usd")
        s["eth"] = p.get("ethereum",{}).get("usd")
    s["fng"] = fear_greed(); time.sleep(DELAY)
    g = global_data()
    if g: s.update(g)
    time.sleep(DELAY)
    s["tvl"] = defi_tvl()
    return s

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--live"
    if mode == "--live":
        s = snapshot()
        print(json.dumps(s, indent=2))
        with open("data/current_market.json","w") as f: json.dump(s,f,indent=2)
        print("Saved to data/current_market.json")
    elif mode == "--test":
        p = prices()
        print(f"BTC: ${p['bitcoin']['usd']:,.0f}  ETH: ${p['ethereum']['usd']:,.0f}")
    else:
        print("Usage: python3 data_collector.py [--live|--test]")
