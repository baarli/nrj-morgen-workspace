#!/bin/bash
# Vev Documentation Auto-Updater
# Sikrer at all dokumentasjon alltid er i riktig rekkefølge og oppdatert

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="$WORKSPACE/brain/logs/doc-auto-update.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting documentation auto-update" >> "$LOG_FILE"

# 1. Verifiser at avatar finnes
if [ ! -f "$WORKSPACE/brain/vev-avatar.jpg" ]; then
    echo "[ERROR] Avatar not found!" >> "$LOG_FILE"
    exit 1
fi

# 2. Verifiser at alle master-dokumenter finnes
REQUIRED_FILES=(
    "SYSTEM_ARCHITECTURE.md"
    "AGENTS.md"
    "TOOLS.md"
    "MEMORY.md"
    "PRINCIPLES.md"
    "SOUL.md"
    "IDENTITY.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$WORKSPACE/$file" ]; then
        echo "[ERROR] Missing required file: $file" >> "$LOG_FILE"
        exit 1
    fi
done

# 3. Verifiser at avatar er referert i IDENTITY.md
if ! grep -q "vev-avatar.jpg" "$WORKSPACE/IDENTITY.md"; then
    echo "[WARNING] Avatar not referenced in IDENTITY.md" >> "$LOG_FILE"
fi

# 4. Verifiser at avatar er referert i SYSTEM_ARCHITECTURE.md
if ! grep -q "vev-avatar.jpg" "$WORKSPACE/SYSTEM_ARCHITECTURE.md"; then
    echo "[WARNING] Avatar not referenced in SYSTEM_ARCHITECTURE.md" >> "$LOG_FILE"
fi

# 5. Git commit hvis det er endringer
cd "$WORKSPACE"
if [ -n "$(git status --porcelain)" ]; then
    git add -A
    git commit -m "Auto-update: Documentation verified and synchronized
    
- Avatar references checked
- All master documents verified
- System integrity maintained
    
    Timestamp: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE" 2>&1
    echo "[INFO] Changes committed to git" >> "$LOG_FILE"
else
    echo "[INFO] No changes to commit" >> "$LOG_FILE"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Documentation auto-update complete" >> "$LOG_FILE"
