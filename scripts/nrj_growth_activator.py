#!/usr/bin/env python3
"""
🚀 NRJ Growth Activator - Aktiv vekststrategi for NRJ Morgen
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

class NRJGrowthActivator:
    """Aktiv vekststrategi for NRJ Morgen podcast"""
    
    def __init__(self):
        self.workspace = Path('/root/.openclaw/workspace')
        self.strategy_file = self.workspace / 'brain' / 'growth-strategy.json'
        self.actions_taken = []
        
    def load_strategy(self):
        """Last eksisterende strategi"""
        if self.strategy_file.exists():
            with open(self.strategy_file, 'r') as f:
                return json.load(f)
        return {'actions': [], 'metrics': {}}
    
    def save_strategy(self, strategy):
        """Lagre strategi"""
        with open(self.strategy_file, 'w') as f:
            json.dump(strategy, f, indent=2)
    
    def identify_growth_opportunities(self):
        """Identifiser vekstmuligheter"""
        opportunities = [
            {
                'id': 1,
                'name': 'YouTube Video Podcast',
                'impact': 'high',
                'effort': 'medium',
                'description': '80% av podcast-video konsumeres på YouTube',
                'action': 'Sette opp YouTube-kanal og laste opp episoder'
            },
            {
                'id': 2,
                'name': 'TikTok Short Clips',
                'impact': 'high',
                'effort': 'low',
                'description': 'TikTok er #1 for 18-35 åringer',
                'action': 'Lage 30-sekunders klipp fra hver episode'
            },
            {
                'id': 3,
                'name': 'Instagram Reels',
                'impact': 'medium',
                'effort': 'low',
                'description': 'Reels når flere enn vanlige posts',
                'action': 'Poste daglige Reels med highlights'
            },
            {
                'id': 4,
                'name': 'Email Newsletter',
                'impact': 'medium',
                'effort': 'medium',
                'description': 'Direkte kontakt med lyttere',
                'action': 'Sette opp ukentlig nyhetsbrev'
            },
            {
                'id': 5,
                'name': 'Cross-Promotion',
                'impact': 'high',
                'effort': 'medium',
                'description': 'Samarbeid med andre norske podcaster',
                'action': 'Kontakte 10 relevante podcaster for samarbeid'
            }
        ]
        return opportunities
    
    def create_action_plan(self):
        """Lag handlingsplan"""
        opportunities = self.identify_growth_opportunities()
        
        # Sorter etter impact/effort ratio
        for opp in opportunities:
            impact_score = {'high': 3, 'medium': 2, 'low': 1}[opp['impact']]
            effort_score = {'high': 3, 'medium': 2, 'low': 1}[opp['effort']]
            opp['score'] = impact_score / effort_score
        
        opportunities.sort(key=lambda x: x['score'], reverse=True)
        
        return opportunities
    
    def execute_quick_wins(self):
        """Utfør raske seiere umiddelbart"""
        
        print("🚀 Starter Quick Wins...\n")
        
        # 1. Opprette vekst-tracker
        self.setup_growth_tracking()
        
        # 2. Generere sosialt medie-innhold
        self.generate_social_content()
        
        # 3. Lage outreach-maler
        self.create_outreach_templates()
        
        # 4. Sette opp innholdskalender
        self.setup_content_calendar()
        
        print("\n✅ Quick Wins fullført!")
    
    def setup_growth_tracking(self):
        """Sett opp tracking av vekstmetrikker"""
        
        tracking_data = {
            'start_date': datetime.now().isoformat(),
            'baseline': {
                'listeners': 17108,
                'rank': 46,
                'episodes': 157
            },
            'targets': {
                '3_months': {'listeners': 25000, 'rank': 35},
                '6_months': {'listeners': 35000, 'rank': 25},
                '12_months': {'listeners': 50000, 'rank': 15}
            },
            'weekly_tracking': []
        }
        
        tracker_file = self.workspace / 'brain' / 'growth-tracking.json'
        with open(tracker_file, 'w') as f:
            json.dump(tracking_data, f, indent=2)
        
        print(f"  ✅ Growth tracking satt opp")
        self.actions_taken.append('Setup growth tracking')
    
    def generate_social_content(self):
        """Generer sosialt medie-innhold"""
        
        content_dir = self.workspace / 'brain' / 'social-content'
        content_dir.mkdir(exist_ok=True)
        
        # Lag 10 ulike post-maler for TikTok/Instagram
        posts = [
            {
                'platform': 'tiktok',
                'hook': 'Du vil ikke tro hva Baarli sa i dag...',
                'cta': 'Følg for mer!',
                'hashtags': ['#NRJMorgen', '#Podcast', '#Norge']
            },
            {
                'platform': 'instagram',
                'hook': 'Ukens reality-drama forklart på 60 sekunder',
                'cta': 'Hør hele episoden - link i bio!',
                'hashtags': ['#NRJMorgen', '#RealityTV', '#NorskPodcast']
            },
            {
                'platform': 'tiktok',
                'hook': 'Benjamin sin reaksjon da han hørte nyheten 😂',
                'cta': 'Hør mer i podcasten!',
                'hashtags': ['#NRJMorgen', '#Humor', '#PodcastNorge']
            }
        ]
        
        with open(content_dir / 'post-templates.json', 'w') as f:
            json.dump(posts, f, indent=2)
        
        print(f"  ✅ Generert {len(posts)} post-maler")
        self.actions_taken.append(f'Generated {len(posts)} social media templates')
    
    def create_outreach_templates(self):
        """Lag maler for outreach til andre podcaster/influencere"""
        
        outreach_dir = self.workspace / 'brain' / 'outreach'
        outreach_dir.mkdir(exist_ok=True)
        
        # Instagram DM mal
        ig_template = """Hei [Navn]! 👋

Jeg hører på [Podcast-navn] og digger stilen deres!

Vi driver NRJ Morgen podcast med Baarli og Benjamin - en morgenpodcast om reality, kjendiser og populærkultur. 

Hadde vært kult å gjøre noe sammen! Kanskje en guest appearance eller cross-promo?

Hva tenker du?

Mvh,
NRJ Morgen Team"""
        
        # Email mal
        email_template = """Emne: Samarbeidsmulighet - NRJ Morgen Podcast

Hei [Navn],

Jeg heter [Ditt navn] og jobber med NRJ Morgen podcast, en av Norges raskest voksende morgenpodcaster med Baarli og Benjamin.

Vi har [X] lyttere per episode og fokuserer på reality-TV, kjendisnyheter og populærkultur.

Jeg ser at dere har en fantastisk podcast i [sjanger], og jeg lurte på om dere ville være interessert i et samarbeid?

Ideer:
• Gjesteopptreden i hverandres podcaster
• Cross-promotion på sosiale medier
• Felles episode om [tema]

La meg vite hva du tenker!

Beste hilsen,
[Ditt navn]
NRJ Morgen Podcast
nrj.no"""
        
        with open(outreach_dir / 'instagram-dm.txt', 'w') as f:
            f.write(ig_template)
        
        with open(outreach_dir / 'collaboration-email.txt', 'w') as f:
            f.write(email_template)
        
        print(f"  ✅ Laget outreach-maler")
        self.actions_taken.append('Created outreach templates')
    
    def setup_content_calendar(self):
        """Sett opp innholdskalender"""
        
        calendar = {
            'weekly_schedule': {
                'monday': {
                    'tiktok': 'Weekend recap clip',
                    'instagram': 'Story: Behind the scenes'
                },
                'tuesday': {
                    'tiktok': 'Funny moment clip',
                    'instagram': 'Reel: Episode highlight'
                },
                'wednesday': {
                    'tiktok': 'Trending sound clip',
                    'instagram': 'Post: Episode announcement'
                },
                'thursday': {
                    'tiktok': 'Q&A clip',
                    'instagram': 'Story: Poll'
                },
                'friday': {
                    'tiktok': 'Best of week compilation',
                    'instagram': 'Reel: Weekend vibes'
                },
                'saturday': {
                    'tiktok': 'Throwback clip',
                    'instagram': 'Story: Listener shoutout'
                },
                'sunday': {
                    'tiktok': 'Preview of next week',
                    'instagram': 'Post: Coming up'
                }
            }
        }
        
        calendar_file = self.workspace / 'brain' / 'content-calendar.json'
        with open(calendar_file, 'w') as f:
            json.dump(calendar, f, indent=2)
        
        print(f"  ✅ Innholdskalender satt opp")
        self.actions_taken.append('Setup content calendar')
    
    def print_growth_plan(self):
        """Print vekstplan"""
        
        print("\n" + "=" * 70)
        print("🚀 NRJ MORGEN GROWTH ACTIVATOR")
        print("=" * 70)
        
        print("\n📊 Nåværende Status:")
        print("  👥 Lyttere: 17,108")
        print("  🏆 Ranking: #46 på Podtoppen")
        print("  🎧 Episoder: 157")
        
        print("\n🎯 Mål:")
        print("  3 måneder: 25,000 lyttere (#35)")
        print("  6 måneder: 35,000 lyttere (#25)")
        print("  12 måneder: 50,000 lyttere (#15)")
        
        print("\n📋 Prioriterte Tiltak:")
        for i, opp in enumerate(self.create_action_plan()[:5], 1):
            print(f"\n  {i}. {opp['name']}")
            print(f"     Impact: {opp['impact']} | Effort: {opp['effort']}")
            print(f"     Action: {opp['action']}")
        
        print("\n✅ Utførte Handlinger:")
        for action in self.actions_taken:
            print(f"  ✓ {action}")
        
        print("\n" + "=" * 70)


def main():
    """Main entry point"""
    activator = NRJGrowthActivator()
    
    # Utfør Quick Wins
    activator.execute_quick_wins()
    
    # Print plan
    activator.print_growth_plan()
    
    # Lagre strategi
    strategy = {
        'last_updated': datetime.now().isoformat(),
        'opportunities': activator.identify_growth_opportunities(),
        'action_plan': activator.create_action_plan(),
        'actions_taken': activator.actions_taken
    }
    activator.save_strategy(strategy)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
