#!/usr/bin/env python3
"""
🏥 BAARLICLAW HEALTH CHECK SERVICE
Komplett helse-sjekk av alle systemer
"""

import sys
import os
import json
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

sys.path.insert(0, '/root/.openclaw/workspace/scripts')

from baarliclaw_toolkit import setup_logging
from date_toolkit import DateUtils
from cli_toolkit import TerminalUI, Colors

logger = setup_logging("health-check")

@dataclass
class HealthCheckResult:
    """Resultat av en helse-sjekk"""
    name: str
    status: str  # healthy, warning, critical
    message: str
    response_time_ms: float
    details: Dict[str, Any]
    timestamp: str
    
    def to_dict(self) -> Dict:
        return asdict(self)

class HealthCheckService:
    """Helse-sjekk tjeneste"""
    
    def __init__(self):
        self.checks: List[HealthCheckResult] = []
        self.check_functions: Dict[str, callable] = {}
    
    def register_check(self, name: str, func: callable):
        """Registrer en sjekk-funksjon"""
        self.check_functions[name] = func
        logger.info(f"Registrert helse-sjekk: {name}")
    
    def run_check(self, name: str) -> HealthCheckResult:
        """Kjør en sjekk"""
        import time
        
        start = time.time()
        
        try:
            if name not in self.check_functions:
                return HealthCheckResult(
                    name=name,
                    status="critical",
                    message=f"Sjekk '{name}' ikke registrert",
                    response_time_ms=0,
                    details={},
                    timestamp=DateUtils.format(DateUtils.now())
                )
            
            result = self.check_functions[name]()
            elapsed = (time.time() - start) * 1000
            
            return HealthCheckResult(
                name=name,
                status=result.get('status', 'unknown'),
                message=result.get('message', ''),
                response_time_ms=elapsed,
                details=result.get('details', {}),
                timestamp=DateUtils.format(DateUtils.now())
            )
            
        except Exception as e:
            elapsed = (time.time() - start) * 1000
            return HealthCheckResult(
                name=name,
                status="critical",
                message=str(e),
                response_time_ms=elapsed,
                details={"error": str(e)},
                timestamp=DateUtils.format(DateUtils.now())
            )
    
    def run_all_checks(self) -> List[HealthCheckResult]:
        """Kjør alle registrerte sjekker"""
        self.checks = []
        
        for name in self.check_functions.keys():
            result = self.run_check(name)
            self.checks.append(result)
        
        return self.checks
    
    def get_overall_status(self) -> str:
        """Hent overall status"""
        if not self.checks:
            return "unknown"
        
        statuses = [c.status for c in self.checks]
        
        if "critical" in statuses:
            return "critical"
        elif "warning" in statuses:
            return "warning"
        else:
            return "healthy"
    
    def display_report(self):
        """Vis helse-rapport"""
        print(f"\n{'='*70}")
        print(f"{Colors.CYAN}🏥 HEALTH CHECK REPORT{Colors.RESET}")
        print(f"{'='*70}")
        
        overall = self.get_overall_status()
        status_color = {
            'healthy': Colors.GREEN,
            'warning': Colors.YELLOW,
            'critical': Colors.RED,
            'unknown': Colors.DIM
        }.get(overall, Colors.RESET)
        
        print(f"\nOverall Status: {status_color}{overall.upper()}{Colors.RESET}")
        print(f"Sjekket: {DateUtils.format(DateUtils.now())}")
        print(f"Antall sjekker: {len(self.checks)}")
        
        print(f"\n📋 Individuelle sjekker:")
        for check in self.checks:
            icon = {
                'healthy': '✅',
                'warning': '⚠️',
                'critical': '❌',
                'unknown': '❓'
            }.get(check.status, '❓')
            
            status_text = f"{check.status.upper()} ({check.response_time_ms:.1f}ms)"
            print(f"  {icon} {check.name}: {status_text}")
            if check.message:
                print(f"     {check.message}")
        
        print(f"{'='*70}")

# === PRE-DEFINED CHECKS ===

def check_disk_space() -> Dict:
    """Sjekk disk-plass"""
    try:
        stat = os.statvfs('/')
        free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
        total_gb = (stat.f_blocks * stat.f_frsize) / (1024**3)
        used_percent = ((total_gb - free_gb) / total_gb) * 100
        
        if used_percent > 95:
            status = "critical"
        elif used_percent > 80:
            status = "warning"
        else:
            status = "healthy"
        
        return {
            'status': status,
            'message': f"{free_gb:.1f} GB ledig av {total_gb:.1f} GB",
            'details': {
                'free_gb': free_gb,
                'total_gb': total_gb,
                'used_percent': used_percent
            }
        }
    except Exception as e:
        return {'status': 'critical', 'message': str(e), 'details': {}}

def check_memory() -> Dict:
    """Sjekk minne"""
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        
        mem_total = 0
        mem_available = 0
        
        for line in lines:
            if line.startswith('MemTotal:'):
                mem_total = int(line.split()[1]) / 1024  # MB
            elif line.startswith('MemAvailable:'):
                mem_available = int(line.split()[1]) / 1024  # MB
        
        used_percent = ((mem_total - mem_available) / mem_total) * 100 if mem_total > 0 else 0
        
        if used_percent > 95:
            status = "critical"
        elif used_percent > 85:
            status = "warning"
        else:
            status = "healthy"
        
        return {
            'status': status,
            'message': f"{mem_available:.0f} MB ledig av {mem_total:.0f} MB",
            'details': {
                'total_mb': mem_total,
                'available_mb': mem_available,
                'used_percent': used_percent
            }
        }
    except Exception as e:
        return {'status': 'critical', 'message': str(e), 'details': {}}

def check_services() -> Dict:
    """Sjekk at viktige tjenester kjører"""
    required_files = [
        '/root/.openclaw/workspace/scripts/agent_orchestrator.py',
        '/root/.openclaw/workspace/scripts/smart_notification_service.py',
        '/root/.openclaw/workspace/scripts/performance_monitor.py',
    ]
    
    missing = []
    for f in required_files:
        if not os.path.exists(f):
            missing.append(os.path.basename(f))
    
    if missing:
        return {
            'status': 'warning',
            'message': f"Mangler filer: {', '.join(missing)}",
            'details': {'missing': missing}
        }
    
    return {
        'status': 'healthy',
        'message': f"Alle {len(required_files)} tjenester tilgjengelig",
        'details': {'services_count': len(required_files)}
    }

def check_logs() -> Dict:
    """Sjekk logg-filer for feil"""
    log_files = [
        '/root/.openclaw/workspace/.auto-exec-log',
        '/root/.openclaw/workspace/.session-end-log',
    ]
    
    total_errors = 0
    for log_file in log_files:
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    content = f.read()
                    total_errors += content.lower().count('error')
            except:
                pass
    
    if total_errors > 10:
        status = "warning"
    else:
        status = "healthy"
    
    return {
        'status': status,
        'message': f"{total_errors} feil funnet i logger",
        'details': {'error_count': total_errors}
    }

def main():
    """Hovedfunksjon"""
    print("="*70)
    print("🏥 HEALTH CHECK SERVICE")
    print("="*70)
    
    service = HealthCheckService()
    
    # Registrer sjekker
    service.register_check("Disk Space", check_disk_space)
    service.register_check("Memory", check_memory)
    service.register_check("Services", check_services)
    service.register_check("Logs", check_logs)
    
    print("\n🔍 Kjører helse-sjekker...")
    service.run_all_checks()
    
    # Vis rapport
    service.display_report()
    
    # Lagre resultat
    result_file = '/tmp/health_check_result.json'
    with open(result_file, 'w') as f:
        json.dump({
            'timestamp': DateUtils.format(DateUtils.now()),
            'overall_status': service.get_overall_status(),
            'checks': [c.to_dict() for c in service.checks]
        }, f, indent=2)
    
    print(f"\n💾 Resultat lagret til: {result_file}")
    
    print("\n" + "="*70)
    print("✅ Health Check Service klar!")
    print("="*70)

if __name__ == "__main__":
    main()
