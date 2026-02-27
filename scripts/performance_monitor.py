#!/usr/bin/env python3
"""
📊 BAARLICLAW PERFORMANCE MONITOR
Overvåking av system-ytelse og ressursbruk
"""

import sys
import os
import time
import json
import psutil
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

sys.path.insert(0, '/root/.openclaw/workspace/scripts')

from baarliclaw_toolkit import setup_logging
from data_analyzer import TrendAnalyzer
from date_toolkit import DateUtils
from cli_toolkit import TerminalUI, Colors

logger = setup_logging("performance-monitor")

@dataclass
class PerformanceSnapshot:
    """Ytelses-snapshot"""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_total_mb: float
    disk_percent: float
    disk_used_gb: float
    disk_total_gb: float
    load_average: List[float]
    network_io_mb: Dict[str, float]
    process_count: int
    
    def to_dict(self) -> Dict:
        return asdict(self)

class PerformanceMonitor:
    """Ytelses-overvåking"""
    
    def __init__(self, history_file: str = "/tmp/performance_history.json"):
        self.history_file = history_file
        self.history: List[PerformanceSnapshot] = []
        self.load()
    
    def load(self):
        """Last historikk"""
        try:
            with open(self.history_file, 'r') as f:
                data = json.load(f)
                self.history = [PerformanceSnapshot(**s) for s in data[-100:]]  # Siste 100
        except (FileNotFoundError, json.JSONDecodeError):
            self.history = []
    
    def save(self):
        """Lagre historikk"""
        with open(self.history_file, 'w') as f:
            json.dump([s.to_dict() for s in self.history[-100:]], f, indent=2)
    
    def capture(self) -> PerformanceSnapshot:
        """Ta ytelses-snapshot"""
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Minne
        memory = psutil.virtual_memory()
        memory_used_mb = memory.used / (1024 * 1024)
        memory_total_mb = memory.total / (1024 * 1024)
        
        # Disk
        disk = psutil.disk_usage('/')
        disk_used_gb = disk.used / (1024 * 1024 * 1024)
        disk_total_gb = disk.total / (1024 * 1024 * 1024)
        
        # Nettverk
        net_io = psutil.net_io_counters()
        network_io_mb = {
            'sent': net_io.bytes_sent / (1024 * 1024),
            'received': net_io.bytes_recv / (1024 * 1024)
        }
        
        # Prosesser
        process_count = len(psutil.pids())
        
        snapshot = PerformanceSnapshot(
            timestamp=DateUtils.format(DateUtils.now()),
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_used_mb=memory_used_mb,
            memory_total_mb=memory_total_mb,
            disk_percent=disk.percent,
            disk_used_gb=disk_used_gb,
            disk_total_gb=disk_total_gb,
            load_average=list(os.getloadavg()),
            network_io_mb=network_io_mb,
            process_count=process_count
        )
        
        self.history.append(snapshot)
        self.save()
        
        return snapshot
    
    def get_current_status(self) -> Dict[str, Any]:
        """Hent nåværende status"""
        if not self.history:
            return {}
        
        latest = self.history[-1]
        
        # Beregn trender
        cpu_trend = "stable"
        memory_trend = "stable"
        
        if len(self.history) >= 3:
            recent_cpu = [s.cpu_percent for s in self.history[-3:]]
            recent_mem = [s.memory_percent for s in self.history[-3:]]
            
            if recent_cpu[-1] > recent_cpu[0] * 1.2:
                cpu_trend = "rising"
            elif recent_cpu[-1] < recent_cpu[0] * 0.8:
                cpu_trend = "falling"
            
            if recent_mem[-1] > recent_mem[0] * 1.1:
                memory_trend = "rising"
        
        return {
            'timestamp': latest.timestamp,
            'cpu': {
                'percent': latest.cpu_percent,
                'trend': cpu_trend,
                'status': 'good' if latest.cpu_percent < 70 else 'warning' if latest.cpu_percent < 90 else 'critical'
            },
            'memory': {
                'percent': latest.memory_percent,
                'used_mb': latest.memory_used_mb,
                'total_mb': latest.memory_total_mb,
                'trend': memory_trend,
                'status': 'good' if latest.memory_percent < 70 else 'warning' if latest.memory_percent < 90 else 'critical'
            },
            'disk': {
                'percent': latest.disk_percent,
                'used_gb': latest.disk_used_gb,
                'total_gb': latest.disk_total_gb,
                'status': 'good' if latest.disk_percent < 80 else 'warning' if latest.disk_percent < 95 else 'critical'
            },
            'load_average': latest.load_average,
            'process_count': latest.process_count
        }
    
    def display_dashboard(self):
        """Vis ytelses-dashboard"""
        status = self.get_current_status()
        
        if not status:
            print("❌ Ingen data tilgjengelig")
            return
        
        print(f"\n{'='*70}")
        print(f"{Colors.CYAN}📊 PERFORMANCE MONITOR{Colors.RESET}")
        print(f"{'='*70}")
        print(f"Sist oppdatert: {status['timestamp']}")
        print()
        
        # CPU
        cpu = status['cpu']
        cpu_color = Colors.GREEN if cpu['status'] == 'good' else Colors.YELLOW if cpu['status'] == 'warning' else Colors.RED
        print(f"🔲 CPU: {cpu_color}{cpu['percent']:.1f}%{Colors.RESET} ({cpu['trend']})")
        self._draw_bar(cpu['percent'], 50)
        
        # Minne
        mem = status['memory']
        mem_color = Colors.GREEN if mem['status'] == 'good' else Colors.YELLOW if mem['status'] == 'warning' else Colors.RED
        print(f"\n💾 Minne: {mem_color}{mem['percent']:.1f}%{Colors.RESET} ({mem['used_mb']:.0f}/{mem['total_mb']:.0f} MB)")
        self._draw_bar(mem['percent'], 50)
        
        # Disk
        disk = status['disk']
        disk_color = Colors.GREEN if disk['status'] == 'good' else Colors.YELLOW if disk['status'] == 'warning' else Colors.RED
        print(f"\n💿 Disk: {disk_color}{disk['percent']:.1f}%{Colors.RESET} ({disk['used_gb']:.1f}/{disk['total_gb']:.1f} GB)")
        self._draw_bar(disk['percent'], 50)
        
        # Load Average
        print(f"\n⚖️  Load Average: {status['load_average'][0]:.2f}, {status['load_average'][1]:.2f}, {status['load_average'][2]:.2f}")
        
        # Prosesser
        print(f"\n🔧 Aktive prosesser: {status['process_count']}")
        
        print(f"\n{'='*70}")
    
    def _draw_bar(self, percent: float, width: int = 40):
        """Tegn progress bar"""
        filled = int(width * percent / 100)
        bar = '█' * filled + '░' * (width - filled)
        print(f"[{bar}] {percent:.1f}%")
    
    def check_alerts(self) -> List[str]:
        """Sjekk for varsler"""
        alerts = []
        status = self.get_current_status()
        
        if not status:
            return alerts
        
        if status['cpu']['status'] == 'critical':
            alerts.append("🔴 CPU bruk er kritisk høy!")
        elif status['cpu']['status'] == 'warning':
            alerts.append("🟠 CPU bruk er høy")
        
        if status['memory']['status'] == 'critical':
            alerts.append("🔴 Minnebruk er kritisk høy!")
        elif status['memory']['status'] == 'warning':
            alerts.append("🟠 Minnebruk er høy")
        
        if status['disk']['status'] == 'critical':
            alerts.append("🔴 Disk er nesten full!")
        elif status['disk']['status'] == 'warning':
            alerts.append("🟠 Disk begynner å bli full")
        
        return alerts

def main():
    """Hovedfunksjon"""
    print("="*70)
    print("📊 PERFORMANCE MONITOR")
    print("="*70)
    
    monitor = PerformanceMonitor()
    
    print("\n📸 Tar ytelses-snapshot...")
    snapshot = monitor.capture()
    
    print("✅ Snapshot lagret")
    
    # Vis dashboard
    monitor.display_dashboard()
    
    # Sjekk varsler
    alerts = monitor.check_alerts()
    if alerts:
        print(f"{Colors.YELLOW}⚠️  VARSLER:{Colors.RESET}")
        for alert in alerts:
            print(f"   {alert}")
    else:
        print(f"{Colors.GREEN}✅ Alle systemer innen normale grenser{Colors.RESET}")
    
    print("\n" + "="*70)
    print("✅ Performance Monitor fullført!")
    print("="*70)

if __name__ == "__main__":
    main()
