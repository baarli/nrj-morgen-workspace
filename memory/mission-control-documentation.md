# Mission Control - System Dokumentasjon

## Oversikt
Mission Control er et komplett dashboard-system for NRJ Morgen som gir total kontroll over saksliste, podcast, statistikk og automatisering.

**Live URL:** https://baarli.github.io/mission-control-live/  
**Passord:** `kloakontroll2026`  
**Sist oppdatert:** 2026-03-04

---

## Arkitektur

### Frontend
- **Plattform:** GitHub Pages (statisk hosting)
- **Teknologi:** Ren HTML5, CSS3, JavaScript (ES6+)
- **Ingen rammeverk:** Bevisst enkel for pålitelighet
- **Responsivt:** Mobil- og desktop-vennlig

### Backend/Databas
- **Database:** Supabase (PostgreSQL)
- **URL:** https://kvniauxokdtmpvjtfnej.supabase.co
- **Autentisering:** Anon Key (read-only for klient)
- **Tabeller:**
  - `agenda_items` - Saker og statistikk
  - `podcast_episodes` - Podcast-episoder

---

## Funksjoner

### 1. Dashboard (📊)
- Live statistikk (saker, radio-lyttere, podcast-ranking)
- System status med tilkoblingsindikator
- Siste 5 saker rask visning
- Hurtighandlinger (oppdater, test tilkobling)

### 2. Saksliste (📋)
- Vis alle saker for gjeldende dato
- Fargekoding etter kategori:
  - TALK (lilla)
  - REALITY_TV (oransje)
  - KJENDIS_DRAMA (rosa)
  - FILM_TV (blå)
  - MUSIKK (grønn)
  - INTERNASJONALT (lilla)
- Legg til ny sak manuelt
- Slett sak med bekreftelse
- Vis notater og lenker

### 3. Podcast (🎧)
- Liste over alle episoder
- Sortert etter publiseringsdato
- Viser varighet og podkast-navn

### 4. Statistikk (📈)
- Radio-statistikk (uker, lyttere, trend)
- Podcast-statistikk (ranking, downloads)
- Hentet fra agenda_items med category=STATS/PODCAST_RANKING

### 5. Verktøy (🛠️)
- Morning Routine (manuell start)
- Vedlikehold (slett saker eldre enn 7 dager)

---

## Tekniske Detaljer

### Supabase Konfigurasjon
```javascript
const SUPABASE_URL = 'https://kvniauxokdtmpvjtfnej.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...';
const TENANT_ID = 'a0000000-0000-0000-0000-000000000001';
const CREATED_BY = '10aa1508-6d52-490c-8ae5-fa3da9a152c4';
```

### API Endepunkter
- `GET /agenda_items` - Hent saker
- `POST /agenda_items` - Legg til sak
- `DELETE /agenda_items?id=eq.{id}` - Slett sak
- `GET /podcast_episodes` - Hent episoder

### Dato-håndtering
Morgenrutinen lagrer saker med `show_date` satt til **neste dag** (ikke i dag).
Mission Control sjekker derfor:
1. Dagens dato først
2. Hvis ingen saker → sjekker morgendagens dato
3. Bruker den datoen som har data

### Auto-refresh
- Hvert 5. minutt (300 000 ms)
- Kun når bruker er logget inn
- Oppdaterer dashboard i bakgrunnen

---

## Kjente Begrensninger

1. **Morning Routine er simulert** - Må kobles til faktisk backend for full funksjonalitet
2. **Ingen redigering av saker** - Kun legg til/slett
3. **Ingen drag-and-drop sortering** - Sortering skjer via order_index i databasen
4. **CORS avhengig** - Krever at Supabase har riktig CORS-config

---

## Feilsøking

### Kan ikke logge inn
- Sjekk at passord er `kloakontroll2026`
- Prøv hard refresh (Ctrl+Shift+R)
- Sjekk browser console for JS-feil

### Ingen data vises
- Klikk "🔌 Test tilkobling" knapp
- Sjekk at Supabase er oppe
- Verifiser at TENANT_ID er korrekt

### Sakene vises ikke
- Sjekk at saker finnes i Supabase
- Husk: Morgenrutinen bruker neste dags dato
- Se etter feilmeldinger i console

---

## Vedlikehold

### Oppdatere koden
1. Rediger `/root/.openclaw/workspace/mission-control-gh-pages/index.html`
2. Commit og push til GitHub
3. Vent 30 sekunder på GitHub Pages deploy

### Endre passord
1. Endre `const PASSWORD = '...'` i index.html
2. Deploy på nytt

### Legge til nye funksjoner
1. Legg til ny seksjon i HTML
2. Legg til navigasjonsknapp
3. Implementer JavaScript-funksjon
4. Test lokalt før deploy

---

## Sikkerhet

- **Passord:** Hardkodet i frontend (akseptabelt for dette brukstilfellet)
- **Supabase Key:** Anon key med begrensede rettigheter
- **RLS:** Row Level Security aktivert i Supabase
- **HTTPS:** GitHub Pages bruker alltid HTTPS

---

## Fremtidige Forbedringer

- [ ] Backend API for Morning Routine
- [ ] Redigering av eksisterende saker
- [ ] Drag-and-drop sortering
- [ ] Bilder/thumbnails for saker
- [ ] Søk i saker
- [ ] Filter etter kategori
- [ ] Eksport til PDF/Excel
- [ ] Notifikasjoner
- [ ] Dark/light mode toggle
- [ ] Multi-tenant støtte

---

## Kontakt
Ved problemer, sjekk:
1. Denne dokumentasjonen
2. GitHub repo: https://github.com/baarli/mission-control-live
3. Supabase dashboard: https://app.supabase.com
