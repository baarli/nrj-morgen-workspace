#!/bin/bash
# AUTO-SYNC TRIGGER - Runs automatically after every change
# This ensures Mission Control is ALWAYS consistent

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="/var/log/mission-control-auto-sync.log"

log() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🔄 AUTO-SYNC TRIGGERED"
log "======================="

# 1. Run the sync script
log "1️⃣ Running mission-control-sync.sh..."
bash "$WORKSPACE/scripts/mission-control-sync.sh" 2>&1 | tee -a "$LOG_FILE"

# 2. Regenerate pages from template
log "2️⃣ Regenerating pages from template..."
python3 "$WORKSPACE/scripts/generate-mission-control-pages.py" 2>&1 | tee -a "$LOG_FILE"

# 3. Deploy to Netlify
log "3️⃣ Deploying to Netlify..."
cd "$WORKSPACE/mission-control/public" && \
netlify deploy --prod \
    --site=834576a6-da2b-4412-9433-315f6437508a \
    --auth=nfp_8B3dDBwZS9W1GSHTUy3am4fia6iZmF6b0092 2>&1 | tail -5 | tee -a "$LOG_FILE"

# 4. Update timestamp
echo "$(date '+%Y-%m-%d %H:%M:%S')" > "$WORKSPACE/mission-control/public/.last-auto-sync"

log "======================="
log "✅ AUTO-SYNC COMPLETE"
log ""

# Notify user
bash "$WORKSPACE/scripts/notify-user.sh" complete \
    "Mission Control Auto-Sync" \
    "All pages regenerated and deployed to ensure consistency" \
    "medium" 2>/dev/null || true
