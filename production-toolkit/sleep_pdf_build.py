from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader

W,H=letter
GOLD=HexColor('#BA7517'); GL=HexColor('#D89A3A'); CARD=HexColor('#222222'); GREY=HexColor('#BBBBBB')
BADGE=ImageReader('/home/claude/logo_badge.png'); MARK=ImageReader('/home/claude/logo_mark.png')
TOTAL=9
OUT='/mnt/user-data/outputs/SLEEP-7-Night-Sleep-Reset.pdf'
body=ParagraphStyle('b',fontName='Helvetica',fontSize=10.5,leading=14,textColor=white)
small=ParagraphStyle('s',parent=body,fontSize=9.5,leading=12.5)
cite=ParagraphStyle('c',fontName='Helvetica-Oblique',fontSize=8,leading=10,textColor=GL)
gital=ParagraphStyle('g',fontName='Helvetica-Oblique',fontSize=9.5,leading=12.5,textColor=GL)

def P(c,text,x,y,w,st=body):
    p=Paragraph(text,st); _,h=p.wrap(w,1000); p.drawOn(c,x,y-h); return y-h
def bg(c): c.setFillColor(black); c.rect(0,0,W,H,fill=1,stroke=0)
def interior(c,n,eyebrow,title):
    bg(c); c.setStrokeColor(GOLD); c.setLineWidth(1.2); m=0.35*inch; c.rect(m,m,W-2*m,H-2*m,fill=0)
    c.setFillColor(GOLD); c.setFont('Helvetica-Bold',9); c.drawString(0.75*inch,H-0.8*inch,f'PAGE {n:02d} / {eyebrow}')
    c.setLineWidth(0.5); c.line(0.75*inch,H-0.86*inch,W-0.75*inch,H-0.86*inch)
    c.setFont('Helvetica-Bold',21); c.drawString(0.75*inch,H-1.25*inch,title)
    c.setFont('Helvetica-Bold',9); c.drawRightString(W-0.6*inch,0.5*inch,f'{n} / {TOTAL}')
    mw=1.6*inch; mh=mw*737/617*0.32
    c.drawImage(BADGE,W/2-0.22*inch,0.42*inch,0.44*inch,0.44*inch,mask='auto')
    c.setFont('Helvetica',7); c.setFillColor(GREY); c.drawCentredString(W/2,0.33*inch,'@melaninfitmen')
    return H-1.5*inch
def card(c,x,y,w,title,text,citation=None,label=None,pad=0.15*inch):
    # measure
    iw=w-2*pad-0.05*inch
    parts=[]
    if label: parts.append(Paragraph(label,ParagraphStyle('l',fontName='Helvetica-Bold',fontSize=8.5,leading=11,textColor=GL)))
    parts.append(Paragraph(title,ParagraphStyle('t',fontName='Helvetica-Bold',fontSize=10.5,leading=13,textColor=GOLD)))
    parts.append(Paragraph(text,small))
    if citation: parts.append(Paragraph(citation,cite))
    hs=[p.wrap(iw,1000)[1] for p in parts]; h=sum(hs)+2*pad+4*(len(parts)-1)
    c.setFillColor(CARD); c.rect(x,y-h,w,h,fill=1,stroke=0)
    c.setFillColor(GOLD); c.rect(x,y-h,2,h,fill=1,stroke=0)
    yy=y-pad
    for p,hh in zip(parts,hs): p.drawOn(c,x+pad+0.05*inch,yy-hh); yy-=hh+4
    return y-h
def badge_row(c,x,y,w,badge,title,why,payoff):
    bw=1.05*inch
    p1=Paragraph(title,ParagraphStyle('t',fontName='Helvetica-Bold',fontSize=11,leading=13.5,textColor=white))
    p2=Paragraph(why,small); p3=Paragraph(payoff,gital)
    iw=w-bw-0.35*inch; hs=[p.wrap(iw,1000)[1] for p in (p1,p2,p3)]; h=max(sum(hs)+0.3*inch,0.8*inch)
    c.setFillColor(CARD); c.rect(x,y-h,w,h,fill=1,stroke=0); c.setFillColor(GOLD); c.rect(x,y-h,2,h,fill=1,stroke=0)
    c.setFillColor(GOLD); c.roundRect(x+0.15*inch,y-h/2-0.2*inch,bw-0.1*inch,0.4*inch,6,fill=1,stroke=0)
    c.setFillColor(black); c.setFont('Helvetica-Bold',10); c.drawCentredString(x+0.15*inch+(bw-0.1*inch)/2,y-h/2-0.05*inch,badge)
    yy=y-0.15*inch; xx=x+bw+0.2*inch
    for p,hh in zip((p1,p2,p3),hs): p.drawOn(c,xx,yy-hh); yy-=hh+2
    return y-h

c=canvas.Canvas(OUT,pagesize=letter); c.setTitle('The 7-Night Sleep Reset'); c.setAuthor('@melaninfitmen')
# 1 COVER
bg(c); s=4*inch; c.drawImage(BADGE,W/2-s/2,H-0.9*inch-s,s,s,mask='auto')
c.setFillColor(GOLD); c.setFont('Helvetica-Bold',36); c.drawCentredString(W/2,H-5.55*inch,'THE 7-NIGHT')
c.drawCentredString(W/2,H-6.1*inch,'SLEEP RESET')
c.setFillColor(white); c.setFont('Helvetica-Bold',14); c.drawCentredString(W/2,H-6.6*inch,'A clinically backed plan for men who are done running on empty')
c.setFillColor(GREY); c.setFont('Helvetica-Oblique',11); c.drawCentredString(W/2,H-6.95*inch,'Built on sleep-medicine guidelines and human studies. No hacks, no gimmicks, no pills.')
c.setStrokeColor(GOLD); c.setLineWidth(1.2); c.line(1.5*inch,H-7.3*inch,W-1.5*inch,H-7.3*inch)
c.setFillColor(GOLD); c.setFont('Helvetica-Bold',10); c.drawCentredString(W/2,H-7.7*inch,'TRAIN HARD. EAT RIGHT. LIVE LONG.')
c.setFillColor(GREY); c.setFont('Helvetica',8); c.drawCentredString(W/2,0.75*inch,'FREE RESOURCE — NOT FOR RESALE')
c.drawCentredString(W/2,0.58*inch,'© @melaninfitmen · Educational only, not medical advice. Talk to your doctor about your own health.')
c.showPage()

# 2 WHY
y=interior(c,2,'WHY THIS MATTERS','SLEEP IS NOT LAZY. IT\'S MAINTENANCE.')
y=P(c,'You train, you eat right, you show up for your family. But if you\'re sleeping five or six hours, you\'re running the whole machine on a low battery. Here\'s what the research actually says.',0.75*inch,y,W-1.5*inch)-0.2*inch
stats=[('7+ HOURS','What adults need, every night, on a regular basis.','American Academy of Sleep Medicine & Sleep Research Society joint consensus (Watson et al., Sleep, 2015)'),
       ('4 IN 10','Black adults in the U.S. sleep less than 7 hours a night (40.2%), compared with 28.9% of white adults.','CDC / National Center for Health Statistics, NCHS Data Brief No. 559 (2024 data)'),
       ('+37%','Higher risk of type 2 diabetes in short sleepers. Also linked: +17% high blood pressure, +38% obesity, +12% death from any cause.','Meta-analysis of 153 studies, 5.1 million people (Itani et al., Sleep Medicine, 2017). These are associations, not proof that short sleep causes them.')]
for big,txt,src in stats:
    c.setFillColor(CARD); h=0.95*inch; c.rect(0.75*inch,y-h,W-1.5*inch,h,fill=1,stroke=0); c.setFillColor(GOLD); c.rect(0.75*inch,y-h,2,h,fill=1,stroke=0)
    c.setFont('Helvetica-Bold',22); c.drawString(0.95*inch,y-0.55*inch,big)
    yy=P(c,txt,2.75*inch,y-0.13*inch,W-3.65*inch,small); P(c,src,2.75*inch,yy-0.04*inch,W-3.65*inch,cite)
    y-=h+0.15*inch
y-=0.05*inch
c.setFillColor(CARD); h=0.85*inch; c.rect(0.75*inch,y-h,W-1.5*inch,h,fill=1,stroke=0); c.setFillColor(GOLD); c.rect(0.75*inch,y-h,3,h,fill=1,stroke=0)
P(c,'"You can\'t out-train, out-diet or out-supplement a body that never gets to recover. Sleep is the cheapest performance tool you own."',0.95*inch,y-0.15*inch,W-1.9*inch,ParagraphStyle('q',fontName='Helvetica-Oblique',fontSize=12,leading=16,textColor=GL))
y-=h+0.2*inch
P(c,'<b>The good news:</b> the habits that fix most bad sleep are free, and the strongest ones have been tested in real clinical trials. That\'s what this 7-night plan is built on.',0.75*inch,y,W-1.5*inch)
c.showPage()

# 3 SCIENCE
y=interior(c,3,'THE SCIENCE','WHAT THE STUDIES ACTUALLY SHOW')
x=0.75*inch; w=W-1.5*inch
y=card(c,x,y,w,'Caffeine stays in your night longer than you think','Across 24 studies, caffeine cut total sleep by about <b>45 minutes</b> and made sleep less efficient. To avoid losing sleep, the researchers estimated a regular coffee should be finished at least <b>8.8 hours</b> before bed, and a typical pre-workout serving (~218 mg) at least <b>13.2 hours</b> before bed.','Gardiner et al., Sleep Medicine Reviews, 2023 (systematic review &amp; meta-analysis)',label='META-ANALYSIS')-0.14*inch
y=card(c,x,y,w,'The nightcap backfires','Even about 2 drinks reduced and delayed REM sleep, and more alcohol made it worse. Alcohol can help you fall asleep, then breaks up the second half of the night.','Gardiner et al., Sleep Medicine Reviews, 2025 (meta-analysis of 27 studies); Ebrahim et al., Alcoholism: Clinical &amp; Experimental Research, 2013',label='META-ANALYSIS')-0.14*inch
y=card(c,x,y,w,'Moving during the day helps you sleep at night','Pooled results from 66 studies: regular exercise modestly improved sleep quality and how fast people fell asleep. It\'s not a sleeping pill, but it adds up.','Kredlow et al., Journal of Behavioral Medicine, 2015 (meta-analysis)',label='META-ANALYSIS')-0.14*inch
y=card(c,x,y,w,'The #1 treatment for insomnia isn\'t a pill','The American College of Physicians recommends CBT-I (cognitive behavioral therapy for insomnia) as the <b>first</b> treatment for chronic insomnia in adults. Two of its core tools, a fixed wake time and only using the bed for sleep, are built into this plan. Note: "sleep hygiene" tips on their own are <b>not</b> recommended as a stand-alone insomnia treatment.','Qaseem et al., Annals of Internal Medicine, 2016 (ACP guideline); Edinger et al., J Clin Sleep Med, 2021 (AASM guideline, based on 124 RCTs)',label='CLINICAL GUIDELINE')-0.14*inch
y=card(c,x,y,w,'Same time, every day','In about 61,000 adults tracked with wrist sensors, people with the most regular sleep schedules had a 20–48% lower risk of death than the least regular, a stronger signal than sleep length alone.','Windred et al., Sleep, 2024 (large prospective cohort; association, not cause and effect)',label='LARGE COHORT')
c.showPage()

# 4 RULES
y=interior(c,4,'THE 5 RULES','FIVE RULES THAT DO THE HEAVY LIFTING')
rows=[('9 HRS','Coffee cutoff: 9 hours before bed','Bed at 11 p.m.? Last coffee by 2 p.m. Pre-workout? Mornings only.','Payoff: you stop losing sleep you never knew you lost.'),
      ('SAME TIME','One wake-up time, 7 days a week','Weekends included. A fixed wake time is the anchor of CBT-I and the CDC\'s #1 tip.','Payoff: your body clock starts making you sleepy on time.'),
      ('30 MIN','Screens off 30 minutes before bed','CDC advice. Phone charges outside the bedroom, or at least across the room.','Payoff: no 1 a.m. scroll stealing tomorrow\'s energy.'),
      ('20 MIN','Bed is for sleep','Can\'t fall asleep after about 20 minutes? Get up, do something calm in dim light, and come back when sleepy (CBT-I stimulus control).','Payoff: your brain relearns that bed = sleep, not stress.'),
      ('LAST CALL','No alcohol on reset nights','Even ~2 drinks cut REM sleep. Run the 7 nights dry and see the difference for yourself.','Payoff: deeper second half of the night.')]
for b,t,wy,pay in rows: y=badge_row(c,0.75*inch,y,W-1.5*inch,b,t,wy,pay)-0.13*inch
P(c,'Also on the CDC list: keep the bedroom quiet, dark and cool, avoid big meals right before bed, and get regular exercise.',0.75*inch,y-0.05*inch,W-1.5*inch,small)
c.showPage()

# 5 PLAN
y=interior(c,5,'THE PLAN','7 NIGHTS, ONE NEW HABIT EACH')
P(c,'Stack them: each night keeps everything from the nights before.',0.75*inch,y,W-1.5*inch,gital)
y-=0.3*inch
nights=[('NIGHT 1','Set your anchor','Pick a wake-up time you can hold all 7 days. Count back 7½–8 hours: that\'s your lights-out time. Fill in the tracker tonight.'),
        ('NIGHT 2','Caffeine cutoff','Last coffee, soda, energy drink or pre-workout 9+ hours before lights-out.'),
        ('NIGHT 3','Phone out','Devices off 30 minutes before bed. Charge the phone outside the bedroom. Old-school alarm if you need one.'),
        ('NIGHT 4','Set the room','Cool, dark and quiet. TV off. Blackout curtains or an eye mask if streetlights get in.'),
        ('NIGHT 5','The 20-minute rule','Bed is only for sleep. Awake for ~20 minutes? Get up, keep the lights low, come back when sleepy. Same wake time no matter what.'),
        ('NIGHT 6','Earn it during the day','Get a 20–30 minute walk or workout in, and finish your big meal a few hours before bed.'),
        ('NIGHT 7','Review and lock in','Look at your tracker. Keep the habits that helped. Take the sleep apnea check on page 7.')]
colw=(W-1.5*inch-0.2*inch)/2; xs=[0.75*inch,0.75*inch+colw+0.2*inch]; ys=[y,y]
for i,(lab,t,txt) in enumerate(nights):
    col=0 if i<4 else 1
    ys[col]=card(c,xs[col],ys[col],colw,t,txt,label=lab)-0.13*inch
card(c,xs[1],ys[1],colw,'Bad night? Hold the line.','Keep the same wake-up time anyway. Sleeping in to "catch up" pushes tonight\'s bedtime later and restarts the cycle. Tomorrow night you\'ll be ready to sleep.',label='IF A NIGHT GOES BAD')
c.showPage()

# 6 TRACKER
y=interior(c,6,'TRACKER','YOUR 7-NIGHT LOG')
P(c,'Fill it in each morning. Don\'t judge it, just write it down. Patterns show up fast.',0.75*inch,y,W-1.5*inch,small)
y-=0.35*inch
cols=['NIGHT','LIGHTS OUT','WOKE UP','HOURS SLEPT','LAST CAFFEINE','SCREENS OFF 30?','DRINKS','RESTED (1–5)']
x0=0.75*inch; tw=W-1.5*inch; cw=tw/len(cols); rh=0.62*inch
c.setFillColor(GOLD); c.rect(x0,y-0.42*inch,tw,0.42*inch,fill=1,stroke=0)
c.setFillColor(black); c.setFont('Helvetica-Bold',7.2)
for i,t in enumerate(cols):
    parts=t.split(' ') if len(t)>11 else [t]
    if len(parts)>1: mid=len(parts)//2; a=' '.join(parts[:mid]); b=' '.join(parts[mid:]); c.drawCentredString(x0+cw*i+cw/2,y-0.18*inch,a); c.drawCentredString(x0+cw*i+cw/2,y-0.32*inch,b)
    else: c.drawCentredString(x0+cw*i+cw/2,y-0.25*inch,t)
y-=0.42*inch
c.setStrokeColor(GOLD); c.setLineWidth(0.6)
for r in range(7):
    c.setFillColor(CARD if r%2==0 else black); c.rect(x0,y-rh,tw,rh,fill=1,stroke=0)
    c.setFillColor(GOLD); c.setFont('Helvetica-Bold',11); c.drawCentredString(x0+cw/2,y-rh/2-4,str(r+1))
    y-=rh
yt=y
for i in range(len(cols)+1): c.line(x0+cw*i,yt,x0+cw*i,yt+rh*7+0.42*inch)
for r in range(8): c.line(x0,yt+rh*r,x0+tw,yt+rh*r)
y=yt-0.3*inch
y=card(c,0.75*inch,y,W-1.5*inch,'After 7 nights, ask yourself','Did my hours go up? Which night felt best, and what did I do differently? Which one habit am I keeping no matter what?',label='REVIEW')
c.showPage()

# 7 APNEA
y=interior(c,7,'SNORE? READ THIS','THE SLEEP PROBLEM MOST MEN MISS')
y=P(c,'Obstructive sleep apnea means your airway keeps closing while you sleep. You can spend 8 hours in bed and still wake up exhausted. It\'s common in men, and most cases are never diagnosed.',0.75*inch,y,W-1.5*inch)-0.15*inch
x=0.75*inch; w=W-1.5*inch
y=card(c,x,y,w,'How common it is','About <b>1 in 10 men aged 30–49</b> and <b>1 in 6 men aged 50–70</b> have moderate-to-severe sleep apnea. In a large study of older U.S. adults, only 7–16% of people with moderate-to-severe apnea had ever been diagnosed.','Peppard et al., American Journal of Epidemiology, 2013; Chen et al., Sleep, 2015 (MESA)',label='LARGE COHORTS')-0.14*inch
# STOP-Bang
items=[('S','Snore loudly (loud enough to hear through a door)?'),('T','Often Tired, fatigued or sleepy during the day?'),('O','Has anyone Observed you stop breathing or choke in your sleep?'),('P','Treated for high blood Pressure?'),('B','BMI over 35?'),('A','Age over 50?'),('N','Neck size over 16 inches (40 cm)?'),('G','Gender: male?')]
h=0.32*inch*len(items)+0.75*inch
c.setFillColor(CARD); c.rect(x,y-h,w,h,fill=1,stroke=0); c.setFillColor(GOLD); c.rect(x,y-h,2,h,fill=1,stroke=0)
c.setFont('Helvetica-Bold',10.5); c.drawString(x+0.2*inch,y-0.28*inch,'THE STOP-BANG CHECK: one point for every YES')
yy=y-0.55*inch
for L,q in items:
    c.setFillColor(GOLD); c.roundRect(x+0.2*inch,yy-0.17*inch,0.26*inch,0.24*inch,3,fill=1,stroke=0)
    c.setFillColor(black); c.setFont('Helvetica-Bold',10); c.drawCentredString(x+0.33*inch,yy-0.11*inch,L)
    c.setFillColor(white); c.setFont('Helvetica',10); c.drawString(x+0.6*inch,yy-0.11*inch,q)
    c.setStrokeColor(GOLD); c.rect(x+w-0.5*inch,yy-0.16*inch,0.2*inch,0.2*inch,fill=0)
    yy-=0.32*inch
c.setFillColor(GL); c.setFont('Helvetica-Oblique',8); c.drawString(x+0.2*inch,y-h+0.12*inch,'Screening questionnaire validated by Chung et al., Anesthesiology 2008 and British Journal of Anaesthesia 2012.')
y-=h+0.14*inch
y=card(c,x,y,w,'Scored 3 or more? Talk to your doctor about a sleep test.','A questionnaire can\'t diagnose sleep apnea; only a sleep study can. The good news: for most otherwise-healthy adults at higher risk, the American Academy of Sleep Medicine says a <b>home sleep apnea test</b> is an appropriate way to check. If you\'re diagnosed, treatment like CPAP lowered blood pressure modestly (about 2–3 mmHg on average) across 51 clinical trials.','Kapur et al., J Clin Sleep Med, 2017 (AASM guideline); Bratton et al., JAMA, 2015 (meta-analysis of 51 RCTs)',label='CLINICAL GUIDELINE')
c.showPage()

# 8 INSIDER + NEXT
y=interior(c,8,'INSIDER TRUTH + NEXT STEPS','BEFORE YOU BUY A SLEEP SUPPLEMENT')
x=0.75*inch; w=W-1.5*inch
y=card(c,x,y,w,'What\'s on the label isn\'t always what\'s in the bottle','I spent 15 years in supplement manufacturing. Here\'s what the testing shows for melatonin: in one study of 31 products, actual melatonin ranged from <b>83% less to 478% more</b> than the label. In a 2023 test of 25 U.S. melatonin gummy brands, 22 were mislabeled, with actual amounts from 74% to 347% of what the label claimed.','Erland &amp; Saxena, J Clin Sleep Med, 2017; Cohen et al., JAMA, 2023',label='PRODUCT TESTING')-0.14*inch
y=card(c,x,y,w,'What the sleep doctors say','For chronic insomnia, the American Academy of Sleep Medicine suggests <b>not</b> using melatonin, valerian or diphenhydramine (the antihistamine in many "PM" pills). Melatonin does have a real use as a timing tool for specific body-clock disorders, under a doctor\'s guidance. Fix the habits first.','Sateia et al., J Clin Sleep Med, 2017 (AASM pharmacologic guideline)',label='CLINICAL GUIDELINE')-0.14*inch
y=card(c,x,y,w,'See a doctor if…','• Trouble sleeping 3+ nights a week for 3+ months: ask about CBT-I (in person or a digital program).<br/>• Loud snoring, gasping, or a STOP-Bang score of 3+: ask about a sleep test.<br/>• You nod off while driving: treat it as urgent.<br/>• You take medications that affect sleep: talk to your doctor before changing anything.',label='WHEN IT\'S MORE THAN HABITS')-0.2*inch
h=1.45*inch
c.setFillColor(GOLD); c.roundRect(x,y-h,w,h,8,fill=1,stroke=0)
c.setFillColor(black); c.setFont('Helvetica-Bold',15); c.drawCentredString(W/2,y-0.38*inch,'FINISHED THE 7 NIGHTS?')
P(c,'<para alignment="center">Comment <b>WALK</b> on any @melaninfitmen post and I\'ll send you the 4-Week Starter Walking Protocol. Daytime movement is the next piece of better sleep.</para>',x+0.3*inch,y-0.5*inch,w-0.6*inch,ParagraphStyle('k',fontName='Helvetica',fontSize=10,leading=13,textColor=black))
c.setFont('Helvetica-Bold',8); c.drawCentredString(W/2,y-h+0.2*inch,'KING · GAINS · FUEL · SUPPS · THERAPY · LIFT · cGMP · TAINTED · GLP · SLEEP · TRUTH · WALK')
c.showPage()

# 9 SOURCES
y=interior(c,9,'SOURCES','THE RESEARCH BEHIND THIS GUIDE')
src=['Watson NF, et al. Recommended amount of sleep for a healthy adult: AASM/SRS joint consensus statement. <i>Sleep</i>. 2015;38(6):843-844.',
'Ng AE, Black LI, Adjaye-Gbewonyo D. Short sleep duration and sleep difficulties among adults: United States, 2024. NCHS Data Brief No. 559.',
'Itani O, et al. Short sleep duration and health outcomes: a systematic review, meta-analysis, and meta-regression. <i>Sleep Med</i>. 2017;32:246-256.',
'Gardiner C, et al. The effect of caffeine on subsequent sleep: a systematic review and meta-analysis. <i>Sleep Med Rev</i>. 2023;69:101764.',
'Gardiner C, et al. The effect of alcohol on subsequent sleep in healthy adults: a systematic review and meta-analysis. <i>Sleep Med Rev</i>. 2025;80:102030.',
'Ebrahim IO, et al. Alcohol and sleep I: effects on normal sleep. <i>Alcohol Clin Exp Res</i>. 2013;37(4):539-549.',
'Kredlow MA, et al. The effects of physical activity on sleep: a meta-analytic review. <i>J Behav Med</i>. 2015;38(3):427-449.',
'Qaseem A, et al. Management of chronic insomnia disorder in adults: a clinical practice guideline from the ACP. <i>Ann Intern Med</i>. 2016;165(2):125-133.',
'Edinger JD, et al. Behavioral and psychological treatments for chronic insomnia disorder in adults: an AASM clinical practice guideline. <i>J Clin Sleep Med</i>. 2021;17(2):255-262.',
'Windred DP, et al. Sleep regularity is a stronger predictor of mortality risk than sleep duration. <i>Sleep</i>. 2024;47(1):zsad253.',
'Centers for Disease Control and Prevention. About sleep: tips for better sleep. cdc.gov/sleep.',
'Peppard PE, et al. Increased prevalence of sleep-disordered breathing in adults. <i>Am J Epidemiol</i>. 2013;177(9):1006-1014.',
'Chen X, et al. Racial/ethnic differences in sleep disturbances: the Multi-Ethnic Study of Atherosclerosis (MESA). <i>Sleep</i>. 2015;38(6):877-888.',
'Chung F, et al. STOP questionnaire: a tool to screen patients for obstructive sleep apnea. <i>Anesthesiology</i>. 2008;108(5):812-821; and Chung F, et al. <i>Br J Anaesth</i>. 2012;108(5):768-775.',
'Kapur VK, et al. Clinical practice guideline for diagnostic testing for adult obstructive sleep apnea: an AASM guideline. <i>J Clin Sleep Med</i>. 2017;13(3):479-504.',
'Bratton DJ, et al. CPAP vs mandibular advancement devices and blood pressure in patients with obstructive sleep apnea. <i>JAMA</i>. 2015;314(21):2280-2293.',
'Erland LA, Saxena PK. Melatonin natural health products and supplements: presence of serotonin and significant variability of melatonin content. <i>J Clin Sleep Med</i>. 2017;13(2):275-281.',
'Cohen PA, et al. Quantity of melatonin and CBD in melatonin gummies sold in the US. <i>JAMA</i>. 2023;329(16):1401-1402.',
'Sateia MJ, et al. Clinical practice guideline for the pharmacologic treatment of chronic insomnia in adults: an AASM guideline. <i>J Clin Sleep Med</i>. 2017;13(2):307-349.']
st=ParagraphStyle('r',fontName='Helvetica',fontSize=8.6,leading=11,textColor=white,leftIndent=14,firstLineIndent=-14)
for i,s in enumerate(src): y=P(c,f'<font color="#BA7517"><b>{i+1}.</b></font> {s}',0.75*inch,y,W-1.5*inch,st)-0.06*inch
y-=0.1*inch
P(c,'This guide is for education only and is not medical advice. It doesn\'t replace a visit with your doctor. If you have a sleep disorder, a medical condition, or take medications, talk to your healthcare provider before making changes.',0.75*inch,y,W-1.5*inch,cite)
c.showPage(); c.save(); print(OUT)
