#!/usr/bin/env python3
"""
Podcast Clipper - Hent og klipp ut snutter fra podkast-episoder
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET

# Konfigurasjon
RSS_FEED = "https://rss.podplaystudio.com/4035.xml"
CACHE_DIR = Path("/tmp/podcast-clips")
CACHE_FILE = CACHE_DIR / "episodes.json"

# Opprett cache-mappe
CACHE_DIR.mkdir(exist_ok=True)

def fetch_rss():
    """Hent og parse RSS-feed"""
    try:
        with urllib.request.urlopen(RSS_FEED, timeout=30) as response:
            xml_content = response.read()
        
        root = ET.fromstring(xml_content)
        
        # Finn alle item-elementer (episoder)
        # RSS namespace
        ns = {'content': 'http://purl.org/rss/1.0/modules/content/'}
        
        episodes = []
        for item in root.findall('.//item'):
            title = item.find('title')
            description = item.find('description')
            pub_date = item.find('pubDate')
            enclosure = item.find('enclosure')
            duration = item.find('.//{http://www.itunes.com/dtds/podcast-1.0.dtd}duration')
            
            episode = {
                'title': title.text.strip() if title is not None and title.text else 'Ukjent tittel',
                'description': description.text if description is not None and description.text else '',
                'pub_date': pub_date.text if pub_date is not None else '',
                'audio_url': enclosure.get('url') if enclosure is not None else '',
                'duration': duration.text if duration is not None else '0'
            }
            episodes.append(episode)
        
        # Lagre til cache
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(episodes, f, ensure_ascii=False, indent=2)
        
        return episodes
    except Exception as e:
        print(f"❌ Feil ved henting av RSS: {e}")
        # Prøv å lese fra cache hvis tilgjengelig
        if CACHE_FILE.exists():
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

def list_episodes(limit=10):
    """List siste episoder"""
    episodes = fetch_rss()
    
    print(f"\n🎙️  SISTE {min(limit, len(episodes))} EPISODER")
    print("=" * 60)
    
    for i, ep in enumerate(episodes[:limit], 1):
        title = ep['title'][:50] + '...' if len(ep['title']) > 50 else ep['title']
        date = ep['pub_date'][:16] if ep['pub_date'] else 'Ukjent dato'
        print(f"\n{i}. {title}")
        print(f"   📅 {date}")
        print(f"   🔗 {ep['audio_url'][:60]}...")
    
    return episodes[:limit]

def download_episode(episode_index=0, output_dir=None, quiet=False):
    """Last ned en episode"""
    episodes = fetch_rss()
    
    if not episodes or episode_index >= len(episodes):
        if not quiet:
            print("❌ Ingen episode funnet")
        return None
    
    episode = episodes[episode_index]
    
    if output_dir is None:
        output_dir = CACHE_DIR
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
    
    # Lag filnavn fra tittel
    safe_title = re.sub(r'[^\w\s-]', '', episode['title']).strip().replace(' ', '_')[:30]
    filename = f"{safe_title}.mp3"
    filepath = output_dir / filename
    
    if filepath.exists():
        if not quiet:
            print(f"✅ Fil finnes allerede: {filepath}")
        return str(filepath)
    
    if not quiet:
        print(f"\n📥 Laster ned: {episode['title'][:50]}...")
        print(f"   URL: {episode['audio_url'][:60]}...")
    
    try:
        urllib.request.urlretrieve(episode['audio_url'], filepath)
        if not quiet:
            print(f"✅ Lastet ned til: {filepath}")
        return str(filepath)
    except Exception as e:
        if not quiet:
            print(f"❌ Feil ved nedlasting: {e}")
        return None

def analyze_audio(filepath):
    """Analyser lydfil for å finne beste øyeblikk (placeholder)"""
    print(f"\n🔍 Analyserer: {filepath}")
    print("   (Krever pydub for faktisk analyse)")
    
    # Placeholder - i produksjon ville dette analysert lydnivå, pauser, etc.
    # For nå returnerer vi mock-data
    return [
        {"start": 120, "end": 150, "confidence": 0.85, "type": "laughter"},
        {"start": 450, "end": 480, "confidence": 0.72, "type": "conversation"},
        {"start": 890, "end": 920, "confidence": 0.68, "type": "reaction"}
    ]

def create_clip(audio_path, start, end, output_path, text=None):
    """Klipp ut en del av lydfilen"""
    print(f"\n✂️  Lager klipp: {start}s - {end}s")
    print(f"   Input: {audio_path}")
    print(f"   Output: {output_path}")
    
    # Bruk ffmpeg for å klippe
    duration = end - start
    cmd = f'ffmpeg -y -i "{audio_path}" -ss {start} -t {duration} -c copy "{output_path}"'
    
    result = os.system(cmd)
    
    if result == 0:
        print(f"✅ Klipp laget: {output_path}")
        return output_path
    else:
        print(f"❌ Feil ved klipping")
        return None

def create_video(audio_path, text, output_path, template="default"):
    """Lag video fra audio med tekst-overlay"""
    print(f"\n🎬 Lager video med tekst: '{text[:40]}...'")
    
    # Placeholder - i produksjon ville dette laget en faktisk video
    # med tekst-overlay, bakgrunnsbilde, etc.
    print(f"   (Krever ffmpeg med filter_complex for full implementasjon)")
    print(f"   Audio: {audio_path}")
    print(f"   Output: {output_path}")
    
    return output_path

def get_latest_episode_info():
    """Hent info om siste episode"""
    episodes = fetch_rss()
    if episodes:
        return episodes[0]
    return None

def main():
    parser = argparse.ArgumentParser(description='Podcast Clipper - Hent og klipp podkast-episoder')
    subparsers = parser.add_subparsers(dest='command', help='Kommandoer')
    
    # fetch-latest
    subparsers.add_parser('fetch-latest', help='Hent siste episoder fra RSS')
    
    # list
    list_parser = subparsers.add_parser('list', help='List episoder')
    list_parser.add_argument('--limit', type=int, default=10, help='Antall episoder å vise')
    
    # download
    download_parser = subparsers.add_parser('download', help='Last ned episode')
    download_parser.add_argument('--episode-index', type=int, default=0, help='Episode-index (0 = siste)')
    download_parser.add_argument('--output-dir', help='Output-mappe')
    download_parser.add_argument('--quiet', action='store_true', help='Kun output filsti')
    
    # analyze
    analyze_parser = subparsers.add_parser('analyze', help='Analyser lydfil')
    analyze_parser.add_argument('--file', required=True, help='Lydfil å analysere')
    
    # create-clip
    clip_parser = subparsers.add_parser('create-clip', help='Lag klipp fra episode')
    clip_parser.add_argument('--file', required=True, help='Lydfil')
    clip_parser.add_argument('--start', type=int, required=True, help='Start-tid (sekunder)')
    clip_parser.add_argument('--end', type=int, required=True, help='Slutt-tid (sekunder)')
    clip_parser.add_argument('--text', help='Tekst/quote fra klippet')
    clip_parser.add_argument('--output', help='Output-fil')
    
    # to-video
    video_parser = subparsers.add_parser('to-video', help='Lag video fra klipp')
    video_parser.add_argument('--audio', required=True, help='Audio-fil')
    video_parser.add_argument('--text', required=True, help='Tekst-overlay')
    video_parser.add_argument('--output', required=True, help='Output-fil')
    
    args = parser.parse_args()
    
    if args.command == 'fetch-latest':
        episodes = fetch_rss()
        print(f"✅ Hentet {len(episodes)} episoder")
        
    elif args.command == 'list':
        list_episodes(args.limit)
        
    elif args.command == 'download':
        result = download_episode(args.episode_index, args.output_dir, args.quiet)
        if result:
            print(result)
        
    elif args.command == 'analyze':
        analyze_audio(args.file)
        
    elif args.command == 'create-clip':
        if not args.output:
            args.output = f"clip_{args.start}_{args.end}.mp3"
        create_clip(args.file, args.start, args.end, args.output, args.text)
        
    elif args.command == 'to-video':
        create_video(args.audio, args.text, args.output)
        
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
