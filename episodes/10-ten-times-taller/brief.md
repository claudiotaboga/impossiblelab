# TIL-10 brief: You, 10× taller

Built 15 Nov 2026 (daily production run), for the 16 Nov 16:00 EET slot. Experiment **E5, reel 3 of 3**.

## 1. Performance update (Make 8451991/8451995 snapshot 15 Nov 13:14 EET)
- **What the evidence shows:** total 13,504 views (IG 4,929 + YT 8,575). TIL-08 (E5 reel 1, "shrunk to 1 cm") is the breakout: 1,090 IG accounts at 21 h = 8.0× the 136 baseline, 1,544 IG views, 1,480 YT views, first save. Its retention is only about median (hook hold 63.1 %, watch ratio 64 %), so the lift came from the premise/distribution, not from holding viewers longer. Instagram freezes after ~12–20 h on every reel. Followers: IG 1 (unchanged), YT 5.
- **What is uncertain:** one breakout is not a pattern; TIL-09 (E5 reel 2) publishes today at 16:00 and has no data yet. Follower conversion is zero on IG.
- **What changes:** nothing (NEXT BUILD INSTRUCTION, 15 Nov 11:08: keep current). TIL-10 = queue F "You, 10× taller": the viewer's own body at an impossible scale, the mirror image of TIL-08.

## 2. Evidence table
| Observation | Evidence | Creative decision |
|---|---|---|
| "You at an impossible scale" broke out | TIL-08: 1,090 accounts at 19–21 h (8.0× baseline) | Same family, inverted: you, ten times taller |
| Body/food premises lead IG reach | mercury 1,146, shrunk-you 1,090, pasta 517 vs 111–137 for the other five | Stakes on the viewer's own legs |
| Hook proven by an image works without sound | TIL-08 balance, TIL-09 two tanks | t = 0: a 17.5 m giant running down a street, houses at its knees, shins glowing red |
| Abstract ratios are hard to see | square-cube law is usually explained with formulas | Show it with blocks: 1 block → 1,000 blocks (weight) vs a 100-tile slab (bone cross-section) |
| Caption v2 running, no engagement bait | decision 13 Nov | One share line + series line + disclaimer, 8 hashtags |

## 3. Concept, audience, reason to share
- **Concept:** scale a 1.75 m, 70 kg person ×10 in every direction. Height 17.5 m, volume and weight ×1,000 (70 t), but bone strength grows only with cross-section ×100, so every bone carries ×10 the stress. Running already loads leg bones to ~55 MPa with a safety factor of only ~3–4 (Biewener), so ×10 means one run breaks them (Haldane's 1926 argument). The twist: the only fix is to let water carry the weight, which is how blue whales get so big.
- **Audience:** 16–35 science-curious viewers, tall people and their friends, anyone who has wished to be a giant.
- **Reason to send it:** "the tallest friend you have" — an instant tag-a-friend reason that is not bait, plus a fact that sounds wrong (being bigger makes you weaker).

## 4. Five hooks (first 1–2 s)
1. **"Giant-sized, your legs would snap."** + giant running past rooftops, shins glowing red. ← **winner**
2. "Ten times taller. A thousand times heavier." (numbers before stakes; slower to land)
3. "Being 17 metres tall would break you." (number hard to picture in 1 s)
4. Image only: a normal person beside a giant's foot, "70 kg → 70 t" (strong scale, no tension)
5. "Your bones can't grow fast enough." (abstract without sound)

**Why #1:** the viewer's own body + a concrete, wrong-sounding consequence in five words, proved on screen by the image (giant, houses to the knee, red shins) and readable without sound. The ending pays it off (legs give way, then the whale fix) and the last second returns to the running giant (loop).

## 5. Timestamped script (15.0 s, Kokoro af_heart speed 1.10, 41 words)
| t (s) | Visual | Speech | On-screen text | Editing | Audio |
|---|---|---|---|---|---|
| 0.0–2.0 | Low follow-cam: 17.5 m giant runs down a suburban street, houses at knee height, a 1.75 m person by the road, shins pulsing red | "Giant-sized, your legs would snap." | Title "YOU, 10× / TALLER?" | Cold open | Giant footsteps |
| 2.2–3.5 | Beside a house, a person and a figure of the same size; the figure grows ×10; white height bar "17.5 m" | "Grow ten times taller." | in-scene 1.75 m / 17.5 m | Cut, static wide | Rising whoosh |
| 3.7–5.2 | Plaza: one orange block "x1" next to a 10×10×10 cube of blocks stacking up layer by layer; label WEIGHT x1,000 | "You'd weigh a thousand times more." | Chip 1: 70 kg → 70 t (×1,000) | Cut, slow push | 10 clicks + thud |
| 5.4–7.6 | High angle: a 10×10 slab of tiles appears in front of the cube; label BONE x100 | "Your bones? Only a hundred times stronger." | Chip 2: BONE STRENGTH: ONLY ×100 | Cut, crane down | Plink |
| 7.8–10.4 | Follow-cam: giant runs, shins glow brighter; on "break" it buckles to its knees | "Ten times the stress. One run, and they break." | Chip 3: STRESS ×10 · BONES FAIL AT ≈3–4× | Follow, hold on the collapse | Heavier steps, crack, knee thud |
| 10.6–11.5 | Giant kneeling on the street | "The only fix?" | — | Hold | Music drops |
| 11.0–13.4 | Lake: giant stands chest-deep, no glow, a whale's tail rises behind | "Live in water, like a blue whale." | — | Cut, slow push | Splash, whale whoomph |
| 13.4–15.0 | Back to the running giant (hook framing) | — | THE REAL SCIENCE card + red disclaimer | Loop | Card thud |

## 6. Scene / generation notes (pipeline)
- `pipeline/reference/scene_ep10.py`: Blender primitives in metres. The giant is the standard mannequin scaled ×10; its shins carry an emissive red sleeve whose strength is keyframed per frame (stress). Running pose = hip/knee keyframes; collapse = hips −0.9 rad, knees +1.9 rad, pelvis −3.5 m, pitch 0.35.
- Sets: suburban street along x with houses (4.5–5.5 m + roof), trees and cars; plaza at x = −145 with 1,000 blocks built as 10 layer meshes (bmesh), one block and a 100-tile slab; lake at x = 160–260 (see-through water box, ep. 09 material), whale body + tail stock + flukes.
- Timing from real line starts (`timeline.py`); `beats.json` holds t_break (the word "break") and cuts. `overlay.py` per-episode block: title, 3 chips, card, disclaimer. `audio_mix.py` SFX: footsteps, grow whoosh, block clicks, crack + knee thud, splash, whale whoomph.

## 7. Caption, cover, hashtags
- **Cover headline:** YOU, 10× TALLER? (title at t = 0 over the running giant)
- **Caption (v2):** see `meta.json`: hook line, science lines, share line ("Send this to the tallest friend you have."), series line, "⚠️ Don't try this." line, 8 hashtags.
- **YouTube title:** What if you were 10 times taller? (33 chars + " #Shorts")

## 8. Two alternative openings (future tests; not produced)
- **A (E9, body part first):** extreme close-up of a giant knee/shin glowing red with a crack line, house roof in the background, "One run would break them."
- **B (E10, you-vs-object hook):** a giant's foot next to a car, "Your foot would outweigh this car." (would need a verified foot-mass number)

## 9. Experiment record
- **Experiment:** E5 (topic selection: stakes on the viewer's own body or an everyday object/food), reel 3 of 3 (TIL-08..10).
- **Hypothesis:** premises with stakes on the viewer's own body reach ≥ 2× the baseline of IG accounts at 24 h.
- **The one variable:** topic selection rule (format, 15 s / 1.10 voice, caption v2, 16:00 slot unchanged).
- **Primary metric:** IG reach at 24 h vs baseline 136 accounts (target ≥ 272). Secondary: hook hold vs median 61.3 %.
- **Checkpoints:** 24 h (17 Nov 16:00), 72 h (19 Nov 16:00), 7 d (23 Nov 16:00). E5 verdict at TIL-10's 72 h.
