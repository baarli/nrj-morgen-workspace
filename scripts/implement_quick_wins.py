#!/usr/bin/env python3
"""
🚀 NRJ Quick Wins - Implementer raske forbedringer
"""

import os
from pathlib import Path

workspace = Path('/root/.openclaw/workspace')
implementations = []

# 1. YouTube Upload Script
youtube_script = '''#!/bin/bash
# 📺 YouTube Upload Script for NRJ Morgen
set -e

EPISODE_FILE="$1"
if [ -z "$EPISODE_FILE" ]; then
    echo "Usage: $0 <episode-file.mp3>"
    exit 1
fi

EPISODE_NAME=$(basename "$EPISODE_FILE" .mp3)
echo "🎬 Forbereder YouTube-opplasting: $EPISODE_NAME"

# Konverter til video
VIDEO_FILE="${EPISODE_FILE%.mp3}.mp4"
if [ ! -f "$VIDEO_FILE" ]; then
    echo "🎵 Konverterer til video..."
    ffmpeg -i "$EPISODE_FILE" -filter_complex "[0:a]showwaves=s=1280x720:mode=cline:colors=white|white,format=yuv420p[v]" -map "[v]" -map 0:a -c:v libx264 -c:a aac -b:a 192k "$VIDEO_FILE" -y 2>/dev/null
fi

echo "✅ Klar for YouTube: $VIDEO_FILE"
echo "⚠️  Last opp manuelt til: https://studio.youtube.com"
'''

youtube_path = workspace / 'scripts' / 'youtube-upload.sh'
with open(youtube_path, 'w') as f:
    f.write(youtube_script)
os.chmod(youtube_path, 0o755)
implementations.append("✅ YouTube upload script")

# 2. Social Media Poster
social_script = '''#!/usr/bin/env python3
"""
📱 Social Media Poster for NRJ Morgen
"""
import sys
from pathlib import Path

def post_clips(clip_dir):
    clips = list(Path(clip_dir).glob('*.mp3'))
    print(f"📱 Found {len(clips)} clips")
    
    for clip in clips:
        video = clip.with_suffix('.mp4')
        if not video.exists():
            print(f"🎬 Converting {clip.name}...")
            import os
            os.system(f'ffmpeg -i "{clip}" -filter_complex "[0:a]showwaves=s=1080x1920:mode=cline,format=yuv420p[v]" -map "[v]" -map 0:a "{video}" -y 2>/dev/null')
        print(f"✅ Ready: {video.name}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: social_media_poster.py <clip_dir>")
        sys.exit(1)
    post_clips(sys.argv[1])
'''

social_path = workspace / 'scripts' / 'social_media_poster.py'
with open(social_path, 'w') as f:
    f.write(social_script)
os.chmod(social_path, 0o755)
implementations.append("✅ Social media poster")

# 3. Newsletter Template
newsletter = '''# 📧 NRJ Morgen Nyhetsbrev - Uke {week}

Hei {name}!

## 🎧 Ukens Høydepunkter
{stories}

### 🎵 Ukens Låt
**{song}** - {artist}

### 🎬 Bak Kulissene
{behind}

### 📅 Kommende Gjester
{guests}

---
**Lytt live:** [NRJ Morgen](https://nrj.no) 06-10
**Podcast:** [Baarli og Benjamin](https://podcasts.apple.com/...)

Følg oss: [Instagram] [TikTok] [YouTube]
'''

newsletter_path = workspace / 'docs' / 'newsletter-template.md'
newsletter_path.parent.mkdir(parents=True, exist_ok=True)
with open(newsletter_path, 'w') as f:
    f.write(newsletter)
implementations.append("✅ Newsletter template")

# 4. Recency Scoring Module
recency_module = '''#!/usr/bin/env python3
"""
📊 Recency Scoring for Morning Routine
"""
import math
from datetime import datetime

def calculate_recency_score(published_date):
    """Calculate recency score with exponential decay"""
    try:
        pub_date = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
        now = datetime.now(pub_date.tzinfo)
        hours_old = (now - pub_date).total_seconds() / 3600
        score = 100 * math.exp(-hours_old / 24)
        return max(0, score)
    except:
        return 50

def calculate_source_authority(source):
    """Calculate source authority score"""
    authority_scores = {
        'vg.no': 100,
        'tv2.no': 95,
        'dagbladet.no': 90,
        'nrk.no': 95,
        'nettavisen.no': 80,
        'seher.no': 75,
        'dailymail.co.uk': 70,
        'tmz.com': 65,
    }
    return authority_scores.get(source, 50)
'''

recency_path = workspace / 'scripts' / 'recency_scoring.py'
with open(recency_path, 'w') as f:
    f.write(recency_module)
implementations.append("✅ Recency scoring module")

# Print results
print("=" * 60)
print("🚀 NRJ QUICK WINS - IMPLEMENTERT")
print("=" * 60)
for item in implementations:
    print(f"  {item}")
print("=" * 60)
print(f"\n✅ {len(implementations)} verktøy opprettet!")
print("\nNeste steg:")
print("  1. Kjør: bash scripts/youtube-upload.sh <episode.mp3>")
print("  2. Kjør: python3 scripts/social_media_poster.py /tmp/podcast-clips")
print("  3. Bruk: docs/newsletter-template.md for ukentlig nyhetsbrev")
print("  4. Integrer: scripts/recency_scoring.py i Morning Routine")
