# TIL-09 brief: Swimming in a pool of olive oil

Built 14 Nov 2026 (daily production run), for the 15 Nov 16:00 EET slot. Experiment **E5, reel 2 of 3**.

## 1. Performance update (data: Make 8451991/8451995 snapshot 14 Nov 13:12 EET)
- **What the evidence shows:** total 10,313 views (IG 3,385 + YT 6,928). IG reach is decided in the first ~12–20 h, then freezes. The two body/food premises still lead IG reach by far (mercury pool 1,146, pasta on Mars 517); the last two non-body premises sit below the 136-account baseline (marathon 117, Moon basketball 125 at 21 h). TIL-07 has the weakest retention so far (hook hold 55.2 %, watch ratio 52 %). YouTube is healthy again for new uploads (TIL-07: 894 YT views at 19 h); only TIL-06 is stuck (8 views at 45 h). Engagement is still zero (0 shares, 0 saves, 0 comments on 3,385 IG views); followers IG 1 / YT 3, unchanged.
- **What is uncertain:** n = 7; topic is confounded with posting time (TIL-05 was the first on-time post) and caption v2 (from TIL-08). TIL-08 (E5 reel 1) publishes today at 16:00, so E5 has no data yet.
- **What changes:** nothing new. TIL-09 = E5 reel 2: a premise with stakes on the viewer's own body (you can't float) using an everyday kitchen product. Same 15 s / 1.10 voice, cold open on a proof image, caption v2, 16:00.

## 2. Evidence table
| Observation | Evidence | Creative decision |
|---|---|---|
| Body/food premises out-reach the rest on IG | reach: mercury 1,146, pasta 517 vs 111–137 for the other five | Premise: your body in a kitchen staple (olive oil) |
| The best reel ever (mercury) was a "pool you can't …" buoyancy claim | TIL-02: 1,146 accounts, hook hold 67.5 % | Same family, inverted: the pool you can't float in |
| Hook hold is weakest on space premises with an empty/action open | TIL-07 55.2 % (lowest), TIL-06 63.9 % | t = 0 is a side-by-side proof: two tanks, WATER/FLOATS vs OLIVE OIL/SINKS, the person visibly sinking (readable without sound) |
| Zero comments with question prompts; caption v2 running | E2 stopped 13 Nov | Caption v2: one share line naming a person type, series line, disclaimer, 8 hashtags |
| Labels crop or hide under captions in wide shots | TIL-07/08 QA | In-scene labels sit inside the tanks at mid-frame height; numbers on chips/card |

## 3. Concept, audience, reason to share
- **Concept:** fill a pool with olive oil and jump in. Oil (0.91) is lighter than your body even with a full breath (0.97–0.99), so you sink with an apparent weight of ~4–5 kg; the oil is 84× more viscous, so kicking up is hard work. The twist: the only thing that floats is pure fat, by 11 mm on a 1 m block.
- **Audience:** 16–35 science-curious viewers and home cooks; people who know the "you float better in the Dead Sea" fact and will enjoy its opposite.
- **Reason to send it:** a surprising, one-line fact about a product in every kitchen ("you'd sink in olive oil"), easy to forward to the friend who pours olive oil on everything.

## 4. Five hooks (first 1–2 s)
1. **"You'd sink in olive oil."** + two tanks side by side, WATER/FLOATS vs OLIVE OIL/SINKS, the person in the oil tank going down. ← **winner**
2. "The pool you can't float in." + golden pool, person going under (repeats TIL-02's wording too closely)
3. "Even a full breath won't save you." (negative framing without the object; unclear without sound)
4. "Olive oil beats your lungs." (vague)
5. Image only: a block of fat bobbing at the surface while the person lies on the pool floor (strong image, but the payoff would be spent in second 1)

**Why #1:** a five-word counter-intuitive claim about the viewer's own body and an everyday product, proved in the same frame by a side-by-side control (water vs oil), readable without sound through the in-scene labels. The ending (fat floats, barely) pays off the hook and the last second returns to the two tanks (loop).

## 5. Timestamped script (15.0 s, Kokoro af_heart speed 1.10, 47 words)
| t (s) | Visual | Speech | On-screen text | Editing | Audio |
|---|---|---|---|---|---|
| 0.0–1.6 | Two cutaway tanks: blue WATER (person floats, head out) and golden OLIVE OIL (person sinking, arms up) | "You'd sink in olive oil." | Title "SWIMMING IN / OLIVE OIL?"; in-scene WATER · FLOATS / OLIVE OIL · SINKS | Cold open, slow push-in | Gloop + slow bubbles |
| 1.6–3.2 | 5 m cutaway pool of oil, person jumps from the deck, golden splash | "Jump into a pool full of it." | — | Hard cut, wide | Whoosh, heavy gloop |
| 3.2–5.6 | Medium shot in the oil: chest inflates (full breath), still drifting down | "Oil is lighter than you, even with a full breath." | Chip 1: OIL 0.91 · YOU ≈ 0.97–0.99 g/cm³ | Cut, slow push | Inhale whoosh |
| 5.7–7.9 | Person lands on the pool floor; red down-arrow "≈4 kg" | "You'd weigh about four kilos and keep sinking." | Chip 2: IN OIL A 70 kg ADULT WEIGHS ≈ 4–5 kg | Cut, lower angle | Thud |
| 8.1–10.7 | Person kicks upward at an angle, slow; glowing drag trails behind the feet | "And it's over eighty times thicker. Every kick drags." | Chip 3: OLIVE OIL ≈ 84× WATER'S VISCOSITY | Follow-cam | Muffled kick whooshes |
| 10.9–11.8 | Wide: a 1 m block drops into the pool and bobs; person sinks back; back wall label OLIVE OIL 0.91 | "What still floats?" | in-scene BODY FAT 0.90 | Cut, music drops | Gloop |
| 12.0–14.4 | Close on the block: top flush with the surface, amber edge = the 11 mm sliver, label ONLY 11 mm ABOVE | "Pure body fat. Barely." | in-scene labels; then THE REAL SCIENCE card | Cut, slow push | Tick, card thud |
| 14.4–15.0 | Back to the two tanks (hook framing) | — | Card + red disclaimer | Loop | — |

## 6. Scene / generation notes (pipeline)
- `pipeline/reference/scene_ep09.py`: Blender primitives in metres. Liquids are a Transparent BSDF (tinted) mixed with a glossy Principled by facing ratio, with shadow visibility off: no refraction noise at 8 samples and the person stays lit inside the liquid. Cutaway tanks (tiled floor/back/sides, open front).
- Sets: story pool at the origin (5 × 2.5 m, oil level 2.3 m, deck on the right), hook tanks at x = 30 (1.5 m wide, liquid level 2.5 m). Fat block 1 m, top 11.3 mm above the oil (1 − 0.9007/0.911).
- Timing from real line starts (`timeline.py`), beats in `beats.json` (entry, floor, kick start, fat-in). `overlay.py` per-episode block: title, 3 chips, card, disclaimer. `audio_mix.py` SFX: gloops, bubbles, jump/breath whooshes, floor thud, kick whooshes, tick.

## 7. Caption, cover, hashtags
- **Cover headline:** SWIMMING IN OLIVE OIL? (title at t = 0 over the two tanks)
- **Caption (v2):** see `meta.json`: hook line, four science lines, share line ("Send this to the friend who pours olive oil on everything."), series line, "⚠️ Don't try this." line, 8 hashtags.
- **YouTube title:** What if you swam in a pool of olive oil? (40 chars + " #Shorts")

## 8. Two alternative openings (future tests; not produced)
- **A (E9, body part first):** extreme close-up of a face going under the golden surface, cheeks puffed, "Even a full breath won't save you."
- **B (object-first / E6 title):** the fat block bobbing at the surface with the person on the floor below, title "THE POOL ONLY FAT FLOATS IN".

## 9. Experiment record
- **Experiment:** E5 (topic selection: stakes on the viewer's own body or an everyday object/food), reel 2 of 3 (TIL-08..10).
- **Hypothesis:** body/food premises reach more accounts on IG than space/abstract premises at the same slot and format.
- **One variable:** topic selection rule (format, length 15 s / 1.10, cold open, 16:00 slot unchanged; caption v2 is a logged minor confound since TIL-08).
- **Primary metric:** IG reach at 24 h vs baseline 136 accounts (median TIL-01..05). Secondary: hook hold vs median 61.3 %.
- **Checkpoint:** 24 h after posting (16 Nov 16:00 EET); E5 review 18 Nov after TIL-10's 24 h.
