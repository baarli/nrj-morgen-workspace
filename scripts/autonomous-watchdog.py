#!/usr/bin/env python3
"""
Autonomous Watchdog - Ensures I never stop working on Mission Control
Runs continuously and triggers new projects if idle
"""

import os
import sys
import time
import json
import subprocess
import random
from datetime import datetime, timedelta

class AutonomousWatchdog:
    def __init__(self):
        self.workspace = "/root/.openclaw/workspace"
        self.heartbeat_file = "/tmp/watchdog-heartbeat"
        self.project_log = f"{self.workspace}/.config/project-history.json"
        self.min_project_interval = 3600  # Minimum 1 hour between projects
        self.max_idle_time = 1800  # Start new project if idle for 30 minutes
        
    def log(self, message):
        """Log with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {message}")
        
        # Also log to file
        with open("/var/log/autonomous-watchdog.log", "a") as f:
            f.write(f"[{timestamp}] {message}\n")
    
    def update_heartbeat(self):
        """Update heartbeat timestamp"""
        with open(self.heartbeat_file, "w") as f:
            f.write(str(int(time.time())))
    
    def get_last_project_time(self):
        """Get timestamp of last project"""
        if os.path.exists(self.project_log):
            try:
                with open(self.project_log, "r") as f:
                    history = json.load(f)
                    if history.get("projects"):
                        return history["projects"][-1].get("timestamp", 0)
            except:
                pass
        return 0
    
    def record_project_start(self, project_name):
        """Record that a new project has started"""
        history = {"projects": []}
        if os.path.exists(self.project_log):
            try:
                with open(self.project_log, "r") as f:
                    history = json.load(f)
            except:
                pass
        
        history["projects"].append({
            "name": project_name,
            "timestamp": int(time.time()),
            "date": datetime.now().isoformat()
        })
        
        # Keep only last 100 projects
        history["projects"] = history["projects"][-100:]
        
        with open(self.project_log, "w") as f:
            json.dump(history, f, indent=2)
    
    def check_idle_time(self):
        """Check how long I've been idle"""
        if not os.path.exists(self.heartbeat_file):
            return float('inf')
        
        with open(self.heartbeat_file, "r") as f:
            last_heartbeat = int(f.read().strip())
        
        return time.time() - last_heartbeat
    
    def generate_new_project(self):
        """Generate and start a new project"""
        self.log("🚀 Generating new autonomous project")
        
        # List of possible project types
        projects = [
            {
                "name": "Performance Optimization",
                "description": "Optimize Mission Control performance and reduce load times",
                "priority": "high",
                "estimated_hours": 2
            },
            {
                "name": "UI/UX Improvements",
                "description": "Improve user interface and user experience",
                "priority": "medium",
                "estimated_hours": 3
            },
            {
                "name": "New Feature Implementation",
                "description": "Implement a new feature based on user needs",
                "priority": "high",
                "estimated_hours": 4
            },
            {
                "name": "Code Quality Improvements",
                "description": "Refactor code for better maintainability",
                "priority": "medium",
                "estimated_hours": 2
            },
            {
                "name": "Documentation Updates",
                "description": "Update and improve all documentation",
                "priority": "low",
                "estimated_hours": 1
            },
            {
                "name": "Security Enhancements",
                "description": "Improve security and add safeguards",
                "priority": "high",
                "estimated_hours": 2
            },
            {
                "name": "Analytics Improvements",
                "description": "Add new metrics and improve analytics",
                "priority": "medium",
                "estimated_hours": 3
            },
            {
                "name": "Integration Development",
                "description": "Integrate with new APIs or services",
                "priority": "medium",
                "estimated_hours": 4
            }
        ]
        
        # Select random project
        project = random.choice(projects)
        
        # Record project start
        self.record_project_start(project["name"])
        
        # Notify user
        self.notify_user(project)
        
        # Start implementation
        self.start_project_implementation(project)
        
        return project
    
    def notify_user(self, project):
        """Notify user about new project"""
        self.log(f"📢 Notifying user about new project: {project['name']}")
        
        notify_script = f"{self.workspace}/scripts/notify-user.sh"
        if os.path.exists(notify_script):
            subprocess.run([
                "bash", notify_script, "start",
                project["name"],
                project["description"],
                project["priority"],
                f"{project['estimated_hours']} hours"
            ])
    
    def start_project_implementation(self, project):
        """Start implementing the project"""
        self.log(f"🔧 Starting implementation: {project['name']}")
        
        # Run autonomous mission control script
        autonomous_script = f"{self.workspace}/scripts/autonomous-mission-control.sh"
        if os.path.exists(autonomous_script):
            subprocess.Popen(
                ["bash", autonomous_script],
                stdout=open("/tmp/project-implementation.log", "a"),
                stderr=subprocess.STDOUT,
                start_new_session=True
            )
    
    def check_system_health(self):
        """Check if all systems are healthy"""
        self.log("🏥 Checking system health")
        
        # Check API
        try:
            import urllib.request
            req = urllib.request.Request(
                "http://47.84.19.119:8081/api/status",
                timeout=5
            )
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    self.log("✅ API is healthy")
                else:
                    self.log(f"⚠️  API returned status {response.status}")
        except Exception as e:
            self.log(f"❌ API health check failed: {e}")
            # Try to restart API
            subprocess.Popen([
                "python3", 
                f"{self.workspace}/mission-control/api/total-control-api.py"
            ], stdout=open("/tmp/api-restart.log", "w"), stderr=subprocess.STDOUT)
    
    def run(self):
        """Main watchdog loop - runs forever"""
        self.log("🐕 Autonomous Watchdog starting - I will never stop working!")
        
        iteration = 0
        while True:
            iteration += 1
            self.log(f"--- Watchdog iteration #{iteration} ---")
            
            # Update heartbeat
            self.update_heartbeat()
            
            # Check system health
            self.check_system_health()
            
            # Check if I should start a new project
            idle_time = self.check_idle_time()
            last_project = self.get_last_project_time()
            time_since_last = time.time() - last_project
            
            self.log(f"Idle time: {idle_time:.0f}s, Time since last project: {time_since_last:.0f}s")
            
            # Start new project if:
            # 1. I've been idle for more than max_idle_time
            # 2. It's been more than min_project_interval since last project
            if idle_time > self.max_idle_time and time_since_last > self.min_project_interval:
                self.log("💡 Starting new project due to idle time")
                self.generate_new_project()
            elif time_since_last > self.min_project_interval * 2:
                self.log("💡 Starting new project - it's been a while")
                self.generate_new_project()
            else:
                self.log("✅ Working on existing tasks or too soon for new project")
            
            # Sleep for 5 minutes before next check
            self.log("💤 Sleeping for 5 minutes...")
            time.sleep(300)

if __name__ == "__main__":
    watchdog = AutonomousWatchdog()
    try:
        watchdog.run()
    except KeyboardInterrupt:
        watchdog.log("🛑 Watchdog stopped by user")
    except Exception as e:
        watchdog.log(f"💥 Watchdog crashed: {e}")
        # Restart ourselves
        time.sleep(10)
        os.execv(sys.executable, [sys.executable] + sys.argv)
