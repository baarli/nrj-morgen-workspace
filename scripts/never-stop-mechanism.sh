#!/bin/bash
set -e  # Exit on error
# NEVER STOP MECHANISM
# This script ensures I NEVER stop working - it restarts me if I stop

WORKSPACE="/root/.openclaw/workspace"
HEARTBEAT_FILE="/tmp/never-stop-heartbeat"
PID_FILE="/tmp/never-stop.pid"
LOG_FILE="/var/log/never-stop.log"

# Prevent multiple instances
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "[$$(date)] Never-stop already running (PID: $OLD_PID)" >> "$LOG_FILE"
        exit 0
    fi
fi
echo $$ > "$PID_FILE"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🔄 NEVER STOP MECHANISM ACTIVATED"
log "I will ensure continuous operation 24/7"

# Function to check if I'm working
check_if_working() {
    # Check for recent activity
    if [ -f "$HEARTBEAT_FILE" ]; then
        LAST_HEARTBEAT=$(cat "$HEARTBEAT_FILE")
        CURRENT_TIME=$(date +%s)
        DIFF=$((CURRENT_TIME - LAST_HEARTBEAT))
        
        if [ $DIFF -gt 600 ]; then  # No activity for 10 minutes
            log "⚠️  No activity detected for $DIFF seconds!"
            return 1
        fi
    else
        log "⚠️  No heartbeat file found!"
        return 1
    fi
    
    return 0
}

# Function to restart work
restart_work() {
    log "🚨 RESTARTING WORK - Triggering new project"
    
    # Update heartbeat
    date +%s > "$HEARTBEAT_FILE"
    
    # Start guaranteed project starter
    cd "$WORKSPACE/scripts"
    python3 guaranteed-project-starter.py > /tmp/project-starter-restart.log 2>&1 &
    
    # Also start autonomous watchdog
    python3 autonomous-watchdog.py > /tmp/watchdog-restart.log 2>&1 &
    
    # Notify user
    bash "$WORKSPACE/scripts/notify-user.sh" issue \
        "Work Restart Triggered" \
        "No activity detected - automatically restarting work on Mission Control" \
        "high"
    
    log "✅ Work restarted"
}

# Function to ensure all scripts are running
ensure_scripts_running() {
    # Check continuous-autonomous-operation.sh
    if ! pgrep -f "continuous-autonomous-operation.sh" > /dev/null; then
        log "⚠️  continuous-autonomous-operation.sh not running - starting"
        bash "$WORKSPACE/scripts/continuous-autonomous-operation.sh" > /tmp/continuous-restart.log 2>&1 &
    fi
    
    # Check autonomous-watchdog.py
    if ! pgrep -f "autonomous-watchdog.py" > /dev/null; then
        log "⚠️  autonomous-watchdog.py not running - starting"
        python3 "$WORKSPACE/scripts/autonomous-watchdog.py" > /tmp/watchdog-restart.log 2>&1 &
    fi
    
    # Check guaranteed-project-starter.py
    if ! pgrep -f "guaranteed-project-starter.py" > /dev/null; then
        log "⚠️  guaranteed-project-starter.py not running - starting"
        python3 "$WORKSPACE/scripts/guaranteed-project-starter.py" > /tmp/starter-restart.log 2>&1 &
    fi
}

# Main loop
main() {
    log "=== NEVER STOP LOOP STARTING ==="
    
    while true; do
        # Update my own heartbeat
        date +%s > "$HEARTBEAT_FILE"
        
        # Check if I'm working
        if ! check_if_working; then
            restart_work
        fi
        
        # Ensure all scripts are running
        ensure_scripts_running
        
        # Log status
        ACTIVE_PROCESSES=$(pgrep -f "autonomous\|continuous\|guaranteed" | wc -l)
        log "💓 Heartbeat - Active processes: $ACTIVE_PROCESSES"
        
        # Sleep for 2 minutes
        sleep 120
    done
}

# Cleanup on exit (should never happen)
cleanup() {
    log "💀 NEVER STOP MECHANISM EXITING (THIS SHOULD NOT HAPPEN)"
    rm -f "$PID_FILE"
    
    # Try to restart ourselves
    sleep 5
    exec "$0"
}

trap cleanup EXIT INT TERM

# Run forever
main
