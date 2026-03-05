#!/usr/bin/env python3
"""
Vev Telegram Auto-Responder
Kontinuerlig lytter og svarer på Telegram-meldinger i realtid
"""
import os
import sys
import time
import json
import requests
from datetime import datetime
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"
LOG_FILE = f"{WORKSPACE}/brain/logs/telegram-auto-responder.log"
STATE_FILE = f"{WORKSPACE}/.vev-telegram-state.json"

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
VEV_VOICE_ID = os.environ.get('VEV_VOICE_ID', '4kCDY3HJwvO7Zp3con83')
VEV_VOICE_MODEL = os.environ.get('VEV_VOICE_MODEL', 'eleven_flash_v2_5')

def log(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg + '\n')

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {'last_update_id': 0, 'conversations': {}}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def get_updates(offset=0):
    """Hent nye meldinger fra Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    params = {'offset': offset, 'limit': 10}
    
    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                return data.get('result', [])
    except Exception as e:
        log(f"Error getting updates: {e}")
    
    return []

def send_message(text, chat_id=None):
    """Send tekstmelding"""
    chat_id = chat_id or TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    try:
        response = requests.post(url, json={
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }, timeout=30)
        return response.status_code == 200
    except Exception as e:
        log(f"Error sending message: {e}")
        return False

def generate_tts(text):
    """Generer TTS via ElevenLabs"""
    import hashlib
    text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
    
    AUDIO_DIR = f"{WORKSPACE}/brain/projects/voice-chat/audio"
    Path(AUDIO_DIR).mkdir(parents=True, exist_ok=True)
    
    filepath = f"{AUDIO_DIR}/auto_{text_hash}.mp3"
    
    # Sjekk cache
    if Path(filepath).exists():
        return filepath
    
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
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return filepath
    except Exception as e:
        log(f"TTS error: {e}")
    
    return None

def send_voice_message(audio_path, chat_id=None, caption=None):
    """Send talemelding"""
    chat_id = chat_id or TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVoice"
    
    try:
        with open(audio_path, 'rb') as audio_file:
            files = {'voice': audio_file}
            data = {'chat_id': chat_id}
            if caption:
                data['caption'] = caption
            
            response = requests.post(url, files=files, data=data, timeout=30)
            return response.status_code == 200
    except Exception as e:
        log(f"Error sending voice: {e}")
        return False

def generate_response(user_message, context=None):
    """Generer respons basert på melding"""
    user_lower = user_message.lower()
    
    # Enkle mønstre
    if any(word in user_lower for word in ['hei', 'hallo', 'hi', 'hello']):
        return "Hei! 👋 Jeg er Vev. Hva kan jeg hjelpe deg med?"
    
    if any(word in user_lower for word in ['hvordan går det', 'how are you']):
        return "Det går bra! Jeg er klar til å hjelpe. Hva trenger du?"
    
    if any(word in user_lower for word in ['takk', 'thanks', 'thank you']):
        return "Bare hyggelig! 😊"
    
    if any(word in user_lower for word in ['stemme', 'voice', 'snakk', 'talk']):
        return "Jeg kan snakke! Vil du høre min stemme?"
    
    if any(word in user_lower for word in ['hjelp', 'help']):
        return "Jeg kan hjelpe deg med:\n• NRJ Morgen saksliste\n• Radio/podcast statistikk\n• Tekniske oppgaver\n• Bare å spørre!"
    
    # Standard respons
    responses = [
        "Interessant! Fortell meg mer.",
        "Jeg hører deg. Hva tenker du?",
        "Skjønner! Hva kan jeg gjøre for deg?",
        "Ja? Jeg lytter.",
        "Hmm, fortell mer om det!"
    ]
    
    # Velg basert på melding hash for konsistens
    msg_hash = sum(ord(c) for c in user_message) % len(responses)
    return responses[msg_hash]

def process_message(message, state):
    """Behandle en melding"""
    update_id = message.get('update_id')
    msg = message.get('message', {})
    chat_id = msg.get('chat', {}).get('id')
    text = msg.get('text', '')
    from_user = msg.get('from', {}).get('first_name', 'Ukjent')
    
    if not text:
        return
    
    log(f"Melding fra {from_user}: {text[:50]}...")
    
    # Generer respons
    response_text = generate_response(text)
    
    # Send tekstrespons
    send_message(response_text, chat_id)
    log(f"Sendt tekst: {response_text[:50]}...")
    
    # Generer og send talemelding
    audio_path = generate_tts(response_text)
    if audio_path:
        send_voice_message(audio_path, chat_id)
        log(f"Sendt talemelding")
    
    # Oppdater state
    state['last_update_id'] = update_id + 1
    state['conversations'][str(chat_id)] = {
        'last_message': text,
        'last_response': response_text,
        'timestamp': datetime.now().isoformat()
    }

def main():
    log("=" * 60)
    log("🤖 VEV TELEGRAM AUTO-RESPONDER STARTET")
    log("=" * 60)
    log("Lytter etter meldinger... Trykk Ctrl+C for å stoppe")
    
    state = load_state()
    
    try:
        while True:
            updates = get_updates(state['last_update_id'])
            
            if updates:
                log(f"Mottatt {len(updates)} oppdatering(er)")
                
                for update in updates:
                    process_message(update, state)
                
                save_state(state)
            
            # Vent før neste sjekk
            time.sleep(2)
            
    except KeyboardInterrupt:
        log("\n🛑 Stoppet av bruker")
        save_state(state)
    except Exception as e:
        log(f"\n❌ Feil: {e}")
        save_state(state)
        raise

if __name__ == "__main__":
    main()
