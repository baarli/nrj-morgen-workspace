#!/usr/bin/env python3
# /root/.openclaw/workspace/scripts/format-title.py
# Formater nyhetstitler til korte, konsise versjoner

import sys
import re

def format_title(original_title):
    """
    Formater en nyhetstittel til kort, konsis versjon.
    Mål: 5-8 ord som forklarer saken 100%
    """
    
    # Fjern alt etter | (kilde/separator)
    title = original_title.split('|')[0].strip()
    
    # Fjern kategorier som "Film", "Instagram" etc etter komma
    title = re.sub(r',\s*(Film|Instagram|TV|Musikk|Sport|Snowboard|Video)\s*$', '', title).strip()
    
    # Fjern vanlige nyhetsfloskler fra STARTEN av tittelen
    fluff_prefixes = [
        'Bildet av ', 'Se bildet av ', 'Video: ', 'BREAKING: ', 'EXCLUSIVE: ',
        'Dette må du vite om ', 'Alt du trenger å vite om ',
        'Nå er det bekreftet: ', 'Endelig: ', 'Slik gikk det: ',
        'Får kritikk for ', 'Raser mot ', 'Sjokkert over ',
        'I hardt vær etter ', 'I trøbbel etter ',
        'Delte emosjonell ', 'Delte rørende ', 'Delte sjokkerende ',
        'Bryter stillheten om ', 'Bryter tauseheten om ',
        'Åpner opp om ', 'Snakker ut om ',
        'Følelsesladd ', 'Hollywoodstjernen ',
    ]
    
    for fluff in fluff_prefixes:
        if title.startswith(fluff):
            title = title[len(fluff):].strip()
    
    # Fjern parenteser med innhold
    title = re.sub(r'\([^)]*\)', '', title).strip()
    
    # Håndter kolon: behold etter kolon hvis første del er kategori/kontekst
    if ':' in title:
        parts = title.split(':')
        before_colon = parts[0].strip()
        after_colon = ':'.join(parts[1:]).strip()
        
        # Hvis første del er kort (1-3 ord), kombiner med etter
        if len(before_colon.split()) <= 3 and after_colon:
            # Sjekk om første del er et navn
            if ',' in before_colon or ' og ' in before_colon.lower():
                title = f"{before_colon}: {after_colon}"
            else:
                title = after_colon
        else:
            title = before_colon
    
    # Håndter bindestrek
    for separator in [' – ', ' - ']:
        if separator in title:
            parts = title.split(separator)
            before = parts[0].strip()
            after = parts[1].strip() if len(parts) > 1 else ''
            
            # Hvis første del er veldig kort (1-2 ord) og andre del er lengre, kombiner
            if len(before.split()) <= 2 and len(after.split()) >= 3:
                title = f"{before} {after}"
            else:
                title = before
            break
    
    # Spesifikke erstattinger for bedre flyt
    replacements = [
        (r'\bdød\b', 'er død'),
        (r'\bpågrepet\b', 'er pågrepet'),
        (r'\bløslatt\b', 'er løslatt'),
        (r'\bfunnet\b', 'er funnet'),
        (r'\bsiktet\b', 'er siktet'),
        (r'\bdømt\b', 'er dømt'),
        (r'\bfrikjent\b', 'er frikjent'),
    ]
    
    for pattern, replacement in replacements:
        if re.search(pattern, title.lower()) and f' {replacement}' not in title.lower():
            title = re.sub(pattern, replacement, title, count=1, flags=re.IGNORECASE)
    
    # Fjern doble mellomrom
    title = ' '.join(title.split())
    
    # Hvis tittelen er veldig kort (under 4 ord), prøv å hente mer fra original
    words = title.split()
    if len(words) < 4:
        # Hent mer kontekst fra original (før |)
        original_main = original_title.split('|')[0].strip()
        # Fjern det vi allerede har
        remaining = original_main.replace(title, '').strip(' ,:–-')
        if remaining and len(remaining.split()) >= 2:
            title = f"{title} {remaining}"
            title = ' '.join(title.split()[:8])  # Begrens til 8 ord
    
    # Begrens lengde til maks 8 ord
    words = title.split()
    if len(words) > 8:
        title = ' '.join(words[:8]) + '...'
    
    # Fjern trailing punctuation
    title = title.rstrip('.,;:').strip()
    
    # Store forbokstav
    if title:
        title = title[0].upper() + title[1:]
    
    return title.strip()

# Test med eksempler
test_titles = [
    ("Andrew Mountbatten Windsor, Prins Andrew | Bildet av en sjokkskadet Andrew Mountbatten-Windsor fyller avisforsider over hele verden", 
     "Prins Andrew på forsiden etter pågripelse"),
    ("Andrew Mountbatten-Windsor løslatt fra politistasjonen etter pågripelse",
     "Prins Andrew er løslatt fra politistasjonen"),
    ("Durek Verrett, Mette-Marit | Følelsesladd Durek Verret snakker om Epstein-skandalen og Mette-Marit",
     "Durek Verrett om Epstein og Mette-Marit"),
    ("Amanda Bynes, Instagram | Hollywoodstjernen er ugjenkjennelig",
     "Amanda Bynes er ugjenkjennelig"),
    ("Prinsesse Désirée av Sverige død: Kongelig begravelse i Västergötland",
     "Prinsesse Désirée er død"),
    ("Ida Elise Broch, Film | Bønn til arbeidsgivere: – Mulig jeg må takke ja til den kaféen på Grønland",
     "Ida Elise Broch søker ny jobb"),
    ("Christy Carlson Romano deler emosjonell helseoppdatering på Instagram",
     "Christy Carlson Romano deler helseoppdatering"),
    ("Vinter-OL 2026, Snowboard | Ny skrekkulykke i OL – gullfavoritt fraktet vekk på båre",
     "Skrekkulykke i OL – gullfavoritt på båre"),
]

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Formater enkelt tittel
        print(format_title(' '.join(sys.argv[1:])))
    else:
        # Test alle eksempler
        print("📝 TITTEL-FORMATERING")
        print("=" * 80)
        for original, expected in test_titles:
            formatted = format_title(original)
            word_count = len(formatted.split())
            print(f"\nOriginal:  {original[:60]}...")
            print(f"Formatert: {formatted}")
            print(f"Forventet: {expected}")
            print(f"Ord: {word_count}")
