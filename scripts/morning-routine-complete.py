#!/usr/bin/env python3
"""
NRJ MORGEN - FULL MORGENRUTINE MED BILDER FOR ALLE SAKER
Genererer 15 saker med AI-bilder for hver eneste sak
"""

import os
import sys
import json
import concurrent.futures
import urllib.request
import uuid
import socket
import time
from datetime import datetime

# Konfigurasjon
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"
TENANT_ID = "a0000000-0000-0000-0000-000000000001"
CREATED_BY = "10aa1508-6d52-490c-8ae5-fa3da9a152c4"
BUCKET_NAME = "media-library"

def load_credentials():
    """Last API-nøkler"""
    creds = {}
    env_files = [
        '/root/.openclaw/workspace/.credentials/live-search.env',
        '/root/.openclaw/workspace/.credentials/nrj-morgen.env'
    ]
    for env_file in env_files:
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        value = value.strip('"').strip("'")
                        creds[key] = value
    return creds

def search_brave(query, api_key, count=10, freshness='pd'):
    """Søk med Brave API"""
    if not api_key:
        return None
    
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.search.brave.com/res/v1/news/search?q={encoded_query}&count={count}&search_lang=nb&country=no&freshness={freshness}"
    
    headers = {
        'X-Subscription-Token': api_key,
        'Accept': 'application/json'
    }
    
    try:
        socket.setdefaulttimeout(15)
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            socket.setdefaulttimeout(None)
            return data
    except Exception as e:
        socket.setdefaulttimeout(None)
        return None

def create_short_title(original_title):
    """Lag kort tittel - maks 6-7 ord"""
    words = original_title.split()
    if len(words) <= 7:
        return original_title
    
    key_words = []
    skip_words = {'den', 'det', 'som', 'for', 'med', 'til', 'av', 'på', 'om', 'er', 'å', 'en', 'et', 'var', 'har'}
    
    for word in words:
        if word.lower() not in skip_words and len(key_words) < 7:
            key_words.append(word)
    
    short_title = ' '.join(key_words)
    if len(words) > 7:
        short_title = short_title.rstrip('.') + '...'
    
    return short_title

def is_hard_news(title, description):
    """Sjekk om det er hard nyhet"""
    combined = (title + ' ' + description).lower()
    hard_keywords = [
        'krig', 'terror', 'angrep', 'drap', 'voldtekt', 'tragedie', 'ulykke', 'død',
        'politi', 'pågripelse', 'fengsel', 'regjering', 'storting', 'politikk'
    ]
    return any(word in combined for word in hard_keywords)

def calculate_score(title, description):
    """Vurder underholdningsverdi"""
    score = 50
    combined = (title + ' ' + description).lower()
    
    if any(x in combined for x in ['rød løper', 'premiere', 'galla']): score += 20
    if any(x in combined for x in ['farmen', 'paradise hotel', 'spillet']): score += 15
    if any(x in combined for x in ['spellemann', 'p3 gull', 'eurovision']): score += 15
    if any(x in combined for x in ['brudd', 'skandale', 'avsløring']): score += 10
    
    return min(100, max(0, score))

def generate_all_images(articles, openai_key):
    """Generer AI-bilder for ALLE saker"""
    import base64
    from ai_images_all import generate_image_prompt
    
    print("\n🎨 GENERERER BILDER FOR ALLE SAKER...")
    print("(Tar ca. 30-40 sekunder)\n")
    
    image_urls = {}
    last_call = 0
    
    for i, article in enumerate(articles, 1):
        title = article.get('title', '')
        description = article.get('description', '')
        article_id = str(uuid.uuid4())
        
        print(f"{i:2}. {title[:40]}...", end=" ")
        
        # Rate limiting
        elapsed = time.time() - last_call
        if elapsed < 2.0:
            time.sleep(2.0 - elapsed)
        
        try:
            # Generer prompt
            prompt = generate_image_prompt(title, description)
            
            # Kall OpenAI
            payload = {
                "model": "gpt-image-1",
                "prompt": prompt[:4000],
                "size": "1024x1024",
                "n": 1
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_key}"
            }
            
            req = urllib.request.Request(
                "https://api.openai.com/v1/images/generations",
                data=json.dumps(payload).encode('utf-8'),
                headers=headers
            )
            
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode())
                image_data = base64.b64decode(data['data'][0]['b64_json'])
            
            last_call = time.time()
            
            # Lagre til Supabase
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c for c in title[:20] if c.isalnum()).replace(' ', '_')
            filename = f"nrj-news/{timestamp}_{safe_title}_{article_id[:6]}.png"
            
            upload_url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{filename}"
            upload_headers = {
                'apikey': SUPABASE_KEY,
                'Authorization': f'Bearer {SUPABASE_KEY}',
                'Content-Type': 'image/png'
            }
            
            req = urllib.request.Request(upload_url, data=image_data, headers=upload_headers, method='POST')
            with urllib.request.urlopen(req, timeout=60) as resp:
                if resp.status in [200, 201]:
                    public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{filename}"
                    image_urls[i] = public_url
                    print("✅")
                else:
                    image_urls[i] = None
                    print("❌")
                    
        except Exception as e:
            print(f"❌ ({str(e)[:30]})")
            image_urls[i] = None
    
    return image_urls

def insert_to_supabase(articles, image_urls):
    """Insert alle saker med bilder til Supabase"""
    today = datetime.now().strftime("%Y-%m-%d")
    inserted = 0
    
    print(f"\n💾 LAGRING TIL SUPABASE...\n")
    
    for i, article in enumerate(articles, 1):
        title = article.get('title', '')
        url = article.get('url', '')
        description = article.get('description', '')
        source = article.get('source', 'Ukjent')
        score = article.get('score', 50)
        
        print(f"{i:2}. {title[:45]}...", end=" ")
        
        notes = f"Score: {score}/100 | Kilde: {source}\n\n{description[:150]}"
        
        payload = {
            'id': str(uuid.uuid4()),
            'tenant_id': TENANT_ID,
            'title': title,
            'description': description,
            'notes': notes,
            'link_url': url,
            'show_date': today,
            'category': 'TALK',
            'created_by': CREATED_BY,
            'is_pinned': False,
            'is_completed': False,
            'order_index': i
        }
        
        # Legg til bilde-URL hvis vi har den
        if image_urls.get(i):
            payload['link_metadata'] = {'image_url': image_urls[i]}
        
        try:
            req = urllib.request.Request(
                f"{SUPABASE_URL}/rest/v1/agenda_items",
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    'apikey': SUPABASE_KEY,
                    'Authorization': f'Bearer {SUPABASE_KEY}',
                    'Content-Type': 'application/json'
                }
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status in [200, 201]:
                    print("✅")
                    inserted += 1
                else:
                    print(f"⚠️  {resp.status}")
        except Exception as e:
            print(f"❌ {str(e)[:30]}")
    
    return inserted

def main():
    print("=" * 70)
    print("🚀 NRJ MORGEN - FULL MORGENRUTINE (ALLE SAKER FÅR BILDER)")
    print("=" * 70)
    print(f"Startet: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # Last credentials
    creds = load_credentials()
    brave_key = creds.get('BRAVE_API_KEY', os.environ.get('BRAVE_API_KEY', ''))
    openai_key = creds.get('OPENAI_API_KEY', os.environ.get('OPENAI_API_KEY', ''))
    
    if not brave_key:
        print("❌ Ingen BRAVE_API_KEY")
        return 1
    if not openai_key:
        print("❌ Ingen OPENAI_API_KEY")
        return 1
    
    # === STEG 1: SØK ===
    print("📡 SØKER ETTER SAKER...")
    print("-" * 70)
    
    search_queries = [
        "site:vg.no rampelys", "site:tv2.no underholdning",
        "site:nettavisen.no kjendis", "site:seher.no kjendis",
        "site:seher.no reality", "Farmen Kjendis 2026",
        "Paradise Hotel Norge", "Spillet TV 2",
        "Spellemannprisen 2026", "Eurovision Norge",
        "rød løper Norge", "norsk premiere"
    ]
    
    all_articles = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(search_brave, q, brave_key, 5): q for q in search_queries}
        for future in concurrent.futures.as_completed(futures):
            query = futures[future]
            try:
                data = future.result()
                if data and 'results' in data:
                    for r in data['results']:
                        title = r.get('title', '').strip()
                        desc = r.get('description', '').strip()
                        url = r.get('url', '').strip()
                        
                        if is_hard_news(title, desc): continue
                        if not any(x in url.lower() for x in ['vg.no', 'tv2.no', 'nettavisen.no', 'seher.no']): continue
                        
                        all_articles.append({
                            'title': create_short_title(title),
                            'description': desc,
                            'url': url,
                            'source': r.get('meta_url', {}).get('hostname', 'Ukjent'),
                            'score': calculate_score(title, desc)
                        })
            except: pass
    
    print(f"✅ {len(all_articles)} artikler funnet")
    
    # Fjern duplikater
    seen = set()
    unique = []
    for a in all_articles:
        key = a['title'][:25].lower()
        if key not in seen:
            seen.add(key)
            unique.append(a)
    
    unique.sort(key=lambda x: x['score'], reverse=True)
    top_15 = unique[:15]
    
    print(f"✅ {len(top_15)} unike saker valgt")
    print()
    
    # === STEG 2: GENERER BILDER FOR ALLE ===
    image_urls = generate_all_images(top_15, openai_key)
    
    # === STEG 3: LAGRE TIL SUPABASE ===
    inserted = insert_to_supabase(top_15, image_urls)
    
    # === OPPSUMMERING ===
    print()
    print("=" * 70)
    print("📊 RESULTAT")
    print("=" * 70)
    print(f"✅ {inserted}/15 saker lagt til sakslista")
    print(f"🎨 {sum(1 for v in image_urls.values() if v)}/15 saker med AI-bilder")
    print(f"⏱️  Fullført: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 70)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
