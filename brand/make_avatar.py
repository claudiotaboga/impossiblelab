"""Profile picture for The Impossible Lab: a lab flask whose liquid pours upward.
Renders at 4x and downsamples for clean edges. Outputs 1080x1080 (Instagram) and 800x800 (YouTube)."""
from PIL import Image, ImageDraw, ImageFilter
import math, os

S = 4320  # 4x of 1080
C = S / 2
INK = (20, 15, 10); INK2 = (40, 28, 16)
AMBER = (255, 168, 38); AMBER_D = (214, 112, 18); GLOW = (255, 196, 90)
WHITE = (250, 244, 232)

img = Image.new("RGB", (S, S), INK)
# soft radial vignette toward the centre
bg = Image.new("L", (S, S), 0); d = ImageDraw.Draw(bg)
for r in range(int(S * 0.62), 0, -40):
    d.ellipse((C - r, C - r, C + r, C + r), fill=int(70 * (1 - r / (S * 0.62))))
img = Image.composite(Image.new("RGB", (S, S), INK2), img, bg)
d = ImageDraw.Draw(img)

# glow behind the flask
glow = Image.new("RGBA", (S, S), (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
g.ellipse((C - 1150, C - 700, C + 1150, C + 1500), fill=(255, 150, 30, 70))
img.paste(glow.filter(ImageFilter.GaussianBlur(260)), (0, 0), glow.filter(ImageFilter.GaussianBlur(260)))
d = ImageDraw.Draw(img)

# flask geometry (conical Erlenmeyer), tilted so the mouth points up-right
neck_w, neck_h = 420, 620
base_w, body_h = 1900, 1500
cx, base_y = C - 60, C + 1420
top_y = base_y - body_h
pts_body = [(cx - neck_w / 2, top_y), (cx + neck_w / 2, top_y),
            (cx + base_w / 2, base_y - 140), (cx + base_w / 2 - 140, base_y),
            (cx - base_w / 2 + 140, base_y), (cx - base_w / 2, base_y - 140)]
neck = [(cx - neck_w / 2, top_y - neck_h), (cx + neck_w / 2, top_y - neck_h),
        (cx + neck_w / 2, top_y), (cx - neck_w / 2, top_y)]

# liquid fills the lower body
liq_y = base_y - 760
def x_at(y, side):
    t = (y - top_y) / (base_y - 140 - top_y)
    w = neck_w / 2 + (base_w / 2 - neck_w / 2) * t
    return cx + side * w
liquid = [(x_at(liq_y, -1) + 40, liq_y), (x_at(liq_y, 1) - 40, liq_y),
          (cx + base_w / 2 - 50, base_y - 160), (cx + base_w / 2 - 170, base_y - 60),
          (cx - base_w / 2 + 170, base_y - 60), (cx - base_w / 2 + 50, base_y - 160)]
d.polygon(liquid, fill=AMBER)
# liquid surface highlight
d.line([(x_at(liq_y, -1) + 60, liq_y + 8), (x_at(liq_y, 1) - 60, liq_y + 8)], fill=GLOW, width=60)

# the impossible stream: liquid rising out of the neck in a curving column, breaking into drops
stream = []
for i in range(0, 101):
    u = i / 100
    y = top_y - neck_h + 40 - u * 920
    x = cx + math.sin(u * 2.6) * 300 * u
    w = 150 * (1 - 0.55 * u)
    stream.append((x, y, w))
for (x, y, w) in stream[:80]:
    d.ellipse((x - w, y - w, x + w, y + w), fill=AMBER)
# column inside the neck connecting to the liquid
d.rectangle((cx - 150, top_y - neck_h + 40, cx + 150, liq_y + 10), fill=AMBER)
# drops breaking away upward
for (u, r) in [(0.86, 105), (0.95, 80), (1.04, 58), (1.12, 40)]:
    y = top_y - neck_h + 40 - u * 920
    x = cx + math.sin(u * 2.6) * 300 * u + (u - 0.8) * 200
    d.ellipse((x - r, y - r * 1.15, x + r, y + r * 1.15), fill=AMBER)

# glass outline on top (white, thick, rounded joins)
LW = 120
def outline(poly):
    for i in range(len(poly) - 1):
        a, b = poly[i], poly[i + 1]
        d.line([a, b], fill=WHITE, width=LW)
        d.ellipse((a[0] - LW / 2, a[1] - LW / 2, a[0] + LW / 2, a[1] + LW / 2), fill=WHITE)
outline([(cx + neck_w / 2, top_y - neck_h), pts_body[1], pts_body[2], pts_body[3], pts_body[4], pts_body[5], pts_body[0], (cx - neck_w / 2, top_y - neck_h)])
# lip of the neck
d.rounded_rectangle((cx - neck_w / 2 - 110, top_y - neck_h - 70, cx + neck_w / 2 + 110, top_y - neck_h + 70), radius=70, fill=WHITE)
# re-draw the stream over the lip so it clearly pours out of the mouth
for (x, y, w) in stream[2:80]:
    d.ellipse((x - w, y - w, x + w, y + w), fill=AMBER)
# bubbles in the liquid
for (bx, by, br) in [(-420, 260, 70), (-160, 470, 50), (300, 330, 85), (560, 520, 45), (80, 600, 38)]:
    d.ellipse((cx + bx - br, liq_y + by - br, cx + bx + br, liq_y + by + br), outline=AMBER_D, width=28)

out = img.resize((1080, 1080), Image.LANCZOS)
os.makedirs("brand", exist_ok=True)
out.save("brand/avatar_1080.png")
img.resize((800, 800), Image.LANCZOS).save("brand/avatar_800_youtube.png")

# preview: how it looks in Instagram's circle at feed size and large
prev = Image.new("RGB", (900, 420), (255, 255, 255))
for size, x in [(320, 40), (110, 420), (56, 600), (32, 720)]:
    a = out.resize((size, size), Image.LANCZOS)
    m = Image.new("L", (size, size), 0); ImageDraw.Draw(m).ellipse((0, 0, size - 1, size - 1), fill=255)
    prev.paste(a, (x, 210 - size // 2), m)
prev.save("brand/avatar_preview.png")
print("ok")
