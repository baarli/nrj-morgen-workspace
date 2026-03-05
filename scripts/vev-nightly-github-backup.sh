#!/bin/bash
# Vev Nightly GitHub Backup
# Runs every night at 03:00 to ensure GitHub is always up to date
# Commits all changes and pushes to origin master

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="$WORKSPACE/brain/logs/nightly-github-backup.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] =========================================" >> "$LOG_FILE"
echo "[$TIMESTAMP] 🌙 NIGHTLY GITHUB BACKUP STARTED" >> "$LOG_FILE"
echo "[$TIMESTAMP] =========================================" >> "$LOG_FILE"

cd "$WORKSPACE"

# Step 1: Check if there are changes
echo "[$TIMESTAMP] Checking for changes..." >> "$LOG_FILE"
if [ -z "$(git status --porcelain)" ]; then
    echo "[$TIMESTAMP] No changes to commit" >> "$LOG_FILE"
    echo "[$TIMESTAMP] ✅ Nightly backup complete (no changes)" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
    exit 0
fi

# Step 2: Add all changes
echo "[$TIMESTAMP] Adding all changes..." >> "$LOG_FILE"
git add -A >> "$LOG_FILE" 2>&1

# Step 3: Create commit with timestamp
DATE_STR=$(date '+%Y-%m-%d')
echo "[$TIMESTAMP] Creating commit..." >> "$LOG_FILE"
git commit -m "Nightly backup - $DATE_STR

Automatic backup of all changes:
- Learning database updates
- Conversation history
- User profiles
- System logs
- Any file modifications

This ensures GitHub always has the latest version.

Backup time: $TIMESTAMP" >> "$LOG_FILE" 2>&1

if [ $? -ne 0 ]; then
    echo "[$TIMESTAMP] ❌ Commit failed" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
    exit 1
fi

# Step 4: Push to GitHub
echo "[$TIMESTAMP] Pushing to GitHub..." >> "$LOG_FILE"
git push origin master >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "[$TIMESTAMP] ✅ Successfully pushed to GitHub" >> "$LOG_FILE"
else
    echo "[$TIMESTAMP] ❌ Push failed" >> "$LOG_FILE"
fi

echo "[$TIMESTAMP] ✅ Nightly backup complete" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
