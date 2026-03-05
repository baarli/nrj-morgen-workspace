# MISSION CONTROL SYNC REGEL

## 📋 REGEL: ALLTID KONSISTENT

**Gyldig fra:** 2026-02-24  
**Versjon:** 3.1  
**Ansvarlig:** BaarliClaw (AI Agent)

---

## 🎯 PRINSIPP

**ETTER HVER ENDRING** skal følgende skje automatisk:

1. ✅ Alle HTML-filer oppdateres med samme meny
2. ✅ Alle sider får samme head-innhold (scripts, CSS)
3. ✅ Alle sider får samme footer-scripts
4. ✅ Aktivt prosjekt-widget vises på alle sider
5. ✅ Deploy til Netlify skjer automatisk
6. ✅ Ingen utdaterte versjoner eksisterer

---

## 🔧 VERKTØY

### 1. mission-control-sync.sh
**Brukes til:** Synkronisere eksisterende filer  
**Kjøres:** Etter hver manuell endring  
**Kommando:**
```bash
bash /root/.openclaw/workspace/scripts/mission-control-sync.sh --deploy
```

### 2. generate-mission-control-pages.py
**Brukes til:** Regenerere alle sider fra TEMPLATE.html  
**Kjøres:** Ved større endringer eller ukentlig  
**Kommando:**
```bash
python3 /root/.openclaw/workspace/scripts/generate-mission-control-pages.py
```

### 3. auto-sync-mission-control.sh
**Brukes til:** Automatisk synkronisering  
**Kjøres:** Av cron hver time, eller manuelt  
**Kommando:**
```bash
bash /root/.openclaw/workspace/scripts/auto-sync-mission-control.sh
```

---

## 📁 FILSTRUKTUR

```
mission-control/public/
├── TEMPLATE.html              # Master template
├── total-control.html         # Generert fra template
├── sakslista-pro.html         # Generert fra template
├── analytics.html             # Generert fra template
├── ... (alle andre sider)
│
├── shared-navigation.js       # Felles navigasjon
├── auto-nav.js               # Auto-inject navigation
├── realtime-collaboration.js # Felles collaboration
├── ai-content-suggestions.js # Felles AI-funksjon
│
└── .last-auto-sync           # Timestamp siste sync
```

---

## ✅ SJEKKLISTE FOR KONSISTENS

Alle HTML-sider MÅ ha:

- [ ] Samme `<head>` struktur
- [ ] Samme navigation meny
- [ ] Samme versjonsnummer (v3.1)
- [ ] `realtime-collaboration.js`
- [ ] `ai-content-suggestions.js`
- [ ] `shared-navigation.js`
- [ ] `auto-nav.js`
- [ ] Aktivt prosjekt-widget
- [ ] Samme CSS variabler
- [ ] Samme footer struktur

---

## 🔄 AUTO-SYNC CRON

**Cron jobb:** Hver time  
**Script:** `auto-sync-mission-control.sh`  
**Gjør:**
1. Synkroniserer alle filer
2. Regenererer sider fra template
3. Deployer til Netlify
4. Sender varsel ved fullføring

---

## 🚨 HVIS NOE GÅR GALT

### Problem: Utdaterte sider eksisterer
**Løsning:**
```bash
cd /root/.openclaw/workspace/mission-control/public
# Slett utdaterte sider
rm -f *.html.backup
# Regenerer alt
python3 /root/.openclaw/workspace/scripts/generate-mission-control-pages.py
# Deploy
bash /root/.openclaw/workspace/scripts/mission-control-sync.sh --deploy
```

### Problem: Forskjellige menyer
**Løsning:**
```bash
# Kjør auto-sync
bash /root/.openclaw/workspace/scripts/auto-sync-mission-control.sh
```

---

## 📊 OVERVÅKING

**Logg-fil:** `/var/log/mission-control-auto-sync.log`  
**Siste sync:** `mission-control/public/.last-auto-sync`  
**Verifisering:** Kjør `mission-control-sync.sh` for rapport

---

## ✍️ ENDRINGSHISTORIK

| Dato | Versjon | Endring |
|------|---------|---------|
| 2026-02-24 | 3.1 | Laget sync-regel og auto-sync system |

---

## 🤖 AUTONOM DRIFT

**Jeg (BaarliClaw) skal:**
1. ✅ Kjøre auto-sync etter hver endring jeg gjør
2. ✅ Verifisere konsistens før deploy
3. ✅ Rapportere avvik umiddelbart
4. ✅ Aldri la utdaterte versjoner eksistere

**Denne regelen er BINDENDE og skal følges til punkt og prikke!**
