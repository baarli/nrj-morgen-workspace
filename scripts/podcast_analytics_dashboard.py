#!/usr/bin/env python3
"""
📈 Podcast Analytics Dashboard - Visuell oversikt over podcast-statistikk
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, '/root/.openclaw/workspace/scripts')

class PodcastAnalyticsDashboard:
    """Generer visuell analytics dashboard for NRJ Morgen podcast"""
    
    def __init__(self):
        self.workspace = Path('/root/.openclaw/workspace')
        self.data_dir = self.workspace / 'brain' / 'podcast-analytics'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_mock_data(self) -> Dict:
        """Generer mock data for demonstrasjon (kan erstattes med faktisk data)"""
        
        # Simulert data for siste 12 uker
        weeks = []
        base_listeners = 16000
        
        for i in range(12, 0, -1):
            week_date = datetime.now() - timedelta(weeks=i)
            
            # Simulert vekst med variasjon
            growth = 1 + (0.02 * (12 - i) / 12)  # 2% vekst over perioden
            listeners = int(base_listeners * growth * (0.95 + 0.1 * (i % 3)))
            
            weeks.append({
                'week': week_date.strftime('%Y-W%W'),
                'listeners': listeners,
                'downloads': int(listeners * 2.1),
                'rank': max(40, 62 - int((12 - i) * 1.5))  # Simulert ranking-forbedring
            })
        
        return {
            'current_listeners': weeks[-1]['listeners'],
            'current_rank': weeks[-1]['rank'],
            'total_episodes': 157,
            'weekly_data': weeks,
            'growth_rate': 15.5,  # %
            'avg_listen_duration': 35.2,  # minutter
            'completion_rate': 68.5  # %
        }
    
    def create_ascii_chart(self, data: List[int], labels: List[str], width: int = 50) -> str:
        """Lag ASCII bar chart"""
        if not data:
            return "Ingen data"
        
        max_val = max(data)
        min_val = min(data)
        
        lines = []
        lines.append("" + "-" * (width + 15))
        
        for i, (val, label) in enumerate(zip(data, labels)):
            bar_len = int((val / max_val) * width) if max_val > 0 else 0
            bar = "█" * bar_len
            lines.append(f"{label:12} │{bar:<{width}}│ {val:,}")
        
        lines.append("" + "-" * (width + 15))
        return "\n".join(lines)
    
    def generate_dashboard(self) -> str:
        """Generer komplett dashboard"""
        data = self.generate_mock_data()
        
        dashboard = f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                    🎙️ NRJ MORGEN PODCAST ANALYTICS                      ║
║                         Dashboard - {datetime.now().strftime('%Y-%m-%d %H:%M')}                         ║
╚══════════════════════════════════════════════════════════════════════════╝

📊 NØKKELTALL
┌─────────────────────────────────────────────────────────────────────────┐
│  👥 Unike Lyttere:     {data['current_listeners']:>10,}                    │
│  🏆 Podtoppen Rank:    #{data['current_rank']:>9}                      │
│  🎧 Episoder:          {data['total_episodes']:>10}                    │
│  📈 Vekstrate:         {data['growth_rate']:>9.1f}%                    │
│  ⏱️  Avg. Lyttetid:    {data['avg_listen_duration']:>9.1f} min          │
│  ✅ Fullføringsrate:   {data['completion_rate']:>9.1f}%                │
└─────────────────────────────────────────────────────────────────────────┘

📈 LYTTERVEKST (Siste 12 uker)
{self.create_ascii_chart(
    [w['listeners'] for w in data['weekly_data']],
    [w['week'][-2:] for w in data['weekly_data']]
)}

🏆 RANKING UTVIKLING
{self.create_ascii_chart(
    [70 - w['rank'] for w in data['weekly_data']],  # Invertert for bedre visuell
    [w['week'][-2:] for w in data['weekly_data']]
)}
* Høyere bar = bedre ranking

📥 DOWNLOADS PER EPISODE
{self.create_ascii_chart(
    [w['downloads'] for w in data['weekly_data']],
    [w['week'][-2:] for w in data['weekly_data']]
)}

🎯 MÅLSETTINGER
┌─────────────────────────────────────────────────────────────────────────┐
│  Kort sikt (6 mnd):    25,000 lyttere  │  #{40} ranking              │
│  Medium (12 mnd):      35,000 lyttere  │  #{30} ranking              │
│  Lang sikt (24 mnd):   50,000 lyttere  │  #{20} ranking              │
└─────────────────────────────────────────────────────────────────────────┘

💡 ANBEFALTE TILTAK
1. 🎬 Start YouTube-kanal for video-podcast
2. 📱 Øke TikTok/Instagram-aktivitet til 3x daglig
3. 🎁 Introduksjon av lytter-lojalitetsprogram
4. 🤝 Samarbeid med influencers for cross-promotion
5. 📧 Ukentlig nyhetsbrev til abonnenter

═══════════════════════════════════════════════════════════════════════════
Generert av BaarliClaw Podcast Analytics System
"""
        
        return dashboard
    
    def save_dashboard(self):
        """Lagre dashboard til fil"""
        dashboard = self.generate_dashboard()
        
        # Lagre som tekst
        date_str = datetime.now().strftime('%Y-%m-%d')
        text_file = self.data_dir / f'dashboard-{date_str}.txt'
        with open(text_file, 'w') as f:
            f.write(dashboard)
        
        # Lagre data som JSON
        data_file = self.data_dir / f'data-{date_str}.json'
        with open(data_file, 'w') as f:
            json.dump(self.generate_mock_data(), f, indent=2)
        
        return text_file, data_file


def main():
    """Main entry point"""
    dashboard = PodcastAnalyticsDashboard()
    
    # Print dashboard
    print(dashboard.generate_dashboard())
    
    # Lagre til fil
    text_file, data_file = dashboard.save_dashboard()
    print(f"\n💾 Dashboard lagret til: {text_file}")
    print(f"💾 Data lagret til: {data_file}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
