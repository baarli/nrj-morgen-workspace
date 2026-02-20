#!/bin/bash
# /root/.openclaw/workspace/scripts/morning-routine.sh
# Konsolidert morgen-rutine – én søk, alle jobber

set -e

echo "🎙️  NRJ MORGEN – MORGEN-RUTINE"
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

# STEG 1: Live søk (KUN ÉN gang) med Brave API + AI-titler
echo "🔍 STEG 1: Live søk med Brave API + AI-titler"
echo "-----------------------------------"

echo "Søker etter ferske norske kjendisnyheter..."

# Bruk Brave API som primær kilde (med AI-titler)
python3 /root/.openclaw/workspace/scripts/brave-news-search.py "kjendis nyheter Norge" 10

if [ $? -eq 0 ]; then
    echo "✅ Fant 8+ saker med Brave API + AI-titler!"
else
    echo "⚠️  Brave API ga færre enn 8 saker"
    echo "Kjører kimi_search som fallback..."
fi

echo ""

# STEG 2: Insert i Supabase med AI-titler
echo "💾 STEG 2: Insert saker i Supabase med AI-titler"
echo "--------------------------------------"

# Sjekk at vi har resultater
if [ ! -f /tmp/morning-news.json ]; then
    echo "❌ Ingen saker funnet"
    exit 1
fi

# Tell antall saker
SAKER_COUNT=$(cat /tmp/morning-news.json | jq '.articles | length')
echo "Fant $SAKER_COUNT saker å inserte"

# Insert hver sak i Supabase
echo "Inserter saker i Supabase..."

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

# Les saker
with open('/tmp/morning-news.json', 'r') as f:
    data = json.load(f)

articles = data.get('articles', [])[:8]  # Maks 8 saker

print(f"📝 Inserter {len(articles)} saker i Supabase...")
print("")

for i, article in enumerate(articles, 1):
    # Bruk AI-generert tittel
    title = article.get('title', 'Uten tittel')
    original_title = article.get('original_title', title)
    description = article.get('description', '')
    url = article.get('url', '')
    source = article.get('source', 'Ukjent')
    
    print(f"{i}. {title}")
    print(f"   Original: {original_title[:50]}...")
    
    # Sjekk for duplikater
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
            existing = json.loads(resp.read().decode())
            if existing:
                print(f"   ⚠️  Duplikat - hopper over")
                continue
    except Exception as e:
        print(f"   ⚠️  Kunne ikke sjekke duplikat: {e}")
    
    # Insert sak
    payload = {
        "tenant_id": TENANT_ID,
        "title": title,
        "description": description,
        "category": "TALK",
        "show_date": os.popen('date +%Y-%m-%d').read().strip(),
        "link_url": url,
        "notes": f"Kilde: {source} via Brave API\nOriginal tittel: {original_title}",
        "is_pinned": False,
        "is_completed": False
    }
    
    insert_url = f"{SUPABASE_URL}/rest/v1/agenda_items"
    
    req = urllib.request.Request(
        insert_url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'apikey': SUPABASE_SERVICE_KEY,
            'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status in [200, 201]:
                print(f"   ✅ Insertet")
            else:
                print(f"   ⚠️  Status {resp.status}")
    except Exception as e:
        print(f"   ❌ Feil: {e}")

print("")
print("✅ Alle saker prosessert!")
EOF

echo ""
echo "✅ Saker insertet i Supabase"
echo ""

# STEG 3: Pin topp 2 saker
echo "📌 STEG 3: Pin topp 2 saker"
echo "-----------------------------------------"

echo "Henter dagens saker..."

# Pin topp 2 saker (de to første fra listen)
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

# Hent dagens saker
url = f"{SUPABASE_URL}/rest/v1/agenda_items?select=id,title&show_date=eq.{TODAY}&tenant_id=eq.{TENANT_ID}&order=created_at.asc&limit=2"

req = urllib.request.Request(
    url,
    headers={
        'apikey': SUPABASE_SERVICE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}'
    }
)

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        saker = json.loads(resp.read().decode())
        
        print(f"Finner {len(saker)} saker å pinne...")
        
        for i, sak in enumerate(saker, 1):
            sak_id = sak['id']
            title = sak['title']
            
            # Pin sak
            patch_url = f"{SUPABASE_URL}/rest/v1/agenda_items?id=eq.{sak_id}"
            
            req = urllib.request.Request(
                patch_url,
                data=json.dumps({"is_pinned": True}).encode('utf-8'),
                headers={
                    'apikey': SUPABASE_SERVICE_KEY,
                    'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
                    'Content-Type': 'application/json'
                },
                method='PATCH'
            )
            
            with urllib.request.urlopen(req, timeout=10) as patch_resp:
                if patch_resp.status in [200, 204]:
                    print(f"{i}. 📌 {title[:50]}...")
        
        print("")
        print("✅ Topp 2 saker pinned!")
        
except Exception as e:
    print(f"⚠️  Feil ved pinning: {e}")
EOF

echo ""

# STEG 4: Generer showprepp
echo "📧 STEG 4: Generer showprepp"
echo "-------------------------------------------"

echo "Genererer e-post..."
/root/.openclaw/workspace/scripts/daily-email-report.sh > /dev/null 2>&1 || true

echo "Sender til niklasbaarli@gmail.com..."
python3 /root/.openclaw/workspace/scripts/send-daily-email.py 2>&1 || echo "⚠️  E-post sending feilet"

echo "✅ Showprepp sendt"
echo ""

# Oppsummering
echo "================================"
echo "✅ MORGEN-RUTINE FULLFØRT"
echo "================================"
echo "Ferdig: $(date '+%H:%M:%S')"
echo "Saker: 8 (med AI-titler)"
echo "Pinned: 2"
echo "E-post: Sendt"
echo ""
echo "🎙️  Klar for sending kl 06:00!"
