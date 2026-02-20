# Løsninger for Video-tilgang fra Norske Medier

## Problem
VG, NRK, TV2, Dagbladet og Nettavisen blokkerer web-scraping (403/418 feil).

## Løsningsalternativer

### 1. Offisielle API-er (Beste løsning)

**Hva:** Bruke medienes offisielle API-er for å hente video-metadata

**Status:**
- **NRK:** Har API (api.nrk.no) - krever søknad
- **VG:** VGTV API - krever avtale/partnerskap
- **TV2:** TV2 Play API - krever avtale
- **Dagbladet:** Ingen offentlig API
- **Nettavisen:** Ingen offentlig API

**Fordeler:**
- Lovlig og stabil
- Høy kvalitet på data
- Direkte tilgang til video-URLer

**Ulemper:**
- Krever avtaler med hver mediehus
- Kan ta tid å få tilgang
- Mulige kostnader

**Hvordan:**
1. Kontakte hvert mediehus' API-avdeling
2. Forklare formål (radio, redaksjonell bruk)
3. Søke om API-nøkkel
4. Integrere API-er i pipeline

---

### 2. RSS-feeds med video

**Hva:** Bruke RSS-feeds som ofte inneholder video-referanser

**Status:**
- **NRK:** RSS-feeds tilgjengelig (nrk.no/rss)
- **VG:** RSS-feeds med video-innhold
- **TV2:** RSS-feeds
- **Dagbladet:** RSS-feeds

**Fordeler:**
- Offentlig tilgjengelig
- Ingen scraping-blokkering
- Standard format

**Ulemper:**
- Ikke alle videoer er i RSS
- Begrenset metadata
- Krever parsing

**Hvordan:**
```python
import feedparser

# NRK RSS
feed = feedparser.parse('https://www.nrk.no/toppsaker.rss')
for entry in feed.entries:
    if 'video' in entry:
        video_url = entry.video_url
```

---

### 3. Samarbeid med Mediehusene

**Hva:** Direkte samarbeid med mediehusene

**Status:**
- NRJ Morgen er en kjent radiokanal
- Kan kontakte presse/PR-avdelinger
- Mulighet for "partner"-status

**Fordeler:**
- Beste løsning på lang sikt
- Kan få direkte tilgang til video-arkiv
- Mulighet for eksklusivt innhold

**Ulemper:**
- Tar tid å etablere
- Krever forhandlinger
- Avhengig av vedlikehold

**Hvordan:**
1. Kontakte presseansvarlig i hvert mediehus
2. Forklare konseptet (video-klipp til radio)
3. Tilby kreditering/link tilbake
4. Etablere fast rutine for tilgang

---

### 4. Manuell URL-innlegging (MVP)

**Hva:** Niklas/Baarli legger inn video-URLer manuelt

**Status:**
- Kan implementeres umiddelbart
- Ingen avhengighet av mediehus

**Fordeler:**
- Fungerer nå
- Full kontroll over innhold
- Ingen tekniske begrensninger

**Ulemper:**
- Krever manuelt arbeid
- Ikke skalerbart
- Tidskrevende

**Hvordan:**
1. Lage UI i nrjmorgen.com for URL-innlegging
2. Niklas finner videoer på VG/TV2/NRK
3. Kopierer URL og limer inn i systemet
4. Pipeline prosesserer automatisk

---

### 5. Browser Automation (Selenium/Playwright)

**Hva:** Bruke nettleser-automasjon for å hente videoer

**Status:**
- Mer avansert enn scraping
- Kan omgå noen blokkeringer

**Fordeler:**
- Fungerer med JavaScript-tunge sider
- Kan simulere ekte bruker

**Ulemper:**
- Tregere enn scraping
- Kan fortsatt bli blokkert
- Ressurskrevende
- Gråsone juridisk

**Hvordan:**
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://www.vg.no/video/...')
    video_url = page.eval_on_selector('video', 'el => el.src')
```

---

## Anbefaling

### Fase 1: Manuell URL-innlegging (NÅ)
- Implementer UI for å lime inn video-URLer
- Niklas kan bruke dette mens vi jobber med API-er

### Fase 2: RSS-feeds (1-2 uker)
- Implementere RSS-parsing
- Automatisk hente video-referanser

### Fase 3: API-avtaler (1-3 måneder)
- Kontakte mediehusene
- Søke om API-tilgang
- Integrere offisielle API-er

### Fase 4: Samarbeid (3-6 måneder)
- Etablere partnerskap
- Direkte tilgang til video-arkiv
- Automatisk daglig leveranse

---

## Hva vil du gjøre?

1. **Starte med manuell URL-innlegging** (raskt, fungerer nå)
2. **Implementere RSS-feeds** (automatisk, men begrenset)
3. **Kontakte mediehusene** (best på lang sikt)
4. **Alle tre samtidig** (komplett løsning)
