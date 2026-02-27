#!/bin/bash
# Podcast Manager - Quick Start Script
# Usage: bash run.sh [command]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="🎙️ Podcast Manager"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Header
show_header() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════╗"
    echo "║     🎙️ PODCAST MANAGER v1.0.0          ║"
    echo "╚════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Help
show_help() {
    show_header
    echo "Usage: bash run.sh [command]"
    echo ""
    echo "Commands:"
    echo "  fetch              Fetch latest episodes from RSS"
    echo "  list               List recent episodes"
    echo "  clips              Generate daily clips"
    echo "  email              Generate clips and send email"
    echo "  analyze [file]     Analyze audio file for best clips"
    echo "  verify             Run system verification"
    echo "  status             Show system status"
    echo "  help               Show this help message"
    echo ""
    echo "Examples:"
    echo "  bash run.sh fetch"
    echo "  bash run.sh clips"
    echo "  bash run.sh analyze /path/to/episode.mp3"
}

# Fetch episodes
cmd_fetch() {
    echo -e "${YELLOW}📥 Fetching latest episodes...${NC}"
    python3 "$SCRIPT_DIR/scripts/podcast-clipper.py" fetch-latest
    echo -e "${GREEN}✅ Episodes fetched${NC}"
}

# List episodes
cmd_list() {
    echo -e "${YELLOW}📋 Listing recent episodes...${NC}"
    python3 "$SCRIPT_DIR/scripts/podcast-clipper.py" list --limit 5
}

# Generate clips
cmd_clips() {
    echo -e "${YELLOW}✂️  Generating daily clips...${NC}"
    bash "$SCRIPT_DIR/scripts/daily-podcast-clips.sh"
}

# Send email
cmd_email() {
    echo -e "${YELLOW}📧 Generating clips and sending email...${NC}"
    python3 "$SCRIPT_DIR/scripts/daily-podcast-email.py" --send-email
}

# Analyze audio
cmd_analyze() {
    local file="$1"
    if [ -z "$file" ]; then
        echo -e "${RED}❌ Please specify an audio file${NC}"
        echo "Usage: bash run.sh analyze /path/to/episode.mp3"
        exit 1
    fi
    
    if [ ! -f "$file" ]; then
        echo -e "${RED}❌ File not found: $file${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}🔍 Analyzing audio...${NC}"
    python3 "$SCRIPT_DIR/scripts/perfect-clip-finder.py" "$file"
}

# Verify system
cmd_verify() {
    echo -e "${YELLOW}🔍 Running system verification...${NC}"
    bash "$SCRIPT_DIR/scripts/verify-podcast-system.sh"
}

# Show status
cmd_status() {
    show_header
    
    echo -e "${BLUE}📊 System Status${NC}"
    echo "================"
    
    # Check files
    echo -n "Scripts: "
    if [ -f "$SCRIPT_DIR/scripts/podcast-clipper.py" ]; then
        echo -e "${GREEN}✅${NC}"
    else
        echo -e "${RED}❌${NC}"
    fi
    
    # Check dependencies
    echo -n "ffmpeg: "
    if command -v ffmpeg >/dev/null 2>&1; then
        echo -e "${GREEN}✅ $(ffmpeg -version 2>/dev/null | head -1 | cut -d' ' -f3)${NC}"
    else
        echo -e "${RED}❌ Not installed${NC}"
    fi
    
    echo -n "python3: "
    if command -v python3 >/dev/null 2>&1; then
        echo -e "${GREEN}✅ $(python3 --version)${NC}"
    else
        echo -e "${RED}❌ Not installed${NC}"
    fi
    
    # Check today's production
    echo ""
    echo -e "${BLUE}📁 Today's Production${NC}"
    TODAY_DIR="/tmp/podcast-clips/$(date +%Y%m%d)"
    if [ -d "$TODAY_DIR" ]; then
        CLIP_COUNT=$(ls -1 "$TODAY_DIR"/*.mp3 2>/dev/null | wc -l)
        echo "  Clips: $CLIP_COUNT"
        echo "  Location: $TODAY_DIR"
    else
        echo "  No production today"
    fi
    
    # Check cron
    echo ""
    echo -n "Cron job: "
    if openclaw cron list 2>/dev/null | grep -q "PODKAST"; then
        echo -e "${GREEN}✅ Active${NC}"
    else
        echo -e "${YELLOW}⚠️  Not found${NC}"
    fi
}

# Main
case "${1:-help}" in
    fetch)
        show_header
        cmd_fetch
        ;;
    list)
        show_header
        cmd_list
        ;;
    clips)
        show_header
        cmd_clips
        ;;
    email)
        show_header
        cmd_email
        ;;
    analyze)
        show_header
        cmd_analyze "$2"
        ;;
    verify)
        cmd_verify
        ;;
    status)
        cmd_status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        show_help
        exit 1
        ;;
esac
