#!/usr/bin/env python3
"""
💾 Auto-Backup System - Automatisk backup av kritisk data
"""

import os
import sys
import json
import shutil
import tarfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, '/root/.openclaw/workspace/scripts')

class AutoBackupSystem:
    """Automatisk backup av workspace data"""
    
    def __init__(self):
        self.workspace = Path('/root/.openclaw/workspace')
        self.backup_dir = self.workspace / 'brain' / 'backups'
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
    def get_backup_items(self) -> list:
        """Liste over hva som skal backupes"""
        return [
            ('scripts', self.workspace / 'scripts'),
            ('skills', self.workspace / 'skills'),
            ('docs', self.workspace / 'docs'),
            ('memory', self.workspace / 'memory'),
            ('brain', self.workspace / 'brain'),
            ('config', self.workspace / '.config'),
            ('root_files', [
                self.workspace / 'MEMORY.md',
                self.workspace / 'TOOLS.md',
                self.workspace / 'AGENTS.md',
                self.workspace / 'SOUL.md',
            ])
        ]
    
    def create_backup(self, backup_type='daily') -> Path:
        """Opprett backup arkiv"""
        
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        backup_name = f"backup-{backup_type}-{timestamp}.tar.gz"
        backup_path = self.backup_dir / backup_name
        
        print(f"📦 Creating backup: {backup_name}")
        
        with tarfile.open(backup_path, 'w:gz') as tar:
            for name, path in self.get_backup_items():
                if isinstance(path, list):
                    # Backup spesifikke filer
                    for file_path in path:
                        if file_path.exists():
                            arcname = f"root/{file_path.name}"
                            tar.add(file_path, arcname=arcname)
                            print(f"  ✅ Added: {file_path.name}")
                elif path.exists():
                    # Backup hele mapper
                    tar.add(path, arcname=name)
                    print(f"  ✅ Added: {name}/")
        
        # Lagre metadata
        meta = {
            'timestamp': timestamp,
            'type': backup_type,
            'size_bytes': backup_path.stat().st_size,
            'size_mb': round(backup_path.stat().st_size / (1024*1024), 2)
        }
        
        meta_path = backup_path.with_suffix('.json')
        with open(meta_path, 'w') as f:
            json.dump(meta, f, indent=2)
        
        print(f"✅ Backup created: {backup_path}")
        print(f"   Size: {meta['size_mb']} MB")
        
        return backup_path
    
    def cleanup_old_backups(self, keep_days=7):
        """Rydd gamle backups"""
        
        cutoff = datetime.now() - __import__('datetime').timedelta(days=keep_days)
        removed = 0
        
        for backup_file in self.backup_dir.glob('backup-*.tar.gz'):
            # Sjekk om det er en gammel backup
            try:
                # Parse timestamp fra filnavn
                timestamp_str = backup_file.stem.split('-')[2]
                file_date = datetime.strptime(timestamp_str, '%Y%m%d')
                
                if file_date < cutoff:
                    backup_file.unlink()
                    # Slett også metadata
                    meta_file = backup_file.with_suffix('.json')
                    if meta_file.exists():
                        meta_file.unlink()
                    removed += 1
                    print(f"  🗑️  Removed old backup: {backup_file.name}")
            except:
                pass
        
        print(f"✅ Cleaned up {removed} old backups")
        return removed
    
    def list_backups(self):
        """List alle backups"""
        
        backups = []
        for backup_file in self.backup_dir.glob('backup-*.tar.gz'):
            meta_file = backup_file.with_suffix('.json')
            if meta_file.exists():
                with open(meta_file, 'r') as f:
                    meta = json.load(f)
                backups.append({
                    'file': backup_file.name,
                    **meta
                })
        
        # Sorter etter dato
        backups.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return backups
    
    def print_backup_status(self):
        """Print backup status"""
        
        print("\n" + "=" * 60)
        print("💾 AUTO-BACKUP SYSTEM STATUS")
        print("=" * 60)
        
        backups = self.list_backups()
        
        print(f"\n📦 Total backups: {len(backups)}")
        print(f"📁 Backup directory: {self.backup_dir}")
        
        if backups:
            print("\n🕐 Recent backups:")
            for backup in backups[:5]:
                print(f"  • {backup['file']}")
                print(f"    Type: {backup['type']} | Size: {backup['size_mb']} MB")
                print(f"    Date: {backup['timestamp']}")
        
        # Beregn total størrelse
        total_size = sum(b['size_mb'] for b in backups)
        print(f"\n💾 Total backup size: {total_size:.1f} MB")
        
        print("=" * 60)


def main():
    """Main entry point"""
    backup = AutoBackupSystem()
    
    print("🚀 Starting auto-backup...\n")
    
    # Opprett backup
    backup_path = backup.create_backup('daily')
    
    # Rydd gamle backups
    print("\n🧹 Cleaning up old backups...")
    backup.cleanup_old_backups(keep_days=7)
    
    # Print status
    backup.print_backup_status()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
