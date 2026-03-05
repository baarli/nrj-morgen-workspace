# NRJ Morgen Dashboard - System Dokumentasjon

## 🎯 Hva skal oppdateres

**IKKE sakslista** - Dette er et eget system for dashboard-paneler.

**KORREKT:** NRJ Statistikk panel på dashboardet (nrjmorgen.com)
- Panel ID: `0b1f6b6b-3fde-434b-b7c8-dcf306beea72`
- Plassering: Dashboard (ikke sakslista)
- Type: `agenda_items` med `is_pinned: true`

---

## 📁 Hvor finner du scripts

**Hovedscript for oppdatering:**
```
/root/.openclaw/workspace/scripts/update_nrj_dashboard.py
```

**Andre relevante scripts:**
```
/root/.openclaw/workspace/scripts/fetch_nielsen_live.py      # Kun Nielsen radio
/root/.openclaw/workspace/scripts/fetch_podtoppen_live.py    # Kun Podtoppen
/root/.openclaw/workspace/scripts/fetch_nrj_dashboard_stats.py  # Gammelt script (oppretter nytt item)
```

**VIKTIG:** Bruk alltid `update_nrj_dashboard.py` - dette oppdaterer eksisterende panel, ikke oppretter nytt.

---

## 🔌 API-er og kilder

### 1. Nielsen Radio Data (API)
**URL:**
```
https://eu-iport.nielsen-iwatch.com/api/Chart?dataid=8eb6daca-1266-4af8-8e8f-f39107dc63fb&publish_key=bd551853-f42b-4b86-813a-79faf3a718e9
```

**Hva hentes:**
- Daglig gjennomsnittlig rekkevidde for NRJ
- Historiske uke-data (uke 1-7 for 2026)
- Siste tilgjengelige uke: **Uke 7** (publiseres med 1 ukes forsinkelse)

**Dataformat:**
```json
{
  "seriesMDData": [{
    "data2D": [
      ["NRJ", "53", "46", "64", "62", "56", "52", "63", "69"]
      //        ^uke52 ^uke1  ^uke2  ^uke3  ^uke4  ^uke5  ^uke6  ^uke7
    ]
  }]
}
```

**Når oppdateres:**
- Nielsen publiserer data med 1 ukes forsinkelse
- Uke 8 blir tilgjengelig neste uke (ca. onsdag/torsdag)

---

### 2. Podtoppen Podkast Data (CSV Export)
**URL:**
```
https://podtoppen.tnslistene.no/export.php
```

**Hva hentes:**
- Rangering for "NRJ Morgen Podkast"
- Unike enheter (lyttere)
- Nedlastet/strømmet antall
- Utgiver (Bauer Media)

**Dataformat:** CSV med semikolon-separator, latin-1 encoding
```csv
Podcast;Produsent;Plattform;Antall_enheter;Nedlastet_strømmet
NRJ Morgen Podkast;Bauer Media;Total;16470;33405
```

**Når oppdateres:**
- Ukentlig (vanligvis onsdag)
- Sjekk https://podtoppen.tnslistene.no/ for siste oppdatering

---

## 🗄️ Supabase Konfigurasjon

**URL:** `https://kvniauxokdtmpvjtfnej.supabase.co`

**Tabell:** `agenda_items`

**Tenant ID:** `a0000000-0000-0000-0000-000000000001`

**Bruker ID (BaarliClaw):** `10aa1508-6d52-490c-8ae5-fa3da9a152c4`

**Panel ID:** `0b1f6b6b-3fde-434b-b7c8-dcf306beea72`

**Query for å finne panel:**
```sql
SELECT * FROM agenda_items 
WHERE tenant_id = 'a0000000-0000-0000-0000-000000000001'
AND title LIKE '%NRJ%Statistikk%'
ORDER BY created_at DESC
LIMIT 1;
```

---

## 🔄 Hvordan oppdatere

### Manuell oppdatering:
```bash
cd /root/.openclaw/workspace/scripts
python3 update_nrj_dashboard.py
```

### Hva scriptet gjør:
1. Finner eksisterende panel (ID: 0b1f6b6b-3fde-434b-b7c8-dcf306beea72)
2. Henter siste data fra Nielsen API
3. Henter siste data fra Podtoppen
4. Genererer HTML for dashboard-visning
5. Oppdaterer eksisterende panel (PATCH, ikke POST)

### Output:
```
📊 NRJ STATISTIKK DASHBOARD - OPPDATERING
============================================================
🔍 Søker etter eksisterende NRJ Statistikk item...
   ✅ Fant eksisterende item: 0b1f6b6b-3fde-434b-b7c8-dcf306beea72
📻 Henter NRJ radio-tall fra Nielsen...
   ✅ 69,000 daglige lyttere (uke 7)
🎧 Henter NRJ Morgen Podkast tall fra Podtoppen...
   ✅ Rangering: #62
   ✅ 16,470 unike lyttere
💾 Oppdaterer eksisterende item...
🎉 NRJ STATISTIKK DASHBOARD OPPDATERT!
```

---

## 📊 Data som vises

### Radio-panel:
- Daglige lyttere (siste uke)
- Gjennomsnitt 2026
- Trend fra forrige uke (%)
- Kilde: Nielsen PPM API

### Podkast-panel:
- Podtoppen rangering
- Unike lyttere
- Nedlastet/strømmet
- Kilde: Kantar/TNS Podtoppen

### Sist oppdatert:
- Vises i header: DD.MM.YYYY HH:MM
- Footer viser datakilder

---

## ⚠️ Viktige notater

1. **IKKE bruk `fetch_nrj_dashboard_stats.py`** - Dette oppretter NYTT item i sakslista
2. **ALLTID bruk `update_nrj_dashboard.py`** - Dette oppdaterer EKSISTERENDE panel
3. **Sjekk alltid at panel ID er:** `0b1f6b6b-3fde-434b-b7c8-dcf306beea72`
4. **Nielsen data har 1 ukes forsinkelse** - Uke 8 kommer neste uke
5. **Podtoppen oppdateres ukentlig** - Vanligvis onsdag

---

## 🔗 Nyttige lenker

- **Dashboard:** https://nrjmorgen.com
- **Nielsen API:** https://eu-iport.nielsen-iwatch.com/api/Chart
- **Podtoppen:** https://podtoppen.tnslistene.no/
- **Supabase:** https://kvniauxokdtmpvjtfnej.supabase.co

---

## 📅 Oppdateringsskjema

| Kilde | Frekvens | Dag | Tid |
|-------|----------|-----|-----|
| Nielsen | Ukentlig | Onsdag/Torsdag | Ettermiddag |
| Podtoppen | Ukentlig | Onsdag | Formiddag |

**Anbefalt:** Sjekk og oppdater hver onsdag kl. 14:00

---

## 🆘 Feilsøking

### Hvis panel ikke finnes:
```python
# Sjekk om panel eksisterer
SELECT id, title FROM agenda_items 
WHERE title LIKE '%NRJ%Statistikk%'
AND tenant_id = 'a0000000-0000-0000-0000-000000000001';
```

### Hvis Nielsen API feiler:
- Sjekk at URL er tilgjengelig i browser
- Verifiser `publish_key` parameter
- Sjekk at User-Agent header er satt

### Hvis Podtoppen feiler:
- Sjekk at https://podtoppen.tnslistene.no/export.php er tilgjengelig
- Verifiser at CSV-format ikke har endret seg
- Sjekk encoding (latin-1)

---

**Sist oppdatert:** 2026-02-24
**Dokumentasjon opprettet av:** BaarliClaw
**Formål:** Garantert riktig oppdatering av NRJ Dashboard
