# KONTINUERLIG OPPDATERING - SYSTEMDOKUMENTASJON

**Versjon:** 1.0  
**Dato:** 2026-02-24  
**Eier:** BaarliClaw (AI Agent)

---

## 🎯 FORMÅL

Sikre at **ALL** kunnskap, **ALLE** filer, **ALLE** prompter og **ALLE** scripts alltid er 100% oppdatert med full kontekst gjennomgående i hele systemet.

---

## 📋 REGEL

**ETTER HVER ENDRING skal følgende skje automatisk:**

### 1. Oppdater MEMORY.md
- Legg til ny kunnskap
- Oppdater timestamps
- Marker utdatert info
- Verifiser konsistens

### 2. Oppdater TOOLS.md
- Legg til nye verktøy
- Oppdater konfigurasjon
- Dokumenter endringer

### 3. Oppdater AGENTS.md
- Legg til nye prosedyrer
- Oppdater arbeidsflyter
- Dokumenter best practices

### 4. Oppdater Skills
- Oppdater eksisterende skills
- Lag nye skills ved behov
- Verifiser at skills fungerer

### 5. Oppdater Prompter
- Oppdater med ny kontekst
- Legg til nye instruksjoner
- Verifiser at prompter er komplette

### 6. Oppdater Scripts
- Legg til nye funksjoner
- Oppdater eksisterende scripts
- Verifiser at scripts fungerer

### 7. Oppdater Dokumentasjon
- Oppdater docs/
- Oppdater .config/
- Verifiser at all docs er konsistent

---

## 🔧 VERKTØY

### auto-update-all-knowledge.sh
**Lokasjon:** `scripts/auto-update-all-knowledge.sh`

**Funksjon:**
- Oppdaterer MEMORY.md
- Sjekker TOOLS.md
- Sjekker AGENTS.md
- Oppdaterer skills
- Oppdaterer .config/system-status.json
- Verifiserer konsistens

**Kjøres:**
- Etter hver endring (manuelt)
- Hver time (via cron)
- Ved systemstart

**Kommando:**
```bash
bash /root/.openclaw/workspace/scripts/auto-update-all-knowledge.sh
```

### Cron Job
**ID:** `a6446e60-d4f5-4e0e-900b-436935241e62`  
**Frekvens:** Hver time  
**Status:** Aktiv

---

## 📁 FILSTRUKTUR

```
/root/.openclaw/workspace/
├── MEMORY.md                    # Hovedkunnskapsbase
├── TOOLS.md                     # Verktøy-konfigurasjon
├── AGENTS.md                    # Agent-prosedyrer
├── SOUL.md                      # Personlighet
├── .last-knowledge-update       # Timestamp siste oppdatering
│
├── scripts/
│   └── auto-update-all-knowledge.sh  # Auto-update script
│
├── .config/
│   └── system-status.json       # System status
│
├── skills/
│   └── [skill-name]/
│       └── SKILL.md             # Oppdateres ved behov
│
└── docs/
    └── [dokumentasjon]          # Oppdateres ved behov
```

---

## ✅ SJEKKLISTE FOR OPPDATERING

### Etter hver endring:
- [ ] MEMORY.md oppdatert med ny kunnskap
- [ ] TOOLS.md sjekket og oppdatert ved behov
- [ ] AGENTS.md sjekket og oppdatert ved behov
- [ ] Relevante skills oppdatert
- [ ] Prompter oppdatert med ny kontekst
- [ ] Scripts oppdatert ved behov
- [ ] Dokumentasjon oppdatert
- [ ] Konsistens verifisert
- [ ] Timestamp oppdatert

---

## 🔄 AUTO-UPDATE FLYT

```
Endring gjøres
    ↓
auto-update-all-knowledge.sh trigges
    ↓
MEMORY.md oppdateres
    ↓
TOOLS.md sjekkes
    ↓
AGENTS.md sjekkes
    ↓
Skills oppdateres
    ↓
system-status.json oppdateres
    ↓
Konsistens verifiseres
    ↓
Timestamp logges
    ↓
✅ Full kontekst opprettholdt
```

---

## 📊 OVERVÅKING

### Logg-filer
- **Auto-update:** `/var/log/auto-update-knowledge.log`
- **Timestamp:** `.last-knowledge-update`
- **System status:** `.config/system-status.json`

### Verifisering
```bash
# Sjekk siste oppdatering
cat /root/.openclaw/workspace/.last-knowledge-update

# Sjekk system status
cat /root/.openclaw/workspace/.config/system-status.json

# Sjekk auto-update log
tail -20 /var/log/auto-update-knowledge.log
```

---

## 🚨 HVIS NOE GÅR GALT

### Problem: Utdatert informasjon funnet
**Løsning:**
```bash
# Kjør auto-update umiddelbart
bash /root/.openclaw/workspace/scripts/auto-update-all-knowledge.sh

# Verifiser at alt er oppdatert
cat /root/.openclaw/workspace/.last-knowledge-update
```

### Problem: Inkonsistens mellom filer
**Løsning:**
1. Identifiser hvilke filer som er inkonsistente
2. Oppdater MEMORY.md med korrekt info
3. Kjør auto-update
4. Verifiser at alle filer nå er konsistente

---

## 🤖 AUTONOM DRIFT

**Jeg (BaarliClaw) skal:**
1. ✅ Kjøre auto-update etter hver endring jeg gjør
2. ✅ Verifisere at all kunnskap er oppdatert
3. ✅ Aldri la utdatert informasjon eksistere
4. ✅ Rapportere avvik umiddelbart
5. ✅ Opprettholde 100% konsistens

**Denne regelen er BINDENDE og skal følges til punkt og prikke!**

---

**Sist oppdatert:** 2026-02-24 17:35  
**Versjon:** 1.0
