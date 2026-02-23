#!/bin/bash
# /root/.openclaw/workspace/scripts/meeting-prep.sh
# Forberede møter

if [ $# -lt 1 ]; then
  echo "Bruk: meeting-prep <møte-tema> [--participants "navn1,navn2"]")
  exit 1
fi

TOPIC="$1"
PARTICIPANTS="${2:-}"

echo "📋 MØTEFORBEREDELSE: $TOPIC"
echo "============================"
echo ""

MEETING_DIR="/root/.openclaw/workspace/brain/meetings"
mkdir -p "$MEETING_DIR"

MEETING_FILE="$MEETING_DIR/meeting-$(date +%Y%m%d)-$(echo $TOPIC | tr ' ' '-' | tr '[:upper:]' '[:lower:]').md"

cat > "$MEETING_FILE" << EOF
# 📋 Møte: $TOPIC

**Dato:** $(date '+%Y-%m-%d')  
**Tid:** [Sett inn tid]  
**Deltakere:** $PARTICIPANTS

---

## Agenda

1. **Åpning** (2 min)
   - Velkommen, runde rundt bordet

2. **[Tema 1]** (10 min)
   - 
   - 

3. **[Tema 2]** (10 min)
   - 
   - 

4. **[Tema 3]** (10 min)
   - 
   - 

5. **Oppsummering og neste steg** (5 min)
   - Action items
   - Neste møte

---

## Forberedelser

- [ ] 
- [ ] 
- [ ] 

---

## Notater

*(Fyll inn under møtet)*

---

## Action Items

| Hvem | Hva | Frist |
|------|-----|-------|
| | | |

---

## Oppsummering

**Viktigste beslutninger:**
- 

**Neste steg:**
- 

**Neste møte:**
- Dato: 
- Tema: 
EOF

echo "✅ Møteplan laget: $MEETING_FILE"
echo ""
echo "💡 Tips:"
echo "   - Del agenda 24t før møtet"
echo "   - Bruk 'voice-transcribe' for notater"
echo "   - Oppdater action items umiddelbart etter møtet"
