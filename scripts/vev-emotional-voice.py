#!/usr/bin/env python3
"""
Vev Emotional Voice Generator
Tilpatter stemme basert på kontekst og emosjon
"""
import os
import requests
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"
AUDIO_DIR = f"{WORKSPACE}/brain/projects/voice-chat/audio-emotional"

# Load credentials
with open(f"{WORKSPACE}/.credentials/elevenlabs.env") as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            key, val = line.strip().split('=', 1)
            val = val.split('#')[0].strip()
            os.environ[key] = val

ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
VEV_VOICE_ID = os.environ.get('VEV_VOICE_ID', '4kCDY3HJwvO7Zp3con83')

# Emosjonelle innstillinger
EMOTIONS = {
    'happy': {
        'stability': 0.35,
        'similarity_boost': 0.85,
        'style': 0.6,
        'use_speaker_boost': True
    },
    'curious': {
        'stability': 0.45,
        'similarity_boost': 0.75,
        'style': 0.4,
        'use_speaker_boost': True
    },
    'serious': {
        'stability': 0.65,
        'similarity_boost': 0.70,
        'style': 0.2,
        'use_speaker_boost': False
    },
    'excited': {
        'stability': 0.25,
        'similarity_boost': 0.90,
        'style': 0.8,
        'use_speaker_boost': True
    },
    'calm': {
        'stability': 0.70,
        'similarity_boost': 0.65,
        'style': 0.1,
        'use_speaker_boost': False
    }
}

def detect_emotion(text, context=None):
    """Detekter emosjon basert på tekst"""
    text_lower = text.lower()
    
    # Excited
    if any(word in text_lower for word in ['fantastisk', 'utrolig', 'wow', 'amazing', 'great', 'elsker']):
        return 'excited'
    
    # Happy
    if any(word in text_lower for word in ['bra', 'godt', 'glad', 'happy', 'fine', 'supert']):
        return 'happy'
    
    # Serious
    if any(word in text_lower for word in ['viktig', 'alvorlig', 'problem', 'feil', 'error', 'serious']):
        return 'serious'
    
    # Calm
    if any(word in text_lower for word in ['rolig', 'avslappet', 'calm', 'peaceful', 'quiet']):
        return 'calm'
    
    # Default: curious
    return 'curious'

def generate_emotional_tts(text, emotion=None, context=None):
    """Generer TTS med emosjonell tilpasning"""
    Path(AUDIO_DIR).mkdir(parents=True, exist_ok=True)
    
    # Detekter emosjon hvis ikke spesifisert
    if not emotion:
        emotion = detect_emotion(text, context)
    
    settings = EMOTIONS.get(emotion, EMOTIONS['curious'])
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VEV_VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": text,
        "model_id": "eleven_flash_v2_5",
        "voice_settings": {
            "stability": settings['stability'],
            "similarity_boost": settings['similarity_boost'],
            "style": settings['style'],
            "use_speaker_boost": settings['use_speaker_boost']
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            import hashlib
            text_hash = hashlib.md5(f"{text}{emotion}".encode()).hexdigest()[:8]
            filepath = f"{AUDIO_DIR}/emotional_{emotion}_{text_hash}.mp3"
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return filepath, emotion
    except Exception as e:
        print(f"Error: {e}")
    
    return None, emotion

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: vev-emotional-voice 'text' [emotion]")
        print(f"Emotions: {', '.join(EMOTIONS.keys())}")
        sys.exit(1)
    
    text = sys.argv[1]
    emotion = sys.argv[2] if len(sys.argv) > 2 else None
    
    print("=" * 60)
    print("🎭 VEV EMOTIONAL VOICE GENERATOR")
    print("=" * 60)
    print(f"Text: {text}")
    
    if emotion:
        print(f"Emotion: {emotion}")
    else:
        detected = detect_emotion(text)
        print(f"Detected emotion: {detected}")
        emotion = detected
    
    print(f"Settings: {EMOTIONS[emotion]}")
    print()
    
    filepath, used_emotion = generate_emotional_tts(text, emotion)
    
    if filepath:
        print(f"✅ Generated: {filepath}")
        print(f"   Emotion: {used_emotion}")
        
        # Play if mpg123 available
        if os.system("which mpg123 > /dev/null 2>&1") == 0:
            print("🔊 Playing...")
            os.system(f"mpg123 -q '{filepath}'")
    else:
        print("❌ Failed to generate")

if __name__ == "__main__":
    main()
