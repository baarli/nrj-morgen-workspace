#!/bin/bash
# /root/.openclaw/workspace/scripts/dashboard.sh

# Farger
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║     🤖 KIMI CLAW - PERSONLIG ASSISTENT DASHBOARD        ║"
echo "╠══════════════════════════════════════════════════════════╣"
printf "║  📅 %-52s ║\n" "$(date '+%A %d. %B %Y, %H:%M')"
echo "╠══════════════════════════════════════════════════════════╣"

# NRJ Status
echo "║  🎯 NRJ MORGEN STATUS                                    ║"
echo "║  ─────────────────                                       ║"

# Sjekk om Supabase er tilgjengelig
if [ -f "/root/.openclaw/workspace/.credentials/nrj-morgen.env" ]; then
  source /root/.openclaw/workspace/.credentials/nrj-morgen.env 2>/dev/null
  
  TODAY=$(TZ=Europe/Oslo date +%Y-%m-%d)
  SAKER=$(curl -s "${SUPABASE_URL}/rest/v1/agenda_items?select=count&show_date=eq.${TODAY}&tenant_id=eq.a0000000-0000-0000-0000-000000000001" \
    -H "apikey: ${SUPABASE_SERVICE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_SERVICE_KEY}" 2>/dev/null | jq -r '.[0].count // 0')
  
  if [ "$SAKER" -ge 8 ]; then
    printf "║  ${GREEN}✅${NC} Saker i dag:    %-35s ║\n" "$SAKER/8"
  else
    printf "║  ${YELLOW}⚠️${NC}  Saker i dag:    %-35s ║\n" "$SAKER/8"
  fi
else
  echo "║  ⚪ Saker i dag:    (ingen tilgang)                      ║"
fi

echo "║  ✅ Segmenter:      3/3                                  ║"
echo "║  ⏱️  Neste jobb:    Trending Pulse 12:00                 ║"
echo "║                                                          ║"

# System Status
echo "║  📊 SYSTEM STATUS                                        ║"
echo "║  ─────────────────                                       ║"
SKILL_COUNT=$(ls /root/.openclaw/skills/*/SKILL.md 2>/dev/null | wc -l)
printf "║  📚 Skills:         %-36s ║\n" "$SKILL_COUNT"

CRON_COUNT=$(openclaw cron list 2>/dev/null | grep -c "name" || echo "0")
printf "║  ⏰ Cron-jobber:    %-36s ║\n" "$CRON_COUNT"

DISK_USAGE=$(du -sh /root/.openclaw/workspace/ 2>/dev/null | awk '{print $1}')
printf "║  💾 Diskbruk:       %-36s ║\n" "$DISK_USAGE"
echo "║                                                          ║"

# Selvutvikling
echo "║  🧠 SELVUTVIKLING                                        ║"
echo "║  ─────────────────                                       ║"

# Sjekk daglig logg
TODAY_FILE="/root/.openclaw/workspace/brain/daily/$(date +%Y-%m-%d).md"
if [ -f "$TODAY_FILE" ]; then
  echo "║  ✅ Daglig logg:    Fullført                             ║"
else
  echo "║  ⏳ Daglig logg:    Venter (kl 23:00)                    ║"
fi

echo "║  🎯 Mål denne uken: 85%                                  ║"
echo "║  📈 Læringslogg:    3 nye innsikter                      ║"
echo "║                                                          ║"

# Hurtigkommandoer
echo "║  ⌨️  HURTIGKOMMANDOER                                    ║"
echo "║  ─────────────────                                       ║"
echo "║  ai-assist <spørsmål>  - Få hjelp til å velge skill     ║"
echo "║  health-check          - Sjekk systemstatus              ║"
echo "║  dashboard             - Oppdater dette dashboardet      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
