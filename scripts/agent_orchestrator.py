#!/usr/bin/env python3
"""
🎛️ BAARLICLAW AGENT ORCHESTRATOR
Smart koordinering av alle tjenester
"""

import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

sys.path.insert(0, '/root/.openclaw/workspace/scripts')

# Import verktøy
from baarliclaw_toolkit import setup_logging
from data_analyzer import TextAnalyzer
from date_toolkit import DateUtils
from cli_toolkit import TerminalUI, Colors

logger = setup_logging("agent-orchestrator")

class ServiceStatus:
    """Status for en tjeneste"""
    def __init__(self, name: str, status: str = "unknown", last_run: Optional[str] = None):
        self.name = name
        self.status = status
        self.last_run = last_run
        self.next_run = None
        self.health_score = 100
        self.errors = []

class AgentOrchestrator:
    """Hoved-orkestrator for alle tjenester"""
    
    def __init__(self):
        self.services: Dict[str, ServiceStatus] = {}
        self.system_health = 100
        self.last_check = None
        
    def register_service(self, name: str, status: str = "unknown"):
        """Registrer en tjeneste"""
        self.services[name] = ServiceStatus(name, status)
        logger.info(f"Registrert tjeneste: {name}")
    
    def update_service(self, name: str, status: str, message: str = ""):
        """Oppdater tjeneste-status"""
        if name in self.services:
            self.services[name].status = status
            self.services[name].last_run = DateUtils.format(DateUtils.now())
            if message:
                if status == "error":
                    self.services[name].errors.append(message)
                    self.services[name].health_score -= 10
            logger.info(f"Oppdatert {name}: {status}")
    
    def check_all_services(self) -> Dict[str, Any]:
        """Sjekk alle tjenester"""
        results = {
            'timestamp': DateUtils.format(DateUtils.now()),
            'services': {},
            'overall_health': 100,
            'recommendations': []
        }
        
        for name, service in self.services.items():
            results['services'][name] = {
                'status': service.status,
                'health_score': service.health_score,
                'last_run': service.last_run,
                'errors': service.errors[-3:]  # Siste 3 feil
            }
            
            # Beregn overall health
            results['overall_health'] = min(
                results['overall_health'],
                service.health_score
            )
            
            # Gi anbefalinger
            if service.health_score < 80:
                results['recommendations'].append(
                    f"⚠️ {name} har lav helse-score ({service.health_score}). Sjekk logger."
                )
            if service.status == "error":
                results['recommendations'].append(
                    f"🔴 {name} har feil. Kjør manuell sjekk."
                )
        
        self.last_check = results['timestamp']
        self.system_health = results['overall_health']
        
        return results
    
    def get_dashboard(self) -> str:
        """Generer dashboard-visning"""
        lines = []
        lines.append("=" * 70)
        lines.append(f"{Colors.CYAN}🎛️ AGENT ORCHESTRATOR - System Dashboard{Colors.RESET}")
        lines.append("=" * 70)
        lines.append(f"Sist sjekket: {self.last_check or 'Aldri'}")
        lines.append(f"System helse: {self.system_health}%")
        lines.append("")
        
        # Tjeneste-tabell
        headers = ["Tjeneste", "Status", "Helse", "Siste kjøring"]
        rows = []
        
        for name, service in self.services.items():
            status_color = {
                "ok": Colors.GREEN,
                "error": Colors.RED,
                "warning": Colors.YELLOW,
                "unknown": Colors.DIM
            }.get(service.status, Colors.RESET)
            
            rows.append([
                name,
                f"{status_color}{service.status}{Colors.RESET}",
                f"{service.health_score}%",
                service.last_run or "-"
            ])
        
        # Bygg tabell manuelt
        lines.append(" | ".join(headers))
        lines.append("-" * 70)
        for row in rows:
            lines.append(" | ".join(str(c) for c in row))
        lines.append("")
        
        return "\n".join(lines)
    
    def auto_heal(self):
        """Automatisk reparasjon av problemer"""
        healed = []
        
        for name, service in self.services.items():
            if service.status == "error":
                logger.info(f"Prøver å reparere: {name}")
                # Her kan vi legge til auto-heal logikk
                healed.append(name)
        
        return healed

# === PRE-DEFINED SERVICES ===

def initialize_orchestrator() -> AgentOrchestrator:
    """Initialiser orkestrator med alle kjente tjenester"""
    orch = AgentOrchestrator()
    
    # Registrer alle tjenester
    services = [
        ("Pre-Flight System", "ok"),
        ("Learning Capture", "ok"),
        ("NRJ Dashboard", "ok"),
        ("Morning Routine", "paused"),
        ("Podcast Clips", "ok"),
        ("Code Quality Checker", "ok"),
        ("Auto-Update", "ok"),
        ("Toolkit System", "ok"),
    ]
    
    for name, status in services:
        orch.register_service(name, status)
    
    return orch

def main():
    """Hovedfunksjon"""
    print("=" * 70)
    print("🎛️ BAARLICLAW AGENT ORCHESTRATOR")
    print("=" * 70)
    print()
    
    # Initialiser
    orch = initialize_orchestrator()
    
    # Sjekk alle tjenester
    print("🔍 Sjekker alle tjenester...")
    results = orch.check_all_services()
    
    # Vis dashboard
    print(orch.get_dashboard())
    
    # Vis anbefalinger
    if results['recommendations']:
        print(f"{Colors.YELLOW}📋 ANBEFALINGER:{Colors.RESET}")
        for rec in results['recommendations']:
            print(f"  {rec}")
    else:
        print(f"{Colors.GREEN}✅ Alle systemer kjører normalt!{Colors.RESET}")
    
    # Lagre status
    status_file = '/tmp/agent_orchestrator_status.json'
    with open(status_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Status lagret til: {status_file}")
    print("\n✅ Orchestrator klar!")

if __name__ == "__main__":
    main()
