#!/usr/bin/env python3
"""
AI Bildegenerering for ALLE saker i NRJ Morgen
Genererer bilder med OpenAI og lagrer i Supabase Storage
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
IMAGE_MODEL = "gpt-image-1"
OPENAI_API_URL = "https://api.openai.com/v1/images/generations"

# Rate limiting
_last_api_call = 0
MIN_DELAY_BETWEEN_CALLS = 2.0  # 2 sekunder mellom kall

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
    """Generer en god prompt for AI-bilde basert på sakens innhold"""
    
    title_short = title[:100]
    desc_short = description[:150] if description else ""
    
    # Identifiser tema for bedre prompt
    keywords = {
        'oscar': 'glamorous Oscar awards ceremony, red carpet, Hollywood lights, elegant celebrities',
        'eurovision': 'Eurovision Song Contest stage, colorful lights, music performance, exciting atmosphere',
        'reality': 'reality TV show scene, dramatic lighting, television studio, entertainment',
        'spillet': 'Norwegian reality TV show, game show setting, dramatic scene',
        'kjendis': 'celebrity news, glamorous setting, entertainment industry, spotlight',
        'premiere': 'movie or show premiere, red carpet event, glamorous atmosphere',
        'brudd': 'emotional scene, relationship drama, soft lighting, intimate setting',
        'influencer': 'social media lifestyle, modern setting, trendy atmosphere, youthful energy',
        'artist': 'music artist performance, concert vibes, creative setting, artistic lighting',
        'film': 'cinema scene, movie setting, dramatic lighting, storytelling atmosphere'
    }
    
    # Finn matchende stikkord
    style_hints = "professional news illustration, vibrant colors, modern composition, clean design"
    combined = (title_short + " " + desc_short).lower()
    
    for key, style in keywords.items():
        if key in combined:
            style_hints = style + ", " + style_hints
            break
    
    prompt = f"""Create a professional news illustration for an entertainment news article.

Headline: "{title_short}"
Context: {desc_short}

Visual style: {style_hints}
Mood: Engaging, energetic, suitable for morning radio show audience 18-35
Composition: Clean, eye-catching, suitable as article header image
Important: No text in the image, no watermarks, professional photojournalism style

Create a compelling visual that captures the essence of this Norwegian entertainment news story."""

    return prompt

def generate_and_upload_image(title, description, article_id, api_key):
    """Generer bilde og last opp til Supabase - med rate limiting"""
    global _last_api_call
    
    # Rate limiting
    elapsed = time.time() - _last_api_call
    if elapsed < MIN_DELAY_BETWEEN_CALLS:
        sleep_time = MIN_DELAY_BETWEEN_CALLS - elapsed
        print(f"      ⏱️  Venter {sleep_time:.1f}s (rate limiting)...")
        time.sleep(sleep_time)
    
    try:
        # 1. Generer prompt
        prompt = generate_image_prompt(title, description)
        
        # 2. Generer bilde med OpenAI
        payload = {
            "model": IMAGE_MODEL,
            "prompt": prompt[:4000],
            "size": "1024x1024",
            "n": 1
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
            image_data = base64.b64decode(b64_image)
        
        _last_api_call = time.time()
        
        # 3. Lag filnavn (ascii-safe)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c for c in title[:20] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_').replace('æ', 'a').replace('ø', 'o').replace('å', 'a')
        safe_title = safe_title.replace('Æ', 'A').replace('Ø', 'O').replace('Å', 'A')
        filename = f"nrj-news/{timestamp}_{safe_title}_{article_id[:6]}.png"
        
        # 4. Last opp til Supabase
        upload_url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{filename}"
        
        upload_headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'image/png'
        }
        
        req = urllib.request.Request(
            upload_url,
            data=image_data,
            headers=upload_headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=60) as resp:
            if resp.status in [200, 201]:
                public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{filename}"
                return public_url
            else:
                return None
                
    except Exception as e:
        print(f"      ⚠️  Feil: {str(e)[:50]}")
        return None

def generate_images_for_all_articles(articles):
    """Generer bilder for ALLE artikler"""
    
    api_key = load_openai_key()
    if not api_key:
        print("❌ Ingen OpenAI API key")
        return {}
    
    print(f"\n🎨 Genererer bilder for {len(articles)} saker...")
    print("(Dette tar ca. {0} sekunder med rate limiting)\n".format(len(articles) * 2))
    
    image_urls = {}
    
    for i, article in enumerate(articles, 1):
        title = article.get('title', '')
        description = article.get('description', '')
        article_id = str(uuid.uuid4())
        
        print(f"{i:2}. {title[:45]}...")
        print("    🎨 Genererer...", end=" ")
        
        image_url = generate_and_upload_image(title, description, article_id, api_key)
        
        if image_url:
            print(f"✅ OK")
            image_urls[i] = image_url
        else:
            print(f"❌ Feilet")
            image_urls[i] = None
    
    return image_urls

if __name__ == '__main__':
    # Test
    print("🧪 TEST: AI Bildegenerering for alle saker")
    print("=" * 60)
    
    test_articles = [
        {"title": "Oscar-fest med kjendiser", "description": "Stjerner på rød løper"},
        {"title": "Eurovision dramatikk", "description": "Svensk artist i trøbbel"},
        {"title": "Ny reality sesong", "description": "Deltakere klare"}
    ]
    
    result = generate_images_for_all_articles(test_articles)
    print(f"\n✅ {sum(1 for v in result.values() if v)}/{len(result)} bilder generert")
