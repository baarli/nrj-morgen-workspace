#!/usr/bin/env python3
"""
λ BAARLICLAW FUNCTIONAL TOOLKIT
Funksjonell programmering
"""

from typing import Callable, TypeVar, List, Any, Optional
from functools import reduce, wraps

T = TypeVar('T')
U = TypeVar('U')

class Functional:
    """Functional programming utilities"""
    
    @staticmethod
    def pipe(value: T, *functions: Callable) -> Any:
        """Pipe value through functions"""
        result = value
        for func in functions:
            result = func(result)
        return result
    
    @staticmethod
    def compose(*functions: Callable) -> Callable:
        """Compose functions right to left"""
        def composed(x):
            result = x
            for func in reversed(functions):
                result = func(result)
            return result
        return composed
    
    @staticmethod
    def curry(func: Callable, arity: int = None) -> Callable:
        """Curry a function"""
        if arity is None:
            arity = func.__code__.co_argcount
        
        def curried(*args):
            if len(args) >= arity:
                return func(*args)
            return lambda *more: curried(*(args + more))
        
        return curried
    
    @staticmethod
    def partial(func: Callable, *args, **kwargs) -> Callable:
        """Partial application"""
        def partial_func(*more_args, **more_kwargs):
            all_args = args + more_args
            all_kwargs = {**kwargs, **more_kwargs}
            return func(*all_args, **all_kwargs)
        return partial_func
    
    @staticmethod
    def memoize(func: Callable) -> Callable:
        """Memoize function"""
        cache = {}
        
        @wraps(func)
        def wrapper(*args):
            if args not in cache:
                cache[args] = func(*args)
            return cache[args]
        
        return wrapper
    
    @staticmethod
    def map(func: Callable[[T], U], iterable: List[T]) -> List[U]:
        """Map function over list"""
        return [func(item) for item in iterable]
    
    @staticmethod
    def filter(predicate: Callable[[T], bool], iterable: List[T]) -> List[T]:
        """Filter list by predicate"""
        return [item for item in iterable if predicate(item)]
    
    @staticmethod
    def reduce(func: Callable[[T, T], T], iterable: List[T], initial: T = None) -> T:
        """Reduce list with function"""
        if initial is None:
            return reduce(func, iterable)
        return reduce(func, iterable, initial)
    
    @staticmethod
    def flatten(nested: List) -> List:
        """Flatten nested list"""
        result = []
        for item in nested:
            if isinstance(item, list):
                result.extend(Functional.flatten(item))
            else:
                result.append(item)
        return result
    
    @staticmethod
    def zip_with(func: Callable, *lists: List) -> List:
        """Zip lists with function"""
        return [func(*items) for items in zip(*lists)]
    
    @staticmethod
    def identity(x: T) -> T:
        """Identity function"""
        return x
    
    @staticmethod
    def constant(value: T) -> Callable:
        """Constant function"""
        return lambda *args, **kwargs: value
    
    @staticmethod
    def flip(func: Callable) -> Callable:
        """Flip function arguments"""
        def flipped(x, y):
            return func(y, x)
        return flipped

# === CONVENIENCE FUNCTIONS ===
def pipe(value: T, *funcs: Callable) -> Any:
    """Quick pipe"""
    return Functional.pipe(value, *funcs)

def compose(*funcs: Callable) -> Callable:
    """Quick compose"""
    return Functional.compose(*funcs)

def memoize(func: Callable) -> Callable:
    """Quick memoize"""
    return Functional.memoize(func)

# === TESTING ===
if __name__ == "__main__":
    print("λ BaarliClaw Functional Toolkit - Testing")
    print("=" * 50)
    
    # Test pipe
    print("\n🧪 Testing Pipe")
    result = Functional.pipe(
        5,
        lambda x: x * 2,
        lambda x: x + 1,
        lambda x: x ** 2
    )
    print(f"  5 -> *2 -> +1 -> **2 = {result}")
    
    # Test compose
    print("\n🧪 Testing Compose")
    add_one = lambda x: x + 1
    double = lambda x: x * 2
    composed = Functional.compose(add_one, double)
    print(f"  compose(add_one, double)(5) = {composed(5)}")
    
    # Test curry
    print("\n🧪 Testing Curry")
    def add(a, b, c):
        return a + b + c
    
    curried_add = Functional.curry(add)
    result = curried_add(1)(2)(3)
    print(f"  curried_add(1)(2)(3) = {result}")
    
    # Test memoize
    print("\n🧪 Testing Memoize")
    
    call_count = [0]
    
    @Functional.memoize
    def fib(n):
        call_count[0] += 1
        if n < 2:
            return n
        return fib(n-1) + fib(n-2)
    
    result = fib(10)
    print(f"  fib(10) = {result}")
    print(f"  Function calls: {call_count[0]}")
    
    # Test map/filter/reduce
    print("\n🧪 Testing Map/Filter/Reduce")
    numbers = [1, 2, 3, 4, 5]
    
    doubled = Functional.map(lambda x: x * 2, numbers)
    print(f"  map(*2): {doubled}")
    
    evens = Functional.filter(lambda x: x % 2 == 0, numbers)
    print(f"  filter(even): {evens}")
    
    total = Functional.reduce(lambda a, b: a + b, numbers)
    print(f"  reduce(+): {total}")
    
    print("\n✅ Functional Toolkit ready!")
