#!/usr/bin/env python3
"""
Manuell oppdatering av radiotall for NRJ Morgen
Bruker offentlig tilgjengelige data fra Nielsen 2024-2025
"""

import json
import urllib.request
from datetime import datetime

# Supabase konfigurasjon
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"
TENANT_ID = "a0000000-0000-0000-0000-000000000001"
BAARLI_CLAW_ID = "10aa1508-6d52-490c-8ae5-fa3da9a152c4"

# Data fra Nielsen 2024-2025 (offentlig tilgjengelig)
# Kilde: https://www.nielsen.com/insights/2025/radio-listening-in-norway-2024/
NIELSEN_DATA = {
    "report_date": "2026-02-23",
    "data_source": "Nielsen PPM Audio Measurement 2024",
    "source_url": "https://www.nielsen.com/insights/2025/radio-listening-in-norway-2024/",
    
    # Generelle markedstall for Norge
    "national_weekly_reach_percent": 83.1,  # Ned fra 84.1% i 2023
    "national_daily_reach_percent": 58.0,   # Ned fra 60.3% i 2023
    "avg_daily_listening_minutes": 79,      # Ned fra 83 min i 2023
    "avg_daily_listening_minutes_listeners": 136,  # For de som lytter
    
    # Bil-lytting
    "car_daily_reach": 1626000,  # 1.626 mill (33.4% av befolkningen)
    "car_avg_listening_minutes": 44,  # Opp fra 38 min i 2023
    
    # Markedsandeler 2024
    "market_shares": {
        "NRK": 66.0,           # Opp fra 64.9% i 2023
        "P4_Group": 22.1,      # Ned fra 23.2% i 2023
        "Bauer_Media": 11.9    # Uendret fra 2023
    },
    
    # Bauer Media inkluderer: NRJ, Radio Norge, Radio Rock, Kiss
    # Estimert fordeling basert på historiske data:
    "bauer_media_breakdown": {
        "NRJ": 4.2,            # Estimert basert på tidligere tall
        "Radio_Norge": 3.8,    # Estimert
        "Radio_Rock": 2.4,     # Estimert
        "Kiss": 1.5            # Estimert
    },
    
    # Estimerte tall for NRJ (basert på markedsandel)
    # Norge har ~5.4 millioner innbyggere, ~4.5 millioner 15+ år
    "nrj_estimated": {
        "weekly_reach_percent": 4.2,
        "weekly_reach_absolute": 189000,  # 4.2% av 4.5 mill
        "daily_reach_absolute": 75000,    # Estimert
        "avg_listening_minutes": 85       # Estimert
    },
    
    # Podkast-tall
    "podcast_weekly_reach_percent": 40,
    "podcast_daily_reach_percent": 13,
    
    # Notis om datakvalitet
    "note": "Stasjon-spesifikke tall krever Nielsen iPort-tilgang. Tallene over er basert på offentlige markedsandeler og estimater.",
    "disclaimer": "Nielsen iPort krever autentisering for stasjon-spesifikke tall. Bruk dashboard-eu-iport.nielsen-iwatch.com for eksakte tall."
}

def insert_to_supabase(data):
    """Insert radiotall til Supabase"""
    
    # Lag title og description
    title = f"📻 Nielsen Radio Tall - {datetime.now().strftime('%d.%m.%Y')}"
    
    description = f"""
    <h3>🎧 NRJ Radio - Estimerte Lyttertall</h3>
    
    <p><strong>Ukentlig rekkevidde:</strong> ~{data['nrj_estimated']['weekly_reach_absolute']:,} lyttere (4.2%)</p>
    <p><strong>Daglig rekkevidde:</strong> ~{data['nrj_estimated']['daily_reach_absolute']:,} lyttere</p>
    <p><strong>Gjennomsnittlig lyttetid:</strong> {data['nrj_estimated']['avg_listening_minutes']} minutter</p>
    
    <h4>📊 Markedsandeler 2024</h4>
    <ul>
        <li>NRK: {data['market_shares']['NRK']}%</li>
        <li>P4 Group: {data['market_shares']['P4_Group']}%</li>
        <li>Bauer Media: {data['market_shares']['Bauer_Media']}%</li>
    </ul>
    
    <h4>📈 Nasjonale trender</h4>
    <ul>
        <li>Ukentlig rekkevidde: {data['national_weekly_reach_percent']}%</li>
        <li>Daglig rekkevidde: {data['national_daily_reach_percent']}%</li>
        <li>Gjennomsnittlig lyttetid: {data['avg_daily_listening_minutes']} min</li>
    </ul>
    
    <p><em>Kilde: {data['data_source']}</em></p>
    <p><small>{data['note']}</small></p>
    """
    
    # Bygg payload
    payload = {
        "title": title,
        "description": description,
        "notes": json.dumps(data, indent=2, ensure_ascii=False),
        "category": "STATS",
        "show_date": datetime.now().strftime("%Y-%m-%d"),
        "tenant_id": TENANT_ID,
        "created_by": BAARLI_CLAW_ID,
        "is_pinned": False,
        "order_index": 999
    }
    
    # Send til Supabase
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
        print(f"✅ Radiotall insertet til Supabase!")
        return True
    except Exception as e:
        print(f"❌ Feil ved insert: {e}")
        return False

def save_locally(data):
    """Lagre data lokalt"""
    import os
    
    output_dir = "/tmp/radio_stats"
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{output_dir}/nielsen_radio_{datetime.now().strftime('%Y-%m-%d')}.json"
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Lagret lokalt: {filename}")
    return filename

def main():
    print("📻 NIELSEN RADIO TALL - OPPDATERING")
    print("=" * 60)
    print()
    
    # Vis data
    print("📊 DATA SOM VIL BLI LAGRET:")
    print("-" * 60)
    print(f"Ukentlig rekkevidde:  ~{NIELSEN_DATA['nrj_estimated']['weekly_reach_absolute']:,} lyttere")
    print(f"Daglig rekkevidde:    ~{NIELSEN_DATA['nrj_estimated']['daily_reach_absolute']:,} lyttere")
    print(f"Markedsandel (Bauer):  {NIELSEN_DATA['market_shares']['Bauer_Media']}%")
    print(f"Estimert NRJ-andel:    {NIELSEN_DATA['nrj_estimated']['weekly_reach_percent']}%")
    print()
    
    # Lagre lokalt
    filename = save_locally(NIELSEN_DATA)
    
    # Insert til Supabase
    print()
    print("💾 LAGRER TIL SUPABASE...")
    if insert_to_supabase(NIELSEN_DATA):
        print()
        print("=" * 60)
        print("✅ RADIOTALL OPPDATERT!")
        print("=" * 60)
        print()
        print("📍 Data tilgjengelig i:")
        print(f"   - Lokal fil: {filename}")
        print(f"   - Supabase: agenda_items (category=STATS)")
        print()
        print("⚠️  VIKTIG:")
        print("   For eksakte stasjon-spesifikke tall, kreves:")
        print("   - Tilgang til Nielsen iPort")
        print("   - Brukernavn/passord fra Bauer Media")
        print("   - Kontakt: dashboard-eu-iport.nielsen-iwatch.com")
    else:
        print()
        print("⚠️  Kunne ikke lagre til Supabase, men data er lagret lokalt")

if __name__ == "__main__":
    main()
