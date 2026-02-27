#!/bin/bash
set -e  # Exit on error
# /root/.openclaw/workspace/scripts/network-manage.sh
# Håndtere kontakter og nettverk

if [ $# -lt 1 ]; then
  echo "Bruk: network-manage <kommando> [options]"
  echo ""
  echo "Kommandoer:"
  echo "  add 'Navn' --role 'Rolle' --contact 'epost@domene.no'"
  echo "  list [--category artist|media|influencer]"
  echo "  find 'søkeord'"
  echo "  followup 'Navn' [--notes 'hva som skjedde']"
  exit 1
fi

COMMAND="$1"

NETWORK_FILE="/root/.openclaw/workspace/brain/network/contacts.md"
mkdir -p $(dirname "$NETWORK_FILE")

# Initialiser fil hvis den ikke finnes
if [ ! -f "$NETWORK_FILE" ]; then
  cat > "$NETWORK_FILE" << 'EOF'
# 🤝 Nettverk og Kontakter

## Artister

## Influencere

## Medier

## Bransje

## Eksperter

EOF
fi

case $COMMAND in
  add)
    NAME="$2"
    echo "➕ Legger til: $NAME"
    echo "" >> "$NETWORK_FILE"
    echo "### $NAME" >> "$NETWORK_FILE"
    echo "**Lagt til:** $(date)" >> "$NETWORK_FILE"
    echo "" >> "$NETWORK_FILE"
    echo "✅ Lagt til i nettverket"
    ;;
  
  list)
    echo "📋 NETTVERK:"
    echo ""
    cat "$NETWORK_FILE"
    ;;
  
  find)
    SEARCH="$2"
    echo "🔍 Søker etter: $SEARCH"
    grep -i "$SEARCH" "$NETWORK_FILE" || echo "Ingen treff"
    ;;
  
  followup)
    NAME="$2"
    echo "📝 Oppfølging med: $NAME"
    echo "Dato: $(date)" >> "$NETWORK_FILE"
    echo "Notat: [Fyll inn]" >> "$NETWORK_FILE"
    echo "✅ Oppfølging logget"
    ;;
  
  *)
    echo "❌ Ukjent kommando: $COMMAND"
    exit 1
    ;;
esac
