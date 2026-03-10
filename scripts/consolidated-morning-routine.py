#!/usr/bin/env python3
"""
NRJ MORGEN - KONSOLIDERT MORGEN-RUTINE v1.0
Kombinerer alle steg i én fil for pålitelighet og enkelhet

STEG:
1. Søk etter nyheter (Brave API)
2. Generer OpenAI-titler (maks 7 ord)
3. Slett gamle saker i Supabase
4. Insert nye saker med alle felter
5. Generer og send showprepp på e-post

Kjøres: Hver morgen kl 04:50 (10 min før sending)
"""

import os
import sys
import json
import concurrent.futures
import urllib.request
import urllib.parse
import re
import smtplib
import ssl
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === KONFIGURASJON ===
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"
TENANT_ID = "a0000000-0000-0000-0000-000000000001"
CREATED_BY = "10aa1508-6d52-490c-8ae5-fa3da9a152c4"
PROFILE_PICTURE = "https://lh3.googleusercontent.com/a/ACg8ocLyiG1iwB_rfOCAN64WGPUUIWprTMX0JfUDsoy7dHkd6AVdaQ=s96-c"

BRAVE_KEY = "BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev"
OPENAI_KEY = "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"

TOMORROW = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
TODAY_STR = datetime.now().strftime('%A %d. %B').capitalize()

# === KILDE-KONFIGURASJON ===
SOURCES = {
    'reality_tv': {
        'name': 'Reality TV',
        'queries': [
            "site:tv2.no Farmen Kjendis",
            "site:tv2.no Paradise Hotel",
            "site:tv2.no Kompani Lauritzen",
            "site:tv2.no Love Island",
        ],
        'max_articles': 3
    },
    'kjendis_drama': {
        'name': 'Kjendis Drama',
        'queries': [
            "site:dagbladet.no kjendis brudd",
            "site:seher.no kjendis",
            "site:nettavisen.no kjendis",
            "site:vg.no rampelys",
        ],
        'max_articles': 3
    },
    'film_tv': {
        'name': 'Film & TV',
        'queries': [
            "site:vg.no rampelys premiere",
            "site:nrk.no kultur film",
            "site:dagbladet.no kultur tv",
            "site:tv2.no underholdning",
        ],
        'max_articles': 3
    },
    'musikk': {
        'name': 'Musikk',
        'queries': [
            "Spellemannprisen 2026",
            "VG-lista",
            "P3 Gull",
            "site:nrk.no kultur musikk",
        ],
        'max_articles': 3
    },
    'internasjonalt': {
        'name': 'Internasjonalt',
        'queries': [
            "site:dailymail.co.uk celebrity",
            "site:tmz.com celebrity news",
            "site:eonline.com news",
            "site:people.com celebrity",
        ],
        'max_articles': 3
    },
}

# === HJELPEFUNKSJONER ===

def log(message, emoji=""):
    """Logg med timestamp"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {emoji} {message}")

def search_brave(query, count=5):
    """Søk med Brave API"""
    if not BRAVE_KEY:
        return None
    
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.search.brave.com/res/v1/news/search?q={encoded_query}&count={count}&search_lang=nb&country=no&freshness=pd"
    
    headers = {
        'X-Subscription-Token': BRAVE_KEY,
        'Accept': 'application/json'
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return None

def is_excluded(title, description):
    """Sjekk om saken skal ekskluderes"""
    combined = (title + ' ' + description).lower()
    
    hard_excluded = [
        'fotball', 'krig', 'terror', 'død', 'tragedie', 'ulykke', 'drap',
        'skudd', 'vold', 'politi', 'pågripelse', 'fengsel', 'dom', 'rettssak',
        'regjering', 'storting', 'parti', 'politiker', 'lovforslag', 'budsjett',
        'skatt', 'økonomi', 'finans', 'rente', 'inflasjon', 'sykehus', 'korona',
        'skiforbundet', 'langrenn', 'ski', 'hopp', 'alpint', 'skiskyting',
    ]
    
    for word in hard_excluded:
        if word in combined:
            return True
    return False

def calculate_score(title, description):
    """Vurder underholdningsverdi (0-100)"""
    score = 50
    combined = (title + ' ' + description).lower()
    
    positive = ['brudd', 'krangel', 'drama', 'skandale', 'avsløring', 'hemmelig',
                'kontrovers', 'konflikt', 'exit', 'overraskelse', 'comeback', 
                'pinlig', 'sterkt sitat', 'tårer', 'raser', 'sjokk', 'kaos']
    
    for keyword in positive:
        if keyword in combined:
            score += 10
    
    return min(100, max(0, score))

def generate_short_title(original_title, description):
    """Generer tittel på maks 7 ord med OpenAI"""
    try:
        prompt = f"""Original tittel: {original_title}
Beskrivelse: {description[:200]}

Lag en kort, catchy tittel på NORSK for NRJ Morgen (morgenradio).
- Maksimum 7 ord
- Fængende og underholdende
- Fokus på det mest interessante
- Bruk norsk språk

Kun tittelen, ingen forklaring."""
        
        headers = {
            'Authorization': f'Bearer {OPENAI_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'gpt-4o-mini',
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.7,
            'max_tokens': 50
        }
        
        req = urllib.request.Request(
            'https://api.openai.com/v1/chat/completions',
            data=json.dumps(data).encode('utf-8'),
            headers=headers
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            new_title = result['choices'][0]['message']['content'].strip()
            new_title = new_title.strip('"\'')
            words = new_title.split()
            if len(words) > 7:
                new_title = ' '.join(words[:7])
            return new_title
            
    except Exception as e:
        words = original_title.split()
        if len(words) > 7:
            return ' '.join(words[:7]) + '...'
        return original_title

def fetch_image_from_url(url):
    """Prøv å hente bilde fra artikkelens meta tags"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            og_match = re.search(r'<meta[^>]*property="og:image"[^>]*content="([^"]+)"', html, re.IGNORECASE)
            if og_match:
                return og_match.group(1)
            
            tw_match = re.search(r'<meta[^>]*name="twitter:image"[^>]*content="([^"]+)"', html, re.IGNORECASE)
            if tw_match:
                return tw_match.group(1)
                
    except:
        pass
    return None

def get_fallback_image(source):
    """Fallback-bilder for kjente kilder"""
    source_lower = source.lower()
    if 'nettavisen' in source_lower:
        return "https://www.nettavisen.no/logo.png"
    elif 'dagbladet' in source_lower:
        return "https://www.dagbladet.no/logo.png"
    elif 'seher' in source_lower or 'se og hør' in source_lower:
        return "https://www.seher.no/logo.png"
    elif 'nrk' in source_lower:
        return "https://www.nrk.no/logo.png"
    elif 'vg' in source_lower:
        return "https://www.vg.no/logo.png"
    elif 'tv2' in source_lower:
        return "https://www.tv2.no/logo.png"
    elif 'aftenposten' in source_lower:
        return "https://www.aftenposten.no/logo.png"
    return None

def supabase_request(method, path, data=None, params=None):
    """Gjør en Supabase-forespørsel"""
    url = f"{SUPABASE_URL}/rest/v1{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
    }
    
    if method == 'GET':
        req = urllib.request.Request(url, headers=headers)
    elif method == 'DELETE':
        req = urllib.request.Request(url, headers=headers, method='DELETE')
    else:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8') if data else None,
            headers=headers,
            method=method
        )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            if method == 'GET':
                return json.loads(response.read().decode('utf-8'))
            return True
    except Exception as e:
        if method == 'GET':
            return []
        return False

# === HOVEDFUNKSJONER ===

def step1_search_news():
    """STEG 1: Søk etter nyheter"""
    log("STEG 1: Søker etter nyheter...", "🔍")
    
    all_articles = []
    
    for key, config in SOURCES.items():
        log(f"Søker: {config['name']}...", "📡")
        
        for query in config['queries']:
            result = search_brave(query, count=5)
            
            if result and 'results' in result:
                for article in result['results']:
                    if is_excluded(article.get('title', ''), article.get('description', '')):
                        continue
                    
                    score = calculate_score(article.get('title', ''), article.get('description', ''))
                    
                    all_articles.append({
                        'title': article.get('title', ''),
                        'url': article.get('url', ''),
                        'description': article.get('description', ''),
                        'source': config['name'],
                        'score': score,
                        'category': config['name'],
                        'publishedAt': article.get('age', 'Nylig')
                    })
    
    # Fjern duplikater
    unique = {}
    for article in all_articles:
        url = article['url'].lower()
        if url not in unique:
            unique[url] = article
    
    unique_list = list(unique.values())
    unique_list.sort(key=lambda x: x['score'], reverse=True)
    
    log(f"Fant {len(unique_list)} unike artikler", "📊")
    return unique_list[:15]

def step2_generate_titles(articles):
    """STEG 2: Generer OpenAI-titler"""
    log("STEG 2: Genererer titler med OpenAI...", "🤖")
    
    for i, article in enumerate(articles, 1):
        original_title = article['title']
        short_title = generate_short_title(original_title, article.get('description', ''))
        article['short_title'] = short_title
        log(f"{i}. {short_title[:50]}...", "✏️")
    
    return articles

def step3_delete_old():
    """STEG 3: Slett gamle saker"""
    log("STEG 3: Sletter gamle saker...", "🗑️")
    
    result = supabase_request(
        'DELETE',
        '/agenda_items',
        params={'tenant_id': f'eq.{TENANT_ID}', 'show_date': f'eq.{TOMORROW}'}
    )
    
    if result:
        log("Gamle saker slettet", "✅")
    else:
        log("Kunne ikke slette gamle saker", "⚠️")
    
    return result

def step4_insert_articles(articles):
    """STEG 4: Insert nye saker med AI-genererte bilder"""
    log("STEG 4: Inserter nye saker med AI-bilder...", "💾")
    
    inserted = 0
    
    # Importer AI bildegenerator
    import sys
    sys.path.insert(0, '/root/.openclaw/workspace/scripts')
    try:
        from ai_image_generator import generate_news_image
        ai_available = True
        log("AI bildegenerering tilgjengelig", "🎨")
    except Exception as e:
        ai_available = False
        log(f"AI bildegenerering ikke tilgjengelig: {e}", "⚠️")
    
    for i, article in enumerate(articles, 1):
        title = article.get('short_title', article.get('title', ''))
        url = article.get('url', '')
        
        if not title or not url:
            continue
        
        # HENT BILDE: Prioriter AI-generering, fallback til meta-tags
        image_url = None
        if ai_available:
            log(f"{i}/{len(articles)}: Genererer AI-bilde...", "🎨")
            article_id = str(uuid.uuid4())
            image_url = generate_news_image(
                title, 
                article.get('description', ''), 
                article_id
            )
        
        # Fallback til meta-tags hvis AI feilet
        if not image_url:
            image_url = fetch_image_from_url(url)
            if not image_url:
                image_url = get_fallback_image(article.get('source', ''))
        
        # Lag notes
        description = article.get('description', '')
        first_sentence = description.split('.')[0] if description else ''
        notes = f"{first_sentence}\n\nKilde: {article.get('source', 'Ukjent')}" 
        
        # Lag description med bilde
        desc_with_image = description
        if image_url:
            desc_with_image = f'<img src="{image_url}" alt="{title}" style="max-width:100%;border-radius:8px;margin-bottom:12px;" />\n\n{description}'
        
        # Payload
        payload = {
            'tenant_id': TENANT_ID,
            'title': title,
            'description': desc_with_image,
            'notes': notes,
            'link_url': url,
            'show_date': TOMORROW,
            'category': 'TALK',
            'created_by': CREATED_BY,
            'is_pinned': False,
            'is_completed': False
        }
        
        if image_url:
            payload['link_metadata'] = {'image_url': image_url}
        
        result = supabase_request('POST', '/agenda_items', payload)
        
        if result:
            inserted += 1
            log(f"{i}/{len(articles)}: {title[:40]}...", "✅")
        else:
            log(f"{i}/{len(articles)}: Feil", "❌")
    
    log(f"{inserted} av {len(articles)} saker insertet", "📊")
    return inserted

def step5_generate_showprepp(articles):
    """STEG 5: Generer showprepp"""
    log("STEG 5: Genererer showprepp...", "📝")
    
    showprepp = f"""# 📻 NRJ MORGEN SHOWPREPP
## {TODAY_STR}

---

## 🎯 Topp 8 Saker (Prioritert)

"""
    
    for i, article in enumerate(articles[:8], 1):
        title = article.get('short_title', article.get('title', 'Ukjent'))
        desc = article.get('description', '')
        url = article.get('url', '')
        first_line = desc.split('.')[0] if desc else ''
        
        showprepp += f"""### {i}. {title}
**Inngang:** {first_line[:100]}{'...' if len(first_line) > 100 else ''}

**Talking points:**
• Hva er det mest interessante her?
• Hvilken vinkel skal vi ta?
• Hvem kan vi ringe?

📎 [Les mer]({url})

---

"""
    
    showprepp += """## 📻 Segment-forslag

### Segment 1 (06:00-06:10): Åpning
• Velkommen til sendingen!
• Topp-sak fra listen
• Værmelding + trafikk

### Segment 2 (06:10-06:20): Kjendis-drama
• De beste kjendis-sakene
• Reality-oppdateringer

### Segment 3 (06:20-06:30): Internasjonalt & Musikk
• Hollywood-nyheter
• Musikk-oppdateringer
• Lytter-interaksjon

---

## 🎭 Dagens Vits

*Hvorfor gikk skuespilleren til legen?*

Fordi han hadde **scene**-vansker! 😄

---

## 🎧 Podkast-forslag

**Baarli og Benjamin går i terapi**
• Siste episode med morgen-humor
• Perfekt for dagens stemning

---

## ⚡ Quick Hits (Hvis tid)

"""
    
    for i, article in enumerate(articles[8:], 9):
        title = article.get('short_title', article.get('title', ''))
        url = article.get('url', '')
        showprepp += f"{i}. {title} - [Les mer]({url})\n"
    
    showprepp += f"""

---

**Generert:** {datetime.now().strftime('%H:%M')} | **Kimi Claw** 🤖
"""
    
    # Lagre til fil
    os.makedirs('/root/.openclaw/workspace/brain/reports', exist_ok=True)
    report_file = f'/root/.openclaw/workspace/brain/reports/showprepp-{TOMORROW}.md'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(showprepp)
    
    log(f"Showprepp lagret: {report_file}", "💾")
    return showprepp

def step6_send_email(showprepp):
    """STEG 6: Send e-post (valgfritt - krever SMTP-config)"""
    log("STEG 6: Sender e-post...", "📧")
    
    # Sjekk om SMTP er konfigurert
    smtp_server = os.environ.get('SMTP_SERVER', '')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    smtp_user = os.environ.get('SMTP_USER', '')
    smtp_pass = os.environ.get('SMTP_PASS', '')
    
    if not all([smtp_server, smtp_user, smtp_pass]):
        log("SMTP ikke konfigurert - hopper over e-post", "⚠️")
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = 'niklasbaarli@gmail.com'
        msg['Subject'] = f'📻 NRJ Morgen Showprepp - {TODAY_STR}'
        
        msg.attach(MIMEText(showprepp, 'plain', 'utf-8'))
        
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        
        log("E-post sendt til niklasbaarli@gmail.com", "✅")
        return True
        
    except Exception as e:
        log(f"Kunne ikke sende e-post: {e}", "❌")
        return False

def main():
    print("=" * 70)
    print("🌅 NRJ MORGEN - KONSOLIDERT MORGEN-RUTINE v1.0")
    print("=" * 70)
    print(f"📅 Dato: {TOMORROW}")
    print(f"🕐 Startet: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 70)
    print()
    
    try:
        # STEG 1: Søk
        articles = step1_search_news()
        
        if len(articles) < 5:
            log(f"Kun {len(articles)} artikler funnet - avbryter", "❌")
            return 1
        
        # STEG 2: Generer titler
        articles = step2_generate_titles(articles)
        
        # STEG 3: Slett gamle
        step3_delete_old()
        
        # STEG 4: Insert nye
        inserted = step4_insert_articles(articles)
        
        if inserted < 5:
            log(f"Kun {inserted} saker insertet - noe gikk galt", "❌")
            return 1
        
        # STEG 5: Generer showprepp
        showprepp = step5_generate_showprepp(articles)
        
        # STEG 6: Send e-post (valgfritt)
        step6_send_email(showprepp)
        
        # Oppsummering
        print()
        print("=" * 70)
        print("✅ MORGEN-RUTINE FULLFØRT!")
        print("=" * 70)
        print(f"📊 {len(articles)} saker funnet")
        print(f"💾 {inserted} saker insertet til Supabase")
        print(f"📝 Showprepp generert")
        print(f"🕐 Fullført: {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 70)
        
        return 0
        
    except Exception as e:
        log(f"FEIL: {e}", "❌")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
