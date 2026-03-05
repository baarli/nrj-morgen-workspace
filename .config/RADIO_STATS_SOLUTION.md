# 📊 Radio Stats Updater - Løsning

## Implementert: 2026-02-21

### 🎯 Funksjonalitet

Automatisk henting og oppdatering av:
1. **Nielsen radiotall** - Hver mandag kl 15:00
2. **Podtoppen tall** - Hver onsdag kl 12:05

### 📁 Filer

```
/root/.openclaw/workspace/scripts/
└── radio-stats-updater.py          # Hovedscript
```

### 📅 Cron-jobber

| Jobb | Tid | Formål |
|------|-----|--------|
| 📊 RADIOTALL | Mandag 15:00 | Hent Nielsen-tall |
| 🎧 PODTOPPEN | Onsdag 12:05 | Hent podkast-tall |

### 🔧 Bruk

```bash
# Hent Nielsen-tall
cd /root/.openclaw/workspace/scripts
python3 radio-stats-updater.py --nielsen

# Hent Podtoppen-tall
python3 radio-stats-updater.py --podtoppen

# Hent begge
python3 radio-stats-updater.py --both
```

### 📊 Data som hentes

**Nielsen:**
- Ukentlig rekkevidde
- Daglig rekkevidde
- Markedsandel
- Trend

**Podtoppen:**
- Ukentlige lyttere
- Endring i prosent
- Totalt nedlastninger
- Rangering på topplisten

### 💾 Lagring

Data lagres på to måter:
1. **Supabase** (hvis tilgjengelig) - Som agenda_items med category="STATS"
2. **Lokalt** (fallback) - JSON-filer i `/tmp/radio_stats/`

### 📝 Neste steg for full implementasjon

For å få **ekte data** (ikke simulert), må følgende implementeres:

#### 1. Nielsen iPort Autentisering
```python
# Krever:
# - Brukernavn/passord for dashboard-eu-iport.nielsen-iwatch.com
# - Cookie-basert autentisering eller API-nøkkel
# - Scraping av HTML eller API-kall
```

#### 2. Podtoppen Scraping
```python
# Krever:
# - HTTP request til https://podtoppen.no/podcasts.php?pid=3873
# - HTML-parsing for å finne tallene
# - Håndtering av uke-basert data
```

### ✅ Status

- ✅ Script opprettet
- ✅ Cron-jobber satt opp
- ✅ Lokal lagring fungerer
- ⚠️ Krever autentisering for ekte data

### 🚀 Klar for produksjon

Systemet er klar til å kjøre automatisk, men vil bruke **simulerte data** inntil autentisering er på plass.

Vil du at jeg skal:
1. Implementere faktisk innlogging for Nielsen?
2. Sette opp HTML-scraping for Podtoppen?
3. Lage en manuell import-funksjon?
