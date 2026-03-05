#!/usr/bin/env python3
"""
Generer showprepp fra saker i Supabase og send på e-post
"""

import json
import os
import requests
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Konfigurasjon
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"
TENANT_ID = "a0000000-0000-0000-0000-000000000001"

def fetch_articles():
    """Hent saker fra Supabase"""
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    
    today = datetime.now().strftime("%Y-%m-%d")
    url = f"{SUPABASE_URL}/rest/v1/agenda_items?select=*&tenant_id=eq.{TENANT_ID}&show_date=eq.{today}&category=eq.TALK&order=order_index.asc"
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def generate_showprep(articles):
    """Generer showprepp fra artikler"""
    
    today = datetime.now().strftime("%d.%m.%Y")
    html = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
    <h1 style="color: #ff6b00;">🎙️ NRJ MORGEN - Showprepp {today}</h1>
    <hr>
    
    <h2>📰 Topp 8 saker med innganger:</h2>
"""
    
    for i, article in enumerate(articles[:8], 1):
        title = article.get('title', '')
        notes = article.get('notes', '')
        link_url = article.get('link_url', '')
        description = article.get('description', '')
        
        # Fjern HTML-tags fra description for ren tekst
        import re
        clean_desc = re.sub(r'<[^>]+>', '', description or '')
        
        html += f"""
    <div style="margin-bottom: 25px; padding: 15px; background: #f5f5f5; border-radius: 8px;">
        <h3>{i}. {title}</h3>
        <p><strong>Essens:</strong> {clean_desc[:200]}...</p>
        <p><strong>Talking points:</strong> {notes}</p>
        <p><a href="{link_url}" style="color: #ff6b00;">Les mer →</a></p>
    </div>
"""
    
    html += """
    <hr>
    <h2>🎧 Segment-forslag (10 min hver):</h2>
    
    <div style="margin-bottom: 15px;">
        <h3>Segment 1: Kongefamilien-drama (05:00-05:10)</h3>
        <ul>
            <li>Märtha Louise i Spania - grusom situasjon</li>
            <li>NRK Humoretaten - Marius Borg Høiby-sjokk</li>
            <li>Epstein-storm mot politikere</li>
        </ul>
    </div>
    
    <div style="margin-bottom: 15px;">
        <h3>Segment 2: Kjendis-nytt (05:10-05:20)</h3>
        <ul>
            <li>Netflix-dokumentar om Tyra Banks</li>
            <li>Renate Reinsve på BAFTA-rød løper</li>
            <li>Dolph Lundgren - aldersforskjell-debatt</li>
        </ul>
    </div>
    
    <div style="margin-bottom: 15px;">
        <h3>Segment 3: Underholdning & Kultur (05:20-05:30)</h3>
        <ul>
            <li>Bjørn Eidsvåg - Hver gang vi møtes</li>
            <li>Aksel Hennie - bot på 124.000 kr</li>
            <li>Paradise Hotel - situasjonen i Mexico</li>
        </ul>
    </div>
    
    <hr>
    <h2>😂 Dagens vits:</h2>
    <p style="font-style: italic; padding: 15px; background: #fff3cd; border-radius: 8px;">
        Hvorfor gikk kongen til psykolog? Fordi han hadde trone-problemer!
    </p>
    
    <hr>
    <h2>🎙️ Podkast-forslag:</h2>
    <ul>
        <li><strong>Baarli og Benjamin går i terapi</strong> - Siste episode</li>
        <li><strong>Gylne tider</strong> - TV2-nyheter</li>
    </ul>
    
    <hr>
    <p style="color: #666; font-size: 12px;">
        Generert av BaarliClaw 🤖 | {datetime.now().strftime("%H:%M")}
    </p>
</body>
</html>
"""
    return html

def send_email(html_content):
    """Send e-post med showprepp"""
    
    # Gmail-konfigurasjon
    gmail_user = "baarliclaw@gmail.com"
    gmail_password = "urarfguqcvpxofft"  # App-spesifikt passord
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"🎙️ NRJ MORGEN - Showprepp {datetime.now().strftime('%d.%m.%Y')}"
    msg['From'] = gmail_user
    msg['To'] = "niklasbaarli@gmail.com"
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Feil ved sending av e-post: {e}")
        return False

def main():
    print("📰 Henter saker fra Supabase...")
    articles = fetch_articles()
    print(f"   ✅ Fant {len(articles)} saker")
    
    if not articles:
        print("❌ Ingen saker funnet!")
        return
    
    print("📝 Genererer showprepp...")
    showprep = generate_showprep(articles)
    
    # Lagre til fil
    output_file = f"/tmp/showprep-{datetime.now().strftime('%Y-%m-%d')}.html"
    with open(output_file, 'w') as f:
        f.write(showprep)
    print(f"   ✅ Lagret til {output_file}")
    
    print("📧 Sender e-post...")
    if send_email(showprep):
        print("   ✅ E-post sendt til niklasbaarli@gmail.com")
    else:
        print("   ❌ Kunne ikke sende e-post")

if __name__ == "__main__":
    main()
