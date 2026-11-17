# TIL-12 brief: Making toast on Venus

Built 17 Nov 2026 (daily production run), for the 18 Nov 16:00 EET slot. Experiment **E7 (series teaser end card), reel 2 of 3**; topic = queue D, binding (named on TIL-11's end card and caption). E5 topic rule kept as the control (everyday food).

## 1. Performance update (Make 8451991/8451995 snapshots 17 Nov 12:14 and 18:44 CET)
- **What the evidence shows:** total ≈21,220 views (IG 9,767 + YT 11,446 at 18:44 CET). Body/food premises still own reach: TIL-08 1,093, TIL-09 2,147, TIL-10 1,078 accounts vs 112–520 for the five non-body premises. Retention flat at median except TIL-09 (side-by-side proof image, 72 % hook hold). IG followers 6, YT subscribers 6; 0 shares on ~9,800 IG views.
- **What is uncertain:** whether E7 lifts follows — TIL-11 (E7 reel 1) went out 3 h 44 min late today (19:43 EET), so its first read is confounded by the slot and is not available yet. Toast on Venus is a space premise with a food angle: E5 says pure space sits at the median, so the food stake must carry the hook.
- **What changes:** nothing new (NEXT BUILD INSTRUCTION 17 Nov 11:28 followed). E7 end card now names TIL-13 = "your weight on Jupiter" (queue H; gravity ratios checked against NASA).

## 2. Evidence table
| Observation | Evidence | Creative decision |
|---|---|---|
| Food/body stakes drive reach; pure space sits at median | E5 3/3 ≥ 7.9× baseline; competitor space "what ifs" at their median (kurzgesagt, astrumspace) | Lead with the viewer's own kitchen: "Venus is hotter than your oven." |
| Side-by-side proof image at t = 0 coincided with the best hold | TIL-09 72.1 % vs median 63.0 % | Hook image: YOUR OVEN vs VENUS, thermometers climbing to 260 vs 464 °C, readable without sound |
| Viewer-vs-familiar-object hooks broke out | TIL-08 "Big raindrops weigh more than you" 8.0× | Hook compares Venus with an object everyone owns (backlog E10 pattern, not the tested variable) |
| Follower conversion is the bottleneck | ≈1.2 IG follows per 1,000 reach (TIL-08..10) | E7 end card "TOMORROW: YOUR WEIGHT ON JUPITER" + caption series line |
| Captions/labels must stay clear of title and caption zones | ep. 11 notes; test stills today (labels clipped at frame edges, fixed) | Values text inside the frame, labels hidden outside their shots |

## 3. Concept, audience, reason to share
- **Concept:** Venus' surface averages ~464 °C (NASA), nearly twice a home oven's max (260–290 °C). Air pressure 92 bar (~91× Earth), 96.5 % CO₂. Bread held out there skips "toast" and chars (plant matter breaks down above ~280 °C; 400–500 °C is charcoal-kiln heat, FAO). Twist: no flames, because there is no free oxygen to burn with.
- **Audience:** 16–35 science-curious viewers, home cooks, space fans.
- **Reason to send it:** "Send this to the friend who burns every toast" — a person everyone knows, and a fact (no fire on the hottest planet) that sounds wrong.

## 4. Five hooks (first 1–2 s)
1. **"Venus is hotter than your oven."** + YOUR OVEN vs VENUS thermometers racing to 260 vs 464 °C. ← **winner**
2. "Toast on Venus never catches fire." (strong twist, but spends the payoff in second 1)
3. "Your toaster is too cold for Venus." (clever, needs a beat to parse)
4. Image only: a slice of bread turning black in one second (strong visual, no claim, risks reading as a cooking fail)
5. "Venus would turn bread to charcoal." (clear, weaker surprise than the oven comparison)

**Why #1:** five words, a familiar object the viewer owns, sounds wrong for a planet farther from the Sun than Mercury yet is true, and is proved on screen at t = 0 by the side-by-side thermometers (the TIL-09 pattern). The payoff (no flames) is held for the end.

## 5. Timestamped script (15.0 s, Kokoro af_heart speed 1.10, 38 words; line starts from timeline.py)
| t (s) | Visual | Speech | On-screen text | Editing | Audio |
|---|---|---|---|---|---|
| 0.0–1.9 | Wide: YOUR OVEN (tiles behind, glowing door) vs VENUS (basalt ground, orange haze); thermometers climb to 260 vs 464 °C | "Venus is hotter than your oven." | Title "TOAST / ON VENUS?" | Cold open, slow push | 12 rising ticks |
| 2.0–3.3 | Venus close: a bread slice lowers onto a steel toast fork | "Hold out a slice of bread." | — | Cut | Whoosh + soft thud |
| 3.5–5.1 | Both thermometers, OVEN MAX line, "≈1.8×" | "Nearly twice your oven's max." | Chip 1: VENUS 464 °C · OVEN MAX ~260 °C | Cut, slow push | — |
| 5.3–7.1 | Bread ringed by 10 pressure arrows squeezing in, "92 BAR" | "The air presses ninety times harder." | Chip 2: AIR PRESSURE ≈ 90× EARTH'S | Cut | Low rumble |
| 7.3–9.5 | Bread chars golden → brown → black; "CHARCOAL" on the word | "Your bread skips toast and turns to charcoal." | Chip 3: CHARCOAL-MAKING HEAT: 400–500 °C | Cut, push in | Dry crackle |
| 9.7–10.5 | Tight push on the black slice | "The weird part?" | — | Push | Music drops |
| 10.7–13.0 | Crossed-out flame beside the slice, NO OXYGEN / 96.5% CO₂ | "No flames. There's no oxygen to burn." | — | Cut | Descending whoosh (the fire that never comes) |
| 13.0–15.0 | Back to the hook framing (loop), Venus slice now charcoal | — | THE REAL SCIENCE card + red disclaimer; **"TOMORROW: YOUR WEIGHT ON JUPITER"** pill (E7) | Loop | Card thud |

## 6. Scene / generation notes (pipeline)
- `pipeline/reference/scene_ep12.py`: Blender primitives in metres at sculpture scale. Oven = steel box with dark door, emissive orange window, handle and knobs (x = −1.4) in front of a tile wall; Venus = basalt-noise slab with pebbles (x = +1.4) in front of an emissive orange haze wall + orange area light. Thermometers (glass tube without caps, emissive red fill box with origin at its bottom, z-scale keyframed; 0–500 °C over 1.9 m); value text via `frame_change_pre`. Bread = empty with bevelled crust/crumb boxes and two flattened sphere lobes; charring = keyframed Principled Base Color (`default_value`) on crumb and crust, slight shrink. Pressure arrows = 10 cones around the slice. Crossed flame = cone + sphere with two red bars. Thermometers and signs hidden outside the hook/thermometer/loop shots (their bulbs sat on top of the slice in close-ups).
- `beats.json`: t_char ("charcoal"), t_loop, cuts. `overlay.py` per-episode block: title, 3 chips, card, disclaimer, `NEXT` pill (auto-shrinks the font to ≤ 820 px). `audio_mix.py` SFX: ticks, whoosh + thud, rumble, crackle, descending whoosh.

## 7. Caption, cover, hashtags
- **Cover headline:** TOAST ON VENUS? (title at t = 0 over the thermometers)
- **Caption (v2 + E7 series line):** see `meta.json`: hook line, 4 science lines, share line ("Send this to the friend who burns every toast."), series line "Tomorrow: your weight on Jupiter.", "⚠️ Don't try this." line, 8 hashtags.
- **YouTube title:** What if you made toast on Venus? (33 chars + " #Shorts")

## 8. Two alternative openings (future tests; not produced)
- **A (E9, body part first):** a hand holding a toast fork into orange haze, the slice blackening in the first second: "Don't hold toast out on Venus."
- **B (E12, survival/"no fire" framing):** a slice on the stand under a crossed-out flame: "The hottest planet can't start a fire."

## 9. Experiment record
- **Experiment:** E7 — series teaser end card ("TOMORROW: <next premise>") + matching caption series line, reel 2 of 3 (TIL-11..13).
- **Hypothesis:** naming a concrete next premise gives viewers a reason to follow/return, raising follower conversion without hurting retention.
- **The one variable:** ending / CTA (end card + caption series line). Topic rule (E5 food/body), 15 s / 1.10, caption v2, side-by-side proof image at t = 0 unchanged.
- **Primary metric:** IG followers + YT subscribers gained per 1,000 IG reach in the 24 h after the post vs control ≈ 1.2 (TIL-08..10).
- **Secondary:** IG reach at 24 h vs E5 median 1,093; hook hold vs 63.0 %.
- **Checkpoint:** first read 19 Nov 16:00 (24 h); verdict after TIL-13's 72 h (22 Nov). Confound: TIL-11 (reel 1) was posted 3 h 44 min late.
