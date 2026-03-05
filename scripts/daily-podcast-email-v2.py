#!/usr/bin/env python3
"""
Daglig podkast-klipp generator med PERFECT CLIP FINDER
For Baarli og Benjamin + NRJ Morgen Podkast
"""

import argparse
import json
import os
import re
import smtplib
import sys
from datetime import datetime
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET

# Import perfect clip finder
sys.path.insert(0, '/root/.openclaw/workspace/scripts')
try:
    from perfect_clip_finder import PerfectClipFinder
    HAS_PERFECT_CLIP = True
except ImportError:
    HAS_PERFECT_CLIP = False
    print("⚠️  Perfect Clip Finder ikke tilgjengelig")

# Konfigurasjon
PODCASTS = {
    "baarli": {
        "name": "Baarli og Benjamin går i terapi",
        "rss": "https://rss.podplaystudio.com/4035.xml",
        "emoji": "🎙️"
    },
    "nrj": {
        "name": "NRJ Morgen Podkast", 
        "rss": "https://rss.podplaystudio.com/3873.xml",
        "emoji": "📻"
    }
}

WORK_DIR = Path("/tmp/podcast-daily")
CACHE_FILE = WORK_DIR / "processed.json"

def load_processed():
    """Last liste over allerede prosesserte episoder"""
    if CACHE_FILE.exists():
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_processed(processed):
    """Lagre liste over prosesserte episoder"""
    CACHE_FILE.parent.mkdir(exist_ok=True)
    with open(CACHE_FILE, 'w') as f:
        json.dump(processed, f, indent=2)

def fetch_rss(rss_url):
    """Hent og parse RSS-feed"""
    try:
        with urllib.request.urlopen(rss_url, timeout=30) as response:
            xml_content = response.read()
        
        root = ET.fromstring(xml_content)
        
        episodes = []
        for item in root.findall('.//item'):
            title = item.find('title')
            pub_date = item.find('pubDate')
            enclosure = item.find('enclosure')
            
            episode = {
                'title': title.text.strip() if title is not None and title.text else 'Ukjent',
                'pub_date': pub_date.text if pub_date is not None else '',
                'audio_url': enclosure.get('url') if enclosure is not None else ''
            }
            episodes.append(episode)
        
        return episodes
    except Exception as e:
        print(f"❌ Feil ved henting av RSS: {e}")
        return []

def download_episode(audio_url, output_path):
    """Last ned episode"""
    try:
        urllib.request.urlretrieve(audio_url, output_path)
        return True
    except Exception as e:
        print(f"❌ Feil ved nedlasting: {e}")
        return False

def create_clip(input_path, output_path, start, duration):
    """Lag klipp med ffmpeg"""
    cmd = f'ffmpeg -y -i "{input_path}" -ss {start} -t {duration} -c copy "{output_path}"'
    result = os.system(cmd)
    return result == 0

def create_video(input_path, output_path):
    """Konverter til videoformat (1080x1920)"""
    cmd = f'ffmpeg -y -i "{input_path}" -f lavfi -i "color=c=#1a1a2e:s=1080x1920:d=30" -shortest -c:v libx264 -c:a aac -b:a 128k -pix_fmt yuv420p "{output_path}"'
    result = os.system(cmd)
    return result == 0

def send_email_with_clips(recipient, clips_info, smtp_host="smtp.gmail.com", smtp_port=587, username=None, password=None):
    """Send e-post med klipp vedlegg"""
    
    # Les credentials fra env eller fil
    if not username or not password:
        cred_file = Path("/root/.openclaw/workspace/.credentials/nrj-morgen.env")
        if cred_file.exists():
            with open(cred_file) as f:
                for line in f:
                    if line.startswith("GMAIL_APP_PASSWORD="):
                        password = line.strip().split("=", 1)[1].strip('"')
                    if line.startswith("GMAIL_USER="):
                        username = line.strip().split("=", 1)[1].strip('"')
    
    if not username or not password:
        print("❌ Mangler e-post credentials")
        return False
    
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = recipient
    msg['Subject'] = f"🎧 Dagens Podkast Klipp - {datetime.now().strftime('%d.%m.%Y')}"
    
    # E-post body
    body = f"""
Hei!

Her er dagens PERFECT podkast-klipp klar for sosiale medier:

"""
    
    for podcast_key, info in clips_info.items():
        podcast_name = PODCASTS[podcast_key]["name"]
        emoji = PODCASTS[podcast_key]["emoji"]
        body += f"\n{emoji} {podcast_name}\n"
        body += f"Episode: {info['episode_title']}\n"
        body += f"Klipp generert: {len(info['clips'])}\n\n"
        
        for i, clip in enumerate(info['clips'], 1):
            body += f"  🎯 KLIPP #{i} (Score: {clip.get('score', 'N/A')}/100)\n"
            body += f"     Tid: {clip['start']}s - {clip['end']}s ({clip['duration']}s)\n"
            body += f"     Parametre:\n"
            body += f"        🔊 Audio energi:      {clip.get('audio_energy', 'N/A')}/100\n"
            body += f"        😂 Latter-deteksjon:  {clip.get('laughter_detection', 'N/A')}/100\n"
            body += f"        💬 Samtaletempo:      {clip.get('conversation_pace', 'N/A')}/100\n"
            body += f"        ❤️  Emosjonell intens: {clip.get('emotional_intensity', 'N/A')}/100\n"
            body += f"        🚀 Viral potensial:   {clip.get('viral_potential', 'N/A')}/100\n"
            body += f"\n"
    
    body += f"""

💡 Tips for posting:
- Legg til tekst-overlay i Instagram/TikTok-appen
- Bruk relevante hashtags: #podcast #norge #humor #radio
- Post på optimal tid: 07:00, 12:00 eller 19:00

Ha en fin dag!
"""
    
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # Legg til vedlegg
    for podcast_key, info in clips_info.items():
        for i, clip in enumerate(info['clips']):
            video_path = clip['video_path']
            if os.path.exists(video_path):
                with open(video_path, 'rb') as f:
                    attachment = MIMEBase('application', 'octet-stream')
                    attachment.set_payload(f.read())
                
                from email import encoders
                encoders.encode_base64(attachment)
                
                filename = f"{podcast_key}_clip{i+1}_{clip.get('type', 'perfect')}.mp4"
                attachment.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                msg.attach(attachment)
    
    # Send e-post
    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
        server.quit()
        print(f"✅ E-post sendt til {recipient}")
        return True
    except Exception as e:
        print(f"❌ Feil ved sending av e-post: {e}")
        return False

def process_podcast(podcast_key, processed, use_perfect_clip=True):
    """Prosesser en podcast med PERFECT CLIP FINDER"""
    config = PODCASTS[podcast_key]
    print(f"\n{config['emoji']} Prosesserer: {config['name']}")
    
    # Sjekk om allerede prosessert i dag
    today = datetime.now().strftime('%Y-%m-%d')
    cache_key = f"{podcast_key}_{today}"
    
    if cache_key in processed:
        print(f"   ⚠️  Allerede prosessert i dag")
        return None
    
    # Hent episoder
    episodes = fetch_rss(config['rss'])
    if not episodes:
        return None
    
    latest = episodes[0]
    episode_title = latest['title']
    
    # Sjekk om denne episoden er prosessert
    episode_id = re.sub(r'[^\w]', '_', episode_title[:30])
    if episode_id in processed.get(podcast_key, []):
        print(f"   ⚠️  Episode allerede prosessert: {episode_title[:50]}...")
        return None
    
    print(f"   📥 Episode: {episode_title[:60]}...")
    
    # Opprett mappe for dagens klipp
    today_dir = WORK_DIR / today / podcast_key
    today_dir.mkdir(parents=True, exist_ok=True)
    
    # Last ned episode
    safe_title = re.sub(r'[^\w\s-]', '', episode_title).strip().replace(' ', '_')[:30]
    audio_path = today_dir / f"{safe_title}.mp3"
    
    if not download_episode(latest['audio_url'], audio_path):
        return None
    
    print(f"   ✅ Nedlastet: {audio_path.name}")
    
    clips = []
    
    if use_perfect_clip and HAS_PERFECT_CLIP:
        # Bruk PERFECT CLIP FINDER
        print(f"   🔍 Finner perfekte klipp...")
        finder = PerfectClipFinder(str(audio_path))
        perfect_clips = finder.find_perfect_clips(num_clips=3, min_duration=25, max_duration=35)
        
        for i, clip_info in enumerate(perfect_clips):
            start = clip_info['start']
            duration = clip_info['duration']
            clip_audio = today_dir / f"clip_{i}_perfect.mp3"
            clip_video = today_dir / f"clip_{i}_perfect.mp4"
            
            if create_clip(audio_path, clip_audio, start, duration):
                if create_video(clip_audio, clip_video):
                    clips.append({
                        'type': 'perfect',
                        'start': start,
                        'end': clip_info['end'],
                        'duration': duration,
                        'score': round(clip_info['total_score'], 1),
                        'audio_energy': round(clip_info['audio_energy'], 1),
                        'laughter_detection': round(clip_info['laughter_detection'], 1),
                        'conversation_pace': round(clip_info['conversation_pace'], 1),
                        'emotional_intensity': round(clip_info['emotional_intensity'], 1),
                        'viral_potential': round(clip_info['viral_potential'], 1),
                        'audio_path': str(clip_audio),
                        'video_path': str(clip_video)
                    })
                    print(f"   ✅ Perfect Clip {i+1}: {start}s (Score: {clip_info['total_score']:.1f})")
    else:
        # Fallback: faste tidssegmenter
        clip_configs = [
            {"start": 120, "duration": 30, "type": "laughter"},
            {"start": 450, "duration": 30, "type": "conversation"},
            {"start": 890, "duration": 30, "type": "reaction"}
        ]
        
        for i, cfg in enumerate(clip_configs):
            clip_audio = today_dir / f"clip_{i}_{cfg['type']}.mp3"
            clip_video = today_dir / f"clip_{i}_{cfg['type']}.mp4"
            
            if create_clip(audio_path, clip_audio, cfg['start'], cfg['duration']):
                if create_video(clip_audio, clip_video):
                    clips.append({
                        'type': cfg['type'],
                        'start': cfg['start'],
                        'end': cfg['start'] + cfg['duration'],
                        'duration': cfg['duration'],
                        'score': 70,
                        'audio_path': str(clip_audio),
                        'video_path': str(clip_video)
                    })
                    print(f"   ✅ Klipp {i+1}: {cfg['type']} ({cfg['start']}s - {cfg['start']+cfg['duration']}s)")
    
    # Marker som prosessert
    if podcast_key not in processed:
        processed[podcast_key] = []
    processed[podcast_key].append(episode_id)
    processed[cache_key] = True
    save_processed(processed)
    
    return {
        "episode_title": episode_title,
        "clips": clips
    }

def main():
    parser = argparse.ArgumentParser(description='Daglig podkast-klipp generator med PERFECT CLIP FINDER')
    parser.add_argument('--email', default='niklasbaarli@gmail.com', help='Mottaker e-post')
    parser.add_argument('--send-email', action='store_true', help='Send e-post med klipp')
    parser.add_argument('--no-perfect-clip', action='store_true', help='Bruk faste tidssegmenter (ikke perfect clip)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🎧 DAGLIG PODKAST KLIPP-GENERATOR")
    print("   MED PERFECT CLIP FINDER")
    print("=" * 60)
    print(f"Dato: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Mottaker: {args.email}")
    print(f"Perfect Clip: {'✅ JA' if not args.no_perfect_clip else '❌ NEI'}")
    
    # Last processed cache
    processed = load_processed()
    
    # Prosesser begge podcastene
    clips_info = {}
    
    for podcast_key in ["baarli", "nrj"]:
        result = process_podcast(podcast_key, processed, use_perfect_clip=not args.no_perfect_clip)
        if result:
            clips_info[podcast_key] = result
    
    if not clips_info:
        print("\n⚠️  Ingen nye episoder å prosessere")
        return
    
    # Send e-post
    if args.send_email:
        print(f"\n📧 Sender e-post til {args.email}...")
        if send_email_with_clips(args.email, clips_info):
            print("✅ E-post sendt!")
        else:
            print("❌ Kunne ikke sende e-post")
    else:
        print("\n📧 E-post ikke sendt (bruk --send-email for å sende)")
    
    print("\n" + "=" * 60)
    print("✅ FERDIG")
    print("=" * 60)

if __name__ == '__main__':
    main()
