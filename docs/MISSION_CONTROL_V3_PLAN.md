# 🎛️ MISSION CONTROL V3 - TOTAL KONTROLLPANEL

## Visjon
Et enkelt, visuelt kontrollpanel hvor du kan:
- ✅ Se status på ALLE systemer på ett blikk
- 🔧 Starte/stoppe automasjoner med ett klikk
- 📊 Konfigurere meg (BaarliClaw) uten koding
- 🔔 Få varsler om det som trenger oppmerksomhet
- 🎛️ Justere alle innstillinger via GUI

---

## 📋 Systemer å Integrere

### 1. **NRJ Morgen Økosystem**
- [x] Sakslista (agenda_items i Supabase)
- [x] Dashboard stats (Nielsen + Podtoppen)
- [x] Morning routine (nyhetssøk)
- [ ] E-post sending (showprepp)
- [ ] Konkurrent-radar
- [ ] Trending Pulse (midtdag)

### 2. **Podkast Systemer**
- [x] Baarli og Benjamin går i terapi
- [x] NRJ Morgen Podkast
- [x] Daglig klipp-henting
- [ ] Auto-posting til sosiale medier
- [ ] Podkast-statistikk

### 3. **BaarliClaw Agent System**
- [x] Auto-Exec Enforcer
- [x] Autonomous Mode
- [x] Pre-flight checklist
- [x] Session End Capture
- [ ] Skills management
- [ ] Memory management
- [ ] Learning capture

### 4. **Cron/Automations**
- [x] 20+ aktive cron-jobs
- [ ] Enable/disable via GUI
- [ ] Manuell trigger
- [ ] Status monitoring
- [ ] Error tracking

### 5. **Git Repositories**
- [ ] baarliogbenjamin (podkast-plattform)
- [ ] nrjmorgen-ui (dashboard)
- [ ] openclaw-workspace (dette repoet)
- [ ] Deploy status
- [ ] Commit history
- [ ] Branch management

### 6. **Supabase Database**
- [ ] agenda_items (sakslista)
- [ ] nielsen_weekly_metrics
- [ ] podtoppen_weekly_data
- [ ] profiles
- [ ] Real-time subscriptions

### 7. **Netlify Deployments**
- [x] Mission Control dashboard
- [ ] Deploy history
- [ ] Build logs
- [ ] Rollback capability

### 8. **System Health**
- [x] Disk usage
- [x] Memory usage
- [x] CPU usage
- [x] API quotas
- [x] Error logs

---

## 🎨 Dashboard Seksjoner

### Hovedpanel (Overview)
```
┌─────────────────────────────────────────────────────────────┐
│  🎛️ MISSION CONTROL - Total System Status                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ 🟢 NRJ   │ │ 🟢 Pod   │ │ 🟢 Agent │ │ 🟢 Cron  │       │
│  │   15     │ │   2      │ │   Active │ │   18/20  │       │
│  │  saker   │ │ podkaster│ │          │ │  running │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│                                                             │
│  System Health: 🟢 All systems operational                 │
│  Last Update: 2 minutes ago                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### NRJ Morgen Kontroll
- Sakslista: Se, rediger, slett, legg til saker
- Dashboard: Oppdater stats, se historikk
- Morning Routine: Kjør manuelt, se schedule
- Konkurrent-radar: Se siste analyse

### Podkast Kontroll
- Episode-liste med spilling
- Klipp-status (generert/postet)
- Statistikk (nedlastinger, rangering)
- Auto-posting innstillinger

### Agent Konfigurasjon
```
┌─────────────────────────────────────────────────────────────┐
│  🤖 BaarliClaw Konfigurasjon                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [x] Auto-Exec Enforcer    [Rediger regler]                │
│  [x] Autonomous Mode       [Rediger schedule]              │
│  [x] Pre-flight Checklist  [Rediger steg]                  │
│  [x] Session End Capture   [Rediger intervall]             │
│  [x] Memory Validator      [Se logs]                       │
│                                                             │
│  Skills: 5 aktive  [Administrer skills]                    │
│  Scripts: 74 tilgjengelige  [Se liste]                     │
│                                                             │
│  [🔄 Restart Agent]  [📊 Se logs]  [⚙️ Avansert]           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Cron Job Manager
```
┌─────────────────────────────────────────────────────────────┐
│  ⏰ Automations (20 jobs)                                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🟢 NRJ Morgen – Konsolidert Morgen-Rutine (04:50)         │
│     Neste: I morgen 04:50  [Kjør nå] [Rediger] [Disable]   │
│                                                             │
│  🟢 Podkast – Daglig klipp (07:00)                         │
│     Neste: I dag 07:00  [Kjør nå] [Rediger] [Disable]      │
│                                                             │
│  🔴 NRJ MORGEN – Morgenbriefing (04:30)                    │
│     Status: Disabled  [Enable] [Rediger]                   │
│                                                             │
│  [+ Legg til ny automation]                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Git & Deploy
```
┌─────────────────────────────────────────────────────────────┐
│  🌿 Repositories                                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  baarliogbenjamin                                          │
│  🟢 main  12 commits ahead  [Deploy] [View] [Logs]         │
│  Sist: "Add Docker support" (2 timer siden)                │
│                                                             │
│  nrjmorgen-ui                                              │
│  🟢 main  Up to date  [View]                               │
│                                                             │
│  openclaw-workspace                                        │
│  🟢 main  5 uncommitted changes  [Commit] [View]           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Database Browser
- Supabase tabeller
- Real-time data
- Query builder
- Export/Import

### System Monitor
```
┌─────────────────────────────────────────────────────────────┐
│  📊 System Resources                                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Disk: ████████░░ 78% (45GB / 60GB)                        │
│  RAM:  ██████░░░░ 45% (3.2GB / 8GB)                        │
│  CPU:  ██░░░░░░░░ 12%                                      │
│                                                             │
│  API Quotas:                                               │
│  - Brave Search: 1500/2000 (resets in 12h)                │
│  - Supabase: Unlimited                                     │
│  - Netlify: 100/300 builds (resets in 20d)                │
│                                                             │
│  [🧹 Rens cache]  [📥 Export logs]                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Konfigurerbare Innstillinger

### NRJ Morgen
```yaml
morning_routine:
  enabled: true
  schedule: "0 6 * * 1-5"  # Man-fre 06:00
  sources:
    - VG Rampelys
    - TV2 Underholdning
    - Nettavisen Kjendis
    - Dagbladet Kjendis
  target_sak_count: 15
  auto_insert_to_supabase: true
  send_email_report: true
  email_recipients:
    - niklasbaarli@gmail.com
```

### Podkast
```yaml
podcast:
  baarli_og_benjamin:
    enabled: true
    rss_url: "https://rss.podplaystudio.com/4035.xml"
    auto_download: true
    clip_generation:
      enabled: true
      schedule: "0 7 * * *"
      clip_count: 3
      clip_duration: 30
    social_posting:
      enabled: false  # Krever API keys
      platforms:
        - instagram
        - tiktok
```

### BaarliClaw Agent
```yaml
agent:
  auto_exec:
    enabled: true
    run_on_startup: true
  autonomous_mode:
    enabled: true
    health_check_interval: 3600
  pre_flight:
    enabled: true
    mandatory: true
  session_end:
    enabled: true
    capture_learning: true
  memory:
    validation_interval: 86400
    auto_update: true
```

---

## 🔔 Varslingssystem

### Kritiske varsler (Push + E-post)
- Cron-jobs feiler 3x på rad
- Disk usage >90%
- API quotas <10%
- Git deploy feiler
- Supabase connection lost

### Daglige oppsummeringer
- Morning briefing kl 06:00
- Podkast klipp kl 08:00
- System health kl 23:00

### Ukentlige rapporter
- Søndag 20:00: Strategi-rapport
- Søndag 21:00: Podkast-vekst
- Søndag 23:00: Vedlikehold

---

## 🛠️ Teknisk Implementasjon

### Backend API (Python)
```python
# Endpoints needed:
GET  /api/v3/status              # Total system status
GET  /api/v3/nrj/saker           # Sakslista
POST /api/v3/nrj/saker           # Legg til sak
GET  /api/v3/nrj/stats           # Nielsen + Podtoppen
POST /api/v3/nrj/update          # Oppdater stats
GET  /api/v3/podcast/episodes    # Podkast-episoder
GET  /api/v3/podcast/clips       # Genererte klipp
GET  /api/v3/cron/jobs           # Alle cron-jobs
POST /api/v3/cron/jobs/{id}/run  # Kjør manuelt
POST /api/v3/cron/jobs/{id}/toggle # Enable/disable
GET  /api/v3/agent/config        # Agent config
POST /api/v3/agent/config        # Oppdater config
GET  /api/v3/git/repos           # Git repositories
POST /api/v3/git/deploy          # Deploy
GET  /api/v3/system/resources    # CPU/RAM/Disk
GET  /api/v3/system/logs         # System logs
```

### Frontend (React/Vue)
- Real-time updates via WebSocket
- Dark mode (selvfølgelig)
- Responsive design
- Drag-and-drop for sakslista
- Inline editing

### Database
- Supabase for persistent storage
- Redis for caching (optional)
- Local JSON for config

---

## 📅 Utviklingsplan

### Fase 1: Core Dashboard (1-2 dager)
- [ ] Forbedre eksisterende Mission Control
- [ ] Legge til alle system-statuser
- [ ] Cron job manager
- [ ] Basic config editing

### Fase 2: NRJ & Podkast (2-3 dager)
- [ ] Full sakslista-kontroll
- [ ] Podkast episode manager
- [ ] Statistikk-visualisering
- [ ] Auto-routine kontroll

### Fase 3: Agent Config (2 dager)
- [ ] GUI for agent-innstillinger
- [ ] Skills manager
- [ ] Memory browser
- [ ] Script runner

### Fase 4: Avansert (3-4 dager)
- [ ] Git integration
- [ ] Database browser
- [ ] Advanced monitoring
- [ ] Varslingssystem

---

## 🎯 MVP - Minimum Viable Product

For å dekke ditt behov "uten at du må bry deg":

1. **One-glance status** - Alt grønt/rødt
2. **Start/stop automasjoner** - Med ett klikk
3. **Rediger config** - Via GUI, ikke kode
4. **Se logs** - Filtrert og forståelig
5. **Manuell trigger** - Kjør rutiner på demand

Dette kan vi bygge på 2-3 dager!

---

## 💡 Neste Steg

Vil du at jeg skal:
1. **Starte med MVP** - Grunnleggende kontrollpanel
2. **Gå for Total Kontroll** - Alt på en gang
3. **Fokusere på én del** - F.eks. bare NRJ eller bare Agent-config

Hva foretrekker du?
