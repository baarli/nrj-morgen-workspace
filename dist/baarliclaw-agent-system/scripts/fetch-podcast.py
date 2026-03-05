#!/usr/bin/env python3
"""Hente podkast-episoder fra RSS-feed"""

import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

RSS_URL = "https://rss.podplaystudio.com/4035.xml"

def fetch_feed():
    """Hent og parse RSS-feed"""
    try:
        req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'PodcastBot/1.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read().decode('utf-8')
            return ET.fromstring(data)
    except Exception as e:
        print(f"❌ Feil ved henting av feed: {e}")
        return None

def parse_episodes(root):
    """Parse episoder fra RSS"""
    episodes = []
    
    # Finn alle item-elementer (episoder)
    channel = root.find('channel')
    if channel is None:
        return episodes
    
    for item in channel.findall('item'):
        episode = {
            'title': item.findtext('title', 'Uten tittel'),
            'description': item.findtext('description', ''),
            'pub_date': item.findtext('pubDate', ''),
            'audio_url': None
        }
        
        # Finn lydfil (enclosure)
        enclosure = item.find('enclosure')
        if enclosure is not None:
            episode['audio_url'] = enclosure.get('url')
            episode['duration'] = enclosure.get('length', '0')
        
        episodes.append(episode)
    
    return episodes

def main():
    print("🎙️  HENTER PODKAST-EPISODER")
    print("=" * 50)
    print(f"Feed: {RSS_URL}")
    print("")
    
    root = fetch_feed()
    if root is None:
        return 1
    
    episodes = parse_episodes(root)
    
    print(f"✅ Fant {len(episodes)} episoder")
    print("")
    
    # Vis siste 5 episoder
    print("📋 SISTE 5 EPISODER:")
    print("-" * 50)
    
    for i, ep in enumerate(episodes[:5], 1):
        print(f"\n{i}. {ep['title']}")
        print(f"   📅 {ep['pub_date'][:16] if ep['pub_date'] else 'Ukjent'}")
        if ep['audio_url']:
            print(f"   🔊 {ep['audio_url'][:60]}...")
    
    # Lagre til fil
    import json
    with open('/tmp/podcast-episodes.json', 'w') as f:
        json.dump(episodes, f, indent=2)
    
    print(f"\n💾 Lagret til /tmp/podcast-episodes.json")
    return 0

if __name__ == '__main__':
    sys.exit(main())
