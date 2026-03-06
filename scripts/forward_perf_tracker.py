#!/usr/bin/env python3
"""Erasto Forward Performance Tracker v1.0"""
import csv, json, os
from datetime import datetime, timezone

ALLOC = {
    "MAX OFFENSE": (50, 40, 10),
    "LEAN AGGRESSIVE": (45, 30, 25),
    "CAUTIOUS": (35, 10, 55),
    "DEFENSIVE": (20, 0, 80),
    "PRESERVATION": (5, 0, 95)
}
PERF_CSV = "data/performance_history.csv"
FIELDS = [
    "date", "cycle", "phase", "score",
    "btc_price", "eth_price", "fng",
    "btc_alloc", "alts_alloc", "stb_alloc",
    "portfolio_value", "btc_hodl_value", "dca_value",
    "port_ret", "hodl_ret", "dca_ret",
    "alpha_btc", "alpha_dca", "max_dd", "win_streak"
]

def load(path=PERF_CSV):
    rows = []
    if os.path.exists(path):
        with open(path) as f:
            for r in csv.DictReader(f):
                rows.append(r)
    return rows

def save(rows, path=PERF_CSV):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

def port_value(entries, bp_now, ep_now, cap=10000):
    if not entries:
        return cap, 0.0
    val = cap
    prev_ph = None
    bu = eu = st = 0
    for e in entries:
        ph = e["phase"]
        bp = float(e["btc_price"])
        ep = float(e["eth_price"])
        if ph != prev_ph or prev_ph is None:
            if prev_ph:
                val = bu * bp + eu * ep + st
            a = ALLOC.get(ph, (20, 0, 80))
            bu = (val * a[0] / 100) / bp if bp else 0
            eu = (val * a[1] / 100) / ep if ep else 0
            st = val * a[2] / 100
            prev_ph = ph
    cur = bu * bp_now + eu * ep_now + st
    return round(cur, 2), round((cur / cap - 1) * 100, 2)

def hodl_value(entries, bp_now, cap=10000):
    if not entries:
        return cap, 0.0
    bp = float(entries[0]["btc_price"])
    cur = (cap / bp) * bp_now if bp else cap
    return round(cur, 2), round((cur / cap - 1) * 100, 2)

def dca_value(entries, bp_now, cap=10000):
    if not entries:
        return cap, 0.0
    per = cap / len(entries)
    units = sum(
        per / float(e["btc_price"])
        for e in entries if float(e["btc_price"]) > 0
    )
    cur = units * bp_now
    return round(cur, 2), round((cur / cap - 1) * 100, 2)

def max_dd(history):
    if not history:
        return 0.0
    vals = [float(h.get("portfolio_value", 10000)) for h in history]
    pk = vals[0]
    md = 0.0
    for v in vals:
        if v > pk:
            pk = v
        dd = (pk - v) / pk * 100 if pk else 0
        if dd > md:
            md = dd
    return round(md, 2)

def win_streak(history):
    s = 0
    for h in reversed(history):
        if float(h.get("alpha_btc", 0)) >= 0:
            s += 1
        else:
            break
    return s

def add_entry(cy, phase, score, bp, ep, fng, bp_now, ep_now, cap=10000):
    hist = load()
    a = ALLOC.get(phase, (20, 0, 80))
    e = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "cycle": str(cy), "phase": phase, "score": str(score),
        "btc_price": str(bp), "eth_price": str(ep), "fng": str(fng),
        "btc_alloc": str(a[0]), "alts_alloc": str(a[1]),
        "stb_alloc": str(a[2])
    }
    all_e = hist + [e]
    pv, pr = port_value(all_e, bp_now, ep_now, cap)
    hv, hr = hodl_value(all_e, bp_now, cap)
    dv, dr = dca_value(all_e, bp_now, cap)
    ab = round(pr - hr, 2)
    ad = round(pr - dr, 2)
    e.update({
        "portfolio_value": str(pv), "btc_hodl_value": str(hv),
        "dca_value": str(dv), "port_ret": str(pr),
        "hodl_ret": str(hr), "dca_ret": str(dr),
        "alpha_btc": str(ab), "alpha_dca": str(ad)
    })
    all_e[-1] = e
    e["max_dd"] = str(max_dd(all_e))
    e["win_streak"] = str(win_streak(all_e))
    save(all_e)
    return e, all_e
