#!/usr/bin/env python3
"""
Vev Telegram Voice Sender
Sender talemeldinger via Telegram
"""
import os
import sys
import requests
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"
AUDIO_DIR = f"{WORKSPACE}/brain/projects/voice-chat/audio"

# Load credentials
with open(f"{WORKSPACE}/.credentials/telegram-bot.env") as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            key, val = line.strip().split('=', 1)
            os.environ[key] = val

with open(f"{WORKSPACE}/.credentials/elevenlabs.env") as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            key, val = line.strip().split('=', 1)
            val = val.split('#')[0].strip()
            os.environ[key] = val

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
VEV_VOICE_ID = os.environ.get('VEV_VOICE_ID', 'JBFqnCBsd6RMkjVDRZzb')
VEV_VOICE_MODEL = os.environ.get('VEV_VOICE_MODEL', 'eleven_flash_v2_5')

def generate_tts(text):
    """Generate TTS via ElevenLabs"""
    import hashlib
    text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
    
    filepath = f"{AUDIO_DIR}/telegram_{text_hash}.mp3"
    
    # Check cache
    if Path(filepath).exists():
        print(f"✅ Using cached audio")
        return filepath
    
    print(f"🎙️ Generating TTS...")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VEV_VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": text,
        "model_id": VEV_VOICE_MODEL,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            Path(AUDIO_DIR).mkdir(parents=True, exist_ok=True)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"✅ Generated: {len(response.content)} bytes")
            return filepath
        else:
            print(f"❌ ElevenLabs error: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def send_voice_message(audio_path, caption=None):
    """Send voice message via Telegram"""
    print(f"📤 Sending to Telegram...")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVoice"
    
    try:
        with open(audio_path, 'rb') as audio_file:
            files = {'voice': audio_file}
            data = {'chat_id': TELEGRAM_CHAT_ID}
            if caption:
                data['caption'] = caption
            
            response = requests.post(url, files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    print(f"✅ Voice message sent!")
                    return True
                else:
                    print(f"❌ Telegram error: {result}")
                    return False
            else:
                print(f"❌ HTTP error: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Error sending: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: vev-telegram-voice 'message to speak'")
        print("       vev-telegram-voice --test")
        sys.exit(1)
    
    if sys.argv[1] == '--test':
        text = "Hei! Dette er Vev. Jeg kan nå sende talemeldinger på Telegram!"
    else:
        text = " ".join(sys.argv[1:])
    
    print("=" * 60)
    print("🎙️ VEV TELEGRAM VOICE SENDER")
    print("=" * 60)
    print()
    print(f"Message: {text}")
    print()
    
    # Generate TTS
    audio_path = generate_tts(text)
    if not audio_path:
        print("❌ Failed to generate audio")
        sys.exit(1)
    
    # Send to Telegram
    success = send_voice_message(audio_path, caption="🎙️ Melding fra Vev")
    
    print()
    print("=" * 60)
    if success:
        print("✅ Voice message delivered!")
    else:
        print("❌ Failed to send")
    print("=" * 60)

if __name__ == "__main__":
    main()
