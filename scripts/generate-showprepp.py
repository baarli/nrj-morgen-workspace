#!/usr/bin/env python3
"""
Generer SHOWPREPP for NRJ Morgen basert på saker i Supabase
"""

import json
import urllib.request
import urllib.parse
import os
from datetime import datetime, timedelta

SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"
TENANT_ID = "a0000000-0000-0000-0000-000000000001"

def supabase_request(method, path, params=None):
    url = f"{SUPABASE_URL}/rest/v1{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json'
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Feil: {e}")
        return []

def generate_showprepp():
    TOMORROW = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Hent saker
    articles = supabase_request(
        'GET',
        '/agenda_items',
        params={
            'tenant_id': f'eq.{TENANT_ID}',
            'show_date': f'eq.{TOMORROW}',
            'select': 'title,description,notes,link_url',
            'order': 'created_at.desc'
        }
    )
    
    if not articles:
        print("Ingen saker funnet")
        return None
    
    # Generer showprepp
    date_str = datetime.now().strftime('%A %d. %B').capitalize()
    
    showprepp = f"""# 📻 NRJ MORGEN SHOWPREPP
## {date_str}

---

## 🎯 Topp 8 Saker (Prioritert)

"""
    
    # Topp 8 saker
    for i, article in enumerate(articles[:8], 1):
        title = article.get('title', 'Ukjent')
        notes = article.get('notes', '')
        url = article.get('link_url', '')
        
        # Hent første setning fra notes
        first_line = notes.split('\n')[0] if notes else ''
        
        showprepp += f"""### {i}. {title}
**Inngang:** {first_line[:100]}{'...' if len(first_line) > 100 else ''}

**Talking points:**
• Hva er det mest interessante her?
• Hvilken vinkel skal vi ta?
• Hvem kan vi ringe?

📎 [Les mer]({url})

---

"""
    
    # Segment-forslag
    showprepp += """## 📻 Segment-forslag

### Segment 1 (06:00-06:10): Åpning
• Velkommen til fredag!
• Topp-sak: Marius Borg Høiby-rettssaken
• Værmelding + trafikk

### Segment 2 (06:10-06:20): Kjendis-drama
• Cody Simpson & Emma McKeon brudd
• Sophie Elise PR-stunt påstander
• Jon Øigarden nabokrangel

### Segment 3 (06:20-06:30): Kongehus & Reality
• Kronprinsparet visste - men stoppet det ikke
• Farmen Kjendis / Paradise Hotel oppdateringer
• Lytter-interaksjon

---

## 🎭 Dagens Vits

*Hvorfor gikk skuespilleren til legen?*

Fordi han hadde **scene**-vansker! 😄

---

## 🎧 Podkast-forslag

**Baarli og Benjamin går i terapi**
• Siste episode: "Handleapp, hyperfokus og husfred"
• God morgen-humor
• Perfekt for fredagsstemning

---

## 📊 Konkurrent-status

• **P3**: Fokus på ny musikk & kultur
• **Radio Norge**: Kjendisnyheter
• **Vår edge**: Raskere, mer underholdende, bedre kjemi

---

## ⚡ Quick Hits (Hvis tid)

"""
    
    # Resten av sakene som quick hits
    for i, article in enumerate(articles[8:], 9):
        title = article.get('title', '')
        url = article.get('link_url', '')
        showprepp += f"{i}. {title} - [Les mer]({url})\n"
    
    showprepp += f"""
---

## 📝 Notater

*Plass til egne notater under sending...*

---

**Generert:** {datetime.now().strftime('%H:%M')} | **Kimi Claw** 🤖
"""
    
    return showprepp

def main():
    print("📝 Genererer SHOWPREPP...")
    
    showprepp = generate_showprepp()
    
    if not showprepp:
        return 1
    
    # Lagre til fil
    date_str = datetime.now().strftime('%Y-%m-%d')
    os.makedirs('/root/.openclaw/workspace/brain/reports', exist_ok=True)
    
    report_file = f'/root/.openclaw/workspace/brain/reports/daily-report-{date_str}.md'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(showprepp)
    
    print(f"✅ Showprepp lagret til: {report_file}")
    print(f"\n📊 {len(showprepp)} tegn")
    
    # Print første del
    print("\n--- FØRSTE DEL AV SHOWPREPP ---")
    print(showprepp[:1000])
    print("...")
    
    return 0

if __name__ == '__main__':
    exit(main())
