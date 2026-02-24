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

*Sist oppdatert: 2026-02-24*
