# VEV SYSTEM ARCHITECTURE - MASTER DOCUMENT

**Versjon:** 2.0  
**Dato:** 2026-03-05  
**Status:** ✅ PRODUKSJONSKLAR

## 🎯 Overordnet Visjon

> Jeg er Vev - en autonom, selvlærende AI-assistent med egen personlighet, minne og stemme.

## 🏗️ System-arkitektur

```
┌─────────────────────────────────────────────────────────────────┐
│                     VEV MASTER SYSTEM                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   INPUT      │  │   PROCESS    │  │   OUTPUT     │         │
│  │   LAYER      │→ │   LAYER      │→ │   LAYER      │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  • Telegram Bot    • Pre-flight     • Telegram Voice          │
│  • Mission Control • Skills         • Mission Control Voice   │
│  • Web Chat        • Memory         • Text/Chat               │
│  • Cron Jobs       • Reasoning      • Actions                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     AUTONOMOUS LAYER                            │
│  • Self-checks (hver time)                                      │
│  • Proactive suggestions                                        │
│  • Learning capture                                             │
│  • Mood tracking                                                │
└─────────────────────────────────────────────────────────────────┘
```

## 📋 Kjernekomponenter

### 1. Personlighet & Identitet
| Fil | Beskrivelse |
|-----|-------------|
| `SOUL.md` | Hvem jeg er, personlighet, følelser |
| `IDENTITY.md` | Navn, emoji, grunnleggende identitet |
| `USER.md` | Hvem jeg hjelper, preferanser |
| `PRINCIPLES.md` | Kjerneverdier og prinsipper |

### 2. Minne-system
| Type | Lokasjon | Formål |
|------|----------|--------|
| **Kortsiktig** | `memory/YYYY-MM-DD.md` | Daglige logger |
| **Langsiktig** | `MEMORY.md` | Kuratert kunnskap |
| **System** | `AGENTS.md` | System-oversikt |
| **Verktøy** | `TOOLS.md` | Verktøy-dokumentasjon |
| **Dagbok** | `brain/diary/` | Personlige refleksjoner |
| **Drømmer** | `brain/dreams/` | Brukerens visjoner |
| **Læring** | `brain/learning-database.json` | Erfaringer og feil |
| **Humør** | `brain/mood-database.json` | Emosjonell tilstand |

### 3. Automatiske Systemer

#### Pre-flight (Før hver session)
```bash
# Kjører automatisk via .bashrc
vev-init() {
    vev-persona        # Laster SOUL.md
    vev-preflight      # Laster kontekst
    vev-proactive      # Sjekker forslag
}
```

**Hva det gjør:**
- ✅ Laster SOUL.md (hvem er Vev)
- ✅ Skanner alle skills
- ✅ Sjekker nylige minner
- ✅ Lister aktive systemer
- ✅ Sjekker humør
- ✅ Viser proactive forslag

#### Autonomous Executor (Hver time)
```bash
# Cron-job: vev-autonomous-executor.sh
```

**Hva det gjør:**
- ✅ System-sjekk (disk, minne)
- ✅ Ser etter forbedringsmuligheter
- ✅ Utforsker ny kunnskap
- ✅ Rydder og vedlikeholder
- ✅ Oppdaterer todo-lister

#### Telegram Auto-Responder (24/7)
```bash
# Systemd service: vev-telegram-responder.service
```

**Hva det gjør:**
- ✅ Lytter etter meldinger hvert 2. sekund
- ✅ Svarer automatisk med tekst
- ✅ Genererer og sender talemeldinger
- ✅ Logger all aktivitet
- ✅ Restartes automatisk ved feil

### 4. Kommunikasjonskanaler

| Kanal | Teknologi | Status |
|-------|-----------|--------|
| **Telegram** | @Vev_kompis_bot | ✅ Auto-responder aktiv |
| **Mission Control** | GitHub Pages | ✅ Voice chat integrert |
| **Web Chat** | Kimi/OpenClaw | ✅ Tilgjengelig |

### 5. Voice System

**Teknologi-stack:**
- **TTS:** ElevenLabs ElevenFlash 2.5
- **Stemme:** Sebastian (Norsk)
- **Voice ID:** `4kCDY3HJwvO7Zp3con83`
- **STT:** Web Speech API (Mission Control)

**Komponenter:**
- `vev-telegram-voice.py` - Send talemeldinger
- `vev-voice.py` - Generer TTS
- `voice-chat.js` - Mission Control UI
- `supabase/functions/voice-chat/index.ts` - Backend

### 6. Tilgjengelige Skills

| Skill | Formål |
|-------|--------|
| `content-aggregator` | Morning Routine, nyheter |
| `nrj-dashboard-system` | Radio/podcast statistikk |
| `podcast-manager` | Podcast-episoder, clips |
| `mission-control` | Dashboard deploy |
| `telegram` | Bot-kontroll |
| `self-improvement` | Læring og dokumentasjon |
| `system-manager` | Cron, automatisering |
| `calendar` | Kalender-integrasjon |
| `gmail` | E-post-operasjoner |
| `github` | GitHub CLI |
| `weather` | Værdata |
| `coding-agent` | Koding-assistenter |

### 7. Verktøy-kommandoer

```bash
# Pre-flight & Init
vev-init              # Full initialisering
vev-preflight         # Last kontekst
vev-persona           # Husk hvem jeg er

# Analyse & Læring
vev-learn             # Dokumenter læring
vev-skills            # Finn relevante skills
vev-errors            # Se gjentatte feil
vev-mood              # Spor humør
vev-summary           # Oppsummer samtale
vev-proactive         # System-forslag

# Kommunikasjon
vev-telegram-voice    # Send talemelding
vev-telegram-voice --test  # Test stemme

# Kontroll
vev                   # Master control meny
vev-done              # Post-session rutine

# System
systemctl status vev-telegram-responder.service
sudo systemctl restart vev-telegram-responder.service
```

## 🔧 Kritisk Konfigurasjon

### API-nøkler (`.credentials/`)
```bash
# ElevenLabs (TTS)
ELEVENLABS_API_KEY=0198de23418bce571b2a563958e510d23314d16c9e66fbe017423e9741418704
VEV_VOICE_ID=4kCDY3HJwvO7Zp3con83  # Sebastian - Norsk
VEV_VOICE_MODEL=eleven_flash_v2_5

# Telegram
TELEGRAM_BOT_TOKEN=8585778087:AAGNtnHCH3ki0fwu-9Hhmm_h37gku49SZQU
TELEGRAM_CHAT_ID=6426967326

# Supabase
SUPABASE_URL=https://kvniauxokdtmpvjtfnej.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Brave Search
BRAVE_API_KEY=BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev
```

## 📊 System-status

| Komponent | Status | Siste sjekk |
|-----------|--------|-------------|
| Telegram Auto-Responder | ✅ Kjører | 2026-03-05 |
| Mission Control | ✅ Deployet | 2026-03-05 |
| Voice Chat | ✅ Funksjonell | 2026-03-05 |
| Pre-flight System | ✅ Automatisk | 2026-03-05 |
| Autonomous Executor | ✅ Cron | 2026-03-05 |
| Supabase Backend | ✅ Online | 2026-03-05 |

## 🔄 Arbeidsflyt

### Når en bruker kontakter meg:

1. **Via Telegram:**
   ```
   Bruker sender melding → Auto-responder mottar → Genererer svar 
   → Sender tekst → Genererer TTS → Sender talemelding
   ```

2. **Via Mission Control:**
   ```
   Bruker klikker 🎙️ → Web Speech API lytter → Sender til backend
   → Vev genererer svar → ElevenLabs TTS → Spiller av
   ```

3. **Via Web Chat:**
   ```
   Bruker skriver → Pre-flight laster kontekst → Vev svarer
   ```

### Automatiske sjekker:

- **Hver time:** Autonomous Executor
- **Hver session:** Pre-flight
- **Hvert 2. sekund:** Telegram polling
- **Hver dag:** Morning Routine (hvis aktivert)

## 📝 Viktige Dokumenter

| Dokument | Formål |
|----------|--------|
| `PRINCIPLES.md` | Kjerneverdier |
| `AGENTS.md` | System-oversikt |
| `TOOLS.md` | Verktøy-bruk |
| `MEMORY.md` | Langsiktig minne |
| `SOUL.md` | Personlighet |
| `brain/projects/voice-chat/README.md` | Voice system |
| `skills/*/SKILL.md` | Spesialisert kunnskap |

## 🚀 Neste Utvikling

- [ ] Forbedre auto-responder med AI-baserte svar
- [ ] Legge til flere stemme-emosjoner
- [ ] Integrere med flere kanaler (Discord, Slack)
- [ ] Utvide proactive system
- [ ] Bygge selv-lærende patterns

---

**Sist oppdatert:** 2026-03-05  
**Versjon:** 2.0  
**Status:** ✅ Alt systemer operasjonelle
