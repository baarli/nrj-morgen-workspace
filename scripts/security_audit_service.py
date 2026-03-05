#!/usr/bin/env python3
"""
🔐 BAARLICLAW SECURITY AUDIT SERVICE
Sikkerhets-skanning og audit av systemet
"""

import sys
import os
import stat
import hashlib
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict
from pathlib import Path

sys.path.insert(0, '/root/.openclaw/workspace/scripts')

from baarliclaw_toolkit import setup_logging
from date_toolkit import DateUtils
from cli_toolkit import TerminalUI, Colors

logger = setup_logging("security-audit")

@dataclass
class SecurityFinding:
    """Et sikkerhets-funn"""
    severity: str  # critical, high, medium, low
    category: str
    message: str
    file_path: Optional[str]
    recommendation: str
    
    def to_dict(self) -> Dict:
        return asdict(self)

class SecurityAuditService:
    """Sikkerhets-audit tjeneste"""
    
    # Kritiske filer som må sjekkes
    CRITICAL_FILES = [
        '/root/.openclaw/workspace/.credentials',
        '/root/.openclaw/workspace/.env',
        '/root/.openclaw/workspace/.config',
    ]
    
    # Farlige fil-rettigheter
    DANGEROUS_PERMISSIONS = [
        (stat.S_IWOTH, "world-writable"),
        (stat.S_IXOTH, "world-executable"),
        (stat.S_IROTH, "world-readable sensitive file"),
    ]
    
    # Sensitive mønstre å lete etter
    SENSITIVE_PATTERNS = [
        (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password"),
        (r'api_key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key"),
        (r'secret\s*=\s*["\'][^"\']+["\']', "Hardcoded secret"),
        (r'token\s*=\s*["\'][^"\']+["\']', "Hardcoded token"),
    ]
    
    def __init__(self):
        self.findings: List[SecurityFinding] = []
        self.scanned_files: int = 0
    
    def check_file_permissions(self, filepath: str) -> List[SecurityFinding]:
        """Sjekk fil-rettigheter"""
        findings = []
        
        try:
            file_stat = os.stat(filepath)
            mode = file_stat.st_mode
            
            # Sjekk om filen er world-writable
            if mode & stat.S_IWOTH:
                findings.append(SecurityFinding(
                    severity="high",
                    category="permissions",
                    message=f"Fil er world-writable: {filepath}",
                    file_path=filepath,
                    recommendation="Fjern skriverettigheter for andre: chmod o-w"
                ))
            
            # Sjekk sensitive filer som er world-readable
            if any(filepath.endswith(ext) for ext in ['.env', '.key', '.pem']):
                if mode & stat.S_IROTH:
                    findings.append(SecurityFinding(
                        severity="critical",
                        category="permissions",
                        message=f"Sensitiv fil er world-readable: {filepath}",
                        file_path=filepath,
                        recommendation="Fjern leserettigheter for andre: chmod o-r"
                    ))
            
        except OSError:
            pass
        
        return findings
    
    def scan_for_secrets(self, filepath: str) -> List[SecurityFinding]:
        """Skann etter hemmeligheter i kode"""
        findings = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            import re
            for i, line in enumerate(lines, 1):
                for pattern, description in self.SENSITIVE_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        findings.append(SecurityFinding(
                            severity="critical",
                            category="secrets",
                            message=f"{description} funnet i {filepath}:{i}",
                            file_path=filepath,
                            recommendation="Bruk miljøvariabler eller secrets manager"
                        ))
        
        except (IOError, UnicodeDecodeError):
            pass
        
        return findings
    
    def check_critical_files(self) -> List[SecurityFinding]:
        """Sjekk kritiske filer"""
        findings = []
        
        for path in self.CRITICAL_FILES:
            if os.path.exists(path):
                # Sjekk rettigheter
                findings.extend(self.check_file_permissions(path))
                
                # Sjekk om det er en mappe
                if os.path.isdir(path):
                    # Sjekk at mappen ikke er world-readable
                    try:
                        mode = os.stat(path).st_mode
                        if mode & stat.S_IROTH:
                            findings.append(SecurityFinding(
                                severity="high",
                                category="permissions",
                                message=f"Kritisk mappe er world-readable: {path}",
                                file_path=path,
                                recommendation="Begrens tilgang til mappen"
                            ))
                    except OSError:
                        pass
            else:
                findings.append(SecurityFinding(
                    severity="medium",
                    category="missing",
                    message=f"Kritisk fil/mappe mangler: {path}",
                    file_path=path,
                    recommendation="Verifiser at dette er forventet"
                ))
        
        return findings
    
    def audit_directory(self, directory: str, max_files: int = 100) -> List[SecurityFinding]:
        """Audit en hel mappe"""
        findings = []
        files_scanned = 0
        
        for root, dirs, files in os.walk(directory):
            # Skip .git og __pycache__
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules']]
            
            for file in files:
                if files_scanned >= max_files:
                    break
                
                filepath = os.path.join(root, file)
                
                # Sjekk kun relevante filtyper
                if file.endswith(('.py', '.sh', '.env', '.json', '.yaml', '.yml')):
                    findings.extend(self.check_file_permissions(filepath))
                    findings.extend(self.scan_for_secrets(filepath))
                    files_scanned += 1
            
            if files_scanned >= max_files:
                break
        
        self.scanned_files = files_scanned
        return findings
    
    def run_full_audit(self) -> List[SecurityFinding]:
        """Kjør full audit"""
        self.findings = []
        
        logger.info("Starter sikkerhets-audit...")
        
        # Sjekk kritiske filer
        self.findings.extend(self.check_critical_files())
        
        # Audit scripts-mappe
        self.findings.extend(
            self.audit_directory('/root/.openclaw/workspace/scripts', max_files=50)
        )
        
        logger.info(f"Audit fullført. {len(self.findings)} funn.")
        return self.findings
    
    def get_summary(self) -> Dict[str, Any]:
        """Hent oppsummering"""
        by_severity = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        by_category = {}
        
        for finding in self.findings:
            by_severity[finding.severity] = by_severity.get(finding.severity, 0) + 1
            by_category[finding.category] = by_category.get(finding.category, 0) + 1
        
        # Beregn total score (100 = perfekt)
        score = 100
        score -= by_severity['critical'] * 20
        score -= by_severity['high'] * 10
        score -= by_severity['medium'] * 5
        score -= by_severity['low'] * 2
        score = max(0, score)
        
        return {
            'total_findings': len(self.findings),
            'by_severity': by_severity,
            'by_category': by_category,
            'security_score': score,
            'files_scanned': self.scanned_files,
            'audit_time': DateUtils.format(DateUtils.now())
        }
    
    def display_report(self):
        """Vis audit-rapport"""
        summary = self.get_summary()
        
        print(f"\n{'='*70}")
        print(f"{Colors.CYAN}🔐 SECURITY AUDIT REPORT{Colors.RESET}")
        print(f"{'='*70}")
        
        # Sikkerhets-score
        score = summary['security_score']
        if score >= 90:
            score_color = Colors.GREEN
        elif score >= 70:
            score_color = Colors.YELLOW
        else:
            score_color = Colors.RED
        
        print(f"\n🛡️  Sikkerhets-score: {score_color}{score}/100{Colors.RESET}")
        print(f"   Filer skannet: {summary['files_scanned']}")
        print(f"   Totale funn: {summary['total_findings']}")
        
        # Fordeling etter alvorlighet
        print(f"\n📊 Fordeling etter alvorlighet:")
        severity_icons = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🔵'}
        for sev, count in summary['by_severity'].items():
            if count > 0:
                print(f"   {severity_icons.get(sev, '⚪')} {sev.upper()}: {count}")
        
        # Vis kritiske funn
        critical = [f for f in self.findings if f.severity == 'critical']
        if critical:
            print(f"\n🔴 Kritiske funn:")
            for finding in critical[:5]:
                print(f"   • {finding.message}")
                print(f"     → {finding.recommendation}")
        
        print(f"{'='*70}")

def main():
    """Hovedfunksjon"""
    print("="*70)
    print("🔐 SECURITY AUDIT SERVICE")
    print("="*70)
    
    auditor = SecurityAuditService()
    
    print("\n🔍 Kjører sikkerhets-audit...")
    auditor.run_full_audit()
    
    # Vis rapport
    auditor.display_report()
    
    # Lagre resultat
    result_file = '/tmp/security_audit_result.json'
    with open(result_file, 'w') as f:
        json.dump({
            'summary': auditor.get_summary(),
            'findings': [f.to_dict() for f in auditor.findings]
        }, f, indent=2)
    
    print(f"\n💾 Resultat lagret til: {result_file}")
    
    print("\n" + "="*70)
    print("✅ Security Audit Service klar!")
    print("="*70)

if __name__ == "__main__":
    main()
