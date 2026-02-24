# Prediktiv Analyse for Mission Control

## Formål
Bruke historiske data for å forutsi fremtidige trender og optimalisere innhold.

## Algoritmer

### 1. Sak Popularitet Prediksjon
```python
def predict_sak_performance(title, category, source):
    # Faktorer:
    # - Tidligere lignende saker (tittel-similaritet)
    # - Kilde-pålitelighet
    # - Kategori-popularitet
    # - Tidspunkt på dagen
    
    score = base_score
    score += source_reliability[source] * 0.3
    score += category_popularity[category] * 0.25
    score += title_engagement_score(title) * 0.35
    score += time_of_day_factor() * 0.1
    
    return min(score, 100)
```

### 2. Beste Publiseringstid
```python
def optimal_publish_time(category, day_of_week):
    # Analysere historiske data for å finne:
    # - Hvilken time på døgnet gir best engasjement
    # - Hvilken ukedag er best for hver kategori
    
    hourly_data = get_hourly_engagement(category)
    return max(hourly_data, key=lambda x: x.engagement)
```

### 3. Trend Forutsigelse
```python
def predict_trending_topics(current_saker, lookback_days=7):
    # Identifisere:
    # - Hvilke temaer øker i popularitet
    # - Hvilke kilder gir treff først
    # - Hvilke kjendiser er "hot" akkurat nå
    
    trending = analyze_word_frequency(current_saker)
    return trending[:10]
```

## Implementasjon

### Frontend
- Legge til "Prediksjon"-panel i analytics.html
- Vise forventet popularitet for nye saker
- Anbefale beste publiseringstid

### Backend
- API-endepunkt: /api/analytics/predict
- Cache prediksjoner i 1 time
- Oppdatere modell ukentlig

## Visualisering
- Score-meter for hver sak
- Heatmap for beste tider
- Trend-pil (opp/ned/stabil)
