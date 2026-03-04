# Mission Control - Teknisk Spesifikasjon

## System Arkitektur

```
┌─────────────────────────────────────────────────────────────┐
│                        BRUKER                                │
│                      (Nettleser)                             │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   GITHUB PAGES                               │
│              (baarli.github.io)                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  index.html (HTML + CSS + JavaScript)               │   │
│  │  - Login med passord                                │   │
│  │  - Dashboard visning                                │   │
│  │  - CRUD operasjoner                                 │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS + REST API
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    SUPABASE                                  │
│           (kvniauxokdtmpvjtfnej.supabase.co)                 │
│  ┌─────────────────────┐  ┌─────────────────────────────┐   │
│  │  agenda_items       │  │  podcast_episodes           │   │
│  │  - id (uuid)        │  │  - id (uuid)                │   │
│  │  - tenant_id        │  │  - title                    │   │
│  │  - title            │  │  - published_at             │   │
│  │  - description      │  │  - duration                 │   │
│  │  - category         │  │  - podcast_name             │   │
│  │  - show_date        │  └─────────────────────────────┘   │
│  │  - link_url         │                                    │
│  │  - link_metadata    │                                    │
│  │  - notes            │                                    │
│  │  - order_index      │                                    │
│  │  - is_pinned        │                                    │
│  │  - created_by       │                                    │
│  └─────────────────────┘                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Dataflyt

### 1. Login
```
Bruker skriver passord → Sjekk mot hardkodet PASSWORD
                          → Lagre i localStorage
                          → Vis app
```

### 2. Hente Saker
```
Dashboard laster → Hent dagens dato
                 → Hent morgendagens dato
                 → Spørring 1: agenda_items?show_date=eq.{today}
                 → Spørring 2: agenda_items?show_date=eq.{tomorrow}
                 → Bruk den som har data
                 → Vis i UI
```

### 3. Legge til Sak
```
Bruker klikker "Legg til" → Prompt for tittel, kategori, lenke
                          → POST /agenda_items
                          → Oppdater visning
```

### 4. Slette Sak
```
Bruker klikker "Slett" → Confirm dialog
                       → DELETE /agenda_items?id=eq.{id}
                       → Oppdater visning
```

---

## API Spørringer

### Hent saker for dato
```http
GET /rest/v1/agenda_items?tenant_id=eq.{TENANT_ID}&show_date=eq.{DATE}&order=order_index.asc
Headers:
  apikey: {SUPABASE_KEY}
  Authorization: Bearer {SUPABASE_KEY}
```

### Legg til sak
```http
POST /rest/v1/agenda_items
Headers:
  apikey: {SUPABASE_KEY}
  Authorization: Bearer {SUPABASE_KEY}
  Content-Type: application/json
Body:
  {
    "tenant_id": "a0000000-0000-0000-0000-000000000001",
    "title": "Sak tittel",
    "category": "TALK",
    "show_date": "2026-03-05",
    "link_url": "https://...",
    "created_by": "10aa1508-6d52-490c-8ae5-fa3da9a152c4"
  }
```

### Slett sak
```http
DELETE /rest/v1/agenda_items?id=eq.{SAK_ID}
Headers:
  apikey: {SUPABASE_KEY}
  Authorization: Bearer {SUPABASE_KEY}
```

---

## Filstruktur

```
mission-control-gh-pages/
├── index.html          # Hovedfil (HTML + CSS + JS)
├── test.html           # Test/debug side
└── .git/               # Git repository

GitHub Repo:
baarli/mission-control-live
├── master branch → GitHub Pages
└── Settings → Pages → Source: master branch
```

---

## CSS Klasser

### Layout
- `.app` - Hovedapp container
- `.header` - Topp navigasjon
- `.container` - Innholdsområde
- `.section` - Side-seksjoner
- `.card` - Info-bokser

### Komponenter
- `.stat-card` - Statistikk-kort
- `.sak-item` - Sak i liste
- `.sak-number` - Nummer-badge
- `.sak-category` - Kategori-badge
- `.btn-*` - Knappe-varianter

### Kategori-farger
- `.cat-talk` - Lilla (#6366f1)
- `.cat-reality` - Oransje (#f59e0b)
- `.cat-kjendis` - Rosa (#ec4899)
- `.cat-film` - Blå (#3b82f6)
- `.cat-musikk` - Grønn (#10b981)
- `.cat-internasjonalt` - Lilla (#8b5cf6)

---

## JavaScript Funksjoner

### Auth
- `doLogin()` - Håndter login
- `doLogout()` - Håndter logout
- `showApp()` - Vis hovedapp

### Navigasjon
- `showSection(section)` - Bytt side

### Data
- `supabaseRequest(endpoint, options)` - API-kall
- `loadDashboard()` - Last dashboard
- `loadSaker()` - Last saksliste
- `loadPodcast()` - Last podcast
- `loadStats()` - Last statistikk

### CRUD
- `addNewSak()` - Legg til sak
- `deleteSak(id)` - Slett sak

### Verktøy
- `runMorningRoutine()` - Start Morning Routine
- `deleteOldSaker()` - Slett gamle saker
- `refreshAll()` - Oppdater alt
- `testConnection()` - Test Supabase-tilkobling

### Hjelpefunksjoner
- `getCategoryClass(cat)` - Map kategori til CSS-klasse
- `getWeekNumber(date)` - Beregn ukenummer
- `escapeHtml(text)` - Escape HTML-tegn

---

## Miljøvariabler/Konstanter

```javascript
// Autentisering
const PASSWORD = 'kloakontroll2026';

// Supabase
const SUPABASE_URL = 'https://kvniauxokdtmpvjtfnej.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...';

// Database
const TENANT_ID = 'a0000000-0000-0000-0000-000000000001';
const CREATED_BY = '10aa1508-6d52-490c-8ae5-fa3da9a152c4';
```

---

## GitHub Pages Deploy

### Automatisk
1. Push til master branch
2. GitHub Pages bygger automatisk (tar ~30 sekunder)
3. Tilgjengelig på https://baarli.github.io/mission-control-live/

### Manuell verifisering
```bash
curl -s https://baarli.github.io/mission-control-live/ | head -20
```

---

## Sikkerhetsvurderinger

### Akseptert risiko
1. **Passord i klartekst** - Hardkodet i JS (OK for intern verktøy)
2. **Anon key i frontend** - Begrenset til lese/skrive egne data
3. **Ingen CSRF-beskyttelse** - Stateless API

### Beskyttelser
1. **Row Level Security (RLS)** - Supabase nivå
2. **Tenant isolation** - Alle spørringer filtrert på tenant_id
3. **HTTPS only** - GitHub Pages + Supabase
4. **LocalStorage auth** - Enkel men effektiv for dette brukstilfellet

---

## Ytelse

### Mål
- Første innlasting: < 2 sekunder
- API-respons: < 500ms
- Auto-refresh: hvert 5. minutt

### Optimaliseringer
- Single-file applikasjon
- Ingen eksterne JS-rammeverk
- Lazy loading av seksjoner
- Caching av data i minnet

---

## Testing

### Manuell test-protokoll
1. Login med riktig passord → Skal fungere
2. Login med feil passord → Skal vise feil
3. Dashboard → Skal vise stats
4. Saksliste → Skal vise saker
5. Legg til sak → Skal opprette i DB
6. Slett sak → Skal fjerne fra DB
7. Test tilkobling → Skal vise suksess
8. Logg ut → Skal gå til login

### Debug
- Åpne browser console (F12)
- Se etter [INFO], [SUCCESS], [ERROR] meldinger
- Sjekk Network tab for API-kall
