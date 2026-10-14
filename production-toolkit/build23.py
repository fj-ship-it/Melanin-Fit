import os, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw
from mfm import anton, raleway, LOGO, GOLD, WHITE, DGOLD, END
K="/home/claude/k17/"; OUT="/mnt/user-data/outputs/MFM-Crash-Diet-vs-Daily-Habits"; os.makedirs(OUT,exist_ok=True)
VW,VH,FPS=1080,1920,30; HW=VW//2-3
def fit(path,w,h,fx=0.5):
    im=cv2.cvtColor(cv2.imread(path),cv2.COLOR_BGR2RGB); ih,iw=im.shape[:2]
    r=max(w/iw,h/ih); im=cv2.resize(im,(int(iw*r+2),int(ih*r+2)),interpolation=cv2.INTER_AREA)
    x=int((im.shape[1]-w)*fx); y=(im.shape[0]-h)//2; return im[y:y+h,x:x+w]
def zoom(im,z):
    if z<=1.0001: return im
    h,w=im.shape[:2]; cw,ch=int(w/z),int(h/z); x=(w-cw)//2; y=(h-ch)//2
    return cv2.resize(im[y:y+ch,x:x+cw],(w,h),interpolation=cv2.INTER_LINEAR)
def ctext(d,t,cx,y,f,col,sw=4):
    tw=d.textlength(t,font=f); d.text((cx-tw/2,y),t,font=f,fill=col,stroke_width=sw,stroke_fill=(0,0,0))
beats=[("WEEK 1","cr_w1a","cr_w1b","Lettuce for dinner.","A real plate.",0.5,0.5),
       ("WEEK 3","cr_w3a","cr_w3b","Midnight cake.","Daily walk.",0.4,0.5),
       ("WEEK 8","cr_w8a","cr_w8b","Back on the couch.","Still showing up.",0.5,0.5),
       ("WEEK 52","cr_w52a","cr_w52b","Starting over. Again.","Dunking with his son.",0.45,0.55)]
def ov(i,wk,la,lb):
    o=Image.new("RGBA",(VW,VH),(0,0,0,0)); d=ImageDraw.Draw(o)
    for y in range(560): d.line([(0,y),(VW,y)],fill=(0,0,0,int(255*0.85*(1-y/560)**1.1)))
    for y in range(1100,VH): d.line([(0,y),(VW,y)],fill=(0,0,0,int(255*0.85*min(1,(y-1100)/300))))
    d.rectangle([VW//2-3,0,VW//2+3,VH],fill=DGOLD)
    o.alpha_composite(LOGO.resize((120,120),Image.LANCZOS),(40,150))
    if i==0:
        f=raleway(36,"ExtraBold"); t="SAME MAN. TWO PLANS."; tw=d.textlength(t,font=f)
        d.rounded_rectangle([(VW-tw)/2-28,175,(VW+tw)/2+28,237],radius=31,fill=GOLD); d.text(((VW-tw)/2,182),t,font=f,fill=(0,0,0))
    ctext(d,"CRASH DIET",VW*0.25,300,anton(84),WHITE,5); ctext(d,"DAILY HABITS",VW*0.75,300,anton(84),GOLD,5)
    f=anton(110); tw=d.textlength(wk,font=f)
    d.rounded_rectangle([(VW-tw)/2-36,1220,(VW+tw)/2+36,1370],radius=24,fill=(0,0,0),outline=DGOLD,width=4)
    d.text(((VW-tw)/2,1232),wk,font=f,fill=GOLD)
    f=raleway(40,"ExtraBold")
    for cx,t in ((VW*0.25,la),(VW*0.75,lb)):
        lines=[t] if d.textlength(t,font=f)<480 else t.rsplit(" ",1) if "." not in t[:-1] else [t[:t.index(".")+1],t[t.index(".")+2:]]
        for k,l in enumerate(lines): ctext(d,l,cx,1410+k*52,f,WHITE,3)
    if i==3:
        f1=anton(58); f2=raleway(36,"ExtraBold"); t1="COMMENT GAINS"; t2="  ·  FREE OVER-40 PLAN"
        tw=d.textlength(t1,font=f1)+d.textlength(t2,font=f2); x=(VW-tw)/2; y=1530
        d.rounded_rectangle([x-34,y,x+tw+34,y+90],radius=45,fill=GOLD)
        d.text((x,y+6),t1,font=f1,fill=(0,0,0)); d.text((x+d.textlength(t1,font=f1),y+24),t2,font=f2,fill=(0,0,0))
    a=np.array(o).astype(np.float32); return a[...,:3],a[...,3:]/255
segs=[]
for i,(wk,a,b,la,lb,fa,fb) in enumerate(beats):
    segs.append(("split",fit(K+a+".png",HW,VH,fa),fit(K+b+".png",HW,VH,fb),ov(i,wk,la,lb),3.6))
e=cv2.cvtColor(cv2.imread(END),cv2.COLOR_BGR2RGB); bg=(cv2.GaussianBlur(fit(END,VW,VH),(0,0),30)*0.45).astype(np.uint8)
ec=cv2.resize(e,(VW,int(e.shape[0]*VW/e.shape[1]))); y0=(VH-ec.shape[0])//2; bg[y0:y0+ec.shape[0]]=ec
segs.append(("still",bg,None,None,3.0))
FADE=0.3; starts=[]; t=0
for s in segs: starts.append(t); t+=s[4]
total=t
def frame_of(si,t):
    kind,A,B,o,dur=segs[si]; p=min(max((t-starts[si])/dur,0),1)
    if kind=="still": return A.astype(np.float32)
    fr=np.zeros((VH,VW,3),np.float32); z=1.0+0.09*p
    fr[:,:HW]=zoom(A,z); fr[:,VW-HW:]=zoom(B,z)
    oc,oa=o; return fr*(1-oa)+oc*oa
pr=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{VW}x{VH}","-r",str(FPS),"-i","-",
   "-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-pix_fmt","yuv420p","-crf","18","-preset","medium",
   "-c:a","aac","-movflags","+faststart",f"{OUT}/MFM-Crash-Diet-vs-Daily-Habits.mp4"],stdin=subprocess.PIPE)
for n in range(int(total*FPS)):
    t=n/FPS; si=max(i for i in range(len(segs)) if starts[i]<=t); fr=frame_of(si,t)
    if si+1<len(segs) and t>starts[si+1]-FADE:
        a=(t-(starts[si+1]-FADE))/FADE; fr=fr*(1-a)+frame_of(si+1,t)*a
    pr.stdin.write(np.clip(fr,0,255).astype(np.uint8).tobytes())
pr.stdin.close(); pr.wait()
Image.fromarray(np.clip(frame_of(0,0),0,255).astype(np.uint8)).save(f"{OUT}/cover.png")
for k,tt in enumerate([1.5,5.2,8.8,12.4]): Image.fromarray(np.clip(frame_of(k,tt),0,255).astype(np.uint8)).save(f"/tmp/claude-0/-home-claude/7908538f-f634-57b6-83b0-a3ec5bf84fbf/scratchpad/cr{k}.png")
print("total",total)
