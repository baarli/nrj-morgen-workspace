#!/usr/bin/env python3
"""
🌐 BAARLICLAW API GATEWAY SERVICE
Sentral API-gateway med routing, caching og rate limiting
"""

import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, '/root/.openclaw/workspace/scripts')

from baarliclaw_toolkit import setup_logging
from cache_toolkit import MemoryCache
from uuid_toolkit import UUIDUtils
from date_toolkit import DateUtils

logger = setup_logging("api-gateway")

@dataclass
class APIRequest:
    """API request data"""
    id: str
    method: str
    path: str
    query_params: Dict[str, List[str]]
    headers: Dict[str, str]
    body: Optional[str]
    timestamp: float
    client_ip: str

@dataclass
class APIResponse:
    """API response data"""
    status_code: int
    body: Any
    headers: Dict[str, str]
    cached: bool = False

class RateLimiter:
    """Simple rate limiter"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests: Dict[str, List[float]] = {}
    
    def is_allowed(self, client_id: str) -> bool:
        """Sjekk om request er tillatt"""
        now = time.time()
        
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Fjern gamle requests
        self.requests[client_id] = [
            t for t in self.requests[client_id]
            if now - t < self.window
        ]
        
        # Sjekk limit
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        # Registrer request
        self.requests[client_id].append(now)
        return True
    
    def get_remaining(self, client_id: str) -> int:
        """Hent gjenværende requests"""
        if client_id not in self.requests:
            return self.max_requests
        return max(0, self.max_requests - len(self.requests[client_id]))

class APIGateway:
    """API Gateway"""
    
    def __init__(self, cache_ttl: int = 300):
        self.routes: Dict[str, Dict[str, Callable]] = {}
        self.cache = MemoryCache(default_ttl=cache_ttl)
        self.rate_limiter = RateLimiter()
        self.request_log: List[APIRequest] = []
        self.middleware: List[Callable] = []
    
    def route(self, path: str, methods: List[str] = None):
        """Decorator for å registrere route"""
        if methods is None:
            methods = ["GET"]
        
        def decorator(func: Callable):
            if path not in self.routes:
                self.routes[path] = {}
            for method in methods:
                self.routes[path][method.upper()] = func
            return func
        return decorator
    
    def add_middleware(self, middleware: Callable):
        """Legg til middleware"""
        self.middleware.append(middleware)
    
    def handle_request(self, request: APIRequest) -> APIResponse:
        """Håndter en request"""
        # Logg request
        self.request_log.append(request)
        
        # Kjør middleware
        for mw in self.middleware:
            result = mw(request)
            if isinstance(result, APIResponse):
                return result
        
        # Rate limiting
        if not self.rate_limiter.is_allowed(request.client_ip):
            return APIResponse(
                status_code=429,
                body={"error": "Rate limit exceeded"},
                headers={"X-RateLimit-Remaining": "0"}
            )
        
        # Sjekk cache for GET requests
        cache_key = f"{request.method}:{request.path}"
        if request.method == "GET":
            cached = self.cache.get(cache_key)
            if cached:
                return APIResponse(
                    status_code=200,
                    body=cached,
                    headers={},
                    cached=True
                )
        
        # Finn handler
        if request.path not in self.routes:
            return APIResponse(
                status_code=404,
                body={"error": "Not found"},
                headers={}
            )
        
        if request.method not in self.routes[request.path]:
            return APIResponse(
                status_code=405,
                body={"error": "Method not allowed"},
                headers={}
            )
        
        # Kjør handler
        try:
            handler = self.routes[request.path][request.method]
            result = handler(request)
            
            # Cache resultat
            if request.method == "GET":
                self.cache.set(cache_key, result)
            
            return APIResponse(
                status_code=200,
                body=result,
                headers={
                    "X-RateLimit-Remaining": str(
                        self.rate_limiter.get_remaining(request.client_ip)
                    )
                }
            )
            
        except Exception as e:
            logger.error(f"Handler error: {e}")
            return APIResponse(
                status_code=500,
                body={"error": str(e)},
                headers={}
            )
    
    def get_stats(self) -> Dict[str, Any]:
        """Hent gateway-statistikk"""
        return {
            'total_requests': len(self.request_log),
            'routes': len(self.routes),
            'cache_entries': len(self.cache.keys()),
            'unique_clients': len(self.rate_limiter.requests)
        }

# === EKSEMPEL ROUTES ===

def create_sample_gateway() -> APIGateway:
    """Lag en sample gateway"""
    gateway = APIGateway()
    
    @gateway.route("/", methods=["GET"])
    def root(request: APIRequest):
        return {
            "service": "BaarliClaw API Gateway",
            "version": "1.0",
            "timestamp": DateUtils.format(DateUtils.now())
        }
    
    @gateway.route("/health", methods=["GET"])
    def health(request: APIRequest):
        return {
            "status": "healthy",
            "timestamp": DateUtils.format(DateUtils.now())
        }
    
    @gateway.route("/stats", methods=["GET"])
    def stats(request: APIRequest):
        return gateway.get_stats()
    
    @gateway.route("/echo", methods=["POST", "GET"])
    def echo(request: APIRequest):
        return {
            "method": request.method,
            "path": request.path,
            "query": request.query_params,
            "headers": request.headers,
            "body": request.body
        }
    
    @gateway.route("/services", methods=["GET"])
    def services(request: APIRequest):
        return {
            "services": [
                {"name": "Agent Orchestrator", "status": "running"},
                {"name": "Notification Service", "status": "running"},
                {"name": "Performance Monitor", "status": "running"},
                {"name": "Task Queue", "status": "running"},
                {"name": "Backup Service", "status": "running"},
            ]
        }
    
    return gateway

def simulate_requests(gateway: APIGateway):
    """Simuler noen requests"""
    requests = [
        ("GET", "/", {}, "127.0.0.1"),
        ("GET", "/health", {}, "127.0.0.1"),
        ("GET", "/services", {}, "127.0.0.1"),
        ("GET", "/stats", {}, "127.0.0.1"),
        ("POST", "/echo", {"Content-Type": "application/json"}, "127.0.0.1"),
        ("GET", "/nonexistent", {}, "127.0.0.1"),
    ]
    
    for method, path, headers, ip in requests:
        request = APIRequest(
            id=UUIDUtils.generate_short(),
            method=method,
            path=path,
            query_params={},
            headers=headers,
            body='{"test": "data"}' if method == "POST" else None,
            timestamp=time.time(),
            client_ip=ip
        )
        
        response = gateway.handle_request(request)
        status_icon = "✅" if response.status_code == 200 else "❌"
        cache_icon = "💾" if response.cached else ""
        print(f"  {status_icon} {method} {path} -> {response.status_code} {cache_icon}")

def main():
    """Hovedfunksjon"""
    print("="*70)
    print("🌐 API GATEWAY SERVICE")
    print("="*70)
    
    # Lag gateway
    gateway = create_sample_gateway()
    
    print("\n📝 Registrerte routes:")
    for path, methods in gateway.routes.items():
        print(f"  {path}: {', '.join(methods.keys())}")
    
    # Simuler requests
    print("\n🔄 Simulerer requests...")
    simulate_requests(gateway)
    
    # Vis stats
    print("\n📊 Gateway statistikk:")
    stats = gateway.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*70)
    print("✅ API Gateway Service klar!")
    print("="*70)

if __name__ == "__main__":
    main()
