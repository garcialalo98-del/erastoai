import csv, json, math

data = []
with open('data/historical_quarterly_2020_2026.csv', 'r') as f:
    for row in csv.DictReader(f):
        data.append({
            'q': row['Quarter'], 'btc': float(row['BTC_Price']),
            'eth': float(row['ETH_Price']), 'score': float(row['Composite']),
            'phase': row['Phase'], 'events': row['Key_Events']
        })

def alloc(score):
    if score >= 4.5: return (0.50, 0.40, 0.10, 'Max Offense')
    if score >= 3.5: return (0.45, 0.30, 0.25, 'Lean Aggressive')
    if score >= 2.5: return (0.35, 0.10, 0.55, 'Cautious')
    if score >= 1.5: return (0.20, 0.00, 0.80, 'Defensive')
    return (0.05, 0.00, 0.95, 'Preservation')

K = 10000.0
# Erasto
ev = K; prev = alloc(2.50); elog = []
for i, d in enumerate(data):
    br = (d['btc'] - data[i-1]['btc']) / data[i-1]['btc'] if i > 0 else 0
    er = (d['eth'] - data[i-1]['eth']) / data[i-1]['eth'] if i > 0 else 0
    ev = ev * prev[0] * (1+br) + ev * prev[1] * (1+er) + ev * prev[2]
    elog.append({'q':d['q'],'score_used':data[i-1]['score'] if i>0 else 'N/A',
        'phase':prev[3],'ba':prev[0],'aa':prev[1],'sa':prev[2],
        'br':br,'er':er,'val':round(ev,2)})
    prev = alloc(d['score'])
    ev = elog[-1]['val']

# BTC B&H
bv = K; blog = []
for i, d in enumerate(data):
    br = (d['btc'] - data[i-1]['btc']) / data[i-1]['btc'] if i > 0 else 0
    bv *= (1+br)
    blog.append({'q':d['q'],'val':round(bv,2)})

# 60/40
sv = K; slog = []
for i, d in enumerate(data):
    br = (d['btc'] - data[i-1]['btc']) / data[i-1]['btc'] if i > 0 else 0
    sv = sv*0.60*(1+br) + sv*0.40
    slog.append({'q':d['q'],'val':round(sv,2)})

def metrics(vals, name):
    tr = vals[-1]/vals[0] - 1
    yrs = (len(vals)-1)/4.0
    cagr = (vals[-1]/vals[0])**(1/yrs)-1 if yrs>0 else 0
    pk = vals[0]; mdd = 0; mdq = ''
    for i,v in enumerate(vals):
        if v > pk: pk = v
        dd = (v-pk)/pk
        if dd < mdd: mdd = dd
    qr = [(vals[i]-vals[i-1])/vals[i-1] for i in range(1,len(vals))]
    avg = sum(qr)/len(qr)
    vol = math.sqrt(sum((r-avg)**2 for r in qr)/len(qr))
    wins = sum(1 for r in qr if r>0)
    sharpe = ((avg-0.01)/vol)*2 if vol>0 else 0
    return {'name':name,'end':round(vals[-1],2),'tr':round(tr*100,1),
        'cagr':round(cagr*100,1),'mdd':round(mdd*100,1),
        'vol':round(vol*2*100,1),'wr':round(wins/len(qr)*100,1),
        'sharpe':round(sharpe,2)}

em = metrics([e['val'] for e in elog], 'Erasto')
bm = metrics([b['val'] for b in blog], 'BTC B&H')
sm = metrics([s['val'] for s in slog], '60/40')

print("=== QUARTER LOG ===")
for i in range(len(elog)):
    e = elog[i]
    print(f"{e['q']}|{e['score_used']}|{e['phase']}|{e['ba']:.0%}/{e['aa']:.0%}/{e['sa']:.0%}|BTC:{e['br']:+.1%}|ETH:{e['er']:+.1%}|E:${e['val']:,.0f}|B:${blog[i]['val']:,.0f}|S:${slog[i]['val']:,.0f}")

print("\n=== METRICS ===")
for m in [em, bm, sm]:
    print(json.dumps(m))
