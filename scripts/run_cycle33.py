#!/usr/bin/env python3
"""Cycle 33: Weekly Digest Engine execution"""
import sys,os,json,csv
sys.path.insert(0,os.path.join(os.path.dirname(__file__),"..","scripts"))
from weekly_digest import score,alloc,regime,bar,send
from datetime import datetime,timezone
# Pre-fetched market data (avoid API timeouts)
d={"btc":68248,"eth":1978.76,"sol":84.61,"fng":18,"fngl":"Extreme Fear","fng7":13.9,
   "bdom":63.0,"stb":311.7e9,"tvl":95.8e9,"tv7":95.3e9,"tv30":103.5e9,"b7":-0.2,"b30":-6.0,
   "sec":[{"s":"HYPE","p":31.01,"d7":1.0,"d30":5.0,"ath":-35},
    {"s":"SOL","p":84.61,"d7":-5.1,"d30":-12.0,"ath":-68},
    {"s":"DOGE","p":0.11,"d7":-3.0,"d30":-15.0,"ath":-85},
    {"s":"SUI","p":0.90,"d7":-6.0,"d30":-18.0,"ath":-82},
    {"s":"LINK","p":8.76,"d7":-5.1,"d30":-10.0,"ath":-83},
    {"s":"AAVE","p":111.58,"d7":-5.8,"d30":-8.0,"ath":-80},
    {"s":"RNDR","p":1.36,"d7":-2.9,"d30":-20.0,"ath":-86},
    {"s":"ARB","p":0.10,"d7":-3.7,"d30":-22.0,"ath":-96},
    {"s":"UNI","p":3.83,"d7":-3.9,"d30":-12.0,"ath":-91},
    {"s":"ONDO","p":0.255,"d7":-3.9,"d30":-15.0,"ath":-85},
    {"s":"TIA","p":0.33,"d7":-3.8,"d30":-25.0,"ath":-97},
    {"s":"FET","p":0.146,"d7":-5.2,"d30":-18.0,"ath":-94}]}
sc=score(d);al=alloc(sc["c"]);rg=regime(d)
print(f"Score: {sc['c']} {al['p']} | Regime: {rg['r']} ({rg['cf']:.0f}%)")
print(f"Alloc: {al['b']}% BTC | {al['a']}% Alts | {al['s']}% Stables")
