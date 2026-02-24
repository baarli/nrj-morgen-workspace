#!/bin/bash
# summarize.sh - Lokal summarize funksjon
# Bruker kimi_fetch + OpenAI/Anthropic API

URL="$1"
MODEL="${2:-anthropic/claude-3-5-sonnet}"

if [ -z "$URL" ]; then
  echo "Bruk: summarize.sh <URL> [model]"
  echo "Eksempel: summarize.sh https://example.com"
  exit 1
fi

echo "Henter innhold fra $URL..."

# Bruk python med requests for å hente innhold
python3 << 'EOF'
import sys
import os
import json

try:
    import requests
    from bs4 import BeautifulSoup
    
    url = sys.argv[1]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Fjern script og style
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Hent tekst
    text = soup.get_text()
    
    # Rens tekst
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    
    # Begrens lengde
    if len(text) > 8000:
        text = text[:8000] + "..."
    
    print(text)
    
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
EOF
"$URL" 2>/tmp/summarize_error.log

if [ $? -ne 0 ]; then
  echo "Kunne ikke hente innhold fra URL"
  cat /tmp/summarize_error.log
  exit 1
fi
