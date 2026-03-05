# 📚 BAKFASADEN BIBEL - Komplett Produksjonsguide

**Segment:** BakFasaden  
**Type:** AI-deepfake celebrity intervju (humoristisk)  
**Varighet:** 3-5 minutter  
**Frekvens:** 2-3 ganger per uke  
**Sist oppdatert:** 2026-03-05

---

## 🎭 SEGMENTOVERSIKT

### Hva er BakFasaden?
Vi "intervjuer" kjendiser som ikke er tilgjengelige ved å bruke AI (voice cloning + ChatGPT). Lytteren vet at det er AI (avsløres tydelig), men det er likevel underholdende og humoristisk.

### Hvorfor fungerer det?
- **Humor:** Selvironisk, leken tone
- **Unikt:** Ingen andre i Norge gjør dette (enda)
- **Viral-potensial:** "Hørte du at NRJ intervjuet Brad Pitt?!"
- **Lav terskel:** Krever minimal produksjon

---

## 📝 MANUSMAL

### Intro (30 sekunder)
```
[Programleder]:
"I dag har vi en VELDIG spesiell gjest i studio. 
Han trenger ingen introduksjon... det er... [KJENDISNAVN]!"

[AI-stemme - ligner på kjendis]:
"Hei! Takk for at jeg fikk komme."

[Programleder]:
"La meg bare gjøre det HELT klart: Dette er IKKE ekte [KJENDIS]. 
Dette er AI. Men la oss leke at det er ham!"
```

### Intervju (2-3 minutter)
```
[Programleder]:
"Så [KJENDIS], hvordan startet du dagen i dag?"

[AI-stemme]:
"[HUMORISTISK SVAR - typisk for kjendisens personlighet]"

[Programleder]:
"Interessant! Nå har jeg hørt at du [Rykte/nyhet]. Stemmer det?"

[AI-stemme]:
"[HUMORISTISK SVAR - spiller på rykte]"

[Programleder]:
"Hva med [NORGE/NORSK TEMA]? Hva synes du om det?"

[AI-stemme]:
"[HUMORISTISK SVAR - inkluderer norsk referanse]"

[Programleder]:
"En siste ting: Kan du si [NORSK SETNING/ORD]?"

[AI-stemme]:
"[FORSØK PÅ NORSK - morsom aksent]"
```

### Avslutning (30 sekunder)
```
[Programleder]:
"Takk for at du kom, [KJENDIS]!"

[AI-stemme]:
"Takk for meg! Hilsen til alle lytterne!"

[Programleder]:
"Og husk: Dette var AI! Ikke ekte [KJENDIS]. 
Men likevel gøy, ikke sant?"

"BakFasaden - hvor vi intervjuer kjendiser som ikke vil komme!"
[lydeffekt: outro]
```

---

## 🎤 KJENDIS-ROTASJON

### Kategori 1: Hollywood-stjerner
- Brad Pitt
- Tom Cruise
- Scarlett Johansson
- Leonardo DiCaprio
- Dwayne "The Rock" Johnson

### Kategori 2: Musikkstjerner
- Taylor Swift
- Ed Sheeran
- Beyoncé
- Justin Bieber
- Adele

### Kategori 3: Norske kjendiser (for ekstra moro!)
- Erna Solberg
- Sigrid
- Karpe Diem
- Pål Anders Ullevålseter
- Therese Johaug

### Kategori 4: Fiktive karakterer
- Batman
- Harry Potter
- Elsa fra Frost
- Darth Vader

---

## 🤖 AI-PRODUKSJON

### Steg 1: Manus-generering (ChatGPT)
```
Prompt:
"Lag et humoristisk radiomanus hvor [KJENDIS] blir intervjuet. 
Kjendisen skal:
- Være selvironisk
- Spille på kjente rykter/nyheter om seg selv
- Inkludere en norsk referanse
- Prøve å si noe på norsk (morsomt)

Intervjuer spør 4 spørsmål:
1. Hvordan startet du dagen?
2. Et rykte som går
3. Hva synes du om Norge?
4. Si noe på norsk

Hold det kort, morsomt, og respektfullt."
```

### Steg 2: Stemme-generering (ElevenLabs)
```python
# voice-generator.py
import requests

def generate_voice(text, voice_id):
    """Generer stemme med ElevenLabs"""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "DIN_API_KEY"
    }
    
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    with open('output.mp3', 'wb') as f:
        f.write(response.content)
    
    return 'output.mp3'

# Eksempel på stemme-ID-er
VOICES = {
    'brad_pitt': 'voice_id_her',
    'taylor_swift': 'voice_id_her',
    # ... flere
}
```

### Steg 3: Lydredigering
```python
# audio-editor.py
from pydub import AudioSegment

def combine_interview(host_segments, ai_segments):
    """Kombiner programleder og AI-stemme"""
    final_audio = AudioSegment.empty()
    
    for i, host in enumerate(host_segments):
        # Legg til programleder
        host_audio = AudioSegment.from_mp3(host)
        final_audio += host_audio
        
        # Legg til pause
        final_audio += AudioSegment.silent(duration=500)
        
        # Legg til AI-svar (hvis det finnes)
        if i < len(ai_segments):
            ai_audio = AudioSegment.from_mp3(ai_segments[i])
            final_audio += ai_audio
            
            # Legg til pause
            final_audio += AudioSegment.silent(duration=500)
    
    final_audio.export('final_interview.mp3', format='mp3')
    return 'final_interview.mp3'
```

---

## 🛠️ TEKNISK SETUP

### Hardware
- **Studio:** Vanlig mikrofonoppsett
- **Datamaskin:** For AI-generering
- **Lydredigering:** Audacity eller lignende

### Software
- **ElevenLabs:** Voice cloning (krever abonnement)
- **ChatGPT/OpenAI API:** Manus-generering
- **Python:** For automatisering
- **Audacity:** Lydredigering (valgfritt)

### Kostnader
- ElevenLabs: ~$5-22/mnd (avhengig av bruk)
- OpenAI API: ~$0.01-0.10 per intervju
- **Total:** ~$10-30/mnd for 2-3 intervjuer per uke

---

## 📋 PRODUKSJONSFLYT

### 3 dager før sending
- [ ] Velg kjendis
- [ ] Generer manus med ChatGPT
- [ ] Gjennomgå og rediger manus

### 2 dager før sending
- [ ] Generer stemme med ElevenLabs
- [ ] Hør gjennom og juster

### 1 dag før sending
- [ ] Kombiner programleder og AI-stemme
- [ ] Final mix
- [ ] Godkjennelse

### Sending
- [ ] Kjør som forhåndsinnspilt segment
- [ ] Eller: Kjør live med programleder som reagerer

---

## ⚖️ ETISKE RETNINGSLINJER

### Hva vi ALLTID gjør:
- ✅ Tydelig merke at det er AI
- ✅ Være respektfull
- ✅ Holde det humoristisk, ikke ondsinnet
- ✅ Unngå sensitive emner

### Hva vi ALDRI gjør:
- ❌ Late som det er ekte
- ❌ Være respektløs mot personen
- ❌ Ta opp traumer/skandaler
- ❌ Bruke det til politisk propaganda

### Eksempel på intro:
```
"Dette er AI-generert. Det er ikke ekte [KJENDIS]. 
Det er ment som underholdning."
```

---

## 🎯 MÅLING AV SUKSESS

### KPI-er
| Måling | Mål | Hvordan måle |
|--------|-----|--------------|
| Sosiale medier-engasjement | 50+ delinger per intervju | Sosiale medier |
| Lytter-feedback | 80%+ positivt | SMS/Telegram |
| Viralitet | 1+ intervju går viral per måned | Delinger |
| Kontrovers | 0 klager | Feedback |

---

## ⚠️ RISIKO OG LØSNINGER

| Risiko | Løsning |
|--------|---------|
| Kjendis klager | Tydelig merking, respektfull tone |
| Dårlig lydkvalitet | Test flere stemmer, juster settings |
| For kostbart | Reduser frekvens, bruk gratis alternativer |
| Ikke morsomt | Test med fokusgruppe først |

---

## 💡 PRO-TIPS

1. **Test stemmen først** - Ikke alle stemmer fungerer like godt
2. **Ha backup-manus** - Hvis AI-generering feiler
3. **Vær konsistent med merking** - Alltid si at det er AI
4. **Lytt til feedback** - Juster basert på hva lyttere sier
5. **Ikke overdrive** - 2-3 ganger per uke er nok

---

## 🚀 NESTE STEG

### Uke 1: Test
- [ ] Lag ett test-intervju
- [ ] Spill av for kollegaer
- [ ] Samle feedback

### Uke 2: Pilot
- [ ] Send ett intervju på luften
- [ ] Mål reaksjoner
- [ ] Juster

### Uke 3-4: Regular
- [ ] 2-3 intervjuer per uke
- [ ] Bygg opp bibliotek
- [ ] Måle suksess

---

**Klar til å "intervjue" noen kjendiser?** 🎭🎙️
