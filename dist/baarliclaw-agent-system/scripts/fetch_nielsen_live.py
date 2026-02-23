#!/usr/bin/env python3
"""
Nielsen Radio Data - Hent EKTE data fra Nielsen PPM API
Bruker publisert chart URL for å hente faktiske lyttertall
"""

import json
import urllib.request
from datetime import datetime

# Nielsen Chart API URL (publisert)
NIELSEN_API_URL = "https://eu-iport.nielsen-iwatch.com/api/Chart?dataid=8eb6daca-1266-4af8-8e8f-f39107dc63fb&show_series_label=0&show_text=1&show_values=0&show_percentages=1&show_legend=1&flip_data=0&start_at_zero=0&red_negative=1&truncate_text=0&center_offset=0&average_center_offset=0&tooltip_show_values=1&tooltip_show_percentages=1&tooltip_show_legend=1&show_title=0&chart_type=grid&scheme=orange&background=fff&color=000&hotspot_color=fff&hotspot_bands=0&hotspot_enabled=1&hotspot_type=report&highest_value_enabled=0&highest_value_color=fff&highest_value_type=report&grid_data_position=1&show_timestamp=0&filter=~R4:-1~C2:-1,3:-1~P1:1&show_menu=0&text_chart_stretch_to_fit=0&show_border=0&pie_radius=0.35&cur_series_id=0&show_series_dropdown=1&grid_row_show_color=0&grid_header_show_color=0&show_logo=1&show_empty_series=1&ignore_zero_values=0&alternate_row_color=1&allow_data_zoom=1&merge_string_cell=1&show_widget_export=1&allow_widget_filters=0&show_thousands_separator=1&zoom_show_thousands_separator=1&tooltip_show_series_label=1&tooltip_show_text=1&focus_level=0&frozen=1&source_locale=de&publish_key=bd551853-f42b-4b86-813a-79faf3a718e9"

# Supabase konfigurasjon
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"
TENANT_ID = "a0000000-0000-0000-0000-000000000001"
BAARLI_CLAW_ID = "10aa1508-6d52-490c-8ae5-fa3da9a152c4"


def fetch_nielsen_data():
    """Hent data fra Nielsen API"""
    try:
        req = urllib.request.Request(
            NIELSEN_API_URL,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except Exception as e:
        print(f"❌ Feil ved henting fra Nielsen: {e}")
        return None


def parse_nrj_data(data):
    """Parse NRJ-data fra Nielsen respons"""
    
    if not data or 'seriesMDData' not in data:
        print("❌ Ugyldig dataformat")
        return None
    
    try:
        # Finn data2D array
        series_data = data['seriesMDData'][0]
        data2d = series_data['data2D']
        
        # Finn NRJ-raden
        nrj_row = None
        for row in data2d:
            if row[0] == "NRJ":
                nrj_row = row
                break
        
        if not nrj_row:
            print("❌ NRJ ikke funnet i data")
            return None
        
        # Parse data
        # Format: ["NRJ","53","46","64","62","56","52","63","69"]
        weekly_data = {
            "2025_uke_52": int(nrj_row[1]) * 1000,
            "2026_uke_1": int(nrj_row[2]) * 1000,
            "2026_uke_2": int(nrj_row[3]) * 1000,
            "2026_uke_3": int(nrj_row[4]) * 1000,
            "2026_uke_4": int(nrj_row[5]) * 1000,
            "2026_uke_5": int(nrj_row[6]) * 1000,
            "2026_uke_6": int(nrj_row[7]) * 1000,
            "2026_uke_7": int(nrj_row[8]) * 1000
        }
        
        # Beregn gjennomsnitt for 2026
        values_2026 = [weekly_data[f"2026_uke_{i}"] for i in range(1, 8)]
        avg_2026 = sum(values_2026) / len(values_2026)
        
        return {
            "station": "NRJ",
            "source": "Nielsen PPM API",
            "source_url": "https://eu-iport.nielsen-iwatch.com/api/Chart",
            "last_updated": data.get('last_updated_date', datetime.now().isoformat()),
            "data_type": "Daily Av. Rch (000s)",
            "weekly_data": weekly_data,
            "latest_week": "2026_uke_7",
            "latest_daily_reach": weekly_data["2026_uke_7"],
            "average_daily_reach_2026": int(avg_2026),
            "average_daily_reach_all": int(sum(weekly_data.values()) / len(weekly_data))
        }
        
    except Exception as e:
        print(f"❌ Feil ved parsing: {e}")
        return None


def insert_to_supabase(nrj_data):
    """Insert data til Supabase"""
    
    title = f"📻 Nielsen Radio Tall - NRJ {nrj_data['latest_daily_reach']:,} daglige lyttere"
    
    description = f"""
    Daglig gjennomsnittlig rekkevidde: {nrj_data['latest_daily_reach']:,} lyttere (uke 7, 2026)
    Gjennomsnitt 2026: {nrj_data['average_daily_reach_2026']:,} lyttere
    Kilde: Nielsen PPM API (ekte data)
    Sist oppdatert: {nrj_data['last_updated']}
    """
    
    notes = f"""📊 NIELSEN RADIO DATA - EKTE DATA FRA API

🎧 NRJ DAGLIG REKKEVIDDE (tusenvis):
• 2025 uke 52: {nrj_data['weekly_data']['2025_uke_52']:,} lyttere
• 2026 uke 1:  {nrj_data['weekly_data']['2026_uke_1']:,} lyttere
• 2026 uke 2:  {nrj_data['weekly_data']['2026_uke_2']:,} lyttere
• 2026 uke 3:  {nrj_data['weekly_data']['2026_uke_3']:,} lyttere
• 2026 uke 4:  {nrj_data['weekly_data']['2026_uke_4']:,} lyttere
• 2026 uke 5:  {nrj_data['weekly_data']['2026_uke_5']:,} lyttere
• 2026 uke 6:  {nrj_data['weekly_data']['2026_uke_6']:,} lyttere
• 2026 uke 7:  {nrj_data['weekly_data']['2026_uke_7']:,} lyttere

📈 STATISTIKK:
• Gjennomsnitt 2026: {nrj_data['average_daily_reach_2026']:,} lyttere
• Siste uke: {nrj_data['latest_daily_reach']:,} lyttere
• Endring fra uke 6: +{nrj_data['latest_daily_reach'] - nrj_data['weekly_data']['2026_uke_6']:,} lyttere

🔗 KILDE:
• Nielsen PPM API
• URL: {nrj_data['source_url']}
• Sist oppdatert: {nrj_data['last_updated']}
• Data type: {nrj_data['data_type']}

✅ EKTE DATA:
Dette er faktiske målte data fra Nielsen PPM, ikke estimater!
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
        return True
    except Exception as e:
        print(f"❌ Feil ved insert: {e}")
        return False


def main():
    print("📻 NIELSEN RADIO DATA - EKTE DATA FRA API")
    print("=" * 60)
    print()
    
    # Hent data
    print("🌐 Henter data fra Nielsen API...")
    data = fetch_nielsen_data()
    
    if not data:
        print("❌ Kunne ikke hente data")
        return
    
    print("✅ Data mottatt!")
    print()
    
    # Parse NRJ-data
    print("📊 Parser NRJ-data...")
    nrj_data = parse_nrj_data(data)
    
    if not nrj_data:
        print("❌ Kunne ikke parse data")
        return
    
    print("✅ Data parset!")
    print()
    
    # Vis data
    print("📈 NRJ DAGLIG REKKEVIDDE:")
    print("-" * 60)
    for week, value in nrj_data["weekly_data"].items():
        print(f"   {week}: {value:,} lyttere")
    print()
    print(f"📊 Gjennomsnitt 2026: {nrj_data['average_daily_reach_2026']:,} lyttere")
    print(f"📊 Siste uke: {nrj_data['latest_daily_reach']:,} lyttere")
    print()
    
    # Lagre til Supabase
    print("💾 Lagrer til Supabase...")
    if insert_to_supabase(nrj_data):
        print("✅ Data lagret!")
        print()
        print("=" * 60)
        print("🎉 EKTE NIELSEN DATA OPPDATERT!")
        print("=" * 60)
        print()
        print(f"📊 NRJ: {nrj_data['latest_daily_reach']:,} daglige lyttere")
        print(f"📈 Gjennomsnitt: {nrj_data['average_daily_reach_2026']:,} lyttere")
    else:
        print("❌ Kunne ikke lagre data")


if __name__ == "__main__":
    main()
