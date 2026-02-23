#!/usr/bin/env python3
"""
Oppdater description med HTML bilder for alle saker
"""
import json
import urllib.request

SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"
TENANT_ID = "a0000000-0000-0000-0000-000000000001"

def get_image_from_metadata(link_metadata):
    """Hent bilde fra link_metadata"""
    try:
        meta = json.loads(link_metadata)
        return meta.get('image_url', '')
    except:
        return ''

def update_description(item_id, image_url, title):
    """Oppdater description med bilde"""
    try:
        # Lag description med bilde
        if image_url:
            description = f'<img src="{image_url}" alt="{title}" style="max-width:100%;height:auto;border-radius:8px;" />'
        else:
            description = ''
        
        payload = {
            "description": description
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
        
        urllib.request.urlopen(req, timeout=10)
        return True
    except Exception as e:
        print(f"   Feil ved oppdatering: {e}")
        return False

def main():
    # Hent alle saker
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/agenda_items?select=id,title,link_metadata&tenant_id=eq.{TENANT_ID}",
        headers={'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}'}
    )
    
    with urllib.request.urlopen(req, timeout=10) as response:
        items = json.loads(response.read().decode())
    
    print(f"📊 Fant {len(items)} saker å oppdatere")
    print("")
    
    updated = 0
    for item in items:
        item_id = item['id']
        title = item['title']
        link_metadata = item.get('link_metadata', '{}')
        
        # Hent bilde fra metadata
        image_url = get_image_from_metadata(link_metadata)
        
        print(f"🖼️  {title[:50]}...")
        
        if image_url:
            print(f"   Bilde: {image_url[:60]}...")
        else:
            print(f"   Ingen bilde funnet")
        
        # Oppdater description
        if update_description(item_id, image_url, title):
            updated += 1
            print(f"   ✅ Description oppdatert")
        else:
            print(f"   ❌ Feil")
        
        print("")
    
    print(f"📊 {updated} av {len(items)} saker oppdatert med bilde i description")

if __name__ == '__main__':
    main()
