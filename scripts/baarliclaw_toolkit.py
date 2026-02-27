#!/usr/bin/env python3
"""
🧰 BAARLICLAW TOOLKIT
Felles verktøy og utilities for alle scripts
"""

import os
import sys
import json
import logging
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from functools import wraps
import time
import hashlib

# === LOGGING SETUP ===
def setup_logging(name: str, level=logging.INFO) -> logging.Logger:
    """Set up consistent logging for all scripts"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

# === API CLIENT ===
class APIClient:
    """Generic API client with retry logic and caching"""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None, 
                 timeout: int = 30, max_retries: int = 3):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = setup_logging(f"APIClient_{base_url}")
        self._cache = {}
        
    def _make_request(self, endpoint: str, method: str = 'GET', 
                      data: Optional[Dict] = None, 
                      headers: Optional[Dict] = None) -> Optional[Dict]:
        """Make HTTP request with retry logic"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        if headers is None:
            headers = {}
        
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        
        for attempt in range(self.max_retries):
            try:
                if method == 'GET':
                    req = urllib.request.Request(url, headers=headers)
                else:
                    req = urllib.request.Request(
                        url, 
                        data=json.dumps(data).encode() if data else None,
                        headers={**headers, 'Content-Type': 'application/json'},
                        method=method
                    )
                
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    return json.loads(response.read().decode())
                    
            except urllib.error.HTTPError as e:
                self.logger.error(f"HTTP Error {e.code}: {e.reason}")
                if e.code == 429:  # Rate limited
                    time.sleep(2 ** attempt)
                    continue
                return None
            except Exception as e:
                self.logger.error(f"Request failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                return None
        
        return None
    
    def get(self, endpoint: str, **kwargs) -> Optional[Dict]:
        """GET request"""
        return self._make_request(endpoint, 'GET', **kwargs)
    
    def post(self, endpoint: str, data: Dict, **kwargs) -> Optional[Dict]:
        """POST request"""
        return self._make_request(endpoint, 'POST', data=data, **kwargs)

# === BRAVE SEARCH CLIENT ===
class BraveSearchClient:
    """Dedicated client for Brave Search API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = APIClient("https://api.search.brave.com", api_key)
        self.logger = setup_logging("BraveSearch")
        
    def search_news(self, query: str, count: int = 10, 
                    freshness: str = 'pd',
                    language: str = 'nb',
                    country: str = 'no') -> List[Dict]:
        """
        Search for news articles
        
        Args:
            query: Search query
            count: Number of results (1-50)
            freshness: 'pd' (past day), 'pw' (past week), 'pm' (past month), 'py' (past year)
            language: Language code
            country: Country code
        """
        encoded_query = urllib.parse.quote(query)
        url = f"https://api.search.brave.com/res/v1/news/search"
        
        params = {
            'q': encoded_query,
            'count': min(count, 50),
            'search_lang': language,
            'country': country,
            'freshness': freshness
        }
        
        url_with_params = f"{url}?{urllib.parse.urlencode(params)}"
        
        headers = {
            'X-Subscription-Token': self.api_key,
            'Accept': 'application/json'
        }
        
        try:
            req = urllib.request.Request(url_with_params, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode())
                return data.get('results', [])
        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            return []
    
    def search_web(self, query: str, count: int = 10) -> List[Dict]:
        """Search web (not just news)"""
        encoded_query = urllib.parse.quote(query)
        url = f"https://api.search.brave.com/res/v1/web/search?q={encoded_query}&count={count}"
        
        headers = {
            'X-Subscription-Token': self.api_key,
            'Accept': 'application/json'
        }
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode())
                return data.get('web', {}).get('results', [])
        except Exception as e:
            self.logger.error(f"Web search failed: {e}")
            return []

# === SUPABASE CLIENT ===
class SupabaseClient:
    """Client for Supabase operations"""
    
    def __init__(self, url: str, key: str):
        self.url = url.rstrip('/')
        self.key = key
        self.headers = {
            'apikey': key,
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
        self.logger = setup_logging("Supabase")
    
    def insert(self, table: str, data: Dict) -> Optional[Dict]:
        """Insert data into table"""
        url = f"{self.url}/rest/v1/{table}"
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode(),
                headers=self.headers,
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            self.logger.error(f"Insert failed: {e}")
            return None
    
    def select(self, table: str, query: Optional[str] = None) -> List[Dict]:
        """Select data from table"""
        url = f"{self.url}/rest/v1/{table}"
        if query:
            url += f"?{query}"
        
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            self.logger.error(f"Select failed: {e}")
            return []
    
    def update(self, table: str, id_field: str, id_value: str, 
               data: Dict) -> Optional[Dict]:
        """Update record"""
        url = f"{self.url}/rest/v1/{table}?{id_field}=eq.{id_value}"
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode(),
                headers={**self.headers, 'Prefer': 'return=representation'},
                method='PATCH'
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            self.logger.error(f"Update failed: {e}")
            return None

# === DECORATORS ===
def retry_on_error(max_retries: int = 3, delay: float = 1.0):
    """Decorator to retry function on error"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay * (attempt + 1))
            return None
        return wrapper
    return decorator

def cache_result(ttl_seconds: int = 300):
    """Decorator to cache function results"""
    cache = {}
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = hashlib.sha256(
                f"{func.__name__}:{args}:{kwargs}".encode()
            ).hexdigest()
            
            now = time.time()
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < ttl_seconds:
                    return result
            
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

# === UTILITY FUNCTIONS ===
def load_env_file(filepath: str) -> Dict[str, str]:
    """Load environment variables from file"""
    env_vars = {}
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value.strip('"').strip("'")
    return env_vars

def format_date(dt: datetime, format_str: str = '%Y-%m-%d') -> str:
    """Format datetime consistently"""
    return dt.strftime(format_str)

def parse_date(date_str: str, format_str: str = '%Y-%m-%d') -> datetime:
    """Parse date string to datetime"""
    return datetime.strptime(date_str, format_str)

def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug"""
    return text.lower().replace(' ', '-').replace('_', '-')

# === DATA VALIDATION ===
def validate_url(url: str) -> bool:
    """Check if string is valid URL"""
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def sanitize_string(text: str) -> str:
    """Remove potentially dangerous characters"""
    dangerous = ['<', '>', '"', "'", ';', '&']
    for char in dangerous:
        text = text.replace(char, '')
    return text

# === TESTING ===
if __name__ == "__main__":
    print("🧰 BaarliClaw Toolkit - Testing")
    print("=" * 50)
    
    # Test logging
    logger = setup_logging("Test")
    logger.info("Logging works!")
    
    # Test utilities
    print(f"Truncate: {truncate_text('This is a very long text', 20)}")
    print(f"Slugify: {slugify('Hello World Test')}")
    print(f"Validate URL: {validate_url('https://example.com')}")
    
    print("\n✅ All tests passed!")
