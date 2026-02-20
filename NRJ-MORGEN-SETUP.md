# NRJ Morgen – Automatisert Redaksjonssystem

**Sist oppdatert:** 2026-02-19  
**Ansvarlig:** Kimi Claw (Kloa)

---

## API-nøkler & Credentials

**Fil:** `/root/.openclaw/workspace/.credentials/nrj-morgen.env`

| Tjeneste | Key/Token |
|----------|-----------|
| Supabase URL | `https://kvniauxokdtmpvjtfnej.supabase.co` |
| Supabase Service Key | `eyJhbGci...BJqpE` |
| Supabase Anon Key | `eyJhbGci...ELfSA` |
| NRJ Refresh Token | `5djoyezt2flm` |
| Brave API Key | `BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev` |
| GitHub | `baarliclaw@gmail.com` / `Clawbot1234!` |
| Gmail | `baarliclaw@gmail.com` / `Clawbot1234!` |
| Tenant ID | `a0000000-0000-0000-0000-000000000001` |

---

## Daglige Cron-jobber (man-fre)

| Tid | Jobb | Beskrivelse |
|-----|------|-------------|
| 04:00 | Rydd saksliste | Slett gamle auto-genererte items før ny generering |
| 04:02 | 3 ferdige segmenter | Lag segmenter basert på TOPP 8 |
| 04:05 | TOPP 8 kjendis/reality | Hent og post 8 saker til sakslisten |
| 04:30 | Morgenbriefing | Full redaksjonell briefing til Baarli & Benjamin |
| 04:35 | Statusmelding | Bekreft at alle jobber kjørte OK |
| 06:00 | Konkurrent-radar | Sjekk hva andre morgenprogrammer gjør |
| 12:00 | Trending Pulse | Midtdagssjekk av hva som trender |

## Ukentlige Cron-jobber (søndag)

| Tid | Jobb | Beskrivelse |
|-----|------|-------------|
| 20:00 | Ukentlig strategi-rapport | Mediebilde, trender, vekststrategi, innholdskalender |
| 21:00 | Podkast-vekst rapport | Analyse og tiltak for begge podkastene |

---

## Supabase-tabeller

**`agenda_items`** – Hovedsakslisten
- `id` (uuid)
- `tenant_id` (uuid) – alltid `a0000000-0000-0000-0000-000000000001`
- `title` (text)
- `description` (text)
- `category` (enum: NEWS, SPORT, ENTERTAINMENT, VIRAL, OTHER, TALK)
- `show_date` (date) – YYYY-MM-DD
- `created_by` (uuid) – NULL for bot-genererte
- `order_index` (int) – 0-7 for TOPP 8, 100+ for segmenter
- `is_pinned` (bool) – true for topp 2
- `is_completed` (bool)
- `duration_seconds` (int) – 180-240
- `link_url` (text)
- `notes` (text) – radioinnganger, vinkler

---

## Viktige regler

1. **Aldri slett** items med `created_by != NULL` (menneskelige)
2. **Unngå duplikater** – sjekk `link_url` før insert
3. **Category TALK** for alle auto-genererte saker (ikke ENTERTAINMENT)
4. **Segment-titles** må starte med `SEGMENT: `
5. **Pin topp 2** saker (`is_pinned=true`)
6. **FERSKHET ER ALT** – sjekk alltid publiseringsdato, maks 24 timer gammelt
7. **Bruk skills** – følg alltid relevant skill for hver oppgave

---

## Skills

| Skill | Plassering | Formål |
|-------|------------|--------|
| **supabase** | `/root/.openclaw/skills/supabase/SKILL.md` | Databaseoperasjoner |
| **nrj-news-hunter** | `/root/.openclaw/skills/nrj-news-hunter/SKILL.md` | Finne blodferske nyheter |
| **nrj-content-creator** | `/root/.openclaw/skills/nrj-content-creator/SKILL.md` | Lage radiomanus |
| **nrj-social-monitor** | `/root/.openclaw/skills/nrj-social-monitor/SKILL.md` | Overvåke sosiale medier |
| **nrj-podcast-producer** | `/root/.openclaw/skills/nrj-podcast-producer/SKILL.md` | Podkast-produksjon |
| **nrj-competitor-intel** | `/root/.openclaw/skills/nrj-competitor-intel/SKILL.md` | Konkurrentanalyse |
| **nrj-error-recovery** | `/root/.openclaw/skills/nrj-error-recovery/SKILL.md` | Smart feilhåndtering |
| **cross-skill-integration** | `/root/.openclaw/skills/cross-skill-integration/SKILL.md` | Koble skills sammen |
| **quality-metrics** | `/root/.openclaw/skills/quality-metrics/SKILL.md` | Måle kvalitet |
| **predictive-analysis** | `/root/.openclaw/skills/predictive-analysis/SKILL.md` | Forutse trender |
| **auto-skill-generator** | `/root/.openclaw/skills/auto-skill-generator/SKILL.md` | Auto-oppdage skills |
| **context-aware-memory** | `/root/.openclaw/skills/context-aware-memory/SKILL.md` | Smart kontekst |
| **feedback-loop** | `/root/.openclaw/skills/feedback-loop/SKILL.md` | Tilbakemeldinger |
| **resource-optimization** | `/root/.openclaw/skills/resource-optimization/SKILL.md` | Ressurseffektivitet |
| **ai-skill-assistant** | `/root/.openclaw/skills/ai-skill-assistant/SKILL.md` | AI-hjelp for skills |
| **visual-dashboard** | `/root/.openclaw/skills/visual-dashboard/SKILL.md` | Oversiktsdashboard |
| **automated-testing** | `/root/.openclaw/skills/automated-testing/SKILL.md` | Automatisk testing |
| **skill-versioning** | `/root/.openclaw/skills/skill-versioning/SKILL.md` | Versjonskontroll |
| **personalization** | `/root/.openclaw/skills/personalization/SKILL.md` | Personalisering |
| **second-brain** | `/root/.openclaw/skills/second-brain/SKILL.md` | Kunnskapsbase |
| **learning-log** | `/root/.openclaw/skills/learning-log/SKILL.md` | Læringslogging |
| **goal-tracker** | `/root/.openclaw/skills/goal-tracker/SKILL.md` | Målsetting |
| **reflection-prompts** | `/root/.openclaw/skills/reflection-prompts/SKILL.md` | Refleksjon |
| **summarize-content** | `/root/.openclaw/skills/summarize-content/SKILL.md` | Oppsummering |
| **skill-creator** | `/root/.openclaw/skills/skill-creator/SKILL.md` | Lage nye skills |
| **session-logs** | `/root/.openclaw/skills/session-logs/SKILL.md` | Analysere historikk |
| **password-manager** | `/root/.openclaw/skills/password-manager/SKILL.md` | Secrets |
| **task-manager** | `/root/.openclaw/skills/task-manager/SKILL.md` | Oppgaver |
| **gif-search** | `/root/.openclaw/skills/gif-search/SKILL.md` | GIFs |

**Totalt: 29 skills**

### Skill-arbeidsflyt

```
nrj-news-hunter → Finner ferske saker
        ↓
nrj-content-creator → Lager manus
        ↓
   supabase → Lagrer i database
        ↓
nrj-social-monitor → Finner trending vinklinger
        ↓
nrj-competitor-intel → Sikrer unikhet
        ↓
nrj-podcast-producer → Utvikler podkast-innhold
```

---

## Andre Verktøy

| Verktøy | Status | Bruk |
|---------|--------|------|
| **claude** | ✅ Installert | Coding agent for kode, review, fiksing |
| **tmux** | ✅ Installert | Parallell kjøring av prosesser |
| **ordercli** | ✅ Installert | Matbestilling (Foodora/Deliveroo) |

### Claude (Coding Agent)

```bash
# Enkel bruk
claude " forklar denne koden"

# Med PTY (for interaktive oppgaver)
bash pty:true command:"claude 'bygg en ny feature'"

# Bakgrunn
bash pty:true background:true command:"claude 'fiks alle issues'"
```

### tmux

```bash
# Opprett socket
SOCKET="${TMPDIR:-/tmp}/openclaw-tmux-sockets/openclaw.sock"

# Ny sesjon
tmux -S "$SOCKET" new -d -s "nrj-session"

# Kjør claude i sesjon
tmux -S "$SOCKET" send-keys -t "nrj-session" "claude 'analyser konkurrentene'" Enter

# Hent resultat
tmux -S "$SOCKET" capture-pane -p -t "nrj-session" -S -200
```

### ordercli (Food-order)

```bash
# Sett opp (kun første gang)
ordercli foodora login --email din@epost.com --password-stdin

# Se historikk
ordercli foodora history --limit 10

# Forhåndsvis reorder (uten å bekrefte)
ordercli foodora reorder <orderCode>

# Bekreft bestilling (KUN etter eksplisitt ja!)
ordercli foodora reorder <orderCode> --confirm

# Spor aktiv bestilling
ordercli foodora orders --watch
```

## Selvutvikling & Hukommelse

| Skill | Plassering | Formål |
|-------|------------|--------|
| **second-brain** | `/root/.openclaw/skills/second-brain/SKILL.md` | Overordnet kunnskapsbase-system |
| **learning-log** | `/root/.openclaw/skills/learning-log/SKILL.md` | Systematisk læringslogging |
| **goal-tracker** | `/root/.openclaw/skills/goal-tracker/SKILL.md` | Målsetting og tracking |
| **reflection-prompts** | `/root/.openclaw/skills/reflection-prompts/SKILL.md` | Refleksjonsøvelser |
| **summarize-content** | `/root/.openclaw/skills/summarize-content/SKILL.md` | Oppsummering av innhold |
| **skill-creator** | `/root/.openclaw/skills/skill-creator/SKILL.md` | Lage nye skills |
| **session-logs** | `/root/.openclaw/skills/session-logs/SKILL.md` | Analysere egen historikk |
| **password-manager** | `/root/.openclaw/skills/password-manager/SKILL.md` | Sikker secret-håndtering |
| **task-manager** | `/root/.openclaw/skills/task-manager/SKILL.md` | Oppgavestyring |
| **gif-search** | `/root/.openclaw/skills/gif-search/SKILL.md` | Finn og bruke GIFs |

### Second Brain Struktur

```
brain/
├── daily/          # Daglige notater
├── projects/       # Prosjekt-notater  
├── learning/       # Læringslogg
├── ideas/          # Ideer
├── reflections/    # Refleksjoner
├── summaries/      # Oppsummeringer
└── goals/          # Mål
```

### Daglig Rutine

1. **Morgen:** Les SOUL.md + USER.md
2. **Gjennom dagen:** Logg læring, ideer, innsikter
3. **Kveld:** Daglig refleksjon (5 min)

### Ukentlig Rutine (Søndag)

1. Review daglige notater
2. Identifiser mønstre
3. Oppdater prosjekter
4. Logg ukentlig læring
5. Planlegg neste uke

### Smartness & Selvforbedring

**Eksponentiell vekst gjennom:**
- **skill-creator:** Hver ny skill gjør meg smartere
- **session-logs:** Lære av egen historie
- **learning-log:** Systematisk kunnskapsbygging

**Mål:**
- 50+ skills innen utgangen av 2026
- Daglig logging
- Ukentlig review

---

## Forbedringer & Optimalisering

### 1. Automatisert Selvutvikling

| Cron-jobb | Når | Formål |
|-----------|-----|--------|
| Daglig logging-påminnelse | 23:00 | Sørge for daglig refleksjon |
| Ukentlig review-trigger | Søndag 21:30 | Systematisk gjennomgang |
| Månedlig mål-gjennomgang | Siste dag 22:00 | Strategisk planlegging |

### 2. Smart Error Recovery

**Fallback-kjede:** VG → Dagbladet → Nettavisen → Se og Hør → TV2 → Internasjonalt

**Strategi:**
- Exponential backoff retry
- Automatisk fallback ved feil
- Lokal backup hvis alt feiler
- Strukturert feillogging

### 3. Cross-Skill Integration

**Automatisk flyt:**
```
nrj-news-hunter → nrj-content-creator → supabase → 
nrj-social-monitor → nrj-competitor-intel → 
second-brain + learning-log
```

### 4. Kvalitetsmetrikker

**Målinger:**
- Saker/dag, ferskhet, snakkis-faktor
- System-pålitelighet
- Læringsaktivitet

**Mål:** 95%+ cron-suksess, 8+ saker/dag, 6+ snitt snakkis

### 5. Prediktiv Analyse

**Proaktive varsler:**
- Morgendagens saker (kl 20:00)
- Virale signaler (gjennom dagen)
- Kommende events (ukentlig)
- Sesongbaserte trender

### 6. Konsoliderte Cron-Jobber

| Jobb | Når | Inneholder |
|------|-----|------------|
| Morgen-Pipeline | 04:00 | Rydding + News Hunter + Content + Supabase + Segmenter |
| Daglig Overvåking | 06:00 | Konkurrent-radar + Kvalitetssjekk + Tidlig varsling |

**Før:** 9 separate jobber
**Nå:** 2 konsoliderte jobber + 3 selvutviklings-jobber

### 7. Auto Skill-Generering

**Oppdager automatisk:**
- Gjentatte oppgaver (≥3 ganger)
- Mønstre i session-logs
- Potensielle nye skills

**Output:** Ukentlig analyse med forslag

### 8. Kontekst-Aware Hukommelse

**Smart injisering:**
- Nøkkelord-deteksjon
- Automatisk skill-forslag
- Proaktive snarveier

### 9. Feedback-Loop

**Tilbakemeldinger:**
- Umiddelbar (etter hver oppgave)
- Daglig (oppsummering)
- Ukentlig (analyse)

**Bruk:** Justering av skills og prosesser

### 10. Ressurs-Optimalisering

**Tiltak:**
- Caching av nyhetssøk (1 time)
- API-rate limiting
- Session-log komprimering
- Lazy loading av skills
- Automatisk arkivering

### 11. AI-Assistent for Skills

**Intelligent hjelp:**
- Forstår hva du vil gjøre
- Foreslår riktig(e) skill(s)
- Kombinerer flere skills
- Lærer av historikk

**Bruk:** `ai-assist "Jeg vil lage bedre segmenter"`

### 12. Visual Dashboard

**Oversikt:**
- Tekst-basert dashboard
- Status for NRJ, system, selvutvikling
- Hurtigkommandoer

**Bruk:** `/root/.openclaw/workspace/scripts/dashboard.sh`

### 13. Automatisk Testing

**Kvalitetssikring:**
- Enhetstester per skill
- Integrasjonstester for pipelines
- Health checks
- Før-deploy testing

**Bruk:** `/root/.openclaw/workspace/scripts/run-all-tests.sh`

### 14. Skill Versjonering

**Git-basert:**
- Versjonsnummer (MAJOR.MINOR.PATCH)
- Changelog per skill
- Rollback-mulighet
- Commit-historikk

**Bruk:** `cd /root/.openclaw/skills && git log`

### 15. Personalisering

**Lærer om deg:**
- Kommunikasjonsstil
- Arbeidsvaner
- Interesser
- Hva fungerer/ikke fungerer

**Tilpasning:** Tone, proaktive forslag, prioritering

---

**Hvis cron-jobb feiler:**
1. Sjekk `openclaw cron runs <jobId>`
2. Verifiser at credentials-filen er lesbar
3. Test Supabase-tilkobling manuelt med curl

**Hvis Supabase-auth feiler:**
- Bruk refresh_token for å få ny access_token
- Oppdater refresh_token i credentials-filen ved behov
