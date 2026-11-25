# TIL-20 brief — A candle in space (E17 cascade middle, reel 3)

Built 25 Nov 2026 (production run 13:12 EET) for the 26 Nov 16:00 EET slot. Binding premise: TIL-19 end card "TOMORROW: A CANDLE IN SPACE". Last space premise before the variety rule bites (S ≤ 1 in 5; low-pressure/boiling banned to 10 Dec — this premise is buoyancy, not pressure). End card names V1 (toast butter-side down), per the 24 Nov variety rule.

## Performance update
- Evidence used: newest capture in store 250779 = 24 Nov 16:02 EET (post-publish run; no pre-build stats run under the Make-credit rule).
- What it shows: TIL-17 (posted 4 h 32 late) 580 IG accounts at 19.5 h, hook 62.3 % / watch 56 %, ≈ medians. TIL-15 (cascade-style middle) still the best watch ratio of 17 (84 %). E5 reels cluster at ~1.1 k accounts at 24 h.
- Uncertain: E17 has no read yet (TIL-18 live < 24 h at capture, TIL-19 publishes today). Shares 0 on every reel; IG followers flat at 6.
- What changes: nothing (22 Nov 13:20 instruction: TIL-20 = E17 reel 3, same variable as TIL-18/19).

## Evidence → decision
| Observation | Evidence | Creative decision |
|---|---|---|
| Continuous change in 3–10 s lifts completion | TIL-15 watch 84 % (mug → plate → book) | Cascade: hot-air dots rise vs spread 3.4 s → flame turns blue 4.2 s → timers start 5.5 s → Earth candle drips and goes out at "10 MIN" 6.7 s → orbit timer to "45 MIN · STILL LIT" 7.7 s → wax melts into a ball 8.1–9.6 s → flame pulses 10.2 s → dies 11.3 s → wax-fog sphere swells 11.3 s → red warning ring 12.3 s |
| Object visibly reacting at t = 0 beside an Earth control holds best | E13: TIL-08/09/13–16 63–72 % vs condition-only TIL-11 53 % | Frame 0: EARTH vs ORBIT candles light together at 0.08 s; Earth = yellow teardrop, orbit = round ball |
| Everyday object (E5) | E5 PASS 19 Nov | A plain household candle; no person on screen |
| Follow invite (house rule) | Claudio 20 Nov | Pill 5.0–8.2 s (kept clear: no labels in 1440–1520 px), end card, caption line |

## Concept
- Audience: curious 16–35 "what if" viewers; people who light candles at home; teachers explaining convection.
- Reason to send it: it overturns a picture everyone knows (the teardrop flame) with a real NASA result — send to the friend who loves candles / the one who says "fire always points up".

## Five hooks (first 1–2 s)
1. **Image: EARTH teardrop flame vs ORBIT ball flame lighting together + line "In space, fire is round." — WINNER**: the consequence is on screen at 0.1 s beside a control (E13), the claim sounds wrong but is true (NASA), 5 words, readable without sound.
2. Line "This candle lasts 45 minutes." over a burning orbit candle and a timer — strong number but the image (a candle) is ordinary at t = 0.
3. Image: a blue ball of fire floating in the dark, no context — striking but unclear for a first-time viewer.
4. Line "Fire doesn't point up in space." — negation, weaker than a positive claim; same image as 1.
5. Image: the white wax-fog cloud with the red ring — the twist used as the opening would spoil the payoff.

## Script (15.0 s; Kokoro af_heart 1.10; measured line starts)
| t (s) | Visuals | Speech | On-screen text | Editing / audio |
|---|---|---|---|---|
| 0.0–1.6 | Wide: EARTH candle (warm tiles) vs ORBIT candle (station panel, porthole with Earth); both light at 0.08 s: teardrop vs ball | "In space, fire is round." | Title A CANDLE / IN SPACE?; EARTH · ORBIT labels | match strike ×2, soft burn |
| 1.8–3.1 | Push in on the orbit candle; yellow ball flame, porthole behind | "Light a candle in orbit." | — | whoosh cut |
| 3.3–5.2 | Wide: orange hot-air dots stream up from the Earth flame; around the orbit flame they spread evenly and stall; at 4.2 s the orbit flame turns blue | "Hot air can't rise, so it balls up." | chip NO GRAVITY: HOT AIR CAN'T RISE; HOT AIR RISES / HOT AIR STAYS → BLUE · NO SOOT | shimmer, whoomph on blue |
| 5.4–7.7 | Wide: timers; Earth candle shrinks, drips, goes out at 10 MIN (6.7 s); orbit runs to 45 MIN · STILL LIT | "It burns slowly, up to forty-five minutes." | chip MIR CANDLES: UP TO 45 MIN; FOLLOW pill 5.0–8.2 s | digit ticks, puff on Earth out |
| 7.9–10.0 | Close on the orbit candle: body melts down into a molten wax ball under the blue flame | "No drips: the wax melts into a ball." | MOLTEN WAX BALL · NO DRIPS | gloop |
| 10.2–11.1 | Flame pulses (~1.6 Hz) and shrinks | "The real danger?" | — | music drops; pulses |
| 11.3–13.5 | Flame dies; a white wax-fog sphere swells to ~2.2× the flame; red warning ring pulses | "It dies, leaving a flammable wax cloud." | chip WAX FOG CLOUD: 2–3× THE FLAME; FLAMMABLE | puff, swell, warning beeps |
| 13.5–15.0 | THE REAL SCIENCE card; at 13.8 s the hook framing returns (loop) | — | card + red disclaimer; TOMORROW: DOES TOAST LAND BUTTER-DOWN?; FOLLOW @the.impossible.lab | thud |

## Scene / generation notes (pipeline)
- `scene.py` (saved as `pipeline/reference/scene_ep20.py`): one set, two candles (x = ±0.11); orbit flame = sphere with an emissive-rim / transparent-centre shader (`shell_mat`), keyed colour yellow → blue; Earth flame = stretched emissive sphere + small blue base; hot-air dots; drips; molten wax ball; fog shell + torus ring; timers via a `frame_change_pre` handler.
- Labels kept between the title zone and the captions; nothing in the FOLLOW band 5–8.2 s.

## Caption, cover, hashtags
- Cover headline: "IN SPACE, FIRE IS ROUND"
- Caption: see meta.json (v2: hook → science → one share line → series line with follow invite → ⚠️ line → 8 hashtags).

## Two alternative openings (future tests, not produced)
1. Timer-led: frame 0 = two burning candles with clocks, EARTH 10 MIN (out) vs ORBIT 45 MIN (still lit), line "This candle lasts 45 minutes."
2. Twist-first: frame 0 = the flame dying into a white fog ball, line "When this flame dies, the danger starts."

## Experiment record
- Experiment: **E17 cascade middle, reel 3 of 3** (constants: E13 opening, E5, caption v2 + follow line, E16 invite, 15 s / 1.10).
- Hypothesis: a new object or part visibly reacting every 1–2 s from 3 to 10 s lifts watch ratio above the median.
- Variable: middle structure (cascade). Primary metric: watch ratio vs median 60 %. Secondary: IG reach at 24 h vs E5 median 1,093; hook hold vs 61.1 %.
- Checkpoint: 24 h = 27 Nov 16:00; E17 first read at the 29 Nov weekly check (TIL-20 at ~67 h).
