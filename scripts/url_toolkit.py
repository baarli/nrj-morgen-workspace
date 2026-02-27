#!/usr/bin/env python3
"""
🌐 BAARLICLAW URL TOOLKIT
URL-håndtering og -parsing
"""

from urllib.parse import urlparse, urlencode, parse_qs, urljoin, quote, unquote
from typing import Dict, Optional, List

class URLUtils:
    """URL utilities"""
    
    @staticmethod
    def parse(url: str) -> Dict:
        """Parse URL into components"""
        parsed = urlparse(url)
        return {
            'scheme': parsed.scheme,
            'netloc': parsed.netloc,
            'path': parsed.path,
            'params': parsed.params,
            'query': parsed.query,
            'fragment': parsed.fragment,
            'username': parsed.username,
            'password': parsed.password,
            'hostname': parsed.hostname,
            'port': parsed.port
        }
    
    @staticmethod
    def build_query(params: Dict) -> str:
        """Build query string from dict"""
        return urlencode(params)
    
    @staticmethod
    def parse_query(query: str) -> Dict[str, List[str]]:
        """Parse query string to dict"""
        return parse_qs(query)
    
    @staticmethod
    def join(base: str, url: str) -> str:
        """Join base URL with relative URL"""
        return urljoin(base, url)
    
    @staticmethod
    def encode(text: str) -> str:
        """URL encode text"""
        return quote(text)
    
    @staticmethod
    def decode(text: str) -> str:
        """URL decode text"""
        return unquote(text)
    
    @staticmethod
    def is_absolute(url: str) -> bool:
        """Check if URL is absolute"""
        return bool(urlparse(url).netloc)
    
    @staticmethod
    def get_domain(url: str) -> str:
        """Extract domain from URL"""
        return urlparse(url).netloc
    
    @staticmethod
    def add_params(url: str, params: Dict) -> str:
        """Add query parameters to URL"""
        parsed = urlparse(url)
        existing = parse_qs(parsed.query)
        existing.update({k: [v] for k, v in params.items()})
        new_query = urlencode(existing, doseq=True)
        return parsed._replace(query=new_query).geturl()

# === CONVENIENCE FUNCTIONS ===
def parse_url(url: str) -> Dict:
    """Quick URL parse"""
    return URLUtils.parse(url)

def encode_url(text: str) -> str:
    """Quick URL encode"""
    return URLUtils.encode(text)

def decode_url(text: str) -> str:
    """Quick URL decode"""
    return URLUtils.decode(text)

# === TESTING ===
if __name__ == "__main__":
    print("🌐 BaarliClaw URL Toolkit - Testing")
    print("=" * 50)
    
    # Test parsing
    print("\n🧪 Testing URL Parsing")
    url = "https://user:pass@example.com:8080/path?key=value#fragment"
    parsed = URLUtils.parse(url)
    print(f"  Scheme: {parsed['scheme']}")
    print(f"  Host: {parsed['hostname']}")
    print(f"  Port: {parsed['port']}")
    print(f"  Path: {parsed['path']}")
    
    # Test query building
    print("\n🧪 Testing Query Building")
    params = {'name': 'John Doe', 'age': '30'}
    query = URLUtils.build_query(params)
    print(f"  Params: {params}")
    print(f"  Query: {query}")
    
    # Test encoding
    print("\n🧪 Testing Encoding")
    text = "Hello World! @#$"
    encoded = URLUtils.encode(text)
    decoded = URLUtils.decode(encoded)
    print(f"  Original: {text}")
    print(f"  Encoded: {encoded}")
    print(f"  Decoded: {decoded}")
    
    # Test URL joining
    print("\n🧪 Testing URL Joining")
    base = "https://example.com/path/"
    relative = "subpage.html"
    joined = URLUtils.join(base, relative)
    print(f"  {base} + {relative} = {joined}")
    
    print("\n✅ URL Toolkit ready!")
