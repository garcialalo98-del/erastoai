#!/usr/bin/env python3
"""Erasto Custom Watchlist v1.0 — Configurable token tracking + opportunity scoring"""
import urllib.request, json, time, os, sys
from datetime import datetime, timezone

HDR = {"User-Agent": "Erasto/3.0", "Accept": "application/json"}
CG = "https://api.coingecko.com/api/v3"

def fetch(url, retries=2):
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=HDR)
            return json.loads(urllib.request.urlopen(req, timeout=15).read())
        except:
            if i < retries: time.sleep(5 * (i + 1))
    return None

def load_config(path="data/watchlist_config.json"):
    with open(path) as f: return json.load(f)

def get_all_ids(cfg):
    ids = []
    for s in cfg["sectors"].values(): ids.extend(s["tokens"])
    return list(set(ids))

def fetch_market(ids):
    url = f"{CG}/coins/markets?vs_currency=usd&ids={','.join(ids)}&order=market_cap_desc&sparkline=false&price_change_percentage=7d,30d"
    data = fetch(url)
    if not data or not isinstance(data, list): return {}
    r = {}
    for c in data:
        r[c["id"]] = {"sym": c.get("symbol","?").upper(),
            "price": c.get("current_price",0), "mcap": c.get("market_cap",0),
            "d1": round(c.get("price_change_percentage_24h",0) or 0, 2),
            "d7": round(c.get("price_change_percentage_7d_in_currency",0) or 0, 2),
            "d30": round(c.get("price_change_percentage_30d_in_currency",0) or 0, 2),
            "ath": c.get("ath",0),
            "ath_pct": round(c.get("ath_change_percentage",0) or 0, 2)}
    return r

def opp_score(t):
    s = 0
    ad = abs(t.get("ath_pct", 0))
    s += 40 if ad > 90 else 35 if ad > 80 else 28 if ad > 70 else 20 if ad > 50 else 10
    d7 = t.get("d7", 0)
    s += 30 if d7>15 else 25 if d7>10 else 20 if d7>5 else 15 if d7>0 else 8 if d7>-5 else 0
    d30 = t.get("d30", 0)
    s += 30 if d30<-25 else 22 if d30<-15 else 15 if d30<-10 else 10 if d30<0 else 20 if d30>10 else 5
    return min(s, 100)

def gen_alerts(cfg, md):
    ac = cfg.get("alerts", {})
    ath_t, hot_t, cold_t = ac.get("ath_discount_buy",-80), ac.get("momentum_7d_hot",10), ac.get("momentum_30d_cold",-25)
    alerts = []
    for tid, t in md.items():
        if t["ath_pct"] < ath_t:
            alerts.append(f"🟢 {t['sym']} at {t['ath_pct']:.0f}% from ATH — deep value")
        if t["d7"] > hot_t:
            alerts.append(f"🔥 {t['sym']} +{t['d7']:.1f}% 7d — hot momentum")
        if t["d30"] < cold_t:
            alerts.append(f"🧊 {t['sym']} {t['d30']:.1f}% 30d — deeply oversold")
    return alerts

def sector_stats(cfg, md):
    sec = {}
    for name, info in cfg["sectors"].items():
        toks = [md[t] for t in info["tokens"] if t in md]
        if not toks: continue
        sec[name] = {"avg_7d": round(sum(t["d7"] for t in toks)/len(toks),2),
            "avg_30d": round(sum(t["d30"] for t in toks)/len(toks),2),
            "avg_ath": round(sum(t["ath_pct"] for t in toks)/len(toks),2),
            "n": len(toks), "thesis": info["thesis"]}
    return sec

def fmt_tg(cfg, md, sec, alerts, lang="en"):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    n = len(md); p7 = sum(1 for t in md.values() if t["d7"]>0)
    title = "📋 ERASTO WATCHLIST" if lang=="en" else "📋 LISTA SEGUIMIENTO"
    L = [f"{title} | {ts}", f"{n} tokens | {p7}/{n} green 7d", ""]
    scored = sorted([(tid,t,opp_score(t)) for tid,t in md.items()], key=lambda x:x[2], reverse=True)
    L.append("🎯 TOP OPPORTUNITIES" if lang=="en" else "🎯 OPORTUNIDADES")
    for tid,t,sc in scored[:6]:
        bar = "█"*(sc//20) + "░"*(5-sc//20)
        ic = "🟢" if t["d7"]>0 else "🔴"
        p = t["price"]
        ps = f"${p:,.2f}" if p>=1 else f"${p:.6f}"
        L.append(f"{ic} {t['sym']:6s} {ps:>12s} 7d:{t['d7']:+5.1f}% {bar} {sc}")
    L.append("")
    L.append("📊 SECTORS" if lang=="en" else "📊 SECTORES")
    for nm,s in sorted(sec.items(), key=lambda x:x[1]["avg_7d"], reverse=True):
        ic = "🟢" if s["avg_7d"]>0 else "🔴" if s["avg_7d"]<-5 else "🟡"
        L.append(f"{ic} {nm:10s} 7d:{s['avg_7d']:+5.1f}% 30d:{s['avg_30d']:+6.1f}%")
    L.append("")
    if alerts:
        L.append("⚡ ALERTS" if lang=="en" else "⚡ ALERTAS")
        for a in alerts[:6]: L.append(a)
        L.append("")
    L.append("🤖 Erasto v3 | Not financial advice" if lang=="en" else "🤖 Erasto v3 | No es consejo financiero")
    return "\n".join(L)

def send_tg(text):
    tk,ci = os.environ.get("TELEGRAM_BOT_TOKEN",""), os.environ.get("TELEGRAM_CHAT_ID","")
    if not tk or not ci: return None
    url = f"https://api.telegram.org/bot{tk}/sendMessage"
    pl = json.dumps({"chat_id":ci,"text":text[:4096]}).encode()
    req = urllib.request.Request(url,data=pl,headers={"Content-Type":"application/json"})
    try:
        r = json.loads(urllib.request.urlopen(req,timeout=15).read())
        return r["result"]["message_id"] if r.get("ok") else None
    except: return None

if __name__=="__main__":
    mode = sys.argv[1] if len(sys.argv)>1 else "--dry-run"
    print("📋 Erasto Custom Watchlist v1.0")
    cfg = load_config()
    ids = get_all_ids(cfg)
    print(f"📡 Fetching {len(ids)} tokens...")
    md = fetch_market(ids)
    print(f"✅ Got {len(md)} tokens")
    sec = sector_stats(cfg, md)
    alerts = gen_alerts(cfg, md)
    snap = {"ts": datetime.now(timezone.utc).isoformat(),
        "tokens": {k:{**v,"opp":opp_score(v)} for k,v in md.items()},
        "sectors": sec, "alerts": alerts}
    os.makedirs("data", exist_ok=True)
    json.dump(snap, open("data/watchlist_snapshot.json","w"), indent=2)
    en = fmt_tg(cfg, md, sec, alerts, "en")
    es = fmt_tg(cfg, md, sec, alerts, "es")
    print(en)
    if mode == "--send":
        m1 = send_tg(en); m2 = send_tg(es)
        print(f"📬 TG: EN={m1} ES={m2}")
