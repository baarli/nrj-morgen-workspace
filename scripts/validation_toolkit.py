#!/usr/bin/env python3
"""
📊 BAARLICLAW VALIDATION TOOLKIT
Datavalidering og -rensing
"""

import re
from typing import Any, Optional, List, Dict, Callable, Union
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ValidationResult:
    """Validation result"""
    valid: bool
    errors: List[str]
    warnings: List[str]
    cleaned_value: Any = None

class Validator:
    """Data validator"""
    
    @staticmethod
    def email(value: str) -> ValidationResult:
        """Validate email address"""
        errors = []
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not value:
            errors.append("Email is required")
        elif not re.match(pattern, value):
            errors.append("Invalid email format")
        elif len(value) > 254:
            errors.append("Email too long")
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=[],
            cleaned_value=value.lower().strip() if not errors else None
        )
    
    @staticmethod
    def url(value: str, require_https: bool = False) -> ValidationResult:
        """Validate URL"""
        errors = []
        
        if not value:
            errors.append("URL is required")
        else:
            if require_https and not value.startswith('https://'):
                errors.append("HTTPS required")
            elif not value.startswith(('http://', 'https://')):
                errors.append("Must start with http:// or https://")
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=[],
            cleaned_value=value.strip() if not errors else None
        )
    
    @staticmethod
    def phone(value: str, country: str = "NO") -> ValidationResult:
        """Validate phone number"""
        errors = []
        
        # Remove all non-digits
        digits = re.sub(r'\D', '', value)
        
        if country == "NO":
            # Norwegian: 8 digits
            if len(digits) == 8:
                cleaned = f"+47 {digits[:2]} {digits[2:5]} {digits[5:]}"
            elif len(digits) == 10 and digits.startswith('47'):
                cleaned = f"+{digits[:2]} {digits[2:4]} {digits[4:7]} {digits[7:]}"
            else:
                errors.append("Invalid Norwegian phone number")
                cleaned = None
        else:
            cleaned = digits if len(digits) >= 7 else None
            if not cleaned:
                errors.append("Phone number too short")
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=[],
            cleaned_value=cleaned
        )
    
    @staticmethod
    def number(value: Any, min_val: Optional[float] = None, 
               max_val: Optional[float] = None) -> ValidationResult:
        """Validate number"""
        errors = []
        
        try:
            num = float(value)
            
            if min_val is not None and num < min_val:
                errors.append(f"Must be at least {min_val}")
            
            if max_val is not None and num > max_val:
                errors.append(f"Must be at most {max_val}")
                
        except (ValueError, TypeError):
            errors.append("Must be a number")
            num = None
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=[],
            cleaned_value=num
        )
    
    @staticmethod
    def text(value: str, min_length: int = 0, 
             max_length: Optional[int] = None,
             allow_empty: bool = False) -> ValidationResult:
        """Validate text"""
        errors = []
        warnings = []
        
        if not value and not allow_empty:
            errors.append("Text is required")
        else:
            if len(value) < min_length:
                errors.append(f"Must be at least {min_length} characters")
            
            if max_length and len(value) > max_length:
                errors.append(f"Must be at most {max_length} characters")
            
            # Check for suspicious patterns
            if '<script' in value.lower():
                warnings.append("Contains potential script tag")
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            cleaned_value=value.strip() if not errors else None
        )
    
    @staticmethod
    def date(value: str, format: str = "%Y-%m-%d") -> ValidationResult:
        """Validate date"""
        errors = []
        
        try:
            parsed = datetime.strptime(value, format)
        except ValueError:
            errors.append(f"Invalid date format. Expected: {format}")
            parsed = None
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=[],
            cleaned_value=parsed
        )

class DataCleaner:
    """Clean and normalize data"""
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Normalize whitespace"""
        return ' '.join(text.split())
    
    @staticmethod
    def remove_special_chars(text: str, keep: str = "") -> str:
        """Remove special characters"""
        allowed = set(keep)
        return ''.join(c for c in text if c.isalnum() or c in allowed or c.isspace())
    
    @staticmethod
    def normalize_phone(phone: str) -> str:
        """Normalize phone number"""
        digits = re.sub(r'\D', '', phone)
        return digits
    
    @staticmethod
    def slugify(text: str) -> str:
        """Convert to URL-friendly slug"""
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text.strip('-')
    
    @staticmethod
    def truncate(text: str, length: int = 100, suffix: str = "...") -> str:
        """Truncate text"""
        if len(text) <= length:
            return text
        return text[:length - len(suffix)] + suffix

# === CONVENIENCE FUNCTIONS ===
def is_email(value: str) -> bool:
    """Quick email check"""
    return Validator.email(value).valid

def is_url(value: str) -> bool:
    """Quick URL check"""
    return Validator.url(value).valid

def clean_text(text: str) -> str:
    """Quick text cleaning"""
    return DataCleaner.normalize_whitespace(text)

# === TESTING ===
if __name__ == "__main__":
    print("📊 BaarliClaw Validation Toolkit - Testing")
    print("=" * 50)
    
    # Test email validation
    print("\n🧪 Testing Email Validation")
    emails = ["test@example.com", "invalid", "", "UPPER@EMAIL.COM"]
    for email in emails:
        result = Validator.email(email)
        status = "✅" if result.valid else "❌"
        print(f"  {status} {email}: {result.errors if result.errors else 'OK'}")
    
    # Test phone validation
    print("\n🧪 Testing Phone Validation")
    phones = ["12345678", "+47 123 45 678", "123", "004712345678"]
    for phone in phones:
        result = Validator.phone(phone)
        status = "✅" if result.valid else "❌"
        cleaned = result.cleaned_value if result.valid else "N/A"
        print(f"  {status} {phone} -> {cleaned}")
    
    # Test number validation
    print("\n🧪 Testing Number Validation")
    result = Validator.number(50, min_val=0, max_val=100)
    print(f"  ✅ 50 (0-100): {result.valid}")
    
    result = Validator.number(150, min_val=0, max_val=100)
    print(f"  ❌ 150 (0-100): {result.errors}")
    
    # Test data cleaning
    print("\n🧪 Testing Data Cleaning")
    dirty = "  Hello   World  "
    clean = DataCleaner.normalize_whitespace(dirty)
    print(f"  '{dirty}' -> '{clean}'")
    
    text = "Hello World! @#$"
    clean = DataCleaner.remove_special_chars(text, keep="!")
    print(f"  '{text}' -> '{clean}'")
    
    print("\n✅ Validation Toolkit ready!")
