#!/usr/bin/env python3
"""
🧹 System Cleaner - Automated cleanup of temporary files and logs
"""

import os
import sys
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("SystemCleaner")

class SystemCleaner:
    """Clean up temporary files, old logs, and cache"""
    
    def __init__(self, workspace='/root/.openclaw/workspace'):
        self.workspace = Path(workspace)
        self.stats = {
            'files_removed': 0,
            'bytes_freed': 0,
            'directories_cleaned': 0
        }
        
    def clean_temp_files(self, days=7) -> Dict:
        """Clean temporary files older than N days"""
        temp_dirs = [
            Path('/tmp'),
            self.workspace / 'tmp',
            self.workspace / '.cache'
        ]
        
        cutoff = datetime.now() - timedelta(days=days)
        
        for temp_dir in temp_dirs:
            if not temp_dir.exists():
                continue
                
            for item in temp_dir.iterdir():
                try:
                    if item.is_file():
                        mtime = datetime.fromtimestamp(item.stat().st_mtime)
                        if mtime < cutoff:
                            size = item.stat().st_size
                            item.unlink()
                            self.stats['files_removed'] += 1
                            self.stats['bytes_freed'] += size
                            
                    elif item.is_dir() and item.name not in ['.git', '__pycache__']:
                        # Check if directory is empty after cleaning
                        self._clean_directory(item, cutoff)
                        
                except Exception as e:
                    logger.warning(f"Could not remove {item}: {e}")
        
        return self.stats
    
    def _clean_directory(self, directory: Path, cutoff: datetime):
        """Clean files in directory older than cutoff"""
        try:
            for item in directory.rglob('*'):
                if item.is_file():
                    mtime = datetime.fromtimestamp(item.stat().st_mtime)
                    if mtime < cutoff:
                        try:
                            size = item.stat().st_size
                            item.unlink()
                            self.stats['files_removed'] += 1
                            self.stats['bytes_freed'] += size
                        except:
                            pass
        except:
            pass
    
    def clean_old_logs(self, days=30) -> Dict:
        """Clean log files older than N days"""
        log_dirs = [
            Path('/var/log'),
            self.workspace / 'logs',
            self.workspace / 'brain' / 'logs'
        ]
        
        cutoff = datetime.now() - timedelta(days=days)
        
        for log_dir in log_dirs:
            if not log_dir.exists():
                continue
                
            for log_file in log_dir.glob('*.log*'):
                try:
                    mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                    if mtime < cutoff:
                        size = log_file.stat().st_size
                        log_file.unlink()
                        self.stats['files_removed'] += 1
                        self.stats['bytes_freed'] += size
                except Exception as e:
                    logger.warning(f"Could not remove {log_file}: {e}")
        
        return self.stats
    
    def clean_pycache(self) -> Dict:
        """Clean Python cache directories"""
        for root, dirs, files in os.walk(self.workspace):
            for dir_name in dirs:
                if dir_name == '__pycache__':
                    pycache_path = Path(root) / dir_name
                    try:
                        size = sum(f.stat().st_size for f in pycache_path.rglob('*') if f.is_file())
                        shutil.rmtree(pycache_path)
                        self.stats['directories_cleaned'] += 1
                        self.stats['bytes_freed'] += size
                    except Exception as e:
                        logger.warning(f"Could not remove {pycache_path}: {e}")
        
        return self.stats
    
    def clean_old_backups(self, keep=10) -> Dict:
        """Keep only N most recent backups"""
        backup_dir = self.workspace / 'brain' / 'backups'
        
        if not backup_dir.exists():
            return self.stats
        
        backups = sorted(backup_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
        
        for old_backup in backups[keep:]:
            try:
                size = sum(f.stat().st_size for f in old_backup.rglob('*') if f.is_file())
                shutil.rmtree(old_backup)
                self.stats['directories_cleaned'] += 1
                self.stats['bytes_freed'] += size
            except Exception as e:
                logger.warning(f"Could not remove {old_backup}: {e}")
        
        return self.stats
    
    def run_all(self) -> Dict:
        """Run all cleanup operations"""
        print("🧹 Starting system cleanup...")
        
        print("  Cleaning temporary files...")
        self.clean_temp_files()
        
        print("  Cleaning old logs...")
        self.clean_old_logs()
        
        print("  Cleaning Python cache...")
        self.clean_pycache()
        
        print("  Cleaning old backups...")
        self.clean_old_backups()
        
        return self.stats
    
    def print_summary(self):
        """Print cleanup summary"""
        print("\n" + "=" * 60)
        print("🧹 SYSTEM CLEANUP SUMMARY")
        print("=" * 60)
        
        print(f"\n📊 Results:")
        print(f"   Files removed: {self.stats['files_removed']}")
        print(f"   Directories cleaned: {self.stats['directories_cleaned']}")
        
        bytes_mb = self.stats['bytes_freed'] / (1024 * 1024)
        print(f"   Space freed: {bytes_mb:.2f} MB")
        
        print("=" * 60)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='System Cleaner')
    parser.add_argument('--temp-days', type=int, default=7, help='Days to keep temp files')
    parser.add_argument('--log-days', type=int, default=30, help='Days to keep logs')
    parser.add_argument('--backups', type=int, default=10, help='Number of backups to keep')
    
    args = parser.parse_args()
    
    cleaner = SystemCleaner()
    cleaner.run_all()
    cleaner.print_summary()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
