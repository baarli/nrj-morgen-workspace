#!/usr/bin/env python3
"""
🤝 Outreach Campaign Manager - Systematisk outreach for vekst
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

class OutreachCampaignManager:
    """Håndter outreach-kampanjer for NRJ Morgen"""
    
    def __init__(self):
        self.workspace = Path('/root/.openclaw/workspace')
        self.campaign_dir = self.workspace / 'brain' / 'outreach-campaigns'
        self.campaign_dir.mkdir(parents=True, exist_ok=True)
        
    def identify_targets(self) -> list:
        """Identifiser potensielle samarbeidspartnere"""
        
        targets = [
            {
                'name': 'P3morgen',
                'platform': 'NRK Radio',
                'category': 'Radio Show',
                'audience_size': 'Large',
                'fit': 'High',
                'approach': 'Cross-promotion',
                'priority': 1
            },
            {
                'name': 'Jan Thomas',
                'platform': 'Instagram/TikTok',
                'category': 'Influencer',
                'audience_size': 'Large',
                'fit': 'High',
                'approach': 'Guest appearance',
                'priority': 2
            },
            {
                'name': 'Sophie Elise',
                'platform': 'Podcast/Blog',
                'category': 'Influencer',
                'audience_size': 'Large',
                'fit': 'High',
                'approach': 'Cross-promotion',
                'priority': 3
            },
            {
                'name': 'Mads Hansen',
                'platform': 'YouTube/TikTok',
                'category': 'Creator',
                'audience_size': 'Medium',
                'fit': 'High',
                'approach': 'Collaboration',
                'priority': 4
            },
            {
                'name': 'Paradise Hotel Norge',
                'platform': 'TV/Instagram',
                'category': 'Reality TV',
                'audience_size': 'Large',
                'fit': 'High',
                'approach': 'Content partnership',
                'priority': 5
            },
            {
                'name': 'Farmen',
                'platform': 'TV/Instagram',
                'category': 'Reality TV',
                'audience_size': 'Large',
                'fit': 'Medium',
                'approach': 'Content partnership',
                'priority': 6
            },
            {
                'name': 'Kompani Lauritzen',
                'platform': 'TV/Instagram',
                'category': 'Reality TV',
                'audience_size': 'Medium',
                'fit': 'Medium',
                'approach': 'Content partnership',
                'priority': 7
            },
            {
                'name': 'Norsk Podcast',
                'platform': 'Various',
                'category': 'Podcast Network',
                'audience_size': 'Medium',
                'fit': 'High',
                'approach': 'Network partnership',
                'priority': 8
            },
            {
                'name': 'Se og Hør',
                'platform': 'Magazine/Online',
                'category': 'Media',
                'audience_size': 'Large',
                'fit': 'High',
                'approach': 'Media partnership',
                'priority': 9
            },
            {
                'name': 'Dagbladet Kjendis',
                'platform': 'Online',
                'category': 'Media',
                'audience_size': 'Large',
                'fit': 'Medium',
                'approach': 'Content sharing',
                'priority': 10
            }
        ]
        
        # Sorter etter prioritet
        targets.sort(key=lambda x: x['priority'])
        
        return targets
    
    def generate_outreach_message(self, target: dict) -> str:
        """Generer tilpasset outreach-melding"""
        
        base_message = f"""Hei {target['name']}!

Jeg heter [Ditt navn] og jobber med NRJ Morgen podcast - en av Norges raskest voksende morgenpodcaster med Baarli og Benjamin.

Vi har 17,000+ lyttere per episode og fokuserer på reality-TV, kjendisnyheter og populærkultur - perfekt for {target['category']}-publikum!

Jeg ser på {target['name']} som en perfekt match for et samarbeid. Her er noen ideer:

"""
        
        if target['approach'] == 'Cross-promotion':
            base_message += """• Cross-promotion på sosiale medier
• Gjesteopptreden i hverandres kanaler
• Felles content serie
"""
        elif target['approach'] == 'Guest appearance':
            base_message += """• Guest appearance i vår podcast
• Behind-the-scenes content
• Q&A session med lyttere
"""
        elif target['approach'] == 'Collaboration':
            base_message += """• Samarbeid om felles episode
• Cross-platform content
• Joint social media campaign
"""
        elif target['approach'] == 'Content partnership':
            base_message += """• Eksklusivt behind-the-scenes innhold
• Tidlig tilgang til nyheter
• Co-created content series
"""
        
        base_message += f"""
Hva tenker du? Jeg er åpen for å diskutere ulike muligheter!

Beste hilsen,
[Ditt navn]
NRJ Morgen Podcast
📧 kontakt@nrjmorgen.no
📱 @nrjmorgen (Instagram/TikTok)

---
PS: Hør gjerne på vår siste episode for å bli kjent med stilen vår! 🎙️"""
        
        return base_message
    
    def create_campaign(self, campaign_name: str) -> dict:
        """Opprett en komplett kampanje"""
        
        targets = self.identify_targets()
        
        campaign = {
            'name': campaign_name,
            'created': datetime.now().isoformat(),
            'status': 'active',
            'targets': []
        }
        
        for target in targets:
            target_data = {
                **target,
                'message': self.generate_outreach_message(target),
                'status': 'pending',
                'contacted': None,
                'response': None,
                'notes': ''
            }
            campaign['targets'].append(target_data)
        
        return campaign
    
    def save_campaign(self, campaign: dict):
        """Lagre kampanje til fil"""
        
        filename = f"campaign-{campaign['name'].lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d')}.json"
        filepath = self.campaign_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(campaign, f, indent=2)
        
        return filepath
    
    def generate_action_plan(self) -> str:
        """Generer handlingsplan"""
        
        plan = """# 🤝 Outreach Action Plan

## Uke 1-2: Forberedelse
- [ ] Fullfør profil-optimalisering (Instagram/TikTok)
- [ ] Lag 5-10 eksempel-innlegg
- [ ] Sett opp tracking system

## Uke 3-4: Første kontakt (Prioritet 1-3)
- [ ] Kontakte P3morgen
- [ ] Kontakte Jan Thomas
- [ ] Kontakte Sophie Elise

## Uke 5-6: Utvidelse (Prioritet 4-7)
- [ ] Kontakte Mads Hansen
- [ ] Kontakte Paradise Hotel
- [ ] Kontakte Farmen
- [ ] Kontakte Kompani Lauritzen

## Uke 7-8: Media-partnerskap (Prioritet 8-10)
- [ ] Kontakte Norsk Podcast
- [ ] Kontakte Se og Hør
- [ ] Kontakte Dagbladet Kjendis

## Mål:
- 3-5 positive responser
- 1-2 faktiske samarbeid
- 10% økning i følgere fra cross-promotion
"""
        
        return plan
    
    def print_campaign_summary(self):
        """Print kampanje-sammendrag"""
        
        campaign = self.create_campaign('Q1 2026 Growth')
        filepath = self.save_campaign(campaign)
        
        # Lagre action plan
        plan_file = self.campaign_dir / 'action-plan.md'
        with open(plan_file, 'w') as f:
            f.write(self.generate_action_plan())
        
        print("\n" + "=" * 70)
        print("🤝 OUTREACH CAMPAIGN MANAGER")
        print("=" * 70)
        
        print(f"\n📋 Kampanje: {campaign['name']}")
        print(f"   Opprettet: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"   Lagret til: {filepath}")
        
        print(f"\n🎯 Identifiserte Mål ({len(campaign['targets'])} totalt):")
        
        for target in campaign['targets'][:5]:
            print(f"\n  {target['priority']}. {target['name']}")
            print(f"     Plattform: {target['platform']}")
            print(f"     Tilnærming: {target['approach']}")
            print(f"     Match: {target['fit']}")
        
        print(f"\n... og {len(campaign['targets']) - 5} til")
        
        print("\n" + "-" * 70)
        print("\n📧 Eksempel på outreach-melding (Jan Thomas):")
        print("-" * 70)
        print(campaign['targets'][1]['message'][:500] + "...")
        
        print("\n" + "=" * 70)
        print("\n✅ Neste steg:")
        print("   1. Les action-plan.md for detaljert tidsplan")
        print("   2. Tilpass meldingene med ditt navn")
        print("   3. Start outreach til prioritet 1-3")
        print("   4. Track responser i kampanje-filen")
        print("=" * 70)


def main():
    """Main entry point"""
    manager = OutreachCampaignManager()
    manager.print_campaign_summary()
    return 0


if __name__ == '__main__':
    sys.exit(main())
