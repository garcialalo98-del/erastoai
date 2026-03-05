#!/usr/bin/env python3
"""Erasto Risk Metrics Engine v1.0"""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from risk_helpers import load_data, simulate, btc_bnh
import json, math
from datetime import datetime

def metrics(log, name, rf_q=0.01):
    vals=[e['val'] for e in log]; rets=[e['ret'] for e in log[1:]]
    n=len(rets); yrs=n/4.0
    tr=vals[-1]/vals[0]-1; cagr=(vals[-1]/vals[0])**(1/yrs)-1
    pk=vals[0]; mdd=0; mddq=''
    for i,v in enumerate(vals):
        if v>pk: pk=v
        dd=(v-pk)/pk
        if dd<mdd: mdd=dd; mddq=log[i]['q']
    avg=sum(rets)/n; var=sum((r-avg)**2 for r in rets)/n
    qv=math.sqrt(var); av=qv*2
    neg=[r for r in rets if r<0]
    dv=math.sqrt(sum(r**2 for r in neg)/n)*2 if neg else 0.001
    wins=sum(1 for r in rets if r>0)
    gains=[r for r in rets if r>0]; losses=[r for r in rets if r<0]
    ag=sum(gains)/len(gains) if gains else 0
    al=sum(losses)/len(losses) if losses else 0
    pf=abs(ag/al) if al else 99
    sh=((avg-rf_q)/qv)*2 if qv>0 else 0
    so=((avg-rf_q)*4)/dv if dv>0 else 0
    ca=cagr/abs(mdd) if mdd else 0
    bq=max(rets); wq=min(rets)
    return {'name':name,'end':round(vals[-1]),'tr':round(tr*100,1),
        'cagr':round(cagr*100,1),'mdd':round(mdd*100,1),'mddq':mddq,
        'vol':round(av*100,1),'dvol':round(dv*100,1),
        'wr':round(wins/n*100,1),'sharpe':round(sh,2),
        'sortino':round(so,2),'calmar':round(ca,2),
        'ret_dd':round(tr/abs(mdd),1) if mdd else 0,
        'best':f"{log[rets.index(bq)+1]['q']} ({bq:+.1%})",
        'worst':f"{log[rets.index(wq)+1]['q']} ({wq:+.1%})",
        'ag':round(ag*100,1),'al':round(al*100,1),'pf':round(pf,2),
        'nq':n,'wq':wins,'lq':n-wins}

def rolling(log, w=8):
    res=[]
    for i in range(w, len(log)):
        sub=log[i-w:i+1]; vs=[e['val'] for e in sub]; rs=[e['ret'] for e in sub[1:]]
        pk=vs[0]; md=0
        for v in vs:
            if v>pk: pk=v
            dd=(v-pk)/pk
            if dd<md: md=dd
        avg=sum(rs)/len(rs); var=sum((r-avg)**2 for r in rs)/len(rs)
        vol=math.sqrt(var)*2
        sh=((avg-0.01)/math.sqrt(var))*2 if var>0 else 0
        res.append({'q':log[i]['q'],'ret':round((vs[-1]/vs[0]-1)*100,1),
            'mdd':round(md*100,1),'vol':round(vol*100,1),'sh':round(sh,2)})
    return res

if __name__=='__main__':
    os.chdir(os.path.join(os.path.dirname(__file__),'..'))
    data=load_data()
    el=simulate(data); bl=btc_bnh(data)
    em=metrics(el,'Erasto'); bm=metrics(bl,'BTC B&H')
    rl=rolling(el)
    for m in [em,bm]:
        print(f"\n--- {m['name']} ---")
        for k,v in m.items():
            if k!='name': print(f"  {k}: {v}")
    print("\n--- Rolling 2Y (Erasto) ---")
    for r in rl: print(f"  {r['q']}: Ret={r['ret']:+.1f}% MDD={r['mdd']:.1f}% Vol={r['vol']:.1f}% Sh={r['sh']:.2f}")
    out={'ts':datetime.utcnow().isoformat(),'erasto':em,'btc':bm,'rolling':rl}
    with open('data/risk_metrics.json','w') as f: json.dump(out,f,indent=2)
    print("\n✅ Saved data/risk_metrics.json")
