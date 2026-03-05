#!/usr/bin/env python3
"""
Vev Proactive Suggester
Foreslår handlinger basert på systemtilstand
"""
import os
import sys
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"
LAST_CHECK_FILE = f"{WORKSPACE}/.vev-last-proactive-check"

def check_email():
    """Check for unread emails"""
    try:
        # This would integrate with gmail skill
        return None  # Placeholder
    except:
        return None

def check_backup_status():
    """Check when last backup was done"""
    try:
        backup_marker = f"{WORKSPACE}/.last-backup"
        if os.path.exists(backup_marker):
            mtime = os.path.getmtime(backup_marker)
            hours_ago = (datetime.now().timestamp() - mtime) / 3600
            if hours_ago > 24:
                return f"Last backup was {hours_ago:.0f} hours ago"
        return None
    except:
        return None

def check_disk_space():
    """Check disk usage"""
    try:
        result = subprocess.run(['df', '/'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            usage = lines[1].split()[4].replace('%', '')
            if int(usage) > 80:
                return f"Disk usage is {usage}%"
        return None
    except:
        return None

def check_git_status():
    """Check for uncommitted changes"""
    try:
        result = subprocess.run(
            ['git', '-C', WORKSPACE, 'status', '--porcelain'],
            capture_output=True, text=True
        )
        if result.stdout.strip():
            lines = result.stdout.strip().split('\n')
            return f"{len(lines)} uncommitted changes"
        return None
    except:
        return None

def check_cron_jobs():
    """Check if cron jobs are running"""
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        jobs = [l for l in result.stdout.split('\n') if l.strip() and not l.startswith('#')]
        return f"{len(jobs)} cron jobs configured" if jobs else None
    except:
        return None

def proactive_check():
    print("=" * 60)
    print("🔔 PROACTIVE SUGGESTIONS")
    print("=" * 60)
    print()
    
    suggestions = []
    
    # Check various systems
    checks = [
        ("💾 Backup", check_backup_status()),
        ("💽 Disk", check_disk_space()),
        ("📁 Git", check_git_status()),
        ("⏰ Cron", check_cron_jobs()),
    ]
    
    for label, result in checks:
        if result:
            suggestions.append((label, result))
    
    # Time-based suggestions
    hour = datetime.now().hour
    weekday = datetime.now().weekday()
    
    if hour == 4 and weekday < 5:
        suggestions.append(("🌅 Morning", "It's early morning - time for NRJ Morning Routine?"))
    
    if hour == 23:
        suggestions.append(("🌙 Evening", "End of day - remember to log learnings!"))
    
    if weekday == 6 and hour == 21:
        suggestions.append(("📅 Sunday", "Sunday evening - weekly review time?"))
    
    if suggestions:
        print("💡 Based on system status:")
        print()
        for label, suggestion in suggestions:
            print(f"   {label}: {suggestion}")
        print()
        print("Run the suggested action or type 'skip' to dismiss.")
    else:
        print("✅ All systems look good!")
        print("   No proactive suggestions at this time.")
    
    # Update last check
    with open(LAST_CHECK_FILE, 'w') as f:
        f.write(datetime.now().isoformat())
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    proactive_check()
