# TIL-15 brief — Earth stops spinning for one second

Built 20 Nov 2026 (production run 13:12 EET) for the 21 Nov 16:00 EET slot. E13 reel 2 of 3, E16 reel 1 with the full follow invite (pill + end card + caption).

## Performance update (data: Make 8451991 / 8451995 captures up to 20 Nov 12:15 CET)
- Body/object-reacting openings hold better: TIL-08 63.0 %, TIL-09 72.1 %, TIL-13 66.1 % (mean 67.1 %) vs readout/condition openings TIL-11 53.2 %, TIL-12 61.1 % (mean 57.2 %). Median hook hold 61.1 %. n = 5, low–medium confidence.
- TIL-13 (Jupiter weight) = 1,081 IG accounts at ~21 h (≈1× E5 median 1,093): E5 topic rule keeps delivering distribution.
- Conversion is the bottleneck: IG followers flat at 6 since 17 Nov; YT subs 6 → 7. E7 end card unseen (avg watch ≈ 9 s, card at 13.45 s) → superseded by E16 (Claudio, 20 Nov).
- Shares: 0 on > 12,000 IG views. Uncertain: whether anything in-video can move sends (E14 still in backlog).
- What changes in this reel: nothing new in the opening rule (E13 constant); the follow invite now appears inside the average watch window (5.0–8.2 s pill) + end card + caption.

## Evidence table
| Observation | Evidence | Creative decision |
|---|---|---|
| Object visibly reacting at t = 0 holds viewers | 67 % vs 57 % mean hook hold (TIL-08/09/13 vs 11/12) | Frame 0: NORMAL EARTH vs STOPPED EARTH tables; at 0.08 s the right table's mug, plate+apple and book fly east with streaks |
| Everyday object + "you" premises get reach | E5 PASS: 4 of 5 ≥ 2× baseline | The stakes are your coffee mug and your kitchen table, not a globe |
| Viewers leave at ≈ 9 s | avg watch 6.2–9.0 s | Payoff structure front-loaded: speed vs sound by 8.6 s; follow pill at 5.0–8.2 s |
| Captions/labels must read without sound | playbook v2 | 3D labels (NORMAL/STOPPED EARTH, MUG: 465 m/s →), speed bars vs a sound-barrier line, 3 chips |

## Concept, audience, reason to share
- Concept: you are already moving east at up to 465 m/s; stop the ground for one second and your coffee keeps going — faster than sound at the equator, near sound speed at 45°, almost still at the pole.
- Audience: curious 18–35 who like "wait, really?" physics; coffee drinkers; people who think Earth's spin is too slow to matter.
- Reason to send: "the friend who never secures the coffee in the car" — the same inertia they ignore every time they brake.

## Five hooks (first 1–2 s)
1. **"Your coffee breaks the sound barrier."** + mug launching off the STOPPED EARTH table. ← **winner**
2. "You're moving at 465 m/s right now." + both tables still, then the right one empties.
3. "Stop Earth. Keep your coffee." + globe halting, mug flying.
4. "Your kitchen is supersonic." + kitchen side by side.
5. "One second without spin." + clock + flying table contents.
Winner: #1 is a claim that sounds wrong but is true (465 > 343 m/s at the equator), names an everyday object, and the image proves it within 0.2 s — the E13 rule. #2 is a readout-style opening (the pattern that held 53–61 %).

## Timestamped script (15.0 s, Kokoro af_heart 1.10)
| t (s) | Visual | Speech | On-screen text | Edit / audio |
|---|---|---|---|---|
| 0.00–1.86 | Hook split: NORMAL EARTH table (mug steaming) vs STOPPED EARTH table; 0.08 s right-table objects launch east with streaks, coffee drops left on the table | "Your coffee breaks the sound barrier." | Title EARTH STOPS / SPINNING?; 3D labels MUG STAYS PUT / MUG: 465 m/s → | double crack + whoosh at 0.08 s, camera jolt |
| 2.01–3.92 | Globe spinning, dead stop at 3.11 s, shudder | "Stop Earth's spin for one second." | EARTH: SPINNING → EARTH: STOPPED · FOR 1 SECOND | hum, heavy thud + clang at the stop |
| 3.92–5.88 | Close-up STOPPED EARTH table, mug back; 4.92 s it launches east | "The ground stops. Your mug doesn't." | GROUND: STOPPED | crack + whoosh; FOLLOW pill from 5.0 s |
| 5.88–7.28 | Globe, glowing equator ring, small mug leaves tangentially east | "At the equator, nearly five hundred metres a second." | EQUATOR ≈465 m/s; chip EQUATOR ≈465 · SOUND 343 | whoosh |
| 7.28–8.80 | Speed bars: SOUND 343 vs EQUATOR MUG 465 past the sound line | (cont.) | FASTER THAN SOUND | ticks as bars grow |
| 8.80–10.00 | Globe from above-front, green 45° N ring | "Halfway to the pole: still near sound speed." | 45° N; chip 45° N ≈329 m/s | |
| 10.00–11.30 | Bars: mug bar shrinks 465 → 329, just short of the sound line | (cont.) | JUST UNDER SOUND SPEED | descending ticks |
| 11.30–13.61 | Pole: mug on the North Pole, steam rising calmly | "And at the pole?" / "Your coffee barely moves." | NORTH POLE ≈ 0 m/s; chip | music drops on the setup, soft wind |
| 13.61–15.0 | THE REAL SCIENCE card over the hook framing (loop) | — | card + red disclaimer; TOMORROW: BOILING AN EGG ON EVEREST; FOLLOW @the.impossible.lab | thud |

## Scene / generation notes
`pipeline/reference/scene_ep15.py` (Blender primitives, 486×864, 8 samples): hook set at x = 0 (two tables, dark slate wall, white divider), globe set at x = 30 (noise-ramp globe, equator + 45° torus rings, pole mug with emissive steam), bars set at x = 60 (bar lengths 2.2 units per 465 m/s, sound line at 343). Launches = constant-velocity + accelerating stylisation (3 s + 12 s² units) with x-stretch smear; streaks are thin emissive boxes. Text via frame_change_pre handler.

## Caption (v2 + follow line), cover, hashtags
See meta.json. Cover headline: "YOUR COFFEE BREAKS THE SOUND BARRIER". Hashtags (8): #science #physics #whatif #sciencefacts #earth #space #coffee #theimpossiblelab. YouTube title: "What if Earth stopped spinning for one second?" (46 chars).

## Two alternative openings (future tests, not produced)
- A: first-person POV from a car dashboard that brakes; coffee slides — then cut to "now do it with the whole planet" (E9 body/POV).
- B: the hook line as a viewer-vs-object comparison: "Your mug is faster than a jet." (E10).

## Experiment record
- E13 reel 2/3 — hypothesis: a familiar object visibly reacting beside an Earth control in the first 0.5 s lifts hook hold. One variable: opening visual. Primary metric: hook hold vs median 61.1 % (target ≥ 65 % mean over TIL-14..16). Secondary: IG reach at 24 h vs E5 median 1,093. Checkpoint: 24 h (22 Nov 16:00), review at TIL-16's 48 h (24 Nov).
- E16 reel 1 (full version) — follow invite pill 5.0–8.2 s + end card + caption. Primary metric: IG followers + YT subs per 1,000 IG reach in the 24 h after posting; baselines ≈ 1.2 (TIL-08..10) and ≈ 0.5 (TIL-11..13). Review after TIL-17's 24 h.
- Constant: E5 topic rule (everyday object), 15 s / 1.10, caption v2 + follow line, disclaimer.
