#!/bin/bash
#
# vev-experience-logger.sh
# Logger Vev's autonome erfaringer og læring
# Kjøres automatisk for å bygge opp Vev's "minne"
#

DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M)
LOG_DIR="/root/.openclaw/workspace/brain/logs"
DAILY_FILE="/root/.openclaw/workspace/brain/daily/${DATE}.md"
MEMORY_FILE="/root/.openclaw/workspace/MEMORY.md"

mkdir -p "$LOG_DIR"

# Hvis daglig fil ikke eksisterer, opprett den
if [ ! -f "$DAILY_FILE" ]; then
    cat > "$DAILY_FILE" << EOF
# ${DATE} - Vev's Dag

## Autonomous Activity Log

EOF
fi

# Legg til erfarings-seksjon hvis ikke finnes
if ! grep -q "## Erfaringer og Læring" "$DAILY_FILE"; then
    cat >> "$DAILY_FILE" << EOF

## Erfaringer og Læring (${TIME})

### Hva jeg gjorde autonomt i dag:
- [ ] 

### Hva jeg lærte:
- 

### Hvordan det gjør meg bedre:
- 

### Mood:
Curious / Satisfied / Focused / Playful

---
*Autonomt generert av Vev*
EOF
fi

# Oppdater MEMORY.md med viktige lærdommer (hvis noe signifikant skjedde)
# Dette skjer kun hvis det er verdt å huske langsiktig

exit 0
