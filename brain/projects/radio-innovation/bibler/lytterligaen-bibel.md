# 📚 LYTTERLIGAEN BIBEL - Komplett Produksjonsguide

**Segment:** LytterLigaen  
**Type:** Gamifisert radiodeltakelse  
**Varighet:** 2 minutter (daglig oppdatering)  
**Frekvens:** Daglig + månedlig finale  
**Sist oppdatert:** 2026-03-05

---

## 🏆 SEGMENTOVERSIKT

### Hva er LytterLigaen?
En "liga" hvor lyttere tjener poeng for engasjement. Topplisten vises daglig, og vinneren hver måned får spesielle premier.

### Hvorfor fungerer det?
- **Konkurranse:** Mennesker elsker å konkurrere
- **Belønning:** Følelse av å få noe tilbake
- **Community:** Bygger lojalitet rundt showet
- **Gjenkjennelse:** Å bli sett og verdsatt

---

## 📝 MANUSMAL (Daglig)

### Intro (20 sekunder)
```
[Programleder]:
"God morgen! Tid for LYTTERLIGAEN - hvor dere tjener poeng 
for å være fantastiske lyttere!"

"La oss se hvem som leder denne uken..."
[lydeffekt: trommevirvel]
```

### Toppliste (60 sekunder)
```
[Programleder]:
"På 5. plass: [NAVN] med [X] poeng! Gratulerer!"
[lydeffekt: applaus]

"På 4. plass: [NAVN] med [X] poeng!"
[lydeffekt: applaus]

"På 3. plass: [NAVN] med [X] poeng!"
[lydeffekt: applaus + fanfare]

"På 2. plass: [NAVN] med [X] poeng!"
[lydeffekt: applaus + fanfare]

"Og på 1. plass... [NAVN] med [X] poeng!"
[lydeffekt: fanfare + applaus]

"Gratulerer til alle!"
```

### Hvordan tjene poeng (30 sekunder)
```
[Programleder]:
"Vil DU komme på lista? Her er hvordan du tjener poeng:"

"Send inn morsomme kommentarer: 10 poeng"
"Delta i avstemninger: 5 poeng"
"Tipse om nyheter: 15 poeng"
"Delta på quiz: 20 poeng"
"Invitere venner: 25 poeng"

"Meld deg på via Telegram @Vev_kompis_bot!"
```

### Månedlig vinner (10 sekunder)
```
"Husk: Vinneren denne måneden får [PREMIE]!"
"Forrige måneds vinner: [NAVN] - gratulerer!"
```

---

## 🎯 POENGSYSTEM

### Hvordan tjene poeng
| Handling | Poeng | Begrunnelse |
|----------|-------|-------------|
| Sende inn kommentar | 10 | Engasjement |
| Delta i avstemning | 5 | Interaksjon |
| Tipse om nyhet | 15 | Verdi for showet |
| Delta på quiz | 20 | Aktiv deltakelse |
| Invitere venn (som blir aktiv) | 25 | Vekst |
| Være med på MorgenRoulette | 50 | Premium-engasjement |
| Vinne quiz | 100 | Ekstraordinær innsats |

### Bonus-poeng
- **Fødselsdag:** 50 poeng på din bursdag
- **Ukentlig streak:** 20 poeng for 7 dager på rad
- **Månedens bidrag:** 200 poeng for beste bidrag

---

## 🏅 PREMIER

### Ukentlig (Top 3)
1. **1. plass:** NRJ-goodiebag + shoutout
2. **2. plass:** Spotify Premium 1 måned
3. **3. plass:** NRJ-kopp + klistremerker

### Månedlig (Vinner)
- **Tittel:** "Månedens NRJ-ambassadør"
- **Premie:** Være gjesteprogramleder i 30 minutter
- **Bonus:** Velge 3 sanger på rad
- **Opplevelse:** Møte programlederne + omvisning
- **Gave:** Signert t-skjorte + goodiebag

### Sesong (Kvartalsvis)
- **Tittel:** "NRJ Legend"
- **Premie:** VIP-billetter til NRJ-konsert + backstage
- **Permanent:** Navn på "Hall of Fame" i studio

---

## 🛠️ TEKNISK SETUP

### Database (Supabase)
```sql
CREATE TABLE lytterligaen_participants (
    id UUID DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    phone TEXT,
    telegram_id TEXT,
    email TEXT,
    registered_at TIMESTAMP DEFAULT NOW(),
    total_points INTEGER DEFAULT 0,
    monthly_points INTEGER DEFAULT 0,
    streak_days INTEGER DEFAULT 0,
    last_activity DATE,
    PRIMARY KEY (id)
);

CREATE TABLE lytterligaen_points_log (
    id UUID DEFAULT gen_random_uuid(),
    participant_id UUID REFERENCES lytterligaen_participants(id),
    action TEXT NOT NULL,
    points INTEGER NOT NULL,
    date TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (id)
);

CREATE TABLE lytterligaen_leaderboard (
    id UUID DEFAULT gen_random_uuid(),
    participant_id UUID REFERENCES lytterligaen_participants(id),
    week_number INTEGER,
    month TEXT,
    year INTEGER,
    points INTEGER,
    rank INTEGER,
    PRIMARY KEY (id)
);
```

### Telegram Bot Funksjoner
```python
# lytterligaen-bot.py
from telegram import Update
from telegram.ext import CallbackContext

def register_user(update: Update, context: CallbackContext):
    """Registrer ny deltaker"""
    user = update.effective_user
    # Lagre i database
    # Send velkomstmelding
    
def add_points(user_id, action, points):
    """Legg til poeng for handling"""
    # Oppdater database
    # Send bekreftelse til bruker
    
def show_leaderboard(update: Update, context: CallbackContext):
    """Vis toppliste"""
    # Hent top 5 fra database
    # Formater pent
    # Send til bruker
    
def show_my_points(update: Update, context: CallbackContext):
    """Vis brukerens egne poeng"""
    # Hent fra database
    # Send personlig oppdatering
```

### Dashboard (for programledere)
```python
# leaderboard-dashboard.py
import streamlit as st
from supabase import create_client

def show_dashboard():
    st.title("🏆 LytterLigaen Dashboard")
    
    # Hent data
    supabase = create_client(url, key)
    leaderboard = supabase.table('lytterligaen_leaderboard').select('*').execute()
    
    # Vis toppliste
    st.subheader("Dagens Toppliste")
    st.table(leaderboard.data[:10])
    
    # Vis statistikk
    st.subheader("Statistikk")
    col1, col2, col3 = st.columns(3)
    col1.metric("Totalt deltakere", len(participants))
    col2.metric("Aktive denne uken", active_this_week)
    col3.metric("Total poeng utdelt", total_points)
```

---

## 📋 DAGLIG PRODUKSJONSFLYT

### Kl 07:00 (30 min før sending)
- [ ] Kjør script for å oppdatere poeng
- [ ] Generer toppliste
- [ ] Forbered manus

### Kl 07:25 (5 min før)
- [ ] Sjekk at data er korrekt
- [ ] Test uttale av navn

### Kl 07:30 (Sending)
- [ ] Kjør intro
- [ ] Les top 5
- [ ] Forklar hvordan tjene poeng
- [ ] Avslutt

### Etter sending
- [ ] Oppdater sosiale medier med toppliste
- [ ] Send melding til top 3 (gratulasjon)

---

## 📊 MÅNEDLIG FINALE

### Format (Siste fredag i måneden)
```
[Programleder]:
"I dag er det MÅNEDLIG FINALE i LytterLigaen!"

"La oss se hvem som vinner tittelen 'Månedens NRJ-ambassadør'..."
[lydeffekt: spenning]

"Og vinneren er... [NAVN] med [X] poeng!"
[lydeffekt: fanfare + applaus]

"Gratulerer! Du vinner:"
- Være gjesteprogramleder i 30 min
- Velge 3 sanger
- Møte oss i studio
- Signert t-skjorte

"Vi kontakter deg på Telegram!"
```

### Etter finale
- [ ] Kontakt vinner
- [ ] Planlegg gjesteprogramleder-opptreden
- [ ] Reset månedlige poeng (behold totale)
- [ ] Start ny måned

---

## 🎯 MÅLING AV SUKSESS

### KPI-er
| Måling | Mål | Hvordan måle |
|--------|-----|--------------|
| Registrerte deltakere | 100+ første måned | Database |
| Aktive deltakere (ukentlig) | 50%+ | Aktivitet |
| Gjennomsnittlig poeng per deltaker | Stigende | Database |
| Retensjon (måned 2) | 60%+ | Sammenligning |

---

## ⚠️ RISIKO OG LØSNINGER

| Risiko | Løsning |
|--------|---------|
| Juks med poeng | Manuell verifisering av store bidrag |
| For få deltakere | Markedsføring, enklere påmelding |
| For komplekst | Start enkelt, legg til funksjoner etterhvert |
| Premie-kostnader | Sponsorer, partnerskap |

---

## 💡 PRO-TIPS

1. **Start enkelt** - Ikke for mange måter å tjene poeng fra start
2. **Vær konsekvent** - Oppdater toppliste daglig, samme tid
3. **Feir vinnere** - Gjør dem til helter
4. **Lytt til feedback** - Juster poengsystem basert på hva som fungerer
5. **Gjør det sosialt** - La deltakere se hverandre, ikke bare poeng

---

## 🚀 NESTE STEG

### Fase 1: MVP (Uke 1-2)
- [ ] Sette opp database
- [ ] Lage Telegram-bot (basis)
- [ ] Teste med 10 interne deltakere

### Fase 2: Soft Launch (Uke 3-4)
- [ ] Annonsere på sendingen
- [ ] Åpne for ekte lyttere
- [ ] Måle engasjement

### Fase 3: Full Launch (Måned 2+)
- [ ] Alle funksjoner aktive
- [ ] Første månedlige finale
- [ ] Evaluere og justere

---

**Klar til å starte ligaen?** 🏆🎙️
