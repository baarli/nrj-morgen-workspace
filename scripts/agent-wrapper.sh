#!/bin/bash
# AGENT WRAPPER - Forces pre-flight before any work
# This script wraps the agent and ensures mandatory procedures

set -e

WORKSPACE="/root/.openclaw/workspace"
PREFLIGHT_SCRIPT="$WORKSPACE/scripts/mandatory-preflight.sh"
COMPLETION_MARKER="$WORKSPACE/.preflight-complete-$(date +%Y%m%d)"

echo "═══════════════════════════════════════════════════════════════════════"
echo "🤖 AGENT WRAPPER - Initializing..."
echo "═══════════════════════════════════════════════════════════════════════"
echo ""

# Check if preflight was completed today
if [ ! -f "$COMPLETION_MARKER" ]; then
    echo "⚠️  Pre-flight not completed today!"
    echo ""
    
    # Run mandatory preflight
    if [ -f "$PREFLIGHT_SCRIPT" ]; then
        bash "$PREFLIGHT_SCRIPT"
        touch "$COMPLETION_MARKER"
    else
        echo "❌ Pre-flight script not found!"
        exit 1
    fi
else
    echo "✅ Pre-flight already completed today"
    echo ""
fi

echo "═══════════════════════════════════════════════════════════════════════"
echo "🚀 Agent ready to work with full context!"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
