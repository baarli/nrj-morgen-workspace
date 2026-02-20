#!/usr/bin/env python3
# /root/.openclaw/workspace/scripts/ai-generate-title.py
# Bruk AI (via kimi) for å generere konsise, informative titler

import sys
import subprocess
import json

def generate_title_with_kimi(original_title, description=""):
    """
    Bruk kimi for å generere en kort, konsis tittel.
    """
    
    prompt = f"""Formater denne nyhetstittelen til en kort, konsis versjon på 5-7 ord.

Original tittel: {original_title}
Beskrivelse: {description}

Regler:
- Maks 7 ord
- Inkluder hovedperson + handling
- Gjør den umiddelbart forståelig
- Fjern unødvendige detaljer
- Bruk aktiv form

Eksempler:
"Prins Andrew Mountbatten-Windsor løslatt fra politistasjonen etter pågripelse" → "Prins Andrew er løslatt fra politiet"
"Ida Elise Broch, Film - Bønn til arbeidsgivere om ny jobb" → "Ida Elise Broch søker ny jobb"
"Durek Verrett snakker om Epstein-skandalen og Mette-Marit" → "Durek Verrett om Epstein og Mette-Marit"

Gi KUN den formaterte tittelen, ingen forklaring:"""

    try:
        # Bruk kimi_search via subprocess (simulert)
        # I praksis ville dette kalt en faktisk AI-tjeneste
        
        # Foreløpig: bruk enkel regel-basert formatering
        return simple_format(original_title, description)
        
    except Exception as e:
        print(f"Feil: {e}", file=sys.stderr)
        return simple_format(original_title, description)

def simple_format(title, description=""):
    """
    Enkel formatering basert på regler.
    """
    import re
    
    # Fjern alt etter |
    title = title.split('|')[0].strip()
    
    # Fjern kategorier etter komma
    title = re.sub(r',\s*(Film|Instagram|TV|Musikk|Sport|Snowboard|Video)\s*$', '', title).strip()
    
    # Fjern fluff
    fluff = [
        'Bildet av ', 'Se bildet av ', 'Video: ', 'BREAKING: ',
        'Følelsesladd ', 'Hollywoodstjernen ', 'Delte emosjonell ',
        'Bryter stillheten om ', 'Åpner opp om ',
    ]
    for f in fluff:
        if title.startswith(f):
            title = title[len(f):].strip()
    
    # Håndter kolon
    if ':' in title:
        parts = title.split(':')
        if len(parts[0].split()) <= 3:
            title = ':'.join(parts[1:]).strip()
        else:
            title = parts[0].strip()
    
    # Håndter bindestrek
    for sep in [' – ', ' - ']:
        if sep in title:
            parts = title.split(sep)
            if len(parts[0].split()) <= 2:
                title = f"{parts[0]} {parts[1]}"
            else:
                title = parts[0]
            break
    
    # Erstatt verb
    replacements = [
        (r'\bdød\b', 'er død'),
        (r'\bpågrepet\b', 'er pågrepet'),
        (r'\bløslatt\b', 'er løslatt'),
    ]
    for pattern, repl in replacements:
        title = re.sub(pattern, repl, title, flags=re.IGNORECASE)
    
    # Hvis veldig kort, bruk beskrivelse
    words = title.split()
    if len(words) < 4 and description:
        # Trekk ut hovedinfo fra beskrivelse
        desc_words = description.split()[:5]
        title = f"{title} {' '.join(desc_words)}"
    
    # Begrens
    words = title.split()
    if len(words) > 7:
        title = ' '.join(words[:7])
    
    return title.strip()

def main():
    if len(sys.argv) < 2:
        print("Bruk: ai-generate-title.py 'original tittel' ['beskrivelse']")
        sys.exit(1)
    
    original = sys.argv[1]
    description = sys.argv[2] if len(sys.argv) > 2 else ""
    
    formatted = generate_title_with_kimi(original, description)
    print(formatted)

if __name__ == '__main__':
    main()
