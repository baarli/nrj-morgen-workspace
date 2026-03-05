#!/usr/bin/env python3
"""
Trigger NRJ Dashboard Stats Update

Dette skriptet trigger Supabase Edge Functions for å:
1. Hente Nielsen radio-tall (NRJ)
2. Hente Podtoppen podkast-tall (NRJ Morgen)

Data lagres i:
- nielsen_weekly_metrics (for Nielsen dashboard panel)
- podtoppen_weekly_data (for Podtoppen dashboard panel)

IKKE i agenda_items - dashboard panelene henter data direkte fra disse tabellene.
"""

import json
import urllib.request
from datetime import datetime

# Supabase konfigurasjon
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"


def invoke_nielsen_scrape():
    """Trigger Nielsen scrape Supabase function"""
    try:
        print("📻 Trigger Nielsen scrape...")
        
        req = urllib.request.Request(
            f"{SUPABASE_URL}/functions/v1/nielsen-scrape",
            data=json.dumps({}).encode('utf-8'),
            headers={
                'Authorization': f'Bearer {SUPABASE_KEY}',
                'Content-Type': 'application/json'
            },
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except Exception as e:
        print(f"❌ Feil ved Nielsen scrape: {e}")
        return None


def invoke_podtoppen_scrape():
    """Trigger Podtoppen scrape Supabase function"""
    try:
        print("🎧 Trigger Podtoppen scrape...")
        
        req = urllib.request.Request(
            f"{SUPABASE_URL}/functions/v1/podtoppen-scrape",
            data=json.dumps({}).encode('utf-8'),
            headers={
                'Authorization': f'Bearer {SUPABASE_KEY}',
                'Content-Type': 'application/json'
            },
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except Exception as e:
        print(f"❌ Feil ved Podtoppen scrape: {e}")
        return None


def check_nielsen_data():
    """Sjekk siste NRJ data i nielsen_weekly_metrics"""
    try:
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/nielsen_weekly_metrics?select=*&channel=eq.NRJ&order=week_key.desc&limit=1",
            headers={
                'apikey': SUPABASE_KEY,
                'Authorization': f'Bearer {SUPABASE_KEY}'
            }
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data and len(data) > 0:
                return data[0]
            return None
    except Exception as e:
        print(f"❌ Feil ved sjekk av Nielsen data: {e}")
        return None


def check_podtoppen_data():
    """Sjekk siste NRJ Morgen data i podtoppen_weekly_data"""
    try:
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/podtoppen_weekly_data?select=*&podcast_name=ilike.*NRJ%20Morgen*&order=week_key.desc&limit=1",
            headers={
                'apikey': SUPABASE_KEY,
                'Authorization': f'Bearer {SUPABASE_KEY}'
            }
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data and len(data) > 0:
                return data[0]
            return None
    except Exception as e:
        print(f"❌ Feil ved sjekk av Podtoppen data: {e}")
        return None


def main():
    print("📊 NRJ DASHBOARD STATS UPDATE")
    print("=" * 60)
    print()
    
    # Sjekk eksisterende data først
    print("🔍 Sjekker eksisterende data...")
    nielsen_before = check_nielsen_data()
    podtoppen_before = check_podtoppen_data()
    
    if nielsen_before:
        print(f"   📻 Nielsen: {nielsen_before['value']:,} lyttere (uke {nielsen_before['week_number']})")
    else:
        print("   📻 Nielsen: Ingen data funnet")
    
    if podtoppen_before:
        print(f"   🎧 Podtoppen: #{podtoppen_before['rank']} (uke {podtoppen_before['week_number']})")
    else:
        print("   🎧 Podtoppen: Ingen data funnet")
    
    print()
    
    # Trigger Nielsen scrape
    print("⏳ Kjører Nielsen scrape (dette kan ta opptil 60 sekunder)...")
    nielsen_result = invoke_nielsen_scrape()
    
    if nielsen_result:
        print(f"   ✅ Nielsen: {nielsen_result.get('message', 'Fullført')}")
        if 'metricsCount' in nielsen_result:
            print(f"      - {nielsen_result['metricsCount']} metrics lagret")
        if 'changesCount' in nielsen_result:
            print(f"      - {nielsen_result['changesCount']} endringer funnet")
    else:
        print("   ⚠️  Nielsen scrape returnerte ingen resultat")
    
    print()
    
    # Trigger Podtoppen scrape
    print("⏳ Kjører Podtoppen scrape (dette kan ta opptil 60 sekunder)...")
    podtoppen_result = invoke_podtoppen_scrape()
    
    if podtoppen_result:
        print(f"   ✅ Podtoppen: {podtoppen_result.get('message', 'Fullført')}")
        if 'podcastsFound' in podtoppen_result:
            print(f"      - {podtoppen_result['podcastsFound']} podkaster funnet")
        if 'changesCount' in podtoppen_result:
            print(f"      - {podtoppen_result['changesCount']} endringer funnet")
    else:
        print("   ⚠️  Podtoppen scrape returnerte ingen resultat")
    
    print()
    
    # Sjekk oppdatert data
    print("🔍 Sjekker oppdatert data...")
    nielsen_after = check_nielsen_data()
    podtoppen_after = check_podtoppen_data()
    
    print()
    print("=" * 60)
    print("📊 DASHBOARD STATUS")
    print("=" * 60)
    print()
    
    if nielsen_after:
        print(f"📻 NIELSEN PANEL (NRJ Radio):")
        print(f"   Daglige lyttere: {nielsen_after['value']:,}")
        print(f"   Uke: {nielsen_after['week_number']} ({nielsen_after['week_key']})")
        print(f"   Sist oppdatert: {nielsen_after['updated_at'][:10]}")
        print()
    
    if podtoppen_after:
        print(f"🎧 PODTOPPEN PANEL (NRJ Morgen Podkast):")
        print(f"   Rangering: #{podtoppen_after['rank']}")
        print(f"   Unike lyttere: {podtoppen_after['unique_listeners']:,}")
        print(f"   Uke: {podtoppen_after['week_number']} ({podtoppen_after['week_key']})")
        print(f"   Sist oppdatert: {podtoppen_after['scraped_at'][:10]}")
        print()
    
    print("=" * 60)
    print("✅ DASHBOARD PANELER OPPDATERT!")
    print("=" * 60)
    print()
    print("📍 Data vises nå i:")
    print("   - Nielsen panel (høyre side)")
    print("   - Podtoppen panel (venstre side)")
    print()
    print("📝 Merk: Data lagres IKKE i sakslista, kun i dedikerte")
    print("   dashboard-paneler som henter direkte fra:")
    print("   - nielsen_weekly_metrics")
    print("   - podtoppen_weekly_data")


if __name__ == "__main__":
    main()
