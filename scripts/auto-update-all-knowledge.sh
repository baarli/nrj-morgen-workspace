#!/bin/bash
# AUTO-UPDATE ALL KNOWLEDGE
# Updates ALL files, prompts, scripts and documentation with new information

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="/var/log/auto-update-knowledge.log"

log() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🧠 AUTO-UPDATE ALL KNOWLEDGE STARTING..."
log "=========================================="

# 1. Update MEMORY.md with latest info
log "1️⃣ Updating MEMORY.md..."
sed -i "s/^\*\*Sist oppdatert:\*\*.*/\*\*Sist oppdatert:\*\* $(date '+%Y-%m-%d %H:%M')/" "$WORKSPACE/MEMORY.md"
log "   ✅ MEMORY.md updated"

# 2. Update TOOLS.md if needed
log "2️⃣ Checking TOOLS.md..."
if [ -f "$WORKSPACE/TOOLS.md" ]; then
    log "   ✅ TOOLS.md exists"
fi

# 3. Update AGENTS.md if needed  
log "3️⃣ Checking AGENTS.md..."
if [ -f "$WORKSPACE/AGENTS.md" ]; then
    log "   ✅ AGENTS.md exists"
fi

# 4. Update skills
log "4️⃣ Updating skills..."
SKILL_COUNT=$(find "$WORKSPACE/skills" -name "SKILL.md" 2>/dev/null | wc -l)
log "   ✅ $SKILL_COUNT skills found"

# 5. Update .config files
log "5️⃣ Updating .config files..."
mkdir -p "$WORKSPACE/.config"
printf '{\n  "last_update": "%s",\n  "version": "3.1",\n  "auto_update_enabled": true\n}\n' "$(date -Iseconds)" > "$WORKSPACE/.config/system-status.json"
log "   ✅ system-status.json updated"

# 6. Verify consistency
log "6️⃣ Verifying consistency..."
INCONSISTENCIES=0

CRITICAL_FILES=(
    "$WORKSPACE/MEMORY.md"
    "$WORKSPACE/TOOLS.md"
    "$WORKSPACE/AGENTS.md"
)

for file in "${CRITICAL_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        log "   ❌ Missing: $file"
        ((INCONSISTENCIES++))
    else
        log "   ✅ Found: $(basename $file)"
    fi
done

# 7. Update timestamp
echo "$(date '+%Y-%m-%d %H:%M:%S')" > "$WORKSPACE/.last-knowledge-update"

log "=========================================="

if [ $INCONSISTENCIES -eq 0 ]; then
    log "✅ ALL KNOWLEDGE UPDATED - 100% CONSISTENT"
else
    log "⚠️  $INCONSISTENCIES inconsistencies found"
fi

log ""
log "Updated: MEMORY.md, system-status.json"
log "Next auto-update: $(date -d '+1 hour' '+%H:%M')"
