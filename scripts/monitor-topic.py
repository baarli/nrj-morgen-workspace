#!/usr/bin/env python3
# /root/.openclaw/workspace/scripts/monitor-topic.py
# Kontinuerlig overvåking av emner

import os
import sys
import time
import json
from datetime import datetime
from urllib.parse import quote
import urllib.request

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

def check_news(topic, api_key, last_titles):
    """Sjekk etter nye nyheter"""
    url = f"https://newsapi.org/v2/everything?q={quote(topic)}&sortBy=publishedAt&language=no&pageSize=5&apiKey={api_key}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'NRJMorgenBot/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            if data.get('status') != 'ok':
                return None, last_titles
            
            articles = data.get('articles', [])
            new_articles = []
            
            for article in articles:
                title = article.get('title', '')
                if title and title not in last_titles:
                    new_articles.append(article)
                    last_titles.add(title)
                    # Begrens sett-størrelse
                    if len(last_titles) > 100:
                        last_titles.pop()
            
            return new_articles, last_titles
            
    except Exception as e:
        print(f"⚠️  Feil: {e}")
        return None, last_titles

def main():
    if len(sys.argv) < 2:
        print("Bruk: monitor-topic.py 'emne' [interval_minutter]")
        sys.exit(1)
    
    topic = sys.argv[1]
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    creds = load_credentials()
    api_key = creds.get('NEWSAPI_KEY', '')
    
    if not api_key:
        print("❌ Ingen API-nøkkel. Sett opp i live-search.env")
        sys.exit(1)
    
    print(f"🔍 Overvåker: {topic}")
    print(f"⏰ Intervall: hvert {interval}. minutt")
    print(f"🛑 Trykk Ctrl+C for å stoppe\n")
    
    last_titles = set()
    
    # Første sjekk
    new_articles, last_titles = check_news(topic, api_key, last_titles)
    print(f"📊 Startet overvåking. Fant {len(new_articles)} eksisterende artikler.")
    
    try:
        while True:
            time.sleep(interval * 60)
            
            new_articles, last_titles = check_news(topic, api_key, last_titles)
            
            if new_articles:
                print(f"\n🚨 {datetime.now().strftime('%H:%M')} - NYE ARTIKLER FUNNET!")
                print("=" * 50)
                for article in new_articles:
                    print(f"📰 {article.get('title')}")
                    print(f"   Fra: {article.get('source', {}).get('name')}")
                    print(f"   {article.get('url')}\n")
            else:
                print(f"✓ {datetime.now().strftime('%H:%M')} - Ingen nye artikler")
                
    except KeyboardInterrupt:
        print("\n\n🛑 Overvåking stoppet")

if __name__ == '__main__':
    main()
