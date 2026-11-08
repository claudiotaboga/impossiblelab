#!/usr/bin/env bash
# Publish one episode: send its meta.json to the Make webhook
# ("TIL — Publish Reels (Instagram + YouTube Shorts)").
# Usage: TIL_WEBHOOK_URL=https://hook.eu1.make.com/... pipeline/publish.sh episodes/01-whisky-bike
# The webhook URL is kept out of this public repo on purpose.
set -euo pipefail
EP="${1:?usage: publish.sh <episode-folder>}"
: "${TIL_WEBHOOK_URL:?set TIL_WEBHOOK_URL to the Make webhook URL}"

URL=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['video_url'])" "$EP/meta.json")
CODE=$(curl -s -o /dev/null -w '%{http_code}' -I -L "$URL")
[ "$CODE" = "200" ] || { echo "video_url not reachable ($CODE): $URL"; exit 1; }

curl -sS -X POST -H 'Content-Type: application/json' --data @"$EP/meta.json" "$TIL_WEBHOOK_URL"
echo
