#!/usr/bin/env python3
"""
🎀 BAARLICLAW DECORATOR TOOLKIT
Nyttige dekoratorer
"""

import time
import functools
from typing import Callable, Any
import logging

class Decorators:
    """Collection of useful decorators"""
    
    @staticmethod
    def timer(func: Callable) -> Callable:
        """Time function execution"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            print(f"⏱️  {func.__name__} took {elapsed:.4f}s")
            return result
        return wrapper
    
    @staticmethod
    def retry(max_attempts: int = 3, delay: float = 1.0):
        """Retry function on failure"""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        if attempt == max_attempts - 1:
                            raise
                        logging.warning(f"Attempt {attempt + 1} failed: {e}")
                        time.sleep(delay)
            return wrapper
        return decorator
    
    @staticmethod
    def log_calls(func: Callable) -> Callable:
        """Log function calls"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_str = ', '.join(repr(a) for a in args)
            kwargs_str = ', '.join(f"{k}={v!r}" for k, v in kwargs.items())
            all_args = ', '.join(filter(None, [args_str, kwargs_str]))
            print(f"📞 {func.__name__}({all_args})")
            result = func(*args, **kwargs)
            print(f"⬅️  {func.__name__} returned {result!r}")
            return result
        return wrapper
    
    @staticmethod
    def cache_result(func: Callable) -> Callable:
        """Cache function results"""
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args):
            if args not in cache:
                cache[args] = func(*args)
            return cache[args]
        
        wrapper.cache = cache
        return wrapper
    
    @staticmethod
    def throttle(seconds: float):
        """Throttle function calls"""
        def decorator(func: Callable) -> Callable:
            last_call = [0]
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                current = time.time()
                if current - last_call[0] >= seconds:
                    last_call[0] = current
                    return func(*args, **kwargs)
            return wrapper
        return decorator
    
    @staticmethod
    def count_calls(func: Callable) -> Callable:
        """Count function calls"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.calls += 1
            return func(*args, **kwargs)
        
        wrapper.calls = 0
        return wrapper
    
    @staticmethod
    def require_types(**types):
        """Require specific argument types"""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                for arg_name, arg_type in types.items():
                    if arg_name in kwargs:
                        if not isinstance(kwargs[arg_name], arg_type):
                            raise TypeError(f"{arg_name} must be {arg_type}")
                return func(*args, **kwargs)
            return wrapper
        return decorator

# === CONVENIENCE DECORATORS ===
def timer(func: Callable) -> Callable:
    """Quick timer decorator"""
    return Decorators.timer(func)

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Quick retry decorator"""
    return Decorators.retry(max_attempts, delay)

def memoize(func: Callable) -> Callable:
    """Quick memoize decorator"""
    return Decorators.cache_result(func)

# === TESTING ===
if __name__ == "__main__":
    print("🎀 BaarliClaw Decorator Toolkit - Testing")
    print("=" * 50)
    
    # Test timer
    print("\n🧪 Testing Timer")
    
    @Decorators.timer
    def slow_function():
        time.sleep(0.1)
        return "Done"
    
    result = slow_function()
    
    # Test retry
    print("\n🧪 Testing Retry")
    
    attempt = [0]
    
    @Decorators.retry(max_attempts=3, delay=0.1)
    def flaky_function():
        attempt[0] += 1
        if attempt[0] < 2:
            raise ValueError("Not yet")
        return "Success"
    
    result = flaky_function()
    print(f"  Result after {attempt[0]} attempts: {result}")
    
    # Test cache
    print("\n🧪 Testing Cache")
    
    @Decorators.cache_result
    def expensive_calculation(n):
        print(f"  Calculating {n}...")
        return n ** 2
    
    result1 = expensive_calculation(5)
    result2 = expensive_calculation(5)  # Should use cache
    print(f"  First call: {result1}, Second call (cached): {result2}")
    
    # Test count calls
    print("\n🧪 Testing Count Calls")
    
    @Decorators.count_calls
    def my_function():
        return 42
    
    my_function()
    my_function()
    my_function()
    print(f"  Function called {my_function.calls} times")
    
    print("\n✅ Decorator Toolkit ready!")
