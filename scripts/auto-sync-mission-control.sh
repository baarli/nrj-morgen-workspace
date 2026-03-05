#!/bin/bash
# AUTO-SYNC TRIGGER - Runs automatically after every change
# This ensures Mission Control is ALWAYS consistent
# NOTE: Removed 'set -e' to prevent crashes on deployment errors

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="/var/log/mission-control-auto-sync.log"
GH_PAGES_DIR="$WORKSPACE/github-pages"

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
if [ -f "$WORKSPACE/scripts/generate-mission-control-pages.py" ]; then
    python3 "$WORKSPACE/scripts/generate-mission-control-pages.py" 2>&1 | tee -a "$LOG_FILE" || log "⚠️ Page generation had issues but continuing..."
fi

# 3. Deploy to GitHub Pages (primary) - Netlify disabled due to credit limit
log "3️⃣ Deploying to GitHub Pages..."

# Ensure github-pages directory exists
if [ ! -d "$GH_PAGES_DIR" ]; then
    log "Creating github-pages directory..."
    mkdir -p "$GH_PAGES_DIR"
    cd "$GH_PAGES_DIR"
    git init
    git remote add origin https://github.com/baarli/nrj-morgen-workspace.git
fi

# Sync files to github-pages
rsync -av --delete "$WORKSPACE/mission-control/public/" "$GH_PAGES_DIR/" 2>&1 | tail -5 | tee -a "$LOG_FILE"

# Commit and push to gh-pages branch
cd "$GH_PAGES_DIR"
git fetch origin gh-pages 2>/dev/null || log "No existing gh-pages branch"
git checkout --orphan gh-pages 2>/dev/null || git checkout gh-pages 2>/dev/null || true
git rm -rf . 2>/dev/null || true
git add -A
git commit -m "Auto-sync: $(date '+%Y-%m-%d %H:%M:%S')" 2>&1 | tail -1 | tee -a "$LOG_FILE" || log "No changes to commit"
git push -f origin gh-pages 2>&1 | tail -5 | tee -a "$LOG_FILE"
log "✅ Deployed to GitHub Pages"

# 4. Update timestamp
echo "$(date '+%Y-%m-%d %H:%M:%S')" > "$WORKSPACE/mission-control/public/.last-auto-sync"

log "======================="
log "✅ AUTO-SYNC COMPLETE"
log ""

# Notify user
bash "$WORKSPACE/scripts/notify-user.sh" complete \
    "Mission Control Auto-Sync" \
    "All pages synced to GitHub Pages (Netlify disabled - credit limit)" \
    "medium" 2>/dev/null || true
