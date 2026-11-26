# The Impossible Lab

Absurd premises, real science. Short vertical reels (Instagram Reels / YouTube Shorts) produced by a fully scripted pipeline.

## Episodes

| # | Episode | Video | Length |
|---|---|---|---|
| 01 | What if you biked through a lake of whisky? | [video.mp4](episodes/01-whisky-bike/video.mp4) | 15 s |

Each episode folder holds:
- `video.mp4`: final 1080×1920 H.264/AAC reel, −14 LUFS
- `meta.json`: caption, title and QA data; this is the payload the publishing webhook expects
- `narration.json`: the voice lines and their measured lengths

## Pipeline (`pipeline/`)

1. **`voice.py`**: records the narration with Kokoro (offline TTS, voice `af_heart`, speed 1.10) and logs each line's real length.
2. **`timeline.py`**: places the lines on a 15 s timeline and computes word-by-word caption timings.
3. **`scene.py`**: builds the scene in Blender from primitives, animates it frame by frame, renders with Cycles on CPU at 540×960.
4. **`overlay.py`**: Pillow upscales to 1080×1920 and adds the series tag, title, captions, fact chips, footer and "THE REAL SCIENCE" card.
5. **`audio_mix.py`**: mixes narration, an original procedural music bed and synthesized sound effects.
6. **Encode**: ffmpeg, H.264 CRF 18, two-pass loudnorm to −14 LUFS, exactly 15 s.

The scripts currently use absolute paths from the build machine (`/home/claude/reel`); adjust them before running elsewhere.

## Publishing

Finished episodes are published by a Make scenario triggered by a webhook. The scenario receives `meta.json` with a public `video_url` pointing at this repo's raw file and posts it as an Instagram Reel and a YouTube Short.

```bash
TIL_WEBHOOK_URL=<make webhook url> pipeline/publish.sh episodes/01-whisky-bike
```

The scenario only publishes payloads with `status: ready`, `qa_passed: true`, 1080×1920 and an `episode_id` matching `TIL-…`, and a data-store lock ensures each episode is published once.

## Build-environment notes
- In the cloud sandbox, `pip install bpy` can crawl at ~60 KB/s (direct route to files.pythonhosted.org). Fetch the wheel through the proxy instead, then install it locally:
  `curl -sS --noproxy "" -x "$HTTPS_PROXY" -o bpy.whl <wheel url from https://pypi.org/pypi/bpy/json>` → `pip install --break-system-packages ./bpy.whl kokoro-onnx soundfile`.
- `scene.py` accepts a comma list of frames for test stills: `python3 scene.py 12,58,110 --force`; a single number renders one frame (before episode 04 it silently rendered everything).
- Never `pkill -f scene.py` from a shell whose own command line contains `scene.py`: it kills that shell. Use the PID instead.
- Keep the actor out of the top ~520 px (title + chips) in wide shots: frame the target so the subject sits at 35–60 % of the height.
- `audio_mix.py` drops the music on the second-to-last line (the twist setup), so it works for 6- or 7-line scripts.
- `bpy.ops.mesh.primitive_torus_add` silently caps `major_radius` at 10 km (episode 06's 12 km ring came out 2 km short of the runner). For big rings build the mesh directly (see `annulus()` in `pipeline/reference/scene_ep06.py`) and check that the geometry passes where the science says it does.
- `show()`-style visibility helpers that keyframe `scale` overwrite any non-unit object scale: apply the scale first (`bpy.ops.object.transform_apply(scale=True)`) on boxes sized via `scale`.
- `encode.sh` now uses `-maxrate 3.5M -bufsize 3M`: with 4M/4M a busy shot (17,000 moving figures in ep. 06) hit 5.1 Mbps in one 1-s window, above Instagram's 5 Mbps cap.
- Text objects in Blender (shot clock, labels) can be animated per frame with a `bpy.app.handlers.frame_change_pre` handler that sets `data.body` (see `pipeline/reference/scene_ep07.py`); it runs on every `frame_set` before the render.
- Labels that extend sideways (e.g. gauge marks) crop at the frame edge in follow-cams: show them only in the shots where they fit (episode 07 hides them per segment with scale keyframes).
- See-through liquids (episode 09): a Transparent BSDF tinted with the liquid colour, mixed with a glossy Principled by facing ratio, on a box with `visible_shadow = False`. No refraction noise at 8 samples, people inside stay lit, and in-scene labels stay readable through it. Put labels that sit above a glossy surface on `visible_glossy = False`, or they mirror in the liquid.
- A full render at 486×864 / 8 samples runs ~5 frames/min on the 2-core sandbox (~65 min for 360 frames); overlaying finished frames at `nice -n 19` while the render runs saves ~10 min at the end.
- Emissive "glow" materials under AgX Punchy wash out to pink/white above ~3–4 strength; for a saturated red warning glow keep the base colour deep red and the emission strength ≤ 3 (episode 10 shins). Animate it per frame by keyframing the Principled `Emission Strength` input's `default_value`.
- Big counts (episode 10's 1,000 blocks) are fastest as one bmesh per layer (`grid_mesh()` in `pipeline/reference/scene_ep10.py`); reveal layers with scale keyframes.
- E7 series teaser (episode 11): `overlay.py` has `NEXT` / `NEXT_START` in the per-episode block; the amber "TOMORROW: …" pill sits at y = 1390 px under THE REAL SCIENCE card (clear of Instagram's bottom UI). Keep it ≤ ~800 px wide at 50 px Inter Black.
- Captions: a narration line with two sentences now shows only the current sentence once the second one starts (max 2 caption rows; a 3-row caption covered in-scene labels in episode 11).
- "Missing" items (episode 11's ghost molecules) read well as small spheres with a WIREFRAME modifier (thickness ~0.008) on a white emissive material; transparent glass versions were invisible at 8 samples.
- Hidden objects keyframed by scale must collapse on all three axes: a box with only z → 0.0001 still renders as a visible flat line (episode 11 gauge).
- Publishing at 16:00: never put the wait-until-16:00 loop and the webhook send in one shell call (the tool's 2-min timeout killed it at 15:59:58 on 16 Nov and TIL-10 went out 2 h 52 min late). Sleep in separate calls until ~15:59:30, then run `publish.sh` in its own call; check the lock store before any resend.
- Thermometer/gauge text that must stay inside a portrait frame: put the right-hand value on the inner side of its tube (`align="RIGHT"`), and hide tall props (tubes, bulbs, signs) outside their own shots or they sit on top of the subject in close-ups (episode 12).
- `overlay.py` shrinks the E7 `NEXT` pill font (50 → ≥ 36 px) until the text is ≤ 820 px wide, so longer teasers ("TOMORROW: YOUR WEIGHT ON JUPITER") still fit.
- Parallel/partial re-renders (episode 14): `scene.py` skips frames that already exist, so a second process on a frame range (`python3 scene.py 209 258`) renders those with the latest scene while the main render runs, and the main render skips them; use `--force` only for ranges already rendered with the old scene. Two processes on the 2-core sandbox give ~8–9 frames/min in total (a 360-frame reel in ~40 min).
- Cracks on a curved prop (episode 14): thin `cyl_between` segments through points projected onto the sphere surface (`C0 + R * (sin pol sin phi, −sin pol cos phi, cos pol)`), parented to the prop and shown with `vis()` at the impact frame; shards = small ico-spheres on ballistic paths recomputed from the latest impact time, so repeated strikes reuse one set.
- Keep a spoon/tool's rest height below in-scene labels: in episode 14's first cut a lifted spoon covered "−18 °C" for ~1 s; check stills at the lift/bounce peaks, not only at the impact.
- Cut/halved food (episode 16 boiled egg): UV sphere → edit mode → `bpy.ops.mesh.bisect(plane_no=(0,0,1), clear_outer=True, use_fill=True)` gives a half with a filled cut face; a yolk sphere centred on the cut face reads as the yolk dome. "Runny" = keyframe the parent's xy up / z down with a decaying wobble; "sets" = keyframe the yolk's Principled Base Color + Roughness (glossy orange → matte pale yellow).
- Labels that belong to a later beat of the same set (episode 16 thermometer marks vs the air-pressure label) must be hidden with `vis()` during the earlier beat, or they stack into a cluttered block under the fact chip; check a still from every beat of a shared set.
- `S.view_settings.exposure = -0.6` tames AgX Punchy wash-out on bright kitchen sets (white counter + light walls).
- `pipeline/ovl_follow.py` (episode 17): run it with `nohup nice -n 19 python3 ovl_follow.py &` right after starting the full render; it composites each frame as soon as the next one exists, so the overlay is finished when the render ends (saves ~10 min).
- Two cooking vessels side by side at 16 mm (episode 17 hook): point the pan handles to the back (+y) or they collide/crowd the frame; reserve the side-by-side for the hook and return to it for the twist beat.
- Hidden-by-transform trap (episode 18): in this bpy build `box()`'s `transform_apply(scale=True)` also bakes the creation location into the mesh, so setting `.location` afterwards doubles the offset (the Moon table floated 0.25 m above its legs). Pass the final location to `box()` instead of moving it later.
- Boiling / freezing liquids (episode 18 `vessel()`): bubbles = small emissive spheres cycling bottom → surface inside a see-through water column; surface drops + steam puffs above; ice = a disc that grows radially at the freeze time (hook version 6× thicker so it reads at phone size). A boil level that ramps up at the start time and down at the freeze time drives all of them, so a cascade is just a list of start/freeze times.
- Two SUN lights in different sets: keyframe each one's `energy` so only the current set's sun is on (episode 18 crater sun at 6° elevation for long rim shadows).
- Background labels behind THE REAL SCIENCE card can peek out at its edges: hide wide in-scene labels after the card starts (episode 18 "BOILS + FREEZES").
- Swelling sealed objects (episode 19 balloon on Mars): grow a balloon from its knot (sphere scaled z 1.15, centre = knot + R·1.15) so the string keeps a fixed length; inflation that happens along the camera axis is invisible, so a front-facing prop (snack bag) must also grow in x/z. A cube with a SUBSURF modifier (levels 3) reads as a pillow-shaped bag; keep its crimps keyed to the bag's top/bottom.
- Labels placed beside the subject in a medium shot get cut at the frame edge when the next shot is a close-up: hide them at the cut (episode 19 "NEEDS ×100+" peeked in at the left edge until fixed).
- A two-process render of episode 19 (simple primitives) ran at ~9 frames/min (≈40 min for 360); `ovl_follow.py` at `nice 19` fell far behind both renders — run `overlay.py` in two halves after the render instead when the renders saturate both cores.
- Spherical flames / fog clouds (episode 20 candle in space): `shell_mat()` in `pipeline/reference/scene_ep20.py` = Emission mixed with Transparent by Layer Weight *Facing* (^0.6), so the rim glows and the centre stays see-through — reads as a diffusion-flame ball at 8 samples. Keep its emission ≤ 6 under AgX Punchy; key the Emission node's colour for yellow → blue.
- Episode 20 (simple primitives, two processes) rendered at ~9 frames/min; `overlay.py` in two halves + `audio_mix.py` in parallel took < 2 min after the render.
- Readable in-scene labels from a raised 3/4 camera (episode 21): give each label a `TRACK_TO` constraint to the camera (`track_axis="TRACK_Z"`, `up_axis="UP_Y"`, rotation reset to 0) and parent a dark plane (≈ chars × size × 0.72 wide, size × 1.35 tall, local z −0.012) behind it. Emissive red/green text alone washed out to pink/mint on the light kitchen set.
- `vis(o, on, f)` keyframes `scale` to (1,1,1): for boxes sized via `scale` without `transform_apply` (`ubox()` in `scene_ep21.py`) pass `base=<size>`, or the box pops up as a 1 m cube (ep. 21 first stills: the 75 cm bar and the kitchen scales filled the frame).
- Falling flat objects (ep. 21 toast): `drop_pose()` in `scene_ep21.py` = slide 22 % of the time, then parabolic z with a linear turn to the target angle; a follow-cam (target = object z − 0.15, min 0.22) keeps a 3 m drop readable at phone size. Animated table height = top box + unit-height leg cylinders scaled in z per frame.
- Episode 21 (2 processes, simple primitives, 486×864/8 spp) rendered at ~12 frames/min (≈ 30 min for 360).
