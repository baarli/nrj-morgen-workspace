#!/usr/bin/env python3
"""
Insert saker fra morning-news.json til Supabase
Bruker eksisterende JSON fra brave-news-search.py
"""

import json
import urllib.request
import urllib.parse
import os
import re
from datetime import datetime, timedelta

# === KONFIGURASJON ===
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"
TENANT_ID = "a0000000-0000-0000-0000-000000000001"
CREATED_BY = "10aa1508-6d52-490c-8ae5-fa3da9a152c4"
PROFILE_PICTURE = "https://lh3.googleusercontent.com/a/ACg8ocLyiG1iwB_rfOCAN64WGPUUIWprTMX0JfUDsoy7dHkd6AVdaQ=s96-c"

TOMORROW = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

def supabase_request(method, path, data=None, params=None):
    """Gjør en Supabase-forespørsel"""
    url = f"{SUPABASE_URL}/rest/v1{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
    }
    
    if method == 'GET':
        req = urllib.request.Request(url, headers=headers)
    elif method == 'DELETE':
        req = urllib.request.Request(url, headers=headers, method='DELETE')
    else:  # POST, PATCH
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8') if data else None,
            headers=headers,
            method=method
        )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            if method == 'GET':
                return json.loads(response.read().decode('utf-8'))
            return True
    except urllib.error.HTTPError as e:
        print(f"   ⚠️  HTTP {e.code}: {e.reason}")
        if method == 'GET':
            return []
        return False
    except Exception as e:
        print(f"   ⚠️  Feil: {e}")
        if method == 'GET':
            return []
        return False

def fetch_image_from_url(url):
    """Prøv å hente bilde fra artikkelens meta tags"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            # Sjekk etter Open Graph image
            og_match = re.search(r'<meta[^>]*property="og:image"[^>]*content="([^"]+)"', html, re.IGNORECASE)
            if og_match:
                return og_match.group(1)
            
            # Sjekk etter Twitter image
            tw_match = re.search(r'<meta[^>]*name="twitter:image"[^>]*content="([^"]+)"', html, re.IGNORECASE)
            if tw_match:
                return tw_match.group(1)
            
            # Sjekk etter meta image
            img_match = re.search(r'<meta[^>]*name="image"[^>]*content="([^"]+)"', html, re.IGNORECASE)
            if img_match:
                return img_match.group(1)
                
    except Exception as e:
        pass
    
    return None

def get_fallback_image(source):
    """Fallback-bilder for kjente kilder"""
    source_lower = source.lower()
    if 'nettavisen' in source_lower:
        return "https://www.nettavisen.no/logo.png"
    elif 'dagbladet' in source_lower:
        return "https://www.dagbladet.no/logo.png"
    elif 'seher' in source_lower or 'se og hør' in source_lower:
        return "https://www.seher.no/logo.png"
    elif 'nrk' in source_lower:
        return "https://www.nrk.no/logo.png"
    elif 'vg' in source_lower:
        return "https://www.vg.no/logo.png"
    elif 'tv2' in source_lower:
        return "https://www.tv2.no/logo.png"
    elif 'aftenposten' in source_lower:
        return "https://www.aftenposten.no/logo.png"
    return None

def create_notes(article):
    """Lag notes-feltet på riktig format"""
    description = article.get('description', '')
    why_nrj = article.get('why_nrj', 'aktuell og underholdende')
    source = article.get('source', 'Ukjent kilde')
    
    # Første setning fra beskrivelsen
    first_sentence = description.split('.')[0] if description else ''
    
    notes = f"""{first_sentence}

Hvorfor NRJ: {why_nrj}
Kilde: {source}"""
    
    return notes

def create_description_with_image(article, image_url):
    """Lag description med HTML img tag"""
    desc = article.get('description', '')
    
    if image_url:
        img_html = f'<img src="{image_url}" alt="{article.get("title", "")}" style="max-width:100%;border-radius:8px;margin-bottom:12px;" />\n\n'
        return img_html + desc
    
    return desc

def main():
    print("🚀 NRJ MORGEN - INSERT TIL SUPABASE")
    print("=" * 60)
    print(f"Dato: {TOMORROW}")
    print("=" * 60)
    
    # Last artikler
    try:
        with open('/tmp/morning-news.json', 'r') as f:
            data = json.load(f)
            articles = data.get('articles', [])
    except Exception as e:
        print(f"❌ Kunne ikke lese /tmp/morning-news.json: {e}")
        return 1
    
    print(f"\n📊 Fant {len(articles)} artikler i JSON-filen")
    
    # === STEG 1: SLETT GAMLE SAKER ===
    print("\n" + "=" * 60)
    print("STEG 1: Sletter gamle saker...")
    print("=" * 60)
    
    # Slett saker for morgendagens dato
    delete_result = supabase_request(
        'DELETE',
        f'/agenda_items',
        params={'tenant_id': f'eq.{TENANT_ID}', 'show_date': f'eq.{TOMORROW}'}
    )
    
    if delete_result:
        print("   ✅ Gamle saker slettet")
    else:
        print("   ⚠️  Kunne ikke slette gamle saker (fortsetter...)")
    
    # === STEG 2: INSERT NYE SAKER ===
    print("\n" + "=" * 60)
    print("STEG 2: Inserter nye saker...")
    print("=" * 60)
    
    inserted = 0
    failed = 0
    
    for i, article in enumerate(articles, 1):
        title = article.get('title', '')
        url = article.get('url', '')
        
        if not title or not url:
            print(f"   ⚠️  Sak {i}: Mangler tittel eller URL - hopper over")
            failed += 1
            continue
        
        print(f"\n   {i}. {title[:50]}...")
        
        # Hent bilde
        print(f"      🖼️  Henter bilde...")
        image_url = fetch_image_from_url(url)
        if not image_url:
            image_url = get_fallback_image(article.get('source', ''))
        
        if image_url:
            print(f"      ✅ Bilde funnet: {image_url[:60]}...")
        else:
            print(f"      ⚠️  Ingen bilde funnet")
        
        # Lag payload
        notes = create_notes(article)
        description = create_description_with_image(article, image_url)
        
        link_metadata = {}
        if image_url:
            link_metadata['image_url'] = image_url
        
        payload = {
            'tenant_id': TENANT_ID,
            'title': title,
            'description': description,
            'notes': notes,
            'link_url': url,
            'show_date': TOMORROW,
            'category': 'TALK',
            'created_by': CREATED_BY,
            'is_pinned': False,
            'is_completed': False
        }
        
        if link_metadata:
            payload['link_metadata'] = link_metadata
        
        # Insert
        result = supabase_request('POST', '/agenda_items', payload)
        
        if result:
            print(f"      ✅ Insertet")
            inserted += 1
        else:
            print(f"      ❌ Feil ved insert")
            failed += 1
    
    # === STEG 3: VERIFISER ===
    print("\n" + "=" * 60)
    print("STEG 3: Verifiserer...")
    print("=" * 60)
    
    verify = supabase_request(
        'GET',
        '/agenda_items',
        params={
            'tenant_id': f'eq.{TENANT_ID}',
            'show_date': f'eq.{TOMORROW}',
            'select': 'id,title,link_url'
        }
    )
    
    print(f"   📊 {len(verify)} saker i Supabase for {TOMORROW}")
    
    if len(verify) >= 10:
        print(f"\n   ✅ SUCCESS! {len(verify)} saker klare for NRJ Morgen")
        for item in verify[:5]:
            print(f"      • {item.get('title', 'Ukjent')[:40]}...")
    else:
        print(f"\n   ⚠️  Kun {len(verify)} saker - målet var 15")
    
    # === OPPSUMMERING ===
    print("\n" + "=" * 60)
    print("OPPSUMMERING")
    print("=" * 60)
    print(f"   📥 Forsøkt insert: {len(articles)}")
    print(f"   ✅ Vellykket: {inserted}")
    print(f"   ❌ Feilet: {failed}")
    print(f"   📊 I Supabase: {len(verify)}")
    print(f"   📅 Dato: {TOMORROW}")
    
    return 0

if __name__ == '__main__':
    exit(main())
