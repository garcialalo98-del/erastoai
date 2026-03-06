#!/usr/bin/env python3
"""Cycle 29: Custom Watchlist + Full Dashboard Update"""
import sys, os, json, time
sys.path.insert(0, "scripts")
from custom_watchlist import *
from erasto_pipeline import get_data, score, alloc, fmt, send_tg as send_tg2

print("=" * 50)
print("🔄 CYCLE 29: Custom Watchlist + Dashboard")
print("=" * 50)

# --- Part 1: Run full pipeline for dashboard ---
print("\n📡 Phase 1: Dashboard data...")
d = get_data()
l1,l2,l3,l4,comp,dp = score(d)
al = alloc(comp)
b,a,s,ph = al
print(f"✅ Score: {comp}/5.0 → {ph}")
print(f"   L1={l1} L2={l2} L3={l3} L4={l4}")
print(f"   Alloc: {b}% BTC | {a}% Alts | {s}% Stables")

# --- Part 2: Run custom watchlist ---
print("\n📋 Phase 2: Custom Watchlist...")
time.sleep(6)
cfg = load_config()
ids = get_all_ids(cfg)
print(f"📡 Fetching {len(ids)} tokens...")
md = fetch_market(ids)
print(f"✅ Got {len(md)} tokens")
sec = sector_stats(cfg, md)
alerts = gen_alerts(cfg, md)

# Score all tokens
scored = sorted([(k,v,opp_score(v)) for k,v in md.items()],
    key=lambda x:x[2], reverse=True)

# Save snapshot
snap = {"ts": d.get("ts",""), "tokens": {k:{**v,"opp":opp_score(v)} for k,v in md.items()},
    "sectors": sec, "alerts": alerts,
    "dashboard": {"score":comp,"phase":ph,"l1":l1,"l2":l2,"l3":l3,"l4":l4,
        "btc":d.get("btc",0),"eth":d.get("eth",0),"fng":d.get("fng",0),
        "stb_b":round(d.get("stb",0)/1e9,2)}}
os.makedirs("data", exist_ok=True)
json.dump(snap, open("data/watchlist_snapshot.json","w"), indent=2)

# Format messages
wl_en = fmt_tg(cfg, md, sec, alerts, "en")
wl_es = fmt_tg(cfg, md, sec, alerts, "es")
dash_en = fmt(d,l1,l2,l3,l4,comp,al,dp,"en")
dash_es = fmt(d,l1,l2,l3,l4,comp,al,dp,"es")

print("\n" + dash_en)
print("\n" + wl_en)

# --- Part 3: Send via Telegram ---
mode = sys.argv[1] if len(sys.argv) > 1 else "--dry-run"
if mode == "--send":
    print("\n📬 Sending to Telegram...")
    m1 = send_tg2(dash_en); time.sleep(1)
    m2 = send_tg2(dash_es); time.sleep(1)
    m3 = send_tg(wl_en); time.sleep(1)
    m4 = send_tg(wl_es)
    print(f"📬 Dashboard: EN={m1} ES={m2}")
    print(f"📬 Watchlist: EN={m3} ES={m4}")

# Print summary
print(f"\n{'='*50}")
print(f"✅ CYCLE 29 COMPLETE")
print(f"   Score: {comp}/5.0 → {ph}")
print(f"   Tokens tracked: {len(md)}")
print(f"   Alerts: {len(alerts)}")
print(f"   Top opp: {scored[0][1]['sym']} (score {scored[0][2]})")
