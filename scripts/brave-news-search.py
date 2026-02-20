#!/usr/bin/env python3
# brave-news-search-parallel.py
# PARALLELLISERT versjon av nyhetssøk

import os
import sys
import json
import concurrent.futures
import urllib.request
import urllib.parse
import socket
from datetime import datetime

def load_credentials():
    """Last API-nøkler"""
    creds = {}
    env_file = '/root/.openclaw/workspace/.credentials/live-search.env'
    
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    value = value.strip('"').strip("'")
                    creds[key] = value
    return creds

def search_single(query, api_key, count=10, timeout=10):
    """Enkelt søk med timeout"""
    if not api_key:
        return None
    
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.search.brave.com/res/v1/news/search?q={encoded_query}&count={count}&search_lang=nb&freshness=pd"
    
    headers = {
        'X-Subscription-Token': api_key,
        'Accept': 'application/json'
    }
    
    try:
        socket.setdefaulttimeout(timeout)
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode())
            socket.setdefaulttimeout(None)
            return data
    except Exception as e:
        socket.setdefaulttimeout(None)
        return None

def format_results(data):
    """Formater søkeresultater med oppsummering"""
    if not data or 'results' not in data:
        return []
    
    articles = []
    for result in data.get('results', []):
        title = result.get('title', 'Uten tittel')
        description = result.get('description', '')
        url = result.get('url', '')
        source = result.get('meta', {}).get('domain', 'Ukjent kilde')
        
        # Lag oppsummerende notat
        summary = create_summary(description, source)
        
        article = {
            'title': title,
            'description': description,
            'url': url,
            'source': source,
            'publishedAt': result.get('age', 'Nylig'),
            'summary': summary
        }
        articles.append(article)
    
    return articles

def create_summary(description, source):
    """Lag et kort oppsummerende notat av saken"""
    if not description:
        return f"Kilde: {source}"
    
    # Trekk ut første setning (eller del av den)
    first_sentence = description.split('.')[0].strip()
    
    # Begrens lengde
    if len(first_sentence) > 150:
        first_sentence = first_sentence[:147] + "..."
    
    # Lag oppsummering
    summary = f"{first_sentence}\n\nKilde: {source}"
    
    return summary

def main():
    max_results = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    
    creds = load_credentials()
    brave_key = creds.get('BRAVE_API_KEY', '')
    
    print("🔍 NRJ MORGEN - PARALLELLISERT SØK")
    print("=" * 60)
    print(f"Maks resultater: {max_results}")
    print(f"⚡ Parallellisering: 10 samtidige søk")
    print("")
    
    # Optimalisert liste med viktigste søk
    queries = [
        "Marius Borg Høiby", "Märtha Louise", "Durek Verrett",
        "Sophie Elise", "Isabel Raad", "Oskar Westerlin",
        "Farmen kjendis", "Paradise Hotel", "Kompani Lauritzen",
        "norsk musikk", "Spellemann", "P3 Gull",
        "Erling Haaland", "Martin Ødegaard",
        "rød løper Norge", "Vixen Awards",
        "kongehuset nyheter", "norsk influencer",
        "Renate Reinsve", "Kristofer Hivju",
    ]
    
    print(f"📡 Starter {len(queries)} parallelle søk...")
    print("")
    
    import time
    start_time = time.time()
    
    # Kjør alle søk parallelt med ThreadPoolExecutor
    all_articles = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Start alle søk
        future_to_query = {
            executor.submit(search_single, query, brave_key, 3, 8): query 
            for query in queries
        }
        
        # Samle resultater
        completed = 0
        for future in concurrent.futures.as_completed(future_to_query):
            query = future_to_query[future]
            completed += 1
            try:
                data = future.result()
                if data:
                    articles = format_results(data)
                    all_articles.extend(articles)
                    print(f"   ✅ {completed}/{len(queries)}: {query[:30]}... ({len(articles)} funnet)")
                else:
                    print(f"   ⚠️  {completed}/{len(queries)}: {query[:30]}... (ingen resultater)")
            except Exception as e:
                print(f"   ❌ {completed}/{len(queries)}: {query[:30]}... (feil)")
    
    print("")
    print(f"⏱️  Søketid: {time.time() - start_time:.1f} sekunder")
    print(f"   📊 Totalt: {len(all_articles)} rå artikler")
    
    # Fjern duplikater
    seen_urls = set()
    unique_articles = []
    for article in all_articles:
        url = article.get('url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_articles.append(article)
    
    print(f"   📊 Unike artikler: {len(unique_articles)}")
    
    # Filtrer
    EXCLUDED = ['fotball', 'politikk', 'økonomi', 'krig']
    filtered = []
    for article in unique_articles:
        combined = (article.get('title', '') + ' ' + article.get('description', '')).lower()
        if not any(kw in combined for kw in EXCLUDED):
            filtered.append(article)
    
    print(f"   🎯 Etter filtrering: {len(filtered)} artikler")
    
    # Prioriter og ta toppen
    def priority(article):
        source = article.get('source', '').lower()
        priority_list = ['vg.no', 'dagbladet.no', 'seher.no', 'nettavisen.no', 'tv2.no']
        for i, s in enumerate(priority_list):
            if s in source:
                return i
        return 999
    
    filtered.sort(key=priority)
    articles = filtered[:max_results]
    
    if len(articles) >= 5:
        print(f"\n🎉 SUCCESS! Fant {len(articles)} relevante saker")
        print("\n📰 TOPP SAKER:")
        print("=" * 60)
        
        for i, article in enumerate(articles, 1):
            print(f"\n{i}. {article['title']}")
            print(f"   📰 {article['source']} | 🕐 {article['publishedAt']}")
            if article.get('description'):
                desc = article['description'][:80] + "..." if len(article['description']) > 80 else article['description']
                print(f"   📝 {desc}")
        
        # Lagre
        output = {
            'timestamp': datetime.now().isoformat(),
            'count': len(articles),
            'articles': articles
        }
        
        with open('/tmp/morning-news.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n💾 Lagret til /tmp/morning-news.json")
        return 0
    else:
        print(f"\n⚠️  Kun {len(articles)} saker funnet")
        return 0

if __name__ == '__main__':
    sys.exit(main())
