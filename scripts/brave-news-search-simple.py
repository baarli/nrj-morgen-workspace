#!/usr/bin/env python3
"""
NRJ MORGEN - SANNTIDS NYHETSSØK
Optimalisert for LETT underholdning (IKKE harde nyheter)
Kilder: VG Rampelys, TV2 Underholdning, Nettavisen Kjendis, Se og Hør, 730.no
"""

import os
import sys
import json
import concurrent.futures
import urllib.request
import urllib.parse
import socket
import time
import random
from datetime import datetime

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
    """Lag kort, beskrivende tittel - maks 6-7 ord"""
    # Fjern unødvendige ord
    words = original_title.split()
    
    # Hvis allerede kort nok, behold den
    if len(words) <= 7:
        return original_title
    
    # Ellers, ta de viktigste ordene
    # Prioriter: hvem + hva + kontekst
    key_words = []
    skip_words = {'den', 'det', 'som', 'for', 'med', 'til', 'av', 'på', 'om', 'er', 'å', 'en', 'et'}
    
    for word in words:
        if word.lower() not in skip_words and len(key_words) < 7:
            key_words.append(word)
    
    short_title = ' '.join(key_words)
    
    # Legg til ... hvis vi kuttet
    if len(words) > 7:
        short_title = short_title.rstrip('.') + '...'
    
    return short_title

def is_hard_news(title, description):
    """Sjekk om det er hard nyhet som skal ekskluderes"""
    combined = (title + ' ' + description).lower()
    
    hard_keywords = [
        'krig', 'terror', 'angrep', 'drap', 'voldtekt', 'overgrep',
        'tragedie', 'ulykke', 'død', 'omkom', 'drept', 'skutt',
        'politi', 'pågripelse', 'fengsel', 'dom', 'rettssak',
        'regjering', 'storting', 'parti', 'politikk', 'lovforslag',
        'skatt', 'budsjett', 'økonomi', 'finans', 'rente', 'inflasjon',
        'sykehus', 'korona', 'covid', 'pandemi',
        'israel', 'gaza', 'palestina', 'ukraina', 'russland'
    ]
    
    for word in hard_keywords:
        if word in combined:
            return True
    return False

def calculate_score(title, description):
    """Vurder underholdningsverdi (0-100)"""
    score = 50
    combined = (title + ' ' + description).lower()
    
    # Boost for ønskede temaer
    if any(x in combined for x in ['rød løper', 'premiere', 'galla', 'fest']):
        score += 20
    if any(x in combined for x in ['farmen', 'paradise hotel', 'spillet', 'kompani lauritzen']):
        score += 15
    if any(x in combined for x in ['spellemann', 'p3 gull', 'vg-lista', 'eurovision']):
        score += 15
    if any(x in combined for x in ['brudd', 'skandale', 'avsløring', 'ny kjæreste']):
        score += 10
    
    # Reduser for potensielt harde temaer
    if any(x in combined for x in ['kronprins', 'mette-marit', 'kongehus']):
        score -= 20
    
    return min(100, max(0, score))

def main():
    max_results = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    
    creds = load_credentials()
    brave_key = creds.get('BRAVE_API_KEY', os.environ.get('BRAVE_API_KEY', ''))
    
    if not brave_key:
        print("❌ Ingen BRAVE_API_KEY funnet")
        return 1
    
    print("🔍 NRJ MORGEN - LETT UNDERHOLDNING")
    print("=" * 60)
    print(f"Mål: {max_results} lettbeinte saker")
    print(f"Kilder: VG Rampelys, TV2, Nettavisen, Se og Hør, 730.no")
    print("")
    
    # Søk - fokus på lett underholdning
    search_queries = [
        # VG Rampelys
        "site:vg.no rampelys",
        "site:vg.no rampelys kjendis",
        "site:vg.no rampelys brudd",
        
        # TV 2 Underholdning  
        "site:tv2.no underholdning",
        "site:tv2.no underholdning kjendis",
        
        # Nettavisen Kjendis
        "site:nettavisen.no kjendis",
        "site:nettavisen.no kjendis brudd",
        
        # Se og Hør
        "site:seher.no kjendis",
        "site:seher.no reality",
        "site:seher.no rød løper",
        
        # 730.no
        "site:730.no",
        
        # Reality
        "Farmen Kjendis 2026",
        "Paradise Hotel Norge",
        "Spillet TV 2",
        
        # Musikk
        "Spellemannprisen 2026",
        "P3 Gull",
        "VG-lista",
        "Eurovision Norge",
        
        # Kjendiser
        "Sophie Elise",
        "Isabel Raad",
        "Oskar Westerlin",
        "Renate Reinsve",
        
        # Rød løper og premier
        "rød løper Norge",
        "norsk premiere",
    ]
    
    print(f"📡 Starter {len(search_queries)} søk...")
    
    all_articles = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_to_query = {
            executor.submit(search_brave, query, brave_key, 5): query 
            for query in search_queries
        }
        
        completed = 0
        for future in concurrent.futures.as_completed(future_to_query):
            query = future_to_query[future]
            completed += 1
            
            try:
                data = future.result()
                if data and 'results' in data:
                    for result in data['results']:
                        title = result.get('title', '').strip()
                        desc = result.get('description', '').strip()
                        url = result.get('url', '').strip()
                        
                        # Ekskluder harde nyheter
                        if is_hard_news(title, desc):
                            continue
                        
                        # Kun fra godkjente kilder
                        if not any(x in url.lower() for x in ['vg.no', 'tv2.no', 'nettavisen.no', 'seher.no', '730.no', 'dagbladet.no']):
                            continue
                        
                        all_articles.append({
                            'title': create_short_title(title),
                            'original_title': title,
                            'description': desc,
                            'url': url,
                            'source': result.get('meta_url', {}).get('hostname', 'Ukjent'),
                            'score': calculate_score(title, desc)
                        })
                    
                    print(f"   ✅ {completed}/{len(search_queries)}: {query[:30]}... ({len(data['results'])} funnet)")
            except Exception as e:
                print(f"   ⚠️  {completed}/{len(search_queries)}: {query[:30]}... (feil)")
    
    print(f"\n📊 {len(all_articles)} artikler funnet")
    
    # Fjern duplikater
    seen_urls = set()
    seen_titles = set()
    unique_articles = []
    
    for article in all_articles:
        url = article['url']
        title_key = article['title'][:25].lower()
        
        if url not in seen_urls and title_key not in seen_titles:
            seen_urls.add(url)
            seen_titles.add(title_key)
            unique_articles.append(article)
    
    print(f"📊 {len(unique_articles)} unike artikler")
    
    # Sorter etter score
    unique_articles.sort(key=lambda x: x['score'], reverse=True)
    
    # Ta topp 15
    top_articles = unique_articles[:max_results]
    
    if len(top_articles) >= 5:
        print(f"\n🎉 Fant {len(top_articles)} relevante saker!")
        print("\n📰 TOPP SAKER:")
        print("=" * 60)
        
        for i, article in enumerate(top_articles, 1):
            print(f"\n{i}. {article['title']}")
            print(f"   📰 {article['source']} | 🎯 {article['score']}/100")
            print(f"   📝 {article['description'][:80]}...")
        
        # Lagre
        with open('/tmp/morning-news.json', 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'count': len(top_articles),
                'articles': top_articles
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Lagret til /tmp/morning-news.json")
        return 0
    else:
        print(f"\n⚠️  Kun {len(top_articles)} saker funnet")
        return 0

if __name__ == '__main__':
    sys.exit(main())
