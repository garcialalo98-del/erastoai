#!/usr/bin/env python3
"""Erasto Multi-Timeframe Scoring Engine v1.0"""
import csv, os

ATH = 126080
PHASES = [(4.5,5.01,"MAX OFFENSE"),(3.5,4.5,"LEAN AGGRESSIVE"),
          (2.5,3.5,"CAUTIOUS"),(1.5,2.5,"DEFENSIVE"),(1.0,1.5,"PRESERVATION")]
ALLOC = {"MAX OFFENSE":(50,40,10),"LEAN AGGRESSIVE":(45,30,25),
         "CAUTIOUS":(35,10,55),"DEFENSIVE":(20,0,80),"PRESERVATION":(5,0,95)}

def phase_for(s):
    for lo,hi,n in PHASES:
        if lo<=s<hi: return n
    return "PRESERVATION"

def composite(l1,l2,l3,l4): return round((l1+l2+l3+l4)/4,2)
def bar(s,w=20): f=int((s/5.0)*w); return "█"*f+"░"*(w-f)

def l1_daily(stb,btc24h):
    s=4.0 if stb>300 else(3.5 if stb>250 else 3.0)
    f=2.5 if btc24h>2 else(2.0 if btc24h>0 else(1.5 if btc24h>-3 else 1.0))
    return round((s+f)/2,2)
def l1_weekly(stb,delta):
    s=4.0 if stb>300 else(3.5 if stb>250 else 3.0)
    d=4.5 if delta>30 else(4.0 if delta>15 else(3.0 if delta>5 else 2.0))
    return round((s+d)/2,2)
def l1_monthly(stb,tvl90):
    s=4.0 if stb>300 else(3.5 if stb>250 else 3.0)
    t=4.0 if tvl90>20 else(3.0 if tvl90>0 else(2.0 if tvl90>-15 else 1.5))
    return round((s+t)/2,2)

def l2(fng):
    if fng>=75: return 4.5
    if fng>=55: return 3.5
    if fng>=35: return 3.0
    if fng>=20: return 2.5
    return 2.0

def l3_daily(d1,d7,pos7):
    a=3.0 if d1>3 else(2.5 if d1>0 else(2.0 if d1>-3 else 1.5))
    b=3.0 if d7>5 else(2.5 if d7>0 else(2.0 if d7>-5 else 1.5))
    c=3.0 if pos7>60 else(2.5 if pos7>40 else(2.0 if pos7>20 else 1.5))
    return round((a+b+c)/3,2)
def l3_weekly(m30,ath_r):
    a=4.0 if m30>20 else(3.0 if m30>10 else(2.5 if m30>0 else(2.0 if m30>-10 else 1.5)))
    b=4.5 if ath_r>.9 else(3.5 if ath_r>.8 else(2.5 if ath_r>.7 else(2.0 if ath_r>.6 else 1.5)))
    return round((a+b)/2,2)
def l3_monthly(m90,pos90):
    a=4.0 if m90>30 else(3.0 if m90>10 else(2.5 if m90>0 else(2.0 if m90>-15 else 1.5)))
    b=4.0 if pos90>70 else(3.0 if pos90>50 else(2.0 if pos90>25 else 1.5))
    return round((a+b)/2,2)

def l4_daily(sec_pct):
    if sec_pct>80: return 4.0
    if sec_pct>50: return 3.0
    if sec_pct>20: return 2.0
    return 1.0
def l4_weekly(tvl30,sec_pct):
    a=4.0 if tvl30>15 else(3.0 if tvl30>5 else(2.0 if tvl30>-5 else 1.5))
    b=4.0 if sec_pct>60 else(3.0 if sec_pct>30 else 2.0)
    return round((a+b)/2,2)
def l4_monthly(tvl90):
    if tvl90>20: return 4.0
    if tvl90>5: return 3.0
    if tvl90>-10: return 2.0
    return 1.5

def divergences(d,w,m):
    sigs=[]
    if d<w: sigs.append(f"⚡ TACTICAL DIP: Daily {d:.2f} < Weekly {w:.2f}")
    elif d>w+0.3: sigs.append(f"⚡ SPIKE: Daily {d:.2f} > Weekly {w:.2f}")
    if w>m+0.3: sigs.append(f"🔄 RECOVERY: Weekly {w:.2f} > Monthly {m:.2f}")
    if d<2.0 and w>=2.5: sigs.append("💰 ENTRY ZONE: Daily fear + Weekly improving")
    return sigs
