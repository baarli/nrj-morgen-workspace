#!/bin/bash
# deploy-video-function.sh - Deploy Supabase Edge Function via API

set -e

echo "🚀 Deployer process-video Edge Function..."
echo ""

# Hent credentials
source /root/.openclaw/workspace/.credentials/nrj-morgen.env

SUPABASE_PROJECT_ID="kvniauxokdtmpvjtfnej"
FUNCTION_NAME="process-video"

echo "📦 Pakker funksjon..."

# Lag temp-mappe
TMP_DIR=$(mktemp -d)
cd "$TMP_DIR"

# Kopier funksjon
mkdir -p "$FUNCTION_NAME"
cp /root/.openclaw/workspace/nrjmorgen-ui/supabase/functions/process-video/index.ts "$FUNCTION_NAME/"

# Zip filene
zip -r "$FUNCTION_NAME.zip" "$FUNCTION_NAME/"

echo ""
echo "⚠️  Manuell deploy nødvendig"
echo ""
echo "Gå til Supabase Dashboard:"
echo "  https://app.supabase.com/project/$SUPABASE_PROJECT_ID/functions"
echo ""
echo "Eller kjør lokalt med Docker:"
echo "  docker run -v /root/.openclaw/workspace/nrjmorgen-ui/supabase/functions:/functions \"
echo "    -e SUPABASE_ACCESS_TOKEN=din_token \"
echo "    supabase/supabase-cli functions deploy process-video"
echo ""

# Rydd opp
rm -rf "$TMP_DIR"

echo "✅ Funksjon klar for deploy!"
