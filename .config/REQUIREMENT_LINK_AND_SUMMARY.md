# KRAV: Alle saker i sakslista MÅ ha lenke og notat

## Dato: 2026-02-21
## Ansvarlig: Kimi Claw
## Status: ✅ IMPLEMENTERT

---

## KRAVSPECIFIKASJON

### Hver sak i sakslista skal ha:

1. **Lenke (URL)** til original artikkel
   - Felt: `link_url`
   - Type: String (URL)
   - Påkrevd: Ja

2. **Notat med oppsummering**
   - Felt: `notes`
   - Type: String
   - Format: "[Første setning fra beskrivelse]\n\nKilde: [Kildenavn]"
   - Påkrevd: Ja

---

## IMPLEMENTASJON

### 1. brave-news-search.py
```python
# Lag oppsummerende notat for hver artikkel
summary = create_summary(description, source)

article = {
    'title': title,
    'description': description,
    'url': url,                    # ← Lenke
    'source': source,
    'publishedAt': publishedAt,
    'summary': summary             # ← Notat med oppsummering
}
```

### 2. create_summary() funksjon
```python
def create_summary(description, source):
    """Lag et kort oppsummerende notat av saken"""
    if not description:
        return f"Kilde: {source}"
    
    # Trekk ut første setning
    first_sentence = description.split('.')[0].strip()
    
    # Begrens lengde
    if len(first_sentence) > 150:
        first_sentence = first_sentence[:147] + "..."
    
    # Lag oppsummering
    summary = f"{first_sentence}\n\nKilde: {source}"
    
    return summary
```

### 3. integrated-morning-routine.sh (Insert til Supabase)
```python
payload = {
    "tenant_id": TENANT_ID,
    "title": title,
    "description": article.get('description', ''),
    "category": "TALK",
    "show_date": TODAY,
    "link_url": url,              # ← Lenke
    "notes": article.get('summary', f"Kilde: {article.get('source', 'Ukjent')}"),  # ← Notat
    "is_pinned": False,
    "is_completed": False
}
```

---

## EKSEMPEL PÅ RESULTAT

### Sak i databasen:
```json
{
  "title": "Nora Haukland vitner mot Marius Høiby",
  "link_url": "https://www.dagbladet.no/nyheter/hun-gruer-seg/84259386",
  "notes": "SKAL VITNE: Danby Choi er venn av både Nora Haukland og Marius Borg Høiby, og skal vitne under rettssaken\n\nKilde: dagbladet.no"
}
```

### Visning i sakslista:
```
📌 Nora Haukland vitner mot Marius Høiby
   🔗 https://www.dagbladet.no/nyheter/hun-gruer-seg/84259386
   📝 SKAL VITNE: Danby Choi er venn av både Nora Haukland og Marius Borg Høiby, 
      og skal vitne under rettssaken
      
      Kilde: dagbladet.no
```

---

## VERIFISERING

### Sjekk at kravet er oppfylt:
```bash
# Hent dagens saker
curl -s "${SUPABASE_URL}/rest/v1/agenda_items?select=title,link_url,notes&show_date=eq.${TODAY}&tenant_id=eq.a0000000-0000-0000-0000-000000000001" \
  -H "apikey: ${SUPABASE_SERVICE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_SERVICE_KEY}"
```

### Forventet resultat:
- Alle saker har `link_url` (ikke null)
- Alle saker har `notes` (ikke null)
- Notes inneholder oppsummering + kilde

---

## FEILSØKING

### Hvis lenke mangler:
- Sjekk at `url` finnes i brave-news-search resultat
- Sjekk at insert-koden sender `link_url`

### Hvis notat mangler:
- Sjekk at `create_summary()` kalles
- Sjekk at `summary` feltet inkluderes i JSON
- Sjekk at insert-koden bruker `article.get('summary', ...)`

---

## HISTORIKK

- **2026-02-21**: Krav implementert og dokumentert
- **2026-02-21**: Testet og verifisert - alle saker har lenke og notat

---

*Dette dokumentet skal leses før endringer i nyhetsinnhenting eller saksliste-håndtering.*
