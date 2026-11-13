"""Mix narration + an original procedural lo-fi music bed + synthesized SFX into mix.wav (DUR s, 48 kHz)."""
import numpy as np, soundfile as sf
from scipy.signal import resample_poly, butter, sosfilt
from timeline import LINES, CARD_START, DUR

SR = 48000; N = int(DUR * SR); rng = np.random.default_rng(3)
t_all = np.arange(N) / SR
def at(s): return int(s * SR)
def env(n, a, r):  # attack/release envelope in seconds
    e = np.ones(n); na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na) if na else 1; e[-nr:] *= np.linspace(1, 0, nr) ** 2 if nr else 1; return e
def lp(x, f): return sosfilt(butter(4, f, "low", fs=SR, output="sos"), x)
def hp(x, f): return sosfilt(butter(4, f, "high", fs=SR, output="sos"), x)
def bp(x, lo, hi): return sosfilt(butter(4, [lo, hi], "band", fs=SR, output="sos"), x)
def put(buf, x, s, g=1.0):
    i = at(s); x = x[: max(0, N - i)]; buf[i:i + len(x)] += x * g

# ---- narration ----
vo = np.zeros(N)
for l in LINES:
    x, sr = sf.read(l["file"])
    if sr != SR: x = resample_poly(x, SR, sr)
    put(vo, x, l["start"])

# ---- music: 90 BPM lo-fi, Dm9 - G13 - Cmaj9 - A7(b13) ----
bpm = 90; beat = 60 / bpm; bar = 4 * beat
chords = [[50, 57, 60, 64, 65], [43, 53, 57, 59, 64], [48, 55, 59, 62, 64], [45, 55, 59, 61, 65]]
mtof = lambda m: 440 * 2 ** ((m - 69) / 12)
music = np.zeros(N)
def keys(freq, dur):
    n = int(dur * SR); tt = np.arange(n) / SR
    x = sum(a * np.sin(2 * np.pi * freq * h * tt) for h, a in [(1, 1), (2, 0.35), (3, 0.12)])
    return x * np.exp(-tt * 1.6) * (1 + 0.15 * np.sin(2 * np.pi * 4.5 * tt)) * env(n, 0.01, 0.2)
nb = int(DUR / bar) + 1
for b in range(nb):
    ch = chords[b % 4]; s = b * bar
    for k, m in enumerate(ch[1:]): put(music, keys(mtof(m + 12), bar * 0.95), s + 0.012 * k, 0.07)
    bass = ch[0]
    for k, (off, ln) in enumerate([(0, 1.4), (1.5, 0.45), (2.0, 1.4), (3.5, 0.45)]):
        n = int(ln * beat * SR); tt = np.arange(n) / SR
        put(music, np.sin(2 * np.pi * mtof(bass - 12 + (7 if k == 3 else 0)) * tt) * env(n, 0.005, 0.08), s + off * beat, 0.28)
    for q in range(8):  # brushed hats with swing
        n = int(0.09 * SR); hat = hp(rng.standard_normal(n), 6000) * np.exp(-np.arange(n) / SR * 40)
        put(music, hat, s + q * beat / 2 + (0.06 if q % 2 else 0), 0.05 if q % 2 else 0.08)
    for q in (0, 2.5):  # soft kick
        n = int(0.25 * SR); tt = np.arange(n) / SR
        put(music, np.sin(2 * np.pi * (50 + 60 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 14), s + q * beat, 0.5)
    for q in (1, 3):  # rim
        n = int(0.06 * SR); put(music, bp(rng.standard_normal(n), 1500, 4000) * np.exp(-np.arange(n) / SR * 60), s + q * beat, 0.12)
music = lp(music, 7000)
# arrangement: full until the twist, drop out, light return for the payoff
gain = np.ones(N)
d0, d1 = at(LINES[-2]["start"] - 0.05), at(LINES[-1]["start"])  # twist setup = second-to-last line
gain[d0:d0 + at(0.08)] = np.linspace(1, 0, at(0.08)); gain[d0 + at(0.08):d1] = 0
gain[d1:] = np.clip(np.linspace(0, 0.8, N - d1) * 4, 0, 0.8)
music *= gain
# sidechain-style ducking under the voice
venv = np.convolve(np.abs(vo), np.ones(2400) / 2400, mode="same")
duck = 1 - 0.55 * np.clip(venv / (venv.max() * 0.25), 0, 1)
music *= np.convolve(duck, np.ones(4800) / 4800, mode="same")

# ---- SFX ----
sfx = np.zeros(N)
def whoosh(dur, lo=300, hi=3000, rise=True):
    n = int(dur * SR); x = rng.standard_normal(n); out = np.zeros(n); seg = 2400
    for i in range(0, n, seg):
        u = i / n; f = lo + (hi - lo) * (u if rise else 1 - u)
        out[i:i + seg] = bp(x[i:i + seg + 0], max(f * 0.7, 40), min(f * 1.4, 20000))[: len(out[i:i + seg])]
    return out * np.sin(np.linspace(0, np.pi, n)) ** 1.5
def thud(dur=0.5, f0=70):
    n = int(dur * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * (f0 + 80 * np.exp(-tt * 25)) * tt) * np.exp(-tt * 9)
def gloop(dur=0.9):  # thick, low-passed splash
    n = int(dur * SR); tt = np.arange(n) / SR
    x = lp(rng.standard_normal(n), 900) * np.exp(-tt * 5) * 1.8
    bub = sum(np.sin(2 * np.pi * (180 + 90 * k) * (1 + 0.6 * tt) * tt) * np.exp(-((tt - 0.08 * k - 0.05) * 30) ** 2) for k in range(6))
    return x + bub * 0.25
def squeak(dur=0.22, f=2600):
    n = int(dur * SR); tt = np.arange(n) / SR
    fm = f * (1 + 0.25 * np.sin(2 * np.pi * 9 * tt))
    x = np.sin(2 * np.pi * np.cumsum(fm) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(fm) / SR)
    return x * np.sin(np.linspace(0, np.pi, n)) ** 2 * (1 + 0.4 * np.sin(2 * np.pi * 45 * tt))
def whoomph(dur=1.0):
    n = int(dur * SR); tt = np.arange(n) / SR
    return lp(rng.standard_normal(n), 500) * np.sin(np.linspace(0, np.pi, n)) ** 0.7 * 1.6
import json as _json
B = _json.load(open("/home/claude/reel/beats.json"))
def bubbling(dur):  # rolling boil: dense random blips
    n = int(dur * SR); out = np.zeros(n)
    for k in range(int(dur * 38)):
        i = rng.integers(0, max(1, n - 4000)); f = rng.uniform(250, 900); m = 3000; tt = np.arange(m) / SR
        out[i:i + m] += np.sin(2 * np.pi * f * (1 + 2.5 * tt) * tt) * np.exp(-tt * 60) * rng.uniform(0.3, 1)
    return lp(out, 2500)
def tick(dur=0.05):
    n = int(dur * SR); tt = np.arange(n) / SR; return np.sin(2 * np.pi * 2400 * tt) * np.exp(-tt * 120)
def clang(dur=0.6):  # lid on a steel pot
    n = int(dur * SR); tt = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt * (9 + k * 4)) for k, f in enumerate([420, 1130, 1870, 2650])) * 0.4 + thud(dur, 90) * 0.6
def whistle(dur):  # pressure-cooker valve hiss + whistle
    n = int(dur * SR); tt = np.arange(n) / SR
    x = bp(rng.standard_normal(n), 3000, 9000) * 0.6 + np.sin(2 * np.pi * (1650 + 30 * np.sin(2 * np.pi * 6 * tt)) * tt) * 0.35
    return x * np.clip(tt / 0.15, 0, 1) * np.clip((dur - tt) / 0.1, 0, 1)
def plink(f=1400, dur=0.35):  # single water drop
    n = int(dur * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * f * (1 + 0.8 * tt * 12) * tt) * np.exp(-tt * 18)
def creak(dur=0.4):  # balance beam tipping
    n = int(dur * SR); tt = np.arange(n) / SR
    return bp(rng.standard_normal(n), 600, 1800) * (0.5 + 0.5 * np.sin(2 * np.pi * 23 * tt)) * np.sin(np.linspace(0, np.pi, n))
def shimmer(dur):  # heat leaving: soft descending tone
    n = int(dur * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * (900 - 300 * tt / dur) * tt) * 0.4 * np.sin(np.linspace(0, np.pi, n)) ** 2
def rain(dur):
    n = int(dur * SR); out = bp(rng.standard_normal(n), 2000, 8000) * 0.25
    for k in range(int(dur * 25)):
        i = rng.integers(0, max(1, n - 8000)); x = plink(rng.uniform(900, 2200), 0.15); out[i:i + len(x)] += x * rng.uniform(0.1, 0.4)
    return out * np.clip(np.arange(n) / SR / 0.2, 0, 1)
put(sfx, creak(), 0.05, 0.35); put(sfx, plink(1200), 0.25, 0.35)            # hook: drop lands on the pan, beam tips
put(sfx, whoosh(1.0, 2400, 600, False), LINES[1]["start"] + 0.05, 0.18)    # shrinking
put(sfx, whoosh(1.5, 300, 900, True), B["t_step"], 0.18)                    # soft fall
put(sfx, thud(0.25, 140), B["t_land"], 0.25)                                # tiny, harmless landing
put(sfx, shimmer(2.2), LINES[3]["start"] + 0.1, 0.25)                       # heat radiating away
put(sfx, rain(LINES[6]["start"] - LINES[4]["start"]), LINES[4]["start"], 0.45)
put(sfx, gloop(0.7), B["t_hit"], 0.6)                                       # the big drop engulfs you
put(sfx, creak(0.6), LINES[6]["start"] + 0.2, 0.3)                          # balance settles level
for t_cut in B["cuts"]:
    put(sfx, whoosh(0.35, 1800, 500, False), t_cut - 0.15, 0.10)
put(sfx, thud(0.4, 60), CARD_START, 0.6); put(sfx, whoosh(0.3, 800, 3000), CARD_START - 0.25, 0.2)
amb = lp(rng.standard_normal(N), 300) * 0.010

mix = vo * 1.0 + music * 0.55 + sfx * 0.55 + amb
fade = at(0.15); mix[-fade:] *= np.linspace(1, 0, fade)
mix /= np.max(np.abs(mix)) * 1.12
sf.write("mix.wav", np.stack([mix, mix], 1), SR, subtype="PCM_24")
print("mix.wav", len(mix) / SR, "s, peak", np.abs(mix).max())
