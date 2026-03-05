#!/usr/bin/env python3
"""
Vev Task Manager
Integrates with Mission Control Kanban for automatic task fetching
"""
import os
import sys
import json
import time
import random
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"
TASKS_DB = f"{WORKSPACE}/brain/vev-tasks.json"
MISSION_CONTROL_API = "http://localhost:8765"
LOG_FILE = f"{WORKSPACE}/brain/logs/task-manager.log"

class VevTaskManager:
    """Manages Vev's tasks from Mission Control"""
    
    def __init__(self):
        self.tasks = []
        self.current_task = None
        self.load_tasks()
    
    def log(self, msg):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] {msg}"
        print(log_msg)
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, 'a') as f:
            f.write(log_msg + '\n')
    
    def load_tasks(self):
        """Load tasks from local database"""
        if os.path.exists(TASKS_DB):
            with open(TASKS_DB) as f:
                data = json.load(f)
                self.tasks = data.get('tasks', [])
                self.current_task = data.get('current_task')
        else:
            self.tasks = []
            self.current_task = None
    
    def save_tasks(self):
        """Save tasks to local database"""
        with open(TASKS_DB, 'w') as f:
            json.dump({
                'tasks': self.tasks,
                'current_task': self.current_task,
                'last_updated': datetime.now().isoformat()
            }, f, indent=2, default=str)
    
    def need_more_tasks(self):
        """Check if Vev needs more tasks"""
        active_tasks = [t for t in self.tasks if t.get('column_id') in ['research', 'write', 'review']]
        return len(active_tasks) < 3
    
    def suggest_task_creation(self):
        """Suggest creating new tasks when empty"""
        suggestions = [
            "🌅 Kjøre Morning Routine for å hente nye saker",
            "📊 Analysere NRJ Morgen statistikk",
            "🎙️ Forbedre Telegram Auto-Responder",
            "📚 Oppdatere dokumentasjon",
            "🔧 Vedlikeholde Mission Control",
            "📈 Lage ukentlig rapport",
            "🧠 Lære nye mønstre fra samtaler",
            "🎨 Forbedre design-system"
        ]
        return random.choice(suggestions)
    
    def get_status(self):
        """Get current status summary"""
        columns = {}
        for task in self.tasks:
            col = task.get('column_id', 'unknown')
            columns[col] = columns.get(col, 0) + 1
        
        return {
            'total_tasks': len(self.tasks),
            'current_task': self.current_task,
            'by_column': columns,
            'need_more': self.need_more_tasks()
        }

def main():
    manager = VevTaskManager()
    
    print("=" * 60)
    print("🎯 VEV TASK MANAGER")
    print("=" * 60)
    print()
    
    status = manager.get_status()
    print(f"Total tasks: {status['total_tasks']}")
    print(f"By column: {status['by_column']}")
    print(f"Need more: {status['need_more']}")
    
    if status['need_more']:
        print(f"\n💡 Suggestion: {manager.suggest_task_creation()}")

if __name__ == "__main__":
    main()
