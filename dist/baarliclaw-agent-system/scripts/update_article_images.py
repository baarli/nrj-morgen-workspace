#!/usr/bin/env python3
"""
Hent bilder fra artikler og last opp til Supabase Storage
"""
import json
import urllib.request
import urllib.parse
import re

SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"
TENANT_ID = "a0000000-0000-0000-0000-000000000001"

def get_image_from_article(url):
    """Hent bilde-URL fra artikkelens meta tags"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            # Se etter meta image tags
            patterns = [
                r'<meta[^>]*property="og:image"[^>]*content="([^"]+)"',
                r'<meta[^>]*name="twitter:image[^"]*"[^>]*content="([^"]+)"',
                r'<meta[^>]*content="([^"]+)"[^>]*property="og:image"',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, html, re.IGNORECASE)
                if match:
                    image_url = match.group(1)
                    # Fiks relative URL-er
                    if image_url.startswith('/'):
                        from urllib.parse import urlparse
                        parsed = urlparse(url)
                        image_url = f"{parsed.scheme}://{parsed.netloc}{image_url}"
                    return image_url
    except Exception as e:
        print(f"   Feil ved henting av bilde: {e}")
    
    return None

def update_agenda_item(item_id, image_url, created_by):
    """Oppdater agenda item med bilde og created_by"""
    try:
        # Bygg link_metadata med bilde
        link_metadata = json.dumps({"image_url": image_url}) if image_url else None
        
        payload = {
            "created_by": created_by,
            "link_metadata": link_metadata
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
        f"{SUPABASE_URL}/rest/v1/agenda_items?select=id,title,link_url&tenant_id=eq.{TENANT_ID}",
        headers={'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}'}
    )
    
    with urllib.request.urlopen(req, timeout=10) as response:
        items = json.loads(response.read().decode())
    
    print(f"📊 Fant {len(items)} saker å oppdatere")
    print("")
    
    # Bruker ID for profilbilde
    created_by = "10aa1508-6d52-490c-8ae5-fa3da9a152c4"  # BaarliClaw
    
    updated = 0
    for item in items:
        item_id = item['id']
        title = item['title']
        url = item['link_url']
        
        print(f"🔍 {title[:50]}...")
        
        # Hent bilde
        image_url = get_image_from_article(url)
        
        if image_url:
            print(f"   🖼️  Bilde funnet: {image_url[:60]}...")
        else:
            print(f"   ⚠️  Ingen bilde funnet")
            # Bruk placeholder basert på kilde
            if 'tv2.no' in url:
                image_url = "https://www.cdn.tv2.no/images/logo.png"
            elif 'dagbladet.no' in url:
                image_url = "https://www.dagbladet.no/logo.png"
            elif 'seher.no' in url:
                image_url = "https://www.seher.no/logo.png"
            elif 'nettavisen.no' in url:
                image_url = "https://www.nettavisen.no/logo.png"
            elif 'nrk.no' in url:
                image_url = "https://www.nrk.no/logo.png"
            else:
                image_url = "https://via.placeholder.com/600x315?text=NRJ+Morgen"
            print(f"   🖼️  Bruker placeholder: {image_url}")
        
        # Oppdater sak
        if update_agenda_item(item_id, image_url, created_by):
            updated += 1
            print(f"   ✅ Oppdatert")
        else:
            print(f"   ❌ Feil")
        
        print("")
    
    print(f"📊 {updated} av {len(items)} saker oppdatert med bilde")

if __name__ == '__main__':
    main()
