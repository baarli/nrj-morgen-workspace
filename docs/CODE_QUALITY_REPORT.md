# 🔍 CODE QUALITY & ERROR HANDLING ANALYSIS REPORT

**Dato:** 2026-03-11  
**Analyst:** Vev Code Quality System  
**Scope:** /root/.openclaw/workspace/scripts/  
**Totalt antall scripts:** 273 filer

---

## 📊 EXECUTIVE SUMMARY

Systemet har **alvorlige kodekvalitetsproblemer** som må adresseres umiddelbart:

| Kategori | Status | Alvorlighet |
|----------|--------|-------------|
| Hardkodede credentials | 🔴 FUNNET | KRITISK |
| Silent exception handling | 🔴 FUNNET | HØY |
| Manglende logging | 🟡 DELVIS | MIDDELS |
| Ingen retry-logikk | 🟡 DELVIS | MIDDELS |
| Ulik error handling | 🔴 FUNNET | HØY |

---

## 🚨 KRITISKE FUNN

### 1. HARDCODED CREDENTIALS (KRITISK)

**Følgende scripts har hardkodede API-nøkler og tokens:**

#### morning-routine-complete.py
```python
# Linje 14-18 - HARDCODED SUPABASE CREDENTIALS
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIs..."
TENANT_ID = "a0000000-0000-0000-0000-000000000001"
CREATED_BY = "10aa1508-6d52-490c-8ae5-fa3da9a152c4"
```

#### ai_images_all.py
```python
# Linje 18-20 - HARDCODED SUPABASE CREDENTIALS
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### insert_to_supabase.py
```python
# Linje 11-12 - HARDCODED SUPABASE CREDENTIALS
SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Risiko:** 
- Kompromittert sikkerhet ved GitHub-commit
- Tokens kan lekkes i commit-historie
- Ingen rotasjon av credentials

---

### 2. SILENT EXCEPTION HANDLING (HØY ALVORLIGHET)

**try-except blokker som svelger feil uten logging:**

#### morning-routine-complete.py
```python
# Linje 93-94
except Exception as e:
    socket.setdefaulttimeout(None)
    return None  # ❌ Ingen logging!

# Linje 191-193
except Exception as e:
    print(f"❌ ({str(e)[:30]})")
    image_urls[i] = None

# Linje 227-228
except Exception as e:
    print(f"❌ {str(e)[:30]}")
```

#### brave-news-search.py
```python
# Linje 30-32
except Exception as e:
    socket.setdefaulttimeout(None)
    return None  # ❌ Ingen logging!

# Linje 143-144
except Exception as e:
    print(f"   ⚠️  {completed}/{len(search_queries)}: {query[:30]}... (feil)")
    # ❌ Feilen logges ikke for debugging!
```

#### ai_images_all.py
```python
# Linje 122-124
except Exception as e:
    print(f"      ⚠️  Feil: {str(e)[:50]}")
    return None  # ❌ Generisk exception, spesifikke feil går tapt
```

**Problem:** Feil blir fanget men ikke logget til fil, kun stdout. Dette gjør debugging nesten umulig.

---

### 3. MANGEL PÅ KONSISTENT LOGGING

**Ingen standardisert logging i de fleste scripts:**

| Script | Logger til fil | Logger til stdout | Standard format |
|--------|---------------|-------------------|-----------------|
| morning-routine-complete.py | ❌ Nei | ✅ Ja (print) | ❌ Nei |
| brave-news-search.py | ❌ Nei | ✅ Ja (print) | ❌ Nei |
| ai_images_all.py | ❌ Nei | ✅ Ja (print) | ❌ Nei |
| vev-telegram-auto-responder.py | ✅ Ja | ✅ Ja | ✅ Ja (custom) |
| baarliclaw_toolkit.py | ✅ Ja | ✅ Ja | ✅ Ja |

**Problem:** 
- Ingen sentralisert loggfil for debugging
- Ulikt format på tvers av scripts
- Ingen log-rotasjon
- Ingen log-nivåer (DEBUG, INFO, ERROR)

---

### 4. MANGEL PÅ RETRY-LOGIKK

**Scripts som kaller eksterne API-er uten retry:**

```python
# morning-routine-complete.py - Linje 62-73
try:
    socket.setdefaulttimeout(15)
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as response:
        data = json.loads(response.read().decode())
        return data
except Exception as e:
    return None  # ❌ Ingen retry!
```

```python
# insert_to_supabase.py - Linje 75-82
response = requests.post(
    f"{SUPABASE_URL}/rest/v1/agenda_items",
    headers=headers,
    json=payload
)

if response.status_code not in [200, 201]:
    print(f"    Feil: {response.status_code}")  # ❌ Ingen retry!
```

**API-kall som mangler retry:**
- Brave Search API
- OpenAI Image Generation API
- Supabase REST API
- Telegram API

---

### 5. ULIK ERROR HANDLING PÅ TVERS AV SCRIPTS

**3 forskjellige patterns brukes:**

#### Pattern A: Silent failure (morning-routine-complete.py)
```python
try:
    result = api_call()
except:
    return None
```

#### Pattern B: Print og fortsett (brave-news-search.py)
```python
try:
    result = api_call()
except Exception as e:
    print(f"Error: {e}")
    continue
```

#### Pattern C: Raise (vev-telegram-auto-responder.py)
```python
try:
    result = api_call()
except Exception as e:
    log(f"Error: {e}")
    raise
```

**Problem:** Ingen konsistens gjør koden vanskelig å vedlikeholde og debugge.

---

## 📋 PRIORITERT LISTE OVER SCRIPTS SOM TRENGER REFAKTURERING

### 🔴 KRITISK (Umiddelbar handling påkrevd)

| # | Script | Problem | Estimert tid |
|---|--------|---------|--------------|
| 1 | morning-routine-complete.py | Hardcoded credentials, silent exceptions, ingen retry | 4 timer |
| 2 | ai_images_all.py | Hardcoded credentials, ingen retry, dårlig error handling | 3 timer |
| 3 | insert_to_supabase.py | Hardcoded credentials, ingen retry | 2 timer |
| 4 | brave-news-search.py | Silent exceptions, ingen retry | 2 timer |

### 🟡 HØY (Bør fikses innen 1 uke)

| # | Script | Problem | Estimert tid |
|---|--------|---------|--------------|
| 5 | vev-telegram-auto-responder.py | Dårlig error recovery | 2 timer |
| 6 | content-hub-api.py | Ingen retry, dårlig error logging | 1.5 timer |
| 7 | integrated-morning-routine.sh | Feil håndtering i embedded Python | 2 timer |

### 🟢 MIDDELS (Bør fikses innen 1 måned)

| # | Script | Problem | Estimert tid |
|---|--------|---------|--------------|
| 8 | All fetch_* scripts | Ingen konsistent retry | 3 timer |
| 9 | All update_* scripts | Ingen transaksjonshåndtering | 2 timer |
| 10 | Shell scripts | Ingen feilhåndtering (set -e mangler) | 2 timer |

---

## 💡 ANBEFALTE LØSNINGER

### 1. Standardisert Base Script Mal

Opprett `/root/.openclaw/workspace/scripts/base_script.py`:

```python
#!/usr/bin/env python3
"""
Base script template for all Vev scripts.
Provides: logging, error handling, retry logic, credential management
"""

import os
import sys
import json
import logging
import traceback
from pathlib import Path
from datetime import datetime
from functools import wraps
from typing import Optional, Dict, Any, Callable
import time
import random

# === KONFIGURASJON ===
WORKSPACE = Path("/root/.openclaw/workspace")
LOG_DIR = WORKSPACE / "brain" / "logs"
CREDENTIALS_DIR = WORKSPACE / ".credentials"

# === LOGGING SETUP ===
def setup_logging(name: str, log_to_file: bool = True) -> logging.Logger:
    """Set up consistent logging for all scripts"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Fjern eksisterende handlers
    logger.handlers = []
    
    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    console.setFormatter(console_format)
    logger.addHandler(console)
    
    # File handler
    if log_to_file:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_file = LOG_DIR / f"{name}_{datetime.now():%Y%m%d}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger

# === CREDENTIAL MANAGEMENT ===
class CredentialManager:
    """Secure credential management"""
    
    def __init__(self):
        self._cache: Dict[str, str] = {}
        self.logger = setup_logging("CredentialManager", log_to_file=False)
    
    def load_env_file(self, filepath: str) -> Dict[str, str]:
        """Load environment variables from file"""
        env_vars = {}
        path = Path(filepath)
        
        if not path.exists():
            self.logger.error(f"Credential file not found: {filepath}")
            return env_vars
        
        try:
            with open(path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        # Remove inline comments
                        value = value.split('#')[0].strip()
                        # Remove quotes
                        value = value.strip('"').strip("'")
                        env_vars[key] = value
        except Exception as e:
            self.logger.error(f"Failed to load credentials: {e}")
            raise
        
        return env_vars
    
    def get_credential(self, name: str, env_file: Optional[str] = None) -> str:
        """Get credential from environment or file"""
        # Check cache
        if name in self._cache:
            return self._cache[name]
        
        # Check environment
        value = os.environ.get(name)
        if value:
            self._cache[name] = value
            return value
        
        # Load from file
        if env_file:
            creds = self.load_env_file(env_file)
            value = creds.get(name)
            if value:
                self._cache[name] = value
                return value
        
        # Try common credential files
        for cred_file in ["nrj-morgen.env", "live-search.env", "telegram-bot.env"]:
            filepath = CREDENTIALS_DIR / cred_file
            if filepath.exists():
                creds = self.load_env_file(filepath)
                value = creds.get(name)
                if value:
                    self._cache[name] = value
                    return value
        
        raise ValueError(f"Credential not found: {name}")

# === RETRY DECORATOR ===
def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: tuple = (Exception,),
    on_retry: Optional[Callable] = None
):
    """Decorator for retry with exponential backoff and jitter"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__module__)
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        logger.error(f"All {max_retries} retries failed for {func.__name__}: {e}")
                        raise last_exception
                    
                    # Exponential backoff with jitter
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    jitter = random.uniform(0, delay * 0.1)
                    total_delay = delay + jitter
                    
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_retries + 1} failed for {func.__name__}: {e}. "
                        f"Retrying in {total_delay:.1f}s..."
                    )
                    
                    if on_retry:
                        on_retry(attempt, e, total_delay)
                    
                    time.sleep(total_delay)
            
            raise last_exception  # Should never reach here
        return wrapper
    return decorator

# === ERROR HANDLER ===
class ScriptError(Exception):
    """Base exception for script errors"""
    pass

class APIError(ScriptError):
    """API-related errors"""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

class CredentialError(ScriptError):
    """Credential-related errors"""
    pass

def handle_error(logger: logging.Logger, error: Exception, context: Optional[Dict] = None) -> None:
    """Centralized error handling"""
    error_info = {
        "timestamp": datetime.now().isoformat(),
        "type": type(error).__name__,
        "message": str(error),
        "traceback": traceback.format_exc(),
        "context": context or {}
    }
    
    logger.error(f"Error in {context.get('function', 'unknown')}: {error}")
    logger.debug(f"Full traceback:\n{error_info['traceback']}")
    
    # Could also send to error tracking service here
    return error_info

# === BASE SCRIPT CLASS ===
class BaseScript:
    """Base class for all scripts"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = setup_logging(name)
        self.credentials = CredentialManager()
        self.start_time = datetime.now()
    
    def run(self) -> int:
        """Main entry point - override in subclass"""
        raise NotImplementedError("Subclasses must implement run()")
    
    def get_credential(self, name: str) -> str:
        """Get credential securely"""
        try:
            return self.credentials.get_credential(name)
        except ValueError as e:
            self.logger.error(f"Missing credential: {name}")
            raise CredentialError(f"Missing credential: {name}") from e
    
    def log_summary(self, success: bool, details: Optional[Dict] = None):
        """Log execution summary"""
        duration = (datetime.now() - self.start_time).total_seconds()
        status = "SUCCESS" if success else "FAILED"
        
        self.logger.info(f"=== Script {self.name} {status} ===")
        self.logger.info(f"Duration: {duration:.2f}s")
        
        if details:
            for key, value in details.items():
                self.logger.info(f"{key}: {value}")

# === USAGE EXAMPLE ===
if __name__ == "__main__":
    # Example usage
    logger = setup_logging("example")
    logger.info("Base script template loaded successfully")
```

### 2. Refactored morning-routine-complete.py (Eksempel)

```python
#!/usr/bin/env python3
"""
NRJ MORGEN - Refactored with proper error handling
"""

import sys
import json
import concurrent.futures
import urllib.request
import urllib.parse
import uuid
import time
from datetime import datetime
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from base_script import BaseScript, retry_with_backoff, APIError, handle_error

class MorningRoutine(BaseScript):
    """NRJ Morgen morning routine with proper error handling"""
    
    def __init__(self):
        super().__init__("morning-routine")
        
        # Load credentials securely - NO HARDCODED VALUES
        self.supabase_url = self.get_credential("SUPABASE_URL")
        self.supabase_key = self.get_credential("SUPABASE_SERVICE_KEY")
        self.brave_key = self.get_credential("BRAVE_API_KEY")
        self.openai_key = self.get_credential("OPENAI_API_KEY")
        
        self.tenant_id = self.get_credential("TENANT_ID")
        self.created_by = self.get_credential("USER_ID")
        self.bucket_name = "media-library"
    
    @retry_with_backoff(max_retries=3, base_delay=2.0, exceptions=(urllib.error.URLError, TimeoutError))
    def search_brave(self, query: str, count: int = 10) -> Optional[dict]:
        """Search with Brave API - with retry logic"""
        encoded_query = urllib.parse.quote(query)
        url = f"https://api.search.brave.com/res/v1/news/search?q={encoded_query}&count={count}"
        
        headers = {
            'X-Subscription-Token': self.brave_key,
            'Accept': 'application/json'
        }
        
        req = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            self.logger.error(f"Brave API HTTP {e.code}: {e.reason}")
            if e.code == 429:  # Rate limited
                raise  # Will trigger retry
            raise APIError(f"Brave API error: {e.reason}", status_code=e.code)
    
    def insert_to_supabase(self, articles: list, image_urls: dict) -> int:
        """Insert articles with proper error handling"""
        inserted = 0
        
        for i, article in enumerate(articles, 1):
            try:
                payload = {
                    'id': str(uuid.uuid4()),
                    'tenant_id': self.tenant_id,
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'link_url': article.get('url', ''),
                    'show_date': datetime.now().strftime("%Y-%m-%d"),
                    'category': 'TALK',
                    'created_by': self.created_by,
                    'order_index': i
                }
                
                if image_urls.get(i):
                    payload['link_metadata'] = {'image_url': image_urls[i]}
                
                # Insert with retry
                self._supabase_insert(payload)
                inserted += 1
                
            except Exception as e:
                handle_error(self.logger, e, {
                    'function': 'insert_to_supabase',
                    'article_index': i,
                    'article_title': article.get('title', 'unknown')
                })
                # Continue with next article
                continue
        
        return inserted
    
    @retry_with_backoff(max_retries=3, base_delay=1.0)
    def _supabase_insert(self, payload: dict) -> None:
        """Internal method with retry logic"""
        req = urllib.request.Request(
            f"{self.supabase_url}/rest/v1/agenda_items",
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'apikey': self.supabase_key,
                'Authorization': f'Bearer {self.supabase_key}',
                'Content-Type': 'application/json',
                'Prefer': 'return=minimal'
            }
        )
        
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status not in [200, 201]:
                raise APIError(f"Supabase insert failed: {resp.status}", status_code=resp.status)
    
    def run(self) -> int:
        """Main execution"""
        try:
            self.logger.info("=== NRJ Morgen Morning Routine Started ===")
            
            # Validate credentials
            if not all([self.brave_key, self.openai_key]):
                raise CredentialError("Missing required API keys")
            
            # Search for articles
            articles = self.search_all()
            self.logger.info(f"Found {len(articles)} articles")
            
            # Generate images
            image_urls = self.generate_images(articles[:15])
            
            # Insert to database
            inserted = self.insert_to_supabase(articles[:15], image_urls)
            
            # Log summary
            self.log_summary(success=True, details={
                "articles_found": len(articles),
                "articles_inserted": inserted,
                "images_generated": sum(1 for v in image_urls.values() if v)
            })
            
            return 0
            
        except Exception as e:
            handle_error(self.logger, e, {'function': 'run'})
            self.log_summary(success=False)
            return 1

if __name__ == '__main__':
    script = MorningRoutine()
    sys.exit(script.run())
```

### 3. Credentials Security Checklist

- [ ] Fjern ALL hardkodede credentials fra scripts
- [ ] Lag sentral `.credentials/` mappe med riktige filrettigheter (chmod 600)
- [ ] Bruk `CredentialManager` klasse for all credential-håndtering
- [ ] Legg til `.credentials/` i `.gitignore`
- [ ] Roter eksponerte tokens umiddelbart
- [ ] Sett opp credential rotation schedule

---

## 🛠️ IMPLEMENTASJONSPLAN

### Fase 1: Kritiske sikkerhetsfikser (1-2 dager)
1. [ ] Roter alle eksponerte Supabase tokens
2. [ ] Fjern hardkodede credentials fra morning-routine-complete.py
3. [ ] Fjern hardkodede credentials fra ai_images_all.py
4. [ ] Fjern hardkodede credentials fra insert_to_supabase.py
5. [ ] Opprett base_script.py

### Fase 2: Error handling refactor (3-5 dager)
1. [ ] Refactor morning-routine-complete.py med base_script
2. [ ] Refactor brave-news-search.py med base_script
3. [ ] Refactor ai_images_all.py med base_script
4. [ ] Legg til retry-logikk på alle API-kall

### Fase 3: Shell script standardisering (2 dager)
1. [ ] Legg til `set -euo pipefail` i alle shell scripts
2. [ ] Standardiser error handling i shell scripts
3. [ ] Legg til logging i shell scripts

### Fase 4: Testing og validering (2 dager)
1. [ ] Skriv unit tests for base_script
2. [ ] Test alle refactored scripts
3. [ ] Verifiser at credentials ikke lekker

---

## 📊 EKSISTERENDE GODE EKSEMPLER

### ✅ vev-telegram-auto-responder.py
- Har egen log-funksjon som skriver til fil
- Bruker try-except med logging
- Har state management

### ✅ error_toolkit.py
- God struktur for error handling
- RetryManager med exponential backoff
- ErrorFormatter for ulike output-formater

### ✅ decorator_toolkit.py
- Gjenbrukbare dekoratorer
- Retry-dekorator
- Timer-dekorator

### ✅ retry_wrapper.py
- God retry-implementasjon med jitter
- Konfigurerbar backoff

---

## 🎯 KONKLUSJON

Systemet har **kritiske sikkerhetshull** som må fikses umiddelbart:
1. **Hardkodede credentials** i minst 3 scripts
2. **Silent exception handling** som gjør debugging umulig
3. **Ingen retry-logikk** for API-kall

**Anbefalt prioritering:**
1. Roter tokens umiddelbart
2. Implementer base_script.py
3. Refactor kritisk scripts
4. Standardiser på tvers av codebase

**Estimert tidsforbruk:** 5-7 dager for full implementasjon

---

*Rapport generert av Vev Code Quality Analysis System*
*Dato: 2026-03-11*
