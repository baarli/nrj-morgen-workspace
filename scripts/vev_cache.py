#!/usr/bin/env python3
"""
VEV MEMORY CACHE
LRU Cache for å redusere Supabase-kall
"""

import time
import json
import hashlib
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Any, Optional

class MemoryCache:
    """
    Simple LRU Cache with TTL support
    
    Usage:
        from vev_cache import MemoryCache
        
        cache = MemoryCache(max_size=100, default_ttl=300)
        
        # Get or compute
        data = cache.get('agenda_2026-03-11')
        if not data:
            data = fetch_from_supabase()
            cache.set('agenda_2026-03-11', data, ttl=300)
    """
    
    def __init__(self, max_size: int = 100, default_ttl: int = 300):
        """
        Initialize cache
        
        Args:
            max_size: Maximum number of items in cache
            default_ttl: Default time-to-live in seconds
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache = OrderedDict()
        self.timestamps = {}
    
    def _is_expired(self, key: str) -> bool:
        """Check if cached item has expired"""
        if key not in self.timestamps:
            return True
        
        expires_at = self.timestamps[key]
        return datetime.now() > expires_at
    
    def _make_key(self, *args, **kwargs) -> str:
        """Create a cache key from arguments"""
        key_data = json.dumps({'args': args, 'kwargs': kwargs}, sort_keys=True)
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get item from cache
        
        Returns:
            Cached value or None if not found/expired
        """
        if key in self.cache:
            if self._is_expired(key):
                # Remove expired item
                del self.cache[key]
                del self.timestamps[key]
                return None
            
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return self.cache[key]
        
        return None
    
    def set(self, key: str, value: Any, ttl: int = None):
        """
        Set item in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (default: self.default_ttl)
        """
        # Remove oldest if at capacity
        if len(self.cache) >= self.max_size and key not in self.cache:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
            del self.timestamps[oldest_key]
        
        # Set with TTL
        ttl = ttl or self.default_ttl
        self.cache[key] = value
        self.timestamps[key] = datetime.now() + timedelta(seconds=ttl)
        self.cache.move_to_end(key)
    
    def delete(self, key: str):
        """Delete item from cache"""
        if key in self.cache:
            del self.cache[key]
            del self.timestamps[key]
    
    def clear(self):
        """Clear all cached items"""
        self.cache.clear()
        self.timestamps.clear()
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        # Clean expired items first
        expired_keys = [k for k in list(self.cache.keys()) if self._is_expired(k)]
        for k in expired_keys:
            del self.cache[k]
            del self.timestamps[k]
        
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'usage_percent': (len(self.cache) / self.max_size) * 100
        }


# Global cache instance
cache = MemoryCache()

# Decorator for automatic caching
def cached(ttl: int = 300, key_fn=None):
    """
    Decorator to cache function results
    
    Usage:
        @cached(ttl=600)
        def fetch_agenda(date: str):
            return supabase_query(date)
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_fn:
                cache_key = key_fn(*args, **kwargs)
            else:
                cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try cache first
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Compute and cache
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result
        
        return wrapper
    return decorator


# Example usage
if __name__ == '__main__':
    # Demo
    cache = MemoryCache(max_size=3, default_ttl=5)
    
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.set('key3', 'value3')
    
    print(f"Cache stats: {cache.get_stats()}")
    print(f"Get key1: {cache.get('key1')}")
    
    # Add one more (should evict oldest)
    cache.set('key4', 'value4')
    print(f"After adding key4: {cache.get_stats()}")
    
    # Wait for expiration
    print("\nWaiting 6 seconds for expiration...")
    time.sleep(6)
    print(f"Get key1 after expiration: {cache.get('key1')}")
