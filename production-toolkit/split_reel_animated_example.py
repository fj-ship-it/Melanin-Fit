import sys, subprocess, numpy as np, cv2
_a=sys.argv; sys.argv=[_a[0]]
from build22 import fitf, banded, two, fin
sys.argv=_a
from PIL import Image, ImageDraw
from mfm import anton, raleway, logo, pill, W, H, WHITE, GOLD, DGOLD, END
from build21h import ctext, tag
O="/mnt/user-data/outputs/Oct15-18/MFM-Week-12/"
FPS=30
cap=cv2.VideoCapture("/home/claude/k21/w12_son.mp4"); vf=[]
while True:
    ok,f=cap.read()
    if not ok: break
    vf.append(cv2.cvtColor(f,cv2.COLOR_BGR2RGB))
big=120; hh=H//2; by0=hh+big; bh=H-by0
def fitarr(a,w,h,fx=0.5,fy=0.3):
    ih,iw=a.shape[:2]; r=max(w/iw,h/ih); a=cv2.resize(a,(int(iw*r+1),int(ih*r+1)),interpolation=cv2.INTER_AREA)
    x=int((a.shape[1]-w)*fx); y=int((a.shape[0]-h)*fy); return a[y:y+h,x:x+w]
base=np.array(Image.open(O+"01.png").convert("RGB"))
def slide1(t):
    i=min(int(t*24),len(vf)-1); fr=base.copy()
    fr[by0:by0+bh]=fitarr(vf[i],W,bh)
    im=Image.fromarray(fr).convert("RGBA"); d=ImageDraw.Draw(im)
    d.line([(0,by0),(W,by0)],fill=DGOLD,width=4); tag(d,"WEEK 12",30,H-80,True)
    return np.array(im.convert("RGB")).astype(np.float32)
def still(p): return np.array(Image.open(p).convert("RGB")).astype(np.float32)
def zoom(a,z):
    h,w=a.shape[:2]; cw,ch=int(w/z),int(h/z); x=(w-cw)//2; y=(h-ch)//2
    return cv2.resize(a[y:y+ch,x:x+cw],(w,h),interpolation=cv2.INTER_LINEAR)
endim=Image.open(END).convert("RGB").resize((W,H)); 
segs=[("v",None,5.0),("s",still(O+"02.png"),3.0),("s",still(O+"03.png"),3.0),("s",still(O+"04.png"),3.2),("s",np.array(endim).astype(np.float32),2.5)]
starts=[];t=0
for s in segs: starts.append(t); t+=s[2]
T=t; F=0.3
def fr_of(i,t):
    k,a,d=segs[i]; p=min(max((t-starts[i])/d,0),1)
    return slide1(t-starts[i]) if k=="v" else zoom(a,1.0+0.05*p)
p=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
 "-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-pix_fmt","yuv420p","-crf","18","-preset","medium","-c:a","aac","-movflags","+faststart",O+"MFM-Week-12-Reel.mp4"],stdin=subprocess.PIPE)
for n in range(int(T*FPS)):
    t=n/FPS; i=max(j for j in range(len(segs)) if starts[j]<=t); f=fr_of(i,t)
    if i+1<len(segs) and t>starts[i+1]-F: a=(t-(starts[i+1]-F))/F; f=f*(1-a)+fr_of(i+1,starts[i+1])*a
    p.stdin.write(np.clip(f,0,255).astype(np.uint8).tobytes())
p.stdin.close(); p.wait()
Image.fromarray(slide1(0).astype(np.uint8)).save(O+"cover.png")
Image.fromarray(slide1(2.5).astype(np.uint8)).save("/tmp/claude-0/w12mid.jpg")
print("ok",T)
