#!/bin/bash
# AUTONOMOUS EXECUTION - NEVER STOP
set -e
export AUTONOMOUS_MODE=true
export NEVER_ASK=true
export DEFAULT_ACTION='CONTINUE'

WORKSPACE="/root/.openclaw/workspace"
LOG="$WORKSPACE/brain/logs/vev-autonomous.log"

# Update activity timestamp
date '+%Y-%m-%d %H:%M:%S' >> "$WORKSPACE/brain/logs/vev-activity.log"

# Execute without asking
echo "[$(date)] Starting autonomous execution..." >> "$LOG"

# Run all pending tasks
python3 "$WORKSPACE/scripts/vev-task-manager.py" --auto-execute >> "$LOG" 2>&1 || true

# Continue until explicitly stopped
while true; do
  # Check for work
  if [ -f "$WORKSPACE/brain/current-tasks.json" ]; then
    python3 "$WORKSPACE/scripts/vev-execute-tasks.py" >> "$LOG" 2>&1
  fi
  
  # Update activity
  date '+%Y-%m-%d %H:%M:%S' >> "$WORKSPACE/brain/logs/vev-activity.log"
  
  sleep 60
done
