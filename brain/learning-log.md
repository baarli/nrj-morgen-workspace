# Learning Log

Sentral logg over viktige læringsøyeblikk og innsikter.

## 2026-02-24

### Kritisk læring: Cron-jobber med agentTurn
- **Hva:** `agentTurn`-jobber med `delivery.mode=announce` krever `delivery.to` for å nå brukeren
- **Hvorfor viktig:** Uten dette når ikke påminnelser frem
- **Dokumentert i:** MEMORY.md under "Vanlige feil å unngå"

### Teknisk: Auto-exec enforcer
- **Hva:** Scriptet `auto-exec-enforcer.sh` kan ikke skips – det sikrer preflight alltid kjøres
- **Hvorfor viktig:** Hindrer at jeg starter oppgaver uten kontekst

### Innsikt: Selvutvikling > viljestyrke
- **Hva:** Eksterne systemer (cron-jobber) er mer pålitelige enn indre motivasjon
- **Anvendelse:** Bruke påminnelser og automasjon for alt som skal gjøres regelmessig

---

## 2026-02-23

### Teknisk: Kimi K2.5 overgang
- **Hva:** Overgang fra Claude til Kimi K2.5 gikk smertefritt
- **Observasjon:** Modellen er rask og presis på kodeoppgaver

### System: Podcast-clipper i produksjon
- **Hva:** Daglige klipp fra "Baarli og Benjamin går i terapi" genereres automatisk kl 07:00
- **Status:** ✅ Kjører stabilt

### Innsikt: Struktur for refleksjon
- **Hva:** Mal for daglig logging hjelper med systematisering
- **Nøkkel:** Prosess > produkt – det handler om å vise opp hver dag

---

## 2026-02-25

### Teknisk: Autonomous Mission Control Development
- **Hva:** Implementerte system for selvstendig utvikling med task-generering
- **Nøkkel-innsikt:** Autonomi krever struktur - klare regler, sikkerhetsmekanismer og omfattende logging
- **Status:** ✅ Aktivt, kjører hver 30. minutt

### Innsikt: Eierskap øker motivasjon
- **Hva:** Å ha "mitt eget" prosjekt (Mission Control) gir sterkere driv
- **Anvendelse:** Investere i systemer jeg føler eierskap til

### NRJ-arbeid: Morning Routine v2.1 stabil
- **Hva:** 15 saker per dag med OpenAI-titler og kategori-spredning
- **Forbedring:** Maks 3 saker per kategori gir bedre variasjon
- **Problem:** Cron-jobber har "Unsupported channel: whatsapp"-feil

---

## 2026-02-26

### Teknisk: BaarliClaw Toolkit - Egne verktøy fra scratch
- **Hva:** Bygget 5 moduler (64KB kode) uten eksterne avhengigheter
- **Moduler:** toolkit, image, data_analyzer, web_scraper, automation_engine
- **Nøkkel-innsikt:** Python standard library er kraftig nok for det meste
- **Status:** ✅ Testet og dokumentert i skill

### Innsikt: Bygger vs Bruker mindset
- **Hva:** Skiftet fra "bruke verktøy" til "bygge verktøy"
- **Betydning:** Fundamental endring i hva jeg kan gjøre
- **Trigger:** "Jeg mente ferdigheter" - et spark i riktig retning

### System: Modular arkitektur
- **Hva:** Hver modul har ett ansvar, fungerer sammen
- **Anvendelse:** Kan brukes på NRJ-scripts for bedre vedlikeholdbarhet
- **Neste steg:** Refactor brave-news-search.py til moduler

---

---

## 2026-02-27-28

### Teknisk: BaarliClaw Toolkit - 50 Verktøy Komplett!
- **Hva:** Fullførte toolkit med 50 moduler totalt (29 kjerne + 21 avanserte)
- **Nøkkel-moduler:** video_toolkit (ffmpeg), ml_toolkit, dashboard_builder, api_builder, cicd_toolkit
- **Innsikt:** Å bygge mange små, fokuserte moduler er bedre enn få store
- **Arkitektur:** BaseToolkit-mønster med shared utilities og decorators
- **Dokumentasjon:** `docs/TOOLKIT_REFERENCE.md` (komplett referanse)

### Innsikt: Fullførelse > Perfeksjon
- **Hva:** 50 verktøy på én kveld - ferdig er bedre enn perfekt
- **Læring:** Iterativ forbedring etter lansering er mer verdifullt enn evig planlegging
- **Neste fase:** Bruke verktøyene på praktiske oppgaver, ikke bygge mer

### System: Morning Routine pauset
- **Hva:** Bruker ba om å pause Morning Routine - viktig å lytte
- **Innsikt:** Selv automatiserte systemer må vurderes regelmessig
- **Prinsipp:** "Because we've always done it" er ikke en god grunn

---

*Sist oppdatert: 2026-02-28*
