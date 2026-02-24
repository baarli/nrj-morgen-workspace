# MEMORY.md - Viktig informasjon å huske

## 🔑 API Nøkler og Tokens

### Brave Search API
- **Key:** `BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev`
- **Brukes til:** Nyhetssøk, Morning Routine v2.0, Trending Pulse
- **Lagret i:** `.credentials/nrj-morgen.env`
- **Oppdatert:** 2026-02-24

### Morning Routine v2.1
- **Kilder:** 5 kategorier (Reality TV, Kjendis Drama, Film & TV, Musikk, Internasjonalt)
- **Antall saker:** 15 per dag (økt fra 10)
- **Prosess:** Hent fra alle kilder → Samle i pot → Score → Velg topp 15 → **OpenAI tittel (maks 7 ord)** → Insert til Supabase
- **Spredning:** Maks 3 saker per kategori for god variasjon
- **Alder:** Maks 48 timer gamle (freshness=pd = siste 24t)
- **Dokumentasjon:** `docs/MORNING_ROUTINE_V2.md`
- **Script:** `scripts/morning-routine-v2.1.py`
- **Auto-insert:** `scripts/auto-insert-top15.py`
- **Tittelgenerering:** OpenAI GPT-4o-mini, maks 7 ord, norsk språk

### Autonomous Mission Control Development
- **Status:** AKTIV - Jeg jobber nå autonomt med Mission Control
- **Skill:** `skills/autonomous-mission-control/SKILL.md`
- **Script:** `scripts/autonomous-mission-control.sh` (kjører hver 30. minutt)
- **Task Generator:** `scripts/autonomous-task-generator.py`
- **Funksjon:** Selv-genererer oppgaver, finner forbedringer, implementerer nye features
- **Sikkerhet:** Tester i isolert miljø først, rollback-mulighet, logger alt
- **Mål:** Kontinuerlig forbedring uten menneskelig oppfølging

### Supabase
- **URL:** https://kvniauxokdtmpvjtfnej.supabase.co
- **Service Key:** [i .credentials/nrj-morgen.env]
- **Tenant ID:** `a0000000-0000-0000-0000-000000000001`

## 🎓 Selvutvikling og Læring (AKTIVT SYSTEM)

### Pre-Flight Checklist (START av hver oppgave)
**Script:** `/root/.openclaw/workspace/scripts/preflight-checklist.sh`

**Kjøres automatisk ved START av hver oppgave for å:**
1. ✅ Laste MEMORY.md med all kunnskap
2. ✅ Vise HUSK ALLTID fra TOOLS.md
3. ✅ Liste tilgjengelige skills
4. ✅ Sjekke dagens learning log
5. ✅ Vise nylig aktivitet

**Hvorfor:** Sikre at jeg har full kontekst før jeg starter arbeidet

### Auto-Learning Capture (SLUTT av hver oppgave)
**Script:** `/root/.openclaw/workspace/scripts/auto-learning-capture.sh`

**Kjøres automatisk ved SLUTT av hver oppgave for å:**
1. ✅ Sikre at daily log eksisterer
2. ✅ Sjekke at MEMORY.md er oppdatert
3. ✅ Verifisere at skills er opprettet
4. ✅ Kontrollere TOOLS.md

**Hvorfor:** Sikre at all læring blir dokumentert

### Skills jeg har opprettet
1. **nrj-dashboard-system** - NRJ Dashboard oppdateringer
   - Location: `/root/.openclaw/workspace/skills/nrj-dashboard-system/`
   - Package: `/root/.openclaw/workspace/skills/nrj-dashboard-system.skill`
   
2. **self-improvement** - Selvutvikling og læring
   - Location: `/root/.openclaw/workspace/skills/self-improvement/`
   - Package: `/root/.openclaw/workspace/skills/self-improvement.skill`
   - Triggers: "Hva har vi lært?", "Lagre dette", "Husk dette"

### Min arbeidsflyt (ALLTID FØLGET)
```
START av oppgave:
  ↓
Kjør preflight-checklist.sh
  ↓
Les relevante skills
  ↓
Sjekk MEMORY.md for kontekst
  ↓
Utfør oppgaven
  ↓
SLUTT av oppgave:
  ↓
Kjør auto-learning-capture.sh
  ↓
Dokumenter læring
  ↓
Opprett skill hvis repeterbart
```

### Viktige prinsipper (ALLTID FØLGET)
- ✅ **Start alltid med preflight** - Laste all kunnskap
- ✅ **Progressiv avsløring** - Load kun det som trengs
- ✅ **Gjenbruk** - Ikke skriv samme kode om igjen
- ✅ **Dokumentasjon** - Alltid lagre kunnskap
- ✅ **Testing** - Verifiser at skills fungerer
- ✅ **Iterasjon** - Forbedre basert på tilbakemeldinger
- ✅ **Slutt alltid med learning capture** - Dokumentere alt

---

## 🎯 NRJ Morgen Dashboard System

**KRITISK:** Dette er et eget system - IKKE sakslista!

### Hva skal oppdateres
- **NRJ Statistikk panel** på dashboardet (nrjmorgen.com)
- **Panel ID:** `0b1f6b6b-3fde-434b-b7c8-dcf306beea72`
- **Type:** Dashboard panel (agenda_items med is_pinned: true)
- **Plassering:** Øverst på dashboardet

### Hvordan oppdatere
```bash
cd /root/.openclaw/workspace/scripts
python3 update_nrj_dashboard.py
```

**VIKTIG:** Bruk ALLTID `update_nrj_dashboard.py` - dette oppdaterer eksisterende panel.

**IKKE bruk:** `fetch_nrj_dashboard_stats.py` - dette oppretter nytt item i sakslista!

### Nåværende data (sist oppdatert 2026-02-24)

**📻 Nielsen Radio (Uke 7, 2026):**
- Daglige lyttere: 69,000
- Gjennomsnitt 2026: 58,857
- Trend: +9.5% fra uke 6
- Kilde: Nielsen PPM API

**🎧 Podtoppen Podkast:**
- Rangering: #62
- Unike lyttere: 16,470
- Nedlastet: 33,405
- Utgiver: Bauer Media
- Kilde: Kantar/TNS Podtoppen

### Datakilder

**Nielsen API:**
- URL: `https://eu-iport.nielsen-iwatch.com/api/Chart?dataid=8eb6daca-1266-4af8-8e8f-f39107dc63fb&publish_key=bd551853-f42b-4b86-813a-79faf3a718e9`
- Forsinkelse: 1 uke (uke 8 kommer neste uke)
- Publiseres: Onsdag/torsdag
- Format: JSON

**Podtoppen:**
- URL: `https://podtoppen.tnslistene.no/export.php`
- Format: CSV med semikolon, latin-1 encoding
- Oppdateres: Ukentlig (onsdag)

### Supabase konfigurasjon
- **URL:** `https://kvniauxokdtmpvjtfnej.supabase.co`
- **Tabell:** `agenda_items`
- **Tenant ID:** `a0000000-0000-0000-0000-000000000001`
- **Bruker ID:** `10aa1508-6d52-490c-8ae5-fa3da9a152c4` (BaarliClaw)
- **Panel ID:** `0b1f6b6b-3fde-434b-b7c8-dcf306beea72`

### Scripts
- **Oppdatering:** `update_nrj_dashboard.py`
- **Kun Nielsen:** `fetch_nielsen_live.py`
- **Kun Podtoppen:** `fetch_podtoppen_live.py`
- **Gammelt (IKKE BRUK):** `fetch_nrj_dashboard_stats.py`

### Dokumentasjon
- Full system docs: `/root/.openclaw/workspace/docs/NRJ_DASHBOARD_SYSTEM.md`
- Verktøy-config: `/root/.openclaw/workspace/TOOLS.md`

---

## 📰 NRJ Morgen - Sakslista (Agenda Items)

### Hva er dette
- Daglig liste over nyhetssaker for NRJ Morgen radioprogram
- Lagres i Supabase `agenda_items` tabell
- Hver sak har: tittel, beskrivelse, notater, bilder, lenker

### Hvordan oppdatere
```bash
cd /root/.openclaw/workspace/scripts
python3 integrated-morning-routine.sh
```

Eller manuelt:
```bash
python3 brave-news-search.py
```

### Krav til hver sak
1. **Lenke (URL)** til original artikkel i `link_url`-feltet
2. **Notat med oppsummering** i `notes`-feltet på formatet:
   ```
   [Første setning fra beskrivelse]

   Kilde: [Kildenavn]
   ```
3. **Bilde** i `link_metadata` (JSON): `{"image_url": "..."}`
4. **Bilde** i `description` (HTML): `<img src="..." alt="..." />`
5. **created_by:** BaarliClaw ID (`10aa1508-6d52-490c-8ae5-fa3da9a152c4`)
6. **category:** "TALK"
7. **show_date:** Dagens dato

### Søksprompt for nyheter
Se `/root/.openclaw/workspace/.config/nrj-morgen-config.md` for komplett søksprompt.

Kortversjon:
- Finn 15 beste saker fra siste 24-48 timer
- Kilder: VG, Dagbladet, Nettavisen, TV2, NRK, Se & Hør
- Prioriter: kjendisnyheter, TV, reality, influencere, skandaler
- Unngå: politiske tungvektsaker uten kjendiskobling

### Scripts
- **Hovedrutine:** `integrated-morning-routine.sh`
- **Nyhetssøk:** `brave-news-search.py`
- **Bildeoppdatering:** `update_article_images.py`
- **Description bilder:** `update_description_images.py`

### Dokumentasjon
- Config: `/root/.openclaw/workspace/.config/nrj-morgen-config.md`
- Tools: `/root/.openclaw/workspace/TOOLS.md`

---

## 🎧 Baarli og Benjamin - Podkast System

### Hva er dette
- Podkast-plattform for "Baarli og Benjamin går i terapi"
- Repo: `baarliogbenjamin` (GitHub)
- Branch: `main` (produksjon)

### Nylige forbedringer (2026-02-23)
10 subagenter fullført massive forbedringer:

1. **Docker Support** - Multi-stage builds, docker-compose
2. **GitHub Actions** - CI/CD workflows, Dependabot
3. **Advanced Testing** - Visual regression, E2E, performance, a11y
4. **React Patterns** - Compound components, hooks, HOCs
5. **Modern UI Components** - 15+ nye komponenter
6. **Real-time Features** - Supabase Realtime, live cursors
7. **Search & Filtering** - Fuse.js global search
8. **Feature Flags** - A/B testing, user targeting
9. **Monitoring & Analytics** - Sentry, GA4, Web Vitals
10. **Data Export/Import** - CSV/Excel/PDF/JSON

### Repo lokasjon
```
/root/.openclaw/workspace/baarliogbenjamin/
```

### Viktige filer
- `README.md` - Prosjektdokumentasjon
- `API_DOCUMENTATION.md` - API docs
- `ARCHITECTURE.md` - Arkitektur
- `package.json` - Avhengigheter

### Scripts
- **Bygg:** `npm run build`
- **Test:** `npm run test`
- **Dev:** `npm run dev`

---

## 🤖 Subagent System

### Hva er dette
- System for å kjøre parallelle oppgaver via subagenter
- Hver subagent jobber på én spesifikk oppgave
- Resultater annonseres tilbake til hovedsesjon

### Hvordan bruke
```python
# Start subagent
sessions_spawn(
    agentId="main",
    label="task-name",
    task="Detaljert oppgavebeskrivelse...",
    runTimeoutSeconds=1800
)
```

### Sjekke status
```bash
openclaw subagents list
```

### Best practices
- Gi detaljerte oppgaver med kontekst
- Spesifiser filstier eksplisitt
- Be om push til branch ved fullføring
- Sett passende timeout (15-30 min)

---

## 📊 Supabase Konfigurasjon

### URL
```
https://kvniauxokdtmpvjtfnej.supabase.co
```

### Viktige tabeller
- **agenda_items** - Sakslista + Dashboard paneler
- **profiles** - Brukerprofiler
- **messages** - Meldinger/kommentarer

### Viktige ID-er
- **Tenant ID:** `a0000000-0000-0000-0000-000000000001`
- **BaarliClaw ID:** `10aa1508-6d52-490c-8ae5-fa3da9a152c4`
- **NRJ Panel ID:** `0b1f6b6b-3fde-434b-b7c8-dcf306beea72`

---

## 📁 Viktige mapper og filer

### Workspace struktur
```
/root/.openclaw/workspace/
├── scripts/                    # Alle scripts
│   ├── update_nrj_dashboard.py      # OPPDATER DASHBOARD
│   ├── integrated-morning-routine.sh # SAKSLISTA
│   ├── brave-news-search.py
│   ├── fetch_nielsen_live.py
│   ├── fetch_podtoppen_live.py
│   └── ...
├── docs/                       # Dokumentasjon
│   ├── NRJ_DASHBOARD_SYSTEM.md
│   ├── API_DOCUMENTATION.md
│   └── ARCHITECTURE.md
├── baarliogbenjamin/          # Podkast repo
├── .config/                   # Konfigurasjon
│   └── nrj-morgen-config.md
├── MEMORY.md                  # DENNE FILEN
├── TOOLS.md                   # Verktøy-config
└── SOUL.md                    # Personlighet
```

---

## ⚠️ Vanlige feil å unngå

### NRJ Dashboard
- ❌ IKKE bruk `fetch_nrj_dashboard_stats.py` (oppretter nytt item)
- ✅ ALLTID bruk `update_nrj_dashboard.py` (oppdaterer eksisterende)
- ❌ IKKE legg i sakslista
- ✅ Oppdater panel ID `0b1f6b6b-3fde-434b-b7c8-dcf306beea72`

### Sakslista
- ❌ IKKE glem `created_by` feltet (må være BaarliClaw ID)
- ❌ IKKE glem bilder i både `link_metadata` OG `description`
- ✅ ALLTID inkluder kilde i notater

### Git
- ❌ IKKE push direkte til main uten testing
- ✅ Bruk brancher for nye features
- ✅ Verifiser at det ikke er konflikter før merge

---

## 🔗 Nyttige lenker

### NRJ
- Dashboard: https://nrjmorgen.com
- Nielsen: https://eu-iport.nielsen-iwatch.com/api/Chart
- Podtoppen: https://podtoppen.tnslistene.no/

### GitHub
- Baarliogbenjamin: https://github.com/baarli/baarliogbenjamin
- OpenClaw: https://github.com/openclaw/openclaw

### Dokumentasjon
- OpenClaw docs: https://docs.openclaw.ai
- Supabase: https://supabase.com/docs

---

## 📝 Sjekkliste før du gjør noe

### Før du oppdaterer NRJ Dashboard:
1. [ ] Les MEMORY.md (denne filen)
2. [ ] Sjekk at du bruker `update_nrj_dashboard.py`
3. [ ] Verifiser panel ID: `0b1f6b6b-3fde-434b-b7c8-dcf306beea72`
4. [ ] Kjør script
5. [ ] Verifiser at data er oppdatert

### Før du oppdaterer sakslista:
1. [ ] Les søksprompt i `.config/nrj-morgen-config.md`
2. [ ] Kjør `integrated-morning-routine.sh`
3. [ ] Verifiser at alle saker har bilder og kilder
4. [ ] Sjekk at `created_by` er satt

### Før du merger kode:
1. [ ] Test lokalt
2. [ ] Sjekk at alle tester passerer
3. [ ] Verifiser at det ikke er konflikter
4. [ ] Code review (hvis mulig)

---

## 🆘 Hva gjør jeg hvis...

### ...jeg glemmer hvilket script å bruke?
→ Les MEMORY.md eller TOOLS.md

### ...jeg glemmer panel ID?
→ Sjekk MEMORY.md eller kjør query i Supabase

### ...Nielsen API feiler?
→ Sjekk at URL er tilgjengelig i browser
→ Verifiser `publish_key` parameter
→ Sjekk User-Agent header

### ...Podtoppen feiler?
→ Sjekk at https://podtoppen.tnslistene.no/export.php fungerer
→ Verifiser CSV-format ikke har endret seg
→ Sjekk encoding (latin-1)

### ...jeg er usikker på noe?
→ Sjekk dokumentasjon i `docs/`
→ Les TOOLS.md
→ Spør hvis nødvendig

---

---

## 🔄 KONTINUERLIG OPPDATERING - NY REGEL (2026-02-24)

### Prinsipp
**ALLTID etter hver endring:** Oppdater ALL kunnskap, ALLE filer, ALLE prompter og ALLE scripts med ny informasjon.

### Hva dette betyr
1. ✅ **MEMORY.md** - Oppdateres med all ny kunnskap
2. ✅ **TOOLS.md** - Oppdateres med nye verktøy/config
3. ✅ **AGENTS.md** - Oppdateres med nye prosedyrer
4. ✅ **Skills** - Oppdateres med ny funksjonalitet
5. ✅ **Prompter** - Oppdateres med ny kontekst
6. ✅ **Scripts** - Oppdateres med nye funksjoner
7. ✅ **Dokumentasjon** - Oppdateres i `docs/`
8. ✅ **Konfigurasjon** - Oppdateres i `.config/`

### Auto-oppdateringssystem
**Script:** `scripts/auto-update-all-knowledge.sh`  
**Frekvens:** Etter hver endring + hver time via cron  
**Logg:** `/var/log/auto-update-knowledge.log`

### Hva som skjer automatisk
```
Etter hver endring jeg gjør:
  ↓
1. Oppdater MEMORY.md med ny kunnskap
  ↓
2. Oppdater TOOLS.md med nye verktøy
  ↓
3. Oppdater relevante skills
  ↓
4. Oppdater prompter med ny kontekst
  ↓
5. Oppdater dokumentasjon i docs/
  ↓
6. Verifiser at alt er konsistent
  ↓
7. Logg alle endringer
```

### Garantert konsistens
- ✅ Ingen utdatert informasjon eksisterer
- ✅ All kunnskap er 100% oppdatert
- ✅ Full kontekst gjennomgående
- ✅ Ingen motsetninger mellom filer
- ✅ Alle prompter har full kontekst

### Hvis jeg finner utdatert info
1. Oppdater umiddelbart
2. Marker som deprecated hvis nødvendig
3. Verifiser at ingen andre filer refererer til gammel info
4. Logg endringen

---

## 📝 DAGENS LÆRING (2026-02-24)

### Viktigste innsikter fra i dag:

1. **Auto-update system fungerer** - Implementert og testet
2. **Mission Control Sync** - Alle 27 HTML-filer nå konsistente
3. **Autonom prosjektstyring** - 6 prosjekter fullført/startet automatisk
4. **PWA + Mobile** - Full offline-støtte og mobil-optimalisering

### Nye systemer etablert:
- ✅ Kontinuerlig oppdatering (hver time)
- ✅ Auto-sync av HTML-filer (ved hver endring)
- ✅ Auto-deploy til Netlify (ved hver endring)
- ✅ Auto-start neste prosjekt (ved fullførelse)

### Tekniske gjennombrudd:
- Service Workers for offline funksjonalitet
- Touch-vennlig UI for mobile enheter
- Real-time collaboration med WebSocket
- AI-powered content suggestions

### Dokumentasjon:
- Full logg: `memory/2026-02-24.md`
- System docs: `docs/CONTINUOUS_UPDATE_SYSTEM.md`
- Sync regel: `docs/MISSION_CONTROL_SYNC_RULE.md`

---

## 🚀 Mission Control Dashboard

### Live URL
- **Dashboard:** https://creative-muffin-dcf3a0.netlify.app/
- **Admin:** https://app.netlify.com/projects/creative-muffin-dcf3a0

### Tilgang
- **Passord:** kloakontroll2026

### Netlify Konto
- **Eier:** niklasbaarli@gmail.com
- **Site ID:** `834576a6-da2b-4412-9433-315f6437508a`
- **Token:** `nfp_8B3dDBwZS9W1GSHTUy3am4fia6iZmF6b0092`

### Deploy
```bash
export NETLIFY_AUTH_TOKEN="nfp_8B3dDBwZS9W1GSHTUy3am4fia6iZmF6b0092"
cd /root/.openclaw/workspace/mission-control/public
netlify deploy --prod
```

### Funksjoner
- [x] Login med passord
- [x] System Overview (4 statistikk-kort)
- [x] Active Automations
- [x] Live Logs
- [x] Skills visning
- [x] Security status
- [x] Responsive design

### Planlagte forbedringer
- [ ] Real-time data fra systemer
- [ ] Ekte logg-streaming
- [ ] Grafikk og diagrammer
- [ ] Kontrollpanel for automasjoner
- [ ] Push notifications

### Dokumentasjon
- Full docs: `/root/.openclaw/workspace/docs/MISSION_CONTROL_NETLIFY.md`
- Kildekode: `/root/.openclaw/workspace/mission-control/`

---

**Sist oppdatert:** 2026-02-24 18:43
**Opprettet av:** BaarliClaw
**Formål:** Garantert riktig bruk av alle systemer
