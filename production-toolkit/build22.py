import os, shutil, sys
from PIL import Image, ImageDraw
from mfm import full, anton, raleway, logo, pill, wrap, W, H, WHITE, GOLD, DGOLD, END
from build21h import grad, ctext, tag, toppill
K="/home/claude/k17/"; K16="/home/claude/k16/"; O="/mnt/user-data/outputs/"
def fitf(path,w,h,fx=0.5,fy=0.5):
    im=Image.open(path).convert("RGB"); r=max(w/im.width,h/im.height)
    im=im.resize((int(im.width*r+1),int(im.height*r+1)),Image.LANCZOS)
    x=int((im.width-w)*fx); y=int((im.height-h)*fy); return im.crop((x,y,x+w,y+h))
def fullf(path,fx=0.5,fy=0.5):
    c=Image.new("RGBA",(W,H),(0,0,0,255)); c.paste(fitf(path,W,H,fx,fy),(0,0)); return c
def banded(a,b,bh,fa=(0.5,0.5),fb=(0.5,0.5)):
    hh=H//2; c=Image.new("RGBA",(W,H),(0,0,0,255))
    c.paste(fitf(a,W,hh-bh,*fa),(0,0)); c.paste(fitf(b,W,H-(hh+bh),*fb),(0,hh+bh))
    d=ImageDraw.Draw(c); d.rectangle([0,hh-bh,W,hh+bh],fill=(0,0,0))
    d.line([(0,hh-bh),(W,hh-bh)],fill=DGOLD,width=4); d.line([(0,hh+bh),(W,hh+bh)],fill=DGOLD,width=4)
    return c,d,hh
def two(d,parts,y,f):
    x=(W-sum(d.textlength(t,font=f) for t,_ in parts))/2
    for t,col in parts: d.text((x,y),t,font=f,fill=col); x+=d.textlength(t,font=f)
def letter(path,y):
    from PIL import ImageFilter
    im=Image.open(path).convert("RGB"); ih=int(im.height*W/im.width); im=im.resize((W,ih),Image.LANCZOS)
    bg=fitf(path,W,H).filter(ImageFilter.GaussianBlur(40)).point(lambda v:int(v*0.35))
    c=Image.new("RGBA",(W,H),(0,0,0,255)); c.paste(bg,(0,0)); c.paste(im,(0,y))
    d=ImageDraw.Draw(c); d.line([(0,y),(W,y)],fill=DGOLD,width=4); d.line([(0,y+ih),(W,y+ih)],fill=DGOLD,width=4); return c
def fin(c,i,n,out):
    logo(c,90,24,18); pill(c,f"{i}/{n}"); c.convert("RGB").save(f"{out}/{i:02d}.png")

def sunday():
    out=O+"MFM-Same-Sunday-Dinner"; os.makedirs(out,exist_ok=True); n=6
    pairs=[("sd_chick_a","sd_chick_b",None),("sd_tea_a","sd_tea_b","THE DRINK"),("sd_mac_a","sd_mac_b","THE MAC"),("sd_cob_a","sd_cob_b","AFTER DINNER")]
    for i,(a,b,lab) in enumerate(pairs):
        if i==0:
            c,d,hh=banded(K+a+".png",K+b+".png",120,(0.5,0.3),(0.5,0.3))
            ctext(d,"SAME SUNDAY DINNER.",hh-108,anton(92),WHITE,0); ctext(d,"DIFFERENT PLATE.",hh+4,anton(92),GOLD,0); ty=hh-200
        else:
            c,d,hh=banded(K+a+".png",K+b+".png",50,(0.5,0.3),(0.5,0.3))
            ctext(d,lab,hh-42,anton(66),GOLD,0); ty=hh-130
        tag(d,"COUCH DAD",30,ty,False); tag(d,"KING DAD",30,H-80,True); fin(c,i+1,n,out)
    c=letter(K+"sd_cob_b.png",470); d=ImageDraw.Draw(c)
    ctext(d,"KEEP THE TABLE.",170,anton(112),WHITE,5); ctext(d,"CHANGE THE PLATE.",300,anton(112),GOLD,5)
    ctext(d,"Follow for Part 2.",H-130,raleway(44,"ExtraBold"),WHITE,3); fin(c,5,n,out); shutil.copy(END,f"{out}/06.png")

def dnt():
    out=O+"MFM-Do-This-Not-That"; os.makedirs(out,exist_ok=True); n=7
    rows=[("dn1","Cut back on soda,","not every food you love."),("dn2","Stretch 10 minutes,","not a 2-hour routine."),
          ("dn3","Take the stairs,","not a mountain."),("dn4","Eat more vegetables,","not the whole garden."),
          ("dn5","Check your blood pressure,","not WebMD at 2 a.m.")]
    for i,(k,l1,l2) in enumerate(rows):
        bh=165 if i==0 else 100
        c,d,hh=banded(K+k+"a.png",K+k+"b.png",bh,(0.5,0.3),(0.5,0.3))
        y=hh-bh+18
        if i==0: two(d,[("DO THIS, ",WHITE),("NOT THAT.",GOLD)],y,anton(84)); y+=122
        f=raleway(46,"ExtraBold"); ctext(d,l1,y,f,WHITE,0); ctext(d,l2,y+60,f,GOLD,0)
        tag(d,"DO THIS",30,hh-bh-80,True); tag(d,"NOT THAT",30,H-80,False); fin(c,i+1,n,out)
    c=full(K+"dn_close.png"); grad(c,top=600,bottom=220); d=ImageDraw.Draw(c)
    ctext(d,"CONSISTENCY",150,anton(130),WHITE,5); ctext(d,"BEATS INTENSITY.",295,anton(112),GOLD,5)
    ctext(d,"Follow for Part 2.",H-130,raleway(44,"ExtraBold"),WHITE,3); fin(c,6,n,out); shutil.copy(END,f"{out}/07.png")

def week4():
    out=O+"MFM-Week-4"; os.makedirs(out,exist_ok=True); n=6
    pairs=[("d1_0","w4_son",None,(0.5,0.32)),("d1_1","w4_block","HOW FAR?",(0.5,0.5)),("d1_2","w4_walk","THE HARD PART",(0.5,0.62))]
    for i,(a,b,lab,fa) in enumerate(pairs):
        if i==0:
            c,d,hh=banded(K16+a+".png",K+b+".png",120,fa,(0.5,0.3))
            two(d,[("DAY 1 ",WHITE),("vs ",WHITE),("WEEK 4.",GOLD)],hh-104,anton(100))
            ctext(d,"SAME MAN. SAME STREET.",hh+28,raleway(44,"ExtraBold"),WHITE,0); ty=hh-200
        else:
            c,d,hh=banded(K16+a+".png",K+b+".png",50,fa,(0.5,0.3))
            ctext(d,lab,hh-42,anton(66),GOLD,0); ty=hh-130
        tag(d,"DAY 1",30,ty,False); tag(d,"WEEK 4",30,H-80,True); fin(c,i+1,n,out)
    c=letter(K+"w4_belt.png",400); d=ImageDraw.Draw(c)
    ctext(d,"WEEK 4.",150,anton(130),WHITE,5); ctext(d,"THE PANTS FIT DIFFERENT.",1060,anton(84),GOLD,5)
    ctext(d,"Down a size. Still walking.",1170,raleway(44,"ExtraBold"),WHITE,3)
    fin(c,4,n,out)
    c=full(K+"w4_close.png"); grad(c,top=620,bottom=220); d=ImageDraw.Draw(c)
    ctext(d,"NOBODY QUITS",130,anton(118),WHITE,5); ctext(d,"AT WEEK 12.",260,anton(118),WHITE,5)
    ctext(d,"THEY QUIT AT WEEK 4.",395,anton(96),GOLD,5)
    ctext(d,"Follow for Week 12.",H-130,raleway(44,"ExtraBold"),WHITE,3); fin(c,5,n,out); shutil.copy(END,f"{out}/06.png")
for fn in sys.argv[1:]: globals()[fn]()
print("ok")
