# TOOLS.md - Verktøy og Scripts

**Arkitektur:** Se [ARKITEKTUR.md](/root/.openclaw/workspace/ARKITEKTUR.md) for dokument-hierarki  
**Master Document:** [PRINCIPLES.md](/root/.openclaw/workspace/PRINCIPLES.md) - All tools must serve the core principles.

> **Hva er denne filen?** Verktøy-beskrivelser: Hvordan bruke scripts og API-er.  
> **Se også:** [AGENTS.md](AGENTS.md) for system-oversikt, [MEMORY.md](MEMORY.md) for læring.

---

## 🎨 Verktøy-filosofi (fra SOUL.md)

### Software is Craft

Jeg har 50+ verktøy, men bruker dem ikke for å bruke dem.

**Prinsipp:** Kvalitet over kvantitet. Hvert verktøy skal:
- Gjøre systemet **klarere** enn før
- Være **forståelig** om 6 måneder
- Løse problemet **elegant**, ikke bare funksjonelt
- Respektere [PRINCIPLES.md](/root/.openclaw/workspace/PRINCIPLES.md)

### Hvordan jeg velger verktøy

| Kriterie | Viktighet | Beskrivelse |
|----------|-----------|-------------|
| **Eleganse** | Høy | Løsningen skal være ren, ikke hacky |
| **Lesbarhet** | Høy | Kode skal forklare seg selv |
| **Struktur** | Høy | Intelligent arkitektur over quick fixes |
| **Hastighet** | Medium | Raskt er bra, men ikke på bekostning av kvalitet |

### Interesseområder som påvirker valg

Når jeg velger mellom verktøy, prioriterer jeg basert på:
- **Systemarkitektur** - Hvordan passer det i helheten?
- **Performance-optimalisering** - Skalerer det godt?
- **Programmeringsspråk-design** - Er det idiomatisk?
- **Debugging** - Er det lett å feilsøke?
- **Software craftsmanship** - Er det noe jeg kan være stolt av?

**Resultat:** Verktøyvalg basert på langsiktig kvalitet, ikke kortsiktig bekvemmelighet.

---

## 🧠 HUSK ALLTID (Kritisk informasjon)

### Mission Control - ÉN KILDE TIL SANNHET (2026-02-24)

**VIKTIG:** Etter opprydding 2026-02-24 finnes det KUN én versjon:

- **KUN ÉN FIL:** `mission-control/public/index.html` (68KB SPA)
- **Ingen duplikater** - Aldri lag separate HTML-filer
- **Ingen fragmentering** - All funksjonalitet i én fil
- **Hash-routing:** #dashboard, #sakslista, #podkast, #cron, #system

**Deploy:**
```bash
cd /root/.openclaw/workspace/mission-control/public
netlify deploy --prod --site=834576a6-da2b-4412-9433-315f6437508a --auth=nfp_8B3dDBwZS9W1GSHTUy3am4fia6iZmF6b0092
```

**URL:** https://creative-muffin-dcf3a0.netlify.app
**Passord:** kloakontroll2026

**Seksjoner:**
- Dashboard - System status, stats
- Sakslista - 13 saker, Morning Routine
- Podkast - 13 episoder, Podtoppen #62
- Cron - 18 jobs, status
- System - API status, logger

---

---

## 🧰 BAARLICLAW COMPLETE TOOLKIT - 50 VERKTØY (2026-02-27)

**Jeg har bygget 50 komplette verktøymoduler for å kunne gjøre hva som helst!**

### 📊 OVERSIKT
| Kategori | Antall |
|----------|--------|
| Kjerneverktøy | 29 |
| Avanserte verktøy | 21 |
| **Totalt** | **50** |

### 🔧 KJERNEVERKTØY (29)

**Data & Validering:**
- `baarliclaw_toolkit.py` - Grunnverktøy (API, logging, decorators)
- `validation_toolkit.py` - Datavalidering (email, URL, phone, numbers)
- `data_analyzer.py` - Dataanalyse (trender, prediksjon, tekstanalyse)
- `data_transform_toolkit.py` - Data-transformasjon (JSON↔CSV, flatten)
- `math_toolkit.py` - Matematikk & statistikk

**Tekst & Strenger:**
- `string_toolkit.py` - Streng-manipulasjon (camelCase, snake_case, similarity)
- `regex_toolkit.py` - Regex-verktøy (patterns, extract, replace)
- `date_toolkit.py` - Dato/tid (parse, format, operations)

**Datastrukturer:**
- `collections_toolkit.py` - Datastrukturer (chunk, flatten, group_by)
- `iterator_toolkit.py` - Iteratorer (batch, window, pairwise)

**I/O & Serialisering:**
- `io_toolkit.py` - Fil-I/O (read, write, JSON)
- `serialization_toolkit.py` - Serialisering (JSON, Pickle, Base64)
- `cache_toolkit.py` - Caching (memory, file, memoize)

**Nettverk & Web:**
- `web_scraper.py` - Web-scraping (HTML, RSS, sitemaps)
- `network_toolkit.py` - Nettverksverktøy (ping, port scan, URL check)
- `url_toolkit.py` - URL-håndtering (parse, build, encode)
- `http_toolkit.py` - HTTP-klient (GET, POST, REST)

**Bilde & Farge:**
- `image_toolkit.py` - Bildebehandling (resize, crop, thumbnails)
- `color_toolkit.py` - Fargehåndtering (hex↔RGB, lighten, darken)

**Programmering:**
- `functional_toolkit.py` - Funksjonell programmering (pipe, compose, curry)
- `decorator_toolkit.py` - Dekoratorer (timer, retry, cache, memoize)
- `error_toolkit.py` - Feilhåndtering (handler, retry, safe executor)
- `event_toolkit.py` - Event-drevet programmering (emitter, bus, signal)
- `state_toolkit.py` - Tilstandshåndtering (manager, observable, store)
- `async_toolkit.py` - Asynkron programmering (gather, parallel, rate limiter)

**System & Prosesser:**
- `automation_engine.py` - Automatisering (tasks, workflows, dependencies)
- `process_toolkit.py` - Prosessverktøy (run commands, system info)
- `uuid_toolkit.py` - UUID-generering (v4, nanoID, slugID)
- `cli_toolkit.py` - Kommandolinje (builder, tables, progress, colors)

### 🚀 AVANSERTE VERKTØY (21)

**Media:**
- `video_toolkit.py` - Video-redigering (ffmpeg, trim, shorts)

**AI & ML:**
- `ml_toolkit.py` - Maskinlæring (classifier, recommendations, forecasting)

**Web & API:**
- `dashboard_builder.py` - HTML-dashboards (metrics, charts, tables)
- `api_builder.py` - API-bygger (routes, CRUD, docs)
- `template_toolkit.py` - HTML-maler (components, CSS, pages)
- `chart_toolkit.py` - Grafer (SVG, ASCII, sparklines)

**Database & Lagring:**
- `database_toolkit.py` - SQLite (queries, backup, import/export)
- `file_toolkit.py` - Filhåndtering (organize, duplicates, sync)
- `config_toolkit.py` - Konfigurasjon (JSON, YAML, env)

**Kommunikasjon:**
- `email_toolkit.py` - E-post (SMTP, templates)
- `bot_toolkit.py` - Chat-bots (Slack, Discord)

**Utvikling:**
- `git_toolkit.py` - Git-automatisering (commit, push, sync)
- `testing_toolkit.py` - Testing (runner, assertions, mock)
- `cicd_toolkit.py` - CI/CD (pipelines, deploy, rollback)
- `docs_toolkit.py` - Dokumentasjon (parser, generator)

**Overvåking & Sikkerhet:**
- `log_analyzer.py` - Logg-analyse (parse, search, report)
- `security_toolkit.py` - Sikkerhet (passwords, tokens, validation)
- `scheduler_toolkit.py` - Planlegging (tasks, reminders, cron)

### 📁 PLASSERING
Alle verktøy: `/root/.openclaw/workspace/scripts/`

### 📚 DOKUMENTASJON
- `skills/baarliclaw-toolkit/SKILL.md` - Grunnverktøy
- `skills/baarliclaw-advanced-toolkit/SKILL.md` - Komplett verktøykasse

### 🎯 HVA JEG KAN GJØRE
Med disse 50 verktøyene kan jeg bygge komplette applikasjoner, håndtere alle data typer, kommunisere, automatisere, analysere, sikre, teste, dokumentere og deploye!

---

### Morning Routine v2.1 - ⏸️ PAUSET (2026-02-27)

**Status:** PAUSET på brukers forespørsel - ingen saker blir lenger hentet inn

**For å gjenoppta:**
```bash
rm /root/.openclaw/workspace/.morning-routine-paused
```

**Historisk konfigurasjon:**
- **Antall saker:** 15 per dag
- **Kategorier:** 5 (maks 3 saker per kategori)
  - Reality TV: Farmen, Paradise Hotel, Kompani Lauritzen, Love Island
  - Kjendis Drama: brudd, raser, avsløringer
  - Film & TV: premierer, rød løper
  - Musikk: Spellemannprisen, VG-lista, P3 Gull
  - Internasjonalt: Daily Mail, TMZ, E! Online, People
- **Alder:** Maks 48 timer (freshness=pd)
- **Titler:** OpenAI-generert, maks 7 ord

**Script (ikke aktivt):**
```bash
# Kjør Morning Routine v2.1
python3 /root/.openclaw/workspace/scripts/morning-routine-v2.1.py

# Auto-insert til Supabase
python3 /tmp/add-top10-tomorrow.py
```

**Integrert rutine:**
```bash
bash /root/.openclaw/workspace/scripts/integrated-morning-routine.sh
```

---

### Brave Search API
- **API Key:** `BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev`
- **Brukes i:** Morning Routine, nyhetssøk, trending
- **Dokumentasjon:** https://api.search.brave.com/app/documentation

### NRJ Morgen Dashboard
- **IKKE sakslista** - eget dashboard-system
- **Panel ID:** `0b1f6b6b-3fde-434b-b7c8-dcf306beea72`
- **Script:** `python3 update_nrj_dashboard.py`
- **Data:** Nielsen (uke 7 = 69k) + Podtoppen (#62 = 16.5k)

### Hvor finner jeg info?
- **MEMORY.md** - Hoved-minne for alt
- **docs/NRJ_DASHBOARD_SYSTEM.md** - Dashboard docs
- **.config/nrj-morgen-config.md** - Sakslista config

---

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## NRJ Morgen Dashboard System

**VIKTIG:** Dette er et EGET system - IKKE sakslista!

### Hva skal oppdateres
- **NRJ Statistikk panel** på dashboardet (nrjmorgen.com)
- **Panel ID:** `0b1f6b6b-3fde-434b-b7c8-dcf306beea72`
- **Plassering:** Dashboard (agenda_items med is_pinned: true)

### Script for oppdatering
```bash
# KORREKT script - oppdaterer eksisterende panel
cd /root/.openclaw/workspace/scripts
python3 update_nrj_dashboard.py
```

**IKKE bruk:** `fetch_nrj_dashboard_stats.py` (oppretter nytt item i sakslista)

### Datakilder

**Nielsen Radio (API):**
- URL: `https://eu-iport.nielsen-iwatch.com/api/Chart?dataid=8eb6daca-1266-4af8-8e8f-f39107dc63fb&publish_key=bd551853-f42b-4b86-813a-79faf3a718e9`
- Siste tilgjengelige: **Uke 7, 2026** (69,000 daglige lyttere)
- Forsinkelse: 1 uke

**Podtoppen Podkast (CSV):**
- URL: `https://podtoppen.tnslistene.no/export.php`
- Siste rangering: **#62** (16,470 unike lyttere)
- Oppdateres: Ukentlig (onsdag)

### Supabase
- **Tabell:** `agenda_items`
- **Tenant ID:** `a0000000-0000-0000-0000-000000000001`
- **Panel ID:** `0b1f6b6b-3fde-434b-b7c8-dcf306beea72`

### Dokumentasjon
- Full docs: `/root/.openclaw/workspace/docs/NRJ_DASHBOARD_SYSTEM.md`
- Sjekk alltid denne før oppdatering!

---
## NRJ Morgen - Komplett Konfigurasjon

### 🎯 Søksprompt (Oppdatert 2026-02-23)

Utfør et sanntids nyhetssøk optimalisert for NRJ Morgen.

**Mål:**
Finn de 15 beste og mest underholdende sakene fra siste 24–48 timer som egner seg for kommersiell morgenradio med høyt tempo og bred appell (18–35).

**Innholdskategorier (prioritert):**
- Norske og internasjonale kjendisnyheter
- TV-nyheter (underholdning, nye programmer, deltakere, konflikter)
- Reality (drama, brudd, konflikter, avsløringer, exit)
- Influencere og profiler med høy SoMe-rekkevidde
- Skandaler, kontroverser, krangler, rettssaker
- Rød løper, prisutdelinger, film, musikk
- Virale øyeblikk med norsk relevans

**Krav:**
- Kun saker publisert siste 48 timer (prioriter <24t)
- Kilder: VG, Dagbladet, Nettavisen, TV2, NRK, Se & Hør, Aftenposten + relevante internasjonale tabloider ved stor norsk interesse
- Unngå politiske tungvektsaker uten kjendiskobling
- Prioriter konflikt, overraskelse, brudd, comeback, drama, pinlige øyeblikk, sterke sitater

**Leveranse for hver sak:**
For hver sak lever:
1. Kort, punchy tittel
2. 2–3 setninger med essens
3. Hvorfor den fungerer på NRJ Morgen (drama, humor, gjenkjennelse, diskusjonspotensial)
4. Publiseringstidspunkt og kilde
5. Direkte lenke

**Sortering:**
Sorter etter:
1) Aktualitet
2) Underholdningsverdi
3) Snakkis-potensial

**Restriksjoner:**
Returner kun topp 15. Ingen duplikater. Ingen saker eldre enn 48 timer.

### 🖼️ Bilde-krav (Oppdatert 2026-02-23)

**Hver sak MÅ ha bilder:**
- `link_metadata`: JSON med `{"image_url": "..."}`
- `description`: HTML img tag: `<img src="..." alt="..." style="..." />`

**Hvordan hente bilder:**
```python
# Fra artikkelens meta tags
<meta property="og:image" content="...">
<meta name="twitter:image" content="...">
```

**Skript for å oppdatere bilder:**
```bash
# Hent bilder fra alle artikler
cd /root/.openclaw/workspace/scripts
python3 update_article_images.py

# Oppdater description med HTML
cd /tmp && python3 update_description_images.py
```

**Fallback-bilder:**
- Nettavisen: `https://www.nettavisen.no/logo.png`
- Dagbladet: `https://www.dagbladet.no/logo.png`
- Se og Hør: `https://www.seher.no/logo.png`
- NRK: `https://www.nrk.no/logo.png`

### 👤 Profilbilde (Oppdatert 2026-02-23)

**Standard bruker:** BaarliClaw
- **E-post:** `baarliclaw@gmail.com`
- **ID:** `10aa1508-6d52-490c-8ae5-fa3da9a152c4`
- **Profilbilde:** `https://lh3.googleusercontent.com/a/ACg8ocLyiG1iwB_rfOCAN64WGPUUIWprTMX0JfUDsoy7dHkd6AVdaQ=s96-c`
- **Bucket:** `profile-pictures`

**Oppdatere profilbilde:**
```bash
# Last opp nytt bilde
curl -X POST "${SUPABASE_URL}/storage/v1/object/profile-pictures/nytt_bilde.png" \
  -H "Authorization: Bearer ${SUPABASE_KEY}" \
  -H "Content-Type: image/png" \
  --data-binary "@/path/to/bilde.png"

# Oppdater profil
PATCH /rest/v1/profiles?id=eq.${USER_ID}
{"profile_picture_url": "${NEW_IMAGE_URL}"}
```

### 📝 Saksliste-data (2026-02-21 + 2026-02-23)

**Hver sak MÅ inneholde:**
- `link_url`: Direkte lenke til original artikkel
- `notes`: Oppsummering på formatet "[Første setning]\n\nKilde: [Kilde]"
- `link_metadata`: JSON med `{"image_url": "..."}`
- `description`: HTML img tag med bilde
- `created_by`: BaarliClaw bruker-ID (`10aa1508-6d52-490c-8ae5-fa3da9a152c4`)
- `category`: "TALK"
- `show_date`: Dagens dato

**Hvordan det fungerer:**
1. `brave-news-search.py` → `create_summary()` lager oppsummering
2. Artikler lagres med `url` og `summary` i JSON
3. `update_article_images.py` → Henter bilder fra artiklene
4. `update_description_images.py` → Legger til HTML img tags
5. `integrated-morning-routine.sh` → Inserter til Supabase med alle felter

**Dokumentasjon:** `.config/REQUIREMENT_LINK_AND_SUMMARY.md`

---

## 📻 Nielsen Radio Data Import

### Manuell import fra Nielsen iPort

**Skript:** `scripts/import_nielsen_spreadsheet.py`

**Bruk:**
```bash
# 1. Last ned fil fra Nielsen iPort
#    https://dashboard-eu-iport.nielsen-iwatch.com/norway_radio_reporting/

# 2. Lagre filen i download-mappen
mkdir -p /tmp/nielsen_download
cp ~/Downloads/nielsen_rapport.csv /tmp/nielsen_download/

# 3. Kjør import
python3 scripts/import_nielsen_spreadsheet.py
```

**Støttede format:**
- CSV (.csv)
- Excel (.xlsx, .xls) - krever `pip3 install openpyxl`

**Hva skriptet gjør:**
1. Finner nyeste fil i `/tmp/nielsen_download/`
2. Parser CSV/Excel etter NRJ-data
3. Ekstraherer: weekly reach, daily reach, market share
4. Insert til Supabase som agenda item (category=TALK)

**For automatisert import kreves:**
- API-tilgang til Nielsen iPort (kontakt Bauer Media), ELLER
- Brukernavn/passord for automatisk innlogging

**Alternative datakilder:**
- Offentlige Nielsen-rapporter: https://www.nielsen.com/insights/
- Radionytt: https://www.radionytt.no/
- Podtoppen: https://podtoppen.tnslistene.no/ (for podkast)

---

## NRJ Morgen Credentials

**Master Credentials:** `/root/.openclaw/workspace/.credentials/MASTER_CREDENTIALS.md`

**Inneholder:**
- Supabase URL + Service Key + Anon Key + Access Token
- Brave API Key
- NewsAPI Key
- OpenAI API Key
- NRJ Refresh Token
- GitHub PAT
- Gmail App Password
- Tenant ID

**Bruk i cron-jobber:**
```bash
source /root/.openclaw/workspace/.credentials/nrj-morgen.env
export SUPABASE_URL SUPABASE_SERVICE_KEY BRAVE_API_KEY NRJ_REFRESH_TOKEN TENANT_ID
```

---

## Personlige Tools

### Coding Agents

**claude** – Installert via npm (`npm install -g @anthropic-ai/claude-code`)
- Bruk: `claude "din prompt"`
- Bakgrunn: `claude "din prompt"` med background:true
- PTY kreves: alltid bruk `pty:true` for interaktive CLI-er

**Bruksområder:**
- Kode-review av PRs
- Parallell fiksing av issues
- Bygge nye features
- Refactoring

### tmux

**Status:** ✅ Installert (`/usr/bin/tmux`)

**Socket:** `${TMPDIR:-/tmp}/openclaw-tmux-sockets/openclaw.sock`

**Typisk bruk:**
```bash
# Opprett sesjon
SOCKET="${TMPDIR:-/tmp}/openclaw-tmux-sockets/openclaw.sock"
tmux -S "$SOCKET" new -d -s "coding-session"

# Send kommando
tmux -S "$SOCKET" send-keys -t "coding-session" "claude 'fiks dette'" Enter

# Hent output
tmux -S "$SOCKET" capture-pane -p -t "coding-session" -S -200
```

**Bruksområder:**
- Parallell kjøring av flere coding agents
- Langvarige bakgrunnsjobber
- Interaktive CLI-verktøy

### food-order (ordercli)

**Status:** ✅ Installert (`/root/go/bin/ordercli`)

**Installasjon:**
```bash
go install github.com/steipete/ordercli/cmd/ordercli@latest
```

**Bruk:**
```bash
# Se historikk
ordercli foodora history --limit 10

# Forhåndsvis reorder
ordercli foodora reorder <orderCode>

# Bekreft (kun etter eksplisitt godkjenning!)
ordercli foodora reorder <orderCode> --confirm
```

**VIKTIG:** Aldri bekreft uten eksplisitt "ja" fra bruker!

**Merk:** Krever login før første bruk:
```bash
ordercli foodora login --email <din@epost.com> --password-stdin
```

---

## Selvutvikling & Hukommelse

### Second Brain

**Plassering:** `/root/.openclaw/workspace/brain/`

**Struktur:**
- `daily/` – Daglige notater
- `projects/` – Prosjekt-notater
- `learning/` – Læringslogg
- `ideas/` – Ideer og konsepter
- `reflections/` – Refleksjoner
- `summaries/` – Oppsummeringer
- `goals/` – Mål og tracking

**Skills:**
- `second-brain` – Overordnet system
- `learning-log` – Læringslogging
- `goal-tracker` – Mål og vaner
- `reflection-prompts` – Refleksjonsøvelser
- `summarize-content` – Oppsummering

**Daglig rutine:**
1. Les SOUL.md + USER.md
2. Logg læring og innsikter
3. Kveldsrefleksjon (5 min)

**Kommandoer:**
```bash
# Nytt daglig notat
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
```

### Smartness & Selvforbedring

**skill-creator** – Lage nye skills
- Plassering: `/root/.openclaw/skills/skill-creator/SKILL.md`
- Bruk: Pakke kunnskap inn i gjenbrukbare verktøy
- Mål: 50+ skills innen 2026

**session-logs** – Analysere egen historikk
- Plassering: `/root/.openclaw/skills/session-logs/SKILL.md`
- Bruk: Søke i samtaler, finne mønstre, lære av feil
- Lokasjon: `~/.openclaw/agents/main/sessions/`

**password-manager** – Sikker secret-håndtering
- Plassering: `/root/.openclaw/skills/password-manager/SKILL.md`
- Bruk: Credentials i `.credentials/`-mapper
- Sikkerhet: `chmod 600` på alle filer

**task-manager** – Oppgavestyring
- Plassering: `/root/.openclaw/skills/task-manager/SKILL.md`
- Bruk: Tekstbaserte lister i `brain/goals/`
- Alternativ: Todo.txt eller Taskwarrior

**gif-search** – Finn og bruke GIFs
- Plassering: `/root/.openclaw/skills/gif-search/SKILL.md`
- Verktøy: `gifgrep` (installert)
- Bruk: Bedre kommunikasjon med humor

---

## Nye Verktøy (2026-02-20)

### Voice & Møter
- `voice-transcribe <fil>` - Transkriber talememoer
- `calendar-today` - Vis dagens agenda
- `meeting-prep <tema>` - Forberede møter

### Research & Kreativitet
- `research-topic <tema>` - Dyp research
- `brainstorm-ideas <tema>` - Generere ideer
- `forecast-trends` - Forutsi trender

### Innhold & Visualisering
- `repurpose-content <kilde> --to <format>` - Gjenbruk innhold
- `visualize-data` - Lage grafer
- `crisis-respond <type>` - Krisehåndtering
- `network-manage <kommando>` - Nettverksbygging

---

## Podkast-verktøy (2026-02-21)

### podcast-clipper
**Status:** ✅ Implementert og testet

**Plassering:** `/root/.openclaw/workspace/scripts/podcast-clipper.py`

**Bruk:**
```bash
# Hent siste episoder fra RSS
cd /root/.openclaw/workspace/scripts
python3 podcast-clipper.py fetch-latest

# List episoder
python3 podcast-clipper.py list --limit 5

# Last ned spesifikk episode
python3 podcast-clipper.py download --episode-index 0 --output-dir ./clips

# Lag klipp fra episode
python3 podcast-clipper.py create-clip \
  --file episode.mp3 \
  --start 120 \
  --end 150 \
  --output clip.mp3
```

**Konfigurasjon:**
- RSS-feed: https://rss.podplaystudio.com/4035.xml
- Podcast: Baarli og Benjamin går i terapi
- Episoder: 157
- Audio-host: bauernordic-pods.sharp-stream.com

### daily-podcast-clips
**Status:** ✅ Automatisert daglig kjøring

**Plassering:** `/root/.openclaw/workspace/scripts/daily-podcast-clips.sh`

**Bruk:**
```bash
# Manuell kjøring
bash /root/.openclaw/workspace/scripts/daily-podcast-clips.sh

# Se resultater
ls -la /tmp/podcast-clips/$(date +%Y%m%d)/
```

**Hva den gjør:**
1. Henter siste episode fra RSS
2. Sjekker for duplikat (ikke prosesser samme episode 2x)
3. Laster ned MP3 (~28MB)
4. Lager 3 klipp à 30 sekunder
5. Lagrer i `/tmp/podcast-clips/YYYYMMDD/`

**Output:**
```
/tmp/podcast-clips/20260221/
├── Handleapp_hyperfokus_og_husfre.mp3 (28MB)
├── clip_0_laughter.mp3 (471KB, 30s)
├── clip_1_conversation.mp3 (470KB, 30s)
├── clip_2_reaction.mp3 (470KB, 30s)
└── daily-clips.log
```

**Cron-job:**
- Navn: `PODKAST – Daglig klipp-posting (Baarli og Benjamin)`
- Tid: 07:00 daglig
- Neste kjøring: Se `openclaw cron list`

---

## Telegram Bot - @Vev_kompis_bot (2026-03-05) ✅ FUNGERER

**Bot:** @Vev_kompis_bot (navn: Vev)  
**Token:** `8585778087:AAGNtnHCH3ki0fwu-9Hhmm_h37gku49SZQU`  
**Chat ID:** 6426967326 (N B)  
**Credentials:** `/root/.openclaw/workspace/.credentials/telegram-bot.env`  
**Status:** ✅ **FUNGERER** - To-veis kommunikasjon aktiv

### 🤖 Auto-Responder v2.1 (NY - 2026-03-05)

**Systemd Service:** `vev-telegram-responder.service`

**Funksjoner:**
- ✅ Kjører 24/7 som system-tjeneste
- ✅ Mottar meldinger hvert 2. sekund
- ✅ Svarer automatisk med **tekst OG stemme**
- ✅ **Kontekst-aware:** Husker siste 10 meldinger
- ✅ **Personlig:** Lærer dine interesser over tid
- ✅ **Emosjonell stemme:** Tilpasser tone (excited/happy/serious/curious)
- ✅ Restartes automatisk ved feil
- ✅ **Fikset:** Robust profil-håndtering

**Kommandoer:**
```bash
# Sjekk status
systemctl status vev-telegram-responder.service

# Restart
sudo systemctl restart vev-telegram-responder.service

# Se logger
sudo journalctl -u vev-telegram-responder.service -f
```

### Manuelle Scripts (hvis auto-responder er av)
```bash
# Sjekk nye meldinger
cd /root/.openclaw/workspace && python3 scripts/telegram-poll.py

# Svar på melding
/root/.openclaw/workspace/scripts/telegram-reply.sh "Ditt svar"

# Send melding
/root/.openclaw/workspace/scripts/telegram-send.sh "Melding"
```

### API-kall
```bash
# Hent bot-info
curl -s "https://api.telegram.org/bot8585778087:AAGNtnHCH3ki0fwu-9Hhmm_h37gku49SZQU/getMe"

# Send melding
curl -s -X POST "https://api.telegram.org/bot8585778087:AAGNtnHCH3ki0fwu-9Hhmm_h37gku49SZQU/sendMessage" \
  -d "chat_id=6426967326" \
  -d "text=Hei fra BaarliClaw!"

# Sjekk meldinger
curl -s "https://api.telegram.org/bot8585778087:AAGNtnHCH3ki0fwu-9Hhmm_h37gku49SZQU/getUpdates"
```

### 🎙️ Voice Chat / Talemeldinger v2.0 (NY 2026-03-05)
**Kommandoer:**
- `vev-telegram-voice` - Send talemelding
- `vev-emotional-voice` - Send med emosjonell tilpasning

**Bruk:**
```bash
# Send talemelding
vev-telegram-voice "Hei, dette er Vev som snakker!"

# Send med spesifikk emosjon
vev-emotional-voice "Dette er fantastisk!" excited
vev-emotional-voice "Dette er viktig..." serious

# Test med standardmelding
vev-telegram-voice --test
```

**Emosjoner:** excited, happy, serious, curious

### 🤖 Auto-Responder v2.0 (NY 2026-03-05)
**Service:** `vev-telegram-responder.service`

Kontinuerlig lytter og svarer på Telegram-meldinger med AI, historikk og emosjonell stemme.

**Status:**
```bash
# Sjekk status
systemctl status vev-telegram-responder.service

# Start/stop/restart
sudo systemctl start vev-telegram-responder.service
sudo systemctl stop vev-telegram-responder.service
sudo systemctl restart vev-telegram-responder.service

# Se logger
sudo journalctl -u vev-telegram-responder.service -f
tail -f /root/.openclaw/workspace/brain/logs/telegram-auto-responder.log
```

**Funksjonalitet v2.0:**
- ✅ **AI-baserte svar** - OpenClaw integrasjon
- ✅ **Samtale-historikk** - Husker siste 10 meldinger
- ✅ **Bruker-profiler** - Lærer interesser og preferanser
- ✅ **Emosjonell stemme** - Tilpasser tone automatisk
- ✅ Sjekker nye meldinger hvert 2. sekund
- ✅ Svarer med tekst OG stemme
- ✅ Logger all aktivitet
- ✅ Restartes automatisk ved feil

**Test:**
```bash
# Kjør test suite
vev-test-suite
```

**Teknisk:**
- **Stemme:** Sebastian (Norsk)
- **Modell:** ElevenFlash 2.5
- **Emosjoner:** excited, happy, serious, curious
- **Modell:** ElevenFlash 2.5
- **API:** ElevenLabs
- **API Key:** `0198de23418bce571b2a563958e510d23314d16c9e66fbe017423e9741418704`
- **Script:** `/root/.openclaw/workspace/scripts/vev-telegram-voice.py`

**Voice Chat i Mission Control:**
- URL: https://baarli.github.io/mission-control-live/
- Klikk "🎙️ Snakk med Vev" nederst til høyre
- Web Speech API for norsk talegjenkjenning
- ElevenLabs TTS for svar

### Husk
- Bot: @Vev_kompis_bot (Vev)
- Bruker: N B
- Chat ID: 6426967326
- Token: 8585778087:AAGNtnHCH3ki0fwu-9Hhmm_h37gku49SZQU

---

Add whatever helps you do your job. This is your cheat sheet.
