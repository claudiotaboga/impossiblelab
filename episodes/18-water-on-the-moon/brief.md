# TIL-18 — A glass of water on the Moon (brief, 23 Nov 2026)

## Performance update (capture 23 Nov 20:31–20:32 EET, Make 8451991 / 8451995 run in this session — no 11:07 check on Mondays since the weekly cadence of 22 Nov)
- **Evidence:** TIL-16 at 26.8 h = 1,659 IG views / 1,155 accounts (1.06× the E5 median 1,093), hook hold 62.3 %, watch 8.65 s = 58 %. TIL-14 at 76.5 h frozen at 328 accounts (hook hold 66.8 %, watch 51 %). TIL-15 at 52.5 h = 1,212 accounts, watch 84 % (still best). E5 food/body reels keep landing in a ~1,080–1,210 reach band (6 of 9); only TIL-09 (hook hold 72 %) broke out (2,149).
- **Uncertain:** TIL-16 on YouTube has 6 views at 27 h (typical 500–1,700) — same pattern as TIL-06 (11); cause unknown (late upload, YT-side). IG followers flat at 6, YT subscribers 7 → 8. Shares still 0 on 17 reels. TIL-17 went out 4 h 32 min late (run started 20:30), so its slot is confounded.
- **What changes:** per the 22 Nov 13:20 NEXT BUILD INSTRUCTION, TIL-18 is **E17 reel 1 (cascade middle)**: from 3 to 10 s a NEW familiar object reacts every 1–2 s, escalating, while the number is spoken. E13 opening, E5 topic rule, hook style, 15 s / 1.10, caption v2 + follow line, E16 pill + end card, ⚠️ disclaimer unchanged.

## Evidence table
| Observation | Evidence | Creative decision |
|---|---|---|
| A familiar object reacting at t = 0 beside a control holds the opening | E13 reels hook hold 66.8 / 64.8 / 62.3 % vs median 62.7 % | Frame 0: EARTH glass (calm) vs MOON glass erupting from 0.08 s; ice crust by ~1 s |
| A cascade of reacting objects kept people watching | TIL-15 (mug → plate + apple → book) 84 % watch, best of 17 | 3–10 s: glass boils (2.5 s) → air vanishes (3.9 s) → tea erupts (4.7 s) → soup erupts (5.9 s) → flower vase erupts (6.9 s) → ice crusts snap on one by one (7.9 / 8.3 / 8.8 / 9.2 s) |
| Everyday food/objects carry reach (E5) | 6 of 9 E5 reels ≈ 1.1 k reach vs 136 pre-E5 baseline | Glass of water, mug of tea, bowl of soup, flower vase |
| Most viewers leave before ~9 s | avg watch 6–12.6 s | FOLLOW pill 5.0–8.2 s kept clear of the props; end card follow line |

## Concept
An open glass of water on the Moon boils at room temperature (almost no air pressure: ~3×10⁻¹⁵ bar; liquid water needs ≥ 611.657 Pa), the boiling pulls heat out so the rest freezes, and then even the ice sublimates away — except in permanently dark polar craters colder than −238 °C, where ice survives.
- **Audience:** space fans, kitchen-physics fans, teens–adults who share "that can't be right" facts.
- **Reason to send it:** "the friend who always leaves a glass of water on the table" — a ritual everyone owns, turned impossible.

## Five hooks (first 1–2 s)
1. **"This water boils and freezes."** + EARTH glass calm vs MOON glass erupting and icing over ← **winner**: two opposite verbs in one claim that sounds wrong but is true, proved on screen within 1 s (E13).
2. "Ice, made by boiling." (clever, but abstract without the glass)
3. "Your drink can't stay liquid here." (true but explains before it shows)
4. "Boiling water. Zero heat." (confusing: the water is at room temperature, not zero heat)
5. "On the Moon, water explodes." (misleading overclaim)

## Script (15.0 s, Kokoro af_heart 1.10; real line starts from timeline.py)
| t (s) | Visuals | Speech | On-screen text | Editing / audio |
|---|---|---|---|---|
| 0.0–1.9 | EARTH (blue tiles) vs MOON (black, stars) glasses; Moon glass erupts at 0.08 s, ice crust from 0.45 s | "This water boils and freezes." | Title WATER / ON THE MOON?; labels EARTH · AIR: 1 BAR / MOON · AIR: ≈ 0; CALM / BOILS + FREEZES | boil + hiss, ice crack |
| 1.9–3.4 | Moon surface, Earth in the sky; the glass is set on a table among a mug, a bowl and a vase, boils on contact (2.5 s) | "Same glass, on the Moon." | — | clink, boil |
| 3.4–5.4 | air dots vanish (3.9 s); the tea erupts (4.7 s) | "Its air is trillions of times thinner." | chip MOON AIR: ≈3×10⁻¹⁵ BAR; AIR: MOON (≈ 0) | shimmer, hiss |
| 5.4–7.6 | thermometer 20 °C; soup erupts (5.9 s), vase erupts (6.9 s) | "Water boils even at room temperature." | chip NO AIR PRESSURE → BOILS AT 20 °C; FOLLOW pill 5.0–8.2 s | hiss + boil per vessel |
| 7.6–9.7 | ice crusts snap on: glass, mug, bowl, vase; thermometer 20 → 0 °C | "Boiling steals heat, so it freezes." | 20 °C → 0 °C | crack + clink per crust |
| 9.7–11.2 | close-up: ice thins, level drops, wisps rise (sublimation) | "Even the ice won't last." | — | music drops, shimmer |
| 11.2–13.8 | dark polar crater from the rim, ice patches glinting | "Except in dark craters, below minus two hundred." | -238 °C · ICE SURVIVES HERE; chip POLAR CRATERS: BELOW −238 °C | thin wind, tinkles |
| 13.8–15.0 | THE REAL SCIENCE card + red disclaimer; hook framing returns (loop) | — | card; TOMORROW: A BALLOON ON MARS; FOLLOW @the.impossible.lab | thud |

## Scene / generation notes
Blender primitives only (saved as `pipeline/reference/scene_ep18.py`): `vessel()` builds glass / mug / bowl / vase with liquid, bubbles (inside see-through water), surface drops, steam puffs and an ice disc; boil level ramps up at each vessel's start time and down at its freeze time; ice discs grow radially, then thin and sink during sublimation. Hook glass ice grows 6× thick to read at phone size. Crater = torus rim + floor disc lit by a grazing sun (6° elevation, only on in that shot) with emissive ice patches. Labels use DejaVu Sans Bold (≈ and ° glyphs).

## Caption (v2 + follow invite)
See meta.json. Share line: "Send this to the friend who always leaves a glass of water on the table." Series line: "Tomorrow: a balloon on Mars. 🔔 Follow @the.impossible.lab (or subscribe on YouTube) so you don't miss it." Disclaimer: "⚠️ Don't try this. Vacuum chambers are lab equipment, not toys: glass under vacuum can implode."
- **Cover headline:** WATER ON THE MOON?
- **Hashtags (8):** #science #physics #whatif #sciencefacts #moon #water #space #theimpossiblelab
- **YouTube / Facebook title:** What if you left a glass of water on the Moon? (46 chars)

## Alternative openings (future tests, not produced)
- A. Single glass, extreme close-up: the surface erupts and a white ice lid slams shut in 1 s (one object, no control).
- B. A hand sets the glass down on grey dust and the water "explodes" into frost on contact (E9 human scale).

## Experiment record
- **E17 (cascade middle), reel 1 of 3** (TIL-18..20). Hypothesis: a new familiar object reacting every 1–2 s between 3 and 10 s keeps viewers past the 9 s average → higher watch ratio and IG reach.
- Variable: middle structure only (cascade of 4 vessels + 4 ice crusts); everything else constant.
- Primary metric: watch ratio vs median 60 %. Secondary: IG reach at 24 h vs E5 median 1,093; hook hold vs median 62.7 %.
- Checkpoint: 24 h after publication (24 Nov 16:00 slot → 25 Nov 16:00); first E17 read at the 29 Nov weekly check.
