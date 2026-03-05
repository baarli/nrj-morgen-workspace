#!/usr/bin/env python3
#
# telegram-poll.py
# Henter nye meldinger fra Telegram og viser dem
#

import json
import urllib.request
import os

# Hent token
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    # Prøv å lese fra fil
    import subprocess
    result = subprocess.run(
        ['bash', '-c', 'source /root/.openclaw/workspace/.credentials/telegram-bot.env && echo $TELEGRAM_BOT_TOKEN'],
        capture_output=True, text=True
    )
    TOKEN = result.stdout.strip()

if not TOKEN:
    print("❌ TELEGRAM_BOT_TOKEN ikke funnet")
    exit(1)

# Offset for å unngå å hente samme melding flere ganger
OFFSET_FILE = "/tmp/telegram_offset"
if os.path.exists(OFFSET_FILE):
    with open(OFFSET_FILE, 'r') as f:
        offset = int(f.read().strip() or 0)
else:
    offset = 0

print("=== Telegram Polling ===")
print(f"Offset: {offset}")
print()

# Hent nye meldinger
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={offset}&limit=10"

try:
    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.loads(response.read().decode())
        
        if not data.get('ok'):
            print(f"❌ Feil fra Telegram API: {data}")
            exit(1)
        
        updates = data.get('result', [])
        
        if not updates:
            print("Ingen nye meldinger.")
            exit(0)
        
        print(f"Fant {len(updates)} nye meldinger:")
        print()
        
        for update in updates:
            update_id = update.get('update_id', 0)
            message = update.get('message', {})
            
            if message:
                chat = message.get('chat', {})
                from_user = message.get('from', {})
                
                chat_id = chat.get('id', 'unknown')
                username = from_user.get('username') or from_user.get('first_name', 'Ukjent')
                text = message.get('text', '[Ingen tekst]')
                
                print(f"📨 Fra {username} (Chat ID: {chat_id}):")
                print(f"   {text}")
                print(f"   Update ID: {update_id}")
                print()
                
                # Lagre update_id+1 for neste polling
                with open(OFFSET_FILE, 'w') as f:
                    f.write(str(update_id + 1))
        
        print(f"=== Neste offset: {offset} ===")
        
except Exception as e:
    print(f"❌ Feil: {e}")
    exit(1)
