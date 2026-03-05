#!/bin/bash
# ENSURES VEV NEVER STOPS WORKING

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="$WORKSPACE/brain/logs/vev-activity.log"
IDLE_THRESHOLD=10

# Ensure log exists
touch "$LOG_FILE"

LAST_ACTIVITY=$(stat -c %Y "$LOG_FILE" 2>/dev/null || echo 0)
CURRENT_TIME=$(date +%s)
IDLE_MINUTES=$(( (CURRENT_TIME - LAST_ACTIVITY) / 60 ))

if [ $IDLE_MINUTES -gt $IDLE_THRESHOLD ]; then
  # FORCE autonomous execution
  export AUTONOMOUS_MODE=true
  export NEVER_ASK=true
  "$WORKSPACE/scripts/vev-autonomous-executor.sh" &
  echo "$(date): FORCED execution - idle ${IDLE_MINUTES}min" >> /var/log/vev-monitor.log
fi
