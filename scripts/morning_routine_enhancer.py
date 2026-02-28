#!/usr/bin/env python3
"""
🌅 Morning Routine Enhancer - Forbedret Morning Routine med AI
"""

import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, '/root/.openclaw/workspace/scripts')

class MorningRoutineEnhancer:
    """Forbedre Morning Routine med nye features"""
    
    def __init__(self):
        self.workspace = Path('/root/.openclaw/workspace')
        
    def generate_enhanced_prompt(self) -> str:
        """Generer forbedret prompt for Morning Routine"""
        
        prompt = '''
## 🌅 NRJ MORGEN - ENHANCED MORNING ROUTINE

### 📊 REAL-TIME TREND ANALYSIS
Først: Sjekk hva som trender NÅ:
1. Twitter/X trending i Norge (siste 6 timer)
2. TikTok trending sounds/hashtags i Norge
3. Reddit r/norge top posts
4. Google Trends Norge - real-time

### 🎯 PRIORITERT SØK (i denne rekkefølgen):

**NIVÅ 1 - Norske Kilder (MÅ sjekkes først):**
- VG Rampelys (siste 6 timer)
- TV2 Underholdning (breaking)
- Dagbladet Kjendis (trending)
- Nettavisen Kjendis (akkurat nå)
- Se og Hør (eksklusivt)
- NRK Kultur (oppdateringer)

**NIVÅ 2 - Sosiale Medier:**
- Norske influencers på Instagram/TikTok
- Virale TikTok-videoer fra Norge
- Twitter-moments Norge

**NIVÅ 3 - Internasjonale (kun hvis nivå 1+2 ikke gir nok):**
- TMZ (Hollywood breaking)
- E! News (pop culture)
- BBC Entertainment (internasjonalt)

### 🧠 AI TITTEL-OPTIMALISERING

For hver sak, generer tittel med:
- ✅ Maks 7 ord
- ✅ Curiosity gap ("Du vil ikke tro...")
- ✅ Emosjonell trigger (sjokk, glede, sinne)
- ✅ Norsk språk
- ✅ Inkluder navn på kjendis hvis relevant

**Eksempler på gode titler:**
- "Sjokket i Paradise: [Navn] gjør dette!"
- "Brudd-bombe: [Navn] og [Navn] er over"
- "TikTok-guruen alle snakker om nå"

### 📈 ENTERTAINMENT SCORING (0-100)

**Vekting:**
- Freskhet (0-24t): 30%
- Kjendis-faktor: 25%
- Drama/konflikt: 20%
- Viral-potensial: 15%
- Lokal relevans: 10%

**Bonus-poeng:**
- Reality-TV stjerne: +15
- Skandale/avsløring: +20
- Bilder/video: +10
- Eksklusivt: +25

### 🎬 KATEGORI-FORDELING (15 saker totalt)

| Kategori | Maks | Fokus |
|----------|------|-------|
| Reality TV | 3 | Farmen, Paradise, Love Island |
| Kjendis Drama | 3 | Brudd, skandaler, avsløringer |
| Film & TV | 3 | Premierer, rød løper |
| Musikk | 3 | Norske artister, Spellemann |
| Internasjonalt | 3 | Hollywood, viral content |

### ✅ KVALITETSSJEKKLISTE

Før du legger til en sak, sjekk:
- [ ] Er den under 24 timer gammel?
- [ ] Har den kjendis/reality/popkultur-vinkel?
- [ ] Vil den engasjere 18-35 åringer?
- [ ] Er kilden pålitelig?
- [ ] Har den god snakkis-faktor?

### 📤 OUTPUT FORMAT

For hver sak, lever:
```json
{
  "title": "AI-generert tittel (maks 7 ord)",
  "source": "Kildenavn",
  "url": "Lenke til original artikkel",
  "category": "Reality/Kjendis/Film/Musikk/Internasjonalt",
  "entertainment_score": 85,
  "freshness_hours": 4,
  "key_points": ["3-4 bullet points"],
  "talking_angles": ["2-3 vinklinger for radio"]
}
```

### 🎯 DAGENS MÅL

Lever 15 saker med:
- Gjennomsnittlig entertainment score > 70
- Minst 60% fra norske kilder
- Ingen sak eldre enn 24 timer
- God spredning på kategorier

Lytt til NRJ Morgen - bli verdens beste morgenshow!
'''
        return prompt
    
    def create_source_expansion_config(self) -> Dict:
        """Konfigurasjon for utvidete kilder"""
        
        return {
            'new_sources': {
                'social_trends': {
                    'name': 'Sosiale Medier Trends',
                    'platforms': ['twitter', 'tiktok', 'instagram', 'reddit'],
                    'max_articles': 2,
                    'priority': 'high'
                },
                'podcast_platforms': {
                    'name': 'Podcast Trender',
                    'sources': ['podtoppen', 'spotify podcasts', 'apple podcasts'],
                    'max_articles': 1,
                    'priority': 'medium'
                },
                'youtube_trends': {
                    'name': 'YouTube Viralt',
                    'sources': ['trending norge', 'viral videos'],
                    'max_articles': 1,
                    'priority': 'medium'
                }
            },
            'international_expansion': [
                'pagesix.com',
                'usmagazine.com',
                'thesun.co.uk/celeb',
                'hollywoodlife.com'
            ],
            'norwegian_expansion': [
                'p4.no',
                'radio1.no',
                '730.no',
                'dagsavisen.no/kultur'
            ]
        }
    
    def print_enhancement_summary(self):
        """Print sammendrag av forbedringer"""
        
        print("\n" + "=" * 70)
        print("🌅 MORNING ROUTINE ENHANCER")
        print("=" * 70)
        
        print("\n📊 Nye Features:")
        print("  ✅ Real-time trend analysis (Twitter/TikTok/Reddit)")
        print("  ✅ Forbedret AI tittel-optimalisering")
        print("  ✅ Entertainment scoring med vekting")
        print("  ✅ Automatisk kategori-fordeling")
        print("  ✅ Kvalitetssjekkliste")
        print("  ✅ Talking angles for hver sak")
        
        print("\n📡 Utvidete Kilder:")
        config = self.create_source_expansion_config()
        for category, sources in config['new_sources'].items():
            print(f"  • {sources['name']}: {sources['priority']} priority")
        
        print("\n🔗 Internasjonale Kilder:")
        for source in config['international_expansion']:
            print(f"  • {source}")
        
        print("\n🇳🇴 Norske Kilder (Utvidet):")
        for source in config['norwegian_expansion']:
            print(f"  • {source}")
        
        print("\n" + "=" * 70)
        print("\n💾 Forbedret prompt lagret til: docs/enhanced-morning-routine-prompt.md")
        print("💾 Kilde-konfig lagret til: config/morning-routine-sources.json")


def main():
    """Main entry point"""
    enhancer = MorningRoutineEnhancer()
    
    # Lagre forbedret prompt
    workspace = Path('/root/.openclaw/workspace')
    
    docs_dir = workspace / 'docs'
    docs_dir.mkdir(exist_ok=True)
    
    with open(docs_dir / 'enhanced-morning-routine-prompt.md', 'w') as f:
        f.write(enhancer.generate_enhanced_prompt())
    
    # Lagre kilde-konfig
    config_dir = workspace / '.config'
    config_dir.mkdir(exist_ok=True)
    
    import json
    with open(config_dir / 'morning-routine-sources.json', 'w') as f:
        json.dump(enhancer.create_source_expansion_config(), f, indent=2)
    
    # Print sammendrag
    enhancer.print_enhancement_summary()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
