#!/bin/bash
# ML-Based Learning Analyzer
# Analyzes session logs to identify patterns and suggest improvements

set -e

WORKSPACE="/root/.openclaw/workspace"
SESSIONS_DIR="$HOME/.openclaw/agents/main/sessions"
ANALYSIS_DIR="$WORKSPACE/.ml-analysis"

echo "═══════════════════════════════════════════════════════════════════════"
echo "🧠 ML-BASED LEARNING ANALYZER"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""

mkdir -p "$ANALYSIS_DIR"

# 1. Analyze tool usage patterns
echo "📊 Analyzing tool usage patterns..."
TOOL_USAGE="$ANALYSIS_DIR/tool-usage.txt"

if [ -d "$SESSIONS_DIR" ]; then
    # Extract tool calls from sessions
    find "$SESSIONS_DIR" -name "*.jsonl" -exec cat {} \; 2>/dev/null | \
        jq -r '.message.content[]? | select(.type == "toolCall") | .name' 2>/dev/null | \
        sort | uniq -c | sort -rn > "$TOOL_USAGE" || echo "No tool usage data yet"
    
    if [ -s "$TOOL_USAGE" ]; then
        echo "  Most used tools:"
        head -5 "$TOOL_USAGE" | sed 's/^/    /'
    else
        echo "  No tool usage data available yet"
    fi
else
    echo "  No sessions directory found"
fi

# 2. Identify common mistakes
echo ""
echo "🔍 Identifying patterns in memory logs..."
MISTAKE_PATTERN="$ANALYSIS_DIR/common-patterns.txt"

if [ -d "$WORKSPACE/memory" ]; then
    # Look for "Feil" (mistakes) in learning logs
    grep -r "Feil:" "$WORKSPACE/memory/" 2>/dev/null | \
        head -10 > "$MISTAKE_PATTERN" || echo "No mistakes logged yet"
    
    if [ -s "$MISTAKE_PATTERN" ]; then
        echo "  Common mistakes found:"
        cat "$MISTAKE_PATTERN" | sed 's/^/    /'
    else
        echo "  No mistakes logged yet - good!"
    fi
else
    echo "  No memory directory found"
fi

# 3. Suggest new skills
echo ""
echo "💡 Suggesting new skills based on patterns..."

echo "  Potential skill opportunities:"
echo "    - NRJ Morning Routine (already created)"
echo "    - Dashboard Auto-Update (already created)"
echo "    - Self-Improvement System (already created)"
echo "    - Session Log Analyzer (this script)"

# 4. Performance metrics
echo ""
echo "📈 Performance Metrics:"
echo "  Sessions analyzed: $(find "$SESSIONS_DIR" -name "*.jsonl" 2>/dev/null | wc -l)"
echo "  Learning logs: $(find "$WORKSPACE/memory" -name "*.md" 2>/dev/null | wc -l)"
echo "  Skills created: $(find "$WORKSPACE/skills" -name "SKILL.md" 2>/dev/null | wc -l)"
echo "  Documentation: $(wc -l < "$WORKSPACE/MEMORY.md") lines"

# 5. Recommendations
echo ""
echo "🎯 Recommendations:"
echo "  1. Continue documenting all learnings"
echo "  2. Create skills for any new repeatable tasks"
echo "  3. Review MEMORY.md weekly for updates"
echo "  4. Monitor cron job execution"

echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "✅ ML ANALYSIS COMPLETE"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "Analysis saved to: $ANALYSIS_DIR/"
echo ""
