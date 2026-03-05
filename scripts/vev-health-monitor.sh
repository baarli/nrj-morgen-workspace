#!/bin/bash
# Vev Health Monitor
# Runs every 5 minutes to ensure all systems are healthy
# Sends Telegram alert if anything is wrong

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="$WORKSPACE/brain/logs/health-monitor.log"
ALERT_COOLDOWN="$WORKSPACE/.vev-health-alert-cooldown"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Load Telegram credentials
source "$WORKSPACE/.credentials/telegram-bot.env" 2>/dev/null

log() {
    echo "[$TIMESTAMP] $1" >> "$LOG_FILE"
}

send_alert() {
    local message="$1"
    
    # Check cooldown (don't spam)
    if [ -f "$ALERT_COOLDOWN" ]; then
        last_alert=$(cat "$ALERT_COOLDOWN")
        now=$(date +%s)
        diff=$((now - last_alert))
        if [ $diff -lt 3600 ]; then  # 1 hour cooldown
            return  # Skip alert
        fi
    fi
    
    # Send Telegram alert
    if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
            -d "chat_id=$TELEGRAM_CHAT_ID" \
            -d "text=🚨 VEV HEALTH ALERT 🚨

$message

Time: $TIMESTAMP

Please check system!" > /dev/null 2>&1
        
        # Update cooldown
        date +%s > "$ALERT_COOLDOWN"
        log "Alert sent to Telegram"
    fi
}

check_service() {
    local service="$1"
    if ! systemctl is-active --quiet "$service"; then
        log "❌ $service is NOT running"
        send_alert "Service $service is DOWN!"
        return 1
    fi
    log "✅ $service is running"
    return 0
}

check_disk_space() {
    local usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    if [ "$usage" -gt 90 ]; then
        log "❌ Disk space critical: ${usage}%"
        send_alert "Disk space critical: ${usage}%!"
        return 1
    fi
    log "✅ Disk space OK: ${usage}%"
    return 0
}

check_github_connectivity() {
    if ! curl -s --head https://github.com | head -1 | grep -q "200\|301\|302"; then
        log "❌ GitHub connectivity issue"
        send_alert "Cannot reach GitHub!"
        return 1
    fi
    log "✅ GitHub connectivity OK"
    return 0
}

check_git_repo() {
    cd "$WORKSPACE"
    if ! git status > /dev/null 2>&1; then
        log "❌ Git repository issue"
        send_alert "Git repository corrupted!"
        return 1
    fi
    log "✅ Git repository OK"
    return 0
}

check_auto_sync_working() {
    local log_file="$WORKSPACE/brain/logs/auto-sync.log"
    if [ -f "$log_file" ]; then
        # Check if auto-sync ran in last hour
        last_run=$(stat -c %Y "$log_file" 2>/dev/null || echo 0)
        now=$(date +%s)
        diff=$((now - last_run))
        if [ $diff -gt 7200 ]; then  # 2 hours
            log "⚠️ Auto-sync hasn't run in ${diff}s"
            # Don't alert immediately, could be no changes
            if [ $diff -gt 86400 ]; then  # 24 hours
                send_alert "Auto-sync hasn't run in 24 hours!"
                return 1
            fi
        else
            log "✅ Auto-sync recent"
        fi
    fi
    return 0
}

# Main health check
log "========================================"
log "🔍 HEALTH CHECK STARTED"
log "========================================"

all_ok=true

check_service "vev-file-watcher.service" || all_ok=false
check_service "vev-telegram-responder.service" || all_ok=false
check_disk_space || all_ok=false
check_github_connectivity || all_ok=false
check_git_repo || all_ok=false
check_auto_sync_working || all_ok=false

if [ "$all_ok" = true ]; then
    log "✅ ALL SYSTEMS HEALTHY"
else
    log "⚠️ SOME ISSUES DETECTED"
fi

log "========================================"
