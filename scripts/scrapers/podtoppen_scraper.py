#!/usr/bin/env python3
"""
Podtoppen Scraper - Hent ekte data fra podtoppen.tnslistene.no
"""

import re
import urllib.request
from datetime import datetime
from typing import Dict, Optional


class PodtoppenScraper:
    """Scrape podtoppen for NRJ Morgen Podkast statistikk"""
    
    BASE_URL = "https://podtoppen.tnslistene.no/"
    PODCAST_ID = "3873"
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_page(self) -> str:
        """Hent HTML-side fra podtoppen"""
        try:
            req = urllib.request.Request(self.BASE_URL, headers=self.headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            print(f"❌ Feil ved henting av side: {e}")
            return ""
    
    def parse_stats(self, html: str) -> Optional[Dict]:
        """Parse HTML og trekk ut statistikk for NRJ Morgen"""
        if not html:
            return None
        
        # Finn raden med NRJ Morgen Podkast
        # Pattern: tr id=3873 ... /tr
        pattern = r"tr id=" + self.PODCAST_ID + r"(.*?)\/tr"
        match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
        
        if not match:
            print("❌ Fant ikke NRJ Morgen i tabellen")
            return None
        
        row_html = match.group(1)
        
        stats = {
            "podcast_name": "NRJ Morgen Podkast",
            "podcast_id": self.PODCAST_ID,
            "source": "podtoppen.tnslistene.no",
            "scraped_at": datetime.now().isoformat(),
            "url": self.BASE_URL
        }
        
        # 1. Rangering (første td med class='number')
        rank_match = re.search(r"td class='number'\s*\u003e\s*(\d+)", row_html)
        if rank_match:
            stats["rank"] = int(rank_match.group(1))
        
        # 2. Podcast-navn
        name_match = re.search(r"\u003e([^\u003c]+)Podkast\u003c", row_html)
        if name_match:
            stats["podcast_name"] = name_match.group(1).strip() + " Podkast"
        
        # 3. Utgiver
        publisher_match = re.search(r"class='[^']*utgiver[^']*'\u003e([^\u003c]+)", row_html)
        if publisher_match:
            stats["publisher"] = publisher_match.group(1).strip()
        
        # 4. Kategori (hidden field)
        category_match = re.search(r"hidden\u003e([^\u003c]+)\u003c", row_html)
        if category_match:
            stats["category"] = category_match.group(1).strip()
        
        # 5. Ukentlige lyttere (første tall etter publisher)
        # Pattern: <td>16 470<span
        listeners_match = re.search(r"\u003ctd\u003e([\d\s]+)\u003cspan", row_html)
        if listeners_match:
            listeners = listeners_match.group(1).replace(' ', '').replace('\xa0', '')
            stats["weekly_listeners"] = int(listeners) if listeners.isdigit() else 0
        
        # 6. Endring prosent
        # Pattern: -2 % eller +5 %
        change_match = re.search(r"([+-]?)\s*(\d+)\s*%", row_html)
        if change_match:
            sign = -1 if change_match.group(1) == '-' else 1
            stats["weekly_change_percent"] = sign * int(change_match.group(2))
        
        # 7. Pil-retning (opp/ned)
        if "arrow down" in row_html or "red" in row_html:
            stats["trend_direction"] = "down"
        elif "arrow up" in row_html or "green" in row_html:
            stats["trend_direction"] = "up"
        else:
            stats["trend_direction"] = "stable"
        
        return stats
    
    def get_current_stats(self) -> Optional[Dict]:
        """Hent nåværende statistikk fra Podtoppen"""
        print("🎧 Henter data fra podtoppen.tnslistene.no...")
        
        html = self.fetch_page()
        if not html:
            return None
        
        stats = self.parse_stats(html)
        
        if stats:
            print(f"   ✅ Rangering: #{stats.get('rank', 'N/A')}")
            print(f"   📊 {stats.get('weekly_listeners', 0):,} ukentlige lyttere")
            print(f"   📈 Endring: {stats.get('weekly_change_percent', 0):+d}%")
        
        return stats


if __name__ == "__main__":
    scraper = PodtoppenScraper()
    stats = scraper.get_current_stats()
    
    if stats:
        print("\n" + "="*60)
        print("📊 KOMPLETT PODTOPPEN DATA")
        print("="*60)
        for key, value in stats.items():
            if isinstance(value, int):
                print(f"{key:25}: {value:,}")
            else:
                print(f"{key:25}: {value}")
        print("="*60)
    else:
        print("❌ Kunne ikke hente data")
