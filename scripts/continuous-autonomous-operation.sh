#!/bin/bash
# Continuous Autonomous Operation - Ensures 24/7 autonomous operation
# This script runs continuously and ensures I never stop working

LOG_FILE="/var/log/continuous-autonomous.log"
WORKSPACE="/root/.openclaw/workspace"
HEARTBEAT_FILE="/tmp/last-autonomous-heartbeat"
PID_FILE="/tmp/continuous-autonomous.pid"

# Prevent multiple instances
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "Already running (PID: $OLD_PID)"
        exit 0
    fi
fi
echo $$ > "$PID_FILE"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Ensure I'm always running
ensure_continuous_operation() {
    log "=== Ensuring Continuous Operation ==="
    
    # Update heartbeat
    date +%s > "$HEARTBEAT_FILE"
    
    # Check if cron daemon is running
    if ! pgrep -x "cron" > /dev/null; then
        log "⚠️  Cron daemon not running - attempting to start"
        service cron start 2>/dev/null || cron 2>/dev/null || true
    fi
    
    # Check if OpenClaw gateway is running
    if ! pgrep -f "openclaw-gateway" > /dev/null; then
        log "⚠️  OpenClaw gateway not detected"
    fi
    
    # Ensure all scripts are executable
    chmod +x "$WORKSPACE/scripts/"*.sh 2>/dev/null || true
    chmod +x "$WORKSPACE/scripts/"*.py 2>/dev/null || true
    
    log "✅ Continuous operation checks complete"
}

# Self-healing mechanism
self_heal() {
    log "=== Self-Healing Check ==="
    
    # Check API health
    if ! curl -s http://47.84.19.119:8081/api/status > /dev/null 2>&1; then
        log "❌ API down - restarting"
        cd "$WORKSPACE/mission-control/api" && python3 total-control-api.py > /tmp/api.log 2>&1 &
        sleep 5
    fi
    
    # Check if heartbeat is stale (>5 minutes)
    if [ -f "$HEARTBEAT_FILE" ]; then
        LAST_HEARTBEAT=$(cat "$HEARTBEAT_FILE")
        CURRENT_TIME=$(date +%s)
        DIFF=$((CURRENT_TIME - LAST_HEARTBEAT))
        
        if [ $DIFF -gt 300 ]; then
            log "⚠️  Heartbeat stale ($DIFF seconds) - triggering recovery"
            # Trigger immediate task execution
            bash "$WORKSPACE/scripts/autonomous-mission-control.sh" > /tmp/recovery.log 2>&1 &
        fi
    fi
    
    log "✅ Self-healing complete"
}

# Generate new project if idle
generate_project_if_idle() {
    log "=== Checking for Idle Time ==="
    
    # Check if there are any active tasks
    ACTIVE_TASKS=$(find /tmp -name "autonomous-task-*" -mtime -0.01 2>/dev/null | wc -l)
    
    if [ "$ACTIVE_TASKS" -eq 0 ]; then
        log "📋 No active tasks - generating new project"
        
        # Generate new task
        cd "$WORKSPACE/scripts"
        python3 autonomous-task-generator.py >> /tmp/task-generation.log 2>&1
        
        # Check if new tasks were generated
        if [ -f "$WORKSPACE/.config/next-task-plan.json" ]; then
            log "🚀 New project generated - starting implementation"
            
            # Start implementation
            bash "$WORKSPACE/scripts/notify-user.sh" start \
                "Autonomous Project Generation" \
                "Generating and implementing new improvements to Mission Control" \
                "high" \
                "30 minutes"
            
            # Execute the plan
            bash "$WORKSPACE/scripts/autonomous-mission-control.sh" > /tmp/implementation.log 2>&1 &
        fi
    else
        log "✅ Active tasks found - continuing work"
    fi
}

# Never-ending loop
main() {
    log "🚀 Starting Continuous Autonomous Operation"
    log "This process will run 24/7 without stopping"
    
    # Initial setup
    ensure_continuous_operation
    
    # Main loop - runs forever
    while true; do
        log "--- Heartbeat ---"
        
        # Update heartbeat
        date +%s > "$HEARTBEAT_FILE"
        
        # Ensure continuous operation
        ensure_continuous_operation
        
        # Self-healing
        self_heal
        
        # Generate project if idle
        generate_project_if_idle
        
        # Log status
        log "💓 Heartbeat - $(date) - System operational"
        
        # Sleep for 2 minutes (check every 2 minutes)
        sleep 120
    done
}

# Cleanup on exit
cleanup() {
    log "🛑 Continuous operation stopping (this should not happen)"
    rm -f "$PID_FILE"
    exit 0
}

trap cleanup EXIT INT TERM

# Run main loop
main
