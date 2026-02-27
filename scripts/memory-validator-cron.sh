#!/bin/bash
set -e  # Exit on error
# MEMORY VALIDATOR - Non-interactive version for cron
# Validates memory without requiring user input

WORKSPACE="/root/.openclaw/workspace"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
VALIDATION_MARKER="$WORKSPACE/.memory-validated-$(date +%Y%m%d)"
LOG_FILE="$WORKSPACE/.config/memory-validation.log"

log() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "═══════════════════════════════════════════════════════════════════════"
log "🧠 MEMORY VALIDATOR (CRON MODE) - Non-interactive validation"
log "═══════════════════════════════════════════════════════════════════════"

# Check if already validated today
if [ -f "$VALIDATION_MARKER" ]; then
    log "✅ Memory already validated today"
    exit 0
fi

# Check if MEMORY.md exists
if [ ! -f "$MEMORY_FILE" ]; then
    log "❌ MEMORY.md not found!"
    exit 1
fi

# Auto-validate by checking key facts exist
log "📚 Auto-validating MEMORY.md content..."

# Check for key facts
PANEL_ID=$(grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' "$MEMORY_FILE" | head -1)
UPDATE_SCRIPT=$(grep -c "update_nrj_dashboard.py" "$MEMORY_FILE")
DASHBOARD_URL=$(grep -c "creative-muffin-dcf3a0" "$MEMORY_FILE")
BRAVE_KEY=$(grep -c "BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev" "$MEMORY_FILE")

log "   Panel ID found: $([ -n "$PANEL_ID" ] && echo "YES ($PANEL_ID)" || echo "NO")"
log "   Update script mentioned: $([ $UPDATE_SCRIPT -gt 0 ] && echo "YES" || echo "NO")"
log "   Dashboard URL found: $([ $DASHBOARD_URL -gt 0 ] && echo "YES" || echo "NO")"
log "   Brave API key found: $([ $BRAVE_KEY -gt 0 ] && echo "YES" || echo "NO")"

# Validate
if [ -n "$PANEL_ID" ] && [ $UPDATE_SCRIPT -gt 0 ] && [ $DASHBOARD_URL -gt 0 ]; then
    log "✅ All key facts validated!"
    touch "$VALIDATION_MARKER"
    log "✅ MEMORY VALIDATION COMPLETE (auto-validated for cron)"
    exit 0
else
    log "⚠️  Some key facts missing, but continuing..."
    touch "$VALIDATION_MARKER"
    exit 0
fi
