#!/bin/bash
# Mandatory Pre-Flight Enforcer v2.0 - AUTOMATIC
# This script runs automatically before any work begins
# NO MANUAL CONFIRMATION REQUIRED

set -e

WORKSPACE="/root/.openclaw/workspace"
PREFLIGHT_SCRIPT="$WORKSPACE/scripts/vev-preflight.py"
COMPLETION_MARKER="$WORKSPACE/.preflight-complete"

# Function to log
log_preflight() {
    echo "[$(date '+%H:%M:%S')] $1"
}

# Check if preflight was already completed this session
if [ -f "$COMPLETION_MARKER" ]; then
    MARKER_TIME=$(stat -c %Y "$COMPLETION_MARKER" 2>/dev/null || stat -f %m "$COMPLETION_MARKER" 2>/dev/null)
    CURRENT_TIME=$(date +%s)
    AGE_MINUTES=$(( (CURRENT_TIME - MARKER_TIME) / 60 ))
    
    if [ $AGE_MINUTES -lt 30 ]; then
        log_preflight "✅ Pre-flight completed $AGE_MINUTES minutes ago - skipping"
        exit 0
    else
        log_preflight "🔄 Pre-flight is $AGE_MINUTES minutes old - refreshing..."
        rm "$COMPLETION_MARKER"
    fi
fi

echo "═══════════════════════════════════════════════════════════════════════"
echo "🧠 VEV PRE-FLIGHT SYSTEM v2.0 - AUTOMATIC CONTEXT LOADING"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""

# Run the AUTOMATIC preflight
if [ -f "$PREFLIGHT_SCRIPT" ]; then
    log_preflight "Loading context automatically..."
    python3 "$PREFLIGHT_SCRIPT"
    echo ""
else
    echo "❌ Pre-flight script not found at $PREFLIGHT_SCRIPT"
    exit 1
fi

# Mark preflight as complete
touch "$COMPLETION_MARKER"

echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "✅ PRE-FLIGHT COMPLETE - Full context loaded automatically"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "💡 Tip: Context is also saved to .vev-preflight-context for reference"
echo ""
