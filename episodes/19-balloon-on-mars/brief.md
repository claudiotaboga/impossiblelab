# TIL-19 brief — A balloon on Mars (E17 cascade middle, reel 2)

Built 24 Nov 2026 (production run 13:12 EET) for the 25 Nov 16:00 EET slot. Binding premise: TIL-18 end card "TOMORROW: A BALLOON ON MARS".

## Performance update
- Evidence used: latest capture in store 250779 = 23 Nov 20:31–20:32 EET (no Tuesday stats check under the weekly cadence; today's fresh capture is the 16:00 post-publish confirmation run, logged in STRATEGY.md).
- What it shows: E5 reels cluster at ~1.1 k IG accounts at 24 h (6 of 9); the only reels that left that tier had exceptional retention (TIL-09 hook 72 % / watch 74 %; TIL-15 watch 84 % with a cascade middle). TIL-16 (Everest egg) 1,155 accounts / hook 62.3 % / watch 58 % at 27 h.
- Uncertain: whether the cascade middle (E17) is what lifted TIL-15's completion — n = 1; TIL-18 (reel 1) goes live 24 Nov 16:00, no data yet. Shares still 0 on every reel.
- What changes: nothing beyond the instruction in force (22 Nov 13:20): TIL-19 is E17 reel 2, same variable as TIL-18.

## Evidence → decision
| Observation | Evidence | Creative decision |
|---|---|---|
| Cascade middle lifted completion | TIL-15 watch 84 % (best of 16) with mug → plate → book reacting 3–10 s | New sealed object reacts every ~0.7–1 s from 4.2 to 10.7 s: air dots vanish 4.2 → balloon swells 4.5 → marshmallows 6.1 → snack bag 6.8 → glove 7.5 → balloon ×2 → ×20 8.5–10.6 → tear lines 10.7 → pop 11.6 → speed bars 11.8 |
| Object visibly reacting at t = 0 holds best | TIL-08/09 63–72 % vs TIL-11 condition-only 53 % (E13) | Frame 0: EARTH vs MARS balloons side by side; the Mars one swells from 0.08 s and pops at 1.0 s |
| E5 body/food/everyday-object rule | E5 PASS (19 Nov) | Party balloon, snacks, rubber glove — objects everyone owns |
| Follow invite (house rule) | Claudio 20 Nov | Pill 5.0–8.2 s, end card, caption line |

## Concept
- Audience: curious 16–35 viewers who like "what if" space physics; parents/teachers who do the balloon-in-a-vacuum demo.
- Reason to send it: "you know the balloon in the vacuum jar trick? On Mars it happens to everything in your bag" — send to the friend who does science demos / the one who always brings balloons to parties.

## Five hooks (first 1–2 s)
1. **Image: EARTH balloon calm, MARS balloon swelling then popping at 1.0 s + line "This balloon pops on its own." — WINNER** (physical consequence at t = 0 beside an Earth control = E13 pattern; the claim sounds wrong; pop is a sound + motion payoff inside 1 s).
2. Line "No pin. Still pops." over the Mars balloon bursting.
3. Image: a snack bag ballooning until the seams strain; line "Your snacks inflate on Mars."
4. Image: a rubber glove inflating by itself on a Mars table; line "This glove fills itself."
5. Line "Mars bursts balloons for free." over a shower of red latex shreds.
Why 1: the most universal object, the clearest Earth-vs-Mars contrast, and the pop lands before most viewers can swipe.

## Script (15.0 s, Kokoro af_heart 1.10; line starts from timeline.py)
| t (s) | Visuals | Speech | On-screen text | Editing / audio |
|---|---|---|---|---|
| 0.0–1.6 | Hook set: EARTH (blue tiles, 1 BAR) vs MARS (rust wall, 0.006 BAR) balloons; Mars one swells, pops 1.0 s, shreds | "This balloon pops on its own." | Title BALLOON / ON MARS? | stretch creak → pop |
| 1.8–3.6 | Cut to Mars surface; fresh tied balloon set on a table beside marshmallows, a sealed snack bag, a rubber glove | "Same balloon, carried to Mars." | — | whoosh, thud |
| 3.75–5.7 | Air dots vanish 4.2 s; balloon starts swelling 4.5 s | "Its air is under one percent of ours." | chip MARS AIR: ≈0.6 % OF EARTH'S; AIR: MARS (0.6 %) | shimmer |
| 5.9–8.4 | Marshmallows puff 6.1 → snack bag bulges 6.8 → glove fingers inflate 7.5 | "Sealed things swell: snacks, bags, gloves." | FOLLOW pill 5.0–8.2; SNACKS label | three soft puffs |
| 8.6–10.5 | Balloon swells ×2 → ×20, latex lightens; labels NEEDS ×100+ / VOLUME ×N | "It tries to grow over a hundred times." | chip SEALED AIR WANTS ×100+ VOLUME | straining creak |
| 10.65–11.3 | Close-up: glowing tear lines race across the balloon | "And the rip?" | — | two cracks |
| 11.5–13.3 | Pop at 11.6 s, shreds fly (Mars gravity); bars race RIP 570 vs MARS SOUND 240 m/s | "Over twice as fast as sound there." | chip RIP ≈570 m/s · MARS SOUND ≈240 m/s | pop, whoosh |
| 13.4–15.0 | THE REAL SCIENCE card over hook framing (Mars balloon swelling again = loop); TOMORROW: A CANDLE IN SPACE; FOLLOW @the.impossible.lab | — | card + red disclaimer | thud |

## Scene notes (pipeline/reference/scene_ep19.py)
Hook set at x = 0 (two tied balloons on weights, EARTH/MARS walls); Mars set at x = 30 (rust ground, cones as hills, table with plate + 6 marshmallow cylinders, subsurf-cube snack bag, standing glove of ellipsoid fingers, balloon on a weight). Balloon = sphere scaled z 1.15 grown from its knot (string length constant); latex colour keyframed lighter as it stretches. Tear lines = thin emissive cylinders on the sphere surface revealed per 0.11 s. Shreds = flattened ico-spheres on ballistic paths (g = 3.71 m/s² on Mars, 9.81 in the hook). 486×864, 8 samples, ~3 s/frame.

## Caption, cover, hashtags
See meta.json (caption v2 + follow line + ⚠️ disclaimer). Cover headline: "THIS BALLOON POPS ON ITS OWN". Hashtags: #science #physics #whatif #sciencefacts #mars #space #balloon #theimpossiblelab.

## Alternative openings (not produced)
- A: start on the snack bag bursting its seam first, balloon last (object-ladder reversed).
- B: slow-motion tear lines at t = 0 ("This rip outruns sound."), then rewind to the intact balloon.

## Experiment record
- E17 reel 2 of 3. Hypothesis: a cascade middle (new object reacting every 1–2 s from 3 to 10 s, escalating) lifts watch ratio above the median.
- One variable: cascade middle (E13 opening, E5 topic, hook style, 15 s / 1.10, caption v2, follow invite, disclaimer unchanged).
- Primary metric: watch ratio vs median 60 %; secondary: IG reach at 24 h vs E5 median 1,093, hook hold vs 62.7 %.
- Baseline: medians TIL-01..16 (hook 62.7 %, watch 60 %); E5 24 h reach median 1,093.
- Checkpoint: 24 h (26 Nov 16:00), 72 h (28 Nov 16:00); E17 first read at the 29 Nov weekly check.

## Science (sources in meta.json)
- Mars mean surface pressure 6.36 mb (4.0–8.7 seasonal), mean temperature ≈ −59 °C (NASA NSSDC Mars Fact Sheet). 6.36 / 1013.25 = 0.63 % → "under one percent".
- Boyle's law: a sealed parcel of air at constant temperature would swell 1013.25 / 6.36 ≈ ×159; cooled from 20 °C to −59 °C (293 → 214 K) ≈ ×116 → "over a hundred times" (card ×116 to ×159).
- Balloons in a vacuum chamber expand and larger ones may burst (Idaho State Univ. physics demo; AVS expanding-balloon demo) → the shown balloon tears at ~×20, honest that it never reaches ×100.
- Latex balloon tear speed ≈ 570 m/s (Moulinet & Adda-Bedia, PRL 2015, via Physics World 3 Nov 2015).
- Speed of sound at the Martian surface ≈ 240 m/s (≈ 250 m/s above ~240 Hz), Perseverance SuperCam microphone (Maurice et al., Nature 2022; NASA/Science News). 570 / 240 ≈ 2.4 → "over twice as fast".
