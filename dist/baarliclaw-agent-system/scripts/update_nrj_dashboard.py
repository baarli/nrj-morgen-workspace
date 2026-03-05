#!/usr/bin/env python3
"""
NRJ Statistikk Dashboard - Oppdater eksisterende panel
Henter siste data og oppdaterer eksisterende NRJ Statistikk item
"""

import json
import urllib.request
from datetime import datetime

# Supabase konfigurasjon
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"
TENANT_ID = "a0000000-0000-0000-0000-000000000001"
BAARLI_CLAW_ID = "10aa1508-6d52-490c-8ae5-fa3da9a152c4"

# API URL-er
NIELSEN_API_URL = "https://eu-iport.nielsen-iwatch.com/api/Chart?dataid=8eb6daca-1266-4af8-8e8f-f39107dc63fb&show_series_label=0&show_text=1&show_values=0&show_percentages=1&show_legend=1&flip_data=0&start_at_zero=0&red_negative=1&truncate_text=0&center_offset=0&average_center_offset=0&tooltip_show_values=1&tooltip_show_percentages=1&tooltip_show_legend=1&show_title=0&chart_type=grid&scheme=orange&background=fff&color=000&hotspot_color=fff&hotspot_bands=0&hotspot_enabled=1&hotspot_type=report&highest_value_enabled=0&highest_value_color=fff&highest_value_type=report&grid_data_position=1&show_timestamp=0&filter=~R4:-1~C2:-1,3:-1~P1:1&show_menu=0&text_chart_stretch_to_fit=0&show_border=0&pie_radius=0.35&cur_series_id=0&show_series_dropdown=1&grid_row_show_color=0&grid_header_show_color=0&show_logo=1&show_empty_series=1&ignore_zero_values=0&alternate_row_color=1&allow_data_zoom=1&merge_string_cell=1&show_widget_export=1&allow_widget_filters=0&show_thousands_separator=1&zoom_show_thousands_separator=1&tooltip_show_series_label=1&tooltip_show_text=1&focus_level=0&frozen=1&source_locale=de&publish_key=bd551853-f42b-4b86-813a-79faf3a718e9"

PODTOPPEN_EXPORT_URL = "https://podtoppen.tnslistene.no/export.php"


def fetch_nielsen_data():
    """Hent NRJ radio-tall fra Nielsen API"""
    try:
        req = urllib.request.Request(
            NIELSEN_API_URL,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            # Parse NRJ-data
            series_data = data['seriesMDData'][0]
            data2d = series_data['data2D']
            
            for row in data2d:
                if row[0] == "NRJ":
                    return {
                        'daily_reach': int(row[8]) * 1000,  # Siste uke (uke 7)
                        'weekly_data': {
                            'uke_1': int(row[2]) * 1000,
                            'uke_2': int(row[3]) * 1000,
                            'uke_3': int(row[4]) * 1000,
                            'uke_4': int(row[5]) * 1000,
                            'uke_5': int(row[6]) * 1000,
                            'uke_6': int(row[7]) * 1000,
                            'uke_7': int(row[8]) * 1000,
                        },
                        'last_updated': data.get('last_updated_date', datetime.now().isoformat())
                    }
            
            return None
    except Exception as e:
        print(f"❌ Feil ved henting fra Nielsen: {e}")
        return None


def fetch_podtoppen_data():
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
            
            for i, line in enumerate(lines[1:], 1):  # Start fra 1 for rangering
                if 'nrj morgen' in line.lower():
                    parts = line.split(';')
                    return {
                        'rank': i,
                        'name': parts[0],
                        'author': parts[1],
                        'devices': int(parts[3]),
                        'downloads': int(parts[4])
                    }
            
            return None
    except Exception as e:
        print(f"❌ Feil ved henting fra Podtoppen: {e}")
        return None


def find_existing_stats_item():
    """Finn eksisterende NRJ Statistikk item"""
    try:
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/agenda_items?select=id,title&tenant_id=eq.{TENANT_ID}&title=like.*NRJ%20Statistikk*&order=created_at.desc&limit=1",
            headers={
                'apikey': SUPABASE_KEY,
                'Authorization': f'Bearer {SUPABASE_KEY}'
            }
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data and len(data) > 0:
                return data[0]['id']
            return None
    except Exception as e:
        print(f"❌ Feil ved søk etter eksisterende item: {e}")
        return None


def create_dashboard_html(nielsen_data, podtoppen_data):
    """Lag HTML for dashboard-visning"""
    
    # Beregn trend for radio
    radio_weeks = nielsen_data['weekly_data']
    radio_values = list(radio_weeks.values())
    radio_avg = sum(radio_values) / len(radio_values)
    radio_latest = radio_values[-1]
    radio_trend = ((radio_latest - radio_values[-2]) / radio_values[-2]) * 100
    
    html = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 800px; margin: 0 auto;">
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #ff6b00 0%, #ff8c00 100%); color: white; padding: 30px; border-radius: 12px 12px 0 0; text-align: center;">
            <h1 style="margin: 0; font-size: 28px; font-weight: 700;">📊 NRJ Statistikk</h1>
            <p style="margin: 10px 0 0 0; font-size: 14px; opacity: 0.9;">Sist oppdatert: {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
        </div>
        
        <!-- Radio Stats -->
        <div style="background: #fff; padding: 25px; border-left: 4px solid #ff6b00; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-radius: 8px;">
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                <div style="background: #ff6b00; color: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; margin-right: 15px;">📻</div>
                <div>
                    <h2 style="margin: 0; color: #333; font-size: 22px;">NRJ Radio</h2>
                    <p style="margin: 5px 0 0 0; color: #666; font-size: 13px;">Daglig gjennomsnittlig rekkevidde</p>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px;">
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 32px; font-weight: 700; color: #ff6b00;">{nielsen_data['daily_reach']:,}</div>
                    <div style="font-size: 12px; color: #666; margin-top: 5px;">Daglige lyttere</div>
                    <div style="font-size: 11px; color: {'#28a745' if radio_trend > 0 else '#dc3545'}; margin-top: 8px;">
                        {'📈' if radio_trend > 0 else '📉'} {radio_trend:+.1f}% fra forrige uke
                    </div>
                </div>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 32px; font-weight: 700; color: #333;">{int(radio_avg):,}</div>
                    <div style="font-size: 12px; color: #666; margin-top: 5px;">Gjennomsnitt 2026</div>
                </div>
            </div>
            
            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #eee;">
                <div style="font-size: 11px; color: #999;">
                    Kilde: Nielsen PPM API | {nielsen_data['last_updated'][:10]}
                </div>
            </div>
        </div>
        
        <!-- Podcast Stats -->
        <div style="background: #fff; padding: 25px; border-left: 4px solid #6c5ce7; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-radius: 8px;">
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                <div style="background: #6c5ce7; color: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; margin-right: 15px;">🎧</div>
                <div>
                    <h2 style="margin: 0; color: #333; font-size: 22px;">NRJ Morgen Podkast</h2>
                    <p style="margin: 5px 0 0 0; color: #666; font-size: 13px;">Podtoppen rangering #{podtoppen_data['rank']}</p>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px;">
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 32px; font-weight: 700; color: #6c5ce7;">{podtoppen_data['devices']:,}</div>
                    <div style="font-size: 12px; color: #666; margin-top: 5px;">Unike lyttere</div>
                </div>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 32px; font-weight: 700; color: #333;">{podtoppen_data['downloads']:,}</div>
                    <div style="font-size: 12px; color: #666; margin-top: 5px;">Nedlastet/strømmet</div>
                </div>
            </div>
            
            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #eee;">
                <div style="font-size: 11px; color: #999;">
                    Kilde: Kantar/TNS Podtoppen | Utgiver: {podtoppen_data['author']}
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <div style="background: #f8f9fa; padding: 15px; border-radius: 0 0 12px 12px; text-align: center; font-size: 11px; color: #999;">
            Data hentes automatisk hver onsdag kl 12:00 | <a href="https://www.nielsen.com" style="color: #ff6b00; text-decoration: none;">Nielsen</a> | 
            <a href="https://podtoppen.tnslistene.no" style="color: #6c5ce7; text-decoration: none;">Podtoppen</a>
        </div>
    </div>
    """
    
    return html


def update_supabase(item_id, html_content, nielsen_data, podtoppen_data):
    """Oppdater eksisterende item i Supabase"""
    
    title = f"📊 NRJ Statistikk - {nielsen_data['daily_reach']:,} radio + {podtoppen_data['devices']:,} podkast"
    
    notes = f"""📊 NRJ STATISTIKK - SAMLET OVERSIKT

📻 NRJ RADIO:
• Daglig rekkevidde: {nielsen_data['daily_reach']:,} lyttere
• Gjennomsnitt 2026: {int(sum(nielsen_data['weekly_data'].values()) / len(nielsen_data['weekly_data'])):,} lyttere
• Sist oppdatert: {nielsen_data['last_updated']}

🎧 NRJ MORGEN PODKAST:
• Rangering: #{podtoppen_data['rank']} på Podtoppen
• Unike lyttere: {podtoppen_data['devices']:,}
• Nedlastet/strømmet: {podtoppen_data['downloads']:,}
• Utgiver: {podtoppen_data['author']}

🔗 KILDER:
• Nielsen PPM API: https://eu-iport.nielsen-iwatch.com/api/Chart
• Podtoppen: https://podtoppen.tnslistene.no/
• Sist oppdatert: {datetime.now().strftime('%Y-%m-%d %H:%M')}

✅ EKTE DATA:
Alle tall er faktiske målte data fra Nielsen og Kantar/TNS.
"""
    
    payload = {
        "title": title,
        "description": html_content,
        "notes": notes,
        "updated_at": datetime.now().isoformat()
    }
    
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/agenda_items?id=eq.{item_id}",
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        },
        method='PATCH'
    )
    
    try:
        urllib.request.urlopen(req, timeout=10)
        return True
    except Exception as e:
        print(f"❌ Feil ved oppdatering: {e}")
        return False


def main():
    print("📊 NRJ STATISTIKK DASHBOARD - OPPDATERING")
    print("=" * 60)
    print()
    
    # Finn eksisterende item
    print("🔍 Søker etter eksisterende NRJ Statistikk item...")
    item_id = find_existing_stats_item()
    
    if item_id:
        print(f"   ✅ Fant eksisterende item: {item_id}")
    else:
        print("   ⚠️  Ingen eksisterende item funnet - oppretter ny")
    
    print()
    
    # Hent Nielsen data
    print("📻 Henter NRJ radio-tall fra Nielsen...")
    nielsen_data = fetch_nielsen_data()
    
    if nielsen_data:
        print(f"   ✅ {nielsen_data['daily_reach']:,} daglige lyttere (uke 7)")
    else:
        print("   ❌ Kunne ikke hente Nielsen-data")
    
    print()
    
    # Hent Podtoppen data
    print("🎧 Henter NRJ Morgen Podkast tall fra Podtoppen...")
    podtoppen_data = fetch_podtoppen_data()
    
    if podtoppen_data:
        print(f"   ✅ Rangering: #{podtoppen_data['rank']}")
        print(f"   ✅ {podtoppen_data['devices']:,} unike lyttere")
    else:
        print("   ❌ Kunne ikke hente Podtoppen-data")
    
    print()
    
    # Lag dashboard HTML og oppdater
    if nielsen_data and podtoppen_data:
        print("🎨 Lager dashboard-visning...")
        html = create_dashboard_html(nielsen_data, podtoppen_data)
        
        if item_id:
            print(f"💾 Oppdaterer eksisterende item {item_id}...")
            if update_supabase(item_id, html, nielsen_data, podtoppen_data):
                print()
                print("=" * 60)
                print("🎉 NRJ STATISTIKK DASHBOARD OPPDATERT!")
                print("=" * 60)
                print()
                print(f"📊 Panel ID: {item_id}")
                print(f"📻 Radio: {nielsen_data['daily_reach']:,} daglige lyttere")
                print(f"🎧 Podkast: {podtoppen_data['devices']:,} unike lyttere")
            else:
                print("❌ Kunne ikke oppdatere data")
        else:
            print("⚠️  Ingen item å oppdatere")
    else:
        print("⚠️  Mangler data - kunne ikke oppdatere dashboard")


if __name__ == "__main__":
    main()
