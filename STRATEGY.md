# Strategy, analytics and experiments

Read by the daily production run before every episode; updated by it after every run.

## Goal
Grow @the.impossible.lab (Instagram) and The Impossible Lab (YouTube Shorts) with one reel a day at **16:00 Europe/Bucharest**, improving every day from real statistics.

## KPIs (in priority order)
1. **Hook hold** = 100 − `reels_skip_rate` (Instagram). Target ≥ 70 %.
2. **Watch ratio** = `ig_reels_avg_watch_time` ÷ video length. Target ≥ 60 %.
3. **Sends** (`shares`) and **saves** per 1,000 views: the strongest growth signals.
4. Views (IG + YT) and followers (IG followers + YT subscribers).

Judge a reel at 48 h, not before. Compare against the median of all reels, not against one post.

## Playbook v1 (8 Nov 2026)
- Format: 16.5 s, 1080×1920, Blender scene built from primitives, Kokoro `af_heart` at speed 1.00. Pacing in `pipeline/config.py`, narration rules in `NARRATION.md`.
- Hook: a claim that sounds wrong but is true, spoken and shown on screen at t = 0, with the most striking visual in the first second.
- Three science beats, each with one rounded number and the reason why.
- A twist near the end that people rewatch, then THE REAL SCIENCE card with the precise values.
- On-screen: series tag "THE IMPOSSIBLE LAB · #NN", two-line title, word-by-word captions, one fact chip per beat, footer "@the.impossible.lab".
- Caption: line 1 = the hook; 3–4 short lines of the science; a comment question that asks for an opinion or prediction; a send line naming a person type; "Follow @the.impossible.lab for more impossible science."; the "⚠️ Don't try this." line; ≤ 10 hashtags.
- YouTube title: "What if you …?" style, ≤ 60 characters (the scenario appends " #Shorts").
- No drinking, brands, real people or graphic harm on screen.
- **Disclaimer on every post (Claudio, 8 Nov 2026, mandatory):** the caption carries a line starting "⚠️ Don't try this." with a premise-specific reason (e.g. "Mercury vapour is toxic"), placed just before the hashtags, and THE REAL SCIENCE card shows a one-line "Don't try this. …" in red. The YouTube description is the caption, so it carries the same line. A post without it fails QA.

## Change rule
One adjustment per day at most, logged in the experiment table with its hypothesis. Keep it for at least 3 reels before judging. On Sundays, write a weekly review and, if the evidence supports it, a new playbook version.

## Experiments
| ID | Started | Change | Hypothesis | Status / result |
|---|---|---|---|---|
| E1 | 9 Nov 2026 | 16.5 s + slower voice (speed 1.00 vs 1.10) | Clearer narration raises watch ratio | running (3 of 3 reels published at 16.5 s: TIL-02 68 %, TIL-03 59 % vs TIL-01 80 % at 15 s; first read at 48 h on 11 Nov, so far the slower/longer format holds viewers less) |
| E2 | 10 Nov 2026 00:46 (TIL-03) | Caption comment prompt as a one-tap yes/no question ("Would this ship ever make it to port? Yes or no") instead of an open opinion question | A one-tap answer lowers the effort to comment: comments > 0 per 1,000 IG views (0 so far on ~2,000 views) | 3 of 3 published; provisional fail (12 Nov: 0 comments on 973 IG views: TIL-03 0/160, TIL-04 0/169, TIL-05 0/644 at 19 h); final read 13 Nov at 48 h |
| E3 | 10 Nov 2026 19:00 (TIL-04, 3 h after the slot) | Flash-forward cold open: the first ~2 s show the climax (mannequin at the 10 m mark, high camera looking down), and the spoken + on-screen hook is a concrete number ("One second. Ten metres up.") before the story restarts from the ground | Hook hold is falling (72 → 67.5 → 61 %); opening on the payoff image + a number raises hook hold back to ≥ the median (67.5 %) | running |
| E4 | TIL-05 (11 Nov 2026, approved by Claudio) | Back to 15 s and Kokoro speed 1.10 (from 16.5 s / 1.00); E3 cold open kept | At 48 h the 15 s / 1.10 reel held better (hook 72 %, watch 80 %) than 16.5 s / 1.00 (67.5 %, 68 %), and TIL-03/04 kept falling: a tighter, faster reel lifts hook hold and watch ratio back above the median | running (TIL-05 at 21 h: hook 60.5 %, watch 60 %, ≈ median, no lift yet; TIL-06 posts 12 Nov 16:00; TIL-07, the third E4 reel, built and in READY for 13 Nov; judge on 15 Nov when all three are ≥ 48 h) → **verdict 15 Nov: no retention lift** (15 s / 1.10 mean hook 60.0 % / watch 61 % over TIL-05..07 vs 62.5 % / 63 % for 16.5 s / 1.00 over TIL-02..04; IG counts frozen after ~12 h so TIL-07 at 43 h is final). Length is not the retention lever; 15 s kept as the default (Claudio's rule; TIL-08's breakout was at 15 s). Closed. |
| E5 | TIL-08 (14 Nov 2026), 3 reels | Premise must put stakes on the viewer's own body or an everyday object/food (topic selection rule); caption v2 (E2 stopped) applied at the same time as a minor confound | Own top IG reaches (mercury 1,144, pasta 510 accounts) are body/food; competitor over-performers are body/mind/food (CAMPAIGN_LOG.md, 13 Nov): IG reach at 24 h ≥ 2× the baseline median of 136 accounts | selected 13 Nov; TIL-08 built 13 Nov (shrunk to 1 cm, in READY for 14 Nov 16:00); checkpoints 24 h / 72 h; verdict after TIL-10 at 72 h. **15 Nov early read, reel 1/3:** TIL-08 IG reach 1,090 at 19 h = 8.0× baseline (target ≥ 2×), YT 1,480 at 19 h (1.32× median); retention ≈ median (hook 63.1 %, watch 64 %). Strong positive, n = 1: running (TIL-09 15 Nov, TIL-10 16 Nov) | **16 Nov early read, reel 2/3:** TIL-09 2,132 accounts at 19.1 h = 15.7× baseline, hook hold 72.0 %, watch 74 %; 2 of 2 measured E5 reels ≥ 2× → on track; verdict 19 Nov. **19 Nov verdict: PASS** — 4 of 5 E5 reels ≥ 2× baseline at ~24 h (8.0×, 15.7×, 7.9×, 0.9×, 4.7× at 19.1 h) vs 0 of 5 non-body/food premises; competitor over-performers confirm (3 checks). **Retained as a standing topic rule** (necessary, not sufficient: TIL-11) |
| E7 | TIL-11 (17 Nov 2026), 3 reels | End card names tomorrow's experiment ("TOMORROW: <next premise>", on screen for the last ~1.5 s, spoken only if it fits the 15 s) as the single reason to return; caption series line names the same premise. Topic rule E5 kept as control | E5 reels now bring 1,000–2,100 new accounts each but convert ≈ 0.9 IG follows per 1,000 reach (1 → 4 over TIL-08/09) and 0 shares: a concrete next-episode promise gives a reason to follow | selected 16 Nov 11:09; baseline ≈ 0.9 IG follows / 1,000 reach (TIL-08+09); review at TIL-13's 72 h (22 Nov), first read 18 Nov; 19 Nov provisional: 0 follows over TIL-11+12 (766 accounts) vs control ≈ 1.2 per 1,000; end card at ~13.45 s vs avg watch ≈ 9 s |
| E13 | TIL-14 (20 Nov 2026), 3 reels | Opening visual: in the first 0.5 s the familiar object (food, body, household item) physically reacts to the impossible condition beside an Earth control — shatters, sinks, sags, chars — not a number readout or thermometer alone; hook line, length, voice, caption v2, E7 end card unchanged | TIL-11 (condition-only opening) had the lowest hook hold (53.2 %); TIL-08/09 (object visibly reacting) 63–72 %; TIL-12 (thermometers climbing, readout) 60.3 %; competitor over-performer zackdfilms drywall anchors (objects tested until they fail, 4.2×): a visible physical consequence at t = 0 lifts hook hold and reach | selected 19 Nov 11:08; primary hook hold vs median 61.1 % (target ≥ 65 % mean over 3 reels); secondary IG reach at 24 h vs E5 median 1,093; review at TIL-16 48 h (24 Nov) |

## Snapshots
| Captured (EET) | Episode | Age | IG views | IG reach | Hook hold | Avg watch s | Shares | Saves | YT views | Followers IG / subs YT |
|---|---|---|---|---|---|---|---|---|---|---|
| 8 Nov 18:42 | TIL-01 | 1.5 h | 2 | 0 | n/a | 0 | 0 | 0 | 3 | n/a / 0 |
| 8 Nov 21:53 | TIL-01 | 4.8 h | 200 | 134 | 72.5 % | 12.2 (81 % of 15 s) | 0 | 0 | 489 (13 likes) | n/a / 1 |
| 8 Nov 21:53 | TIL-02 | 0 h | 0 | 0 | n/a | 0 | 0 | 0 | 0 | n/a / 1 |
| 9 Nov 22:57 | TIL-01 | 27.8 h | 205 | 136 | 72.4 % | 12.0 (80 % of 15 s) | 0 | 0 | 1,250 (16 likes) | n/a / 2 |
| 9 Nov 22:57 | TIL-02 | 25.1 h | 1,774 | 1,144 | 67.5 % | 11.2 (68 % of 16.5 s) | 0 | 0 | 1,135 (9 likes) | n/a / 2 |
| 10 Nov 13:15 | TIL-01 | 42.1 h | 207 | 137 | 71.9 % | 12.0 (80 % of 15 s) | 0 | 0 | 1,371 (16 likes) | n/a / 2 |
| 10 Nov 13:15 | TIL-02 | 39.4 h | 1,776 | 1,146 | 67.5 % | 11.2 (68 % of 16.5 s) | 0 | 0 | 1,210 (9 likes) | n/a / 2 |
| 10 Nov 13:15 | TIL-03 | 12.5 h | 160 | 111 | 61.3 % | 9.8 (59 % of 16.5 s) | 0 | 0 | 969 (19 likes) | n/a / 2 |
| 11 Nov 01:55 | TIL-01 | 54.8 h | 207 | 137 | 71.9 % | 12.0 (80 % of 15 s) | 0 | 0 | 1,628 (17 likes) | n/a / 2 |
| 11 Nov 01:55 | TIL-02 | 52.1 h | 1,776 | 1,146 | 67.5 % | 11.2 (68 % of 16.5 s) | 0 | 0 | 1,219 (9 likes) | n/a / 2 |
| 11 Nov 01:55 | TIL-03 | 27.2 h | 160 | 111 | 61.3 % | 9.8 (59 % of 16.5 s) | 0 | 0 | 975 (19 likes) | n/a / 2 |
| 11 Nov 01:55 | TIL-04 | 6.9 h | 169 | 113 | 58.6 % | 10.3 (62 % of 16.5 s) | 0 | 0 | 382 (7 likes) | n/a / 2 |
| 11 Nov 11:08 | TIL-01 | 64.0 h | 207 | 137 | 71.9 % | 12.0 (80 % of 15 s) | 0 | 0 | 1,677 (17 likes) | n/a / 2 |
| 11 Nov 11:08 | TIL-02 | 61.3 h | 1,776 | 1,146 | 67.5 % | 11.2 (68 % of 16.5 s) | 0 | 0 | 1,222 (9 likes) | n/a / 2 |
| 11 Nov 11:08 | TIL-03 | 34.4 h | 160 | 111 | 61.3 % | 9.8 (59 % of 16.5 s) | 0 | 0 | 969 (19 likes) | n/a / 2 |
| 11 Nov 11:08 | TIL-04 | 16.1 h | 169 | 113 | 58.6 % | 10.2 (62 % of 16.5 s) | 0 | 0 | 464 (9 likes) | n/a / 2 |
| 11 Nov 13:21 | TIL-01 | 66.2 h | 207 | 137 | 71.9 % | 12.0 (80 % of 15 s) | 0 | 0 | 1,688 (17 likes) | n/a / 2 |
| 11 Nov 13:21 | TIL-02 | 63.5 h | 1,776 | 1,146 | 67.5 % | 11.2 (68 % of 16.5 s) | 0 | 0 | 1,222 (9 likes) | n/a / 2 |
| 11 Nov 13:21 | TIL-03 | 36.6 h | 160 | 111 | 61.3 % | 9.8 (59 % of 16.5 s) | 0 | 0 | 1,060 (19 likes) | n/a / 2 |
| 11 Nov 13:21 | TIL-04 | 18.3 h | 169 | 113 | 58.6 % | 10.2 (62 % of 16.5 s) | 0 | 0 | 464 (9 likes) | n/a / 2 |
| 12 Nov 11:08 | TIL-01 | 88.0 h | 207 | 137 | 71.9 % | 12.0 (80 % of 15 s) | 0 | 0 | 1,722 (17 likes) | n/a / 3 |
| 12 Nov 11:08 | TIL-02 | 85.3 h | 1,776 | 1,146 | 67.5 % | 11.2 (68 % of 16.5 s) | 0 | 0 | 1,226 (9 likes) | n/a / 3 |
| 12 Nov 11:08 | TIL-03 | 58.4 h | 160 | 111 | 61.3 % | 9.8 (59 % of 16.5 s) | 0 | 0 | 1,166 (19 likes) | n/a / 3 |
| 12 Nov 11:08 | TIL-04 | 40.1 h | 169 | 113 | 58.6 % | 10.2 (62 % of 16.5 s) | 0 | 0 | 517 (9 likes) | n/a / 3 |
| 12 Nov 11:08 | TIL-05 | 19.1 h | 644 | 465 | 60.7 % | 9.2 (61 % of 15 s) | 0 | 0 | 1,117 (13 likes) | n/a / 3 |
| 12 Nov 13:16 | TIL-01 | 90.2 h | 207 | 137 | 71.9 % | 12.0 (80 % of 15 s) | 0 | 0 | 1,729 (17 likes) | n/a / 3 |
| 12 Nov 13:16 | TIL-02 | 87.4 h | 1,776 | 1,146 | 67.5 % | 11.2 (68 % of 16.5 s) | 0 | 0 | 1,228 (9 likes) | n/a / 3 |
| 12 Nov 13:16 | TIL-03 | 60.5 h | 160 | 111 | 61.3 % | 9.8 (59 % of 16.5 s) | 0 | 0 | 1,166 (19 likes) | n/a / 3 |
| 12 Nov 13:16 | TIL-04 | 42.2 h | 169 | 113 | 58.6 % | 10.2 (62 % of 16.5 s) | 0 | 0 | 520 (9 likes) | n/a / 3 |
| 12 Nov 13:16 | TIL-05 | 21.3 h | 670 | 486 | 60.5 % | 9.0 (60 % of 15 s) | 0 | 0 | 1,117 (13 likes) | n/a / 3 |
| 13 Nov 11:08 | TIL-01 | 112.0 h | 207 | 137 | 71.9 % | 12.0 (80 % of 15 s) | 0 | 0 | 1,735 (17 likes) | 1 / 3 |
| 13 Nov 11:08 | TIL-02 | 109.3 h | 1,776 | 1,146 | 67.5 % | 11.2 (68 % of 16.5 s) | 0 | 0 | 1,225 (9 likes) | 1 / 3 |
| 13 Nov 11:08 | TIL-03 | 82.4 h | 160 | 111 | 61.3 % | 9.8 (59 % of 16.5 s) | 0 | 0 | 1,166 (19 likes) | 1 / 3 |
| 13 Nov 11:08 | TIL-04 | 64.1 h | 169 | 113 | 58.6 % | 10.2 (62 % of 16.5 s) | 0 | 0 | 528 (9 likes) | 1 / 3 |
| 13 Nov 11:08 | TIL-05 | 43.1 h | 712 | 517 | 60.8 % | 9.3 (62 % of 15 s) | 0 | 0 | 1,119 (13 likes) | 1 / 3 |
| 13 Nov 11:08 | TIL-06 | 19.1 h | 183 | 117 | 63.9 % | 10.4 (69 % of 15 s) | 0 | 0 | 5 (0 likes) | 1 / 3 |
| 13 Nov 13:15 | TIL-01 | 114.1 h | 207 | 137 | 71.9 % | 12.0 (80 % of 15 s) | 0 | 0 | 1,735 (17 likes) | 1 / 3 |
| 13 Nov 13:15 | TIL-02 | 111.4 h | 1,776 | 1,146 | 67.5 % | 11.2 (68 % of 16.5 s) | 0 | 0 | 1,226 (9 likes) | 1 / 3 |
| 13 Nov 13:15 | TIL-03 | 84.5 h | 160 | 111 | 61.3 % | 9.8 (59 % of 16.5 s) | 0 | 0 | 1,166 (19 likes) | 1 / 3 |
| 13 Nov 13:15 | TIL-04 | 66.2 h | 169 | 113 | 58.6 % | 10.2 (62 % of 16.5 s) | 0 | 0 | 528 (9 likes) | 1 / 3 |
| 13 Nov 13:15 | TIL-05 | 45.2 h | 712 | 517 | 60.8 % | 9.3 (62 % of 15 s) | 0 | 0 | 1,119 (16 likes) | 1 / 3 |
| 13 Nov 13:15 | TIL-06 | 21.2 h | 183 | 117 | 63.9 % | 10.4 (69 % of 15 s) | 0 | 0 | 5 (0 likes) | 1 / 3 |
| 14 Nov 11:08 | TIL-01 | 136.0 h | 207 | 137 | 71.9 % | 12.0 (80 % of 15 s) | 0 | 0 | 1,736 (17 likes) | 1 / 3 |
| 14 Nov 11:08 | TIL-02 | 133.3 h | 1,776 | 1,146 | 67.5 % | 11.2 (68 % of 16.5 s) | 0 | 0 | 1,230 (9 likes) | 1 / 3 |
| 14 Nov 11:08 | TIL-03 | 106.4 h | 160 | 111 | 61.3 % | 9.8 (59 % of 16.5 s) | 0 | 0 | 1,162 (19 likes) | 1 / 3 |
| 14 Nov 11:08 | TIL-04 | 88.1 h | 169 | 113 | 58.6 % | 10.2 (62 % of 16.5 s) | 0 | 0 | 520 (9 likes) | 1 / 3 |
| 14 Nov 11:08 | TIL-05 | 67.1 h | 712 | 517 | 60.8 % | 9.3 (62 % of 15 s) | 0 | 0 | 1,378 (16 likes) | 1 / 3 |
| 14 Nov 11:08 | TIL-06 | 43.1 h | 183 | 117 | 63.9 % | 10.4 (69 % of 15 s) | 0 | 0 | 8 (0 likes) | 1 / 3 |
| 14 Nov 11:08 | TIL-07 | 19.1 h | 177 | 124 | 55.6 % | 7.9 (53 % of 15 s) | 0 | 0 | 894 (11 likes) | 1 / 3 |
| 15 Nov 11:08 | TIL-01 | 160.0 h | 207 | 137 | 71.9 % | 12.0 (80 % of 15 s) | 0 | 0 | 1,736 (17 likes) | 1 / 5 |
| 15 Nov 11:08 | TIL-02 | 157.3 h | 1,776 | 1,146 | 67.5 % | 11.2 (68 % of 16.5 s) | 0 | 0 | 1,230 (9 likes) | 1 / 5 |
| 15 Nov 11:08 | TIL-03 | 130.4 h | 160 | 111 | 61.3 % | 9.8 (59 % of 16.5 s) | 0 | 0 | 1,162 (19 likes) | 1 / 5 |
| 15 Nov 11:08 | TIL-04 | 112.1 h | 169 | 113 | 58.6 % | 10.2 (62 % of 16.5 s) | 0 | 0 | 520 (9 likes) | 1 / 5 |
| 15 Nov 11:08 | TIL-05 | 91.1 h | 712 | 517 | 60.8 % | 9.3 (62 % of 15 s) | 0 | 0 | 1,384 (16 likes) | 1 / 5 |
| 15 Nov 11:08 | TIL-06 | 67.1 h | 183 | 117 | 63.9 % | 10.4 (69 % of 15 s) | 0 | 0 | 9 (0 likes) | 1 / 5 |
| 15 Nov 11:08 | TIL-07 | 43.1 h | 178 | 125 | 55.2 % | 7.9 (52 % of 15 s) | 0 | 0 | 1,048 (13 likes) | 1 / 5 |
| 15 Nov 11:08 | TIL-08 | 19.1 h | 1,544 | 1,090 | 63.1 % | 9.5 (64 % of 15 s) | 0 | 1 | 1,480 (9 likes) | 1 / 5 |
| 15 Nov 16:02 | TIL-01 | 165.0 h | 207 | 137 | 71.9 % | 12.0 (80 % of 15 s) | 0 | 0 | 1,736 (17 likes) | 1 / 5 |
| 15 Nov 16:02 | TIL-02 | 162.2 h | 1,776 | 1,146 | 67.5 % | 11.2 (68 % of 16.5 s) | 0 | 0 | 1,230 (9 likes) | 1 / 5 |
| 15 Nov 16:02 | TIL-03 | 135.3 h | 160 | 111 | 61.3 % | 9.8 (59 % of 16.5 s) | 0 | 0 | 1,162 (19 likes) | 1 / 5 |
| 15 Nov 16:02 | TIL-04 | 117.0 h | 169 | 113 | 58.6 % | 10.2 (62 % of 16.5 s) | 0 | 0 | 520 (9 likes) | 1 / 5 |
| 15 Nov 16:02 | TIL-05 | 96.0 h | 712 | 517 | 60.8 % | 9.3 (62 % of 15 s) | 0 | 0 | 1,384 (16 likes) | 1 / 5 |
| 15 Nov 16:02 | TIL-06 | 72.0 h | 183 | 117 | 63.9 % | 10.4 (69 % of 15 s) | 0 | 0 | 9 (0 likes) | 1 / 5 |
| 15 Nov 16:02 | TIL-07 | 48.0 h | 178 | 125 | 55.2 % | 7.9 (52 % of 15 s) | 0 | 0 | 1,096 (15 likes) | 1 / 5 |
| 15 Nov 16:02 | TIL-08 | 24.0 h | 1,545 | 1,093 | 63.0 % | 9.5 (63 % of 15 s) | 0 | 1 | 1,480 (9 likes) | 1 / 5 |
| 15 Nov 16:02 | TIL-09 | 1.0 h | 0 | 0 | n/a | n/a | 0 | 0 | 0 (insights not populated yet) | 1 / 5 |
| 16 Nov 11:09 | TIL-01 | 184.0 h | 208 | 138 | 71.3 % | 11.9 (80 % of 15 s) | 0 | 0 | 1,736 (17 likes) | 4 / 6 |
| 16 Nov 11:09 | TIL-02 | 181.3 h | 1,777 | 1,148 | 67.5 % | 11.2 (68 % of 16.5 s) | 0 | 0 | 1,231 (9 likes) | 4 / 6 |
| 16 Nov 11:09 | TIL-03 | 154.4 h | 161 | 112 | 61.6 % | 9.8 (60 % of 16.5 s) | 0 | 0 | 1,162 (19 likes) | 4 / 6 |
| 16 Nov 11:09 | TIL-04 | 136.1 h | 170 | 114 | 58.0 % | 10.1 (61 % of 16.5 s) | 0 | 0 | 520 (9 likes) | 4 / 6 |
| 16 Nov 11:09 | TIL-05 | 115.1 h | 714 | 519 | 60.7 % | 9.3 (62 % of 15 s) | 0 | 0 | 1,384 (16 likes) | 4 / 6 |
| 16 Nov 11:09 | TIL-06 | 91.1 h | 186 | 119 | 64.8 % | 10.4 (69 % of 15 s) | 0 | 0 | 10 (0 likes) | 4 / 6 |
| 16 Nov 11:09 | TIL-07 | 67.1 h | 180 | 127 | 55.1 % | 7.9 (52 % of 15 s) | 0 | 0 | 1,210 (15 likes) | 4 / 6 |
| 16 Nov 11:09 | TIL-08 | 43.1 h | 1,547 | 1,093 | 63.1 % | 9.5 (63 % of 15 s) | 0 | 1 | 1,657 (9 likes) | 4 / 6 |
| 20 Nov 16:02 | TIL-07 | 168.0 h | 180 | 127 | 55.1 % | 7.8 (52 % of 15 s) | 0 | 0 | 1,209 (15 likes) | 6 / 7 |
| 20 Nov 16:02 | TIL-08 | 144.0 h | 1,548 | 1,093 | 63.0 % | 9.5 (63 % of 15 s) | 0 | 1 | 1,688 (9 likes) | 6 / 7 |
| 20 Nov 16:02 | TIL-09 | 120.0 h | 3,285 | 2,149 | 72.1 % | 11.1 (74 % of 15 s) | 0 | 0 | 1,466 (7 likes) | 6 / 7 |
| 20 Nov 16:02 | TIL-10 | 93.2 h | 1,534 | 1,079 | 61.0 % | 9.0 (60 % of 15 s) | 0 | 0 | 1,121 (9 likes) | 6 / 7 |
| 20 Nov 16:02 | TIL-11 | 70.3 h | 156 | 124 | 53.2 % | 6.2 (41 % of 15 s) | 0 | 0 | 551 (2 likes) | 6 / 7 |
| 20 Nov 16:02 | TIL-12 | 48.0 h | 968 | 749 | 61.1 % | 9.0 (60 % of 15 s) | 0 | 0 | 928 (7 likes) | 6 / 7 |
| 20 Nov 16:02 | TIL-13 | 24.0 h | 1,545 | 1,100 | 66.0 % | 8.6 (58 % of 15 s) | 0 | 0 | 1,040 (9 likes, 1 comment) | 6 / 7 |
| 20 Nov 16:02 | TIL-14 | 0.02 h | 0 | 0 | n/a | 0 | 0 | 0 | 0 | 6 / 7 |
| 16 Nov 11:09 | TIL-09 | 19.1 h | 3,259 | 2,132 | 72.0 % | 11.1 (74 % of 15 s) | 0 | 0 | 1,384 (7 likes) | 4 / 6 |
| 21 Nov 11:08 | TIL-01 | 304.0 h | 210 | 139 | 71.0 % | 11.8 (79 % of 15 s) | 0 | 0 | 1,738 (17 likes) | 6 / 7 |
| 21 Nov 11:08 | TIL-02 | 301.3 h | 1,779 | 1,150 | 67.5 % | 11.2 (68 % of 16.5 s) | 0 | 0 | 1,237 (9 likes) | 6 / 7 |
| 21 Nov 11:08 | TIL-03 | 274.4 h | 162 | 113 | 61.1 % | 9.7 (59 % of 16.5 s) | 0 | 0 | 1,162 (19 likes) | 6 / 7 |
| 21 Nov 11:08 | TIL-04 | 256.1 h | 171 | 115 | 57.5 % | 10.0 (61 % of 16.5 s) | 0 | 0 | 520 (9 likes) | 6 / 7 |
| 21 Nov 11:08 | TIL-05 | 235.1 h | 716 | 521 | 60.7 % | 9.3 (62 % of 15 s) | 0 | 0 | 1,383 (16 likes) | 6 / 7 |
| 21 Nov 11:08 | TIL-06 | 211.1 h | 186 | 120 | 64.8 % | 10.4 (69 % of 15 s) | 0 | 0 | 11 (0 likes) | 6 / 7 |
| 21 Nov 11:08 | TIL-07 | 187.1 h | 180 | 127 | 55.1 % | 7.8 (52 % of 15 s) | 0 | 0 | 1,210 (15 likes) | 6 / 7 |
| 21 Nov 11:08 | TIL-08 | 163.1 h | 1,548 | 1,093 | 63.0 % | 9.5 (63 % of 15 s) | 0 | 1 | 1,691 (10 likes) | 6 / 7 |
| 21 Nov 11:08 | TIL-09 | 139.1 h | 3,285 | 2,149 | 72.1 % | 11.1 (74 % of 15 s) | 0 | 0 | 1,471 (8 likes) | 6 / 7 |
| 21 Nov 11:08 | TIL-10 | 112.3 h | 1,534 | 1,079 | 61.0 % | 9.0 (60 % of 15 s) | 0 | 0 | 1,122 (10 likes) | 6 / 7 |
| 21 Nov 11:08 | TIL-11 | 87.4 h | 156 | 124 | 53.2 % | 6.2 (41 % of 15 s) | 0 | 0 | 549 (2 likes) | 6 / 7 |
| 21 Nov 11:08 | TIL-12 | 67.1 h | 968 | 749 | 61.1 % | 9.0 (60 % of 15 s) | 0 | 0 | 927 (8 likes) | 6 / 7 |
| 21 Nov 11:08 | TIL-13 | 43.1 h | 1,552 | 1,108 | 65.9 % | 8.6 (58 % of 15 s) | 0 | 0 | 1,067 (10 likes, 1 comment) | 6 / 7 |
| 21 Nov 11:08 | TIL-14 | 19.1 h | 413 | 295 | 68.4 % | 7.9 (52 % of 15 s) | 0 | 0 | 1,276 (9 likes) | 6 / 7 |
| 21 Nov 16:02 | TIL-08 | 168.0 h | 1,548 | 1,093 | 63.0 % | 9.5 (63 % of 15 s) | 0 | 1 | 1,692 (10 likes) | 6 / 7 |
| 21 Nov 16:02 | TIL-12 | 72.0 h | 968 | 749 | 61.1 % | 9.0 (60 % of 15 s) | 0 | 0 | 927 (8 likes) | 6 / 7 |
| 21 Nov 16:02 | TIL-13 | 48.0 h | 1,554 | 1,110 | 65.8 % | 8.6 (58 % of 15 s) | 0 | 0 | 1,068 (10 likes, 1 comment) | 6 / 7 |
| 21 Nov 16:02 | TIL-14 | 24.0 h | 444 | 327 | 66.7 % | 7.7 (51 % of 15 s) | 0 | 0 | 1,276 (9 likes) | 6 / 7 |
| 21 Nov 16:02 | TIL-15 | 0.03 h | 0 | 0 | n/a | 0 | 0 | 0 | 0 | 6 / 7 |
| 22 Nov 17:47 | TIL-09 | 169.8 h | 3,285 | 2,149 | 72.1 % | 11.1 (74 % of 15 s) | 0 | 0 | 1,478 (8 likes) | 6 / 7 |
| 22 Nov 17:47 | TIL-13 | 73.8 h | 1,564 | 1,117 | 65.4 % | 8.6 (57 % of 15 s) | 0 | 0 | 1,081 (10 likes, 1 comment) | 6 / 7 |
| 22 Nov 17:47 | TIL-14 | 49.8 h | 445 | 328 | 66.8 % | 7.7 (51 % of 15 s) | 0 | 0 | 1,292 (9 likes) | 6 / 7 |
| 22 Nov 17:47 | TIL-15 | 25.8 h | 1,730 | 1,211 | 64.8 % | 12.6 (84 % of 15 s) | 0 | 0 | 583 (7 likes) | 6 / 7 |
| 22 Nov 17:47 | TIL-16 | 0.02 h | 0 | 0 | n/a | 0 | 0 | 0 | 0 | 6 / 7 |
| 24 Nov 16:02 | TIL-13 | 120.0 h | 1,569 | 1,122 | 65.3 % | 8.6 (57 % of 15 s) | 0 | 0 | 1,088 (10 likes, 1 comment) | 6 / 8 |
| 24 Nov 16:02 | TIL-14 | 96.0 h | 445 | 328 | 66.8 % | 7.6 (51 % of 15 s) | 0 | 0 | 1,309 (9 likes) | 6 / 8 |
| 24 Nov 16:02 | TIL-15 | 72.0 h | 1,731 | 1,212 | 64.8 % | 12.6 (84 % of 15 s) | 0 | 0 | 659 (9 likes) | 6 / 8 |
| 24 Nov 16:02 | TIL-16 | 46.3 h | 1,659 | 1,155 | 62.3 % | 8.6 (58 % of 15 s) | 0 | 0 | 307 (3 likes) | 6 / 8 |
| 24 Nov 16:02 | TIL-17 | 19.5 h | 785 | 580 | 62.3 % | 8.5 (56 % of 15 s) | 0 | 0 | 605 (6 likes) | 6 / 8 |
| 24 Nov 16:02 | TIL-18 | 0.03 h | 0 | 0 | n/a | 0 | 0 | 0 | 0 | 6 / 8 |

## Findings log
- **9 Nov (run for TIL-03), reels < 48 h old, provisional:**
  1. Instagram distribution is one burst: TIL-02 went 1,771 → 1,774 views between 13:19 and 22:57 EET, TIL-01 has been flat at ~205 since its first evening. The first hours decide reach, so the 16:00 slot matters.
  2. TIL-02 reached 8.4× more accounts than TIL-01 (1,144 vs 136) but held them less (hook hold 67.5 % vs 72.4 %, watch ratio 68 % vs 80 %). E1 is not judgeable yet (n = 2, different reach pools).
  3. Zero shares, saves and comments across ~2,000 IG views: engagement, not reach, is the bottleneck. YouTube delivers similar volume (2,385 views, 1.0–1.3 % likes).
- **Today's adjustment:** E2 (yes/no comment prompt). TIL-03 was published at 00:46 EET on 10 Nov, 8 h 46 min after the 16:00 slot (the run itself started at ~22:56 EET); treat its reach as confounded by the night slot.

- **10 Nov (run for TIL-04), oldest reel 42 h, still provisional (no reel ≥ 48 h):**
  1. Hook hold and watch ratio fall with every episode: hook hold 71.9 → 67.5 → 61.3 %, watch ratio 80 → 68 → 59 % (TIL-01 → 03; median 67.5 % / 68 %). TIL-03 is the weakest on both, but it went out at 00:46 EET, so its audience pool is confounded.
  2. YouTube now out-delivers Instagram: 3,550 vs 2,143 views in total. TIL-03 took 969 YT views and 19 likes (2.0 %, best like rate) in 12.5 h despite the night slot, while IG gave it 160 views. IG reach stays a one-burst lottery (TIL-02 1,146 accounts, TIL-01 137, TIL-03 111).
  3. Still zero shares, saves and comments on IG across 2,143 views (E2 so far: 0 comments on 160 views, too small to judge).
- **Today's adjustment:** E3 (flash-forward cold open + number hook) aimed at KPI #1, hook hold. Everything else unchanged (16.5 s, one-tap comment prompt kept for E2). TIL-04 went out at 19:00 EET, 3 h after the 16:00 slot (the run stalled during the pre-publish wait), so its reach is partly confounded too.

- **11 Nov 01:55 (stats check), TIL-01/02 now ≥ 48 h:**
  1. Instagram stalls at ~110–140 accounts for every reel except TIL-02 (1,146). Hook hold alone does not explain it (TIL-01 had the best hold, 71.9 %, and the lowest reach); TIL-02's premise was the most visceral ("You can't drown in this pool"). Topic appeal looks like the reach lever; hook hold the gate.
  2. E3 shows no lift yet: TIL-04 hook hold 58.6 % at 7 h (lowest; median of 4 = 64.4 %), watch ratio 62 % (TIL-03: 59 %). Posted 3 h late, so one confounded data point; the rule says 3 reels before judging.
  3. YouTube: 4,204 views vs Instagram 2,312 (total 6,516). Whisky (TIL-01) still gains (+257 in 13 h): YouTube has a long tail, Instagram does not.
  4. E1 at 48 h (n = 1 vs 1): 15 s / speed 1.10 held better (72 % hold, 80 % watch) than 16.5 s / speed 1.00 (67.5 %, 68 %), and TIL-03/04 keep falling. Not reverting: the slower, longer format is Claudio's explicit request. Flagged to him as a decision.

NEXT BUILD INSTRUCTION (from 11 Nov 01:55 check): keep E3 (cold open on the climax + number/claim hook) and E2 (one-tap comment prompt) for TIL-05; change nothing else. Publish on time at 16:00 (two of the last three reels were late, which confounds every comparison). Topic: the queue's next item is fine; when choosing between equivalent premises, prefer the most visceral one (familiar danger, "you can't…" claim).

- **11 Nov (Claudio's decisions):** (1) a daily light stats check now runs at 11:07 EET and writes the NEXT BUILD INSTRUCTION; (2) test going back to 15 s / speed 1.10 (E4); (3) buffer-first publishing: the daily run publishes the reel in EPISODES.md → READY TO PUBLISH at 16:00, then builds the next one into READY. E3 can no longer be judged on its own: from TIL-05 it is confounded with E4.

NEXT BUILD INSTRUCTION (from 11 Nov 01:55 check, updated after Claudio's decisions): build at 15 s / speed 1.10 (E4), keep the cold open on the climax with a claim hook (E3) and the one-tap comment prompt (E2); no other change. Prefer the most visceral premise among equivalent ones.

- **11 Nov 11:08 (daily stats check):** total 6,644 views (IG 2,312 + YT 4,332), +128 since 01:55, all from YouTube; 2 YT subscribers, IG followers not available.
  1. Instagram is frozen: 0 new views on all four reels in 9 h. Every reel's IG life is the first ~12 h; after that, only YouTube grows (whisky +49, gravity +82 in 9 h).
  2. TIL-04 (gravity, E3 cold open) is the weakest reel at a comparable age on both platforms: YT 464 at 16 h vs ~1,000–1,130 for TIL-02/03 at 12–15 h (≈ 0.45×), IG hook hold 58.6 % (lowest; median 64.4 %). One late-posted data point, and E3 is now confounded with E4 from TIL-05, so no verdict on E3.
  3. E2 (one-tap comment prompt): 0 comments on 329 IG views across TIL-03/04 (2 of 3 reels); TIL-05 completes it. Engagement is still zero on IG (0 shares, saves, comments on 2,312 views).

NEXT BUILD INSTRUCTION (from 11 Nov 11:08 check): keep current. Build TIL-06 exactly as TIL-05 (15 s / speed 1.10 for E4, cold open on the climax with a claim hook, one-tap comment prompt); no new change until E4 has 3 reels. Hypothesis unchanged: the tighter 15 s reel lifts hook hold and watch ratio above the median (64.4 % / 65 %). Publish TIL-05 on time at 16:00.

- **11 Nov 13:21 (daily production run):** total 6,746 views (IG 2,312 + YT 4,434), +102 since 11:08, all YouTube.
  1. YouTube's long tail reaches older reels unevenly: honey (TIL-03) jumped 969 → 1,060 in 2 h after being flat for a day, while gravity (TIL-04) stayed at 464. Instagram is unchanged for every reel (frozen after ~12 h).
  2. No new IG evidence: still 0 shares, saves and comments on 2,312 views; TIL-05 (first E4 reel, posting 16:00 today) is the next data point.
- **TIL-05 published on time** at 16:00:15 EET (Make exec 1ab7499172db4e17a0eb3da4fd74e9fb, IG DfmpWn_pbJK, YT YFPL9A8-KX0): first E4 reel and the first post exactly in the slot, so it is also the first clean timing data point. E2 is now complete (3 reels); judge it at 48 h (13 Nov).
- **Adjustment applied:** none (NEXT BUILD INSTRUCTION "keep current" followed). TIL-06 built exactly like TIL-05: 15 s / speed 1.10 (E4), cold open on the climax with a claim hook (E3: the finish-line sprint, "A marathon in two minutes."), one-tap comment prompt (E2 style: "Could anyone survive the first kilometre? Yes or no"). Topic: queue #5/#6 skipped for #7 (marathon at the speed of sound), the most visceral premise with every number computable; friction-off still lacks a clean number per beat.

- **12 Nov 11:08 (daily stats check):** total 8,704 views (IG 2,956 + YT 5,748), +1,958 since 11 Nov 13:21 (IG +644, YT +1,314); YT subscribers 2 → 3; IG followers not available.
  1. TIL-05 (pasta on Mars, first on-time 16:00 post, first E4 reel) is the 2nd-best IG reel: 644 views / 465 accounts at 19 h, 3.1× the IG median (207) and 4× TIL-03/04; YT 1,117 at 19 h, in line with TIL-01/02 (~1,130–1,250 at 18–25 h). Reach improved, retention did not: hook hold 60.7 % (median of 5 = 61.3 %), watch ratio 61 % (median 62 %). The lift looks like slot/topic, not the 15 s format; n = 1, so E4 is not judged yet.
  2. Retention has not recovered with E4: 15 s / 1.10 alone did not bring hook hold back to TIL-01's 72 %. The open is now the suspect (the last three reels all open on a cold-open/claim and all sit at 59–61 %).
  3. Engagement is still zero: 0 shares, 0 saves, 0 comments on 2,956 IG views; E2 (one-tap yes/no prompt) has 0 comments on 973 IG views over its 3 reels → provisional fail, final read at 48 h tomorrow (13 Nov).

NEXT BUILD INSTRUCTION (from 12 Nov 11:08 check): keep current. Build TIL-07 exactly like TIL-05/06 (15 s / speed 1.10, cold open on the climax with a claim hook, one-tap comment prompt): TIL-07 is E4's third reel, so no new change. Topic: prefer a familiar everyday object or act in an impossible setting (pool, pasta: the two best IG reaches); from the queue, #13 basketball on the Moon or #6 shrunk to 1 cm, whichever has every number verifiable. Publish TIL-06 on time at 16:00 (on-time posting is the one variable that coincided with better reach). Planned next change after E4's read (14 Nov): retention (hook) or engagement (prompt), decided on the data.

- **12 Nov 13:16 (daily production run):** total 8,742 views (IG 2,982 + YT 5,760), +38 since 11:08; YT subscribers 3; IG followers not available.
  1. TIL-05 is the only reel still gaining on Instagram after 12 h (644 → 670 views, 465 → 486 accounts in 2 h, hook hold 60.5 %, watch ratio 60 %); every older reel stayed frozen. A slow IG tail exists only for the on-time 16:00 post, a further hint that the slot matters.
  2. YouTube was flat in the last 2 h (+38 views in total, TIL-05 unchanged at 1,117): YT counts appear to refresh in batches, so compare YT only across captures ≥ 12 h apart.
  3. Engagement still zero: 0 shares, 0 saves, 0 comments on 2,982 IG views.
- **TIL-06 published on time** at 16:00:07 EET (Make exec a1872f54522c4a3bb9f041704b30fdf7, SUCCESS, 5 operations; IG DfpOOiYlRDP, YT nV-sE7p3f4w): second consecutive on-time post from the READY buffer; E4 reel 2 of 3.
- **Adjustment applied:** none (NEXT BUILD INSTRUCTION "keep current" followed). TIL-07 built exactly like TIL-05/06: 15 s / speed 1.10 (E4's third reel), cold open on the climax with a claim hook ("You'd jump over the hoop.", player hovering 6 m up, feet above the rim), one-tap comment prompt ("Could you still sink a free throw up there? Yes or no"). Topic: queue #13 basketball on the Moon (familiar everyday act in an impossible setting, every number verifiable; set in an air-filled dome so no suit is needed and the free-throw range includes air drag).

- **13 Nov 08:10 (Claudio's creative-director brief, BRIEF.md):** campaign log started (CAMPAIGN_LOG.md: checkpoints 24 h / 72 h / 7 d, competitor group via Make 8550000, experiment backlog). Competitor check: over-performers in the peer group are about the viewer's own body, mind or food; space "what ifs" sit at the median. E2 stopped (0 comments on ~1,000 IG views). Caption v2 from TIL-08.

NEXT BUILD INSTRUCTION (from 13 Nov 08:10 brief run): build TIL-08 as E5: premise with stakes for the viewer's own body or an everyday object/food (queue reordered: shrunk to 1 cm, pool of olive oil, coffee the size of a lake lead). Keep 15 s / 1.10, cold open on the climax, 16:00. Caption v2 (see CAMPAIGN_LOG.md → Decisions): no yes/no prompt, no "Follow … for more"; one share line + one series line + disclaimer. Write episodes/NN-<slug>/brief.md with the BRIEF.md §6 deliverables (5 hooks + winner, timestamped script, evidence table, 2 alternative openings, experiment record). Primary metric: IG reach at 24 h vs baseline 136 accounts.

- **13 Nov 11:08 (daily stats check):** total 8,985 views (IG 3,207 + YT 5,778), +243 since 12 Nov 13:16 (IG +225: TIL-06 +183, TIL-05 +42; YT +18). Followers IG 1 / YT subs 3 (unchanged). Competitor check not due (Mon/Thu).
  1. **YouTube stalled channel-wide (confidence medium):** +18 views in ~21 h across all six Shorts, and TIL-06 has **5 YT views at 19 h** vs a 24 h median of 1,118 (TIL-01..05 all had 380–1,250 by 7–25 h). Channel views (5,778) equal the sum of the six videos, so the API is consistent; YT batch-refresh lag cannot explain 21 h. Cause not visible from the API (possible: limited distribution / visibility or "made for kids" setting on the TIL-06 upload, or a channel-level throttle). Needs a check in YouTube Studio by Claudio.
  2. **TIL-06 IG (marathon, non-body premise):** 183 views / 117 accounts at 19 h = 0.86× the 24 h reach baseline (136), flat since ~16 h. Best retention since TIL-01 (hook hold 63.9 %, watch ratio 69 %) but no reach: consistent with the E5 hypothesis that topic, not retention, gates IG reach (n = 1, low confidence).
  3. TIL-05 (pasta) is the only reel with an IG tail (670 → 712 views, 486 → 517 accounts in 21 h). Engagement still zero: 0 shares, 0 saves, 0 comments on 3,207 IG views (likes 20 total).
- E4 early read (verdict 15 Nov, TIL-07 still unpublished): TIL-05 hook 60.8 % / watch 62 %, TIL-06 63.9 % / 69 % vs median of 6 reels 62.6 % / 65 %: no clear lift yet.

NEXT BUILD INSTRUCTION (from 13 Nov 11:08 check): keep current. Build TIL-08 as E5 exactly as set in the 13 Nov 08:10 instruction (first queue topic A "shrunk to 1 cm", caption v2, 15 s / 1.10, cold open, 16:00); no extra variable. After publishing TIL-07 at 16:00, confirm the YouTube upload is public and record its first YT count; if TIL-07 also stays < 50 YT views by the next check, YouTube distribution is broken, not the content.

- **13 Nov 13:15 (daily production run):** total 8,986 views (IG 3,207 + YT 5,779), +1 since 11:08 (YT); IG followers 1, YT subscribers 3.
  1. Instagram is frozen on all six reels (identical counts to the 11:08 capture); TIL-06 (marathon) ends its IG burst at 117 accounts (0.86× the 136 baseline) despite the best retention since TIL-01 (hook hold 63.9 %, watch ratio 69 %). Retention without a body/food premise did not buy reach (n = 1, low confidence; supports E5).
  2. YouTube still stalled: TIL-06 at 5 views at 21 h. The publishing scenario (8451092) uploads with privacyStatus = public, selfDeclaredMadeForKids = false, notifySubscribers = true, containsSyntheticMedia = true, category 28: identical for TIL-01..05, which all got 380–1,250 views in the first day, so the Make settings are not the cause. Remaining suspects are on YouTube's side (Studio restrictions/visibility on nV-sE7p3f4w, or a channel-level distribution drop). TIL-07 at 16:00 is the test.
  3. Engagement unchanged: 0 shares, 0 saves, 0 comments on 3,207 IG views (likes 20).
- **Adjustment applied:** none beyond the NEXT BUILD INSTRUCTION (E5 started): TIL-08 = queue topic A "shrunk to 1 cm tall", 15 s / 1.10, cold open on the hook image (balance already tipping toward the raindrop at t = 0), caption v2, brief in episodes/08-shrunk-1cm/brief.md. Today's numbers do not contradict the instruction.

- **14 Nov 11:08 (daily stats check):** total 10,312 views (IG 3,384 + YT 6,928), +1,326 since 13 Nov 13:15 (IG +177, all TIL-07; YT +1,149: TIL-07 +894, TIL-05 +259). IG followers 1 / YT subs 3 (unchanged: zero follower conversion so far). Competitor check not due (Mon/Thu). TIL-07 publish confirmed: Make exec 4a57507ad5da42e08b9b204da522ad07 SUCCESS (ended 16:01:14 EET), IG Dfry8LwiPLm, YT CH-vb3eFBFI.
  1. **YouTube is not broken channel-wide (confidence medium-high):** TIL-07 took 894 YT views in 19 h (0.80× the 24 h median 1,118) and TIL-05 resumed (+259). TIL-06 is the only stuck video: 8 YT views at 43 h. The problem is specific to nV-sE7p3f4w (same upload settings as every other reel), so the Studio check on that one video is still Claudio's decision; nothing to change in the pipeline.
  2. **TIL-07 (basketball on the Moon, space premise) has the weakest retention ever:** hook hold 55.6 % (median of 7 = 61.3 %), watch ratio 53 % (median 62 %); IG reach 124 = 0.91× baseline 136 at 19 h. Second consecutive non-body premise at/below baseline reach (TIL-06 0.86×). Supports E5's topic hypothesis (n = 2 negatives vs 2 body/food positives; low-medium confidence).
  3. **E4 provisional (verdict at 48 h, 15 Nov):** the three 15 s / 1.10 reels (TIL-05/06/07) hold 60.1 % hook / 61 % watch on average vs 62.5 % / 63 % for the three 16.5 s / 1.00 reels (TIL-02..04): no lift. IG counts freeze after ~12 h, so this is unlikely to change. Length is Claudio's standing rule: decision for him (keep 15 s for simplicity, or accept that length is not the lever and move the next experiment to the opening/topic). Engagement still 0 shares / 0 saves / 0 comments on 3,384 IG views.

NEXT BUILD INSTRUCTION (from 14 Nov 11:08 check): keep current. E5 is running (TIL-08 publishes at 16:00 today = reel 1 of 3); build TIL-09 as E5 reel 2: queue topic B (pool of olive oil) or D (toast on Venus), whichever has every number verified; 15 s / 1.10, cold open on the hook image, caption v2, 16:00. No new variable until E5 has 3 reels (TIL-08..10, review 18 Nov after TIL-10's 24 h). Primary metric: IG reach at 24 h vs baseline 136 accounts; secondary: hook hold vs median 61.3 %.

- **14 Nov 13:12 (daily production run):** total 10,313 views (IG 3,385 + YT 6,928), +1 since 11:08 (IG, TIL-07); IG followers 1, YT subscribers 3.

| Reel | Age | IG views | IG reach | Hook hold | Avg watch | Watch ratio | Shares / saves | YT views |
|---|---|---|---|---|---|---|---|---|
| TIL-01 whisky | 6.0 d | 207 | 137 | 71.9 % | 12.0 s | 80 % | 0 / 0 | 1,736 |
| TIL-02 mercury | 5.9 d | 1,776 | 1,146 | 67.5 % | 11.2 s | 68 % | 0 / 0 | 1,230 |
| TIL-03 honey | 4.6 d | 160 | 111 | 61.3 % | 9.8 s | 59 % | 0 / 0 | 1,162 |
| TIL-04 gravity | 3.8 d | 169 | 113 | 58.6 % | 10.2 s | 62 % | 0 / 0 | 520 |
| TIL-05 pasta | 2.9 d | 712 | 517 | 60.8 % | 9.3 s | 62 % | 0 / 0 | 1,378 |
| TIL-06 marathon | 1.9 d | 183 | 117 | 63.9 % | 10.4 s | 69 % | 0 / 0 | 8 |
| TIL-07 basketball | 21.2 h | 178 | 125 | 55.2 % | 7.9 s | 52 % | 0 / 0 | 894 |
  1. No new evidence since the 11:08 check: Instagram is frozen on every reel (TIL-07 ends its burst at 125 accounts = 0.92× baseline, the third non-body premise in a row at or below baseline), YouTube counts unchanged (batch refresh). Findings from 11:08 stand; nothing contradicts the NEXT BUILD INSTRUCTION.
  2. Retention keeps sliding on the 15 s format (TIL-07 hook hold 55.2 % at 21 h, lowest ever) while reach follows topic: consistent with E5, and with E9 (open on a human body in the first frame) as the next retention test once E5 closes.
- **TIL-08 published on time** at 16:00:02 EET (Make exec 0bc079057dfb49d3b660793c3c6afba4, SUCCESS, 5 operations; IG DfuXtOHk5bT, YT H-dUAmQbBeg): E5 reel 1 of 3, first caption-v2 reel.
- **Adjustment applied:** none (NEXT BUILD INSTRUCTION followed). TIL-09 = E5 reel 2: queue B "swimming in a pool of olive oil" (chosen over D "toast on Venus": every number verified, and it is the buoyancy family of the best reel, TIL-02). 15 s / 1.10, cold open on a proof image (water vs oil tanks with the person visibly sinking; in-scene labels readable without sound), caption v2, 16:00 on 15 Nov. E5 status: running, 1 of 3 live; review 18 Nov after TIL-10's 24 h.

- **15 Nov 11:08 (daily stats check, Sunday):** total **13,498 views** (IG 4,929 + YT 8,569), **+3,185** since 14 Nov 13:12 (IG +1,544, all TIL-08; YT +1,641: TIL-08 +1,480, TIL-07 +153, TIL-05 +6, TIL-06 +1). YT subscribers 3 → **5**; IG followers 1 (unchanged). Competitor check not due (Mon/Thu). Data store 250779 trimmed (snapshots before 14 Nov, 42 records, removed; newest per media kept).

| Reel | Age | IG views | IG reach | Hook hold | Avg watch | Watch ratio | Shares / saves / comments | per 1,000 reach | YT views |
|---|---|---|---|---|---|---|---|---|---|
| TIL-01 whisky | 160 h | 207 | 137 | 71.9 % | 12.0 s | 80 % | 0 / 0 / 0 | 0 / 0 / 0 | 1,736 |
| TIL-02 mercury | 157 h | 1,776 | 1,146 | 67.5 % | 11.2 s | 68 % | 0 / 0 / 0 | 0 / 0 / 0 | 1,230 |
| TIL-03 honey | 130 h | 160 | 111 | 61.3 % | 9.8 s | 59 % | 0 / 0 / 0 | 0 / 0 / 0 | 1,162 |
| TIL-04 gravity | 112 h | 169 | 113 | 58.6 % | 10.2 s | 62 % | 0 / 0 / 0 | 0 / 0 / 0 | 520 |
| TIL-05 pasta | 91 h | 712 | 517 | 60.8 % | 9.3 s | 62 % | 0 / 0 / 0 | 0 / 0 / 0 | 1,384 |
| TIL-06 marathon | 67 h | 183 | 117 | 63.9 % | 10.4 s | 69 % | 0 / 0 / 0 | 0 / 0 / 0 | 9 |
| TIL-07 basketball | 43 h | 178 | 125 | 55.2 % | 7.9 s | 52 % | 0 / 0 / 0 | 0 / 0 / 0 | 1,048 |
| **TIL-08 shrunk 1 cm** | **19 h** | **1,544** | **1,090** | 63.1 % | 9.5 s | 64 % | 0 / **1** / 0 | 0 / 0.9 / 0 | **1,480** |
Medians (TIL-01..07): hook hold 61.3 %, watch ratio 62 %; 24 h IG reach baseline 136, YT 24 h 1,118.
  1. **Breakout: TIL-08 (E5 reel 1, "Big raindrops weigh more than you.")** — 1,090 accounts reached at 19 h = **8.0× the 136 baseline** (and ≈ TIL-02's 1,146 lifetime), 1,544 IG views; YT 1,480 at 19 h = 1.32× median, best YT start so far; first save ever; YT subs +2. Retention only ≈ median (hook 63.1 % vs 61.3 %, watch 64 % vs 62 %), so the lift is distribution/topic, not hold. Confidence: medium that "you vs a familiar object" premises drive reach (now 3 of 3 top IG reaches: mercury pool, pasta, shrunk-you; the other five premises all at 0.8–1.0× baseline), low on its size (one exceptional result is not a pattern; TIL-09/10 decide).
  2. **Follower conversion is the new bottleneck (confidence medium):** 1,090 new accounts reached and IG followers stayed at 1; 0 shares on 4,929 IG views across 8 reels. Reach can now be bought with the premise; nothing gives a viewer a reason to follow. This is the case for E7 (series teaser end card) after E5.
  3. **E4 verdict: no retention lift from 15 s / 1.10** (TIL-05..07 hook 60.0 % / watch 61 % vs 62.5 % / 63 % at 16.5 s). Length is not the lever; recommend keeping 15 s (simpler, breakout happened at 15 s). TIL-06 still stuck on YouTube (9 views at 67 h): Studio check on nV-sE7p3f4w still open for Claudio.
- Experiment ideas from finding 1 (backlog in CAMPAIGN_LOG.md): (a) E5 continues unchanged (TIL-09, TIL-10) — selected; (b) E10 hook pattern "<familiar object> weighs/is more than you" (viewer-vs-object comparison in the first line); (c) E7 series end card to convert the new reach into follows. One variable at a time: finish E5 first.

NEXT BUILD INSTRUCTION (from 15 Nov 11:08 check): keep current. E5 reel 3 = TIL-10 (built today, publishes 16 Nov 16:00): take queue item F "You, 10× taller" (new, top of queue: the viewer's own body at an impossible scale, the TIL-08 family; square-cube numbers) if every number verifies cleanly; otherwise C (coffee the size of a lake). 15 s / 1.10, cold open on a proof image, caption v2, 16:00. No other change. Primary metric: IG reach at 24 h vs baseline 136 (E5 target ≥ 272); secondary: hook hold vs median 61.3 %. E5 verdict at TIL-10's 72 h (19 Nov); next experiment candidate E7 (series teaser) to attack follower conversion.

### Production run 15 Nov 2026 (13:12–16:15 EET)
- **Snapshot 16:02:** totals 13,547 views (IG 4,930 + YT 8,617); followers IG 1 / YT 5. TIL-08 24 h checkpoint confirmed: 1,093 accounts (8.0× baseline), hook hold 63.0 %, watch ratio 63 %, 1 save. Older reels frozen on IG; TIL-07 YT +48 since 13:14.
- **Findings:** 1. No new evidence since the 11:08 check; the 11:08 findings stand (TIL-08 breakout driven by premise, not retention; follower conversion is the bottleneck). 2. TIL-07 at 48 h is the clearest non-body control: 125 accounts (0.92× baseline) with the lowest hook hold (55.2 %), consistent with E5. Confidence unchanged (low–medium).
- **Adjustment applied:** none (NEXT BUILD INSTRUCTION followed). TIL-10 = E5 reel 3: queue F "You, 10× taller" (every number verified: Haldane 1926; Biewener 1991 peak bone stress 40–80 MPa, safety factor ≈3–4). 15 s / 1.10, cold open on a proof image (17.5 m giant running past rooftops, red shins), caption v2, 16:00 on 16 Nov. E5 status: running, 2 of 3 live (TIL-08, TIL-09); verdict 19 Nov at TIL-10's 72 h.

- **16 Nov 11:09 (daily stats check, Monday):** total **18,496 views** (IG 8,202 + YT 10,294), **+4,949** since 15 Nov 16:02 (IG +3,272: TIL-09 +3,259, older reels +13; YT +1,677: TIL-09 +1,384, TIL-08 +177, TIL-07 +114, TIL-02 +1, TIL-06 +1). **IG followers 1 → 4** (first growth), YT subscribers 5 → 6. Competitor check done (CAMPAIGN_LOG.md, group change −physicsfun +astrumspace). Data store 250779 trimmed 98 → 68.

| Reel | Age | IG views | IG reach | Hook hold | Avg watch | Watch ratio | Shares / saves / comments | per 1,000 reach | YT views |
|---|---|---|---|---|---|---|---|---|---|
| TIL-01 whisky | 184 h | 208 | 138 | 71.3 % | 11.9 s | 80 % | 0 / 0 / 0 | 0 / 0 / 0 | 1,736 |
| TIL-02 mercury | 181 h | 1,777 | 1,148 | 67.5 % | 11.2 s | 68 % | 0 / 0 / 0 | 0 / 0 / 0 | 1,231 |
| TIL-03 honey | 154 h | 161 | 112 | 61.6 % | 9.8 s | 60 % | 0 / 0 / 0 | 0 / 0 / 0 | 1,162 |
| TIL-04 gravity | 136 h | 170 | 114 | 58.0 % | 10.1 s | 61 % | 0 / 0 / 0 | 0 / 0 / 0 | 520 |
| TIL-05 pasta | 115 h | 714 | 519 | 60.7 % | 9.3 s | 62 % | 0 / 0 / 0 | 0 / 0 / 0 | 1,384 |
| TIL-06 marathon | 91 h | 186 | 119 | 64.8 % | 10.4 s | 69 % | 0 / 0 / 0 | 0 / 0 / 0 | 10 |
| TIL-07 basketball | 67 h | 180 | 127 | 55.1 % | 7.9 s | 52 % | 0 / 0 / 0 | 0 / 0 / 0 | 1,210 |
| TIL-08 shrunk 1 cm | 43 h | 1,547 | 1,093 | 63.1 % | 9.5 s | 63 % | 0 / 1 / 0 | 0 / 0.9 / 0 | 1,657 |
| **TIL-09 olive oil** | **19 h** | **3,259** | **2,132** | **72.0 %** | 11.1 s | **74 %** | 0 / 0 / 0 | 0 / 0 / 0 | 1,384 |
Medians (TIL-01..08): hook hold 62.4 %, watch ratio 62.5 %; 24 h IG reach baseline 136, YT 24 h 1,118.
  1. **Breakout #2: TIL-09 ("You'd sink in olive oil.")** — 2,132 accounts at 19 h = **15.7× baseline** (≈ 2× TIL-08), and unlike TIL-08 the retention also moved: hook hold 72.0 % (first ≥ 70 % target since TIL-01), watch 74 %. Likely contributors: a 5-word counterintuitive claim about the viewer plus a side-by-side control image (water floats / oil sinks) readable without sound at t = 0 (hypothesis, n = 1 → E11 in backlog). Confidence: **medium-high** that E5 premises drive reach (2 of 2 E5 reels ≥ 2×, top 4 IG reaches all body/food; 0 of 5 non-body premises above 1.0×); low on why retention rose this time. YT is flatter (1.24× median): the YT lift from E5 is modest.
  2. **Conversion moved but is still the bottleneck (medium):** first follows (IG +3, ≈ 1.4 per 1,000 TIL-09 reach; YT +1). Still 0 shares on 8,202 IG views and 1 save total. A reach of 2,000+ accounts per reel is now the norm for E5 premises; the reason to follow is the gap → E7.
  3. **Competitors (medium):** food/body/"you" stakes over-perform again at every size (zackdfilms food companies 2.0×, baby survives 2.2×; kurzgesagt processed food 4.4×); space topics sit at median, also on the new small peer astrumspace (31.6 k, median 2.5 k, no over-performer). New angle to test later: survival framing (E12).
- Experiment ideas from finding 1–2 (backlog in CAMPAIGN_LOG.md): (a) **E7 series teaser end card — selected** (attacks the bottleneck, keeps the proven topic rule constant); (b) E11 side-by-side control image at t = 0 as an opening rule (hook hold); (c) E12 survival framing for body premises (reach). E5 has all 3 reels built/published, so its measurement is not disturbed: TIL-11 keeps the E5 topic rule and changes only the ending.

NEXT BUILD INSTRUCTION (from 16 Nov 11:09 check): start **E7** with TIL-11 (built today, publishes 17 Nov 16:00). Topic: queue **G "your breath on Everest's summit"** (body; reordered to the top; verify summit pressure ≈ ⅓ atm and the time-of-useful-consciousness number before use, hedge; if it does not verify cleanly, take H, then D). Keep everything else as TIL-09/10: 15 s / 1.10, cold open on a proof image readable without sound (side-by-side control vs impossible if the premise allows), caption v2, ⚠️ disclaimer on caption + card, 16:00. **The one change:** the last ~1.5 s (after THE REAL SCIENCE card, or merged into it if 15 s does not allow) shows a clean end card "TOMORROW: <next premise in ≤ 5 words>" (e.g. "TOMORROW: TOAST ON VENUS"), and the caption's series line names the same premise ("Tomorrow: toast on Venus."), replacing "A new impossible experiment every day."; no "follow" wording. Name only a premise whose numbers the run has already checked (default D toast on Venus); the named premise is then binding for TIL-12. Primary metric: IG followers + YT subscribers gained per 1,000 IG reach in the 24 h after the post vs baseline ≈ 0.9 (TIL-08+09); secondary: IG reach at 24 h vs E5 median (1,613) and hook hold vs 62.4 %. Review: first read 18 Nov, verdict after TIL-13's 72 h (22 Nov). E5 verdict 19 Nov unchanged.

### Production run 16 Nov 2026 (13:14–19:05 EET)
- **Snapshot 17:54 CET (18:54 EET):** totals **18,528 views** (IG 8,226 + YT 10,302); followers IG 4 / YT 6 (unchanged since 11:09). Checkpoints: TIL-09 24 h = 3,264 / 2,132 · YT 1,387 (21.2 h; 15.7× baseline, hook hold 72.1 %, watch 74 %); TIL-07 72 h = 180 / 127 · YT 1,213 (74.9 h). Older reels frozen on IG; YT batch unchanged.

| Reel | Age | IG views | IG reach | Hook hold | Avg watch | Watch ratio | Shares / saves | YT views |
|---|---|---|---|---|---|---|---|---|
| TIL-01 whisky | 192 h | 208 | 138 | 71.3 % | 11.9 s | 80 % | 0 / 0 | 1,736 |
| TIL-02 mercury | 189 h | 1,778 | 1,149 | 67.5 % | 11.2 s | 68 % | 0 / 0 | 1,231 |
| TIL-03 honey | 162 h | 161 | 112 | 61.6 % | 9.8 s | 60 % | 0 / 0 | 1,162 |
| TIL-04 gravity | 144 h | 170 | 114 | 58.0 % | 10.1 s | 61 % | 0 / 0 | 520 |
| TIL-05 pasta | 123 h | 715 | 520 | 60.8 % | 9.3 s | 62 % | 0 / 0 | 1,384 |
| TIL-06 marathon | 99 h | 186 | 120 | 64.8 % | 10.4 s | 69 % | 0 / 0 | 10 |
| TIL-07 basketball | 75 h | 180 | 127 | 55.1 % | 7.8 s | 52 % | 0 / 0 | 1,213 |
| TIL-08 shrunk 1 cm | 51 h | 1,548 | 1,093 | 63.0 % | 9.5 s | 63 % | 0 / 1 | 1,658 |
| TIL-09 olive oil | 27 h | 3,278 | 2,144 | 72.1 % | 11.1 s | 74 % | 0 / 0 | 1,388 |
| TIL-10 10× taller | 1 h | 2 | 0 | n/a | n/a | n/a | 0 / 0 | 0 |
- **Findings:** 1. No new evidence vs the 11:09 check (IG frozen after ~20 h; TIL-09 +19 views/+12 accounts). 11:09 findings stand. 2. **TIL-10 went out 2 h 52 min late** (process failure, see CAMPAIGN_LOG decisions); all four earlier late posts reached ~110–140 accounts, so TIL-10 is a confounded E5 data point (confidence in E5 rests on TIL-08/09: medium-high, unchanged).
- **Adjustment applied:** none (NEXT BUILD INSTRUCTION followed). TIL-11 = queue G "Your breath on Everest's summit", E7 reel 1: end card "TOMORROW: TOAST ON VENUS" (13.45–15 s, under THE REAL SCIENCE card) + caption series line "Tomorrow: toast on Venus."; everything else as TIL-09/10 (15 s / 1.10, side-by-side proof image at t = 0, caption v2, disclaimer on caption + card). E7 status: reel 1 built, publishes 17 Nov 16:00; baseline ≈0.9 follows per 1,000 IG reach; first read 18 Nov. **Binding:** TIL-12 = toast on Venus.

- **17 Nov 11:28 EET (daily stats check, Tuesday, light run):** total **21,211 views** (IG 9,756 + YT 11,455), **+2,683** since 16 Nov 17:54 CET (IG +1,530: TIL-10 +1,527, TIL-09 +3; YT +1,153: TIL-10 +1,087, TIL-09 +43, TIL-08 +12, TIL-07 +7, TIL-02 +2). IG followers 4 → **6**, YT subscribers 6. Make runs 8451991 exec 6d736234… and 8451995 exec 4fd7ef7c… SUCCESS. Competitors not due.

| Reel | Age | IG views | IG reach | Hook hold | Avg watch | Watch ratio | Shares / saves / comments | per 1,000 reach | YT views / likes |
|---|---|---|---|---|---|---|---|---|---|
| TIL-01 whisky | 208 h | 208 | 138 | 71.3 % | 11.9 s | 80 % | 0 / 0 / 0 | 0 / 0 / 0 | 1,736 / 17 |
| TIL-02 mercury | 206 h | 1,778 | 1,149 | 67.5 % | 11.2 s | 68 % | 0 / 0 / 0 | 0 / 0 / 0 | 1,235 / 9 |
| TIL-03 honey | 179 h | 161 | 112 | 61.6 % | 9.8 s | 60 % | 0 / 0 / 0 | 0 / 0 / 0 | 1,162 / 19 |
| TIL-04 gravity | 160 h | 170 | 114 | 58.0 % | 10.1 s | 61 % | 0 / 0 / 0 | 0 / 0 / 0 | 520 / 9 |
| TIL-05 pasta | 139 h | 715 | 520 | 60.8 % | 9.3 s | 62 % | 0 / 0 / 0 | 0 / 0 / 0 | 1,384 / 16 |
| TIL-06 marathon | 115 h | 186 | 120 | 64.8 % | 10.4 s | 69 % | 0 / 0 / 0 | 0 / 0 / 0 | 10 / 0 |
| TIL-07 basketball | 91 h | 180 | 127 | 55.1 % | 7.8 s | 52 % | 0 / 0 / 0 | 0 / 0 / 0 | 1,220 / 15 |
| TIL-08 shrunk 1 cm | 67.5 h | 1,548 | 1,093 | 63.0 % | 9.5 s | 63 % | 0 / 1 / 0 | 0 / 0.9 / 0 | 1,670 / 9 |
| TIL-09 olive oil | 43.5 h | 3,281 | 2,147 | 72.1 % | 11.1 s | 74 % | 0 / 0 / 0 | 0 / 0 / 0 | 1,431 / 7 |
| **TIL-10 10× taller** | **16.6 h** | **1,529** | **1,073** | 61.1 % | 9.0 s | 60 % | 0 / 0 / 0 (1 repost) | 0 / 0 / 0 | **1,087** / 9 |
Medians (TIL-01..09): hook hold 63.0 %, watch ratio 63 %; 24 h IG reach baseline 136 (TIL-01..05); E5 median IG reach ≈ 1,093 (TIL-08..10); YT 24 h median 1,118.
  1. **E5 now 3 of 3 (confidence high for direction, medium for size):** TIL-10 reached 1,073 accounts at 16.6 h = 7.9× baseline, ≈ TIL-08, with median retention (hook 61.1 %, watch 60 %). Body/"you" premises reach 1,000–2,100 accounts; all five non-body premises 112–520. Formal verdict 19 Nov (IG freezes after ~20 h, so expected: retain as rule, pending one retest window under E7).
  2. **Late posting was not the reach killer (confidence medium, n = 1 counter-example):** TIL-10 went out at 18:52 and still hit 7.9×; the earlier "late = ~110 accounts" pattern coincided with non-body premises (TIL-03/04), and TIL-02 (21:52) reached 1,146. The 16:00 slot stays (Claudio's rule; on time remains the default and removes a confound) — no decision needed now, flagged as information.
  3. **Retention is the next ceiling, not reach (medium):** only TIL-09 (side-by-side proof image, 72 %) broke the 70 % hook target; TIL-08/10 sit at 61–63 % with the same topic rule. Supports E11 (side-by-side control image at t = 0) as the next experiment after E7. Conversion still thin: IG +2 followers on 1,073 TIL-10 accounts (1.9 per 1,000), 0 shares on 9,756 IG views.
- Experiment status: E5 3/3 measured at ≥ 16 h, verdict 19 Nov. **E7 running** (TIL-11 today 16:00 = reel 1; control baseline updated with TIL-10: IG followers +5 over 4,313 accounts reached by TIL-08..10 ≈ 1.2 per 1,000; first read 18 Nov). Ideas from finding 3 (backlog): (a) E11 side-by-side control vs impossible at t = 0 as a fixed opening rule — next candidate after E7; (b) E9 human body part in frame at t = 0; (c) E10 viewer-vs-familiar-object hook line. No change while E7 runs.

NEXT BUILD INSTRUCTION (from 17 Nov 11:28 check): keep current. E7 is running (TIL-11 publishes today 16:00 from READY = reel 1). Build **TIL-12 = queue D "Making toast on Venus"** (binding: named on TIL-11's end card and caption; verify bread charring temperature and NASA Venus surface numbers, hedge), as E7 reel 2: same end card "TOMORROW: <next premise in ≤ 5 words>" + matching caption series line, naming a premise whose numbers the run has checked (default H "your weight on every planet", binding for TIL-13). Everything else as TIL-11: 15 s / 1.10, cold open on a side-by-side proof image readable without sound where the premise allows (e.g. EARTH toaster vs VENUS toaster), caption v2, ⚠️ disclaimer on caption + card, **16:00 on time** (send in short separate calls, never inside one blocking wait). Primary metric: IG followers + YT subscribers per 1,000 IG reach in the 24 h after each E7 post vs control ≈ 1.2 (IG, TIL-08..10); secondary: IG reach at 24 h vs E5 median 1,093, hook hold vs 63.0 %. Verdict after TIL-13's 72 h (22 Nov).

### Production run 17 Nov 2026 (13:12–20:50 EET)
- **Snapshot 18:44 CET (19:44 EET):** totals **21,233 views** (IG 9,767 + YT 11,466); followers IG 6 / YT 6. Make 8451991 exec 94c8bdc9… and 8451995 exec 67372d35… SUCCESS. Checkpoints filled: TIL-10 24 h = 1,534 / 1,078 · YT 1,094 (24.9 h); TIL-08 72 h = 1,548 / 1,093 · 1,670 (69.2 h); TIL-04 7 d = 171 / 115 · 520 (168.7 h).

| Reel | Age | IG views | IG reach | Hook hold | Avg watch | Watch ratio | Shares / saves | YT views |
|---|---|---|---|---|---|---|---|---|
| TIL-01 whisky | 216 h | 209 | 138 | 70.8 % | 11.9 s | 79 % | 0 / 0 | 1,736 |
| TIL-02 mercury | 214 h | 1,778 | 1,149 | 67.5 % | 11.2 s | 68 % | 0 / 0 | 1,237 |
| TIL-03 honey | 187 h | 162 | 113 | 61.1 % | 9.7 s | 59 % | 0 / 0 | 1,162 |
| TIL-04 gravity | 168.7 h | 171 | 115 | 57.5 % | 10.0 s | 61 % | 0 / 0 | 520 |
| TIL-05 pasta | 147.7 h | 715 | 520 | 60.8 % | 9.3 s | 62 % | 0 / 0 | 1,383 |
| TIL-06 marathon | 123.7 h | 186 | 120 | 64.8 % | 10.4 s | 69 % | 0 / 0 | 10 |
| TIL-07 basketball | 99.7 h | 180 | 127 | 55.1 % | 7.8 s | 52 % | 0 / 0 | 1,213 |
| TIL-08 shrunk 1 cm | 75.7 h | 1,548 | 1,093 | 63.0 % | 9.5 s | 63 % | 0 / 1 | 1,671 |
| TIL-09 olive oil | 51.7 h | 3,284 | 2,147 | 72.1 % | 11.1 s | 74 % | 0 / 0 | 1,440 |
| TIL-10 10× taller | 24.9 h | 1,534 | 1,078 | 61.1 % | 9.0 s | 60 % | 0 / 0 | 1,094 |
| TIL-11 Everest breath | 1.0 h | 0 | 0 | n/a | n/a | n/a | 0 / 0 | 0 |
- **Findings:** 1. No new performance evidence since the 11:28 check (IG frozen on all reels ≥ 24 h; YT +11). The 11:28 findings stand (E5 3/3; retention is the next ceiling; conversion thin). 2. **Process, high confidence:** two consecutive late posts (TIL-10 +2 h 52 min, TIL-11 +3 h 44 min) both came from the long production session stalling before the 16:00 send, not from the build. Publishing should not depend on that session (decision for Claudio, see CAMPAIGN_LOG).
- **Adjustment applied:** none (NEXT BUILD INSTRUCTION followed). TIL-12 = queue D "Making toast on Venus" (binding), E7 reel 2: end card "TOMORROW: YOUR WEIGHT ON JUPITER" + caption series line "Tomorrow: your weight on Jupiter."; side-by-side proof image at t = 0 (oven vs Venus thermometers), caption v2, disclaimer on caption + card. **Binding:** TIL-13 = queue H "your weight on Jupiter/every planet" (NASA gravity ratios: Moon 0.166, Mars 0.377, Jupiter 2.36). E7 status: reel 1 live (late), reel 2 in READY for 18 Nov 16:00; verdict after TIL-13's 72 h.

### Daily stats check 18 Nov 2026 (11:08 EET, Wednesday, light run)
- **Snapshot 11:08 EET** (Make 8451991 exec b1999267… and 8451995 exec 2462f0f5… SUCCESS): total **21,806 views** (IG 9,922 + YT 11,884), **+573** since 17 Nov 18:44 CET (IG +155: TIL-11 +154; YT +418: TIL-11 +403, TIL-09 +12, TIL-10 +5, TIL-08 +3). IG followers 6, YT subscribers 6 (unchanged). Competitors not due (Mon/Thu).

| Reel | Age | IG views | IG reach | Hook hold | Avg watch | Watch ratio | Shares / saves / comments | YT views |
|---|---|---|---|---|---|---|---|---|
| TIL-01 whisky | 232 h | 209 | 138 | 70.8 % | 11.9 s | 79 % | 0 / 0 / 0 | 1,736 |
| TIL-02 mercury | 229 h | 1,779 | 1,150 | 67.5 % | 11.2 s | 68 % | 0 / 0 / 0 | 1,237 |
| TIL-03 honey | 202 h | 162 | 113 | 61.1 % | 9.7 s | 59 % | 0 / 0 / 0 | 1,162 |
| TIL-04 gravity | 184 h | 171 | 115 | 57.5 % | 10.0 s | 61 % | 0 / 0 / 0 | 520 |
| TIL-05 pasta | 163 h | 715 | 520 | 60.8 % | 9.3 s | 62 % | 0 / 0 / 0 | 1,383 |
| TIL-06 marathon | 139 h | 186 | 120 | 64.8 % | 10.4 s | 69 % | 0 / 0 / 0 | 10 |
| TIL-07 basketball | 115 h | 180 | 127 | 55.1 % | 7.8 s | 52 % | 0 / 0 / 0 | 1,208 |
| TIL-08 shrunk 1 cm | 91 h | 1,548 | 1,093 | 63.0 % | 9.5 s | 63 % | 0 / 1 / 0 | 1,674 |
| TIL-09 olive oil | 67 h | 3,284 | 2,149 | 72.1 % | 11.1 s | 74 % | 0 / 0 / 0 | 1,452 |
| TIL-10 10× taller | 40 h | 1,534 | 1,079 | 61.0 % | 9.0 s | 60 % | 0 / 0 / 0 (1 repost) | 1,099 |
| **TIL-11 Everest breath** | **15.4 h** | **154** | **122** | **53.2 %** | **6.2 s** | **41 %** | 0 / 0 / 0 | **403** |
Medians (TIL-01..10): hook hold 62.1 %, watch ratio 63 %; 24 h IG reach baseline 136; E5 median ≈ 1,093; YT 24 h median 1,118.
- **Findings:**
  1. **Clear drop — TIL-11 (E5 body premise + E7 reel 1) at 15.4 h: 122 IG accounts = 0.9× the 136 baseline and 0.11× the E5 median; YT 403 = 0.37× TIL-10 at a similar age.** Hook hold 53.2 % and watch ratio 41 % are the **lowest of all 11 reels**. Confidence: medium that the weakness is real (both platforms down together, IG usually freezes after ~20 h), low on the cause (n = 1, < 48 h; not a verdict).
  2. **Likely cause = the opening, not the slot or the end card (low–medium):** the late post (19:43) is a weaker explanation because TIL-10 went out at 18:52 and still hit 7.9×, and YT (less slot-sensitive) fell in step. The E7 end card sits at 13.45 s and average watch was 6.2 s, so most viewers never saw it — it cannot explain the drop. Plausible mechanism: the first frame (sea level vs summit, breath bubbles) shows a *condition* (thin air) instead of a *visible consequence* on a familiar object; the "you'd faint" payoff only lands later. TIL-08 (balance tipping) and TIL-09 (person sinking in a labelled tank) showed the consequence moving at t = 0.
  3. **E5 is now 3 of 4, not 4 of 4:** a "you" premise is necessary but not sufficient; the opening image has to prove the claim at a glance. E7 reel 1 conversion: 0 follows on 122 accounts — unreadable at this reach.
- Experiment ideas from finding 2 (backlog): (a) **E13 consequence-in-motion at t = 0** (the familiar object visibly reacting in the first 0.5 s: needle slamming, body sinking, bread blackening) vs a static comparison; (b) E11 side-by-side control vs impossible as a fixed rule; (c) E9 a human body part in frame at t = 0. **No switch now:** E7 is running (reel 2 TIL-12 today, reel 3 TIL-13 binding) — finish it first.

NEXT BUILD INSTRUCTION (from 18 Nov 11:08 check): keep current (E7 running; one variable at a time). Build **TIL-13 = queue H "Your weight on Jupiter"** (binding: named on TIL-12's end card and caption) as E7 reel 3: end card "TOMORROW: <next premise in ≤ 5 words>" + matching caption series line, naming only a premise whose numbers the run has checked (default C coffee the size of a lake, or E ice cream on Mercury, whichever verifies). Apply the **existing** proof-image rule strictly after TIL-11's weak opening (no new variable, just the playbook): t = 0 must show the consequence already happening on a familiar object, readable without sound — e.g. two bathroom scales side by side, EARTH 70 kg vs JUPITER needle slamming to ≈165 kg (70 × 2.36; NASA, at the 1-bar level, no solid surface — say so in the science card), not a planet or a label-only frame. Everything else as TIL-12: 15 s / 1.10, caption v2, ⚠️ disclaimer on caption + card, **16:00 on time** (short separate calls). Primary metric: IG followers + YT subscribers per 1,000 IG reach in the 24 h after each E7 post vs control ≈ 1.2; secondary: IG reach at 24 h vs E5 median 1,093 and hook hold vs 62.1 %. E7 verdict after TIL-13's 72 h (22 Nov); E5 verdict 19 Nov (now 3 of 4). If TIL-12 also opens below 55 % hook hold, the next experiment after E7 is E13.

### Production run 18 Nov 2026 (13:13–16:10 EET)
- **TIL-12 published on time** 16:00:07 EET (exec f606781d… SUCCESS, IG Df4q5VSj7PI, YT kHuZS3kFJUI). **Snapshot 15:03 CET (16:03 EET)** (Make 8451991 exec d150c8b2…, 8451995 exec ce696525… SUCCESS): total **21,815 views** (IG 9,925 + YT 11,890); IG followers 6, YT subscribers 6. Checkpoints filled: TIL-05 7 d = 715 / 520 · 1,383 (168.0 h); TIL-09 72 h = 3,284 / 2,149 · 1,453 (72.0 h).

| Reel | Age | IG views | IG reach | Hook hold | Avg watch | Watch ratio | Shares / saves | YT views |
|---|---|---|---|---|---|---|---|---|
| TIL-01 whisky | 237 h | 210 | 139 | 71.0 % | 11.8 s | 79 % | 0 / 0 | 1,736 |
| TIL-02 mercury | 234 h | 1,779 | 1,150 | 67.5 % | 11.2 s | 68 % | 0 / 0 | 1,237 |
| TIL-03 honey | 207 h | 162 | 113 | 61.1 % | 9.7 s | 59 % | 0 / 0 | 1,162 |
| TIL-04 gravity | 189 h | 171 | 115 | 57.5 % | 10.0 s | 61 % | 0 / 0 | 520 |
| TIL-05 pasta | 168 h | 715 | 520 | 60.8 % | 9.3 s | 62 % | 0 / 0 | 1,383 |
| TIL-06 marathon | 144 h | 186 | 120 | 64.8 % | 10.4 s | 69 % | 0 / 0 | 10 |
| TIL-07 basketball | 120 h | 180 | 127 | 55.1 % | 7.8 s | 52 % | 0 / 0 | 1,208 |
| TIL-08 shrunk 1 cm | 96 h | 1,548 | 1,093 | 63.0 % | 9.5 s | 63 % | 0 / 1 | 1,670 |
| TIL-09 olive oil | 72 h | 3,284 | 2,149 | 72.1 % | 11.1 s | 74 % | 0 / 0 | 1,453 |
| TIL-10 10× taller | 46 h | 1,534 | 1,079 | 61.0 % | 9.0 s | 60 % | 0 / 0 | 1,104 |
| TIL-11 Everest breath | 20.3 h | 156 | 124 | 53.2 % | 6.2 s | 41 % | 0 / 0 (1 repost) | 407 |
| TIL-12 toast on Venus | 0.05 h | 0 | 0 | n/a | n/a | n/a | 0 / 0 | 0 |
- **Findings:** 1. No new performance evidence since 11:08 (IG frozen on reels ≥ 24 h; TIL-11 +2 accounts, +4 YT) — the 11:08 findings stand (TIL-11 weakest opening; E5 3 of 4). 2. **Process, high confidence:** on-time posting restored (build done 14:33, buffer hosted, send at 16:00:07 in its own call) — the README fix works when the run does not stall.
- **Adjustment applied:** none (NEXT BUILD INSTRUCTION 18 Nov 11:08 followed). TIL-13 = queue H "Your weight on Jupiter", E7 reel 3: t = 0 shows the consequence moving (JUPITER readout 100 → 165 kg, figure sagging, platform squashing) beside an EARTH 70 kg control; end card "TOMORROW: ICE CREAM ON MERCURY" + caption series line. **Binding:** TIL-14 = queue E "Ice cream on Mercury" (NASA night −180 °C checked; Tg' value still to source). E7 status: reels 1–2 live (TIL-11 late, TIL-12 on time), reel 3 in READY for 19 Nov 16:00; verdict after TIL-13's 72 h (22 Nov).

### Daily stats check 19 Nov 2026 (11:08 EET, Thursday, light run)
- **Snapshot 11:08 EET** (Make 8451991 exec ab67554d… and 8451995 exec c98e9058… SUCCESS): total **23,697 views** (IG 10,784 + YT 12,913), **+1,882** since 18 Nov 16:03 EET (IG +859: TIL-12 +858, TIL-05 +1; YT +1,023: TIL-12 +917, TIL-11 +78, TIL-10 +14, TIL-08 +9, TIL-09 +4, TIL-01 +1). IG followers 6, YT subscribers 6 (unchanged since 17 Nov). Competitors checked (Thursday): see CAMPAIGN_LOG.md.

| Reel | Age | IG views | IG reach | Hook hold | Avg watch | Watch ratio | Shares / saves / comments | YT views |
|---|---|---|---|---|---|---|---|---|
| TIL-01 whisky | 256 h | 210 | 139 | 71.0 % | 11.8 s | 79 % | 0 / 0 / 0 | 1,737 |
| TIL-02 mercury | 253 h | 1,779 | 1,150 | 67.5 % | 11.2 s | 68 % | 0 / 0 / 0 | 1,237 |
| TIL-03 honey | 226 h | 162 | 113 | 61.1 % | 9.7 s | 59 % | 0 / 0 / 0 | 1,162 |
| TIL-04 gravity | 208 h | 171 | 115 | 57.5 % | 10.0 s | 61 % | 0 / 0 / 0 | 520 |
| TIL-05 pasta | 187 h | 716 | 521 | 60.7 % | 9.3 s | 62 % | 0 / 0 / 0 | 1,383 |
| TIL-06 marathon | 163 h | 186 | 120 | 64.8 % | 10.4 s | 69 % | 0 / 0 / 0 | 10 |
| TIL-07 basketball | 139 h | 180 | 127 | 55.1 % | 7.9 s | 52 % | 0 / 0 / 0 | 1,208 |
| TIL-08 shrunk 1 cm | 115 h | 1,548 | 1,093 | 63.0 % | 9.5 s | 63 % | 0 / 1 / 0 | 1,679 |
| TIL-09 olive oil | 91 h | 3,284 | 2,149 | 72.1 % | 11.1 s | 74 % | 0 / 0 / 0 | 1,457 |
| TIL-10 10× taller | 64 h | 1,534 | 1,079 | 61.0 % | 9.0 s | 60 % | 0 / 0 / 0 (1 repost) | 1,118 |
| TIL-11 Everest breath | 39 h | 156 | 124 | 53.2 % | 6.2 s | 41 % | 0 / 0 / 0 (1 repost) | 485 |
| **TIL-12 toast on Venus** | **19.1 h** | **858** | **642** | **60.3 %** | **9.1 s** | **61 %** | 0 / 0 / 0 | **917** |
Medians (TIL-01..11): hook hold 61.1 %, watch ratio 62 %; 24 h IG reach baseline 136; E5 24 h median 1,093; YT 24 h median 1,118. Shares per 1,000 IG views: 0 (0 of 10,784 across 12 reels); saves 0.09.
- **Findings:**
  1. **E5 verdict: PASS (confidence medium).** 4 of 5 E5 reels ≥ 2× the 136 baseline at ~24 h (TIL-08 8.0×, TIL-09 15.7×, TIL-10 7.9×, TIL-11 0.9×, TIL-12 4.7× at 19.1 h; IG counts freeze after ~20 h) vs 0 of 5 non-body/food premises (0.8–1.0×); both pre-E5 body/food reels also cleared 2× (mercury 8.4×, pasta 3.8×). Competitor over-performers agree for the third check. Retained as a standing topic rule (playbook v3 candidate on Sunday); TIL-11 shows it is necessary, not sufficient.
  2. **TIL-12 is mid (low confidence, < 48 h):** 4.7× baseline but 0.59× the E5 median, hook hold 60.3 % ≈ median. Openings that showed the familiar object physically reacting (TIL-08 balance tipping, TIL-09 person sinking) held 63–72 %; a readout/condition opening (TIL-12 thermometers, TIL-11 thin air) held 53–60 %. Pattern across n = 4, two of them weak — a hypothesis, not a rule.
  3. **E7 provisional: no conversion lift (low–medium).** IG followers and YT subscribers flat at 6 / 6 across TIL-11+12 (766 accounts reached) vs ≈ 1.2 per 1,000 for the no-teaser control; average watch ≈ 9 s while the card appears at ~13.45 s, so most viewers never see it. Reel 3 (TIL-13) publishes today; verdict 22 Nov. Separately, 0 shares in 12 reels: the caption share line is not producing sends.
- Experiment ideas from finding 2: (a) **E13 consequence in motion at t = 0** — the familiar object physically reacting beside an Earth control in the first 0.5 s; (b) E10 viewer-vs-familiar-object hook line ("<object> … more than you"); (c) E9 a human body part in frame at t = 0. Plus E14 (on-screen share beat) and E15 (teaser in the first half) added from finding 3. **Selected E13** (strongest evidence: own hook-hold spread 53–72 % tracks the opening type; competitor anchors-test 4.2×). E7 is complete in production (3 reels published by today 16:00), so E13 does not overlap its measurement; the E7 end card stays unchanged as a constant until its verdict.

NEXT BUILD INSTRUCTION (from 19 Nov 11:08 check): start **E13 (reel 1 of 3) on TIL-14 = queue E "Ice cream on Mercury's night side"** (binding: named on TIL-13's end card and caption). The one variable is the opening visual: within the first 0.5 s, a familiar scoop of ice cream visibly reacts to the impossible condition beside an Earth control, readable without sound — e.g. EARTH: a spoon sinks into a soft scoop; MERCURY NIGHT −180 °C: the same spoon strikes the scoop and it shatters like glass. No thermometer/readout-only or planet-only first frame. Keep everything else as TIL-13: hook line as a claim that sounds wrong but is true, 15 s / 1.10, caption v2, ⚠️ "Don't try this." on caption + card, E7 end card "TOMORROW: <next premise>" (default C coffee the size of a lake, only if its numbers verify), 16:00 on time (short separate calls). Science: source a Tg' value for ice cream before use (Univ. of Guelph dairy e-book or a peer-reviewed source; hedge if only a range exists) and NASA Mercury night −180 °C / day 430 °C; if the glass-shatter claim cannot be sourced, show a "rock-hard, spoon bounces" consequence instead. Primary metric: hook hold vs median 61.1 % (E13 target ≥ 65 % mean over TIL-14..16); secondary: IG reach at 24 h vs E5 median 1,093. Review at TIL-16's 48 h. E7 verdict 22 Nov.

### Production run 19 Nov 2026 (13:12–16:20 EET)
- **TIL-13 published on time** 16:00:07 EET (exec bcdb68f4… SUCCESS, IG Df7PsCnDpPL, YT yABGZH8K4Yg). **Snapshot 15:03 CET (16:03 EET)** (Make 8451991 exec 0764f118…, 8451995 exec 4cfc8037… SUCCESS): total **23,826 views** (IG 10,892 + YT 12,934); IG followers 6, YT subscribers 6. Checkpoints filled: TIL-12 24 h = 966 / 744 · 920 (24.0 h); TIL-10 72 h = 1,534 / 1,079 · 1,118 (69.2 h); TIL-06 7 d = 186 / 120 · 10 (168.0 h). Snapshot store trimmed to the newest 3 captures (deleted 18 Nov 12:14 and 15:03 CET).

| Reel | Age | IG views | IG reach | Hook hold | Avg watch | Watch ratio | Shares / saves | YT views |
|---|---|---|---|---|---|---|---|---|
| TIL-01 whisky | 261 h | 210 | 139 | 71.0 % | 11.8 s | 79 % | 0 / 0 | 1,737 |
| TIL-02 mercury | 258 h | 1,779 | 1,150 | 67.5 % | 11.2 s | 68 % | 0 / 0 | 1,237 |
| TIL-03 honey | 231 h | 162 | 113 | 61.1 % | 9.7 s | 59 % | 0 / 0 | 1,162 |
| TIL-04 gravity | 213 h | 171 | 115 | 57.5 % | 10.0 s | 61 % | 0 / 0 | 520 |
| TIL-05 pasta | 192 h | 716 | 521 | 60.7 % | 9.3 s | 62 % | 0 / 0 | 1,383 |
| TIL-06 marathon | 168 h | 186 | 120 | 64.8 % | 10.4 s | 69 % | 0 / 0 | 10 |
| TIL-07 basketball | 144 h | 180 | 127 | 55.1 % | 7.8 s | 52 % | 0 / 0 | 1,208 |
| TIL-08 shrunk 1 cm | 120 h | 1,548 | 1,093 | 63.0 % | 9.5 s | 63 % | 0 / 1 | 1,679 |
| TIL-09 olive oil | 96 h | 3,284 | 2,149 | 72.1 % | 11.1 s | 74 % | 0 / 0 | 1,458 |
| TIL-10 10× taller | 69 h | 1,534 | 1,079 | 61.0 % | 9.0 s | 60 % | 0 / 0 | 1,118 |
| TIL-11 Everest breath | 44 h | 156 | 124 | 53.2 % | 6.2 s | 41 % | 0 / 0 | 502 |
| **TIL-12 toast on Venus** | **24.0 h** | **966** | **744** | **61.1 %** | **9.0 s** | **60 %** | 0 / 0 | **920** |
| TIL-13 Jupiter weight | 0.05 h | 0 | 0 | n/a | n/a | n/a | 0 / 0 | 0 |
- **Findings:** 1. **TIL-12 at 24 h = 744 IG accounts (5.5× baseline, 0.68× E5 median 1,093), hook hold 61.1 % = median** — the topic rule delivered distribution, the readout-style opening did not lift retention; consistent with the E13 rationale (confidence medium, n = 5 openings). 2. **E7 still no conversion:** IG followers / YT subscribers 6 / 6 since 17 Nov over 868 accounts reached by TIL-11+12 (0 per 1,000 vs control ≈1.2); verdict after TIL-13's 72 h on 22 Nov (low–medium). 3. YT TIL-12 920 at 24 h = 0.82× YT median 1,118 (low; YT batches).
- **Adjustment applied:** none — NEXT BUILD INSTRUCTION (19 Nov 11:08) followed: **TIL-14 = queue E "Ice cream on Mercury's night side", E13 reel 1**: t = 0 shows the consequence moving (spoon strikes the MERCURY NIGHT −180 °C scoop at 0.12 s, cracks + glassy shards by 0.3 s) beside an EARTH −18 °C control the spoon sinks into. Science sourced: NASA night −180 °C / day 430 °C / solar day 176 d; FDA freezer −18 °C; glass transition ≈ −28 to −32 °C (Physics World) and brittle glass below Tg' (Univ. of Guelph) → "shatter" kept as "cracks like glass / chips". One logged deviation: the E7 teaser names queue #10 "EARTH STOPS SPINNING" (default C coffee lake had no checkable cooling source today). **Binding:** TIL-15 = queue #10. E13 status: reel 1 in READY for 20 Nov 16:00; review at TIL-16's 48 h.

### Stats check 20 Nov 2026 11:08 EET (light run, Friday)
- Make 8451991 exec 17a30e55… and 8451995 exec d053425b… (both returned; capture 10:08 CET = 11:08 EET present for all 13 IG + 13 YT media). **Total 26,400 views (IG 12,359 + YT 14,041), +2,574 since 19 Nov 15:03 CET.** IG followers 6 (unchanged), **YT subscribers 6 → 7**. Competitors not due (Mon/Thu). Data store 250779 trimmed 100 → 52 (19 Nov 10:08 + 12:14 CET snapshots removed; newest per media kept).

| Reel | Age | IG views | IG reach | Hook hold | Avg watch | Watch ratio | Shares / saves / reposts | YT views |
|---|---|---|---|---|---|---|---|---|
| TIL-01 whisky | 280 h | 210 | 139 | 71.0 % | 11.8 s | 79 % | 0 / 0 / 1 | 1,737 |
| TIL-02 mercury | 277 h | 1,779 | 1,150 | 67.5 % | 11.2 s | 68 % | 0 / 0 / 2 | 1,237 |
| TIL-03 honey | 250 h | 162 | 113 | 61.1 % | 9.7 s | 59 % | 0 / 0 / 0 | 1,162 |
| TIL-04 gravity | 232 h | 171 | 115 | 57.5 % | 10.0 s | 61 % | 0 / 0 / 0 | 520 |
| TIL-05 pasta | 211 h | 716 | 521 | 60.7 % | 9.3 s | 62 % | 0 / 0 / 0 | 1,383 |
| TIL-06 marathon | 187 h | 186 | 120 | 64.8 % | 10.4 s | 69 % | 0 / 0 / 0 | 10 |
| TIL-07 basketball | 163 h | 180 | 127 | 55.1 % | 7.8 s | 52 % | 0 / 0 / 0 | 1,208 |
| TIL-08 shrunk 1 cm | 139 h | 1,548 | 1,093 | 63.0 % | 9.5 s | 63 % | 0 / 1 / 0 | 1,681 |
| TIL-09 olive oil | 115 h | 3,285 | 2,149 | 72.1 % | 11.1 s | 74 % | 0 / 0 / 0 | 1,464 |
| TIL-10 10× taller | 88 h | 1,534 | 1,079 | 61.0 % | 9.0 s | 60 % | 0 / 0 / 1 | 1,120 |
| TIL-11 Everest breath | 63 h | 156 | 124 | 53.2 % | 6.2 s | 41 % | 0 / 0 / 1 | 551 |
| TIL-12 toast on Venus | 43 h | 968 | 749 | 61.1 % | 9.0 s | 60 % | 0 / 0 / 0 | 928 |
| **TIL-13 Jupiter weight** | **19.1 h** | **1,464** | **1,040** | **66.1 %** | **8.6 s** | **58 %** | 0 / 0 / 2 | **1,040** |
Medians (TIL-01..12): hook hold 61.1 %, watch ratio 61 %; 24 h IG reach baseline 136; E5 24 h median 1,093; YT 24 h median 1,118. Shares: 0 of 12,359 IG views over 13 reels; saves 1.
- **Findings:**
  1. **TIL-13 (strict proof-image opening: EARTH 70 kg vs JUPITER readout racing to 165 kg with the figure sagging inside 0.65 s) = 1,040 IG accounts at 19.1 h (7.6× the 136 baseline, 0.95× E5 median; > 1,000 IG views in 24 h) and hook hold 66.1 %, the 3rd best of 13 and +5 pts on the median.** Openings where the body/object visibly reacts (TIL-08 63.0 %, TIL-09 72.1 %, TIL-13 66.1 %; mean 67.1 %) vs condition/readout-only openings (TIL-11 53.2 %, TIL-12 61.1 %; mean 57.2 %). Supports the E13 hypothesis before E13 itself starts measuring; confidence low–medium (n = 5, TIL-13 < 48 h, IG counts usually freeze after ~20 h). TIL-13 is pre-E13 evidence, not an E13 reel.
  2. **E7 (end-card teaser) heading for FAIL (low–medium):** 3 of 3 reels published; IG followers 6 → 6 and YT subs 6 → 7 since 17 Nov across 1,913 accounts reached by TIL-11..13 (≈ 0.5 per 1,000 incl. YT vs control ≈ 1.2 IG per 1,000). Avg watch 6.2–9.0 s vs card at ~13.45 s: most viewers never reach it. Verdict 22 Nov at TIL-13's 72 h; if it fails the cause is placement, which points to E15 (teaser in the first half).
  3. **Shares remain the dead metric (medium):** 0 shares on 12,359 IG views over 13 reels; the only redistribution is reposts (TIL-13: 2, total 8). The caption share line does not work; E14 (on-screen share beat) stays the next candidate after E13.
- Experiment ideas from finding 1 (backlog): (a) **E13 running** (consequence in motion at t = 0); (b) E9 human body part in frame at t = 0 — TIL-13's sagging figure suggests it compounds with E13 (later test); (c) E11 fixed side-by-side control vs impossible as the permanent opening rule after E13 passes (retest before permanent).
- **Selection: keep current** — E13 reel 1 (TIL-14) publishes today 16:00 from READY; one variable at a time, ≥ 3 reels before judging.

NEXT BUILD INSTRUCTION (from 20 Nov 11:08 check): keep current (E13 reel 2 of 3). Build **TIL-15 = queue #10 "Earth stops spinning for one second"** (binding: TIL-14 end card + caption). E13 variable unchanged: within the first 0.5 s a familiar object (and, where safe, the viewer's figure) visibly reacts beside an Earth control — e.g. NORMAL EARTH: a coffee mug standing still on a table; EARTH STOPPED: the same mug and table contents launching east at speed, readable without sound — no globe-only or speed-readout-only first frame (TIL-11/12 pattern held 53–61 %). Keep the E5 body/everyday-object framing ("you and your kitchen keep moving at 465 m/s"), safe content (objects fly; no injured people on screen), hook line as a claim that sounds wrong but is true, 15 s / 1.10, caption v2, ⚠️ "Don't try this." on caption + card, E7 end card "TOMORROW: <next premise>" unchanged as a constant until its 22 Nov verdict, 16:00 on time (short separate calls). Science: re-verify equatorial speed ≈ 465 m/s (NASA: 40,075 km / sidereal day 23.93 h) and the latitude scaling (v = 465 × cos φ; ≈ 329 m/s at 45° vs sound ≈ 343 m/s at 20 °C, so "about the speed of sound" must be stated as "close to"). Primary metric: hook hold vs median 61.1 % (E13 target ≥ 65 % mean over TIL-14..16); secondary: IG reach at 24 h vs E5 median 1,093. Review at TIL-16's 48 h (24 Nov 16:00).

## Weekly reviews
### Week 1 (8–15 Nov 2026), written 15 Nov 11:08
- Output: 8 reels published (TIL-01..08), 4 consecutive on-time 16:00 posts since TIL-05; READY buffer working (TIL-09 ready for today). Totals at 15 Nov 11:08: 13,498 views (IG 4,929 + YT 8,569); IG followers 1, YT subscribers 5.
- What worked: premises where the viewer's own body meets a familiar substance/object (mercury pool 1,146 accounts, shrunk-you 1,090 at 19 h, pasta 517); on-time 16:00 posting (every late post sat at ~110 accounts); YouTube as a steady second channel (median ~1,160 views per Short, long tail for days, IG freezes after ~12 h).
- What did not: E1 (16.5 s / slower voice) and E4 (back to 15 s / 1.10) — neither moved retention; E2 (one-tap yes/no comment prompt) — 0 comments, stopped; E3 (cold open on climax) — unresolved, confounded. Shares 0 and comments 0 across 4,929 IG views; only 1 save.
- Bottlenecks, in order: (1) follower conversion (0 IG follows from ~3,400 accounts reached); (2) sharing (0 sends); (3) hook hold stuck at 55–64 % on every reel after TIL-01 (target 70 %).
- Next week: finish E5 (TIL-09, TIL-10; verdict 19 Nov); then E7 (series teaser end card, conversion) or E9 (body in frame at t = 0, hook hold), chosen on the E5 data. Competitor check Mon 16 Nov: add 1–3 small (< 100 k) format peers.

### Playbook v2 (15 Nov 2026) — consolidates decisions already in force; supersedes v1 where different
- Format: 15 s, Kokoro `af_heart` speed 1.10 (Claudio's rule, `pipeline/config.py`); Blender primitives, 1080×1920.
- Topic (provisional rule while E5 runs): a premise with stakes for the viewer's own body or an everyday object/food; avoid pure space/abstract physics premises without a "you" angle.
- Hook: true-but-wrong-sounding claim at t = 0, proved on screen by an image readable without sound (TIL-08 balance, TIL-09 two tanks).
- Caption v2: hook line, 3–4 science lines, one share line naming a person type, one series line, "⚠️ Don't try this." line, ≤ 8 hashtags; no comment prompt, no "Follow … for more".
- **Follow invite on every reel (Claudio, 20 Nov 2026, standing rule; overrides caption v2's "no Follow … for more" and BRIEF §5's "not 'follow for more'"):** (1) video: an amber pill "FOLLOW · A NEW IMPOSSIBLE EXPERIMENT EVERY DAY" from 5.0 to 8.2 s (inside the average watch of ≈ 9 s), between the captions and Instagram's bottom UI, plus "FOLLOW @the.impossible.lab" under the TOMORROW end card — both built into pipeline/overlay.py (FOLLOW_TEXT / FOLLOW_START / FOLLOW_END / END_FOLLOW), so no per-episode work; (2) caption: the series line ends with "🔔 Follow @the.impossible.lab (or subscribe on YouTube) so you don't miss it." (this is the one CTA together with the share line; no engagement bait). Optional, only if the narration still fits the 15 s budget: a last spoken line ≤ 4 words ("Follow for tomorrow's."); never speed the voice up for it.
- Unchanged from v1: three beats with one rounded number each, twist, THE REAL SCIENCE card with the red disclaimer, series tag, word-by-word captions, safe content, verified science, 16:00 slot, buffer-first publishing.

NEXT BUILD INSTRUCTION (from 20 Nov 12:50 — Claudio's decision, added to the 20 Nov 11:08 instruction, which otherwise stands): apply the **follow invite** standing rule (Playbook v2 note, 20 Nov) to TIL-15 and every later reel: overlay.py already draws the mid-reel FOLLOW pill (5.0–8.2 s) and the end-card "FOLLOW @the.impossible.lab"; keep FACTS chips and key subjects clear of the 1440–1520 px band during 5–8.2 s; caption series line = "Tomorrow: <next premise>. 🔔 Follow @the.impossible.lab (or subscribe on YouTube) so you don't miss it." TIL-14 (READY, already rendered) carries it in the caption only. **E7 closed early as superseded** (its own read stays as recorded: no lift, card unseen at 13.45 s). **E16 started**: explicit follow invite (mid-reel pill + end card + caption) — primary metric IG followers + YT subscribers gained per 1,000 IG reach in the 24 h after each post; baseline ≈ 1.2 per 1,000 (no-teaser control TIL-08..10) and ≈ 0.5 (E7 TIL-11..13); runs as a constant alongside E13 (E13 measures hook hold in the first 3 s, the invite starts at 5 s, so the two do not overlap); review after TIL-17's 24 h (24 Nov 16:00).

### Production run 20 Nov 2026 (13:12–16:10 EET)
- **TIL-14 published on time** 16:00:04 EET (exec 5661f04e… SUCCESS, 5 operations; IG Df90gUOirkY, YT as3BaHKjHbE) — E13 reel 1 live. Snapshot 15:02 CET (16:02 EET; Make 8451991 exec 0cb393b8…, 8451995 exec eeaf317c… SUCCESS): **total 26,492 views (IG 12,440 + YT 14,052)**; IG followers 6, YT subscribers 7 (unchanged since 11:08). Snapshot rows added above.
- **Findings:** 1. **TIL-13 24 h checkpoint = 1,100 IG accounts (8.1× the 136 baseline, 1.01× E5 median 1,093), hook hold 66.0 % (+4.9 pts on the 61.1 % median), watch 58 %** — confirms the 11:08 read; the object/body-reacting opening pattern (TIL-08/09/13 mean 67.0 %) vs readout openings (TIL-11/12 mean 57.2 %) holds at 24 h (low–medium, n = 5). 2. **Conversion still flat:** 0 new IG followers and 0 new YT subs in the 5 h since 11:08; the E16 follow invite only reaches viewers from TIL-15 (video) on, so no read yet. 3. TIL-11 (72 h) and TIL-07 (7 d) are final at 124 and 127 accounts: both sit at the non-E5 baseline level, the two weakest reels of the E5/E7 era by reach.
- **Adjustment applied:** none — NEXT BUILD INSTRUCTIONS (20 Nov 11:08 + 12:50) followed: **TIL-15 = queue #10 "Earth stops spinning for one second", E13 reel 2**: frame 0 = NORMAL EARTH table (mug steaming) vs STOPPED EARTH table, whose mug, plate + apple and book launch east with streaks at 0.08 s ("MUG: 465 m/s →"); E16 in full (FOLLOW pill 5.0–8.2 s kept clear of chips/subjects, end card "FOLLOW @the.impossible.lab", caption "🔔 Follow … so you don't miss it"). Science re-verified: NASA fact sheet 6378.137 km / 23.9345 h → 465.1 m/s; × cos 45° = 328.9 m/s; sound 343 m/s at 20 °C → "near sound speed", not "at". One logged choice (not a new variable): the TIL-16 teaser names queue #16 "BOILING AN EGG ON EVEREST" (E5 food premise; C coffee lake still unverifiable). **Binding:** TIL-16 = queue #16. E13 status: reel 1 live, reel 2 in READY for 21 Nov 16:00; review at TIL-16's 48 h (24 Nov). E16 status: reel 1 (full) in READY; review after TIL-17's 24 h.

### Stats check 21 Nov 2026 11:08 EET (light run, Saturday)
- Make 8451991 exec c9abe2dd… and 8451995 exec 2fd6121c… (both returned; capture 10:08 CET = 11:08 EET present for all 14 IG + 14 YT media). **Total 28,224 views (IG 12,860 + YT 15,364), +1,732 since 20 Nov 15:02 CET** (+1,689 of it from TIL-14). IG followers 6 (unchanged since 17 Nov), YT subscribers 7 (unchanged). Competitors not due (Mon/Thu); no weekly review (not Sunday). Data store 250779: 52 records removed (20 Nov 10:08 + 12:15 CET snapshots; newest per media kept) — the listing had hit its 100-record limit before the trim.

| Reel | Age | IG views | IG reach | Hook hold | Avg watch | Watch ratio | Shares / saves / reposts | YT views |
|---|---|---|---|---|---|---|---|---|
| TIL-08 shrunk 1 cm | 163 h | 1,548 | 1,093 | 63.0 % | 9.5 s | 63 % | 0 / 1 / 0 | 1,691 |
| TIL-09 olive oil | 139 h | 3,285 | 2,149 | 72.1 % | 11.1 s | 74 % | 0 / 0 / 0 | 1,471 |
| TIL-10 10× taller | 112 h | 1,534 | 1,079 | 61.0 % | 9.0 s | 60 % | 0 / 0 / 1 | 1,122 |
| TIL-11 Everest breath | 87 h | 156 | 124 | 53.2 % | 6.2 s | 41 % | 0 / 0 / 1 | 549 |
| TIL-12 toast on Venus | 67 h | 968 | 749 | 61.1 % | 9.0 s | 60 % | 0 / 0 / 0 | 927 |
| TIL-13 Jupiter weight | 43 h | 1,552 | 1,108 | 65.9 % | 8.6 s | 58 % | 0 / 0 / 2 | 1,067 |
| **TIL-14 ice cream on Mercury (E13 reel 1)** | **19.1 h** | **413** | **295** | **68.4 %** | **7.9 s** | **52 %** | 0 / 0 / 1 | **1,276** |
TIL-01..07 unchanged vs 20 Nov (IG frozen; YT ±1; TIL-06 still 11 YT views at 211 h). Medians (TIL-01..13): hook hold 61.1 %, watch ratio 60 %; 24 h IG reach baseline 136; E5 24 h median 1,093; YT 24 h median 1,118. Shares: 0 of 12,860 IG views over 14 reels; saves 1; reposts 9.
- **Findings:**
  1. **TIL-14 decouples hold from reach (low, n = 1, < 48 h):** hook hold **68.4 %** (2nd best of 14, +7.3 pts on the median — E13's primary metric moved the right way) but IG reach **295 at 19.1 h = 0.27× the E5 median** (2.2× the old 136 baseline), and watch ratio 52 % (7.9 s), the 2nd lowest. Viewers stayed past the strike and then left before the payoff. YT went the other way: 1,276 at 19 h = 1.14× the YT median, best YT early read since TIL-08. IG counts usually freeze after ~20 h, so the reach read will barely move.
  2. **Among body/food reels, IG reach tracks watch ratio more than hook hold (low–medium, n = 7, observational):** watch ratio → 24 h reach: TIL-09 74 % → 2,149; TIL-08 63 % → 1,093; TIL-10 60 % → 1,079; TIL-12 60 % → 749; TIL-13 58 % → 1,108; TIL-14 52 % → 295; TIL-11 41 % → 124. Rank order holds except 12/13. Hook hold alone does not predict it (TIL-14 68 % → 295). Hypothesis: IG distributes on completion, so after the E13 opening the bottleneck is the 3–10 s middle (escalation/payoff), not the first second. Possible confound on TIL-14: the premise is food but framed by a planet (Mercury) — the "space framing" that sits at the median for competitors too.
  3. **E16 reel 1 (caption-only follow line on TIL-14):** IG followers 6 → 6, YT subs 7 → 7 over 295 IG accounts + 1,276 YT views — unreadable at this reach; TIL-15 today is the first full E16 reel (pill 5.0–8.2 s sits inside the 7.9–9 s average watch).
- Experiment ideas from finding 2 (backlog, E17): (a) **second escalation beat at 6–8 s** — the object's reaction gets bigger or a second familiar object reacts, inside the average watch, so the payoff does not wait for the end; (b) **payoff-first middle**: state the number that explains the shock by 5 s, then spend the rest showing the consequence (no explanation after 10 s); (c) shorter reel (e.g. 12 s) so the same watch time is a higher ratio — **this touches Claudio's 15 s / 1.10 rule, so it is a decision for him, not a lever**.
- **Selection: keep current** — E13 is at reel 1 of 3 (≥ 3 reels before judging; one variable at a time). TIL-15 (E13 reel 2 + E16 full) publishes today 16:00 from READY; TIL-16 = queue #16 egg on Everest (bound by TIL-15's end card) is E13 reel 3. E17 (a) is the next candidate once E13 is reviewed at TIL-16's 48 h (24 Nov 16:00).

NEXT BUILD INSTRUCTION (from 21 Nov 11:08 check): keep current (E13 reel 3 of 3). Build **TIL-16 = queue #16 "Boiling an egg on Everest"** (binding: TIL-15 end card "TOMORROW: BOILING AN EGG ON EVEREST"). E13 variable unchanged: within the first 0.5 s a familiar egg/pot visibly reacts beside a SEA LEVEL control (e.g. both pots at a rolling boil, the Everest egg still runny when cut / the thermometer pinned at ~70 °C while bubbling) — no mountain-only or readout-only first frame (TIL-11 Everest opening held 53 %). Keep everything else as TIL-15: E5 food/kitchen framing, hook as a claim that sounds wrong but is true, 15 s / 1.10, caption v2 with the follow line, E16 FOLLOW pill 5.0–8.2 s + end card, ⚠️ "Don't try this." on caption + card, 16:00 on time (short separate calls). Within the current format, protect the middle (finding 2): no explanation-only stretch between 3 and 10 s — keep the egg/pot on screen and changing while the number is given. Science: verify the boiling point at Everest's summit (≈ 68–71 °C at ~33–34 kPa; cite a standard source) and the egg-white/yolk setting temperatures (≈ 62–65 °C white starts, ≈ 70 °C+ yolk) and hedge to "barely cooks / stays runny" if the sources only give ranges. Primary metric: hook hold vs median 61.1 % (E13 target ≥ 65 % mean over TIL-14..16; reel 1 = 68.4 %); secondary: IG reach at 24 h vs E5 median 1,093 and watch ratio vs median 60 %. Review at TIL-16's 48 h (24 Nov 16:00).

### Production run 21 Nov 2026 (13:12–16:10 EET)
- **TIL-15 published on time** 16:00:03 EET (exec 5c5090e3… SUCCESS, 5 operations; IG DgAZSURDzAy, YT gJNJxehlwhk) — E13 reel 2 + first full E16 reel live. Make-credit rule (Claudio, 21 Nov): build used the 11:08 snapshot (2 h old); only the post-publish confirmation ran (8451991 exec d4803f27…, 8451995 exec d3a6a91a… SUCCESS, capture 15:02 CET = 16:02 EET). **Total 28,266 views (IG 12,893 + YT 15,373)**, +42 since 11:08; IG followers 6, YT subscribers 7. Snapshot rows added above (TIL-01..07/09–11 unchanged vs 11:08).
- **Findings:** 1. **TIL-14 24 h checkpoint = 327 IG accounts (0.30× E5 median 1,093), hook hold 66.7 %, watch 51 %** — E13's opening lifts the first seconds (66.7 % vs 61.1 % median) but without completion the reel did not get distributed; supports finding 2 of 11:08 (reach tracks watch ratio) (low–medium, n = 1). 2. **IG reach is final by ~20 h** on every reel (TIL-08 1,093 at 24 h = 1,093 at 7 d; TIL-12 749 at 43 h = 749 at 72 h): the 24 h checkpoint is the decisive IG read; YT keeps adding (TIL-08 YT 1,480 → 1,692 from 24 h to 7 d) (medium, n = 14). 3. E16: no conversion read yet (TIL-15 live 2 min at capture; IG 6 / YT 7 flat since 17–20 Nov).
- **Adjustment applied:** none — NEXT BUILD INSTRUCTION (21 Nov 11:08) followed: **TIL-16 = queue #16 "Boiling an egg on Everest", E13 reel 3** (binding): frame 0 = SEA LEVEL vs EVEREST stations, boiled-egg halves drop at 0.08 s and land at 0.25 s — the sea-level halves hold their dome (COOKED), the Everest half slumps and spreads (RUNNY); no mountain until line 2. Middle protected (finding 2): 3–10 s keeps the pot/egg on screen and changing every 1–2 s (2/3 of air dots vanish at 4.6 s → thermometer climbs 20 → 70 and the boil starts at 6.1 s → 80 °C "white sets" mark lights at 7.7 s → spoon taps the runny egg at 10.0/10.6 s → yolk turns matte at 12.5 s). Science: West 1983 summit 253 vs 760 mmHg (≈1/3); boiling ≈70 °C (CK-12 ~70, IFLScience 68, Antoine at 253 mmHg 71.9 → card "68–72 °C"); ovalbumin = 54 % of the white, sets ≈80 °C (IFLScience); white 60–65 °C, yolk 62–70 °C (BCcampus) → spoken "the yolk *can* set before the white" (hedged). One logged choice: TIL-17 teaser = queue #17 **"POPCORN ON MARS"** (E5 food premise; next in queue) → **binding for TIL-17**; its numbers (Mars pressure, kernel burst pressure) are verified in that build. E13 status: reels 1–2 live, reel 3 in READY for 22 Nov 16:00; verdict at TIL-16's 48 h (24 Nov 16:00). E16 status: reel 1 (full) live today, reel 2 in READY; review after TIL-17's 24 h.

### Stats check 22 Nov 2026 13:16 EET (light run, Sunday; ran ~2 h after its 11:07 slot)
- Make 8451991 exec 02856644… and 8451995 exec f5b95fc4… (both status 1; capture 12:16 CET = 13:16 EET for all 15 IG + 15 YT media). **Total 30,619 views (IG 14,628 + YT 15,991), +2,353 since 21 Nov 15:02 CET** (+1,726 IG / +583 YT from TIL-15). IG followers 6 (flat since 17 Nov), YT subscribers 7 (flat since 20 Nov). Competitors not due (Mon/Thu). Data store 250779: 56 records removed (20 Nov 15:02 + 21 Nov 10:08 CET snapshots; newest per media kept) — the 100-record listing had cut off today's YT rows before the trim.

| Reel | Age | IG views | IG reach | Hook hold | Avg watch | Watch ratio | Shares / saves / reposts | YT views |
|---|---|---|---|---|---|---|---|---|
| TIL-09 olive oil | 165 h | 3,285 | 2,149 | 72.1 % | 11.1 s | 74 % | 0 / 0 / 0 | 1,477 |
| TIL-13 Jupiter weight | 69 h | 1,562 | 1,115 | 65.5 % | 8.6 s | 57 % | 0 / 0 / 2 | 1,080 |
| TIL-14 ice cream on Mercury (E13 r1) | 45 h | 445 | 328 | 66.8 % | 7.7 s | 51 % | 0 / 0 / 1 | 1,291 |
| **TIL-15 Earth stops spinning (E13 r2, E16 r1 full)** | **21.3 h** | **1,726** | **1,211** | **64.8 %** | **12.6 s** | **84 %** | 0 / 0 / 0 (11 likes) | **583** |
Other reels unchanged vs 21 Nov 15:02 (IG frozen; YT +0–15). Medians TIL-01..14: hook hold 61.1 %, watch ratio 60 %; E5 24 h IG reach median 1,093; YT 24 h median 1,118. Shares 0 on 14,628 IG views over 15 reels.
- **Findings:**
  1. **TIL-15 = best watch ratio of 15 reels (84 %, 12.6 s avg on 15 s; previous best TIL-09 74 %) and 1,211 IG accounts at 21 h = 1.11× the E5 median (> 1,000 IG views in 24 h)**, after TIL-14's 328. Hook hold 64.8 % (E13 reels 1–2 mean 65.8 % at ~24 h vs target 65 %). The middle had a new object reacting every 1–2 s (mug → plate + apple → book). Strengthens finding 2 of 21 Nov: watch ratio → IG reach now holds on 8 body/food reels (74 % → 2,149; 84 % → 1,211; 63 % → 1,093; 60 % → 1,079; 57–60 % → 749–1,115; 52 % → 328; 41 % → 124) (medium, n = 8, observational; TIL-15 not yet 48 h). An avg watch of 12.6 s on a 15 s reel implies replays/loops are part of it.
  2. **E16 (follow invite) is not converting yet (low, n = 1 full reel):** 0 IG follows + 0 YT subs on 1,211 IG accounts + 583 YT views in 21 h, with the pill at 5.0–8.2 s now inside a 12.6 s average watch (so it was seen). Baseline ≈ 1.2 per 1,000 (TIL-08..10). Since 17 Nov: 0 net followers over ≈ 3,400 IG accounts reached (TIL-12..15). Review stays at TIL-17's 24 h (24 Nov); TIL-16 is reel 2.
  3. YT on TIL-15 is behind (583 at 21 h = 0.52× the YT median; YT refreshes in batches, compare ≥ 12 h apart) — not a drop yet; check at the 16:02 capture.
- Experiment ideas from finding 1 (backlog): (a) **E17 cascade middle** — a new familiar object reacts every 1–2 s from 3 to 10 s (TIL-15 pattern) as the tested variable; (b) **E18 loop ending** — last frame visually rhymes with frame 0 so the replay is seamless (follow end card kept, shown before the rhyme frame), to lift replays/watch ratio; (c) payoff-first middle (number by 5 s, then consequences only).
- **Selection: keep current** for TIL-17 (bound to "POPCORN ON MARS"): E13 is complete with TIL-16 and gets its verdict at TIL-16's 48 h (24 Nov); TIL-16 already applies the protected middle, so TIL-17 keeps both as constants. E17 (a) is the next variable, to start at the first build after the E13 verdict.

NEXT BUILD INSTRUCTION (from 22 Nov 13:16 check): keep current. Build **TIL-17 = queue #17 "Popcorn on Mars"** (binding: TIL-16 end card). Keep as constants: E13 opening (within 0.5 s a familiar kernel/pan visibly reacts beside an EARTH control — e.g. Earth kernels popping into fluffy popcorn vs Mars kernels that pop small/dense or just split; no planet-only or readout-only first frame), the protected middle as in TIL-15/16 (a new on-screen change every 1–2 s from 3 to 10 s while the number is given — TIL-15 cascade: 84 % watch), E5 food framing, hook as a claim that sounds wrong but is true, 15 s / 1.10, caption v2 with the follow line, E16 FOLLOW pill 5.0–8.2 s + end card, ⚠️ "Don't try this." on caption + card, 16:00 on time. Science to verify in the build: Mars surface pressure ≈ 0.6 kPa (NASA, ≈ 0.6 % of Earth); kernel pops when internal steam reaches ≈ 9 atm / ~180 °C (cite a food-science source); on Mars, water boils at ≈ 0–2 °C and the hull's pressure difference is larger, so state only what sources support (e.g. "pops early / smaller"); hedge if sources disagree; the pan heats in a pressurised habitat or note open-air assumption. Primary metric: watch ratio vs median 60 % and IG reach at 24 h vs E5 median 1,093; secondary: hook hold vs 61.1 %, E16 follows per 1,000 reach.

### Week 2 (15–22 Nov 2026), written 22 Nov 13:16
- Output: 7 reels (TIL-09..15), 2 late (TIL-10 +2 h 52, TIL-11 +3 h 44), then 5 on time in a row; READY buffer held every day (TIL-16 ready for today). Facebook Page added as a third channel (21 Nov). Totals 30,619 views (IG 14,628 + YT 15,991) vs 13,498 a week ago (+127 %); IG followers 1 → 6, YT subs 5 → 7.
- What worked: E5 body/food topic rule (verdict PASS 19 Nov); side-by-side proof openings with the object visibly reacting (E13 reels 1–2 hook hold 66.7 / 64.8 % vs 61.1 % median); a middle with continuous change (TIL-15 84 % watch).
- What did not: E7 end-card teaser (no follower lift, closed 20 Nov); hook hold alone does not drive reach (TIL-14 68 % hold, 328 accounts); shares still 0 on 14,628 IG views; follower growth stalled at 6 since 17 Nov despite the E16 invite.
- Bottlenecks, in order: (1) follower conversion (0 net follows on ≈ 3,400 accounts since 17 Nov); (2) completion/watch ratio, which decides IG distribution; (3) sharing (0).
- Next week: E13 verdict 24 Nov; E16 review 24 Nov; then E17 cascade middle. **No new playbook version:** the watch-ratio → reach link is observational (n = 8) and E17 will test it; playbook v2 + follow invite stand.

NEXT BUILD INSTRUCTION (from 22 Nov 13:20 — Claudio: "make the check weekly"; the stats/experiment check now runs Sundays only, next 29 Nov 11:07, so this instruction covers the whole week and replaces the 13:16 line where different): **TIL-17** as in the 13:16 line (Popcorn on Mars; E13 opening + protected middle as constants). **TIL-18, TIL-19, TIL-20 = E17 (cascade middle)**, the single variable: from 3 to 10 s a NEW familiar object (or a new part of the same object) visibly reacts every 1–2 s, escalating, while the number is spoken (TIL-15 pattern: mug → plate + apple → book; 84 % watch); keep E13 opening, E5 topic rule, hook style, 15 s / 1.10, caption v2 + follow line, E16 pill 5.0–8.2 s + end card, ⚠️ "Don't try this." on caption + card, 16:00 on time. Primary metric: watch ratio vs median 60 %; secondary: IG reach at 24 h vs E5 median 1,093, hook hold vs 61.1 %. **TIL-21 onward (until the 29 Nov check):** keep the TIL-20 format unchanged (no new variable). Topics: follow the queue order in EPISODES.md, each daily build binding the next one through its end card as now. Reviews moved to the weekly check of 29 Nov: E13 verdict (TIL-14..16), E16 follow-invite review (TIL-15 onward), E17 first read (TIL-18..20 at ≥ 48 h only for TIL-18/19; TIL-20 at its 24 h).

### Production run 22 Nov 2026 (17:45–19:15 EET, session started late)
- **TIL-16 published 1 h 46 min late** 17:45:56 EET (exec 6bf8b6a6… SUCCESS, 5 operations; IG DgDKLqEDmPH, YT 7OjiRahIKHk; FB exec e71b7fa5… SUCCESS) — E13 reel 3 live, slot-confounded (the scheduled session began at ~17:45). Stats: the 13:16 capture was > 3 h old, so the post-publish confirmation run served as the snapshot (17:47 EET): **total 30,628 views (IG 14,634 + YT 15,994)**; IG followers 6, YT subs 7. Medians (TIL-01..15): hook hold 63.0 %, watch ratio 61 %.
- **Findings:** 1. TIL-15 at 24 h (25.8 h) = 1,211 IG accounts with watch ratio 84 % (best of 16) — the cascade middle lifts completion and distribution (medium, observational; E17 tests it from TIL-18). 2. TIL-14 confirmed at 49.8 h: 328 accounts, hook hold 66.8 %, watch 51 % — hook hold alone does not earn reach (medium–low). 3. E16: still 0 follows on 1,211 accounts (low; review 29 Nov).
- **Adjustment applied:** none — NEXT BUILD INSTRUCTION (22 Nov 13:20) followed: **TIL-17 = queue #17 "Popcorn on Mars"** with E13 opening (EARTH vs MARS pans popping from 0.08 s, Mars flakes visibly 2× volume) and protected middle as constants (air dots vanish 4.5 s → gauge 0 → 9 ATM 6.1–7.8 s → burst 8.0 s → EARTH-size flake 8.8 s → Mars flake puffs to 2× 9.7 s → duds 12.3 s); E5 food framing; caption v2 + follow line; ⚠️ on caption + card. Science: NASA Mars 6.36 mb (≈0.6 % of 1,013); popcorn.org 135 psi ≈ 9 atm, 347 °F ≈ 175 °C; Quinn, Hong & Both 2005 (1/30 atm: expansion volume more than doubled, unpopped ÷5) — hedged as a lab result, Mars thinner still. Teaser binds **TIL-18 = #18 water on the Moon = E17 reel 1**. Experiment status: E13 3/3 published (verdict 29 Nov), E16 running, E17 starts TIL-18.

### Production run 23 Nov 2026 (20:30–21:25 EET, session started late)
- **TIL-17 published 4 h 32 min late** 20:31:46 EET (exec ca4871a9… SUCCESS, 5 operations; IG DgGB9LwjSoV, YT 2kRxqWRTU2c; FB exec 6d7d06c0… SUCCESS). Snapshot = Make 8451991 / 8451995 at 20:31–20:32 EET (no Monday 11:07 check under the weekly cadence).

| Reel | Age | IG views | IG reach | Hook hold | Avg watch | Watch ratio | Shares / saves | YT views |
|---|---|---|---|---|---|---|---|---|
| TIL-09 olive oil | 196 h | 3,285 | 2,149 | 72.1 % | 11.1 s | 74 % | 0 / 0 | 1,483 |
| TIL-10 10× taller | 170 h | 1,534 | 1,079 | 61.0 % | 9.0 s | 60 % | 0 / 0 | 1,123 |
| TIL-13 Jupiter weight | 100 h | 1,568 | 1,120 | 65.3 % | 8.6 s | 57 % | 0 / 0 | 1,087 |
| TIL-14 ice cream on Mercury | 76 h | 445 | 328 | 66.8 % | 7.6 s | 51 % | 0 / 0 | 1,308 |
| TIL-15 Earth stops spinning | 52 h | 1,730 | 1,212 | 64.8 % | 12.6 s | 84 % | 0 / 0 | 656 |
| **TIL-16 egg on Everest (late)** | **27 h** | **1,659** | **1,155** | **62.3 %** | **8.7 s** | **58 %** | 0 / 0 | **6** |
| TIL-17 popcorn on Mars | 0 h | 0 | 0 | – | – | – | – | 0 |
Other reels unchanged (IG frozen). Totals **32,406 views (IG 16,297 + YT 16,109)**; IG followers 6, YT subscribers 8. Medians TIL-01..16: hook hold 62.7 %, watch ratio 60 %; E5 24 h IG reach median 1,093.
- **Findings:** 1. TIL-16 at 24 h: 1,155 accounts (1.06× E5 median), hook hold 62.3 %, watch 58 % → E13 mean 64.6 % over 3 reels (target 65 %; verdict 29 Nov) (medium). 2. E5 reels cluster at ~1.1 k accounts (6 of 9); the one breakout had hook hold 72 % and watch 74 % — retention must be exceptional to leave the tier (low–medium). 3. YT anomaly: TIL-16 6 YT views at 27 h (cf. TIL-06), platform-side, IG/FB unaffected (low).
- **Adjustment applied:** none — 22 Nov 13:20 instruction followed: **TIL-18 = #18 "A glass of water on the Moon" = E17 reel 1** (cascade middle: glass boils 2.5 s → air vanishes 3.9 s → tea 4.7 s → soup 5.9 s → vase 6.9 s → four ice crusts 7.9–9.2 s → ice steams away 9.9 s → polar crater 11.8 s); E13 opening (EARTH glass calm vs MOON glass erupting from 0.08 s, iced over by ~1 s); caption v2 + follow line; ⚠️ on caption + card. Science: NASA NSSDC 3×10⁻¹⁵ bar (night); triple point 611.657 Pa; Harvard bell-jar demo; LRO Diviner < −397 °F (≈ −238 °C). Teaser binds **TIL-19 = #19 balloon on Mars (E17 reel 2)**. Experiment status: E13 complete (verdict 29 Nov), E16 running, **E17 reel 1 in READY for 24 Nov 16:00**.
- **Process risk:** the scheduled production session started +4 h 33 (22 Nov) and +7 h 18 (23 Nov) late; the buffer protects the build but not the 16:00 slot.

### Production run 24 Nov 2026 (13:12–16:20 EET, on schedule)
- **TIL-18 published on time** 16:00:03 EET (exec f31d65d0… SUCCESS, 5 operations; IG DgIHp5VDuHL, YT 7QnidzPiyQ0; FB exec c0ad2340… SUCCESS, 3 operations). A duplicate webhook delivery at 16:00:50 was stopped by the lock (exec 6c98317f… "Duplicate key") but auto-deactivated scenario 8451092; re-activated by this run. Snapshot = post-publish confirmation run 16:02 EET (no pre-publish stats run under the Make-credit rule).

| Reel | Age | IG views | IG reach | Hook hold | Avg watch | Watch ratio | Shares / saves | YT views |
|---|---|---|---|---|---|---|---|---|
| TIL-09 olive oil | 216 h | 3,285 | 2,149 | 72.1 % | 11.1 s | 74 % | 0 / 0 | 1,486 |
| TIL-13 Jupiter weight | 120 h | 1,569 | 1,122 | 65.3 % | 8.6 s | 57 % | 0 / 0 | 1,088 |
| TIL-14 ice cream on Mercury | 96 h | 445 | 328 | 66.8 % | 7.6 s | 51 % | 0 / 0 | 1,309 |
| TIL-15 Earth stops spinning | 72 h | 1,731 | 1,212 | 64.8 % | 12.6 s | 84 % | 0 / 0 | 659 |
| TIL-16 egg on Everest | 46 h | 1,659 | 1,155 | 62.3 % | 8.6 s | 58 % | 0 / 0 | 307 |
| **TIL-17 popcorn on Mars (late)** | **19.5 h** | **785** | **580** | **62.3 %** | **8.5 s** | **56 %** | 0 / 0 | **605** |
| TIL-18 water on the Moon | 0 h | 0 | 0 | – | – | – | – | 0 |
Totals **34,111 views (IG 17,085 + YT 17,026)**; IG followers 6, YT subscribers 8. Medians TIL-01..16: hook hold 62.7 %, watch ratio 60 %; E5 24 h IG reach median 1,093.
- **Findings:** 1. TIL-17 at 19.5 h: 580 accounts (0.53× E5 median at a younger age; posted 4 h 32 late), retention at the medians — the off-slot post is the likeliest drag (low–medium). 2. TIL-15 72 h final: watch 84 % still the best of 17 (medium). 3. TIL-16 YT 6 → 307 at 46 h: the anomaly was batch lag (medium).
| 27 Nov 16:10 | TIL-14 | 168.2 h | 446* | 329* | 66.9 %* | 7.6* (51 % of 15 s) | 0 | 0 | 1,311 (9 likes) | 6* / 8 |
| 27 Nov 16:10 | TIL-18 | 72.2 h | 166* | 125* | 56.0 %* | 8.0* (54 % of 15 s) | 0 | 0 | 404 (3 likes) | 6* / 8 |
| 27 Nov 16:10 | TIL-19 | 48.1 h | 560* | 399* | 64.3 %* | 8.2* (54 % of 15 s) | 0 | 0 | 970 (3 likes) | 6* / 8 |
| 27 Nov 16:10 | TIL-20 | 24.2 h | n/a | n/a | n/a | n/a | n/a | n/a | 1,095 (14 likes) | n/a / 8 |
(* = IG values from the 26 Nov 16:03 capture; no IG capture on 27 Nov — Instagram token invalidated, OAuth 190.)

- **Adjustment applied:** none — 22 Nov 13:20 instruction followed: **TIL-19 = #19 "A balloon on Mars" = E17 reel 2** (E13 opening: EARTH vs MARS balloons, Mars one pops at 1.0 s; cascade middle: air vanishes 4.2 s → balloon swells 4.5 → marshmallows 6.1 → snack bag 6.8 → glove 7.5 → ×2 → ×20 8.6–10.6 → tears 10.7 → pop 11.6 → rip vs sound bars 11.8); caption v2 + follow line; ⚠️ on caption + card. Teaser binds **TIL-20 = #20 candle in space (E17 reel 3)**. Experiment status: E13 complete (verdict 29 Nov), E16 running, **E17 reel 1 live, reel 2 in READY for 25 Nov 16:00**.

### Production run 25 Nov 2026 (13:12–16:20 EET, on schedule)
- **TIL-19 published on time by the guard task** 16:00:10 EET (exec db810191… SUCCESS; IG DgKsj76qPzQ, YT MZOVYps1WYU; FB exec bcb33db0… SUCCESS) — single delivery, no duplicate; this run (fallback only) sent nothing. Snapshot = guard's post-publish capture 16:02–16:03 EET.

| Reel | Age | IG views | IG reach | Hook hold | Avg watch | Watch ratio | Shares / saves | YT views |
|---|---|---|---|---|---|---|---|---|
| TIL-09 olive oil | 240 h | 3,285 | 2,149 | 72.1 % | 11.1 s | 74 % | 0 / 0 | 1,493 |
| TIL-13 Jupiter weight | 144 h | 1,571 | 1,124 | 65.3 % | 8.6 s | 57 % | 0 / 0 | 1,089 |
| TIL-14 ice cream on Mercury | 120 h | 445 | 328 | 66.8 % | 7.6 s | 51 % | 0 / 0 | 1,309 |
| TIL-15 Earth stops spinning | 96 h | 1,731 | 1,212 | 64.8 % | 12.6 s | 84 % | 0 / 0 | 660 |
| TIL-16 egg on Everest | 70 h | 1,659 | 1,155 | 62.3 % | 8.7 s | 58 % | 0 / 0 | 387 |
| TIL-17 popcorn on Mars (late) | 43.5 h | 800 | 590 | 62.4 % | 8.5 s | 57 % | 0 / 0 | 682 |
| **TIL-18 water on the Moon (E17 r1)** | **24.0 h** | **166** | **125** | **56.0 %** | **8.0 s** | **54 %** | 0 / 0 | **388** |
| TIL-19 balloon on Mars (E17 r2) | 0 h | 0 | 0 | – | – | – | – | 0 |
Totals **34,852 views (IG 17,268 + YT 17,584)**; IG followers 6, YT subscribers 8. Medians TIL-01..17: hook hold 62.4 %, watch ratio 60 %; E5 24 h IG reach median 1,093.
- **Findings:** 1. E17 reel 1 (TIL-18) at 24 h: 125 accounts (0.11× E5 median), hook 56.0 %, watch 54 % — no completion lift; the drop starts at the opening (medium–low, n = 1). 2. Two low-pressure space premises in a row fell (TIL-17 590 at 43.5 h, TIL-18 125) — supports the 24 Nov variety rule (low–medium). 3. TIL-16 final ~1.16 k accounts; YT batch lag confirmed (387) (medium).
- **Adjustment applied:** none — 22 Nov 13:20 instruction followed (n = 1 does not clearly contradict it; TIL-20 completes E17's three reels for the 29 Nov verdict): **TIL-20 = #20 "A candle in space" = E17 reel 3** (E13 opening: EARTH teardrop vs ORBIT ball flame at 0.08 s; cascade: hot air rises vs stalls 3.4 → blue 4.2 → timers 5.5 → Earth out at 10 MIN 6.7 → orbit 45 MIN 7.7 → wax ball 8.1–9.6 → pulses 10.2 → dies 11.3 → wax fog 11.3 → warning ring 12.3); caption v2 + follow line; ⚠️ on caption + card. Teaser binds **TIL-21 = V1 toast butter-side down** (lane C, variety rule). Experiment status: E13 complete, E16 running, **E17 reel 1 weak at 24 h, reel 2 live today, reel 3 in READY for 26 Nov 16:00** — verdict 29 Nov.

NEXT BUILD INSTRUCTION (from 25 Nov 16:20 — Claudio: "Change a bit the topics. Too many comparisons in earth and planets so far"; adds to the 22 Nov 13:20 instruction, which otherwise stands until the 29 Nov check): from **TIL-21**, **no planet/space premises and no EARTH-vs-planet split screens** (EPISODES.md "No-planets rule"). TIL-21 = V1 toast butter-side down (binding: TIL-20 end card). Keep the E13 principle (the object visibly reacts at t = 0 beside a control) but the control is the normal-world version of the same scene (e.g. 75 cm table vs 3 m table), and vary the frame (before/after, scale ladder or single escalating scene are allowed, not only left/right). Keep E17 cascade middle, E5, caption v2 + follow line, E16 pill + end card, ⚠️ on caption + card, 15 s / 1.10. Rotate lanes A/B/C/D/E, never the same twice in a row. TIL-20 (candle in space) stays in READY for 26 Nov — promised by TIL-19's end card; it is the last space reel.

### Production run 26 Nov 2026 (13:12–16:20 EET, on schedule)
- **TIL-20 published on time by the guard task** 16:00:13 EET (exec 0065f1ec… SUCCESS; IG DgNRRUszoi1, YT ENb5iRVbGD4; FB exec 6c005d14… SUCCESS) — single delivery; this run (fallback only) sent nothing. Snapshot = guard's post-publish capture 16:03 EET.

| Reel | Age | IG views | IG reach | Hook hold | Avg watch | Watch ratio | Shares / saves | YT views |
|---|---|---|---|---|---|---|---|---|
| TIL-09 olive oil | 264 h | 3,285 | 2,149 | 72.1 % | 11.1 s | 74 % | 0 / 0 | 1,493 |
| TIL-13 Jupiter weight (7 d) | 168 h | 1,574 | 1,127 | 65.3 % | 8.6 s | 57 % | 0 / 0 | 1,089 |
| TIL-15 Earth stops spinning | 120 h | 1,731 | 1,212 | 64.8 % | 12.6 s | 84 % | 0 / 0 | 660 |
| TIL-16 egg on Everest | 94 h | 1,661 | 1,157 | 62.4 % | 8.7 s | 58 % | 0 / 0 | 391 |
| TIL-17 popcorn on Mars (late) | 67.5 h | 800 | 590 | 62.4 % | 8.5 s | 57 % | 0 / 0 | 682 |
| TIL-18 water on the Moon (E17 r1) | 48 h | 166 | 125 | 56.0 % | 8.0 s | 54 % | 0 / 0 | 390 |
| **TIL-19 balloon on Mars (E17 r2)** | **24.0 h** | **560** | **399** | **64.3 %** | **8.2 s** | **54 %** | 0 / 0 | **969** |
| TIL-20 candle in space (E17 r3) | 0 h | 0 | 0 | – | – | – | – | 0 |
Totals **36,398 views (IG 17,834 + YT 18,564)**; IG followers 6, YT subscribers 8. Medians TIL-01..18: hook hold 62.4 %, watch ratio 60 %; E5 24 h IG reach median 1,093.
- **Findings:** 1. E17 cascade middle, 2 reels at 24 h: watch ratio 54 % / 54 % vs median 60 % — no completion lift so far (medium-low; n = 2 and both are space/low-pressure premises, so topic is a confound). 2. TIL-19 hook hold 64.3 % (above median) and YT 969 at 24 h (best early YT since TIL-14), but IG reach 0.37× the E5 median (low–medium). 3. TIL-18 frozen at 125 accounts at 48 h (final low).
- **Adjustment applied:** none — 22 Nov 13:20 + 25 Nov 16:20 instructions followed: **TIL-21 = V1 "Does toast really land butter-side down?"** (lane C, first no-planets reel): E13 reaction at t = 0 with a normal-world control (75 cm table → 3 m table as the twist), framing varied to a single escalating scene, E17 cascade middle kept (75 CM replay 2.0 s → scales 40 g vs 4 g 3.9 s → slow-mo ½ TURN 6.1–7.5 s → 8 school tables + counter 8.1–11.1 s → table grows to 3 m 11.5 s → full turn BUTTER-UP 13.7 s); caption v2 + follow line; ⚠️ on caption + card. Science: Matthews 1995 Eur. J. Phys. 16:172 (½ turn from 0.7–1.8 m; ≈ 3 m for a full turn; Ig Nobel Physics 1996); Stewart 1995 (butter ≤ 10 % of ~40 g, negligible); Matthews 2001 schools test (62 % of almost 10,000 drops). Teaser binds **TIL-22 = V2 "All your bacteria on a scale"** (lane A; Sender, Fuchs & Milo 2016, to verify in that build). Experiment status: E13 complete, E16 running, E17 3/3 published (TIL-20 today) — verdict 29 Nov.


### Production run 27 Nov 2026 (13:12–16:30 EET, on schedule)
- **TIL-21 NOT published** — guard sent the webhook once at 16:00:08 EET; Make exec d4aeb991… ERROR at the Instagram module (OAuth 190: session invalidated; connection 12732691). YouTube and Facebook did not run; scenario 8451092 inactive; queue holds the TIL-21 payload; lock TIL-21 set. This run (fallback) sent nothing: the lock means the slot counts as taken and a resend is forbidden; fix needs Claudio (reconnect → delete lock → reactivate). Push notification sent.
- Snapshot: YT 27 Nov 16:10 (this run's 8451995 exec f64f8684…); IG unavailable today (8451991 exec ad19ae3a… wrote no rows) → IG = 26 Nov 16:03.

| Reel | Age | IG views* | IG reach* | Hook hold* | Avg watch* | Watch ratio* | Shares / saves* | YT views |
|---|---|---|---|---|---|---|---|---|
| TIL-09 olive oil | 288 h | 3,285 | 2,149 | 72.1 % | 11.1 s | 74 % | 0 / 0 | 1,494 |
| TIL-14 ice cream on Mercury (7 d) | 168 h | 446 | 329 | 66.9 % | 7.6 s | 51 % | 0 / 0 | 1,311 |
| TIL-15 Earth stops spinning | 144 h | 1,731 | 1,212 | 64.8 % | 12.6 s | 84 % | 0 / 0 | 660 |
| TIL-16 egg on Everest | 118 h | 1,661 | 1,157 | 62.4 % | 8.7 s | 58 % | 0 / 0 | 391 |
| TIL-17 popcorn on Mars | 91.5 h | 800 | 590 | 62.4 % | 8.5 s | 57 % | 0 / 0 | 684 |
| TIL-18 water on the Moon (72 h) | 72 h | 166 | 125 | 56.0 % | 8.0 s | 54 % | 0 / 0 | 404 |
| TIL-19 balloon on Mars | 48 h | 560 | 399 | 64.3 % | 8.2 s | 54 % | 0 / 0 | 970 |
| **TIL-20 candle in space (24 h)** | 24 h | n/a | n/a | n/a | n/a | n/a | n/a | **1,095** |
(* IG as of 26 Nov 16:03.) Totals **≥ 37,496 views (IG 17,834 as of 26 Nov + YT 19,662)**; IG followers 6 (26 Nov), YT subscribers 8.
- **Findings:** 1. TIL-20 YT 1,095 at 24 h — best 24 h YT since TIL-14 (medium). 2. IG publishing and IG stats both blocked by the invalidated token; the 29 Nov weekly check needs the connection restored to judge E17 / TIL-21 (high). 3. YT subscribers flat at 8 since 24 Nov (low–medium; E16 review 29 Nov).
- **Adjustment applied:** none — 22 Nov 13:20 + 25 Nov 16:20 instructions followed: **TIL-22 = V2 "Every bacterium in your body on one scale"** (lane A after C; E13 balance hook with an apple as the everyday control; E17 cascade middle; caption v2 + follow line; ⚠️ on caption + card). Teaser binds **TIL-23 = V3 push a ship with one finger** (lane D). Buffer now TIL-21 (blocked) → TIL-22. Experiment status unchanged: E13 complete, E16 running, E17 3/3 published — verdict 29 Nov (IG data permitting).
- **Update 27 Nov 23:10 EET (Claudio: "fix it"):** Instagram token valid again → lock TIL-21 cleared, scenario 8451092 reactivated, queued TIL-21 published at 23:05 (exec 71258e6c… SUCCESS; IG DgQmpwfMKFu, YT Inm1PWd5Jv8; FB cb00977f… SUCCESS). 23:07 capture: **TIL-20 at 31 h — IG 1,582 views / 1,081 accounts, hook hold 70.3 %, watch 10.5 s = 70 %, 1 save; YT 1,112.** First E17 reel above the 60 % watch median and near the E5 reach median (1,093) — input for the 29 Nov E17 verdict. Totals 39,113 views (IG 19,431 + YT 19,682).
