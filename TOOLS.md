# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

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

## NRJ Morgen - Viktige Krav

### Saksliste-data (2026-02-21):
**Hver sak MÅ inneholde:**
- `link_url`: Direkte lenke til original artikkel
- `notes`: Oppsummering på formatet "[Første setning]\n\nKilde: [Kilde]"

**Hvordan det fungerer:**
1. `brave-news-search.py` → `create_summary()` lager oppsummering
2. Artikler lagres med `url` og `summary` i JSON
3. `integrated-morning-routine.sh` → Inserter til Supabase med `link_url` og `notes`

**Dokumentasjon:** `.config/REQUIREMENT_LINK_AND_SUMMARY.md`

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

Add whatever helps you do your job. This is your cheat sheet.
