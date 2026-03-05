#!/usr/bin/env python3
"""
Vev Auto-Learning Capture
Kjører automatisk etter hver samtale
Dokumenterer læring, feil, og innsikter
"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"
LEARNING_DB = f"{WORKSPACE}/brain/learning-database.json"
DAILY_LOG = f"{WORKSPACE}/memory/{datetime.now().strftime('%Y-%m-%d')}.md"
DIARY_DIR = f"{WORKSPACE}/brain/diary"

def ensure_dirs():
    os.makedirs(os.path.dirname(LEARNING_DB), exist_ok=True)
    os.makedirs(os.path.dirname(DAILY_LOG), exist_ok=True)
    os.makedirs(DIARY_DIR, exist_ok=True)

def load_learning_db():
    if os.path.exists(LEARNING_DB):
        with open(LEARNING_DB) as f:
            return json.load(f)
    return {"learnings": [], "errors": [], "insights": [], "patterns": []}

def save_learning_db(db):
    with open(LEARNING_DB, 'w') as f:
        json.dump(db, f, indent=2, default=str)

def capture_learning():
    ensure_dirs()
    db = load_learning_db()
    
    print("=" * 60)
    print("🧠 AUTO-LEARNING CAPTURE")
    print("=" * 60)
    print()
    
    # Auto-detect from recent activity
    print("📊 Analyzing recent activity...")
    
    # Check for modified files
    recent_files = []
    try:
        import subprocess
        result = subprocess.run(
            ["find", WORKSPACE, "-name", "*.py", "-o", "-name", "*.sh", "-o", "-name", "*.md"],
            capture_output=True, text=True, timeout=10
        )
        files = result.stdout.strip().split('\n')[:20]
        recent_files = [f for f in files if f and 'node_modules' not in f][:10]
    except:
        pass
    
    # Build learning entry
    learning_entry = {
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime('%Y-%m-%d'),
        "files_modified": recent_files,
        "learnings": [],
        "errors": [],
        "insights": []
    }
    
    print("💡 What did you learn in this session?")
    print("   (Press Enter with empty line when done)")
    while True:
        learning = input("   > ").strip()
        if not learning:
            break
        learning_entry["learnings"].append(learning)
        db["learnings"].append({
            "text": learning,
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime('%Y-%m-%d')
        })
    
    print()
    print("❌ Any mistakes or errors?")
    print("   (Press Enter with empty line when done)")
    while True:
        error = input("   > ").strip()
        if not error:
            break
        learning_entry["errors"].append(error)
        db["errors"].append({
            "text": error,
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime('%Y-%m-%d')
        })
    
    print()
    print("🔍 Any insights or observations?")
    print("   (Press Enter with empty line when done)")
    while True:
        insight = input("   > ").strip()
        if not insight:
            break
        learning_entry["insights"].append(insight)
        db["insights"].append({
            "text": insight,
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime('%Y-%m-%d')
        })
    
    # Save to database
    save_learning_db(db)
    
    # Append to daily log
    with open(DAILY_LOG, 'a') as f:
        f.write(f"\n## Learning Capture ({datetime.now().strftime('%H:%M')})\n\n")
        if learning_entry["learnings"]:
            f.write("### Learnings\n")
            for l in learning_entry["learnings"]:
                f.write(f"- {l}\n")
            f.write("\n")
        if learning_entry["errors"]:
            f.write("### Mistakes\n")
            for e in learning_entry["errors"]:
                f.write(f"- {e}\n")
            f.write("\n")
        if learning_entry["insights"]:
            f.write("### Insights\n")
            for i in learning_entry["insights"]:
                f.write(f"- {i}\n")
            f.write("\n")
    
    print()
    print("=" * 60)
    print(f"✅ Learning captured!")
    print(f"   📁 Database: {LEARNING_DB}")
    print(f"   📝 Daily log: {DAILY_LOG}")
    print(f"   📊 Total learnings: {len(db['learnings'])}")
    print(f"   ❌ Total errors: {len(db['errors'])}")
    print(f"   🔍 Total insights: {len(db['insights'])}")
    print("=" * 60)

if __name__ == "__main__":
    capture_learning()
