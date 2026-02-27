#!/usr/bin/env python3
"""
🔁 BAARLICLAW ITERATOR TOOLKIT
Iterator- og generator-verktøy
"""

from typing import Iterator, Iterable, TypeVar, Callable, List, Any
import itertools

T = TypeVar('T')

class IteratorUtils:
    """Iterator utilities"""
    
    @staticmethod
    def batch(iterable: Iterable[T], size: int) -> Iterator[List[T]]:
        """Batch iterator into chunks"""
        it = iter(iterable)
        while True:
            batch = list(itertools.islice(it, size))
            if not batch:
                return
            yield batch
    
    @staticmethod
    def take(iterable: Iterable[T], n: int) -> List[T]:
        """Take first n elements"""
        return list(itertools.islice(iterable, n))
    
    @staticmethod
    def skip(iterable: Iterable[T], n: int) -> Iterator[T]:
        """Skip first n elements"""
        it = iter(iterable)
        for _ in range(n):
            try:
                next(it)
            except StopIteration:
                return
        return it
    
    @staticmethod
    def enumerate_from(iterable: Iterable[T], start: int = 0) -> Iterator[tuple[int, T]]:
        """Enumerate from specific start"""
        return enumerate(iterable, start)
    
    @staticmethod
    def cycle(iterable: Iterable[T], times: int = 1) -> Iterator[T]:
        """Cycle through iterable n times"""
        for _ in range(times):
            for item in iterable:
                yield item
    
    @staticmethod
    def pairwise(iterable: Iterable[T]) -> Iterator[tuple[T, T]]:
        """Iterate pairwise"""
        it = iter(iterable)
        try:
            prev = next(it)
        except StopIteration:
            return
        
        for item in it:
            yield (prev, item)
            prev = item
    
    @staticmethod
    def window(iterable: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
        """Sliding window"""
        it = iter(iterable)
        window = tuple(itertools.islice(it, size))
        if len(window) == size:
            yield window
        
        for item in it:
            window = window[1:] + (item,)
            yield window

class GeneratorUtils:
    """Generator utilities"""
    
    @staticmethod
    def range_step(start: int, stop: int, step: int) -> Iterator[int]:
        """Range with custom step"""
        current = start
        while current < stop:
            yield current
            current += step
    
    @staticmethod
    def countdown(start: int, stop: int = 0) -> Iterator[int]:
        """Countdown generator"""
        while start >= stop:
            yield start
            start -= 1
    
    @staticmethod
    def repeat(value: T, times: int = None) -> Iterator[T]:
        """Repeat value n times (or forever if None)"""
        if times is None:
            while True:
                yield value
        else:
            for _ in range(times):
                yield value
    
    @staticmethod
    def chain(*iterables: Iterable[T]) -> Iterator[T]:
        """Chain multiple iterables"""
        for iterable in iterables:
            yield from iterable

# === CONVENIENCE FUNCTIONS ===
def chunks(lst: List[T], size: int) -> Iterator[List[T]]:
    """Quick chunking"""
    return IteratorUtils.batch(lst, size)

def pairwise_iter(lst: List[T]) -> Iterator[tuple[T, T]]:
    """Quick pairwise"""
    return IteratorUtils.pairwise(lst)

# === TESTING ===
if __name__ == "__main__":
    print("🔁 BaarliClaw Iterator Toolkit - Testing")
    print("=" * 50)
    
    # Test batching
    print("\n🧪 Testing Batching")
    data = list(range(1, 11))
    for i, batch in enumerate(IteratorUtils.batch(data, 3)):
        print(f"  Batch {i+1}: {batch}")
    
    # Test take/skip
    print("\n🧪 Testing Take/Skip")
    first_5 = IteratorUtils.take(data, 5)
    print(f"  First 5: {first_5}")
    
    skipped = list(IteratorUtils.skip(data, 5))
    print(f"  After skip 5: {skipped}")
    
    # Test pairwise
    print("\n🧪 Testing Pairwise")
    pairs = list(IteratorUtils.pairwise([1, 2, 3, 4, 5]))
    print(f"  Pairs: {pairs}")
    
    # Test window
    print("\n🧪 Testing Window")
    windows = list(IteratorUtils.window([1, 2, 3, 4, 5], 3))
    print(f"  Windows of 3: {windows}")
    
    # Test generators
    print("\n🧪 Testing Generators")
    countdown = list(GeneratorUtils.countdown(5, 2))
    print(f"  Countdown 5 to 2: {countdown}")
    
    repeated = list(GeneratorUtils.repeat("X", 5))
    print(f"  Repeat 'X' 5x: {repeated}")
    
    print("\n✅ Iterator Toolkit ready!")
