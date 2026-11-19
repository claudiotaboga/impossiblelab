# TIL-14 brief: a scoop of ice cream on Mercury's night side

Built 19 Nov 2026 (production run, 13:12 EET) for the 20 Nov 16:00 EET slot. E13 reel 1 of 3 (consequence in motion at t = 0); E5 topic rule and the E7 end card held constant.

## 1. Performance update (snapshot 19 Nov 12:14 CET / 13:14 EET, Make 8451991 exec ca0a6757…, 8451995 exec c92056f4…)
- **What the evidence shows:** E5 (your body / everyday food) passed on 19 Nov: 4 of 5 E5 reels ≥ 2× the 136-account baseline at ~24 h vs 0 of 5 non-body/food reels. TIL-12 (toast on Venus) now 702 IG accounts / 921 IG views / 920 YT views at 22.2 h (5.2× baseline, 0.64× the E5 median 1,093); hook hold 60.8 %, watch 60 %.
- **Opening matters more than topic once the topic is right:** reels whose first frame showed a familiar object physically reacting held 63–72 % (TIL-08 balance tipping, TIL-09 person sinking); readout/condition openings held 53–60 % (TIL-11 thin air 53.2 %, TIL-12 thermometers 60.8 %). n = 4 → hypothesis.
- **Uncertain:** E7 (teaser end card) shows no conversion lift so far (IG followers 6, YT subscribers 6 flat since 17 Nov); verdict 22 Nov. Shares are 0 on ~11,000 IG views.
- **What changes in this reel:** the one variable is the opening visual (E13): the spoon strikes the Mercury scoop at 0.12 s and it cracks with shards flying, beside an Earth scoop the spoon sinks into.

## 2. Evidence table
| Observation | Evidence | Creative decision |
|---|---|---|
| Object-reacting openings hold better | TIL-08 63.0 %, TIL-09 72.1 % vs TIL-11 53.2 %, TIL-12 60.8 % hook hold | t = 0: spoon already striking; cracks + shards by 0.2 s; Earth control spoon sinking in |
| Everyday food/body premises get distributed | E5 PASS (4 of 5 ≥ 2× at 24 h) | Ice cream + your freezer + your spoon as the familiar anchors |
| Most viewers leave around 9 s | avg watch 6–11 s on 15 s reels | The payoff ("It chips.") lands by ~10.5 s; twist kept to 2 s |
| Sound-off viewing | captions + chips are the only text | In-scene labels EARTH −18 °C / MERCURY NIGHT −180 °C readable at t = 0 |
| Teaser card unseen by most (avg watch < card time) | E7 data so far | End card unchanged (E7 constant until its 22 Nov verdict) |

## 3. Concept, audience, reason to share
- **Concept:** the coldest night in the inner solar system turns a dessert into glass — and then the same planet bakes it.
- **Audience:** curious 16–35s who like food science and space trivia; ice-cream lovers who fight rock-hard tubs.
- **Reason to send:** "you always complain the ice cream is too hard — try Mercury" → the friend who microwaves the tub.

## 4. Five hooks (first 1–2 s)
1. **Image + line "This ice cream cracks like glass."** — spoon hits a Mercury scoop, it cracks and chips fly; Earth spoon sinks in beside it. (WINNER)
2. Line "Your spoon would bounce off this." — spoon bouncing off the scoop, no shards.
3. Image only: a scoop shattering in slow motion on grey regolith, label −180 °C.
4. Line "Mercury turns dessert into glass." — planet-first framing.
5. Line "Your freezer is too warm for this." — freezer vs Mercury thermometers.
**Why 1:** it is the only option that shows the consequence on a familiar object at t = 0 with a built-in Earth control (E13's variable), states a claim that sounds wrong but is true (the glass transition), and needs no planet knowledge. Hook 3 is strong visually but has no claim; 4 starts with the planet (the TIL-11/12 failure mode); 5 opens on a readout.

## 5. Timestamped script (15.0 s, Kokoro af_heart 1.10)
| t (s) | Visuals | Speech | On-screen text | Editing | Audio |
|---|---|---|---|---|---|
| 0.00–2.06 | Split set: EARTH kitchen scoop (spoon sinks in, lifts a little ball) vs MERCURY NIGHT scoop on regolith under stars (spoon strikes at 0.12 s, cracks appear, glassy shards fly) | "This ice cream cracks like glass." | Title ICE CREAM / ON MERCURY?; in-scene EARTH −18 °C, MERCURY NIGHT −180 °C | Locked wide, slow push | soft squish (left), glassy clink + crack + tinkling shards (right) |
| 2.06–4.28 | Mercury night plain with craters, the frosted scoop in its bowl | "Night on Mercury: minus one eighty." | Chip MERCURY AT NIGHT: −180 °C | Cut + slow push | whoosh |
| 4.28–6.02 | Open home freezer, spoon scoops easily | "Your freezer: minus eighteen." | Chip HOME FREEZER: −18 °C | Cut | squish |
| 6.02–8.71 | Macro "inside the scoop": ice crystals drifting in amber syrup; counter −18 → −30 °C; syrup turns blue glass, crystals freeze, cracks appear | "Below minus thirty, its syrup turns to glass." | Chip GLASS POINT ≈ −30 °C; in-scene "−30 °C: GLASS" | Cut | ticks, crack + clink |
| 8.71–10.75 | Close-up Mercury scoop: spoon bounces (9.0 s), then chips it (9.9 s), shards fly | "Your spoon won't scoop. It chips." | — | Cut | two clinks, tinkles |
| 10.75–13.80 | Wide Mercury plain: NIGHT LASTS ≈88 EARTH DAYS, counter DAY 1 → 88; sunrise, 430 °C, scoop collapses and scorches | "The weird part?" / "Night lasts three months. Then it bakes." | in-scene SUNRISE 430 °C | Cut, slow push | ticks, whoomph, sizzle; music drops on line 6 |
| 13.80–15.00 | Back to the hook framing (loop) | — | THE REAL SCIENCE card + red disclaimer; TOMORROW: EARTH STOPS SPINNING | Card slides in | thud |

## 6. Scene / generation notes (pipeline)
`pipeline/reference/scene_ep14.py` (Blender primitives, 486×864, 8 samples): bowl = cone, scoop = sphere + lumps; spoon = flattened sphere + cylinder aimed with a quaternion; cracks = zigzag thin cylinders on the scoop surface parented to the bowl; shards = 16 ico-spheres on ballistic paths per impact; macro slab = amber Principled box with ico-sphere crystals, colour keyframed to icy blue; sunrise = emissive sphere + SUN lamp energy keyframed; text labels via `frame_change_pre`. SFX in `audio_mix.py`: clink (inharmonic ring), squish, tinkles, counter ticks, whoomph, sizzle.

## 7. Caption, cover, hashtags
- **Cover headline:** ICE CREAM ON MERCURY?
- **Caption (v2):** see `meta.json` → caption (hook line, 3 science lines, twist, one share line, one series line, ⚠️ disclaimer, 8 hashtags).
- **YouTube title:** What if you scooped ice cream on Mercury?

## 8. Two alternative openings (future tests, not produced)
- A. Slow-motion shatter only (no Earth control), hook line "Your spoon would bounce off this."
- B. Hand-held POV: a viewer's hand + spoon in frame (E9 body-in-frame) striking the scoop.

## 9. Experiment record
- **Experiment:** E13 consequence in motion at t = 0 (reel 1 of 3: TIL-14..16).
- **Hypothesis:** an opening where a familiar object visibly reacts within 0.5 s, beside an Earth control, raises hook hold vs readout/condition openings.
- **One variable:** the opening visual (topic rule E5, 15 s / 1.10, caption v2, E7 end card unchanged).
- **Primary metric:** IG hook hold (100 − reels_skip_rate); baseline median 61.1 % (TIL-01..11); target ≥ 65 % mean over TIL-14..16.
- **Secondary:** IG reach at 24 h vs E5 median 1,093; watch ratio vs 62 %.
- **Checkpoint:** 24 h (21 Nov 16:00), review at TIL-16's 48 h (24 Nov).
