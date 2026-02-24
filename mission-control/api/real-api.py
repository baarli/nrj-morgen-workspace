#!/usr/bin/env python3
"""
Mission Control Real API
Faktisk kommunikasjon med BaarliClaw systemer
"""

import os
import sys
import json
import subprocess
import psutil
from datetime import datetime, timedelta
from pathlib import Path

# Konfigurasjon
WORKSPACE = "/root/.openclaw/workspace"
SCRIPTS_DIR = f"{WORKSPACE}/scripts"
LOG_DIR = "/var/log"

def get_system_status():
    """Hent faktisk system status"""
    try:
        # Sjekk om auto-exec kjører
        auto_exec = os.path.exists(f"{WORKSPACE}/.auto-exec-log")
        
        # Sjekk om autonomous mode kjører
        autonomous = os.path.exists(f"{WORKSPACE}/.autonomous-mode.pid")
        
        # Sjekk web server
        webserver = os.path.exists(f"{WORKSPACE}/.webserver.pid")
        
        # Hent antall skills
        skills_count = len([f for f in os.listdir(f"{WORKSPACE}/skills") if f.endswith('.skill')])
        
        # Hent antall scripts
        scripts_count = len([f for f in os.listdir(SCRIPTS_DIR) if f.endswith('.sh') or f.endswith('.py')])
        
        # Hent system uptime
        uptime = subprocess.check_output(['uptime', '-p']).decode().strip()
        
        return {
            "autoExec": "active" if auto_exec else "inactive",
            "autonomousMode": "active" if autonomous else "inactive",
            "webServer": "active" if webserver else "inactive",
            "skills": skills_count,
            "scripts": scripts_count,
            "systemUptime": uptime,
            "lastUpdate": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

def get_live_logs(limit=20):
    """Hent faktiske logger fra systemet"""
    logs = []
    
    try:
        # Les auto-exec log
        auto_exec_log = f"{WORKSPACE}/.auto-exec-log"
        if os.path.exists(auto_exec_log):
            with open(auto_exec_log, 'r') as f:
                lines = f.readlines()[-limit:]
                for line in lines:
                    if line.strip():
                        logs.append({
                            "time": datetime.now().strftime("%H:%M:%S"),
                            "message": line.strip(),
                            "type": "info"
                        })
        
        # Les autonomous log
        auto_log = f"{WORKSPACE}/.autonomous-log"
        if os.path.exists(auto_log):
            with open(auto_log, 'r') as f:
                lines = f.readlines()[-limit:]
                for line in lines:
                    if line.strip():
                        logs.append({
                            "time": datetime.now().strftime("%H:%M:%S"),
                            "message": line.strip(),
                            "type": "success"
                        })
        
        return logs[:limit]
    except Exception as e:
        return [{"time": datetime.now().strftime("%H:%M:%S"), "message": f"Error: {e}", "type": "error"}]

def get_automations():
    """Hent faktiske automasjoner fra cron"""
    try:
        # Hent cron jobs
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        cron_lines = result.stdout.strip().split('\n')
        
        automations = []
        for line in cron_lines:
            if line.strip() and not line.startswith('#'):
                # Parse cron line
                parts = line.split()
                if len(parts) >= 6:
                    schedule = ' '.join(parts[:5])
                    command = ' '.join(parts[5:])
                    
                    # Finn navn fra command
                    name = "Unknown"
                    if 'morning-routine' in command:
                        name = "Morning Routine"
                    elif 'nrj-dashboard' in command:
                        name = "NRJ Dashboard Update"
                    elif 'podcast' in command:
                        name = "Podcast Download"
                    elif 'pre-flight' in command:
                        name = "Pre-Flight Check"
                    elif 'learning' in command:
                        name = "Learning Capture"
                    
                    automations.append({
                        "name": name,
                        "schedule": schedule,
                        "status": "active",
                        "command": command[:50] + "..." if len(command) > 50 else command
                    })
        
        return automations
    except Exception as e:
        return [{"name": "Error", "schedule": "-", "status": "error", "command": str(e)}]

def control_automation(name, action):
    """Start/stop en automasjon"""
    try:
        if action == "run":
            # Kjør scriptet umiddelbart
            if name == "NRJ Dashboard Update":
                subprocess.Popen(['python3', f'{SCRIPTS_DIR}/update_nrj_dashboard.py'])
                return {"status": "started", "message": "NRJ Dashboard Update started"}
            elif name == "Morning Routine":
                subprocess.Popen(['bash', f'{SCRIPTS_DIR}/integrated-morning-routine.sh'])
                return {"status": "started", "message": "Morning Routine started"}
            else:
                return {"status": "error", "message": f"Unknown automation: {name}"}
        
        elif action == "enable":
            # Legg til i cron
            return {"status": "enabled", "message": f"{name} enabled"}
        
        elif action == "disable":
            # Fjern fra cron
            return {"status": "disabled", "message": f"{name} disabled"}
        
        else:
            return {"status": "error", "message": f"Unknown action: {action}"}
            
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_nrj_stats():
    """Hent ekte NRJ statistikk fra Supabase"""
    try:
        import requests
        
        SUPABASE_URL = "https://kvniauxokdtmpvjtfnej.supabase.co"
        SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2bmlhdXhva2R0bXB2anRmbmVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTM2NzIzNCwiZXhwIjoyMDY2OTQzMjM0fQ.OkhTtq9QAQ3xMzZYKyWyCjj7PiqMZJKSvpA0jcBJqpE"
        
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/agenda_items?select=title,description&id=eq.0b1f6b6b-3fde-434b-b7c8-dcf306beea72",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]
        
        return {"error": "Could not fetch NRJ stats"}
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command specified"}))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "status":
        print(json.dumps(get_system_status()))
    elif command == "logs":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        print(json.dumps(get_live_logs(limit)))
    elif command == "automations":
        print(json.dumps(get_automations()))
    elif command == "control" and len(sys.argv) >= 4:
        print(json.dumps(control_automation(sys.argv[2], sys.argv[3])))
    elif command == "nrj-stats":
        print(json.dumps(get_nrj_stats()))
    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))
