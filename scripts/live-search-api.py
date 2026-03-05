#!/usr/bin/env python3
# /root/.openclaw/workspace/scripts/live-search-api.py
# Faktisk live-søk med NewsAPI

import os
import sys
import json
from datetime import datetime, timedelta
from urllib.parse import quote
import urllib.request
import urllib.error

def load_credentials():
    """Last API-nøkler fra credentials-fil"""
    creds = {}
    env_file = '/root/.openclaw/workspace/.credentials/live-search.env'
    
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    # Fjern quotes hvis de finnes
                    value = value.strip('"').strip("'")
                    creds[key] = value
    return creds

def search_newsapi(query, api_key, freshness_hours=1):
    """Søk med NewsAPI"""
    if not api_key:
        return None
    
    # Beregn fra-dato
    from_date = (datetime.now() - timedelta(hours=freshness_hours)).strftime('%Y-%m-%d')
    
    # Bygg URL
    encoded_query = quote(query)
    url = f"https://newsapi.org/v2/everything?q={encoded_query}&from={from_date}&sortBy=publishedAt&language=no&apiKey={api_key}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'NRJMorgenBot/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        return {"error": str(e)}

def format_results(data, max_results=10):
    """Formater søkeresultater"""
    if not data or "error" in data:
        return f"❌ Feil: {data.get('error', 'Ukjent feil')}"
    
    if data.get('status') != 'ok':
        return f"❌ API-feil: {data.get('message', 'Ukjent feil')}"
    
    articles = data.get('articles', [])
    
    if not articles:
        return "ℹ️ Ingen resultater funnet"
    
    output = []
    output.append(f"🔍 Fant {len(articles)} artikler\n")
    output.append("=" * 60)
    
    for i, article in enumerate(articles[:max_results], 1):
        title = article.get('title', 'Uten tittel')
        source = article.get('source', {}).get('name', 'Ukjent kilde')
        published = article.get('publishedAt', '')
        url = article.get('url', '')
        
        # Formater dato
        if published:
            try:
                dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
                published_str = dt.strftime('%d.%m %H:%M')
            except:
                published_str = published
        else:
            published_str = 'Ukjent dato'
        
        output.append(f"\n{i}. {title}")
        output.append(f"   📰 {source} | 🕐 {published_str}")
        if url:
            output.append(f"   🔗 {url}")
    
    return '\n'.join(output)

def main():
    if len(sys.argv) < 2:
        print("Bruk: live-search-api.py 'søkeord' [max-results]")
        sys.exit(1)
    
    query = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    # Last credentials
    creds = load_credentials()
    api_key = creds.get('NEWSAPI_KEY', '')
    
    if not api_key:
        print("❌ Ingen API-nøkkel funnet")
        print("\n1. Gå til https://newsapi.org og registrer deg (gratis)")
        print("2. Kopier API-nøkkel til:")
        print("   /root/.openclaw/workspace/.credentials/live-search.env")
        print("\nFormat:")
        print('NEWSAPI_KEY="din_nøkkel_her"')
        sys.exit(1)
    
    print(f"🔍 Søker etter: {query}")
    print("⏳ Henter ferske nyheter...\n")
    
    # Søk
    data = search_newsapi(query, api_key)
    
    # Formater og vis
    print(format_results(data, max_results))

if __name__ == '__main__':
    main()
