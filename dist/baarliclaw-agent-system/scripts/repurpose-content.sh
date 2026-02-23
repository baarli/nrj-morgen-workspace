#!/bin/bash
# /root/.openclaw/workspace/scripts/repurpose-content.sh
# Gjenbruke innhold på tvers av plattformer

if [ $# -lt 1 ]; then
  echo "Bruk: repurpose-content <kilde> --to <format>"
  echo "Formater: podcast, instagram, tiktok, twitter, newsletter"
  exit 1
fi

SOURCE="$1"
FORMAT="${2:-instagram}"

echo "🔄 GJENBRUK AV INNHOLD"
echo "======================"
echo "Kilde: $SOURCE"
echo "Format: $FORMAT"
echo ""

REPURPOSE_DIR="/root/.openclaw/workspace/brain/repurposed"
mkdir -p "$REPURPOSE_DIR"

OUTPUT_FILE="$REPURPOSE_DIR/$(basename "$SOURCE")-$FORMAT-$(date +%Y%m%d).md"

case $FORMAT in
  instagram)
    cat > "$OUTPUT_FILE" << EOF
# 📸 Instagram-post fra: $SOURCE

**Bilde:** [Beskrivelse av bilde]

**Caption:**
🎙️ [Hook - fang oppmerksomhet]

[1-2 setninger om saken]

💬 Hva synes du? Del i kommentarene!

#NRJMorgen #Radio #Morgen #Kjendis #Underholdning #Norge

---
**Stories:**
- Poll: "Hva synes du om [saken]?"
- Quiz: "Gjett hvem som..."
- Behind the scenes: Fra studio
EOF
    ;;
  
  tiktok)
    cat > "$OUTPUT_FILE" << EOF
# 🎵 TikTok-video fra: $SOURCE

**Konsept:** [Kort beskrivelse]

**Script (30-60 sek):**
0-3s: [Hook - visuelt + tekst]
3-15s: [Oppsett av situasjon]
15-45s: [Hovedinnhold]
45-60s: [Call to action]

**Lyd:** Trending lyd eller egen stemme

**Tekst på skjerm:**
- [Tekst 1]
- [Tekst 2]

**Hashtags:**
#nrj #morgenradio #norge #kjendis #fyp #viral
EOF
    ;;
  
  podcast)
    cat > "$OUTPUT_FILE" << EOF
# 🎧 Podkast-episode fra: $SOURCE

**Tittel:** [Fengende tittel]

**Beskrivelse:**
[2-3 setninger som selger episoden]

**Varighet:** 20-30 minutter

**Struktur:**
- Intro (1 min)
- Bakgrunn (5 min)
- Hovedintervju/diskusjon (15 min)
- Oppsummering (3 min)
- Outro + CTA (1 min)

**Gjester:** [Hvis relevant]

**Show notes:**
- Tidsstempler
- Lenker nevnt
- Referanser
EOF
    ;;
  
  twitter)
    cat > "$OUTPUT_FILE" << EOF
# 🐦 Twitter/X-tråd fra: $SOURCE

Tweet 1/5 🧵
[Hook - kontroversielt eller spørsmål]

Tweet 2/5
[Context - bakgrunn]

Tweet 3/5
[Hovedpoeng]

Tweet 4/5
[Detalj/innsikt]

Tweet 5/5
[Oppsummering + CTA]
Hva synes du? 🤔

#NRJMorgen
EOF
    ;;
  
  newsletter)
    cat > "$OUTPUT_FILE" << EOF
# 📧 Nyhetsbrev fra: $SOURCE

**Emnelinje:** [Fengende emne]

**Preview tekst:** [2-3 ord som får folk til å åpne]

---

Hei [Navn]!

[Personlig intro]

**[Hovedsak tittel]**

[2-3 avsnitt om saken]

**[Andre saker]**
- Punkt 1
- Punkt 2
- Punkt 3

[Call to action]

Ha en strålende dag!
[Niklas/Baarli]

---
**PS:** [Noe morsomt eller ekstra]
EOF
    ;;
  
  *)
    echo "❌ Ukjent format: $FORMAT"
    exit 1
    ;;
esac

echo "✅ Innhold gjenbrukt: $OUTPUT_FILE"
echo ""
echo "💡 Tips: Tilpass tonen til hver plattform!"
