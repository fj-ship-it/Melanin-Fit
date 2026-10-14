"""MFM 1080x1920 Instagram Story builder (2 per day: AM interactive, PM post-push).

Usage:
    from stories import story
    story(out_dir, "01-Sun-AM-Poll", ("a.png","b.png"), 0.4, "POLL",
          [[("ONE PLATE",WHITE)],[("OR ROUND TWO?",GOLD)]], sub="Be honest.")

img: one path, or a (left, right) tuple for a side-by-side pair.
fy: vertical focus for cropping the scene band (0 top .. 1 bottom).
lines: list of lines; each line is a list of (text, color) parts (Anton, auto-shrinks).
band: optional list of (text, color, size) Raleway lines drawn at y=1520 (use for keyword replies).
Layout: gold kicker pill + headline at top, scene band y=760..1480, empty dark area below
for the Instagram sticker (poll/quiz/slider/questions/post sticker) so it never covers a face.
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from mfm import anton, raleway, LOGO, GOLD, WHITE, DGOLD
VW, VH = 1080, 1920

def _load(p): return Image.open(p).convert("RGB")
def _cover(im, w, h, fy=0.5):
    r = max(w / im.width, h / im.height); im = im.resize((int(im.width * r + 1), int(im.height * r + 1)), Image.LANCZOS)
    x = (im.width - w) // 2; y = int((im.height - h) * fy); return im.crop((x, y, x + w, y + h))
def _ctext(d, t, y, f, col, stroke=4):
    tw = d.textlength(t, font=f); d.text(((VW - tw) / 2, y), t, font=f, fill=col, stroke_width=stroke, stroke_fill=(0, 0, 0))
def _lines(d, lines, y, size, maxw=960):
    for parts in lines:
        if isinstance(parts, str): parts = [(parts, WHITE)]
        s = size; f = anton(s)
        while sum(d.textlength(t, font=f) for t, _ in parts) > maxw: s -= 4; f = anton(s)
        x = (VW - sum(d.textlength(t, font=f) for t, _ in parts)) / 2
        for t, c in parts: d.text((x, y), t, font=f, fill=c, stroke_width=4, stroke_fill=(0, 0, 0)); x += d.textlength(t, font=f)
        y += int(s * 1.12)
    return y

def story(out, fn, img, fy, kicker, lines, sub=None, band=None, size=104):
    os.makedirs(out, exist_ok=True)
    pair = isinstance(img, tuple); src = _load(img[0] if pair else img)
    bg = ImageEnhance.Brightness(_cover(src, VW, VH).filter(ImageFilter.GaussianBlur(38))).enhance(0.38)
    c = bg.convert("RGBA"); BY0, BH = 760, 720
    if pair:
        b = Image.new("RGBA", (VW, BH))
        b.paste(_cover(_load(img[0]), VW // 2 - 3, BH, fy), (0, 0)); b.paste(_cover(_load(img[1]), VW // 2 - 3, BH, fy), (VW // 2 + 3, 0))
        ImageDraw.Draw(b).rectangle([VW // 2 - 3, 0, VW // 2 + 3, BH], fill=DGOLD)
    else: b = _cover(src, VW, BH, fy).convert("RGBA")
    m = Image.new("L", (VW, BH), 255); md = ImageDraw.Draw(m)
    for y in range(90):
        a = int(255 * y / 90); md.line([(0, y), (VW, y)], fill=a); md.line([(0, BH - 1 - y), (VW, BH - 1 - y)], fill=a)
    c.paste(b, (0, BY0), m); d = ImageDraw.Draw(c)
    c.alpha_composite(LOGO.resize((110, 110), Image.LANCZOS), (VW - 150, 230))
    f = raleway(38, "ExtraBold"); tw = d.textlength(kicker, font=f)
    d.rounded_rectangle([(VW - tw) / 2 - 32, 300, (VW + tw) / 2 + 32, 372], radius=36, fill=GOLD)
    d.text(((VW - tw) / 2, 310), kicker, font=f, fill=(0, 0, 0))
    y = _lines(d, lines, 410, size)
    if sub: _ctext(d, sub, y + 10, raleway(38, "Bold"), (230, 230, 230), 3)
    if band:
        y = 1520
        for t, col, fs in band: _ctext(d, t, y, raleway(fs, "ExtraBold"), col, 3); y += int(fs * 1.35)
    path = f"{out}/{fn}.png"; c.convert("RGB").save(path); return path
