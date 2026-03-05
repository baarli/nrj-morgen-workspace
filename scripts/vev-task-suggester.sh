#!/bin/bash
# Vev Task Suggester
# Automatically suggests tasks when Vev is idle

WORKSPACE="/root/.openclaw/workspace"
TASKS_FILE="$WORKSPACE/brain/vev-tasks.json"
LOG_FILE="$WORKSPACE/brain/logs/task-suggester.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo "[$TIMESTAMP] $1" >> "$LOG_FILE"
}

# Check if we have active tasks
if [ -f "$TASKS_FILE" ]; then
    ACTIVE_TASKS=$(cat "$TASKS_FILE" | grep -c '"column_id": "research"\|"column_id": "write"\|"column_id": "review"' 2>/dev/null || echo 0)
else
    ACTIVE_TASKS=0
fi

if [ "$ACTIVE_TASKS" -lt 3 ]; then
    log "⚠️  Running low on tasks ($ACTIVE_TASKS active)"
    
    # Suggest next action
    SUGGESTIONS=(
        "🌅 Kjøre Morning Routine for å hente nye saker fra NRJ Morgen"
        "📊 Analysere NRJ Morgen statistikk og lage rapport"
        "🎙️ Forbedre Telegram Auto-Responder med nye features"
        "📚 Oppdatere SYSTEM_ARCHITECTURE.md med nye endringer"
        "🔧 Vedlikeholde Mission Control - sjekke for bugs"
        "📈 Lage ukentlig rapport for Bauer Media"
        "🧠 Analysere samtale-mønstre og lære nye ting"
        "🎨 Forbedre design-system med nye komponenter"
        "🚀 Teste nye features i Voice Chat"
        "💾 Sikkerhetskopiere alle systemer til GitHub"
        "📻 Hente nyeste radio-statistikk fra Nielsen"
        "🎧 Sjekke Podtoppen for podcast-rankinger"
        "📝 Skrive oppsummering av ukens sendinger"
        "🔍 Forske på nye kilder for Morning Routine"
        "✨ Forbedre auto-sync systemet"
    )
    
    # Pick random suggestion
    RANDOM_INDEX=$((RANDOM % ${#SUGGESTIONS[@]}))
    SUGGESTION="${SUGGESTIONS[$RANDOM_INDEX]}"
    
    log "💡 Suggestion: $SUGGESTION"
    
    # Send to Telegram if configured
    if [ -f "$WORKSPACE/.credentials/telegram-bot.env" ]; then
        source "$WORKSPACE/.credentials/telegram-bot.env"
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
            -d "chat_id=$TELEGRAM_CHAT_ID" \
            -d "text=🤖 Vev har lite å gjøre!\n\n$SUGGESTION\n\nSkal jeg starte på dette?" \
            > /dev/null 2>&1
    fi
    
    echo "$SUGGESTION"
else
    log "✅ Sufficient tasks available ($ACTIVE_TASKS active)"
fi
