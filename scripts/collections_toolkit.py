#!/usr/bin/env python3
"""
📦 BAARLICLAW COLLECTIONS TOOLKIT
Datastruktur-håndtering
"""

from typing import Dict, List, Any, Optional, Callable
from collections import defaultdict, Counter

class ListUtils:
    """List utilities"""
    
    @staticmethod
    def chunk(lst: List, size: int) -> List[List]:
        """Split list into chunks"""
        return [lst[i:i + size] for i in range(0, len(lst), size)]
    
    @staticmethod
    def flatten(lst: List) -> List:
        """Flatten nested list"""
        result = []
        for item in lst:
            if isinstance(item, list):
                result.extend(ListUtils.flatten(item))
            else:
                result.append(item)
        return result
    
    @staticmethod
    def unique(lst: List) -> List:
        """Get unique elements"""
        seen = set()
        return [x for x in lst if not (x in seen or seen.add(x))]

class DictUtils:
    """Dictionary utilities"""
    
    @staticmethod
    def get_nested(d: Dict, path: str, default: Any = None) -> Any:
        """Get nested dict value"""
        keys = path.split(".")
        current = d
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        
        return current

# === TESTING ===
if __name__ == "__main__":
    print("📦 BaarliClaw Collections Toolkit - Testing")
    print("=" * 50)
    
    # Test list utils
    print("\n🧪 Testing List Utils")
    
    data = list(range(1, 11))
    chunks = ListUtils.chunk(data, 3)
    print(f"  Chunk [1-10] by 3: {chunks}")
    
    nested = [1, [2, 3], [4, [5, 6]]]
    flat = ListUtils.flatten(nested)
    print(f"  Flatten: {flat}")
    
    duplicates = [1, 2, 2, 3, 3, 3]
    unique = ListUtils.unique(duplicates)
    print(f"  Unique: {unique}")
    
    # Test dict utils
    print("\n🧪 Testing Dict Utils")
    
    nested_dict = {"a": {"b": {"c": "value"}}}
    value = DictUtils.get_nested(nested_dict, "a.b.c")
    print(f"  Get nested: {value}")
    
    print("\n✅ Collections Toolkit ready!")
