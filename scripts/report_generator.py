#!/usr/bin/env python3
"""
📄 BAARLICLAW REPORT GENERATOR
Automatisk generering av rapporter i ulike formater
"""

import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

sys.path.insert(0, '/root/.openclaw/workspace/scripts')

from baarliclaw_toolkit import setup_logging
from date_toolkit import DateUtils
from cli_toolkit import TerminalUI, Colors

logger = setup_logging("report-generator")

@dataclass
class ReportSection:
    """En seksjon i en rapport"""
    title: str
    content: str
    data: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        return asdict(self)

class ReportGenerator:
    """Rapport-generator"""
    
    def __init__(self, title: str = "BaarliClaw Report"):
        self.title = title
        self.sections: List[ReportSection] = []
        self.generated_at = DateUtils.format(DateUtils.now())
    
    def add_section(self, title: str, content: str = "", data: Dict = None):
        """Legg til seksjon"""
        self.sections.append(ReportSection(
            title=title,
            content=content,
            data=data or {}
        ))
    
    def to_markdown(self) -> str:
        """Generer Markdown-rapport"""
        lines = []
        
        # Header
        lines.append(f"# {self.title}")
        lines.append(f"\n_Generated: {self.generated_at}_")
        lines.append("\n---\n")
        
        # Seksjoner
        for section in self.sections:
            lines.append(f"## {section.title}")
            lines.append("")
            
            if section.content:
                lines.append(section.content)
                lines.append("")
            
            # Data som tabell hvis dict
            if section.data:
                if isinstance(section.data, dict):
                    lines.append("| Key | Value |")
                    lines.append("|-----|-------|")
                    for key, value in section.data.items():
                        lines.append(f"| {key} | {value} |")
                    lines.append("")
                elif isinstance(section.data, list):
                    for item in section.data:
                        lines.append(f"- {item}")
                    lines.append("")
        
        return "\n".join(lines)
    
    def to_html(self) -> str:
        """Generer HTML-rapport"""
        html = []
        
        html.append("<!DOCTYPE html>")
        html.append("<html>")
        html.append("<head>")
        html.append(f"<title>{self.title}</title>")
        html.append("<style>")
        html.append("""
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #333; border-bottom: 2px solid #007bff; }
            h2 { color: #555; margin-top: 30px; }
            table { border-collapse: collapse; width: 100%; margin: 20px 0; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .timestamp { color: #666; font-style: italic; }
        """)
        html.append("</style>")
        html.append("</head>")
        html.append("<body>")
        
        # Header
        html.append(f"<h1>{self.title}</h1>")
        html.append(f"<p class='timestamp'>Generated: {self.generated_at}</p>")
        html.append("<hr>")
        
        # Seksjoner
        for section in self.sections:
            html.append(f"<h2>{section.title}</h2>")
            
            if section.content:
                html.append(f"<p>{section.content}</p>")
            
            if section.data:
                if isinstance(section.data, dict):
                    html.append("<table>")
                    html.append("<tr><th>Key</th><th>Value</th></tr>")
                    for key, value in section.data.items():
                        html.append(f"<tr><td>{key}</td><td>{value}</td></tr>")
                    html.append("</table>")
                elif isinstance(section.data, list):
                    html.append("<ul>")
                    for item in section.data:
                        html.append(f"<li>{item}</li>")
                    html.append("</ul>")
        
        html.append("</body>")
        html.append("</html>")
        
        return "\n".join(html)
    
    def to_json(self) -> str:
        """Generer JSON-rapport"""
        return json.dumps({
            'title': self.title,
            'generated_at': self.generated_at,
            'sections': [s.to_dict() for s in self.sections]
        }, indent=2)
    
    def save(self, filepath: str, format: str = "markdown"):
        """Lagre rapport til fil"""
        if format == "markdown":
            content = self.to_markdown()
        elif format == "html":
            content = self.to_html()
        elif format == "json":
            content = self.to_json()
        else:
            raise ValueError(f"Ukjent format: {format}")
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        logger.info(f"Rapport lagret: {filepath}")

def generate_system_report() -> ReportGenerator:
    """Generer system-rapport"""
    report = ReportGenerator("BaarliClaw System Report")
    
    # System-oversikt
    report.add_section(
        title="System Oversikt",
        content="Oversikt over BaarliClaw-systemet",
        data={
            "Versjon": "10.0",
            "Miljø": "Production",
            "Siste oppstart": DateUtils.format(DateUtils.now()),
            "Tjenester": "9 aktive"
        }
    )
    
    # Tjenester
    report.add_section(
        title="Aktive Tjenester",
        content="Alle tjenester kjører normalt",
        data={
            "Agent Orchestrator": "✅ Running",
            "Notification Service": "✅ Running",
            "Performance Monitor": "✅ Running",
            "Task Queue Manager": "✅ Running",
            "Smart Backup Service": "✅ Running",
            "API Gateway Service": "✅ Running",
            "Metrics Collector": "✅ Running",
            "Log Analyzer Service": "✅ Running",
            "Health Check Service": "✅ Running",
        }
    )
    
    # Verktøy
    report.add_section(
        title="BaarliClaw Toolkit",
        content="50 verktøymoduler tilgjengelig",
        data={
            "Kjerneverktøy": "29",
            "Avanserte verktøy": "21",
            "Totalt": "50"
        }
    )
    
    return report

def main():
    """Hovedfunksjon"""
    print("="*70)
    print("📄 REPORT GENERATOR")
    print("="*70)
    
    # Generer system-rapport
    print("\n📝 Genererer system-rapport...")
    report = generate_system_report()
    
    # Lagre i ulike formater
    formats = [
        ('/tmp/report.md', 'markdown'),
        ('/tmp/report.html', 'html'),
        ('/tmp/report.json', 'json')
    ]
    
    for filepath, format in formats:
        report.save(filepath, format)
        print(f"  ✅ {format.upper()}: {filepath}")
    
    # Vis Markdown-versjon
    print("\n📋 Markdown-rapport (siste 20 linjer):")
    markdown = report.to_markdown()
    for line in markdown.split('\n')[-20:]:
        print(f"  {line}")
    
    print("\n" + "="*70)
    print("✅ Report Generator klar!")
    print("="*70)

if __name__ == "__main__":
    main()
