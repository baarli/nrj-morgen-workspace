# NRJ Morgen Content Pipeline v3

## Oversikt
Automatisk innholdsgenerering og publiseringssystem for NRJ Morgen med AI-drevet research, content approval workflow og integrasjon med Supabase.

## Funksjoner

### 1. AI Research Module
- Søker i 5 kategorier: Reality TV, Kjendis Drama, Film & TV, Musikk, Internasjonalt
- Bruker Brave Search API for nyhetsinnhenting
- Beregner engagement score for hver sak
- Henter opptil 30 potensielle saker per kjøring

### 2. Content Approval Workflow
- Auto-godkjenning basert på regler:
  - Tittel lengde: 10-100 tegn
  - Sammendrag: >50 tegn
  - Gyldig URL
  - Engagement score >0.3
- Manuell godkjenning for resten

### 3. Supabase Integrasjon
- Publiserer godkjente saker direkte til `agenda_items`
- Inkluderer metadata: kilde, kategori, engagement score
- Automatisk tidsstempling

## Bruk

### Kjør pipeline (kun research)
```bash
cd /root/.openclaw/workspace/scripts
python3 content-pipeline-v3.py
```

### Kjør pipeline med publisering
```bash
cd /root/.openclaw/workspace/scripts
python3 content-pipeline-v3.py --publish
```

## Filstruktur
```
scripts/
├── content-pipeline-v3.py      # Hoved pipeline
├── ai-research-module.py        # Research modul (standalone)
└── supabase-publisher.py        # Supabase integrasjon (standalone)
```

## Resultater
Lagres i: `/tmp/content-pipeline-results-YYYYMMDD.json`

## Logger
`/var/log/content-pipeline-v3.log`

## API Keys
- Brave Search API: `BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev`
- Supabase: Lastes fra `.credentials/nrj-morgen.env`

## Siste kjøring
- Dato: 2026-02-25
- Funnet: 30 saker
- Godkjent: 15 saker
- Publisert: 5 saker

## Forbedringsmuligheter
- [ ] Bildegenerering med AI
- [ ] Dashboard for manuell godkjenning
- [ ] Cron-job for automatisk kjøring
- [ ] Bedre filtrering av ikke-norske saker
- [ ] Integrasjon med Morning Routine v2.1
