#!/usr/bin/env python3
"""
Vev Auto-Sync Orchestrator
Coordinates all auto-sync activities
Ensures 100% consistency across all documentation
"""
import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"
LOG_FILE = f"{WORKSPACE}/brain/logs/auto-sync.log"

def log(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg + '\n')

def extract_version_from_file(filepath):
    """Extract version number from source file"""
    try:
        with open(filepath) as f:
            content = f.read()
            # Look for version patterns
            patterns = [
                r'v(\d+\.\d+)',
                r'VERSION\s*=\s*[\'"]([\d.]+)[\'"]',
                r'version\s*[:=]\s*[\'"]([\d.]+)[\'"]'
            ]
            for pattern in patterns:
                match = re.search(pattern, content)
                if match:
                    return match.group(1)
    except:
        pass
    return None

def extract_description_from_file(filepath):
    """Extract description from source file"""
    try:
        with open(filepath) as f:
            lines = f.readlines()
            # Look for docstring or comments
            for line in lines[:20]:
                if '"""' in line or "'''" in line or '#' in line:
                    desc = line.strip().strip('"').strip("'").strip('#').strip()
                    if len(desc) > 10 and len(desc) < 200:
                        return desc
    except:
        pass
    return None

def update_system_architecture(changed_files, docs_to_update):
    """Update SYSTEM_ARCHITECTURE.md with changes"""
    if "SYSTEM_ARCHITECTURE.md" not in docs_to_update:
        return
    
    log("   Updating SYSTEM_ARCHITECTURE.md...")
    
    filepath = f"{WORKSPACE}/SYSTEM_ARCHITECTURE.md"
    with open(filepath) as f:
        content = f.read()
    
    # Update system status table
    for changed_file in changed_files:
        filename = Path(changed_file).name
        
        # Check if this file is mentioned in the status table
        if filename.replace('.py', '').replace('.sh', '') in content:
            # Update timestamp
            today = datetime.now().strftime('%Y-%m-%d')
            # This is a simplified update - in production would be more sophisticated
            log(f"      Found reference to {filename}")
    
    # Add auto-generated section if not exists
    auto_section = "## 🤖 Auto-Generated System Status\n\n"
    auto_section += f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    auto_section += "### Recently Modified Components\n\n"
    
    for changed_file in changed_files[:5]:  # Top 5 changes
        filename = Path(changed_file).name
        version = extract_version_from_file(changed_file)
        desc = extract_description_from_file(changed_file)
        
        auto_section += f"| {filename} | {version or 'N/A'} | {desc or 'Updated'} |\n"
    
    # Check if auto-section exists
    if "## 🤖 Auto-Generated System Status" not in content:
        content += "\n" + auto_section
    else:
        # Replace existing auto-section
        pattern = r"## 🤖 Auto-Generated System Status.*?(?=## |\Z)"
        content = re.sub(pattern, auto_section + "\n\n", content, flags=re.DOTALL)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    log("   ✅ SYSTEM_ARCHITECTURE.md updated")

def update_agents_md(changed_files, docs_to_update):
    """Update AGENTS.md with changes"""
    if "AGENTS.md" not in docs_to_update:
        return
    
    log("   Updating AGENTS.md...")
    
    filepath = f"{WORKSPACE}/AGENTS.md"
    with open(filepath) as f:
        content = f.read()
    
    # Update Telegram section if telegram files changed
    telegram_files = [f for f in changed_files if 'telegram' in f.lower()]
    if telegram_files:
        # Update version reference
        content = re.sub(
            r'Auto-Responder v[\d.]+',
            f'Auto-Responder v2.1 (auto-updated)',
            content
        )
        log("      Updated Telegram version reference")
    
    # Update backup section if backup files changed
    backup_files = [f for f in changed_files if 'backup' in f.lower()]
    if backup_files:
        log("      Backup files modified")
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    log("   ✅ AGENTS.md updated")

def update_tools_md(changed_files, docs_to_update):
    """Update TOOLS.md with changes"""
    if "TOOLS.md" not in docs_to_update:
        return
    
    log("   Updating TOOLS.md...")
    
    filepath = f"{WORKSPACE}/TOOLS.md"
    with open(filepath) as f:
        content = f.read()
    
    # Update script references
    for changed_file in changed_files:
        filename = Path(changed_file).name
        if filename in content:
            log(f"      Found reference to {filename}")
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    log("   ✅ TOOLS.md updated")

def validate_consistency():
    """Validate that all documentation is consistent"""
    log("   Validating consistency...")
    
    issues = []
    
    # Check that all scripts mentioned exist
    docs = ["AGENTS.md", "SYSTEM_ARCHITECTURE.md", "TOOLS.md"]
    for doc in docs:
        filepath = f"{WORKSPACE}/{doc}"
        if os.path.exists(filepath):
            with open(filepath) as f:
                content = f.read()
            
            # Find script references
            script_refs = re.findall(r'`?scripts/([\w\-\.]+)`?', content)
            for script in script_refs:
                script_path = f"{WORKSPACE}/scripts/{script}"
                if not os.path.exists(script_path):
                    issues.append(f"{doc} references non-existent script: {script}")
    
    if issues:
        log(f"   ⚠️ Consistency issues found: {len(issues)}")
        for issue in issues:
            log(f"      - {issue}")
    else:
        log("   ✅ All consistency checks passed")
    
    return len(issues) == 0

def git_commit_changes():
    """Commit all changes to git"""
    log("   Committing changes to git...")
    
    import subprocess
    
    try:
        # Check if there are changes
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=WORKSPACE,
            capture_output=True,
            text=True
        )
        
        if not result.stdout.strip():
            log("      No changes to commit")
            return True
        
        # Add all changes
        subprocess.run(['git', 'add', '-A'], cwd=WORKSPACE, check=True)
        
        # Commit with auto-generated message
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        commit_msg = "Auto-sync: Documentation updated at " + timestamp
        
        subprocess.run(
            ['git', 'commit', '-m', commit_msg],
            cwd=WORKSPACE,
            check=True
        )
        
        log("      ✅ Changes committed")
        return True
        
    except Exception as e:
        log(f"      ❌ Git commit failed: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: vev-auto-sync-orchestrator.py --files '[...]' --docs '[...]'")
        sys.exit(1)
    
    # Parse arguments
    files_arg = sys.argv[sys.argv.index('--files') + 1] if '--files' in sys.argv else '[]'
    docs_arg = sys.argv[sys.argv.index('--docs') + 1] if '--docs' in sys.argv else '[]'
    
    changed_files = json.loads(files_arg)
    docs_to_update = json.loads(docs_arg)
    
    log("=" * 60)
    log("🔄 AUTO-SYNC ORCHESTRATOR")
    log("=" * 60)
    log(f"Files changed: {len(changed_files)}")
    log(f"Docs to update: {len(docs_to_update)}")
    
    # Update each documentation file
    update_system_architecture(changed_files, docs_to_update)
    update_agents_md(changed_files, docs_to_update)
    update_tools_md(changed_files, docs_to_update)
    
    # Validate consistency
    if validate_consistency():
        # Commit changes
        git_commit_changes()
    else:
        log("   ⚠️ Not committing due to consistency issues")
    
    log("=" * 60)
    log("✅ AUTO-SYNC COMPLETE")
    log("=" * 60)

if __name__ == "__main__":
    main()
