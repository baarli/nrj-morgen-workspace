#!/usr/bin/env python3
"""
💾 BAARLICLAW SERIALIZATION TOOLKIT
Data-serialisering
"""

import json
import base64
from typing import Any, Optional
from dataclasses import dataclass, asdict

# SECURITY: pickle has been removed due to arbitrary code execution risk
# Use JSON serialization instead for all data

class JSONSerializer:
    """JSON serialization"""
    
    @staticmethod
    def encode(data: Any, indent: Optional[int] = None) -> str:
        """Encode to JSON string"""
        return json.dumps(data, indent=indent, default=str)
    
    @staticmethod
    def decode(json_str: str) -> Any:
        """Decode from JSON string"""
        return json.loads(json_str)
    
    @staticmethod
    def save(data: Any, filepath: str, indent: int = 2):
        """Save to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, default=str)
    
    @staticmethod
    def load(filepath: str) -> Any:
        """Load from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

class PickleSerializer:
    """Pickle serialization - DEPRECATED for security reasons
    
    WARNING: Pickle can execute arbitrary code during deserialization.
    This class now raises SecurityError if used.
    Use JSONSerializer instead.
    """
    
    class SecurityError(Exception):
        """Raised when unsafe serialization is attempted"""
        pass
    
    @staticmethod
    def encode(data: Any) -> bytes:
        """DEPRECATED - Use JSONSerializer instead"""
        raise PickleSerializer.SecurityError(
            "Pickle serialization is disabled for security. Use JSONSerializer instead."
        )
    
    @staticmethod
    def decode(pickle_bytes: bytes) -> Any:
        """DEPRECATED - Use JSONSerializer instead"""
        raise PickleSerializer.SecurityError(
            "Pickle deserialization is disabled for security. Use JSONSerializer instead."
        )
    
    @staticmethod
    def save(data: Any, filepath: str):
        """DEPRECATED - Use JSONSerializer instead"""
        raise PickleSerializer.SecurityError(
            "Pickle serialization is disabled for security. Use JSONSerializer.save() instead."
        )
    
    @staticmethod
    def load(filepath: str) -> Any:
        """DEPRECATED - Use JSONSerializer instead"""
        raise PickleSerializer.SecurityError(
            "Pickle deserialization is disabled for security. Use JSONSerializer.load() instead."
        )

class Base64Serializer:
    """Base64 encoding"""
    
    @staticmethod
    def encode(data: bytes) -> str:
        """Encode bytes to base64 string"""
        return base64.b64encode(data).decode('utf-8')
    
    @staticmethod
    def decode(base64_str: str) -> bytes:
        """Decode base64 string to bytes"""
        return base64.b64decode(base64_str)
    
    @staticmethod
    def encode_string(text: str) -> str:
        """Encode string to base64"""
        return Base64Serializer.encode(text.encode('utf-8'))
    
    @staticmethod
    def decode_string(base64_str: str) -> str:
        """Decode base64 to string"""
        return Base64Serializer.decode(base64_str).decode('utf-8')

class DataConverter:
    """Convert between data formats"""
    
    @staticmethod
    def to_json(data: Any) -> str:
        """Convert to JSON"""
        return JSONSerializer.encode(data)
    
    @staticmethod
    def from_json(json_str: str) -> Any:
        """Convert from JSON"""
        return JSONSerializer.decode(json_str)
    
    @staticmethod
    def dict_to_object(d: dict, cls: type) -> Any:
        """Convert dict to object"""
        return cls(**d)
    
    @staticmethod
    def object_to_dict(obj: Any) -> dict:
        """Convert object to dict"""
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        elif hasattr(obj, '__dataclass_fields__'):
            return asdict(obj)
        return {}

# === CONVENIENCE FUNCTIONS ===
def to_json(data: Any) -> str:
    """Quick JSON encode"""
    return JSONSerializer.encode(data)

def from_json(json_str: str) -> Any:
    """Quick JSON decode"""
    return JSONSerializer.decode(json_str)

def to_base64(text: str) -> str:
    """Quick base64 encode"""
    return Base64Serializer.encode_string(text)

def from_base64(base64_str: str) -> str:
    """Quick base64 decode"""
    return Base64Serializer.decode_string(base64_str)

# === TESTING ===
if __name__ == "__main__":
    print("💾 BaarliClaw Serialization Toolkit - Testing")
    print("=" * 50)
    
    # Test JSON
    print("\n🧪 Testing JSON")
    data = {"name": "Test", "value": 42, "items": [1, 2, 3]}
    json_str = JSONSerializer.encode(data, indent=2)
    print(f"  Encoded: {json_str[:50]}...")
    decoded = JSONSerializer.decode(json_str)
    print(f"  Decoded: {decoded}")
    
    # Test Pickle (Security check)
    print("\n🧪 Testing Pickle Security")
    try:
        PickleSerializer.encode(data)
        print("  ❌ Pickle should be disabled!")
    except PickleSerializer.SecurityError as e:
        print(f"  ✅ Pickle correctly disabled: {str(e)[:50]}...")
    
    # Test Base64
    print("\n🧪 Testing Base64")
    text = "Hello, World!"
    encoded = Base64Serializer.encode_string(text)
    print(f"  '{text}' -> '{encoded}'")
    decoded = Base64Serializer.decode_string(encoded)
    print(f"  Decoded: '{decoded}'")
    
    # Test conversion
    print("\n🧪 Testing Data Conversion")
    
    @dataclass
    class Person:
        name: str
        age: int
    
    person = Person("John", 30)
    person_dict = DataConverter.object_to_dict(person)
    print(f"  Object to dict: {person_dict}")
    
    print("\n✅ Serialization Toolkit ready!")
