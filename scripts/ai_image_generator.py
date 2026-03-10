#!/usr/bin/env python3
"""
AI Bildegenerering for NRJ Morgen - INTEGRERT VERSION
Genererer bilder med OpenAI DALL-E og lagrer i Supabase Storage
Integrert i morgenrutinen
"""

import os
import json
import urllib.request
import base64
import time
import random
from datetime import datetime

# Konfigurasjon
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"
BUCKET_NAME = "media-library"

# Tilgjengelige modeller: gpt-image-1.5, dall-e-2, dall-e-3, gpt-image-1, gpt-image-1-mini
IMAGE_MODEL = "gpt-image-1-mini"  # Raskest og billigst
OPENAI_API_URL = "https://api.openai.com/v1/images/generations"

# Rate limiting - global variabel for å tracke siste kall
_last_api_call = 0
MIN_DELAY_BETWEEN_CALLS = 3.0  # Sekunder mellom API-kall

def rate_limited_call(func, *args, **kwargs):
    """Rate limiting wrapper - sikrer minimum tid mellom kall"""
    global _last_api_call
    
    elapsed = time.time() - _last_api_call
    if elapsed < MIN_DELAY_BETWEEN_CALLS:
        sleep_time = MIN_DELAY_BETWEEN_CALLS - elapsed
        print(f"   ⏱️  Rate limiting: venter {sleep_time:.1f}s...")
        time.sleep(sleep_time)
    
    result = func(*args, **kwargs)
    _last_api_call = time.time()
    return result

def call_with_retry(func, max_retries=3):
    """Prøv funksjon på nytt med exponential backoff ved feil"""
    for attempt in range(max_retries):
        try:
            return func()
        except urllib.error.HTTPError as e:
            if e.code == 429:  # Rate limit
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"   ⚠️  Rate limit (forsøk {attempt+1}/{max_retries}), venter {wait_time:.1f}s...")
                time.sleep(wait_time)
            else:
                raise
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"   ⚠️  Feil (forsøk {attempt+1}/{max_retries}), venter {wait_time:.1f}s...")
                time.sleep(wait_time)
            else:
                raise
    return None

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
    
    title_short = title[:100]
    desc_short = description[:150] if description else ""
    
    # Identifiser tema for bedre prompt
    keywords = {
        'kongelig': 'royal family, palace, elegant',
        'reality': 'reality TV show, dramatic scene',
        'influencer': 'social media, modern lifestyle',
        'musikk': 'music concert, stage performance',
        'film': 'movie scene, cinema',
        'brudd': 'emotional scene, dramatic',
        'bryllup': 'wedding celebration, romantic',
        'sport': 'sports event, action',
    }
    
    # Finn matchende stikkord
    style_hints = "professional news photography, vibrant colors, modern composition"
    combined = (title_short + " " + desc_short).lower()
    
    for key, style in keywords.items():
        if key in combined:
            style_hints = style + ", " + style_hints
            break
    
    prompt = f"""Professional news illustration for entertainment news website.

Headline: "{title_short}"
Context: {desc_short}

Visual style: {style_hints}
Mood: Engaging, suitable for morning radio show audience 18-35
Composition: Clean, eye-catching, suitable as article header image
Important: No text, no watermarks, photorealistic style

Create a compelling visual that captures the essence of this celebrity/entertainment news story."""

    return prompt

def generate_image_with_openai(prompt, api_key):
    """Generer bilde med OpenAI DALL-E 3 - med rate limiting og retry"""
    
    def _do_generate():
        payload = {
            "model": "dall-e-3",
            "prompt": prompt[:4000],  # Max 4000 chars
            "size": "1024x1024",
            "quality": "standard",
            "n": 1,
            "response_format": "b64_json"
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        req = urllib.request.Request(
            OPENAI_API_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers
        )
        
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode())
            b64_image = data['data'][0]['b64_json']
            return base64.b64decode(b64_image)
    
    # Bruk rate limiting + retry
    try:
        return rate_limited_call(call_with_retry, _do_generate)
    except Exception as e:
        print(f"   ⚠️  OpenAI API feil etter retries: {e}")
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
        
        with urllib.request.urlopen(req, timeout=60) as resp:
            if resp.status in [200, 201]:
                public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{filename}"
                return public_url
            else:
                print(f"   ⚠️  Upload status: {resp.status}")
                return None
                
    except Exception as e:
        print(f"   ⚠️  Opplasting feilet: {e}")
        return None

def get_fallback_image_url():
    """Fallback URL hvis AI-generering feiler"""
    # Bruk et generisk bilde fra media-library
    return f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/nrj-news/placeholder.png"

def generate_news_image(title, description, article_id):
    """
    Hovedfunksjon: Generer bilde og last opp til Supabase
    
    Returns:
        str: Bilde URL eller None hvis feil
    """
    
    api_key = load_openai_key()
    if not api_key:
        print("   ⚠️  Ingen OpenAI API key - bruker fallback")
        return get_fallback_image_url()
    
    print(f"   🎨 Genererer AI-bilde...")
    
    # 1. Generer prompt
    prompt = generate_image_prompt(title, description)
    
    # 2. Generer bilde
    image_data = generate_image_with_openai(prompt, api_key)
    if not image_data:
        print("   ⚠️  AI-generering feilet - bruker fallback")
        return get_fallback_image_url()
    
    # 3. Lag filnavn
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = "".join(c for c in title[:25] if c.isalnum()).rstrip()
    filename = f"nrj-news/{timestamp}_{safe_title}_{article_id[:8]}.png"
    
    # 4. Last opp til Supabase
    print(f"   📤 Laster opp til Supabase...")
    image_url = upload_to_supabase(image_data, filename)
    
    if image_url:
        print(f"   ✅ AI-bilde klar")
        return image_url
    else:
        print(f"   ⚠️  Opplasting feilet - bruker fallback")
        return get_fallback_image_url()

# For testing
if __name__ == '__main__':
    print("🧪 TEST: AI Bildegenerering")
    print("=" * 60)
    
    test_title = "Marius Borg Høiby vil løslates fra varetekt"
    test_desc = "Kongelig rettssak med høy dramafaktor"
    test_id = "test12345"
    
    result = generate_news_image(test_title, test_desc, test_id)
    
    print(f"\n{'='*60}")
    if result:
        print(f"✅ Resultat: {result[:70]}...")
    else:
        print("❌ Ingen bilde URL returnert")
