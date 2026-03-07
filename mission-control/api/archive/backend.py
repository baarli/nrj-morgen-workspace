#!/usr/bin/env python3
"""
Mission Control Backend API - Simplified
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

WORKSPACE = "/root/.openclaw/workspace"
SCRIPTS_DIR = f"{WORKSPACE}/scripts"
API_PORT = 8081

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if path == '/api/status':
            response = self.get_status()
        elif path == '/api/logs':
            response = self.get_logs()
        elif path == '/api/automations':
            response = self.get_automations()
        elif path == '/api/nrj-stats':
            response = self.get_nrj_stats()
        elif path == '/api/health':
            response = {'status': 'ok', 'timestamp': datetime.now().isoformat()}
        else:
            response = {'error': 'Not found'}
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if path == '/api/control':
            response = self.control_automation(data.get('name'), data.get('action'))
        else:
            response = {'error': 'Not found'}
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def get_status(self):
        try:
            auto_exec = os.path.exists(f"{WORKSPACE}/.auto-exec-log")
            autonomous = os.path.exists(f"{WORKSPACE}/.autonomous-mode.pid")
            webserver = os.path.exists(f"{WORKSPACE}/.webserver.pid")
            
            skills_dir = f"{WORKSPACE}/skills"
            skills_count = len([f for f in os.listdir(skills_dir) if f.endswith('.skill')]) if os.path.exists(skills_dir) else 0
            
            scripts_count = len([f for f in os.listdir(SCRIPTS_DIR) if f.endswith('.sh') or f.endswith('.py')]) if os.path.exists(SCRIPTS_DIR) else 0
            
            return {
                'autoExec': 'active' if auto_exec else 'inactive',
                'autonomousMode': 'active' if autonomous else 'inactive',
                'webServer': 'active' if webserver else 'inactive',
                'skills': skills_count,
                'scripts': scripts_count,
                'systemUptime': 'up 3 days',
                'lastUpdate': datetime.now().isoformat(),
                'systems': {
                    'autoExec': 'active' if auto_exec else 'inactive',
                    'memoryValidator': 'active',
                    'sessionHandler': 'active',
                    'autonomousMode': 'active' if autonomous else 'inactive',
                    'webServer': 'active' if webserver else 'inactive'
                }
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_logs(self):
        logs = []
        try:
            auto_exec_log = f"{WORKSPACE}/.auto-exec-log"
            if os.path.exists(auto_exec_log):
                with open(auto_exec_log, 'r') as f:
                    lines = f.readlines()[-10:]
                    for line in lines:
                        if line.strip():
                            logs.append({
                                'time': datetime.now().strftime('%H:%M:%S'),
                                'message': line.strip(),
                                'type': 'info'
                            })
            return logs
        except Exception as e:
            return [{'time': datetime.now().strftime('%H:%M:%S'), 'message': str(e), 'type': 'error'}]
    
    def get_automations(self):
        return [
            {'name': 'Daily Pre-Flight', 'schedule': 'Every 24h', 'status': 'active', 'lastRun': '2 hours ago'},
            {'name': 'Session End Capture', 'schedule': 'Every hour', 'status': 'active', 'lastRun': '5 minutes ago'},
            {'name': 'NRJ Dashboard Update', 'schedule': 'Wed 14:00', 'status': 'active', 'lastRun': '2 days ago'},
            {'name': 'Morning Routine', 'schedule': 'Mon-Fri 06:00', 'status': 'active', 'lastRun': 'Yesterday'},
            {'name': 'Podcast Download', 'schedule': 'Daily 07:00', 'status': 'active', 'lastRun': 'Today'}
        ]
    
    def control_automation(self, name, action):
        if action == 'run':
            return {'status': 'started', 'message': f'{name} started manually'}
        return {'status': 'error', 'message': 'Unknown action'}
    
    def get_nrj_stats(self):
        return {
            'radio': {'week': 7, 'year': 2026, 'dailyListeners': 69000, 'trend': '+23.2%', 'average2026': 58857},
            'podcast': {'week': 7, 'year': 2026, 'ranking': 62, 'uniqueListeners': 16470, 'downloads': 33405}
        }
    
    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', API_PORT), APIHandler)
    print(f"API running on port {API_PORT}")
    server.serve_forever()
