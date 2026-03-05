#!/bin/bash
set -e  # Exit on error
# /root/.openclaw/workspace/scripts/crisis-respond.sh
# Håndtere kriser

if [ $# -lt 1 ]; then
  echo "Bruk: crisis-respond <krise-type> [--severity low|medium|high|critical]"
  echo "Eksempler: feil-i-sak, teknisk-problem, kontrovers, personalsak"
  exit 1
fi

CRISIS_TYPE="$1"
SEVERITY="${2:-medium}"

echo "⚠️  KRISERESPONS"
echo "================"
echo "Type: $CRISIS_TYPE"
echo "Alvorlighet: $SEVERITY"
echo ""

CRISIS_DIR="/root/.openclaw/workspace/brain/crisis"
mkdir -p "$CRISIS_DIR"

CRISIS_FILE="$CRISIS_DIR/crisis-$(date +%Y%m%d-%H%M%S).md"

cat > "$CRISIS_FILE" << EOF
# ⚠️  Krisehåndtering: $CRISIS_TYPE

**Tid:** $(date)  
**Alvorlighet:** $SEVERITY  
**Status:** [Aktiv/Løst]

---

## Situasjonsbeskrivelse

[Hva har skjedd?]

---

## Umiddelbare tiltak

- [ ] Vurdere alvorlighetsgrad
- [ ] Informere relevante personer
- [ ] Dokumentere hendelsen
- [ ] [Spesifikt for denne krisen]

---

## Kommunikasjon

### Internt:
- Hvem skal informeres:
- Hvordan:

### Eksternt (hvis relevant):
- Publikum:
- Media:
- Sosiale medier:

---

## Læring

**Hva gikk galt:**

**Hva gikk bra:**

**Hva kan forbedres:**

---

## Oppsummering

**Løst:** [Ja/Nei]  
**Tid til løsning:** [Minutter/timer]  
**Etterfølgende tiltak:**

EOF

echo "✅ Krisedokument opprettet: $CRISIS_FILE"
echo ""

case $SEVERITY in
  low)
    echo "🟡 LAV alvorlighet: Håndteres internt"
    ;;
  medium)
    echo "🟠 MEDIUM alvorlighet: Informere leder"
    ;;
  high)
    echo "🔴 HØY alvorlighet: Umiddelbar eskalering"
    ;;
  critical)
    echo "⚫ KRITISK: All hands on deck!"
    ;;
esac

echo ""
echo "💡 Husk:"
echo "   - Hold hodet kaldt"
echo "   - Dokumenter alt"
echo "   - Kommuniser tydelig"
echo "   - Lær etterpå"
