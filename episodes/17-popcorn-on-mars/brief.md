# TIL-17 — Popcorn on Mars (brief, 22 Nov 2026)

## Performance update
- **Evidence:** TIL-15 24 h (25.8 h capture) = 1,730 IG views / 1,211 accounts (1.11× the E5 median 1,093), watch ratio **84 %** (best of 16), hook hold 64.8 %. TIL-14 at 49.8 h is frozen at 328 accounts with hook hold 66.8 % but watch ratio 51 %. Across the body/food reels, 24 h IG reach tracks watch ratio more than hook hold.
- **Uncertain:** E16 (follow invite) still unreadable — IG followers flat at 6, YT subs 7. TIL-16 went out 1 h 46 min late (scheduled run started late), so its slot is confounded.
- **What changes:** nothing new. Per the 22 Nov 13:20 NEXT BUILD INSTRUCTION, TIL-17 keeps the E13 opening and the protected middle (a new on-screen change every 1–2 s from 3 to 10 s) as constants. E17 (cascade middle) starts with TIL-18.

## Evidence table
| Observation | Evidence | Creative decision |
|---|---|---|
| Openings where a familiar object reacts at t = 0 hold better | TIL-08/09/13/14 hook hold 63–72 % vs TIL-11/12 53–61 % | Frame 0: EARTH pan vs MARS pan, kernels pop from 0.08 s, Mars flakes visibly bigger |
| Watch ratio drives IG reach | TIL-15 84 % → 1,211; TIL-14 51 % → 328 | 3–10 s middle changes every ~1–2 s: Mars surface pull-back, air dots vanish, gauge 0 → 9 atm, burst, Earth-size flake appears, Mars flake puffs to 2× |
| Food premises carry topic reach (E5 PASS) | 4 of 5 E5 reels ≥ 2× baseline | Popcorn: everyone has made it |
| Most viewers leave before 13.5 s | avg watch 6–12.6 s | FOLLOW pill 5.0–8.2 s + end-card follow line + caption follow line |

## Concept
Popcorn made on Mars comes out bigger: with almost no air outside, the steam that bursts the hull puffs the starch further. Lab proof: at 1/30 atm, popcorn's expansion volume more than doubled and unpopped kernels fell ~5× (Quinn, Hong & Both 2005). Mars air is ≈0.6 % of Earth's (even thinner than the lab test).
- **Audience:** snack people, movie-night people, space fans; teens–adults who share "wait, really?" food facts.
- **Reason to send it:** "the friend who always burns the popcorn" — a counter-intuitive upgrade to a ritual they own.

## Five hooks (first 1–2 s)
1. **"Popcorn pops bigger on Mars."** + EARTH vs MARS pans popping side by side, Mars flakes bigger. ← **winner**: a claim that sounds wrong but is true, proved on screen in the first second (E13).
2. "These are the same kernels." + two piles, one twice the size.
3. "Mars makes better popcorn." (vaguer — "better" is a judgement, not a measurable claim)
4. "Thin air, giant popcorn." (readable but abstract; no claim a viewer can disbelieve)
5. "Zero duds on Mars." (overclaims — the lab saw ~5× fewer, not zero)
Winner: #1 — shortest falsifiable claim, matches the visual exactly, food + place everyone knows.

## Script (15.0 s, Kokoro af_heart 1.10; real line starts from timeline.py)
| t (s) | Visuals | Speech | On-screen text | Editing / audio |
|---|---|---|---|---|
| 0.0–2.0 | EARTH (blue wall) vs MARS (rust wall) pans; kernels pop from 0.08 s, Mars flakes 1.26× linear (2× volume) | "Popcorn pops bigger on Mars." | Title POPCORN / ON MARS?; wall labels EARTH · AIR: 1 ATM / MARS · AIR: ≈0.006 ATM | pop SFX per kernel |
| 2.1–3.5 | Mars surface: pan on a stove on red ground, camera pulls back | "Same kernels, same pan." | MARS SURFACE | cut whoosh, thin wind |
| 3.7–5.6 | close-up pan, 36 air dots; all but one vanish at 4.5 s | "Mars has under one percent of our air." | chip MARS AIR: ≈0.6 % OF EARTH'S; label AIR: EARTH → AIR: MARS (<1 %) | shimmer |
| 5.8–8.3 | pan + gauge "INSIDE THE KERNEL", needle 0 → 9 ATM, kernel swells/shakes, bursts at 8.0 s | "Steam bursts the hull at about nine atmospheres." | chip HULL BURSTS AT ≈9 ATM (135 PSI); FOLLOW pill 5.0–8.2 s | tick counter, creak, big pop + whoomph |
| 8.5–11.2 | EARTH SIZE flake appears on a plate (8.8 s); Mars flake puffs to 2× (9.7 s) | "With no air pushing back, it puffs up twice as big." | EARTH SIZE / MARS: 2× VOLUME | whoomph on puff |
| 11.4–13.8 | back to both pans; duds ringed: EARTH 5, MARS 1 | "The bonus?" "About five times fewer duds." | DUDS: 5 / DUDS: 1; chip LAB, 1/30 ATM: ≈5× FEWER DUDS | double beep |
| 13.9–15.0 | THE REAL SCIENCE card + red disclaimer; hook framing returns (loop); TOMORROW: WATER ON THE MOON + FOLLOW @the.impossible.lab | — | card | thud |

## Scene / generation notes
Blender primitives only (scene saved as pipeline/reference/scene_ep17.py): flakes = 6 puffy lobes + hull fleck under an animated empty; kernels = squashed glossy spheres; gauge = disc + ticks + needle empty rotated −135° → +135°; text bodies via frame_change_pre handler. Pan handles point to the back so two pans fit side by side at 16 mm.

## Caption (v2 + follow invite)
See meta.json. Share line: "Send this to the friend who always burns the popcorn." Series line: "Tomorrow: a glass of water on the Moon. 🔔 Follow @the.impossible.lab (or subscribe on YouTube) so you don't miss it." Disclaimer: "⚠️ Don't try this. Hot oil, steam and popping kernels can burn, and low-pressure chambers are lab equipment."
- **Cover headline:** POPCORN ON MARS?
- **Hashtags (8):** #science #physics #whatif #sciencefacts #mars #popcorn #space #theimpossiblelab

## Alternative openings (future tests, not produced)
- A. One kernel in extreme close-up bursting into a flake twice its Earth twin's size (single-object proof).
- B. A movie-night bowl filling twice as fast on the Mars side (volume race).

## Experiment record
- Running: E13 (opening) + protected middle as **constants** (22 Nov instruction), E5 topic rule, E16 follow invite. No new variable in this reel.
- Hypothesis carried: a visible consequence at t = 0 plus a change every 1–2 s through 3–10 s keeps watch ratio ≥ 60 % and 24 h IG reach ≥ the E5 median.
- Primary metric: watch ratio vs median 60 %; IG reach at 24 h vs E5 median 1,093. Secondary: hook hold vs median 63 %, follows per 1,000 reach.
- Checkpoint: 24 h = 23 Nov 16:00 (read at the 29 Nov weekly check, plus the daily post-publish snapshots).
