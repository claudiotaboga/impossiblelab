# TIL-13 brief: Your weight on Jupiter

Built 18 Nov 2026 (daily production run), for the 19 Nov 16:00 EET slot. Experiment **E7 (series teaser end card), reel 3 of 3**; topic = queue H, binding (named on TIL-12's end card "TOMORROW: YOUR WEIGHT ON JUPITER" and caption). E5 topic rule kept as the control (the viewer's own body weight). NEXT BUILD INSTRUCTION (18 Nov 11:08) followed: proof-image rule applied strictly — t = 0 shows the consequence already happening on a familiar object.

## 1. Performance update (Make 8451991 exec 3e6a1911…, 8451995 exec 660ebdbf…, snapshot 18 Nov 12:14 CET)
- **What the evidence shows:** total ≈21,800 views (IG 9,923 + YT 11,889); IG followers 6, YT subs 6. E5 body/food premises 3 of 4 ≥ 2× baseline (TIL-08 1,093, TIL-09 2,149, TIL-10 1,079 accounts) but TIL-11 (Everest breath) stalled at 123 accounts with the lowest hook hold (52.8 %) and watch ratio (41 %) of all reels.
- **What is uncertain:** whether TIL-11's drop came from its static opening (a *condition*: thin air) or from its late slot; TIL-12 (E7 reel 2, on time today) is the next read. E7 conversion is unreadable so far (0 follows on 123 accounts).
- **What changes:** nothing new as a variable. The opening is built to the existing playbook rule at its strictest: two scales side by side, EARTH 70 kg vs JUPITER readout racing 100 → 165 kg while the figure sags and the platform squashes, all inside the first 0.65 s.

## 2. Evidence table
| Observation | Evidence | Creative decision |
|---|---|---|
| Openings that show the consequence moving hold better | TIL-09 (person sinking in a labelled tank) 72.1 % vs TIL-11 (static thin-air comparison) 52.8 % | t = 0: Jupiter readout already climbing (100 kg at frame 0), figure sagging |
| Side-by-side control vs impossible reads without sound | TIL-08 balance, TIL-09 two tanks, TIL-12 two thermometers | EARTH vs JUPITER column scales, numbers on big displays |
| "You" stakes drive reach | E5 3 of 4 ≥ 2× | Premise = the viewer's own weight, a number everyone knows |
| Follower conversion is the bottleneck | ≈1.2 IG follows / 1,000 reach (control) | E7 end card "TOMORROW: ICE CREAM ON MERCURY" + caption series line |
| Average watch 6–11 s, end card at ~14 s reaches few viewers | TIL-11 6.2 s avg watch | The twist (Saturn) lands at 11.7 s; the teaser is a bonus for completers, not the hook |

## 3. Concept, audience, reason to share
- **Concept:** the same 70 kg person on a column scale on Earth, Jupiter, Mars, the Moon and Saturn. Jupiter's pull at its 1-bar cloud level is 2.36× Earth's, so the scale reads ≈165 kg; Mars 0.377 → ≈26 kg; Moon 0.166 → ≈12 kg. Jupiter has no solid surface to stand on. Twist: Saturn has 95× Earth's mass, yet you'd weigh less there (0.916 g → ≈64 kg) because it is so wide.
- **Audience:** 14–35, curious, gym-goers and anyone who checks a bathroom scale; space fans who like a counter-intuitive twist.
- **Reason to send it:** "Your weight isn't yours, it's the planet's" — a one-line flex to send to the friend who complains about their weight (light, non-shaming framing: the punchline is the planet, not the body).

## 4. Five hooks (first 1–2 s)
1. **"Jupiter more than doubles your weight."** + EARTH 70 kg vs JUPITER readout racing to 165 kg. ← **winner**
2. "Step on a scale on Jupiter." + figure stepping onto the red scale.
3. "You'd weigh 165 kilos on Jupiter." + close-up of the readout.
4. "Same you. Different planet." + five scales in a row.
5. "Saturn is lighter on you than Earth." (cold open on the twist) + Saturn scale reading 64.
**Why 1:** a claim that sounds wrong-but-true about the viewer, proved at t = 0 by a moving number on a familiar object (the playbook rule TIL-11 broke); "more than doubles" is easier to grasp in 1 s than a three-digit number, and the number appears on screen anyway. Hook 5 is the strongest alternative (twist-first) for a future test.

## 5. Timestamped script (15 s, Kokoro af_heart 1.10, line starts from timeline.py)
| t (s) | Visuals | Speech | On-screen text | Editing | Audio |
|---|---|---|---|---|---|
| 0.0–2.0 | EARTH vs JUPITER column scales side by side, Earth & banded Jupiter spheres behind; Jupiter readout 100 → 165 kg in 0.65 s, figure sags, platform squashes | "Jupiter more than doubles your weight." | Title YOUR WEIGHT / ON JUPITER?; displays EARTH 70 kg, JUPITER 165 kg | Static wide, slow push-in | Thud + creak at 0.05 s, rising digit ticks, confirm beep |
| 2.0–4.8 | Close-up: Jupiter display 165 kg over the sagging figure | "Seventy kilos here, about one sixty-five there." | Chip JUPITER PULLS 2.36× EARTH | Cut | Whoosh on cut |
| 4.8–7.1 | MARS station, red sphere; readout 70 → 26 kg, arms lift | "On Mars, the same you weighs twenty-six." | Chip MARS 0.38× · MOON 0.17× | Cut | Falling ticks |
| 7.1–8.4 | MOON station; readout 70 → 12 kg; figure hops | "On the Moon, just twelve." | (chip held) | Cut | Ticks, soft plinks on hops |
| 8.5–10.7 | Jupiter clouds: scale + figure sink through banded clouds, camera follows down | "But Jupiter has no ground to stand on." | Chip GAS GIANT: NO SOLID SURFACE | Cut, follow-cam | Descending whoosh + wind |
| 10.7–13.8 | SATURN station with ring; label "SATURN · 95× EARTH'S MASS"; readout 70 → 64 kg, figure shrugs | "The weird part?" / "On giant Saturn, you'd weigh less than here." | display text | Cut, push-in | Music drops on the setup, ticks |
| 13.9–15.0 | Back to the hook framing; THE REAL SCIENCE card + red disclaimer; amber pill TOMORROW: ICE CREAM ON MERCURY at 14.0 s | — | Card rows (below) | Loop to opening | Card thud |

## 6. Scene / generation notes (pipeline)
- `pipeline/reference/scene_ep13.py`: column scale = platform + steel column + dark display head (name 0.12, number 0.27 emissive); readouts via `frame_change_pre` handler (`readouts`), Jupiter readout red (`M_DIGR`), others amber. Stations: hook x = ±0.85, Mars 12, Moon 22, Saturn 46 (torus ring scaled z 0.06), Jupiter clouds x = 80 (vertical banded wall at y = 3 + side puffs, never in front of the figure; the floor plane must not reach this set). Planet spheres behind each station (`wave_mat` bands for Jupiter/Saturn).
- Framing: hook camera (0, −6.7, 1.95) → target z 1.6 at 30 mm keeps both displays at 30–40 % height; station cams 5.4 m away, target z 1.65.
- Render 486×864, 8 samples, ~10 s/frame.

## 7. Caption (v2), cover, hashtags
Caption: see `meta.json`. Cover headline: **YOUR WEIGHT ON JUPITER?** (title rows). YouTube title: "What if you stood on a scale on Jupiter?" (41 chars). Hashtags (8): #science #physics #whatif #sciencefacts #jupiter #space #gravity #theimpossiblelab.

## 8. Alternative openings for future tests (not produced)
- A. Twist-first cold open: Saturn scale reading 64 kg, "Saturn is 95 times heavier than Earth. You'd weigh less there."
- B. Body part at t = 0 (E9): close-up of two feet on a scale whose digits race to 165 as the platform cracks.

## 9. Experiment record
- **Experiment:** E7 reel 3 of 3 — end card names tomorrow's experiment ("TOMORROW: ICE CREAM ON MERCURY") + caption series line "Tomorrow: ice cream on Mercury." Topic rule E5 as control.
- **Hypothesis:** a concrete next-episode promise raises follows per 1,000 reach above the no-teaser control.
- **One variable:** ending / series teaser (unchanged from TIL-11/12).
- **Primary metric:** IG followers + YT subscribers gained per 1,000 IG accounts reached in the 24 h after the post. **Baseline:** ≈1.2 per 1,000 (TIL-08..10, no teaser).
- **Secondary:** IG reach at 24 h vs E5 median ≈1,093; hook hold vs median 62.1 % (tests the strict proof-image opening after TIL-11's 52.8 %).
- **Checkpoints:** 24 h 20 Nov 16:00, 72 h 22 Nov 16:00 (E7 verdict), 7 d 26 Nov 16:00.

## 10. Science check (sources in meta.json)
- NASA NSSDCA ratio table: gravity Moon 0.166, Mars 0.377, Jupiter 2.36, Saturn 0.916 (incl. rotation; gas giants at the 1-bar level). Jupiter fact sheet: 23.12 m/s² at the equator, 1 bar; ratio 2.364. Saturn fact sheet: mass 95.16× Earth, 8.96 m/s² (0.916). 70 kg × 2.36 = 165.2; × 0.377 = 26.4; × 0.166 = 11.6; × 0.916 = 64.1.
- Scale "reads" kg calibrated for Earth; the card says "70 kg reads ≈…" (mass unchanged, weight changes).
- Teaser TIL-14 checked: NASA Mercury facts — night side ≈ −180 °C; ice cream technology (Univ. of Guelph): below Tg' the freeze-concentrated phase becomes "a brittle, amorphous solid glass".
