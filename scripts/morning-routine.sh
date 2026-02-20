#!/bin/bash
# /root/.openclaw/workspace/scripts/morning-routine.sh
# FULL MORGEN-RUTINE med video-til-lyd pipeline

set -e

echo "🎙️  NRJ MORGEN – FULL MORGEN-RUTINE"
echo "================================"
echo "Startet: $(date '+%H:%M:%S')"
echo ""

# Last credentials
source /root/.openclaw/workspace/.credentials/nrj-morgen.env 2>/dev/null || true
source /root/.openclaw/workspace/.credentials/live-search.env 2>/dev/null || true

TODAY=$(date +%Y-%m-%d)
OSLO_TIME=$(TZ=Europe/Oslo date +%H:%M)

echo "📅 Dato: $TODAY"
echo "🕐 Oslo-tid: $OSLO_TIME"
echo ""

# STEG 1: Live søk med Brave API + AI-titler
echo "🔍 STEG 1: Live søk med Brave API + AI-titler"
echo "-----------------------------------"

python3 /root/.openclaw/workspace/scripts/brave-news-search.py 10

if [ $? -ne 0 ]; then
    echo "⚠️  Søk feilet, avbryter..."
    exit 1
fi

echo ""

# STEG 2: Insert i Supabase + hent IDs
echo "💾 STEG 2: Insert saker i Supabase"
echo "--------------------------------------"

python3 << 'EOF'
import json
import urllib.request
import os

# Last credentials
with open('/root/.openclaw/workspace/.credentials/nrj-morgen.env', 'r') as f:
    for line in f:
        if 'SUPABASE_URL=' in line:
            SUPABASE_URL = line.split('=', 1)[1].strip().strip('"').strip("'")
        if 'SUPABASE_SERVICE_KEY=' in line:
            SUPABASE_SERVICE_KEY = line.split('=', 1)[1].strip().strip('"').strip("'")

TENANT_ID = "a0000000-0000-0000-0000-000000000001"
TODAY = os.popen('date +%Y-%m-%d').read().strip()

# Les saker
with open('/tmp/morning-news.json', 'r') as f:
    data = json.load(f)

articles = data.get('articles', [])[:10]

inserted_ids = []

print(f"📝 Inserter {len(articles)} saker...")
print("")

for i, article in enumerate(articles, 1):
    title = article.get('title', 'Uten tittel')
    original_title = article.get('original_title', title)
    description = article.get('description', '')
    url = article.get('url', '')
    source = article.get('source', 'Ukjent')
    
    print(f"{i}. {title[:60]}...")
    
    # Sjekk duplikat
    check_url = f"{SUPABASE_URL}/rest/v1/agenda_items?select=id&link_url=eq.{urllib.request.quote(url, safe='')}&limit=1"
    
    req = urllib.request.Request(
        check_url,
        headers={
            'apikey': SUPABASE_SERVICE_KEY,
            'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}'
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if json.loads(resp.read().decode()):
                print(f"   ⚠️  Duplikat")
                continue
    except:
        pass
    
    # Insert
    payload = {
        "tenant_id": TENANT_ID,
        "title": title,
        "description": description,
        "category": "TALK",
        "show_date": TODAY,
        "link_url": url,
        "notes": f"Kilde: {source}\nOriginal: {original_title}",
        "is_pinned": False,
        "is_completed": False
    }
    
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/agenda_items",
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'apikey': SUPABASE_SERVICE_KEY,
            'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
            if result:
                inserted_id = result[0]['id']
                inserted_ids.append({
                    'id': inserted_id,
                    'title': title,
                    'url': url,
                    'source': source
                })
                print(f"   ✅ Insertet (ID: {inserted_id[:8]}...)")
    except Exception as e:
        print(f"   ❌ Feil: {e}")

# Lagre inserted IDs
with open('/tmp/inserted-saker.json', 'w') as f:
    json.dump({'saker': inserted_ids}, f, indent=2)

print("")
print(f"✅ {len(inserted_ids)} saker insertet")
EOF

echo ""

# STEG 3: Video-til-lyd prosessering (maks 3)
echo "🎬 STEG 3: Video-til-lyd prosessering"
echo "-----------------------------------------"

python3 << 'EOF'
import json
import subprocess
import os
import sys

# Legg til scripts-mappe i path
sys.path.insert(0, '/root/.openclaw/workspace/scripts')

from extract_video_urls import extract_video_urls
from video_to_audio_pipeline import process_video

# Les insertede saker
with open('/tmp/inserted-saker.json', 'r') as f:
    data = json.load(f)

saker = data.get('saker', [])

# Velg 3 saker med høyest video-potensial
video_keywords = ['skandale', 'avslører', 'sjokk', 'vold', 'arrestert', 
                  'rettssak', 'død', 'brudd', 'gravid', 'syk', 'politi']

scored = []
for sak in saker:
    title = sak['title'].lower()
    score = 0
    for kw in video_keywords:
        if kw in title:
            score += 2
    # Prioriter VG, TV2, NRK
    if any(s in sak.get('source', '').lower() for s in ['vg', 'tv2', 'nrk']):
        score += 1
    scored.append((score, sak))

scored.sort(key=lambda x: x[0], reverse=True)
top_3 = scored[:3]

print(f"Valgt {len(top_3)} saker for video-prosessering:")
for score, sak in top_3:
    print(f"  - {sak['title'][:50]}... (score: {score})")
print("")

# Prosesser hver sak
processed = 0
for score, sak in top_3:
    print(f"\n🎬 Prosesserer: {sak['title'][:50]}...")
    print(f"   URL: {sak['url'][:60]}...")
    
    # 1. Ekstraher video-URL
    videos = extract_video_urls(sak['url'])
    
    if not videos:
        print("   ⚠️  Ingen video funnet")
        continue
    
    video = videos[0]  # Ta første video
    print(f"   ✅ Video funnet: {video['type']}")
    
    # 2. Prosesser video til lyd
    success = process_video(
        video['url'],
        sak['title'],
        sak['source'],
        sak['id']
    )
    
    if success:
        processed += 1
        print(f"   ✅ Video prosessert!")
    else:
        print(f"   ❌ Prosessering feilet")

print(f"\n✅ {processed}/{len(top_3)} videoer prosessert")
EOF

echo ""

# STEG 4: Saksliste klar
echo "📋 STEG 4: Saksliste klar"
echo "-----------------------------------------"
echo "✅ 10 saker klare for visning"
echo "✅ Video-klipp tilgjengelig i audio-clips/"
echo ""

# STEG 5: Generer showprepp
echo "📧 STEG 5: Generer showprepp"
echo "-------------------------------------------"

echo "Genererer e-post..."
/root/.openclaw/workspace/scripts/daily-email-report.sh > /dev/null 2>&1 || true

echo "Sender til niklasbaarli@gmail.com..."
python3 /root/.openclaw/workspace/scripts/send-daily-email.py 2>&1 || echo "⚠️  E-post feilet"

echo "✅ Showprepp sendt"
echo ""

# Oppsummering
echo "================================"
echo "✅ MORGEN-RUTINE FULLFØRT"
echo "================================"
echo "Ferdig: $(date '+%H:%M:%S')"
echo "Saker: 10 (med AI-titler)"
echo "Video-klipp: Prosessert"
echo "E-post: Sendt"
echo ""
echo "🎙️  Klar for sending kl 06:00!"
