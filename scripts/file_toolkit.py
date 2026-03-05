#!/usr/bin/env python3
"""
📁 BAARLICLAW FILE TOOLKIT
Avansert filhåndtering og -organisering
"""

import os
import sys
import shutil
import hashlib
import json
from typing import List, Dict, Optional, Tuple, Callable
from pathlib import Path
from datetime import datetime, timedelta
import mimetypes

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("FileToolkit")

class FileManager:
    """Advanced file management"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
    
    def list_files(self, pattern: str = "*", 
                   recursive: bool = False) -> List[Dict]:
        """List files with metadata"""
        files = []
        
        if recursive:
            iterator = self.base_path.rglob(pattern)
        else:
            iterator = self.base_path.glob(pattern)
        
        for path in iterator:
            if path.is_file():
                stat = path.stat()
                files.append({
                    "path": str(path),
                    "name": path.name,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "extension": path.suffix.lower(),
                    "mime_type": mimetypes.guess_type(str(path))[0] or "unknown"
                })
        
        return sorted(files, key=lambda x: x["modified"], reverse=True)
    
    def find_duplicates(self) -> List[List[str]]:
        """Find duplicate files by hash"""
        hashes: Dict[str, List[str]] = {}
        
        for path in self.base_path.rglob("*"):
            if path.is_file():
                file_hash = self._hash_file(str(path))
                if file_hash:
                    hashes.setdefault(file_hash, []).append(str(path))
        
        # Return only groups with duplicates
        return [paths for paths in hashes.values() if len(paths) > 1]
    
    def _hash_file(self, filepath: str, block_size: int = 65536) -> Optional[str]:
        """Calculate MD5 hash of file"""
        try:
            hasher = hashlib.sha256()
            with open(filepath, 'rb') as f:
                for block in iter(lambda: f.read(block_size), b''):
                    hasher.update(block)
            return hasher.hexdigest()
        except Exception as e:
            logger.error(f"Failed to hash {filepath}: {e}")
            return None
    
    def organize_by_date(self, source_dir: str, dest_dir: str,
                        date_format: str = "%Y/%m"):
        """Organize files by modification date"""
        source = Path(source_dir)
        dest = Path(dest_dir)
        
        moved = 0
        for path in source.rglob("*"):
            if path.is_file():
                stat = path.stat()
                date = datetime.fromtimestamp(stat.st_mtime)
                date_folder = date.strftime(date_format)
                
                target_dir = dest / date_folder
                target_dir.mkdir(parents=True, exist_ok=True)
                
                target_path = target_dir / path.name
                shutil.move(str(path), str(target_path))
                moved += 1
        
        logger.info(f"Organized {moved} files by date")
        return moved
    
    def organize_by_type(self, source_dir: str, dest_dir: str):
        """Organize files by type/extension"""
        source = Path(source_dir)
        dest = Path(dest_dir)
        
        type_mapping = {
            "images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"],
            "videos": [".mp4", ".avi", ".mov", ".mkv", ".webm"],
            "audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
            "documents": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
            "data": [".json", ".csv", ".xml", ".yaml", ".yml"],
            "archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c"]
        }
        
        moved = 0
        for path in source.rglob("*"):
            if path.is_file():
                ext = path.suffix.lower()
                
                # Find category
                category = "other"
                for cat, extensions in type_mapping.items():
                    if ext in extensions:
                        category = cat
                        break
                
                target_dir = dest / category
                target_dir.mkdir(parents=True, exist_ok=True)
                
                target_path = target_dir / path.name
                shutil.move(str(path), str(target_path))
                moved += 1
        
        logger.info(f"Organized {moved} files by type")
        return moved
    
    def clean_old_files(self, days: int = 30, 
                       pattern: str = "*",
                       dry_run: bool = True) -> List[str]:
        """Find or delete old files"""
        cutoff = datetime.now() - timedelta(days=days)
        to_delete = []
        
        for path in self.base_path.rglob(pattern):
            if path.is_file():
                stat = path.stat()
                modified = datetime.fromtimestamp(stat.st_mtime)
                
                if modified < cutoff:
                    to_delete.append(str(path))
                    
                    if not dry_run:
                        path.unlink()
                        logger.info(f"Deleted: {path}")
        
        if dry_run:
            logger.info(f"Found {len(to_delete)} files older than {days} days (dry run)")
        else:
            logger.info(f"Deleted {len(to_delete)} files")
        
        return to_delete
    
    def sync_directories(self, source: str, dest: str, 
                        delete: bool = False) -> Dict:
        """Sync two directories"""
        source_path = Path(source)
        dest_path = Path(dest)
        
        stats = {"copied": 0, "updated": 0, "deleted": 0, "skipped": 0}
        
        # Copy/update files
        for src_file in source_path.rglob("*"):
            if src_file.is_file():
                rel_path = src_file.relative_to(source_path)
                dst_file = dest_path / rel_path
                
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                
                if not dst_file.exists():
                    shutil.copy2(str(src_file), str(dst_file))
                    stats["copied"] += 1
                elif src_file.stat().st_mtime > dst_file.stat().st_mtime:
                    shutil.copy2(str(src_file), str(dst_file))
                    stats["updated"] += 1
                else:
                    stats["skipped"] += 1
        
        # Delete extra files if requested
        if delete:
            for dst_file in dest_path.rglob("*"):
                if dst_file.is_file():
                    rel_path = dst_file.relative_to(dest_path)
                    src_file = source_path / rel_path
                    
                    if not src_file.exists():
                        dst_file.unlink()
                        stats["deleted"] += 1
        
        logger.info(f"Sync complete: {stats}")
        return stats
    
    def get_directory_size(self, path: Optional[str] = None) -> int:
        """Get total size of directory"""
        target = Path(path) if path else self.base_path
        total = 0
        
        for entry in target.rglob("*"):
            if entry.is_file():
                total += entry.stat().st_size
        
        return total
    
    def format_size(self, size_bytes: int) -> str:
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    def create_backup(self, backup_dir: str, 
                     exclude_patterns: Optional[List[str]] = None):
        """Create timestamped backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = Path(backup_dir) / f"backup_{timestamp}"
        
        exclude_patterns = exclude_patterns or []
        
        copied = 0
        for src_file in self.base_path.rglob("*"):
            if src_file.is_file():
                # Check exclusions
                if any(pattern in str(src_file) for pattern in exclude_patterns):
                    continue
                
                rel_path = src_file.relative_to(self.base_path)
                dst_file = backup_path / rel_path
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                
                shutil.copy2(str(src_file), str(dst_file))
                copied += 1
        
        logger.info(f"Backup created: {backup_path} ({copied} files)")
        return str(backup_path)

class FileWatcher:
    """Watch files for changes"""
    
    def __init__(self, path: str):
        self.path = Path(path)
        self.callbacks: List[Callable] = []
        self._state: Dict[str, float] = {}
        self._running = False
    
    def on_change(self, callback: Callable):
        """Register callback for file changes"""
        self.callbacks.append(callback)
    
    def scan(self) -> List[Dict]:
        """Scan for changes"""
        changes = []
        current_state = {}
        
        for path in self.path.rglob("*"):
            if path.is_file():
                stat = path.stat()
                mtime = stat.st_mtime
                current_state[str(path)] = mtime
                
                if str(path) in self._state:
                    if self._state[str(path)] != mtime:
                        changes.append({
                            "type": "modified",
                            "path": str(path)
                        })
                else:
                    changes.append({
                        "type": "created",
                        "path": str(path)
                    })
        
        # Check for deletions
        for old_path in self._state:
            if old_path not in current_state:
                changes.append({
                    "type": "deleted",
                    "path": old_path
                })
        
        self._state = current_state
        return changes

# === CONVENIENCE FUNCTIONS ===
def quick_find(pattern: str, path: str = ".") -> List[str]:
    """Quick file find"""
    fm = FileManager(path)
    files = fm.list_files(pattern, recursive=True)
    return [f["path"] for f in files]

def quick_backup(source: str, dest: str):
    """Quick backup"""
    fm = FileManager(source)
    return fm.create_backup(dest)

def find_large_files(min_size_mb: int = 100, path: str = ".") -> List[Dict]:
    """Find large files"""
    fm = FileManager(path)
    files = fm.list_files(recursive=True)
    min_bytes = min_size_mb * 1024 * 1024
    return [f for f in files if f["size"] > min_bytes]

# === TESTING ===
if __name__ == "__main__":
    print("📁 BaarliClaw File Toolkit - Testing")
    print("=" * 50)
    
    # Create test directory
    test_dir = "/tmp/file_toolkit_test"
    os.makedirs(test_dir, exist_ok=True)
    
    # Create some test files
    for i in range(5):
        with open(f"{test_dir}/file_{i}.txt", "w") as f:
            f.write(f"Content {i}")
    
    fm = FileManager(test_dir)
    
    # Test list
    print("\n🧪 Testing list_files")
    files = fm.list_files()
    print(f"✅ Found {len(files)} files")
    
    # Test size formatting
    print("\n🧪 Testing format_size")
    print(f"✅ 1024 bytes = {fm.format_size(1024)}")
    print(f"✅ 1048576 bytes = {fm.format_size(1048576)}")
    
    # Test directory size
    print("\n🧪 Testing directory size")
    size = fm.get_directory_size()
    print(f"✅ Total size: {fm.format_size(size)}")
    
    # Test find duplicates
    print("\n🧪 Testing find_duplicates")
    # Create a duplicate
    shutil.copy(f"{test_dir}/file_0.txt", f"{test_dir}/file_0_copy.txt")
    duplicates = fm.find_duplicates()
    print(f"✅ Found {len(duplicates)} duplicate groups")
    
    # Cleanup
    shutil.rmtree(test_dir)
    
    print("\n✅ File Toolkit ready!")
