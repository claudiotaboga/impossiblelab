"""Shared timeline: narration line starts and per-word timings (15 s reel)."""
import json, re

from config import DUR, FPS, GAP, START, CARD_MIN
LINES = json.load(open("/home/claude/reel/vo/lines.json"))

t = START
for l in LINES:
    l["start"] = round(t, 3); l["end"] = round(t + l["dur"], 3); t = l["end"] + GAP
    words = l["text"].split()
    # weight = letters + pause bonus for punctuation; spread over 92% of the clip
    w = [len(re.sub(r"[^\w]", "", x)) + 2 + (3 if x[-1] in ",.?" else 0) for x in words]
    span = l["dur"] * 0.92; tot = sum(w); acc = l["start"] + l["dur"] * 0.03
    l["words"] = []
    for word, wt in zip(words, w):
        l["words"].append({"w": word, "t": round(acc, 3)}); acc += span * wt / tot

CARD_START = LINES[-1]["end"] + 0.05
assert CARD_START <= DUR - CARD_MIN, (
    f"narration too long: ends at {LINES[-1]['end']:.2f}s, card needs {CARD_MIN}s of {DUR}s; shorten lines")

if __name__ == "__main__":
    for l in LINES: print(l["i"], l["start"], l["end"], l["text"])
    print("card", CARD_START)
