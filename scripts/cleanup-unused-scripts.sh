#!/bin/bash
#
# cleanup-unused-scripts.sh
# Rydder opp i ubrukte scripts (KJØR MED FORSIKTIGHET!)
#

echo "=== Script Rydding ==="
echo ""
echo "Scripts som er i aktiv bruk (fra cron, AGENTS.md, etc.):"
echo ""

# Liste over scripts som er kjent i bruk
USED_SCRIPTS=(
    "telegram-poll.py"
    "telegram-reply.sh"
    "telegram-send.sh"
    "auto-exec-enforcer.sh"
    "auto-learning-capture.sh"
    "auto-update-all-knowledge.sh"
    "brave-news-search.py"
    "podcast-clipper.py"
    "daily-podcast-clips.sh"
    "update_nrj_dashboard.py"
)

echo "✅ Beholdes (i aktiv bruk):"
for script in "${USED_SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        echo "  - $script"
    fi
done

echo ""
echo "⚠️  Vurderes for sletting (ikke bekreftet i bruk):"
find . -name "*.sh" -o -name "*.py" | while read f; do
    basename=$(basename "$f")
    if [[ ! " ${USED_SCRIPTS[@]} " =~ " ${basename} " ]]; then
        echo "  - $basename"
    fi
done

echo ""
echo "⚠️  VIKTIG: Ikke slett noe før du har bekreftet at det ikke er i bruk!"
echo "   Sjekk: cron jobs, AGENTS.md, andre scripts, skills."
