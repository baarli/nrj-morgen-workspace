#!/usr/bin/env python3
"""
NRJ Dashboard Stats - Hent data for visning i dashboard paneler

Dette skriptet henter:
1. Nielsen radio-tall for NRJ
2. Podtoppen podkast-tall for NRJ Morgen

Dataen skal vises i to dedikerte paneler på nrjmorgen.com/dashboard:
- Venstre panel: Podtoppen (rød/oransje)
- Høyre panel: Nielsen (mørk)

VIKTIG: Data lagres IKKE i sakslista. Dashboard-panelene henter 
data direkte fra:
- nielsen_weekly_metrics (for Nielsen panel)
- podtoppen_weekly_data (for Podtoppen panel)

Dette skriptet viser nåværende data som skal vises i panelene.
"""

import os
import json
import urllib.request
from datetime import datetime

NIELSEN_API_URL = os.environ.get("NIELSEN_API_URL", "")

PODTOPPEN_EXPORT_URL = "https://podtoppen.tnslistene.no/export.php"


def fetch_nielsen_nrj():
    """Hent NRJ radio-tall fra Nielsen API"""
    try:
        req = urllib.request.Request(
            NIELSEN_API_URL,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            series_data = data['seriesMDData'][0]
            data2d = series_data['data2D']
            
            for row in data2d:
                if row[0] == "NRJ":
                    weekly_values = [int(x) * 1000 for x in row[1:9]]
                    current = weekly_values[-1]
                    previous = weekly_values[-2]
                    change = current - previous
                    change_pct = (change / previous) * 100
                    
                    return {
                        'daily_listeners': current,
                        'change': change,
                        'change_pct': change_pct,
                        'week': 'Uke 7',
                        'last_updated': data.get('last_updated_date', datetime.now().isoformat())
                    }
            return None
    except Exception as e:
        print(f"❌ Feil: {e}")
        return None


def fetch_podtoppen_nrj():
    """Hent NRJ Morgen Podkast tall fra Podtoppen"""
    try:
        req = urllib.request.Request(
            PODTOPPEN_EXPORT_URL,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            raw_data = response.read()
            csv_data = raw_data.decode('latin-1')
            
            lines = csv_data.strip().split('\n')
            
            for i, line in enumerate(lines[1:], 1):
                if 'nrj morgen' in line.lower():
                    parts = line.split(';')
                    return {
                        'rank': i,
                        'name': parts[0],
                        'unique_listeners': int(parts[3]),
                        'downloads': int(parts[4]),
                        'week': 'Uke 8'
                    }
            return None
    except Exception as e:
        print(f"❌ Feil: {e}")
        return None


def main():
    print("📊 NRJ DASHBOARD STATS")
    print("=" * 60)
    print()
    print("Henter data for visning i dashboard paneler...")
    print()
    
    # Hent Nielsen data
    nielsen = fetch_nielsen_nrj()
    
    # Hent Podtoppen data
    podtoppen = fetch_podtoppen_nrj()
    
    print("=" * 60)
    print()
    
    # Vis Podtoppen panel data
    if podtoppen:
        print("🎧 PODTOPPEN PANEL (Venstre side - Rød/Oransje)")
        print("-" * 60)
        print(f"   Rangering:    #{podtoppen['rank']}")
        print(f"   Navn:         {podtoppen['name']}")
        print(f"   Unike lyttere: {podtoppen['unique_listeners']:,}")
        print(f"   Nedlastet:    {podtoppen['downloads']:,}")
        print(f"   Uke:          {podtoppen['week']}")
        print()
    
    # Vis Nielsen panel data
    if nielsen:
        print("📻 NIELSEN PANEL (Høyre side - Mørk)")
        print("-" * 60)
        print(f"   Daglige lyttere: {nielsen['daily_listeners']:,}")
        print(f"   Endring:         {nielsen['change']:+,.0f}")
        print(f"   Endring %:       {nielsen['change_pct']:+.1f}%")
        print(f"   Uke:             {nielsen['week']}")
        print()
    
    print("=" * 60)
    print()
    print("✅ DATA HENTET!")
    print()
    print("📍 Disse dataene skal vises i:")
    print("   - Podtoppen panel (venstre side)")
    print("   - Nielsen panel (høyre side)")
    print()
    print("📝 VIKTIG:")
    print("   Data lagres IKKE i sakslista!")
    print("   Panelene henter data direkte fra:")
    print("   - nielsen_weekly_metrics tabellen")
    print("   - podtoppen_weekly_data tabellen")
    print()
    print("   For å oppdatere data i panelene:")
    print("   1. Kjør Supabase function 'nielsen-scrape'")
    print("   2. Kjør Supabase function 'podtoppen-scrape'")
    print()


if __name__ == "__main__":
    main()
