# TIL-23 — Push a 100,000-tonne ship with one finger (brief, 28 Nov 2026)

CORE reel (Playbook v3 / E19: TIL-23 is the last build before the variance cycle starts at TIL-24). Lane D (ships & engineering) after lane A (TIL-22). Binding: named on TIL-22's end card ("TOMORROW: PUSH A SHIP WITH ONE FINGER").

## 1. Performance update (newest capture: Make store 250779, 27 Nov 22:07 CET = 23:07 EET)
- **What the evidence shows:** TIL-20 (candle in space) at 31 h: 1,582 IG views / 1,081 accounts, hook hold 70.3 %, watch 10.5 s = 70 %, 1 save — first E17 cascade reel above the 60 % watch median and at the E5 reach median (1,093). Best IG retention since TIL-09 (72.1 % / 74 %).
- **Breakout check (rule 3):** none. Highest IG 24 h views ever = TIL-09 3,264 at 21 h vs a ~24 h IG views median of 1,534 for TIL-08..20 (≈ 2.1×, below the 5× threshold); no reel > 10,000 views on any platform.
- **Conversion:** IG followers 6, YT subscribers 8 — flat since 24 Nov. Shares 0 on all 21 IG reels.
- **Uncertain:** TIL-21 (toast, first no-planets reel) published 7 h late (23:05) and had 0 views at the last capture; TIL-22 publishes today 16:00. Lane D (ships) has one data point: TIL-03 honey ship, 111 accounts at 24 h, but posted 8 h 46 min late (confounded).
- **What changes:** nothing in the format (CORE slot; one-variable experiments are the weekly check's job). The end card switches to the first EXPLORE premise (X1-a lightning vs your car) as Claudio's 28 Nov instruction requires.

## 2. Evidence table
| Observation | Evidence | Creative decision |
|---|---|---|
| Retention wins when the consequence is visible in the first second | TIL-09 72 % hook / 74 % watch (person already sinking at t = 0); TIL-20 70 % (two flames lit at 0.08 s) | t = 0: the finger is already on the hull and the time-lapse is running — the red hull mark is sliding off the yellow START line from 0.08 s, "+5 CM" readable by 0.5 s |
| Familiar stakes beat abstract ones (E5) | E5 body/everyday reels cluster ≈ 1.1 k accounts; abstract/space below | "Your finger" vs the biggest object people can picture; the person on the quay is the viewer |
| Claudio 25 Nov: no planets, vary the frame | No-planets rule | Single escalating harbour scene, no split screen; control = the quay's START mark (normal world) |
| Every reel needs a reason to share (send test) | 0 shares on 21 reels | Myth-flavoured claim people argue about ("you can't move a ship by hand") |
| Follow invite mandatory | Claudio 20 Nov | Pill 5.0–8.2 s (only captions + chips in the 1440–1520 px band at that time) + end card + caption line |

## 3. Concept, audience, reason to share
- **Concept:** in still water there is no static friction, so even a one-finger push (10 N) moves a 100,000-tonne ship — 0.2 mm after a minute, about 65 cm after an hour — and stopping it takes just as long.
- **Audience:** 16–40, curious, likes "that can't be true" facts; people who live near harbours/boats; physics students.
- **Send test:** *the friend who wins every pub argument sends this to the friend who insists "big things need big forces", because it proves him wrong with his own finger.*

## 4. Five hooks (first 1–2 s)
1. **"One finger can move this ship."** — person on the quay, one finger on a steel rib of a giant navy-grey hull; TIME-LAPSE timer racing; red hull mark sliding past the yellow START line. **← winner**
2. "This weighs 100,000 tonnes. Watch." — aerial of the whole ship, tiny person.
3. "Your finger vs an aircraft carrier." — macro: fingertip touching steel.
4. "No engine. No tug. One finger." — ship gliding along the quay.
5. "You could push this ship. Really." — person leaning in, gap ruler opening.
**Why #1:** a 6-word claim that sounds wrong, proven on screen in the same second (time-lapse + START mark), understandable without sound; #2/#4 delay the person (no stake), #3 hides the ship, #5 is weaker wording of #1.

## 5. Timestamped script (15.0 s, Kokoro af_heart 1.10; real line starts from timeline.py)
| t (s) | Visuals | Speech | On-screen text | Editing / audio |
|---|---|---|---|---|
| 0.00–1.73 | HOOK (flash-forward): high 3/4 from the quay; person's finger on the stern-corner rib; red waterline stripe, water; TIME-LAPSE 0 → 60 MIN; red mark slides +65 CM from START | 0.20 "One finger can move this ship." | Title PUSH A SHIP / WITH ONE FINGER; in-scene TIME-LAPSE · N MIN, +N CM | hull groan, clock ticks accelerating, harbour lapping |
| 1.73–3.91 | Aerial from the sea side, whole 330 m ship, "100,000 T" on deck, camera rising | 1.79 "A hundred thousand tonnes, floating free." | — | horn, whoosh cut |
| 3.91–6.19 | Close-up from the water: fingertip on the steel rib, amber arrow "10 N", "NO GRIP" | 3.96 "Water can't grip it, so any push moves it." | chip WATER HAS NO STATIC FRICTION; FOLLOW pill from 5.0 s | soft thud on contact |
| 6.19–8.41 | Macro on the marks at the quay edge: red hull mark still on the yellow START line | 6.24 "One minute: about a fifth of a millimetre." | in-scene 1 MIN → 0.2 MM; chip 10 N ÷ 100,000 t = 0.0000001 m/s²; FOLLOW pill to 8.2 s | two clock ticks |
| 8.41–10.42 | Back to the quay: TIME-LAPSE 1 → 60 MIN, gap opens to +65 CM, person walks along | 8.46 "Push for an hour: over half a metre." | chip 1 HOUR OF PUSHING ≈ 65 cm | ticks + hull groan |
| 10.42–11.52 | Wide from the sea: hands off, the ship keeps drifting | 10.47 "The real problem?" | in-scene STILL MOVING | wind, music drops |
| 11.52–13.03 | Person turns and pushes back: TIME-LAPSE 1 H 10 → 2 H 10, SLOWING → STOPPED · +1 HOUR | 11.57 "Stopping it takes another hour." | in-scene timer, +N CM | ticks, final thud |
| 13.03–15.0 | THE REAL SCIENCE card over the hook framing (loop); end card TOMORROW: LIGHTNING VS YOUR CAR + FOLLOW @the.impossible.lab | — | card rows + red disclaimer | card thud |

## 6. Scene / generation notes (pipeline)
Blender primitives, Cycles 8 spp, 486×864. Harbour: concrete quay (top 2 m above water, edge y = 0.25) with bollards and a white edge line; water plane with noise bump. Ship: navy-grey hull 330 m (main box + bow wedge), red boot-top stripe at the waterline, white sheer line + portholes, dark deck, island; stern transom at ship-local x = 0 with a light-steel rib bracket the person pushes. Motion: ship x(t) = ½·a·t² mapped to time-lapse minutes (state() in scene_ep23.py); person follows the rib (walk cycle while moving). Labels: camera-tracked text on dark plates (ep. 21 pattern). Scene = pipeline/reference/scene_ep23.py.

## 7. Caption, cover, hashtags
- **Caption:** see meta.json (caption v2: claim, explanation with numbers, one share line, one series line ending with the follow invite, ⚠️ disclaimer, 8 hashtags).
- **Cover headline:** PUSH A SHIP WITH ONE FINGER
- **YouTube / Facebook title:** "Can one finger move a 100,000-tonne ship?"
- **Hashtags:** #physics #science #ships #whatif #sciencefacts #newton #engineering #theimpossiblelab

## 8. Two alternative openings (future tests, not produced)
- A. **Scale-first:** aerial of the 330 m ship with a single red dot on the quay, zoom-crash down to the finger in 1 s ("This ship is pushed by one finger.").
- B. **Proof-first macro:** the two marks splitting apart in extreme close-up with "+65 CM" growing, reveal the ship and the finger at 1.5 s.

## 9. Experiment record
- **Slot:** CORE, no new variable (Playbook v3; the weekly check chooses CORE variables; E19 starts at TIL-24).
- **Hypothesis (observational):** a familiar-stakes engineering myth with the proof visible at t = 0 reaches at least the E5 median at 24 h and holds hook hold ≥ the 62.4 % median.
- **Primary metric:** IG accounts reached at ~24 h vs E5 median 1,093. **Secondary:** hook hold vs 62.4 %, watch ratio vs 60 %, shares and follows per 1,000 reach (baseline 0).
- **Checkpoint:** 24 h = 30 Nov 16:00 EET (if posted on time 29 Nov 16:00), 72 h = 2 Dec, 7 d = 6 Dec.
