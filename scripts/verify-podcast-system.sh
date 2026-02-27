#!/bin/bash
set -e  # Exit on error
# Verifiser at podcast-klippe-systemet fungerer
# Bruk: bash verify-podcast-system.sh

echo "=========================================="
echo "  PODCAST SYSTEM VERIFIKASJON"
echo "=========================================="
echo ""

ERRORS=0

# 1. Sjekk at nødvendige filer finnes
echo "✓ Sjekker filer..."
if [ ! -f "/root/.openclaw/workspace/scripts/podcast-clipper.py" ]; then
    echo "  ❌ podcast-clipper.py mangler"
    ERRORS=$((ERRORS+1))
else
    echo "  ✅ podcast-clipper.py"
fi

if [ ! -f "/root/.openclaw/workspace/scripts/daily-podcast-clips.sh" ]; then
    echo "  ❌ daily-podcast-clips.sh mangler"
    ERRORS=$((ERRORS+1))
else
    echo "  ✅ daily-podcast-clips.sh"
fi

# 2. Sjekk at ffmpeg er installert
echo ""
echo "✓ Sjekker avhengigheter..."
if command -v ffmpeg >/dev/null 2>&1; then
    echo "  ✅ ffmpeg ($(ffmpeg -version | head -1 | cut -d' ' -f3))"
else
    echo "  ❌ ffmpeg ikke installert"
    ERRORS=$((ERRORS+1))
fi

if command -v python3 >/dev/null 2>&1; then
    echo "  ✅ python3 ($(python3 --version))"
else
    echo "  ❌ python3 ikke installert"
    ERRORS=$((ERRORS+1))
fi

# 3. Sjekk at dagens klipp finnes
echo ""
echo "✓ Sjekker dagens produksjon..."
TODAY_DIR="/tmp/podcast-clips/$(date +%Y%m%d)"
if [ -d "$TODAY_DIR" ]; then
    CLIP_COUNT=$(ls -1 "$TODAY_DIR"/clip_*.mp3 2>/dev/null | wc -l)
    if [ "$CLIP_COUNT" -ge 3 ]; then
        echo "  ✅ $CLIP_COUNT klipp funnet i $TODAY_DIR"
    else
        echo "  ⚠️  Kun $CLIP_COUNT klipp funnet (forventet 3+)"
    fi
else
    echo "  ⚠️  Ingen produksjon i dag ($TODAY_DIR finnes ikke)"
fi

# 4. Verifiser at klipp er gyldige
echo ""
echo "✓ Verifiserer MP3-filer..."
for f in "$TODAY_DIR"/clip_*.mp3; do
    if [ -f "$f" ]; then
        if ffprobe -v error "$f" >/dev/null 2>&1; then
            DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" | cut -d. -f1)
            echo "  ✅ $(basename $f) (${DURATION}s)"
        else
            echo "  ❌ $(basename $f) - ugyldig fil"
            ERRORS=$((ERRORS+1))
        fi
    fi
done

# 5. Sjekk cron-job
echo ""
echo "✓ Sjekker cron-job..."
if openclaw cron list 2>/dev/null | grep -q "PODKAST.*Daglig klipp"; then
    echo "  ✅ Cron-job aktiv"
else
    echo "  ⚠️  Cron-job ikke funnet"
fi

# 6. Sjekk RSS-feed
echo ""
echo "✓ Sjekker RSS-feed..."
if python3 /root/.openclaw/workspace/scripts/podcast-clipper.py fetch-latest >/dev/null 2>&1; then
    EP_COUNT=$(cat /tmp/podcast-clips/episodes.json 2>/dev/null | grep -c '"title"' || echo "0")
    echo "  ✅ RSS-feed tilgjengelig ($EP_COUNT episoder)"
else
    echo "  ❌ RSS-feed utilgjengelig"
    ERRORS=$((ERRORS+1))
fi

# Oppsummering
echo ""
echo "=========================================="
if [ $ERRORS -eq 0 ]; then
    echo "  ✅ SYSTEMET FUNGERER PERFEKT"
else
    echo "  ⚠️  $ERRORS FEIL FUNNET"
fi
echo "=========================================="
echo ""

exit $ERRORS
