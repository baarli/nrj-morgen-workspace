#!/usr/bin/env python3
"""
⚙️ BAARLICLAW PROCESS TOOLKIT
Prosess- og system-verktøy
"""

import os
import sys
import subprocess
import signal
import psutil
from typing import List, Optional, Dict, Any

class ProcessUtils:
    """Process utilities"""
    
    @staticmethod
    def run(command: List[str], cwd: Optional[str] = None, 
            env: Optional[Dict[str, str]] = None,
            timeout: Optional[int] = None) -> Dict[str, Any]:
        """Run command and return result"""
        result = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return {
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'success': result.returncode == 0
        }
    
    @staticmethod
    def get_processes() -> List[Dict]:
        """Get list of running processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return processes
    
    @staticmethod
    def kill_process(pid: int, force: bool = False) -> bool:
        """Kill process by PID"""
        try:
            proc = psutil.Process(pid)
            if force:
                proc.kill()
            else:
                proc.terminate()
            return True
        except psutil.NoSuchProcess:
            return False
    
    @staticmethod
    def get_system_info() -> Dict:
        """Get system information"""
        return {
            'cpu_count': psutil.cpu_count(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory': psutil.virtual_memory()._asdict(),
            'disk': psutil.disk_usage('/')._asdict(),
            'boot_time': psutil.boot_time()
        }

class SystemUtils:
    """System utilities"""
    
    @staticmethod
    def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
        """Get environment variable"""
        return os.environ.get(key, default)
    
    @staticmethod
    def set_env(key: str, value: str):
        """Set environment variable"""
        os.environ[key] = value
    
    @staticmethod
    def get_cwd() -> str:
        """Get current working directory"""
        return os.getcwd()
    
    @staticmethod
    def change_dir(path: str):
        """Change working directory"""
        os.chdir(path)
    
    @staticmethod
    def exit(code: int = 0):
        """Exit program"""
        sys.exit(code)

# === CONVENIENCE FUNCTIONS ===
def run_command(command: str) -> str:
    """Quick command execution"""
    result = ProcessUtils.run(command.split())
    return result['stdout'] if result['success'] else result['stderr']

def get_cpu_usage() -> float:
    """Quick CPU usage"""
    return psutil.cpu_percent(interval=1)

def get_memory_usage() -> Dict:
    """Quick memory usage"""
    return psutil.virtual_memory()._asdict()

# === TESTING ===
if __name__ == "__main__":
    print("⚙️ BaarliClaw Process Toolkit - Testing")
    print("=" * 50)
    
    # Test command execution
    print("\n🧪 Testing Command Execution")
    result = ProcessUtils.run(['echo', 'Hello, World!'])
    print(f"  Command: echo 'Hello, World!'")
    print(f"  Success: {result['success']}")
    print(f"  Output: {result['stdout'].strip()}")
    
    # Test system info
    print("\n🧪 Testing System Info")
    info = ProcessUtils.get_system_info()
    print(f"  CPU cores: {info['cpu_count']}")
    print(f"  CPU usage: {info['cpu_percent']:.1f}%")
    print(f"  Memory used: {info['memory']['percent']:.1f}%")
    
    # Test system utils
    print("\n🧪 Testing System Utils")
    print(f"  Current directory: {SystemUtils.get_cwd()}")
    print(f"  PATH exists: {SystemUtils.get_env('PATH') is not None}")
    
    print("\n✅ Process Toolkit ready!")
