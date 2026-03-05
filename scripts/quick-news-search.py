#!/usr/bin/env python3
"""
🔍 Raskt nyhetssøk - Morning Routine style
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/scripts')

from baarliclaw_toolkit import BraveSearchClient

BRAVE_API_KEY = 'BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev'

# Kategorier
queries = [
    ("Farmen 2026", "reality"),
    ("Paradise Hotel 2026", "reality"),
    ("Kompani Lauritzen", "reality"),
    ("kjendis brudd 2026", "celebrity"),
    ("norsk kjendisnytt", "celebrity"),
    ("Spellemannprisen 2026", "music"),
    ("VG-lista", "music"),
    ("film premiere 2026", "film_tv"),
]

print("=" * 70)
print("🔍 NYHETSSØK - Morning Routine Style")
print("=" * 70)

client = BraveSearchClient(api_key=BRAVE_API_KEY)
all_articles = []

for query, category in queries:
    print(f"\n📁 Søker: {query}")
    try:
        data = client.search_news(query, count=3)
        if data and isinstance(data, list):
            for item in data[:2]:
                article = {
                    'title': item.get('title', ''),
                    'source': item.get('meta_url', {}).get('hostname', 'Ukjent'),
                    'category': category,
                    'age': item.get('age', 'Nylig'),
                    'url': item.get('url', '')
                }
                all_articles.append(article)
                print(f"  ✓ {article['title'][:55]}...")
        elif data and isinstance(data, dict) and 'results' in data:
            for item in data['results'][:2]:
                article = {
                    'title': item.get('title', ''),
                    'source': item.get('meta_url', {}).get('hostname', 'Ukjent'),
                    'category': category,
                    'age': item.get('age', 'Nylig'),
                    'url': item.get('url', '')
                }
                all_articles.append(article)
                print(f"  ✓ {article['title'][:55]}...")
    except Exception as e:
        print(f"  ✗ Feil: {e}")

# Fjern duplikater
seen = set()
unique = []
for a in all_articles:
    if a['title'] not in seen:
        seen.add(a['title'])
        unique.append(a)

print("\n" + "=" * 70)
print(f"📊 RESULTAT: {len(unique)} unike artikler funnet")
print("=" * 70)

# Vis alle
for i, article in enumerate(unique[:15], 1):
    print(f"\n{i}. {article['title']}")
    print(f"   📁 {article['category'].upper()} | 📰 {article['source']} | 🕐 {article['age']}")

print("\n" + "=" * 70)
print("✅ Søk fullført!")
print("=" * 70)
