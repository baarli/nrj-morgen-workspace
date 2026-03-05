#!/usr/bin/env python3
"""
⚡ Performance Monitor - Overvåk systemytelse
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

class PerformanceMonitor:
    """Overvåk systemytelse over tid"""
    
    def __init__(self):
        self.workspace = Path('/root/.openclaw/workspace')
        self.metrics_file = self.workspace / 'brain' / 'performance-metrics.json'
        
    def collect_metrics(self) -> dict:
        """Samle ytelsesmetrikker"""
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        # Disk usage
        try:
            stat = os.statvfs('/')
            total = stat.f_blocks * stat.f_frsize
            used = (stat.f_blocks - stat.f_bfree) * stat.f_frsize
            metrics['disk_percent'] = round((used / total) * 100, 1)
            metrics['disk_free_gb'] = round((stat.f_bfree * stat.f_frsize) / (1024**3), 2)
        except:
            metrics['disk_percent'] = 0
        
        # Filantall
        try:
            total_files = 0
            for root, dirs, files in os.walk(self.workspace):
                # Skip node_modules og .git
                dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__']]
                total_files += len(files)
            metrics['total_files'] = total_files
        except:
            metrics['total_files'] = 0
        
        # Python filer
        try:
            scripts_dir = self.workspace / 'scripts'
            py_files = len(list(scripts_dir.glob('*.py')))
            metrics['python_scripts'] = py_files
        except:
            metrics['python_scripts'] = 0
        
        # Git commits (siste 24t)
        try:
            import subprocess
            result = subprocess.run(
                ['git', 'log', '--since=24 hours ago', '--oneline'],
                cwd=self.workspace,
                capture_output=True,
                text=True
            )
            commits_today = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            metrics['commits_today'] = commits_today
        except:
            metrics['commits_today'] = 0
        
        return metrics
    
    def save_metrics(self, metrics: dict):
        """Lagre metrikker"""
        
        data = []
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    data = json.load(f)
            except:
                pass
        
        data.append(metrics)
        
        # Behold kun siste 30 dager
        cutoff = datetime.now() - __import__('datetime').timedelta(days=30)
        data = [d for d in data if datetime.fromisoformat(d['timestamp']) > cutoff]
        
        with open(self.metrics_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def print_dashboard(self):
        """Print performance dashboard"""
        
        metrics = self.collect_metrics()
        self.save_metrics(metrics)
        
        print("\n" + "=" * 60)
        print("⚡ PERFORMANCE DASHBOARD")
        print("=" * 60)
        print(f"Time: {metrics['date']}")
        print()
        
        print(f"💾 Disk Usage: {metrics['disk_percent']}%")
        print(f"   Free: {metrics['disk_free_gb']} GB")
        print()
        
        print(f"📁 Total Files: {metrics['total_files']:,}")
        print(f"🐍 Python Scripts: {metrics['python_scripts']}")
        print()
        
        print(f"📊 Commits Today: {metrics['commits_today']}")
        
        # Trend hvis vi har historikk
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    data = json.load(f)
                
                if len(data) >= 2:
                    prev = data[-2]
                    file_growth = metrics['total_files'] - prev.get('total_files', 0)
                    if file_growth > 0:
                        print(f"   📈 +{file_growth} files since last check")
            except:
                pass
        
        print("=" * 60)


def main():
    """Main entry point"""
    monitor = PerformanceMonitor()
    monitor.print_dashboard()
    return 0


if __name__ == '__main__':
    sys.exit(main())
