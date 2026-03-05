#!/usr/bin/env python3
"""
📱 Social Content Factory - Automatisk generering av TikTok/Instagram-innhold
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

class SocialContentFactory:
    """Generer innhold for sosiale medier"""
    
    def __init__(self):
        self.workspace = Path('/root/.openclaw/workspace')
        self.content_dir = self.workspace / 'brain' / 'social-content'
        self.content_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_weekly_content(self):
        """Generer en ukes innhold"""
        
        week_number = datetime.now().isocalendar()[1]
        
        content_plan = {
            'week': week_number,
            'generated': datetime.now().isoformat(),
            'posts': []
        }
        
        # Mandag - Weekend recap
        content_plan['posts'].append({
            'day': 'Mandag',
            'platform': 'TikTok',
            'type': 'Weekend Recap',
            'hook': 'Helgen som gikk i kjendis-Norge...',
            'script': [
                'Start: "Du vil ikke tro hva som skjedde i helgen..."',
                'Midt: Fortell om 2-3 kjendis-hendelser',
                'Slutt: "Hør mer i dagens episode!"'
            ],
            'hashtags': ['#NRJMorgen', '#KjendisNorge', '#Helg', '#Podcast'],
            'duration': '30-45 sek',
            'music': 'Trending sound - check TikTok trends'
        })
        
        # Tirsdag - Funny moment
        content_plan['posts'].append({
            'day': 'Tirsdag',
            'platform': 'Instagram Reels',
            'type': 'Funny Moment',
            'hook': 'Baarli sin reaksjon da... 😂',
            'script': [
                'Start: Vis Baarli/Benjamin som reagerer',
                'Midt: Spill av den morsomme kommentaren',
                'Slutt: "Hver dag på NRJ Morgen!"'
            ],
            'hashtags': ['#NRJMorgen', '#Humor', '#Radio', '#Norge'],
            'duration': '15-30 sek',
            'music': 'Funny/trending audio'
        })
        
        # Onsdag - Reality update
        content_plan['posts'].append({
            'day': 'Onsdag',
            'platform': 'TikTok',
            'type': 'Reality Update',
            'hook': 'Paradise Hotel-oppdatering! 🏝️',
            'script': [
                'Start: "Paradise Hotel-nyheter!"',
                'Midt: Hva skjedde i siste episode',
                'Slutt: "Vi diskuterer dette i morgen!"'
            ],
            'hashtags': ['#NRJMorgen', '#ParadiseHotel', '#RealityTV', '#Norge'],
            'duration': '30-45 sek',
            'music': 'Dramatic/trending sound'
        })
        
        # Torsdag - Q&A
        content_plan['posts'].append({
            'day': 'Torsdag',
            'platform': 'Instagram Reels',
            'type': 'Q&A',
            'hook': 'Spørsmål fra lytteren! ❓',
            'script': [
                'Start: "Spørsmål fra @brukernavn"',
                'Midt: Les spørsmålet + svar',
                'Slutt: "Still spørsmål i kommentarene!"'
            ],
            'hashtags': ['#NRJMorgen', '#QandA', '#Podcast', '#Norge'],
            'duration': '30-60 sek',
            'music': 'Upbeat/trending'
        })
        
        # Fredag - Best of week
        content_plan['posts'].append({
            'day': 'Fredag',
            'platform': 'TikTok',
            'type': 'Best of Week',
            'hook': 'Ukens beste øyeblikk! 🎉',
            'script': [
                'Start: "Ukens høydepunkter!"',
                'Midt: Kompilasjon av morsomme klipp',
                'Slutt: "God helg fra NRJ Morgen!"'
            ],
            'hashtags': ['#NRJMorgen', '#BestOf', '#Uke', '#Podcast'],
            'duration': '45-60 sek',
            'music': 'High energy/trending'
        })
        
        # Lørdag - Behind the scenes
        content_plan['posts'].append({
            'day': 'Lørdag',
            'platform': 'Instagram Stories',
            'type': 'Behind the Scenes',
            'hook': 'Bak kulissene på NRJ Morgen 🎙️',
            'script': [
                'Vis studio',
                'Vis forberedelser',
                'Fortell om kommende uke'
            ],
            'hashtags': ['#NRJMorgen', '#BTS', '#Radio', '#Studio'],
            'duration': 'Stories format',
            'music': 'Chill background'
        })
        
        # Søndag - Preview
        content_plan['posts'].append({
            'day': 'Søndag',
            'platform': 'TikTok',
            'type': 'Week Preview',
            'hook': 'Hva skjer neste uke? 👀',
            'script': [
                'Start: "Neste uke på NRJ Morgen:"',
                'Midt: List opp 3 ting som kommer',
                'Slutt: "Følg med!"'
            ],
            'hashtags': ['#NRJMorgen', '#ComingUp', '#NesteUke', '#Podcast'],
            'duration': '30-45 sek',
            'music': 'Exciting/trending'
        })
        
        return content_plan
    
    def generate_captions(self) -> dict:
        """Generer ferdige captions"""
        
        captions = {
            'tiktok_viral': """🎙️ NRJ Morgen Podcast

Baarli og Benjamin diskuterer det du bryr deg om!

Reality ✦ Kjendiser ✦ Popkultur

🔗 Hør hele episoden - link i bio!

#NRJMorgen #Podcast #Norge #Radio #BaarliOgBenjamin #Morgenradio #NorskPodcast""",

            'instagram_engaging': """🎙️ Hva synes du om dette?

Baarli og Benjamin tar opp det alle snakker om i dagens episode!

💬 Kommenter din mening nedenfor!
👆 Trykk link i bio for å høre mer

#NRJMorgen #Podcast #Norge #Radio #KjendisNorge""",

            'instagram_reel': """😂 Denne reaksjonen da!

Hør mer i dagens episode av NRJ Morgen Podcast med Baarli og Benjamin 🎙️

#NRJMorgen #Podcast #Humor #Norge #Radio""",

            'story_poll': """🎙️ Dagens spørsmål!

Hva synes du?

👆 Stem i poll ovenfor!

#NRJMorgen #Podcast #Norge"""
        }
        
        return captions
    
    def generate_hashtag_sets(self) -> list:
        """Generer hashtag-sett for ulike typer innhold"""
        
        return [
            {
                'name': 'General',
                'tags': ['#NRJMorgen', '#Podcast', '#Norge', '#Radio', '#Morgenradio']
            },
            {
                'name': 'Reality',
                'tags': ['#NRJMorgen', '#RealityTV', '#ParadiseHotel', '#Farmen', '#Norge']
            },
            {
                'name': 'Kjendis',
                'tags': ['#NRJMorgen', '#KjendisNorge', '#CelebNews', '#Norge', '#Popkultur']
            },
            {
                'name': 'Humor',
                'tags': ['#NRJMorgen', '#Humor', '#Funny', '#Podcast', '#Norge', '#Comedy']
            },
            {
                'name': 'Viral',
                'tags': ['#NRJMorgen', '#Viral', '#Trending', '#Podcast', '#Norge', '#FYP']
            }
        ]
    
    def save_content_package(self):
        """Lagre komplett innholdspakke"""
        
        package = {
            'generated': datetime.now().isoformat(),
            'weekly_content': self.generate_weekly_content(),
            'captions': self.generate_captions(),
            'hashtag_sets': self.generate_hashtag_sets()
        }
        
        # Lagre som JSON
        json_file = self.content_dir / f'content-package-{datetime.now().strftime("%Y%m%d")}.json'
        with open(json_file, 'w') as f:
            json.dump(package, f, indent=2)
        
        # Lagre som markdown for enkel lesing
        md_file = self.content_dir / f'content-package-{datetime.now().strftime("%Y%m%d")}.md'
        with open(md_file, 'w') as f:
            f.write(self.generate_markdown_content(package))
        
        return json_file, md_file
    
    def generate_markdown_content(self, package: dict) -> str:
        """Generer markdown versjon av innholdet"""
        
        md = f"""# 📱 Social Content Package

**Generert:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 🗓️ Ukens Innholdsplan

"""
        
        for post in package['weekly_content']['posts']:
            md += f"""### {post['day']} - {post['platform']}

**Type:** {post['type']}  
**Varighet:** {post['duration']}

**Hook:** {post['hook']}

**Script:**
"""
            for line in post['script']:
                md += f"- {line}\n"
            
            md += f"\n**Hashtags:** {' '.join(post['hashtags'])}\n\n"
            md += f"**Musikk:** {post['music']}\n\n---\n\n"
        
        md += """## 📝 Ferdige Captions

"""
        
        for name, caption in package['captions'].items():
            md += f"""### {name.replace('_', ' ').title()}

```
{caption}
```

---

"""
        
        md += """## 🏷️ Hashtag Sett

"""
        
        for hashtag_set in package['hashtag_sets']:
            md += f"""### {hashtag_set['name']}

{' '.join(hashtag_set['tags'])}

"""
        
        return md
    
    def print_content_summary(self):
        """Print sammendrag av innholdet"""
        
        json_file, md_file = self.save_content_package()
        
        print("\n" + "=" * 70)
        print("📱 SOCIAL CONTENT FACTORY")
        print("=" * 70)
        
        print(f"\n✅ Generert innholdspakke:")
        print(f"   JSON: {json_file}")
        print(f"   Markdown: {md_file}")
        
        print(f"\n📋 Innhold generert:")
        print(f"   • 7 ukentlige poster")
        print(f"   • 4 ferdige captions")
        print(f"   • 5 hashtag-sett")
        
        print(f"\n📱 Plattformer:")
        print(f"   • TikTok: 4 poster")
        print(f"   • Instagram Reels: 2 poster")
        print(f"   • Instagram Stories: 1 post")
        
        print("\n" + "=" * 70)
        print("\n💡 Neste steg:")
        print("   1. Les markdown-filen for detaljert innhold")
        print("   2. Ta opp videoer basert på scriptene")
        print("   3. Post på respektive plattformer")
        print("   4. Track engasjement i Growth Tracker")
        print("=" * 70)


def main():
    """Main entry point"""
    factory = SocialContentFactory()
    factory.print_content_summary()
    return 0


if __name__ == '__main__':
    sys.exit(main())
