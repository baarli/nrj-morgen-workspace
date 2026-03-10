#!/usr/bin/env python3
"""
AI Bildegenerering for NRJ Morgen
Genererer bilder med OpenAI DALL-E og lagrer i Supabase Storage
"""

import os
import json
import urllib.request
import base64
from datetime import datetime

# Konfigurasjon
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"
BUCKET_NAME = "media-library"

def load_openai_key():
    """Last OpenAI API key"""
    creds = {}
    env_files = [
        '/root/.openclaw/workspace/.credentials/live-search.env',
        '/root/.openclaw/workspace/.credentials/nrj-morgen.env'
    ]
    for env_file in env_files:
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        creds[key] = value.strip('"').strip("'")
    return creds.get('OPENAI_API_KEY', os.environ.get('OPENAI_API_KEY', ''))

def generate_image_prompt(title, description):
    """Generer en god prompt for DALL-E basert på sakens innhold"""
    
    # Begrens lengden
    title_short = title[:80]
    desc_short = description[:100] if description else ""
    
    # Bygg prompt
    prompt = f"""Create a professional news illustration for an entertainment news article.

Article title: "{title_short}"
Article context: {desc_short}

Style: Modern, vibrant, eye-catching news header image suitable for a radio show website. Clean composition with good lighting. Professional photojournalism style. No text in the image.

The image should be engaging and suitable for a morning radio show audience (18-35 years old)."""

    return prompt

def generate_image_with_openai(prompt, api_key):
    """Generer bilde med OpenAI DALL-E 3"""
    
    url = "https://api.openai.com/v1/images/generations"
    
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "size": "1024x1024",
        "quality": "standard",
        "n": 1,
        "response_format": "b64_json"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers
        )
        
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode())
            
            # Hent base64-encoded bilde
            b64_image = data['data'][0]['b64_json']
            return base64.b64decode(b64_image)
            
    except Exception as e:
        print(f"❌ Feil ved bildegenerering: {e}")
        return None

def upload_to_supabase(image_data, filename):
    """Last opp bilde til Supabase Storage"""
    
    upload_url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{filename}"
    
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'image/png'
    }
    
    try:
        req = urllib.request.Request(
            upload_url,
            data=image_data,
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status in [200, 201]:
                # Returner public URL
                public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{filename}"
                return public_url
            else:
                print(f"⚠️  Upload status: {resp.status}")
                return None
                
    except Exception as e:
        print(f"❌ Feil ved opplasting: {e}")
        return None

def generate_and_upload_image(title, description, article_id):
    """Hovedfunksjon: Generer bilde og last opp til Supabase"""
    
    api_key = load_openai_key()
    if not api_key:
        print("❌ Ingen OpenAI API key funnet")
        return None
    
    print(f"🎨 Genererer bilde for: {title[:50]}...")
    
    # 1. Generer prompt
    prompt = generate_image_prompt(title, description)
    
    # 2. Generer bilde
    image_data = generate_image_with_openai(prompt, api_key)
    if not image_data:
        return None
    
    print(f"   ✅ Bilde generert ({len(image_data)} bytes)")
    
    # 3. Lag filnavn
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = "".join(c for c in title[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_title = safe_title.replace(' ', '_')
    filename = f"nrj-news/{timestamp}_{safe_title}_{article_id[:8]}.png"
    
    # 4. Last opp til Supabase
    print(f"   📤 Laster opp til Supabase...")
    image_url = upload_to_supabase(image_data, filename)
    
    if image_url:
        print(f"   ✅ Bilde tilgjengelig: {image_url[:60]}...")
        return image_url
    else:
        return None

def test_generation():
    """Test bildegenerering"""
    test_title = "Kronprinsen taus om Mette-Marit sak"
    test_desc = "Kronprins Haakon ville ikke svare på spørsmål om Mette-Marit"
    test_id = "test123"
    
    print("🧪 TESTER AI-BILDEGENERERING")
    print("=" * 60)
    
    result = generate_and_upload_image(test_title, test_desc, test_id)
    
    if result:
        print(f"\n✅ SUCCESS! Bilde URL: {result}")
    else:
        print(f"\n❌ FAILED")
    
    return result

if __name__ == '__main__':
    # Test hvis kjørt direkte
    test_generation()
