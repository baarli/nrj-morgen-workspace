# SYSTEM INTEGRATION & DATA FLOW ANALYSIS
## Vev Master System - Integrasjonsrapport

**Dato:** 2026-03-11  
**Analysert av:** Vev Subagent  
**Systemversjon:** 3.0  
**Status:** 🔴 KRITISKE PROBLEMER IDENTIFISERT

---

## 📊 EXECUTIVE SUMMARY

Analysen identifiserte **12 kritiske integrasjonsproblemer**, **8 datakonsistens-utfordringer**, og **5 områder** som krever øyeblikkelig oppmerksomhet. Systemet har betydelig teknisk gjeld som påvirker pålitelighet og vedlikeholdbarhet.

### Kritiske funn:
- ⚠️ **33% av cron-jobs feiler** (7 av 21 jobs med error status)
- ⚠️ **Ingen transaksjonsstyring** i dataflyt
- ⚠️ **Dupliserte API-nøkler** hardkodet på tvers av scripts
- ⚠️ **Ingen sentral error-håndtering** eller retry-mekanismer
- ⚠️ **Race conditions** i Morning Routine → Supabase flyt

---

## 1. INTEGRASJONSPROBLEMER IDENTIFISERT

### 🔴 KRITISK - Nivå 1

#### 1.1 Ingen transaksjonsstyring i Morning Routine
**Problem:** Dataflyten fra Morning Routine til Supabase har ingen transaksjonsstyring.

**Nåværende flyt:**
```
Morning Routine v2.1 → JSON file → Python insert script → Supabase
```

**Risiko:**
- Hvis insert feiler midtveis, har man delvis data i Supabase
- Ingen rollback-mekanisme
- Kan resultere i duplikate eller ufullstendige datasett

**Lokasjon:**
- `scripts/morning-routine-v2.1.py`
- `scripts/integrated-morning-routine.sh` (STEG 8)

**Anbefaling:**
```python
# Implementer transaksjonsstyring
BEGIN TRANSACTION;
  DELETE FROM agenda_items WHERE show_date = '2026-03-11' AND source = 'morning_routine';
  INSERT INTO agenda_items (...) VALUES (...);
  INSERT INTO agenda_items (...) VALUES (...);
  -- alle 15 inserts
COMMIT;
```

---

#### 1.2 Race Condition i Dashboard-statistikk
**Problem:** Flere scripts kan oppdatere samme panel samtidig.

**Berørte scripts:**
- `update_nrj_dashboard.py` (korrekt - oppdaterer eksisterende)
- `fetch_nrj_dashboard_stats.py` (feil - oppretter nytt item)
- `update_nrj_dashboard.py` via cron (onsdager kl 14:00)
- Manuell oppdatering via Mission Control

**Konsekvens:** Data inkonsistens, duplikate paneler, overskrevne data.

**Dokumentasjon fra NRJ_DASHBOARD_SYSTEM.md:**
> "IKKE bruk `fetch_nrj_dashboard_stats.py` - Dette oppretter NYTT item i sakslista"

**Status:** Delvis fikset med dokumentasjon, men ikke teknisk løst.

---

#### 1.3 Hardkodede API-nøkler på tvers av systemet
**Problem:** Samme API-nøkler er hardkodet i flere scripts.

**Eksempler:**
```python
# morning-routine-v2.1.py
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6..."
BRAVE_KEY = "BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev"
OPENAI_KEY = "sk-proj-siJLBYXi6DDjl2DxsZf7..."

# update_nrj_dashboard.py (samme nøkler)
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6..."

# total-control-api.py (samme nøkler)
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6..."
```

**Risiko:**
- Vanskelig å rotere nøkler
- Sikkerhetsrisiko hvis kode deles
- Inconsistent hvis én nøkkel oppdateres, men ikke alle

---

#### 1.4 Ingen sentralisert error-håndtering
**Problem:** Hvert script har sin egen feilhåndtering, ingen konsistent strategi.

**Observasjoner:**
- `brave-news-search.py`: `socket.setdefaulttimeout(15)` - unødvendig kompleks
- `update_nrj_dashboard.py`: Basic try/except, logger til stdout
- `morning-routine-v2.1.py`: Ingen retry-mekanisme ved API-feil

**Cron status viser 7 feilende jobs:**
```
b69094e4-... NRJ MORGEN – Daglig O... error     isolated
8488e609-... Podkast - Auto Clip D... error     isolated
fea8054f-... PODKAST – Daglig klip... error     isolated
d6148357-... VEV - Proaktiv Initia... error     isolated
67e1de35-... SELVUTVIKLING – Måned... error     isolated
f06c1cfd-... VEV - Daglig Læring (... error     isolated
```

---

### 🟡 HOY - Nivå 2

#### 1.5 Inconsistent dataformat i Supabase
**Problem:** `link_metadata` felt brukes inkonsistent.

**Schema forventet:**
```json
{"image_url": "...", "source": "...", "category": "..."}
```

**Faktisk bruk:**
- Morning Routine: Lagrer ikke `link_metadata`
- NRJ Stats: Lagrer kompleks JSON med Nielsen/Podtoppen data
- Manuell insert: Varierer

**Frontend forventning (supabase-integration.js):**
```javascript
const imageUrl = item.link_metadata?.image_url || item.image_url || '';
```

**Konsekvens:** Bilder vises ikke konsekvent i Mission Control.

---

#### 1.6 Duplisert funksjonalitet
**Problem:** Flere scripts gjør det samme.

| Funksjon | Scripts |
|----------|---------|
| NRJ Stats | `update_nrj_dashboard.py`, `fetch_nrj_dashboard_stats.py`, `fetch_nielsen_live.py`, `fetch_podtoppen_live.py` |
| Morning Routine | `morning-routine-v2.1.py`, `brave-news-search.py`, `integrated-morning-routine.sh` |
| Supabase Insert | Inline i shell scripts, separate Python scripts |

---

#### 1.7 Ingen API-rate limiting håndtering
**Problem:** Scripts håndterer ikke rate limiting fra eksterne API-er.

**Brave API:**
- Ingen retry med exponential backoff
- Ingen håndtering av 429 responses
- Flere samtidige requests kan utløse rate limits

**OpenAI API:**
- 10 sekunders timeout (kan være for kort)
- Ingen retry-logikk

**ElevenLabs:**
- Ingen caching-strategi (unødvendige API-kall)

---

#### 1.8 Feil i dato-håndtering
**Problem:** Inkonsistent tidszone-håndtering.

**Eksempler:**
```bash
# integrated-morning-routine.sh
TODAY=$(TZ=Europe/Oslo date -d "+1 day" +%Y-%m-%d)

# morning-routine-v2.1.py
TOMORROW = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
# ^ Bruker system-tid, ikke Europe/Oslo
```

**Konsekvens:** Saker kan bli satt til feil dato hvis server ikke er i samme tidszone.

---

### 🟢 MIDDELS - Nivå 3

#### 1.9 Ingen datavalidering før insert
**Problem:** Ingen validering av data før Supabase insert.

**Manglende valideringer:**
- URL-format
- Påkrevde felter (title, show_date, tenant_id)
- Maks lengde på felter
- Gyldige kategorier

#### 1.10 Ingen deduplisering på tvers av kilder
**Problem:** Samme sak kan komme fra flere kilder.

**Nåværende dedup:**
```python
# Kun innenfor samme kjøring
url = article['url'].lower()
if url not in unique_articles:
    unique_articles[url] = article
```

**Mangler:**
- Sjekk mot eksisterende saker i Supabase
- Sjekk mot siste N dager
- Sjekk på tittel-similarity (ikke bare URL)

#### 1.11 Ingen health checks for avhengigheter
**Problem:** Ingen sjekk om Supabase/Brave/OpenAI er oppe før kjøring.

#### 1.12 WebSocket ikke tilgjengelig
**Problem:** `websocket-server` pakke mangler.

```python
# total-control-api.py
try:
    from websocket_server import WebsocketServer
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False
```

**Konsekvens:** Real-time updates fungerer ikke i Mission Control.

---

## 2. DATAFLYT-ANALYSE

### 2.1 Nåværende Dataflyt

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MORNING ROUTINE DATAFLYT                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐              │
│  │ Brave Search │───→│  OpenAI      │───→│  JSON File   │              │
│  │   API        │    │  Titler      │    │  /tmp/...    │              │
│  └──────────────┘    └──────────────┘    └──────┬───────┘              │
│                                                  │                      │
│                       ┌──────────────────────────┘                      │
│                       ↓                                                 │
│              ┌──────────────────┐                                       │
│              │ Python Insert    │                                       │
│              │ Script           │                                       │
│              └────────┬─────────┘                                       │
│                       ↓                                                 │
│              ┌──────────────────┐                                       │
│              │    Supabase      │                                       │
│              │  agenda_items    │                                       │
│              └────────┬─────────┘                                       │
│                       ↓                                                 │
│              ┌──────────────────┐                                       │
│              │ Mission Control  │                                       │
│              │    Frontend      │                                       │
│              └──────────────────┘                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Problemer med nåværende flyt

| Problem | Alvorlighet | Beskrivelse |
|---------|-------------|-------------|
| Ingen transaksjoner | 🔴 Kritisk | Delvis insert mulig |
| Ingen retry | 🔴 Kritisk | API-feil = tapte data |
| File-basert overlevering | 🟡 Høy | Fragil midlertidig lagring |
| Ingen validering | 🟡 Høy | Ugyldig data kan lagres |
| Sync-operasjoner | 🟡 Høy | Blokkerer, tregt |

### 2.3 Foreslått forbedret dataflyt

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FORESLÅTT DATAFLYT (Event-Driven)                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────┐       │
│  │                     MESSAGE QUEUE                           │       │
│  │                 (Redis / In-Memory)                         │       │
│  └─────────────────────────────────────────────────────────────┘       │
│                              ▲                                          │
│          ┌───────────────────┼───────────────────┐                     │
│          ↓                   ↓                   ↓                     │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐              │
│  │   Fetcher    │   │  Processor   │   │   Inserter   │              │
│  │   Service    │   │   Service    │   │   Service    │              │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘              │
│         │                  │                  │                       │
│         ↓                  ↓                  ↓                       │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐              │
│  │ Brave/OpenAI │   │  Transform   │   │  Supabase    │              │
│  │    APIs      │   │   Validate   │   │  (Atomic)    │              │
│  └──────────────┘   └──────────────┘   └──────────────┘              │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────┐       │
│  │                    DEAD LETTER QUEUE                        │       │
│  │              (Failed items for retry)                       │       │
│  └─────────────────────────────────────────────────────────────┘       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.4 Endringsanbefalinger

1. **Implementer event-driven arkitektur**
   - Bruk Redis eller lignende for meldingskø
   - Separate services for fetch, process, insert

2. **Atomic transactions**
   - Wrap alle inserts i én transaksjon
   - Rollback ved feil

3. **Idempotent operations**
   - Sikre at samme sak kan prosesseres flere ganger uten duplikater

4. **Async processing**
   - Ikke blokker på eksterne API-er
   - Bruk asyncio/concurrent.futures

---

## 3. FALLBACK-STRATEGIER

### 3.1 Nåværende fallback (mangler)

| Komponent | Fallback? | Beskrivelse |
|-----------|-----------|-------------|
| Brave Search | ❌ Nei | Ingen fallback hvis API er nede |
| OpenAI | ❌ Nei | Ingen fallback hvis rate limit |
| Supabase | ❌ Nei | Ingen lokal cache |
| ElevenLabs | ✅ Delvis | Lokal cache av TTS |

### 3.2 Anbefalte fallback-strategier

#### Strategi 1: API-fallback kjede
```python
# OpenAI med fallback
async def generate_title(content):
    try:
        return await openai_generate(content)
    except RateLimitError:
        return await openrouter_generate(content)  # Fallback
    except Exception:
        return manual_truncate(content)  # Siste fallback
```

#### Strategi 2: Lokal cache for Supabase
```python
# Redis/Memcached cache
cache_key = f"saker:{date}"
saker = cache.get(cache_key)
if not saker:
    saker = await supabase.get_saker(date)
    cache.set(cache_key, saker, ttl=300)
```

#### Strategi 3: Circuit Breaker pattern
```python
# Forhindre kaskade-feil
@circuit_breaker(threshold=5, timeout=60)
async def brave_search(query):
    return await call_brave_api(query)
```

#### Strategi 4: Graceful degradation
```python
# Mission Control viser cached data hvis Supabase er nede
if supabase_error:
    show_cached_data()
    show_warning("Viser cachet data - ikke sanntid")
```

---

## 4. DATAKONSISTENS-FORSLAG

### 4.1 Schema-validering

**Implementer Pydantic-modeller:**
```python
from pydantic import BaseModel, HttpUrl
from datetime import date
from typing import Optional

class AgendaItem(BaseModel):
    tenant_id: str
    title: str  # max 200 chars
    description: Optional[str]  # max 2000 chars
    category: str  # enum: TALK, REALITY_TV, etc.
    show_date: date
    link_url: Optional[HttpUrl]
    link_metadata: Optional[dict]
    order_index: int = 0
    
    class Config:
        json_schema_extra = {
            "example": {
                "tenant_id": "a0000000-0000-0000-0000-000000000001",
                "title": "Farmen-vinner avslører hemmelighet",
                "category": "REALITY_TV"
            }
        }
```

### 4.2 Database constraints

**Anbefalte SQL-endringer:**
```sql
-- Enforce valid categories
ALTER TABLE agenda_items 
ADD CONSTRAINT valid_category 
CHECK (category IN ('TALK', 'REALITY_TV', 'KJENDIS_DRAMA', 'FILM_TV', 'MUSIKK', 'INTERNASJONALT', 'STATS'));

-- Prevent duplicates
CREATE UNIQUE INDEX idx_unique_sak_per_date 
ON agenda_items(tenant_id, show_date, md5(title));

-- Foreign key validation
ALTER TABLE agenda_items
ADD CONSTRAINT valid_tenant
FOREIGN KEY (tenant_id) REFERENCES tenants(id);
```

### 4.3 Data-klargjøring

**Sanitize før insert:**
```python
def sanitize_agenda_item(item: dict) -> dict:
    return {
        'title': item['title'][:200].strip(),
        'description': clean_html(item.get('description', ''))[:2000],
        'link_url': normalize_url(item.get('link_url')),
        'category': normalize_category(item.get('category')),
        # ...
    }
```

### 4.4 Konsistens-sjekker

**Implementer daglig validering:**
```python
async def validate_data_consistency():
    # Sjekk for duplikater
    duplicates = await find_duplicate_saks()
    
    # Sjekk for manglende metadata
    missing_meta = await find_missing_metadata()
    
    # Sjekk for ugyldige URLs
    invalid_urls = await find_invalid_urls()
    
    # Rapport
    await send_consistency_report(duplicates, missing_meta, invalid_urls)
```

---

## 5. PRIORITERT LISTE OVER INTEGRASJONS-FORBEDRINGER

### 🔴 KRITISK (Umiddelbart)

| # | Forbedring | Innsats | Impact | Kompleksitet |
|---|------------|---------|--------|--------------|
| 1 | **Implementer transaksjonsstyring** i Morning Routine | 4t | Høy | Middels |
| 2 | **Sentraliser API-nøkler** i miljøvariabler | 2t | Høy | Lav |
| 3 | **Legg til retry-mekanisme** med exponential backoff | 4t | Høy | Middels |
| 4 | **Fiks duplisert dashboard-script** (slett/fiks fetch_nrj_dashboard_stats.py) | 1t | Høy | Lav |
| 5 | **Implementer health checks** før job-execution | 3t | Middels | Lav |

**Estimert tid:** 14 timer  
**Dager:** 2-3 dager

---

### 🟡 HOY (Denne uken)

| # | Forbedring | Innsats | Impact | Kompleksitet |
|---|------------|---------|--------|--------------|
| 6 | **Pydantic schema-validering** for alle inserts | 6t | Høy | Middels |
| 7 | **Implementer deduplisering** på tvers av kilder | 4t | Middels | Middels |
| 8 | **Circuit breaker** for eksterne API-er | 4t | Middels | Middels |
| 9 | **Flytt til asyncio** for concurrent API-kall | 8t | Høy | Høy |
| 10 | **Implementer lokal cache** for Supabase | 4t | Middels | Middels |

**Estimert tid:** 26 timer  
**Dager:** 4-5 dager

---

### 🟢 MIDDELS (Denne måneden)

| # | Forbedring | Innsats | Impact | Kompleksitet |
|---|------------|---------|--------|--------------|
| 11 | **Event-driven arkitektur** (Redis kø) | 16t | Høy | Høy |
| 12 | **Database constraints** og indekser | 4t | Middels | Middels |
| 13 | **Automatisk data-validering** (daglig cron) | 4t | Middels | Lav |
| 14 | **WebSocket server** installasjon og konfig | 2t | Middels | Lav |
| 15 | **Observability** (metrikker, tracing) | 8t | Middels | Middels |

**Estimert tid:** 34 timer  
**Dager:** 6-7 dager

---

### 🟣 LAV (Neste kvartal)

| # | Forbedring | Innsats | Impact | Kompleksitet |
|---|------------|---------|--------|--------------|
| 16 | **Microservices-arkitektur** | 40t | Høy | Høy |
| 17 | **Automatisk skalering** | 16t | Middels | Høy |
| 18 | **Multi-region støtte** | 24t | Lav | Høy |

---

## 6. KONKLUSJON

Systemet har betydelig teknisk gjeld som påvirker pålitelighet. De kritiske problemene bør adresseres umiddelbart for å forhindre data-tap og inkonsistens.

### Anbefalt veikart:

**Uke 1:** Kritiske fikser (transaksjoner, API-nøkler, retry)  
**Uke 2:** Datakvalitet (validering, deduplisering)  
**Uke 3-4:** Arkitektur (async, cache, event-driven)  
**Måned 2+:** Observability og optimalisering  

**Totalt estimert innsats:** ~74 timer (ca. 4 uker for 1 utvikler)

---

**Rapport generert:** 2026-03-11  
**Neste review:** Anbefales innen 30 dager
