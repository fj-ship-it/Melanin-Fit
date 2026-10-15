import os, sys, json, shutil, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from mfm import anton, raleway, logo, pill, W, H, WHITE, GOLD, DGOLD, END
KIT=os.path.dirname(os.path.abspath(__file__))+"/"; K=KIT+"food_library/"; OUT=os.environ.get("OUT","out/MFM-The-Fuel-Chart/"); os.makedirs(OUT,exist_ok=True)
GREY=(160,160,160); LG=(255,214,130)
import functools
@functools.lru_cache(maxsize=None)
def column(name,maxw=124,maxh=560):
    im=Image.open(K+name+".jpg").convert("RGB"); a=np.asarray(im).astype(int)
    lum=a.max(axis=2); h=a.shape[0]
    # food = bright rows in upper ~78% (exclude the reflection under it)
    mask=lum>60; z=mask[:int(h*0.80)]; rows=np.where(z.sum(axis=1)>a.shape[1]*0.06)[0]
    cols=np.where(z[rows.min():rows.max()+1].sum(axis=0)>(rows.max()-rows.min())*0.08)[0]
    y0,y1=rows.min(),rows.max(); x0,x1=cols.min(),cols.max()
    # find base: last row in food zone with substantial width
    crop=im.crop((max(0,x0-6),y0,min(im.width,x1+6),y1+2))
    r=min(maxw/crop.width,500/crop.height); crop=crop.resize((max(1,int(crop.width*r)),max(1,int(crop.height*r))),Image.LANCZOS)
    m=Image.fromarray((np.clip((np.asarray(crop).max(axis=2).astype(float)-18)*6,0,255)).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    return crop,m
def bg():
    c=Image.new("RGB",(W,H),(6,6,6)); g=Image.new("L",(W,H),0); d=ImageDraw.Draw(g)
    d.ellipse([-200,520,W+200,1500],fill=110); g=g.filter(ImageFilter.GaussianBlur(160))
    glow=Image.new("RGB",(W,H),(70,46,10)); c=Image.composite(glow,c,g)
    d=ImageDraw.Draw(c); d.rectangle([0,1138,W,H],fill=(10,9,8))
    return c.convert("RGBA")
def ctext(d,t,y,f,col,cx=W/2,stroke=0):
    tw=d.textlength(t,font=f); d.text((cx-tw/2,y),t,font=f,fill=col,stroke_width=stroke,stroke_fill=(0,0,0)); return tw
def fit(d,t,size,maxw,font=anton):
    f=font(size)
    while d.textlength(t,font=f)>maxw: size-=2; f=font(size)
    return f
BASE=1130
def chart(spec,i,n,prog=1.0,save=True):
    c=bg(); d=ImageDraw.Draw(c)
    t1,t2=spec["title"]; ctext(d,t1,150,fit(d,t1,104,1000),WHITE); ctext(d,t2,262,fit(d,t2,104,1000),GOLD)
    ctext(d,spec["sub"],384,fit(d,spec["sub"],32,1000,lambda s:raleway(s,"Bold")),(230,230,230))
    f=raleway(22,"ExtraBold"); bt=spec["basis"].upper(); 
    # letter-spaced basis line
    tw=sum(d.textlength(ch,font=f)+2 for ch in bt); x=(W-tw)/2
    for ch in bt: d.text((x,432),ch,font=f,fill=GREY); x+=d.textlength(ch,font=f)+2
    items=spec["items"]; k=len(items); cw=W/k
    for j,(img,val,small,label) in enumerate(items):
        cx=cw*j+cw/2
        p=min(max((prog*k*1.0-j*0.55)/1.2,0),1) if prog<1 else 1.0
        e=1-(1-p)**3
        col,m=column(img,int(cw-10))
        hgt=col.height; top=BASE-hgt
        if e>0:
            vis=int(hgt*e)
            if vis>2:
                cc=col.crop((0,hgt-vis,col.width,hgt)); mm=m.crop((0,hgt-vis,col.width,hgt))
                c.paste(cc,(int(cx-col.width/2),BASE-vis),mm)
                rf=col.transpose(Image.FLIP_TOP_BOTTOM).crop((0,0,col.width,min(70,hgt)))
                fade=Image.linear_gradient("L").resize((col.width,rf.height)).point(lambda v:int((255-v)*0.35))
                rm=Image.fromarray((np.asarray(m.transpose(Image.FLIP_TOP_BOTTOM).crop((0,0,col.width,rf.height))).astype(float)*np.asarray(fade)/255).astype(np.uint8))
                if e>0.9: c.paste(rf,(int(cx-col.width/2),BASE+2),rm)
        d=ImageDraw.Draw(c)
        # number + leader line
        numtxt=val if e>=1 else spec.get("fmt",lambda v,e:v)(val,e)
        fv=fit(d,val,50,cw-8); ctext(d,numtxt,478,fv,GOLD,cx)
        fs=raleway(19,"Bold"); ctext(d,small,538,fit(d,small,19,cw-6,lambda s:raleway(s,"Bold")),(210,210,210),cx)
        ly1=top-14 if e>=1 else BASE-int(hgt*e)-14
        d.line([(cx,568),(cx,max(570,ly1))],fill=(150,105,30),width=2); d.ellipse([cx-4,max(570,ly1)-4,cx+4,max(570,ly1)+4],fill=GOLD)
        fl=raleway(21,"ExtraBold"); words=label.upper().split(); lines=[]; cur=""
        for w in words:
            tt=(cur+" "+w).strip()
            if d.textlength(tt,font=fl)<=cw-8: cur=tt
            else: lines.append(cur); cur=w
        lines.append(cur); lines=[l for l in lines if l]
        for li,l in enumerate(lines[:2]): ctext(d,l,1212+li*26,fit(d,l,21,cw-6,lambda s:raleway(s,"ExtraBold")),WHITE,cx)
    ctext(d,spec["src"],1300,raleway(21,"Bold"),GREY)
    logo(c,90,24,18); pill(c,f"{i}/{n}")
    if save: c.convert("RGB").save(f"{OUT}{i:02d}.png")
    return c.convert("RGB")
S=[
 dict(title=("THE MOST PROTEIN","PER BITE"),sub="More protein for every calorie you spend.",basis="grams protein per 100 g cooked · calories",src="Source: USDA FoodData Central",
  items=[("chicken","31g","165 cal","Chicken breast"),("turkey","30g","136 cal","Turkey breast"),("beef","29g","209 cal","Lean beef 93/7"),("shrimp","24g","99 cal","Shrimp"),
         ("tuna","19g","86 cal","Tuna (canned)"),("eggs","13g","155 cal","Eggs"),("gyogurt","10g","59 cal","Greek yogurt"),("cottage","10g","81 cal","Cottage cheese")]),
 dict(title=("CARBS RANKED","BY FIBER"),sub="Same carbs. More fiber keeps you full longer.",basis="fiber per 100 g cooked · carbs · calories",src="Source: USDA FoodData Central",
  items=[("bbeans","8.7g","24g carbs","Black beans"),("sweetpot","3.3g","21g carbs","Sweet potato"),("quinoa","2.8g","21g carbs","Quinoa"),("banana","2.6g","23g carbs","Banana"),
         ("potato","2.2g","21g carbs","Potato (skin on)"),("oatmeal","1.7g","12g carbs","Oatmeal"),("brice","1.6g","26g carbs","Brown rice"),("wrice","0.4g","28g carbs","White rice")]),
 dict(title=("THE MOST FILLING","FOODS"),sub="Same 240 calories. Very different hunger afterward.",basis="satiety index · white bread = 100",src="Source: Holt et al., Eur J Clin Nutr, 1995",
  items=[("potato","323","boiled","Potatoes"),("whitefish","225","baked","White fish"),("oatmeal","209","porridge","Oatmeal"),("orange","202","whole","Oranges"),
         ("apple","197","whole","Apples"),("wwpasta","188","whole wheat","Pasta"),("steak","176","lean","Beef steak"),("bakedbeans","168","","Baked beans")]),
 dict(title=("FOODS FOR YOUR","BLOOD PRESSURE"),sub="Potassium helps balance sodium. Men need 3,400 mg a day.",basis="potassium (mg) per serving",src="Source: USDA FoodData Central",
  items=[("wbeans","1,000","1 cup","White beans"),("potato","930","1 medium","Baked potato"),("spinach","840","1 cup cooked","Spinach"),("gyogurt","620","1 cup","Plain yogurt"),
         ("sweetpot","540","1 medium","Sweet potato"),("salmon","530","3 oz wild","Salmon"),("banana","420","1 medium","Banana"),("avocado","360","1/2 cup","Avocado")]),
 dict(title=("FIBER FOR","YOUR GUT"),sub="Men need about 28–34 grams a day. Start here.",basis="grams of fiber per serving",src="Source: USDA FoodData Central · Dietary Guidelines 2020–2025",
  items=[("lentils","16g","1 cup","Lentils"),("splitpeas","16g","1 cup","Split peas"),("bbeans","15g","1 cup","Black beans"),("chia","10g","1 oz","Chia seeds"),
         ("raspberry","8g","1 cup","Raspberries"),("pear","6g","1 medium","Pear"),("broccoli","5g","1 cup","Broccoli"),("oatmeal","4g","1 cup","Oatmeal")]),
 dict(title=("VITAMIN D","FROM YOUR PLATE"),sub="Melanin lowers how much vitamin D your skin makes from sun.",basis="vitamin d (iu) per serving",src="Source: NIH Office of Dietary Supplements",
  items=[("trout","645","3 oz","Rainbow trout"),("salmon","570","3 oz","Sockeye salmon"),("mushroom","366","1/2 cup","UV mushrooms"),("milk","120","1 cup","Milk (fortified)"),
         ("oj","100","1 cup","OJ (fortified)"),("sardines","46","2 fish","Sardines"),("eggs","44","1 large","Egg"),("tuna","40","3 oz","Tuna (canned)")]),
 dict(title=("OMEGA-3s FOR","YOUR HEART"),sub="EPA + DHA, the omega-3s in fish. Aim for fish twice a week.",basis="grams epa + dha per 3 oz cooked",src="Source: NIH Office of Dietary Supplements",
  items=[("salmon","1.8g","farmed","Atlantic salmon"),("herring","1.7g","","Herring"),("sardines","1.2g","canned","Sardines"),("mackerel","1.0g","Atlantic","Mackerel"),
         ("trout","0.8g","","Rainbow trout"),("shrimp","0.2g","","Shrimp"),("tuna","0.2g","canned light","Tuna")]),
]
N=len(S)+1
if __name__=="__main__":
    for i,s in enumerate(S): chart(s,i+1,N)
    shutil.copy(END,f"{OUT}{N:02d}.png"); print("slides ok")
