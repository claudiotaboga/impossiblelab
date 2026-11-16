# TIL-11 brief: Your breath on Everest's summit

Built 16 Nov 2026 (daily production run), for the 17 Nov 16:00 EET slot. Experiment **E7 (series teaser end card), reel 1 of 3**; topic keeps the E5 rule (viewer's own body) as the control.

## 1. Performance update (Make 8451991/8451995 snapshot 16 Nov 12:15 CET = 13:15 EET)
- **What the evidence shows:** total 18,505 views (IG 8,208 + YT 10,297). E5 premises keep winning reach: TIL-08 (shrunk) 1,093 accounts at 24 h = 8.0× baseline; TIL-09 (olive oil) 2,132 at 21 h = 15.7×, and the first reel since TIL-01 with hook hold ≥ 70 % (72.1 %, watch ratio 74 %). First follower growth (IG 1 → 4, YT 5 → 6), but still 0 shares on 8,208 IG views.
- **What is uncertain:** why TIL-09's retention jumped (side-by-side control image at t = 0 is the leading hypothesis, n = 1); TIL-10 (E5 reel 3) publishes today at 16:00, no data yet.
- **What changes:** one variable: the ending (E7). The last ~1.5 s shows THE REAL SCIENCE card plus a "TOMORROW: TOAST ON VENUS" end card, and the caption's series line names the same premise. Everything else as TIL-09/10.

## 2. Evidence table
| Observation | Evidence | Creative decision |
|---|---|---|
| Body premises drive reach | E5: TIL-08 8.0×, TIL-09 15.7× vs 0.8–1.0× for 5 non-body premises | Topic: your own breath/brain at the top of Everest |
| Side-by-side proof image at t = 0 coincided with the best hold | TIL-09 two tanks: hook hold 72.1 % vs median 62.4 % | Hook image: SEA LEVEL vs EVEREST 8,849 m, a full vs a sparse "breath" bubble, the summit figure slumping |
| Reach no longer converts to follows | IG +3 follows on 3,225 accounts (≈0.9 per 1,000 reach); 0 shares | E7: end card names tomorrow's premise (a concrete reason to come back), no "follow" wording |
| Competitors: danger/survival on the body over-performs | zackdfilms "…And Survives" 2.2×, thephysicsgirl danger framing | Stakes: you'd faint; payoff: how climbers survive |
| Abstract ratios need a picture | "a third of the oxygen" is invisible | 30 vs 10 molecules, 1 in 5 red in both; the 20 missing ones appear as wireframe ghosts |

## 3. Concept, audience, reason to share
- **Concept:** teleport straight to the 8,849 m summit. The air is still ~21 % oxygen, but the pressure is about a third of sea level (253 vs 760 mmHg), so each breath brings about a third of the oxygen (inspired PO₂ ≈43 vs 149 mmHg). Unadapted, useful consciousness at 28,000–30,000 ft is about 1–3 minutes (FAA); "unconscious within a couple of minutes" (NOVA/PBS). Twist: climbers survive by weeks of acclimatisation, and ~97 % of summits use bottled oxygen.
- **Audience:** 16–35 science-curious viewers, hikers/travellers, anyone who has felt breathless on a mountain or a plane.
- **Reason to send it:** "Send this to the friend who wants to climb Everest" — a real person type, a fact that sounds wrong (the oxygen % does not change).

## 4. Five hooks (first 1–2 s)
1. **"Teleported to Everest, you'd faint."** + SEA LEVEL vs EVEREST side by side, summit figure slumping, sparse breath bubble. ← **winner**
2. "Everest air is still 21 % oxygen." (true-but-wrong-sounding; weaker stakes for the viewer)
3. "Each breath up there is a third." (abstract before the image is understood)
4. Image only: a bubble losing two thirds of its molecules (strong visual, no stakes)
5. "Your brain has two minutes." (strong, but needs the premise first)

**Why #1:** the viewer's own body + an immediate, concrete consequence in five words, proved at t = 0 by the side-by-side image (the TIL-09 pattern), readable without sound. The ending pays it off (how climbers survive) and the last ~1.3 s returns to the hook framing.

## 5. Timestamped script (15.0 s, Kokoro af_heart speed 1.10, 39 words; line starts from timeline.py)
| t (s) | Visual | Speech | On-screen text | Editing | Audio |
|---|---|---|---|---|---|
| 0.0–2.0 | Wide: SEA LEVEL plinth (person standing, full breath bubble, 30 molecules) vs EVEREST 8,849 m peak (person sitting, slumping; bubble 10 molecules) | "Teleported to Everest, you'd faint." | Title "YOUR BREATH / ON EVEREST?" | Cold open, slow push | Thin wind, two shallow gasps |
| 2.2–4.0 | Close on both bubbles; "21% O₂" under each; 1 in 5 molecules red in both | "The air is still one-fifth oxygen." | Chip 1: AIR UP THERE: STILL 21% OXYGEN | Cut, push | 10 plinks |
| 4.2–6.8 | Close on the summit bubble: 20 wireframe ghosts pop in (the missing two thirds); "⅓ THE AIR" | "It's three times thinner: each breath brings a third." | Chip 2: PRESSURE ≈ ⅓ OF SEA LEVEL | Cut, slow push | 20 ticks |
| 7.0–9.6 | Summit figure + BRAIN O₂ gauge draining, timer 0:00 → 2:00; on "lights" the figure tips over and the lights dim | "Your brain starves. In about two minutes, lights out." | Chip 3: UNADAPTED: USEFUL ~1–3 MIN | Cut, hold | Heartbeat 95 → 140 bpm, descending whoosh + thud |
| 9.8–12.1 | Base camp: tents, teal-jacket climber, sign BASE CAMP / WEEKS OF ADAPTING | "How do climbers survive?" / "Weeks of adapting, …" | — | Cut, static wide | Music drops; wind |
| 12.1–13.7 | Summit again: climber with orange oxygen bottle + mask, arms up; label BOTTLED O₂ | "…and most bring oxygen." | — | Cut | Valve hiss, shimmer |
| 13.45–15.0 | Back to the hook framing (loop) | — | THE REAL SCIENCE card + red disclaimer; **"TOMORROW: TOAST ON VENUS"** pill below (E7) | Loop | Card thud |

## 6. Scene / generation notes (pipeline)
- `pipeline/reference/scene_ep11.py`: Blender primitives in metres. Sea-level plinth (x = −1.4, top 0.9 m, sand + sea strip) vs a 7-sided rock cone with a snow cap (x = +1.4, top 1.7 m). Glass "breath" bubbles (r 0.42 m, z 3.35) with 30 vs 10 molecules (every 5th red emissive = O₂); 20 ghost molecules use a WIREFRAME modifier on a white emissive sphere. BRAIN O₂ gauge = box with origin at its bottom, z-scale keyframed; timer text via `frame_change_pre` handler. Lights out = keyframed sun/fill energy + world strength. Base camp at x = 40 (4-sided cone tents, snow mountains, dark sign board behind the labels). Climber has an orange bottle, hose and mask parented to the body; summit bubble hidden in that shot (it would sit on his head).
- Timing from real line starts; `beats.json` holds t_out ("lights"), t_summit2, t_loop, cuts. `overlay.py` per-episode block: title, 3 chips, card, disclaimer, and the new E7 `NEXT` pill (from 13.45 s, y = 1390 px, under the card and above Instagram's bottom UI). `audio_mix.py` SFX: wind, gasps, plinks, ghost ticks, heartbeat, lights-out whoosh + thud, valve hiss.

## 7. Caption, cover, hashtags
- **Cover headline:** YOUR BREATH ON EVEREST? (title at t = 0 over the side-by-side)
- **Caption (v2 + E7 series line):** see `meta.json`: hook line, 4 science lines, share line ("Send this to the friend who wants to climb Everest."), series line "Tomorrow: toast on Venus." (replaces "A new impossible experiment every day."), "⚠️ Don't try this." line, 8 hashtags.
- **YouTube title:** What if you breathed on top of Everest? (≤ 60 chars + " #Shorts")

## 8. Two alternative openings (future tests; not produced)
- **A (E9, body part first):** extreme close-up of a hand with a pulse-oximeter-style readout dropping, summit snow behind: "Watch your oxygen drop."
- **B (E10, you-vs-object):** a sealed crisp packet puffing up on the summit next to you: "Your snack bag would swell up." (needs a verified volume number)

## 9. Experiment record
- **Experiment:** E7 — series teaser end card ("TOMORROW: <next premise>") + matching caption series line, reel 1 of 3 (TIL-11..13).
- **Hypothesis:** naming a concrete next premise gives viewers a reason to follow/return, raising follower conversion without hurting retention.
- **The one variable:** ending / CTA (end card + caption series line). Topic rule (E5), length (15 s / 1.10), caption v2, cold open on a proof image unchanged.
- **Primary metric:** IG followers + YT subscribers gained per 1,000 IG reach in the 24 h after the post. **Baseline:** ≈0.9 per 1,000 (TIL-08+09: IG +3 on 3,225 accounts; YT +1 over the same window).
- **Secondary:** IG reach at 24 h vs E5 median (1,613); hook hold vs median 62.4 %; watch ratio vs 62.5 % (the end card must not lower it).
- **Checkpoint:** first read 18 Nov 16:00 (TIL-11 24 h); verdict after TIL-13's 72 h (22 Nov). Binding: TIL-12 = toast on Venus.
