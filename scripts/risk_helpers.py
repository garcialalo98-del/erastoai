import csv, json, math
from datetime import datetime

def load_data(path='data/historical_quarterly_2020_2026.csv'):
    data = []
    with open(path, 'r') as f:
        for row in csv.DictReader(f):
            data.append({'q': row['Quarter'], 'btc': float(row['BTC_Price']),
                'eth': float(row['ETH_Price']), 'score': float(row['Composite']),
                'phase': row['Phase']})
    return data

def alloc(score):
    if score >= 4.5: return (0.50, 0.40, 0.10, 'Max Offense')
    if score >= 3.5: return (0.45, 0.30, 0.25, 'Lean Aggressive')
    if score >= 2.5: return (0.35, 0.10, 0.55, 'Cautious')
    if score >= 1.5: return (0.20, 0.00, 0.80, 'Defensive')
    return (0.05, 0.00, 0.95, 'Preservation')

def simulate(data, start=10000):
    prev = alloc(2.50); val = start; log = []
    for i, d in enumerate(data):
        br = (d['btc']-data[i-1]['btc'])/data[i-1]['btc'] if i>0 else 0
        er = (d['eth']-data[i-1]['eth'])/data[i-1]['eth'] if i>0 else 0
        bp = val*prev[0]*br; ap = val*prev[1]*er; val += bp+ap
        pr = (bp+ap)/(val-bp-ap) if i>0 else 0
        log.append({'q':d['q'],'val':round(val,2),'ret':round(pr,4),'phase':prev[3],'score':d['score']})
        prev = alloc(d['score'])
    return log

def btc_bnh(data, start=10000):
    val = start; log = []
    for i, d in enumerate(data):
        r = (d['btc']-data[i-1]['btc'])/data[i-1]['btc'] if i>0 else 0
        val *= (1+r); log.append({'q':d['q'],'val':round(val,2),'ret':round(r,4)})
    return log
