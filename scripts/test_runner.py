#!/usr/bin/env python3
"""
Test Runner - Automated testing framework for workspace scripts
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

class TestRunner:
    """Run automated tests for workspace components"""
    
    def __init__(self, workspace_path='/root/.openclaw/workspace'):
        self.workspace = Path(workspace_path)
        self.results = []
        
    def run_python_test(self, test_file: Path) -> Dict:
        """Run a Python test file"""
        start_time = time.time()
        
        try:
            result = subprocess.run(
                [sys.executable, str(test_file)],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=self.workspace
            )
            
            duration = time.time() - start_time
            
            return {
                'file': str(test_file),
                'type': 'python',
                'status': 'passed' if result.returncode == 0 else 'failed',
                'returncode': result.returncode,
                'stdout': result.stdout[-500:] if result.stdout else '',
                'stderr': result.stderr[-500:] if result.stderr else '',
                'duration': round(duration, 3)
            }
            
        except subprocess.TimeoutExpired:
            return {
                'file': str(test_file),
                'type': 'python',
                'status': 'timeout',
                'duration': 60
            }
        except Exception as e:
            return {
                'file': str(test_file),
                'type': 'python',
                'status': 'error',
                'error': str(e)
            }
    
    def run_shell_test(self, test_file: Path) -> Dict:
        """Run a shell test script"""
        start_time = time.time()
        
        try:
            result = subprocess.run(
                ['bash', str(test_file)],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=self.workspace
            )
            
            duration = time.time() - start_time
            
            return {
                'file': str(test_file),
                'type': 'shell',
                'status': 'passed' if result.returncode == 0 else 'failed',
                'returncode': result.returncode,
                'stdout': result.stdout[-500:] if result.stdout else '',
                'stderr': result.stderr[-500:] if result.stderr else '',
                'duration': round(duration, 3)
            }
            
        except subprocess.TimeoutExpired:
            return {
                'file': str(test_file),
                'type': 'shell',
                'status': 'timeout',
                'duration': 60
            }
        except Exception as e:
            return {
                'file': str(test_file),
                'type': 'shell',
                'status': 'error',
                'error': str(e)
            }
    
    def discover_tests(self) -> Tuple[List[Path], List[Path]]:
        """Discover test files in workspace"""
        python_tests = []
        shell_tests = []
        
        scripts_dir = self.workspace / 'scripts'
        
        if scripts_dir.exists():
            # Python tests
            for py_file in scripts_dir.glob('test_*.py'):
                python_tests.append(py_file)
            
            # Shell tests
            for sh_file in scripts_dir.glob('test_*.sh'):
                shell_tests.append(sh_file)
        
        # Also check for tests directory
        tests_dir = self.workspace / 'tests'
        if tests_dir.exists():
            python_tests.extend(tests_dir.glob('test_*.py'))
            python_tests.extend(tests_dir.glob('*_test.py'))
            shell_tests.extend(tests_dir.glob('test_*.sh'))
        
        return python_tests, shell_tests
    
    def run_all_tests(self) -> List[Dict]:
        """Run all discovered tests"""
        python_tests, shell_tests = self.discover_tests()
        
        print(f"🔍 Discovered {len(python_tests)} Python tests, {len(shell_tests)} Shell tests")
        
        # Run Python tests
        for test_file in python_tests:
            print(f"🐍 Running {test_file.name}...")
            result = self.run_python_test(test_file)
            self.results.append(result)
        
        # Run Shell tests
        for test_file in shell_tests:
            print(f"📜 Running {test_file.name}...")
            result = self.run_shell_test(test_file)
            self.results.append(result)
        
        return self.results
    
    def print_report(self):
        """Print formatted test report"""
        print("\n" + "=" * 70)
        print("🧪 TEST RESULTS")
        print("=" * 70)
        
        passed = sum(1 for r in self.results if r['status'] == 'passed')
        failed = sum(1 for r in self.results if r['status'] == 'failed')
        errors = sum(1 for r in self.results if r['status'] in ['error', 'timeout'])
        
        print(f"\n📊 Summary: {passed} passed, {failed} failed, {errors} errors")
        print(f"   Total: {len(self.results)} tests")
        
        if self.results:
            total_duration = sum(r.get('duration', 0) for r in self.results)
            print(f"   Duration: {total_duration:.2f}s")
        
        if failed > 0 or errors > 0:
            print("\n❌ Failed tests:")
            for result in self.results:
                if result['status'] != 'passed':
                    file_name = Path(result['file']).name
                    print(f"  • {file_name}: {result['status']}")
                    if 'stderr' in result and result['stderr']:
                        print(f"    {result['stderr'][:100]}")
        
        print("=" * 70)
    
    def save_report(self, output_dir='/root/.openclaw/workspace/brain/reports'):
        """Save test report to JSON"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        report_file = Path(output_dir) / f'test-report-{timestamp}.json'
        
        passed = sum(1 for r in self.results if r['status'] == 'passed')
        failed = sum(1 for r in self.results if r['status'] == 'failed')
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': len(self.results),
                'passed': passed,
                'failed': failed,
                'success_rate': round(passed / len(self.results) * 100, 2) if self.results else 0
            },
            'tests': self.results
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_file


def main():
    """Main entry point"""
    runner = TestRunner()
    
    print("🧪 Running automated tests...")
    runner.run_all_tests()
    
    runner.print_report()
    
    report_file = runner.save_report()
    print(f"\n💾 Report saved to: {report_file}")
    
    # Return exit code based on results
    failed = sum(1 for r in runner.results if r['status'] != 'passed')
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
