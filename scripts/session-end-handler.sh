#!/bin/bash
# SESSION END HANDLER - Automatically runs at session end
# This ensures learning capture happens even if I forget

set -e

WORKSPACE="/root/.openclaw/workspace"
SCRIPT_DIR="$WORKSPACE/scripts"
LOG_FILE="$WORKSPACE/.session-end-log"

echo "$(date): Session end handler triggered" >> "$LOG_FILE"

echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "🏁 SESSION END DETECTED - Running mandatory cleanup"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""

# Run auto-learning capture
if [ -f "$SCRIPT_DIR/auto-learning-capture.sh" ]; then
    echo "📝 Running auto-learning-capture.sh..."
    bash "$SCRIPT_DIR/auto-learning-capture.sh"
    echo "$(date): auto-learning-capture completed" >> "$LOG_FILE"
else
    echo "❌ auto-learning-capture.sh not found!"
    echo "$(date): ERROR - auto-learning-capture.sh not found" >> "$LOG_FILE"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "✅ SESSION END PROCEDURES COMPLETED"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "All learnings have been captured."
echo "See you next session!"
echo ""
