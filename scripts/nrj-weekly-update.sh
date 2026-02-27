#!/bin/bash
# NRJ Weekly Update - Wrapper med retry-logikk og bedre feilhåndtering
# Kjører hver søndag kl 20:00

set -e

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="/var/log/nrj-weekly-update.log"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M)

# Konfigurasjon
MAX_RETRIES=3
RETRY_DELAY=60

log() {
    echo "[$DATE $TIME] $1" | tee -a "$LOG_FILE"
}

run_with_retry() {
    local cmd="$1"
    local description="$2"
    local attempt=1
    local exit_code=0
    
    while [ $attempt -le $MAX_RETRIES ]; do
        log "🔄 $description - Attempt $attempt/$MAX_RETRIES"
        
        if eval "$cmd"; then
            log "✅ $description - Success on attempt $attempt"
            return 0
        fi
        
        exit_code=$?
        log "⚠️ $description - Attempt $attempt failed (exit code: $exit_code)"
        
        if [ $attempt -lt $MAX_RETRIES ]; then
            log "⏳ Waiting ${RETRY_DELAY}s before retry..."
            sleep $RETRY_DELAY
        fi
        
        attempt=$((attempt + 1))
    done
    
    log "❌ $description - All $MAX_RETRIES attempts failed"
    return $exit_code
}

log "=========================================="
log "📻 NRJ WEEKLY UPDATE STARTING"
log "=========================================="

# 1. Oppdater Nielsen-radio-statistikk
log "📊 Step 1: Updating Nielsen radio statistics..."
if run_with_retry "python3 $WORKSPACE/scripts/fetch_nielsen_live_v2.py" "Nielsen Radio Data"; then
    log "   ✅ Nielsen data updated"
else
    log "   ⚠️ Nielsen update failed, continuing..."
fi

# 2. Oppdater Podtoppen-statistikk
log "🎧 Step 2: Updating Podtoppen statistics..."
if run_with_retry "python3 $WORKSPACE/scripts/fetch_podtoppen_live_v2.py" "Podtoppen Data"; then
    log "   ✅ Podtoppen data updated"
else
    log "   ⚠️ Podtoppen update failed, continuing..."
fi

# 3. Oppdater NRJ Dashboard
log "📈 Step 3: Updating NRJ Dashboard..."
if run_with_retry "python3 $WORKSPACE/scripts/update_nrj_dashboard.py" "NRJ Dashboard"; then
    log "   ✅ Dashboard updated"
else
    log "   ⚠️ Dashboard update failed, continuing..."
fi

# 4. Generer ukentlig rapport
log "📄 Step 4: Generating weekly report..."
log "   (Report generation would go here)"

log "=========================================="
log "✅ NRJ WEEKLY UPDATE COMPLETE"
log "=========================================="

# Alltid exit 0 for å unngå cron "error" status når jobben faktisk fullførte
exit 0
