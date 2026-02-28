#!/usr/bin/env python3
"""
🎙️ NRJ Podcast Promoter - Automatisk promotering av podcast-episoder
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

sys.path.insert(0, '/root/.openclaw/workspace/scripts')

class PodcastPromoter:
    """Automatisk promotering av NRJ Morgen podcast"""
    
    def __init__(self):
        self.workspace = Path('/root/.openclaw/workspace')
        self.promotions_file = self.workspace / 'brain' / 'podcast-promotions.json'
        
    def generate_social_posts(self, episode_title: str, highlights: list) -> dict:
        """Generer sosiale medie-innlegg for en episode"""
        
        # Instagram/TikTok caption
        instagram_caption = f"""🎙️ NY EPISODE: {episode_title}

{highlights[0] if highlights else 'Hør dagens episode!'}

🔗 Link i bio
#NRJMorgen #Podcast #Norge #Radio #Morgenradio"""

        # Twitter/X post
        twitter_post = f"""🎙️ Ny episode ute: {episode_title}

{highlights[0][:100] if highlights else 'Hør nå!'}...

#NRJMorgen #Podcast #Norge"""

        # Facebook post
        facebook_post = f"""🎙️ NY EPISODE AV NRJ MORGEN PODCAST!

{episode_title}

{chr(10).join(['• ' + h for h in highlights[:3]]) if highlights else 'Hør dagens episode!'}

Hva synes du? Kommenter nedenfor! 👇

#NRJMorgen #Podcast #Norge #Radio"""

        return {
            'instagram': instagram_caption,
            'tiktok': instagram_caption,  # Samme som Instagram
            'twitter': twitter_post,
            'facebook': facebook_post
        }
    
    def generate_email_newsletter(self, week_number: int, episodes: list, top_stories: list) -> str:
        """Generer e-post nyhetsbrev"""
        
        newsletter = f"""# 📧 NRJ Morgen Nyhetsbrev - Uke {week_number}

Hei lytter!

## 🎧 Ukens Episoder

"""
        
        for ep in episodes:
            newsletter += f"""### {ep['title']}
{ep['description'][:150]}...

[Hør episoden]

"""
        
        newsletter += f"""## 📰 Ukens Toppsaker

"""
        
        for story in top_stories[:5]:
            newsletter += f"- {story}\n"
        
        newsletter += f"""

## 🎁 Eksklusivt for Nyhetsbrev-abonnenter

Denne uken: Bak kulissene-bilder fra studio!

---

**Lytt live:** NRJ Morgen hver morgen 06-10
**Podcast:** [Baarli og Benjamin går i terapi]

Følg oss på [Instagram] [TikTok] [YouTube]

---

*Du mottar dette fordi du abonnerer på NRJ Morgen nyhetsbrev.*
"""
        
        return newsletter
    
    def generate_youtube_description(self, episode_title: str, description: str, 
                                     timestamps: dict, links: list) -> str:
        """Generer YouTube beskrivelse"""
        
        yt_desc = f"""{episode_title}

{description}

🎧 LYTT TIL PODCASTEN:
https://podcasts.apple.com/no/podcast/baarli-og-benjamin-gar-i-terapi/id...

⏱️ KAPITTELMERKER:
"""
        
        for time, title in timestamps.items():
            yt_desc += f"{time} - {title}\n"
        
        yt_desc += f"""
🔗 RELEVANTE LINKER:
"""
        
        for link in links:
            yt_desc += f"{link}\n"
        
        yt_desc += f"""
---

🎙️ NRJ MORGEN PODCAST
Med Baarli og Benjamin

📻 Hør oss live på NRJ hver morgen 06-10
📱 Følg oss på Instagram: @nrjmorgen
🎵 TikTok: @nrjmorgen

#NRJMorgen #Podcast #Norge #Radio #BaarliOgBenjamin
"""
        
        return yt_desc
    
    def save_promotion(self, episode_id: str, promotion_data: dict):
        """Lagre promotering for tracking"""
        
        promotions = []
        if self.promotions_file.exists():
            with open(self.promotions_file, 'r') as f:
                promotions = json.load(f)
        
        promotion = {
            'episode_id': episode_id,
            'date': datetime.now().isoformat(),
            'data': promotion_data
        }
        
        promotions.append(promotion)
        
        with open(self.promotions_file, 'w') as f:
            json.dump(promotions, f, indent=2)
    
    def print_promotion_package(self, episode_title: str, highlights: list):
        """Print komplett promotering-pakke"""
        
        print("\n" + "=" * 70)
        print("🎙️ PODCAST PROMOTION PAKKE")
        print("=" * 70)
        print(f"\nEpisode: {episode_title}")
        print(f"Generert: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Sosiale medier
        print("\n" + "-" * 70)
        print("📱 SOSIALE MEDIER INNLEGG")
        print("-" * 70)
        
        posts = self.generate_social_posts(episode_title, highlights)
        
        for platform, content in posts.items():
            print(f"\n{platform.upper()}:")
            print(content)
            print()
        
        print("=" * 70)


def main():
    """Main entry point"""
    promoter = PodcastPromoter()
    
    # Eksempel på bruk
    promoter.print_promotion_package(
        episode_title="Episode 158: Ukens reality-drama og kjendisnyheter",
        highlights=[
            "Vi diskuterer Paradise Hotel-sjokket",
            "Kjendis-brudd som fikk alle til å snakke",
            "TikTok-trenden alle prøver nå"
        ]
    )
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
