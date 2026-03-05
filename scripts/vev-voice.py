#!/usr/bin/env python3
"""
Vev Voice Generator v2.0
Bruker ElevenLabs for TTS
"""
import os
import sys
import hashlib
import requests
from datetime import datetime
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"
AUDIO_DIR = f"{WORKSPACE}/brain/projects/voice-chat/audio"

# Load credentials
with open(f"{WORKSPACE}/.credentials/elevenlabs.env") as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            key, val = line.strip().split('=', 1)
            # Remove inline comments
            val = val.split('#')[0].strip()
            os.environ[key] = val

ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
VEV_VOICE_ID = os.environ.get('VEV_VOICE_ID', '21m00Tcm4TlvDq8ikWAM')
VEV_VOICE_MODEL = os.environ.get('VEV_VOICE_MODEL', 'eleven_multilingual_v2')

def ensure_dirs():
    os.makedirs(AUDIO_DIR, exist_ok=True)

def generate_voice(text, voice_id=None):
    """
    Generer TTS via ElevenLabs
    """
    ensure_dirs()
    
    voice_id = (voice_id or VEV_VOICE_ID).strip()
    text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"vev_{timestamp}_{text_hash}.mp3"
    filepath = f"{AUDIO_DIR}/{filename}"
    
    # Sjekk cache
    existing = find_existing_audio(text_hash)
    if existing:
        print(f"✅ Using cached audio: {existing}")
        return existing
    
    print(f"🎙️ Generating voice via ElevenLabs...")
    print(f"   Text: {text[:60]}...")
    
    # ElevenLabs API
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": text,
        "model_id": VEV_VOICE_MODEL,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            # Lagre audio fil
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Generated: {filepath}")
            print(f"   Size: {len(response.content)} bytes")
            return filepath
        else:
            print(f"❌ ElevenLabs error: {response.status_code}")
            print(f"   {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def find_existing_audio(text_hash):
    """Finn eksisterende audio for samme tekst"""
    for f in Path(AUDIO_DIR).glob(f"*_{text_hash}.mp3"):
        return str(f)
    return None

def list_voices():
    """List available ElevenLabs voices"""
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": ELEVENLABS_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            voices = response.json().get('voices', [])
            print("🎙️ Available voices:")
            for v in voices[:10]:
                print(f"   {v['voice_id']}: {v['name']} ({v.get('category', 'unknown')})")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: vev-voice 'text to speak'")
        print("       vev-voice --list-voices")
        sys.exit(1)
    
    if sys.argv[1] == '--list-voices':
        list_voices()
        sys.exit(0)
    
    text = " ".join(sys.argv[1:])
    
    print("=" * 60)
    print("🎙️ VEV VOICE GENERATOR v2.0 (ElevenLabs)")
    print("=" * 60)
    print()
    
    filepath = generate_voice(text)
    
    if filepath:
        print()
        print("=" * 60)
        print(f"✅ Audio ready: {filepath}")
        print("=" * 60)
        
        # Spill av hvis mpg123 er tilgjengelig
        if os.system("which mpg123 > /dev/null 2>&1") == 0:
            print("🔊 Playing audio...")
            os.system(f"mpg123 -q '{filepath}'")
    else:
        print()
        print("❌ Failed to generate audio")

if __name__ == "__main__":
    main()
