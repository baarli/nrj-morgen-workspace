# NRJ Morgen - Morning Routine v2.0 Dokumentasjon

**Oppdatert:** 2026-02-24
**Versjon:** 2.0

---

## 🎯 Oversikt

Morning Routine v2.0 henter nyheter fra **7 kilder**, samler i en **pot**, og velger de **10 beste** til sakslista hver dag.

## 📡 Kilder

| Kilde | Type | Søk |
|-------|------|-----|
| **Morgenrutinen** | 47 målrettede søk | Kjendis, reality, influencere |
| **VG Rampelys** | Site-søk | vg.no/rampelys |
| **Nettavisen Kjendis** | Site-søk | nettavisen.no/kjendis |
| **TV2 Underholdning** | Site-søk | tv2.no/underholdning |
| **Dagbladet Kjendis** | Site-søk | dagbladet.no/kjendis |
| **Se og Hør** | Site-søk | seher.no |
| **730.no** | Site-søk | 730.no |

---

## 🔄 Prosess

```
1. HENT → Alle kilder (maks 48 timer gamle)
   ↓
2. SAMLE → I pot (unike saker)
   ↓
3. SCORE → Underholdningsverdi (0-100)
   ↓
4. SORTER → Etter score
   ↓
5. VELG → Topp 10
   ↓
6. INSERT → Til Supabase
```

---

## 🤖 OpenAI Tittelgenerering

Alle titler genereres med OpenAI GPT-4o-mini:

### Krav til titler:
- **Maks 7 ord**
- **Catchy og underholdende**
- **Norsk språk**
- **Fokus på det mest interessante**

### Eksempel:
```
Original: "Netflix-dokumentar avslører sjokkerende detaljer fra Tyra Banks i America's Next Top Model"
→ "Netflix avslører Tyra Banks-skandale"
```

### API
- **Modell:** GPT-4o-mini
- **Temperatur:** 0.7
- **Max tokens:** 50

---

## ✅ Inkluderes (Lett underholdning)

- Kjendisnyheter (brudd, drama, avsløringer)
- Reality-TV (Farmen, Paradise Hotel, Kompani Lauritzen)
- Influencere og profiler
- Film og musikk (premierer, priser)
- Kongehus (lett underholdning)
- Sosiale medier og viral content
- Premier og rød løper

## ❌ Ekskluderes (KUTTET)

- **Sport** (fotball, ski, håndball, etc.)
- **Hard politikk** (regjering, storting, lovforslag)
- **Krig og konflikt**
- **Harde nyheter** (drap, ulykker, tragedier)
- **Økonomi og finans**
- **Korona og helse**

---

## 📊 Scoring

Saker scores etter:

| Faktor | Poeng |
|--------|-------|
| Brudd/drama | +10 |
| Avsløring/hemmelig | +10 |
| Sterke følelser (raser, tårer) | +10 |
| Overraskelse/sjokk | +10 |
| Pinlig øyeblikk | +10 |
| Kjent navn (Marius, Mette-Marit, etc.) | +15 |

**Maks score:** 100

---

## 🚀 Bruk

### Manuell kjøring:
```bash
cd /root/.openclaw/workspace/scripts
python3 morning-routine-v2.py
```

### Auto-insert til Supabase:
```bash
python3 auto-insert-top10.py
```

### Full Morning Routine:
```bash
bash integrated-morning-routine.sh
```

---

## 📁 Filer

| Fil | Beskrivelse |
|-----|-------------|
| `morning-routine-v2.py` | Hovedscript - henter fra alle kilder |
| `auto-insert-top10.py` | Wrapper - legger topp 10 i Supabase |
| `brave-news-search.py` | Originalt script (beholdt for bakoverkompatibilitet) |

---

## 🔑 API Nøkler

- **Brave Search:** `BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev`
- **Supabase:** Service key i `.credentials/nrj-morgen.env`

---

## ⏰ Cron Job

Morning Routine kjører automatisk:
- **Tid:** 04:50 CET (hverdager)
- **Jobb:** `NRJ MORGEN – Konsolidert Morgen-Rutine (04:50)`

---

## 📈 Statistikk

Eksempel fra testkjøring:
- **Totalt i pot:** 207 saker
- **Unike saker:** 163
- **Topp 15 valgt:** 15 (økt fra 10)
- **Tid brukt:** ~30 sekunder
- **Spredning:** 3 saker per kategori (maks)

---

## 📝 Viktig

- Alle saker er **maks 48 timer gamle**
- **Freshness=pd** (past day) = siste 24 timer
- **Ingen duplikater** (sjekk på URL)
- **Automatisk filtrering** av upassende innhold
- **15 saker per dag** med god spredning på temaer
- **Maks 3 saker per kategori** for variasjon
