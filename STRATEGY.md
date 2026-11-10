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
| E2 | 10 Nov 2026 00:46 (TIL-03) | Caption comment prompt as a one-tap yes/no question ("Would this ship ever make it to port? Yes or no") instead of an open opinion question | A one-tap answer lowers the effort to comment: comments > 0 per 1,000 IG views (0 so far on ~2,000 views) | running (1 of 3: TIL-03 0 comments on 160 IG views at 12.5 h; TIL-04 uses a one-word binary prompt) |
| E3 | 10 Nov 2026 19:00 (TIL-04, 3 h after the slot) | Flash-forward cold open: the first ~2 s show the climax (mannequin at the 10 m mark, high camera looking down), and the spoken + on-screen hook is a concrete number ("One second. Ten metres up.") before the story restarts from the ground | Hook hold is falling (72 → 67.5 → 61 %); opening on the payoff image + a number raises hook hold back to ≥ the median (67.5 %) | running |

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

## Weekly reviews
(none yet)
