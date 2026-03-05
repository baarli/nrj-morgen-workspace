#!/bin/bash
# MEMORY VALIDATOR - Ensures I actually read MEMORY.md
# This quizzes me on the content to verify understanding

set -e

WORKSPACE="/root/.openclaw/workspace"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
VALIDATION_MARKER="$WORKSPACE/.memory-validated-$(date +%Y%m%d)"

echo "═══════════════════════════════════════════════════════════════════════"
echo "🧠 MEMORY VALIDATOR - Verifying you actually read the file"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""

# Check if already validated today
if [ -f "$VALIDATION_MARKER" ]; then
    echo "✅ Memory already validated today"
    exit 0
fi

# Check if MEMORY.md exists
if [ ! -f "$MEMORY_FILE" ]; then
    echo "❌ MEMORY.md not found!"
    exit 1
fi

# Extract key facts for quiz
echo "📚 Reading MEMORY.md and preparing validation..."
echo ""

# Get NRJ Panel ID from MEMORY.md
PANEL_ID=$(grep "Panel ID:" "$MEMORY_FILE" | head -1 | grep -oE '[0-9a-f-]{36}' || echo "NOT_FOUND")

# Get script names
UPDATE_SCRIPT=$(grep "update_nrj_dashboard.py" "$MEMORY_FILE" | head -1 | grep -oE '[^[:space:]]+\.py' || echo "NOT_FOUND")

echo "═══════════════════════════════════════════════════════════════════════"
echo "📝 VALIDATION QUIZ - Answer these questions:"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""

# Question 1
echo "Question 1: What is the NRJ Dashboard Panel ID?"
echo "(Type the ID or 'skip' to see it)"
read -r ANSWER1
echo ""

if [ "$ANSWER1" = "skip" ]; then
    echo "The answer is: $PANEL_ID"
    echo "Please remember this for next time."
    echo ""
elif [ "$ANSWER1" != "$PANEL_ID" ]; then
    echo "❌ Incorrect!"
    echo "The correct answer is: $PANEL_ID"
    echo ""
    echo "You MUST read MEMORY.md more carefully!"
    echo "Run: cat $MEMORY_FILE"
    exit 1
else
    echo "✅ Correct!"
fi

echo ""

# Question 2
echo "Question 2: Which script should you use to update the NRJ Dashboard?"
echo "(a) fetch_nrj_dashboard_stats.py"
echo "(b) update_nrj_dashboard.py"
echo "(c) fetch_nielsen_live.py"
read -r ANSWER2
echo ""

if [ "$ANSWER2" != "b" ] && [ "$ANSWER2" != "update_nrj_dashboard.py" ]; then
    echo "❌ Incorrect!"
    echo "The correct answer is: (b) update_nrj_dashboard.py"
    echo ""
    echo "You MUST read MEMORY.md more carefully!"
    echo "Run: cat $MEMORY_FILE"
    exit 1
else
    echo "✅ Correct!"
fi

echo ""

# Question 3
echo "Question 3: What is the difference between the Dashboard and Sakslista?"
echo "(Your answer shows you understand the context)"
read -r ANSWER3
echo ""

if [ -z "$ANSWER3" ] || [ ${#ANSWER3} -lt 10 ]; then
    echo "⚠️  Please provide a more detailed answer to show understanding."
    echo "The Dashboard is a SEPARATE system from the sakslista."
    echo "Dashboard = panel with ID, Sakslista = daily agenda items"
    echo ""
    echo "You MUST understand this distinction!"
    exit 1
else
    echo "✅ Answer accepted!"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "✅ MEMORY VALIDATION COMPLETE"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""

# Create validation marker
touch "$VALIDATION_MARKER"

echo "You have proven that you read and understood MEMORY.md"
echo "You may now proceed with work."
echo ""
