# Episodes

## Register
| # | Episode ID | Date (EET) | Premise | Hook line | Length | Make exec | IG | YouTube |
|---|---|---|---|---|---|---|---|---|
| 01 | TIL-01 | 8 Nov 2026 19:07 | Biking through a lake of whisky | Whisky is thicker than water. | 15.0 s | 93029ec632584a19ac1d082c2eb5f0e7 | [DffQRVvDtzH](https://www.instagram.com/reel/DffQRVvDtzH/) | [LsY0nDQW1Zc](https://youtube.com/shorts/LsY0nDQW1Zc) |
| 02 | TIL-02 | 8 Nov 2026 21:52 | Diving into a pool of mercury | You can't drown in this pool. | 16.5 s | 9559508bcfdc4091bfb3a37c33066ce6 | [DffjNPrkrjD](https://www.instagram.com/reel/DffjNPrkrjD/) | [k4IGjqt1y7A](https://youtube.com/shorts/k4IGjqt1y7A) |
| 03 | TIL-03 | 10 Nov 2026 00:46 (9 Nov slot, 8 h 46 min late) | A ship launched into a sea of honey | Ships float higher on honey. | 16.5 s | c22f3293609644f8ad59c1a9786b4243 | [Dfib4ySiF1g](https://www.instagram.com/reel/Dfib4ySiF1g/) | [blv90cdrvmo](https://youtube.com/shorts/blv90cdrvmo) |
| 04 | TIL-04 | 10 Nov 2026 19:00 (16:00 slot, 3 h late) | Gravity reversed for one second | One second. Ten metres up. | 16.5 s | 1b9bf72da1ea4467843d06eb652f1d65 | [DfkZOtAD4Jo](https://www.instagram.com/reel/DfkZOtAD4Jo/) | [JrLsjK9ZiNg](https://youtube.com/shorts/JrLsjK9ZiNg) |
| 05 | TIL-05 | 11 Nov 2026 16:00 (on time; from READY) | Boiling pasta on Mars | Pasta never cooks on Mars. | 15.0 s | 1ab7499172db4e17a0eb3da4fd74e9fb | [DfmpWn_pbJK](https://www.instagram.com/reel/DfmpWn_pbJK/) | [YFPL9A8-KX0](https://youtube.com/shorts/YFPL9A8-KX0) |
| 06 | TIL-06 | 12 Nov 2026 16:00 (on time; from READY) | Running a marathon at the speed of sound | A marathon in two minutes. | 15.0 s | a1872f54522c4a3bb9f041704b30fdf7 | [DfpOOiYlRDP](https://www.instagram.com/reel/DfpOOiYlRDP/) | [nV-sE7p3f4w](https://youtube.com/shorts/nV-sE7p3f4w) |

## READY TO PUBLISH
Buffer: the daily run publishes the first entry here at 16:00 EET (its `meta.json` is final and its video is already hosted), moves it to the register, then builds the next episode into this section.

| Episode ID | Folder | Premise | Hook line | Length | SHA-256 | Built |
|---|---|---|---|---|---|---|
| TIL-07 | episodes/07-moon-basketball | Basketball on the Moon (court in an air-filled dome) | You'd jump over the hoop. | 15.0 s (E4) | `24c8a0a3ae3d6971fceedaea1958f5aafd6313e23febba865444cb44f1ca261b` | 12 Nov 2026 15:17 EET |

## Topic queue
Take the first item that is not in the register. Every premise must be buildable from Blender primitives, safe to show, and its science checkable. Verify every number before use; the notes are starting points, not facts.

1. ~~**Diving into a pool of mercury**~~ (done, TIL-02): density 13.5, you float with ~7 % submerged, can't dive or swim; the danger is the vapour above the pool.
2. ~~**A ship launched into a sea of honey**~~ (done, TIL-03): draft ~28 % shallower, honey thousands of times thicker, 1 m ripples fade in ~1 s, no barnacles. Note: the old claim "the launch wave never travels" was wrong: ship-scale waves (λ ≈ 10 m) survive ~1.5 min in honey; only small ripples die fast.
3. ~~**Gravity reversed for one second**~~ (done, TIL-04): rise 4.9 m in the flipped second, peak 9.8 m, land at ~13.9 m/s (~50 km/h) after 1.4 s; indoors the ceiling stops you after <1 m.
4. ~~**Boiling pasta on Mars**~~ (done, TIL-05; moved up 11 Nov: friction-off has no clean, checkable number per beat yet; air drag vs. friction is ambiguous): water boils near 0 °C at Mars pressure; the pasta never cooks; the fix is a pressure cooker.
5. **Friction switched off for one minute** (skipped again 11 Nov: still no clean, checkable number per beat): you can stand but not walk; knots slip, nails lose grip; friction returns at full speed.
6. **Shrunk to 1 cm tall**: falls are harmless, a raindrop is a trap, you'd have to eat like a shrew.
7. ~~**Running a marathon at the speed of sound**~~ (done, TIL-06; taken ahead of #5/#6 as the most visceral fully computable premise): 123 s; drag ≥ 17 kN with CdA 0.24 m² (the old ~35 kN note was too high); ≥ 5.8 MW ≈ 17,000× an elite ~341 W; 1 g turn radius 12 km.
8. **Shouting on Venus**: 92 bar, ~465 °C, air ~65× denser; your voice changes (hedge: modelled, uncertain).
9. **Every cat on Earth meowing at once**: total sound power less than one car engine; sound arrives staggered.
10. **Earth stops spinning for one second**: everything loose keeps moving east at up to ~465 m/s; at ~45° N that is about the speed of sound.
11. **A bowling ball dropped onto a trampoline made of soap film** (pick only if the science checks out cleanly).
12. **A cup of coffee the size of a lake**: how long it would take to cool, and what the steam would do.
13. ~~**Basketball on the Moon**~~ (done, TIL-07: 1 m Earth leap → 6.05 m, 5.5 s airtime, free throw ≈21 m in dome air ≈ 5× too far): 1/6 gravity (1.62 m/s²): the same jump goes ~6× higher and hangs ~6× longer; a free throw needs a much flatter, slower shot. Check: lunar g, standing-jump heights.
14. **A paper plane thrown from the International Space Station**: orbital speed ~7.7 km/s, no lift in near-vacuum, the plane stays in orbit beside you; re-entry heating if it ever drops (check published paper-plane-from-space experiments).
15. **A snowball fight on Mars**: thin CO₂ air, −60 °C average, snow there is partly dry ice that sublimates; check Phoenix lander snowfall data and CO₂ frost point (~−125 °C at Mars pressure).
16. **Swimming in a pool of olive oil**: oil ~0.91 g/cm³, you float lower, ~80× thicker than water; strokes feel slow; check viscosity and density of olive oil at 20 °C.
