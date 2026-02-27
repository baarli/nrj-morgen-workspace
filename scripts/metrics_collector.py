#!/usr/bin/env python3
"""
📊 Metrics Collector - System metrics collection and storage
"""

import os
import sys
import json
import time
import psutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("MetricsCollector")

class MetricsCollector:
    """Collect and store system metrics"""
    
    def __init__(self, metrics_dir='/root/.openclaw/workspace/brain/metrics'):
        self.metrics_dir = Path(metrics_dir)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        self.data = {}
        
    def collect_system_metrics(self) -> Dict[str, Any]:
        """Collect system-level metrics"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'cpu_count': psutil.cpu_count(),
            'memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'percent': psutil.virtual_memory().percent,
                'used': psutil.virtual_memory().used
            },
            'disk': {
                'total': psutil.disk_usage('/').total,
                'used': psutil.disk_usage('/').used,
                'free': psutil.disk_usage('/').free,
                'percent': psutil.disk_usage('/').percent
            },
            'boot_time': psutil.boot_time(),
            'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else None
        }
    
    def collect_workspace_metrics(self) -> Dict[str, Any]:
        """Collect workspace-specific metrics"""
        workspace = Path('/root/.openclaw/workspace')
        
        # Count files by type
        file_counts = {
            'python': 0,
            'shell': 0,
            'markdown': 0,
            'json': 0,
            'html': 0,
            'total': 0
        }
        
        total_lines = 0
        
        for root, dirs, files in os.walk(workspace):
            # Skip certain directories
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__', '.netlify']]
            
            for file in files:
                file_counts['total'] += 1
                
                if file.endswith('.py'):
                    file_counts['python'] += 1
                elif file.endswith('.sh'):
                    file_counts['shell'] += 1
                elif file.endswith('.md'):
                    file_counts['markdown'] += 1
                elif file.endswith('.json'):
                    file_counts['json'] += 1
                elif file.endswith('.html'):
                    file_counts['html'] += 1
                
                # Count lines in code files
                if file.endswith(('.py', '.sh', '.js')):
                    try:
                        filepath = Path(root) / file
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            total_lines += len(f.readlines())
                    except:
                        pass
        
        return {
            'file_counts': file_counts,
            'total_lines': total_lines,
            'skills_count': len(list((workspace / 'skills').glob('*/SKILL.md'))) if (workspace / 'skills').exists() else 0
        }
    
    def collect_git_metrics(self) -> Dict[str, Any]:
        """Collect git repository metrics"""
        import subprocess
        
        workspace = Path('/root/.openclaw/workspace')
        
        try:
            # Check for uncommitted changes
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=workspace,
                capture_output=True,
                text=True
            )
            
            changes = len([l for l in result.stdout.strip().split('\n') if l.strip()])
            
            # Get last commit info
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%H|%ci|%s'],
                cwd=workspace,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                parts = result.stdout.strip().split('|')
                last_commit = {
                    'hash': parts[0][:8] if len(parts) > 0 else None,
                    'date': parts[1] if len(parts) > 1 else None,
                    'message': parts[2] if len(parts) > 2 else None
                }
            else:
                last_commit = None
            
            return {
                'uncommitted_changes': changes,
                'last_commit': last_commit
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def collect_all(self) -> Dict[str, Any]:
        """Collect all metrics"""
        self.data = {
            'timestamp': datetime.now().isoformat(),
            'system': self.collect_system_metrics(),
            'workspace': self.collect_workspace_metrics(),
            'git': self.collect_git_metrics()
        }
        return self.data
    
    def save_metrics(self):
        """Save metrics to file"""
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        metrics_file = self.metrics_dir / f'metrics-{timestamp}.json'
        
        with open(metrics_file, 'w') as f:
            json.dump(self.data, f, indent=2)
        
        # Also save as latest
        latest_file = self.metrics_dir / 'latest.json'
        with open(latest_file, 'w') as f:
            json.dump(self.data, f, indent=2)
        
        return metrics_file
    
    def print_summary(self):
        """Print metrics summary"""
        print("\n" + "=" * 60)
        print("📊 SYSTEM METRICS")
        print("=" * 60)
        
        sys_metrics = self.data.get('system', {})
        ws_metrics = self.data.get('workspace', {})
        git_metrics = self.data.get('git', {})
        
        print(f"\n🖥️  System:")
        print(f"   CPU: {sys_metrics.get('cpu_percent', 'N/A')}%")
        print(f"   Memory: {sys_metrics.get('memory', {}).get('percent', 'N/A')}%")
        print(f"   Disk: {sys_metrics.get('disk', {}).get('percent', 'N/A')}%")
        
        print(f"\n📁 Workspace:")
        file_counts = ws_metrics.get('file_counts', {})
        print(f"   Total files: {file_counts.get('total', 0)}")
        print(f"   Python: {file_counts.get('python', 0)}")
        print(f"   Shell: {file_counts.get('shell', 0)}")
        print(f"   Lines of code: {ws_metrics.get('total_lines', 0):,}")
        print(f"   Skills: {ws_metrics.get('skills_count', 0)}")
        
        print(f"\n📝 Git:")
        print(f"   Uncommitted changes: {git_metrics.get('uncommitted_changes', 'N/A')}")
        
        print("=" * 60)


def main():
    """Main entry point"""
    collector = MetricsCollector()
    collector.collect_all()
    collector.print_summary()
    
    metrics_file = collector.save_metrics()
    print(f"\n💾 Metrics saved to: {metrics_file}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
