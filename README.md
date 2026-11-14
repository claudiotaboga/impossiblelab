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
