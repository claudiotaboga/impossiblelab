# TIL-22 brief — Every bacterium in your body on one scale (lane A, your body)

Built 27 Nov 2026 (production run 13:12 EET) for the 28 Nov 16:00 EET slot. Binding premise: TIL-21 end card "TOMORROW: ALL YOUR BACTERIA ON A SCALE" (= V2). Lane A (body) after C (toast); end card names V3 (lane D, ships & engineering), per the rotation rule.

## Performance update
- Evidence used: newest capture in store 250779 = 26 Nov 16:03 EET (guard's post-publish run; no pre-build stats run under the Make-credit rule).
- What it shows: TIL-19 (balloon on Mars, E17 r2) 399 IG accounts at 24 h (0.37× the E5 median 1,093), hook 64.3 %, watch 54 %; TIL-18 frozen at 125 accounts. E17 cascade middle: watch 54 % / 54 % on its first two reels vs median 60 %. Body/everyday Earth premises (TIL-08/09/10/15/16) hold ~1.1–2.1 k accounts.
- Uncertain: TIL-20 (last space reel) had no 24 h read at build time; TIL-21 (first no-planets reel) publishes today; shares still 0 on every reel; IG followers flat at 6.
- What changes: topic only (V2, lane A — first pure "your body" premise since TIL-11). Format unchanged per the 22 Nov 13:20 instruction (keep TIL-20 format until the 29 Nov check): E13 reaction at t = 0 with a normal-world control (a familiar apple on the other pan), E17 cascade middle, E16 follow invite, 15 s / 1.10.

## Evidence → decision
| Observation | Evidence | Creative decision |
|---|---|---|
| Object visibly reacting at t = 0 holds best | E13: TIL-08/09/13–16 hook 63–72 % vs condition-only TIL-11 53 % | Frame 0: a jar of glowing green "bacteria" drops onto a balance at 0.08 s (beam slams down), an apple drops on the other pan at 0.40 s and the beam swings back to almost level |
| Body premises reach furthest | E5 PASS (19 Nov): 4 of 5 body/food reels ≥ 2× baseline; TIL-09 2,149 accounts | Stakes on the viewer's own body: "your bacteria", "your own cells", "your gut" |
| Continuous change in 3–10 s lifts completion | TIL-15 cascade 84 % watch; E17 kept as constant | 2.1 s gut beads stream into the jar → 3.9 s disc stacks grow (1 disc = 1 trillion) → 6.3 s one human cell → 6.8 s one bacterium → 7.3 s ~1,000× SMALLER → 7.7 s back to the balance ALL ≈ 200 g → 9.0 s colon lights up → 11.3 s flush |
| Space/low-pressure premises fell; Claudio asked for variety | TIL-17/18 590/125 accounts; Claudio 24 + 25 Nov | Earth/body premise, no planets, control = an apple (everyday) |
| Follow invite (house rule) | Claudio 20 Nov | Pill 5.0–8.2 s (no labels in 1440–1520 px), end card, caption line |

## Concept
- Audience: curious adults 18–45 who have heard "you're 90 % bacteria"; health/fitness and gut-health followers; biology students and teachers.
- Reason to send it: it corrects a myth almost everyone repeats ("10 bacteria for every cell", "2 kg of germs") with a surprising, concrete image (an apple) and a funny twist (the toilet flips the count) — send it to the friend who keeps quoting the 90 % myth.

## Five hooks (first 1–2 s)
1. **Image: jar of green bacteria vs an apple on a balance, the beam settles level + line "Your bacteria weigh about an apple." — WINNER**: an object physically reacts at t = 0 beside a familiar control (E13), the claim sounds wrong but is true (Sender et al. 2016), 6 words, readable without sound.
2. Line "You're not 90 % bacteria." — myth-busting, but no image advantage and a negation is weaker than a concrete claim.
3. Image: two stacks, green 38 vs red 30 — a chart first; unclear to a first-time viewer at t = 0.
4. Line "One flush changes who you are." — strongest curiosity, but spoils the twist and risks reading as a misleading promise.
5. Image: a see-through body with a glowing gut — striking but no tension at t = 0.

## Script (15.0 s; Kokoro af_heart 1.10; measured line starts)
| t (s) | Visuals | Speech | On-screen text | Editing / audio |
|---|---|---|---|---|
| 0.0–1.8 | Close on a kitchen balance; jar of green beads lands 0.25 s (beam slams left), apple lands 0.55 s, beam swings back to almost level | "Your bacteria weigh about an apple." | Title ALL YOUR BACTERIA / ON ONE SCALE; BACTERIA · 1 APPLE labels | whoosh, glass clink, creak, thud, creak |
| 1.95–3.6 | Wide: a see-through body beside the table; 64 gut beads arc out into the empty jar; beam goes from apple-down to level | "Every germ in you, on one scale." | — | drop plinks |
| 3.8–6.1 | Two disc stacks grow (1 disc = 1 trillion): BACTERIA 38 T vs YOUR CELLS 30 T; green keeps growing after red stops | "Nearly forty trillion, more than your own cells." | chip 1 DISC = 1 TRILLION · 38 vs 30; FOLLOW pill from 5.0 s | rising ticks, one per disc |
| 6.3–8.7 | Navy "microscope" set: one human cell pops in (6.3), one bacterium with an amber ring (6.8), ~1,000× SMALLER (7.3); 7.7 s cut to the balance: ALL ≈ 200 g | "Each is so tiny, they total two hundred grams." | chip ALL TOGETHER ≈ 0.2 kg · 0.3 % OF YOU; 1 HUMAN CELL / 1 BACTERIUM | pops, chime, chime |
| 8.9–10.0 | Close on the torso: the colon lights up green | "Most live in your gut." | chip ALMOST ALL LIVE IN YOUR COLON; COLON | shimmer |
| 10.2–10.8 | Back to the stacks, 38 vs 30 | "The twist?" | — | music drops |
| 11.0–13.1 | Flush: 13 top green discs fly off one by one, green falls below red → < 30 T, HUMAN CELLS AHEAD | "One trip to the toilet can flip the count." | HUMAN CELLS AHEAD | water swirl, whooshes, chime |
| 13.15–15.0 | THE REAL SCIENCE card; hook framing returns at 13.4 s (loop) | — | card + red disclaimer; TOMORROW: PUSH A SHIP WITH ONE FINGER; FOLLOW @the.impossible.lab | thud |

## Scene / generation notes (pipeline)
- `pipeline/reference/scene_ep22.py`: three sets side by side (cells x = −6, kitchen x = 0, stacks x = 6). Balance = beam box rotated per frame about a pivot; pans + strings placed from the beam angle (`pan_pos()`; sign: left end z = −ARM·sin a for a > 0). Beam angle: damped swing in the hook, apple-down → level while the jar fills.
- Bacteria = small emissive green spheres (deep base colour, emission ≤ 1 — brighter washed out to mint inside the glass jar). The see-through body uses the `liquid()` material so the glowing colon (torus) and gut beads read through it.
- Disc stacks: 1 disc = 1 trillion (pitch 3 cm), revealed one per 34 ms; the name/count labels ride on top of each stack. Flush = top 13 discs fly off one per 75 ms (38 → 25, shown as "< 30 T", hedged).

## Caption (v2 + follow invite), cover, hashtags
- Cover headline: ALL YOUR BACTERIA ON ONE SCALE
- Caption: see meta.json (hook, 2 short science paragraphs, one share line, series line ending with the follow invite, ⚠️ line, 7 hashtags).
- YouTube / Facebook title: "What do all your bacteria weigh?" (32 chars)

## Alternative openings (future tests; not produced)
- A. Myth first: a "90 % BACTERIA" sign that cracks as the green stack shrinks to match the red one; line "You're not 90 % bacteria."
- B. Twist first (E3 flash-forward): the flush at t = 0 with HUMAN CELLS AHEAD, line "One flush changes the count."

## Experiment record
- No new variable (22 Nov 13:20 instruction: keep the TIL-20 format until the 29 Nov check). Claudio's 25 Nov no-planets / lane rotation rules applied: lane A after C.
- Hypothesis (observational): a "your body" myth-buster with an everyday control object (apple) returns to the E5 reach level (≥ 1,093 accounts at 24 h) after the space run.
- Primary metric: IG reach at 24 h vs E5 median 1,093; secondary: watch ratio vs median 60 %, hook hold vs 62.4 %, IG follows per 1,000 reach (E16).
- Checkpoints: 24 h 29 Nov 16:00 · 72 h 1 Dec 16:00 · 7 d 5 Dec 16:00.

## Sources
- Sender R, Fuchs S, Milo R (2016) "Revised Estimates for the Number of Human and Bacteria Cells in the Body", PLOS Biology 14(8):e1002533 — 3.8·10¹³ bacteria, 3.0·10¹³ human cells (84 % red blood cells), B/H ≈ 1.3, "about 0.2 kg of bacteria", ≈ 0.3 % of body weight, reference man 70 kg / 20–30 y / 170 cm; replaces "1–3 kg" and 10:1 (Luckey 1972) — https://pmc.ncbi.nlm.nih.gov/articles/PMC4991899/
- Weizmann Institute press release "Germs, Humans and Numbers" (2016): "just under 40 trillion bacterial cells and about 30 trillion human ones"; average bacterium "about 1,000 times smaller" than the average human cell — https://wis-wander.weizmann.ac.il/node/7871
- Nature News via Scientific American (2016): the authors' preprint — "each defecation event may flip the ratio to favour human cells over bacteria" — https://www.scientificamerican.com/article/scientists-bust-myth-that-our-bodies-have-more-bacteria-than-human-cells/
- USDA SR Legacy 171688 (apples, raw, with skin): 1 medium (3" dia) = 182 g — https://tools.myfooddata.com/nutrition-facts/171688/wt4/1
