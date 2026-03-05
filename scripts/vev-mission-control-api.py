#!/usr/bin/env python3
"""
Vev Mission Control API Server
Exposes all Vev system statuses and controls
"""
import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

WORKSPACE = "/root/.openclaw/workspace"
PORT = 8765

class VevAPIHandler(BaseHTTPRequestHandler):
    """Handle API requests"""
    
    def log_message(self, format, *args):
        # Custom logging
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {args[0]}")
    
    def do_GET(self):
        """Handle GET requests"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        path = self.path
        
        if path == '/api/status':
            response = self.get_overall_status()
        elif path == '/api/telegram/status':
            response = self.get_telegram_status()
        elif path == '/api/learning/status':
            response = self.get_learning_status()
        elif path == '/api/health/status':
            response = self.get_health_status()
        elif path == '/api/backup/status':
            response = self.get_backup_status()
        elif path == '/api/subagents/status':
            response = self.get_subagent_status()
        elif path == '/api/morning-routine/status':
            response = self.get_morning_routine_status()
        else:
            response = {"error": "Unknown endpoint", "available": [
                "/api/status",
                "/api/telegram/status",
                "/api/learning/status",
                "/api/health/status",
                "/api/backup/status",
                "/api/subagents/status",
                "/api/morning-routine/status"
            ]}
        
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def get_overall_status(self):
        """Get overall system status"""
        return {
            "timestamp": datetime.now().isoformat(),
            "vev_version": "2.1",
            "systems": {
                "telegram": self._check_service("vev-telegram-responder"),
                "file_watcher": self._check_service("vev-file-watcher"),
                "learning_loop": True,
                "health_monitor": True,
                "backup_system": True
            },
            "overall_health": "healthy",
            "active_features": [
                "Auto-Responder",
                "Learning Loop",
                "File Watcher",
                "Health Monitor",
                "Nightly Backup",
                "Sub-Agent System"
            ]
        }
    
    def get_telegram_status(self):
        """Get Telegram bot status"""
        try:
            # Check if service is running
            result = subprocess.run(
                ['systemctl', 'is-active', 'vev-telegram-responder.service'],
                capture_output=True,
                text=True
            )
            is_running = result.returncode == 0
            
            # Get stats from log
            log_file = f"{WORKSPACE}/brain/logs/telegram-auto-responder.log"
            total_messages = 0
            if os.path.exists(log_file):
                with open(log_file) as f:
                    content = f.read()
                    total_messages = content.count("Melding fra")
            
            return {
                "bot_username": "@Vev_kompis_bot",
                "status": "online" if is_running else "offline",
                "service_status": "running" if is_running else "stopped",
                "total_messages": total_messages,
                "auto_responder": "active" if is_running else "inactive",
                "features": [
                    "AI-based responses",
                    "Conversation history",
                    "User profiles",
                    "Emotional voice",
                    "Context awareness"
                ]
            }
        except Exception as e:
            return {"error": str(e), "status": "unknown"}
    
    def get_learning_status(self):
        """Get learning system status"""
        try:
            db_file = f"{WORKSPACE}/brain/learning-database.json"
            total_learnings = 0
            total_sessions = 0
            
            if os.path.exists(db_file):
                with open(db_file) as f:
                    db = json.load(f)
                    total_learnings = len(db.get("learnings", []))
                    total_sessions = len(db.get("sessions", []))
            
            # Check file watcher
            result = subprocess.run(
                ['systemctl', 'is-active', 'vev-file-watcher.service'],
                capture_output=True,
                text=True
            )
            file_watcher_running = result.returncode == 0
            
            return {
                "total_learnings": total_learnings,
                "total_sessions": total_sessions,
                "file_watcher": "running" if file_watcher_running else "stopped",
                "auto_sync": "active" if file_watcher_running else "inactive",
                "learning_loop": "active",
                "status": "healthy"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_health_status(self):
        """Get health monitor status"""
        try:
            # Check services
            services = {
                "telegram_responder": self._check_service("vev-telegram-responder"),
                "file_watcher": self._check_service("vev-file-watcher"),
                "health_monitor": True
            }
            
            # Check disk space
            result = subprocess.run(
                ['df', '-h', '/'],
                capture_output=True,
                text=True
            )
            disk_line = result.stdout.strip().split('\n')[1]
            disk_usage = disk_line.split()[4].replace('%', '')
            
            # Check GitHub connectivity
            gh_result = subprocess.run(
                ['curl', '-s', '--head', 'https://github.com'],
                capture_output=True,
                text=True
            )
            github_ok = '200' in gh_result.stdout or '301' in gh_result.stdout
            
            all_healthy = all(services.values()) and int(disk_usage) < 90
            
            return {
                "overall_status": "healthy" if all_healthy else "warning",
                "services": services,
                "disk_usage": f"{disk_usage}%",
                "github_connected": github_ok,
                "last_check": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e), "overall_status": "unknown"}
    
    def get_backup_status(self):
        """Get backup system status"""
        try:
            # Check last backup from log
            log_file = f"{WORKSPACE}/brain/logs/nightly-github-backup.log"
            last_backup = None
            status = "unknown"
            
            if os.path.exists(log_file):
                with open(log_file) as f:
                    lines = f.readlines()
                    for line in reversed(lines):
                        if "NIGHTLY GITHUB BACKUP" in line:
                            last_backup = line.split(']')[0].strip('[')
                        if "Successfully pushed" in line:
                            status = "success"
                            break
                        if "failed" in line.lower():
                            status = "failed"
                            break
            
            return {
                "github_repo": "baarli/nrj-morgen-workspace",
                "last_backup": last_backup,
                "status": status,
                "next_backup": "03:00 tomorrow",
                "backup_type": "automatic (cron)",
                "includes": [
                    "All code",
                    "Learning database",
                    "Configuration",
                    "Documentation"
                ]
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_subagent_status(self):
        """Get sub-agent system status"""
        return {
            "status": "available",
            "active_tasks": [],
            "worker_types": [
                "research",
                "analysis",
                "coding"
            ],
            "features": [
                "Parallel execution",
                "Progress tracking",
                "User interrupt",
                "Result collection"
            ]
        }
    
    def get_morning_routine_status(self):
        """Get morning routine status"""
        return {
            "status": "configured",
            "schedule": "06:00 daily",
            "features": [
                "Brave News API",
                "Auto-title generation",
                "Saksliste insertion",
                "Email notifications"
            ],
            "sources": [
                "VG",
                "Dagbladet",
                "NRK",
                "Daily Mail"
            ]
        }
    
    def _check_service(self, service_name):
        """Check if a systemd service is running"""
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', f'{service_name}.service'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False

def run_server():
    """Run the API server"""
    server = HTTPServer(('0.0.0.0', PORT), VevAPIHandler)
    print(f"🚀 Vev Mission Control API Server running on port {PORT}")
    print(f"   Endpoints:")
    print(f"   - http://localhost:{PORT}/api/status")
    print(f"   - http://localhost:{PORT}/api/telegram/status")
    print(f"   - http://localhost:{PORT}/api/learning/status")
    print(f"   - http://localhost:{PORT}/api/health/status")
    print(f"   - http://localhost:{PORT}/api/backup/status")
    print(f"   Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        server.shutdown()

if __name__ == "__main__":
    run_server()
