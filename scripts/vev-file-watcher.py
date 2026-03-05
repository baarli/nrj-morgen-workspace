#!/usr/bin/env python3
"""
Vev File System Watcher
Monitors ALL files for changes and triggers auto-sync
24/7 operation with dependency mapping
"""
import os
import sys
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
import subprocess

WORKSPACE = "/root/.openclaw/workspace"
STATE_FILE = f"{WORKSPACE}/.vev-file-watcher-state.json"
DEPENDENCY_MAP = f"{WORKSPACE}/brain/config/file-dependencies.json"
LOG_FILE = f"{WORKSPACE}/brain/logs/file-watcher.log"

def log(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg + '\n')

def load_dependency_map():
    """Load which files affect which documentation"""
    default_map = {
        "scripts/vev-telegram-auto-responder.py": {
            "docs": ["AGENTS.md", "SYSTEM_ARCHITECTURE.md", "TOOLS.md"],
            "keywords": ["Telegram", "Auto-Responder"],
            "extract_version": True
        },
        "scripts/vev-learning-loop.sh": {
            "docs": ["SYSTEM_ARCHITECTURE.md", "AGENTS.md"],
            "keywords": ["Learning", "Auto-detect"],
            "extract_version": False
        },
        "scripts/vev-nightly-github-backup.sh": {
            "docs": ["SYSTEM_ARCHITECTURE.md", "AGENTS.md", "TOOLS.md"],
            "keywords": ["Backup", "GitHub"],
            "extract_version": False
        },
        "scripts/vev-preflight.py": {
            "docs": ["SYSTEM_ARCHITECTURE.md"],
            "keywords": ["Pre-flight", "Context"],
            "extract_version": True
        },
        "skills/*/SKILL.md": {
            "docs": ["SYSTEM_ARCHITECTURE.md"],
            "keywords": ["Skills"],
            "extract_version": False
        }
    }
    
    if os.path.exists(DEPENDENCY_MAP):
        with open(DEPENDENCY_MAP) as f:
            return json.load(f)
    return default_map

def get_file_hash(filepath):
    """Get MD5 hash of file content"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def scan_all_files():
    """Scan workspace for all relevant files"""
    files = {}
    
    # Python scripts
    for f in Path(WORKSPACE).glob("scripts/*.py"):
        files[str(f)] = get_file_hash(f)
    
    # Shell scripts
    for f in Path(WORKSPACE).glob("scripts/*.sh"):
        files[str(f)] = get_file_hash(f)
    
    # Skills
    for f in Path(WORKSPACE).glob("skills/*/SKILL.md"):
        files[str(f)] = get_file_hash(f)
    
    # Main docs
    for doc in ["AGENTS.md", "SYSTEM_ARCHITECTURE.md", "TOOLS.md", "MEMORY.md"]:
        f = Path(WORKSPACE) / doc
        if f.exists():
            files[str(f)] = get_file_hash(f)
    
    return files

def detect_changes(old_state, new_state):
    """Detect what files changed"""
    changes = []
    
    for filepath, new_hash in new_state.items():
        old_hash = old_state.get(filepath)
        if old_hash != new_hash:
            changes.append(filepath)
    
    return changes

def determine_docs_to_update(changed_files, dependency_map):
    """Determine which documentation files need updating"""
    docs_to_update = set()
    
    for changed_file in changed_files:
        # Check direct matches
        for pattern, info in dependency_map.items():
            if pattern in changed_file or Path(changed_file).match(pattern):
                docs_to_update.update(info.get("docs", []))
    
    return list(docs_to_update)

def trigger_auto_sync(changed_files, docs_to_update):
    """Trigger the auto-sync process"""
    log(f"🔄 Triggering auto-sync for {len(changed_files)} changed files")
    log(f"   Files: {', '.join(Path(f).name for f in changed_files)}")
    log(f"   Docs to update: {', '.join(docs_to_update)}")
    
    # Call the auto-sync orchestrator
    sync_script = f"{WORKSPACE}/scripts/vev-auto-sync-orchestrator.py"
    if os.path.exists(sync_script):
        try:
            result = subprocess.run(
                [sys.executable, sync_script, 
                 '--files', json.dumps(changed_files),
                 '--docs', json.dumps(docs_to_update)],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                log("   ✅ Auto-sync completed successfully")
            else:
                log(f"   ⚠️ Auto-sync had issues: {result.stderr}")
        except Exception as e:
            log(f"   ❌ Auto-sync failed: {e}")

def main():
    log("=" * 60)
    log("👁️ VEV FILE WATCHER STARTED")
    log("=" * 60)
    log("Monitoring all files for changes...")
    
    dependency_map = load_dependency_map()
    
    # Load previous state
    old_state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            old_state = json.load(f)
    
    scan_count = 0
    
    try:
        while True:
            scan_count += 1
            new_state = scan_all_files()
            
            # Detect changes
            changes = detect_changes(old_state, new_state)
            
            if changes:
                log(f"\n🔍 Scan #{scan_count}: Detected {len(changes)} change(s)")
                
                # Determine what docs need updating
                docs_to_update = determine_docs_to_update(changes, dependency_map)
                
                if docs_to_update:
                    trigger_auto_sync(changes, docs_to_update)
                else:
                    log("   No documentation updates needed")
                
                # Save new state
                with open(STATE_FILE, 'w') as f:
                    json.dump(new_state, f, indent=2)
                
                old_state = new_state
            
            # Wait before next scan
            time.sleep(30)  # Check every 30 seconds
            
    except KeyboardInterrupt:
        log("\n🛑 File watcher stopped")
    except Exception as e:
        log(f"\n❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()
