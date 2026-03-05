#!/bin/bash
set -e  # Exit on error
# /root/.openclaw/workspace/scripts/health-check.sh

ERRORS=0
WARNINGS=0

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║           🔍 SYSTEM HELSE-SJEKK                          ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo ""

# Test 1: Supabase tilkobling
echo "📡 Tester Supabase-tilkobling..."
if [ -f "/root/.openclaw/workspace/.credentials/nrj-morgen.env" ]; then
  source /root/.openclaw/workspace/.credentials/nrj-morgen.env 2>/dev/null
  
  if curl -s "${SUPABASE_URL}/rest/v1/agenda_items?limit=1" \
    -H "apikey: ${SUPABASE_SERVICE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_SERVICE_KEY}" > /dev/null 2>&1; then
    echo "   ✅ Supabase: Tilkoblet"
  else
    echo "   ❌ Supabase: Tilkoblingsfeil"
    ((ERRORS++))
  fi
else
  echo "   ⚠️  Supabase: Credentials-fil ikke funnet"
  ((WARNINGS++))
fi

# Test 2: Skills tilgjengelig
echo ""
echo "📚 Tester skills..."
SKILL_COUNT=$(ls /root/.openclaw/skills/*/SKILL.md 2>/dev/null | wc -l)
if [ $SKILL_COUNT -ge 29 ]; then
  echo "   ✅ Skills: $SKILL_COUNT funnet"
else
  echo "   ⚠️  Skills: Kun $SKILL_COUNT funnet (forventet 29)"
  ((WARNINGS++))
fi

# Test 3: Git versjonering
echo ""
echo "📝 Tester Git versjonering..."
if [ -d "/root/.openclaw/skills/.git" ]; then
  cd /root/.openclaw/skills
  COMMIT_COUNT=$(git log --oneline 2>/dev/null | wc -l)
  echo "   ✅ Git: Initialisert ($COMMIT_COUNT commits)"
else
  echo "   ⚠️  Git: Ikke initialisert"
  ((WARNINGS++))
fi

# Test 4: Cron-jobber
echo ""
echo "⏰ Tester cron-jobber..."
CRON_COUNT=$(openclaw cron list 2>/dev/null | grep -E '^[a-f0-9]{8}-' | wc -l)
if [ "$CRON_COUNT" -ge 10 ]; then
  echo "   ✅ Cron: $CRON_COUNT jobber aktive"
else
  echo "   ⚠️  Cron: $CRON_COUNT jobber (forventet 10+)"
  ((WARNINGS++))
fi

# Test 5: Diskplass
echo ""
echo "💾 Sjekker diskplass..."
USAGE=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
if [ $USAGE -lt 80 ]; then
  echo "   ✅ Disk: ${USAGE}% brukt"
elif [ $USAGE -lt 90 ]; then
  echo "   ⚠️  Disk: ${USAGE}% brukt (overvåk)"
  ((WARNINGS++))
else
  echo "   ❌ Disk: ${USAGE}% brukt (kritisk!)"
  ((ERRORS++))
fi

# Test 6: Verktøy
echo ""
echo "🔧 Sjekker verktøy..."
for TOOL in claude tmux git; do
  if which $TOOL > /dev/null 2>&1; then
    echo "   ✅ $TOOL: Installert"
  else
    echo "   ⚠️  $TOOL: Ikke funnet"
    ((WARNINGS++))
  fi
done

# Test 7: Brain-struktur
echo ""
echo "🧠 Sjekker brain-struktur..."
for DIR in daily projects learning ideas reflections goals user; do
  if [ -d "/root/.openclaw/workspace/brain/$DIR" ]; then
    echo "   ✅ brain/$DIR: OK"
  else
    echo "   ⚠️  brain/$DIR: Mangler"
    ((WARNINGS++))
  fi
done

# Test 8: Personlig profil
echo ""
echo "👤 Sjekker personlig profil..."
if [ -f "/root/.openclaw/workspace/brain/user/profile.json" ]; then
  echo "   ✅ Profil: Konfigurert"
else
  echo "   ⚠️  Profil: Ikke funnet"
  ((WARNINGS++))
fi

# Oppsummering
echo ""
echo "╠══════════════════════════════════════════════════════════╣"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
  echo "║  🎉 ALLE SYSTEMER GO!                                    ║"
elif [ $ERRORS -eq 0 ]; then
  echo "║  ⚠️  $WARNINGS advarsler (ikke kritisk)                  ║"
else
  echo "║  ❌ $ERRORS feil, $WARNINGS advarsler                   ║"
fi
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

exit $ERRORS
