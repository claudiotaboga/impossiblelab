"""Pillow overlays: upscale each render to 1080x1920 and add tag, title, word-by-word captions,
fact chips, footer and THE REAL SCIENCE card. Usage: python3 overlay.py [start end]"""
import sys, os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from timeline import LINES, CARD_START, FPS, DUR

W, H = 1080, 1920
F = "/usr/share/fonts/opentype/inter/"
def font(w, s): return ImageFont.truetype(F + f"Inter-{w}.otf", s)
AMBER = (255, 176, 46); WHITE = (255, 255, 255); INK = (18, 12, 6)

# ---- per-episode content: the only block to change for a new episode ----
EP_NUM = 9
TITLE = ["SWIMMING IN", "OLIVE OIL?"]
FACTS = [  # (start, end, text) — times match the narration lines
    (3.18, 5.53, "OIL 0.91 · YOU ≈ 0.97–0.99 g/cm³"),
    (5.73, 7.89, "IN OIL A 70 kg ADULT WEIGHS ≈ 4–5 kg"),
    (8.09, 10.70, "OLIVE OIL ≈ 84× WATER'S VISCOSITY"),
]
CARD_SUB = "70 kg adult, lungs full · olive oil at 20 °C"
CARD = [("Olive oil vs you", "0.91 vs 0.97–0.99", "g/cm³ · you = tissue 1.058 + 5–6 L of air"),
        ("Your weight in oil", "≈4–5 kg", "in water you float: ≈1–2 kg spare lift"),
        ("Pure body fat", "0.90 g/cm³", "Siri model · ≈1 % rides above 0.911 oil"),
       ]
DISCLAIMER = "Don't try this. Oil can't hold you up; inhaled oil harms lungs."

def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3

def shadow_text(base, xy, text, fnt, fill, anchor="mm", blur=10, alpha=170, stroke=0):
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    d.text((xy[0], xy[1] + 4), text, font=fnt, fill=(0, 0, 0, alpha), anchor=anchor, stroke_width=stroke + 3, stroke_fill=(0, 0, 0, alpha))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))
    ImageDraw.Draw(base).text(xy, text, font=fnt, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=INK)

def pill(base, cx, cy, text, fnt, bg, fg, pad=(28, 14), a=1.0):
    d = ImageDraw.Draw(base); bb = d.textbbox((0, 0), text, font=fnt)
    w, h = bb[2] - bb[0] + 2 * pad[0], bb[3] - bb[1] + 2 * pad[1]
    lay = Image.new("RGBA", base.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    dl.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=h / 2, fill=(*bg, int(235 * a)))
    dl.text((cx, cy), text, font=fnt, fill=(*fg, int(255 * a)), anchor="mm")
    base.alpha_composite(lay)

def wrap(words, fnt, maxw, d):
    rows, cur = [], []
    for w in words:
        test = " ".join(x["w"] for x in cur + [w])
        if cur and d.textlength(test, font=fnt) > maxw: rows.append(cur); cur = [w]
        else: cur.append(w)
    if cur: rows.append(cur)
    return rows

def frame(f):
    t = f / FPS
    src = Image.open(f"frames/{f:04d}.png").convert("RGBA").resize((W, H), Image.LANCZOS)
    img = src
    # top/bottom gradient for legibility
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    for y in range(520): gd.line([(0, y), (W, y)], fill=(0, 0, 0, int(150 * (1 - y / 520) ** 1.6)))
    for y in range(H - 600, H): gd.line([(0, y), (W, y)], fill=(0, 0, 0, int(170 * ((y - (H - 600)) / 600) ** 1.6)))
    img.alpha_composite(g)

    # tag
    pill(img, W / 2, 150, f"THE IMPOSSIBLE LAB  ·  #{EP_NUM:02d}", font("Bold", 34), AMBER, INK)
    # title: big for the hook, then smaller
    k = ease((t - 1.3) / 0.5)
    size = int(84 - 26 * k); y0 = 250 - 10 * k
    tf = font("Black", size)
    for i, row in enumerate(TITLE):
        shadow_text(img, (W / 2, y0 + i * size * 1.12), row, tf, WHITE if i == 0 else AMBER)

    # fact chips
    for (a, b, txt) in FACTS:
        if a <= t <= b:
            al = min(ease((t - a) / 0.25), ease((b - t) / 0.25))
            pill(img, W / 2, 470 + 20 * (1 - al), txt, font("ExtraBold", 40), (20, 60, 160), WHITE, a=al)

    # word-by-word captions
    d = ImageDraw.Draw(img)
    cf = font("Black", 68)
    for l in LINES:
        if l["start"] - 0.05 <= t <= l["end"] + 0.12:
            shown = [w for w in l["words"] if w["t"] <= t] or l["words"][:1]
            rows = wrap(shown, cf, W - 160, d)
            yb = 1330 - (len(rows) - 1) * 40
            for ri, row in enumerate(rows):
                xs = sum(d.textlength(w["w"] + " ", font=cf) for w in row) - d.textlength(" ", font=cf)
                x = W / 2 - xs / 2
                for w in row:
                    active = w is shown[-1]
                    pop = 1 + 0.12 * (1 - ease((t - w["t"]) / 0.12)) if active else 1
                    fnt = font("Black", int(68 * pop))
                    shadow_text(img, (x, yb + ri * 84), w["w"], fnt, AMBER if active else WHITE, anchor="lm", blur=8, stroke=4)
                    x += d.textlength(w["w"] + " ", font=cf)

    # footer
    shadow_text(img, (W / 2, H - 120), "@the.impossible.lab", font("Bold", 36), WHITE)
    shadow_text(img, (W / 2, H - 72), "real science · impossible situations", font("Medium", 28), (235, 225, 210))

    # THE REAL SCIENCE card
    if t >= CARD_START:
        a = ease((t - CARD_START) / 0.35)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        cx0, cy0, cw, ch = 90, 640 + 80 * (1 - a), W - 180, 640
        dl.rounded_rectangle((cx0, cy0, cx0 + cw, cy0 + ch), radius=36, fill=(16, 12, 8, int(232 * a)), outline=(*AMBER, int(255 * a)), width=4)
        dl.text((W / 2, cy0 + 80), "THE REAL SCIENCE", font=font("Black", 58), fill=(*AMBER, int(255 * a)), anchor="mm")
        dl.text((W / 2, cy0 + 138), CARD_SUB, font=font("Medium", 30), fill=(220, 210, 195, int(255 * a)), anchor="mm")
        for i, (lab, val, ref) in enumerate(CARD):
            yy = cy0 + 240 + i * 125
            dl.line((cx0 + 50, yy - 52, cx0 + cw - 50, yy - 52), fill=(255, 255, 255, int(40 * a)), width=2)
            dl.text((cx0 + 60, yy), lab, font=font("SemiBold", 40), fill=(235, 228, 215, int(255 * a)), anchor="lm")
            dl.text((cx0 + cw - 60, yy - 14), val, font=font("Black", 50), fill=(255, 255, 255, int(255 * a)), anchor="rm")
            dl.text((cx0 + cw - 60, yy + 30), ref, font=font("Medium", 26), fill=(200, 190, 175, int(255 * a)), anchor="rm")
        dl.text((W / 2, cy0 + ch - 50), DISCLAIMER, font=font("SemiBold", 30), fill=(255, 120, 90, int(255 * a)), anchor="mm")
        img.alpha_composite(lay)
    return img.convert("RGB")

if __name__ == "__main__":
    a, b = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, int(DUR * FPS) - 1)
    os.makedirs("comp", exist_ok=True)
    for f in range(a, b + 1):
        if os.path.exists(f"frames/{f:04d}.png"):
            frame(f).save(f"comp/{f:04d}.png", compress_level=1)
