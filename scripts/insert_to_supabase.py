#!/usr/bin/env python3
"""
Insert 15 saker fra morning-news.json til Supabase agenda_items
Bruker korrekt format med alle påkrevde felter
"""

import json
import os
import requests
from datetime import datetime

# Konfigurasjon
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"
TENANT_ID = "a0000000-0000-0000-0000-000000000001"
USER_ID = "10aa1508-6d52-490c-8ae5-fa3da9a152c4"
PROFILE_PICTURE = "https://lh3.googleusercontent.com/a/ACg8ocLyiG1iwB_rfOCAN64WGPUUIWprTMX0JfUDsoy7dHkd6AVdaQ=s96-c"

def get_image_for_source(source):
    """Fallback-bilder for ulike kilder"""
    fallbacks = {
        "www.seher.no": "https://www.seher.no/logo.png",
        "www.dagbladet.no": "https://www.dagbladet.no/logo.png",
        "dagbladet.no": "https://www.dagbladet.no/logo.png",
        "www.tv2.no": "https://www.tv2.no/logo.png",
        "www.nrk.no": "https://www.nrk.no/logo.png",
        "www.dailymail.co.uk": "https://www.dailymail.co.uk/logo.png",
        "www.nettavisen.no": "https://www.nettavisen.no/logo.png"
    }
    return fallbacks.get(source, "")

def insert_article(article, order_index):
    """Insert en artikkel til Supabase"""
    
    title = article.get("title", "")
    description = article.get("description", "")
    url = article.get("url", "")
    source = article.get("source", "")
    summary = article.get("summary", "")
    why_nrj = article.get("why_nrj", "")
    published = article.get("publishedAt", "")
    
    # Lag notes med oppsummering
    first_sentence = description.split(".")[0] if description else ""
    notes = f"{first_sentence}\n\nKilde: {source}"
    if why_nrj:
        notes += f"\nHvorfor NRJ: {why_nrj}"
    
    # Lag link_metadata med bilde
    image_url = get_image_for_source(source)
    link_metadata = json.dumps({"image_url": image_url}) if image_url else None
    
    # Lag description med HTML-bilde
    if image_url:
        html_description = f'<img src="{image_url}" alt="{title}" style="max-width:100%;border-radius:8px;margin-bottom:12px;" />\n\n{description}'
    else:
        html_description = description
    
    # Bygg payload
    payload = {
        "tenant_id": TENANT_ID,
        "title": title,
        "description": html_description,
        "notes": notes,
        "link_url": url,
        "link_metadata": link_metadata,
        "category": "TALK",
        "show_date": datetime.now().strftime("%Y-%m-%d"),
        "created_by": USER_ID,
        "order_index": order_index,
        "is_pinned": False
    }
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/agenda_items",
        headers=headers,
        json=payload
    )
    
    if response.status_code not in [200, 201]:
        print(f"    Feil: {response.status_code} - {response.text[:200]}")
    
    return response.status_code in [200, 201]

def main():
    # Les artikler fra JSON
    with open("/tmp/morning-news.json", "r") as f:
        data = json.load(f)
    
    articles = data.get("articles", [])
    print(f"📰 Fant {len(articles)} artikler å inserte")
    
    # Insert hver artikkel
    success_count = 0
    for i, article in enumerate(articles):
        if insert_article(article, i):
            print(f"  ✅ {i+1}. {article.get('title', '')[:50]}...")
            success_count += 1
        else:
            print(f"  ❌ {i+1}. Feil ved insert")
    
    print(f"\n🎉 {success_count}/{len(articles)} saker insertet!")
    return success_count

if __name__ == "__main__":
    main()
