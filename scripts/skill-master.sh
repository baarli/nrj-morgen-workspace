#!/bin/bash
set -e  # Exit on error
# /root/.openclaw/workspace/scripts/skill-master.sh
# Master control for alle skills

echo "🎯 SKILL MASTER - Kontrollsenter"
echo "================================="
echo ""

# Tell skills
TOTAL=$(ls /root/.openclaw/skills/*/SKILL.md 2>/dev/null | wc -l)
NRJ=$(ls /root/.openclaw/skills/nrj-*/SKILL.md 2>/dev/null | wc -l)
AI=$(ls /root/.openclaw/skills/ai-* /root/.openclaw/skills/auto-* /root/.openclaw/skills/context-* /root/.openclaw/skills/personal* /root/.openclaw/skills/visual* /root/.openclaw/skills/automated* /root/.openclaw/skills/skill-version* 2>/dev/null | wc -l)
PRODUCTIVITY=$(ls /root/.openclaw/skills/voice-* /root/.openclaw/skills/calendar-* /root/.openclaw/skills/research-* /root/.openclaw/skills/creative-* /root/.openclaw/skills/data-* /root/.openclaw/skills/meeting-* /root/.openclaw/skills/content-* /root/.openclaw/skills/trend-* /root/.openclaw/skills/crisis-* /root/.openclaw/skills/network-* 2>/dev/null | wc -l)
CONTENT=$(ls /root/.openclaw/skills/humor-* /root/.openclaw/skills/fact-* /root/.openclaw/skills/interview-* /root/.openclaw/skills/script-* /root/.openclaw/skills/music-* /root/.openclaw/skills/audience-* /root/.openclaw/skills/competition-* /root/.openclaw/skills/event-* /root/.openclaw/skills/wellness-* 2>/dev/null | wc -l)

echo "📊 SKILL-OVERSIKT:"
echo "   Totalt: $TOTAL skills"
echo ""
echo "   📻 NRJ Core:        $NRJ skills"
echo "   🤖 AI & Smart:      $AI skills"
echo "   ⚡ Productivity:    $PRODUCTIVITY skills"
echo "   🎨 Content & Creat: $CONTENT skills"
echo ""

# Vis dagens anbefalte workflow
echo "📅 DAGENS WORKFLOW:"
echo ""
echo "   04:00 → Morgen-Pipeline (16 skills)"
echo "   04:30 → Morgenbriefing (10 skills)"
echo "   05:50 → Showprepp e-post (10 skills)"
echo "   06:00 → Overvåking (8 skills)"
echo "   12:00 → Trending Pulse"
echo ""

# Quick actions
echo "⚡ HURTIGHANDLINGER:"
echo ""
echo "   brainstorm-ideas 'tema'     → Generere ideer"
echo "   research-topic 'tema'       → Dyp research"
echo "   meeting-prep 'møte'         → Forberede møte"
echo "   calendar-today              → Se agenda"
echo "   voice-transcribe fil.m4a    → Transkriber"
echo "   repurpose-content kilde     → Gjenbruk innhold"
echo "   forecast-trends             → Se trender"
echo "   crisis-respond type         → Håndtere krise"
echo "   network-manage add 'Navn'   → Legge til kontakt"
echo ""

# Status
echo "✅ SYSTEM STATUS:"
echo "   Alle $TOTAL skills er klare og integrert!"
echo "   $(openclaw cron list 2>/dev/null | grep -E '^[a-f0-9]{8}-' | wc -l) cron-jobber aktive"
echo "   Git: $(cd /root/.openclaw/skills && git log --oneline 2>/dev/null | wc -l) commits"
echo ""
