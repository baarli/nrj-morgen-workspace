#!/usr/bin/env python3
"""
NRJ MORGEN - UTVIKLET MORNING ROUTINE v2.0
Henter nyheter fra multiple kilder, samler i pot, velger topp 10, genererer titler med OpenAI

BRAVE API KEY: BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev
OPENAI API KEY: [i .credentials/live-search.env]

KILDER:
1. Morgenrutinen-søk (47 søk) - eksisterende
2. VG Rampelys
3. Nettavisen Kjendis
4. TV2 Underholdning
5. Dagbladet Kjendis
6. Se og Hør
7. 730.no

PROSESS:
1. Hent fra alle kilder (maks 48 timer gamle)
2. Samle i pot (unike saker)
3. Score hver sak (underholdningsverdi)
4. Velg topp 10
5. Generer korte titler med OpenAI (maks 7 ord)
6. Insert til Supabase

TITTELKRAV:
- Maks 7 ord
- Generert med OpenAI GPT-4o-mini
- Catchy og underholdende
- Norsk språk

KRAV:
- KUN lett underholdning
- INGEN sport, politikk, krig, harde nyheter
- Maks 48 timer gamle
- Kilder: VG, TV2, Dagbladet, Nettavisen, Se og Hør, 730
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

TODAY = datetime.now().strftime('%Y-%m-%d')
CUTOFF_DATE = (datetime.now() - timedelta(hours=48)).strftime('%Y-%m-%d')

# === KILDE-KONFIGURASJON ===
SOURCES = {
    'morgenrutinen': {
        'name': 'Morgenrutinen (47 søk)',
        'queries': [
            "site:dagbladet.no kjendis brudd", "site:dagbladet.no kjendis raser",
            "site:dagbladet.no kjendis avslører", "site:seher.no kjendis",
            "site:seher.no reality", "site:nettavisen.no kjendis",
            "site:vg.no rampelys", "site:vg.no kjendis reagerer",
            "site:tv2.no underholdning", "site:nrk.no kultur reality",
            "Farmen Kjendis", "Paradise Hotel Norge", "Spillet TV 2",
            "Kompani Lauritzen", "Love Island Norge", "Ex on the Beach Norge",
            "Sophie Elise", "Isabel Raad", "Oskar Westerlin",
            "Marius Borg Høiby", "Mikael Simpson", "Christine Dancke",
            "Mette-Marit", "Märtha Louise", "prinsesse Ingrid Alexandra",
            "kronprinsessen", "Aksel Hennie", "Kristofer Hivju",
            "Renate Reinsve", "Spellemannprisen", "P3 Gull", "VG-lista",
            "brudd kjendis", "kjendispar slutt", "krangel reality",
            "avsløring reality", "deltaker exit", "raser mot", "slakter",
            "hylles", "vekker oppsikt", "premiere TV Norge",
            "premiere film Norge", "rød løper Norge",
            "TikTok Norge viral", "Instagram Norge influencer"
        ]
    },
    'vg_rampelys': {
        'name': 'VG Rampelys',
        'queries': ["site:vg.no/rampelys"]
    },
    'nettavisen_kjendis': {
        'name': 'Nettavisen Kjendis',
        'queries': ["site:nettavisen.no/kjendis"]
    },
    'tv2_underholdning': {
        'name': 'TV2 Underholdning',
        'queries': ["site:tv2.no/underholdning"]
    },
    'dagbladet_kjendis': {
        'name': 'Dagbladet Kjendis',
        'queries': ["site:dagbladet.no/kjendis"]
    },
    'seher': {
        'name': 'Se og Hør',
        'queries': ["site:seher.no"]
    },
    '730': {
        'name': '730.no',
        'queries': ["site:730.no"]
    }
}

# === OPENAI TITTELGENERERING ===

def generate_short_title(original_title, description):
    """Generer tittel på maks 7 ord med OpenAI"""
    try:
        import urllib.request
        import json
        
        OPENAI_KEY = os.environ.get('OPENAI_API_KEY') or "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"
        
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
            
            # Fjern quotes hvis present
            new_title = new_title.strip('"\'')
            
            # Verifiser maks 7 ord
            words = new_title.split()
            if len(words) > 7:
                new_title = ' '.join(words[:7])
            
            return new_title
            
    except Exception as e:
        # Fallback: bruk original men begrens til 7 ord
        words = original_title.split()
        if len(words) > 7:
            return ' '.join(words[:7]) + '...'
        return original_title

# === HJELPEFUNKSJONER ===

def search_brave(query, count=10):
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
        'fotballforbundet', 'håndball', 'volleyball', 'basketball', 'ishockey'
    ]
    
    for word in hard_excluded:
        if word in combined:
            return True
    
    # Sport (uten kjendis)
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
    
    # Kjente navn
    celebrities = ['marius borg høiby', 'mette-marit', 'martha louise',
                   'sophie elise', 'isabel raad', 'renate reinsve']
    
    for celeb in celebrities:
        if celeb in combined:
            score += 15
    
    return min(100, max(0, score))

def explain_why(title, description):
    """Forklar hvorfor saken fungerer på NRJ"""
    combined = (title + ' ' + description).lower()
    reasons = []
    
    if any(w in combined for w in ['brudd', 'slutt']): reasons.append("brudd-drama")
    if any(w in combined for w in ['avsløring', 'hemmelig']): reasons.append("avsløring")
    if any(w in combined for w in ['raser', 'sint']): reasons.append("sterke følelser")
    if any(w in combined for w in ['sjokk', 'overrask']): reasons.append("overraskelse")
    
    return ", ".join(reasons) if reasons else "aktuell og underholdende"

# === HOVEDFUNKSJON ===

def fetch_from_source(source_key, source_config):
    """Hent saker fra en kilde"""
    print(f"\n{'='*60}")
    print(f"📡 {source_config['name']}")
    print(f"{'='*60}")
    
    articles = []
    
    for query in source_config['queries']:
        print(f"  🔍 {query[:50]}...")
        result = search_brave(query, count=10)
        
        if result and 'results' in result:
            found = result['results']
            print(f"     ✅ {len(found)} funnet")
            
            for article in found:
                # Sjekk ekskludering
                if is_excluded(article.get('title', ''), article.get('description', '')):
                    continue
                
                # Beregn score
                score = calculate_score(article.get('title', ''), article.get('description', ''))
                why = explain_why(article.get('title', ''), article.get('description', ''))
                
                articles.append({
                    'title': article.get('title', ''),
                    'url': article.get('url', ''),
                    'description': article.get('description', ''),
                    'source': source_key,
                    'score': score,
                    'why_nrj': why
                })
        else:
            print(f"     ⚠️  Ingen resultater")
    
    print(f"  📊 Totalt: {len(articles)} godkjente saker")
    return articles

def main():
    print("🌅 NRJ MORGEN - UTVIKLET MORNING ROUTINE v2.0")
    print("=" * 60)
    print(f"Dato: {TODAY}")
    print(f"Maks alder: 48 timer (cutoff: {CUTOFF_DATE})")
    print("=" * 60)
    
    # === STEG 1: Hent fra alle kilder ===
    print("\n" + "="*60)
    print("STEG 1: Henter fra alle kilder...")
    print("="*60)
    
    all_articles = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_source = {
            executor.submit(fetch_from_source, key, config): key 
            for key, config in SOURCES.items()
        }
        
        for future in concurrent.futures.as_completed(future_to_source):
            source_key = future_to_source[future]
            try:
                articles = future.result()
                all_articles.extend(articles)
            except Exception as e:
                print(f"  ❌ Feil i {source_key}: {e}")
    
    print(f"\n{'='*60}")
    print(f"📊 TOTALT I POT: {len(all_articles)} saker")
    print(f"{'='*60}")
    
    # === STEG 2: Fjern duplikater ===
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
    
    # === STEG 3: Sorter etter score ===
    print("\n" + "="*60)
    print("STEG 3: Sorterer etter underholdningsverdi...")
    print("="*60)
    
    sorted_articles = sorted(unique_list, key=lambda x: x['score'], reverse=True)
    
    # === STEG 4: Velg topp 10 og generer korte titler ===
    print("\n" + "="*60)
    print("STEG 4: Velger topp 10 og genererer korte titler...")
    print("="*60)
    
    top_10 = sorted_articles[:10]
    
    print("\n🤖 Genererer titler på maks 7 ord med OpenAI...")
    for i, article in enumerate(top_10, 1):
        original_title = article['title']
        short_title = generate_short_title(original_title, article.get('description', ''))
        article['short_title'] = short_title
        
        print(f"\n{i}. {short_title}")
        print(f"   📰 {article['source']}")
        print(f"   🎯 Score: {article['score']}/100")
        print(f"   💡 {article['why_nrj']}")
        print(f"   📝 Original: {original_title[:50]}...")
    
    # === STEG 5: Lagre resultat ===
    result = {
        'timestamp': datetime.now().isoformat(),
        'total_in_pot': len(all_articles),
        'unique_articles': len(unique_list),
        'top_10': top_10
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
