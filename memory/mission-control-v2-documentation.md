# Mission Control v2.0 - Komplett Dokumentasjon

**Opprettet:** 2026-03-04  
**Sist oppdatert:** 2026-03-04  
**Versjon:** 2.0

---

## 📋 Oversikt

Mission Control er et dashboard for NRJ Morgen som gir oversikt over:
- Radio-statistikk (Nielsen)
- Podcast-ranking (Podtoppen)
- Saksliste for sendinger
- Systemstatus

---

## 🌐 URL-er og Tilgang

| Ressurs | URL |
|---------|-----|
| **Live Dashboard** | https://baarli.github.io/mission-control-live/ |
| **GitHub Repo** | https://github.com/baarli/mission-control-live |
| **Passord** | `kloakontroll2026` |

---

## 🗄️ Database-arkitektur

### Tabeller brukt av Mission Control

#### 1. `nielsen_weekly_metrics` - Radio-statistikk
```sql
CREATE TABLE nielsen_weekly_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    channel TEXT NOT NULL,           -- 'NRJ'
    week_number INTEGER NOT NULL,    -- 1-53
    year INTEGER NOT NULL,           -- 2026
    value INTEGER NOT NULL,          -- 69000 (daglige lyttere)
    created_at TIMESTAMP DEFAULT now()
);
```

**Eksempel data:**
```json
{
  "channel": "NRJ",
  "week_number": 9,
  "year": 2026,
  "value": 69000
}
```

#### 2. `podtoppen_weekly_data` - Podcast-statistikk
```sql
CREATE TABLE podtoppen_weekly_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    podcast_title TEXT NOT NULL,     -- 'NRJ Morgen Podkast'
    week_number INTEGER NOT NULL,    -- 1-53
    year INTEGER NOT NULL,           -- 2026
    rank INTEGER NOT NULL,           -- 38
    unique_units INTEGER,            -- Unike lyttere
    downloaded_streamed INTEGER,     -- Totale downloads
    created_at TIMESTAMP DEFAULT now()
);
```

**Eksempel data:**
```json
{
  "podcast_title": "NRJ Morgen Podkast",
  "week_number": 8,
  "year": 2026,
  "rank": 38,
  "unique_units": 12345,
  "downloaded_streamed": 67890
}
```

#### 3. `agenda_items` - Saksliste
```sql
CREATE TABLE agenda_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,                   -- 'REALITY_TV', 'KJENDIS_DRAMA', etc.
    show_date DATE NOT NULL,         -- YYYY-MM-DD
    link_url TEXT,
    notes TEXT,
    order_index INTEGER DEFAULT 0,
    created_by UUID,
    created_at TIMESTAMP DEFAULT now()
);
```

### 4. `brave_searches` - Søkehistorikk (NY!)
```sql
CREATE TABLE brave_searches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    query TEXT NOT NULL,
    category TEXT,
    freshness TEXT,
    results_count INTEGER,
    created_at TIMESTAMP DEFAULT now()
);
```

---

## 🔌 API-endepunkter

### Brave News API (NY!)
```javascript
// Søk etter nyheter
GET https://api.search.brave.com/res/v1/news/search

Headers:
  X-Subscription-Token: BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev
  Accept: application/json

Query Parameters:
  q: søkeord
  count: 20 (antall resultater)
  search_lang: nb (norsk)
  country: no (Norge)
  freshness: pd (past day) eller pw (past week)

Response:
{
  "results": [
    {
      "title": "Artikkel tittel",
      "description": "Beskrivelse...",
      "url": "https://...",
      "source": "vg.no",
      "published": "2 hours ago"
    }
  ]
}
```

### Underholdningsscore Algoritme (NY!)
```javascript
function calculateScore(title, description) {
  const text = (title + ' ' + description).toLowerCase();
  let score = 50; // Baseline
  
  // Positive faktorer (+10 hver)
  const positive = [
    'brudd', 'krangel', 'drama', 'skandale', 'avsløring',
    'hemmelig', 'kontrovers', 'konflikt', 'exit', 'overraskelse',
    'pinlig', 'sterkt sitat', 'tårer', 'raser', 'sjokk', 'kaos',
    'kjendis', 'reality', 'farmen', 'paradise', 'kompani'
  ];
  
  // Negative faktorer (-20 hver)
  const negative = [
    'sport', 'fotball', 'håndball', 'ski',
    'politikk', 'økonomi', 'skatt', 'lovforslag',
    'krig', 'død', 'ulykke', 'tragedie'
  ];
  
  return Math.min(100, Math.max(0, score));
}
```

### Radio-statistikk
```javascript
// Hent siste radio-statistikk
GET /rest/v1/nielsen_weekly_metrics?channel=eq.NRJ&order=created_at.desc&limit=1

Headers:
  apikey: <SUPABASE_KEY>
  Authorization: Bearer <SUPABASE_KEY>

Response:
[{
  "id": "...",
  "channel": "NRJ",
  "week_number": 9,
  "year": 2026,
  "value": 69000,
  "created_at": "2026-03-01T10:00:00Z"
}]
```

### Podcast-statistikk
```javascript
// Hent siste podcast-ranking
GET /rest/v1/podtoppen_weekly_data?podcast_title=eq.NRJ%20Morgen%20Podkast&order=created_at.desc&limit=1

Response:
[{
  "id": "...",
  "podcast_title": "NRJ Morgen Podkast",
  "week_number": 8,
  "year": 2026,
  "rank": 38,
  "unique_units": 12345,
  "downloaded_streamed": 67890
}]
```

### Saksliste
```javascript
// Hent saker for spesifikk dato
GET /rest/v1/agenda_items?tenant_id=eq.<TENANT_ID>&show_date=eq.2026-03-05&order=order_index.asc

Response:
[{
  "id": "...",
  "title": "Farmen-premiere",
  "category": "REALITY_TV",
  "show_date": "2026-03-05",
  "order_index": 1
}]
```

---

## 🔐 Autentisering og Sikkerhet

### Supabase Service Key
```javascript
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE';
```

### RLS (Row Level Security)
- **Problem:** Anon-key blokkeres av RLS-policyer
- **Løsning:** Bruk service_role key som bypasser RLS
- **Risiko:** Service key har full tilgang - må beskyttes!

### Dashboard Passord
- Passord: `kloakontroll2026`
- Lagres i localStorage: `localStorage.setItem('mc_auth', 'true')`
- Ingen server-side validering - kun client-side

---

## 📁 Filstruktur

```
mission-control-gh-pages/
├── index.html          # ENKELTFIL - All kode her
├── app.js              # Separat JS (ikke i bruk)
├── test.html           # Test/debug side
└── .git/               # Git repo
```

### Viktig: GitHub Pages begrensning
- **KUN statiske filer** (HTML/CSS/JS)
- **Ingen server-side kode** (PHP, Node, etc.)
- **Alt må være i én HTML-fil** for enkelhet
- **Ingen byggeprosess** - direkte redigering

---

## 🚀 Deploy-prosess

### Steg-for-steg

1. **Rediger filen lokalt:**
```bash
cd /root/.openclaw/workspace/mission-control-gh-pages
# Rediger index.html
```

2. **Commit endringer:**
```bash
git add index.html
git commit -m "Beskriv endringene"
```

3. **Push til GitHub:**
```bash
git push origin master
```

4. **Vent på deploy:**
- GitHub Pages bygger automatisk
- Tar 1-2 minutter
- Sjekk: https://baarli.github.io/mission-control-live/

### Force refresh (hvis cache problemer)
```
https://baarli.github.io/mission-control-live/?nocache=1
```

---

## 🎨 UI-komponenter

### Seksjoner
1. **Dashboard** - Oversikt med statistikk
2. **Saksliste** - Vis/slett saker med dato-filter
3. **Statistikk** - Historikk for radio og podcast

### Stat-kort
```html
<div class="stat">
  <div class="val" id="dash-radio">69.0k</div>
  <div class="lbl">Radio lyttere</div>
</div>
```

### Dato-velger
```html
<input type="date" id="saksliste-date" onchange="loadSaker()">
```

---

## ⚙️ Konfigurasjon

### JavaScript konstanter
```javascript
const PASSWORD = 'kloakontroll2026';
const SUPABASE_URL = 'https://kvniauxokdtmpvjtfnej.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...';
const TENANT_ID = 'a0000000-0000-0000-0000-000000000001';
const CREATED_BY = '10aa1508-6d52-490c-8ae5-fa3da9a152c4';
```

### Auto-refresh
```javascript
setInterval(() => {
  if (document.getElementById('app').style.display === 'block') {
    loadDashboard();
  }
}, 300000); // 5 minutter
```

---

## 🐛 Feilsøking

### Problem: "-" vises i stedet for tall
**Årsak:** API-kallet feiler eller returnerer tom liste  
**Løsning:** Sjekk browser console for feilmeldinger

### Problem: "Feil passord"
**Årsak:** Passordet er feil eller localStorage er korrupt  
**Løsning:** 
1. Sjekk at passord er `kloakontroll2026`
2. Clear localStorage: `localStorage.clear()`
3. Refresh siden

### Problem: Endringer vises ikke etter deploy
**Årsak:** GitHub Pages cache  
**Løsning:** 
1. Vent 2-5 minutter
2. Bruk `?nocache=1` parameter
3. Hard refresh: Ctrl+Shift+R

---

## 📊 Dataflyt

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   GitHub Pages  │────▶│   Supabase API  │────▶│   PostgreSQL    │
│   (Frontend)    │◄────│   (REST)        │◄────│   (Database)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │
        ▼
┌─────────────────┐
│  localStorage   │
│  (Auth state)   │
└─────────────────┘
```

---

## 🔧 Vedlikehold

### Regelmessige oppgaver
- [ ] Sjekk at data vises korrekt
- [ ] Verifiser at dato-velger fungerer
- [ ] Test login/logout
- [ ] Sjekk GitHub Pages status

### Overvåking
- Dashboard laster automatisk hvert 5. minutt
- Feil vises i rød alert-boks
- Sjekk browser console for JS-feil

---

## 📝 Endringslogg

### v2.0 (2026-03-04)
- ✅ Fikset radio-statistikk (bruker nielsen_weekly_metrics)
- ✅ Fikset podcast-statistikk (bruker podtoppen_weekly_data)
- ✅ La til dato-velger for saksliste
- ✅ Byttet til service_role key (bypass RLS)
- ✅ Forenklet UI til én HTML-fil
- ✅ Fjernet ubrukte seksjoner

### v1.0 (2026-03-03)
- 🎉 Første versjon
- Dashboard med grunnleggende statistikk
- Saksliste-visning
- Login-funksjonalitet

---

## 🔗 Relatert dokumentasjon

- **MEMORY.md** - Hovedminne med oversikt
- **SKILL.md** - Hvis dette blir en skill
- **GitHub Repo** - https://github.com/baarli/mission-control-live

---

## 👨‍💻 Utvikler-notater

**Husk:**
1. Alltid bruk service_role key for Supabase
2. Test i browser før push
3. Sjekk at dato-format er YYYY-MM-DD
4. Radio-data er i `nielsen_weekly_metrics`, IKKE `agenda_items`
5. Podcast-data er i `podtoppen_weekly_data`, IKKE `agenda_items`

**Forbedringsmuligheter:**
- [ ] Legge til Brave News API-søk
- [ ] Legge til mulighet for å redigere saker
- [ ] Legge til graf/historikk-visning
- [ ] Legge til eksport-funksjon
