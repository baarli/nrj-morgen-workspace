#!/bin/bash
set -e  # Exit on error
# /root/.openclaw/workspace/scripts/research-topic.sh
# Dyp research om et tema

if [ $# -lt 1 ]; then
  echo "Bruk: research-topic <tema> [--depth basic|deep] [--sources n]"
  exit 1
fi

TOPIC="$1"
DEPTH="${2:-deep}"
SOURCES="${3:-10}"

echo "🔍 RESEARCH: $TOPIC"
echo "=================="
echo "Dybde: $DEPTH | Kilder: $SOURCES"
echo ""

RESEARCH_DIR="/root/.openclaw/workspace/brain/research"
mkdir -p "$RESEARCH_DIR"

RESEARCH_FILE="$RESEARCH_DIR/$(echo $TOPIC | tr ' ' '-' | tr '[:upper:]' '[:lower:]')-$(date +%Y%m%d).md"

echo "⏳ Søker etter informasjon..."
echo ""

# Start research-dokument
cat > "$RESEARCH_FILE" << EOF
# 🔍 Research: $TOPIC

**Dato:** $(date '+%Y-%m-%d %H:%M')  
**Dybde:** $DEPTH  
**Kilder:** $SOURCES

---

## Sammendrag

*(Genereres basert på funn)*

---

## Hovedfunn

EOF

# Simulere research (i praksis ville dette bruke kimi_search)
echo "📚 Kilder funnet:"
echo ""

# Legg til seksjoner
cat >> "$RESEARCH_FILE" << EOF
### 1. Bakgrunn

*[Research om temaets bakgrunn]*

### 2. Nøkkelaktører

*[Viktige personer, bedrifter, organisasjoner]*

### 3. Aktuell situasjon

*[Hva skjer nå]*

### 4. Trender og utvikling

*[Hvor er dette på vei]*

### 5. Kilder og referanser

EOF

echo "✅ Research lagret: $RESEARCH_FILE"
echo ""
echo "💡 Neste steg:"
echo "   - Fyll inn seksjonene med funn"
echo "   - Bruk 'summarize-content' for å kondensere"
echo "   - Del med team via 'meeting-assistant'"
