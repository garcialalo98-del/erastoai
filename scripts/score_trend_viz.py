#!/usr/bin/env python3
"""Erasto Score Trend Visualization Engine v1.0"""
import csv, os

PHASES = [(4.5,5.01,"MAX OFFENSE","🟢"),(3.5,4.5,"LEAN AGGR","🔵"),
          (2.5,3.5,"CAUTIOUS","🟡"),(1.5,2.5,"DEFENSIVE","🟠"),(1.0,1.5,"PRESERVATION","🔴")]
SPARK = "▁▂▃▄▅▆▇█"

def phase_for(s):
    for lo,hi,n,e in PHASES:
        if lo<=s<hi: return n,e
    return "PRESERVATION","🔴"

def sparkline(vals, w=20):
    if not vals: return ""
    mn,mx = min(vals),max(vals)
    r = mx-mn if mx!=mn else 1
    return "".join(SPARK[min(int((v-mn)/r*7),7)] for v in vals[-w:])

def bar(v, mx=5.0, w=20):
    f = int((v/mx)*w)
    return "█"*f + "░"*(w-f)

def trend_arrow(vals):
    if len(vals)<2: return "➡️"
    d = vals[-1]-vals[-2]
    return "⬆️" if d>0.2 else ("↗️" if d>0 else ("↘️" if d>-0.2 else "⬇️"))

def load_history(path):
    if not os.path.exists(path): return []
    with open(path) as f: return list(csv.DictReader(f))

def gen_timeline(rows):
    lines = ["📊 SCORE TIMELINE","─"*44]
    for r in rows:
        s = float(r.get('composite',0)); _,e = phase_for(s)
        lines.append(f"{r['date']} │ {e} {s:.2f} │{bar(s,5,15)}│ ${float(r.get('btc',0)):,.0f}")
    lines.append("─"*44)
    return "\n".join(lines)

def gen_levels(rows):
    if not rows: return "No data"
    lvs = {k:[] for k in ['l1','l2','l3','l4']}
    for r in rows:
        for k in lvs:
            try: lvs[k].append(float(r.get(k,0)))
            except: lvs[k].append(0)
    labels = {'l1':'💧 Liquidity','l2':'🌍 Macro','l3':'🔄 Cycle','l4':'📈 Sectors'}
    lines = ["📈 LEVEL TRENDS","─"*40]
    for k,lb in labels.items():
        v = lvs[k]; lines.append(f"{lb}: {sparkline(v,15)} {v[-1]:.1f} {trend_arrow(v)}")
    return "\n".join(lines)

def gen_momentum(rows):
    if len(rows)<2: return "📡 Need more data"
    scores = [float(r.get('composite',0)) for r in rows]
    cur,prev = scores[-1],scores[-2]; d = cur-prev
    sig = f"{'✅' if d>0 else '⚠️'} Score: {prev:.2f}→{cur:.2f} ({d:+.2f})"
    bounds = [1.5,2.5,3.5,4.5]
    near = min(bounds, key=lambda b: abs(cur-b)); dist = near-cur
    if abs(dist)<0.2:
        sig += f"\n🔔 {abs(dist):.2f}pts to {'upgrade' if dist>0 else 'downgrade'}!"
    return sig

def gen_phase_stats(rows):
    c = {}
    for r in rows: p=r.get('phase','?'); c[p]=c.get(p,0)+1
    t = sum(c.values())
    lines = ["⏱️ TIME IN PHASE"]
    for _,_,n,e in PHASES:
        if c.get(n,0)>0: lines.append(f"{e} {n}: {c[n]}d ({c[n]/t*100:.0f}%)")
    return "\n".join(lines)
