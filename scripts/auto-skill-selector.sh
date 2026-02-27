#!/bin/bash
set -e  # Exit on error
# Velger automatisk riktig skills basert på kontekst

echo "🤖 Auto Skill Selector"
echo ""

# Sjekk hvilken oppgave som skal gjøres
if [ -f "/tmp/current-task.txt" ]; then
    TASK=$(cat /tmp/current-task.txt)
else
    TASK="morning"
fi

echo "Oppgave: $TASK"
echo ""

# Velg skills
bash /root/.openclaw/workspace/scripts/skill-activation.sh "$TASK"
