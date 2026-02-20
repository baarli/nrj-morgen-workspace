#!/usr/bin/env python3
# /root/.openclaw/workspace/scripts/video-to-audio-pipeline.py
# Video-til-lyd pipeline for NRJ Morgen
# Laster ned video, ekstraherer lyd, finner beste sitater, kliper ut, laster opp

import os
import sys
import json
import re
import subprocess
import tempfile
import urllib.request
from pathlib import Path
from datetime import datetime

# Konfigurasjon
WORKSPACE = "/root/.openclaw/workspace"
CREDENTIALS = f"{WORKSPACE}/.credentials/nrj-morgen.env"
DOWNLOAD_DIR = f"{WORKSPACE}/downloads"
OUTPUT_DIR = f"{WORKSPACE}/audio-clips"

def load_credentials():
    """Last API-nøkler fra credentials-fil"""
    creds = {}
    if os.path.exists(CREDENTIALS):
        with open(CREDENTIALS, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    value = value.strip('"').strip("'")
                    creds[key] = value
    return creds

def download_video(url, output_path):
    """Last ned video med yt-dlp"""
    print(f"  📥 Laster ned video...")
    
    cmd = [
        'yt-dlp',
        '--no-playlist',
        '--format', 'best[height<=720]',  # Max 720p for rask nedlasting
        '--output', output_path,
        '--quiet',
        '--no-warnings',
        url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            # Finn faktisk filnavn
            base = os.path.splitext(output_path)[0]
            for ext in ['.mp4', '.webm', '.mkv']:
                if os.path.exists(base + ext):
                    return base + ext
        else:
            print(f"  ⚠️  Nedlasting feilet: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        print("  ⚠️  Nedlasting timeout")
        return None
    except Exception as e:
        print(f"  ⚠️  Feil: {e}")
        return None
    
    return None

def extract_audio(video_path, audio_path):
    """Ekstraher lyd fra video med ffmpeg"""
    print(f"  🎵 Ekstraherer lyd...")
    
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vn',  # Ingen video
        '-acodec', 'libmp3lame',
        '-ar', '44100',
        '-ac', '2',
        '-b:a', '192k',
        '-y',  # Overskriv
        audio_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and os.path.exists(audio_path):
            return True
        else:
            print(f"  ⚠️  FFmpeg feil")
            return False
    except Exception as e:
        print(f"  ⚠️  Feil: {e}")
        return False

def transcribe_audio(audio_path):
    """Transkriber lyd med whisper"""
    print(f"  📝 Transkriberer...")
    
    # Bruk whisper via subprocess
    cmd = [
        'whisper',
        audio_path,
        '--model', 'base',  # Rask modell
        '--language', 'no',
        '--output_format', 'json',
        '--output_dir', os.path.dirname(audio_path),
        '--verbose', 'False'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        # Finn transkripsjonsfil
        base = os.path.splitext(audio_path)[0]
        transcript_path = base + '.json'
        
        if os.path.exists(transcript_path):
            with open(transcript_path, 'r') as f:
                return json.load(f)
        else:
            print("  ⚠️  Ingen transkripsjon funnet")
            return None
            
    except subprocess.TimeoutExpired:
        print("  ⚠️  Transkripsjon timeout")
        return None
    except Exception as e:
        print(f"  ⚠️  Feil: {e}")
        return None

def find_best_quotes(transcript, num_quotes=3):
    """Finn beste sitater fra transkripsjon"""
    print(f"  💎 Finner beste sitater...")
    
    if not transcript or 'segments' not in transcript:
        return []
    
    segments = transcript['segments']
    quotes = []
    
    # Enkel algoritme: finn segmenter med følelsesladde ord eller viktige utsagn
    keywords = ['sjokk', 'raser', 'avslører', 'bekrefter', 'død', 'skandale', 
                'kjærlighet', 'brudd', 'gravid', 'syk', 'vold', 'politi',
                'arrestert', 'løslatt', 'dom', 'sak', 'rettssak']
    
    for segment in segments:
        text = segment.get('text', '').lower()
        score = 0
        
        # Sjekk for nøkkelord
        for keyword in keywords:
            if keyword in text:
                score += 2
        
        # Lengde-faktor (ikke for kort, ikke for langt)
        duration = segment.get('end', 0) - segment.get('start', 0)
        if 5 <= duration <= 30:  # 5-30 sekunder
            score += 1
        
        # Første segmenter ofte intro (lavere score)
        if segment.get('start', 0) < 10:
            score -= 1
        
        if score > 0:
            quotes.append({
                'text': segment['text'].strip(),
                'start': segment['start'],
                'end': segment['end'],
                'score': score
            })
    
    # Sorter etter score
    quotes.sort(key=lambda x: x['score'], reverse=True)
    
    return quotes[:num_quotes]

def clip_audio(audio_path, output_path, start_time, end_time):
    """Klipp ut del av lydfil"""
    duration = end_time - start_time
    print(f"  ✂️  Kliper ut {duration:.1f}s...")
    
    cmd = [
        'ffmpeg',
        '-i', audio_path,
        '-ss', str(start_time),
        '-t', str(duration),
        '-c', 'copy',
        '-y',
        output_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0 and os.path.exists(output_path)
    except Exception as e:
        print(f"  ⚠️  Feil: {e}")
        return False

def upload_to_content_hub(file_path, title, description, agenda_item_id=None):
    """Last opp til content-hub (foreløpig: lagre lokalt og logg)"""
    print(f"  ☁️  Opplasting til content-hub...")
    
    # TODO: Implementer faktisk API-kall til content-hub
    # Foreløpig: kopier til output-mappe
    
    filename = os.path.basename(file_path)
    output_path = os.path.join(OUTPUT_DIR, filename)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Kopier fil
    import shutil
    shutil.copy2(file_path, output_path)
    
    # Lag metadata
    meta = {
        'filename': filename,
        'title': title,
        'description': description,
        'created_at': datetime.now().isoformat(),
        'agenda_item_id': agenda_item_id
    }
    
    meta_path = output_path + '.json'
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)
    
    print(f"  ✅ Lagret: {output_path}")
    return output_path

def process_video(url, article_title, article_source, agenda_item_id=None):
    """Prosesser én video gjennom hele pipelinen"""
    
    print(f"\n🎬 Prosesserer: {article_title[:50]}...")
    print(f"   URL: {url[:60]}...")
    
    # Opprett temp-mappe
    with tempfile.TemporaryDirectory() as tmpdir:
        # Steg 1: Last ned video
        video_path = os.path.join(tmpdir, 'video')
        video_file = download_video(url, video_path)
        
        if not video_file:
            print("  ❌ Nedlasting feilet")
            return False
        
        print(f"  ✅ Video lastet ned")
        
        # Steg 2: Ekstraher lyd
        audio_path = os.path.join(tmpdir, 'audio.mp3')
        if not extract_audio(video_file, audio_path):
            print("  ❌ Lyd-ekstrahering feilet")
            return False
        
        print(f"  ✅ Lyd ekstrahert")
        
        # Steg 3: Transkriber
        transcript = transcribe_audio(audio_path)
        
        if not transcript:
            # Hvis transkripsjon feiler, bruk hele lyden
            print("  ⚠️  Bruker hele lyden (ingen transkripsjon)")
            clip_path = audio_path
            quote_text = "[Ingen transkripsjon]"
        else:
            print(f"  ✅ Transkribert")
            
            # Steg 4: Finn beste sitater
            quotes = find_best_quotes(transcript)
            
            if not quotes:
                print("  ⚠️  Ingen gode sitater funnet, bruker hele lyden")
                clip_path = audio_path
                quote_text = "[Ingen sitater funnet]"
            else:
                # Steg 5: Klipp ut beste sitat
                best_quote = quotes[0]
                clip_path = os.path.join(tmpdir, 'clip.mp3')
                
                if clip_audio(audio_path, clip_path, best_quote['start'], best_quote['end']):
                    quote_text = best_quote['text']
                    print(f"  ✅ Sitat klippet ut ({best_quote['end'] - best_quote['start']:.1f}s)")
                else:
                    clip_path = audio_path
                    quote_text = best_quote['text']
        
        # Steg 6: Last opp
        safe_title = re.sub(r'[^\w\s-]', '', article_title)[:40]
        output_filename = f"{datetime.now().strftime('%Y%m%d')}_{safe_title.replace(' ', '_')}.mp3"
        
        title = f"Sitat: {quote_text[:60]}..."
        description = f"Fra: {article_source} | Sak: {article_title}"
        
        upload_path = upload_to_content_hub(clip_path, title, description, agenda_item_id)
        
        if upload_path:
            print(f"  ✅ Ferdig!")
            return True
        else:
            print(f"  ❌ Opplasting feilet")
            return False

def main():
    """Hovedfunksjon - kan kalles med URL eller prosesser dagens saker"""
    
    if len(sys.argv) > 1:
        # Prosesser spesifikk URL
        url = sys.argv[1]
        title = sys.argv[2] if len(sys.argv) > 2 else "Ukjent tittel"
        source = sys.argv[3] if len(sys.argv) > 3 else "Ukjent kilde"
        
        success = process_video(url, title, source)
        sys.exit(0 if success else 1)
    
    else:
        # Prosesser dagens saker fra Supabase
        print("🎙️  NRJ MORGEN – VIDEO-TIL-LYD PIPELINE")
        print("=" * 60)
        
        # TODO: Hent saker med video fra Supabase
        # For nå: test med en eksempel-URL
        
        print("\n⚠️  Ingen URL gitt. Bruk:")
        print(f"  {sys.argv[0]} <video-url> [tittel] [kilde]")
        print("")
        print("Eksempel:")
        print(f'  {sys.argv[0]} "https://www.tv2.no/video/nyheter/..." "Tittel" "TV2"')
        
        sys.exit(1)

if __name__ == '__main__':
    main()
