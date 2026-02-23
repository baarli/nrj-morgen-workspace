#!/usr/bin/env python3
"""
NRJ Morgen Podkast - Hent EKTE tall fra Podtoppen
Fokuserer spesifikt på NRJ Morgen Podkast for visning på dashboardet
"""

import json
import urllib.request
from datetime import datetime

# Supabase konfigurasjon
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"
TENANT_ID = "a0000000-0000-0000-0000-000000000001"
BAARLI_CLAW_ID = "10aa1508-6d52-490c-8ae5-fa3da9a152c4"

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
    """Finn spesifikt NRJ Morgen Podkast"""
    
    if not csv_data:
        return None
    
    try:
        lines = csv_data.strip().split('\n')
        
        # Hopp over header
        for line in lines[1:]:
            parts = line.split(';')
            if len(parts) >= 5:
                name = parts[0]
                author = parts[1]
                platform = parts[2]
                devices = parts[3]
                downloads = parts[4]
                
                # Se etter NRJ Morgen Podkast spesifikt
                if 'nrj morgen' in name.lower():
                    try:
                        devices_int = int(devices)
                        downloads_int = int(downloads)
                    except:
                        devices_int = 0
                        downloads_int = 0
                    
                    return {
                        'name': name,
                        'author': author,
                        'platform': platform,
                        'devices': devices_int,
                        'downloads': downloads_int,
                        'rank': None  # Vil bli satt senere
                    }
        
        return None
        
    except Exception as e:
        print(f"❌ Feil ved parsing: {e}")
        return None


def find_ranking(csv_data, podcast_name):
    """Finn rangering for podkasten"""
    try:
        lines = csv_data.strip().split('\n')
        
        for i, line in enumerate(lines[1:], 1):  # Start fra 1 for å telle rangering
            if podcast_name in line:
                return i
        
        return None
    except:
        return None


def insert_to_supabase(podcast_data, rank):
    """Insert NRJ Morgen Podkast data til Supabase"""
    
    if not podcast_data:
        print("❌ Ingen data å inserte")
        return False
    
    title = f"🎧 NRJ Morgen Podkast - {podcast_data['devices']:,} lyttere"
    
    description = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #ff6b00;">🎧 NRJ Morgen Podkast</h2>
        <div style="font-size: 24px; font-weight: bold; margin: 10px 0;">
            {podcast_data['devices']:,} unike lyttere
        </div>
        <div style="font-size: 18px; color: #666;">
            {podcast_data['downloads']:,} nedlastet/strømmet
        </div>
        <div style="margin-top: 15px; padding: 10px; background: #f5f5f5; border-radius: 5px;">
            <strong>Rangering:</strong> #{rank} på Podtoppen<br>
            <strong>Utgiver:</strong> {podcast_data['author']}<br>
            <strong>Sist oppdatert:</strong> {datetime.now().strftime('%d.%m.%Y')}
        </div>
    </div>
    """
    
    notes = f"""📊 NRJ MORGEN PODKAST - PODTOPPEN DATA

🎧 PODKAST: {podcast_data['name']}

📈 TALL:
• Rangering: #{rank} på Podtoppen
• Unike lyttere: {podcast_data['devices']:,}
• Nedlastet/strømmet: {podcast_data['downloads']:,}
• Utgiver: {podcast_data['author']}
• Plattform: {podcast_data['platform']}

🔗 KILDE:
• Podtoppen (Kantar/TNS)
• https://podtoppen.tnslistene.no/
• Sist oppdatert: {datetime.now().strftime('%Y-%m-%d %H:%M')}

✅ EKTE DATA:
Dette er faktiske målte data fra Kantar/TNS Podtoppen!

📊 FORRIGE UKE:
Sammenlign med forrige ukes tall for å se trend.
"""
    
    payload = {
        "title": title,
        "description": description,
        "notes": notes,
        "category": "TALK",
        "show_date": datetime.now().strftime("%Y-%m-%d"),
        "tenant_id": TENANT_ID,
        "created_by": BAARLI_CLAW_ID,
        "is_pinned": True,  # Pin til toppen av dashboardet
        "order_index": 1    # Vis først
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
        return True
    except Exception as e:
        print(f"❌ Feil ved insert: {e}")
        return False


def main():
    print("🎧 NRJ MORGEN PODKAST - HENTING FRA PODTOPPEN")
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
        print("❌ NRJ Morgen Podkast ikke funnet i topplisten")
        return
    
    # Finn rangering
    rank = find_ranking(csv_data, podcast['name'])
    podcast['rank'] = rank
    
    print(f"✅ Funnet! Rangering: #{rank}")
    print()
    
    # Vis data
    print("📊 NRJ MORGEN PODKAST TALL:")
    print("-" * 60)
    print(f"🎧 {podcast['name']}")
    print(f"   Rangering: #{rank} på Podtoppen")
    print(f"   Unike lyttere: {podcast['devices']:,}")
    print(f"   Nedlastet/strømmet: {podcast['downloads']:,}")
    print(f"   Utgiver: {podcast['author']}")
    print()
    
    # Lagre til Supabase
    print("💾 Lagrer til Supabase (dashboard)...")
    if insert_to_supabase(podcast, rank):
        print()
        print("=" * 60)
        print("🎉 NRJ MORGEN PODKAST DATA LAGRET!")
        print("=" * 60)
        print()
        print("📍 Data vises nå på nrjmorgen.com dashboardet")
        print(f"   Rangering: #{rank}")
        print(f"   Lyttere: {podcast['devices']:,}")
    else:
        print("❌ Kunne ikke lagre data")


if __name__ == "__main__":
    main()
