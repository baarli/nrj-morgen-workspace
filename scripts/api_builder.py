#!/usr/bin/env python3
"""
🔌 BAARLICLAW API BUILDER
Bygg raskt API-er med FastAPI-lignende syntaks
"""

import os
import sys
import json
import re
from typing import Dict, List, Optional, Callable, Any, Tuple
from dataclasses import dataclass
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import threading

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("APIBuilder")

@dataclass
class Route:
    """API Route definition"""
    method: str
    path: str
    handler: Callable
    description: str = ""

class APIBuilder:
    """Build simple HTTP APIs"""
    
    def __init__(self, title: str = "API", version: str = "1.0.0"):
        self.title = title
        self.version = version
        self.routes: List[Route] = []
        self.middleware: List[Callable] = []
        self.server = None
    
    def get(self, path: str, description: str = ""):
        """Decorator for GET routes"""
        def decorator(func: Callable):
            self.routes.append(Route("GET", path, func, description))
            return func
        return decorator
    
    def post(self, path: str, description: str = ""):
        """Decorator for POST routes"""
        def decorator(func: Callable):
            self.routes.append(Route("POST", path, func, description))
            return func
        return decorator
    
    def put(self, path: str, description: str = ""):
        """Decorator for PUT routes"""
        def decorator(func: Callable):
            self.routes.append(Route("PUT", path, func, description))
            return func
        return decorator
    
    def delete(self, path: str, description: str = ""):
        """Decorator for DELETE routes"""
        def decorator(func: Callable):
            self.routes.append(Route("DELETE", path, func, description))
            return func
        return decorator
    
    def _match_route(self, method: str, path: str) -> Optional[Tuple[Route, Dict[str, str]]]:
        """Match request to route and extract parameters"""
        for route in self.routes:
            if route.method != method:
                continue
            
            # Convert route path to regex
            pattern = route.path
            param_names = []
            
            # Find path parameters {name}
            for match in re.finditer(r'\{(\w+)\}', route.path):
                param_names.append(match.group(1))
                pattern = pattern.replace(match.group(0), r'(\w+)')
            
            # Match
            regex = f'^{pattern}$'
            match = re.match(regex, path)
            
            if match:
                params = dict(zip(param_names, match.groups()))
                return route, params
        
        return None
    
    def _create_handler(self):
        """Create HTTP request handler"""
        api = self
        
        class APIHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                logger.info(f"{self.command} {self.path} - {args}")
            
            def _send_json(self, data: Any, status: int = 200):
                """Send JSON response"""
                self.send_response(status)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())
            
            def _send_error(self, message: str, status: int = 500):
                """Send error response"""
                self._send_json({"error": message}, status)
            
            def _get_body(self) -> Dict:
                """Parse request body"""
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    body = self.rfile.read(content_length).decode()
                    try:
                        return json.loads(body)
                    except:
                        return {"raw": body}
                return {}
            
            def do_GET(self):
                self._handle_request("GET")
            
            def do_POST(self):
                self._handle_request("POST")
            
            def do_PUT(self):
                self._handle_request("PUT")
            
            def do_DELETE(self):
                self._handle_request("DELETE")
            
            def do_OPTIONS(self):
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
            
            def _handle_request(self, method: str):
                parsed = urllib.parse.urlparse(self.path)
                path = parsed.path
                query = urllib.parse.parse_qs(parsed.query)
                
                # Special routes
                if path == "/docs":
                    self._send_docs()
                    return
                
                if path == "/health":
                    self._send_json({"status": "healthy", "version": api.version})
                    return
                
                # Match route
                matched = api._match_route(method, path)
                
                if not matched:
                    self._send_error("Not found", 404)
                    return
                
                route, params = matched
                
                try:
                    # Build context
                    context = {
                        "params": params,
                        "query": query,
                        "body": self._get_body() if method in ["POST", "PUT"] else {},
                        "headers": dict(self.headers)
                    }
                    
                    # Call handler
                    result = route.handler(context)
                    
                    if result is None:
                        self._send_json({"message": "Success"})
                    elif isinstance(result, tuple):
                        data, status = result
                        self._send_json(data, status)
                    else:
                        self._send_json(result)
                        
                except Exception as e:
                    logger.error(f"Handler error: {e}")
                    self._send_error(str(e), 500)
            
            def _send_docs(self):
                """Send API documentation"""
                docs = {
                    "title": api.title,
                    "version": api.version,
                    "routes": [
                        {
                            "method": r.method,
                            "path": r.path,
                            "description": r.description
                        }
                        for r in api.routes
                    ]
                }
                self._send_json(docs)
        
        return APIHandler
    
    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Start the API server"""
        handler = self._create_handler()
        self.server = HTTPServer((host, port), handler)
        
        logger.info(f"🚀 API server starting on http://{host}:{port}")
        logger.info(f"📚 Documentation: http://{host}:{port}/docs")
        logger.info(f"💚 Health check: http://{host}:{port}/health")
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            logger.info("\n🛑 Server stopped")
    
    def start_background(self, host: str = "0.0.0.0", port: int = 8000):
        """Start server in background thread"""
        handler = self._create_handler()
        self.server = HTTPServer((host, port), handler)
        
        thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        thread.start()
        
        logger.info(f"🚀 API server started in background on http://{host}:{port}")
        return thread
    
    def stop(self):
        """Stop the server"""
        if self.server:
            self.server.shutdown()
            logger.info("🛑 Server stopped")

# === PRE-BUILT API COMPONENTS ===
class CRUDAPI:
    """Quick CRUD API for a resource"""
    
    def __init__(self, resource_name: str, initial_data: Optional[List[Dict]] = None):
        self.resource = resource_name
        self.data = initial_data or []
        self.id_counter = max([d.get('id', 0) for d in self.data] + [0]) + 1
        self.api = APIBuilder(f"{resource_name.title()} API")
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup CRUD routes"""
        
        @self.api.get(f"/{self.resource}", f"List all {self.resource}")
        def list_items(ctx):
            return {
                "data": self.data,
                "count": len(self.data)
            }
        
        @self.api.get(f"/{self.resource}/{{id}}", f"Get a specific {self.resource}")
        def get_item(ctx):
            item_id = int(ctx["params"]["id"])
            item = next((d for d in self.data if d.get('id') == item_id), None)
            if item:
                return item
            return {"error": "Not found"}, 404
        
        @self.api.post(f"/{self.resource}", f"Create a new {self.resource}")
        def create_item(ctx):
            item = ctx["body"]
            item['id'] = self.id_counter
            self.id_counter += 1
            self.data.append(item)
            return item, 201
        
        @self.api.put(f"/{self.resource}/{{id}}", f"Update a {self.resource}")
        def update_item(ctx):
            item_id = int(ctx["params"]["id"])
            item = next((d for d in self.data if d.get('id') == item_id), None)
            if not item:
                return {"error": "Not found"}, 404
            
            updates = ctx["body"]
            item.update(updates)
            return item
        
        @self.api.delete(f"/{self.resource}/{{id}}", f"Delete a {self.resource}")
        def delete_item(ctx):
            item_id = int(ctx["params"]["id"])
            item = next((d for d in self.data if d.get('id') == item_id), None)
            if not item:
                return {"error": "Not found"}, 404
            
            self.data.remove(item)
            return {"message": "Deleted"}
    
    def run(self, host: str = "0.0.0.0", port: int = 8000):
        self.api.run(host, port)

# === TESTING ===
if __name__ == "__main__":
    print("🔌 BaarliClaw API Builder - Testing")
    print("=" * 50)
    
    # Test 1: Simple API
    print("\n🧪 Test 1: Simple API")
    api = APIBuilder("Test API", "1.0.0")
    
    @api.get("/", "Root endpoint")
    def root(ctx):
        return {"message": "Hello, World!", "version": "1.0.0"}
    
    @api.get("/users/{id}", "Get user by ID")
    def get_user(ctx):
        user_id = ctx["params"]["id"]
        return {"id": user_id, "name": f"User {user_id}"}
    
    @api.post("/users", "Create a user")
    def create_user(ctx):
        body = ctx["body"]
        return {"created": True, "data": body}, 201
    
    print("✅ Routes registered:")
    for route in api.routes:
        print(f"   {route.method} {route.path}")
    
    # Test 2: CRUD API
    print("\n🧪 Test 2: CRUD API")
    crud = CRUDAPI("tasks", [
        {"id": 1, "title": "Task 1", "done": False},
        {"id": 2, "title": "Task 2", "done": True}
    ])
    
    print("✅ CRUD API created with sample data")
    print("   Routes:")
    for route in crud.api.routes:
        print(f"   {route.method} {route.path}")
    
    print("\n✅ API Builder ready!")
    print("\nTo start a server:")
    print("  api.run(port=8000)")
    print("\nOr in background:")
    print("  api.start_background(port=8000)")
