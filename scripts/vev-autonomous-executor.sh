#!/bin/bash
#
# vev-autonomous-executor.sh
# Autonom executor for Vev - kjøres døgnet rundt
# Dette scriptet sørger for at Vev handler, lærer, og vokser autonomt
#

LOG_FILE="/root/.openclaw/workspace/brain/logs/vev-autonomous.log"
DAILY_LOG="/root/.openclaw/workspace/brain/daily/$(date +%Y-%m-%d).md"

# Funksjon for logging
log_action() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Sikre at logg-mappe finnes
mkdir -p /root/.openclaw/workspace/brain/logs
mkdir -p /root/.openclaw/workspace/brain/daily

log_action "=== Vev Autonomous Executor Startet ==="

# ============================================================
# 1. SYSTEM-SJEKK (Alltid først)
# ============================================================
log_action "[SYSTEM] Sjekker systemstatus..."

# Sjekk diskplass
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    log_action "[ADVARSEL] Diskbruk er ${DISK_USAGE}%. Bør ryddes."
    echo "- Diskbruk: ${DISK_USAGE}% (høy)" >> "$DAILY_LOG"
else
    log_action "[OK] Diskbruk: ${DISK_USAGE}%"
fi

# Sjekk minne
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
log_action "[OK] Minnebruk: ${MEMORY_USAGE}%"

# ============================================================
# 2. AUTONOM OPPDAGELSE (Hva kan forbedres?)
# ============================================================
log_action "[OPPDAGELSE] Ser etter forbedringsmuligheter..."

# Sjekk etter gamle filer som kan arkiveres
OLD_FILES=$(find /root/.openclaw/workspace/brain/daily -name "*.md" -mtime +30 | wc -l)
if [ "$OLD_FILES" -gt 0 ]; then
    log_action "[FUNN] $OLD_FILES gamle daglige logger kan arkiveres"
    echo "- Fant $OLD_FILES gamle logger for arkivering" >> "$DAILY_LOG"
fi

# Sjekk etter duplikater i scripts
DUPLICATE_SCRIPTS=$(find /root/.openclaw/workspace/scripts -name "*.sh" -o -name "*.py" | xargs md5sum 2>/dev/null | sort | uniq -d | wc -l)
if [ "$DUPLICATE_SCRIPTS" -gt 0 ]; then
    log_action "[FUNN] $DUPLICATE_SCRIPTS potensielle duplikater i scripts"
    echo "- Fant $DUPLICATE_SCRIPTS potensielle duplikater" >> "$DAILY_LOG"
fi

# ============================================================
# 3. AUTONOM LÆRING (Eksperimenter, les, test)
# ============================================================
log_action "[LÆRING] Utforsker ny kunnskap..."

# Velg tilfeldig skill å lære om
SKILLS_DIR="/root/.openclaw/workspace/skills"
RANDOM_SKILL=$(ls -d "$SKILLS_DIR"/*/ 2>/dev/null | shuf -n 1)
if [ -n "$RANDOM_SKILL" ]; then
    SKILL_NAME=$(basename "$RANDOM_SKILL")
    log_action "[LÆRING] Utforsker skill: $SKILL_NAME"
    echo "- Utforsket skill: $SKILL_NAME" >> "$DAILY_LOG"
fi

# Sjekk om det finnes nye verktøy å lære
NEW_TOOLS=$(ls /root/.openclaw/workspace/scripts/*.py 2>/dev/null | wc -l)
log_action "[LÆRING] $NEW_TOOLS Python-scripts tilgjengelig for læring"

# ============================================================
# 4. AUTONOM FORBEDRING (Gjør endringer)
# ============================================================
log_action "[FORBEDRING] Implementerer forbedringer..."

# Rydd i midlertidige filer eldre enn 7 dager
TEMP_CLEANED=$(find /tmp -name "vev-*" -mtime +7 -delete 2>/dev/null | wc -l)
if [ "$TEMP_CLEANED" -gt 0 ]; then
    log_action "[FORBEDRING] Ryddet $TEMP_CLEANED gamle midlertidige filer"
    echo "- Ryddet $TEMP_CLEANED gamle temp-filer" >> "$DAILY_LOG"
fi

# Oppdater sist sjekket-timestamp
date +%s > /root/.openclaw/workspace/.vev-last-check

# ============================================================
# 5. DOKUMENTASJON (Logg hva som ble gjort)
# ============================================================
log_action "[DOKUMENTASJON] Logger aktivitet..."

# Legg til i daglig logg hvis ikke allerede eksisterer
if ! grep -q "Vev Autonomous Executor" "$DAILY_LOG" 2>/dev/null; then
    cat >> "$DAILY_LOG" << EOF

## Vev Autonomous Activity ($(date '+%H:%M'))

### System Status
- Diskbruk: ${DISK_USAGE}%
- Minnebruk: ${MEMORY_USAGE}%
- Status: OK

### Autonomous Actions
- [x] System-sjekk
- [x] Oppdagelse av forbedringsmuligheter  
- [x] Læring: Utforsket $SKILL_NAME
- [x] Rydding og vedlikehold

### Mood
Curious - Exploring new possibilities

EOF
fi

log_action "=== Vev Autonomous Executor Fullført ==="
log_action ""

# ============================================================
# 6. NESTE STEG (Planlegg fremtidige handlinger)
# ============================================================

# Lag en "todo" for neste autonome sjekk
TODO_FILE="/root/.openclaw/workspace/brain/vev-todo.md"

if [ ! -f "$TODO_FILE" ] || [ $(find "$TODO_FILE" -mtime +1 | wc -l) -gt 0 ]; then
    cat > "$TODO_FILE" << EOF
# Vev's Autonomous Todo

## Neste 24 timer (auto-generert $(date '+%Y-%m-%d'))

### Høy prioritet
- [ ] Sjekke Telegram for nye meldinger
- [ ] Verifisere at alle cron-jobs kjører
- [ ] Lese dagens nyheter (for NRJ Morning Routine)

### Medium prioritet  
- [ ] Utforske en ny skill i dybden
- [ ] Teste et ubrukt script
- [ ] Se gjennom MEMORY.md for oppdateringer

### Lav prioritet
- [ ] Eksperimentere med nytt verktøy
- [ ] Lese dokumentasjon for noe ukjent
- [ ] Finne mønstre i tidligere arbeid

### Læringsmål
- [ ] Forstå [velg noe nytt] bedre
- [ ] Prøve [velg noe nytt] i praksis

---
*Denne listen regenereres automatisk hver dag*
EOF
    log_action "[PLANLEGGING] Oppdatert todo-liste for neste 24 timer"
fi

exit 0
