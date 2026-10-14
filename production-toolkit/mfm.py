"""Shared MFM slide helpers (rebuilt)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
KIT = os.path.dirname(os.path.abspath(__file__)) + "/"

W, H = 1080, 1350
HALF = H // 2
GOLD = (224, 160, 58)
DGOLD = (186, 117, 23)
WHITE = (255, 255, 255)
F = KIT + "fonts/"
LOGO = Image.open(KIT + "logo_badge.png").convert("RGBA")
MARK = Image.open(KIT + "logo_mark.png").convert("RGBA")
END = KIT + "MFM-Follow-End-Card.png"

_RW = {"Regular": 400, "Medium": 500, "Bold": 700, "ExtraBold": 800}

def anton(s): return ImageFont.truetype(F + "Anton.woff", s)
def raleway(s, w="Regular"): return ImageFont.truetype(F + f"Raleway-{_RW.get(w, 400)}.woff", s)
def comic(s): return ImageFont.truetype(F + "ComicNeue-700.woff", s)

def cover_fit(im, w, h):
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r + 1), int(im.height * r + 1)), Image.LANCZOS)
    x = (im.width - w) // 2; y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))

def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

def pill(c, text):
    d = ImageDraw.Draw(c); f = raleway(24, "Bold"); tw = d.textlength(text, font=f)
    x1 = W - 40 - tw - 36; y1 = 30
    d.rounded_rectangle([x1, y1, W - 40, y1 + 44], radius=22, fill=(0, 0, 0), outline=DGOLD, width=2)
    d.text((x1 + 18, y1 + 8), text, font=f, fill=WHITE)

def logo(c, w=100, x=34, y=24):
    """New MF circle badge (Oct 2026). w is the legacy width hint; badge diameter scales from it."""
    D = int(max(120, w * 1.35))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([x - 6, y - 2, x + D + 6, y + D + 10], fill=(0, 0, 0, 170))
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    c.alpha_composite(LOGO.resize((D, D), Image.LANCZOS), (int(x), int(y)))

def mark(c, h, cx, y):
    """Keyed gold MF mark + wordmark, centered at cx, for dark backgrounds."""
    m = MARK.resize((int(MARK.width * h / MARK.height), h), Image.LANCZOS)
    c.alpha_composite(m, (int(cx - m.width / 2), int(y)))

def full(img):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    c.paste(cover_fit(Image.open(img).convert("RGB"), W, H), (0, 0)); return c

def bubble(c, text, x, y, size=40, maxw=560, tail="down-left"):
    d = ImageDraw.Draw(c); f = comic(size)
    lines = wrap(d, text, f, maxw)
    lh = int(size * 1.18)
    tw = max(d.textlength(l, font=f) for l in lines)
    pw, ph = 34, 22
    bw, bh = tw + 2 * pw, lh * len(lines) + 2 * ph
    x0, y0 = x, y
    if tail == "down-left":
        tx, ty = x0 + bw * 0.28, y0 + bh
        tri = [(tx - 18, ty - 6), (tx + 22, ty - 6), (tx - 22, ty + 38)]
    else:
        tx, ty = x0 + bw * 0.72, y0 + bh
        tri = [(tx - 22, ty - 6), (tx + 18, ty - 6), (tx + 22, ty + 38)]
    d.ellipse([x0 - 8, y0 - 6, x0 + bw + 8, y0 + bh + 6], fill=WHITE, outline=(0, 0, 0), width=4)
    d.polygon(tri, fill=WHITE, outline=(0, 0, 0))
    d.line([tri[0], tri[2]], fill=(0, 0, 0), width=4); d.line([tri[1], tri[2]], fill=(0, 0, 0), width=4)
    d.rectangle([tri[0][0] + 3, tri[0][1] - 8, tri[1][0] - 3, tri[0][1] + 2], fill=WHITE)
    yy = y0 + ph
    for l in lines:
        lw = d.textlength(l, font=f)
        d.text((x0 + (bw - lw) / 2, yy), l, font=f, fill=(0, 0, 0)); yy += lh
    return bw, bh
