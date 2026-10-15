import subprocess, numpy as np
from PIL import Image
import fuel_chart as B
W,H=1080,1350; FPS=30; OUT=B.OUT
segs=[]
for i,s in enumerate(B.S): segs.append(("c",i,3.6 if i else 4.0))
segs.append(("e",None,2.6))
endim=np.asarray(Image.open(B.END).convert("RGB").resize((W,H))).astype(np.float32)
p=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
 "-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-pix_fmt","yuv420p","-crf","19","-preset","medium","-c:a","aac","-movflags","+faststart",OUT+"MFM-The-Fuel-Chart-Reel.mp4"],stdin=subprocess.PIPE)
first=True
for k,i,d in segs:
    n=int(d*FPS)
    for f in range(n):
        t=f/FPS
        if k=="e": fr=endim
        else:
            rise=1.6
            # first chart: start with columns already 35% up so frame 1 isn't empty
            pr=min(1.0,(0.35 if first else 0)+t/rise) if t<rise else 1.0
            fr=np.asarray(B.chart(B.S[i],i+1,B.N,prog=pr if pr<1 else 1.0,save=False)).astype(np.float32)
        p.stdin.write(fr.astype(np.uint8).tobytes())
    first=False
p.stdin.close(); p.wait()
B.chart(B.S[0],1,B.N,save=False).save(OUT+"cover.png"); print("reel ok")
