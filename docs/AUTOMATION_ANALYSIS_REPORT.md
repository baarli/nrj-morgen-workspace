# 🤖 VEV AUTOMATION & CRON JOB SYSTEM - ANALYSERAPPORT
**Dato:** 2026-03-11  
**Analyst:** Vev System Audit  
**Status:** 🔴 KRITISKE FUNN IDENTIFISERT

---

## 📊 EKSEKUTIV OPPSUMMERING

| Kategori | Status | Prioritet |
|----------|--------|-----------|
| Cron-jobb optimalisering | 🟡 TILBEHØR FORBEDRING | Medium |
| Redundante scripts | 🔴 HØYT ANTALL | Høy |
| Logging | 🟡 DELVIS OK | Medium |
| Retry-mekanismer | 🔴 MANGELFULLT | Høy |
| Notifikasjoner | 🟡 BASALT | Medium |
| Feilhåndtering | 🔴 SVAKT | Høy |

**Totalt antall scripts:** 263 filer (2.3MB)  
**Aktive cron-jobber:** 5 jobber  
**System-tjenester:** 3 (file-watcher, mission-control-api, telegram-responder)

---

## 1️⃣ CRON-JOBBER ANALYSE

### Nåværende Cron-oppsett

```cron
*/5 * * * * /bin/bash /root/.openclaw/workspace/scripts/vev-work-monitor.sh
0 * * * * /bin/bash /root/.openclaw/workspace/scripts/vev-autonomous-executor.sh
*/30 * * * * /bin/bash /root/.openclaw/workspace/scripts/vev-task-suggester.sh
0 3 * * * /bin/bash /root/.openclaw/workspace/scripts/vev-nightly-github-backup.sh
* * * * * /bin/bash /root/.openclaw/workspace/scripts/vev-activity-tracker.sh
```

### Identifiserte Problemer

| Problem | Alvorlighet | Beskrivelse |
|---------|-------------|-------------|
| **Overlappende jobber** | 🟡 Medium | `vev-autonomous-executor.sh` (hver time) og `vev-work-monitor.sh` (hvert 5. min) kan konflikte |
| **Manglende stagger** | 🟡 Medium | Ingen tidsforskyvning - alle kjører på hele minutter |
| **Ingen låsmekanisme** | 🔴 Høy | Ingen forhindring av overlappende kjøringer av samme script |
| **Manglende retry** | 🔴 Høy | Ingen automatisk retry ved feil |
| **Stdout redirect til /dev/null** | 🟡 Medium | Hindrer debugging - all output kastes |

### Forslag til Forbedret Cron-oppsett

```cron
# === SYSTEM OVERVÅKNING ===
# Activity tracker - hvert minutt
* * * * * /bin/bash /root/.openclaw/workspace/scripts/vev-activity-tracker.sh >> /var/log/vev/activity.log 2>&1

# Work monitor - hvert 5. minutt med lås
*/5 * * * * flock -n /var/lock/vev-work-monitor.lock /bin/bash /root/.openclaw/workspace/scripts/vev-work-monitor.sh >> /var/log/vev/monitor.log 2>&1

# === HOVEDARBEID ===
# Autonomous executor - hver time på minutt 5 (unngå kollisjon med andre)
5 * * * * flock -n /var/lock/vev-executor.lock /bin/bash /root/.openclaw/workspace/scripts/vev-autonomous-executor.sh >> /var/log/vev/executor.log 2>&1

# Task suggester - hver halvtime på minutt 15 og 45
15,45 * * * * flock -n /var/lock/vev-suggester.lock /bin/bash /root/.openclaw/workspace/scripts/vev-task-suggester.sh >> /var/log/vev/suggester.log 2>&1

# === BACKUP ===
# Nightly backup - kl 03:00 med retry
0 3 * * * flock -n /var/lock/vev-backup.lock /bin/bash /root/.openclaw/workspace/scripts/vev-nightly-github-backup.sh >> /var/log/vev/backup.log 2>&1 || (sleep 300 && flock -n /var/lock/vev-backup.lock /bin/bash /root/.openclaw/workspace/scripts/vev-nightly-github-backup.sh)

# === WEEKLY MAINTENANCE ===
# Log rotation - søndag kl 04:00
0 4 * * 0 /bin/bash /root/.openclaw/workspace/scripts/log-rotation.sh

# System cleanup - søndag kl 05:00  
0 5 * * 0 flock -n /var/lock/vev-cleanup.lock /bin/bash /root/.openclaw/workspace/scripts/system_cleanup.sh
```

---

## 2️⃣ REDUNDANTE OG UTDATERTE SCRIPTS

### 🔴 HØY REDUNDANS - Morning Routine (10+ varianter)

| Script | Status | Beskrivelse | Anbefaling |
|--------|--------|-------------|------------|
| `morning-routine.sh` | 🟡 Utdatert | Original versjon | **SLETT** |
| `morning-routine.sh.backup` | 🔴 Utdatert | Backup av gammel versjon | **SLETT** |
| `morning-routine-v2.py` | 🟡 Utdatert | Versjon 2.0 | **SLETT** |
| `morning-routine-v2.1.py` | 🟢 Aktiv | Versjon 2.1 - brukes i integrert rutine | BEHOLD |
| `morning-routine-complete.py` | 🟡 Overlappende | Komplett med AI-bilder | **KONSOLIDER** |
| `consolidated-morning-routine.py` | 🟡 Overlappende | Konsolidert versjon med email | **KONSOLIDER** |
| `integrated-morning-routine.sh` | 🟢 Master | Hovedscript som orkestrerer | BEHOLD |
| `morning_routine_enhancer.py` | 🔴 Utdatert | Enhancer-modul | **SLETT** |
| `insert-morning-news.py` | 🟡 Overlappende | Separat insert-script | **KONSOLIDER** |

### 🔴 HØY REDUNDANS - Dashboard Updates (8+ varianter)

| Script | Status | Beskrivelse | Anbefaling |
|--------|--------|-------------|------------|
| `update_nrj_dashboard.py` | 🟢 Aktiv | Hovedscript - oppdaterer eksisterende panel | BEHOLD |
| `trigger_nrj_dashboard_update.py` | 🟢 Aktiv | Trigger Supabase Edge Functions | BEHOLD |
| `fetch_nrj_dashboard_stats.py` | 🔴 Utdatert | V1 - oppretter nytt item i sakslista | **SLETT** |
| `fetch_nrj_dashboard_stats_v2.py` | 🟡 Overlappende | V2 - dashboard JSON format | **KONSOLIDER** |
| `show_nrj_dashboard_data.py` | 🔴 Utdatert | Visningsscript | **SLETT** |
| `insert_nrj_dashboard_data.py` | 🔴 Utdatert | Separat insert | **SLETT** |
| `update_nielsen_radio_stats.py` | 🟡 Overlappende | Kun Nielsen | **KONSOLIDER** |
| `update_nrj_podcast_dashboard.py` | 🟡 Overlappende | Kun Podkast | **KONSOLIDER** |
| `radio-stats-updater.py` | 🔴 Utdatert | Gammel versjon | **SLETT** |
| `radio-stats-updater-v2.py` | 🟡 Overlappende | V2 av radio stats | **KONSOLIDER** |

### 🟡 MEDIUM REDUNDANS - Backup Scripts

| Script | Status | Beskrivelse | Anbefaling |
|--------|--------|-------------|------------|
| `vev-nightly-github-backup.sh` | 🟢 Aktiv | Hoved backup - GitHub push | BEHOLD |
| `smart_backup_service.py` | 🟡 Delvis brukt | Versjonering og deduplisering | VURDER |
| `auto_backup.py` | 🔴 Utdatert | Gammel auto-backup | **SLETT** |

### 🟡 MEDIUM REDUNDANS - Andre Duplikater

| Script | Duplikat av | Anbefaling |
|--------|-------------|------------|
| `update_article_images.py` | `update_description_images.py` | **KONSOLIDER** |
| `ai_image_generator.py` | `ai-image-generator.py` (forskjellig case) | **KONSOLIDER** |
| `dashboard.sh` | `agent-dashboard.sh` | **KONSOLIDER** |
| `vev-system-updater.py` | `system_analyzer.py` | **KONSOLIDER** |

### 📋 ANBEFALT SLETTLISTE (16 scripts)

```bash
# Morning routine duplikater
rm /root/.openclaw/workspace/scripts/morning-routine.sh
rm /root/.openclaw/workspace/scripts/morning-routine.sh.backup
rm /root/.openclaw/workspace/scripts/morning-routine-v2.py
rm /root/.openclaw/workspace/scripts/morning_routine_enhancer.py
rm /root/.openclaw/workspace/scripts/insert-morning-news.py

# Dashboard duplikater
rm /root/.openclaw/workspace/scripts/fetch_nrj_dashboard_stats.py
rm /root/.openclaw/workspace/scripts/show_nrj_dashboard_data.py
rm /root/.openclaw/workspace/scripts/insert_nrj_dashboard_data.py
rm /root/.openclaw/workspace/scripts/radio-stats-updater.py
rm /root/.openclaw/workspace/scripts/update_nielsen_radio_stats.py
rm /root/.openclaw/workspace/scripts/update_nrj_podcast_dashboard.py

# Backup duplikater
rm /root/.openclaw/workspace/scripts/auto_backup.py

# Andre duplikater
rm /root/.openclaw/workspace/scripts/dashboard.sh
rm /root/.openclaw/workspace/scripts/vev-system-updater.py
```

---

## 3️⃣ KONSOLIDERINGSFORSLAG

### Forslag 1: Unified Morning Routine

**Ny fil:** `scripts/vev-morning-routine-master.py`

```python
#!/usr/bin/env python3
"""
VEV MORNING ROUTINE MASTER v3.0
Konsolidert versjon som erstatter:
- morning-routine-v2.1.py
- morning-routine-complete.py
- consolidated-morning-routine.py
- insert-morning-news.py
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/scripts')

from retry_wrapper import retry_with_backoff
from notification_service import NotificationService
import logging

# Konfigurer logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/vev/morning-routine.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('morning-routine')

class MorningRoutineMaster:
    def __init__(self):
        self.notifier = NotificationService()
        self.stats = {
            'articles_found': 0,
            'articles_inserted': 0,
            'images_generated': 0,
            'errors': []
        }
    
    @retry_with_backoff(max_retries=3, base_delay=5)
    def search_news(self):
        """Søk etter nyheter med retry"""
        logger.info("Starter nyhetssøk...")
        # ... implementasjon
    
    @retry_with_backoff(max_retries=3, base_delay=2)
    def insert_to_supabase(self, articles):
        """Insert til Supabase med retry"""
        logger.info(f"Inserter {len(articles)} artikler...")
        # ... implementasjon
    
    def run(self):
        """Hovedflyt med feilhåndtering"""
        try:
            self.notifier.notify(
                title="Morning Routine Startet",
                message="Henter 15 saker med AI-bilder...",
                level="info",
                source="morning-routine"
            )
            
            # Kjør rutine
            articles = self.search_news()
            inserted = self.insert_to_supabase(articles)
            
            # Rapporter suksess
            self.notifier.notify(
                title="Morning Routine Fullført",
                message=f"✅ {inserted}/15 saker lagt til sakslista",
                level="info",
                source="morning-routine"
            )
            
        except Exception as e:
            logger.error(f"Morning routine feilet: {e}")
            self.notifier.notify(
                title="Morning Routine FEILET",
                message=str(e),
                level="critical",
                source="morning-routine"
            )
            raise

if __name__ == '__main__':
    routine = MorningRoutineMaster()
    routine.run()
```

### Forslag 2: Unified Dashboard Updater

**Ny fil:** `scripts/vev-dashboard-updater.py`

```python
#!/usr/bin/env python3
"""
VEV DASHBOARD UPDATER v2.0
Konsolidert versjon som erstatter:
- update_nrj_dashboard.py
- trigger_nrj_dashboard_update.py
- fetch_nrj_dashboard_stats_v2.py
- radio-stats-updater-v2.py
"""

from retry_wrapper import retry_with_backoff
from notification_service import NotificationService

class DashboardUpdater:
    SOURCES = {
        'nielsen': {
            'url': 'https://eu-iport.nielsen-iwatch.com/api/Chart?...',
            'timeout': 30,
            'retries': 3
        },
        'podtoppen': {
            'url': 'https://podtoppen.tnslistene.no/export.php',
            'timeout': 30,
            'retries': 3
        }
    }
    
    @retry_with_backoff(max_retries=3, base_delay=5, exceptions=(Exception,))
    def update_source(self, source_name):
        """Oppdater en datakilde med retry"""
        # ... implementasjon
```

---

## 4️⃣ LOGGING ANALYSE

### Nåværende Loggstruktur

```
/root/.openclaw/workspace/brain/logs/
├── auto-sync.log              (14KB)
├── doc-auto-update.log        (2KB)
├── file-watcher.log           (14KB)
├── health-monitor.log         (399B)
├── learning-loop.log          (14KB)
├── nightly-github-backup.log  (5KB)
├── subagent.log               (240B)
├── task-suggester.log         (5KB)
├── telegram-auto-responder.log (420KB - STØRST)
├── vev-activity.log           (1KB)
├── vev-autonomous.log         (1KB)
├── vev-discovery.log          (534B)
├── vev-minute-reports.log     (857KB)
└── vev-progress.log           (23KB)
```

### Identifiserte Problemer

| Problem | Alvorlighet | Beskrivelse |
|---------|-------------|-------------|
| **Ingen logg-rotasjon** | 🔴 Høy | `telegram-auto-responder.log` er 420KB og vokser |
| **Ingen sentralisert logging** | 🟡 Medium | Logger spredt på ulike steder |
| **Ulikt loggformat** | 🟡 Medium | Noen logger har timestamps, andre ikke |
| **Ingen logg-nivåer** | 🟡 Medium | Ikke differensiert mellom INFO, WARN, ERROR |
| **Manglende strukturerte logger** | 🟡 Medium | Ingen JSON-logging for enkel parsing |

### Foreslått Loggstruktur

```
/var/log/vev/                    # Sentral logg-mappe
├── morning-routine/
│   ├── 2026-03-11.log
│   ├── 2026-03-10.log
│   └── current -> 2026-03-11.log
├── dashboard/
│   ├── 2026-03-11.log
│   └── current
├── backup/
│   └── nightly.log
├── telegram/
│   ├── responder.log          (rotasjon ved 10MB)
│   └── voice.log
├── system/
│   ├── executor.log
│   ├── monitor.log
│   └── suggester.log
└── errors/
    ├── 2026-03-11-errors.json
    └── current
```

### Ny Logg-wrapper

**Fil:** `scripts/vev_logger.py`

```python
#!/usr/bin/env python3
"""
VEV Standard Logger - Ensartet logging på tvers av alle scripts
"""

import logging
import json
import sys
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler

class VevLogger:
    """Standardisert logger for Vev-systemet"""
    
    LOG_DIR = Path('/var/log/vev')
    
    def __init__(self, name: str, log_dir: str = None):
        self.name = name
        self.log_dir = Path(log_dir) if log_dir else self.LOG_DIR / name
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Hovedlogger
        self.logger = logging.getLogger(f'vev.{name}')
        self.logger.setLevel(logging.DEBUG)
        
        # Unngå duplikat handlers
        if self.logger.handlers:
            return
        
        # Formater
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Daglig loggfil
        daily_file = self.log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        file_handler = logging.FileHandler(daily_file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        
        # Roterende error-logg
        error_file = self.log_dir / 'errors.log'
        error_handler = RotatingFileHandler(error_file, maxBytes=10*1024*1024, backupCount=5)
        error_handler.setFormatter(formatter)
        error_handler.setLevel(logging.ERROR)
        
        # Konsoll output
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, msg: str, extra: dict = None):
        self.logger.info(msg, extra=extra)
    
    def warning(self, msg: str, extra: dict = None):
        self.logger.warning(msg, extra=extra)
    
    def error(self, msg: str, extra: dict = None):
        self.logger.error(msg, extra=extra)
    
    def critical(self, msg: str, extra: dict = None):
        self.logger.critical(msg, extra=extra)
    
    def structured(self, level: str, message: str, data: dict):
        """Logg strukturert JSON-data"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'logger': self.name,
            'level': level,
            'message': message,
            'data': data
        }
        
        structured_file = self.log_dir / 'structured.jsonl'
        with open(structured_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
```

---

## 5️⃣ RETRY-MEKANISMER

### Nåværende Status

| Script | Har Retry | Type | Kommentar |
|--------|-----------|------|-----------|
| `retry_wrapper.py` | ✅ | Dekorator | Eksisterer men brukes ikke konsekvent |
| `morning-routine-v2.1.py` | ❌ | - | Ingen retry ved API-feil |
| `update_nrj_dashboard.py` | ❌ | - | Ingen retry ved nettverksfeil |
| `vev-telegram-auto-responder.py` | ❌ | - | Ingen retry ved send-feil |
| `vev-nightly-github-backup.sh` | ❌ | - | Ingen retry ved push-feil |

### Foreslått Retry-Strategi

**Fil:** `scripts/vev_retry_policy.py`

```python
#!/usr/bin/env python3
"""
VEV Retry Policies - Standardiserte retry-konfigurasjoner
"""

from retry_wrapper import retry_with_backoff

class VevRetryPolicies:
    """Standard retry-konfigurasjoner for ulike typer operasjoner"""
    
    # API-kall (eksterne tjenester)
    API_CALL = retry_with_backoff(
        max_retries=3,
        base_delay=2,
        max_delay=30,
        exceptions=(Exception,)
    )
    
    # Nettverksoperasjoner
    NETWORK = retry_with_backoff(
        max_retries=5,
        base_delay=5,
        max_delay=60,
        exceptions=(ConnectionError, TimeoutError)
    )
    
    # Database-operasjoner
    DATABASE = retry_with_backoff(
        max_retries=3,
        base_delay=1,
        max_delay=10,
        exceptions=(Exception,)
    )
    
    # Git-operasjoner
    GIT = retry_with_backoff(
        max_retries=3,
        base_delay=10,
        max_delay=120,
        exceptions=(Exception,)
    )
    
    # File I/O
    FILE_IO = retry_with_backoff(
        max_retries=3,
        base_delay=0.5,
        max_delay=5,
        exceptions=(IOError, OSError)
    )

# Brukseksempel:
# from vev_retry_policy import VevRetryPolicies
# 
# @VevRetryPolicies.API_CALL
# def fetch_from_brave_api(query):
#     ...
```

---

## 6️⃣ NOTIFIKASJONSSYSTEM

### Nåværende Status

| Kanal | Implementert | Brukes aktivt |
|-------|--------------|---------------|
| Telegram | ✅ | Ja (bare auto-responder) |
| E-post | ✅ | Delvis (bare daily-podcast-email.py) |
| JSON-fil | ✅ | Ja (notification_service.py) |
| System logs | ✅ | Delvis |

### Identifiserte Mangler

| Mangel | Alvorlighet | Beskrivelse |
|--------|-------------|-------------|
| **Ingen feil-notifikasjoner** | 🔴 Høy | Cron-jobber sender ikke ved feil |
| **Ingen suksess-confirmations** | 🟡 Medium | Bruker vet ikke om backup var vellykket |
| **Ingen oppsummeringer** | 🟡 Medium | Ingen daglig/ukentlig rapport |
| **Manglende alvorlighetsgradering** | 🟡 Medium | Alle meldinger like viktige |

### Foreslått Notifikasjons-oppsett

**Cron-jobb med notifikasjon ved feil:**

```bash
#!/bin/bash
# Wrapper for cron-jobber med notifikasjon

SCRIPT_PATH="$1"
SCRIPT_NAME=$(basename "$SCRIPT_PATH")
LOG_FILE="/var/log/vev/cron-${SCRIPT_NAME}.log"
NOTIFY_SCRIPT="/root/.openclaw/workspace/scripts/notify.sh"

# Kjør script med timeout
timeout 300 "$SCRIPT_PATH" > "$LOG_FILE" 2>&1
EXIT_CODE=$?

# Håndter resultat
case $EXIT_CODE in
    0)
        # Suksess - logg stille
        logger -t "vev-cron" "✅ $SCRIPT_NAME fullført"
        ;;
    124)
        # Timeout
        "$NOTIFY_SCRIPT" "warning" "⏱️ $SCRIPT_NAME timeout etter 5 minutter"
        ;;
    *)
        # Feil
        ERROR_MSG=$(tail -5 "$LOG_FILE")
        "$NOTIFY_SCRIPT" "error" "❌ $SCRIPT_NAME feilet (kode $EXIT_CODE)\n\nSiste logg:\n$ERROR_MSG"
        ;;
esac

exit $EXIT_CODE
```

**Notifikasjons-script:**

```bash
#!/bin/bash
# notify.sh - Send notifikasjon til alle kanaler

LEVEL="$1"      # info, warning, error, critical
MESSAGE="$2"
SOURCE="${3:-system}"

WORKSPACE="/root/.openclaw/workspace"

# Logg til fil
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$LEVEL] $MESSAGE" >> "$WORKSPACE/brain/logs/notifications.log"

# Send til Telegram ved warning eller høyere
if [[ "$LEVEL" == "warning" ]] || [[ "$LEVEL" == "error" ]] || [[ "$LEVEL" == "critical" ]]; then
    source "$WORKSPACE/.credentials/telegram-bot.env"
    
    EMOJI="ℹ️"
    [[ "$LEVEL" == "warning" ]] && EMOJI="⚠️"
    [[ "$LEVEL" == "error" ]] && EMOJI="❌"
    [[ "$LEVEL" == "critical" ]] && EMOJI="🔴"
    
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d "chat_id=${TELEGRAM_CHAT_ID}" \
        -d "text=${EMOJI} *${SOURCE}*\n\n${MESSAGE}" \
        -d "parse_mode=Markdown" \
        > /dev/null 2>&1
fi

# Lagre til notification service
python3 << PYEOF
import sys
sys.path.insert(0, '$WORKSPACE/scripts')
from notification_service import NotificationService

service = NotificationService()
service.notify(
    title="$SOURCE: $LEVEL",
    message="""$MESSAGE""",
    level="$LEVEL",
    source="$SOURCE"
)
PYEOF
```

---

## 7️⃣ FEILHÅNDTERING

### Nåværende Status

```
❌ Ingen unified error handling
❌ Ingen circuit breaker mønster
❌ Ingen graceful degradation
❌ Ingen error aggregasjon
```

### Foreslått Error Handling Framework

**Fil:** `scripts/vev_error_handler.py`

```python
#!/usr/bin/env python3
"""
VEV Error Handler - Sentralisert feilhåndtering
"""

import sys
import traceback
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable
from functools import wraps
from notification_service import NotificationService

class VevErrorHandler:
    """Sentralisert feilhåndtering for Vev-systemet"""
    
    ERROR_LOG = Path('/var/log/vev/errors/errors.jsonl')
    
    def __init__(self):
        self.notifier = NotificationService()
        self.ERROR_LOG.parent.mkdir(parents=True, exist_ok=True)
    
    def log_error(self, error: Exception, context: dict = None):
        """Logg feil med kontekst"""
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': type(error).__name__,
            'message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {}
        }
        
        # Append til JSONL
        with open(self.ERROR_LOG, 'a') as f:
            f.write(json.dumps(error_entry) + '\n')
        
        # Send notifikasjon ved kritiske feil
        if context and context.get('critical'):
            self.notifier.notify(
                title=f"🔴 KRITISK FEIL: {type(error).__name__}",
                message=str(error),
                level='critical',
                source=context.get('component', 'unknown')
            )
    
    def handle(self, func: Callable) -> Callable:
        """Dekorator for automatisk feilhåndtering"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                context = {
                    'function': func.__name__,
                    'module': func.__module__,
                    'args': str(args),
                    'kwargs': str(kwargs)
                }
                self.log_error(e, context)
                raise
        return wrapper
    
    def get_recent_errors(self, hours: int = 24) -> list:
        """Hent feil fra siste N timer"""
        errors = []
        cutoff = datetime.now() - __import__('datetime').timedelta(hours=hours)
        
        if not self.ERROR_LOG.exists():
            return errors
        
        with open(self.ERROR_LOG) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    entry_time = datetime.fromisoformat(entry['timestamp'])
                    if entry_time > cutoff:
                        errors.append(entry)
                except:
                    continue
        
        return errors

# Global instance
error_handler = VevErrorHandler()

# Convenience decorator
def handle_errors(context: dict = None):
    """Dekorator for enkel feilhåndtering"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                ctx = context or {}
                ctx['function'] = func.__name__
                error_handler.log_error(e, ctx)
                raise
        return wrapper
    return decorator
```

---

## 8️⃣ ANBEFALTE TILTAK (PRIORITERT)

### 🔴 HØY PRIORITET (Gjøres umiddelbart)

1. **Implementer låsmekanisme i cron-jobber**
   ```bash
   # Legg til i alle cron-script
   LOCKFILE="/var/lock/vev-$(basename $0).lock"
   exec 200>"$LOCKFILE"
   flock -n 200 || { echo "Script kjører allerede"; exit 1; }
   ```

2. **Slett identifiserte duplikat-scripts** (16 stk)
   Se "ANBEFALT SLETTLISTE" over

3. **Implementer retry-wrapper på alle API-kall**
   - Morning routine: Brave API + OpenAI API
   - Dashboard: Nielsen API + Podtoppen
   - Telegram: Send message API

4. **Sett opp logg-rotasjon**
   ```bash
   # /etc/logrotate.d/vev
   /var/log/vev/*.log {
       daily
       rotate 30
       compress
       delaycompress
       missingok
       notifempty
       create 0644 root root
   }
   ```

### 🟡 MEDIUM PRIORITET (Gjøres innen 1 uke)

5. **Konsolider morning routine scripts** til én master-fil
6. **Konsolider dashboard updater scripts** til én master-fil
7. **Implementer unified notification wrapper** for alle cron-jobber
8. **Opprett sentralisert logg-mappe** `/var/log/vev/`

### 🟢 LAV PRIORITET (Gjøres ved anledning)

9. **Implementer VevLogger klasse** i alle Python-scripts
10. **Sett opp strukturert logging** (JSONL format)
11. **Implementer Error Handler framework**
12. **Opprett daglig status-rapport** som sendes på Telegram

---

## 9️⃣ KONKLUSJON

Systemet har **263 scripts** med betydelig redundans og manglende standardisering. De største problemene er:

1. **10+ varianter** av morning routine (kun 1 er nødvendig)
2. **8+ varianter** av dashboard updater (kun 1-2 er nødvendig)
3. **Ingen låsmekanismer** - risiko for overlappende kjøringer
4. **Ingen retry-logikk** - API-feil fører til tapte data
5. **Mangelfull logging** - vanskelig å debugge
6. **Ingen feil-notifikasjoner** - bruker får ikke vite om problemer

**Estimert tidsbesparelse etter konsolidering:** 40-50% færre scripts å vedlikeholde.

**Anbefalt neste steg:** Start med å implementere låsmekanismer og slette identifiserte duplikater.

---

*Rapport generert: 2026-03-11 01:55:00*  
*Versjon: 1.0*
