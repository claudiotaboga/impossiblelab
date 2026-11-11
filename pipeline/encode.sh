#!/usr/bin/env bash
# Final encode: composited frames + mix -> Instagram/YouTube-compliant MP4.
# H.264 <= 3.5 Mbps (bufsize 3M keeps every 1-s window < 5 Mbps) (Instagram Reel cap is 5), AAC 128k 48 kHz, two-pass loudnorm to -14 LUFS, faststart.
# Usage: pipeline/encode.sh <comp_dir> <mix.wav> <out.mp4>
set -euo pipefail
COMP="$1"; MIX="$2"; OUT="$3"
DIR="$(cd "$(dirname "$0")" && pwd)"
DUR=$(python3 -c "import sys; sys.path.insert(0,'$DIR'); import config; print(config.DUR)")
J=$(ffmpeg -hide_banner -i "$MIX" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
MI=$(echo "$J" | python3 -c "import json,sys;d=json.load(sys.stdin);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -hide_banner -y -framerate 24 -i "$COMP/%04d.png" -i "$MIX" \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11:$MI:linear=true,aresample=48000" \
  -c:v libx264 -preset veryfast -crf 20 -profile:v high -pix_fmt yuv420p -g 48 -keyint_min 48 -sc_threshold 0 \
  -maxrate 3.5M -bufsize 3M -movflags +faststart -c:a aac -b:a 128k -ac 2 -t "$DUR" "$OUT"
