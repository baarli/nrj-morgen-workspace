#!/usr/bin/env python3
"""
⚡ BAARLICLAW ASYNC TOOLKIT
Asynkron programmering
"""

import asyncio
from typing import Callable, List, Any, Optional, Awaitable
from concurrent.futures import ThreadPoolExecutor
import time

class AsyncUtils:
    """Async utilities"""
    
    @staticmethod
    async def sleep(seconds: float):
        """Async sleep"""
        await asyncio.sleep(seconds)
    
    @staticmethod
    async def gather(*tasks: Awaitable) -> List[Any]:
        """Gather multiple async tasks"""
        return await asyncio.gather(*tasks)
    
    @staticmethod
    async def run_in_thread(func: Callable, *args, **kwargs) -> Any:
        """Run sync function in thread"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: func(*args, **kwargs))
    
    @staticmethod
    async def timeout(task: Awaitable, seconds: float) -> Any:
        """Run task with timeout"""
        return await asyncio.wait_for(task, timeout=seconds)
    
    @staticmethod
    def create_task(coro: Awaitable) -> asyncio.Task:
        """Create background task"""
        return asyncio.create_task(coro)

class ParallelRunner:
    """Run tasks in parallel"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    def run(self, func: Callable, items: List[Any]) -> List[Any]:
        """Run function on all items in parallel"""
        futures = [self.executor.submit(func, item) for item in items]
        return [f.result() for f in futures]
    
    def shutdown(self):
        """Shutdown executor"""
        self.executor.shutdown()

class RateLimiter:
    """Rate limiter"""
    
    def __init__(self, calls: int, period: float):
        self.calls = calls
        self.period = period
        self.timestamps: List[float] = []
    
    async def acquire(self):
        """Acquire rate limit slot"""
        now = time.time()
        
        # Remove old timestamps
        self.timestamps = [t for t in self.timestamps if now - t < self.period]
        
        # Wait if limit reached
        if len(self.timestamps) >= self.calls:
            sleep_time = self.timestamps[0] + self.period - now
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
        
        self.timestamps.append(time.time())

class Debouncer:
    """Debounce function calls"""
    
    def __init__(self, delay: float):
        self.delay = delay
        self.task: Optional[asyncio.Task] = None
    
    async def __call__(self, func: Callable, *args, **kwargs):
        """Debounce function call"""
        if self.task:
            self.task.cancel()
        
        async def delayed_call():
            await asyncio.sleep(self.delay)
            return func(*args, **kwargs)
        
        self.task = asyncio.create_task(delayed_call())
        return await self.task

# === CONVENIENCE FUNCTIONS ===
def run_async(coro: Awaitable) -> Any:
    """Quick run async function"""
    return asyncio.run(coro)

def run_parallel(func: Callable, items: List[Any], max_workers: int = 4) -> List[Any]:
    """Quick parallel execution"""
    runner = ParallelRunner(max_workers)
    try:
        return runner.run(func, items)
    finally:
        runner.shutdown()

# === TESTING ===
if __name__ == "__main__":
    print("⚡ BaarliClaw Async Toolkit - Testing")
    print("=" * 50)
    
    async def test_async():
        # Test gather
        print("\n🧪 Testing Gather")
        
        async def task(n):
            await asyncio.sleep(0.1)
            return n * 2
        
        results = await AsyncUtils.gather(
            task(1), task(2), task(3)
        )
        print(f"  Results: {results}")
        
        # Test timeout
        print("\n🧪 Testing Timeout")
        try:
            await AsyncUtils.timeout(
                asyncio.sleep(1),
                0.1
            )
        except asyncio.TimeoutError:
            print("  Timeout works!")
    
    # Run async tests
    asyncio.run(test_async())
    
    # Test parallel runner
    print("\n🧪 Testing Parallel Runner")
    
    def slow_square(n):
        time.sleep(0.1)
        return n ** 2
    
    numbers = [1, 2, 3, 4, 5]
    results = run_parallel(slow_square, numbers)
    print(f"  Squares: {results}")
    
    # Test rate limiter
    print("\n🧪 Testing Rate Limiter")
    
    async def test_rate_limit():
        limiter = RateLimiter(calls=2, period=1.0)
        
        for i in range(4):
            await limiter.acquire()
            print(f"  Call {i+1} at {time.time():.2f}")
    
    asyncio.run(test_rate_limit())
    
    print("\n✅ Async Toolkit ready!")
