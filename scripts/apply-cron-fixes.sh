#!/bin/bash
# 🔧 CRON JOB FIXES - Applied 2026-02-28
# Fixes for common cron job issues

set -e

echo "🔧 Applying cron job fixes..."

# 1. Create missing self-dev directory
echo "1️⃣ Creating self-dev directory..."
mkdir -p /root/.openclaw/workspace/memory/self-dev
echo "   ✅ self-dev directory created"

# 2. Fix script permissions
echo "2️⃣ Fixing script permissions..."
chmod +x /root/.openclaw/workspace/scripts/*.sh 2>/dev/null || true
echo "   ✅ Script permissions fixed"

# 3. Verify critical files exist
echo "3️⃣ Verifying critical files..."
CRITICAL_SCRIPTS=(
    "/root/.openclaw/workspace/scripts/auto-update-all-knowledge.sh"
    "/root/.openclaw/workspace/scripts/self-dev-task-generator.sh"
    "/root/.openclaw/workspace/scripts/fetch_nielsen_live.py"
    "/root/.openclaw/workspace/scripts/fetch_podtoppen_live.py"
)

for script in "${CRITICAL_SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        echo "   ✅ Found: $(basename $script)"
    else
        echo "   ❌ Missing: $(basename $script)"
    fi
done

# 4. Test Python imports
echo "4️⃣ Testing Python imports..."
cd /root/.openclaw/workspace/scripts
python3 -c "import requests; import json; print('   ✅ Core imports OK')" 2>/dev/null || echo "   ⚠️  Import issues detected"

echo ""
echo "✅ Cron job fixes applied!"
echo "Run 'openclaw cron list' to verify job status"
