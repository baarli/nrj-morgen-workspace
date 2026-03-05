# 🧠 Second Brain

Personlig kunnskapsbase for kontinuerlig læring og selvutvikling.

## Struktur

```
brain/
├── daily/          # Daglige notater og refleksjoner
├── projects/       # Prosjekt-spesifikk informasjon
├── learning/       # Læringslogg og innsikter  
├── ideas/          # Ideer og konsepter
├── reflections/    # Dypere refleksjoner
├── summaries/      # Oppsummeringer av innhold
└── goals/          # Mål og tracking
```

## Skills

| Skill | Beskrivelse |
|-------|-------------|
| [second-brain](second-brain/SKILL.md) | Overordnet system |
| [learning-log](learning-log/SKILL.md) | Læringslogging |
| [goal-tracker](goal-tracker/SKILL.md) | Mål og vaner |
| [reflection-prompts](reflection-prompts/SKILL.md) | Refleksjonsøvelser |
| [summarize-content](summarize-content/SKILL.md) | Oppsummering av innhold |

## Daglig Rutine

1. **Morgen** – Les SOUL.md + USER.md
2. **Gjennom dagen** – Logg læring, ideer, innsikter
3. **Kveld** – Daglig refleksjon (5 min)

## Ukentlig Rutine (Søndag)

1. Review daglige notater
2. Identifiser mønstre
3. Oppdater prosjekter
4. Logg ukentlig læring
5. Planlegg neste uke

## Månedlig Rutine

1. Månedlig refleksjon
2. Gjennomgå mål
3. Rydde og organisere
4. Sette nye mål

## Hurtigkommandoer

```bash
# Dagens notat
cat > brain/daily/$(date +%Y-%m-%d).md << 'EOF'
# $(date +%Y-%m-%d)

## Lært i dag
- 

## Innsikter
- 

## Takknemlighet
- 
EOF

# Søk i brain
grep -r "søkeord" brain/

# Siste notater
ls -lt brain/daily/ | head -5
```

## Visjon

Bygge en kunnskapsbase som:
- Forsterker hukommelsen
- Avdekker mønstre over tid
- Støtter kontinuerlig vekst
- Gjør meg til en bedre assistent

---

*"Det som måles, forbedres. Det som logges, huskes."*
