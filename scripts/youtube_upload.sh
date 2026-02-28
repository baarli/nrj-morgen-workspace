#!/bin/bash
# 🎬 YouTube Uploader - Last opp podcast-episoder til YouTube
# Bruk: ./youtube_upload.sh [video_file] [title] [description_file]

set -e

# Konfigurasjon
VIDEO_FILE="${1:-}"
TITLE="${2:-NRJ Morgen Podcast - Episode}"
DESC_FILE="${3:-}"

# Farger
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🎬 NRJ Morgen YouTube Uploader"
echo "================================"

# Sjekk om video-fil finnes
if [ -z "$VIDEO_FILE" ] || [ ! -f "$VIDEO_FILE" ]; then
    echo -e "${RED}❌ Feil: Video-fil ikke funnet${NC}"
    echo "Bruk: $0 [video_file] [title] [description_file]"
    echo ""
    echo "Tilgjengelige videoer:"
    find /root/.openclaw/workspace/downloads -name "*.mp4" 2>/dev/null | head -5
    exit 1
fi

# Sjekk om yt-dlp er installert (for metadata)
if ! command -v yt-dlp &> /dev/null; then
    echo -e "${YELLOW}⚠️  yt-dlp ikke installert${NC}"
    echo "   Installer med: pip install yt-dlp"
fi

# Generer beskrivelse hvis ikke oppgitt
if [ -z "$DESC_FILE" ] || [ ! -f "$DESC_FILE" ]; then
    echo "📝 Genererer standard beskrivelse..."
    
    DESC_FILE="/tmp/youtube_description_$$.txt"
    cat > "$DESC_FILE" << 'EOF'
🎙️ NRJ MORGEN PODCAST
Med Baarli og Benjamin

📻 Hør oss live på NRJ hver morgen 06-10
🎧 Podcast: Søk etter "Baarli og Benjamin går i terapi" der du lytter til podcaster

📱 Følg oss:
• Instagram: @nrjmorgen
• TikTok: @nrjmorgen
• Facebook: NRJ Morgen

🔗 RELEVANTE LINKER:
• NRJ: https://nrj.no
• Podkast: https://podcasts.apple.com/no/podcast/baarli-og-benjamin-gar-i-terapi

#NRJMorgen #Podcast #Norge #Radio #BaarliOgBenjamin #Morgenradio
EOF
fi

echo ""
echo "📋 Opplastingsdetaljer:"
echo "  Video: $VIDEO_FILE"
echo "  Tittel: $TITLE"
echo "  Beskrivelse: $DESC_FILE"
echo ""

# Sjekk filstørrelse
FILE_SIZE=$(du -h "$VIDEO_FILE" | cut -f1)
echo "📦 Filstørrelse: $FILE_SIZE"

# Sjekk video-lengde hvis ffprobe er tilgjengelig
if command -v ffprobe &> /dev/null; then
    DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VIDEO_FILE" 2>/dev/null | cut -d. -f1)
    if [ -n "$DURATION" ]; then
        MINUTES=$((DURATION / 60))
        SECONDS=$((DURATION % 60))
        echo "⏱️  Varighet: ${MINUTES}m ${SECONDS}s"
    fi
fi

echo ""
echo -e "${YELLOW}⚠️  Viktig:${NC}"
echo "For å laste opp til YouTube må du:"
echo "1. Ha en Google-konto"
echo "2. Ha opprettet en YouTube-kanal"
echo "3. Bruke YouTube Studio eller API"
echo ""

echo "🔧 Anbefalt fremgangsmåte:"
echo "1. Gå til https://studio.youtube.com"
echo "2. Klikk 'Create' → 'Upload videos'"
echo "3. Velg fil: $VIDEO_FILE"
echo "4. Kopier tittel: $TITLE"
echo "5. Kopier beskrivelse fra: $DESC_FILE"
echo ""

echo "📋 Klar til opplasting!"
echo ""
echo "Tittel (kopier denne):"
echo "======================"
echo "$TITLE"
echo ""
echo "Beskrivelse (kopier denne):"
echo "==========================="
cat "$DESC_FILE"
echo ""
echo "======================="

# Lagre metadata for senere
META_DIR="/root/.openclaw/workspace/brain/youtube-uploads"
mkdir -p "$META_DIR"

META_FILE="$META_DIR/upload_$(date +%Y%m%d_%H%M%S).json"
cat > "$META_FILE" << EOF
{
  "date": "$(date -Iseconds)",
  "video_file": "$VIDEO_FILE",
  "title": "$TITLE",
  "description_file": "$DESC_FILE",
  "file_size": "$FILE_SIZE",
  "status": "ready_for_upload"
}
EOF

echo ""
echo -e "${GREEN}✅ Metadata lagret til: $META_FILE${NC}"
echo ""
echo "Neste steg:"
echo "1. Åpne YouTube Studio"
echo "2. Last opp videoen"
echo "3. Marker oppgaven som fullført i Task Master"
