#!/bin/bash
# /root/.openclaw/workspace/scripts/forecast-trends.sh
# Forutsi kommende trender

echo "🔮 TRENDFORECAST"
echo "================="
echo ""
echo "Analyse basert på:"
echo "  • Sosiale medier-signal"
echo "  • Søketrender"
echo "  • Nyhetsmønstre"
echo ""

FORECAST_FILE="/root/.openclaw/workspace/brain/forecasts/trend-$(date +%Y%m%d).md"
mkdir -p $(dirname "$FORECAST_FILE")

cat > "$FORECAST_FILE" << EOF
# 🔮 Trend Forecast - $(date '+%Y-%m-%d')

## Trender som bygger seg opp

### 1. [Trend navn]
**Konfidens:** [Høy/Medium/Lav]  
**Tidsramme:** [Når den treffer]  
**Signal:** [Hva som tyder på denne trenden]

### 2. [Trend navn]
**Konfidens:** [Høy/Medium/Lav]  
**Tidsramme:** [Når den treffer]  
**Signal:** [Hva som tyder på denne trenden]

### 3. [Trend navn]
**Konfidens:** [Høy/Medium/Lav]  
**Tidsramme:** [Når den treffer]  
**Signal:** [Hva som tyder på denne trenden]

---

## Tidlige signaler

| Signal | Styrke | Kilde |
|--------|--------|-------|
| | | |

---

## Anbefalinger

### For NRJ Morgen:
- [ ] 
- [ ] 

### For Podkast:
- [ ] 
- [ ] 

---

*Sist oppdatert: $(date)*
*Neste oppdatering: $(date -d '+3 days' '+%Y-%m-%d')*
EOF

echo "✅ Forecast laget: $FORECAST_FILE"
echo ""
echo "💡 Tips:"
echo "   - Sjekk TikTok, Twitter, Reddit daglig"
echo "   - Bruk Google Trends for søkedata"
echo "   - Følg med på hva influencere snakker om"
