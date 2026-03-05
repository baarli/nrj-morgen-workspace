#!/usr/bin/env python3
# /root/.openclaw/workspace/scripts/extract-video-urls.py
# Ekstraher video-URLer fra norske nyhetsartikler

import sys
import re
import json
import urllib.request
import urllib.error
from urllib.parse import urljoin, urlparse

def fetch_page(url):
    """Hent HTML-innhold fra URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"⚠️  Kunne ikke hente {url}: {e}")
        return None

def extract_video_urls_vg(html, base_url):
    """Ekstraher video-URLer fra VG-artikler"""
    videos = []
    
    # VG bruker data-video-id eller video-elementer
    patterns = [
        r'data-video-id="(\d+)"',
        r'"videoId":\s*"(\d+)"',
        r'"videoUrl":\s*"([^"]+)"',
        r'<video[^>]+src="([^"]+)"',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html)
        for match in matches:
            if match.isdigit():
                # VG video ID - konstruer URL
                videos.append({
                    'url': f"https://www.vg.no/video/{match}",
                    'type': 'vg_video',
                    'id': match
                })
            elif match.startswith('http'):
                videos.append({
                    'url': match,
                    'type': 'direct'
                })
    
    return videos

def extract_video_urls_tv2(html, base_url):
    """Ekstraher video-URLer fra TV2-artikler"""
    videos = []
    
    # TV2 bruker data-video-id eller embed-koder
    patterns = [
        r'data-video-id="(\d+)"',
        r'"videoId":\s*"(\d+)"',
        r'"videoUrl":\s*"([^"]+)"',
        r'tv2\.no/video/[^"\s]+',
        r'embed\.tv2\.no/[^"\s]+',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html)
        for match in matches:
            if match.isdigit():
                videos.append({
                    'url': f"https://www.tv2.no/video/{match}",
                    'type': 'tv2_video',
                    'id': match
                })
            elif 'tv2.no/video' in match or 'embed.tv2' in match:
                videos.append({
                    'url': match if match.startswith('http') else f"https://{match}",
                    'type': 'tv2_video'
                })
    
    return videos

def extract_video_urls_dagbladet(html, base_url):
    """Ekstraher video-URLer fra Dagbladet-artikler"""
    videos = []
    
    # Dagbladet bruker ofte YouTube eller egne videoer
    patterns = [
        r'youtube\.com/embed/([a-zA-Z0-9_-]+)',
        r'youtu\.be/([a-zA-Z0-9_-]+)',
        r'data-video-id="(\d+)"',
        r'"videoUrl":\s*"([^"]+)"',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html)
        for match in matches:
            if len(match) == 11:  # YouTube ID
                videos.append({
                    'url': f"https://www.youtube.com/watch?v={match}",
                    'type': 'youtube',
                    'id': match
                })
            elif match.isdigit():
                videos.append({
                    'url': f"https://www.dagbladet.no/video/{match}",
                    'type': 'dagbladet_video',
                    'id': match
                })
            elif match.startswith('http'):
                videos.append({
                    'url': match,
                    'type': 'direct'
                })
    
    return videos

def extract_video_urls_nrk(html, base_url):
    """Ekstraher video-URLer fra NRK-artikler"""
    videos = []
    
    # NRK bruker data-video-id eller psapi
    patterns = [
        r'data-video-id="([^"]+)"',
        r'"id":\s*"([^"]{8,})"[^}]*"video"',
        r'nrk\.no/video/[^"\s]+',
        r'psapi\.nrk\.no/[^"\s]+',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html)
        for match in matches:
            if 'nrk.no/video' in match:
                videos.append({
                    'url': match if match.startswith('http') else f"https://{match}",
                    'type': 'nrk_video'
                })
            elif len(match) > 8:  # Sannsynligvis NRK video ID
                videos.append({
                    'url': f"https://www.nrk.no/video/{match}",
                    'type': 'nrk_video',
                    'id': match
                })
    
    return videos

def extract_video_urls_nettavisen(html, base_url):
    """Ekstraher video-URLer fra Nettavisen-artikler"""
    videos = []
    
    patterns = [
        r'data-video-id="(\d+)"',
        r'nettavisen\.no/[^"\s]*video[^"\s]*',
        r'vgtv\.no/[^"\s]+',  # Nettavisen bruker ofte VGTV
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html)
        for match in matches:
            if match.isdigit():
                videos.append({
                    'url': f"https://www.nettavisen.no/video/{match}",
                    'type': 'nettavisen_video',
                    'id': match
                })
            elif 'nettavisen' in match or 'vgtv' in match:
                videos.append({
                    'url': match if match.startswith('http') else f"https://{match}",
                    'type': 'nettavisen_video'
                })
    
    return videos

def extract_video_urls_generic(html, base_url):
    """Generisk ekstrahering for ukjente kilder"""
    videos = []
    
    # YouTube (vanlig på mange sider)
    youtube_patterns = [
        r'youtube\.com/embed/([a-zA-Z0-9_-]+)',
        r'youtu\.be/([a-zA-Z0-9_-]+)',
        r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
    ]
    
    for pattern in youtube_patterns:
        matches = re.findall(pattern, html)
        for match in matches:
            videos.append({
                'url': f"https://www.youtube.com/watch?v={match}",
                'type': 'youtube',
                'id': match
            })
    
    # Generiske video-elementer
    video_patterns = [
        r'<video[^>]+src="([^"]+)"',
        r'<source[^>]+src="([^"]+)"[^>]+type="video',
    ]
    
    for pattern in video_patterns:
        matches = re.findall(pattern, html)
        for match in matches:
            if match.startswith('http'):
                videos.append({
                    'url': match,
                    'type': 'direct'
                })
    
    return videos

def extract_video_urls(url):
    """Hovedfunksjon - ekstraher video-URLer fra en artikkel"""
    
    print(f"🔍 Sjekker: {url[:60]}...")
    
    html = fetch_page(url)
    if not html:
        return []
    
    # Identifiser kilde
    domain = urlparse(url).netloc.lower()
    
    if 'vg.no' in domain:
        videos = extract_video_urls_vg(html, url)
    elif 'tv2.no' in domain:
        videos = extract_video_urls_tv2(html, url)
    elif 'dagbladet.no' in domain:
        videos = extract_video_urls_dagbladet(html, url)
    elif 'nrk.no' in domain:
        videos = extract_video_urls_nrk(html, url)
    elif 'nettavisen.no' in domain:
        videos = extract_video_urls_nettavisen(html, url)
    else:
        videos = extract_video_urls_generic(html, url)
    
    # Fjern duplikater
    seen = set()
    unique = []
    for v in videos:
        if v['url'] not in seen:
            seen.add(v['url'])
            unique.append(v)
    
    return unique

def main():
    if len(sys.argv) < 2:
        print("Bruk: extract-video-urls.py <artikkel-url>")
        print("")
        print("Støttede kilder:")
        print("  - vg.no")
        print("  - tv2.no")
        print("  - dagbladet.no")
        print("  - nrk.no")
        print("  - nettavisen.no")
        print("  - + generisk YouTube")
        sys.exit(1)
    
    url = sys.argv[1]
    
    print("=" * 60)
    print("🎬 VIDEO-URL EKSTRAHERING")
    print("=" * 60)
    print("")
    
    videos = extract_video_urls(url)
    
    if videos:
        print(f"\n✅ Fant {len(videos)} video(er):")
        print("")
        for i, video in enumerate(videos, 1):
            print(f"{i}. Type: {video['type']}")
            print(f"   URL: {video['url']}")
            if 'id' in video:
                print(f"   ID: {video['id']}")
            print("")
        
        # Lagre til fil
        output = {
            'source_url': url,
            'videos': videos
        }
        
        with open('/tmp/extracted-videos.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print("💾 Lagret til /tmp/extracted-videos.json")
        
    else:
        print("\n⚠️  Ingen videoer funnet")
        print("   (Siden kan ha videoer som krever JavaScript for å laste)")
    
    return 0 if videos else 1

if __name__ == '__main__':
    sys.exit(main())
