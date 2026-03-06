#!/usr/bin/env python3
"""Erasto Score Prediction Engine v1.0
Predicts phase transitions: what triggers change, when, how likely."""

ATH = 126080
PHASES = [(4.5,5.01,"MAX OFFENSE"),(3.5,4.5,"LEAN AGGRESSIVE"),
          (2.5,3.5,"CAUTIOUS"),(1.5,2.5,"DEFENSIVE"),(1.0,1.5,"PRESERVATION")]
ALLOC = {"MAX OFFENSE":(50,40,10),"LEAN AGGRESSIVE":(45,30,25),
         "CAUTIOUS":(35,10,55),"DEFENSIVE":(20,0,80),"PRESERVATION":(5,0,95)}
LN = {0:"L1 Liquidity",1:"L2 Macro",2:"L3 Cycle",3:"L4 Sectors"}

def phase_for(s):
    for lo,hi,n in PHASES:
        if lo<=s<hi: return n,lo,hi
    return "PRESERVATION",1.0,1.5

def predict(history):
    if len(history)<2: return None
    lvs = [[float(r.get(f'l{i+1}',0)) for r in history] for i in range(4)]
    comps = [float(r.get('composite',0)) for r in history]
    cur = comps[-1]; cl = [l[-1] for l in lvs]
    phase,lo,hi = phase_for(cur)
    cv = comps[-1]-comps[-2]
    av = (comps[-1]-comps[0])/max(len(comps)-1,1)
    du = round(hi-cur,2); dd = round(cur-lo,2)
    up_p = dn_p = None
    for a,b,n in PHASES:
        if a==hi: up_p=n
        if b==lo: dn_p=n
    scenarios = []
    for i in range(4):
        needed = du*4; tgt = min(cl[i]+needed,5.0)
        chg = round(tgt-cl[i],2)
        feas = "HIGH" if chg<1.0 else ("MED" if chg<2.0 else "LOW")
        vel = lvs[i][-1]-lvs[i][-2] if len(lvs[i])>=2 else 0
        scenarios.append({"level":LN[i],"cur":cl[i],"tgt":round(tgt,2),
                          "chg":chg,"feas":feas,"vel":round(vel,2)})
    return {"score":cur,"phase":phase,"alloc":ALLOC.get(phase,(5,0,95)),
            "levels":cl,"du":du,"dd":dd,"up":up_p,"dn":dn_p,
            "cv":round(cv,2),"av":round(av,2),"scenarios":scenarios}

def triggers(cl,btc,fng,stb,tvl):
    t = []
    t.append(("L1",cl[0],[f"Stables>${stb/1e9+20:.0f}B (now ${stb/1e9:.0f}B)",
        "ETF inflows >$500M/day sustained","Fed signals rate cuts"],
        ["Stablecoin redemptions >5%","ETF outflows >5 days"]))
    t.append(("L2",cl[1],[f"F&G rises >35 (now {fng})","Fed cuts rates",
        "Trade deal / tariff rollback"],
        [f"F&G drops <10 (now {fng})","Recession confirmed"]))
    t.append(("L3",cl[2],[f"BTC>${ATH*0.8:,.0f} (80% ATH)",
        "30d momentum >+10%","Exchange outflow accumulation"],
        [f"BTC<${btc*0.85:,.0f} (-15%)","30d momentum <-15%"]))
    t.append(("L4",cl[3],[f"TVL>${tvl/1e9*1.3:.0f}B (now ${tvl/1e9:.0f}B)",
        "AI/RWA sector rotation","New narrative catalyst"],
        [f"TVL<${tvl/1e9*0.8:.0f}B","Major exploit >$100M"]))
    return t
