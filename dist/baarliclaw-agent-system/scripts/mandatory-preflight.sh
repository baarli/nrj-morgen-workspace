#!/bin/bash
# Mandatory Pre-Flight Enforcer
# This script MUST run before any work begins
# It blocks execution until checklist is complete

set -e

WORKSPACE="/root/.openclaw/workspace"
PREFLIGHT_SCRIPT="$WORKSPACE/scripts/preflight-checklist.sh"
COMPLETION_MARKER="$WORKSPACE/.preflight-complete"

echo "═══════════════════════════════════════════════════════════════════════"
echo "🚨 MANDATORY PRE-FLIGHT CHECK"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""

# Check if preflight was already completed this session
if [ -f "$COMPLETION_MARKER" ]; then
    MARKER_TIME=$(stat -c %Y "$COMPLETION_MARKER" 2>/dev/null || stat -f %m "$COMPLETION_MARKER" 2>/dev/null)
    CURRENT_TIME=$(date +%s)
    AGE_MINUTES=$(( (CURRENT_TIME - MARKER_TIME) / 60 ))
    
    if [ $AGE_MINUTES -lt 60 ]; then
        echo "✅ Pre-flight completed $AGE_MINUTES minutes ago"
        echo "   Skipping to work..."
        echo ""
        exit 0
    else
        echo "⚠️  Pre-flight is $AGE_MINUTES minutes old - refreshing..."
        rm "$COMPLETION_MARKER"
    fi
fi

echo "🛑 STOP: Pre-flight checklist REQUIRED before work"
echo ""
echo "This ensures I have full context and knowledge before starting."
echo ""
read -p "Press ENTER to run pre-flight checklist..."
echo ""

# Run the preflight checklist
if [ -f "$PREFLIGHT_SCRIPT" ]; then
    bash "$PREFLIGHT_SCRIPT"
else
    echo "❌ Pre-flight script not found!"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "📝 MANDATORY CONFIRMATION"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "Before proceeding, confirm:"
echo ""
read -p "Have you read MEMORY.md? (yes/no): " READ_MEMORY
if [ "$READ_MEMORY" != "yes" ]; then
    echo "❌ You MUST read MEMORY.md before starting work!"
    exit 1
fi

echo ""
read -p "Have you checked for relevant skills? (yes/no): " CHECKED_SKILLS
if [ "$CHECKED_SKILLS" != "yes" ]; then
    echo "❌ You MUST check for relevant skills before starting work!"
    exit 1
fi

echo ""
read -p "Do you understand the task context? (yes/no): " UNDERSTAND_CONTEXT
if [ "$UNDERSTAND_CONTEXT" != "yes" ]; then
    echo "❌ You MUST understand the context before starting work!"
    exit 1
fi

# Mark preflight as complete
touch "$COMPLETION_MARKER"

echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "✅ PRE-FLIGHT COMPLETE - You may now proceed with work"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "Remember to run auto-learning-capture.sh at the end!"
echo ""
