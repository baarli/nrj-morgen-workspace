#!/usr/bin/env python3
"""
💾 BAARLICLAW SMART BACKUP SERVICE
Automatisk backup med versjonering og deduplisering
"""

import sys
import os
import json
import shutil
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

sys.path.insert(0, '/root/.openclaw/workspace/scripts')

from baarliclaw_toolkit import setup_logging
from date_toolkit import DateUtils
from uuid_toolkit import UUIDUtils
from cli_toolkit import TerminalUI, Colors

logger = setup_logging("smart-backup")

@dataclass
class BackupEntry:
    """En backup-post"""
    id: str
    source_path: str
    backup_path: str
    timestamp: str
    size_bytes: int
    checksum: str
    version: int
    is_incremental: bool = False
    parent_version: Optional[int] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)

class SmartBackupService:
    """Smart backup-tjeneste"""
    
    def __init__(self, backup_dir: str = "/tmp/backups"):
        self.backup_dir = backup_dir
        self.manifest_file = os.path.join(backup_dir, "manifest.json")
        self.backups: Dict[str, List[BackupEntry]] = {}
        self.checksums: Dict[str, str] = {}  # checksum -> path
        
        os.makedirs(backup_dir, exist_ok=True)
        self.load_manifest()
    
    def load_manifest(self):
        """Last manifest"""
        try:
            with open(self.manifest_file, 'r') as f:
                data = json.load(f)
                for source, entries in data.items():
                    self.backups[source] = [BackupEntry(**e) for e in entries]
        except (FileNotFoundError, json.JSONDecodeError):
            self.backups = {}
    
    def save_manifest(self):
        """Lagre manifest"""
        with open(self.manifest_file, 'w') as f:
            json.dump(
                {k: [e.to_dict() for e in v] for k, v in self.backups.items()},
                f, indent=2
            )
    
    def calculate_checksum(self, filepath: str) -> str:
        """Beregn MD5 checksum"""
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def backup_file(self, source_path: str, incremental: bool = True) -> Optional[BackupEntry]:
        """Backup en fil"""
        if not os.path.exists(source_path):
            logger.error(f"Fil finnes ikke: {source_path}")
            return None
        
        # Beregn checksum
        checksum = self.calculate_checksum(source_path)
        
        # Sjekk om vi allerede har denne filen (deduplisering)
        if incremental and checksum in self.checksums:
            logger.info(f"Fil allerede backupet (dedup): {source_path}")
            return None
        
        # Beregn versjon
        source_key = os.path.abspath(source_path)
        existing = self.backups.get(source_key, [])
        version = len(existing) + 1
        
        # Lag backup path
        timestamp = DateUtils.format(DateUtils.now()).replace(':', '-')
        filename = f"{Path(source_path).name}.{version}.{timestamp}"
        backup_path = os.path.join(self.backup_dir, filename)
        
        # Kopier fil
        shutil.copy2(source_path, backup_path)
        size = os.path.getsize(source_path)
        
        # Opprett entry
        entry = BackupEntry(
            id=UUIDUtils.generate_short(),
            source_path=source_path,
            backup_path=backup_path,
            timestamp=DateUtils.format(DateUtils.now()),
            size_bytes=size,
            checksum=checksum,
            version=version,
            is_incremental=incremental,
            parent_version=existing[-1].version if existing else None
        )
        
        # Lagre
        if source_key not in self.backups:
            self.backups[source_key] = []
        self.backups[source_key].append(entry)
        self.checksums[checksum] = backup_path
        self.save_manifest()
        
        logger.info(f"Backup fullført: {source_path} (v{version})")
        return entry
    
    def backup_directory(self, source_dir: str, pattern: str = "*") -> List[BackupEntry]:
        """Backup en hel mappe"""
        entries = []
        
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if pattern == "*" or file.endswith(pattern.replace("*", "")):
                    filepath = os.path.join(root, file)
                    entry = self.backup_file(filepath)
                    if entry:
                        entries.append(entry)
        
        return entries
    
    def restore(self, source_path: str, version: Optional[int] = None,
                restore_path: Optional[str] = None) -> bool:
        """Gjenopprett fra backup"""
        source_key = os.path.abspath(source_path)
        
        if source_key not in self.backups:
            logger.error(f"Ingen backup funnet for: {source_path}")
            return False
        
        entries = self.backups[source_key]
        
        # Finn riktig versjon
        if version:
            entry = next((e for e in entries if e.version == version), None)
        else:
            entry = entries[-1]  # Siste versjon
        
        if not entry:
            logger.error(f"Versjon {version} ikke funnet")
            return False
        
        # Bestem restore path
        if restore_path:
            target = restore_path
        else:
            target = source_path
        
        # Kopier
        shutil.copy2(entry.backup_path, target)
        logger.info(f"Gjenopprettet: {source_path} (v{entry.version}) til {target}")
        
        return True
    
    def list_backups(self, source_path: Optional[str] = None) -> List[BackupEntry]:
        """List alle backups"""
        if source_path:
            source_key = os.path.abspath(source_path)
            return self.backups.get(source_key, [])
        
        all_entries = []
        for entries in self.backups.values():
            all_entries.extend(entries)
        return all_entries
    
    def cleanup_old(self, keep_versions: int = 5):
        """Slett gamle versjoner"""
        removed = 0
        
        for source_key, entries in self.backups.items():
            if len(entries) > keep_versions:
                to_remove = entries[:-keep_versions]
                for entry in to_remove:
                    try:
                        os.remove(entry.backup_path)
                        removed += 1
                    except OSError:
                        pass
                
                self.backups[source_key] = entries[-keep_versions:]
        
        self.save_manifest()
        logger.info(f"Slettet {removed} gamle backups")
        return removed
    
    def get_stats(self) -> Dict[str, Any]:
        """Hent statistikk"""
        total_backups = sum(len(entries) for entries in self.backups.values())
        total_size = sum(
            e.size_bytes for entries in self.backups.values() for e in entries
        )
        unique_files = len(self.backups)
        
        return {
            'total_backups': total_backups,
            'unique_files': unique_files,
            'total_size_mb': total_size / (1024 * 1024),
            'backup_dir': self.backup_dir
        }
    
    def display_status(self):
        """Vis status i terminal"""
        stats = self.get_stats()
        
        print(f"\n{'='*70}")
        print(f"{Colors.CYAN}💾 SMART BACKUP SERVICE{Colors.RESET}")
        print(f"{'='*70}")
        print(f"Backup-mappe: {stats['backup_dir']}")
        print(f"Unike filer: {stats['unique_files']}")
        print(f"Totale backups: {stats['total_backups']}")
        print(f"Total størrelse: {stats['total_size_mb']:.2f} MB")
        print(f"{'='*70}")
        
        # Vis siste backups
        all_entries = self.list_backups()
        if all_entries:
            print("\n📋 SISTE BACKUPS:")
            for entry in sorted(all_entries, key=lambda e: e.timestamp, reverse=True)[:10]:
                size_kb = entry.size_bytes / 1024
                print(f"  v{entry.version}: {Path(entry.source_path).name} ({size_kb:.1f} KB)")

def main():
    """Hovedfunksjon"""
    print("="*70)
    print("💾 SMART BACKUP SERVICE")
    print("="*70)
    
    # Initialiser
    backup = SmartBackupService()
    
    # Test backup av noen filer
    test_files = [
        "/root/.openclaw/workspace/MEMORY.md",
        "/root/.openclaw/workspace/TOOLS.md",
    ]
    
    print("\n📤 Backuper test-filer...")
    for filepath in test_files:
        if os.path.exists(filepath):
            entry = backup.backup_file(filepath)
            if entry:
                print(f"  ✅ {Path(filepath).name}")
        else:
            print(f"  ⚠️  Fil finnes ikke: {filepath}")
    
    # Vis status
    backup.display_status()
    
    # Vis statistikk
    stats = backup.get_stats()
    print(f"\n📊 Statistikk:")
    print(f"  Totale backups: {stats['total_backups']}")
    print(f"  Unike filer: {stats['unique_files']}")
    print(f"  Størrelse: {stats['total_size_mb']:.2f} MB")
    
    print("\n" + "="*70)
    print("✅ Smart Backup Service klar!")
    print("="*70)

if __name__ == "__main__":
    main()
