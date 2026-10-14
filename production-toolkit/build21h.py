import os, shutil, math, sys
from PIL import Image, ImageDraw, ImageFilter
from mfm import full, comic, anton, raleway, logo, pill, wrap, cover_fit, W, H, WHITE, GOLD, DGOLD, END
L="/home/claude/k16/"; O="/mnt/user-data/outputs/"
def grad(c,top=0,bottom=0,mt=0.85,mb=0.85):
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    for y in range(H):
        a=0
        if top and y<top: a=mt*(1-y/top)**0.8
        if bottom and y>H-bottom: a=max(a,mb*((y-(H-bottom))/bottom))
        d.line([(0,y),(W,y)],fill=(0,0,0,int(255*a)))
    c.alpha_composite(ov)
def label(d,t,cx,y,col=WHITE,size=50,maxw=470):
    f=comic(size); lines=wrap(d,t,f,maxw); lh=int(size*1.2)
    for i,l in enumerate(lines):
        tw=d.textlength(l,font=f); d.text((cx-tw/2,y+i*lh),l,font=f,fill=col,stroke_width=4,stroke_fill=(0,0,0))
    return y+len(lines)*lh
def arrow(d,p0,p2,bend=60):
    mx,my=(p0[0]+p2[0])/2,(p0[1]+p2[1])/2; dx,dy=p2[0]-p0[0],p2[1]-p0[1]; L_=math.hypot(dx,dy) or 1
    p1=(mx-dy/L_*bend,my+dx/L_*bend)
    pts=[((1-t)**2*p0[0]+2*(1-t)*t*p1[0]+t*t*p2[0],(1-t)**2*p0[1]+2*(1-t)*t*p1[1]+t*t*p2[1]) for t in [i/30 for i in range(31)]]
    d.line(pts,fill=(0,0,0),width=10,joint="curve"); d.line(pts,fill=WHITE,width=5,joint="curve")
    ax,ay=pts[-1]; bx,by=pts[-4]; a=math.atan2(ay-by,ax-bx)
    d.polygon([(ax,ay),(ax-26*math.cos(a-0.45),ay-26*math.sin(a-0.45)),(ax-26*math.cos(a+0.45),ay-26*math.sin(a+0.45))],fill=WHITE,outline=(0,0,0))
def ctext(d,t,y,f,col,stroke=4,cx=W/2):
    tw=d.textlength(t,font=f); d.text((cx-tw/2,y),t,font=f,fill=col,stroke_width=stroke,stroke_fill=(0,0,0)); return tw
def toppill(d,t):
    f=raleway(28,"ExtraBold"); tw=d.textlength(t,font=f)
    d.rounded_rectangle([(W-tw)/2-24,34,(W+tw)/2+24,84],radius=25,fill=GOLD); d.text(((W-tw)/2,42),t,font=f,fill=(0,0,0))
def tag(d,t,x,y,gold):
    f=raleway(30,"ExtraBold"); tw=d.textlength(t,font=f)
    d.rounded_rectangle([x,y,x+tw+40,y+52],radius=26,fill=GOLD if gold else (255,255,255)); d.text((x+20,y+8),t,font=f,fill=(0,0,0))
