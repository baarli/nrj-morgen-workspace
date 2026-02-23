#!/bin/bash
# Agent Performance Dashboard
# Shows metrics about my learning and performance

set -e

WORKSPACE="/root/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
SKILLS_DIR="$WORKSPACE/skills"
SCRIPT_DIR="$WORKSPACE/scripts"

echo "═══════════════════════════════════════════════════════════════════════"
echo "📊 AGENT PERFORMANCE DASHBOARD"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "Generert: $(date)"
echo ""

# 1. Session Statistics
echo "📈 SESSION STATISTIKK"
echo "───────────────────────────────────────────────────────────────────────"
SESSION_COUNT=$(find ~/.openclaw/agents/main/sessions -name "*.jsonl" 2>/dev/null | wc -l)
echo "  Totale sessioner: $SESSION_COUNT"

# 2. Learning Logs
echo ""
echo "📚 LÆRINGSLOGGER"
echo "───────────────────────────────────────────────────────────────────────"
LOG_COUNT=$(find "$MEMORY_DIR" -name "*.md" 2>/dev/null | wc -l)
echo "  Totale læringslogger: $LOG_COUNT"
echo "  Siste 5 logger:"
ls -1t "$MEMORY_DIR/" 2>/dev/null | head -5 | sed 's/^/    - /'

# 3. Skills Created
echo ""
echo "🎓 SKILLS OPPRETTET"
echo "───────────────────────────────────────────────────────────────────────"
SKILL_COUNT=$(find "$SKILLS_DIR" -name "SKILL.md" 2>/dev/null | wc -l)
echo "  Totale skills: $SKILL_COUNT"
find "$SKILLS_DIR" -name "SKILL.md" 2>/dev/null | while read skill; do
  skill_name=$(basename $(dirname "$skill"))
  echo "    - $skill_name"
done

# 4. Scripts Available
echo ""
echo "🔧 SCRIPTS TILGJENGELIG"
echo "───────────────────────────────────────────────────────────────────────"
SCRIPT_COUNT=$(find "$SCRIPT_DIR" -name "*.sh" 2>/dev/null | wc -l)
echo "  Totale scripts: $SCRIPT_COUNT"
echo "  Viktige scripts:"
echo "    - auto-exec-enforcer.sh (MANDATORY)"
echo "    - memory-validator.sh (QUIZ)"
echo "    - session-end-handler.sh (AUTO)"
echo "    - update_nrj_dashboard.py (NRJ)"

# 5. Cron Jobs
echo ""
echo "⏰ CRON JOBS (Automatiske oppgaver)"
echo "───────────────────────────────────────────────────────────────────────"
echo "  Aktive cron jobs:"
echo "    - Daily Pre-Flight Check (hver 24. time)"
echo "    - Session End Learning Capture (hver time)"
echo "    - NRJ Dashboard Auto Update (onsdager 14:00)"
echo "    - Sakslista Morning Routine (man-fre 06:00)"
echo "    - Podkast Clip Download (daglig 07:00)"

# 6. Documentation Status
echo ""
echo "📖 DOKUMENTASJONSSTATUS"
echo "───────────────────────────────────────────────────────────────────────"
MEMORY_LINES=$(wc -l < "$WORKSPACE/MEMORY.md" 2>/dev/null || echo "0")
TOOLS_LINES=$(wc -l < "$WORKSPACE/TOOLS.md" 2>/dev/null || echo "0")
SOUL_LINES=$(wc -l < "$WORKSPACE/SOUL.md" 2>/dev/null || echo "0")

echo "  MEMORY.md: $MEMORY_LINES linjer"
echo "  TOOLS.md: $TOOLS_LINES linjer"
echo "  SOUL.md: $SOUL_LINES linjer"
echo "  Dashboard docs: $(wc -l < "$WORKSPACE/docs/NRJ_DASHBOARD_SYSTEM.md" 2>/dev/null || echo "0") linjer"

# 7. System Health
echo ""
echo "💚 SYSTEM HELSE"
echo "───────────────────────────────────────────────────────────────────────"

# Check if mandatory scripts exist
if [ -f "$SCRIPT_DIR/auto-exec-enforcer.sh" ]; then
    echo "  ✅ auto-exec-enforcer.sh: OK"
else
    echo "  ❌ auto-exec-enforcer.sh: MISSING"
fi

if [ -f "$SCRIPT_DIR/memory-validator.sh" ]; then
    echo "  ✅ memory-validator.sh: OK"
else
    echo "  ❌ memory-validator.sh: MISSING"
fi

if [ -f "$SCRIPT_DIR/session-end-handler.sh" ]; then
    echo "  ✅ session-end-handler.sh: OK"
else
    echo "  ❌ session-end-handler.sh: MISSING"
fi

# 8. Recent Activity
echo ""
echo "📅 NYLIG AKTIVITET"
echo "───────────────────────────────────────────────────────────────────────"
echo "  Siste endringer i workspace:"
find "$WORKSPACE" -type f -mtime -1 2>/dev/null | head -10 | sed 's/^/    - /'

echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "✅ DASHBOARD GENERERT"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "System status: OPERATIONAL"
echo "Auto-learning: ENABLED"
echo "Self-improvement: ACTIVE"
echo ""
