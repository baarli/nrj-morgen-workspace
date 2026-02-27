#!/usr/bin/env python3
"""
Performance Profiler - Track execution time and resource usage
"""

import time
import functools
import json
import os
from datetime import datetime
from pathlib import Path
from collections import defaultdict

class PerformanceProfiler:
    """Track and analyze performance metrics"""
    
    _instance = None
    _data = defaultdict(lambda: {'calls': 0, 'total_time': 0, 'max_time': 0, 'min_time': float('inf')})
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def reset(cls):
        """Reset all profiling data"""
        cls._data.clear()
    
    @classmethod
    def record(cls, name, duration):
        """Record a timing measurement"""
        cls._data[name]['calls'] += 1
        cls._data[name]['total_time'] += duration
        cls._data[name]['max_time'] = max(cls._data[name]['max_time'], duration)
        cls._data[name]['min_time'] = min(cls._data[name]['min_time'], duration)
    
    @classmethod
    def get_stats(cls, name=None):
        """Get profiling statistics"""
        if name:
            data = cls._data.get(name, {})
            if not data or data['calls'] == 0:
                return None
            return {
                'name': name,
                'calls': data['calls'],
                'total_time': data['total_time'],
                'avg_time': data['total_time'] / data['calls'],
                'max_time': data['max_time'],
                'min_time': data['min_time'] if data['min_time'] != float('inf') else 0
            }
        else:
            return [cls.get_stats(name) for name in cls._data.keys()]
    
    @classmethod
    def print_report(cls):
        """Print formatted performance report"""
        print("\n" + "=" * 70)
        print("📊 PERFORMANCE PROFILE REPORT")
        print("=" * 70)
        print(f"{'Function':<30} {'Calls':<8} {'Total':<10} {'Avg':<10} {'Max':<10}")
        print("-" * 70)
        
        stats = sorted(cls.get_stats(), key=lambda x: x['total_time'], reverse=True)
        
        for stat in stats:
            print(f"{stat['name']:<30} {stat['calls']:<8} "
                  f"{stat['total_time']:.3f}s   {stat['avg_time']:.4f}s   {stat['max_time']:.4f}s")
        
        print("=" * 70)
    
    @classmethod
    def save_report(cls, output_dir='/root/.openclaw/workspace/brain/reports'):
        """Save report to JSON file"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        report_file = Path(output_dir) / f'performance-profile-{timestamp}.json'
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'functions': cls.get_stats()
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_file


def profile(func):
    """Decorator to profile function execution time"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        
        # Get function identifier
        name = f"{func.__module__}.{func.__name__}"
        PerformanceProfiler.record(name, duration)
        
        return result
    return wrapper


class Timer:
    """Context manager for timing code blocks"""
    
    def __init__(self, name="block"):
        self.name = name
        self.start_time = None
        self.duration = None
    
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, *args):
        self.duration = time.perf_counter() - self.start_time
        PerformanceProfiler.record(self.name, self.duration)
    
    def __str__(self):
        if self.duration is not None:
            return f"Timer({self.name}): {self.duration:.4f}s"
        return f"Timer({self.name}): running..."


# Example usage and testing
if __name__ == '__main__':
    @profile
    def slow_function():
        time.sleep(0.1)
        return "done"
    
    @profile
    def fast_function():
        time.sleep(0.01)
        return "done"
    
    # Run some test functions
    for _ in range(5):
        slow_function()
        fast_function()
    
    # Time a block
    with Timer("test_block"):
        time.sleep(0.05)
    
    # Print report
    PerformanceProfiler.print_report()
    
    # Save report
    report_file = PerformanceProfiler.save_report()
    print(f"\n💾 Report saved to: {report_file}")
