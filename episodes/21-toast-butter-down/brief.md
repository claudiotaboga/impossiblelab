# TIL-21 brief — Does toast really land butter-side down? (lane C, first reel under the no-planets rule)

Built 26 Nov 2026 (production run 13:12 EET) for the 27 Nov 16:00 EET slot. Binding premise: TIL-20 end card "TOMORROW: DOES TOAST LAND BUTTER-DOWN?" (= V1). Lane C (kitchen/everyday) after S; end card names V2 (lane A, your body), per the rotation rule.

## Performance update
- Evidence used: newest capture in store 250779 = 25 Nov 16:02–16:03 EET (guard's post-publish run; no pre-build stats run under the Make-credit rule).
- What it shows: TIL-18 (water on the Moon, E17 r1) 125 IG accounts at 24 h — 0.11× the E5 median 1,093, hook 56.0 %, watch 54 %. TIL-17 590 at 43.5 h. Two low-pressure space premises in a row fell; body/everyday Earth premises (TIL-08/09/10/15/16) hold ~1.1–2.1 k accounts.
- Uncertain: E17 (cascade middle) has n = 1 at 24 h; TIL-19 only 24 h old at 16:00 today; shares still 0 on every reel; IG followers flat at 6.
- What changes: topic only (Claudio 25 Nov: no planets; normal-world control). Format: a single escalating scene (allowed by the 25 Nov instruction) instead of a left/right split; E17 cascade middle, E13 t = 0 reaction, E16 follow invite, 15 s / 1.10 kept.

## Evidence → decision
| Observation | Evidence | Creative decision |
|---|---|---|
| Object visibly reacting at t = 0 holds best | E13: TIL-08/09/13–16 hook 63–72 % vs condition-only TIL-11 53 % | Frame 0: buttered toast already sliding off a 75 cm kitchen table at 0.08 s; flips; lands BUTTER-DOWN by 0.93 s with a red label |
| Continuous change in 3–10 s lifts completion | TIL-15 cascade 84 % watch | 3.9 s scales (toast 40 g, butter pat lifts onto its own scale 4 g) → 6.1 s slow-mo drop with ghost copies → ½ TURN 7.5 s → 8.1–10.7 s a row of 8 school tables drop toast one after another, live DOWN/UP counter → 62 % BUTTER-DOWN |
| Space/low-pressure premises fell; Claudio asked for variety | TIL-17/18 590/125; Claudio 24 + 25 Nov | Earth kitchen premise, control = the same table at normal height vs a 3 m table (twist) |
| Everyday object (E5) | E5 PASS 19 Nov | Breakfast toast + kitchen table; no person on screen |
| Follow invite (house rule) | Claudio 20 Nov | Pill 5.0–8.2 s (no labels in 1440–1520 px), end card, caption line |

## Concept
- Audience: everyone who has ever picked toast off the floor; families, teachers, Murphy's-law fans; 16–45.
- Reason to send it: it turns a "bad luck" myth into a physics result with a ridiculous fix — send it to the friend who blames bad luck (or the butter) every time.

## Five hooks (first 1–2 s)
1. **Image: toast sliding off the table at 0.08 s, flipping and landing BUTTER-DOWN by 0.9 s + line "Blame the table, not the butter." — WINNER**: the familiar event happens on screen at once (E13), the claim sounds wrong but is true (Matthews 1995), 6 words, readable without sound.
2. Line "Toast isn't unlucky. It's physics." — generic, no image advantage.
3. Image: a 3 m tall breakfast table with a toast on top — strong absurd image but spoils the twist.
4. Line "62 % of toast lands butter-down." — number first, but a statistic is weaker than a visible event at t = 0.
5. Image: butter pat on a kitchen scale reading 4 g — unclear to a first-time viewer.

## Script (15.0 s; Kokoro af_heart 1.10; measured line starts)
| t (s) | Visuals | Speech | On-screen text | Editing / audio |
|---|---|---|---|---|
| 0.0–1.8 | Raised 3/4 view of a kitchen table; toast slides off the plate at 0.08 s, tips, half turn, lands butter-down 0.93 s | "Blame the table, not the butter." | Title WHY TOAST LANDS / BUTTER-DOWN; BUTTER-DOWN label | slide, splat, low buzz |
| 2.0–3.7 | Side angle replay; amber height bar 75 CM; second toast lands 3.4 s | "Toast slides off a normal table." | 75 CM | slide, whoosh, splat |
| 3.9–5.8 | Close: two kitchen scales; toast reads 40 g; butter pat lifts off onto the second scale: 4 g | "Butter is a tenth of its weight, at most." | chip BUTTER: ≤ 10 % OF A ~40 g SLICE; TOAST / BUTTER; FOLLOW pill from 5.0 s | digit ticks, squeak, beep |
| 6.0–7.7 | Front: slow-mo drop, 4 ghost copies trace the arc; ½ TURN at landing 7.5 s | "It only has time for half a turn." | chip 75 CM TABLE → ABOUT ½ TURN; ½ TURN | whoosh, splat |
| 7.9–11.4 | School canteen: 8 tables, toasts slide off one every 0.33 s; red/green floor marks; counter DOWN n · UP n → 62 % BUTTER-DOWN | "In nearly ten thousand drops, sixty-two percent hit butter-down." | chip SCHOOL TEST: 62 % OF ~10,000 DROPS | 8 slides + splats |
| 11.6–12.2 | Back in the kitchen: the table legs grow to 3 m; camera pulls back; 3 M bar | "The fix?" | 3 M | creak + rising whoosh; music drops |
| 12.4–13.8 | Toast slides off the 3 m table; follow-cam down; full turn; lands BUTTER-UP 13.67 s | "A table three metres tall." | BUTTER-UP (green) | long whoosh, splat, ding |
| 13.85–15.0 | THE REAL SCIENCE card; hook framing returns at 14.1 s (loop) | — | card + red disclaimer; TOMORROW: ALL YOUR BACTERIA ON A SCALE; FOLLOW @the.impossible.lab | thud |

## Scene / generation notes (pipeline)
- `pipeline/reference/scene_ep21.py`: one kitchen set + a school row set at x = 6 m. `drop_pose()` = slide 22 % of the drop + parabolic fall with a linear turn to π (½ turn) or 2π (full turn). Butter = separate box placed from the toast's rotation each frame (so it can lift onto its own scale).
- Labels are billboards (TRACK_TO the camera) on dark backing plates — readable at phone size from a raised 3/4 camera.
- Table height animated: top box + legs (unit cylinders scaled in z) keyed per frame; follow-cam on the 3 m drop.

## Caption (v2 + follow invite), cover, hashtags
- Cover headline: WHY TOAST LANDS BUTTER-DOWN
- Caption: see meta.json (hook, 2 short science paragraphs, one share line, series line ending with the follow invite, ⚠️ line, 7 hashtags).
- YouTube / Facebook title: "Why does toast land butter-side down?" (37 chars)

## Alternative openings (future tests; not produced)
- A. Absurd image first: a 3 m breakfast table with a toast on top, line "Your table is too short." (flash-forward, E3 style).
- B. Statistic first: a wall of falling toast with a 62 % counter racing up, line "Toast lands butter-down 62 % of the time."

## Experiment record
- No new variable (22 Nov 13:20 instruction: keep the TIL-20 format until the 29 Nov check). Claudio's 25 Nov topic rule applies: first Earth-only premise after 10 space/altitude reels; framing varied (single escalating scene) as the instruction allows.
- Hypothesis (observational): an everyday Earth premise with a visible event at t = 0 returns to the E5 reach level after the space run.
- Primary metric: IG reach at 24 h vs E5 median 1,093; secondary: watch ratio vs median 60 %, hook hold vs 62.4 %, follows per 1,000 reach (E16).
- Checkpoints: 24 h 28 Nov 16:00 · 72 h 30 Nov 16:00 · 7 d 4 Dec 16:00; read at the 29 Nov weekly check (24 h only).

## Sources
- Matthews, R. A. J. (1995) "Tumbling toast, Murphy's Law and the fundamental constants", European Journal of Physics 16(4):172–176, doi:10.1088/0143-0807/16/4/005 — https://ui.adsabs.harvard.edu/abs/1995EJPh...16..172M/abstract
- Wikipedia, Buttered toast phenomenon (tables 0.7–1.83 m → ≈ ½ turn; > 3 m → full turn; Ig Nobel Physics 1996) — https://en.wikipedia.org/wiki/Buttered_toast_phenomenon
- Ian Stewart, "The Anthropomurphic Principle" (Scientific American 1995 reprint): ~40 g slice, butter ≤ 10 %, effect negligible; ≈ 3 m table — https://whydomath.org/Reading_Room_Material/ian_stewart/anthro/anthro.html
- Indiana Public Media, A Moment of Science "Murphy's Toast" (2019): ten-foot table for a full turn — https://www.ipm.org/show/amomentofscience/2019-09-18/murphys-toast
- R. Matthews, Telegraph 2001 (reprint): "Of almost 10,000 trials, toast landed butter-side down 62 per cent of the time" — https://diyhpl.us/~bryan/irc/extropians/extracted-extropians-archive/archive/0105/83777.html ; BBC Science Focus (Matthews): "almost two-thirds" — https://www.sciencefocus.com/science/why-does-toast-often-land-butter-side-down
