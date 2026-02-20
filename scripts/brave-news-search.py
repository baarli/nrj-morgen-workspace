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

def search_brave(query, api_key, count=10, site_filter=None):
    """Søk med Brave Search API"""
    import urllib.request
    import urllib.parse
    
    if not api_key:
        return None
    
    # Bygg query med eventuelt site-filter
    if site_filter:
        full_query = f"{query} site:{site_filter}"
    else:
        full_query = query
    
    encoded_query = urllib.parse.quote(full_query)
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
        return None

# Prioriterte kilder for norsk kjendis/popkultur-nyheter
PRIORITY_SOURCES = [
    'vg.no', 'dagbladet.no', 'seher.no', '730.no', 'nettavisen.no',
    'tv2.no', 'aftenposten.no', 'nrk.no'
]

# Internasjonale kilder
INTL_SOURCES = ['tmz.com', 'bbc.com']

# Kategorier vi søker etter
SEARCH_QUERIES = [
    "kjendis",
    "reality TV",
    "musikk artist",
    "popkultur",
    "underholdning"
]

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

def generate_ai_title(original_title, description=""):
    """Bruk OpenAI for å generere konsis tittel"""
    import urllib.request
    
    creds = load_credentials()
    api_key = creds.get('OPENAI_API_KEY', '')
    
    if not api_key:
        return None
    
    prompt = f"""Formater denne nyhetstittelen til en kort, konsis versjon på 5-7 ord for en radiomorgensending.

Original tittel: {original_title}
Beskrivelse: {description}

Krav:
- Maks 7 ord, helst 5-6
- Inkluder hovedperson (navn) + handling
- Gjør den umiddelbart forståelig for lyttere
- Fjern unødvendige detaljer og fluff
- Bruk aktiv form
- Skriv på norsk

Eksempler på gode titler:
- "Ida Elise Broch søker ny jobb"
- "Prins Andrew er løslatt fra politiet"  
- "Durek Verrett om Epstein og Mette-Marit"
- "Amanda Bynes er ugjenkjennelig"
- "Prinsesse Désirée av Sverige er død"

Gi KUN den formaterte tittelen, ingen forklaring eller anførselstegn:"""

    try:
        url = "https://api.openai.com/v1/chat/completions"
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Du er en erfaren nyhetsredaktør for NRK P3 og NRJ Morgen. Din jobb er å lage korte, fengende titler som umiddelbart forteller hva saken handler om."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 50
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            },
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            generated = result['choices'][0]['message']['content'].strip()
            return generated.strip('"').strip("'")
    except Exception as e:
        print(f"⚠️  OpenAI feil: {e}")
        return None

def format_brave_results(data, use_ai_titles=False):
    """Formater Brave søkeresultater, med valgfri AI tittel-generering"""
    if not data or 'results' not in data:
        return []
    
    articles = []
    for result in data.get('results', []):
        original_title = result.get('title', 'Uten tittel')
        description = result.get('description', '')
        
        # Generer AI-tittel hvis aktivert
        if use_ai_titles:
            ai_title = generate_ai_title(original_title, description)
            if ai_title:
                title = ai_title
            else:
                title = original_title
        else:
            title = original_title
        
        article = {
            'title': title,
            'original_title': original_title,
            'description': description,
            'url': result.get('url', ''),
            'source': result.get('meta', {}).get('domain', 'Ukjent kilde'),
            'publishedAt': result.get('age', 'Nylig')
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
    max_results = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    
    creds = load_credentials()
    brave_key = creds.get('BRAVE_API_KEY', '')
    use_ai = creds.get('OPENAI_API_KEY', '') != ''
    
    print("🔍 NRJ MORGEN – KJENDIS/POPKULTUR SØK")
    print("=" * 60)
    print(f"Maks resultater: {max_results}")
    print(f"AI-titler: {'Aktivert' if use_ai else 'Deaktivert'}")
    print("")
    
    all_articles = []
    
    # Søk 1: Norske kjendisnyheter (bredt)
    print("📡 Søker: Norske kjendisnyheter...")
    data = search_brave("kjendisnyheter Norge", brave_key, 10)
    if data:
        articles = format_brave_results(data, use_ai_titles=use_ai)
        all_articles.extend(articles)
        print(f"   ✅ {len(articles)} saker")
    
    # Søk 2: Reality TV
    print("📡 Søker: Reality TV...")
    data = search_brave("reality TV Norge", brave_key, 5)
    if data:
        articles = format_brave_results(data, use_ai_titles=use_ai)
        existing_urls = {a['url'] for a in all_articles}
        new_articles = [a for a in articles if a['url'] not in existing_urls]
        all_articles.extend(new_articles)
        print(f"   ✅ {len(new_articles)} nye saker")
    
    # Søk 3: Musikk
    print("📡 Søker: Musikknyheter...")
    data = search_brave("norsk musikk artist nyheter", brave_key, 5)
    if data:
        articles = format_brave_results(data, use_ai_titles=use_ai)
        existing_urls = {a['url'] for a in all_articles}
        new_articles = [a for a in articles if a['url'] not in existing_urls]
        all_articles.extend(new_articles)
        print(f"   ✅ {len(new_articles)} nye saker")
    
    # Søk 4: Popkultur
    print("📡 Søker: Popkultur...")
    data = search_brave("popkultur underholdning Norge", brave_key, 5)
    if data:
        articles = format_brave_results(data, use_ai_titles=use_ai)
        existing_urls = {a['url'] for a in all_articles}
        new_articles = [a for a in articles if a['url'] not in existing_urls]
        all_articles.extend(new_articles)
        print(f"   ✅ {len(new_articles)} nye saker")
    
    print("")
    
    # Fjern duplikater basert på URL
    seen_urls = set()
    unique_articles = []
    for article in all_articles:
        url = article.get('url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_articles.append(article)
    
    # Fjern veldig lignende titler (samme sak fra ulike kilder)
    def normalize_title(title):
        words = title.lower().split()
        key_words = [w for w in words if len(w) > 3 and w not in 
                    ['om', 'fra', 'etter', 'med', 'til', 'den', 'det', 'som', 'han', 'hun']]
        return ' '.join(sorted(set(key_words)))
    
    seen_titles = set()
    final_articles = []
    for article in unique_articles:
        norm = normalize_title(article.get('title', ''))
        is_duplicate = False
        for seen in seen_titles:
            norm_words = set(norm.split())
            seen_words = set(seen.split())
            if norm_words and seen_words:
                overlap = len(norm_words & seen_words) / max(len(norm_words), len(seen_words))
                if overlap > 0.7:
                    is_duplicate = True
                    break
        
        if not is_duplicate:
            seen_titles.add(norm)
            final_articles.append(article)
    
    # Prioriter etter kilde
    def source_priority(article):
        source = article.get('source', '').lower()
        priority_sources = [
            'vg.no', 'dagbladet.no', '730.no', 'seher.no', 
            'nettavisen.no', 'tv2.no', 'aftenposten.no', 'nrk.no',
            'tmz.com', 'bbc.com'
        ]
        for i, s in enumerate(priority_sources):
            if s in source:
                return i
        return 999
    
    final_articles.sort(key=source_priority)
    
    # Ta topp 10
    articles = final_articles[:10]
    
    if len(articles) >= 8:
        print(f"🎉 SUCCESS! Fant {len(articles)} relevante saker")
        print("\n📰 TOPP 10 SAKER:")
        print("=" * 60)
        
        for i, article in enumerate(articles, 1):
            print(f"\n{i}. {article['title']}")
            print(f"   📰 {article['source']} | 🕐 {article['publishedAt']}")
            if article['description']:
                desc = article['description'][:80] + "..." if len(article['description']) > 80 else article['description']
                print(f"   📝 {desc}")
        
        # Lagre til fil
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
        print(f"\n⚠️  Kun {len(articles)} saker funnet (trenger 8+)")
        return 1

if __name__ == '__main__':
    sys.exit(main())
