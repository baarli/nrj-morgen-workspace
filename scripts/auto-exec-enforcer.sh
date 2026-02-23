#!/bin/bash
# AUTO-EXEC ENFORCER - Forces execution of mandatory scripts
# This runs automatically and cannot be skipped

set -e

WORKSPACE="/root/.openclaw/workspace"
SCRIPT_DIR="$WORKSPACE/scripts"
LOG_FILE="$WORKSPACE/.auto-exec-log"

echo "$(date): Auto-exec enforcer started" >> "$LOG_FILE"

# Function to run script with verification
run_with_verification() {
    local script_name=$1
    local script_path="$SCRIPT_DIR/$script_name"
    local marker_file="$WORKSPACE/.$(basename $script_name .sh)-complete-$(date +%Y%m%d-%H%M)"
    
    if [ -f "$marker_file" ]; then
        echo "✅ $script_name already completed this session"
        return 0
    fi
    
    echo "🚨 MANDATORY: Running $script_name..."
    echo "This CANNOT be skipped. Press Ctrl+C to abort entire session."
    echo ""
    
    if [ -f "$script_path" ]; then
        bash "$script_path"
        touch "$marker_file"
        echo "✅ $script_name completed successfully"
        echo "$(date): $script_name completed" >> "$LOG_FILE"
    else
        echo "❌ $script_path not found!"
        echo "$(date): ERROR - $script_path not found" >> "$LOG_FILE"
        exit 1
    fi
}

# Main execution
echo "═══════════════════════════════════════════════════════════════════════"
echo "🔒 AUTO-EXEC ENFORCER - MANDATORY PROCEDURES"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""

# Run pre-flight
run_with_verification "mandatory-preflight.sh"

# Run memory validator
run_with_verification "memory-validator.sh"

echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "✅ ALL MANDATORY PROCEDURES COMPLETED"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "You may now proceed with work."
echo "Remember: auto-learning-capture.sh will run at session end."
echo ""
