#!/usr/bin/env python3
"""Erasto Weekly Digest v1.0"""
import urllib.request,json,time,os
from datetime import datetime,timezone
CG="https://api.coingecko.com/api/v3"
HDR={"User-Agent":"Erasto/3.0","Accept":"application/json"}
ATH=126080;PSB=271.8e9;D=4
AL=[(4.5,5.01,50,40,10,"MAX OFFENSE"),(3.5,4.5,45,30,25,"LEAN AGGRESSIVE"),(2.5,3.5,35,10,55,"CAUTIOUS"),(1.5,2.5,20,0,80,"DEFENSIVE"),(1.0,1.5,5,0,95,"PRESERVATION")]
def F(url,r=2):
 for i in range(r+1):
  try:q=urllib.request.Request(url,headers=HDR);return json.loads(urllib.request.urlopen(q,timeout=15).read())
  except:
   if i<r:time.sleep(D*(i+2))
 return None
def score(d):
 dp=(d.get("stb",0)-PSB)/PSB*100;l1=4.0 if dp>10 else 3.5 if dp>5 else 3.0 if dp>0 else 2.0 if dp>-5 else 1.0
 fg=d.get("fng",25);l2=4.0 if fg>=75 else 3.5 if fg>=50 else 2.5 if fg>=25 else 2.0 if fg>=10 else 1.0
 ar=d.get("btc",70000)/ATH;s1=4.5 if ar>0.9 else 3.5 if ar>0.75 else 2.5 if ar>0.6 else 1.5 if ar>0.4 else 1.0
 m=d.get("b30",0);s2=4.0 if m>15 else 3.0 if m>5 else 2.5 if m>0 else 2.0 if m>-10 else 1.5;l3=round((s1+s2)/2,2)
 sec=d.get("sec",[]);pos=sum(1 for s in sec if s["d30"]>0)/len(sec) if sec else 0
 l4=3.5 if pos>0.7 else 3.0 if pos>0.5 else 2.5 if pos>0.3 else 2.0 if pos>0.1 else 1.5
 return {"l1":l1,"l2":l2,"l3":l3,"l4":l4,"c":round((l1+l2+l3+l4)/4,2)}
def alloc(c):
 for lo,hi,b,a,s,p in AL:
  if lo<=c<hi:return {"b":b,"a":a,"s":s,"p":p}
 return {"b":5,"a":0,"s":95,"p":"PRESERVATION"}
def regime(d):
 btc=d.get("btc",0);fng=d.get("fng",50);stb=d.get("stb",0);tvl=d.get("tvl",0);tv30=d.get("tv30",tvl)
 ad=100-(btc/ATH)*100;m30=d.get("b30",0);sd=((stb-PSB)/PSB)*100;td=((tvl/tv30)-1)*100 if tv30 else 0
 sg=[]
 sg.append("A" if ad>20 else("U" if ad>10 else "D"))
 sg.append("U" if m30>5 else("A" if m30>-5 else "M"))
 sg.append("A" if fng<=25 else("U" if fng<=60 else "D"))
 sg.append("A" if sd>2 else("U" if sd>0 else "M"))
 sg.append("U" if td>5 else("A" if td>-3 else "M"))
 rc={}
 for s in sg:rc[s]=rc.get(s,0)+1
 nm={"A":"ACCUMULATION","U":"MARKUP","D":"DISTRIBUTION","M":"MARKDOWN"}
 rg=max(rc,key=rc.get)
 return {"r":nm[rg],"cf":rc[rg]/len(sg)*100,"ad":ad,"m":m30}
def bar(v,n=5):f=max(0,min(n,int(round(v))));return chr(9608)*f+chr(9617)*(n-f)
def send(text):
 tk=os.environ.get("TELEGRAM_BOT_TOKEN","");ci=os.environ.get("TELEGRAM_CHAT_ID","")
 if not tk or not ci:return None
 url=f"https://api.telegram.org/bot{tk}/sendMessage"
 pl=json.dumps({"chat_id":ci,"text":text}).encode()
 req=urllib.request.Request(url,data=pl,headers={"Content-Type":"application/json"})
 try:return json.loads(urllib.request.urlopen(req,timeout=15).read()).get("ok")
 except:return None
