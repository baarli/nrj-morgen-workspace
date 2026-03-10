#!/usr/bin/env python3
"""
BAARLICLAW ERROR HANDLING MODULE
Unified error handling, logging and retry logic for all NRJ Morgen scripts
"""

import sys
import traceback
import logging
import json
import time
from datetime import datetime
from functools import wraps
from typing import Callable, Any, Optional

# ============================================================================
# CONFIGURATION
# ============================================================================

LOG_DIR = "/root/.openclaw/workspace/brain/logs"
MAX_RETRIES = 3
RETRY_DELAY_BASE = 2  # seconds (exponential backoff)

# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging(script_name: str, level=logging.INFO) -> logging.Logger:
    """
    Set up structured logging for a script.
    
    Args:
        script_name: Name of the script (used in log filename)
        level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    import os
    os.makedirs(LOG_DIR, exist_ok=True)
    
    logger = logging.getLogger(script_name)
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers = []
    
    # File handler with rotation
    log_file = f"{LOG_DIR}/{script_name}.log"
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Structured format
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# ============================================================================
# ERROR HANDLING DECORATORS
# ============================================================================

def safe_execute(logger: Optional[logging.Logger] = None, 
                 default_return: Any = None,
                 log_level: int = logging.ERROR):
    """
    Decorator that catches all exceptions and logs them.
    
    Args:
        logger: Logger instance (if None, uses print)
        default_return: Value to return on exception
        log_level: Logging level for errors
    
    Usage:
        @safe_execute(logger=my_logger, default_return=[])
        def fetch_data():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_msg = f"Error in {func.__name__}: {str(e)}"
                tb = traceback.format_exc()
                
                if logger:
                    logger.log(log_level, f"{error_msg}\n{tb}")
                else:
                    print(f"❌ {error_msg}", file=sys.stderr)
                    
                return default_return
        return wrapper
    return decorator


def retry_on_error(max_retries: int = MAX_RETRIES,
                   delay_base: float = RETRY_DELAY_BASE,
                   exceptions: tuple = (Exception,),
                   logger: Optional[logging.Logger] = None):
    """
    Decorator that retries function on specified exceptions with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        delay_base: Base delay in seconds (doubles each retry)
        exceptions: Tuple of exceptions to catch
        logger: Logger instance
    
    Usage:
        @retry_on_error(max_retries=3, exceptions=(ConnectionError, TimeoutError))
        def api_call():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt < max_retries:
                        delay = delay_base * (2 ** attempt)
                        msg = f"Attempt {attempt + 1}/{max_retries + 1} failed for {func.__name__}: {e}. Retrying in {delay}s..."
                        
                        if logger:
                            logger.warning(msg)
                        else:
                            print(f"⚠️  {msg}")
                            
                        time.sleep(delay)
                    else:
                        msg = f"All {max_retries + 1} attempts failed for {func.__name__}"
                        if logger:
                            logger.error(f"{msg}: {e}")
                        else:
                            print(f"❌ {msg}: {e}", file=sys.stderr)
                            
            raise last_exception
        return wrapper
    return decorator


def rate_limited(min_delay: float = 1.0, logger: Optional[logging.Logger] = None):
    """
    Decorator that enforces minimum delay between function calls.
    
    Args:
        min_delay: Minimum seconds between calls
        logger: Logger instance
    """
    last_call_time = {}
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_id = func.__name__
            now = time.time()
            
            if func_id in last_call_time:
                elapsed = now - last_call_time[func_id]
                if elapsed < min_delay:
                    sleep_time = min_delay - elapsed
                    if logger:
                        logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
                    time.sleep(sleep_time)
            
            last_call_time[func_id] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

# ============================================================================
# CONTEXT MANAGERS
# ============================================================================

class ErrorContext:
    """Context manager for error handling with automatic cleanup."""
    
    def __init__(self, operation_name: str, 
                 logger: Optional[logging.Logger] = None,
                 cleanup: Optional[Callable] = None):
        self.operation_name = operation_name
        self.logger = logger
        self.cleanup = cleanup
        self.error = None
        
    def __enter__(self):
        if self.logger:
            self.logger.info(f"Starting: {self.operation_name}")
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.error = exc_val
            error_msg = f"Failed: {self.operation_name} - {exc_val}"
            tb = traceback.format_exception(exc_type, exc_val, exc_tb)
            
            if self.logger:
                self.logger.error(f"{error_msg}\n{''.join(tb)}")
            else:
                print(f"❌ {error_msg}", file=sys.stderr)
        else:
            if self.logger:
                self.logger.info(f"Completed: {self.operation_name}")
                
        if self.cleanup:
            try:
                self.cleanup()
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Cleanup failed: {e}")
                    
        return True  # Suppress exception if cleanup succeeded

# ============================================================================
# API ERROR HANDLING
# ============================================================================

class APIError(Exception):
    """Custom exception for API errors with structured data."""
    
    def __init__(self, message: str, status_code: Optional[int] = None,
                 response_body: Optional[str] = None,
                 endpoint: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body
        self.endpoint = endpoint
        self.timestamp = datetime.now().isoformat()
        
    def to_dict(self) -> dict:
        return {
            'error': str(self),
            'status_code': self.status_code,
            'endpoint': self.endpoint,
            'timestamp': self.timestamp
        }


def handle_api_error(response, endpoint: str, logger: Optional[logging.Logger] = None):
    """
    Handle API response errors consistently.
    
    Args:
        response: HTTP response object
        endpoint: API endpoint URL
        logger: Logger instance
    
    Raises:
        APIError: If response indicates an error
    """
    try:
        status = response.status if hasattr(response, 'status') else response.status_code
    except:
        status = None
        
    if status and status >= 400:
        try:
            body = response.read().decode() if hasattr(response, 'read') else str(response)
        except:
            body = "Could not read response body"
            
        error = APIError(
            message=f"API error {status}",
            status_code=status,
            response_body=body[:500],  # Limit size
            endpoint=endpoint
        )
        
        if logger:
            logger.error(f"API Error: {error.to_dict()}")
            
        raise error

# ============================================================================
# ERROR REPORTING
# ============================================================================

def generate_error_report(script_name: str, 
                         error_count: int,
                         details: list) -> str:
    """
    Generate a formatted error report.
    
    Args:
        script_name: Name of the script
        error_count: Number of errors
        details: List of error detail strings
    
    Returns:
        Formatted report string
    """
    report = f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                         ERROR REPORT                                        ║
╚═══════════════════════════════════════════════════════════════════════════╝

Script:     {script_name}
Timestamp:  {datetime.now().isoformat()}
Errors:     {error_count}

Details:
"""
    for i, detail in enumerate(details, 1):
        report += f"  {i}. {detail}\n"
        
    report += """
═══════════════════════════════════════════════════════════════════════════
"""
    return report

# ============================================================================
# MAIN EXECUTION WRAPPER
# ============================================================================

def run_with_error_handling(script_name: str, main_func: Callable, 
                           notify_on_error: bool = False):
    """
    Wrapper for main script execution with comprehensive error handling.
    
    Args:
        script_name: Name of the script
        main_func: Main function to execute
        notify_on_error: Whether to send notification on error
    """
    logger = setup_logging(script_name)
    error_details = []
    
    try:
        logger.info(f"=" * 70)
        logger.info(f"Starting {script_name}")
        logger.info(f"=" * 70)
        
        result = main_func()
        
        logger.info(f"=" * 70)
        logger.info(f"Completed {script_name} successfully")
        logger.info(f"=" * 70)
        
        return result
        
    except Exception as e:
        error_msg = f"Critical error in {script_name}: {str(e)}"
        tb = traceback.format_exc()
        
        logger.error(f"{error_msg}\n{tb}")
        error_details.append(error_msg)
        
        # Print to stderr for visibility
        print(f"\n❌ {error_msg}\n", file=sys.stderr)
        
        # Generate and save error report
        report = generate_error_report(script_name, 1, error_details)
        report_file = f"{LOG_DIR}/{script_name}_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(report_file, 'w') as f:
            f.write(report)
            f.write(f"\n\nFull traceback:\n{tb}")
            
        print(f"Error report saved to: {report_file}")
        
        # Exit with error code
        sys.exit(1)

# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    'setup_logging',
    'safe_execute',
    'retry_on_error',
    'rate_limited',
    'ErrorContext',
    'APIError',
    'handle_api_error',
    'generate_error_report',
    'run_with_error_handling',
]

# ============================================================================
# TEST / EXAMPLE
# ============================================================================

if __name__ == '__main__':
    # Example usage
    logger = setup_logging('error_handler_test')
    
    @safe_execute(logger=logger, default_return="fallback")
    def risky_operation():
        raise ValueError("Something went wrong!")
    
    @retry_on_error(max_retries=2, logger=logger)
    def flaky_api_call():
        import random
        if random.random() < 0.7:
            raise ConnectionError("Network error")
        return "Success!"
    
    print("Testing error handling module...")
    result = risky_operation()
    print(f"Safe execute result: {result}")
    
    try:
        result = flaky_api_call()
        print(f"Retry result: {result}")
    except Exception as e:
        print(f"Retry failed: {e}")
        
    print("✅ Error handling module test complete")
