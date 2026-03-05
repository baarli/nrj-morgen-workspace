#!/bin/bash
# VEV SESSION WRAPPER v2.0
# This script ensures pre-flight runs before EVERY session
# 
# USAGE:
#   Option 1: Run this manually before starting work
#   Option 2: Set as alias in shell profile
#   Option 3: Call from any session initialization
#
# To make this automatic, add to your shell profile:
#   alias vev-session="/root/.openclaw/workspace/scripts/vev-session-wrapper.sh"

set -e

WORKSPACE="/root/.openclaw/workspace"
SCRIPT_DIR="$WORKSPACE/scripts"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🤖 VEV SESSION WRAPPER v2.0${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════${NC}"
echo ""

# Step 1: Run Auto-Exec Enforcer
echo -e "${YELLOW}Step 1: Running Auto-Exec Enforcer...${NC}"
if [ -f "$SCRIPT_DIR/auto-exec-enforcer.sh" ]; then
    bash "$SCRIPT_DIR/auto-exec-enforcer.sh"
else
    echo -e "${RED}❌ Auto-exec enforcer not found!${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Session initialization complete!${NC}"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🚀 You now have full context loaded:${NC}"
echo -e "${BLUE}   • All skills scanned${NC}"
echo -e "${BLUE}   • Recent memories loaded${NC}"
echo -e "${BLUE}   • Active systems identified${NC}"
echo -e "${BLUE}   • Current mood: $(cat $WORKSPACE/.vev-preflight-context 2>/dev/null | grep 'Current Mood' | cut -d: -f2 | xargs || echo 'unknown')${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "You can now start working with complete context."
echo ""
