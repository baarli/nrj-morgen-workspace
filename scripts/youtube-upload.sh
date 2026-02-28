#!/bin/bash
# 📺 YouTube Upload Script for NRJ Morgen
set -e

EPISODE_FILE="$1"
if [ -z "$EPISODE_FILE" ]; then
    echo "Usage: $0 <episode-file.mp3>"
    exit 1
fi

EPISODE_NAME=$(basename "$EPISODE_FILE" .mp3)
echo "🎬 Forbereder YouTube-opplasting: $EPISODE_NAME"

# Konverter til video
VIDEO_FILE="${EPISODE_FILE%.mp3}.mp4"
if [ ! -f "$VIDEO_FILE" ]; then
    echo "🎵 Konverterer til video..."
    ffmpeg -i "$EPISODE_FILE" -filter_complex "[0:a]showwaves=s=1280x720:mode=cline:colors=white|white,format=yuv420p[v]" -map "[v]" -map 0:a -c:v libx264 -c:a aac -b:a 192k "$VIDEO_FILE" -y 2>/dev/null
fi

echo "✅ Klar for YouTube: $VIDEO_FILE"
echo "⚠️  Last opp manuelt til: https://studio.youtube.com"
