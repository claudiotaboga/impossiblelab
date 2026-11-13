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
| E4 | TIL-05 (11 Nov 2026, approved by Claudio) | Back to 15 s and Kokoro speed 1.10 (from 16.5 s / 1.00); E3 cold open kept | At 48 h the 15 s / 1.10 reel held better (hook 72 %, watch 80 %) than 16.5 s / 1.00 (67.5 %, 68 %), and TIL-03/04 kept falling: a tighter, faster reel lifts hook hold and watch ratio back above the median | running (TIL-05 at 21 h: hook 60.5 %, watch 60 %, ≈ median, no lift yet; TIL-06 posts 12 Nov 16:00; TIL-07, the third E4 reel, built and in READY for 13 Nov; judge on 15 Nov when all three are ≥ 48 h) |
| E5 | TIL-08 (14 Nov 2026), 3 reels | Premise must put stakes on the viewer's own body or an everyday object/food (topic selection rule); caption v2 (E2 stopped) applied at the same time as a minor confound | Own top IG reaches (mercury 1,144, pasta 510 accounts) are body/food; competitor over-performers are body/mind/food (CAMPAIGN_LOG.md, 13 Nov): IG reach at 24 h ≥ 2× the baseline median of 136 accounts | selected 13 Nov; checkpoints 24 h / 72 h; verdict after TIL-10 at 72 h |

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

## Weekly reviews
(none yet)
