#!/usr/bin/env python3
"""
🧰 BAARLICLAW BASE SCRIPT TEMPLATE
==================================
Standardisert baseklasse for alle Vev scripts.

Tilbyr:
- ✅ Konsistent logging (fil + stdout)
- ✅ Sikker credential-håndtering
- ✅ Retry-logikk med exponential backoff
- ✅ Standardisert error handling
- ✅ Execution summary

Bruk:
    from base_script import BaseScript, retry_with_backoff, APIError
    
    class MyScript(BaseScript):
        def run(self) -> int:
            # Din kode her
            return 0
    
    if __name__ == '__main__':
        sys.exit(MyScript().run())
"""

import os
import sys
import json
import logging
import traceback
import time
import random
from pathlib import Path
from datetime import datetime
from functools import wraps
from typing import Optional, Dict, Any, Callable, Union, List

# === KONFIGURASJON ===
WORKSPACE = Path("/root/.openclaw/workspace")
LOG_DIR = WORKSPACE / "brain" / "logs"
CREDENTIALS_DIR = WORKSPACE / ".credentials"

# Sikre at logg-mappen finnes
LOG_DIR.mkdir(parents=True, exist_ok=True)

# === LOGGING SETUP ===
def setup_logging(name: str, log_to_file: bool = True, level: int = logging.DEBUG) -> logging.Logger:
    """
    Set up consistent logging for all scripts.
    
    Args:
        name: Logger name (typisk script-navn)
        log_to_file: Om det skal logges til fil
        level: Log level (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Konfigurert logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Fjern eksisterende handlers for å unngå duplikater
    logger.handlers = []
    
    # Console handler - INFO og høyere
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )
    console.setFormatter(console_format)
    logger.addHandler(console)
    
    # File handler - DEBUG og høyere (mer detaljert)
    if log_to_file:
        timestamp = datetime.now().strftime('%Y%m%d')
        log_file = LOG_DIR / f"{name}_{timestamp}.log"
        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
        
        logger.debug(f"Logging initialized. Log file: {log_file}")
    
    return logger

# === CREDENTIAL MANAGEMENT ===
class CredentialManager:
    """
    Sikker credential management.
    
    Henter credentials fra:
    1. Environment variables
    2. Credential files i .credentials/
    3. Cache (for å unngå gjentatt fillesing)
    """
    
    def __init__(self):
        self._cache: Dict[str, str] = {}
        self.logger = setup_logging("CredentialManager", log_to_file=False)
    
    def load_env_file(self, filepath: Union[str, Path]) -> Dict[str, str]:
        """
        Last environment variables fra fil.
        
        Støtter format:
            KEY=value
            KEY="value"
            KEY='value'  # inline comment
        """
        env_vars = {}
        path = Path(filepath)
        
        if not path.exists():
            self.logger.warning(f"Credential file not found: {filepath}")
            return env_vars
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Skip tomme linjer og kommentarer
                    if not line or line.startswith('#'):
                        continue
                    
                    if '=' not in line:
                        continue
                    
                    try:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        
                        # Fjern inline kommentarer
                        value = value.split('#')[0].strip()
                        
                        # Fjern quotes
                        value = value.strip('"').strip("'")
                        
                        env_vars[key] = value
                    except ValueError as e:
                        self.logger.warning(f"Could not parse line {line_num} in {filepath}: {e}")
                        continue
                        
        except Exception as e:
            self.logger.error(f"Failed to load credentials from {filepath}: {e}")
            raise
        
        return env_vars
    
    def get_credential(self, name: str, env_file: Optional[str] = None) -> str:
        """
        Hent credential fra miljø eller fil.
        
        Args:
            name: Navn på credential (f.eks. "SUPABASE_URL")
            env_file: Spesifikk credential-fil å lese fra
        
        Returns:
            Credential verdi
        
        Raises:
            ValueError: Hvis credential ikke finnes
        """
        # Check cache først
        if name in self._cache:
            return self._cache[name]
        
        # Sjekk environment
        value = os.environ.get(name)
        if value:
            self._cache[name] = value
            self.logger.debug(f"Loaded {name} from environment")
            return value
        
        # Last fra spesifikk fil
        if env_file:
            filepath = CREDENTIALS_DIR / env_file
            if filepath.exists():
                creds = self.load_env_file(filepath)
                value = creds.get(name)
                if value:
                    self._cache[name] = value
                    self.logger.debug(f"Loaded {name} from {env_file}")
                    return value
        
        # Prøv vanlige credential filer
        common_files = [
            "nrj-morgen.env",
            "live-search.env", 
            "telegram-bot.env",
            "elevenlabs.env"
        ]
        
        for cred_file in common_files:
            filepath = CREDENTIALS_DIR / cred_file
            if filepath.exists():
                creds = self.load_env_file(filepath)
                value = creds.get(name)
                if value:
                    self._cache[name] = value
                    self.logger.debug(f"Loaded {name} from {cred_file}")
                    return value
        
        raise ValueError(f"Credential not found: {name}")
    
    def get_optional_credential(self, name: str, default: Optional[str] = None, env_file: Optional[str] = None) -> Optional[str]:
        """Hent credential, returner default hvis ikke funnet."""
        try:
            return self.get_credential(name, env_file)
        except ValueError:
            return default
    
    def clear_cache(self):
        """Tøm credential cache."""
        self._cache.clear()
        self.logger.debug("Credential cache cleared")

# === RETRY DECORATOR ===
def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: tuple = (Exception,),
    on_retry: Optional[Callable[[int, Exception, float], None]] = None,
    retry_on_result: Optional[Callable[[Any], bool]] = None
):
    """
    Dekorator for retry med exponential backoff og jitter.
    
    Args:
        max_retries: Maksimalt antall forsøk
        base_delay: Start delay i sekunder
        max_delay: Maksimalt delay
        exceptions: Tuple med exceptions som skal trigge retry
        on_retry: Callback funksjon ved retry (attempt, exception, delay)
        retry_on_result: Callback som sjekker om resultat krever retry
    
    Example:
        @retry_with_backoff(max_retries=3, base_delay=2.0)
        def api_call():
            return requests.get(url)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger = logging.getLogger(func.__module__)
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    result = func(*args, **kwargs)
                    
                    # Sjekk om resultat krever retry
                    if retry_on_result and retry_on_result(result):
                        if attempt == max_retries:
                            logger.warning(f"Max retries reached, result check failed")
                            return result
                        
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        jitter = random.uniform(0, delay * 0.1)
                        total_delay = delay + jitter
                        
                        logger.warning(f"Retrying after {total_delay:.1f}s due to result check")
                        time.sleep(total_delay)
                        continue
                    
                    return result
                    
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        logger.error(f"All {max_retries} retries failed for {func.__name__}: {e}")
                        raise last_exception
                    
                    # Exponential backoff med jitter
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
            
            raise last_exception  # Skal aldri nå hit
        
        # Legg til metadata for testing
        wrapper._retry_config = {
            'max_retries': max_retries,
            'base_delay': base_delay,
            'max_delay': max_delay
        }
        
        return wrapper
    return decorator

# Network-specific retry decorator
retry_on_network_error = lambda max_retries=3, base_delay=2.0: retry_with_backoff(
    max_retries=max_retries,
    base_delay=base_delay,
    exceptions=(
        ConnectionError,
        TimeoutError,
        OSError,
        Exception  # requests.RequestException ikke all tilgjengelig
    )
)

# === CUSTOM EXCEPTIONS ===
class ScriptError(Exception):
    """Base exception for alle script-feil."""
    pass

class APIError(ScriptError):
    """API-relaterte feil."""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[str] = None, endpoint: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response
        self.endpoint = endpoint
    
    def __str__(self) -> str:
        parts = [self.message]
        if self.status_code:
            parts.append(f"(HTTP {self.status_code})")
        if self.endpoint:
            parts.append(f"at {self.endpoint}")
        return " ".join(parts)

class CredentialError(ScriptError):
    """Credential-relaterte feil."""
    pass

class ValidationError(ScriptError):
    """Valideringsfeil."""
    pass

# === ERROR HANDLING ===
def handle_error(
    logger: logging.Logger, 
    error: Exception, 
    context: Optional[Dict[str, Any]] = None,
    reraise: bool = False
) -> Dict[str, Any]:
    """
    Sentralisert error handling.
    
    Args:
        logger: Logger å bruke
        error: Exception som ble fanget
        context: Ekstra kontekst (f.eks. {'function': 'my_func', 'user_id': 123})
        reraise: Om exception skal kastes på nytt
    
    Returns:
        Dict med error informasjon
    """
    error_info = {
        "timestamp": datetime.now().isoformat(),
        "type": type(error).__name__,
        "message": str(error),
        "traceback": traceback.format_exc(),
        "context": context or {}
    }
    
    # Logg feil
    func_name = context.get('function', 'unknown') if context else 'unknown'
    logger.error(f"Error in {func_name}: {error}")
    logger.debug(f"Full traceback:\n{error_info['traceback']}")
    
    # Ekstra logging for spesifikke error typer
    if isinstance(error, APIError):
        logger.error(f"API Error details - Status: {error.status_code}, Endpoint: {error.endpoint}")
    
    if reraise:
        raise
    
    return error_info

def safe_execute(
    func: Callable, 
    *args, 
    default: Any = None, 
    logger: Optional[logging.Logger] = None,
    **kwargs
) -> Any:
    """
    Trygg funksjonseksekvering med fallback.
    
    Args:
        func: Funksjon å kalle
        args: Positional arguments
        default: Verdi å returnere ved feil
        logger: Optional logger
        kwargs: Keyword arguments
    
    Returns:
        Funksjonens resultat eller default ved feil
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if logger:
            logger.warning(f"safe_execute failed for {func.__name__}: {e}")
        return default

# === BASE SCRIPT CLASS ===
class BaseScript:
    """
    Base class for alle Vev scripts.
    
    Example:
        class MyScript(BaseScript):
            def __init__(self):
                super().__init__("my-script")
                self.api_key = self.get_credential("API_KEY")
            
            def run(self) -> int:
                try:
                    result = self.do_work()
                    self.log_summary(success=True, details={"result": result})
                    return 0
                except Exception as e:
                    handle_error(self.logger, e, {'function': 'run'})
                    self.log_summary(success=False)
                    return 1
    """
    
    def __init__(self, name: str, log_to_file: bool = True):
        """
        Initialize base script.
        
        Args:
            name: Script navn (brukes i logging)
            log_to_file: Om det skal logges til fil
        """
        self.name = name
        self.logger = setup_logging(name, log_to_file=log_to_file)
        self.credentials = CredentialManager()
        self.start_time = datetime.now()
        self._error_count = 0
        
        self.logger.info(f"=== {name} started ===")
    
    def run(self) -> int:
        """
        Hoved entry point - MÅ overrides i subklasser.
        
        Returns:
            Exit code (0 for suksess, 1+ for feil)
        """
        raise NotImplementedError("Subclasses must implement run()")
    
    def get_credential(self, name: str, env_file: Optional[str] = None) -> str:
        """
        Hent credential sikkert.
        
        Args:
            name: Credential navn
            env_file: Spesifikk credential-fil
        
        Returns:
            Credential verdi
        
        Raises:
            CredentialError: Hvis credential ikke finnes
        """
        try:
            return self.credentials.get_credential(name, env_file)
        except ValueError as e:
            self.logger.error(f"Missing required credential: {name}")
            raise CredentialError(f"Missing credential: {name}") from e
    
    def get_optional_credential(self, name: str, default: Optional[str] = None) -> Optional[str]:
        """Hent optional credential."""
        return self.credentials.get_optional_credential(name, default)
    
    def log_summary(self, success: bool, details: Optional[Dict[str, Any]] = None):
        """
        Logg execution summary.
        
        Args:
            success: Om scriptet var vellykket
            details: Ekstra detaljer å logge
        """
        duration = (datetime.now() - self.start_time).total_seconds()
        status = "✅ SUCCESS" if success else "❌ FAILED"
        
        self.logger.info(f"=== {self.name} {status} ===")
        self.logger.info(f"Duration: {duration:.2f}s")
        self.logger.info(f"Errors: {self._error_count}")
        
        if details:
            for key, value in details.items():
                self.logger.info(f"  {key}: {value}")
    
    def record_error(self):
        """Registrer en feil (brukt for summary)."""
        self._error_count += 1
    
    def validate_required_credentials(self, *names: str) -> bool:
        """
        Valider at påkrevde credentials finnes.
        
        Args:
            names: Liste med credential navn
        
        Returns:
            True hvis alle finnes
        
        Raises:
            CredentialError: Hvis noen mangler
        """
        missing = []
        
        for name in names:
            try:
                self.credentials.get_credential(name)
            except ValueError:
                missing.append(name)
        
        if missing:
            raise CredentialError(f"Missing required credentials: {', '.join(missing)}")
        
        return True

# === UTILITY FUNCTIONS ===
def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """Trunker tekst til maks lengde."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def format_duration(seconds: float) -> str:
    """Formatér varighet på lesbar måte."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"

def chunk_list(items: List, chunk_size: int) -> List[List]:
    """Del liste opp i chunks."""
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

# === TESTING ===
if __name__ == "__main__":
    print("🧰 BaarliClaw Base Script Template")
    print("=" * 50)
    
    # Test logging
    logger = setup_logging("test", log_to_file=True)
    logger.info("Testing logging")
    logger.debug("Debug message")
    logger.warning("Warning message")
    
    # Test credentials
    cm = CredentialManager()
    
    # Test retry
    @retry_with_backoff(max_retries=2, base_delay=0.1)
    def flaky_function(fail_count: int):
        flaky_function.calls = getattr(flaky_function, 'calls', 0) + 1
        if flaky_function.calls < fail_count:
            raise ValueError(f"Not yet ({flaky_function.calls})")
        return f"Success after {flaky_function.calls} attempts"
    
    result = flaky_function(3)
    print(f"\nRetry test: {result}")
    
    # Test base script
    class TestScript(BaseScript):
        def run(self) -> int:
            self.logger.info("Running test script")
            self.log_summary(success=True, details={"test": "passed"})
            return 0
    
    test = TestScript("test-script")
    exit_code = test.run()
    print(f"\nTest script exit code: {exit_code}")
    
    print("\n✅ Base script template loaded successfully!")
    print(f"   Log directory: {LOG_DIR}")
    print(f"   Credentials directory: {CREDENTIALS_DIR}")
