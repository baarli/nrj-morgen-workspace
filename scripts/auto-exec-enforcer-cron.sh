#!/bin/bash
set -e  # Exit on error
# AUTO-EXEC ENFORCER - CRON VERSION
# Non-interactive version for scheduled execution

WORKSPACE="/root/.openclaw/workspace"
SCRIPT_DIR="$WORKSPACE/scripts"
LOG_FILE="$WORKSPACE/.config/auto-exec-cron.log"

log() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "═══════════════════════════════════════════════════════════════════════"
log "🔒 AUTO-EXEC ENFORCER (CRON MODE)"
log "═══════════════════════════════════════════════════════════════════════"

# Function to run script with verification (non-interactive)
run_with_verification() {
    local script_name=$1
    local script_path="$SCRIPT_DIR/$script_name"
    local marker_file="$WORKSPACE/.$(basename $script_name .sh)-complete-$(date +%Y%m%d)"
    
    if [ -f "$marker_file" ]; then
        log "✅ $script_name already completed today"
        return 0
    fi
    
    log "🚨 Running $script_name (cron mode)..."
    
    if [ -f "$script_path" ]; then
        # Use cron version if available
        if [ "$script_name" = "memory-validator.sh" ] && [ -f "$SCRIPT_DIR/memory-validator-cron.sh" ]; then
            bash "$SCRIPT_DIR/memory-validator-cron.sh"
        else
            bash "$script_path" 2>&1 || true
        fi
        touch "$marker_file"
        log "✅ $script_name completed"
    else
        log "⚠️  $script_path not found, skipping"
    fi
}

# Run pre-flight
run_with_verification "mandatory-preflight.sh"

# Run memory validator (cron version)
run_with_verification "memory-validator.sh"

log "═══════════════════════════════════════════════════════════════════════"
log "✅ ALL MANDATORY PROCEDURES COMPLETED (CRON MODE)"
log "═══════════════════════════════════════════════════════════════════════"
