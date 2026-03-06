"""Erasto Market Regime Classifier v1.0
4 regimes: ACCUMULATION, MARKUP, DISTRIBUTION, MARKDOWN
6 signals: ATH dist, 30d momentum, F&G, stablecoin flow, TVL, ETF"""

def classify_regime(btc,ath,b30a,b30l,b30h,fng,stb,stb_p,tvl,tvl_p,etf="neutral"):
    S={}
    ad=100-(btc/ath)*100
    S['ath']={'v':ad,'l':'DEEP DISCOUNT' if ad>40 else('DISCOUNT' if ad>20 else('MODERATE' if ad>10 else 'NEAR ATH')),'r':'ACCUMULATION' if ad>20 else('MARKUP' if ad>10 else 'DISTRIBUTION')}
    m=((btc/b30a)-1)*100
    if m>15: S['mom']={'v':m,'l':'STRONG UP','r':'MARKUP'}
    elif m>5: S['mom']={'v':m,'l':'UP','r':'MARKUP'}
    elif m>-5: S['mom']={'v':m,'l':'SIDEWAYS','r':'ACCUMULATION'}
    elif m>-15: S['mom']={'v':m,'l':'DOWN','r':'MARKDOWN'}
    else: S['mom']={'v':m,'l':'CRASH','r':'MARKDOWN'}
    if fng<=20: S['fng']={'v':fng,'l':'EXTREME FEAR','r':'ACCUMULATION'}
    elif fng<=40: S['fng']={'v':fng,'l':'FEAR','r':'ACCUMULATION'}
    elif fng<=60: S['fng']={'v':fng,'l':'NEUTRAL','r':'MARKUP'}
    else: S['fng']={'v':fng,'l':'GREED','r':'DISTRIBUTION'}
    sd=((stb-stb_p)/stb_p)*100 if stb_p else 0
    if sd>2: S['stb']={'v':sd,'l':'STRONG INFLOW','r':'ACCUMULATION'}
    elif sd>0.5: S['stb']={'v':sd,'l':'INFLOW','r':'ACCUMULATION'}
    elif sd>-0.5: S['stb']={'v':sd,'l':'STABLE','r':'MARKUP'}
    else: S['stb']={'v':sd,'l':'OUTFLOW','r':'MARKDOWN'}
    td=((tvl/tvl_p)-1)*100 if tvl_p else 0
    if td>5: S['tvl']={'v':td,'l':'GROWTH','r':'MARKUP'}
    elif td>-3: S['tvl']={'v':td,'l':'STABLE','r':'ACCUMULATION'}
    else: S['tvl']={'v':td,'l':'DECLINE','r':'MARKDOWN'}
    em={'strong_inflow':('BUYING','MARKUP'),'inflow':('INFLOW','ACCUMULATION'),'neutral':('MIXED','ACCUMULATION'),'outflow':('SELLING','DISTRIBUTION'),'strong_outflow':('FLEEING','MARKDOWN')}
    el,er=em.get(etf,('MIXED','ACCUMULATION'))
    S['etf']={'v':etf,'l':el,'r':er}
    rc={}
    for s in S.values(): rc[s['r']]=rc.get(s['r'],0)+1
    regime=max(rc,key=rc.get)
    conf=rc[regime]/len(S)*100
    vol=((b30h-b30l)/b30l)*100
    G={'ACCUMULATION':{'s':'DCA into BTC. Keep dry powder. Patience wins.','a':'BTC 30-40% | Alts 5-10% | Stables 50-65%','e':'🟢'},
       'MARKUP':{'s':'Increase exposure. Rotate stables into quality alts.','a':'BTC 40-55% | Alts 15-25% | Stables 20-40%','e':'🔵'},
       'DISTRIBUTION':{'s':'Take profits. Reduce alts. Move to stables.','a':'BTC 20-30% | Alts 0-10% | Stables 60-80%','e':'🟡'},
       'MARKDOWN':{'s':'Capital preservation. Stay defensive. Wait.','a':'BTC 10-20% | Alts 0% | Stables 80-90%','e':'🔴'}}
    return {'regime':regime,'conf':conf,'signals':S,'counts':rc,'guide':G[regime],'all_guide':G,'vol':vol,'ath_d':ad,'mom':m}
