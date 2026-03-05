#!/bin/bash
set -e  # Exit on error
# /root/.openclaw/workspace/scripts/brainstorm-ideas.sh
# Generere kreative ideer

if [ $# -lt 1 ]; then
  echo "Bruk: brainstorm-ideas <tema> [--count n] [--wild]"
  exit 1
fi

TOPIC="$1"
COUNT="${2:-20}"

echo "💡 BRAINSTORM: $TOPIC"
echo "====================="
echo "Mål: $COUNT ideer"
echo ""

IDEAS_FILE="/root/.openclaw/workspace/brain/ideas/brainstorm-$(date +%Y%m%d-%H%M%S).md"
mkdir -p $(dirname "$IDEAS_FILE")

cat > "$IDEAS_FILE" << EOF
# 💡 Brainstorm: $TOPIC

**Dato:** $(date '+%Y-%m-%d %H:%M')  
**Antall ideer:** $COUNT

---

## Ideer

EOF

echo "🎯 Genererer ideer..."
echo ""

# Ide-generering basert på teknikker
declare -a TECHNIQUES=(
  "SCAMPER: Substitute (bytt ut)"
  "SCAMPER: Combine (kombiner)"
  "SCAMPER: Adapt (tilpass)"
  "SCAMPER: Modify (modifiser)"
  "SCAMPER: Put to other use (annen bruk)"
  "SCAMPER: Eliminate (fjern)"
  "SCAMPER: Reverse (reverser)"
  "What if:...scenario"
  "Opposite: Gjør det motsatte"
  "Random: Legg til noe uventet"
  "Scale: Gjør det 10x større"
  "Scale: Gjør det 10x mindre"
)

for i in $(seq 1 $COUNT); do
  TECHNIQUE=${TECHNIQUES[$((RANDOM % ${#TECHNIQUES[@]}))]}
  
  echo "$i. **[$TECHNIQUE]**" >> "$IDEAS_FILE"
  echo "   - Idé basert på teknikken..." >> "$IDEAS_FILE"
  echo "" >> "$IDEAS_FILE"
  
  echo "   $i. [$TECHNIQUE]"
done

cat >> "$IDEAS_FILE" << EOF

---

## Top 3 Ideer å Utforske

1. **[Idé 1]** - Hvorfor denne er god
2. **[Idé 2]** - Hvorfor denne er god  
3. **[Idé 3]** - Hvorfor denne er god

---

## Neste Steg

- [ ] Vurdere ideer med team
- [ ] Velge 1-3 ideer å utvikle
- [ ] Lage prototype/plan
- [ ] Teste på målgruppe

EOF

echo ""
echo "✅ Brainstorm lagret: $IDEAS_FILE"
echo ""
echo "💡 Tips: Bruk 'creative-brainstorm' skill for mer strukturert tilnærming"
