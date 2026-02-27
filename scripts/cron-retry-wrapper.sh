#!/bin/bash
set -euo pipefail
# Cron Job Retry Wrapper
# Adds retry logic to external API dependent cron jobs
# 
# SECURITY NOTE: This script uses "$@" to pass arguments safely.
# Do not pass untrusted user input to this script.

MAX_RETRIES=3
RETRY_DELAY=60

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

run_with_retry() {
    local attempt=1
    local exit_code=0
    
    while [ $attempt -le $MAX_RETRIES ]; do
        log "Attempt $attempt of $MAX_RETRIES: $*"
        
        # Run the command with arguments safely
        "$@" || exit_code=$?
        
        if [ $exit_code -eq 0 ]; then
            log "✅ Success on attempt $attempt"
            return 0
        fi
        
        log "⚠️ Attempt $attempt failed with exit code $exit_code"
        
        if [ $attempt -lt $MAX_RETRIES ]; then
            log "⏳ Waiting ${RETRY_DELAY}s before retry..."
            sleep $RETRY_DELAY
        fi
        
        attempt=$((attempt + 1))
        exit_code=0
    done
    
    log "❌ All $MAX_RETRIES attempts failed"
    return $exit_code
}

# Main execution
if [ $# -eq 0 ]; then
    echo "Usage: $0 <command> [args...]"
    echo "Example: $0 python3 /path/to/script.py"
    exit 1
fi

run_with_retry "$@"
exit $?
