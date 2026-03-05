# 📝 Mission Control - Oppgaveliste / Todo List

**Opprettet:** 2026-03-04  
**Formål:** Systematisk oppgavehåndtering for videreutvikling

---

## 🎯 Nåværende Oppgaver (Aktive)

### 🔴 Kritisk (Må gjøres nå)
- [ ] **Fiks Brave Search** - Søk fungerer ikke fra Mission Control
  - Problembeskrivelse: Brave News API-kall feiler
  - Sjekk: API-nøkkel, nettverkskall, CORS, error handling
  
- [ ] **Custom Brave Prompt** - Bruker skal kunne skrive egen prompt
  - Input-felt for prompt
  - Lagre prompt i localStorage
  - Bruke prompt i Brave API-kall

### 🟡 Høy prioritet (Gjør etter kritisk)
- [ ] **Forbedret søkeresultat-visning**
  - Bedre UI for å velge enkeltsaker
  - Preview av saker før import
  - Bulk-select funksjonalitet

### 🟢 Medium prioritet (Gjør når tid)
- [ ] **Autosave** - Automatisk lagring av endringer
- [ ] **Duplikatsjekk** - Varsle hvis sak finnes fra før
- [ ] **Søkefilter** - Filtrer resultater etter score/kategori

---

## ✅ Fullførte Oppgaver

### Fase 1-5 Fullført
- [x] Quick Wins (loading states, toast, keyboard shortcuts)
- [x] Fase 2 (inline editing, search history)
- [x] Fase 3 (animations, dark/light mode)
- [x] Fase 4 (charts, CSV export)
- [x] Fase 5 delvis (accessibility, fjernet broken onboarding)

### Bug Fixes
- [x] Fikset login-problemer
- [x] Fikset JavaScript syntax feil
- [x] Fikset loadCharts error
- [x] Fjernet broken onboarding

---

## 🐛 Kjente Bugs (Å fikse)

| Bug | Status | Prioritet | Notater |
|-----|--------|-----------|---------|
| Brave Search fungerer ikke | 🔴 Ny | Kritisk | Sjekk API-kall |
| ~Onboarding broken~ | ✅ Fikset | - | Fjernet helt |
| ~loadCharts error~ | ✅ Fikset | - | Lagt til sjekk |

---

## 💡 Fremtidige Forbedringer (Backlog)

### Funksjonalitet
- [ ] **Drag & drop** - Endre rekkefølge på saker
- [ ] **Favoritter** - Lagre saker til senere
- [ ] **Notater** - Legge til interne notater på saker
- [ ] **Tags** - Merke saker med egne tags
- [ ] **Søk i saksliste** - Fuzzy search

### Integrasjoner
- [ ] **Slack** - Send saker til Slack
- [ ] **E-post** - E-post saksliste
- [ ] **Kalender** - Synk med Google Calendar

### Brukeropplevelse
- [ ] **Onboarding v2** - Ny, fungerende onboarding
- [ ] **Hurtigtaster** - Flere keyboard shortcuts
- [ ] **Mobilapp** - PWA med offline-støtte

### Admin
- [ ] **Brukere** - Flere brukerkontoer
- [ ] **Rettigheter** - Rollebasert tilgang
- [ ] **Audit log** - Logg alle endringer

---

## 📊 Statistikk

**Fullførte oppgaver:** 15+  
**Gjenstående kritiske:** 2  
**Gjenstående høy:** 1  
**Gjenstående medium:** 3  
**Backlog:** 10+

---

## 🔄 Oppdatering

**Sist oppdatert:** 2026-03-04 23:18  
**Neste gjennomgang:** Etter Brave Search-fiks

---

## 📝 Notater

### Brave Search Feilsøking
- Sjekk at BRAVE_KEY er korrekt
- Verifiser at API-endepunkt fungerer
- Sjekk nettverks-tab i browser
- Se etter CORS-feil
- Sjekk rate limiting

### Custom Prompt Implementasjon
1. Legg til textarea i søkeseksjon
2. Lagre prompt i localStorage
3. Bruk prompt i API-kall
4. Vis prompt-historikk

---

**Husk:** Oppdater denne filen etter hver oppgave som fullføres!