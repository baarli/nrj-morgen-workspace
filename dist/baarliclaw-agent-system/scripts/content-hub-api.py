#!/usr/bin/env python3
# /root/.openclaw/workspace/scripts/content-hub-api.py
# API-klient for content-hub i nrjmorgen.com

import os
import sys
import json
import urllib.request
from pathlib import Path

# Konfigurasjon
WORKSPACE = "/root/.openclaw/workspace"
CREDENTIALS = f"{WORKSPACE}/.credentials/nrj-morgen.env"
CONTENT_HUB_URL = "https://nrjmorgen.com/api/content-hub"  # Juster etter faktisk URL

def load_credentials():
    """Last API-nøkler"""
    creds = {}
    if os.path.exists(CREDENTIALS):
        with open(CREDENTIALS, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    value = value.strip('"').strip("'")
                    creds[key] = value
    return creds

def upload_audio(file_path, title, description, tags=None, agenda_item_id=None):
    """Last opp lydfil til content-hub"""
    
    print(f"☁️  Laster opp til content-hub...")
    
    # Les fil
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    # Bygg multipart/form-data
    boundary = '----FormBoundary' + os.urandom(8).hex()
    
    # Metadata som JSON
    metadata = {
        'title': title,
        'description': description,
        'tags': tags or [],
        'agenda_item_id': agenda_item_id,
        'type': 'audio_clip',
        'mime_type': 'audio/mpeg'
    }
    
    # Bygg body
    body = []
    
    # Metadata del
    body.append(f'--{boundary}'.encode())
    body.append(b'Content-Disposition: form-data; name="metadata"')
    body.append(b'Content-Type: application/json')
    body.append(b'')
    body.append(json.dumps(metadata).encode())
    
    # Fil del
    filename = os.path.basename(file_path)
    body.append(f'--{boundary}'.encode())
    body.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"'.encode())
    body.append(b'Content-Type: audio/mpeg')
    body.append(b'')
    body.append(file_data)
    
    # Avslutt
    body.append(f'--{boundary}--'.encode())
    body.append(b'')
    
    # Kombiner
    body = b'\r\n'.join(body)
    
    # Send request
    url = f"{CONTENT_HUB_URL}/upload"
    
    headers = {
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'Content-Length': str(len(body))
    }
    
    try:
        req = urllib.request.Request(url, data=body, headers=headers, method='POST')
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode())
            print(f"  ✅ Opplasting vellykket!")
            print(f"     ID: {result.get('id')}")
            print(f"     URL: {result.get('url')}")
            return result
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"  ❌ HTTP {e.code}: {error_body}")
        return None
    except Exception as e:
        print(f"  ❌ Feil: {e}")
        return None

def create_audio_clip(file_path, title, description, source_url=None, agenda_item_id=None):
    """Opprett en ny audio-clip i content-hub"""
    
    print(f"🎵 Oppretter audio-clip...")
    print(f"   Fil: {file_path}")
    print(f"   Tittel: {title[:50]}...")
    
    # For nå: simuler opplasting (siden vi ikke har faktisk API-endepunkt)
    # TODO: Erstatt med faktisk API-kall når content-hub er klart
    
    # Lagre lokalt i stedet
    output_dir = f"{WORKSPACE}/audio-clips"
    os.makedirs(output_dir, exist_ok=True)
    
    import shutil
    filename = os.path.basename(file_path)
    output_path = os.path.join(output_dir, filename)
    shutil.copy2(file_path, output_path)
    
    # Lag metadata
    metadata = {
        'id': f"clip_{os.urandom(4).hex()}",
        'filename': filename,
        'title': title,
        'description': description,
        'source_url': source_url,
        'agenda_item_id': agenda_item_id,
        'local_path': output_path,
        'status': 'ready',
        'created_at': __import__('datetime').datetime.now().isoformat()
    }
    
    # Lagre metadata
    meta_path = output_path + '.json'
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"  ✅ Lagret lokalt: {output_path}")
    print(f"  📄 Metadata: {meta_path}")
    
    return metadata

def link_to_agenda_item(clip_id, agenda_item_id):
    """Link en audio-clip til en sak i Supabase"""
    
    print(f"🔗 Linker clip {clip_id} til sak {agenda_item_id}...")
    
    # TODO: Implementer faktisk linking i Supabase
    # For nå: logg bare
    
    print(f"  ✅ Linket (simulert)")
    return True

def list_clips():
    """List alle lokale audio-clips"""
    
    output_dir = f"{WORKSPACE}/audio-clips"
    
    if not os.path.exists(output_dir):
        print("Ingen clips funnet")
        return []
    
    clips = []
    for filename in os.listdir(output_dir):
        if filename.endswith('.json'):
            with open(os.path.join(output_dir, filename), 'r') as f:
                clips.append(json.load(f))
    
    return clips

def main():
    if len(sys.argv) < 2:
        print("Content Hub API Client")
        print("")
        print("Bruk:")
        print(f"  {sys.argv[0]} upload <fil> <tittel> [beskrivelse]")
        print(f"  {sys.argv[0]} list")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'upload':
        if len(sys.argv) < 4:
            print("Mangler fil eller tittel")
            sys.exit(1)
        
        file_path = sys.argv[2]
        title = sys.argv[3]
        description = sys.argv[4] if len(sys.argv) > 4 else ""
        
        result = create_audio_clip(file_path, title, description)
        sys.exit(0 if result else 1)
    
    elif command == 'list':
        clips = list_clips()
        print(f"Fant {len(clips)} clip(s):")
        for clip in clips:
            print(f"  - {clip['title'][:50]}... ({clip['filename']})")
        sys.exit(0)
    
    else:
        print(f"Ukjent kommando: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
