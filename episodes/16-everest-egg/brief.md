# TIL-16 brief — Boiling an egg on Everest

Built 21 Nov 2026 (production run 13:12 EET) for the 22 Nov 16:00 EET slot. Binding premise from the TIL-15 end card ("TOMORROW: BOILING AN EGG ON EVEREST"). E13 reel 3 of 3, E16 reel 2 (full follow invite: pill + end card + caption).

## Performance update (data: Make data store 250779, 11:08 EET capture of 21 Nov; no new Make runs before publishing, per the 21 Nov credit rule)
- E13 reel 1 (TIL-14) hook hold **68.4 %** at 19 h (+7.3 pts on the 61.1 % median) — the opening rule works for the first second.
- But TIL-14 IG reach was only **295** at 19 h (0.27× the E5 median 1,093) and watch ratio 52 %: viewers stayed past the strike, then left before the payoff.
- Among 7 body/food reels, 24 h reach tracks watch ratio (74 % → 2,149 … 41 % → 124) more than hook hold (low–medium, observational).
- Conversion flat: IG followers 6, YT subscribers 7 since 17 Nov. TIL-15 (first full E16 reel) posts today 16:00.
- Uncertain: whether a food premise framed by a place (Everest) carries like body/food premises did; TIL-11 (Everest, condition-only opening) held only 53 %.
- What changes: nothing in the variable (E13 constant). Within the format, the middle is protected (11:08 instruction): the pot/egg stays on screen and changes every 1–2 s between 3 and 10 s (air dots vanish → thermometer climbs → boil starts at 70 → 80 °C mark lights → spoon taps → wobble).

## Evidence table
| Observation | Evidence | Creative decision |
|---|---|---|
| Object visibly reacting at t = 0 holds viewers | TIL-08/09/13/14 mean 67.4 % vs readout openings TIL-11/12 57.2 % | Frame 0: SEA LEVEL vs EVEREST plates; at 0.08 s both boiled-egg halves drop — the sea-level halves hold their dome, the Everest half slumps and spreads (RUNNY) |
| Everest condition-only opening was the weakest hook (53 %) | TIL-11 | No mountain in the first 1.8 s; the summit appears only on line 2 as context |
| Reach tracks watch ratio | finding 2, 21 Nov 11:08 | No explanation-only stretch: every number lands on a moving prop (thermometer column, bubbles starting, spoon taps) |
| Viewers leave at ≈ 8–9 s | avg watch 7.9–9.0 s | Both key numbers (≈70 °C, ≈80 °C) are on screen by 7.7 s; follow pill 5.0–8.2 s |
| Food + kitchen premises get reach | E5 PASS (4 of 5 ≥ 2× baseline) | Stakes = your breakfast egg and your pot, not the mountain |

## Concept, audience, reason to share
- Concept: on Everest's summit water boils at about 70 °C, so a "boiled" egg never sets properly — and the yolk can firm up before the white.
- Audience: curious 18–35, home cooks, hikers/travellers, people who swear by their soft-boiled-egg timing.
- Reason to send: "the friend who times their boiled eggs to the second" — their method fails at altitude.

## Five hooks (first 1–2 s)
1. **"Boiling water can't cook this egg."** + both eggs drop: sea-level halves stay domed, Everest half slumps runny — *winner*: sounds wrong, is true, and the image proves it within 0.3 s without sound.
2. "This egg boiled for ten minutes." + runny egg cut open (needs a time claim the sources don't give — rejected).
3. "Water boils at seventy here." + thermometer pinned at 70 while bubbling (readout opening — E13 says no).
4. "Same pot. Same egg. Raw." + two pots side by side (≤ 6 words, but "raw" overstates: part of the white does set at 60–65 °C).
5. "Your yolk sets first up here." + yolk turning matte (gives away the twist).

## Timestamped script (15 s, Kokoro af_heart 1.10)
| t (s) | Visuals | Speech | On-screen text | Editing / audio |
|---|---|---|---|---|
| 0.0–1.7 | Hook kitchen: SEA LEVEL / EVEREST stations, pots boiling; egg halves drop at 0.08 s, land 0.25 s, Everest half slumps and wobbles | "Boiling water can't cook this egg." | Title AN EGG ON / EVEREST?; 3D: SEA LEVEL · BOILS AT 100 °C, EVEREST · BOILS AT ≈70 °C, COOKED / RUNNY | thud + squish at 0.25 s, rolling-boil bed |
| 1.9–3.5 | Cut: pot bubbling on the summit rock; camera pulls back to reveal the snowy peak | "Same pot, on top of Everest." | 3D: EVEREST SUMMIT · 8,849 m | whoosh cut, thin wind |
| 3.7–7.1 | Cut: pot close-up; 24 of 36 air dots vanish (4.6 s); thermometer climbs 20 → 70 °C (5.3–6.1 s), pot starts boiling at 70 | "A third of the air pressure, so water boils near seventy degrees." | chip SUMMIT AIR: ≈1/3 OF SEA-LEVEL PRESSURE; 3D AIR: ≈1/3, readout follows the column; FOLLOW pill 5.0–8.2 s | shimmer, rising ticks, boil kicks in |
| 7.3–9.5 | Push in on the thermometer: 70 mark vs 80 mark (lights red at 7.7 s); egg rocking in the bubbling water | "Most of the white needs about eighty to set." | chip EGG WHITE (OVALBUMIN) SETS AT ≈80 °C; 3D WHITE SETS ≈80 °C, BOILS ≈70 °C | double beep at 80 |
| 9.7–11.2 | Cut: close-up of the Everest egg on the plate; spoon taps twice, white wobbles | "So it stays soft and wobbly." | — | clink + squish ×2 |
| 11.4–12.2 | Push in on the yolk | "The weird part?" | — | music drops out |
| 12.4–13.9 | Yolk turns matte pale yellow (sets) while the white stays glossy | "The yolk can set before the white." | chip YOLK SETS AT ≈62–70 °C | shimmer, music returns |
| 13.9–15.0 | THE REAL SCIENCE card; camera back to the hook framing (loop) | — | card + red disclaimer; TOMORROW: POPCORN ON MARS; FOLLOW @the.impossible.lab | thud |

## Scene / generation notes (pipeline)
- `pipeline/reference/scene_ep16.py`: hook set x = 0 (two stove+pot stations, plates at x = ±0.2, egg halves = bisected UV sphere + yolk sphere; runny half scales xy +70 %, z −60 % with decaying wobble), summit set x = 30 (snow cones + rock + same pot, emissive sky plane, its own area "sun"), close-up set x = 60 (36 air dots, 2/3 shrink at T_THIN; thermometer 0.0055 m/°C with marks 70/80/100, readout text follows the column top; egg rocking in the water).
- Yolk "sets" by keyframing the Principled Base Color/Roughness (glossy orange → matte pale yellow).
- Exposure −0.6 (AgX Punchy washed out the bright counter/walls at 0).
- Render 486×864, 8 samples, two processes (0–179, 180–359).

## Caption (v2 + follow invite), cover, hashtags
See meta.json `caption`. Cover headline: "AN EGG ON EVEREST?" (title rows). Hashtags (8): #science #physics #whatif #sciencefacts #everest #cooking #eggs #theimpossiblelab.

## Two alternative openings for future tests (not produced)
- A: split-screen cut eggs at full frame (no pots), the Everest one oozing as the knife passes — tighter on the object.
- B: the thermometer column racing up and stopping dead at 70 while the pot erupts into a boil — "it's boiling, it's not hot" contradiction (readout-led; would test E13's opposite).

## Experiment record
- E13 reel 3 of 3. Hypothesis: a visible physical consequence at t = 0 (beside an Earth control) lifts hook hold vs the 61.1 % median (target ≥ 65 % mean over TIL-14..16).
- One variable: opening visual (object reacting vs control). Everything else constant (15 s / 1.10, caption v2, E16 follow invite, E5 food framing).
- Primary metric: hook hold (100 − reels_skip_rate). Secondary: IG reach at 24 h vs E5 median 1,093; watch ratio vs median 60 %.
- Baseline: hook median 61.1 %; reel 1 TIL-14 = 68.4 %. Checkpoint: TIL-16 at 48 h (24 Nov 16:00) → E13 verdict.
- E16 (constant alongside): followers + subscribers gained per 1,000 IG reach in the 24 h after the post; baseline ≈ 1.2 (TIL-08..10) / ≈ 0.5 (TIL-11..13); review after TIL-17's 24 h.
