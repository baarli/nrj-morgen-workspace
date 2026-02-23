#!/usr/bin/env python3
"""
NRJ MORGEN - SANNTIDS NYHETSSØK
Optimalisert for kommersiell morgenradio med høyt tempo og bred appell (18–35)

Utfør et sanntids nyhetssøk optimalisert for NRJ Morgen.

Mål:
Finn de 15 beste og mest underholdende sakene fra siste 24–48 timer som egner seg 
for kommersiell morgenradio med høyt tempo og bred appell (18–35).

Innholdskategorier (prioritert):
- Norske og internasjonale kjendisnyheter
- TV-nyheter (underholdning, nye programmer, deltakere, konflikter)
- Reality (drama, brudd, konflikter, avsløringer, exit)
- Influencere og profiler med høy SoMe-rekkevidde
- Skandaler, kontroverser, krangler, rettssaker
- Rød løper, prisutdelinger, film, musikk
- Virale øyeblikk med norsk relevans

Krav:
- Kun saker publisert siste 48 timer (prioriter <24t)
- Kilder: VG, Dagbladet, Nettavisen, TV2, NRK, Se & Hør, Aftenposten + 
  relevante internasjonale tabloider ved stor norsk interesse
- Unngå politiske tungvektsaker uten kjendiskobling
- Prioriter konflikt, overraskelse, brudd, comeback, drama, pinlige øyeblikk, 
  sterke sitater

For hver sak lever:
1. Kort, punchy tittel
2. 2–3 setninger med essens
3. Hvorfor den fungerer på NRJ Morgen (drama, humor, gjenkjennelse, 
   diskusjonspotensial)
4. Publiseringstidspunkt og kilde
5. Direkte lenke

Sorter etter:
1) Aktualitet
2) Underholdningsverdi
3) Snakkis-potensial

Returner kun topp 15. Ingen duplikater. Ingen saker eldre enn 48 timer.

VIKTIG - SAKSLISTE-KRAV (oppdatert 2026-02-23):
- Hver sak MÅ ha bilde i link_metadata: {"image_url": "..."}
- Hver sak MÅ ha bilde i description: <img src="..." alt="..." />
- Hver sak MÅ ha created_by satt til BaarliClaw: 10aa1508-6d52-490c-8ae5-fa3da9a152c4
- Hver sak MÅ ha notes med format: "[Første setning]\n\nKilde: [Kilde]"
- Hver sak MÅ ha link_url med direkte lenke til artikkel
- Se: .config/nrj-morgen-config.md for full konfigurasjon
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
    """Sjekk om saken skal ekskluderes"""
    combined = (title + ' ' + description).lower()
    
    # Ekskluder politiske tungvektsaker uten kjendiskobling
    political_heavy = ['politikk', 'storting', 'regjering', 'lovforslag', 'budsjett']
    has_celebrity = any(word in combined for word in [
        'kjendis', 'artist', 'skuespiller', 'influencer', 'profil'
    ])
    
    if all(word in combined for word in political_heavy) and not has_celebrity:
        return True
    
    # Ekskluder spesifikke temaer
    excluded = ['fotball', 'krig', 'terror', 'død', 'tragedie']
    if any(word in combined for word in excluded):
        # Men behold hvis det er kjendis-relatert
        if not has_celebrity:
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
    
    # Optimaliserte søk for NRJ Morgen
    search_queries = [
        # Kjendis-fokus
        "site:dagbladet.no kjendis",
        "site:seher.no kjendis",
        "site:nettavisen.no kjendis",
        "site:vg.no rampelys",
        
        # TV og Reality
        "site:tv2.no underholdning",
        "site:nrk.no kultur",
        "Farmen kjendis",
        "Paradise Hotel",
        "Spillet TV 2",
        "Kompani Lauritzen",
        
        # Influencere og profiler
        "Sophie Elise",
        "Isabel Raad",
        "Oskar Westerlin",
        "Marius Borg Høiby",
        
        # Kongehus (alltid interessant)
        "Mette-Marit",
        "Märtha Louise",
        "kronprinsessen",
        
        # Film og musikk
        "Renate Reinsve",
        "Kristofer Hivju",
        "Spellemannprisen",
        "P3 Gull",
        
        # Skandaler og drama
        "brudd kjendis",
        "krangel reality",
        "avsløring",
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
