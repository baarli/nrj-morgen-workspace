#!/usr/bin/env python3
"""
NRJ MORGEN - AUTO INSERT TOPP 10
Kjører morning-routine-v2.py og legger topp 10 i Supabase

Bruker OpenAI-genererte titler (maks 7 ord) fra morning-routine-v2.py
"""

import subprocess
import json
import urllib.request
import uuid
from datetime import datetime

# Supabase config
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"
TENANT_ID = "a0000000-0000-0000-0000-000000000001"
CREATED_BY = "10aa1508-6d52-490c-8ae5-fa3da9a152c4"
TODAY = datetime.now().strftime('%Y-%m-%d')

print("🌅 NRJ MORGEN - AUTO INSERT TOPP 10")
print("=" * 60)
print()

# Kjør morning-routine-v2
print("1️⃣ Kjører Morning Routine v2.0...")
result = subprocess.run(['python3', '/root/.openclaw/workspace/scripts/morning-routine-v2.py'], 
                       capture_output=True, text=True)
print(result.stdout)

# Les resultat
try:
    with open('/tmp/morning-routine-v2-result.json', 'r') as f:
        data = json.load(f)
    top_10 = data['top_10']
    print(f"✅ Fant {len(top_10)} saker i topp 10")
except Exception as e:
    print(f"❌ Feil ved lesing av resultat: {e}")
    exit(1)

# Hent eksisterende URL-er
print("\n2️⃣ Sjekker eksisterende saker...")
req = urllib.request.Request(
    f"{SUPABASE_URL}/rest/v1/agenda_items?tenant_id=eq.{TENANT_ID}&select=link_url",
    headers={'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}'}
)

with urllib.request.urlopen(req, timeout=15) as response:
    existing = json.loads(response.read().decode('utf-8'))
    existing_urls = {item['link_url'].lower() for item in existing if item.get('link_url')}

print(f"   {len(existing)} saker allerede i databasen")

# Hent max order_index
req2 = urllib.request.Request(
    f"{SUPABASE_URL}/rest/v1/agenda_items?tenant_id=eq.{TENANT_ID}&select=order_index&order=order_index.desc&limit=1",
    headers={'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}'}
)

try:
    with urllib.request.urlopen(req2, timeout=15) as response:
        max_order = json.loads(response.read().decode('utf-8'))
        start_order = max_order[0]['order_index'] + 1 if max_order else 1
except:
    start_order = 1

# Legg til nye saker
print("\n3️⃣ Legger til nye saker...")
added = 0

for idx, article in enumerate(top_10):
    url = article['url'].lower()
    
    # Sjekk duplikat
    if url in existing_urls:
        print(f"   ⚠️  Hopper over (finnes): {article['title'][:50]}...")
        continue
    
    payload = {
        'id': str(uuid.uuid4()),
        'tenant_id': TENANT_ID,
        'title': article.get('short_title', article['title'])[:200],
        'description': article.get('description', '')[:500],
        'notes': f"{article.get('description', '')[:300]}\n\nUnderholdningsverdi: {article.get('score', 70)}/100\nHvorfor NRJ: {article.get('why_nrj', 'aktuell')}",
        'link_url': article['url'],
        'link_metadata': json.dumps({
            'source': article.get('source', ''),
            'publishedAt': 'Nylig',
            'image_url': ''
        }),
        'category': 'TALK',
        'show_date': TODAY,
        'order_index': start_order + idx,
        'created_by': CREATED_BY,
        'is_pinned': False
    }
    
    req3 = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/agenda_items",
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json'
        }
    )
    
    try:
        with urllib.request.urlopen(req3, timeout=15):
            added += 1
            print(f"   ✅ Lagt til: {article['title'][:50]}...")
    except Exception as e:
        print(f"   ❌ Feil: {e}")

print(f"\n{'='*60}")
print(f"🎉 Fullført!")
print(f"   Lagt til: {added} nye saker")
print(f"   Fra pot: {data['total_in_pot']} totale saker")
print(f"   Unike: {data['unique_articles']} unike saker")
print(f"{'='*60}")
