#!/usr/bin/env python3
"""
Daglig podkast-klipp generator - BRUKER SKILLS_LIB
For Baarli og Benjamin + NRJ Morgen Podkast

Skills brukt:
- podcast_clipper (hente episoder, lage klipp)
- perfect_clip_finder (finne beste øyeblikk)
- audio_producer (konvertere til video)
- email_sender (sende e-post)
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Legg til skills_lib i path
sys.path.insert(0, '/root/.openclaw')

from skills_lib import PodcastClipper, PerfectClipFinder, AudioProducer, EmailSender


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


def process_podcast(podcast_key: str, processed: dict, use_perfect_clip: bool = True):
    """Prosesser en podcast med SKILLS"""
    config = PODCASTS[podcast_key]
    print(f"\n{config['emoji']} Prosesserer: {config['name']}")
    
    # Sjekk om allerede prosessert i dag
    today = datetime.now().strftime('%Y-%m-%d')
    cache_key = f"{podcast_key}_{today}"
    
    if cache_key in processed:
        print(f"   ⚠️  Allerede prosessert i dag")
        return None
    
    # SKILL: PodcastClipper - Hent episode
    # Sørg for at work dir eksisterer
    (WORK_DIR / today / podcast_key).mkdir(parents=True, exist_ok=True)
    clipper = PodcastClipper(cache_dir=str(WORK_DIR / today / podcast_key))
    episode = clipper.get_latest_episode(config['rss'])
    
    if not episode:
        print(f"   ❌ Kunne ikke hente episode")
        return None
    
    episode_title = episode['title']
    print(f"   📥 Episode: {episode_title[:60]}...")
    
    # Sjekk om denne episoden er prosessert
    import re
    episode_id = re.sub(r'[^\w]', '_', episode_title[:30])
    if episode_id in processed.get(podcast_key, []):
        print(f"   ⚠️  Episode allerede prosessert")
        return None
    
    # Last ned episode
    audio_path = clipper.download_episode(episode, quiet=True)
    if not audio_path:
        print(f"   ❌ Kunne ikke laste ned episode")
        return None
    
    print(f"   ✅ Nedlastet")
    
    # SKILL: PerfectClipFinder - Finn beste klipp
    clips = []
    
    if use_perfect_clip:
        print(f"   🔍 Finner PERFECT klipp...")
        finder = PerfectClipFinder(audio_path)
        perfect_clips = finder.find_perfect_clips(num_clips=3)
        
        for i, clip_info in enumerate(perfect_clips):
            start = clip_info['start']
            end = clip_info['end']
            duration = clip_info['duration']
            
            # SKILL: PodcastClipper - Lag klipp
            clip_audio = str(WORK_DIR / today / podcast_key / f"clip_{i}_perfect.mp3")
            clip_video = str(WORK_DIR / today / podcast_key / f"clip_{i}_perfect.mp4")
            
            if clipper.create_clip(audio_path, start, end, clip_audio):
                # SKILL: AudioProducer - Lag video
                producer = AudioProducer()
                if producer.create_social_media_video(clip_audio, clip_video):
                    clips.append({
                        'type': 'perfect',
                        'start': start,
                        'end': end,
                        'duration': duration,
                        'score': round(clip_info['total_score'], 1),
                        'audio_energy': round(clip_info['audio_energy'], 1),
                        'laughter_detection': round(clip_info['laughter_detection'], 1),
                        'conversation_pace': round(clip_info['conversation_pace'], 1),
                        'emotional_intensity': round(clip_info['emotional_intensity'], 1),
                        'viral_potential': round(clip_info['viral_potential'], 1),
                        'audio_path': clip_audio,
                        'video_path': clip_video
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
            clip_audio = str(WORK_DIR / today / podcast_key / f"clip_{i}_{cfg['type']}.mp3")
            clip_video = str(WORK_DIR / today / podcast_key / f"clip_{i}_{cfg['type']}.mp4")
            
            if clipper.create_clip(audio_path, cfg['start'], cfg['start'] + cfg['duration'], clip_audio):
                producer = AudioProducer()
                if producer.create_social_media_video(clip_audio, clip_video):
                    clips.append({
                        'type': cfg['type'],
                        'start': cfg['start'],
                        'end': cfg['start'] + cfg['duration'],
                        'duration': cfg['duration'],
                        'score': 70,
                        'video_path': clip_video
                    })
    
    # Marker som prosessert
    if podcast_key not in processed:
        processed[podcast_key] = []
    processed[podcast_key].append(episode_id)
    processed[cache_key] = True
    save_processed(processed)
    
    return {
        "podcast_name": config['name'],
        "episode_title": episode_title,
        "clips": clips
    }


def main():
    parser = argparse.ArgumentParser(
        description='Daglig podkast-klipp generator - BRUKER SKILLS_LIB'
    )
    parser.add_argument('--email', default='niklasbaarli@gmail.com',
                        help='Mottaker e-post')
    parser.add_argument('--send-email', action='store_true',
                        help='Send e-post med klipp')
    parser.add_argument('--no-perfect-clip', action='store_true',
                        help='Bruk faste tidssegmenter (ikke perfect clip)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🎧 DAGLIG PODKAST KLIPP-GENERATOR")
    print("   MED SKILLS LIB")
    print("=" * 60)
    print(f"Dato: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Mottaker: {args.email}")
    print(f"Perfect Clip: {'✅ JA' if not args.no_perfect_clip else '❌ NEI'}")
    print("")
    print("Skills brukt:")
    print("  📦 podcast_clipper - Hente episoder")
    print("  🎯 perfect_clip_finder - Finne beste klipp")
    print("  🎵 audio_producer - Lage video")
    print("  📧 email_sender - Sende e-post")
    
    # Last processed cache
    processed = load_processed()
    
    # Prosesser begge podcastene
    clips_info = {}
    
    for podcast_key in ["baarli", "nrj"]:
        result = process_podcast(podcast_key, processed,
                                 use_perfect_clip=not args.no_perfect_clip)
        if result:
            clips_info[podcast_key] = result
    
    if not clips_info:
        print("\n⚠️  Ingen nye episoder å prosessere")
        return
    
    # SKILL: EmailSender - Send e-post
    if args.send_email:
        print(f"\n📧 Sender e-post til {args.email}...")
        sender = EmailSender()
        if sender.send_podcast_clips(args.email, clips_info):
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
