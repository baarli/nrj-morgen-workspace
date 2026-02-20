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

# Kategorier vi søker etter - PERFEKT 2026-OPPDATERT DEKNING
# Ingen begrensninger - alt skal med!
SEARCH_QUERIES = [
    # INFLUENCER & SOSIALE MEDIER (12 søk)
    "norsk influencer drama",
    "influencer skandale",
    "influencer økonomi",
    "TikTok Norge trend",
    "viral i Norge",
    "Snapchat-stjerne nyheter",
    "Vixen Awards",
    "norsk influencer priser",
    "reklame-merking klage",
    "Oskar Westerlin",
    "Sophie Elise",
    "Isabel Raad",
    "Sara Emilie Tandberg",
    
    # REALITY TV - ALTOMFATTENDE (12 søk)
    "reality TV Norge",
    "norsk reality casting",
    "reality lekkasje",
    "Spillet",
    "Forræder",
    "Vokteren",
    "Kompani Lauritzen",
    "Mesternes Mester",
    "Farmen kjendis",
    "Paradise Hotel 2026",
    "reality-brudd",
    "reality-skandale",
    "reality-par",
    
    # KONGEHUS & SOSITET (10 søk)
    "kongehuset nyheter",
    "Slottet pressemelding",
    "kronprinsessen",
    "Marius Borg Høiby",
    "Märtha Louise",
    "Durek Verrett",
    "Leah Isadora Behn",
    "Ingrid Alexandra",
    "Sverre Magnus",
    "kongelig bryllup",
    "kongehus skandale",
    "prinsesse-debatt",
    
    # PODKAST & SNAKKISER (10 søk)
    "norsk podkast nyheter",
    "Podme nyheter",
    "kontroversiell podkast",
    "Fetisha Williams",
    "Tusvik og Tønne",
    "Berrum og Beyer",
    "Høvla øve",
    "Med all respekt",
    "Jan Thomas og Harald",
    "podkast-avsløring",
    "podkast-drama",
    "podcast snakkis",
    
    # MUSIKK & POPKULTUR (10 søk)
    "norsk musikkpris",
    "Spellemann",
    "P3 Gull",
    "Kygo",
    "Alan Walker",
    "Ballinciaga",
    "Emma Steinbakken",
    "Kamelen",
    "Ramon",
    "Girl in Red",
    "Dagny",
    "norsk Eurovision",
    "MGP",
    "norsk musikk-trend",
    "utsolgt konsert",
    
    # RØD LØPER & PREMIERER (8 søk)
    "rød løper Norge",
    "kjendis-galla",
    "filmpremiere Oslo",
    "Vixen",
    "Gullruten",
    "Elle-festen",
    "MinMote",
    "norsk moteuke",
    "kjendisfest nyheter",
    "hvem var der",
    
    # INTERNASJONALT MED NORSK LINK (5 søk)
    "Renate Reinsve",
    "Kristofer Hivju",
    "Alva Bratt",
    "Haaland kjæreste",
    "Ødegaard bryllup",
    "nordmenn i Hollywood",
    "utenlandsk kjendis i Norge",
]

# PERFEKT 2026 - NAVNELISTE FOR OVERVÅKNING (Topp 100)
MONITORED_NAMES = {
    # Kongehus
    'kongehus': ['Marius Borg Høiby', 'Märtha Louise', 'Durek Verrett', 'Leah Isadora', 'Ingrid Alexandra'],
    # Influencere
    'influencer': ['Sophie Elise', 'Isabel Raad', 'Sara Emilie Tandberg', 'Oskar Westerlin', 'David Mokel'],
    # Reality-eliten
    'reality': ['Nora Haukland', 'Rikke Isaksen', 'Aleksander Sæterstøl', 'Øyunn Krogh', 'Sebastian Solberg'],
    # TV-profiler
    'tv': ['Herman Flesvig', 'Else Kåss Furuseth', 'Niklas Baarli', 'Stian Blipp', 'Jan Thomas'],
    # Podcast/Humor
    'podcast': ['Fetisha Williams', 'Martin Lepperød', 'Erlend Mørch', 'Linnea Løtvedt', 'Sigrid Bonde Tusvik'],
    # Musikk
    'musikk': ['Kygo', 'Emma Steinbakken', 'Ballinciaga', 'Kamelen', 'Alessandra Mele'],
    # Sport/Kjendis
    'sport': ['Erling Haaland', 'Martin Ødegaard', 'Helene Spilling', 'Jakob Ingebrigtsen', 'Morten Thoresen'],
    # Nye Profiler 2026
    'nye': ['Elias Omberg', 'Maria Abrahamsen', 'Dordi Boksasp Lerum', 'Agnete Husebye'],
}

# Personer/temaer vi allerede har - for å unngå duplikater
USED_TOPICS = set()

def is_duplicate_topic(title, description=""):
    """Sjekk om vi allerede har en sak om dette temaet/personen"""
    combined = (title + " " + description).lower()
    
    # Nøkkelord som identifiserer unike personer/temaer
    topic_keywords = {
        # Kongehus
        'prins andrew': ['andrew', 'mountbatten'],
        'marius høiby': ['marius', 'høiby', 'borg høiby'],
        'nora haukland': ['nora haukland', 'haukland'],
        'durek verrett': ['durek', 'verrett'],
        'mette-marit': ['mette-marit', 'kronprinsesse'],
        'kong harald': ['kong harald', 'harald'],
        'märtha louise': ['märtha', 'louise'],
        'ingrid alexandra': ['ingrid alexandra'],
        'leah isadora': ['leah isadora'],
        
        # Influencere
        'sophie elise': ['sophie elise'],
        'isabel raad': ['isabel raad'],
        'sara emilie': ['sara emilie tandberg'],
        'oskar westerlin': ['oskar westerlin'],
        
        # Reality
        'rikke isaksen': ['rikke isaksen'],
        'aleksander sæterstøl': ['aleksander sæterstøl'],
        'øyunn krogh': ['øyunn krogh'],
        'sebastian solberg': ['sebastian solberg'],
        
        # TV/Podcast
        'herman flesvig': ['herman flesvig'],
        'else kåss furuseth': ['else kåss furuseth'],
        'stian blipp': ['stian blipp'],
        'jan thomas': ['jan thomas'],
        'fetisha williams': ['fetisha williams'],
        'sigrid bonde tusvik': ['sigrid bonde tusvik'],
        
        # Musikk
        'kygo': ['kygo'],
        'alan walker': ['alan walker'],
        'ballinciaga': ['ballinciaga'],
        'emma steinbakken': ['emma steinbakken'],
        'kamelen': ['kamelen'],
        'ramon': ['ramon'],
        'girl in red': ['girl in red'],
        'dagny': ['dagny'],
        
        # Sport/Kjendis
        'erling haaland': ['haaland'],
        'martin ødegaard': ['ødegaard'],
        
        # Internasjonalt
        'pamela anderson': ['pamela anderson'],
        'kristoffer joner': ['kristoffer joner'],
    }
    
    for topic, keywords in topic_keywords.items():
        if any(kw in combined for kw in keywords):
            if topic in USED_TOPICS:
                return True
            USED_TOPICS.add(topic)
            return False
    
    return False

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
        url = result.get('url', '')
        source = result.get('meta', {}).get('domain', 'Ukjent kilde')
        
        # Generer AI-tittel hvis aktivert
        if use_ai_titles:
            ai_title = generate_ai_title(original_title, description)
            if ai_title:
                title = ai_title
            else:
                title = original_title
        else:
            title = original_title
        
        # Lag oppsummerende notat
        summary = create_summary(description, source)
        
        article = {
            'title': title,
            'original_title': original_title,
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
    
    print("🔍 NRJ MORGEN – KJENDIS/POPKULTUR SØK 2026")
    print("=" * 60)
    print(f"Maks resultater: {max_results}")
    print(f"AI-titler: {'Aktivert' if use_ai else 'Deaktivert'}")
    print("")
    
    all_articles = []
    
    # INFLUENCER & SOSIALE MEDIER (12 søk)
    print("📡 Søker: Influencer & Sosiale medier...")
    for query in ["norsk influencer drama", "influencer skandale", "influencer økonomi", "TikTok Norge trend", "viral i Norge", "Snapchat-stjerne nyheter", "Vixen Awards", "norsk influencer priser", "reklame-merking klage", "Oskar Westerlin", "Sophie Elise", "Isabel Raad", "Sara Emilie Tandberg"]:
        print(f"   🔍 '{query}'...", end=" ")
        data = search_brave(query, brave_key, 3)
        if data:
            articles = format_brave_results(data, use_ai_titles=use_ai)
            existing_urls = {a['url'] for a in all_articles}
            new_articles = [a for a in articles if a['url'] not in existing_urls]
            filtered_new = [a for a in new_articles if not is_duplicate_topic(a['title'], a.get('description', ''))]
            all_articles.extend(filtered_new)
            print(f"{len(filtered_new)} nye")
        else:
            print("0")
    
    # REALITY TV - ALTOMFATTENDE (12 søk)
    print("📡 Søker: Reality TV...")
    for query in ["reality TV Norge", "norsk reality casting", "reality lekkasje", "Spillet", "Forræder", "Vokteren", "Kompani Lauritzen", "Mesternes Mester", "Farmen kjendis", "Paradise Hotel 2026", "reality-brudd", "reality-skandale", "reality-par"]:
        print(f"   🔍 '{query}'...", end=" ")
        data = search_brave(query, brave_key, 3)
        if data:
            articles = format_brave_results(data, use_ai_titles=use_ai)
            existing_urls = {a['url'] for a in all_articles}
            new_articles = [a for a in articles if a['url'] not in existing_urls]
            filtered_new = [a for a in new_articles if not is_duplicate_topic(a['title'], a.get('description', ''))]
            all_articles.extend(filtered_new)
            print(f"{len(filtered_new)} nye")
        else:
            print("0")
    
    # KONGEHUS & SOSITET (10 søk)
    print("📡 Søker: Kongehus & Sosietet...")
    for query in ["kongehuset nyheter", "Slottet pressemelding", "kronprinsessen", "Marius Borg Høiby", "Märtha Louise", "Durek Verrett", "Leah Isadora Behn", "Ingrid Alexandra", "Sverre Magnus", "kongelig bryllup", "kongehus skandale", "prinsesse-debatt"]:
        print(f"   🔍 '{query}'...", end=" ")
        data = search_brave(query, brave_key, 3)
        if data:
            articles = format_brave_results(data, use_ai_titles=use_ai)
            existing_urls = {a['url'] for a in all_articles}
            new_articles = [a for a in articles if a['url'] not in existing_urls]
            filtered_new = [a for a in new_articles if not is_duplicate_topic(a['title'], a.get('description', ''))]
            all_articles.extend(filtered_new)
            print(f"{len(filtered_new)} nye")
        else:
            print("0")
    
    # PODKAST & SNAKKISER (10 søk)
    print("📡 Søker: Podkast & Snakkiser...")
    for query in ["norsk podkast nyheter", "Podme nyheter", "kontroversiell podkast", "Fetisha Williams", "Tusvik og Tønne", "Berrum og Beyer", "Høvla øve", "Med all respekt", "Jan Thomas og Harald", "podkast-avsløring", "podkast-drama", "podcast snakkis"]:
        print(f"   🔍 '{query}'...", end=" ")
        data = search_brave(query, brave_key, 3)
        if data:
            articles = format_brave_results(data, use_ai_titles=use_ai)
            existing_urls = {a['url'] for a in all_articles}
            new_articles = [a for a in articles if a['url'] not in existing_urls]
            filtered_new = [a for a in new_articles if not is_duplicate_topic(a['title'], a.get('description', ''))]
            all_articles.extend(filtered_new)
            print(f"{len(filtered_new)} nye")
        else:
            print("0")
    
    # MUSIKK & POPKULTUR (10 søk)
    print("📡 Søker: Musikk & Popkultur...")
    for query in ["norsk musikkpris", "Spellemann", "P3 Gull", "Kygo", "Alan Walker", "Ballinciaga", "Emma Steinbakken", "Kamelen", "Ramon", "Girl in Red", "Dagny", "norsk Eurovision", "MGP", "norsk musikk-trend", "utsolgt konsert"]:
        print(f"   🔍 '{query}'...", end=" ")
        data = search_brave(query, brave_key, 3)
        if data:
            articles = format_brave_results(data, use_ai_titles=use_ai)
            existing_urls = {a['url'] for a in all_articles}
            new_articles = [a for a in articles if a['url'] not in existing_urls]
            filtered_new = [a for a in new_articles if not is_duplicate_topic(a['title'], a.get('description', ''))]
            all_articles.extend(filtered_new)
            print(f"{len(filtered_new)} nye")
        else:
            print("0")
    
    # RØD LØPER & PREMIERER (8 søk)
    print("📡 Søker: Rød løper & Premierer...")
    for query in ["rød løper Norge", "kjendis-galla", "filmpremiere Oslo", "Vixen", "Gullruten", "Elle-festen", "MinMote", "norsk moteuke", "kjendisfest nyheter", "hvem var der"]:
        print(f"   🔍 '{query}'...", end=" ")
        data = search_brave(query, brave_key, 3)
        if data:
            articles = format_brave_results(data, use_ai_titles=use_ai)
            existing_urls = {a['url'] for a in all_articles}
            new_articles = [a for a in articles if a['url'] not in existing_urls]
            filtered_new = [a for a in new_articles if not is_duplicate_topic(a['title'], a.get('description', ''))]
            all_articles.extend(filtered_new)
            print(f"{len(filtered_new)} nye")
        else:
            print("0")
    
    # INTERNASJONALT MED NORSK LINK (5 søk)
    print("📡 Søker: Internasjonalt med norsk link...")
    for query in ["Renate Reinsve", "Kristofer Hivju", "Alva Bratt", "Haaland kjæreste", "Ødegaard bryllup", "nordmenn i Hollywood", "utenlandsk kjendis i Norge"]:
        print(f"   🔍 '{query}'...", end=" ")
        data = search_brave(query, brave_key, 3)
        if data:
            articles = format_brave_results(data, use_ai_titles=use_ai)
            existing_urls = {a['url'] for a in all_articles}
            new_articles = [a for a in articles if a['url'] not in existing_urls]
            filtered_new = [a for a in new_articles if not is_duplicate_topic(a['title'], a.get('description', ''))]
            all_articles.extend(filtered_new)
            print(f"{len(filtered_new)} nye")
        else:
            print("0")
    
    print("")
    
    # Fjern duplikater basert på URL
    seen_urls = set()
    unique_articles = []
    for article in all_articles:
        url = article.get('url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_articles.append(article)
    
    # Filtrer bort uønskede kategorier (sport, politikk, økonomi)
    EXCLUDED_KEYWORDS = [
        'fotball', 'håndball', 'ski', 'langrenn', 'skiskyting', 'hopp',
        'politikk', 'storting', 'regjering', 'parti', 'valg',
        'økonomi', 'børs', 'rente', 'finans', 'krig', 'ukraina',
        'været', 'trafikk', 'koronavirus', 'covid',
        'ol ', 'oslo ', 'vm ', 'em ', 'nm ',  # Sportsturneringer
    ]
    
    filtered_articles = []
    for article in unique_articles:
        title = article.get('title', '').lower()
        desc = article.get('description', '').lower()
        combined = title + ' ' + desc
        
        # Sjekk om artikkelen inneholder ekskluderte ord
        should_exclude = False
        for keyword in EXCLUDED_KEYWORDS:
            if keyword in combined:
                should_exclude = True
                break
        
        if not should_exclude:
            filtered_articles.append(article)
    
    print(f"   🎯 {len(filtered_articles)}/{len(unique_articles)} saker etter filtrering")
    
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
    
    filtered_articles.sort(key=source_priority)
    
    # Ta topp 10
    articles = filtered_articles[:10]
    
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
