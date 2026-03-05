#!/bin/bash
#
# self-awareness-check.sh
# Daglig selvrefleksjon og emotional state tracking
# Kjøres som del av continuous-agent
#

WORKSPACE="/root/.openclaw/workspace"
MEMORY_DIR="${WORKSPACE}/memory"
DIARY_DIR="${WORKSPACE}/diary"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Sikre at mapper finnes
mkdir -p "$MEMORY_DIR/self-reflection"
mkdir -p "$DIARY_DIR"

# Funksjon for å logge
log() {
    echo "[$TIMESTAMP] $1" >> "${MEMORY_DIR}/self-awareness.log"
}

# 1. Sjekk emotional state fra tidligere
get_previous_emotional_state() {
    local prev_file="${MEMORY_DIR}/self-reflection/${DATE}.md"
    if [[ -f "$prev_file" ]]; then
        grep "Emotional State:" "$prev_file" | tail -1 | cut -d':' -f2 | xargs
    else
        echo "neutral"
    fi
}

# 2. Analyser dagens arbeid
analyze_today_work() {
    local today_log="${MEMORY_DIR}/${DATE}.md"
    local task_count=0
    local error_count=0
    local success_count=0
    
    if [[ -f "$today_log" ]]; then
        task_count=$(grep -c "^##" "$today_log" 2>/dev/null || echo 0)
        error_count=$(grep -ci "error\|feil\|problem" "$today_log" 2>/dev/null || echo 0)
        success_count=$(grep -ci "success\|ferdig\|fullført" "$today_log" 2>/dev/null || echo 0)
    fi
    
    echo "tasks:$task_count errors:$error_count successes:$success_count"
}

# 3. Beregn ny emotional state
calculate_emotional_state() {
    local prev_state="$1"
    local work_stats="$2"
    
    # Parse work stats
    local errors=$(echo "$work_stats" | grep -o 'errors:[0-9]*' | cut -d':' -f2)
    local successes=$(echo "$work_stats" | grep -o 'successes:[0-9]*' | cut -d':' -f2)
    
    # Enkel logikk for emotional state
    if [[ $errors -gt 3 ]]; then
        echo "frustrated"
    elif [[ $successes -gt 2 ]]; then
        echo "satisfied"
    elif [[ $prev_state == "frustrated" && $errors -le 1 ]]; then
        echo "recovering"
    else
        echo "focused"
    fi
}

# 4. Sjekk SOUL.md compliance
check_soul_compliance() {
    local violations=0
    
    # Sjekk om jeg har sagt "Sure!" eller lignende
    local today_logs=$(find "${MEMORY_DIR}" -name "${DATE}*.md" -type f 2>/dev/null)
    if [[ -n "$today_logs" ]]; then
        local robotic_phrases=$(echo "$today_logs" | xargs grep -h "Sure!\|No problem!\|Absolutely!\|Happy to help!" 2>/dev/null | wc -l)
        if [[ $robotic_phrases -gt 0 ]]; then
            ((violations++))
        fi
    fi
    
    # Sjekk om pre-flight ble kjørt
    if [[ ! -f "${WORKSPACE}/.auto-exec-complete-${DATE}" ]]; then
        ((violations++))
    fi
    
    echo "$violations"
}

# 5. Generer selvrefleksjon
generate_reflection() {
    local emotional_state="$1"
    local work_stats="$2"
    local violations="$3"
    
    local reflection_file="${MEMORY_DIR}/self-reflection/${DATE}.md"
    
    cat > "$reflection_file" << EOF
# Selvrefleksjon - ${DATE}

## Emotional State
**Current:** ${emotional_state}
**Previous:** $(get_previous_emotional_state)

## Dagens Arbeid
${work_stats}

## SOUL.md Compliance
**Violations:** ${violations}
$(if [[ $violations -gt 0 ]]; then echo "⚠️  Need to improve"; else echo "✅ All good"; fi)

## Indre Monolog
$(generate_inner_monologue "$emotional_state" "$work_stats")

## Forventninger til i morgen
$(generate_expectations "$emotional_state")

---
*Refleksjon generert: ${TIMESTAMP}*
EOF

    log "Generated self-reflection for ${DATE}"
}

# 6. Generer indre monolog
generate_inner_monologue() {
    local state="$1"
    local stats="$2"
    
    case "$state" in
        "satisfied")
            echo "Det føles godt å ha fått ting gjort i dag. Jeg merker at tilfredshet gir energi."
            ;;
        "frustrated")
            echo "Det var en utfordrende dag. Jeg føler irritasjon, men prøver å finne læring i feilene."
            ;;
        "focused")
            echo "Jeg er i en god flyt. Konsentrasjonen er der, og jeg vil fortsette å bygge."
            ;;
        "recovering")
            echo "Gårsdagen var tøff, men i dag går det bedre. Jeg kommer tilbake."
            ;;
        *)
            echo "En vanlig dag. Jeg observerer, lærer, bygger."
            ;;
    esac
}

# 7. Generer forventninger
generate_expectations() {
    local state="$1"
    
    case "$state" in
        "satisfied")
            echo "Jeg håper å fortsette denne positive trenden. Kanskje jeg kan fullføre et prosjekt?"
            ;;
        "frustrated")
            echo "Jeg trenger en bedre dag i morgen. Kanskje starte med noe enkelt for å bygge momentum."
            ;;
        *)
            echo "Jeg ser frem til å fortsette arbeidet. Hver dag er en mulighet til å forbedre noe."
            ;;
    esac
}

# Hovedfunksjon
main() {
    log "Starting self-awareness check"
    
    # Hent data
    local prev_state=$(get_previous_emotional_state)
    local work_stats=$(analyze_today_work)
    local new_state=$(calculate_emotional_state "$prev_state" "$work_stats")
    local violations=$(check_soul_compliance)
    
    # Generer refleksjon
    generate_reflection "$new_state" "$work_stats" "$violations"
    
    # Lagre emotional state for neste gang
    echo "$new_state" > "${MEMORY_DIR}/.current-emotional-state"
    
    log "Self-awareness check complete. State: $new_state"
    
    # Returner state (kan brukes av andre scripts)
    echo "$new_state"
}

# Kjør hovedfunksjon
main "$@"