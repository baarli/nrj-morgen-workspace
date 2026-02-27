#!/usr/bin/env python3
"""
🧪 BAARLICLAW TESTING TOOLKIT
Testing framework for scripts and functions
"""

import os
import sys
import time
import traceback
from typing import List, Dict, Callable, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("TestingToolkit")

@dataclass
class TestResult:
    """Test result"""
    name: str
    passed: bool
    duration_ms: float
    error: Optional[str] = None
    output: Any = None

@dataclass
class TestSuite:
    """Test suite results"""
    name: str
    results: List[TestResult] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    
    @property
    def passed_count(self) -> int:
        return sum(1 for r in self.results if r.passed)
    
    @property
    def failed_count(self) -> int:
        return sum(1 for r in self.results if not r.passed)
    
    @property
    def total_duration_ms(self) -> float:
        return sum(r.duration_ms for r in self.results)
    
    @property
    def success_rate(self) -> float:
        if not self.results:
            return 0.0
        return (self.passed_count / len(self.results)) * 100

class TestRunner:
    """Run tests and collect results"""
    
    def __init__(self, suite_name: str = "Test Suite"):
        self.suite = TestSuite(name=suite_name)
        self.setup_func: Optional[Callable] = None
        self.teardown_func: Optional[Callable] = None
    
    def setup(self, func: Callable):
        """Set setup function"""
        self.setup_func = func
        return func
    
    def teardown(self, func: Callable):
        """Set teardown function"""
        self.teardown_func = func
        return func
    
    def test(self, name: Optional[str] = None):
        """Decorator for test functions"""
        def decorator(func: Callable):
            test_name = name or func.__name__
            
            def wrapper(*args, **kwargs):
                return self._run_test(test_name, func, *args, **kwargs)
            
            wrapper._is_test = True
            wrapper._test_name = test_name
            return wrapper
        return decorator
    
    def _run_test(self, name: str, func: Callable, *args, **kwargs) -> TestResult:
        """Run a single test"""
        # Setup
        if self.setup_func:
            try:
                self.setup_func()
            except Exception as e:
                return TestResult(name, False, 0, f"Setup failed: {e}")
        
        # Run test
        start = time.time()
        try:
            output = func(*args, **kwargs)
            duration = (time.time() - start) * 1000
            
            result = TestResult(name, True, duration, output=output)
            
        except AssertionError as e:
            duration = (time.time() - start) * 1000
            result = TestResult(name, False, duration, str(e))
            
        except Exception as e:
            duration = (time.time() - start) * 1000
            error = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
            result = TestResult(name, False, duration, error)
        
        # Teardown
        if self.teardown_func:
            try:
                self.teardown_func()
            except:
                pass
        
        self.suite.results.append(result)
        return result
    
    def run_all(self, obj: Any) -> TestSuite:
        """Run all test methods in an object"""
        for attr_name in dir(obj):
            attr = getattr(obj, attr_name)
            if callable(attr) and hasattr(attr, '_is_test'):
                attr()
        
        return self.suite
    
    def report(self) -> str:
        """Generate test report"""
        lines = [
            f"\n{'='*60}",
            f"🧪 TEST REPORT: {self.suite.name}",
            f"{'='*60}",
            f"Total tests: {len(self.suite.results)}",
            f"Passed: {self.suite.passed_count} ✅",
            f"Failed: {self.suite.failed_count} ❌",
            f"Success rate: {self.suite.success_rate:.1f}%",
            f"Total duration: {self.suite.total_duration_ms:.2f}ms",
            f"{'='*60}",
        ]
        
        if self.suite.failed_count > 0:
            lines.append("\n❌ FAILED TESTS:")
            for result in self.suite.results:
                if not result.passed:
                    lines.append(f"\n  • {result.name}")
                    lines.append(f"    Duration: {result.duration_ms:.2f}ms")
                    if result.error:
                        lines.append(f"    Error: {result.error[:200]}")
        
        lines.append(f"\n{'='*60}")
        
        return "\n".join(lines)

class Assert:
    """Assertion helpers"""
    
    @staticmethod
    def equal(actual: Any, expected: Any, message: Optional[str] = None):
        """Assert equal"""
        if actual != expected:
            msg = message or f"Expected {expected}, got {actual}"
            raise AssertionError(msg)
    
    @staticmethod
    def true(value: bool, message: Optional[str] = None):
        """Assert true"""
        if not value:
            raise AssertionError(message or "Expected True, got False")
    
    @staticmethod
    def false(value: bool, message: Optional[str] = None):
        """Assert false"""
        if value:
            raise AssertionError(message or "Expected False, got True")
    
    @staticmethod
    def is_none(value: Any, message: Optional[str] = None):
        """Assert is None"""
        if value is not None:
            raise AssertionError(message or f"Expected None, got {value}")
    
    @staticmethod
    def is_not_none(value: Any, message: Optional[str] = None):
        """Assert is not None"""
        if value is None:
            raise AssertionError(message or "Expected not None")
    
    @staticmethod
    def in_list(item: Any, container: list, message: Optional[str] = None):
        """Assert item in list"""
        if item not in container:
            raise AssertionError(message or f"{item} not in {container}")
    
    @staticmethod
    def raises(exception_type: type, func: Callable, *args, **kwargs):
        """Assert raises exception"""
        try:
            func(*args, **kwargs)
            raise AssertionError(f"Expected {exception_type.__name__} to be raised")
        except exception_type:
            pass
    
    @staticmethod
    def almost_equal(actual: float, expected: float, 
                     places: int = 7, message: Optional[str] = None):
        """Assert almost equal (for floats)"""
        if round(abs(actual - expected), places) != 0:
            msg = message or f"Expected {expected}, got {actual}"
            raise AssertionError(msg)

class Mock:
    """Simple mocking utility"""
    
    def __init__(self, return_value: Any = None):
        self.return_value = return_value
        self.calls: List[tuple] = []
    
    def __call__(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        return self.return_value
    
    @property
    def call_count(self) -> int:
        return len(self.calls)
    
    def assert_called(self):
        """Assert was called"""
        if self.call_count == 0:
            raise AssertionError("Expected to be called, but wasn't")
    
    def assert_called_with(self, *args, **kwargs):
        """Assert called with specific args"""
        if (args, kwargs) not in self.calls:
            raise AssertionError(f"Expected call with {args}, {kwargs}")

# === CONVENIENCE FUNCTIONS ===
def quick_test(name: str, func: Callable) -> TestResult:
    """Quick single test"""
    runner = TestRunner()
    return runner._run_test(name, func)

def run_tests_in_module(module) -> TestSuite:
    """Run all tests in a module"""
    runner = TestRunner(module.__name__)
    
    for name in dir(module):
        obj = getattr(module, name)
        if callable(obj) and hasattr(obj, '_is_test'):
            obj()
    
    return runner.suite

# === TESTING ===
if __name__ == "__main__":
    print("🧪 BaarliClaw Testing Toolkit - Testing")
    print("=" * 50)
    
    # Create test runner
    runner = TestRunner("Demo Tests")
    
    # Define tests
    @runner.test("test_addition")
    def test_addition():
        Assert.equal(1 + 1, 2)
    
    @runner.test("test_string")
    def test_string():
        Assert.true("hello".startswith("he"))
    
    @runner.test("test_list")
    def test_list():
        my_list = [1, 2, 3]
        Assert.in_list(2, my_list)
    
    @runner.test("test_failure")
    def test_failure():
        # This will fail
        Assert.equal(1, 2, "One should equal two")
    
    # Run tests
    print("\n🧪 Running tests...")
    test_addition()
    test_string()
    test_list()
    test_failure()
    
    # Report
    print(runner.report())
    
    print("\n✅ Testing Toolkit ready!")
