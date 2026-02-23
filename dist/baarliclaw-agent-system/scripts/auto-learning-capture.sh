#!/bin/bash
# Auto-learning capture script
# Run at end of every session to ensure documentation

set -e

WORKSPACE="/root/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date +%Y-%m-%d)
NOW=$(date +"%Y-%m-%d %H:%M")

echo "═══════════════════════════════════════════════════════════════════════"
echo "🎓 AUTO-LEARNING CAPTURE"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""

# 1. Ensure daily log exists
echo "📋 Step 1: Ensuring daily learning log exists..."
mkdir -p "$MEMORY_DIR"

DAILY_LOG="$MEMORY_DIR/$TODAY.md"
if [ ! -f "$DAILY_LOG" ]; then
    cat > "$DAILY_LOG" << EOF
# $TODAY - Læringslogg

## Hva vi gjorde i dag
- 

## Innsikter
1. 

## Feil gjort og læring
- 

## Nye systemer/prosesser
- 

## Takknemlighet
- 

---
**Sist oppdatert:** $NOW
EOF
    echo "   ✅ Created new daily log: $DAILY_LOG"
else
    echo "   ✅ Daily log already exists: $DAILY_LOG"
fi

echo ""

# 2. Check MEMORY.md is current
echo "📚 Step 2: Checking MEMORY.md..."
if [ -f "$WORKSPACE/MEMORY.md" ]; then
    LAST_MODIFIED=$(stat -c %Y "$WORKSPACE/MEMORY.md" 2>/dev/null || stat -f %m "$WORKSPACE/MEMORY.md" 2>/dev/null)
    CURRENT_TIME=$(date +%s)
    AGE_HOURS=$(( (CURRENT_TIME - LAST_MODIFIED) / 3600 ))
    
    if [ $AGE_HOURS -gt 24 ]; then
        echo "   ⚠️  MEMORY.md is $AGE_HOURS hours old - consider updating!"
    else
        echo "   ✅ MEMORY.md is current (last modified $AGE_HOURS hours ago)"
    fi
else
    echo "   ❌ MEMORY.md not found!"
fi

echo ""

# 3. Check for skills that should be created
echo "🎓 Step 3: Checking for skill creation opportunities..."
SKILL_COUNT=$(ls -1 "$WORKSPACE/skills/" 2>/dev/null | wc -l)
echo "   📦 Current skills: $SKILL_COUNT"
echo "   💡 Remember: Create skills for repeatable processes!"

echo ""

# 4. Verify TOOLS.md has HUSK ALLTID section
echo "🔧 Step 4: Checking TOOLS.md..."
if grep -q "HUSK ALLTID" "$WORKSPACE/TOOLS.md" 2>/dev/null; then
    echo "   ✅ TOOLS.md has 'HUSK ALLTID' section"
else
    echo "   ⚠️  Consider adding 'HUSK ALLTID' section to TOOLS.md"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "✅ AUTO-LEARNING CHECK COMPLETE"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "📖 Remember to:"
echo "   1. Fill in today's learning log"
echo "   2. Update MEMORY.md with critical info"
echo "   3. Create skills for repeatable tasks"
echo "   4. Document mistakes and solutions"
echo ""
echo "═══════════════════════════════════════════════════════════════════════"
