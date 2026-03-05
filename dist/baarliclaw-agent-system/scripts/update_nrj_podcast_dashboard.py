#!/usr/bin/env python3
"""
NRJ Morgen Podkast Dashboard Integration
Henter data fra Podtoppen og lagrer i podtoppen_weekly_data tabellen
for visning i nrjmorgen.com/dashboard
"""

import json
import urllib.request
from datetime import datetime

# Supabase konfigurasjon
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"

PODTOPPEN_EXPORT_URL = "https://podtoppen.tnslistene.no/export.php"


def fetch_podtoppen_data():
    """Hent data fra Podtoppen export"""
    try:
        req = urllib.request.Request(
            PODTOPPEN_EXPORT_URL,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            raw_data = response.read()
            csv_data = raw_data.decode('latin-1')
            return csv_data
    except Exception as e:
        print(f"❌ Feil ved henting fra Podtoppen: {e}")
        return None


def find_nrj_morgen_podcast(csv_data):
    """Finn NRJ Morgen Podkast i dataene"""
    
    if not csv_data:
        return None
    
    try:
        lines = csv_data.strip().split('\n')
        
        for i, line in enumerate(lines[1:], 1):  # Start fra 1 for rangering
            if 'nrj morgen' in line.lower():
                parts = line.split(';')
                return {
                    'rank': i,
                    'name': parts[0],
                    'publisher': parts[1],
                    'platform': parts[2],
                    'unique_listeners': int(parts[3]),
                    'downloads_streams': int(parts[4])
                }
        
        return None
    except Exception as e:
        print(f"❌ Feil ved parsing: {e}")
        return None


def insert_to_podtoppen_table(podcast_data):
    """Insert data til podtoppen_weekly_data tabellen"""
    
    if not podcast_data:
        print("❌ Ingen data å inserte")
        return False
    
    # Beregn uke-nummer
    today = datetime.now()
    week_number = today.isocalendar()[1]
    year = today.year
    week_key = f"{year}-W{week_number:02d}"
    
    payload = {
        "podcast_name": podcast_data['name'],
        "publisher": podcast_data['publisher'],
        "week_key": week_key,
        "week_number": week_number,
        "year": year,
        "rank": podcast_data['rank'],
        "unique_listeners": podcast_data['unique_listeners'],
        "downloads_streams": podcast_data['downloads_streams'],
        "platform": podcast_data['platform'],
        "scraped_at": datetime.now().isoformat()
    }
    
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/podtoppen_weekly_data",
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        }
    )
    
    try:
        urllib.request.urlopen(req, timeout=10)
        print(f"✅ Data lagret i podtoppen_weekly_data")
        return True
    except Exception as e:
        print(f"❌ Feil ved insert: {e}")
        return False


def main():
    print("🎧 NRJ MORGEN PODKAST - DASHBOARD INTEGRASJON")
    print("=" * 60)
    print()
    
    # Hent data
    print("🌐 Henter data fra Podtoppen...")
    csv_data = fetch_podtoppen_data()
    
    if not csv_data:
        print("❌ Kunne ikke hente data")
        return
    
    print("✅ Data mottatt!")
    print()
    
    # Finn NRJ Morgen Podkast
    print("🔍 Finner NRJ Morgen Podkast...")
    podcast = find_nrj_morgen_podcast(csv_data)
    
    if not podcast:
        print("❌ NRJ Morgen Podkast ikke funnet")
        return
    
    print(f"✅ Funnet! Rangering: #{podcast['rank']}")
    print()
    
    # Vis data
    print("📊 NRJ MORGEN PODKAST:")
    print("-" * 60)
    print(f"🎧 {podcast['name']}")
    print(f"   Rangering: #{podcast['rank']} på Podtoppen")
    print(f"   Unike lyttere: {podcast['unique_listeners']:,}")
    print(f"   Nedlastet/strømmet: {podcast['downloads_streams']:,}")
    print(f"   Utgiver: {podcast['publisher']}")
    print()
    
    # Lagre til Supabase
    print("💾 Lagrer til podtoppen_weekly_data...")
    if insert_to_podtoppen_table(podcast):
        print()
        print("=" * 60)
        print("🎉 DATA LAGRET FOR DASHBOARD!")
        print("=" * 60)
        print()
        print("📍 Data vil vises i NRJ Statistikk panelet på dashboardet")
    else:
        print("❌ Kunne ikke lagre data")


if __name__ == "__main__":
    main()
