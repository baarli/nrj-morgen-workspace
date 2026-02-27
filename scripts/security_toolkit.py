#!/usr/bin/env python3
"""
🔒 BAARLICLAW SECURITY TOOLKIT
Sikkerhetsverktøy og -håndtering
"""

import os
import sys
import hashlib
import secrets
import string
import re
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("SecurityToolkit")

class PasswordManager:
    """Password generation and validation"""
    
    @staticmethod
    def generate(length: int = 16, 
                 include_upper: bool = True,
                 include_lower: bool = True,
                 include_digits: bool = True,
                 include_special: bool = True) -> str:
        """Generate secure password"""
        chars = ""
        if include_lower:
            chars += string.ascii_lowercase
        if include_upper:
            chars += string.ascii_uppercase
        if include_digits:
            chars += string.digits
        if include_special:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if not chars:
            raise ValueError("At least one character type must be included")
        
        # Ensure at least one of each required type
        password = []
        if include_lower:
            password.append(secrets.choice(string.ascii_lowercase))
        if include_upper:
            password.append(secrets.choice(string.ascii_uppercase))
        if include_digits:
            password.append(secrets.choice(string.digits))
        if include_special:
            password.append(secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
        
        # Fill remaining length
        for _ in range(length - len(password)):
            password.append(secrets.choice(chars))
        
        # Shuffle
        secrets.SystemRandom().shuffle(password)
        return ''.join(password)
    
    @staticmethod
    def check_strength(password: str) -> Dict:
        """Check password strength"""
        score = 0
        feedback = []
        
        # Length
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("Too short (min 8 characters)")
        
        # Character types
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))
        
        if has_lower:
            score += 1
        else:
            feedback.append("Add lowercase letters")
        
        if has_upper:
            score += 1
        else:
            feedback.append("Add uppercase letters")
        
        if has_digit:
            score += 1
        else:
            feedback.append("Add numbers")
        
        if has_special:
            score += 1
        else:
            feedback.append("Add special characters")
        
        # Determine strength
        if score >= 6:
            strength = "strong"
        elif score >= 4:
            strength = "medium"
        else:
            strength = "weak"
        
        return {
            "score": score,
            "max_score": 7,
            "strength": strength,
            "feedback": feedback,
            "length": len(password)
        }
    
    @staticmethod
    def hash_password(password: str, salt: Optional[bytes] = None) -> Tuple[bytes, bytes]:
        """Hash password with salt"""
        if salt is None:
            salt = secrets.token_bytes(32)
        
        # Use PBKDF2
        import hashlib
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000  # iterations
        )
        
        return key, salt
    
    @staticmethod
    def verify_password(password: str, key: bytes, salt: bytes) -> bool:
        """Verify password against hash"""
        new_key, _ = PasswordManager.hash_password(password, salt)
        return secrets.compare_digest(key, new_key)

class TokenManager:
    """Generate and validate tokens"""
    
    @staticmethod
    def generate(length: int = 32) -> str:
        """Generate secure random token"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_api_key(prefix: str = "baarli") -> str:
        """Generate API key"""
        key = secrets.token_urlsafe(32)
        return f"{prefix}_{key}"
    
    @staticmethod
    def generate_otp(length: int = 6) -> str:
        """Generate one-time password"""
        return ''.join(secrets.choice(string.digits) for _ in range(length))

class Encryption:
    """Simple encryption utilities"""
    
    @staticmethod
    def xor_encrypt(data: str, key: str) -> str:
        """Simple XOR encryption (not for production!)"""
        encrypted = []
        for i, char in enumerate(data):
            key_char = key[i % len(key)]
            encrypted.append(chr(ord(char) ^ ord(key_char)))
        return ''.join(encrypted)
    
    @staticmethod
    def xor_decrypt(encrypted: str, key: str) -> str:
        """Decrypt XOR encrypted data"""
        return Encryption.xor_encrypt(encrypted, key)  # XOR is symmetric
    
    @staticmethod
    def caesar_cipher(text: str, shift: int) -> str:
        """Caesar cipher (for educational purposes)"""
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result.append(chr((ord(char) - base + shift) % 26 + base))
            else:
                result.append(char)
        return ''.join(result)

class InputValidator:
    """Validate and sanitize input"""
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """Remove HTML tags"""
        import re
        return re.sub(r'<[^>]+>', '', text)
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url))
    
    @staticmethod
    def escape_sql(value: str) -> str:
        """Basic SQL escaping"""
        return value.replace("'", "''").replace(";", "")
    
    @staticmethod
    def is_safe_filename(filename: str) -> bool:
        """Check if filename is safe"""
        dangerous = ['..', '/', '\\', '\x00']
        return not any(d in filename for d in dangerous)

class SecurityScanner:
    """Scan for security issues"""
    
    DANGEROUS_PATTERNS = [
        (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password"),
        (r'api_key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key"),
        (r'secret\s*=\s*["\'][^"\']+["\']', "Hardcoded secret"),
        (r'eval\s*\(', "Use of eval()"),
        (r'exec\s*\(', "Use of exec()"),
        (r'subprocess\.call\s*\([^)]*shell\s*=\s*True', "Shell=True in subprocess"),
    ]
    
    def scan_file(self, filepath: str) -> List[Dict]:
        """Scan a file for security issues"""
        issues = []
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for pattern, description in self.DANGEROUS_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append({
                            'file': filepath,
                            'line': line_num,
                            'issue': description,
                            'content': line.strip()[:100]
                        })
        
        except Exception as e:
            logger.error(f"Failed to scan {filepath}: {e}")
        
        return issues
    
    def scan_directory(self, path: str, extensions: List[str] = None) -> List[Dict]:
        """Scan directory for security issues"""
        extensions = extensions or ['.py', '.js', '.sh']
        all_issues = []
        
        for root, dirs, files in os.walk(path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    filepath = os.path.join(root, file)
                    issues = self.scan_file(filepath)
                    all_issues.extend(issues)
        
        return all_issues

# === CONVENIENCE FUNCTIONS ===
def quick_password(length: int = 16) -> str:
    """Generate a quick password"""
    return PasswordManager.generate(length)

def check_password(password: str) -> str:
    """Quick password strength check"""
    result = PasswordManager.check_strength(password)
    return f"Strength: {result['strength']} ({result['score']}/{result['max_score']})"

def generate_token() -> str:
    """Generate a quick token"""
    return TokenManager.generate()

def scan_security(path: str = ".") -> List[Dict]:
    """Quick security scan"""
    scanner = SecurityScanner()
    return scanner.scan_directory(path)

# === TESTING ===
if __name__ == "__main__":
    print("🔒 BaarliClaw Security Toolkit - Testing")
    print("=" * 50)
    
    # Test password generation
    print("\n🧪 Testing password generation")
    pwd = PasswordManager.generate()
    print(f"✅ Generated: {pwd[:8]}...")
    
    # Test password strength
    print("\n🧪 Testing password strength")
    test_passwords = ["123", "password123", "MyStr0ng!P@ss"]
    for pwd in test_passwords:
        result = PasswordManager.check_strength(pwd)
        print(f"  '{pwd[:10]}...' -> {result['strength']}")
    
    # Test token generation
    print("\n🧪 Testing token generation")
    token = TokenManager.generate()
    api_key = TokenManager.generate_api_key()
    otp = TokenManager.generate_otp()
    print(f"✅ Token: {token[:20]}...")
    print(f"✅ API Key: {api_key[:25]}...")
    print(f"✅ OTP: {otp}")
    
    # Test encryption
    print("\n🧪 Testing encryption")
    message = "Hello, World!"
    key = "secret"
    encrypted = Encryption.xor_encrypt(message, key)
    decrypted = Encryption.xor_decrypt(encrypted, key)
    print(f"  Original: {message}")
    print(f"  Encrypted: {encrypted[:20]}...")
    print(f"  Decrypted: {decrypted}")
    
    # Test validation
    print("\n🧪 Testing input validation")
    print(f"  Email 'test@example.com': {InputValidator.validate_email('test@example.com')}")
    print(f"  URL 'https://google.com': {InputValidator.validate_url('https://google.com')}")
    print(f"  Sanitize '<b>hello</b>': {InputValidator.sanitize_html('<b>hello</b>')}")
    
    print("\n✅ Security Toolkit ready!")
    print("\n⚠️  Remember: XOR encryption is for educational purposes only!")
    print("   Use proper encryption libraries for production.")
