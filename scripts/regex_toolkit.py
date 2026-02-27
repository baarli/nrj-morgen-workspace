#!/usr/bin/env python3
"""
🔍 BAARLICLAW REGEX TOOLKIT
Regulære uttrykk-verktøy
"""

import re
from typing import List, Optional, Pattern, Match

class RegexUtils:
    """Regex utilities"""
    
    COMMON_PATTERNS = {
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'url': r'^https?://[^\s/$.?#].[^\s]*$',
        'phone': r'^\+?[\d\s\-\(\)]{7,}$',
        'ipv4': r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
        'credit_card': r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})$',
        'hex_color': r'^#(?:[0-9a-fA-F]{3}){1,2}$',
        'date_iso': r'^\d{4}-\d{2}-\d{2}$',
        'time_24h': r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$',
    }
    
    @staticmethod
    def is_match(pattern: str, text: str) -> bool:
        """Check if text matches pattern"""
        return bool(re.match(pattern, text))
    
    @staticmethod
    def find_all(pattern: str, text: str) -> List[str]:
        """Find all matches"""
        return re.findall(pattern, text)
    
    @staticmethod
    def find_first(pattern: str, text: str) -> Optional[str]:
        """Find first match"""
        match = re.search(pattern, text)
        return match.group(0) if match else None
    
    @staticmethod
    def replace(pattern: str, text: str, replacement: str) -> str:
        """Replace all matches"""
        return re.sub(pattern, replacement, text)
    
    @staticmethod
    def replace_first(pattern: str, text: str, replacement: str) -> str:
        """Replace first match only"""
        return re.sub(pattern, replacement, text, count=1)
    
    @staticmethod
    def split(pattern: str, text: str) -> List[str]:
        """Split by pattern"""
        return re.split(pattern, text)
    
    @staticmethod
    def extract_groups(pattern: str, text: str) -> Optional[tuple]:
        """Extract groups from match"""
        match = re.search(pattern, text)
        return match.groups() if match else None
    
    @staticmethod
    def check_pattern(pattern_name: str, text: str) -> bool:
        """Check against common pattern"""
        pattern = RegexUtils.COMMON_PATTERNS.get(pattern_name)
        if not pattern:
            raise ValueError(f"Unknown pattern: {pattern_name}")
        return RegexUtils.is_match(pattern, text)

# === CONVENIENCE FUNCTIONS ===
def matches(pattern: str, text: str) -> bool:
    """Quick match check"""
    return RegexUtils.is_match(pattern, text)

def extract(pattern: str, text: str) -> List[str]:
    """Quick extract"""
    return RegexUtils.find_all(pattern, text)

def sub(pattern: str, text: str, replacement: str) -> str:
    """Quick replace"""
    return RegexUtils.replace(pattern, text, replacement)

# === TESTING ===
if __name__ == "__main__":
    print("🔍 BaarliClaw Regex Toolkit - Testing")
    print("=" * 50)
    
    # Test common patterns
    print("\n🧪 Testing Common Patterns")
    
    tests = [
        ('email', 'test@example.com', True),
        ('email', 'invalid', False),
        ('url', 'https://google.com', True),
        ('hex_color', '#FF5733', True),
        ('date_iso', '2026-02-27', True),
    ]
    
    for pattern_name, text, expected in tests:
        result = RegexUtils.check_pattern(pattern_name, text)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {pattern_name}: '{text}' -> {result}")
    
    # Test extraction
    print("\n🧪 Testing Extraction")
    
    text = "Contact: john@email.com or jane@email.com"
    emails = RegexUtils.find_all(r'[\w\.-]+@[\w\.-]+', text)
    print(f"  Emails from '{text}': {emails}")
    
    # Test replacement
    print("\n🧪 Testing Replacement")
    
    text = "Hello World! Hello Universe!"
    replaced = RegexUtils.replace(r'Hello', text, 'Hi')
    print(f"  Replace 'Hello' with 'Hi': {replaced}")
    
    print("\n✅ Regex Toolkit ready!")
