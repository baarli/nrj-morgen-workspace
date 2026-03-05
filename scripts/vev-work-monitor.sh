#!/bin/bash
# vev-work-monitor.sh
# Ensures Vev keeps working autonomously

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="$WORKSPACE/brain/logs/vev-activity.log"
MONITOR_LOG="/var/log/vev-monitor.log"
IDLE_THRESHOLD_MINUTES=10

# Create log if doesn't exist
touch "$LOG_FILE"

# Check last activity
LAST_ACTIVITY=$(stat -c %Y "$LOG_FILE" 2>/dev/null || echo 0)
CURRENT_TIME=$(date +%s)
IDLE_MINUTES=$(( (CURRENT_TIME - LAST_ACTIVITY) / 60 ))

if [ $IDLE_MINUTES -gt $IDLE_THRESHOLD_MINUTES ]; then
  echo "$(date '+%Y-%m-%d %H:%M:%S'): Vev idle for ${IDLE_MINUTES}min - triggering autonomous execution" >> "$MONITOR_LOG"
  
  # Trigger autonomous work
  "$WORKSPACE/scripts/vev-autonomous-executor.sh" > /dev/null 2>&1 &
  
  # Update activity log
  echo "$(date '+%Y-%m-%d %H:%M:%S'): Autonomous execution triggered by monitor" >> "$LOG_FILE"
fi
