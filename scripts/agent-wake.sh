#!/bin/bash
#
# agent-wake.sh
# Vekker BaarliClaw fra eksterne hendelser (webhook, event, etc.)
#

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="${WORKSPACE}/memory/agent-wake.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Parse input
EVENT_TYPE="${1:-unknown}"
EVENT_DATA="${2:-{}}"

log "🔔 Wake event received: $EVENT_TYPE"

# Lagre hendelse i Supabase for sporing
cd "$WORKSPACE" && source .credentials/nrj-morgen.env 2>/dev/null || true

curl -s -X POST "${SUPABASE_URL}/rest/v1/activity_log" \
    -H "apikey: ${SUPABASE_SERVICE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_SERVICE_KEY}" \
    -H "Content-Type: application/json" \
    -d "{
        \"level\": \"info\",
        \"category\": \"system\",
        \"message\": \"Agent wake: $EVENT_TYPE\",
        \"details\": {\"event\": \"$EVENT_TYPE\", \"data\": $EVENT_DATA},
        \"actionable\": true
    }" > /dev/null 2>&1 || true

# Håndter ulike hendelse-typer
case "$EVENT_TYPE" in
    "supabase_change")
        log "📊 Database change detected"
        # Sjekk hva som endret seg
        ;;
    "github_webhook")
        log "📝 GitHub activity detected"
        # Hent commit info, PR, etc.
        ;;
    "system_alert")
        log "🚨 System alert received"
        # Prioriter håndtering
        ;;
    "user_command")
        log "💬 User command received"
        # Utfør kommando
        ;;
    *)
        log "❓ Unknown event type: $EVENT_TYPE"
        ;;
esac

# Send "jeg er våken" signal
log "✅ Agent is now awake and processing"

# Oppdater sist aktivitet
date +%s > "${WORKSPACE}/.last-agent-activity"

# TODO: Send notifikasjon til bruker hvis kritisk
echo "Agent wake complete: $EVENT_TYPE"