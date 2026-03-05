---
name: content-aggregator
description: News and content aggregation system with Brave News API integration, AI title generation, and automated research workflows. Powers the Morning Routine system for NRJ Morgen.
---

# 📰 Content Aggregator

A comprehensive news and content aggregation system that automatically collects, processes, and organizes content from multiple sources. Built for NRJ Morgen but adaptable for any content aggregation needs.

## 🎯 What This Skill Does

- **News Aggregation**: Collects news from Brave News API across multiple categories
- **AI Title Generation**: Uses OpenAI to create concise, engaging titles (max 7 words)
- **Content Filtering**: Automatically excludes unwanted topics (sports, politics, tragedies)
- **Entertainment Scoring**: Ranks content by entertainment value for radio audiences
- **Morning Routine**: Automated daily workflow for show preparation
- **Research Automation**: Deep research on topics with trend detection

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTENT AGGREGATOR                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   SOURCES    │───▶│  PROCESSING  │───▶│   OUTPUT     │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                   │                   │           │
│         ▼                   ▼                   ▼           │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Brave News   │    │ AI Title Gen │    │ Supabase     │  │
│  │ API          │    │ Filtering    │    │ Database     │  │
│  └──────────────┘    │ Scoring      │    │ JSON Export  │  │
│                      └──────────────┘    └──────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Files

### Core Scripts

| Script | Purpose | Location |
|--------|---------|----------|
| `brave-news-search.py` | Real-time news search with entertainment scoring | `/root/.openclaw/workspace/scripts/` |
| `morning-routine-v2.1.py` | Daily workflow - 15 articles from 5 categories | `/root/.openclaw/workspace/scripts/` |
| `ai-generate-title.py` | AI-powered title generation (max 7 words) | `/root/.openclaw/workspace/scripts/` |
| `integrated-morning-routine.sh` | Full automation pipeline | `/root/.openclaw/workspace/scripts/` |

### Configuration

| File | Purpose |
|------|---------|
| `.credentials/nrj-morgen.env` | API keys (Brave, OpenAI, Supabase) |
| `.morning-routine-paused` | Pause flag for maintenance |

## 🚀 Quick Start

### 1. Basic News Search

```bash
cd /root/.openclaw/workspace/scripts
python3 brave-news-search.py 15
```

Output: `/tmp/morning-news.json`

### 2. Run Morning Routine

```bash
# Full routine with AI titles
python3 morning-routine-v2.1.py

# Or use the integrated pipeline
bash integrated-morning-routine.sh
```

Output: `/tmp/morning-routine-v2-result.json`

### 3. Generate AI Title

```bash
python3 ai-generate-title.py "Original long news title here" "Description text"
```

## 📊 Morning Routine v2.1 Configuration

### Category Distribution

| Category | Max Articles | Sources |
|----------|--------------|---------|
| Reality TV | 3 | Farmen, Paradise Hotel, Kompani Lauritzen, Love Island |
| Kjendis Drama | 3 | Dagbladet, Se & Hør, Nettavisen, VG Rampelys |
| Film & TV | 3 | Premieres, red carpet events |
| Musikk | 3 | Spellemannprisen, VG-lista, P3 Gull |
| Internasjonalt | 3 | Daily Mail, TMZ, E! Online, People |

**Total: 15 articles per day**

### Content Filters

**✅ INCLUDED:**
- Celebrity news (breakups, drama, revelations)
- Reality TV updates
- Influencers and profiles
- Film and music (premieres, awards)
- Royal family (light entertainment)
- Social media and viral content

**❌ EXCLUDED:**
- Sports (football, handball, skiing)
- Hard politics (government, parliament, legislation)
- War and conflict
- Hard news (deaths, accidents, tragedies)
- Economy and finance
- Health and COVID

### Age Requirements
- **Freshness**: Past 24-48 hours (`freshness=pd`)
- **Maximum age**: 48 hours

## 🔌 API Integration

### Brave News API

```python
# Configuration
BRAVE_API_KEY = "BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev"
SEARCH_URL = "https://api.search.brave.com/res/v1/news/search"

# Parameters
params = {
    "q": "site:vg.no rampelys",
    "count": 10,
    "search_lang": "nb",
    "country": "no",
    "freshness": "pd"  # past day
}

# Headers
headers = {
    "X-Subscription-Token": BRAVE_API_KEY,
    "Accept": "application/json"
}
```

### OpenAI Title Generation

```python
# Configuration
OPENAI_API_KEY = "your-key-here"
MODEL = "gpt-4o-mini"

# Prompt template
prompt = f"""Original tittel: {original_title}
Beskrivelse: {description[:200]}

Lag en kort, catchy tittel på NORSK for NRJ Morgen (morgenradio).
- Maksimum 7 ord
- Fængende og underholdende
- Fokus på det mest interessante
- Bruk norsk språk

Kun tittelen, ingen forklaring."""
```

### Supabase Integration

```python
# Configuration
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "your-service-role-key"
TENANT_ID = "a0000000-0000-0000-0000-000000000001"
CREATED_BY = "10aa1508-6d52-490c-8ae5-fa3da9a152c4"

# Data structure
article = {
    "tenant_id": TENANT_ID,
    "title": "AI-generated title (max 7 words)",
    "description": "Original description",
    "category": "TALK",
    "show_date": "2026-02-28",
    "link_url": "https://...",
    "notes": "Summary + entertainment score",
    "is_pinned": False,
    "is_completed": False
}
```

## 🎭 Entertainment Scoring Algorithm

```python
def calculate_score(title, description):
    score = 50  # Baseline
    combined = (title + ' ' + description).lower()
    
    # Positive factors (+10 each)
    positive = ['brudd', 'krangel', 'drama', 'skandale', 'avsløring',
                'hemmelig', 'kontrovers', 'konflikt', 'exit', 'overraskelse',
                'comeback', 'pinlig', 'sterkt sitat', 'tårer', 'raser', 
                'sjokk', 'kaos']
    
    # Celebrity boost (+15 each)
    celebrities = ['marius borg høiby', 'mette-marit', 'sophie elise',
                   'isabel raad', 'renate reinsve']
    
    # Negative factors (-20 each)
    negative = ['politikk', 'økonomi', 'skatt', 'lovforslag', 'regjering']
    
    return min(100, max(0, score))
```

## 🔄 Automation Workflows

### Daily Morning Routine

```bash
# Cron schedule: 06:00 daily
0 6 * * * cd /root/.openclaw/workspace/scripts && bash integrated-morning-routine.sh >> /var/log/morning-routine.log 2>&1
```

### Pipeline Steps

1. **Media Monitor** - Check media for new trends
2. **News Aggregator** - Collect articles from Brave API
3. **Intelligence Hub** - Analyze trends and competitors
4. **Trend Detector** - Identify trending topics
5. **Browser Automation** - Fetch article details
6. **Content Suite** - Generate content
7. **Quality Validator** - Validate content quality
8. **Morning Routine v2.1** - Generate 15 articles with AI titles
9. **Email Automation** - Send show prep email
10. **Social Publisher** - Schedule social posts
11. **Analytics Suite** - Generate reports
12. **Self-Improvement** - Log learnings

## 🛠️ Customization

### Adding New Sources

Edit `morning-routine-v2.1.py`:

```python
SOURCES = {
    'new_category': {
        'name': 'New Category Name',
        'queries': [
            "site:example.com query1",
            "site:example.com query2",
        ],
        'max_articles': 3
    },
    # ... existing categories
}
```

### Modifying Filters

Edit `brave-news-search.py`:

```python
# Add to hard_excluded list
hard_excluded = [
    'existing', 'filters',
    'new_filter_word',  # Add here
]
```

### Custom Title Generation

Edit `ai-generate-title.py`:

```python
# Modify prompt template
prompt = f"""Your custom prompt here...
Original: {original_title}
Description: {description}
"""
```

## 📈 Output Formats

### JSON Structure (morning-news.json)

```json
{
  "timestamp": "2026-02-28T06:00:00",
  "count": 15,
  "articles": [
    {
      "title": "Original article title",
      "description": "Full description...",
      "url": "https://source.com/article",
      "source": "vg.no",
      "publishedAt": "2 hours ago",
      "summary": "2-3 sentence summary.\n\nKilde: vg.no",
      "entertainment_score": 85,
      "why_nrj": "brudd-drama, sterke følelser"
    }
  ]
}
```

### JSON Structure (morning-routine-v2-result.json)

```json
{
  "timestamp": "2026-02-28T06:00:00",
  "total": 45,
  "unique": 28,
  "top_15": [
    {
      "title": "Original title",
      "short_title": "AI-generated title (max 7 words)",
      "url": "https://...",
      "description": "Description...",
      "source": "kjendis_drama",
      "score": 90,
      "category": "Kjendis Drama"
    }
  ]
}
```

## 🔧 Troubleshooting

### Common Issues

#### 1. No Articles Found

```bash
# Check API key
echo $BRAVE_API_KEY

# Test API directly
curl -H "X-Subscription-Token: $BRAVE_API_KEY" \
  "https://api.search.brave.com/res/v1/news/search?q=test&count=1"
```

#### 2. AI Title Generation Fails

```bash
# Check OpenAI API key
echo $OPENAI_API_KEY

# Test with simple prompt
python3 ai-generate-title.py "Test title here" "Test description"
```

#### 3. Supabase Insert Fails

```bash
# Verify credentials
cat /root/.openclaw/workspace/.credentials/nrj-morgen.env

# Check network connectivity
curl -I $SUPABASE_URL
```

#### 4. Morning Routine Paused

```bash
# Check pause status
ls -la /root/.openclaw/workspace/.morning-routine-paused

# Resume routine
rm /root/.openclaw/workspace/.morning-routine-paused
```

### Debug Mode

```bash
# Run with verbose output
python3 brave-news-search.py 15 2>&1 | tee /tmp/debug.log

# Check logs
tail -f /var/log/morning-routine.log
```

### Performance Issues

```bash
# Check execution time
time python3 morning-routine-v2.1.py

# Monitor API rate limits
# Brave: 2000 queries/month on free tier
```

## 📚 Advanced Usage

### Research Automation

```python
# Deep research on a topic
from brave-news-search import search_brave, format_article

queries = [
    "Marius Borg Høiby",
    "Mette-Marit",
    "Kongehuset",
]

results = []
for query in queries:
    data = search_brave(query, api_key, count=10)
    results.extend(data.get('results', []))

# Analyze trends
from data_analyzer import TrendAnalyzer
trend = TrendAnalyzer()
# ... analysis code
```

### Custom Aggregation Pipeline

```bash
#!/bin/bash
# custom-pipeline.sh

# Step 1: Search
python3 brave-news-search.py 20

# Step 2: Filter
cat /tmp/morning-news.json | jq '.articles | map(select(.entertainment_score > 70))' > /tmp/filtered.json

# Step 3: Generate titles
for article in $(cat /tmp/filtered.json | jq -r '.[].title'); do
    python3 ai-generate-title.py "$article"
done

# Step 4: Export
cp /tmp/filtered.json /output/$(date +%Y%m%d)-news.json
```

### Integration with Other Skills

```python
# Use with baarliclaw-toolkit
from baarliclaw_toolkit import BraveSearchClient, SupabaseClient
from data_analyzer import TrendAnalyzer

# Combine with image processing
from image_toolkit import ImageProcessor

# Combine with web scraping
from web_scraper import quick_scrape
```

## 🔐 Security Notes

- API keys stored in `.credentials/nrj-morgen.env`
- Service role key for Supabase (keep secret!)
- Brave API key has rate limits (2000 queries/month)
- OpenAI API costs apply for title generation

## 📞 Support

- **Skill Location**: `/root/.openclaw/workspace/skills/content-aggregator/`
- **Scripts**: `/root/.openclaw/workspace/scripts/`
- **Logs**: `/var/log/morning-routine.log`
- **Output**: `/tmp/morning-*.json`

## 📝 Changelog

### v2.1 (2026-02-24)
- Increased from 10 to 15 articles per day
- Better category distribution (max 3 per category)
- OpenAI title generation (max 7 words)
- Integrated with Supabase for direct insertion

### v2.0 (2026-02-21)
- Added entertainment scoring
- Content filtering for radio audience
- Parallel search execution
- JSON export format

### v1.0 (2026-02-15)
- Initial release
- Basic Brave News API integration
- Simple filtering

## 🎯 Success Metrics

- **Coverage**: 15 articles/day across 5 categories
- **Freshness**: <48 hours old
- **Quality**: Entertainment score >50
- **Automation**: Fully automated daily workflow
- **Integration**: Direct Supabase insertion

---

*Built for NRJ Morgen - Norway's #1 Commercial Morning Radio Show*
