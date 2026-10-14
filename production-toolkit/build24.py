import sys, os, shutil
_a=sys.argv; sys.argv=[_a[0]]
from build22 import *
sys.argv=_a
from PIL import Image, ImageDraw
from mfm import anton, raleway, W, H, WHITE, GOLD, DGOLD, END, full, cover_fit
from build21h import grad, ctext, tag
K="/home/claude/k19/"; O="/mnt/user-data/outputs/"
def strip(c,kw,offer,y=H-250):
    d=ImageDraw.Draw(c); f1=anton(54); f2=raleway(34,"ExtraBold"); t1=f"COMMENT {kw}"; t2=f"  ·  {offer}"
    tw=d.textlength(t1,font=f1)+d.textlength(t2,font=f2); x=(W-tw)/2
    d.rounded_rectangle([x-34,y,x+tw+34,y+84],radius=42,fill=GOLD)
    d.text((x,y+6),t1,font=f1,fill=(0,0,0)); d.text((x+d.textlength(t1,font=f1),y+22),t2,font=f2,fill=(0,0,0))
def close(img,l1,l2,kw,offer,follow,i,n,out,s1=118,s2=104):
    c=full(K+img); grad(c,top=620,bottom=360); d=ImageDraw.Draw(c)
    ctext(d,l1,140,anton(s1),WHITE,5); ctext(d,l2,140+s1+16,anton(s2),GOLD,5)
    strip(c,kw,offer); d=ImageDraw.Draw(c); ctext(d,follow,H-130,raleway(44,"ExtraBold"),WHITE,3); fin(c,i,n,out)
def lclose(img,l1,l2,kw,offer,follow,i,n,out,s1=104,s2=88):
    c=letter(K+img,400); d=ImageDraw.Draw(c)
    ctext(d,l1,120,anton(s1),WHITE,5); ctext(d,l2,120+s1+14,anton(s2),GOLD,5)
    strip(c,kw,offer,H-280); d=ImageDraw.Draw(c); ctext(d,follow,H-150,raleway(44,"ExtraBold"),WHITE,3); fin(c,i,n,out)
def splits(out,rows,title,tags,n,big=120):
    for i,(a,b,lab) in enumerate(rows):
        if i==0:
            c,d,hh=banded(K+a+".png",K+b+".png",big,(0.5,0.3),(0.5,0.3))
            two(d,title,hh-big+10,anton(92)); ctext(d,lab,hh+big-62,raleway(42,"ExtraBold"),WHITE,0); ty=hh-big-80
        else:
            c,d,hh=banded(K+a+".png",K+b+".png",50,(0.5,0.3),(0.5,0.3)); ctext(d,lab,hh-42,anton(66),GOLD,0); ty=hh-130
        tag(d,tags[0],30,ty,False); tag(d,tags[1],30,H-80,True); fin(c,i+1,n,out)
def ysiw4():
    out=O+"MFM-Your-Son-Is-Watching-Pt4"; os.makedirs(out,exist_ok=True); n=6
    splits(out,[("y4_bar_a","y4_bar_b","AT THE BARBERSHOP"),("y4_doc_a","y4_doc_b","AT THE DOCTOR'S OFFICE"),
                ("y4_sat_a","y4_sat_b","SATURDAY MORNING"),("y4_str_a","y4_str_b","WHEN HE'S STRESSED")],
           [("YOUR SON ",WHITE),("IS WATCHING.",GOLD)],("COUCH DAD","KING DAD"),n)
    close("y4_close.png","HE LEARNS HOW TO BE A MAN","BY WATCHING YOU.","GAINS","FREE OVER-40 TRAINING PLAN","Follow for Part 5.",5,n,out,84,96)
    shutil.copy(END,f"{out}/06.png")
def tboost():
    out=O+"MFM-Same-Goal-Different-Plan"; os.makedirs(out,exist_ok=True); n=5
    splits(out,[("tb1a","tb1b","MORE ENERGY. MORE DRIVE."),("tb2a","tb2b","THE BELLY"),("tb3a","tb3b","THE CHECKUP")],
           [("SAME GOAL. ",WHITE),("DIFFERENT PLAN.",GOLD)],("COUCH DAD","KING DAD"),n)
    lclose("tb_close2.png","THE BOOSTER","WAS NEVER IN A BOTTLE.","SUPPS","FREE SUPPLEMENT CHECKLIST","Follow for Part 2.",4,n,out,110,84)
    shutil.copy(END,f"{out}/05.png")
def hours():
    out=O+"MFM-Both-Have-24-Hours"; os.makedirs(out,exist_ok=True); n=6
    splits(out,[("h6a","h6b","6:00 A.M."),("h12a","h12b","12:00 P.M."),("h18a","h18b","6:00 P.M."),("h23a","h23b","11:30 P.M.")],
           [("BOTH HAVE ",WHITE),("24 HOURS.",GOLD)],("COUCH DAD","KING DAD"),n)
    close("h_close.png","SAME 24 HOURS.","DIFFERENT LIFE.","SLEEP","FREE 7-NIGHT SLEEP RESET","Follow for Part 2.",5,n,out,118,110)
    shutil.copy(END,f"{out}/06.png")
def archer():
    out=O+"MFM-Stop-Overthinking"; os.makedirs(out,exist_ok=True); n=6
    c=Image.new("RGBA",(W,H),(0,0,0,255)); ph=(H-12)//3
    labs=[("ar1","RESEARCHING THE PERFECT PROGRAM",False),("ar2","OVERTHINKING THE FIRST WORKOUT",False),("ar3","DOING IT.",True)]
    for k,(img,lab,g) in enumerate(labs):
        c.paste(fitf(K+img+".png",W,ph,0.5,0.3),(0,k*(ph+6)))
    d=ImageDraw.Draw(c)
    for k in (1,2): d.rectangle([0,k*(ph+6)-6,W,k*(ph+6)],fill=DGOLD)
    for k,(img,lab,g) in enumerate(labs): tag(d,lab,30,k*(ph+6)+ph-72,g)
    fin(c,1,n,out)
    rows=[("ar1","STAGE 1: RESEARCHING.","12 tabs open. 0 reps done."),("ar2","STAGE 2: OVERTHINKING.","20 minutes in the doorway."),("ar3","STAGE 3: DOING IT.","One dumbbell. One set. Today.")]
    for i,(img,h1,sub) in enumerate(rows):
        c=letter(K+img+".png",400); d=ImageDraw.Draw(c)
        ctext(d,h1,170,anton(100),GOLD if i==2 else WHITE,5); ctext(d,sub,1070,raleway(48,"ExtraBold"),WHITE,3); fin(c,i+2,n,out)
    lclose("ar_close2.png","THE FIRST REP","BEATS THE PERFECT PLAN.","GAINS","FREE OVER-40 TRAINING PLAN","Follow for more.",5,n,out,110,84)
    shutil.copy(END,f"{out}/06.png")
for fn in sys.argv[1:]: globals()[fn]()
print("done")
