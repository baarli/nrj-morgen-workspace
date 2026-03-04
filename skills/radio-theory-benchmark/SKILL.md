---
name: radio-theory-benchmark
description: Creative radio theory knowledge base and benchmark generator for podcast and radio show development. Use when generating innovative segment ideas, benchmarking radio formats, analyzing show structures, or creating new radio concepts. Triggers on requests about radio theory, podcast benchmarks, show formats, segment ideas, or when user wants creative radio/podcast inspiration.
---

# Radio Theory Benchmark Skill

Denne skillen gir dyp kunnskap om radioteori og hjelper med å generere kreative benchmarks for podcast- og radioproduksjon.

## Hva skillen gjør

1. **Radioteori-database** - Omfattende kunnskap om radioformater, strukturer og teknikker
2. **Benchmark-generator** - Skaper nye, innovative segmentkonsepter basert på etablerte prinsipper
3. **Format-analyse** - Analyserer eksisterende show og foreslår forbedringer
4. **Kreativ inspirasjon** - Kombinerer radioteori med kreativ tenkning for unike ideer

## Når du skal bruke denne skillen

- Bruker ber om radioteori-kunnskap
- Bruker vil ha nye segmentideer eller benchmarks
- Bruker vil analysere et show-format
- Bruker vil ha kreativ inspirasjon for podcast/radio
- Bruker nevner "benchmark", "radio theory", "segment ideas", "show format"

## Viktige radioteori-prinsipper

### The PPM Paradox (Nielsen)
- Lyttere husker ikke hva de hørte for 5 minutter siden
- Maks 8-10 minutter per segment for å unngå "tuning out"
- "Tease, deliver, reset" - struktur for hvert segment

### The Clock Concept
- Fast struktur skaper trygghet
- Topp og bunn av timen = høyest lytterskjerphet
- "Quarter hours matter" - hver 15. minutt teller

### The Three E's
- **Entertain** - Underhold først
- **Educate** - Lær noe nytt
- **Engage** - Få lytteren til å føle seg involvert

### The Hook Theory
- Første 30 sekunder avgjør om lytteren blir
- Start med spørsmål, konflikt eller overraskelse
- Aldri "soft open" i radio

## Benchmark-typer

### 1. Content Benchmarks
- **Top 10 Lists** - Klassisk, alltid populært
- **Mystery Guest** - Gjett hvem som ringer
- **Truth or Dare** - Sannhet eller utfordring
- **Would You Rather** - Dilemmaer
- **Rate My...** - Vurdering av lytter-innhold

### 2. Interaction Benchmarks
- **Phone Scams** - Ringe og lure noen
- **Text Line** - Lyttere sender inn, host velger
- **Poll Battles** - To motsetninger, lytterne stemmer
- **Shoutouts** - Hyllester med twist

### 3. Personality Benchmarks
- **The Confession** - Personlig avsløring
- **The Argument** - Kjørt debatt
- **The Prank** - Practical joke på air
- **The Challenge** - Host gjør noe dumt

## Hvordan generere nye benchmarks

### Steg 1: Velg en teoretisk base
- Hvilken psykologisk trigger vil du bruke?
- FOMO, schadenfreude, nysgjerrighet, fellesskap?

### Steg 2: Kombiner med format
- Telefon? Tekst? Stemme? Video?
- Live eller produsert?

### Steg 3: Legg til twist
- Hva gjør dette annerledes?
- Hva er "the hook"?

### Steg 4: Test strukturen
- Tease (10 sek)
- Setup (30 sek)
- Execution (2-5 min)
- Payoff (30 sek)
- Reset (10 sek)

## Eksempel: Ny benchmark - "The Reverse Interview"

**Konsept:** Gjest intervjuer hosten
**Teoretisk base:** Rollebytte skaper uventet dynamikk
**Hook:** "I dag er det DU som stiller spørsmålene"
**Struktur:**
1. Intro: Forklar reglene (20s)
2. Gjest velger 3 spørsmål fra lyttere (30s)
3. Host svarer ærlig (3-4 min)
4. Gjest vurderer svarene (30s)
5. Utro: Neste gjest annonseres (10s)

## Referanser

For detaljert informasjon om spesifikke formater, se:
- `references/radio_formats.md` - Kjente radioformater verden over
- `references/psychology_triggers.md` - Psykologiske prinsipper i radio
- `references/show_structures.md` - Time-planer og show-arkitektur

## Scripts

- `scripts/benchmark_generator.py` - Genererer nye benchmark-ideer
- `scripts/format_analyzer.py` - Analyserer show-formater
- `scripts/segment_timer.py` - Beregner optimal segment-lengde

## Bruk

### Generere ny benchmark:
```bash
python3 scripts/benchmark_generator.py --type content --mood funny --duration 5
```

### Analysere format:
```bash
python3 scripts/format_analyzer.py --show "NRJ Morgen" --segments 4
```

### Beregne segment-tid:
```bash
python3 scripts/segment_timer.py --content-type interview --attention high
```
