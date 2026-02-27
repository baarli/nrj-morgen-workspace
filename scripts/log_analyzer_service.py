#!/usr/bin/env python3
"""
📜 BAARLICLAW LOG ANALYZER SERVICE
Intelligent analyse av loggfiler med mønster-gjenkjenning
"""

import sys
import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict

sys.path.insert(0, '/root/.openclaw/workspace/scripts')

from baarliclaw_toolkit import setup_logging
from date_toolkit import DateUtils
from cli_toolkit import TerminalUI, Colors

logger = setup_logging("log-analyzer")

@dataclass
class LogEntry:
    """En logg-entry"""
    timestamp: Optional[str]
    level: str
    message: str
    source: str
    line_number: int
    
    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class LogPattern:
    """Et oppdaget mønster"""
    pattern: str
    count: int
    examples: List[str]
    severity: str

class LogAnalyzer:
    """Logg-analysator"""
    
    # Log-nivå mønstre
    LEVEL_PATTERNS = {
        'ERROR': r'\bERROR\b|\bEXCEPTION\b|\bCRITICAL\b',
        'WARNING': r'\bWARNING\b|\bWARN\b',
        'INFO': r'\bINFO\b|\bINFORMATION\b',
        'DEBUG': r'\bDEBUG\b',
    }
    
    # Vanlige feil-mønstre
    ERROR_PATTERNS = [
        (r'Connection.*refused', 'Connection Error', 'high'),
        (r'Timeout', 'Timeout Error', 'medium'),
        (r'Permission.*denied', 'Permission Error', 'high'),
        (r'File.*not found', 'Missing File', 'medium'),
        (r'Memory.*exhausted', 'Memory Error', 'critical'),
        (r'Disk.*full', 'Disk Full', 'critical'),
    ]
    
    def __init__(self):
        self.entries: List[LogEntry] = []
        self.patterns: List[LogPattern] = []
    
    def parse_line(self, line: str, line_number: int, source: str = "unknown") -> Optional[LogEntry]:
        """Parse en logg-linje"""
        # Finn log-nivå
        level = 'INFO'
        for lvl, pattern in self.LEVEL_PATTERNS.items():
            if re.search(pattern, line, re.IGNORECASE):
                level = lvl
                break
        
        # Prøv å finne timestamp
        timestamp = None
        ts_patterns = [
            r'(\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}:\d{2})',
            r'(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2})',
            r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})',
        ]
        
        for pattern in ts_patterns:
            match = re.search(pattern, line)
            if match:
                timestamp = match.group(1)
                break
        
        # Ekstraher melding (fjern timestamp og log-nivå)
        message = line
        if timestamp:
            message = re.sub(re.escape(timestamp), '', message, count=1)
        for pattern in self.LEVEL_PATTERNS.values():
            message = re.sub(pattern, '', message, flags=re.IGNORECASE)
        message = message.strip(' []-:')
        
        return LogEntry(
            timestamp=timestamp,
            level=level,
            message=message[:200],  # Begrens lengde
            source=source,
            line_number=line_number
        )
    
    def analyze_file(self, filepath: str) -> 'LogAnalyzer':
        """Analyser en logg-fil"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if line:
                    entry = self.parse_line(line, i, filepath)
                    if entry:
                        self.entries.append(entry)
            
            self._analyze_patterns()
            logger.info(f"Analyserte {len(self.entries)} logg-linjer fra {filepath}")
            
        except FileNotFoundError:
            logger.error(f"Fil ikke funnet: {filepath}")
        
        return self
    
    def _analyze_patterns(self):
        """Analyser mønstre i loggene"""
        # Tell log-nivåer
        level_counts = Counter(e.level for e in self.entries)
        
        # Finn feil-mønstre
        for pattern, name, severity in self.ERROR_PATTERNS:
            matches = []
            for entry in self.entries:
                if re.search(pattern, entry.message, re.IGNORECASE):
                    matches.append(entry.message[:100])
            
            if matches:
                self.patterns.append(LogPattern(
                    pattern=name,
                    count=len(matches),
                    examples=matches[:3],
                    severity=severity
                ))
    
    def get_summary(self) -> Dict[str, Any]:
        """Hent oppsummering"""
        if not self.entries:
            return {"total": 0, "by_level": {}, "patterns": []}
        
        by_level = Counter(e.level for e in self.entries)
        by_source = Counter(e.source for e in self.entries)
        
        # Finn tidsperiode
        timestamps = [e.timestamp for e in self.entries if e.timestamp]
        time_range = None
        if timestamps:
            time_range = f"{timestamps[0]} til {timestamps[-1]}"
        
        return {
            "total": len(self.entries),
            "by_level": dict(by_level),
            "by_source": dict(by_source),
            "time_range": time_range,
            "patterns": [p.to_dict() for p in self.patterns],
            "error_rate": by_level.get('ERROR', 0) / len(self.entries) * 100
        }
    
    def get_errors(self, limit: int = 20) -> List[LogEntry]:
        """Hent feil-entries"""
        errors = [e for e in self.entries if e.level in ['ERROR', 'CRITICAL']]
        return errors[-limit:]
    
    def display_report(self):
        """Vis analyse-rapport"""
        summary = self.get_summary()
        
        print(f"\n{'='*70}")
        print(f"{Colors.CYAN}📜 LOG ANALYZER REPORT{Colors.RESET}")
        print(f"{'='*70}")
        
        print(f"\n📊 Oppsummering:")
        print(f"   Totale entries: {summary['total']}")
        print(f"   Tidsperiode: {summary['time_range'] or 'Ukjent'}")
        print(f"   Feil-rate: {summary['error_rate']:.2f}%")
        
        print(f"\n📈 Fordeling etter nivå:")
        for level, count in summary['by_level'].items():
            icon = {'ERROR': '🔴', 'WARNING': '🟠', 'INFO': '🔵', 'DEBUG': '⚪'}.get(level, '⚪')
            print(f"   {icon} {level}: {count}")
        
        if summary['patterns']:
            print(f"\n🔍 Oppdagede mønstre:")
            for pattern in summary['patterns']:
                severity_icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '⚪'}.get(pattern['severity'], '⚪')
                print(f"   {severity_icon} {pattern['pattern']}: {pattern['count']} forekomster")
        
        # Vis siste feil
        errors = self.get_errors(5)
        if errors:
            print(f"\n❌ Siste feil:")
            for entry in errors:
                print(f"   Linje {entry.line_number}: {entry.message[:60]}...")
        
        print(f"{'='*70}")

def main():
    """Hovedfunksjon"""
    print("="*70)
    print("📜 LOG ANALYZER SERVICE")
    print("="*70)
    
    analyzer = LogAnalyzer()
    
    # Analyser noen logg-filer
    log_files = [
        "/root/.openclaw/workspace/.auto-exec-log",
        "/root/.openclaw/workspace/.session-end-log",
    ]
    
    for log_file in log_files:
        if sys.path[0] in log_file or log_file.startswith('/root/.openclaw'):
            print(f"\n📁 Analyserer: {log_file}")
            analyzer.analyze_file(log_file)
    
    # Hvis ingen filer ble funnet, generer test-data
    if not analyzer.entries:
        print("\n📝 Genererer test-logg-data...")
        test_lines = [
            "2026-02-28 01:00:00 INFO System started successfully",
            "2026-02-28 01:00:05 INFO Loading configuration",
            "2026-02-28 01:00:10 WARNING Deprecated API used",
            "2026-02-28 01:00:15 ERROR Connection refused to database",
            "2026-02-28 01:00:16 ERROR Timeout while fetching data",
            "2026-02-28 01:00:20 INFO Retrying connection",
            "2026-02-28 01:00:25 INFO Connection established",
            "2026-02-28 01:00:30 DEBUG Processing request 12345",
            "2026-02-28 01:00:35 INFO Request completed",
            "2026-02-28 01:00:40 ERROR Memory limit approaching",
        ]
        
        for i, line in enumerate(test_lines, 1):
            entry = analyzer.parse_line(line, i, "test.log")
            if entry:
                analyzer.entries.append(entry)
        
        analyzer._analyze_patterns()
    
    # Vis rapport
    analyzer.display_report()
    
    print("\n" + "="*70)
    print("✅ Log Analyzer Service klar!")
    print("="*70)

if __name__ == "__main__":
    main()
