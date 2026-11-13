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
| TIL-07 | 13 Nov 16:00 (READY) | Basketball on the Moon (air-filled dome) | 15 s | "You'd jump over the hoop." (player 6 m up) | v1 | E3, E4 |

Links: see EPISODES.md register (IG permalink + YouTube link per reel).

## Checkpoints (nearest capture to ~24 h / ~72 h / 7 d; actual age in brackets)
| ID | 24 h: IG views / reach · YT | 72 h: IG views / reach · YT | 7 d (due) |
|---|---|---|---|
| TIL-01 | 205 / 136 · 1,250 (27.8 h) | 207 / 137 · 1,688 (66 h) | due 15 Nov 19:07 |
| TIL-02 | 1,774 / 1,144 · 1,135 (25.1 h) | 1,776 / 1,146 · 1,222 (63.5 h) | due 15 Nov 21:52 |
| TIL-03 | 160 / 111 · 975 (27.2 h) | 160 / 111 · 1,166 (60.5 h; 72 h capture missed) | due 17 Nov 00:46 |
| TIL-04 | 169 / 113 · 464 (16.1 h) | due 13 Nov 19:00 | due 17 Nov 19:00 |
| TIL-05 | 706 / 510 · 1,118 (23 h) | due 14 Nov 16:00 | due 18 Nov 16:00 |
| TIL-06 | 183 / 117 · n/a (17.2 h, early read: hook hold 63.9 %, watch 10.4 s = 69 %) | due 15 Nov 16:00 | due 19 Nov 16:00 |
| TIL-07 | due 14 Nov 16:00 | due 16 Nov 16:00 | due 20 Nov 16:00 |
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

## Decisions
- 13 Nov: **stop E2** (one-tap yes/no comment prompt): 0 comments on ~1,000 IG views over TIL-03/04/05; also conflicts with the brief's "no engagement bait". Caption v2 from TIL-08: hook line, 3–4 science lines, one share line naming a person type, one series line ("A new impossible experiment every day."), disclaimer, ≤ 8 hashtags; no "Follow … for more", no question prompt. Logged as a minor confound for E5.
- 13 Nov: **retain** 16:00 slot, buffer-first publishing, cold open on the climax (E3, unresolved), 15 s / 1.10 (E4, verdict 15 Nov).
- 13 Nov: **selected E5** (see STRATEGY.md NEXT BUILD INSTRUCTION). Confidence low–medium: n = 5 own reels; topic is confounded with slot timing (TIL-05 was also the first on-time post).
