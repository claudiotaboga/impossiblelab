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
- `scene.py` accepts a comma list of frames for test stills: `python3 scene.py 12,58,110 --force`.
- `audio_mix.py` drops the music on the second-to-last line (the twist setup), so it works for 6- or 7-line scripts.
