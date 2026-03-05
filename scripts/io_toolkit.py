#!/usr/bin/env python3
"""
💾 BAARLICLAW IO TOOLKIT
Inn/ut-operasjoner
"""

import os
import json
import csv
from typing import Any, Optional, List, Dict
from pathlib import Path

class FileIO:
    """File I/O operations"""
    
    @staticmethod
    def read_text(path: str) -> str:
        """Read text file"""
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def write_text(path: str, content: str):
        """Write text file"""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    @staticmethod
    def read_json(path: str) -> Any:
        """Read JSON file"""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def write_json(path: str, data: Any, indent: int = 2):
        """Write JSON file"""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent)
    
    @staticmethod
    def read_lines(path: str) -> List[str]:
        """Read file as lines"""
        with open(path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f]
    
    @staticmethod
    def append_line(path: str, line: str):
        """Append line to file"""
        with open(path, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    
    @staticmethod
    def exists(path: str) -> bool:
        """Check if file exists"""
        return os.path.exists(path)
    
    @staticmethod
    def size(path: str) -> int:
        """Get file size"""
        return os.path.getsize(path)

# === CONVENIENCE FUNCTIONS ===
def read_file(path: str) -> str:
    """Quick file read"""
    return FileIO.read_text(path)

def write_file(path: str, content: str):
    """Quick file write"""
    FileIO.write_text(path, content)

def load_json(path: str) -> Any:
    """Quick JSON load"""
    return FileIO.read_json(path)

def save_json(path: str, data: Any):
    """Quick JSON save"""
    FileIO.write_json(path, data)

# === TESTING ===
if __name__ == "__main__":
    print("💾 BaarliClaw IO Toolkit - Testing")
    print("=" * 50)
    
    test_path = "/tmp/test_io.txt"
    json_path = "/tmp/test_io.json"
    
    # Test text I/O
    print("\n🧪 Testing Text I/O")
    FileIO.write_text(test_path, "Hello, World!")
    content = FileIO.read_text(test_path)
    print(f"  Read: {content}")
    
    # Test JSON I/O
    print("\n🧪 Testing JSON I/O")
    data = {"name": "Test", "value": 42}
    FileIO.write_json(json_path, data)
    loaded = FileIO.read_json(json_path)
    print(f"  Loaded: {loaded}")
    
    # Cleanup
    os.remove(test_path)
    os.remove(json_path)
    
    print("\n✅ IO Toolkit ready!")
