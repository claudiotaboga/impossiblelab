# Campaign log: The Impossible Lab

Maintained by the scheduled runs under BRIEF.md (from 13 Nov 2026). Newest entries at the bottom of each section; never delete earlier entries. Detailed snapshots stay in STRATEGY.md → Snapshots; the publication register in EPISODES.md.

Metric definitions: **IG views** = Instagram `views` (plays incl. replays); **IG reach** = accounts reached (never mixed with views); **hook hold** = 100 − `reels_skip_rate`; **watch ratio** = `ig_reels_avg_watch_time` ÷ the reel's own length; **YT views** = YouTube view count. Baseline = median of comparable reels at the same checkpoint.
Missing data (13 Nov, updated 08:16 EET after Claudio's OK): scenario 8451991 now records the account's IG follower count on every snapshot (`followers=` in metrics; 1 follower on 13 Nov). Per-reel `follows` and `profile_visits` were tested the same morning and are **rejected by the Instagram API for Reels**, so follower conversion per reel is tracked as the change in the account follower count (IG) and YT subscribers between snapshots. Per-second retention curves are not available through the API. YouTube counts refresh in batches (compare only captures ≥ 12 h apart).

## Reels
| ID | Published (EET) | Topic | Format / duration | Hook (spoken + on-screen) | Creative version | Experiment |
|---|---|---|---|---|---|---|
| TIL-01 | 8 Nov 19:07 | Biking through a lake of whisky | Blender 3D, 15 s, voice 1.10 | "Whisky is thicker than water." | playbook v1 | — |
| TIL-02 | 8 Nov 21:52 | Diving into a pool of mercury | 16.5 s, voice 1.00 | "You can't drown in this pool." | v1 | E1 |
| TIL-03 | 10 Nov 00:46 (late) | Ship launched into a sea of honey | 16.5 s | "Ships float higher on honey." | v1 | E1, E2 |
| TIL-04 | 10 Nov 19:00 (3 h late) | Gravity reversed for one second | 16.5 s | "One second. Ten metres up." (cold open on climax) | v1 | E1, E2, E3 |
| TIL-05 | 11 Nov 16:00 | Boiling pasta on Mars | 15 s, voice 1.10 | "Pasta never cooks on Mars." | v1 | E2, E3, E4 |
| TIL-06 | 12 Nov 16:00 | Marathon at the speed of sound | 15 s | "A marathon in two minutes." | v1 | E3, E4 |
| TIL-07 | 13 Nov 16:00 (confirmed 14 Nov: exec 4a57507a… SUCCESS, IG Dfry8LwiPLm, YT CH-vb3eFBFI) | Basketball on the Moon (air-filled dome) | 15 s | "You'd jump over the hoop." (player 6 m up) | v1 | E3, E4 |
| TIL-08 | 14 Nov 16:00:02 (exec 0bc07905… SUCCESS, IG DfuXtOHk5bT, YT H-dUAmQbBeg) | Shrunk to 1 cm tall (your body) | Blender 3D, 15 s, voice 1.10 | "Big raindrops weigh more than you." (lab balance tipping toward a 5 mm drop, labels YOU 13 mg / DROP 65 mg) | v1 + caption v2 | E5 (1/3), E4 |
| TIL-09 | 15 Nov 16:00 (READY, built 14 Nov) | Swimming in a pool of olive oil (your body + kitchen staple) | Blender 3D, 15 s, voice 1.10 | "You'd sink in olive oil." (two tanks: WATER/FLOATS vs OLIVE OIL/SINKS, person sinking in the oil) | v1 + caption v2 | E5 (2/3), E4 |

Links: see EPISODES.md register (IG permalink + YouTube link per reel).

## Checkpoints (nearest capture to ~24 h / ~72 h / 7 d; actual age in brackets)
| ID | 24 h: IG views / reach · YT | 72 h: IG views / reach · YT | 7 d (due) |
|---|---|---|---|
| TIL-01 | 205 / 136 · 1,250 (27.8 h) | 207 / 137 · 1,688 (66 h) | due 15 Nov 19:07 |
| TIL-02 | 1,774 / 1,144 · 1,135 (25.1 h) | 1,776 / 1,146 · 1,222 (63.5 h) | due 15 Nov 21:52 |
| TIL-03 | 160 / 111 · 975 (27.2 h) | 160 / 111 · 1,166 (60.5 h; 72 h capture missed) | due 17 Nov 00:46 |
| TIL-04 | 169 / 113 · 464 (16.1 h) | 169 / 113 · 528 (66.2 h; next capture 88.1 h: 169 / 113 · 520) | due 17 Nov 19:00 |
| TIL-05 | 706 / 510 · 1,118 (23 h) | 712 / 517 · 1,378 (IG 72.0 h; YT 70.2 h, the 72 h YT row was beyond the listing limit) | due 18 Nov 16:00 |
| TIL-06 | 183 / 117 · n/a (17.2 h, early read: hook hold 63.9 %, watch 10.4 s = 69 %); 19.1 h: 183 / 117 · **5** (YT anomaly); 21.2 h (nearest capture before the 13 Nov Make outage): 183 / 117 · 5 | due 15 Nov 16:00 (early read 43.1 h: 183 / 117 · 8) | due 19 Nov 16:00 |
| TIL-07 | 178 / 125 · 895 (25.0 h; hook hold 55.2 %, watch 7.86 s = 52 %) | due 16 Nov 16:00 | due 20 Nov 16:00 |
| TIL-08 | due 15 Nov 16:00 | due 17 Nov 16:00 | due 21 Nov 16:00 |
| TIL-09 | due 16 Nov 16:00 | due 18 Nov 16:00 | due 22 Nov 16:00 |
24 h IG reach baseline (median TIL-01..05) = **136 accounts**; 24 h IG views median = 205; 24 h YT views median = 1,118.

## Competitor group (checked 13 Nov 2026 06:07 UTC via Make scenario 8550000, IG Business Discovery; public counts only)
Median = median views of the account's last reels that are ≥ 3 days old (up to 15 recent posts). Views ÷ followers = that median ÷ followers.
| Account | Followers | Median reel views | Views ÷ followers | Over-performers (≥ 2× own median) | Notes |
|---|---|---|---|---|---|
| [zackdfilms](https://www.instagram.com/zackdfilms/) | 11.55 M | 4.33 M | 0.37 | [Why Your Brain Focuses On Negative Things](https://www.instagram.com/reel/DfnLvTNCFqA/) 10.7 M; [Why Penny Lick Ice Cream Was Banned](https://www.instagram.com/reel/Dfkm9m-kcn4/) 9.9 M; [How Letting Go Can Set You Free](https://www.instagram.com/reel/DfiTZxigl8b/) 15.0 M | Closest format peer: 3D animated explainer, ~5 reels/day, titles "Why… / How… / The X That…" + one emoji |
| [kurzgesagt](https://www.instagram.com/kurzgesagt/) | 1.61 M | 187 k | 0.12 | [processed food reel](https://www.instagram.com/reel/DffB6fAH3Kx/) 718 k (3.8×) | Its space "what if" ([swap the Moon](https://www.instagram.com/reel/De6-yIzAVeA/), 157 k) sat at the median |
| [asapscience](https://www.instagram.com/asapscience/) | 637 k | 190 k | 0.30 | [Brothers…](https://www.instagram.com/reel/Dez4FepvBP-/) 405 k; [Is your hand…](https://www.instagram.com/reel/Dd9iKjVvCxU/) 400 k | Body/identity questions about the viewer; low posting frequency |
| [thephysicsgirl](https://www.instagram.com/thephysicsgirl/) | 572 k | 115 k | 0.20 | personal/health updates (not transferable); [nuclear submarine dive](https://www.instagram.com/reel/DZbE-awEuBK/) 419 k | Danger + "what could go wrong" framing over-performs demos |
| [sciencechannel](https://www.instagram.com/sciencechannel/) | 2.65 M | 35 k | 0.013 | none | Large, low-ratio TV clips: typical, not a model |
| [scishow](https://www.instagram.com/scishow/) | 147 k | 10.8 k | 0.07 | none | Promo-heavy, few reels |
| [physicsfun](https://www.instagram.com/physicsfun/) | 1.95 M | n/a (API returned no view counts) | n/a | — | Physics toys; likes ~0.6–2.5 k |
Dropped: smartereveryday (no reels since 2024). Not resolvable via Business Discovery: veritasium, vsauce, minutephysics, theactionlab, stevemould, nilered, popmech. **Gap:** no smaller (< 100 k) format peer yet; add 1–3 at the next check.

Transferable principles (hypotheses, not rules):
1. Over-performers are about the viewer's own body, mind or food (zackdfilms brain/ice-cream, kurzgesagt processed food, asapscience body), while pure space "what ifs" sit at the median. Matches our own data: the two best IG reaches are mercury pool (drowning/body) and pasta (food).
2. Curiosity titles name a concrete object + a mechanism ("Why X…", "The X That Y") rather than a hypothetical frame.
3. Danger framing ("what could go wrong…") lifts even demo-style accounts.

## Experiment backlog
| ID | Idea | Variable | Primary metric | Status |
|---|---|---|---|---|
| E5 | Premises with stakes for the viewer's own body or an everyday object/food (you, your kitchen, your body) | topic selection rule | IG reach at 24 h vs baseline 136 | **selected 13 Nov** for TIL-08..10 |
| E6 | On-screen title + cover as a concrete curiosity line ("WHY YOU CAN'T…", "THE POOL YOU CAN'T DROWN IN") instead of "WHAT IF YOU…?" | title/cover wording | hook hold vs median 61.3 % | backlog (after E5) |
| E7 | End-card series teaser ("Tomorrow: <next experiment>") as the single reason to return | ending / CTA | change in IG followers + YT subscribers per 1,000 reach in the 24 h after the post (per-reel follows are not exposed for Reels) | backlog |
| E8 | YouTube-specific packaging: YT title as a concrete curiosity line ("Why pasta never cooks on Mars") instead of "What if you…?" | YT title wording | YT views at 24 h vs median 1,118 | backlog (only once YT distribution is confirmed healthy) |
| E9 | First second shows a human body part for scale (hand, face, feet) in the impossible situation, instead of an empty set/object | opening visual | hook hold vs median 61.3 % (TIL-07: 55.6 %, lowest so far) | backlog (added 14 Nov; after E5) |

## Decisions
- 13 Nov: **stop E2** (one-tap yes/no comment prompt): 0 comments on ~1,000 IG views over TIL-03/04/05; also conflicts with the brief's "no engagement bait". Caption v2 from TIL-08: hook line, 3–4 science lines, one share line naming a person type, one series line ("A new impossible experiment every day."), disclaimer, ≤ 8 hashtags; no "Follow … for more", no question prompt. Logged as a minor confound for E5.
- 13 Nov: **retain** 16:00 slot, buffer-first publishing, cold open on the climax (E3, unresolved), 15 s / 1.10 (E4, verdict 15 Nov).
- 13 Nov: **selected E5** (see STRATEGY.md NEXT BUILD INSTRUCTION). Confidence low–medium: n = 5 own reels; topic is confounded with slot timing (TIL-05 was also the first on-time post).
- 13 Nov 11:08 (stats check): **YouTube anomaly** — TIL-06 at 5 YT views at 19 h (median 1,118 at 24 h), channel +18 views in 21 h. Decision for Claudio: check TIL-06 (nV-sE7p3f4w) visibility / "made for kids" / restrictions in YouTube Studio; if the Make YT module sets privacy/madeForKids, confirm values. **Retain** E5 for TIL-08 (keep current, no new variable). TIL-06 IG reach 0.86× baseline (non-body premise) — weak support for E5. Data store 250779 trimmed 98 → 68 records (oldest snapshots before 11 Nov 12:00 removed, newest per media kept).
- 13 Nov 13:15 (production run): Make publish scenario 8451092 checked: YouTube upload uses privacyStatus public, selfDeclaredMadeForKids false, containsSyntheticMedia true, notifySubscribers true, category 28 — the same for every upload, so these settings do not explain TIL-06's 5 YT views; the check in YouTube Studio is still needed. **Retain** E5: TIL-08 built (shrunk to 1 cm; hook proved on screen by a balance; caption v2). Snapshot unchanged vs 11:08 (IG frozen, YT +1).
- 13 Nov 16:00: **TIL-07 sent on time** (webhook answered "Accepted" at 16:00:00–16:00:01). From ~15:43 EET the Make connector of this session failed (Service Unavailable / 502 / "Failed to connect"), so the lock store, the execution result, the IG permalink and the YouTube link could **not** be confirmed in this run. Missing data: TIL-07 exec ID + links; TIL-06 24 h checkpoint capture (only 21.2 h available). Next run: run executions_list 8451092 (13 Nov ≥ 13:55 UTC), 8451991 and 8451995, then fill the TIL-07 register row before publishing TIL-08.
- 14 Nov 11:08 (stats check): **TIL-07 publish confirmed** (exec 4a57507ad5da42e08b9b204da522ad07 SUCCESS; IG Dfry8LwiPLm; YT CH-vb3eFBFI); register row filled. **YouTube restored:** TIL-07 894 YT views at 19 h, TIL-05 +259 → the stall is isolated to TIL-06 (8 views at 43 h). Decision for Claudio unchanged: check nV-sE7p3f4w in YouTube Studio (restrictions/visibility). **E4 provisional: no lift** (15 s / 1.10 mean hook 60.1 % / watch 61 % vs 16.5 s 62.5 % / 63 %); verdict 15 Nov; length is Claudio's rule, so flagged as his decision. **Retain** E5 (reel 2 = TIL-09). Backlog +E9 (body part in frame at t = 0). Total 10,312 views (IG 3,384 + YT 6,928), +1,326 since 13 Nov 13:15. Data store 250779 trimmed 94 → 76 (11 Nov snapshots removed). Missing data: per-reel follows/profile visits (not exposed for Reels), retention curves.
- 14 Nov 13:12–16:05 (production run): **TIL-08 published on time** at 16:00:02 EET (Make exec 0bc079057dfb49d3b660793c3c6afba4 SUCCESS, 5 operations; IG [DfuXtOHk5bT](https://www.instagram.com/reel/DfuXtOHk5bT/), YT [H-dUAmQbBeg](https://youtube.com/shorts/H-dUAmQbBeg)): E5 reel 1 live, fourth consecutive on-time post. **Retain** E5: TIL-09 built (queue B, pool of olive oil: hook proved by a water-vs-oil side-by-side; caption v2; brief in episodes/09-olive-oil-pool/brief.md), no new variable. Checkpoints filled: TIL-05 72 h, TIL-07 24 h. Snapshot vs 11:08: IG frozen on all seven older reels (TIL-07 +1 view / +1 account), YT unchanged (batch refresh); followers IG 1 / YT 3. Data store 250779 trimmed (12 Nov snapshots, 20 records, removed; newest per media kept). Missing data: YT 72 h row for TIL-05 (listing limit of 100 records; 70.2 h value used).
