#!/usr/bin/env python3
"""
💾 BAARLICLAW CACHE TOOLKIT
Caching og lagring av data
"""

import os
import sys
import json
import hashlib
import time
from typing import Any, Optional, Dict, Callable
from functools import wraps
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("CacheToolkit")

@dataclass
class CacheEntry:
    """Cache entry"""
    key: str
    value: Any
    created_at: float
    expires_at: Optional[float]
    hits: int = 0
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'key': self.key,
            'value': self.value,
            'created_at': self.created_at,
            'expires_at': self.expires_at,
            'hits': self.hits
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'CacheEntry':
        """Create CacheEntry from dictionary"""
        return CacheEntry(
            key=data['key'],
            value=data['value'],
            created_at=data['created_at'],
            expires_at=data.get('expires_at'),
            hits=data.get('hits', 0)
        )

class MemoryCache:
    """In-memory cache"""
    
    def __init__(self, default_ttl: Optional[int] = None):
        self._cache: Dict[str, CacheEntry] = {}
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        entry = self._cache.get(key)
        
        if entry is None:
            return None
        
        # Check expiration
        if entry.expires_at and time.time() > entry.expires_at:
            del self._cache[key]
            return None
        
        entry.hits += 1
        return entry.value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache"""
        ttl = ttl or self.default_ttl
        
        expires_at = None
        if ttl:
            expires_at = time.time() + ttl
        
        self._cache[key] = CacheEntry(
            key=key,
            value=value,
            created_at=time.time(),
            expires_at=expires_at
        )
    
    def delete(self, key: str) -> bool:
        """Delete from cache"""
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    def clear(self):
        """Clear all cache"""
        self._cache.clear()
    
    def keys(self) -> list:
        """Get all keys"""
        return list(self._cache.keys())
    
    def stats(self) -> Dict:
        """Get cache statistics"""
        total = len(self._cache)
        hits = sum(e.hits for e in self._cache.values())
        
        return {
            'entries': total,
            'total_hits': hits,
            'avg_hits': hits / total if total > 0 else 0
        }

class FileCache:
    """File-based cache"""
    
    def __init__(self, cache_dir: str = "/tmp/baarliclaw_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_path(self, key: str) -> str:
        """Get file path for key"""
        # Hash the key for safe filename
        hashed = hashlib.sha256(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{hashed}.cache")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from file cache"""
        path = self._get_path(key)
        
        if not os.path.exists(path):
            return None
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                entry = json.load(f)
            
            # Check expiration
            if entry.get('expires_at') and time.time() > entry['expires_at']:
                os.remove(path)
                return None
            
            return entry['value']
            
        except Exception as e:
            logger.error(f"Cache read error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in file cache"""
        path = self._get_path(key)
        
        expires_at = None
        if ttl:
            expires_at = time.time() + ttl
        
        entry = {
            'key': key,
            'value': value,
            'created_at': time.time(),
            'expires_at': expires_at
        }
        
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(entry, f, default=str)
        except Exception as e:
            logger.error(f"Cache write error: {e}")
    
    def delete(self, key: str) -> bool:
        """Delete from file cache"""
        path = self._get_path(key)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False
    
    def clear(self):
        """Clear file cache"""
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.cache'):
                os.remove(os.path.join(self.cache_dir, filename))

class CacheDecorator:
    """Cache decorator utilities"""
    
    @staticmethod
    def memoize(ttl: Optional[int] = None):
        """Memoize function results"""
        cache = MemoryCache(default_ttl=ttl)
        
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Create cache key
                key_parts = [func.__name__]
                key_parts.extend(str(a) for a in args)
                key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
                key = hashlib.sha256('|'.join(key_parts).encode()).hexdigest()
                
                # Check cache
                result = cache.get(key)
                if result is not None:
                    return result
                
                # Compute and cache
                result = func(*args, **kwargs)
                cache.set(key, result, ttl)
                return result
            
            wrapper.cache = cache
            return wrapper
        return decorator
    
    @staticmethod
    def cache_to_file(cache_dir: str = "/tmp/cache", ttl: Optional[int] = None):
        """Cache function results to file"""
        cache = FileCache(cache_dir)
        
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                key_parts = [func.__name__]
                key_parts.extend(str(a) for a in args)
                key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
                key = hashlib.sha256('|'.join(key_parts).encode()).hexdigest()
                
                result = cache.get(key)
                if result is not None:
                    return result
                
                result = func(*args, **kwargs)
                cache.set(key, result, ttl)
                return result
            
            wrapper.cache = cache
            return wrapper
        return decorator

# === CONVENIENCE FUNCTIONS ===
def quick_cache(key: str, value: Any, ttl: int = 3600) -> bool:
    """Quick cache set"""
    cache = MemoryCache()
    cache.set(key, value, ttl)
    return True

def quick_get(key: str) -> Optional[Any]:
    """Quick cache get"""
    cache = MemoryCache()
    return cache.get(key)

@CacheDecorator.memoize(ttl=300)
def expensive_function(n: int) -> int:
    """Example of memoized function"""
    time.sleep(1)  # Simulate expensive operation
    return n * n

# === TESTING ===
if __name__ == "__main__":
    print("💾 BaarliClaw Cache Toolkit - Testing")
    print("=" * 50)
    
    # Test memory cache
    print("\n🧪 Testing Memory Cache")
    cache = MemoryCache()
    
    cache.set("key1", "value1")
    cache.set("key2", {"data": "test"}, ttl=60)
    
    print(f"✅ key1: {cache.get('key1')}")
    print(f"✅ key2: {cache.get('key2')}")
    print(f"✅ key3 (missing): {cache.get('key3')}")
    
    stats = cache.stats()
    print(f"✅ Cache stats: {stats}")
    
    # Test file cache
    print("\n🧪 Testing File Cache")
    file_cache = FileCache("/tmp/test_cache")
    
    file_cache.set("file_key", [1, 2, 3], ttl=300)
    result = file_cache.get("file_key")
    print(f"✅ File cache: {result}")
    
    # Test memoize decorator
    print("\n🧪 Testing Memoize Decorator")
    
    @CacheDecorator.memoize(ttl=10)
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    import time
    start = time.time()
    result = fibonacci(30)
    duration = time.time() - start
    print(f"✅ First call: fib(30) = {result} ({duration:.3f}s)")
    
    start = time.time()
    result = fibonacci(30)
    duration = time.time() - start
    print(f"✅ Second call (cached): fib(30) = {result} ({duration:.6f}s)")
    
    # Cleanup
    file_cache.clear()
    
    print("\n✅ Cache Toolkit ready!")
