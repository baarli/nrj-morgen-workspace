#!/bin/bash
# /root/.openclaw/workspace/scripts/visualize-data.sh
# Lage enkle visualiseringer

if [ $# -lt 1 ]; then
  echo "Bruk: visualize-data <type> [options]"
  echo "Typer: bar, pie, line, ascii"
  exit 1
fi

TYPE="$1"

echo "📊 VISUALISERING: $TYPE"
echo "======================="
echo ""

# ASCII Bar Chart
ascii_bar() {
  local label="$1"
  local value=$2
  local max=$3
  local width=30
  
  local filled=$((value * width / max))
  local empty=$((width - filled))
  
  printf "%-15s [" "$label"
  printf '%*s' "$filled" '' | tr ' ' '█'
  printf '%*s' "$empty" '' | tr ' ' '░'
  printf "] %d\n" "$value"
}

# Demo data
echo "Eksempeldata - Lyttertall siste uke:"
echo ""
ascii_bar "Mandag" 8500 10000
ascii_bar "Tirsdag" 9200 10000
ascii_bar "Onsdag" 8800 10000
ascii_bar "Torsdag" 9500 10000
ascii_bar "Fredag" 10200 10000

echo ""
echo "💡 For mer avanserte grafer, vurder:"
echo "   - Python matplotlib"
echo "   - gnuplot"
echo "   - Online verktøy som Canva"
