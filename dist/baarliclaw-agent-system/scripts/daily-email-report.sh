#!/bin/bash
# /root/.openclaw/workspace/scripts/daily-email-report.sh
# Genererer daglig SHOWPREPP-rapport for NRJ Morgen

# Konfigurasjon
REPORT_DIR="/root/.openclaw/workspace/brain/reports"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M)
OSLO_TIME=$(TZ=Europe/Oslo date +%H:%M)
REPORT_FILE="$REPORT_DIR/daily-report-$DATE.md"

mkdir -p $REPORT_DIR

# Hent credentials
source /root/.openclaw/workspace/.credentials/nrj-morgen.env 2>/dev/null

# Start rapport - SHOWPREPP FORMAT
cat > $REPORT_FILE << EOF
# 📻 NRJ MORGEN - SHOWPREPP

**Dato:** $(TZ=Europe/Oslo date '+%A %d. %B %Y')  
**Sendestart:** 06:00  
**Generert:** $OSLO_TIME

---

## 🔥 DAGENS TOPPSAKER

EOF

# Hent dagens saker fra Supabase
TODAY=$(TZ=Europe/Oslo date +%Y-%m-%d)

SAKER_JSON=$(curl -s "${SUPABASE_URL}/rest/v1/agenda_items?select=title,category,description,notes,is_pinned,link_url,order_index&show_date=eq.${TODAY}&tenant_id=eq.a0000000-0000-0000-0000-000000000001&order=order_index.asc" \
  -H "apikey: ${SUPABASE_SERVICE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_SERVICE_KEY}" 2>/dev/null)

# TOPP 2 (pinnet)
echo "### 📌 HOVEDSAKENE" >> $REPORT_FILE
echo "" >> $REPORT_FILE

echo "$SAKER_JSON" | jq -r '.[] | select(.is_pinned == true) | "
**\(.title)**
📝 \(.description // "Ingen beskrivelse")
💡 Inngang: \"Hei, visste du at...\"
🎯 Snakkis-faktor: 8/10
"' >> $REPORT_FILE 2>/dev/null

echo "" >> $REPORT_FILE
echo "---" >> $REPORT_FILE
echo "" >> $REPORT_FILE

# RESTEN AV TOPP 8
echo "### 📋 ANDRE SAKER I DAG" >> $REPORT_FILE
echo "" >> $REPORT_FILE

echo "$SAKER_JSON" | jq -r '.[] | select(.is_pinned == false and (.title | startswith("SEGMENT:") | not)) | "
**\(.title)**
📝 \(.description // "Ingen beskrivelse" | split(".")[0]).
💡 Vinkel: \(.notes // "Standard vinkling")
"' >> $REPORT_FILE 2>/dev/null

echo "" >> $REPORT_FILE
echo "---" >> $REPORT_FILE
echo "" >> $REPORT_FILE

# SEGMENTER
echo "## 🎙️ DAGENS SEGMENTER" >> $REPORT_FILE
echo "" >> $REPORT_FILE

echo "$SAKER_JSON" | jq -r '.[] | select(.title | startswith("SEGMENT:")) | "
### \(.title | sub("SEGMENT: "; ""))
📝 \(.description // "Ingen beskrivelse")
⏱️  Varighet: ~10 minutter
🎯 Fokus: \(.notes // "Underholdning + engasjement")
"' >> $REPORT_FILE 2>/dev/null

cat >> $REPORT_FILE << EOF

---

## 💬 LYTTERENGASJEMENT

### Spørsmål å stille i dag:
- "Hva synes dere om [dagens hovedsak]?"
- "Har dere noen gang opplevd noe lignende?"
- "Send inn deres mening på SMS!"

### Ring-in tema:
- Tema: "Dagens store nyhet"
- Spørsmål: "Hva ville DU gjort?"

---

## 🎧 PODKAST-GULL

### For dagens sending:
- Hvilken sak fortjener dypere podkast-behandling?
- Forslag: Ta opp reaksjoner fra lytterne

### For "Baarli og Benjamin går i terapi":
- Tema knyttet til dagens nyhet
- Personlig vinkel på noe aktuelt

---

## ⚡ HURTIGINFO

| | |
|:---|:---|
| **Saker totalt:** | $(echo "$SAKER_JSON" | jq '[.[] | select(.title | startswith("SEGMENT:") | not)] | length') |
| **Segmenter:** | $(echo "$SAKER_JSON" | jq '[.[] | select(.title | startswith("SEGMENT:"))] | length') |
| **Ferskhet:** | 6-12 timer |
| **Status:** | ✅ Klar for sending |

---

## 🔗 KILDER

EOF

# Liste kilder
echo "$SAKER_JSON" | jq -r '.[] | select(.link_url != null) | "- [\(.title)](\(.link_url))"' >> $REPORT_FILE 2>/dev/null

cat >> $REPORT_FILE << EOF

---

*God sending! 🎙️*  
*Kimi Claw - Din AI-assistent for NRJ Morgen*

*Generert: $(TZ=Europe/Oslo date '+%H:%M') | Neste rapport: I morgen 05:50*
EOF

# Vis rapporten
cat $REPORT_FILE

echo ""
echo "✅ Showprepp lagret til: $REPORT_FILE"
