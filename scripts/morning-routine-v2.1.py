#!/usr/bin/env python3
"""
NRJ MORGEN - UTVIKLET MORNING ROUTINE v2.1
Bedre spredning på temaer - unngå for mange saker om samme person/tema
"""

import os
import sys
import json
import concurrent.futures
import urllib.request
import urllib.parse
import uuid
from datetime import datetime, timedelta

# === KONFIGURASJON ===
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = os.environ.get('SUPABASE_KEY') or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"
TENANT_ID = "a0000000-0000-0000-0000-000000000001"
CREATED_BY = "10aa1508-6d52-490c-8ae5-fa3da9a152c4"
BRAVE_KEY = os.environ.get('BRAVE_API_KEY') or "BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev"
OPENAI_KEY = os.environ.get('OPENAI_API_KEY') or "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"

TOMORROW = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

print("🌅 NRJ MORGEN - MORNING ROUTINE v2.1 (Bedre spredning)")
print("=" * 60)
print(f"Dato: {TOMORROW}")
print("=" * 60)

# === KILDE-KONFIGURASJON - BEDRE SPREDNING ===
# Vi deler søkene i kategorier og tar maks 2 fra hver kategori
SOURCES = {
    'reality_tv': {
        'name': 'Reality TV',
        'queries': [
            "site:tv2.no Farmen Kjendis",
            "site:tv2.no Paradise Hotel",
            "site:tv2.no Kompani Lauritzen",
            "site:tv2.no Love Island",
        ],
        'max_articles': 3
    },
    'kjendis_drama': {
        'name': 'Kjendis Drama',
        'queries': [
            "site:dagbladet.no kjendis brudd",
            "site:seher.no kjendis",
            "site:nettavisen.no kjendis",
            "site:vg.no rampelys",
        ],
        'max_articles': 3
    },
    'film_tv': {
        'name': 'Film & TV',
        'queries': [
            "site:vg.no rampelys premiere",
            "site:nrk.no kultur film",
            "site:dagbladet.no kultur tv",
            "site:tv2.no underholdning",
        ],
        'max_articles': 3
    },
    'musikk': {
        'name': 'Musikk',
        'queries': [
            "Spellemannprisen 2026",
            "VG-lista",
            "P3 Gull",
            "site:nrk.no kultur musikk",
        ],
        'max_articles': 3
    },
    'internasjonalt': {
        'name': 'Internasjonalt',
        'queries': [
            "site:dailymail.co.uk celebrity",
            "site:tmz.com celebrity news",
            "site:eonline.com news",
            "site:people.com celebrity",
        ],
        'max_articles': 3
    },
}

# === HJELPEFUNKSJONER ===

def search_brave(query, count=5):
    """Søk med Brave API"""
    if not BRAVE_KEY:
        return None
    
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.search.brave.com/res/v1/news/search?q={encoded_query}&count={count}&search_lang=nb&country=no&freshness=pd"
    
    headers = {
        'X-Subscription-Token': BRAVE_KEY,
        'Accept': 'application/json'
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"  ⚠️  Feil i søk: {e}")
        return None

def is_excluded(title, description):
    """Sjekk om saken skal ekskluderes"""
    combined = (title + ' ' + description).lower()
    
    # HARD EKSKLUDERING
    hard_excluded = [
        'fotball', 'krig', 'terror', 'død', 'tragedie', 'ulykke', 'drap',
        'skudd', 'vold', 'politi', 'pågripelse', 'fengsel', 'dom', 'rettssak',
        'regjering', 'storting', 'parti', 'politiker', 'lovforslag', 'budsjett',
        'skatt', 'økonomi', 'finans', 'rente', 'inflasjon', 'sykehus', 'korona',
        'skiforbundet', 'langrenn', 'ski', 'hopp', 'alpint', 'skiskyting',
    ]
    
    for word in hard_excluded:
        if word in combined:
            return True
    
    return False

def calculate_score(title, description):
    """Vurder underholdningsverdi (0-100)"""
    score = 50
    combined = (title + ' ' + description).lower()
    
    # Positive faktorer
    positive = ['brudd', 'krangel', 'drama', 'skandale', 'avsløring', 'hemmelig',
                'kontrovers', 'konflikt', 'exit', 'overraskelse', 'comeback', 
                'pinlig', 'sterkt sitat', 'tårer', 'raser', 'sjokk', 'kaos']
    
    for keyword in positive:
        if keyword in combined:
            score += 10
    
    return min(100, max(0, score))

def generate_short_title(original_title, description):
    """Generer tittel på maks 7 ord med OpenAI"""
    try:
        prompt = f"""Original tittel: {original_title}
Beskrivelse: {description[:200]}

Lag en kort, catchy tittel på NORSK for NRJ Morgen (morgenradio).
- Maksimum 7 ord
- Fængende og underholdende
- Fokus på det mest interessante
- Bruk norsk språk

Kun tittelen, ingen forklaring."""
        
        headers = {
            'Authorization': f'Bearer {OPENAI_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'gpt-4o-mini',
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.7,
            'max_tokens': 50
        }
        
        req = urllib.request.Request(
            'https://api.openai.com/v1/chat/completions',
            data=json.dumps(data).encode('utf-8'),
            headers=headers
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            new_title = result['choices'][0]['message']['content'].strip()
            new_title = new_title.strip('"\'')
            words = new_title.split()
            if len(words) > 7:
                new_title = ' '.join(words[:7])
            return new_title
            
    except Exception as e:
        words = original_title.split()
        if len(words) > 7:
            return ' '.join(words[:7]) + '...'
        return original_title

def fetch_from_source(source_key, source_config):
    """Hent saker fra en kilde"""
    print(f"\n📡 {source_config['name']}")
    print("-" * 40)
    
    articles = []
    
    for query in source_config['queries']:
        print(f"  🔍 {query[:40]}...")
        result = search_brave(query, count=5)
        
        if result and 'results' in result:
            found = result['results']
            print(f"     ✅ {len(found)} funnet")
            
            for article in found:
                if is_excluded(article.get('title', ''), article.get('description', '')):
                    continue
                
                score = calculate_score(article.get('title', ''), article.get('description', ''))
                
                articles.append({
                    'title': article.get('title', ''),
                    'url': article.get('url', ''),
                    'description': article.get('description', ''),
                    'source': source_key,
                    'score': score,
                    'category': source_config['name']
                })
        else:
            print(f"     ⚠️  Ingen resultater")
    
    # Sorter etter score og ta de beste
    articles.sort(key=lambda x: x['score'], reverse=True)
    best_articles = articles[:source_config['max_articles']]
    
    print(f"  📊 Valgt: {len(best_articles)} av {len(articles)} saker")
    return best_articles

# === HOVEDFUNKSJON ===

def main():
    # Hent fra alle kilder
    print("\n" + "="*60)
    print("STEG 1: Henter fra alle kilder (maks 2 per kategori)...")
    print("="*60)
    
    all_articles = []
    
    for key, config in SOURCES.items():
        articles = fetch_from_source(key, config)
        all_articles.extend(articles)
    
    print(f"\n{'='*60}")
    print(f"📊 TOTALT: {len(all_articles)} saker fra alle kilder")
    print(f"{'='*60}")
    
    # Fjern duplikater
    print("\n" + "="*60)
    print("STEG 2: Fjerner duplikater...")
    print("="*60)
    
    unique_articles = {}
    for article in all_articles:
        url = article['url'].lower()
        if url not in unique_articles:
            unique_articles[url] = article
    
    unique_list = list(unique_articles.values())
    print(f"  ✅ {len(unique_list)} unike saker")
    
    # Sorter etter score
    sorted_articles = sorted(unique_list, key=lambda x: x['score'], reverse=True)
    
    # Velg topp 15 (økt fra 10)
    print("\n" + "="*60)
    print("STEG 3: Velger topp 15 med spredning...")
    print("="*60)
    
    top_15 = sorted_articles[:15]
    
    print("\n🤖 Genererer titler med OpenAI...")
    for i, article in enumerate(top_15, 1):
        original_title = article['title']
        short_title = generate_short_title(original_title, article.get('description', ''))
        article['short_title'] = short_title
        
        print(f"\n{i}. {short_title}")
        print(f"   📰 {article['category']}")
        print(f"   🎯 Score: {article['score']}/100")
    
    # Lagre resultat
    result = {
        'timestamp': datetime.now().isoformat(),
        'total': len(all_articles),
        'unique': len(unique_list),
        'top_15': top_15
    }
    
    with open('/tmp/morning-routine-v2-result.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n{'='*60}")
    print("✅ Fullført!")
    print(f"💾 Lagret til: /tmp/morning-routine-v2-result.json")
    print(f"{'='*60}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
