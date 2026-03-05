#!/usr/bin/env python3
"""
NRJ Statistikk Dashboard - Samlet visning for nrjmorgen.com/dashboard
Henter og viser:
- Nielsen Radio tall (NRJ)
- Podtoppen tall (NRJ Morgen Podkast)

Lagrer i agenda_items med spesiell markering for dashboard-visning
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


def fetch_nielsen_nrj_data():
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
                    weekly_data = [int(x) * 1000 for x in row[1:9]]
                    return {
                        'current_week': weekly_data[-1],
                        'previous_week': weekly_data[-2],
                        'weekly_average': int(sum(weekly_data) / len(weekly_data)),
                        'trend_percent': ((weekly_data[-1] - weekly_data[-2]) / weekly_data[-2]) * 100,
                        'last_updated': data.get('last_updated_date', datetime.now().isoformat())
                    }
            return None
    except Exception as e:
        print(f"❌ Feil ved henting fra Nielsen: {e}")
        return None


def fetch_podtoppen_nrj_data():
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
                        'publisher': parts[1],
                        'unique_listeners': int(parts[3]),
                        'downloads_streams': int(parts[4])
                    }
            return None
    except Exception as e:
        print(f"❌ Feil ved henting fra Podtoppen: {e}")
        return None


def create_dashboard_content(nielsen_data, podtoppen_data):
    """Lag JSON-struktur for dashboard"""
    
    return {
        "type": "nrj_statistics_dashboard",
        "version": "1.0",
        "last_updated": datetime.now().isoformat(),
        "radio": {
            "channel": "NRJ",
            "daily_listeners": nielsen_data['current_week'],
            "previous_week": nielsen_data['previous_week'],
            "weekly_average": nielsen_data['weekly_average'],
            "trend_percent": round(nielsen_data['trend_percent'], 1),
            "trend_direction": "up" if nielsen_data['trend_percent'] > 0 else "down",
            "source": "Nielsen PPM",
            "last_updated": nielsen_data['last_updated']
        },
        "podcast": {
            "name": podtoppen_data['name'],
            "rank": podtoppen_data['rank'],
            "unique_listeners": podtoppen_data['unique_listeners'],
            "downloads_streams": podtoppen_data['downloads_streams'],
            "publisher": podtoppen_data['publisher'],
            "source": "Podtoppen (Kantar/TNS)",
            "last_updated": datetime.now().isoformat()
        }
    }


def insert_to_supabase(dashboard_data, nielsen_data, podtoppen_data):
    """Insert til agenda_items for dashboard-visning"""
    
    # Lag tittel med nøkkeltall
    title = f"📊 NRJ Statistikk | Radio: {nielsen_data['current_week']:,} | Podkast: #{podtoppen_data['rank']}"
    
    # Lag HTML-beskrivelse for visning
    trend_icon = "📈" if nielsen_data['trend_percent'] > 0 else "📉"
    trend_color = "#28a745" if nielsen_data['trend_percent'] > 0 else "#dc3545"
    
    description = f"""
    <div class="nrj-stats-dashboard" style="font-family: system-ui, -apple-system, sans-serif; max-width: 100%;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
            <!-- Radio Stats -->
            <div style="background: linear-gradient(135deg, #ff6b00 0%, #ff8533 100%); color: white; padding: 24px; border-radius: 12px;">
                <div style="font-size: 14px; opacity: 0.9; margin-bottom: 8px;">📻 NRJ Radio</div>
                <div style="font-size: 36px; font-weight: 700; margin-bottom: 4px;">{nielsen_data['current_week']:,}</div>
                <div style="font-size: 13px; opacity: 0.9;">daglige lyttere</div>
                
                <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.3); font-size: 13px;">
                    {trend_icon} <span style="color: {trend_color};">{nielsen_data['trend_percent']:+.1f}%</span> vs forrige uke
                </div>
            </div>
            
            <!-- Podcast Stats -->
            <div style="background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%); color: white; padding: 24px; border-radius: 12px;">
                <div style="font-size: 14px; opacity: 0.9; margin-bottom: 8px;">🎧 NRJ Morgen Podkast</div>
                
                <div style="font-size: 36px; font-weight: 700; margin-bottom: 4px;">#{podtoppen_data['rank']}</div>
                <div style="font-size: 13px; opacity: 0.9;">på Podtoppen</div>
                
                <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.3); font-size: 13px;">
                    {podtoppen_data['unique_listeners']:,} unike lyttere
                </div>
            </div>
        </div>
        
        <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; font-size: 12px; color: #666;">
            Sist oppdatert: {datetime.now().strftime('%d.%m.%Y %H:%M')} | 
            Kilder: <a href="https://www.nielsen.com" style="color: #ff6b00;">Nielsen</a>, 
            <a href="https://podtoppen.tnslistene.no" style="color: #6c5ce7;">Podtoppen</a>
        </div>
    </div>
    """
    
    # Lag detaljerte notater
    notes = f"""📊 NRJ STATISTIKK DASHBOARD DATA

📻 NRJ RADIO (Nielsen PPM):
• Daglige lyttere: {nielsen_data['current_week']:,}
• Forrige uke: {nielsen_data['previous_week']:,}
• Gjennomsnitt: {nielsen_data['weekly_average']:,}
• Trend: {nielsen_data['trend_percent']:+.1f}%
• Sist oppdatert: {nielsen_data['last_updated']}

🎧 NRJ MORGEN PODKAST (Podtoppen):
• Rangering: #{podtoppen_data['rank']}
• Unike lyttere: {podtoppen_data['unique_listeners']:,}
• Nedlastet/strømmet: {podtoppen_data['downloads_streams']:,}
• Utgiver: {podtoppen_data['publisher']}

🔗 JSON DATA FOR DASHBOARD:
{json.dumps(dashboard_data, indent=2, ensure_ascii=False)}

✅ EKTE DATA:
Alle tall er faktiske målte data fra Nielsen og Kantar/TNS.
"""
    
    payload = {
        "title": title,
        "description": description,
        "notes": notes,
        "category": "TALK",
        "show_date": datetime.now().strftime("%Y-%m-%d"),
        "tenant_id": TENANT_ID,
        "created_by": BAARLI_CLAW_ID,
        "is_pinned": True,
        "order_index": 0,
        "link_metadata": json.dumps(dashboard_data)  # JSON data for eventuell API-bruk
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
    print("📊 NRJ STATISTIKK DASHBOARD")
    print("=" * 60)
    print()
    
    # Hent Nielsen data
    print("📻 Henter NRJ radio-tall fra Nielsen...")
    nielsen_data = fetch_nielsen_nrj_data()
    
    if nielsen_data:
        print(f"   ✅ {nielsen_data['current_week']:,} daglige lyttere")
    else:
        print("   ❌ Kunne ikke hente Nielsen-data")
        return
    
    print()
    
    # Hent Podtoppen data
    print("🎧 Henter NRJ Morgen Podkast tall fra Podtoppen...")
    podtoppen_data = fetch_podtoppen_nrj_data()
    
    if podtoppen_data:
        print(f"   ✅ Rangering: #{podtoppen_data['rank']}")
    else:
        print("   ❌ Kunne ikke hente Podtoppen-data")
        return
    
    print()
    
    # Lag dashboard data
    print("🎨 Lager dashboard-data...")
    dashboard_data = create_dashboard_content(nielsen_data, podtoppen_data)
    
    # Lagre til Supabase
    print("💾 Lagrer til Supabase...")
    if insert_to_supabase(dashboard_data, nielsen_data, podtoppen_data):
        print()
        print("=" * 60)
        print("🎉 NRJ STATISTIKK DASHBOARD OPPDATERT!")
        print("=" * 60)
        print()
        print("📊 Data vises nå på nrjmorgen.com/dashboard:")
        print(f"   📻 Radio: {nielsen_data['current_week']:,} daglige lyttere")
        print(f"   🎧 Podkast: #{podtoppen_data['rank']} på Podtoppen")
        print()
        print("📍 Plassering: Øverst i dashboardet")
    else:
        print("❌ Kunne ikke lagre data")


if __name__ == "__main__":
    main()
