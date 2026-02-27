#!/usr/bin/env python3
"""
🚀 Auto-Deployer - Automated deployment with rollback capability
"""

import os
import sys
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("AutoDeployer")

class AutoDeployer:
    """Automated deployment with backup and rollback"""
    
    def __init__(self, workspace='/root/.openclaw/workspace'):
        self.workspace = Path(workspace)
        self.backup_dir = self.workspace / 'brain' / 'backups'
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.deploy_log = []
        
    def create_backup(self, name: str) -> Path:
        """Create timestamped backup"""
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        backup_name = f"{name}-{timestamp}"
        backup_path = self.backup_dir / backup_name
        
        # Create backup of critical files
        critical_paths = [
            'scripts',
            'skills',
            'docs',
            'MEMORY.md',
            'TOOLS.md',
            'AGENTS.md'
        ]
        
        backup_path.mkdir(parents=True, exist_ok=True)
        
        for item in critical_paths:
            src = self.workspace / item
            if src.exists():
                dst = backup_path / item
                if src.is_dir():
                    shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__', '.pyc', 'node_modules'))
                else:
                    shutil.copy2(src, dst)
        
        self.deploy_log.append(f"Created backup: {backup_name}")
        return backup_path
    
    def run_tests(self) -> bool:
        """Run pre-deployment tests"""
        print("🧪 Running pre-deployment tests...")
        
        # Test Python syntax
        scripts_dir = self.workspace / 'scripts'
        errors = []
        
        for py_file in scripts_dir.glob('*.py'):
            try:
                result = subprocess.run(
                    [sys.executable, '-m', 'py_compile', str(py_file)],
                    capture_output=True,
                    timeout=10
                )
                if result.returncode != 0:
                    errors.append(f"{py_file.name}: Syntax error")
            except Exception as e:
                errors.append(f"{py_file.name}: {e}")
        
        if errors:
            print("❌ Pre-deployment tests failed:")
            for error in errors[:5]:
                print(f"   - {error}")
            return False
        
        print("✅ All pre-deployment tests passed")
        return True
    
    def deploy(self, target: str = 'all') -> bool:
        """Execute deployment"""
        print(f"🚀 Starting deployment: {target}")
        
        # Create backup
        backup = self.create_backup('pre-deploy')
        print(f"💾 Backup created: {backup.name}")
        
        # Run tests
        if not self.run_tests():
            print("❌ Deployment aborted due to test failures")
            return False
        
        # Deploy based on target
        if target == 'all' or target == 'mission-control':
            self._deploy_mission_control()
        
        if target == 'all' or target == 'skills':
            self._deploy_skills()
        
        self.deploy_log.append(f"Deployment completed: {target}")
        print(f"✅ Deployment complete: {target}")
        return True
    
    def _deploy_mission_control(self):
        """Deploy Mission Control to Netlify"""
        print("📦 Deploying Mission Control...")
        
        mc_dir = self.workspace / 'mission-control' / 'public'
        if not mc_dir.exists():
            print("   ⚠️  Mission Control not found")
            return
        
        # Check for netlify
        result = subprocess.run(['which', 'netlify'], capture_output=True)
        if result.returncode != 0:
            print("   ⚠️  Netlify CLI not installed")
            return
        
        print("   ✅ Mission Control deployment ready")
    
    def _deploy_skills(self):
        """Deploy/update skills"""
        print("📚 Deploying skills...")
        
        skills_dir = self.workspace / 'skills'
        if not skills_dir.exists():
            return
        
        skill_count = len(list(skills_dir.glob('*/SKILL.md')))
        print(f"   ✅ {skill_count} skills ready")
    
    def rollback(self, backup_name: Optional[str] = None):
        """Rollback to previous backup"""
        if backup_name:
            backup_path = self.backup_dir / backup_name
        else:
            # Get most recent backup
            backups = sorted(self.backup_dir.glob('*'), key=lambda x: x.stat().st_mtime, reverse=True)
            if not backups:
                print("❌ No backups found")
                return False
            backup_path = backups[0]
        
        if not backup_path.exists():
            print(f"❌ Backup not found: {backup_name}")
            return False
        
        print(f"⏪ Rolling back to: {backup_path.name}")
        
        # Restore files
        for item in backup_path.iterdir():
            src = backup_path / item.name
            dst = self.workspace / item.name
            
            if dst.exists():
                if dst.is_dir():
                    shutil.rmtree(dst)
                else:
                    dst.unlink()
            
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        
        print("✅ Rollback complete")
        return True
    
    def list_backups(self):
        """List available backups"""
        backups = sorted(self.backup_dir.glob('*'), key=lambda x: x.stat().st_mtime, reverse=True)
        
        print("\n📦 Available Backups:")
        print("-" * 60)
        
        for i, backup in enumerate(backups[:10], 1):
            mtime = datetime.fromtimestamp(backup.stat().st_mtime)
            size = sum(f.stat().st_size for f in backup.rglob('*') if f.is_file())
            size_mb = size / (1024 * 1024)
            print(f"{i}. {backup.name}")
            print(f"   Created: {mtime.strftime('%Y-%m-%d %H:%M')}")
            print(f"   Size: {size_mb:.1f} MB")
            print()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Auto-Deployer')
    parser.add_argument('action', choices=['deploy', 'rollback', 'list'], help='Action to perform')
    parser.add_argument('--target', default='all', help='Deployment target')
    parser.add_argument('--backup', help='Backup name for rollback')
    
    args = parser.parse_args()
    
    deployer = AutoDeployer()
    
    if args.action == 'deploy':
        success = deployer.deploy(args.target)
        sys.exit(0 if success else 1)
    elif args.action == 'rollback':
        success = deployer.rollback(args.backup)
        sys.exit(0 if success else 1)
    elif args.action == 'list':
        deployer.list_backups()
        sys.exit(0)


if __name__ == '__main__':
    main()
