#!/bin/bash
# 🧹 System Cleanup Script
# Rydder gamle filer og optimaliserer systemet

set -e

echo "🧹 Starting system cleanup..."

# 1. Fjern Python cache
echo "1️⃣  Fjerner Python cache..."
find /root/.openclaw/workspace -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find /root/.openclaw/workspace -type f -name "*.pyc" -delete 2>/dev/null || true
echo "   ✅ Python cache fjernet"

# 2. Fjern gamle loggfiler
echo "2️⃣  Fjerner gamle logger..."
find /var/log -name "*.log.*" -mtime +7 -delete 2>/dev/null || true
find /root/.openclaw/workspace -name "*.log" -mtime +7 -delete 2>/dev/null || true
echo "   ✅ Logger fjernet"

# 3. Rydd /tmp
echo "3️⃣  Rydder /tmp..."
find /tmp -type f -mtime +3 -delete 2>/dev/null || true
echo "   ✅ /tmp ryddet"

# 4. Komprimer gamle rapporter
echo "4️⃣  Komprimerer gamle rapporter..."
cd /root/.openclaw/workspace/brain/reports
for file in *.json; do
    if [ -f "$file" ] && [ ! -f "$file.gz" ]; then
        gzip -k "$file" 2>/dev/null || true
    fi
done 2>/dev/null || true
echo "   ✅ Rapporter komprimert"

# 5. Vis disk-bruk
echo ""
echo "💾 Disk-bruk etter cleanup:"
df -h / | tail -1

echo ""
echo "✅ System cleanup fullført!"
