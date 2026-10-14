from PIL import Image, ImageDraw
from mfm import anton, raleway, W, H, GOLD
def strip(path,kw,offer,y=H-250):
    c=Image.open(path).convert("RGB"); d=ImageDraw.Draw(c)
    f1=anton(54); f2=raleway(34,"ExtraBold")
    t1=f"COMMENT {kw}"; t2=f"  ·  {offer}"
    tw=d.textlength(t1,font=f1)+d.textlength(t2,font=f2)
    x=(W-tw)/2; d.rounded_rectangle([x-34,y,x+tw+34,y+84],radius=42,fill=GOLD)
    d.text((x,y+6),t1,font=f1,fill=(0,0,0)); d.text((x+d.textlength(t1,font=f1),y+22),t2,font=f2,fill=(0,0,0))
    c.save(path)
O="/mnt/user-data/outputs/"
strip(O+"MFM-Week-4/05.png","WALK","FREE 4-WEEK WALKING PLAN")
strip(O+"MFM-Same-Sunday-Dinner/05.png","FUEL","FREE MEAL PREP BLUEPRINT")
strip(O+"MFM-Do-This-Not-That/06.png","KING","FREE HEALTH STARTER GUIDE")
