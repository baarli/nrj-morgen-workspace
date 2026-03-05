#!/usr/bin/env python3
"""
📈 Trend Analyzer - Analyze trends in system metrics over time
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("TrendAnalyzer")

class TrendAnalyzer:
    """Analyze trends in system metrics"""
    
    def __init__(self, metrics_dir='/root/.openclaw/workspace/brain/metrics'):
        self.metrics_dir = Path(metrics_dir)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        
    def load_metrics_history(self, days=7) -> List[Dict]:
        """Load metrics from the last N days"""
        cutoff = datetime.now() - timedelta(days=days)
        metrics = []
        
        for metrics_file in self.metrics_dir.glob('metrics-*.json'):
            try:
                # Parse timestamp from filename
                timestamp_str = metrics_file.stem.replace('metrics-', '')
                file_time = datetime.strptime(timestamp_str, '%Y%m%d-%H%M%S')
                
                if file_time >= cutoff:
                    with open(metrics_file, 'r') as f:
                        data = json.load(f)
                        data['_file_time'] = file_time
                        metrics.append(data)
            except Exception as e:
                logger.warning(f"Could not load {metrics_file}: {e}")
        
        # Sort by timestamp
        metrics.sort(key=lambda x: x.get('timestamp', ''))
        return metrics
    
    def analyze_cpu_trend(self, metrics: List[Dict]) -> Dict:
        """Analyze CPU usage trend"""
        cpu_values = [m.get('system', {}).get('cpu_percent', 0) for m in metrics]
        
        if not cpu_values:
            return {'error': 'No data'}
        
        avg_cpu = sum(cpu_values) / len(cpu_values)
        max_cpu = max(cpu_values)
        min_cpu = min(cpu_values)
        
        # Calculate trend
        if len(cpu_values) >= 2:
            first_half = sum(cpu_values[:len(cpu_values)//2]) / (len(cpu_values)//2)
            second_half = sum(cpu_values[len(cpu_values)//2:]) / (len(cpu_values) - len(cpu_values)//2)
            trend = "increasing" if second_half > first_half * 1.1 else "decreasing" if second_half < first_half * 0.9 else "stable"
        else:
            trend = "insufficient data"
        
        return {
            'average': round(avg_cpu, 2),
            'maximum': round(max_cpu, 2),
            'minimum': round(min_cpu, 2),
            'trend': trend,
            'samples': len(cpu_values)
        }
    
    def analyze_memory_trend(self, metrics: List[Dict]) -> Dict:
        """Analyze memory usage trend"""
        mem_values = [m.get('system', {}).get('memory', {}).get('percent', 0) for m in metrics]
        
        if not mem_values:
            return {'error': 'No data'}
        
        return {
            'average': round(sum(mem_values) / len(mem_values), 2),
            'maximum': round(max(mem_values), 2),
            'minimum': round(min(mem_values), 2),
            'samples': len(mem_values)
        }
    
    def analyze_disk_trend(self, metrics: List[Dict]) -> Dict:
        """Analyze disk usage trend"""
        disk_values = [m.get('system', {}).get('disk', {}).get('percent', 0) for m in metrics]
        
        if not disk_values:
            return {'error': 'No data'}
        
        return {
            'average': round(sum(disk_values) / len(disk_values), 2),
            'current': round(disk_values[-1], 2),
            'samples': len(disk_values)
        }
    
    def analyze_code_growth(self, metrics: List[Dict]) -> Dict:
        """Analyze code growth trend"""
        line_counts = [m.get('workspace', {}).get('total_lines', 0) for m in metrics]
        
        if not line_counts or line_counts[0] == 0:
            return {'error': 'No data'}
        
        growth = line_counts[-1] - line_counts[0]
        growth_percent = (growth / line_counts[0] * 100) if line_counts[0] > 0 else 0
        
        return {
            'initial_lines': line_counts[0],
            'current_lines': line_counts[-1],
            'growth': growth,
            'growth_percent': round(growth_percent, 2)
        }
    
    def generate_report(self, days=7) -> Dict:
        """Generate comprehensive trend report"""
        metrics = self.load_metrics_history(days)
        
        if not metrics:
            return {'error': f'No metrics found for last {days} days'}
        
        return {
            'period_days': days,
            'samples': len(metrics),
            'cpu': self.analyze_cpu_trend(metrics),
            'memory': self.analyze_memory_trend(metrics),
            'disk': self.analyze_disk_trend(metrics),
            'code_growth': self.analyze_code_growth(metrics),
            'generated_at': datetime.now().isoformat()
        }
    
    def print_report(self, report: Dict):
        """Print formatted report"""
        print("\n" + "=" * 60)
        print("📈 TREND ANALYSIS REPORT")
        print("=" * 60)
        
        if 'error' in report:
            print(f"\n❌ {report['error']}")
            return
        
        print(f"\n📊 Period: Last {report['period_days']} days")
        print(f"   Samples: {report['samples']}")
        
        cpu = report.get('cpu', {})
        if 'error' not in cpu:
            print(f"\n🖥️  CPU Usage:")
            print(f"   Average: {cpu.get('average', 'N/A')}%")
            print(f"   Range: {cpu.get('minimum', 'N/A')}% - {cpu.get('maximum', 'N/A')}%")
            print(f"   Trend: {cpu.get('trend', 'N/A')}")
        
        memory = report.get('memory', {})
        if 'error' not in memory:
            print(f"\n💾 Memory Usage:")
            print(f"   Average: {memory.get('average', 'N/A')}%")
            print(f"   Peak: {memory.get('maximum', 'N/A')}%")
        
        disk = report.get('disk', {})
        if 'error' not in disk:
            print(f"\n💿 Disk Usage:")
            print(f"   Average: {disk.get('average', 'N/A')}%")
            print(f"   Current: {disk.get('current', 'N/A')}%")
        
        code = report.get('code_growth', {})
        if 'error' not in code:
            print(f"\n📁 Code Growth:")
            print(f"   Lines: {code.get('initial_lines', 0):,} → {code.get('current_lines', 0):,}")
            print(f"   Growth: {code.get('growth', 0):,} lines ({code.get('growth_percent', 0)}%)")
        
        print("=" * 60)
    
    def save_report(self, report: Dict):
        """Save report to JSON"""
        report_dir = Path('/root/.openclaw/workspace/brain/reports')
        report_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        report_file = report_dir / f'trend-analysis-{timestamp}.json'
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_file


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Trend Analyzer')
    parser.add_argument('--days', type=int, default=7, help='Number of days to analyze')
    
    args = parser.parse_args()
    
    analyzer = TrendAnalyzer()
    report = analyzer.generate_report(args.days)
    analyzer.print_report(report)
    
    report_file = analyzer.save_report(report)
    print(f"\n💾 Report saved to: {report_file}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
