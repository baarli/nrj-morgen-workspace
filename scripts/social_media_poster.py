#!/usr/bin/env python3
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
