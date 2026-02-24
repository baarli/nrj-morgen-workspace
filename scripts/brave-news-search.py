#!/usr/bin/env python3
"""
NRJ MORGEN - SANNTIDS NYHETSSØK
Optimalisert for kommersiell morgenradio med høyt tempo og bred appell (18–35)

BRAVE API KEY: BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev

VIKTIG - KUN LETT UNDERHOLDNING:
✅ Kjendisnyheter (brudd, drama, avsløringer)
✅ Reality-TV (Farmen, Paradise Hotel, Kompani Lauritzen)
✅ Influencere og profiler
✅ Film og musikk (premierer, priser)
✅ Kongehus (lett underholdning)
✅ Sosiale medier og viral content

❌ KUTTET - IKKE INKLUDER:
- Sport (fotball, håndball, ski, etc.)
- Hard politikk (regjering, storting, lovforslag)
- Krig og konflikt
- Harde nyheter (drap, ulykker, tragedier)
- Økonomi og finans
- Korona og helse

KRAV:
- KUN saker publisert siste 24 timer (freshness=pd)
- Maks 48 timer gamle
- Kilder: VG, Dagbladet, Nettavisen, TV2, NRK, Se & Hør, Aftenposten
- Prioriter: konflikt, overraskelse, brudd, drama, pinlige øyeblikk

For hver sak lever:
1. Kort, punchy tittel
2. 2–3 setninger med essens
3. Hvorfor den fungerer på NRJ Morgen
4. Publiseringstidspunkt og kilde
5. Direkte lenke

Returner kun topp 15. Ingen duplikater. Ingen saker eldre enn 48 timer.
"""

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
    # Prøv flere mulige lokasjoner
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
    """Søk med Brave API
    
    Args:
        query: Søkeord
        api_key: Brave API nøkkel
        count: Antall resultater (default 10)
        freshness: 'pd' (past day), 'pw' (past week), 'pm' (past month)
    """
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
        print(f"   Søkefeil: {e}")
        return None

def format_article(result):
    """Formater en artikkel fra Brave resultat"""
    title = result.get('title', '').strip()
    description = result.get('description', '').strip()
    url = result.get('url', '').strip()
    
    # Hent kilde fra meta_url
    meta_url = result.get('meta_url', {})
    source = meta_url.get('hostname', 'Ukjent kilde')
    
    # Hent publiseringstid
    published = result.get('age', result.get('page_age', 'Nylig'))
    
    # Lag oppsummering (2-3 setninger)
    summary = create_summary(description, source)
    
    # Vurder underholdningsverdi (0-100)
    entertainment_score = calculate_entertainment_score(title, description)
    
    return {
        'title': title,
        'description': description,
        'url': url,
        'source': source,
        'publishedAt': published,
        'summary': summary,
        'entertainment_score': entertainment_score,
        'why_nrj': explain_why_nrj(title, description)
    }

def create_summary(description, source):
    """Lag 2-3 setninger med essens"""
    if not description:
        return f"Kilde: {source}"
    
    # Del opp i setninger
    sentences = [s.strip() for s in description.split('.') if s.strip()]
    
    # Ta de 2-3 første setningene
    selected = sentences[:3]
    summary = '. '.join(selected)
    
    if summary and not summary.endswith('.'):
        summary += '.'
    
    return f"{summary}\n\nKilde: {source}"

def calculate_entertainment_score(title, description):
    """Vurder underholdningsverdi (0-100)"""
    score = 50  # Baseline
    combined = (title + ' ' + description).lower()
    
    # Positive faktorer (konflikt, drama, overraskelse)
    positive_keywords = [
        'brudd', 'krangel', 'drama', 'skandale', 'avsløring', 'hemmelig',
        'kontrovers', 'konflikt', 'exit', 'kastet ut', 'bekjentgjøring',
        'overraskelse', 'comeback', 'pinlig', 'sterkt sitat', 'avslører',
        'tårer', 'raser', 'sint', 'sjokk', 'kaos', 'krise'
    ]
    
    # Negative faktorer (tungt, politisk, tørt)
    negative_keywords = [
        'politikk', 'økonomi', 'skatt', 'lovforslag', 'regjering',
        'kommune', 'fylke', 'budsjett', 'valg', 'parti'
    ]
    
    for keyword in positive_keywords:
        if keyword in combined:
            score += 10
    
    for keyword in negative_keywords:
        if keyword in combined:
            score -= 20
    
    # Boost for kjente navn
    celebrities = [
        'marius borg høiby', 'mette-marit', 'haakon', 'martha louise',
        'sophie elise', 'isabel raad', 'oskar westerlin', 'stig henrik hoff',
        'renate reinsve', 'kristofer hivju', 'erling haaland'
    ]
    
    for celeb in celebrities:
        if celeb in combined:
            score += 15
    
    return min(100, max(0, score))

def explain_why_nrj(title, description):
    """Forklar hvorfor saken fungerer på NRJ Morgen"""
    combined = (title + ' ' + description).lower()
    reasons = []
    
    if any(word in combined for word in ['brudd', 'slutt', 'over']):
        reasons.append("brudd-drama")
    if any(word in combined for word in ['krangel', 'konflikt', 'krig']):
        reasons.append("konflikt")
    if any(word in combined for word in ['avsløring', 'hemmelig', 'skandale']):
        reasons.append("avsløring")
    if any(word in combined for word in ['tårer', 'raser', 'sint', 'emot']):
        reasons.append("sterke følelser")
    if any(word in combined for word in ['comeback', 'returnerer', 'igjen']):
        reasons.append("comeback")
    if any(word in combined for word in ['pinlig', 'feil', 'bommet']):
        reasons.append("pinlig øyeblikk")
    if any(word in combined for word in ['sjokk', 'overrask', 'uventet']):
        reasons.append("overraskelse")
    
    if not reasons:
        return "aktuell og underholdende"
    
    return ", ".join(reasons)

def is_relevant_source(url):
    """Sjekk om kilden er relevant for NRJ Morgen"""
    relevant_sources = [
        'vg.no', 'dagbladet.no', 'nettavisen.no', 'tv2.no', 
        'nrk.no', 'seher.no', 'aftenposten.no',
        'dailymail.co.uk', 'tmz.com', 'eonline.com', 'people.com'
    ]
    
    url_lower = url.lower()
    return any(source in url_lower for source in relevant_sources)

def is_excluded(title, description):
    """Sjekk om saken skal ekskluderes - KUTT: sport, hard politikk, krig, harde nyheter"""
    combined = (title + ' ' + description).lower()
    
    # HARD EKSKLUDERING - disse skal ALLTID kuttes
    hard_excluded = [
        'fotball', 'krig', 'terror', 'død', 'tragedie', 'ulykke', 'drap',
        'skudd', 'vold', 'politi', 'pågripelse', 'fengsel', 'dom', 'rettssak',
        'regjering', 'storting', 'parti', 'politiker', 'lovforslag', 'budsjett',
        'skatt', 'økonomi', 'finans', 'rente', 'inflasjon', 'sykehus', 'korona',
        'skiforbundet', 'langrenn', 'ski', 'hopp', 'alpint', 'skiskyting',
        'fotballforbundet', 'håndball', 'volleyball', 'basketball', 'ishockey'
    ]
    
    for word in hard_excluded:
        if word in combined:
            return True
    
    # EKSKLUDER sport (med mindre det er kjendis-relatert)
    sport_words = ['seriegull', 'gull', 'sølv', 'bronse', 'medalje', 'cup', 'liga', 
                   'kamp', 'seier', 'tap', 'spiller', 'laget', 'trener', 'slår',
                   'konkurrere', 'konkurranse', 'mesterskap', 'forbund']
    has_sport = any(word in combined for word in sport_words)
    has_celebrity = any(word in combined for word in [
        'kjendis', 'artist', 'skuespiller', 'influencer', 'profil', 'rampelys'
    ])
    
    if has_sport and not has_celebrity:
        return True
    
    return False

def main():
    max_results = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    
    creds = load_credentials()
    brave_key = creds.get('BRAVE_API_KEY', os.environ.get('BRAVE_API_KEY', ''))
    
    if not brave_key:
        print("❌ Ingen BRAVE_API_KEY funnet")
        return 1
    
    print("🔍 NRJ MORGEN - SANNTIDS NYHETSSØK")
    print("=" * 60)
    print(f"Mål: {max_results} beste sakene (siste 24-48t)")
    print(f"Målgruppe: 18-35 år, kommersiell morgenradio")
    print("")
    
    # Optimaliserte søk for NRJ Morgen - FOKUS: Lett underholdning, maks 48 timer gamle
    # KUTTET: Sport, hard politikk, krig, harde nyheter
    search_queries = [
        # Kjendis-fokus (lett underholdning)
        "site:dagbladet.no kjendis brudd",
        "site:dagbladet.no kjendis raser",
        "site:dagbladet.no kjendis avslører",
        "site:seher.no kjendis",
        "site:seher.no reality",
        "site:nettavisen.no kjendis",
        "site:vg.no rampelys",
        "site:vg.no kjendis reagerer",
        
        # TV og Reality (underholdning)
        "site:tv2.no underholdning",
        "site:nrk.no kultur reality",
        "Farmen Kjendis",
        "Paradise Hotel Norge",
        "Spillet TV 2",
        "Kompani Lauritzen",
        "Love Island Norge",
        "Ex on the Beach Norge",
        
        # Influencere og profiler
        "Sophie Elise",
        "Isabel Raad",
        "Oskar Westerlin",
        "Marius Borg Høiby",
        "Mikael Simpson",
        "Christine Dancke",
        
        # Kongehus (lett underholdning)
        "Mette-Marit",
        "Märtha Louise",
        "kronprinsessen",
        "prinsesse Ingrid Alexandra",
        
        # Film og musikk (underholdning)
        "Renate Reinsve",
        "Kristofer Hivju",
        "Aksel Hennie",
        "Spellemannprisen",
        "P3 Gull",
        "VG-lista",
        "Eurovision Norge",
        
        # Skandaler og drama (lett underholdning)
        "brudd kjendis",
        "kjendispar slutt",
        "krangel reality",
        "avsløring reality",
        "deltaker exit",
        "raser mot",
        "slakter",
        "hylles",
        "vekker oppsikt",
        
        # Premier og events
        "premiere TV Norge",
        "rød løper Norge",
        "premiere film Norge",
        
        # Sosiale medier og viral
        "TikTok Norge viral",
        "Instagram Norge influencer",
    ]
    
    print(f"📡 Starter {len(search_queries)} målrettede søk...")
    print("")
    
    import time
    start_time = time.time()
    
    # Kjør søk parallelt
    all_articles = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
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
                        article = format_article(result)
                        
                        # Filtrer
                        if not is_relevant_source(article['url']):
                            continue
                        if is_excluded(article['title'], article['description']):
                            continue
                        
                        all_articles.append(article)
                    
                    print(f"   ✅ {completed}/{len(search_queries)}: {query[:35]}... ({len(data['results'])} funnet)")
                else:
                    print(f"   ⚠️  {completed}/{len(search_queries)}: {query[:35]}... (ingen resultater)")
            except Exception as e:
                print(f"   ❌ {completed}/{len(search_queries)}: {query[:35]}... (feil: {str(e)[:30]})")
    
    print("")
    print(f"⏱️  Søketid: {time.time() - start_time:.1f} sekunder")
    print(f"   📊 Totalt: {len(all_articles)} artikler funnet")
    
    # Fjern duplikater
    seen_urls = set()
    unique_articles = []
    for article in all_articles:
        url = article.get('url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_articles.append(article)
    
    print(f"   📊 Unike artikler: {len(unique_articles)}")
    
    # Sorter etter underholdningsverdi (descending)
    unique_articles.sort(key=lambda x: x['entertainment_score'], reverse=True)
    
    # Ta topp 15
    top_articles = unique_articles[:max_results]
    
    if len(top_articles) >= 5:
        print(f"\n🎉 SUCCESS! Fant {len(top_articles)} relevante saker")
        print("\n📰 TOPP SAKER FOR NRJ MORGEN:")
        print("=" * 60)
        
        for i, article in enumerate(top_articles, 1):
            print(f"\n{i}. {article['title']}")
            print(f"   📰 {article['source']} | 🕐 {article['publishedAt']}")
            print(f"   🎯 Underholdningsverdi: {article['entertainment_score']}/100")
            print(f"   💡 Hvorfor NRJ: {article['why_nrj']}")
            if article.get('description'):
                desc = article['description'][:100] + "..." if len(article['description']) > 100 else article['description']
                print(f"   📝 {desc}")
        
        # Lagre til JSON
        output = {
            'timestamp': datetime.now().isoformat(),
            'count': len(top_articles),
            'articles': top_articles
        }
        
        with open('/tmp/morning-news.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Lagret til /tmp/morning-news.json")
        return 0
    else:
        print(f"\n⚠️  Kun {len(top_articles)} saker funnet (mål: {max_results})")
        return 0

if __name__ == '__main__':
    sys.exit(main())
