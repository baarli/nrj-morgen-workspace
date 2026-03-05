#!/usr/bin/env python3
"""
🔑 BAARLICLAW UUID TOOLKIT
UUID-generering og -håndtering
"""

import uuid
import secrets
import hashlib
from typing import Optional

class UUIDUtils:
    """UUID utilities"""
    
    @staticmethod
    def generate_v4() -> str:
        """Generate UUID v4 (random)"""
        return str(uuid.uuid4())
    
    @staticmethod
    def generate_v1() -> str:
        """Generate UUID v1 (timestamp-based)"""
        return str(uuid.uuid1())
    
    @staticmethod
    def generate_short() -> str:
        """Generate short UUID (8 chars)"""
        return secrets.token_hex(4)
    
    @staticmethod
    def from_string(text: str, namespace: Optional[uuid.UUID] = None) -> str:
        """Generate UUID from string (v5)"""
        if namespace is None:
            namespace = uuid.NAMESPACE_DNS
        return str(uuid.uuid5(namespace, text))
    
    @staticmethod
    def from_name(name: str) -> str:
        """Generate deterministic UUID from name"""
        hash_obj = hashlib.sha256(name.encode())
        return str(uuid.UUID(hash_obj.hexdigest()))
    
    @staticmethod
    def is_valid(uuid_str: str) -> bool:
        """Check if string is valid UUID"""
        try:
            uuid.UUID(uuid_str)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def normalize(uuid_str: str) -> str:
        """Normalize UUID string"""
        return str(uuid.UUID(uuid_str))
    
    @staticmethod
    def to_int(uuid_str: str) -> int:
        """Convert UUID to integer"""
        return uuid.UUID(uuid_str).int
    
    @staticmethod
    def to_bytes(uuid_str: str) -> bytes:
        """Convert UUID to bytes"""
        return uuid.UUID(uuid_str).bytes

class IDGenerator:
    """Various ID generators"""
    
    @staticmethod
    def nanoid(size: int = 21) -> str:
        """Generate nanoID-like string"""
        alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        return ''.join(secrets.choice(alphabet) for _ in range(size))
    
    @staticmethod
    def slugid() -> str:
        """Generate URL-safe slug ID"""
        return secrets.token_urlsafe(12)
    
    @staticmethod
    def sequential(prefix: str = "") -> str:
        """Generate sequential ID"""
        import time
        timestamp = int(time.time() * 1000)
        return f"{prefix}{timestamp}"

# === CONVENIENCE FUNCTIONS ===
def uuid4() -> str:
    """Quick UUID v4"""
    return UUIDUtils.generate_v4()

def short_id() -> str:
    """Quick short ID"""
    return UUIDUtils.generate_short()

def nanoid(size: int = 21) -> str:
    """Quick nanoID"""
    return IDGenerator.nanoid(size)

# === TESTING ===
if __name__ == "__main__":
    print("🔑 BaarliClaw UUID Toolkit - Testing")
    print("=" * 50)
    
    # Test UUID generation
    print("\n🧪 Testing UUID Generation")
    
    v4 = UUIDUtils.generate_v4()
    print(f"  UUID v4: {v4}")
    
    v1 = UUIDUtils.generate_v1()
    print(f"  UUID v1: {v1}")
    
    short = UUIDUtils.generate_short()
    print(f"  Short UUID: {short}")
    
    # Test from string
    print("\n🧪 Testing UUID from String")
    name_uuid = UUIDUtils.from_string("example.com")
    print(f"  From 'example.com': {name_uuid}")
    
    # Test validation
    print("\n🧪 Testing Validation")
    print(f"  Is '{v4}' valid? {UUIDUtils.is_valid(v4)}")
    print(f"  Is 'invalid' valid? {UUIDUtils.is_valid('invalid')}")
    
    # Test ID generators
    print("\n🧪 Testing ID Generators")
    
    nano = IDGenerator.nanoid()
    print(f"  NanoID: {nano}")
    
    slug = IDGenerator.slugid()
    print(f"  SlugID: {slug}")
    
    seq = IDGenerator.sequential("usr_")
    print(f"  Sequential: {seq}")
    
    print("\n✅ UUID Toolkit ready!")
