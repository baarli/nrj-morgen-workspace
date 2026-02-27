#!/usr/bin/env python3
"""
🖥️ System Monitor - Real-time system monitoring dashboard
"""

import os
import sys
import time
import json
import psutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("SystemMonitor")

class SystemMonitor:
    """Real-time system monitoring with alerting"""
    
    def __init__(self, alert_thresholds=None):
        self.alert_thresholds = alert_thresholds or {
            'cpu_percent': 80,
            'memory_percent': 85,
            'disk_percent': 90,
            'load_average': 4.0
        }
        self.alerts = []
        
    def check_cpu(self) -> Dict:
        """Check CPU usage"""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        alert = cpu_percent > self.alert_thresholds['cpu_percent']
        
        return {
            'percent': cpu_percent,
            'count': cpu_count,
            'alert': alert,
            'status': 'warning' if alert else 'ok'
        }
    
    def check_memory(self) -> Dict:
        """Check memory usage"""
        mem = psutil.virtual_memory()
        
        alert = mem.percent > self.alert_thresholds['memory_percent']
        
        return {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'percent': mem.percent,
            'alert': alert,
            'status': 'warning' if alert else 'ok'
        }
    
    def check_disk(self) -> Dict:
        """Check disk usage"""
        disk = psutil.disk_usage('/')
        
        alert = disk.percent > self.alert_thresholds['disk_percent']
        
        return {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent,
            'alert': alert,
            'status': 'warning' if alert else 'ok'
        }
    
    def check_load(self) -> Dict:
        """Check system load"""
        if hasattr(os, 'getloadavg'):
            load1, load5, load15 = os.getloadavg()
            alert = load1 > self.alert_thresholds['load_average']
            
            return {
                '1min': load1,
                '5min': load5,
                '15min': load15,
                'alert': alert,
                'status': 'warning' if alert else 'ok'
            }
        return {'status': 'unknown'}
    
    def check_processes(self) -> Dict:
        """Check running processes"""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                info = proc.info
                if info['cpu_percent'] > 10 or info['memory_percent'] > 5:
                    processes.append(info)
            except:
                pass
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
        
        return {
            'count': len(list(psutil.process_iter())),
            'top': processes[:5]
        }
    
    def run_checks(self) -> Dict:
        """Run all system checks"""
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu': self.check_cpu(),
            'memory': self.check_memory(),
            'disk': self.check_disk(),
            'load': self.check_load(),
            'processes': self.check_processes()
        }
    
    def print_dashboard(self, results: Dict):
        """Print monitoring dashboard"""
        print("\n" + "=" * 70)
        print("🖥️  SYSTEM MONITOR DASHBOARD")
        print("=" * 70)
        print(f"Last updated: {results['timestamp']}")
        print()
        
        # CPU
        cpu = results['cpu']
        cpu_icon = "🔴" if cpu.get('alert') else "🟢"
        print(f"{cpu_icon} CPU: {cpu['percent']:.1f}% ({cpu['count']} cores)")
        
        # Memory
        mem = results['memory']
        mem_icon = "🔴" if mem.get('alert') else "🟢"
        mem_gb = mem['used'] / (1024**3)
        mem_total_gb = mem['total'] / (1024**3)
        print(f"{mem_icon} Memory: {mem['percent']:.1f}% ({mem_gb:.1f}GB / {mem_total_gb:.1f}GB)")
        
        # Disk
        disk = results['disk']
        disk_icon = "🔴" if disk.get('alert') else "🟢"
        disk_gb = disk['used'] / (1024**3)
        disk_total_gb = disk['total'] / (1024**3)
        print(f"{disk_icon} Disk: {disk['percent']:.1f}% ({disk_gb:.1f}GB / {disk_total_gb:.1f}GB)")
        
        # Load
        load = results['load']
        if '1min' in load:
            load_icon = "🔴" if load.get('alert') else "🟢"
            print(f"{load_icon} Load: {load['1min']:.2f} (1m) / {load['5min']:.2f} (5m) / {load['15min']:.2f} (15m)")
        
        # Processes
        procs = results['processes']
        print(f"\n📊 Processes: {procs['count']} total")
        
        if procs['top']:
            print("\nTop resource consumers:")
            for proc in procs['top'][:3]:
                print(f"  {proc['name']} (PID {proc['pid']}): CPU {proc['cpu_percent']:.1f}%, MEM {proc['memory_percent']:.1f}%")
        
        print("=" * 70)
    
    def save_results(self, results: Dict):
        """Save monitoring results"""
        output_dir = Path('/root/.openclaw/workspace/brain/metrics')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        output_file = output_dir / f'monitor-{timestamp}.json'
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Also save as latest
        latest_file = output_dir / 'latest-monitor.json'
        with open(latest_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        return output_file


def main():
    """Main entry point"""
    monitor = SystemMonitor()
    
    print("🔍 Running system monitoring...")
    results = monitor.run_checks()
    monitor.print_dashboard(results)
    
    output_file = monitor.save_results(results)
    print(f"\n💾 Results saved to: {output_file}")
    
    # Return error code if any alerts
    alerts = sum(1 for check in ['cpu', 'memory', 'disk', 'load'] 
                 if results.get(check, {}).get('alert', False))
    
    return 1 if alerts > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
