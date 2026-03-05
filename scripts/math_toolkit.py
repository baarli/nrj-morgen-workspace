#!/usr/bin/env python3
"""
📐 BAARLICLAW MATH TOOLKIT
Matematiske og statistiske verktøy
"""

import math
import random
from typing import List, Optional, Tuple, Callable, Any
from dataclasses import dataclass

@dataclass
class StatsResult:
    """Statistics result"""
    count: int
    sum: float
    mean: float
    median: float
    mode: Optional[float]
    std_dev: float
    min: float
    max: float
    range: float

class Statistics:
    """Statistical calculations"""
    
    @staticmethod
    def calculate(data: List[float]) -> StatsResult:
        """Calculate all statistics"""
        if not data:
            raise ValueError("Empty dataset")
        
        n = len(data)
        total = sum(data)
        mean = total / n
        
        # Median
        sorted_data = sorted(data)
        mid = n // 2
        if n % 2 == 0:
            median = (sorted_data[mid - 1] + sorted_data[mid]) / 2
        else:
            median = sorted_data[mid]
        
        # Mode
        from collections import Counter
        counts = Counter(data)
        max_count = max(counts.values())
        modes = [k for k, v in counts.items() if v == max_count]
        mode = modes[0] if len(modes) == 1 else None
        
        # Standard deviation
        variance = sum((x - mean) ** 2 for x in data) / n
        std_dev = math.sqrt(variance)
        
        return StatsResult(
            count=n,
            sum=total,
            mean=mean,
            median=median,
            mode=mode,
            std_dev=std_dev,
            min=min(data),
            max=max(data),
            range=max(data) - min(data)
        )
    
    @staticmethod
    def percentile(data: List[float], p: float) -> float:
        """Calculate percentile"""
        if not 0 <= p <= 100:
            raise ValueError("Percentile must be between 0 and 100")
        
        sorted_data = sorted(data)
        k = (len(sorted_data) - 1) * p / 100
        f = math.floor(k)
        c = math.ceil(k)
        
        if f == c:
            return sorted_data[int(k)]
        
        return sorted_data[f] * (c - k) + sorted_data[c] * (k - f)
    
    @staticmethod
    def correlation(x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient"""
        if len(x) != len(y):
            raise ValueError("Lists must have same length")
        
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denom_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x))
        denom_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
        
        if denom_x == 0 or denom_y == 0:
            return 0
        
        return numerator / (denom_x * denom_y)
    
    @staticmethod
    def moving_average(data: List[float], window: int) -> List[float]:
        """Calculate moving average"""
        if window > len(data):
            return []
        
        result = []
        for i in range(len(data) - window + 1):
            avg = sum(data[i:i + window]) / window
            result.append(avg)
        
        return result
    
    @staticmethod
    def normalize(data: List[float], method: str = "minmax") -> List[float]:
        """Normalize data"""
        if not data:
            return []
        
        if method == "minmax":
            min_val = min(data)
            max_val = max(data)
            range_val = max_val - min_val
            
            if range_val == 0:
                return [0.5] * len(data)
            
            return [(x - min_val) / range_val for x in data]
        
        elif method == "zscore":
            mean = sum(data) / len(data)
            variance = sum((x - mean) ** 2 for x in data) / len(data)
            std_dev = math.sqrt(variance)
            
            if std_dev == 0:
                return [0] * len(data)
            
            return [(x - mean) / std_dev for x in data]
        
        else:
            raise ValueError(f"Unknown method: {method}")

class MathUtils:
    """Mathematical utilities"""
    
    @staticmethod
    def clamp(value: float, min_val: float, max_val: float) -> float:
        """Clamp value between min and max"""
        return max(min_val, min(max_val, value))
    
    @staticmethod
    def lerp(start: float, end: float, t: float) -> float:
        """Linear interpolation"""
        return start + (end - start) * t
    
    @staticmethod
    def map_range(value: float, 
                  from_min: float, from_max: float,
                  to_min: float, to_max: float) -> float:
        """Map value from one range to another"""
        from_range = from_max - from_min
        to_range = to_max - to_min
        
        if from_range == 0:
            return to_min
        
        return to_min + (value - from_min) * to_range / from_range
    
    @staticmethod
    def round_to(value: float, nearest: float) -> float:
        """Round to nearest multiple"""
        return round(value / nearest) * nearest
    
    @staticmethod
    def is_prime(n: int) -> bool:
        """Check if number is prime"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        
        return True
    
    @staticmethod
    def fibonacci(n: int) -> int:
        """Calculate nth Fibonacci number"""
        if n <= 0:
            return 0
        if n == 1:
            return 1
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        
        return b
    
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Greatest common divisor"""
        while b:
            a, b = b, a % b
        return a
    
    @staticmethod
    def lcm(a: int, b: int) -> int:
        """Least common multiple"""
        return abs(a * b) // MathUtils.gcd(a, b) if a and b else 0

class RandomUtils:
    """Random utilities"""
    
    @staticmethod
    def choice_weighted(choices: List[Tuple[Any, float]]) -> Any:
        """Make weighted random choice"""
        total = sum(weight for _, weight in choices)
        r = random.uniform(0, total)
        
        cumulative = 0
        for choice, weight in choices:
            cumulative += weight
            if r <= cumulative:
                return choice
        
        return choices[-1][0]
    
    @staticmethod
    def shuffle(data: List) -> List:
        """Return shuffled copy"""
        result = data.copy()
        random.shuffle(result)
        return result
    
    @staticmethod
    def sample_unique(min_val: int, max_val: int, count: int) -> List[int]:
        """Sample unique random integers"""
        if count > (max_val - min_val + 1):
            raise ValueError("Count exceeds range")
        
        return random.sample(range(min_val, max_val + 1), count)

# === CONVENIENCE FUNCTIONS ===
def mean(data: List[float]) -> float:
    """Quick mean"""
    return sum(data) / len(data) if data else 0

def median(data: List[float]) -> float:
    """Quick median"""
    if not data:
        return 0
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    return sorted_data[mid]

def std_dev(data: List[float]) -> float:
    """Quick standard deviation"""
    if not data:
        return 0
    m = mean(data)
    variance = sum((x - m) ** 2 for x in data) / len(data)
    return math.sqrt(variance)

# === TESTING ===
if __name__ == "__main__":
    print("📐 BaarliClaw Math Toolkit - Testing")
    print("=" * 50)
    
    # Test statistics
    print("\n🧪 Testing Statistics")
    data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    stats = Statistics.calculate(data)
    
    print(f"  Count: {stats.count}")
    print(f"  Mean: {stats.mean:.2f}")
    print(f"  Median: {stats.median:.2f}")
    print(f"  Std Dev: {stats.std_dev:.2f}")
    print(f"  Range: {stats.range}")
    
    # Test percentiles
    p25 = Statistics.percentile(data, 25)
    p75 = Statistics.percentile(data, 75)
    print(f"  25th percentile: {p25}")
    print(f"  75th percentile: {p75}")
    
    # Test correlation
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    corr = Statistics.correlation(x, y)
    print(f"\n  Correlation: {corr:.4f}")
    
    # Test math utils
    print("\n🧪 Testing Math Utils")
    print(f"  clamp(150, 0, 100): {MathUtils.clamp(150, 0, 100)}")
    print(f"  lerp(0, 100, 0.5): {MathUtils.lerp(0, 100, 0.5)}")
    print(f"  map_range(50, 0, 100, 0, 1): {MathUtils.map_range(50, 0, 100, 0, 1)}")
    print(f"  is_prime(17): {MathUtils.is_prime(17)}")
    print(f"  fibonacci(10): {MathUtils.fibonacci(10)}")
    print(f"  gcd(48, 18): {MathUtils.gcd(48, 18)}")
    
    # Test random
    print("\n🧪 Testing Random Utils")
    choices = [("A", 0.5), ("B", 0.3), ("C", 0.2)]
    results = {"A": 0, "B": 0, "C": 0}
    for _ in range(1000):
        choice = RandomUtils.choice_weighted(choices)
        results[choice] += 1
    print(f"  Weighted choices (1000 trials): {results}")
    
    print("\n✅ Math Toolkit ready!")
