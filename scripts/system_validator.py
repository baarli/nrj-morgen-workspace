#!/usr/bin/env python3
"""
✅ System Validator - Comprehensive system validation
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("SystemValidator")

class SystemValidator:
    """Validate system configuration and health"""
    
    def __init__(self, workspace='/root/.openclaw/workspace'):
        self.workspace = Path(workspace)
        self.checks = []
        self.results = []
        
    def check_critical_files(self) -> Tuple[bool, List[str]]:
        """Check that critical files exist"""
        critical_files = [
            'MEMORY.md',
            'TOOLS.md',
            'AGENTS.md',
            'SOUL.md',
            'scripts/auto-update-all-knowledge.sh',
            'scripts/system_health_dashboard.py'
        ]
        
        missing = []
        for file in critical_files:
            path = self.workspace / file
            if not path.exists():
                missing.append(file)
        
        return len(missing) == 0, missing
    
    def check_directory_structure(self) -> Tuple[bool, List[str]]:
        """Check that required directories exist"""
        required_dirs = [
            'scripts',
            'skills',
            'docs',
            'brain',
            'memory',
            '.config'
        ]
        
        missing = []
        for dir_name in required_dirs:
            path = self.workspace / dir_name
            if not path.exists():
                missing.append(dir_name)
        
        return len(missing) == 0, missing
    
    def check_python_syntax(self) -> Tuple[bool, List[str]]:
        """Check Python files for syntax errors"""
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
        
        return len(errors) == 0, errors
    
    def check_cron_jobs(self) -> Tuple[bool, str]:
        """Check cron job status"""
        try:
            result = subprocess.run(
                ['openclaw', 'cron', 'list'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return False, "Could not retrieve cron jobs"
            
            # Count errors
            error_count = result.stdout.count('error')
            
            if error_count > 0:
                return False, f"{error_count} cron jobs with errors"
            
            return True, "All cron jobs healthy"
            
        except Exception as e:
            return False, str(e)
    
    def check_disk_space(self) -> Tuple[bool, str]:
        """Check available disk space"""
        try:
            import psutil
            disk = psutil.disk_usage('/')
            percent_used = disk.percent
            
            if percent_used > 90:
                return False, f"Critical disk usage: {percent_used}%"
            elif percent_used > 80:
                return True, f"Warning: Disk usage {percent_used}%"
            else:
                return True, f"Disk usage: {percent_used}%"
                
        except Exception as e:
            return False, str(e)
    
    def run_all_checks(self) -> Dict:
        """Run all validation checks"""
        self.checks = [
            ('Critical Files', self.check_critical_files),
            ('Directory Structure', self.check_directory_structure),
            ('Python Syntax', self.check_python_syntax),
            ('Cron Jobs', self.check_cron_jobs),
            ('Disk Space', self.check_disk_space),
        ]
        
        for name, check_func in self.checks:
            success, details = check_func()
            self.results.append({
                'name': name,
                'status': '✅' if success else '❌',
                'success': success,
                'details': details if isinstance(details, str) else ', '.join(details) if details else 'OK'
            })
        
        return {
            'timestamp': datetime.now().isoformat(),
            'checks': self.results,
            'overall_status': 'healthy' if all(r['success'] for r in self.results) else 'issues_found'
        }
    
    def print_report(self, report: Dict):
        """Print formatted report"""
        print("\n" + "=" * 60)
        print("✅ SYSTEM VALIDATION REPORT")
        print("=" * 60)
        
        for result in report['checks']:
            print(f"\n{result['status']} {result['name']}:")
            print(f"   {result['details']}")
        
        print("=" * 60)
        
        passed = sum(1 for r in report['checks'] if r['success'])
        total = len(report['checks'])
        
        print(f"\n📊 Summary: {passed}/{total} checks passed")
        
        if report['overall_status'] == 'healthy':
            print("✅ System is healthy!")
        else:
            print("⚠️  Some issues found - review details above")
        
        print("=" * 60)
    
    def save_report(self, report: Dict):
        """Save report to JSON"""
        report_dir = self.workspace / 'brain' / 'reports'
        report_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        report_file = report_dir / f'system-validation-{timestamp}.json'
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_file


def main():
    """Main entry point"""
    validator = SystemValidator()
    
    print("🔍 Running system validation...")
    report = validator.run_all_checks()
    validator.print_report(report)
    
    report_file = validator.save_report(report)
    print(f"\n💾 Report saved to: {report_file}")
    
    return 0 if report['overall_status'] == 'healthy' else 1


if __name__ == '__main__':
    sys.exit(main())
