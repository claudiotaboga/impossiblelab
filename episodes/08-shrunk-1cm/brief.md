# TIL-08 brief: Shrunk to 1 cm tall

Built 13 Nov 2026 (daily production run), for the 14 Nov 16:00 EET slot. Experiment **E5, reel 1 of 3**.

## 1. Performance update (data: Make 8451991/8451995 snapshot 13 Nov 13:15 EET)
- **What the evidence shows:** Instagram reach is decided in the first ~12–20 h and then freezes. Only the two premises with stakes for the viewer's own body or food broke out: mercury pool 1,146 accounts, pasta on Mars 517; every other reel sits at 111–137 (TIL-06 marathon 117 at 21 h, 0.86× the 136 baseline). Retention is flat across formats: hook hold 58.6–71.9 % (median 62.6 %), watch ratio 59–80 %. Engagement is zero (0 shares, 0 saves, 0 comments on 3,207 IG views).
- **What is uncertain:** n = 6; topic is confounded with timing (TIL-05 was the first on-time 16:00 post). YouTube has stalled channel-wide (TIL-06: 5 views at 21 h vs a 24 h median of 1,118); cause unknown (upload settings in Make are public / not made for kids).
- **What changes:** topic selection only (E5: a premise about *your* body). Caption v2 (no question prompt, no "follow for more") goes live at the same time as a minor confound. Format, length (15 s / voice 1.10), cold open and 16:00 slot unchanged.

## 2. Evidence table
| Observation | Evidence | Creative decision |
|---|---|---|
| Body/food premises out-reach everything else | IG reach: mercury 1,146, pasta 517 vs 111–137 for the rest | Premise puts stakes on the viewer's own body (you, shrunk) |
| Peer over-performers are about the viewer's body, mind or food | zackdfilms / kurzgesagt / asapscience over-performers (CAMPAIGN_LOG.md, 13 Nov) | "You" in every line; heat, falls and water all act on your body |
| Hook hold stuck at ~60–64 % with claim hooks | TIL-03..06 hook hold 58.6–63.9 % | Hook = a proof image, not just a claim: the balance tips toward a drop smaller than you in the first second, with on-object labels (works without sound) |
| Zero comments with a yes/no prompt | E2: 0 comments on ~1,000 IG views | Caption v2: one share line naming a person type, one series line, disclaimer |
| Labels crop at frame edges in follow-cams | TIL-07 QA | All labels sit in the static balance shots; framing checked at 486×864 |

## 3. Concept, audience, reason to share
- **Concept:** you, shrunk 175× to 1 cm. Physics flips: falls stop hurting, heat drains away, and water becomes the real danger. Proof object: a lab balance where one raindrop outweighs you, and at the end the water clinging to you balances you exactly.
- **Audience:** 16–35 science-curious viewers who grew up on "Honey, I Shrunk…" style what-ifs and Haldane-style scaling facts; people who argue about "what if I were ant-sized".
- **Reason to send it:** "you'd be in danger from a raindrop" is a one-line fact people forward to the friend who always says they'd want to be tiny (or who is always cold).

## 4. Five hooks (first 1–2 s)
1. **"Big raindrops weigh more than you."** + balance tipping toward a 5 mm drop, figure lifted on the other pan. ← **winner**
2. "Falling off a wall? Harmless." + figure stepping off a garden wall (risk: reads as a dare; safety)
3. "You'd freeze in a warm room." (not verifiable as stated; heat-loss ratio only)
4. "Rain is your new enemy." + rain from below (vague, no number)
5. "You weigh less than a raindrop." + close-up of figure next to a drop (subject-first variant of #1)

**Why #1:** a counter-intuitive comparison that is visually *proved* in the same second (the smaller object wins the balance), concrete, on the viewer's body, no greeting or question, readable without sound thanks to the in-scene labels "YOU 13 mg / DROP 65 mg". The ending (water = you, balance level) pays it off and loops to the same framing.

## 5. Timestamped script (15.0 s, Kokoro af_heart speed 1.10, 44 words)
| t (s) | Visual | Speech | On-screen text | Editing | Audio |
|---|---|---|---|---|---|
| 0.0–1.8 | Lab balance on a patio stone, grass blades towering behind; the right pan with a 5 mm raindrop sinks, the 1 cm figure rises on the left pan | "Big raindrops weigh more than you." | Title "SHRUNK TO / 1 CM TALL?"; in-scene "YOU 13 mg", "DROP 65 mg" | Cold open, slow push-in | Creak + drop plink |
| 1.8–3.4 | Figure shrinks from 3.2× to 1 cm on a ruler; amber "1 cm" bracket appears | "Now shrink to one centimetre." | Chip 1: YOU ≈ 13 mg · 5 mm RAINDROP ≈ 65 mg | Hard cut, slow pull-back | Descending whoosh |
| 3.4–5.9 | Figure on top of a garden wall steps off; follow-cam as it drifts down arms out; lands softly in the soil, stands up | "Falls barely hurt: you'd land at running pace." | Chip 2: FALL SPEED ≈ 4 m/s (FULL SIZE ≈ 53 m/s) | Cut → follow-cam | Soft whoosh, tiny thud |
| 5.9–8.6 | Close-up: figure shivering, orange heat rings radiate away | "But you'd lose heat nearly two hundred times faster." | Chip 3: HEAT LOSS PER kg ≈ 175× FASTER | Slow push-in | Falling shimmer tone |
| 8.6–10.0 | Low angle: giant raindrops falling around the tiny figure | "And the real danger?" | — | Cut, music drops out | Rain plinks |
| 10.0–10.7 | A drop lands: the figure is wrapped in a water shell, splash beads fly out | "Getting wet." | — | Cut on impact | Gloop |
| 10.7–12.9 | Back to the balance: "YOU 13 mg" vs "WATER 13 mg"; the beam settles level | "The water clinging to you weighs as much as you." | in-scene labels | Cut to the hook set-up (loop) | Creak, music returns |
| 12.9–15.0 | THE REAL SCIENCE card over the balance; last ~1 s back on the hook framing | — | Card rows + red disclaimer | Card fade-in | Thud |

## 6. Scene / generation notes (pipeline)
- `pipeline/reference/scene_ep08.py`: Blender primitives, 1 unit = 5.71 mm (mannequin 1.75 units = 1 cm). Drop radius 0.438 units (5 mm), water blob for the finale 13 mg (radius 0.256 units). Water = Principled transmission 1.0, IOR 1.33 (transmission bounces 4). Separate sets: balance (origin), ruler (x = 40), garden wall 26 units high (x = −60), heat/rain spot (26, −22).
- Timing from real line starts (`timeline.py`), beats in `beats.json`. The fall is shown at a readable pace (1.45 s on screen); the chip gives the physical terminal speed.
- `overlay.py` per-episode block: title, 3 chips, card, disclaimer. `audio_mix.py` SFX: creak/plink, shrink whoosh, soft fall, shimmer, rain, gloop, creak.

## 7. Caption, cover, hashtags
- **Cover headline:** SHRUNK TO 1 CM TALL? (title at t = 0 over the balance tipping toward the drop)
- **Caption (v2):** see `meta.json` → hook line, four science lines, share line ("Send this to the friend who's always cold."), series line, "⚠️ Don't try this." line, 8 hashtags.
- **YouTube title:** What if you were shrunk to 1 cm tall? (38 chars + " #Shorts")

## 8. Two alternative openings (future tests; not produced)
- **A (subject-first):** "You'd weigh less than a raindrop." over a tight close-up of the figure beside a drop as big as its torso, then the balance.
- **B (impact-first):** open on the drop engulfing the figure (t = 10 s image) with "Rain could trap you." then rewind to the balance.

## 9. Experiment record
- **Experiment:** E5 (topic selection: stakes on the viewer's own body or an everyday object/food), reel 1 of 3 (TIL-08..10).
- **Hypothesis:** a body-stakes premise lifts Instagram reach at 24 h to ≥ 2× the baseline (≥ 272 accounts).
- **One variable:** topic selection rule (format, length, voice, cold open, slot unchanged; caption v2 noted as a minor confound).
- **Primary metric:** IG accounts reached at ~24 h. **Baseline:** 136 accounts (median 24 h reach TIL-01..05). Secondary: hook hold vs median 62.6 %, shares + saves per 1,000 views (baseline 0).
- **Checkpoints:** 24 h = 15 Nov 16:00 EET, 72 h = 17 Nov 16:00, 7 d = 21 Nov 16:00. Verdict on E5 after TIL-10 at 72 h.
