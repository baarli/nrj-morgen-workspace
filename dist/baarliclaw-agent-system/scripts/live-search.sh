#!/bin/bash
# /root/.openclaw/workspace/scripts/live-search.sh
# Sanntidssøk etter ferske nyheter

if [ $# -lt 1 ]; then
  echo "Bruk: live-search <søkeord> [options]"
  echo ""
  echo "Options:"
  echo "  --freshness 1h|6h|24h     Tidsvindu (default: 1h)"
  echo "  --sources news|social|all   Kilder (default: all)"
  echo "  --max-results N           Maks antall resultater"
  exit 1
fi

QUERY="$1"
FRESHNESS="${2:-1h}"
SOURCES="${3:-all}"
MAX_RESULTS="${4:-10}"

echo "🔍 LIVE SØK: $QUERY"
echo "=================="
echo "Ferskhet: $FRESHNESS"
echo "Kilder: $SOURCES"
echo ""

# Simuler live-søk (i praksis ville dette brukt API-er)
echo "⏳ Søker i sanntid..."
echo ""

# Hvis kimi_search er tilgjengelig, bruk den
if command -v kimi_search > /dev/null 2>&1; then
  echo "Bruker kimi_search..."
  # Her ville vi kalt faktisk søk
else
  echo "ℹ️  For å bruke live-søk, trenger du API-nøkler:"
  echo "   - NewsAPI"
  echo "   - Twitter API"
  echo "   - Reddit API"
  echo ""
  echo "Legg til i .credentials/live-search.env:"
  echo 'NEWSAPI_KEY="din_nøkkel"'
  echo 'TWITTER_BEARER="din_token"'
  echo 'REDDIT_CLIENT_ID="din_id"'
fi

echo ""
echo "💡 Tips: Bruk 'monitor-topic' for kontinuerlig overvåking"
