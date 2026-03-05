# 🏛️ ARKITEKTUR - Én Kilde til Sannhet

**Dokumentversjon:** 1.0  
**Sist oppdatert:** 2026-03-05  
**Formål:** Definere hierarki og ansvar for all dokumentasjon

---

## 🚀 QUICK REFERENCE

| Vil du vite... | Gå til |
|----------------|--------|
| **Hva er status på X?** | [AGENTS.md](AGENTS.md) |
| **Hvordan bruker jeg X?** | [TOOLS.md](TOOLS.md) |
| **Hva lærte jeg om X?** | [MEMORY.md](MEMORY.md) |
| **Hva skjedde på dato Y?** | `brain/daily/YYYY-MM-DD.md` |
| **Hva er API key til X?** | `.credentials/` |
| **Hva er prinsippene?** | [PRINCIPLES.md](PRINCIPLES.md) |
| **Hvem er jeg?** | [SOUL.md](SOUL.md) |

---

## 📋 DOKUMENT-HIERARKI

```
PRINCIPLES.md (Rot - alle må følge)
    │
    ├── AGENTS.md (System-oversikt, agenter, verktøy)
    │   └── Refererer til: MEMORY.md, TOOLS.md
    │
    ├── MEMORY.md (Langsiktig minne, læring, historikk)
    │   └── Refererer til: Daglige logger i memory/
    │
    ├── TOOLS.md (Verktøy, scripts, API-er)
    │   └── Refererer til: skills/, scripts/
    │
    └── SOUL.md (Personlighet, verdier, arbeidsstil)
        └── Påvirker: All kommunikasjon
```

---

## 📁 ANSVARSFORDELING

### 1. PRINCIPLES.md - 🔴 KJERNEN
**Ansvar:** Overordnede prinsipper alle må følge  
**Innhold:** Verdier, regler, filosofi  
**Oppdateres:** Sjeldent (kun ved fundamentale endringer)

### 2. AGENTS.md - 🟠 SYSTEM-OVERSIKT
**Ansvar:** Hva finnes, hvor finnes det, status  
**Innhold:**
- Telegram Bot (status, token, chat ID)
- Mission Control (URL, passord, repo)
- Supabase (URL, project ID)
- Andre systemer

**SKAL IKKE INNEHOLDE:**
- Detaljerte API keys (henvis til .credentials/)
- Historikk (henvis til MEMORY.md)
- Verktøy-detaljer (henvis til TOOLS.md)

### 3. MEMORY.md - 🟡 LANGSIKTIG MINNE
**Ansvar:** Hva har jeg lært, hva må jeg huske  
**Innhold:**
- Kritisk læring (feil, løsninger)
- System-endringer
- Viktige hendelser
- Bruker-preferanser

**SKAL IKKE INNEHOLDE:**
- Daglige detaljer (henvis til memory/YYYY-MM-DD.md)
- Tekniske spesifikasjoner (henvis til AGENTS.md)
- Verktøy-beskrivelser (henvis til TOOLS.md)

### 4. TOOLS.md - 🟢 VERKTØY
**Ansvar:** Hvordan bruke verktøy og scripts  
**Innhold:**
- Script-beskrivelser
- API-endepunkter
- Bruks-eksempler
- Kommandoer

**SKAL IKKE INNEHOLDE:**
- Credentials (henvis til .credentials/)
- Historikk (henvis til MEMORY.md)
- System-status (henvis til AGENTS.md)

### 5. SOUL.md - 🔵 PERSONLIGHET
**Ansvar:** Hvem er jeg, hvordan jobber jeg  
**Innhold:**
- Personlighetstrekk
- Arbeidsstil
- Kommunikasjonsmønster
- Følelser og stemning

---

## 🗂️ DAGLIGE LOGGER (brain/daily/)

**Formål:** Rå data om hva som skjedde hver dag  
**Struktur:** `brain/daily/YYYY-MM-DD.md`  
**Innhold:**
- Hva ble gjort
- Tekniske detaljer
- Problemer og løsninger
- Læring

**Viktig:** MEMORY.md er et **sammendrag** av det viktigste fra daglige logger.  
**Cron-jobs:** Bruker `brain/daily/` (ikke `memory/`).

---

## 🔐 CREDENTIALS (.credentials/)

**Formål:** Sensitiv data (tokens, keys, passord)  
**Struktur:**
```
.credentials/
├── MASTER_CREDENTIALS.md    # Oversikt (uten sensitive data)
├── telegram-bot.env         # Telegram-spesifikt
├── nrj-morgen.env          # NRJ-spesifikt
└── live-search.env         # Søk/API-spesifikt
```

**Regel:** ALDRI referer til credentials direkte i dokumentasjon. Bruk: "Se .credentials/telegram-bot.env"

---

## 🎯 SKILL-FILER (skills/)

**Formål:** Spesialisert kunnskap for spesifikke oppgaver  
**Struktur:** `skills/<navn>/SKILL.md`

**Innhold:**
- Hva skillen gjør
- Hvordan bruke den
- Eksempler

**Viktig:** Skills skal være **selvstendige** og ikke duplisere informasjon fra MEMORY.md eller TOOLS.md.

---

## 🧹 OPPRYDDING - HVA SKAL SLETTES/FLETES

### Duplisert informasjon:
- [ ] `memory/MINNEOVERSIKT.md` → Flett inn i AGENTS.md
- [ ] `telegram-setup-manual.md` → Flett inn i AGENTS.md
- [ ] `telegram-webhook-plan.md` → Flett inn i MEMORY.md
- [ ] `communication-plan.md` → Vurdere om nødvendig
- [ ] `VEV-PROTOCOL.md` → Flett inn i AGENTS.md

### Gamle/utdaterte filer:
- [ ] Sjekke `memory/` for duplikater
- [ ] Sjekke `scripts/` for ubrukte scripts

---

## 📝 BEST PRACTICES

### Når jeg oppdaterer dokumentasjon:

1. **Start med PRINCIPLES.md** - Følger jeg prinsippene?
2. **Sjekk AGENTS.md** - Er system-oversikten riktig?
3. **Oppdater MEMORY.md** - Hva må jeg huske langsiktig?
4. **Oppdater TOOLS.md** - Trengs nye verktøy-beskrivelser?
5. **Daglig logg** - Dokumenter detaljer i `memory/YYYY-MM-DD.md`

### Når jeg trenger informasjon:

| Jeg vil vite... | Gå til |
|----------------|--------|
| Hva er status på X? | AGENTS.md |
| Hvordan bruker jeg X? | TOOLS.md |
| Hva lærte jeg om X? | MEMORY.md |
| Hva skjedde på dato Y? | memory/YYYY-MM-DD.md |
| Hva er API key til X? | .credentials/ |
| Hva er prinsippene? | PRINCIPLES.md |

---

## ✅ OPPGAVE: Rydding

**Steg 1:** Flette MINNEOVERSIKT.md inn i AGENTS.md  
**Steg 2:** Slette duplikater i memory/  
**Steg 3:** Oppdatere alle filer til å følge hierarkiet  
**Steg 4:** Lage "sannhetskontroll" - skript som sjekker konsistens

---

**Denne arkitekturen skal følges av alle fremtidige oppdateringer.**
