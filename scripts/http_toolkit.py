#!/usr/bin/env python3
"""
🌐 BAARLICLAW HTTP TOOLKIT
Avansert HTTP-klient med retry, caching, osv.
"""

import os
import sys
import json
import time
from typing import Dict, Optional, Any, Callable, List
from dataclasses import dataclass
from urllib import request, error, parse

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("HTTPToolkit")

@dataclass
class HTTPResponse:
    """HTTP response"""
    status: int
    body: str
    headers: Dict[str, str]
    url: str
    elapsed_ms: float
    
    def json(self) -> Optional[Dict]:
        """Parse response as JSON"""
        try:
            return json.loads(self.body)
        except:
            return None

class HTTPClient:
    """Advanced HTTP client"""
    
    def __init__(self, base_url: str = "", 
                 timeout: int = 30,
                 retries: int = 3,
                 retry_delay: float = 1.0):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.retries = retries
        self.retry_delay = retry_delay
        self.default_headers: Dict[str, str] = {
            'User-Agent': 'BaarliClaw-HTTP-Client/1.0'
        }
        self._cache: Dict[str, HTTPResponse] = {}
    
    def _make_request(self, method: str, url: str,
                     headers: Optional[Dict] = None,
                     data: Optional[bytes] = None) -> HTTPResponse:
        """Make HTTP request with retries"""
        full_url = f"{self.base_url}{url}" if self.base_url else url
        
        # Merge headers
        req_headers = self.default_headers.copy()
        if headers:
            req_headers.update(headers)
        
        # Build request
        req = request.Request(
            full_url,
            data=data,
            headers=req_headers,
            method=method
        )
        
        # Retry logic
        last_error = None
        for attempt in range(self.retries):
            start = time.time()
            try:
                with request.urlopen(req, timeout=self.timeout) as response:
                    body = response.read().decode('utf-8')
                    elapsed = (time.time() - start) * 1000
                    
                    return HTTPResponse(
                        status=response.getcode(),
                        body=body,
                        headers=dict(response.headers),
                        url=full_url,
                        elapsed_ms=elapsed
                    )
                    
            except error.HTTPError as e:
                last_error = e
                if e.code >= 500:  # Server error, retry
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise
            except Exception as e:
                last_error = e
                time.sleep(self.retry_delay * (attempt + 1))
        
        raise last_error or Exception("Request failed")
    
    def get(self, url: str, 
            headers: Optional[Dict] = None,
            use_cache: bool = False) -> HTTPResponse:
        """GET request"""
        cache_key = f"GET:{url}"
        
        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]
        
        response = self._make_request('GET', url, headers)
        
        if use_cache:
            self._cache[cache_key] = response
        
        return response
    
    def post(self, url: str,
             data: Optional[Dict] = None,
             json_data: Optional[Dict] = None,
             headers: Optional[Dict] = None) -> HTTPResponse:
        """POST request"""
        req_headers = headers or {}
        body = None
        
        if json_data:
            req_headers['Content-Type'] = 'application/json'
            body = json.dumps(json_data).encode()
        elif data:
            body = parse.urlencode(data).encode()
            req_headers['Content-Type'] = 'application/x-www-form-urlencoded'
        
        return self._make_request('POST', url, req_headers, body)
    
    def put(self, url: str,
            json_data: Optional[Dict] = None,
            headers: Optional[Dict] = None) -> HTTPResponse:
        """PUT request"""
        req_headers = headers or {}
        body = None
        
        if json_data:
            req_headers['Content-Type'] = 'application/json'
            body = json.dumps(json_data).encode()
        
        return self._make_request('PUT', url, req_headers, body)
    
    def delete(self, url: str,
               headers: Optional[Dict] = None) -> HTTPResponse:
        """DELETE request"""
        return self._make_request('DELETE', url, headers)
    
    def set_auth_token(self, token: str, header: str = "Authorization"):
        """Set auth token"""
        self.default_headers[header] = f"Bearer {token}"
    
    def set_basic_auth(self, username: str, password: str):
        """Set basic auth"""
        import base64
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
        self.default_headers['Authorization'] = f"Basic {credentials}"
    
    def clear_cache(self):
        """Clear response cache"""
        self._cache.clear()

class RESTClient:
    """REST API client"""
    
    def __init__(self, base_url: str, client: Optional[HTTPClient] = None):
        self.base_url = base_url
        self.client = client or HTTPClient()
    
    def list(self, resource: str) -> List[Dict]:
        """List resources"""
        response = self.client.get(f"/{resource}")
        data = response.json()
        return data if isinstance(data, list) else data.get('data', [])
    
    def get(self, resource: str, id: str) -> Optional[Dict]:
        """Get single resource"""
        response = self.client.get(f"/{resource}/{id}")
        return response.json()
    
    def create(self, resource: str, data: Dict) -> Dict:
        """Create resource"""
        response = self.client.post(f"/{resource}", json_data=data)
        return response.json() or {}
    
    def update(self, resource: str, id: str, data: Dict) -> Dict:
        """Update resource"""
        response = self.client.put(f"/{resource}/{id}", json_data=data)
        return response.json() or {}
    
    def delete(self, resource: str, id: str) -> bool:
        """Delete resource"""
        response = self.client.delete(f"/{resource}/{id}")
        return 200 <= response.status < 300

# === CONVENIENCE FUNCTIONS ===
def quick_get(url: str, timeout: int = 30) -> Optional[str]:
    """Quick GET request"""
    client = HTTPClient(timeout=timeout)
    try:
        response = client.get(url)
        return response.body
    except Exception as e:
        logger.error(f"Request failed: {e}")
        return None

def quick_post(url: str, data: Dict) -> Optional[Dict]:
    """Quick POST request"""
    client = HTTPClient()
    try:
        response = client.post(url, json_data=data)
        return response.json()
    except Exception as e:
        logger.error(f"Request failed: {e}")
        return None

def download_file(url: str, output_path: str) -> bool:
    """Download file"""
    try:
        request.urlretrieve(url, output_path)
        return True
    except Exception as e:
        logger.error(f"Download failed: {e}")
        return False

# === TESTING ===
if __name__ == "__main__":
    print("🌐 BaarliClaw HTTP Toolkit - Testing")
    print("=" * 50)
    
    # Test HTTP client
    print("\n🧪 Testing HTTP Client")
    client = HTTPClient(timeout=10)
    
    try:
        response = client.get("https://httpbin.org/get")
        print(f"✅ GET status: {response.status}")
        print(f"✅ Response time: {response.elapsed_ms:.0f}ms")
        
        data = response.json()
        if data:
            print(f"✅ JSON parsed: {type(data)}")
    except Exception as e:
        print(f"⚠️ GET test: {e}")
    
    # Test POST
    try:
        response = client.post(
            "https://httpbin.org/post",
            json_data={"test": "data", "number": 42}
        )
        print(f"✅ POST status: {response.status}")
    except Exception as e:
        print(f"⚠️ POST test: {e}")
    
    # Test quick functions
    print("\n🧪 Testing Quick Functions")
    
    result = quick_get("https://httpbin.org/ip")
    if result:
        print(f"✅ Quick GET: {len(result)} chars")
    
    print("\n✅ HTTP Toolkit ready!")
