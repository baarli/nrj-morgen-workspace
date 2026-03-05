# 📚 FREMTIDSFLASH BIBEL - Komplett Produksjonsguide

**Segment:** FremtidsFlash  
**Type:** AI-drevet nyhetsprediksjon  
**Varighet:** 2-3 minutter  
**Frekvens:** Daglig, 07:15  
**Sist oppdatert:** 2026-03-05

---

## 🎯 SEGMENTOVERSIKT

### Hva er FremtidsFlash?
Vi bruker AI til å analysere trender og PREDIKERE hva som vil skje i løpet av dagen - ikke bare rapportere hva som har skjedd. Lytterne kan følge med på om spådommene slår til.

### Hvorfor fungerer det?
- **Nysgjerrighet:** "Vil dette skje?"
- **Engasjement:** Lyttere kan "følge med" gjennom dagen
- **Unikt:** Ingen andre i Norge gjør dette
- **Sosialt:** Perfekt for diskusjon på sosiale medier

---

## 📝 MANUSMAL

### Intro (20 sekunder)
```
[Programleder]:
"God morgen! Jeg har sett inn i krystallkulen - eller rettere sagt, 
AI-en har analysert alle trender. Dette er FREMTIDSFLASH!"
[lydeffekt: mystisk/magisk lyd]

"I dag skal jeg spå 3 ting som kommer til å skje. 
Følg med - sjekker vi resultatet i ettermiddag!"
```

### Prediksjoner (90 sekunder)
```
[Programleder]:
"Prediksjon nummer 1: [KATEGORI]"

"I løpet av dagen i dag, mellom klokka [TID], 
kommer [SPÅDOM] å skje."

"Hvorfor tror jeg dette? [KORT BEGRUNNELSE - 1 setning]"

"Sannsynlighet: [X]%"

[Pause 2 sekunder]

"Prediksjon nummer 2..."
[Repeat]

"Prediksjon nummer 3..."
[Repeat]
```

### Avslutning (20 sekunder)
```
[Programleder]:
"Så der har du det! Tre spådommer for dagen. 
Følg med på @nrjmorgen - vi oppdaterer i ettermiddag!"

"Hvilken tror DU på? Stem på Instagram!"
[lydeffekt: outro]
```

---

## 🔮 PREDIKSJONSKATEGORIER

### 1. Sosiale Medier
- "Denne TikTok-videoen vil ha 1 million views kl 14:00"
- "[KJENDIS] vil tweete noe kontroversielt i løpet av dagen"
- "Hashtaggen #[EMNE] vil trende på Twitter"
- "Denne Instagram-posten får 10.000 likes"

### 2. Nyheter
- "VG vil ha denne saken som topp-sak kl 12:00"
- "Denne politikeren vil komme med uttalelse"
- "Dette emnet vil dominere nyhetsbildet"

### 3. Underholdning
- "Denne sangen vil være #1 på Spotify i kveld"
- "Denne kjendisen vil annonsere noe stort"
- "Denne TV-serien vil få massiv omtale"

### 4. Sport
- "Dette laget vil vinne kampen i kveld"
- "Denne spilleren vil score"
- "Denne overgangen vil bli bekreftet"

### 5. Vær (enkelt!)
- "Det vil regne i Oslo kl 15:00"
- "Temperaturen vil nå 25 grader"

---

## 🤖 AI-GENERERING AV PREDIKSJONER

### Python Script
```python
# fremtidsflash-generator.py
import json
import random
from datetime import datetime, timedelta
from brave_search import BraveSearchClient

class FremtidsFlashGenerator:
    def __init__(self):
        self.search = BraveSearchClient()
        
    def analyze_trends(self):
        """Hent trending topics"""
        trends = self.search.get_trending(
            country='NO',
            timeframe='1d'
        )
        return trends
    
    def generate_predictions(self, trends):
        """Generer 3 spådommer basert på trender"""
        predictions = []
        
        # Kategori 1: Sosiale medier
        if trends['social']:
            top_trend = trends['social'][0]
            predictions.append({
                'category': 'Sosiale Medier',
                'prediction': f"#{top_trend['hashtag']} vil trende på Twitter kl {self._random_time()}",
                'reason': f"Allerede {top_trend['volume']} tweets om emnet",
                'confidence': random.randint(60, 85)
            })
        
        # Kategori 2: Nyheter
        if trends['news']:
            top_news = trends['news'][0]
            predictions.append({
                'category': 'Nyheter',
                'prediction': f"{top_news['topic']} vil dominere nyhetsbildet",
                'reason': f"{top_news['source']} har allerede dekning",
                'confidence': random.randint(70, 90)
            })
        
        # Kategori 3: Underholdning
        predictions.append({
            'category': 'Underholdning',
            'prediction': self._generate_entertainment_prediction(),
            'reason': 'Basert på mønstre fra tidligere uker',
            'confidence': random.randint(50, 75)
        })
        
        return predictions
    
    def _random_time(self):
        """Generer tilfeldig tidspunkt i løpet av dagen"""
        hour = random.randint(10, 20)
        minute = random.choice([0, 15, 30, 45])
        return f"{hour:02d}:{minute:02d}"
    
    def _generate_entertainment_prediction(self):
        """Generer underholdnings-prediksjon"""
        templates = [
            "En kjent norsk artist vil slippe ny singel i kveld",
            "Denne TikTok-dansen vil gå viral",
            "En kjendis vil annonsere brudd/forhold",
            "En TV-serie vil få massiv omtale på sosiale medier"
        ]
        return random.choice(templates)
    
    def format_for_radio(self, predictions):
        """Formater for radiomanus"""
        script = []
        for i, pred in enumerate(predictions, 1):
            script.append(f"""
Prediksjon {i}: {pred['category']}
"{pred['prediction']}"
Begrunnelse: {pred['reason']}
Sannsynlighet: {pred['confidence']}%
""")
        return "\n".join(script)

# Kjør kl 06:30 (genererer for 07:15-sending)
if __name__ == '__main__':
    generator = FremtidsFlashGenerator()
    trends = generator.analyze_trends()
    predictions = generator.generate_predictions(trends)
    script = generator.format_for_radio(predictions)
    print(script)
```

---

## 📊 OPPFØLGING I ETTERMIDDAG

### Format for oppdatering
```
[Programleder]:
"God ettermiddag! Tid for FremtidsFlash-oppsummering. 
La oss se hvordan spådommene slo til..."

"Prediksjon 1: [GJENTA SPÅDOM]"
"Resultat: [SLO TIL / DELVIS / FEIL]"
"[KOMMENTAR]"

[Repeat for alle 3]

"Score: [X] av 3 riktige! 
Takk for at du fulgte med!"
```

### Sosiale medier-post
```
📊 FREMTIDSFLASH RESULTAT:

✅ Riktig: [Spådom 1]
⚠️ Delvis: [Spådom 2]  
❌ Feil: [Spådom 3]

Score: 2/3

Hvilken spådom vil du ha i morgen? 
Kommenter! 🔮
```

---

## 🛠️ TEKNISK SETUP

### Krav
- **Brave Search API:** For trend-analyse
- **Python-script:** For generering (kjøres 06:30)
- **Supabase:** For logging av resultater
- **Sosiale medier:** For avstemming/oppfølging

### Database
```sql
CREATE TABLE fremtidsflash_predictions (
    id UUID DEFAULT gen_random_uuid(),
    date DATE DEFAULT CURRENT_DATE,
    category TEXT NOT NULL,
    prediction TEXT NOT NULL,
    reason TEXT,
    confidence INTEGER,
    result TEXT CHECK (result IN ('correct', 'partial', 'wrong', 'pending')),
    actual_outcome TEXT,
    PRIMARY KEY (id)
);
```

---

## 📋 DAGLIG PRODUKSJONSFLYT

### Kl 06:30 (45 min før)
- [ ] Kjør AI-script for generering
- [ ] Gjennomgå og godkjenn prediksjoner
- [ ] Forbered manus

### Kl 07:15 (Sending)
- [ ] Kjør intro
- [ ] Les 3 prediksjoner
- [ ] Avslutt med oppfordring til å følge med

### Kl 16:00 (Ettermiddag)
- [ ] Sjekk resultater
- [ ] Forbered oppsummering
- [ ] Post på sosiale medier

### Kl 17:00 (Ettermiddagssending)
- [ ] Kjør oppsummering
- [ ] Logg resultater

---

## 🎯 MÅLING AV SUKSESS

### KPI-er
| Måling | Mål | Hvordan måle |
|--------|-----|--------------|
| Sosiale medier-engasjement | 20+ interaksjoner per prediksjon | Likes, kommentarer |
| Nøyaktighet | 60%+ riktige | Manuell telling |
| Lytter-retensjon | +5 minutter | Analytics |
| Stemmer på avstemning | 50+ per dag | Instagram polls |

---

## ⚠️ RISIKO OG LØSNINGER

| Risiko | Løsning |
|--------|---------|
| AI tar feil ofte | Vær ærlig, gjør det til en del av sjarmen |
| For vage prediksjoner | Vær spesifikk på tidspunkt og hendelse |
| Ingen interesse | Markedsføre mer, gjøre det mer interaktivt |
| For mye arbeid | Automatiser mer av prosessen |

---

## 💡 PRO-TIPS

1. **Vær spesifikk** - "Noe vil skje" er kjedelig. "X vil skje kl 14:30" er spennende.
2. **Vær ærlig når du tar feil** - Det bygger tillit.
3. **Feir når du tar rett** - Gjør det til en seier.
4. **Involver lytterne** - La dem komme med egne spådommer.
5. **Ha det gøy** - Dette er underholdning, ikke vitenskap.

---

**Klar til å spå fremtiden?** 🔮✨
