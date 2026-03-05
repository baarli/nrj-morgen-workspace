#!/usr/bin/env python3
# /root/.openclaw/workspace/scripts/final-title-generator.py
# Final title generator - extracts person and key action

import sys
import re

def generate_title(title, description=""):
    """Generate concise title from news article."""
    
    # Clean title
    title = title.split('|')[0].strip()
    title = re.sub(r',\s*(Film|Instagram|TV|Musikk|Sport|Snowboard)\s*$', '', title).strip()
    
    # Extract person name (first 2-3 capitalized words)
    words = title.split()
    person = []
    for word in words[:4]:
        if word[0].isupper():
            person.append(word)
        elif person:
            break
    person = ' '.join(person[:3]) if person else words[0] if words else ""
    
    # Determine action from description or title
    text = (description + " " + title).lower()
    
    # Action mapping
    if 'søker' in text and 'jobb' in text:
        action = "søker ny jobb"
    elif 'pågrepet' in text or 'arrestert' in text:
        action = "er pågrepet"
    elif 'løslatt' in text or 'sluppet fri' in text:
        action = "er løslatt"
    elif 'død' in text or 'døde' in text or 'gått bort' in text:
        action = "er død"
    elif 'skilt' in text or 'brudd' in text:
        action = "har gått fra partner"
    elif 'gravid' in text or 'venter barn' in text:
        action = "venter barn"
    elif 'syk' in text or 'sykehus' in text:
        action = "er syk"
    elif 'ugjenkjennelig' in text:
        action = "er ugjenkjennelig"
    elif 'skandale' in text:
        action = "i skandale"
    elif 'snakker' in text or 'bryter stillheten' in text:
        # Extract topic after "om"
        match = re.search(r'om\s+([^.,:;]+)', description.lower())
        if match:
            topic = match.group(1).strip()
            topic = ' '.join(topic.split()[:3])  # Max 3 words
            action = f"om {topic}"
        else:
            action = "snakker ut"
    else:
        # Extract remaining words from title after person
        person_words = len(person.split())
        remaining = words[person_words:]
        # Remove common stop words
        stop_words = ['fra', 'til', 'på', 'i', 'med', 'etter', 'om', 'av']
        remaining = [w for w in remaining if w.lower() not in stop_words]
        action = ' '.join(remaining[:4])
    
    # Combine
    if person and action:
        result = f"{person} {action}"
    else:
        result = person or ' '.join(words[:5])
    
    # Clean up
    result = result.strip()
    result = re.sub(r'\s+', ' ', result)
    result = result.rstrip('.,;:')
    
    # Limit length
    result_words = result.split()
    if len(result_words) > 7:
        result = ' '.join(result_words[:7])
    
    return result.capitalize() if result else result

def main():
    if len(sys.argv) < 2:
        print("Usage: final-title-generator.py 'title' ['description']")
        sys.exit(1)
    
    title = sys.argv[1]
    desc = sys.argv[2] if len(sys.argv) > 2 else ""
    
    print(generate_title(title, desc))

if __name__ == '__main__':
    main()
