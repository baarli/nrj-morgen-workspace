#!/bin/bash
set -e  # Exit on error
# Sjekker at alle skills er klare til bruk

echo "🏥 Skill Health Check"
echo ""

SKILLS_DIR="/root/.openclaw/skills"
HEALTHY=0
MISSING=0

for skill in $(ls $SKILLS_DIR/*/SKILL.md 2>/dev/null | xargs -n1 dirname | xargs -n1 basename); do
    if [ -f "$SKILLS_DIR/$skill/SKILL.md" ]; then
        echo "  ✅ $skill"
        HEALTHY=$((HEALTHY + 1))
    else
        echo "  ❌ $skill (mangler SKILL.md)"
        MISSING=$((MISSING + 1))
    fi
done

echo ""
echo "Resultat: $HEALTHY healthy, $MISSING missing"
