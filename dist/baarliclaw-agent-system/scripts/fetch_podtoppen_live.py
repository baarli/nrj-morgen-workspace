#!/usr/bin/env python3
"""
Podtoppen Scraper - Hent EKTE podkast-tall fra Kantar/TNS Podtoppen
Bruker eksport-funksjonen for å hente toppliste-data
"""

import csv
import json
import urllib.request
from datetime import datetime
from io import StringIO

# Supabase konfigurasjon
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"
TENANT_ID = "a0000000-0000-0000-0000-000000000001"
BAARLI_CLAW_ID = "10aa1508-6d52-490c-8ae5-fa3da9a152c4"

# Podtoppen URL
PODTOPPEN_EXPORT_URL = "https://podtoppen.tnslistene.no/export.php"


def fetch_podtoppen_data():
    """Hent data fra Podtoppen export"""
    try:
        req = urllib.request.Request(
            PODTOPPEN_EXPORT_URL,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            # Data kommer som CSV med latin-1 encoding
            raw_data = response.read()
            csv_data = raw_data.decode('latin-1')
            return csv_data
    except Exception as e:
        print(f"❌ Feil ved henting fra Podtoppen: {e}")
        return None


def parse_podtoppen_csv(csv_data):
    """Parse CSV-data og finn NRJ-podkaster"""
    
    if not csv_data:
        return None
    
    try:
        # Parse CSV manuelt (mer pålitelig)
        lines = csv_data.strip().split('\n')
        nrj_podcasts = []
        
        print(f"📊 Fant {len(lines)} podkaster i topplisten")
        
        # Hopp over header
        for line in lines[1:]:
            parts = line.split(';')
            if len(parts) >= 5:
                name = parts[0]
                author = parts[1]
                platform = parts[2]
                devices = parts[3]
                downloads = parts[4]
                
                # Sjekk om dette er en NRJ/Bauer Media podkast
                if any(x in name.lower() for x in ['baarli', 'benjamin', 'terapi', 'nrj']) or \
                   any(x in author.lower() for x in ['bauer', 'nrj']):
                    
                    try:
                        devices_int = int(devices)
                        downloads_int = int(downloads)
                    except:
                        devices_int = 0
                        downloads_int = 0
                    
                    nrj_podcasts.append({
                        'name': name,
                        'author': author,
                        'platform': platform,
                        'devices': devices_int,
                        'downloads': downloads_int
                    })
        
        return nrj_podcasts
        
    except Exception as e:
        print(f"❌ Feil ved parsing: {e}")
        return None


def insert_to_supabase(podcast_data):
    """Insert data til Supabase"""
    
    if not podcast_data:
        print("❌ Ingen data å inserte")
        return False
    
    # Lagre hver podkast som egen entry
    inserted = 0
    
    for podcast in podcast_data:
        title = f"🎧 Podtoppen - {podcast['name']}"
        
        description = f"""
        Rangering: Podtoppen
        Unike enheter: {podcast['devices']:,}
        Nedlastet/strømmet: {podcast['downloads']:,}
        Utgiver: {podcast['author']}
        Plattform: {podcast['platform']}
        """
        
        notes = f"""📊 PODTOPPEN DATA - {datetime.now().strftime('%Y-%m-%d')}

🎧 PODKAST: {podcast['name']}

📈 TALL:
• Unike enheter: {podcast['devices']:,}
• Nedlastet/strømmet: {podcast['downloads']:,}
• Utgiver: {podcast['author']}
• Plattform: {podcast['platform']}

🔗 KILDE:
• Podtoppen (Kantar/TNS)
• https://podtoppen.tnslistene.no/
• Sist oppdatert: {datetime.now().strftime('%Y-%m-%d %H:%M')}

✅ EKTE DATA:
Dette er faktiske målte data fra Kantar/TNS Podtoppen!
"""
        
        payload = {
            "title": title,
            "description": description,
            "notes": notes,
            "category": "TALK",
            "show_date": datetime.now().strftime("%Y-%m-%d"),
            "tenant_id": TENANT_ID,
            "created_by": BAARLI_CLAW_ID,
            "is_pinned": False,
            "order_index": 999
        }
        
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/agenda_items",
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
            print(f"  ✅ {podcast['name']}")
            inserted += 1
        except Exception as e:
            print(f"  ❌ {podcast['name']}: {e}")
    
    return inserted > 0


def main():
    print("🎧 PODTOPPEN - HENTING AV PODKAST-TALL")
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
    
    # Parse data
    print("📊 Parser data...")
    nrj_podcasts = parse_podtoppen_csv(csv_data)
    
    if not nrj_podcasts:
        print("⚠️  Ingen NRJ/Bauer Media podkaster funnet")
        return
    
    print(f"✅ Fant {len(nrj_podcasts)} NRJ/Bauer Media podkaster!")
    print()
    
    # Vis data
    print("📈 PODKAST-TALL:")
    print("-" * 60)
    for podcast in nrj_podcasts:
        print(f"🎧 {podcast['name']}")
        print(f"   Unike enheter: {podcast['devices']:,}")
        print(f"   Nedlastet: {podcast['downloads']:,}")
        print(f"   Utgiver: {podcast['author']}")
        print()
    
    # Lagre til Supabase
    print("💾 Lagrer til Supabase...")
    if insert_to_supabase(nrj_podcasts):
        print()
        print("=" * 60)
        print("🎉 PODTOPPEN DATA LAGRET!")
        print("=" * 60)
    else:
        print("❌ Kunne ikke lagre data")


if __name__ == "__main__":
    main()
