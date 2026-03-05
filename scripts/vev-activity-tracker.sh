#!/bin/bash
# VEV ACTIVITY TRACKER - Reports every minute

WORKSPACE="/root/.openclaw/workspace"
REPORT_FILE="$WORKSPACE/brain/logs/vev-minute-reports.log"
LAST_REPORT_FILE="$WORKSPACE/brain/logs/.last-report-time"

# Ensure files exist
touch "$REPORT_FILE"
touch "$LAST_REPORT_FILE"

# Check if we should report (every 60 seconds)
LAST_REPORT=$(cat "$LAST_REPORT_FILE" 2>/dev/null || echo 0)
CURRENT_TIME=$(date +%s)
TIME_DIFF=$((CURRENT_TIME - LAST_REPORT))

if [ $TIME_DIFF -ge 60 ]; then
    # Get current status
    CURRENT_TASK="Unknown"
    if [ -f "$WORKSPACE/brain/plans/mission-control-60-tasks.md" ]; then
        CURRENT_TASK=$(grep "^\- \[ \]" "$WORKSPACE/brain/plans/mission-control-60-tasks.md" | head -1 | sed 's/- \[ \] //' || echo "No active tasks")
    fi
    
    # Count completed tasks
    COMPLETED=$(grep "^\- \[x\]" "$WORKSPACE/brain/plans/mission-control-60-tasks.md" 2>/dev/null | wc -l)
    TOTAL=60
    
    # Generate report
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    REPORT="[$TIMESTAMP] PROGRESS: $COMPLETED/$TOTAL tasks | CURRENT: $CURRENT_TASK | STATUS: Working"
    
    echo "$REPORT" >> "$REPORT_FILE"
    echo "$CURRENT_TIME" > "$LAST_REPORT_FILE"
    
    # Also log to console for visibility
    echo "$REPORT"
fi
