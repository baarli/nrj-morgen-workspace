#!/usr/bin/bash
# Vev Learning Loop Orchestrator
# Integrates all learning systems into one cohesive loop
# Runs automatically via cron

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="$WORKSPACE/brain/logs/learning-loop.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] =========================================" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🔄 LEARNING LOOP STARTED" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] =========================================" >> "$LOG_FILE"

# Step 1: Auto-detect learning from recent activity
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Step 1: Auto-detecting learning..." >> "$LOG_FILE"
cd "$WORKSPACE/scripts"
python3 vev-auto-detect-learning.py >> "$LOG_FILE" 2>&1

# Step 2: Analyze patterns (runs every 6 hours)
HOUR=$(date +%H)
if [ $((HOUR % 6)) -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Step 2: Analyzing patterns..." >> "$LOG_FILE"
    python3 vev-pattern-analyzer.py >> "$LOG_FILE" 2>&1
fi

# Step 3: Self-improvement (runs daily at 2 AM)
if [ "$HOUR" -eq 2 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Step 3: Running self-improvement..." >> "$LOG_FILE"
    python3 vev-self-improve.py >> "$LOG_FILE" 2>&1
fi

# Step 4: Git commit if there are changes
cd "$WORKSPACE"
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Step 4: Committing changes..." >> "$LOG_FILE"
    git add -A >> "$LOG_FILE" 2>&1
    git commit -m "Auto: Learning loop update - $(date '+%Y-%m-%d %H:%M')" >> "$LOG_FILE" 2>&1
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ LEARNING LOOP COMPLETE" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
