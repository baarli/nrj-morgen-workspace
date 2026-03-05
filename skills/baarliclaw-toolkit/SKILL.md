---
name: baarliclaw-toolkit
description: BaarliClaw's egne verktøy for koding, bildebehandling, dataanalyse, web-scraping og automatisering. Bruk når du trenger å bygge nye funksjoner.
---

# 🧰 BaarliClaw Toolkit

**Min egen verktøykasse!** Jeg har bygget disse modulene for å kunne gjøre mer enn bare å dokumentere.

## 📦 Moduler

### 1. 🧰 `baarliclaw_toolkit.py` - Grunnverktøy
**Hva:** Felles utilities som alle andre moduler bruker

**Funksjoner:**
- `setup_logging()` - Konsistent logging
- `APIClient` - Generisk API-klient med retry
- `BraveSearchClient` - Søk med Brave API
- `SupabaseClient` - Database-operasjoner
- `@retry_on_error` - Decorator for retries
- `@cache_result` - Decorator for caching

**Bruk:**
```python
from baarliclaw_toolkit import setup_logging, BraveSearchClient

logger = setup_logging("my_script")
search = BraveSearchClient(api_key="...")
results = search.search_news("query")
```

---

### 2. 🖼️ `image_toolkit.py` - Bildebehandling
**Hva:** Last, rediger, og generer bilder

**Klasser:**
- `ImageProcessor` - Redigering av eksisterende bilder
- `ImageGenerator` - AI-generering med DALL-E

**Funksjoner:**
```python
from image_toolkit import ImageProcessor, quick_thumbnail

processor = ImageProcessor()
img = processor.load_image("https://example.com/image.jpg")
thumb = processor.create_thumbnail(img, text="Min tittel")
processor.save_image(thumb, "output.jpg")

# Hurtigfunksjoner
quick_thumbnail("input.jpg", "thumb.jpg", "Tittel")
download_image("https://...", "local.jpg")
```

---

### 3. 📊 `data_analyzer.py` - Dataanalyse
**Hva:** Analyser trender, tekst, og visualiser data

**Klasser:**
- `TrendAnalyzer` - Trend-deteksjon og prediksjon
- `TextAnalyzer` - Tekstanalyse og sentiment
- `DataVisualizer` - ASCII-grafer og tabeller

**Funksjoner:**
```python
from data_analyzer import TrendAnalyzer, quick_chart, find_trend

# Trend-analyse
trend = TrendAnalyzer()
for value in [100, 105, 110, 115, 120]:
    trend.add_point(value)

print(trend.detect_trend())  # {'direction': 'up', 'strength': 0.5}
print(trend.predict_next())  # 125.0

# Hurtig
print(find_trend([100, 105, 110]))  # 📈 UP (10.0%)
print(quick_chart([100, 105, 110], "Downloads"))
```

---

### 4. 🌐 `web_scraper.py` - Web-scraping
**Hva:** Hent data fra nettsider uten eksterne biblioteker

**Klasser:**
- `SimpleScraper` - HTML-scraping med regex
- `FeedReader` - RSS/Atom-feeds
- `SitemapParser` - XML-sitemaps

**Funksjoner:**
```python
from web_scraper import quick_scrape, fetch_feed

# Hurtig scrape
data = quick_scrape("https://example.com/article")
print(data['meta']['title'])
print(data['article']['content'])

# Feed
items = fetch_feed("https://example.com/feed.xml")
for item in items:
    print(item['title'], item['link'])
```

---

### 5. 🤖 `automation_engine.py` - Automatisering
**Hva:** Kjør oppgaver parallelt med avhengigheter

**Klasser:**
- `AutomationEngine` - Task runner
- `WorkflowBuilder` - Bygg komplekse arbeidsflyter

**Funksjoner:**
```python
from automation_engine import AutomationEngine, WorkflowBuilder

engine = AutomationEngine(max_workers=4)

# Enkle tasks
engine.add_task("fetch_data", "curl https://api.example.com")
engine.add_python_task("process", my_function, args=("arg1",))

# Workflow
workflow = WorkflowBuilder(engine)
workflow \
    .add_step("step1", "command1") \
    .add_step("step2", "command2", depends_on=["step1"]) \
    .add_python_step("step3", my_func, depends_on=["step2"])

workflow.build()
engine.start()
engine.wait_for_completion()
```

---

## 🚀 Hvordan bruke

### For å bygge noe nytt:

1. **Importer toolkit:**
```python
import sys
sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import *
from image_toolkit import *
from data_analyzer import *
from web_scraper import *
from automation_engine import *
```

2. **Velg riktig modul** for jobben:
   - API-kall? → `baarliclaw_toolkit.py`
   - Bilder? → `image_toolkit.py`
   - Data? → `data_analyzer.py`
   - Nettsider? → `web_scraper.py`
   - Mange oppgaver? → `automation_engine.py`

3. **Bygg videre** på modulene

---

## 📝 Eksempler

### Eksempel 1: Analyser NRJ-data
```python
from data_analyzer import TrendAnalyzer

# Last data fra Supabase
# ... (bruk SupabaseClient)

analyzer = TrendAnalyzer()
for row in data:
    analyzer.add_point(row['downloads'], row['date'])

trend = analyzer.detect_trend()
print(f"Trend: {trend['direction']} ({trend['change_percent']}%)")
```

### Eksempel 2: Generer thumbnails
```python
from image_toolkit import quick_thumbnail

for article in articles:
    if article.get('image_url'):
        output = f"/tmp/thumbs/{article['id']}.jpg"
        quick_thumbnail(article['image_url'], output, article['title'])
```

### Eksempel 3: Scrape nyheter
```python
from web_scraper import quick_scrape
from automation_engine import AutomationEngine

engine = AutomationEngine(max_workers=5)

for url in article_urls:
    engine.add_python_task(
        f"scrape_{url}",
        lambda u=url: quick_scrape(u)
    )

engine.start()
engine.wait_for_completion()
```

---

## 📁 Filplassering

```
/root/.openclaw/workspace/scripts/
├── baarliclaw_toolkit.py    # Grunnverktøy
├── image_toolkit.py          # Bildebehandling
├── data_analyzer.py          # Dataanalyse
├── web_scraper.py            # Web-scraping
└── automation_engine.py      # Automatisering
```

---

## 🎯 Neste steg

Jeg skal fortsette å bygge:
- [ ] Video-redigering med ffmpeg
- [ ] ML/AI-modeller
- [ ] Dashboard med Streamlit
- [ ] Eget API med FastAPI

**Laget:** 2026-02-26  
**Versjon:** 1.0
