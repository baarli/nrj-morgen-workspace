#!/bin/bash
# vev-freeride-auto.sh
# Automatically use FreeRide fallback for all operations

export FREERIDE_AUTO="true"
export FREERIDE_PRIMARY="kimi-coding/k2p5"
export FREERIDE_FALLBACK="openrouter/gpt-4o,openrouter/claude-3-opus,openrouter/mistral-large"

WORKSPACE="/root/.openclaw/workspace"
LOG="$WORKSPACE/brain/logs/freeride-auto.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] FreeRide Auto enabled" >> "$LOG"
echo "Primary: $FREERIDE_PRIMARY" >> "$LOG"
echo "Fallbacks: $FREERIDE_FALLBACK" >> "$LOG"

# Run the Python fallback manager
python3 "$WORKSPACE/scripts/vev-freeride-fallback.py" --daemon >> "$LOG" 2>&1 &

echo "✅ FreeRide Auto started"
echo "PID: $!"
echo "Log: $LOG"
