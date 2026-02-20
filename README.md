# NRJ Morgen - Komplett Systemdokumentasjon

## 🎙️ Oversikt

Automatisert redaksjonelt system for NRJ Morgen (norsk morgenradio på P4).

---

## 📁 Repositories

| Repo | URL | Beskrivelse |
|------|-----|-------------|
| **UI** | https://github.com/baarli/nrjmorgen-a32b6810 | React/Vite frontend |
| **Workspace** | https://github.com/baarli/nrj-morgen-workspace | Scripts & skills |

---

## 🚀 Funksjonalitet

### 1. Automatisk Nyhetsinnhenting
- **Brave Search API** - Primær kilde for norske kjendisnyheter
- **AI Tittel-generering** - GPT-4o-mini for konsise titler
- **10 saker hver morgen** - Fra VG, DB, TV2, NRK, Nettavisen

### 2. Video-til-Lyd Pipeline (NY!)
- **Manuell URL-innlegging** - Via dashboard UI
- **Automatisk prosessering** - yt-dlp → ffmpeg → whisper
- **Sitat-utvelgelse** - AI finner beste lydklipp
- **Content-hub integrasjon** - Lydklipp tilgjengelig i studio

### 3. Morgenrutine (Cron)
```
04:50 - Søk etter nyheter (Brave API)
04:52 - Generer AI-titler
04:55 - Insert i Supabase
04:58 - Prosesser videoer
05:00 - Send showprepp (e-post)
```

### 4. Dashboard (nrjmorgen.com)
- **Saksliste** - Drag & drop, pinning, notater
- **Video Input** - "Legg til video" på hver sak
- **AI Intro-generator** - Automatiske radiointroer
- **Content-hub** - Lyd, video, bilder

---

## 🛠️ Teknisk Stack

| Komponent | Teknologi |
|-----------|-----------|
| Frontend | React + Vite + TypeScript |
| Backend | Supabase (PostgreSQL + Edge Functions) |
| AI | OpenAI GPT-4o-mini |
| Søk | Brave Search API |
| Video | yt-dlp + ffmpeg + whisper |
| Hosting | Supabase + GitHub Pages |

---

## 📋 Miljøvariabler

```bash
# Supabase
SUPABASE_URL=https://kvniauxokdtmpvjtfnej.supabase.co
SUPABASE_SERVICE_KEY=...
SUPABASE_ANON_KEY=...

# APIs
BRAVE_API_KEY=...
OPENAI_API_KEY=...
NEWSAPI_KEY=...

# E-post
GMAIL_USER=...
GMAIL_APP_PASSWORD=...
```

---

## 🚀 Deployment

### 1. Supabase Edge Functions
```bash
cd nrjmorgen-ui
./scripts/deploy-functions.sh
```

### 2. Frontend
```bash
cd nrjmorgen-ui
npm run build
# Deploy til GitHub Pages/Supabase
```

### 3. Cron-jobb
```bash
# På server
openclaw cron list  # Vis alle jobber
openclaw cron runs  # Kjør manuelt
```

---

## 📊 Status

| Komponent | Status |
|-----------|--------|
| Nyhetsinnhenting | ✅ Produksjon |
| AI-titler | ✅ Produksjon |
| Video-til-lyd | 🧪 Testing |
| Dashboard UI | ✅ Produksjon |
| E-post showprepp | ✅ Produksjon |

---

## 🔮 Neste steg

1. **Test video-pipeline** med ekte videoer
2. **API-avtaler** med VG/TV2/NRK for direkte tilgang
3. **Automatisk publisering** til sosiale medier
4. **Podcast-generering** fra sendinger

---

*Sist oppdatert: 21. februar 2026*
*Av: Kimi Claw* 🤖
