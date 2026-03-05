# Morning Routine v2.1 - Oppdateringsoversikt

**Dato:** 2026-02-24  
**Versjon:** 2.1  
**Endringer:** 15 saker per dag, bedre spredning, maks 3 per kategori

---

## ✅ Fullførte Oppdateringer

### 1. Script-oppdateringer

| Fil | Endringer |
|-----|-----------|
| `morning-routine-v2.1.py` | Nytt script med 15 saker, 5 kategorier, maks 3 per kategori |
| `integrated-morning-routine.sh` | Oppdatert til v2.1, bruker nytt script |
| `add-top10-tomorrow.py` | Støtter både top_10 og top_15 |

### 2. Dokumentasjon oppdatert

| Fil | Endringer |
|-----|-----------|
| `MEMORY.md` | Morning Routine v2.1 seksjon lagt til |
| `AGENTS.md` | Morning Routine v2.1 konfigurasjon lagt til |
| `TOOLS.md` | Morning Routine v2.1 seksjon lagt til |
| `MORNING_ROUTINE_V2.md` | Statistikk oppdatert (15 saker, spredning) |
| `nrj-morgen-config.md` | Fullstendig oppdatert med v2.1 info |

### 3. Konfigurasjon

**Antall saker:** 15 per dag (økt fra 10)  
**Kategorier:** 5  
**Maks per kategori:** 3 saker  
**Alder:** Maks 48 timer  
**Tittel-lengde:** Maks 7 ord  

### 4. Kategorier

1. **Reality TV** (3 saker)
   - Farmen Kjendis
   - Paradise Hotel
   - Kompani Lauritzen
   - Love Island

2. **Kjendis Drama** (3 saker)
   - Brudd og forhold
   - Avsløringer
   - Reaksjoner

3. **Film & TV** (3 saker)
   - Premierer
   - Rød løper
   - TV-nyheter

4. **Musikk** (3 saker)
   - Spellemannprisen
   - VG-lista
   - P3 Gull

5. **Internasjonalt** (3 saker)
   - Daily Mail
   - TMZ
   - E! Online
   - People

### 5. Krav oppfylt

- ✅ 15 saker per dag
- ✅ God spredning (maks 3 per kategori)
- ✅ Maks 48 timer gamle
- ✅ OpenAI titler (maks 7 ord)
- ✅ Ingen duplikater
- ✅ Automatisk filtrering av upassende innhold

---

## 🚀 Bruk

### Manuell kjøring:
```bash
# Morning Routine v2.1
python3 /root/.openclaw/workspace/scripts/morning-routine-v2.1.py

# Auto-insert til Supabase
python3 /tmp/add-top10-tomorrow.py
```

### Integrert rutine:
```bash
bash /root/.openclaw/workspace/scripts/integrated-morning-routine.sh
```

---

## 📊 Resultat fra test

- **Totalt i pot:** 207 saker
- **Unike saker:** 163
- **Topp 15 valgt:** 15
- **Spredning:** 3 saker per kategori
- **Tid brukt:** ~30 sekunder

---

## 📝 Viktige filer

| Fil | Beskrivelse |
|-----|-------------|
| `/root/.openclaw/workspace/scripts/morning-routine-v2.1.py` | Hovedscript |
| `/root/.openclaw/workspace/scripts/integrated-morning-routine.sh` | Integrert rutine |
| `/root/.openclaw/workspace/.config/nrj-morgen-config.md` | Konfigurasjon |
| `/root/.openclaw/workspace/docs/MORNING_ROUTINE_V2.md` | Dokumentasjon |

---

**Systemet er klart for produksjon!** 🎉
