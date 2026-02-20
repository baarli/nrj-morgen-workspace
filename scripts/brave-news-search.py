#!/usr/bin/env python3
# /root/.openclaw/workspace/scripts/brave-news-search.py
# Søk etter nyheter med Brave API (primær), fallback til NewsAPI og kimi_search

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta

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

def search_brave(query, api_key, count=10):
    """Søk med Brave Search API"""
    import urllib.request
    import urllib.parse
    
    if not api_key:
        return None
    
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.search.brave.com/res/v1/news/search?q={encoded_query}&count={count}&search_lang=nb&freshness=pd"
    
    headers = {
        'X-Subscription-Token': api_key,
        'Accept': 'application/json'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        print(f"⚠️  Brave API feil: {e}")
        return None

def search_newsapi(query, api_key, count=10):
    """Fallback: Søk med NewsAPI"""
    import urllib.request
    import urllib.parse
    
    if not api_key:
        return None
    
    from_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    encoded_query = urllib.parse.quote(query)
    url = f"https://newsapi.org/v2/everything?q={encoded_query}&from={from_date}&sortBy=publishedAt&language=no&pageSize={count}&apiKey={api_key}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'NRJMorgenBot/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        print(f"⚠️  NewsAPI feil: {e}")
        return None

def search_kimi(query, count=10):
    """Siste fallback: Bruk kimi_search via CLI"""
    try:
        # Dette vil bli håndtert av cron-jobben som bruker kimi_search direkte
        return None
    except:
        return None

def format_brave_results(data):
    """Formater Brave søkeresultater"""
    if not data or 'results' not in data:
        return []
    
    articles = []
    for result in data.get('results', []):
        article = {
            'title': result.get('title', 'Uten tittel'),
            'description': result.get('description', ''),
            'url': result.get('url', ''),
            'source': result.get('meta', {}).get('domain', 'Ukjent kilde'),
            'publishedAt': result.get('age', 'Nylig'),
            'image': result.get('meta', {}).get('thumbnail', '')
        }
        articles.append(article)
    
    return articles

def format_newsapi_results(data):
    """Formater NewsAPI resultater"""
    if not data or data.get('status') != 'ok':
        return []
    
    articles = []
    for article in data.get('articles', []):
        formatted = {
            'title': article.get('title', 'Uten tittel'),
            'description': article.get('description', ''),
            'url': article.get('url', ''),
            'source': article.get('source', {}).get('name', 'Ukjent kilde'),
            'publishedAt': article.get('publishedAt', ''),
            'image': article.get('urlToImage', '')
        }
        articles.append(formatted)
    
    return articles

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "kjendis nyheter"
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    creds = load_credentials()
    brave_key = creds.get('BRAVE_API_KEY', '')
    newsapi_key = creds.get('NEWSAPI_KEY', '')
    
    print(f"🔍 Søker etter: {query}")
    print(f"Maks resultater: {max_results}")
    print("")
    
    articles = []
    
    # STEG 1: Prøv Brave API først
    if brave_key:
        print("📡 Bruker Brave Search API (primær)...")
        brave_data = search_brave(query, brave_key, max_results)
        articles = format_brave_results(brave_data)
        
        if articles:
            print(f"✅ Fant {len(articles)} artikler med Brave API")
        else:
            print("⚠️  Ingen resultater fra Brave API")
    
    # STEG 2: Fallback til NewsAPI hvis Brave ikke ga nok
    if len(articles) < 8 and newsapi_key:
        print("📡 Bruker NewsAPI (fallback)...")
        newsapi_data = search_newsapi(query, newsapi_key, max_results)
        newsapi_articles = format_newsapi_results(newsapi_data)
        
        # Legg til nye artikler (unngå duplikater basert på URL)
        existing_urls = {a['url'] for a in articles}
        for article in newsapi_articles:
            if article['url'] not in existing_urls:
                articles.append(article)
        
        print(f"✅ Totalt {len(articles)} artikler etter NewsAPI fallback")
    
    # STEG 3: Sjekk om vi har nok
    if len(articles) >= 8:
        print(f"\n🎉 SUCCESS! Fant {len(articles)} artikler")
        print("\n📰 TOPP 8 SAKER:")
        print("=" * 60)
        
        for i, article in enumerate(articles[:8], 1):
            print(f"\n{i}. {article['title']}")
            print(f"   📰 {article['source']} | 🕐 {article['publishedAt']}")
            if article['description']:
                desc = article['description'][:100] + "..." if len(article['description']) > 100 else article['description']
                print(f"   📝 {desc}")
        
        # Lagre til fil for videre bruk
        output = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'count': len(articles),
            'articles': articles[:8]
        }
        
        with open('/tmp/morning-news.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n💾 Lagret til /tmp/morning-news.json")
        return 0
    
    else:
        print(f"\n⚠️  Kun {len(articles)} artikler funnet (trenger 8)")
        print("💡 Kjører kimi_search som siste fallback...")
        return 1

if __name__ == '__main__':
    sys.exit(main())
