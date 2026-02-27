#!/bin/bash
set -e  # Exit on error
# /root/.openclaw/workspace/scripts/calendar-today.sh
# Vis dagens agenda

echo "📅 DAGENS AGENDA"
echo "================"
echo ""
echo "Dato: $(date '+%A %d. %B %Y')"
echo ""

# Sjekk om det finnes kalenderintegrasjon
if [ -f "/root/.openclaw/workspace/.credentials/calendar.env" ]; then
  source /root/.openclaw/workspace/.credentials/calendar.env
  
  # Her ville vi integrere med Google Calendar API
  echo "(Kalenderintegrasjon krever Google Calendar API-oppsett)"
  echo ""
fi

# Vis cron-jobber som kjører i dag
echo "⏰ AUTOMATISKE JOBBER I DAG:"
echo ""

TODAY_HOUR=$(date +%H)

# Liste kommende jobber
openclaw cron list 2>/dev/null | grep -E "^[a-f0-9]{8}-" | while read line; do
  NAME=$(echo "$line" | awk '{print $2}')
  SCHEDULE=$(echo "$line" | awk '{print $3}')
  
  # Sjekk om jobben kjører i dag
  echo "  • $NAME - $SCHEDULE"
done

echo ""
echo "🎯 ANBEFALTE AKTIVITETER:"
echo ""

# Basert på dag og tid
DAY=$(date +%u)
HOUR=$(date +%H)

if [ $DAY -le 5 ]; then
  echo "  ✅ Hverdag - NRJ Morgen sending"
  
  if [ $HOUR -lt 6 ]; then
    echo "  ⏰ Sending starter kl 06:00"
    echo "  📧 Showprepp sendt til e-post"
  elif [ $HOUR -ge 6 ] && [ $HOUR -lt 10 ]; then
    echo "  🎙️ Sending pågår!"
  fi
  
  echo "  📊 Sjekk dashboard: /root/.openclaw/workspace/scripts/dashboard.sh"
fi

echo ""
echo "💡 Tips:"
echo "   - Bruk 'voice-transcribe' for møtenotater"
echo "   - Sjekk 'brain/daily/' for dagens logg"
echo "   - Kjør 'health-check' for systemstatus"
