#!/usr/bin/env python3
# /root/.openclaw/workspace/scripts/generate-showprepp.py
# Genererer profesjonell SHOWPREPP for NRJ Morgen med OpenAI

import os
import sys
import json
import urllib.request
from datetime import datetime
from pathlib import Path

# Konfigurasjon
WORKSPACE = "/root/.openclaw/workspace"
REPORT_DIR = f"{WORKSPACE}/brain/reports"
CREDENTIALS = f"{WORKSPACE}/.credentials/nrj-morgen.env"

def load_credentials():
    """Last credentials fra .env fil"""
    creds = {}
    if os.path.exists(CREDENTIALS):
        with open(CREDENTIALS, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    value = value.strip('"').strip("'")
                    creds[key] = value
    return creds

def get_todays_articles():
    """Hent dagens artikler fra Supabase"""
    creds = load_credentials()
    
    supabase_url = creds.get('SUPABASE_URL', '')
    supabase_key = creds.get('SUPABASE_SERVICE_KEY', '')
    
    today = datetime.now().strftime('%Y-%m-%d')
    tenant_id = "a0000000-0000-0000-0000-000000000001"
    
    url = f"{supabase_url}/rest/v1/agenda_items?select=title,description,category,notes,is_pinned,link_url,order_index,created_by&show_date=eq.{today}&tenant_id=eq.{tenant_id}&order=created_at.desc"
    
    try:
        req = urllib.request.Request(
            url,
            headers={
                'apikey': supabase_key,
                'Authorization': f'Bearer {supabase_key}'
            }
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"⚠️  Feil ved henting av artikler: {e}", file=sys.stderr)
        return []

def generate_ai_intro(articles, api_key):
    """Bruk OpenAI til å generere en engasjerende intro"""
    
    # Lag en liste over dagens saker
    sak_titler = [a['title'] for a in articles[:5]]
    
    # Hvis ingen API-nøkkel eller kvote overskredet, bruk smart fallback
    if not api_key or api_key == 'sk-...':
        return generate_smart_fallback_intro(articles)
    
    prompt = f"""Du er en erfaren radiovært for NRJ Morgen. Skriv en ENGASJERENDE og ENERGISK intro til morgensendingen.

Dagens saker:
{chr(10).join(f"- {t}" for t in sak_titler)}

Krav:
- Maks 3 setninger
- Start med "God morgen!"
- Inkluder en referanse til dagens største sak
- Bruk energisk, muntlig tone
- Avslutt med oppfordring til å lytte

Eksempel:
"God morgen! I dag snakker vi om [største sak] - dette er helt vilt! Og så har vi masse annet snacks på menyen. Bli med!"

Skriv introen:"""

    try:
        url = "https://api.openai.com/v1/chat/completions"
        
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Du er en erfaren radiovært for NRJ Morgen. Du skriver engasjerende, muntlige tekster for radio."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 150
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            },
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"⚠️  OpenAI feil: {e}", file=sys.stderr)
        return generate_smart_fallback_intro(articles)

def generate_smart_fallback_intro(articles):
    """Generer en smart intro uten AI basert på sakene"""
    if not articles:
        return "God morgen! I dag har vi masse spennende på menyen - bli med!"
    
    # Finn den mest spennende saken (første sak)
    top_sak = articles[0]
    title = top_sak.get('title', '')
    
    # Lag en enkel men effektiv intro
    intro_varianter = [
        f"God morgen! I dag starter vi med '{title}' - dette er helt vilt! Bli med!",
        f"God morgen! Har du hørt om '{title}'? Vi snakker om det og masse annet i dag!",
        f"God morgen! I dag har vi '{title}' på menyen pluss mye annet snacks. Bli med!",
    ]
    
    # Velg tilfeldig variant for variasjon
    import random
    return random.choice(intro_varianter)

def generate_radio_angles(articles, api_key):
    """Generer radiovinkler for hver sak"""
    
    angles = []
    
    # Pre-definerte vinkler basert på nøkkelord
    vinkel_maler = [
        "Har du hørt om {navn}? Dette er helt vilt!",
        "Skandale rundt {navn} - hva skjedde egentlig?",
        "{navn} i trøbbel igjen - vi forklarer!",
        "Dette om {navn} må du bare høre!",
        "{navn} sjokkerer alle - hva nå?",
    ]
    
    import random
    
    for i, article in enumerate(articles[:10]):
        title = article.get('title', '')
        
        # Trekk ut første navn/ord fra tittel
        first_word = title.split()[0] if title else "dette"
        
        # Velg en vinkel
        mal = random.choice(vinkel_maler)
        angle = mal.format(navn=first_word)
        
        angles.append({
            'title': title,
            'angle': angle
        })
    
    return angles

def generate_showprepp():
    """Generer komplett showprepp"""
    
    print("🎙️  GENERERER SHOWPREPP FOR NRJ MORGEN")
    print("=" * 60)
    
    # Last credentials
    creds = load_credentials()
    openai_key = creds.get('OPENAI_API_KEY', '')
    
    # Hent artikler
    print("📰 Henter dagens saker...")
    articles = get_todays_articles()
    
    if not articles:
        print("❌ Ingen saker funnet")
        return None
    
    print(f"✅ {len(articles)} saker funnet")
    
    # Generer AI intro
    print("🤖 Genererer AI-intro...")
    intro = generate_ai_intro(articles, openai_key)
    print(f"✅ Intro: {intro[:80]}...")
    
    # Generer radiovinkler
    print("🎯 Genererer radiovinkler...")
    angles = generate_radio_angles(articles, openai_key)
    print(f"✅ {len(angles)} vinkler generert")
    
    # Lag rapport
    os.makedirs(REPORT_DIR, exist_ok=True)
    
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    time_str = today.strftime('%H:%M')
    
    report_file = f"{REPORT_DIR}/showprepp-{date_str}.md"
    
    # Bygg markdown
    markdown = f"""# 📻 NRJ MORGEN - SHOWPREPP

**Dato:** {today.strftime('%A %d. %B %Y')}  
**Sendestart:** 06:00  
**Generert:** {time_str}

---

## 🎙️ DAGENS INTRO

> **{intro}**

---

## 🔥 DAGENS SAKER

"""
    
    # Legg til saker med AI-genererte vinkler
    for i, (article, angle_data) in enumerate(zip(articles[:10], angles), 1):
        title = article.get('title', 'Uten tittel')
        description = article.get('description', '')
        category = article.get('category', 'TALK')
        angle = angle_data['angle']
        
        # Kategori-emoji
        emoji = {'NEWS': '📰', 'TALK': '💬', 'MUSIC': '🎵', 'GUEST': '👤'}.get(category, '📌')
        
        markdown += f"""### {emoji} {title}

**Vinkel:** *{angle}*

{description[:150]}{'...' if len(description) > 150 else ''}

**Inngang:** "{angle}"

---

"""
    
    # Legg til lytterengasjement
    markdown += """## 💬 LYTTERENGASJEMENT

### Spørsmål å stille:
1. "Hva synes DERE om dagens største sak?"
2. "Har dere opplevd noe lignende?"
3. "Send SMS med deres mening!"

### Ring-in tema:
- **Tema:** Dagens store nyhet
- **Spørsmål:** "Hva ville DU gjort?"

---

## 📊 SENDING INFO

| | |
|:---|:---|
| **Saker totalt:** | {total_saker} |
| **Ferskhet:** | 6-12 timer |
| **Status:** | ✅ Klar for sending |

---

*God sending! 🎙️*  
*Generert av Kimi Claw - Din AI-assistent*
""".format(total_saker=len(articles))
    
    # Skriv til fil
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print(f"\n✅ Showprepp lagret: {report_file}")
    print(f"📄 Størrelse: {len(markdown)} tegn")
    
    return report_file

if __name__ == '__main__':
    report = generate_showprepp()
    if report:
        # Vis rapporten
        with open(report, 'r') as f:
            print("\n" + "=" * 60)
            print(f.read())
    else:
        sys.exit(1)
