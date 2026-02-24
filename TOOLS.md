# TOOLS.md - Local Notes

## 🧠 HUSK ALLTID (Kritisk informasjon)

### Mission Control Dashboard
- **URL:** https://creative-muffin-dcf3a0.netlify.app/
- **Passord:** kloakontroll2026
- **Netlify Site ID:** `834576a6-da2b-4412-9433-315f6437508a`
- **Token:** `nfp_8B3dDBwZS9W1GSHTUy3am4fia6iZmF6b0092`
- **Deploy:** `cd mission-control/public && netlify deploy --prod`

### Morning Routine v2.1 (Oppdatert 2026-02-24)

**Konfigurasjon:**
- **Antall saker:** 15 per dag
- **Kategorier:** 5 (maks 3 saker per kategori)
  - Reality TV: Farmen, Paradise Hotel, Kompani Lauritzen, Love Island
  - Kjendis Drama: brudd, raser, avsløringer
  - Film & TV: premierer, rød løper
  - Musikk: Spellemannprisen, VG-lista, P3 Gull
  - Internasjonalt: Daily Mail, TMZ, E! Online, People
- **Alder:** Maks 48 timer (freshness=pd)
- **Titler:** OpenAI-generert, maks 7 ord

**Script:**
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

Add whatever helps you do your job. This is your cheat sheet.
