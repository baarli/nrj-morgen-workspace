#!/usr/bin/env python3
"""
Vev Auto-Learning Detection System v2.0
Automatically detects learning from session activity
NO manual input required
"""
import os
import sys
import json
import subprocess
import hashlib
from datetime import datetime
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"
LEARNING_DB = f"{WORKSPACE}/brain/learning-database.json"
SESSION_LOG = f"{WORKSPACE}/brain/session-activity.json"

def ensure_dirs():
    os.makedirs(os.path.dirname(LEARNING_DB), exist_ok=True)
    os.makedirs(os.path.dirname(SESSION_LOG), exist_ok=True)

def load_json(path, default=None):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default if default is not None else {}

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def get_recent_files_changed(minutes=60):
    """Detect files changed in last N minutes"""
    try:
        result = subprocess.run(
            ["find", WORKSPACE, "-type", "f", "-mmin", f"-{minutes}", 
             "!", "-path", "*/node_modules/*", "!", "-path", "*/.git/*"],
            capture_output=True, text=True, timeout=30
        )
        files = [f for f in result.stdout.strip().split('\n') if f]
        return files[:50]  # Limit to 50 files
    except Exception as e:
        return []

def detect_learning():
    """Main learning detection function"""
    ensure_dirs()
    
    files_changed = get_recent_files_changed(minutes=120)
    
    if not files_changed:
        return None
    
    # Categorize files
    types = {"python": [], "shell": [], "markdown": [], "config": [], "other": []}
    for f in files_changed:
        if f.endswith('.py'): types["python"].append(f)
        elif f.endswith('.sh'): types["shell"].append(f)
        elif f.endswith('.md'): types["markdown"].append(f)
        elif f.endswith(('.json', '.yaml', '.yml', '.toml')): types["config"].append(f)
        else: types["other"].append(f)
    
    # Auto-generate learnings
    learnings = []
    if types['python']:
        learnings.append(f"Worked with Python: {len(types['python'])} files")
    if types['shell']:
        learnings.append(f"Created shell scripts: {len(types['shell'])} files")
    if types['markdown']:
        learnings.append(f"Updated documentation: {len(types['markdown'])} files")
    
    # Save to database
    db = load_json(LEARNING_DB, {"sessions": [], "learnings": []})
    
    session_entry = {
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime('%Y-%m-%d'),
        "files_changed": len(files_changed),
        "learnings": learnings
    }
    
    db["sessions"].append(session_entry)
    db["learnings"].extend([{
        "text": l,
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime('%Y-%m-%d')
    } for l in learnings])
    
    save_json(LEARNING_DB, db)
    
    return session_entry

if __name__ == "__main__":
    result = detect_learning()
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("No recent activity detected")
