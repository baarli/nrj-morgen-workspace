#!/usr/bin/env python3
"""
🔍 Log Analyzer - Intelligent log analysis and alerting
"""

import os
import re
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("LogAnalyzer")

class LogAnalyzer:
    """Analyze system logs for errors and patterns"""
    
    def __init__(self, log_dirs=None):
        if log_dirs is None:
            log_dirs = ['/var/log', '/root/.openclaw/workspace/logs']
        self.log_dirs = [Path(d) for d in log_dirs if Path(d).exists()]
        self.error_patterns = [
            r'ERROR',
            r'CRITICAL',
            r'FATAL',
            r'Exception',
            r'Traceback',
            r'failed',
            r'failure',
        ]
        self.findings = defaultdict(list)
        
    def scan_logs(self, hours=24) -> Dict:
        """Scan logs for errors in the last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        
        for log_dir in self.log_dirs:
            for log_file in log_dir.glob('*.log'):
                try:
                    self._analyze_file(log_file, cutoff)
                except Exception as e:
                    logger.error(f"Error analyzing {log_file}: {e}")
        
        return dict(self.findings)
    
    def _analyze_file(self, log_file: Path, cutoff: datetime):
        """Analyze a single log file"""
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            # Check for error patterns
            for pattern in self.error_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self.findings[str(log_file)].append({
                        'line': line_num,
                        'content': line.strip()[:200],
                        'pattern': pattern
                    })
    
    def analyze_cron_logs(self) -> Dict:
        """Analyze cron job execution logs"""
        cron_issues = []
        
        # Check for common cron issues
        log_file = Path('/var/log/syslog') if Path('/var/log/syslog').exists() else Path('/var/log/messages')
        
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Look for cron errors
            cron_errors = re.findall(r'.*cron.*error.*', content, re.IGNORECASE)
            cron_failures = re.findall(r'.*cron.*fail.*', content, re.IGNORECASE)
            
            cron_issues.extend(cron_errors[-10:])
            cron_issues.extend(cron_failures[-10:])
        
        return {
            'cron_issues': cron_issues,
            'count': len(cron_issues)
        }
    
    def generate_summary(self) -> Dict:
        """Generate analysis summary"""
        total_errors = sum(len(v) for v in self.findings.values())
        files_with_errors = len(self.findings)
        
        # Top error patterns
        all_patterns = []
        for findings in self.findings.values():
            for finding in findings:
                all_patterns.append(finding['pattern'])
        
        top_patterns = Counter(all_patterns).most_common(5)
        
        return {
            'total_errors': total_errors,
            'files_with_errors': files_with_errors,
            'top_patterns': top_patterns,
            'timestamp': datetime.now().isoformat()
        }
    
    def print_report(self):
        """Print formatted report"""
        summary = self.generate_summary()
        
        print("\n" + "=" * 60)
        print("🔍 LOG ANALYSIS REPORT")
        print("=" * 60)
        
        print(f"\n📊 Summary:")
        print(f"   Total errors found: {summary['total_errors']}")
        print(f"   Files with errors: {summary['files_with_errors']}")
        
        if summary['top_patterns']:
            print(f"\n🔥 Top Error Patterns:")
            for pattern, count in summary['top_patterns']:
                print(f"   {pattern}: {count} occurrences")
        
        if self.findings:
            print(f"\n📝 Recent Errors by File:")
            for file_path, errors in list(self.findings.items())[:5]:
                print(f"\n   {Path(file_path).name} ({len(errors)} errors)")
                for error in errors[:3]:
                    print(f"      Line {error['line']}: {error['content'][:80]}...")
        
        print("=" * 60)
    
    def save_report(self):
        """Save report to JSON"""
        report_dir = Path('/root/.openclaw/workspace/brain/reports')
        report_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        report_file = report_dir / f'log-analysis-{timestamp}.json'
        
        report = {
            'summary': self.generate_summary(),
            'findings': dict(self.findings)
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_file


def main():
    """Main entry point"""
    analyzer = LogAnalyzer()
    
    print("🔍 Analyzing system logs...")
    analyzer.scan_logs(hours=24)
    analyzer.analyze_cron_logs()
    
    analyzer.print_report()
    
    report_file = analyzer.save_report()
    print(f"\n💾 Report saved to: {report_file}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
