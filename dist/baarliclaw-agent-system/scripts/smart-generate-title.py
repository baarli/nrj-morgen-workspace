#!/usr/bin/env python3
# /root/.openclaw/workspace/scripts/smart-generate-title.py
# Smart tittel-generering med forbedret regel-basert tilnærming

import sys
import re

def smart_generate_title(original_title, description=""):
    """
    Generer en konsis, informativ tittel basert på original og beskrivelse.
    """
    
    # Start med original tittel
    title = original_title.strip()
    
    # Fjern alt etter | (kilde)
    title = title.split('|')[0].strip()
    
    # Fjern kategorier etter komma
    title = re.sub(r',\s*(Film|Instagram|TV|Musikk|Sport|Snowboard|Video)\s*$', '', title).strip()
    
    # Trekk ut hovedperson (første 2-3 ord som ser ut som navn)
    words = title.split()
    name_words = []
    for word in words:
        if word[0].isupper() and len(word) > 1:
            name_words.append(word)
        elif name_words:
            break
    
    # Maks 3 navne-ord
    if len(name_words) > 3:
        name_words = name_words[:3]
    
    main_person = ' '.join(name_words) if name_words else words[0] if words else ""
    
    # Analyser beskrivelse for handling
    action = ""
    if description:
        desc_lower = description.lower()
        
        # Sjekk for vanlige handlinger (prioritert rekkefølge)
        action_patterns = [
            (r'\b(søker|leter|vil ha)\b.*\b(jobb|arbeid|stilling)\b', 'søker ny jobb'),
            (r'\b(søker|leter|vil ha)\b.*\b(leilighet|bolig|hus)\b', 'søker ny bolig'),
            (r'\b(pågrepet|arrestert)\b', 'er pågrepet'),
            (r'\b(løslatt|frikjent|sluppet fri)\b', 'er løslatt'),
            (r'\b(død|gått bort|sovet inn)\b', 'er død'),
            (r'\b(skilt|brudd|separert)\b', 'har gått fra partner'),
            (r'\b(gravid|venter barn|blir foreldre)\b', 'venter barn'),
            (r'\b(syk|innlagt|sykehus|sykdom)\b', 'er syk'),
            (r'\b(kritikk|raser|angrep)\b', 'får kritikk'),
            (r'\b(snakker|åpner|forteller)\b.*\bom\b', None),  # Spesiell håndtering
        ]
        
        for pattern, replacement in action_patterns:
            if re.search(pattern, desc_lower):
                if replacement:
                    action = replacement
                else:
                    # For "snakker om", trekk ut tema
                    about_match = re.search(r'om\s+([^.,]+)', description.lower())
                    if about_match:
                        topic = about_match.group(1).strip()
                        # Begrens tema-lengde
                        topic_words = topic.split()
                        if len(topic_words) > 3:
                            topic = ' '.join(topic_words[:3])
                        action = f"om {topic}"
                    else:
                        action = "snakker ut"
                break
    
    # Hvis vi ikke fant handling i beskrivelse, analyser tittelen
    if not action:
        title_lower = title.lower()
        
        title_actions = [
            ('pågrepet', 'er pågrepet'),
            ('løslatt', 'er løslatt'),
            ('død', 'er død'),
            ('skilt', 'har gått fra partner'),
            ('ugjenkjennelig', 'er ugjenkjennelig'),
            ('skandale', 'i skandale'),
        ]
        
        for keyword, act in title_actions:
            if keyword in title_lower:
                action = act
                break
        
        if not action:
            # Generisk handling: bruk verb fra tittel etter navn
            name_word_count = len(main_person.split())
            if len(words) > name_word_count:
                action_words = words[name_word_count:]
                # Fjern fluff-ord
                fluff = ['fra', 'til', 'på', 'i', 'med', 'om', 'etter']
                action_words = [w for w in action_words if w.lower() not in fluff]
                action = ' '.join(action_words[:4])
    
    # Bygg ny tittel
    if main_person and action:
        new_title = f"{main_person} {action}"
    elif main_person:
        new_title = main_person
    else:
        new_title = ' '.join(words[:5])  # Fallback
    
    # Rens og formater
    new_title = new_title.strip()
    new_title = re.sub(r'\s+', ' ', new_title)
    new_title = new_title.rstrip('.,;:')
    
    # Begrens lengde
    final_words = new_title.split()
    if len(final_words) > 7:
        new_title = ' '.join(final_words[:7])
    
    # Store forbokstav
    if new_title:
        new_title = new_title[0].upper() + new_title[1:]
    
    return new_title

def main():
    if len(sys.argv) < 2:
        print("Bruk: smart-generate-title.py 'original tittel' ['beskrivelse']")
        sys.exit(1)
    
    original = sys.argv[1]
    description = sys.argv[2] if len(sys.argv) > 2 else ""
    
    formatted = smart_generate_title(original, description)
    print(formatted)

if __name__ == '__main__':
    main()
