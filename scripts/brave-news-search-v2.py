#!/usr/bin/env python3
"""
NRJ MORGEN - SANNTIDS NYHETSSØK (v2.0 med BaarliClaw Toolkit)
Optimalisert for kommersiell morgenradio med høyt tempo og bred appell (18–35)

BRUKER: baarliclaw_toolkit, validation_toolkit, data_analyzer, string_toolkit, cache_toolkit
"""

import os
import sys
import json

# Legg til scripts-mappe i path
sys.path.insert(0, '/root/.openclaw/workspace/scripts')

# IMPORTER VERKTØY
from baarliclaw_toolkit import setup_logging, BraveSearchClient, retry_on_error
from validation_toolkit import Validator
from data_analyzer import TextAnalyzer
from string_toolkit import StringUtils
from cache_toolkit import MemoryCache, CacheDecorator
from date_toolkit import DateUtils

# Setup
logger = setup_logging("brave-news-search-v2")
cache = MemoryCache(default_ttl=300)  # 5 min cache

# API KEY
BRAVE_API_KEY = "BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev"

# KATEGORIER
CATEGORIES = {
    "reality": {
        "queries": ["Farmen 2026", "Paradise Hotel 2026", "Kompani Lauritzen", "Love Island Norge"],
        "weight": 1.2
    },
    "celebrity": {
        "queries": ["kjendis brudd 2026", "kjendis drama", "norsk kjendisnytt"],
        "weight": 1.3
    },
    "film_tv": {
        "queries": ["film premiere 2026", "TV premiere Norge", "rød løper"],
        "weight": 1.0
    },
    "music": {
        "queries": ["Spellemannprisen 2026", "VG-lista", "P3 Gull"],
        "weight": 1.1
    },
    "international": {
        "queries": ["Daily Mail celebrity", "TMZ news", "E! Online news"],
        "weight": 0.9
    }
}

@retry_on_error(max_retries=3)
def search_category(category_name, queries, api_key):
    """Søk i en kategori med caching og retry"""
    client = BraveSearchClient(api_key=api_key)
    results = []
    
    for query in queries:
        try:
            data = client.search_news(query, count=5)
            if data and 'results' in data:
                for item in data['results']:
                    # Valider URL
                    url_check = Validator.url(item.get('url', ''))
                    if url_check.valid:
                        results.append({
                            'title': item.get('title', ''),
                            'description': item.get('description', ''),
                            'url': url_check.cleaned_value,
                            'source': item.get('meta_url', {}).get('hostname', 'Ukjent'),
                            'category': category_name,
                            'published': item.get('age', 'Nylig')
                        })
        except Exception as e:
            logger.error(f"Søkefeil for {query}: {e}")
    
    return results

def analyze_entertainment_value(article):
    """Analyser underholdningsverdi med TextAnalyzer"""
    text = f"{article['title']} {article['description']}"
    
    # Keywords som indikerer høy underholdningsverdi
    keywords = [
        'brudd', 'drama', 'krangel', 'avsløring', 'sjokk', 'overraskelse',
        'hemmelig', 'skandale', 'krise', 'konflikt', 'vinner', 'taper',
        'kjæreste', 'ex', 'bryllup', 'gravid', 'barn', 'forelsket'
    ]
    
    analyzer = TextAnalyzer()
    sentiment = analyzer.analyze_sentiment(text)
    
    # Beregn score basert på keywords og sentiment
    score = 50  # Baseline
    text_lower = text.lower()
    
    for keyword in keywords:
        if keyword in text_lower:
            score += 10
    
    # Juster basert på sentiment intensity
    score += abs(sentiment['polarity']) * 20
    
    return min(100, max(0, score))

def format_title(title):
    """Formater tittel med StringUtils"""
    # Begrens lengde
    if len(title) > 80:
        title = title[:77] + "..."
    
    # Normaliser whitespace
    return StringUtils.normalize_whitespace(title)

def create_summary(description, source):
    """Lag oppsummering"""
    if not description:
        return f"Kilde: {source}"
    
    # Del opp i setninger
    sentences = [s.strip() for s in description.split('.') if s.strip()]
    selected = sentences[:2]  # Ta 2 første setninger
    summary = '. '.join(selected)
    
    if summary and not summary.endswith('.'):
        summary += '.'
    
    return f"{summary}\n\nKilde: {source}"

def collect_all_articles():
    """Samle alle artikler fra alle kategorier"""
    all_articles = []
    
    logger.info("Starter nyhetssøk med BaarliClaw Toolkit...")
    
    for category_name, config in CATEGORIES.items():
        logger.info(f"Søker i kategori: {category_name}")
        
        articles = search_category(
            category_name,
            config['queries'],
            BRAVE_API_KEY
        )
        
        # Legg til vekt og analyser
        for article in articles:
            article['category'] = category_name
            article['weight'] = config['weight']
            article['entertainment_score'] = analyze_entertainment_value(article)
            article['final_score'] = article['entertainment_score'] * config['weight']
        
        all_articles.extend(articles)
        logger.info(f"  Fant {len(articles)} artikler i {category_name}")
    
    return all_articles

def select_top_articles(articles, count=15):
    """Velg topp artikler med spredning"""
    # Fjern duplikater basert på URL
    seen_urls = set()
    unique = []
    for a in articles:
        if a['url'] not in seen_urls:
            seen_urls.add(a['url'])
            unique.append(a)
    
    # Sorter etter score
    sorted_articles = sorted(unique, key=lambda x: x['final_score'], reverse=True)
    
    # Velg med spredning (maks 3 per kategori)
    selected = []
    category_counts = {cat: 0 for cat in CATEGORIES.keys()}
    
    for article in sorted_articles:
        cat = article['category']
        if category_counts[cat] < 3 and len(selected) < count:
            selected.append(article)
            category_counts[cat] += 1
    
    return selected

def main():
    """Hovedfunksjon"""
    print("=" * 60)
    print("📰 NRJ MORGEN - Nyhetssøk v2.0 (med BaarliClaw Toolkit)")
    print("=" * 60)
    
    # Samle artikler
    all_articles = collect_all_articles()
    print(f"\n📊 Totalt funnet: {len(all_articles)} artikler")
    
    # Velg topp 15
    top_articles = select_top_articles(all_articles, 15)
    print(f"✅ Valgt ut: {len(top_articles)} artikler")
    
    # Vis resultater
    print("\n" + "=" * 60)
    print("🎯 TOPP 15 SAKER:")
    print("=" * 60)
    
    for i, article in enumerate(top_articles, 1):
        print(f"\n{i}. {format_title(article['title'])}")
        print(f"   📁 Kategori: {article['category']}")
        print(f"   📊 Score: {article['final_score']:.1f}")
        print(f"   📝 {create_summary(article['description'], article['source'])}")
        print(f"   🔗 {article['url']}")
    
    # Lagre til JSON
    output_file = '/tmp/brave_results_v2.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(top_articles, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Lagret til: {output_file}")
    print("\n✅ Ferdig!")
    
    return top_articles

if __name__ == "__main__":
    main()
