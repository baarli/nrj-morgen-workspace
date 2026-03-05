#!/usr/bin/env python3
"""
Supabase API Wrapper for BaarliClaw
Enkel wrapper for å kommunisere med Supabase
"""

import os
import json
import urllib.request
import urllib.error
from datetime import datetime

SUPABASE_URL = "https://kvniauxokdtmpvjtfnje.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"

class SupabaseAPI:
    def __init__(self):
        self.base_url = SUPABASE_URL + "/rest/v1"
        self.headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
    
    def _request(self, method, endpoint, data=None, params=None):
        """Utfør HTTP request"""
        url = f"{self.base_url}{endpoint}"
        if params:
            url += "?" + "&".join([f"{k}={v}" for k, v in params.items()])
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode() if data else None,
            headers=self.headers,
            method=method
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code} - {e.read().decode()}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    # Agent Commands
    def get_pending_commands(self):
        """Hent kommandoer som venter på behandling"""
        return self._request("GET", "/agent_commands", params={
            "status": "eq.pending",
            "order": "created_at.asc"
        })
    
    def update_command(self, cmd_id, updates):
        """Oppdater en kommando"""
        return self._request("PATCH", f"/agent_commands?id=eq.{cmd_id}", updates)
    
    # Agent Responses
    def send_response(self, command_id, response_type, response_data):
        """Send svar på en kommando"""
        return self._request("POST", "/agent_responses", {
            "command_id": command_id,
            "response_type": response_type,
            "response_data": response_data
        })
    
    # Approval Requests
    def create_approval_request(self, request_type, title, description, details=None):
        """Opprett en godkjenningsforespørsel"""
        return self._request("POST", "/approval_requests", {
            "request_type": request_type,
            "title": title,
            "description": description,
            "details": details or {}
        })
    
    def get_pending_approvals(self):
        """Hent ventende godkjenningsforespørsler"""
        return self._request("GET", "/approval_requests", params={
            "status": "eq.pending",
            "order": "created_at.asc"
        })
    
    # System Status
    def update_system_status(self, system_name, status, metrics=None):
        """Oppdater system status"""
        updates = {
            "status": status,
            "last_check": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        if metrics:
            updates["metrics"] = metrics
        
        return self._request("PATCH", f"/system_status?system_name=eq.{system_name}", updates)
    
    def get_system_status(self):
        """Hent status for alle systemer"""
        return self._request("GET", "/system_status")
    
    # Activity Log
    def log_activity(self, level, category, message, details=None, actionable=False):
        """Logg en aktivitet"""
        return self._request("POST", "/activity_log", {
            "level": level,
            "category": category,
            "message": message,
            "details": details or {},
            "actionable": actionable
        })
    
    def get_recent_activity(self, limit=50):
        """Hent nylig aktivitet"""
        return self._request("GET", "/activity_log", params={
            "order": "created_at.desc",
            "limit": limit
        })

# Test
if __name__ == "__main__":
    api = SupabaseAPI()
    
    # Test system status
    print("Testing system status...")
    status = api.get_system_status()
    print(f"System status: {json.dumps(status, indent=2)}")
    
    # Test log
    print("\nTesting activity log...")
    result = api.log_activity("info", "system", "API wrapper test", {"test": True})
    print(f"Log result: {result}")
