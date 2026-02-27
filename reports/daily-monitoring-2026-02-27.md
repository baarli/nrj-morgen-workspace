# NRJ Morgen – Daglig Overvåking
**Dato:** 27. februar 2026 (CET: 06:00)  
**Utført av:** BaarliClaw Autonomous System

---

## 🔴 KRITISK FUNN: Ingen saker i Supabase!

**Status:** Supabase returnerer **TOM liste** for agenda_items.  
**Konsekvens:** Morning Routine har IKKE kjørt i natt.

**Mulige årsaker:**
1. Morning Routine cron-job feilet
2. Brave Search API nede/mangler
3. Supabase autentisering feilet
4. Script-feil i morning-routine-v2.1.py

**Tiltak nødvendig:**
- [ ] Verifiser cron-job status
- [ ] Sjekk Brave API key konfigurasjon
- [ ] Kjør morning-routine manuelt
- [ ] Verifiser Supabase credentials

---

## 1. 🎯 KONKURRENT-RADAR

### P4 – Radiofrokost
**Hovedvinkler:**
- **Gjest:** Jonas Hoff Oftebro (skuespiller)
- **Tema:** Penisprotese i norsk TV/film, het sexscene
- **Stil:** Kjendis-intervju med sjokkfaktor

**Analyse:**
- ✅ Sterk gjest (Oftebro er aktuell)
- ✅ Tabloid vinkel (sex/penis)
- ⚠️ Kan oppleves som "gammeldags" sjokk-journalistikk
- **NRJ mulighet:** Gå dypere – hva med psykologien bak slike scener?

### P5 – Frokostshowet
**Hovedvinkler:**
- Spotify Wrapped-refleksjon
- Lyttealder-sjokk
- Julebords-humor

**Analyse:**
- ✅ Selvironi (alderskompleks)
- ✅ Relatérbart (alle har Spotify)
- ⚠️ Lite "nyhet" – mer "prat"
- **NRJ mulighet:** Konkret musikk-analyse, ikke bare prat

### NRK P3 – P3morgen
**Hovedvinkler:**
- Jonas, Arin, Henning – etablert trio
- Musikkfokus (Portugal. The Man, Madison Beer)
- Live-musikk (P3 Live)

**Analyse:**
- ✅ Sterk musikkprofil
- ✅ Live-musikk er unikt
- ⚠️ Mindre fleksible (NRK-standarder)
- **NRJ mulighet:** Raskere, råere, mer ufiltrert

### Morgenklubben (Radio Norge)
**Hovedvinkler:**
- Loven & Co – etablert merkevare
- 80-90-2000-talls musikk
- 234k+ følgere på Facebook

**Analyse:**
- ✅ Stor følgerskare
- ✅ Nostalgi-fokus
- ⚠️ Eldre målgruppe (nostalgi = 35+)
- **NRJ mulighet:** Fremtidsorientert, ikke fortid

### 🎖️ KONKURRENT-SVAKHETER NRJ KAN UTNYTTE:

| Konkurrent | Svakhet | NRJ Mulighet |
|------------|---------|--------------|
| P4 | Forutsigbar gjeste-struktur | Uventede gjester, "stunt"-intervjuer |
| P5 | Lite nyhets-fokus | Være først ute med breaking |
| P3 | Tungrodd (NRK) | Rask produksjon, samme dag |
| Morgenklubben | Eldre målgruppe | Eie 18-35 segmentet fullstendig |

---

## 2. ✅ KVALITETS-SJEKK

### Supabase Status
```
Tabell: agenda_items
Tenant: a0000000-0000-0000-0000-000000000001
Siste saker: INGEN FUNNET
```

**Forventet:** 8 saker + 3 segmenter = 11 items  
**Faktisk:** 0 items  
**Status:** 🔴 **KRITISK FEIL**

### Morning Routine v2.1 Config
```
Antall saker: 15 per dag
Kategorier: 5 (maks 3 per kategori)
Maks alder: 48 timer
Titler: OpenAI, maks 7 ord
```

### Fakta-sjekk (automatisert)
- [ ] Kilder verifisert
- [ ] Publiseringsdatoer sjekket
- [ ] Bilde-URLer validert
- [ ] Lenker testet

**Status:** Kan ikke verifisere – ingen saker å sjekke

---

## 3. 🔮 TIDLIG VARSLING

### Kommende Events (neste 7 dager)

| Dato | Event | Potensial | Forberedelse |
|------|-------|-----------|--------------|
| Mars 2026 | Paradise Hotel ny sesong | 🔥🔥🔥 HØY | Forhåndsintervjuer, deltakerprofiler |
| 22. mars 2026 | Spellemannprisen Operaen | 🔥🔥🔥 HØY | Nominerte-sjekk, vinner-tipping |
| Løpende | Farmen Kjendis 2026 | 🔥🔥 MEDIUM | Deltaker-drama, exit-rapporter |
| Løpende | Kompani Lauritzen 2026 | 🔥🔥 MEDIUM | Dag Otto/Kristian Ødegård intervjuer |

### "Hva Hvis"-Scenarier

**Scenario A: Paradise Hotel-deltaker trekker seg**
- **Sannsynlighet:** Medium (skjer hver sesong)
- **Tiltak:** Ha backup-deltaker klar, forhåndsintervju
- **Vinkel:** "Hvorfor sa hun nei til Paradise?"

**Scenario B: Spellemann-skandale**
- **Sannsynlighet:** Lav, men høy impact
- **Tiltak:** Overvåke nominerte, klar fakta-sjekk
- **Vinkel:** "Den kontroversielle vinneren"

**Scenario C: Farmen-kjendis med skandale**
- **Sannsynlighet:** Høy (reality = drama)
- **Tiltak:** Overvåke deltakerne før sending
- **Vinkel:** "Dette visste du ikke om Farmen-stjernen"

---

## 4. 👥 LYTTER-INNSIKT

### Podtoppen Data (siste tilgjengelig)
```
Rangering: #62
Unike lyttere: 16,470
Uke: 7, 2026
Trend: Stabil
```

### Nielsen Radio (siste tilgjengelig)
```
Uke: 7, 2026
Daglige lyttere: 69,000
Status: Venter på uke 8-data
```

### Temaer som Treffer (basert på historikk)
1. **Reality-drama** – alltid høyt engasjement
2. **Kjendis-brudd** – deling og kommentarer
3. **Musikknyheter** – særlig norsk hip-hop/pop
4. **Influencer-kontroverser** – ung målgruppe engasjerer

### Tilbakemeldinger å Ta Med
- Lyttere vil ha **mer musikk-analyse**
- Ønske om **flere live-intervjuer**
- **Kortere segmenter** (under 3 minutter)

---

## 5. 🌐 NETTVERKSMULIGHETER

### Kontakter å Følge Opp

**Høy prioritet:**
- Dag Otto Lauritzen (Kompani Lauritzen) – aktuell med ny sesong
- Kristian Ødegård – alltid god på radio
- Paradise Hotel-produsenter – forhåndstilgang

**Medium prioritet:**
- Spellemann-nominerte artister – intervju før prisutdeling
- Farmen Kjendis-deltakere – profilbygging

**Ny potensiell:**
- TikTok-stjerner på vei opp (18-35 målgruppe)
- Norske Netflix-stjerner (internasjonal rekkevidde)

### Samarbeidsmuligheter
1. **PodPlay** – podcast-samarbeid (allerede i bruk)
2. **VG/Nettavisen** – nyhetsdeling
3. **TV2** – cross-promo med reality-serier
4. **Universal/Sony Music** – eksklusive låter

---

## 6. 📅 EVENT-PLANLEGGING

### Kommende Eventer å Forberede

**Spellemannprisen (22. mars 2026)**
- [ ] Book intervju med 3 nominerte
- [ ] Lag "vinner-tipping" segment
- [ ] Forbered "beste øyeblikk"-montasje
- [ ] Koordiner med Operaen for bak-scenen-tilgang

**Paradise Hotel Premiere (mars 2026)**
- [ ] Få deltakerliste på forhånd
- [ ] Forhåndsintervju med 2-3 deltakere
- [ ] Lag "møt deltakerne"-serie
- [ ] Planlegg live-reaksjon på første episode

**Farmen Kjendis (pågående)**
- [ ] Ukentlig oppfølging med eks-deltakere
- [ ] Lag "ukens drama"-oppsummering
- [ ] Book intervju med exit-deltakere samme dag

---

## 📊 OPPSUMMERING

| Kategori | Status | Prioritet |
|----------|--------|-----------|
| Konkurrent-radar | 🟡 OK | Medium |
| Kvalitets-sjekk | 🔴 KRITISK | HØYEST |
| Tidlig varsling | 🟢 OK | Medium |
| Lytter-innsikt | 🟡 OK | Medium |
| Nettverk | 🟢 OK | Lav |
| Event-planlegging | 🟡 OK | Medium |

### Umiddelbare Tiltak
1. **🔴 KRITISK:** Fiks Morning Routine – ingen saker i dag!
2. Verifiser Brave Search API key
3. Kjør morning-routine-v2.1.py manuelt
4. Sjekk cron-job logg for feil

### Neste Overvåking
- **Neste sjekk:** 28. februar 2026, 06:00 CET
- **Fokus:** Verifisere at Morning Routine kjører korrekt

---

*Rapport generert av BaarliClaw Autonomous System*  
*Mission Control: https://creative-muffin-dcf3a0.netlify.app*
