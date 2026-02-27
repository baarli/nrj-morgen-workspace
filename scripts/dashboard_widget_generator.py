#!/usr/bin/env python3
"""
🎨 Dashboard Widget Generator - Generate HTML widgets for Mission Control
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

class DashboardWidgetGenerator:
    """Generate HTML widgets for Mission Control dashboard"""
    
    def __init__(self, output_dir='/root/.openclaw/workspace/mission-control/widgets'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_health_widget(self, data: Dict) -> str:
        """Generate system health widget"""
        score = data.get('health_score', 0)
        status = data.get('status', 'unknown')
        
        color = '#10b981' if score >= 80 else '#f59e0b' if score >= 50 else '#ef4444'
        
        html = f'''
        <div class="widget health-widget" style="border-left: 4px solid {color};">
            <h3>🩺 System Health</h3>
            <div class="health-score" style="color: {color}; font-size: 2em; font-weight: bold;">
                {score}/100
            </div>
            <div class="health-status" style="text-transform: uppercase;">{status}</div>
            <ul class="issues-list">
        '''
        
        for issue in data.get('issues', []):
            html += f'                <li>⚠️ {issue}</li>\n'
        
        html += '''            </ul>
        </div>'''
        
        return html
    
    def generate_metrics_widget(self, data: Dict) -> str:
        """Generate metrics widget"""
        system = data.get('system', {})
        workspace = data.get('workspace', {})
        
        html = '''
        <div class="widget metrics-widget">
            <h3>📊 System Metrics</h3>
            <div class="metrics-grid" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;">
        '''
        
        cpu = system.get('cpu_percent', 'N/A')
        memory = system.get('memory', {}).get('percent', 'N/A')
        disk = system.get('disk', {}).get('percent', 'N/A')
        
        html += f'''                <div class="metric">
                    <div class="metric-label">CPU</div>
                    <div class="metric-value">{cpu}%</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Memory</div>
                    <div class="metric-value">{memory}%</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Disk</div>
                    <div class="metric-value">{disk}%</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Files</div>
                    <div class="metric-value">{workspace.get('file_counts', {}).get('total', 0)}</div>
                </div>
            </div>
        </div>'''
        
        return html
    
    def generate_cron_widget(self, data: Dict) -> str:
        """Generate cron status widget"""
        enabled = data.get('enabled', 0)
        errors = data.get('errors', 0)
        
        status_color = '#10b981' if errors == 0 else '#ef4444'
        
        html = f'''
        <div class="widget cron-widget" style="border-left: 4px solid {status_color};">
            <h3>⏰ Cron Jobs</h3>
            <div class="cron-stats" style="display: flex; gap: 20px;">
                <div class="stat">
                    <div class="stat-value" style="font-size: 1.5em;">{enabled}</div>
                    <div class="stat-label">Enabled</div>
                </div>
                <div class="stat">
                    <div class="stat-value" style="font-size: 1.5em; color: {status_color};">{errors}</div>
                    <div class="stat-label">Errors</div>
                </div>
            </div>
        </div>'''
        
        return html
    
    def generate_all_widgets(self):
        """Generate all dashboard widgets"""
        # Load latest data
        metrics_file = Path('/root/.openclaw/workspace/brain/metrics/latest.json')
        health_file = Path('/root/.openclaw/workspace/brain/reports/system-health-*.json')
        
        widgets = {}
        
        # Generate metrics widget
        if metrics_file.exists():
            with open(metrics_file, 'r') as f:
                metrics_data = json.load(f)
            widgets['metrics'] = self.generate_metrics_widget(metrics_data)
        
        # Save widgets
        for name, html in widgets.items():
            widget_file = self.output_dir / f'{name}-widget.html'
            with open(widget_file, 'w') as f:
                f.write(html)
        
        return widgets


if __name__ == '__main__':
    generator = DashboardWidgetGenerator()
    widgets = generator.generate_all_widgets()
    print(f"Generated {len(widgets)} widgets")
    for name in widgets:
        print(f"  - {name}-widget.html")
