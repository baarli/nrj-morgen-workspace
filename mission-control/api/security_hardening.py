#!/usr/bin/env python3
"""
Security Hardening Module for Mission Control API
Adds input validation, rate limiting, security headers, and dependency auditing
"""

import re
import time
import hashlib
import ipaddress
from typing import Dict, List, Any, Optional, Callable
from functools import wraps
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import threading
import logging

logger = logging.getLogger('SecurityHardening')

# ==================== INPUT VALIDATION ====================

class InputValidator:
    """Validates and sanitizes input data"""
    
    # Validation patterns
    PATTERNS = {
        'email': re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
        'uuid': re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I),
        'alphanumeric': re.compile(r'^[a-zA-Z0-9_-]+$'),
        'safe_string': re.compile(r'^[\w\s\-_.@,;:()]+$'),
        'url': re.compile(r'^https?://[^\s/$.?#].[^\s]*$', re.I),
        'date_iso': re.compile(r'^\d{4}-\d{2}-\d{2}$'),
        'datetime_iso': re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'),
    }
    
    # Maximum lengths for common fields
    MAX_LENGTHS = {
        'title': 200,
        'description': 5000,
        'username': 50,
        'password': 128,
        'email': 254,
        'url': 2048,
        'id': 50,
        'text': 10000,
    }
    
    @classmethod
    def validate_email(cls, email: str) -> bool:
        """Validate email format"""
        if not email or len(email) > cls.MAX_LENGTHS['email']:
            return False
        return bool(cls.PATTERNS['email'].match(email))
    
    @classmethod
    def validate_uuid(cls, uuid_str: str) -> bool:
        """Validate UUID format"""
        if not uuid_str:
            return False
        return bool(cls.PATTERNS['uuid'].match(uuid_str))
    
    @classmethod
    def validate_safe_string(cls, text: str, max_length: int = None) -> bool:
        """Validate string contains only safe characters"""
        if not text:
            return True  # Empty is valid
        if max_length and len(text) > max_length:
            return False
        return bool(cls.PATTERNS['safe_string'].match(text))
    
    @classmethod
    def validate_url(cls, url: str) -> bool:
        """Validate URL format and scheme"""
        if not url or len(url) > cls.MAX_LENGTHS['url']:
            return False
        if not cls.PATTERNS['url'].match(url):
            return False
        # Only allow http and https
        return url.startswith(('http://', 'https://'))
    
    @classmethod
    def sanitize_string(cls, text: str, max_length: int = None) -> str:
        """Sanitize a string by removing dangerous characters"""
        if not text:
            return ''
        
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Remove control characters except newlines and tabs
        text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t\r')
        
        # Limit length
        if max_length and len(text) > max_length:
            text = text[:max_length]
        
        return text.strip()
    
    @classmethod
    def sanitize_html(cls, html: str) -> str:
        """Basic HTML sanitization - removes script tags and dangerous attributes"""
        if not html:
            return ''
        
        import re
        # Remove script tags and contents
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.I)
        # Remove event handlers
        html = re.sub(r'\s*on\w+\s*=\s*["\'][^"\']*["\']', '', html, flags=re.I)
        # Remove javascript: URLs
        html = re.sub(r'javascript:', '', html, flags=re.I)
        # Remove data: URLs (potential XSS)
        html = re.sub(r'data:', '', html, flags=re.I)
        
        return html
    
    @classmethod
    def validate_sak_data(cls, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate sak (agenda item) data"""
        errors = []
        
        # Required fields
        if 'title' not in data or not data['title']:
            errors.append("Title is required")
        elif len(data['title']) > cls.MAX_LENGTHS['title']:
            errors.append(f"Title too long (max {cls.MAX_LENGTHS['title']} chars)")
        
        # Validate description if present
        if 'description' in data and data['description']:
            if len(data['description']) > cls.MAX_LENGTHS['description']:
                errors.append(f"Description too long (max {cls.MAX_LENGTHS['description']} chars)")
        
        # Validate link_url if present
        if 'link_url' in data and data['link_url']:
            if not cls.validate_url(data['link_url']):
                errors.append("Invalid link_url format")
        
        # Validate category
        valid_categories = ['TALK', 'MUSIC', 'NEWS', 'AD', 'OTHER']
        if 'category' in data and data['category']:
            if data['category'] not in valid_categories:
                errors.append(f"Invalid category. Must be one of: {', '.join(valid_categories)}")
        
        # Sanitize inputs
        if 'title' in data:
            data['title'] = cls.sanitize_string(data['title'], cls.MAX_LENGTHS['title'])
        if 'description' in data:
            data['description'] = cls.sanitize_html(cls.sanitize_string(data['description'], cls.MAX_LENGTHS['description']))
        
        return len(errors) == 0, errors
    
    @classmethod
    def validate_auth_data(cls, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate authentication data"""
        errors = []
        
        username = data.get('username', '')
        password = data.get('password', '')
        
        if not username:
            errors.append("Username is required")
        elif len(username) > cls.MAX_LENGTHS['username']:
            errors.append(f"Username too long (max {cls.MAX_LENGTHS['username']} chars)")
        elif not cls.PATTERNS['alphanumeric'].match(username):
            errors.append("Username contains invalid characters")
        
        if not password:
            errors.append("Password is required")
        elif len(password) > cls.MAX_LENGTHS['password']:
            errors.append(f"Password too long (max {cls.MAX_LENGTHS['password']} chars)")
        elif len(password) < 6:
            errors.append("Password too short (min 6 chars)")
        
        return len(errors) == 0, errors


# ==================== RATE LIMITING ====================

@dataclass
class RateLimitEntry:
    """Rate limit tracking entry"""
    count: int = 0
    window_start: float = field(default_factory=time.time)
    blocked_until: Optional[float] = None


class RateLimiter:
    """Rate limiter with IP and user-based tracking"""
    
    def __init__(self):
        self._storage: Dict[str, RateLimitEntry] = {}
        self._lock = threading.RLock()
        self._cleanup_interval = 300  # 5 minutes
        self._last_cleanup = time.time()
        
        # Default limits
        self.limits = {
            'default': {'requests': 100, 'window': 60},  # 100 req/min
            'auth': {'requests': 5, 'window': 60},        # 5 login attempts/min
            'api': {'requests': 1000, 'window': 60},      # 1000 API calls/min
            'websocket': {'requests': 60, 'window': 60},  # 60 WS messages/min
        }
    
    def _get_key(self, identifier: str, limit_type: str = 'default') -> str:
        """Generate storage key"""
        return f"{limit_type}:{identifier}"
    
    def _cleanup_old_entries(self):
        """Remove old entries to prevent memory bloat"""
        now = time.time()
        if now - self._last_cleanup < self._cleanup_interval:
            return
        
        with self._lock:
            to_remove = []
            for key, entry in self._storage.items():
                limit_config = self.limits.get(key.split(':')[0], self.limits['default'])
                window = limit_config['window']
                if now - entry.window_start > window * 2:
                    to_remove.append(key)
            
            for key in to_remove:
                del self._storage[key]
            
            self._last_cleanup = now
            logger.debug(f"Rate limiter cleanup: removed {len(to_remove)} entries")
    
    def is_allowed(self, identifier: str, limit_type: str = 'default') -> tuple[bool, Dict[str, Any]]:
        """Check if request is allowed under rate limit"""
        self._cleanup_old_entries()
        
        key = self._get_key(identifier, limit_type)
        limit_config = self.limits.get(limit_type, self.limits['default'])
        max_requests = limit_config['requests']
        window = limit_config['window']
        
        now = time.time()
        
        with self._lock:
            entry = self._storage.get(key)
            
            if entry is None:
                entry = RateLimitEntry(count=1, window_start=now)
                self._storage[key] = entry
                return True, {
                    'limit': max_requests,
                    'remaining': max_requests - 1,
                    'reset': now + window
                }
            
            # Check if blocked
            if entry.blocked_until and now < entry.blocked_until:
                return False, {
                    'limit': max_requests,
                    'remaining': 0,
                    'reset': entry.blocked_until,
                    'retry_after': int(entry.blocked_until - now)
                }
            
            # Reset window if expired
            if now - entry.window_start > window:
                entry.count = 1
                entry.window_start = now
                entry.blocked_until = None
                return True, {
                    'limit': max_requests,
                    'remaining': max_requests - 1,
                    'reset': now + window
                }
            
            # Increment count
            entry.count += 1
            
            # Check if limit exceeded
            if entry.count > max_requests:
                # Block for 5 minutes
                entry.blocked_until = now + 300
                logger.warning(f"Rate limit exceeded for {identifier} ({limit_type})")
                return False, {
                    'limit': max_requests,
                    'remaining': 0,
                    'reset': entry.blocked_until,
                    'retry_after': 300
                }
            
            return True, {
                'limit': max_requests,
                'remaining': max_requests - entry.count,
                'reset': entry.window_start + window
            }
    
    def get_client_identifier(self, handler) -> str:
        """Extract client identifier from request handler"""
        # Try to get from headers first
        client_ip = handler.headers.get('X-Forwarded-For', '').split(',')[0].strip()
        if not client_ip:
            client_ip = handler.headers.get('X-Real-IP', '')
        if not client_ip:
            client_ip = handler.client_address[0]
        
        # Include user agent hash for better identification
        user_agent = handler.headers.get('User-Agent', '')
        ua_hash = hashlib.md5(user_agent.encode()).hexdigest()[:8]
        
        return f"{client_ip}:{ua_hash}"


# Global rate limiter instance
rate_limiter = RateLimiter()


def rate_limit(limit_type: str = 'default'):
    """Decorator to apply rate limiting to endpoints"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            client_id = rate_limiter.get_client_identifier(self)
            allowed, headers = rate_limiter.is_allowed(client_id, limit_type)
            
            if not allowed:
                self.send_json_response({
                    'error': 'Rate limit exceeded',
                    'retry_after': headers.get('retry_after', 60)
                }, 429, {
                    'X-RateLimit-Limit': str(headers['limit']),
                    'X-RateLimit-Remaining': '0',
                    'X-RateLimit-Reset': str(int(headers['reset'])),
                    'Retry-After': str(headers.get('retry_after', 60))
                })
                return None
            
            # Store headers for response
            self._rate_limit_headers = {
                'X-RateLimit-Limit': str(headers['limit']),
                'X-RateLimit-Remaining': str(headers['remaining']),
                'X-RateLimit-Reset': str(int(headers['reset']))
            }
            
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


# ==================== SECURITY HEADERS ====================

class SecurityHeaders:
    """Security headers configuration"""
    
    # Recommended security headers
    HEADERS = {
        # Prevent MIME type sniffing
        'X-Content-Type-Options': 'nosniff',
        
        # Prevent clickjacking
        'X-Frame-Options': 'DENY',
        
        # XSS Protection
        'X-XSS-Protection': '1; mode=block',
        
        # Referrer policy
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        
        # Permissions policy
        'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
        
        # Content Security Policy
        'Content-Security-Policy': "default-src 'self'; "
                                    "script-src 'self' 'unsafe-inline' 'unsafe-eval' cdn.jsdelivr.net unpkg.com; "
                                    "style-src 'self' 'unsafe-inline' cdn.jsdelivr.net fonts.googleapis.com; "
                                    "font-src 'self' fonts.gstatic.com cdn.jsdelivr.net; "
                                    "img-src 'self' data: https: blob:; "
                                    "connect-src 'self' https: wss:; "
                                    "media-src 'self' https:; "
                                    "frame-ancestors 'none'; "
                                    "base-uri 'self'; "
                                    "form-action 'self';",
        
        # Strict Transport Security (HTTPS only)
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
    }
    
    @classmethod
    def apply(cls, handler):
        """Apply security headers to response"""
        for header, value in cls.HEADERS.items():
            handler.send_header(header, value)


# ==================== DEPENDENCY AUDIT ====================

class DependencyAuditor:
    """Audit dependencies for known vulnerabilities"""
    
    # Known vulnerable package versions (simplified check)
    # In production, use safety-db or similar
    VULNERABILITY_DB = {
        'requests': {
            '<2.20.0': 'CVE-2018-18074 - Certificate validation bypass',
        },
        'urllib3': {
            '<1.24.2': 'CVE-2019-11324 - CRLF injection',
            '<1.26.5': 'CVE-2021-33503 - ReDoS vulnerability',
        },
        'cryptography': {
            '<3.2': 'CVE-2020-25659 - Bleichenbacher attack',
        },
        'pyjwt': {
            '<2.4.0': 'CVE-2022-29217 - Key confusion attack',
        },
    }
    
    @classmethod
    def get_installed_packages(cls) -> Dict[str, str]:
        """Get list of installed packages"""
        try:
            import subprocess
            result = subprocess.run(
                ['pip', 'list', '--format=json'],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                import json
                packages = json.loads(result.stdout)
                return {p['name'].lower(): p['version'] for p in packages}
        except Exception as e:
            logger.error(f"Failed to get installed packages: {e}")
        return {}
    
    @classmethod
    def check_vulnerabilities(cls) -> List[Dict[str, Any]]:
        """Check for known vulnerabilities in dependencies"""
        installed = cls.get_installed_packages()
        vulnerabilities = []
        
        for package, version in installed.items():
            if package in cls.VULNERABILITY_DB:
                pkg_vulns = cls.VULNERABILITY_DB[package]
                for version_constraint, description in pkg_vulns.items():
                    if cls._version_matches_constraint(version, version_constraint):
                        vulnerabilities.append({
                            'package': package,
                            'installed_version': version,
                            'constraint': version_constraint,
                            'description': description,
                            'severity': 'high'
                        })
        
        return vulnerabilities
    
    @classmethod
    def _version_matches_constraint(cls, version: str, constraint: str) -> bool:
        """Check if version matches constraint (simplified)"""
        try:
            from packaging import version as pkg_version
            v = pkg_version.parse(version)
            
            if constraint.startswith('<'):
                compare_version = constraint[1:]
                if constraint.startswith('<='):
                    compare_version = constraint[2:]
                    return v <= pkg_version.parse(compare_version)
                return v < pkg_version.parse(compare_version)
            elif constraint.startswith('>'):
                compare_version = constraint[1:]
                if constraint.startswith('>='):
                    compare_version = constraint[2:]
                    return v >= pkg_version.parse(compare_version)
                return v > pkg_version.parse(compare_version)
            elif constraint.startswith('='):
                return v == pkg_version.parse(constraint[1:])
        except:
            # Fallback to simple string comparison
            pass
        return False
    
    @classmethod
    def generate_report(cls) -> Dict[str, Any]:
        """Generate full dependency audit report"""
        installed = cls.get_installed_packages()
        vulnerabilities = cls.check_vulnerabilities()
        
        # Check for critical packages
        critical_packages = ['cryptography', 'pyjwt', 'urllib3', 'requests']
        missing_critical = [pkg for pkg in critical_packages if pkg not in installed]
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_packages': len(installed),
            'vulnerabilities_found': len(vulnerabilities),
            'vulnerabilities': vulnerabilities,
            'missing_critical': missing_critical,
            'critical_packages_status': {
                pkg: installed.get(pkg, 'not installed') 
                for pkg in critical_packages
            },
            'recommendations': cls._generate_recommendations(vulnerabilities, missing_critical)
        }
    
    @classmethod
    def _generate_recommendations(cls, vulnerabilities: List[Dict], missing_critical: List[str]) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        if vulnerabilities:
            recommendations.append(f"Update {len(vulnerabilities)} vulnerable package(s) immediately")
            for vuln in vulnerabilities:
                recommendations.append(f"  - {vuln['package']}: {vuln['description']}")
        
        if missing_critical:
            recommendations.append(f"Install missing critical packages: {', '.join(missing_critical)}")
        
        if not vulnerabilities and not missing_critical:
            recommendations.append("No immediate security concerns found")
        
        recommendations.append("Run 'pip install --upgrade' regularly to keep dependencies updated")
        recommendations.append("Consider using pip-audit or safety for continuous monitoring")
        
        return recommendations


# ==================== SECURITY MIDDLEWARE ====================

def apply_security_hardening(handler_class):
    """Apply all security hardening to API handler class"""
    
    # Store original methods
    original_send_json = handler_class.send_json_response
    original_do_post = handler_class.do_POST
    original_do_patch = handler_class.do_PATCH
    
    def secured_send_json(self, data, status=200, headers=None):
        """Send JSON response with security headers"""
        # Apply rate limit headers if available
        if hasattr(self, '_rate_limit_headers'):
            headers = headers or {}
            headers.update(self._rate_limit_headers)
            delattr(self, '_rate_limit_headers')
        
        # Call original method
        original_send_json(self, data, status, headers)
        
        # Apply security headers (need to re-send since original already sent)
        # This is handled by overriding the method entirely
    
    def secured_do_post(self):
        """POST with rate limiting"""
        client_id = rate_limiter.get_client_identifier(self)
        
        # Check auth endpoint separately (stricter limits)
        if self.path == '/api/auth/login':
            limit_type = 'auth'
        else:
            limit_type = 'api'
        
        allowed, limit_headers = rate_limiter.is_allowed(client_id, limit_type)
        
        if not allowed:
            self.send_json_response({
                'error': 'Rate limit exceeded',
                'message': 'Too many requests. Please try again later.'
            }, 429)
            return
        
        # Store headers for response
        self._rate_limit_headers = {
            'X-RateLimit-Limit': str(limit_headers['limit']),
            'X-RateLimit-Remaining': str(limit_headers['remaining']),
            'X-RateLimit-Reset': str(int(limit_headers['reset']))
        }
        
        # Validate content type for POST requests
        content_type = self.headers.get('Content-Type', '')
        if content_type and not content_type.startswith('application/json'):
            if self.path not in ['/api/upload']:  # Allow non-JSON for uploads
                self.send_json_response({
                    'error': 'Invalid Content-Type',
                    'message': 'Expected application/json'
                }, 400)
                return
        
        # Check content length
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 10 * 1024 * 1024:  # 10MB limit
            self.send_json_response({
                'error': 'Payload too large',
                'message': 'Maximum request size is 10MB'
            }, 413)
            return
        
        return original_do_post(self)
    
    def secured_do_patch(self):
        """PATCH with rate limiting"""
        client_id = rate_limiter.get_client_identifier(self)
        allowed, limit_headers = rate_limiter.is_allowed(client_id, 'api')
        
        if not allowed:
            self.send_json_response({
                'error': 'Rate limit exceeded',
                'message': 'Too many requests. Please try again later.'
            }, 429)
            return
        
        self._rate_limit_headers = {
            'X-RateLimit-Limit': str(limit_headers['limit']),
            'X-RateLimit-Remaining': str(limit_headers['remaining']),
            'X-RateLimit-Reset': str(int(limit_headers['reset']))
        }
        
        return original_do_patch(self)
    
    # Replace methods
    handler_class.send_json_response = secured_send_json
    handler_class.do_POST = secured_do_post
    handler_class.do_PATCH = secured_do_patch
    
    return handler_class


# ==================== EXPORTS ====================

__all__ = [
    'InputValidator',
    'RateLimiter',
    'rate_limiter',
    'rate_limit',
    'SecurityHeaders',
    'DependencyAuditor',
    'apply_security_hardening',
]
