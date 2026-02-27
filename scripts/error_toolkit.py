#!/usr/bin/env python3
"""
⚠️ BAARLICLAW ERROR TOOLKIT
Feilhåndtering og -logging
"""

import sys
import traceback
import logging
from typing import Optional, Callable, Any, Dict, List
from dataclasses import dataclass
from datetime import datetime
from functools import wraps

@dataclass
class ErrorInfo:
    """Error information"""
    type: str
    message: str
    traceback: str
    timestamp: datetime
    context: Optional[Dict] = None

class ErrorHandler:
    """Central error handling"""
    
    def __init__(self):
        self.handlers: List[Callable] = []
        self.errors: List[ErrorInfo] = []
        self.max_errors = 100
    
    def register(self, handler: Callable):
        """Register error handler"""
        self.handlers.append(handler)
    
    def handle(self, exception: Exception, context: Optional[Dict] = None):
        """Handle an exception"""
        error_info = ErrorInfo(
            type=type(exception).__name__,
            message=str(exception),
            traceback=traceback.format_exc(),
            timestamp=datetime.now(),
            context=context
        )
        
        # Store error
        self.errors.append(error_info)
        if len(self.errors) > self.max_errors:
            self.errors.pop(0)
        
        # Call handlers
        for handler in self.handlers:
            try:
                handler(error_info)
            except Exception as e:
                logging.error(f"Error handler failed: {e}")
    
    def get_errors(self, limit: Optional[int] = None) -> List[ErrorInfo]:
        """Get recent errors"""
        if limit:
            return self.errors[-limit:]
        return self.errors.copy()
    
    def clear(self):
        """Clear error history"""
        self.errors.clear()
    
    def has_errors(self, error_type: Optional[str] = None) -> bool:
        """Check if errors exist"""
        if error_type:
            return any(e.type == error_type for e in self.errors)
        return len(self.errors) > 0

class RetryManager:
    """Retry logic for functions"""
    
    def __init__(self, max_retries: int = 3, 
                 delay: float = 1.0,
                 backoff: float = 2.0,
                 exceptions: tuple = (Exception,)):
        self.max_retries = max_retries
        self.delay = delay
        self.backoff = backoff
        self.exceptions = exceptions
    
    def __call__(self, func: Callable) -> Callable:
        """Decorator for retry logic"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = self.delay
            
            for attempt in range(self.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except self.exceptions as e:
                    if attempt == self.max_retries:
                        raise
                    
                    logging.warning(
                        f"Attempt {attempt + 1} failed: {e}. "
                        f"Retrying in {delay}s..."
                    )
                    
                    import time
                    time.sleep(delay)
                    delay *= self.backoff
            
            return None  # Should never reach here
        
        return wrapper

class SafeExecutor:
    """Safely execute functions"""
    
    def __init__(self, default_return: Any = None,
                 log_errors: bool = True):
        self.default_return = default_return
        self.log_errors = log_errors
        self.error_handler = ErrorHandler()
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function safely"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if self.log_errors:
                self.error_handler.handle(e, {
                    'function': func.__name__,
                    'args': args,
                    'kwargs': kwargs
                })
            return self.default_return
    
    def __call__(self, func: Callable) -> Callable:
        """Decorator for safe execution"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.execute(func, *args, **kwargs)
        return wrapper

class ErrorFormatter:
    """Format errors for display"""
    
    @staticmethod
    def format_short(error: ErrorInfo) -> str:
        """Short error format"""
        return f"[{error.timestamp.strftime('%H:%M:%S')}] {error.type}: {error.message[:50]}"
    
    @staticmethod
    def format_full(error: ErrorInfo) -> str:
        """Full error format"""
        lines = [
            f"Error: {error.type}",
            f"Message: {error.message}",
            f"Time: {error.timestamp.isoformat()}",
            "Traceback:",
            error.traceback
        ]
        
        if error.context:
            lines.extend([
                "Context:",
                str(error.context)
            ])
        
        return '\n'.join(lines)
    
    @staticmethod
    def format_user_friendly(error: ErrorInfo) -> str:
        """User-friendly error message"""
        friendly_messages = {
            'ValueError': 'Invalid value provided',
            'TypeError': 'Wrong type of data',
            'KeyError': 'Required information missing',
            'IndexError': 'Position out of range',
            'FileNotFoundError': 'File not found',
            'ConnectionError': 'Network connection failed',
            'TimeoutError': 'Operation timed out'
        }
        
        return friendly_messages.get(
            error.type, 
            f"An error occurred: {error.message}"
        )

# === CONVENIENCE FUNCTIONS ===
def safe_call(func: Callable, *args, default: Any = None, **kwargs) -> Any:
    """Quick safe function call"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logging.error(f"Error in {func.__name__}: {e}")
        return default

def retry(max_retries: int = 3, delay: float = 1.0):
    """Quick retry decorator"""
    return RetryManager(max_retries=max_retries, delay=delay)

# === TESTING ===
if __name__ == "__main__":
    print("⚠️ BaarliClaw Error Toolkit - Testing")
    print("=" * 50)
    
    # Test error handler
    print("\n🧪 Testing Error Handler")
    handler = ErrorHandler()
    
    def log_error(error: ErrorInfo):
        print(f"  Handled: {error.type} - {error.message[:30]}")
    
    handler.register(log_error)
    
    try:
        1 / 0
    except Exception as e:
        handler.handle(e, {'operation': 'division'})
    
    print(f"  Total errors: {len(handler.get_errors())}")
    
    # Test retry manager
    print("\n🧪 Testing Retry Manager")
    
    attempt_count = [0]  # Use list to make it mutable
    
    @RetryManager(max_retries=2, delay=0.1)
    def flaky_function():
        attempt_count[0] += 1
        if attempt_count[0] < 3:
            raise ValueError("Not yet!")
        return "Success!"
    
    result = flaky_function()
    print(f"  Result after {attempt_count[0]} attempts: {result}")
    
    # Test safe executor
    print("\n🧪 Testing Safe Executor")
    
    executor = SafeExecutor(default_return="fallback")
    
    def risky_function():
        raise ValueError("Oops!")
    
    result = executor.execute(risky_function)
    print(f"  Safe execution result: {result}")
    
    # Test error formatter
    print("\n🧪 Testing Error Formatter")
    
    error = ErrorInfo(
        type="ValueError",
        message="Invalid input",
        traceback="Traceback...",
        timestamp=datetime.now()
    )
    
    short = ErrorFormatter.format_short(error)
    print(f"  Short: {short}")
    
    user_friendly = ErrorFormatter.format_user_friendly(error)
    print(f"  User friendly: {user_friendly}")
    
    print("\n✅ Error Toolkit ready!")
