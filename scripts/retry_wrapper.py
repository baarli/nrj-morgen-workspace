#!/usr/bin/env python3
"""
🔄 Retry Wrapper - Add retry logic to external API calls
"""

import functools
import time
import random
from typing import Callable, Any

def retry_with_backoff(max_retries=3, base_delay=1, max_delay=60, exceptions=(Exception,)):
    """
    Decorator to retry function calls with exponential backoff
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exceptions: Tuple of exceptions to catch
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        raise last_exception
                    
                    # Calculate delay with exponential backoff and jitter
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    jitter = random.uniform(0, delay * 0.1)  # 10% jitter
                    total_delay = delay + jitter
                    
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying in {total_delay:.1f}s...")
                    time.sleep(total_delay)
            
            raise last_exception
        
        return wrapper
    return decorator


def retry_on_network_error(max_retries=3):
    """Convenience decorator for network operations"""
    import requests
    return retry_with_backoff(
        max_retries=max_retries,
        base_delay=2,
        exceptions=(requests.RequestException, ConnectionError, TimeoutError)
    )


# Example usage
if __name__ == '__main__':
    @retry_with_backoff(max_retries=3, base_delay=1)
    def test_function():
        import random
        if random.random() < 0.7:
            raise Exception("Random failure")
        return "Success!"
    
    print("Testing retry wrapper...")
    try:
        result = test_function()
        print(f"Result: {result}")
    except Exception as e:
        print(f"Final failure: {e}")
