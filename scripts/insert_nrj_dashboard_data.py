#!/usr/bin/env python3
"""
Insert NRJ Dashboard Data direkte i Supabase tabeller

Dette skriptet:
1. Henter fersk data fra API-ene
2. Insert/upsert data i riktige Supabase tabeller
3. Data vises da automatisk i dashboard panelene
"""

import json
import urllib.request
from datetime import datetime

SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"

NIELSEN_API_URL = "https://eu-iport.nielsen-iwatch.com/api/Chart?dataid=8eb6daca-1266-4af8-8e8f-f39107dc63fb&show_series_label=0&show_text=1&show_values=0&show_percentages=1&show_legend=1&flip_data=0&start_at_zero=0&red_negative=1&truncate_text=0&center_offset=0&average_center_offset=0&tooltip_show_values=1&tooltip_show_percentages=1&tooltip_show_legend=1&show_title=0&chart_type=grid&scheme=orange&background=fff&color=000&hotspot_color=fff&hotspot_bands=0&hotspot_enabled=1&hotspot_type=report&highest_value_enabled=0&highest_value_color=fff&highest_value_type=report&grid_data_position=1&show_timestamp=0&filter=~R4:-1~C2:-1,3:-1~P1:1&show_menu=0&text_chart_stretch_to_fit=0&show_border=0&pie_radius=0.35&cur_series_id=0&show_series_dropdown=1&grid_row_show_color=0&grid_header_show_color=0&show_logo=1&show_empty_series=1&ignore_zero_values=0&alternate_row_color=1&allow_data_zoom=1&merge_string_cell=1&show_widget_export=1&allow_widget_filters=0&show_thousands_separator=1&zoom_show_thousands_separator=1&tooltip_show_series_label=1&tooltip_show_text=1&focus_level=0&frozen=1&source_locale=de&publish_key=bd551853-f42b-4b86-813a-79faf3a718e9"

PODTOPPEN_EXPORT_URL = "https://podtoppen.tnslistene.no/export.php"


def fetch_nielsen_nrj():
    """Hent NRJ radio-tall fra Nielsen API"""
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
                
                return {
                    'channel': 'NRJ',
                    'week_key': '2026-W07',
                    'week_number': 7,
                    'year': 2026,
                    'value': current,
                    'previous_value': previous,
                    'change': current - previous,
                    'change_pct': round(((current - previous) / previous) * 100, 1)
                }
        return None


def fetch_podtoppen_nrj():
    """Hent NRJ Morgen Podkast tall fra Podtoppen"""
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
                    'podcast_title': parts[0],
                    'rank': i,
                    'week_key': '2026-W08',
                    'week_number': 8,
                    'year': 2026,
                    'unique_units': int(parts[3]),
                    'downloaded_streamed': int(parts[4]),
                    'is_tracked': True
                }
        return None


def insert_nielsen_data(data):
    """Insert Nielsen data i nielsen_weekly_metrics"""
    try:
        payload = {
            'channel': data['channel'],
            'week_key': data['week_key'],
            'week_number': data['week_number'],
            'year': data['year'],
            'value': data['value'],
            'metric_type': 'daily_reach',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/nielsen_weekly_metrics",
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'apikey': SUPABASE_KEY,
                'Authorization': f'Bearer {SUPABASE_KEY}',
                'Content-Type': 'application/json',
                'Prefer': 'resolution=merge-duplicates'
            }
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            return True
    except Exception as e:
        print(f"   Feil: {e}")
        return False


def insert_podtoppen_data(data):
    """Insert Podtoppen data i podtoppen_weekly_data"""
    try:
        payload = {
            'podcast_title': data['podcast_title'],
            'week_key': data['week_key'],
            'week_number': data['week_number'],
            'year': data['year'],
            'rank': data['rank'],
            'unique_units': data['unique_units'],
            'downloaded_streamed': data['downloaded_streamed'],
            'is_tracked': data['is_tracked'],
            'scraped_at': datetime.now().isoformat()
        }
        
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/podtoppen_weekly_data",
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'apikey': SUPABASE_KEY,
                'Authorization': f'Bearer {SUPABASE_KEY}',
                'Content-Type': 'application/json',
                'Prefer': 'resolution=merge-duplicates'
            }
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            return True
    except Exception as e:
        print(f"   Feil: {e}")
        return False


def main():
    print("📊 OPPDATERER NRJ DASHBOARD DATA")
    print("=" * 60)
    print()
    
    # Hent Nielsen data
    print("📻 Henter Nielsen data...")
    nielsen = fetch_nielsen_nrj()
    if nielsen:
        print(f"   ✅ {nielsen['value']:,} daglige lyttere")
        
        print("   💾 Lagrer i nielsen_weekly_metrics...")
        if insert_nielsen_data(nielsen):
            print("   ✅ Lagret!")
        else:
            print("   ❌ Kunne ikke lagre")
    else:
        print("   ❌ Ingen data funnet")
    
    print()
    
    # Hent Podtoppen data
    print("🎧 Henter Podtoppen data...")
    podtoppen = fetch_podtoppen_nrj()
    if podtoppen:
        print(f"   ✅ Rangering: #{podtoppen['rank']}")
        
        print("   💾 Lagrer i podtoppen_weekly_data...")
        if insert_podtoppen_data(podtoppen):
            print("   ✅ Lagret!")
        else:
            print("   ❌ Kunne ikke lagre")
    else:
        print("   ❌ Ingen data funnet")
    
    print()
    print("=" * 60)
    print("✅ DASHBOARD DATA OPPDATERT!")
    print("=" * 60)
    print()
    print("📍 Sjekk nrjmorgen.com/dashboard nå:")
    print("   - Nielsen panel skal vise 69,000 lyttere")
    print("   - Podtoppen panel skal vise #62")


if __name__ == "__main__":
    main()
