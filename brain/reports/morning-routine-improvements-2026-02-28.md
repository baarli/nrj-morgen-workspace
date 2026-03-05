# Morning Routine System - Analysis & Improvement Recommendations

**Date:** 2026-02-28  
**System:** Content Aggregator Skill for NRJ Morgen  
**Analyst:** BaarliClaw  
**Status:** PAUSED (as of 2026-02-27)

---

## Executive Summary

The Morning Routine system is a content aggregation pipeline designed to collect, process, and deliver entertainment news for NRJ Morgen's morning radio show. While the system has a solid foundation with Brave News API integration, AI title generation, and automated Supabase insertion, there are significant opportunities for improvement across all four analyzed areas.

**Current State:**
- 15 articles/day across 5 categories
- OpenAI GPT-4o-mini title generation (max 7 words)
- Entertainment scoring algorithm (0-100)
- Automated Supabase insertion
- **Status:** PAUSED on user request

---

## 1. Current News Sources and Coverage

### 1.1 Existing Sources Analysis

| Category | Sources | Queries | Max Articles |
|----------|---------|---------|--------------|
| Reality TV | TV2.no | 4 queries | 3 |
| Kjendis Drama | Dagbladet, Se & Hør, Nettavisen, VG | 4 queries | 3 |
| Film & TV | VG, NRK, Dagbladet, TV2 | 4 queries | 3 |
| Musikk | General search, NRK | 4 queries | 3 |
| Internasjonalt | Daily Mail, TMZ, E! Online, People | 4 queries | 3 |

### 1.2 Strengths

✅ **Good source diversity** across Norwegian entertainment media  
✅ **Category balancing** prevents over-representation of single topics  
✅ **International coverage** via major tabloids  
✅ **Freshness filtering** (max 48 hours, prioritizes <24h)

### 1.3 Weaknesses & Gaps

❌ **Missing social media monitoring** - No TikTok, Instagram, or X (Twitter) trends  
❌ **Limited podcast coverage** - No integration with podcast platforms  
❌ **No YouTube monitoring** - Missing viral video trends  
❌ **Static source list** - No dynamic source discovery  
❌ **Limited local coverage** - Missing regional Norwegian sources  
❌ **No Reddit monitoring** - Missing grassroots trends

### 1.4 Recommendations

#### 1.4.1 Add Social Media Trend Monitoring
```python
# New source category: social_trends
SOCIAL_SOURCES = {
    'social_trends': {
        'name': 'Sosiale Medier Trends',
        'sources': [
            {'type': 'rss', 'url': 'https://trendogate.com/trending/rss'},
            {'type': 'api', 'platform': 'tiktok', 'endpoint': 'trending'},
            {'type': 'api', 'platform': 'youtube', 'endpoint': 'trending'},
        ],
        'max_articles': 2,
        'priority': 'high'
    }
}
```

#### 1.4.2 Implement Dynamic Source Discovery
```python
def discover_new_sources(seed_keywords, min_relevance_score=0.7):
    """
    Automatically discover new relevant sources based on trending keywords.
    """
    # Use Brave Search to find new entertainment blogs, influencers
    # Add sources that consistently produce high-entertainment-score content
    pass
```

#### 1.4.3 Add Podcast & YouTube Monitoring
```python
PODCAST_SOURCES = [
    'https://rss.podplaystudio.com/4035.xml',  # Baarli og Benjamin
    'https://feeds.megaphone.fm/PPY8223029287',  # Other Norwegian podcasts
]

YOUTUBE_CHANNELS = [
    'UC...',  # Popular Norwegian influencers
]
```

#### 1.4.4 Expand International Sources
```python
INTERNATIONAL_SOURCES = {
    'existing': ['dailymail.co.uk', 'tmz.com', 'eonline.com', 'people.com'],
    'recommended_additions': [
        'pagesix.com',      # NY Post - celebrity news
        'usmagazine.com',   # US Magazine
        'entertainment tonight.com',
        'hollywoodreporter.com',
        'variety.com',
        'thesun.co.uk',     # UK tabloid
        'mirror.co.uk',     # UK tabloid
    ]
}
```

---

## 2. AI Title Generation Quality

### 2.1 Current Implementation

**Model:** GPT-4o-mini  
**Prompt Strategy:** Simple one-shot with constraints  
**Constraints:**
- Maximum 7 words
- Norwegian language
- Catchy and entertaining
- Focus on most interesting aspect

### 2.2 Current Prompt Template
```python
prompt = f"""Original tittel: {original_title}
Beskrivelse: {description[:200]}

Lag en kort, catchy tittel på NORSK for NRJ Morgen (morgenradio).
- Maksimum 7 ord
- Fængende og underholdende
- Fokus på det mest interessante
- Bruk norsk språk

Kun tittelen, ingen forklaring."""
```

### 2.3 Strengths

✅ **Consistent length constraint** (max 7 words)  
✅ **Language consistency** (Norwegian)  
✅ **Context awareness** (uses both title and description)  
✅ **Fast model** (GPT-4o-mini is cost-effective)

### 2.4 Weaknesses & Issues

❌ **No A/B testing framework** - Can't measure which titles perform better  
❌ **No engagement prediction** - Titles aren't optimized for click-through  
❌ **Limited context** - Doesn't consider trending topics or show history  
❌ **No personality matching** - Generic tone, not matched to NRJ Morgen's voice  
❌ **No emoji/character optimization** - Missing visual appeal elements  
❌ **Fallback is too simple** - Rule-based fallback lacks sophistication

### 2.5 Recommendations

#### 2.5.1 Implement Engagement-Optimized Title Generation
```python
ENGAGEMENT_PROMPT = f"""Original tittel: {original_title}
Beskrivelse: {description[:300]}
Kategori: {category}
Trender i dag: {trending_topics}

Lag en TITTEL på NORSK for NRJ Morgen som:
1. Maks 7 ord
2. Skaper nysgjerrighet (curiosity gap)
3. Inneholder emosjonelt ladde ord (hvis relevant)
4. Bruk tall hvis relevant ("3 grunner til...")
5. Matcher NRJ Morgen's tone: ungdommelig, energisk, direkte

EKSEMPLER på gode NRJ-titler:
- "Sophie Elise raser mot Farmen-deltaker"
- "Marius Høiby med sjokk-beskjed til moren"
- "Paradise-para med brudd etter finale"

Dårlige titler (unngå):
- "Kjendis deler bilde på Instagram" (for generisk)
- "Dette skjedde i går" (for vag)

Kun tittelen, ingen forklaring."""
```

#### 2.5.2 Add Title Performance Tracking
```python
class TitlePerformanceTracker:
    """Track which titles drive engagement."""
    
    def log_title_performance(self, article_id, title, metrics):
        """
        metrics = {
            'click_through_rate': 0.15,
            'time_on_page': 45,
            'social_shares': 12,
            'show_mentions': 3  # How many times mentioned in show
        }
        """
        pass
    
    def get_best_performing_patterns(self, days=30):
        """Identify title patterns that perform best."""
        pass
```

#### 2.5.3 Implement Multi-Variant Title Generation
```python
def generate_title_variants(original_title, description, num_variants=3):
    """
    Generate multiple title variants for A/B testing.
    """
    variants = []
    
    # Variant 1: Curiosity gap
    variants.append(generate_with_prompt(CURIOSITY_PROMPT))
    
    # Variant 2: Emotional trigger
    variants.append(generate_with_prompt(EMOTION_PROMPT))
    
    # Variant 3: Direct benefit
    variants.append(generate_with_prompt(BENEFIT_PROMPT))
    
    return variants
```

#### 2.5.4 Add Show Context Awareness
```python
def get_show_context():
    """Get recent show topics to avoid repetition."""
    # Query Supabase for last 7 days of topics
    # Return set of discussed celebrities, themes
    pass

def generate_title_with_context(original, description, show_context):
    """Generate title that complements recent show content."""
    # Avoid repeating same celebrities
    # Build on previous topics if relevant
    pass
```

---

## 3. Content Filtering and Scoring

### 3.1 Current Scoring Algorithm

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

### 3.2 Current Exclusion List

**Hard Excluded (28 items):**
- Sports: fotball, langrenn, ski, hopp, alpint, skiskyting
- Violence: krig, terror, drap, skudd, vold
- Politics: regjering, storting, parti, politiker
- Economy: skatt, økonomi, finans, rente, inflasjon
- Other: død, tragedie, ulykke, sykehus, korona

### 3.3 Strengths

✅ **Simple and fast** - No ML model required  
✅ **Clear rules** - Easy to understand and modify  
✅ **Celebrity boosting** - Prioritizes known personalities  
✅ **Keyword-based** - Transparent scoring logic

### 3.4 Weaknesses & Issues

❌ **Static keyword list** - Doesn't adapt to trending terms  
❌ **No sentiment analysis** - Can't detect negative sentiment in context  
❌ **Binary exclusion** - No nuance in filtering (all or nothing)  
❌ **No recency weighting** - 1-hour-old and 47-hour-old stories score equally  
❌ **No source quality weighting** - All sources treated equally  
❌ **Missing engagement prediction** - Score doesn't predict listener interest  
❌ **No duplicate detection** - Similar stories from different sources both included  
❌ **Celebrity list is static** - Doesn't update with trending personalities

### 3.5 Recommendations

#### 3.5.1 Implement ML-Based Scoring
```python
class MLContentScorer:
    """
    Machine learning model trained on historical performance data.
    """
    
    def __init__(self):
        self.model = self.load_pretrained_model()
    
    def score_article(self, article):
        features = self.extract_features(article)
        # Features: sentiment, entities, topic, source authority, 
        #           time since publish, historical engagement
        return self.model.predict(features)
    
    def extract_features(self, article):
        return {
            'sentiment': analyze_sentiment(article['description']),
            'entities': extract_entities(article['title'] + article['description']),
            'topic': classify_topic(article),
            'source_authority': get_source_authority(article['source']),
            'recency_hours': calculate_recency(article['publishedAt']),
            'title_engagement_score': predict_title_engagement(article['title'])
        }
```

#### 3.5.2 Add Dynamic Keyword Learning
```python
class TrendingKeywordTracker:
    """Automatically learn which keywords correlate with engagement."""
    
    def update_keyword_scores(self, articles, engagement_data):
        """
        Update keyword weights based on actual performance.
        """
        for article in articles:
            keywords = extract_keywords(article['title'])
            for keyword in keywords:
                if keyword not in self.keyword_scores:
                    self.keyword_scores[keyword] = {'score': 50, 'samples': 0}
                
                # Update with exponential moving average
                engagement = engagement_data.get(article['id'], 0)
                old_score = self.keyword_scores[keyword]['score']
                self.keyword_scores[keyword]['score'] = (
                    0.9 * old_score + 0.1 * engagement
                )
                self.keyword_scores[keyword]['samples'] += 1
```

#### 3.5.3 Implement Smart Duplicate Detection
```python
class DuplicateDetector:
    """Detect similar stories using semantic similarity."""
    
    def __init__(self):
        self.embedding_model = load_sentence_transformer()
    
    def find_duplicates(self, articles, threshold=0.85):
        """
        Find articles covering the same story.
        """
        embeddings = self.embedding_model.encode(
            [a['title'] + ' ' + a['description'][:200] for a in articles]
        )
        
        duplicates = []
        for i in range(len(articles)):
            for j in range(i+1, len(articles)):
                similarity = cosine_similarity(embeddings[i], embeddings[j])
                if similarity > threshold:
                    duplicates.append((articles[i], articles[j], similarity))
        
        return duplicates
    
    def merge_duplicates(self, duplicates):
        """Keep best source for each story."""
        # Prefer: higher authority source, more complete information
        pass
```

#### 3.5.4 Add Recency-Weighted Scoring
```python
def calculate_recency_score(published_at, max_age_hours=48):
    """
    Higher score for fresher content.
    Exponential decay: score = 100 * e^(-0.05 * hours)
    """
    hours_old = (datetime.now() - published_at).total_seconds() / 3600
    
    if hours_old > max_age_hours:
        return 0
    
    return 100 * math.exp(-0.05 * hours_old)

# Combine with base score
def calculate_final_score(article):
    base_score = calculate_entertainment_score(article)
    recency_score = calculate_recency_score(article['publishedAt'])
    
    # Weight: 60% entertainment, 40% recency
    return 0.6 * base_score + 0.4 * recency_score
```

#### 3.5.5 Implement Source Authority Scoring
```python
SOURCE_AUTHORITY = {
    # Norwegian sources
    'vg.no': 0.95,
    'dagbladet.no': 0.90,
    'tv2.no': 0.88,
    'nrk.no': 0.85,
    'nettavisen.no': 0.75,
    'seher.no': 0.80,
    
    # International sources
    'dailymail.co.uk': 0.70,
    'tmz.com': 0.85,  # High for entertainment
    'eonline.com': 0.80,
    'people.com': 0.82,
}

def apply_source_weight(score, source_domain):
    authority = SOURCE_AUTHORITY.get(source_domain, 0.50)
    return score * (0.7 + 0.3 * authority)  # Max 30% boost from authority
```

---

## 4. Integration with Show Preparation

### 4.1 Current Integration Points

| Integration | Status | Description |
|-------------|--------|-------------|
| Supabase Insert | ✅ Active | Direct database insertion |
| Email Show Prep | ✅ Active | Daily email with top stories |
| Sakslista UI | ✅ Active | Mission Control dashboard |
| Image Fetching | ✅ Active | Automatic image extraction |

### 4.2 Current Data Flow

```
Brave API → Filter/Score → AI Titles → Supabase → Sakslista UI
                ↓
         Email Show Prep
```

### 4.3 Strengths

✅ **Automated insertion** - No manual copy-paste  
✅ **Rich metadata** - Images, summaries, sources  
✅ **Email delivery** - Show prep delivered to inbox  
✅ **Dashboard visibility** - Mission Control integration

### 4.4 Weaknesses & Gaps

❌ **No host briefing generation** - Raw articles, no talking points  
❌ **No segment suggestions** - Doesn't suggest how to use stories  
❌ **No timing optimization** - Doesn't suggest when to air stories  
❌ **No cross-reference with competitors** - Missing competitive intelligence  
❌ **No listener feedback loop** - No data on which stories resonated  
❌ **No prep sheet generation** - No printable/scriptable format  
❌ **No audio clip suggestions** - Doesn't suggest sound bites  
❌ **No social media cross-post** - Stories not auto-shared to SoMe

### 4.5 Recommendations

#### 4.5.1 Generate Host Briefing Documents
```python
def generate_host_briefing(articles, show_date):
    """
    Generate a comprehensive briefing document for show hosts.
    """
    briefing = {
        'date': show_date,
        'top_stories': [],
        'talking_points': {},
        'suggested_segments': [],
        'background_info': {}
    }
    
    for article in articles[:5]:  # Top 5 stories
        briefing['top_stories'].append({
            'title': article['short_title'],
            'hook': generate_opening_hook(article),
            'key_facts': extract_key_facts(article),
            'potential_angles': suggest_angles(article),
            'related_stories': find_related(article, articles),
            'questions_to_ask': generate_questions(article)
        })
    
    return briefing

def generate_opening_hook(article):
    """Generate an attention-grabbing opening line."""
    templates = [
        "Du vil ikke tro hva {celebrity} har gjort nå...",
        "Skandale i {show}: {event}",
        "{Celebrity} raser etter {event}",
    ]
    # Select and fill template based on article content
    pass
```

#### 4.5.2 Implement Segment Suggestion Engine
```python
class SegmentSuggester:
    """Suggest radio segments based on available stories."""
    
    SEGMENT_TYPES = {
        'hot_take': 'Rask kommentar på aktuell sak',
        'deep_dive': 'Grundig gjennomgang av større sak',
        'debate': 'To sider av en sak',
        'quiz': 'Quiz basert på kjendisnyheter',
        'trending': 'Hva trender nå?',
    }
    
    def suggest_segments(self, articles, available_time_minutes):
        """
        Suggest optimal segment mix for the show.
        """
        segments = []
        
        # Always suggest a hot take for top story
        segments.append({
            'type': 'hot_take',
            'article': articles[0],
            'duration': 2,
            'timing': 'opening'
        })
        
        # Suggest deep dive for high-engagement story
        high_engagement = [a for a in articles if a['score'] > 80]
        if high_engagement:
            segments.append({
                'type': 'deep_dive',
                'article': high_engagement[0],
                'duration': 5,
                'timing': 'mid_show'
            })
        
        return segments
```

#### 4.5.3 Add Competitive Intelligence Integration
```python
class CompetitiveMonitor:
    """Monitor what competitors are covering."""
    
    COMPETITORS = [
        {'name': 'P3 Morgen', 'rss': '...'},
        {'name': 'Radio 1', 'rss': '...'},
    ]
    
    def analyze_coverage(self, our_articles):
        """
        Compare our planned coverage with competitors.
        """
        competitor_stories = self.fetch_competitor_stories()
        
        analysis = {
            'unique_to_us': [],      # Stories only we're covering
            'also_covered': [],       # Stories everyone has
            'missed_opportunities': []  # Stories competitors have that we don't
        }
        
        return analysis
    
    def suggest_differentiation(self, article, competitor_coverage):
        """Suggest unique angles when competitors cover same story."""
        pass
```

#### 4.5.4 Implement Listener Feedback Loop
```python
class ListenerFeedbackTracker:
    """Track which stories generate listener engagement."""
    
    def track_story_performance(self, article_id):
        """
        Track metrics:
        - Phone-in volume during/after story
        - Social media mentions
        - App engagement
        - Website clicks
        """
        pass
    
    def generate_performance_report(self, days=7):
        """Report on which story types perform best."""
        pass
```

#### 4.5.5 Create Prep Sheet Generator
```python
def generate_prep_sheet(articles, output_format='pdf'):
    """
    Generate a printable prep sheet for show hosts.
    """
    prep_sheet = {
        'header': {
            'show_date': datetime.now().strftime('%Y-%m-%d'),
            'generated_at': datetime.now().isoformat(),
            'total_stories': len(articles)
        },
        'stories': [],
        'quick_reference': {}
    }
    
    for i, article in enumerate(articles, 1):
        prep_sheet['stories'].append({
            'number': i,
            'title': article['short_title'],
            'category': article['category'],
            'summary': article['description'][:200],
            'source': article['source'],
            'url': article['url'],
            'suggested_timing': estimate_segment_time(article),
            'key_quote': extract_quote(article),
            'background': get_background_info(article)
        })
    
    # Export to PDF or printable HTML
    return export_prep_sheet(prep_sheet, output_format)
```

#### 4.5.6 Add Audio Clip Suggestions
```python
def suggest_audio_clips(article):
    """
    Suggest relevant audio clips for the story.
    """
    suggestions = []
    
    # Check if article mentions songs, shows, or viral videos
    entities = extract_entities(article['description'])
    
    for entity in entities:
        if entity['type'] == 'song':
            suggestions.append({
                'type': 'song_snippet',
                'search_query': f"{entity['name']} {entity.get('artist', '')}",
                'suggested_duration': '10-15 seconds'
            })
        elif entity['type'] == 'tv_show':
            suggestions.append({
                'type': 'show_clip',
                'show_name': entity['name'],
                'context': 'relevant scene or promo'
            })
    
    return suggestions
```

---

## 5. Implementation Priority Matrix

| Priority | Improvement | Effort | Impact | Quick Win? |
|----------|-------------|--------|--------|------------|
| **P0** | Recency-weighted scoring | Low | High | ✅ Yes |
| **P0** | Source authority weighting | Low | Medium | ✅ Yes |
| **P0** | Host briefing generation | Medium | High | ❌ No |
| **P1** | Dynamic keyword learning | Medium | High | ❌ No |
| **P1** | Social media trend monitoring | Medium | Medium | ❌ No |
| **P1** | Engagement-optimized titles | Medium | High | ❌ No |
| **P2** | ML-based scoring | High | High | ❌ No |
| **P2** | Smart duplicate detection | Medium | Medium | ❌ No |
| **P2** | Competitive intelligence | Medium | Medium | ❌ No |
| **P3** | Segment suggestion engine | High | Medium | ❌ No |
| **P3** | Listener feedback loop | High | High | ❌ No |
| **P3** | Audio clip suggestions | Medium | Low | ❌ No |

---

## 6. Quick Wins (Implement First)

### 6.1 Recency-Weighted Scoring (1-2 hours)
```python
import math

def calculate_recency_score(published_at, max_age_hours=48):
    hours_old = (datetime.now() - published_at).total_seconds() / 3600
    if hours_old > max_age_hours:
        return 0
    return 100 * math.exp(-0.05 * hours_old)
```

### 6.2 Source Authority Weighting (1 hour)
Add the `SOURCE_AUTHORITY` dictionary and apply weight in scoring.

### 6.3 Enhanced Title Prompt (30 minutes)
Update the prompt template with engagement-focused examples.

### 6.4 Add International Sources (30 minutes)
Add `pagesix.com`, `usmagazine.com`, `thesun.co.uk` to source list.

---

## 7. Long-Term Vision

### 7.1 Predictive Content Curation
The system should predict which stories will resonate based on:
- Historical performance of similar stories
- Current trending topics
- Day-of-week patterns
- Seasonal trends

### 7.2 Automated Show Prep
Full automation of show preparation:
- Story selection
- Briefing generation
- Segment timing
- Audio clip preparation
- Social media scheduling

### 7.3 Real-Time Adaptation
During the show, the system should:
- Monitor breaking news
- Suggest real-time updates
- Track listener engagement
- Adapt recommendations based on live feedback

---

## 8. Conclusion

The Morning Routine system has a solid foundation but significant room for improvement. The highest-impact changes are:

1. **Immediate (This Week):**
   - Implement recency-weighted scoring
   - Add source authority weighting
   - Update title generation prompt

2. **Short-Term (Next Month):**
   - Add social media trend monitoring
   - Implement dynamic keyword learning
   - Generate host briefing documents

3. **Long-Term (Next Quarter):**
   - ML-based content scoring
   - Full competitive intelligence integration
   - Listener feedback loop implementation

These improvements will transform the Morning Routine from a basic aggregator into an intelligent content curation system that actively drives listener engagement and show quality.

---

**Report Generated:** 2026-02-28  
**Next Review:** 2026-03-15
