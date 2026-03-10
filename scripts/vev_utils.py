#!/usr/bin/env python3
"""
VEV UTILITIES
Utility functions: debounce, throttle, rate limiting
"""

import time
import functools
from typing import Callable, Any

def debounce(wait: float):
    """
    Debounce decorator
    
    Venter med å kjøre funksjonen til det har gått `wait` 
    sekunder uten nye kall.
    
    Usage:
        @debounce(0.3)
        def filter_saker(query):
            # This will only run 300ms after last call
            render_results(query)
    """
    def decorator(func: Callable) -> Callable:
        timer = None
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal timer
            
            # Cancel existing timer
            if timer is not None:
                timer.cancel()
            
            # Schedule new execution
            def delayed():
                func(*args, **kwargs)
            
            import threading
            timer = threading.Timer(wait, delayed)
            timer.start()
        
        return wrapper
    return decorator


def throttle(wait: float):
    """
    Throttle decorator
    
    Begrenser funksjonen til å kjøre maksimalt én gang 
    per `wait` sekunder.
    
    Usage:
        @throttle(1.0)
        def update_stats():
            # This will run at most once per second
            fetch_stats()
    """
    def decorator(func: Callable) -> Callable:
        last_called = 0
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_called
            
            now = time.time()
            if now - last_called >= wait:
                last_called = now
                return func(*args, **kwargs)
        
        return wrapper
    return decorator


def rate_limit(calls: int, period: float):
    """
    Rate limit decorator
    
    Begrenser til `calls` antall kall per `period` sekunder.
    
    Usage:
        @rate_limit(calls=10, period=60)  # 10 calls per minute
        def api_call():
            return fetch_data()
    """
    def decorator(func: Callable) -> Callable:
        timestamps = []
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            
            # Remove timestamps outside the window
            timestamps[:] = [t for t in timestamps if now - t < period]
            
            # Check if we can make the call
            if len(timestamps) < calls:
                timestamps.append(now)
                return func(*args, **kwargs)
            else:
                wait_time = timestamps[0] + period - now
                raise Exception(f"Rate limit exceeded. Try again in {wait_time:.1f}s")
        
        return wrapper
    return decorator


def memoize(ttl: float = None):
    """
    Memoization decorator with optional TTL
    
    Cacher resultatet av funksjonen.
    
    Usage:
        @memoize(ttl=300)  # Cache for 5 minutes
        def expensive_calculation(x, y):
            return x ** y
    """
    def decorator(func: Callable) -> Callable:
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(sorted(kwargs.items()))
            now = time.time()
            
            # Check cache
            if key in cache:
                result, timestamp = cache[key]
                if ttl is None or now - timestamp < ttl:
                    return result
            
            # Compute and cache
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        
        return wrapper
    return decorator


# Example usage
if __name__ == '__main__':
    import threading
    
    # Test debounce
    @debounce(0.5)
    def search(query):
        print(f"Searching for: {query}")
    
    print("Testing debounce...")
    search("a")
    search("ab")
    search("abc")  # Only this should execute after 0.5s
    
    time.sleep(0.6)
    
    # Test memoize
    @memoize(ttl=2)
    def slow_function(x):
        time.sleep(1)
        return x * 2
    
    print("\nTesting memoize...")
    print(slow_function(5))  # Takes 1s
    print(slow_function(5))  # Instant (from cache)
