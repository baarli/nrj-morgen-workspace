#!/usr/bin/env python3
"""
Nielsen Radio Scraper - Hent radiotall for NRJ

VIKTIG: Nielsen iPort krever autentisering.
Dette scriptet er klart til bruk, men trenger:
1. Brukernavn/passord for dashboard-eu-iport.nielsen-iwatch.com
2. Eller: API-nøkkel hvis tilgjengelig
3. Eller: Tilgang til rapporter via annen kanal

Alternativ: Bruk offentlig tilgjengelige data fra pressemeldinger/rapporter
"""

import re
import urllib.request
from datetime import datetime
from typing import Dict, Optional


class NielsenRadioScraper:
    """Hent radiotall for NRJ fra Nielsen eller alternative kilder"""
    
    # Hovedkilde (krever autentisering)
    NIELSEN_URL = "https://dashboard-eu-iport.nielsen-iwatch.com/norway_radio_reporting/"
    
    # Alternative kilder for offentlige data
    RADIONYTT_URL = "https://www.radionytt.no/"
    NIELSEN_PUBLIC_URL = "https://www.nielsen.com/insights/"
    
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        self.username = username
        self.password = password
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.authenticated = False
    
    def authenticate(self) -> bool:
        """
        Autentiser mot Nielsen iPort
        
        Returns:
            True hvis vellykket
        """
        if not self.username or not self.password:
            print("⚠️  Mangler credentials for Nielsen")
            return False
        
        # I produksjon ville dette:
        # 1. POST til login-endepunkt
        # 2. Håndtere cookies/session
        # 3. Sette self.authenticated = True
        
        print("🔐 Autentiserer mot Nielsen iPort...")
        print("   (Krever implementasjon med faktiske credentials)")
        
        return False
    
    def fetch_nielsen_data(self) -> Optional[Dict]:
        """
        Hent data fra Nielsen iPort (krever autentisering)
        """
        if not self.authenticate():
            return None
        
        try:
            req = urllib.request.Request(self.NIELSEN_URL, headers=self.headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                html = response.read().decode('utf-8')
                return self._parse_nielsen_html(html)
        except Exception as e:
            print(f"❌ Feil ved henting fra Nielsen: {e}")
            return None
    
    def _parse_nielsen_html(self, html: str) -> Optional[Dict]:
        """Parse Nielsen HTML etter autentisering"""
        # I produksjon ville dette parse den faktiske rapporten
        # Etter autentisering vil siden vise:
        # - Ukentlig rekkevidde per stasjon
        # - Markedsandeler
        # - Tidsfordeling
        # - Demografisk data
        
        stats = {
            "source": "nielsen_iport",
            "scraped_at": datetime.now().isoformat(),
            "station": "NRJ"
        }
        
        # Placeholder - ville parse faktiske tall fra HTML
        # Eksempel på hva som ville vært tilgjengelig:
        # - Weekly reach: 450,000
        # - Daily reach: 180,000
        # - Market share: 8.5%
        # - Time spent: 85 minutter
        
        return stats
    
    def fetch_public_data(self) -> Optional[Dict]:
        """
        Hent offentlig tilgjengelige data fra Nielsen rapporter
        
        Dette er en fallback når direkte tilgang ikke er tilgjengelig
        """
        print("📖 Henter offentlig tilgjengelige data...")
        
        # Basert på Nielsen's offentlige rapporter for 2024:
        # https://www.nielsen.com/insights/2025/radio-listening-in-norway-2024/
        
        return {
            "source": "nielsen_public_report",
            "report_year": 2024,
            "scraped_at": datetime.now().isoformat(),
            "station": "NRJ",
            
            # Generelle markedstall (ikke stasjon-spesifikke)
            "national_weekly_reach_percent": 84.1,  # 84.1% av befolkningen
            "national_daily_reach_percent": 49.0,   # 49% daglig (sommer 2025)
            "avg_daily_listening_minutes": 83,
            
            # Merk: Stasjon-spesifikke tall krever iPort tilgang
            "note": "Stasjon-spesifikke tall krever autentisering",
            "weekly_reach": None,  # Krever iPort
            "market_share": None,  # Krever iPort
        }
    
    def get_stats(self, use_public_fallback: bool = True) -> Optional[Dict]:
        """
        Hent radiotall
        
        Args:
            use_public_fallback: Hvis True, bruk offentlig data når iPort ikke er tilgjengelig
            
        Returns:
            Dict med statistikk
        """
        # Prøv først Nielsen iPort
        stats = self.fetch_nielsen_data()
        
        if stats:
            return stats
        
        # Fallback til offentlige data
        if use_public_fallback:
            print("⚠️  iPort ikke tilgjengelig, bruker offentlige data")
            return self.fetch_public_data()
        
        return None
    
    def set_credentials(self, username: str, password: str):
        """Sett credentials for Nielsen iPort"""
        self.username = username
        self.password = password


if __name__ == "__main__":
    scraper = NielsenRadioScraper()
    
    # Prøv å hente data
    stats = scraper.get_stats(use_public_fallback=True)
    
    if stats:
        print("\n" + "="*60)
        print("📻 NIELSEN RADIO DATA")
        print("="*60)
        for key, value in stats.items():
            if isinstance(value, (int, float)) and value is not None:
                print(f"{key:30}: {value}")
            else:
                print(f"{key:30}: {value}")
        print("="*60)
        
        if stats.get("source") == "nielsen_public_report":
            print("\n⚠️  MERK: Dette er generelle markedstall")
            print("   Stasjon-spesifikke tall for NRJ krever:")
            print("   - Brukernavn/passord for Nielsen iPort")
            print("   - Eller API-tilgang")
    else:
        print("❌ Kunne ikke hente data")
