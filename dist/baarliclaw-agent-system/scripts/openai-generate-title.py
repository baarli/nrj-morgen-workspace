#!/usr/bin/env python3
# /root/.openclaw/workspace/scripts/openai-generate-title.py
# Bruk OpenAI GPT-4 for å generere konsise, informative titler

import os
import sys
import json
import urllib.request
import urllib.error

def load_credentials():
    """Last API-nøkkel fra credentials"""
    env_file = '/root/.openclaw/workspace/.credentials/live-search.env'
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=', 1)[1].strip().strip('"').strip("'")
    return None

def generate_title_with_openai(original_title, description=""):
    """
    Bruk OpenAI GPT-4 for å generere en kort, konsis tittel.
    """
    api_key = load_credentials()
    
    if not api_key:
        print("❌ Ingen OpenAI API-nøkkel funnet", file=sys.stderr)
        return None
    
    prompt = f"""Formater denne nyhetstittelen til en kort, konsis versjon på 5-7 ord for en radiomorgensending.

Original tittel: {original_title}
Beskrivelse: {description}

Krav:
- Maks 7 ord, helst 5-6
- Inkluder hovedperson (navn) + handling
- Gjør den umiddelbart forståelig for lyttere
- Fjern unødvendige detaljer og fluff
- Bruk aktiv form
- Skriv på norsk

Eksempler på gode titler:
- "Ida Elise Broch søker ny jobb"
- "Prins Andrew er løslatt fra politiet"  
- "Durek Verrett om Epstein og Mette-Marit"
- "Amanda Bynes er ugjenkjennelig"
- "Prinsesse Désirée av Sverige er død"

Gi KUN den formaterte tittelen, ingen forklaring eller anførselstegn:"""

    try:
        url = "https://api.openai.com/v1/chat/completions"
        
        data = {
            "model": "gpt-4o-mini",  # Rask og rimelig modell
            "messages": [
                {"role": "system", "content": "Du er en erfaren nyhetsredaktør for NRK P3 og NRJ Morgen. Din jobb er å lage korte, fengende titler som umiddelbart forteller hva saken handler om."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 50
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
            result = json.loads(response.read().decode('utf-8'))
            generated_title = result['choices'][0]['message']['content'].strip()
            
            # Fjern anførselstegn hvis AI la dem til
            generated_title = generated_title.strip('"').strip("'")
            
            return generated_title
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"❌ OpenAI API feil: {e.code} - {error_body}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ Feil: {e}", file=sys.stderr)
        return None

def main():
    if len(sys.argv) < 2:
        print("Bruk: openai-generate-title.py 'original tittel' ['beskrivelse']")
        sys.exit(1)
    
    original = sys.argv[1]
    description = sys.argv[2] if len(sys.argv) > 2 else ""
    
    print(f"🤖 Genererer tittel med OpenAI...")
    print(f"Original: {original[:60]}...")
    
    formatted = generate_title_with_openai(original, description)
    
    if formatted:
        print(f"\n✅ Generert tittel:")
        print(formatted)
        print(f"Lengde: {len(formatted.split())} ord")
    else:
        print("\n❌ Kunne ikke generere tittel")
        sys.exit(1)

if __name__ == '__main__':
    main()
