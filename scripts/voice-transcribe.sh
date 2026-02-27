#!/bin/bash
set -e  # Exit on error
# /root/.openclaw/workspace/scripts/voice-transcribe.sh
# Transkriber talememoer til tekst

if [ $# -lt 1 ]; then
  echo "Bruk: voice-transcribe <lydfil> [--output <fil>]"
  exit 1
fi

AUDIO_FILE="$1"
OUTPUT_FILE="${2:-/root/.openclaw/workspace/brain/voice/transcript-$(date +%Y%m%d-%H%M%S).md}"

if [ ! -f "$AUDIO_FILE" ]; then
  echo "❌ Fil ikke funnet: $AUDIO_FILE"
  exit 1
fi

mkdir -p $(dirname "$OUTPUT_FILE")

echo "🎤 Transkriberer: $AUDIO_FILE"
echo "⏳ Dette kan ta litt tid..."

# Bruk OpenAI Whisper hvis tilgjengelig, ellers bruk alternativ
if which whisper > /dev/null 2>&1; then
  whisper "$AUDIO_FILE" --language Norwegian --output_format txt --output_dir /tmp/
  TRANSCRIPT=$(cat /tmp/$(basename "$AUDIO_FILE" .m4a).txt 2>/dev/null || cat /tmp/$(basename "$AUDIO_FILE" .mp3).txt 2>/dev/null)
else
  # Fallback: Bruk speech_recognition via Python
  TRANSCRIPT=$(python3 << 'EOF'
import speech_recognition as sr
import sys

try:
    r = sr.Recognizer()
    with sr.AudioFile(sys.argv[1]) as source:
        audio = r.record(source)
    text = r.recognize_google(audio, language="no-NO")
    print(text)
except Exception as e:
    print(f"[Transkripsjon krever whisper eller speech_recognition: {e}]")
EOF
  "$AUDIO_FILE" 2>/dev/null || echo "[Installér whisper: pip install openai-whisper]")
fi

# Lag markdown-fil
cat > "$OUTPUT_FILE" << EOF
# 🎤 Talememo - $(date '+%Y-%m-%d %H:%M')

**Kilde:** $(basename "$AUDIO_FILE")
**Transkribert:** $(date)

---

$TRANSCRIPT

---

## Handlinger
- [ ] Gå gjennom og trekke ut viktige punkter
- [ ] Konvertere til oppgaver hvis relevant
- [ ] Arkivere i riktig mappe
EOF

echo "✅ Transkripsjon lagret: $OUTPUT_FILE"
echo ""
echo "📝 Oppsummering:"
echo "$TRANSCRIPT" | head -5
echo "..."
