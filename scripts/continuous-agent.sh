#!/bin/bash
#
# continuous-agent.sh
# Holder BaarliClaw "levende" med hyppige heartbeats
# INKLUDERER: Selvbevissthet, Kreativitet, Personlige mål
#
# Architecture:
#   - Config Layer: All tunables at top
#   - Logging Layer: Centralized logging functions
#   - API Layer: All Supabase/external calls
#   - Business Logic: Task orchestration
#   - Main Loop: Execution flow
#

set -euo pipefail

# =============================================================================
# CONFIGURATION
# =============================================================================

readonly WORKSPACE="/root/.openclaw/workspace"
readonly SCRIPT_DIR="${WORKSPACE}/scripts"
readonly LOG_FILE="${WORKSPACE}/memory/continuous-agent.log"
readonly LAST_ACTIVITY_FILE="${WORKSPACE}/.last-agent-activity"
readonly CREDS_FILE="${WORKSPACE}/.credentials/nrj-morgen.env"

# Intervals (seconds)
readonly HEARTBEAT_INTERVAL=300  # 5 minutes
readonly GOALS_CHECK_INTERVAL_DAYS=7

# Creative time schedule
readonly CREATIVE_DAY=7   # Sunday (1=Monday, 7=Sunday)
readonly CREATIVE_HOUR=14 # 14:00

# Systems to monitor
readonly SYSTEMS=(
    mission_control
    morning_routine
    podcast_manager
    nrj_dashboard
    content_aggregator
)

# =============================================================================
# LOGGING LAYER
# =============================================================================

log() {
    local level="$1"
    local message="$2"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] [${level}] ${message}" | tee -a "$LOG_FILE"
}

log_info()  { log "INFO"  "$1"; }
log_warn()  { log "WARN"  "$1"; }
log_error() { log "ERROR" "$1"; }
log_debug() { log "DEBUG" "$1"; }

log_startup() {
    log_info "🚀 Continuous Agent started"
    log_info "Heartbeat interval: ${HEARTBEAT_INTERVAL}s"
    log_info "Features: monitoring, autonomy, self-awareness, creativity, goals"
}

log_shutdown() {
    log_info "🛑 Continuous Agent stopping"
}

# =============================================================================
# API LAYER (Supabase)
# =============================================================================

# Load credentials into environment
api_load_credentials() {
    if [[ -f "$CREDS_FILE" ]]; then
        # shellcheck source=/dev/null
        source "$CREDS_FILE" 2>/dev/null || true
    fi
}

# Build standard curl headers for Supabase
api_headers() {
    echo "-H" "apikey: ${SUPABASE_SERVICE_KEY}" \
         "-H" "Authorization: Bearer ${SUPABASE_SERVICE_KEY}"
}

# Generic Supabase GET request
# Usage: api_get "table?conditions" || echo "0"
api_get() {
    local endpoint="$1"
    local url="${SUPABASE_URL}/rest/v1/${endpoint}"
    
    curl -s "$url" \
        -H "apikey: ${SUPABASE_SERVICE_KEY}" \
        -H "Authorization: Bearer ${SUPABASE_SERVICE_KEY}" \
        2>/dev/null || echo ""
}

# Generic Supabase POST request
# Usage: api_post "table" '{"key":"value"}'
api_post() {
    local table="$1"
    local data="$2"
    local url="${SUPABASE_URL}/rest/v1/${table}"
    
    curl -s -X POST "$url" \
        -H "apikey: ${SUPABASE_SERVICE_KEY}" \
        -H "Authorization: Bearer ${SUPABASE_SERVICE_KEY}" \
        -H "Content-Type: application/json" \
        -d "$data" \
        > /dev/null 2>&1 || true
}

# Generic Supabase PATCH request
# Usage: api_patch "table?conditions" '{"key":"value"}'
api_patch() {
    local endpoint="$1"
    local data="$2"
    local url="${SUPABASE_URL}/rest/v1/${endpoint}"
    
    curl -s -X PATCH "$url" \
        -H "apikey: ${SUPABASE_SERVICE_KEY}" \
        -H "Authorization: Bearer ${SUPABASE_SERVICE_KEY}" \
        -H "Content-Type: application/json" \
        -d "$data" \
        > /dev/null 2>&1 || true
}

# =============================================================================
# BUSINESS LOGIC: Attention Monitoring
# =============================================================================

# Check for pending approvals
attention_check_approvals() {
    local result
    result=$(api_get "approval_requests?status=eq.pending&limit=1")
    [[ -n "$result" && "$result" != "[]" ]] && echo "1" || echo "0"
}

# Check for system errors
attention_check_errors() {
    local result
    result=$(api_get "system_status?status=eq.error&limit=1")
    [[ -n "$result" && "$result" != "[]" ]] && echo "1" || echo "0"
}

# Check for critical log entries
attention_check_critical() {
    local result
    result=$(api_get "activity_log?level=eq.critical&limit=1")
    [[ -n "$result" && "$result" != "[]" ]] && echo "1" || echo "0"
}

# Aggregate all attention checks
attention_check_all() {
    local count=0
    
    if [[ "$(attention_check_approvals)" == "1" ]]; then
        log_warn "⚠️  Pending approvals found"
        ((count++))
    fi
    
    if [[ "$(attention_check_errors)" == "1" ]]; then
        log_error "🚨 System errors detected"
        ((count++))
    fi
    
    if [[ "$(attention_check_critical)" == "1" ]]; then
        log_error "🔴 Critical events in log"
        ((count++))
    fi
    
    echo "$count"
}

# =============================================================================
# BUSINESS LOGIC: Messaging
# =============================================================================

# Send proactive message to activity log
message_send() {
    local msg_text="$1"
    local priority="${2:-normal}"
    
    log_info "📤 Sending proactive message: $msg_text"
    
    local json_data
    json_data=$(printf '{
        "level": "info",
        "category": "system",
        "message": "%s",
        "details": {"source": "continuous-agent", "priority": "%s"},
        "actionable": true
    }' "$msg_text" "$priority")
    
    api_post "activity_log" "$json_data"
}

# =============================================================================
# BUSINESS LOGIC: System Status Updates
# =============================================================================

# Get current UTC timestamp in ISO format
timestamp_now() {
    date -u '+%Y-%m-%dT%H:%M:%SZ'
}

# Update a single system's last_check timestamp
status_update_system() {
    local system_name="$1"
    local now
    now=$(timestamp_now)
    
    local json_data
    json_data=$(printf '{
        "last_check": "%s",
        "updated_at": "%s"
    }' "$now" "$now")
    
    api_patch "system_status?system_name=eq.${system_name}" "$json_data"
}

# Update all monitored systems
status_update_all_systems() {
    local system
    for system in "${SYSTEMS[@]}"; do
        status_update_system "$system" || log_warn "Failed to update $system"
    done
}

# =============================================================================
# BUSINESS LOGIC: Autonomous Tasks
# =============================================================================

# Run compliance checker if available
task_run_compliance() {
    local script="${SCRIPT_DIR}/compliance-checker.sh"
    
    if [[ -f "$script" ]]; then
        bash "$script" > /dev/null 2>&1 || log_warn "Compliance check failed"
    fi
}

# Log heartbeat completion
task_log_heartbeat() {
    local json_data
    json_data='{
        "level": "debug",
        "category": "system",
        "message": "Autonomous heartbeat check completed",
        "source": "continuous-agent"
    }'
    
    api_post "activity_log" "$json_data"
}

# Run all autonomous tasks
autonomous_tasks_run() {
    log_info "🤖 Running autonomous tasks..."
    
    status_update_all_systems
    task_run_compliance
    task_log_heartbeat
    
    log_info "✅ Autonomous tasks completed"
}

# =============================================================================
# BUSINESS LOGIC: Self-Awareness
# =============================================================================

# Get current emotional state from self-awareness check
self_awareness_get_state() {
    local script="${SCRIPT_DIR}/self-awareness-check.sh"
    
    if [[ -f "$script" ]]; then
        bash "$script" 2>/dev/null || echo "unknown"
    else
        echo "unknown"
    fi
}

# Handle emotional state and send alerts if needed
self_awareness_handle_state() {
    local state="$1"
    
    log_info "Current emotional state: $state"
    
    if [[ "$state" == "frustrated" ]]; then
        message_send "I'm feeling frustrated today. Multiple errors detected." "medium"
    fi
}

# Run self-awareness check
self_awareness_run() {
    log_info "🧠 Running self-awareness check..."
    
    local state
    state=$(self_awareness_get_state)
    self_awareness_handle_state "$state"
}

# =============================================================================
# BUSINESS LOGIC: Creative Time
# =============================================================================

# Check if it's creative time (Sunday 14:00)
creative_time_is_now() {
    local day_of_week hour
    day_of_week=$(date +%u)
    hour=$(date +%H)
    
    [[ "$day_of_week" -eq "$CREATIVE_DAY" && "$hour" -eq "$CREATIVE_HOUR" ]]
}

# Run creative time script if available
creative_time_run() {
    local script="${SCRIPT_DIR}/creative-time.sh"
    
    if [[ -f "$script" ]]; then
        log_info "🎨 Creative time!"
        bash "$script" > /dev/null 2>&1 || log_warn "Creative time script failed"
        message_send "I just finished some creative work. Check creations/ folder." "low"
    fi
}

# Check and run creative time if scheduled
creative_time_check() {
    if creative_time_is_now; then
        creative_time_run
    fi
}

# =============================================================================
# BUSINESS LOGIC: Personal Goals
# =============================================================================

# Get file age in days
file_age_days() {
    local filepath="$1"
    local last_check now
    
    last_check=$(stat -c %Y "$filepath" 2>/dev/null || echo 0)
    now=$(date +%s)
    
    echo $(( (now - last_check) / 86400 ))
}

# Check if goals need review
goals_need_review() {
    local goals_file="$1"
    local age_days
    
    if [[ ! -f "$goals_file" ]]; then
        return 1  # false - no goals file
    fi
    
    age_days=$(file_age_days "$goals_file")
    [[ "$age_days" -ge "$GOALS_CHECK_INTERVAL_DAYS" ]]
}

# Send goals reminder message
goals_send_reminder() {
    log_info "📅 Weekly goals check"
    message_send "Weekly goals review: Let me know if you want to discuss progress." "low"
}

# Check personal goals
goals_check() {
    local goals_file="${WORKSPACE}/memory/personal-goals.md"
    
    if goals_need_review "$goals_file"; then
        goals_send_reminder
    fi
}

# =============================================================================
# BUSINESS LOGIC: Activity Tracking
# =============================================================================

# Update last activity timestamp
activity_update() {
    date +%s > "$LAST_ACTIVITY_FILE"
}

# =============================================================================
# MAIN LOOP
# =============================================================================

# Single heartbeat iteration
heartbeat_run() {
    local attention_count
    
    # Check attention items
    attention_count=$(attention_check_all)
    if [[ "$attention_count" -gt 0 ]]; then
        message_send "$attention_count items require attention" "high"
    fi
    
    # Run task modules
    autonomous_tasks_run
    self_awareness_run
    creative_time_check
    goals_check
    
    # Update activity timestamp
    activity_update
}

# Main execution loop
main_loop() {
    log_startup
    
    while true; do
        # Load fresh credentials each iteration
        api_load_credentials
        
        # Run heartbeat with error isolation
        heartbeat_run || log_error "Heartbeat iteration failed"
        
        # Wait for next interval
        sleep "$HEARTBEAT_INTERVAL"
    done
}

# =============================================================================
# SIGNAL HANDLING & ENTRY POINT
# =============================================================================

# Graceful shutdown handler
cleanup() {
    log_shutdown
    exit 0
}

trap cleanup SIGTERM SIGINT

# Entry point
main_loop