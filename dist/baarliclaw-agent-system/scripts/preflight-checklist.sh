#!/bin/bash
# Pre-flight checklist - Run at the START of every session/task
# Ensures I have all context and knowledge before starting work

set -e

WORKSPACE="/root/.openclaw/workspace"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
TOOLS_FILE="$WORKSPACE/TOOLS.md"
SKILLS_DIR="$WORKSPACE/skills"

echo "═══════════════════════════════════════════════════════════════════════"
echo "🚀 PRE-FLIGHT CHECKLIST - Laster all kunnskap"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""

# 1. Check if MEMORY.md exists and show summary
echo "📚 Step 1: Loading MEMORY.md..."
if [ -f "$MEMORY_FILE" ]; then
    echo "   ✅ MEMORY.md found"
    
    # Extract key sections
    echo ""
    echo "   📋 CRITICAL SYSTEMS I KNOW:"
    grep "^## " "$MEMORY_FILE" | head -10 | sed 's/^## /      - /'
    
    # Show NRJ Dashboard info
    if grep -q "NRJ Morgen Dashboard" "$MEMORY_FILE"; then
        echo ""
        echo "   🎯 NRJ Dashboard Panel ID:"
        grep "Panel ID:" "$MEMORY_FILE" | head -1 | sed 's/.*Panel ID:/      /'
    fi
    
    echo ""
    echo "   💡 Tip: Read full MEMORY.md for complete context"
else
    echo "   ❌ MEMORY.md not found!"
fi

echo ""

# 2. Check TOOLS.md for quick reference
echo "🔧 Step 2: Loading TOOLS.md..."
if [ -f "$TOOLS_FILE" ]; then
    echo "   ✅ TOOLS.md found"
    
    # Show HUSK ALLTID section if exists
    if grep -q "HUSK ALLTID" "$TOOLS_FILE"; then
        echo ""
        echo "   🧠 HUSK ALLTID (Quick Reference):"
        grep -A 10 "HUSK ALLTID" "$TOOLS_FILE" | grep "^\s*-" | head -5 | sed 's/^/      /'
    fi
else
    echo "   ❌ TOOLS.md not found!"
fi

echo ""

# 3. List available skills
echo "🎓 Step 3: Loading available skills..."
if [ -d "$SKILLS_DIR" ]; then
    SKILL_COUNT=$(find "$SKILLS_DIR" -name "SKILL.md" | wc -l)
    echo "   ✅ Found $SKILL_COUNT skills:"
    
    for skill_dir in "$SKILLS_DIR"/*/; do
        if [ -f "$skill_dir/SKILL.md" ]; then
            skill_name=$(basename "$skill_dir")
            # Extract description from frontmatter
            description=$(grep -A 1 "^description:" "$skill_dir/SKILL.md" | tail -1 | sed 's/^\s*//' | cut -c1-60)
            echo "      • $skill_name: $description..."
        fi
    done
else
    echo "   ℹ️  No skills directory found"
fi

echo ""

# 4. Check for daily learning log
echo "📋 Step 4: Checking daily learning log..."
TODAY=$(date +%Y-%m-%d)
DAILY_LOG="$WORKSPACE/memory/$TODAY.md"

if [ -f "$DAILY_LOG" ]; then
    echo "   ✅ Today's log exists: $TODAY.md"
else
    echo "   ℹ️  No log yet for today - will create at end of session"
fi

echo ""

# 5. Show recent activity
echo "📊 Step 5: Recent activity..."
if [ -d "$WORKSPACE/memory" ]; then
    echo "   Recent learning logs:"
    ls -1t "$WORKSPACE/memory/" 2>/dev/null | head -5 | sed 's/^/      - /'
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "✅ PRE-FLIGHT COMPLETE - Ready to work with full context!"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "🎯 Remember to:"
echo "   1. Read relevant skills for your task"
echo "   2. Check MEMORY.md for system details"
echo "   3. Use TOOLS.md for quick reference"
echo "   4. Document learnings at end of session"
echo ""
echo "═══════════════════════════════════════════════════════════════════════"
