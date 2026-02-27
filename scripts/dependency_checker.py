#!/usr/bin/env python3
"""
Dependency Checker - Verify all system dependencies are available
"""

import subprocess
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple

class DependencyChecker:
    """Check system and Python dependencies"""
    
    def __init__(self):
        self.checks = []
        self.results = []
        
    def add_check(self, name: str, check_type: str, **kwargs):
        """Add a dependency check"""
        self.checks.append({
            'name': name,
            'type': check_type,
            'kwargs': kwargs
        })
    
    def check_command(self, command: str, args: List[str] = None, 
                      version_flag: str = '--version') -> Tuple[bool, str]:
        """Check if a command is available"""
        try:
            cmd = [command]
            if args:
                cmd.extend(args)
            else:
                cmd.append(version_flag)
            
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                version = result.stdout.strip().split('\n')[0][:50]
                return True, version
            return False, f"Exit code: {result.returncode}"
        except FileNotFoundError:
            return False, "Not installed"
        except subprocess.TimeoutExpired:
            return False, "Timeout"
        except Exception as e:
            return False, str(e)
    
    def check_python_package(self, package: str) -> Tuple[bool, str]:
        """Check if a Python package is installed"""
        try:
            __import__(package)
            return True, "Installed"
        except ImportError:
            return False, "Not installed"
    
    def check_file_exists(self, path: str) -> Tuple[bool, str]:
        """Check if a file exists"""
        if Path(path).exists():
            return True, "Exists"
        return False, "Missing"
    
    def check_env_var(self, var: str) -> Tuple[bool, str]:
        """Check if environment variable is set"""
        value = os.environ.get(var)
        if value:
            # Mask the value for security
            masked = value[:4] + '...' if len(value) > 4 else 'set'
            return True, masked
        return False, "Not set"
    
    def run_checks(self):
        """Run all registered checks"""
        self.results = []
        
        for check in self.checks:
            name = check['name']
            check_type = check['type']
            kwargs = check['kwargs']
            
            if check_type == 'command':
                success, message = self.check_command(**kwargs)
            elif check_type == 'python_package':
                success, message = self.check_python_package(**kwargs)
            elif check_type == 'file':
                success, message = self.check_file_exists(**kwargs)
            elif check_type == 'env_var':
                success, message = self.check_env_var(**kwargs)
            else:
                success, message = False, f"Unknown check type: {check_type}"
            
            self.results.append({
                'name': name,
                'type': check_type,
                'status': '✅' if success else '❌',
                'success': success,
                'message': message
            })
        
        return self.results
    
    def print_report(self):
        """Print formatted report"""
        print("\n" + "=" * 70)
        print("🔍 DEPENDENCY CHECK REPORT")
        print("=" * 70)
        print(f"{'Component':<30} {'Status':<8} {'Details':<30}")
        print("-" * 70)
        
        for result in self.results:
            status = result['status']
            name = result['name']
            message = result['message'][:30]
            print(f"{name:<30} {status:<8} {message}")
        
        print("=" * 70)
        
        passed = sum(1 for r in self.results if r['success'])
        total = len(self.results)
        print(f"\n📊 Summary: {passed}/{total} checks passed")
        
        if passed < total:
            print("\n⚠️ Missing dependencies:")
            for result in self.results:
                if not result['success']:
                    print(f"  • {result['name']}: {result['message']}")
        
        return passed == total
    
    def save_report(self, output_dir='/root/.openclaw/workspace/brain/reports'):
        """Save report to JSON"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        report_file = Path(output_dir) / f'dependency-check-{timestamp}.json'
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': len(self.results),
                'passed': sum(1 for r in self.results if r['success']),
                'failed': sum(1 for r in self.results if not r['success'])
            },
            'checks': self.results
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_file


def run_full_check():
    """Run full dependency check for BaarliClaw workspace"""
    checker = DependencyChecker()
    
    # System commands
    checker.add_check('Python 3', 'command', command='python3')
    checker.add_check('pip', 'command', command='pip3')
    checker.add_check('Git', 'command', command='git')
    checker.add_check('Node.js', 'command', command='node')
    checker.add_check('npm', 'command', command='npm')
    checker.add_check('curl', 'command', command='curl')
    checker.add_check('jq', 'command', command='jq')
    checker.add_check('ffmpeg', 'command', command='ffmpeg')
    
    # Python packages (core)
    checker.add_check('requests', 'python_package', package='requests')
    checker.add_check('json', 'python_package', package='json')
    checker.add_check('pathlib', 'python_package', package='pathlib')
    
    # Key files
    checker.add_check('MEMORY.md', 'file', path='/root/.openclaw/workspace/MEMORY.md')
    checker.add_check('AGENTS.md', 'file', path='/root/.openclaw/workspace/AGENTS.md')
    checker.add_check('scripts dir', 'file', path='/root/.openclaw/workspace/scripts')
    checker.add_check('skills dir', 'file', path='/root/.openclaw/workspace/skills')
    
    # Environment variables (optional checks)
    # checker.add_check('OPENAI_API_KEY', 'env_var', var='OPENAI_API_KEY')
    
    # Run checks
    checker.run_checks()
    all_passed = checker.print_report()
    
    report_file = checker.save_report()
    print(f"\n💾 Report saved to: {report_file}")
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(run_full_check())
