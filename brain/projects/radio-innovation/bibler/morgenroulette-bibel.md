# 📚 MORGENROULETTE BIBEL - Komplett Produksjonsguide

**Segment:** MorgenRoulette  
**Type:** AI-drevet lytterutfordring  
**Varighet:** 3-4 minutter  
**Frekvens:** Daglig, 07:30  
**Sist oppdatert:** 2026-03-05

---

## 🎯 SEGMENTOVERSIKT

### Hva er MorgenRoulette?
En virtuell "rulett" velger hver morgen en tilfeldig lytter som har meldt seg på. Den utvalgte får 60 sekunder på seg til å fullføre en morsom utfordring direkte på luften.

### Hvorfor fungerer det?
- **Nysgjerrighet:** "Hvem blir dagens vinner?"
- **Engasjement:** Lytteren blir hovedperson
- **FOMO:** Hvis du ikke lytter, går du glipp av noe unikt
- **Underholdning:** Uforutsigbart, autentisk, morsomt

---

## 📝 MANUSMAL

### Intro (30 sekunder)
```
[Programleder 1]: 
"God morgen! Klokka er 07:30 og det betyr én ting... 
[lydeffekt: rulett-surr] ...det er tid for MORGENROULETTE!"

[Programleder 2]:
"I dag har [X] lyttere meldt seg på. La oss se hvem ruletten velger..."
[lydeffekt: rulett-stopper]

[Programleder 1]:
"Og vinneren er... [NAVN]! Gratulerer!"
```

### Utfordring (60 sekunder)
```
[Programleder 2]:
"[NAVN], du har 60 sekunder på deg. Er du klar?"

[Lytter]: "Ja!"

[Programleder 1]:
"Din utfordring er: [LES UT FORDRING]. 
Tiden starter... NÅ!"
[lydeffekt: tikking]

[60 sekunder med lytter som prøver å fullføre utfordringen]

[Programleder 2]:
"Tiden er ute! Stopper!"
[lydeffekt: buzzer]
```

### Avslutning (30 sekunder)
```
[Programleder 1]:
"[NAVN], du klarte [X] av [Y]! Det er [imponerende/bra/ok/dårlig]!"

[Programleder 2]:
"Premien din er [PREMIE]. Vi sender deg en SMS med detaljer."

[Programleder 1]:
"Takk for at du spilte med! Vil DU være med i morgen? 
Meld deg på via Telegram @Vev_kompis_bot eller SMS til [NUMMER]."

[Programleder 2]:
"MorgenRoulette - hver morgen klokka 07:30!"
[lydeffekt: jingle]
```

---

## 🎲 UTDFORDRINGER (Roterende Pool)

### Kategori 1: Rask Tanke
1. "Navngi 5 grønnsaker på 10 sekunder"
2. "Rim på ordet 'katt' - så mange som mulig på 30 sek"
3. "Si alfabetet baklengs fra M"
4. "Navngi 3 land som starter på B"
5. "Tell baklengs fra 100 til 90"

### Kategori 2: Morsomme Oppgaver
1. "Synge 'Happy Birthday' som en opera-sanger"
2. "Les denne setningen med norsk aksent: [engelsk setning]"
3. "Gjør din beste imitasjon av en kjendis (vi velger)"
4. "Fortell en vits på maks 20 sekunder"
5. "Lag en reklame for et produkt vi velger"

### Kategori 3: Personlige Spørsmål
1. "Hva er det pinligste som har skjedd deg på jobb?"
2. "Hvis du kunne bytte liv med én person i 24 timer - hvem?"
3. "Hva er din guilty pleasure?"
4. "Fortell om din verste date"
5. "Hvis du vant 10 millioner - hva er det FØRSTE du kjøper?"

### Kategori 4: Fysiske Utfordringer (hvis video)
1. "Gjør 10 jumping jacks på 20 sekunder"
2. "Spin rundt 5 ganger og si navnet ditt"
3. "Balanser noe på hodet i 10 sekunder"

---

## 🛠️ TEKNISK SETUP

### Hardware
- **Studio:** Vanlig mikrofonoppsett
- **Telefonlinje:** For lytter (eller VoIP)
- **Datamaskin:** For rulett-script

### Software
```python
# rulett-selector.py
import random
import json
from datetime import datetime

def select_winner():
    # Les påmeldte fra database
    with open('pameldt.json', 'r') as f:
        participants = json.load(f)
    
    # Velg tilfeldig
    winner = random.choice(participants)
    
    # Logg
    with open('log.txt', 'a') as f:
        f.write(f"{datetime.now()}: Vinner - {winner['name']}\n")
    
    return winner

def get_challenge():
    challenges = [
        {"type": "quick_think", "text": "Navngi 5 grønnsaker på 10 sekunder"},
        {"type": "funny", "text": "Synge Happy Birthday som opera"},
        # ... flere
    ]
    return random.choice(challenges)

# Kjør kl 07:28 (2 min før sending)
if __name__ == '__main__':
    winner = select_winner()
    challenge = get_challenge()
    print(f"VINNER: {winner['name']}")
    print(f"TELEFON: {winner['phone']}")
    print(f"UTFORDRING: {challenge['text']}")
```

### Database (Supabase)
```sql
CREATE TABLE morgenroulette_participants (
    id UUID DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    telegram_id TEXT,
    registered_at TIMESTAMP DEFAULT NOW(),
    has_played BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (id)
);

CREATE TABLE morgenroulette_winners (
    id UUID DEFAULT gen_random_uuid(),
    participant_id UUID REFERENCES morgenroulette_participants(id),
    challenge TEXT NOT NULL,
    result TEXT,
    prize TEXT,
    date DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (id)
);
```

---

## 📋 DAGLIG PRODUKSJONSFLYT

### Kl 07:25 (5 min før)
- [ ] Kjør rulett-script
- [ ] Sjekk at vinner er tilgjengelig på telefon
- [ ] Forbered utfordring
- [ ] Test lyd

### Kl 07:28 (2 min før)
- [ ] Ring vinner for sjekk: "Er du klar?"
- [ ] Forklar regler raskt
- [ ] Si: "Vi ringer deg opp om 2 minutter"

### Kl 07:30 (Sending)
- [ ] Kjør intro
- [ ] Kjør utfordring (60 sek)
- [ ] Kjør avslutning
- [ ] Takk for seg

### Etter sending
- [ ] Send SMS til vinner med premie-info
- [ ] Logg resultat i database
- [ ] Oppdater påmeldte (fjern vinner fra pool)
- [ ] Forbered morgendagens pool

---

## 🎁 PREMIEIDÉER

### Ukentlig rotasjon
- **Mandag:** NRJ-goodiebag (t-skjorte, kopp, klistremerker)
- **Tirsdag:** Spotify Premium 3 måneder
- **Onsdag:** Gavekort på kino
- **Torsdag:** Restaurant-gavekort
- **Fredag:** VIP-billetter til NRJ-konsert

### Sponsede premier (inntektsmulighet)
- Kaffe-abonnement
- Treningssenter-medlemskap
- Mobilabonnement
- Streaming-tjenester

---

## 📊 MÅLING AV SUKSESS

### KPI-er
| Måling | Mål | Hvordan måle |
|--------|-----|--------------|
| Påmeldte per uke | 50+ | Database-telling |
| Gjennomsnittlig lyttertid | +2 min | Analytics |
| Sosiale medier-engasjement | 10+ delinger/dag | Sosiale medier |
| Tilbakemeldinger | 80%+ positive | SMS/ Telegram |

### Evaluering etter 4 uker
- [ ] Tallet på påmeldte økende?
- [ ] Lyttere ringer inn og spør om segmentet?
- [ ] Sosiale medier-buzz?
- [ ] Vil du fortsette?

---

## ⚠️ RISIKO OG LØSNINGER

| Risiko | Sannsynlighet | Løsning |
|--------|--------------|---------|
| Vinner ikke svarer | Medium | Ha 2-3 backup-vinnere klare |
| Vinner er uegnet (beruset, støtende) | Lav | Forhåndssamtale, "kill switch" |
| Tekniske problemer | Lav | Test alltid 5 min før |
| For få påmeldte | Medium | Markedsføring, enklere påmelding |
| Lytter klager på privatliv | Lav | Tydelig samtykke, opt-in |

---

## 🚀 NESTE STEG

### Uke 1: Pilot
- [ ] Sette opp teknisk infrastruktur
- [ ] Teste med 5 interne "lyttere"
- [ ] Justere manus etter feedback

### Uke 2: Soft Launch
- [ ] Annonsere på sosiale medier
- [ ] Kjøre 3 dager med ekte lyttere
- [ ] Samle feedback

### Uke 3-4: Full Launch
- [ ] Daglig sending
- [ ] Markedsføring
- [ ] Måle KPI-er

### Etter 4 uker
- [ ] Evaluering
- [ ] Beslutning: Fortsette, justere, eller avslutte

---

## 💡 PRO-TIPS

1. **Alltid ha backup-vinnere klare** - tekniske problemer skjer
2. **Forhåndsring vinneren** - sjekk at de er våkne og klar
3. **Vær forberedt på alt** - lyttere kan overraske deg
4. **Ha det gøy selv** - entusiasme smitter
5. **Ikke ta det for seriøst** - dette skal være gøy, ikke stress

---

**Klar til å rulle?** 🎲🎙️
