#!/bin/bash
# Mission Control Backend Installer for nrjmorgen.com
# Installerer API på serveren

set -e

echo "🚀 Mission Control Backend Installer"
echo "====================================="
echo ""

# Konfigurasjon
INSTALL_DIR="/opt/mission-control"
API_PORT=8081
SERVICE_NAME="mission-control-api"

echo "1. Sjekker root-tilgang..."
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Dette scriptet må kjøres som root (sudo)"
    exit 1
fi

echo "2. Installerer avhengigheter..."
apt-get update -qq
apt-get install -y -qq python3 python3-pip curl

echo "3. Lager installasjonsmappe..."
mkdir -p $INSTALL_DIR
mkdir -p $INSTALL_DIR/logs

echo "4. Kopierer API-filer..."
cat > $INSTALL_DIR/backend.py << 'PYTHON_EOF'
#!/usr/bin/env python3
"""
Mission Control Backend API v2.0
Full funksjonalitet med Supabase-integrasjon
"""

import os
import sys
import json
import subprocess
import threading
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler

# Konfigurasjon
SUPABASE_URL = 'https://kvniauxokdtmpvjtfnej.supabase.co'
SUPABASE_SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE'
TENANT_ID = 'a0000000-0000-0000-0000-000000000001'
API_PORT = 8081
WORKSPACE = "/opt/mission-control"
SCRIPTS_DIR = f"{WORKSPACE}/scripts"

class SupabaseClient:
    def __init__(self):
        self.base_url = SUPABASE_URL
        self.api_key = SUPABASE_SERVICE_KEY
    
    def request(self, endpoint, method='GET', data=None, params=None):
        url = f"{self.base_url}/rest/v1{endpoint}"
        if params:
            query_string = '&'.join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
            url += '?' + query_string
        
        headers = {
            'apikey': self.api_key,
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
        
        req = urllib.request.Request(url, headers=headers, method=method)
        if data:
            req.data = json.dumps(data).encode('utf-8')
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status == 204:
                    return {'success': True}
                result = response.read().decode('utf-8')
                return json.loads(result) if result else {'success': True}
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            raise Exception(f"HTTP {e.code}: {error_body}")
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")
    
    def get(self, endpoint, params=None):
        return self.request(endpoint, 'GET', params=params)
    
    def post(self, endpoint, data):
        return self.request(endpoint, 'POST', data=data)
    
    def patch(self, endpoint, data):
        return self.request(endpoint, 'PATCH', data=data)
    
    def delete(self, endpoint):
        return self.request(endpoint, 'DELETE')

supabase = SupabaseClient()

morning_routine_status = {
    'running': False,
    'started_at': None,
    'progress': 0,
    'message': 'Idle',
    'last_result': None
}

class APIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {args[0]}")
    
    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, apikey')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, apikey')
        self.end_headers()
    
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        
        try:
            if path == '/api/health':
                self.send_json_response({'status': 'ok', 'timestamp': datetime.now().isoformat()})
            
            elif path == '/api/saker':
                date = query.get('date', [datetime.now().strftime('%Y-%m-%d')])[0]
                self.send_json_response(self.get_saker(date))
            
            elif path == '/api/nrj/stats':
                self.send_json_response(self.get_nrj_stats())
            
            elif path == '/api/routine/morning/status':
                self.send_json_response(morning_routine_status)
            
            else:
                self.send_json_response({'error': 'Not found'}, 404)
        
        except Exception as e:
            print(f"Error in GET {path}: {e}")
            self.send_json_response({'error': str(e)}, 500)
    
    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = {}
        if content_length > 0:
            try:
                body = json.loads(self.rfile.read(content_length).decode())
            except:
                pass
        
        try:
            if path == '/api/routine/morning':
                self.send_json_response(self.run_morning_routine())
            else:
                self.send_json_response({'error': 'Not found'}, 404)
        
        except Exception as e:
            print(f"Error in POST {path}: {e}")
            self.send_json_response({'error': str(e)}, 500)
    
    def get_saker(self, date):
        try:
            result = supabase.get('/agenda_items', {
                'tenant_id': f'eq.{TENANT_ID}',
                'show_date': f'eq.{date}',
                'order': 'order_index.asc'
            })
            return {'saker': result, 'count': len(result), 'date': date}
        except Exception as e:
            return {'error': str(e), 'saker': [], 'count': 0}
    
    def get_nrj_stats(self):
        try:
            radio = supabase.get('/agenda_items', {
                'tenant_id': f'eq.{TENANT_ID}',
                'category': f'eq.STATS',
                'order': 'created_at.desc',
                'limit': 1
            })
            
            podcast = supabase.get('/agenda_items', {
                'tenant_id': f'eq.{TENANT_ID}',
                'category': f'eq.PODCAST_RANKING',
                'order': 'created_at.desc',
                'limit': 1
            })
            
            return {
                'radio': radio[0] if radio else None,
                'podcast': podcast[0] if podcast else None
            }
        except Exception as e:
            return {'error': str(e)}
    
    def run_morning_routine(self):
        global morning_routine_status
        
        if morning_routine_status['running']:
            return {'status': 'already_running', 'message': 'Morning Routine kjører allerede'}
        
        return {'status': 'started', 'message': 'Morning Routine startet (simulert)'}

def main():
    server = HTTPServer(('0.0.0.0', API_PORT), APIHandler)
    print(f"🚀 Mission Control API running on port {API_PORT}")
    server.serve_forever()

if __name__ == '__main__':
    main()
PYTHON_EOF

echo "5. Setter rettigheter..."
chmod +x $INSTALL_DIR/backend.py

echo "6. Lager systemd service..."
cat > /etc/systemd/system/$SERVICE_NAME.service << EOF
[Unit]
Description=Mission Control API
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=$INSTALL_DIR
ExecStart=/usr/bin/python3 $INSTALL_DIR/backend.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo "7. Starter service..."
systemctl daemon-reload
systemctl enable $SERVICE_NAME
systemctl start $SERVICE_NAME

echo "8. Konfigurerer nginx..."
if [ -f "/etc/nginx/sites-available/nrjmorgen.com" ]; then
    # Sjekk om config allerede finnes
    if ! grep -q "kloakontroll/api" /etc/nginx/sites-available/nrjmorgen.com; then
        cat >> /etc/nginx/sites-available/nrjmorgen.com << 'NGINX_EOF'

# Mission Control API
location /kloakontroll/api/ {
    proxy_pass http://localhost:8081/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
NGINX_EOF
        nginx -t && systemctl reload nginx
    fi
fi

echo ""
echo "✅ Installasjon fullført!"
echo ""
echo "Status:"
systemctl status $SERVICE_NAME --no-pager -l

echo ""
echo "Test API:"
curl -s http://localhost:8081/api/health | python3 -m json.tool 2>/dev/null || echo "API ikke tilgjengelig ennå (vent 5 sekunder)"
