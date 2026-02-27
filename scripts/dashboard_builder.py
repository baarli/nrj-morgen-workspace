#!/usr/bin/env python3
"""
📊 BAARLICLAW DASHBOARD BUILDER
Bygg interaktive dashboards med Streamlit-lignende syntaks
"""

import os
import sys
import json
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("DashboardBuilder")

@dataclass
class Component:
    """Base dashboard component"""
    type: str
    props: Dict[str, Any] = field(default_factory=dict)

class DashboardBuilder:
    """Build HTML dashboards programmatically"""
    
    def __init__(self, title: str = "Dashboard"):
        self.title = title
        self.components: List[Component] = []
        self.css = self._default_css()
        self.js = self._default_js()
    
    def _default_css(self) -> str:
        """Default dashboard CSS"""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            line-height: 1.6;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 24px;
            border: 1px solid #334155;
        }
        .header h1 { font-size: 2rem; color: #f8fafc; margin-bottom: 8px; }
        .header p { color: #94a3b8; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }
        .card {
            background: #1e293b;
            border-radius: 12px;
            padding: 24px;
            border: 1px solid #334155;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }
        .card h3 {
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #94a3b8;
            margin-bottom: 12px;
        }
        .metric {
            font-size: 2.5rem;
            font-weight: 700;
            color: #f8fafc;
            margin-bottom: 8px;
        }
        .metric.positive { color: #22c55e; }
        .metric.negative { color: #ef4444; }
        .metric.neutral { color: #3b82f6; }
        .change {
            font-size: 0.875rem;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .change.positive { color: #22c55e; }
        .change.negative { color: #ef4444; }
        .chart-container {
            background: #1e293b;
            border-radius: 12px;
            padding: 24px;
            border: 1px solid #334155;
            margin-bottom: 20px;
        }
        .chart-container h3 {
            margin-bottom: 16px;
            color: #f8fafc;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #334155;
        }
        th {
            color: #94a3b8;
            font-weight: 500;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
        }
        td { color: #e2e8f0; }
        tr:hover td { background: #334155; }
        .badge {
            display: inline-flex;
            align-items: center;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 500;
        }
        .badge.success { background: rgba(34, 197, 94, 0.2); color: #22c55e; }
        .badge.warning { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }
        .badge.error { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #334155;
            border-radius: 4px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6);
            border-radius: 4px;
            transition: width 0.5s ease;
        }
        """
    
    def _default_js(self) -> str:
        """Default dashboard JavaScript"""
        return """
        // Auto-refresh every 60 seconds
        setInterval(() => {
            location.reload();
        }, 60000);
        
        // Animate progress bars
        document.querySelectorAll('.progress-fill').forEach(bar => {
            const width = bar.style.width;
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.width = width;
            }, 100);
        });
        """
    
    def header(self, title: str, subtitle: str = ""):
        """Add header section"""
        self.components.append(Component("header", {
            "title": title,
            "subtitle": subtitle
        }))
        return self
    
    def metric(self, label: str, value: Any, 
               change: Optional[float] = None,
               prefix: str = "",
               suffix: str = "",
               positive_is_good: bool = True):
        """Add metric card"""
        self.components.append(Component("metric", {
            "label": label,
            "value": value,
            "change": change,
            "prefix": prefix,
            "suffix": suffix,
            "positive_is_good": positive_is_good
        }))
        return self
    
    def chart(self, chart_type: str, data: List[Dict], 
              title: str = "", x_key: str = "x", y_key: str = "y"):
        """Add chart (line, bar, pie)"""
        self.components.append(Component("chart", {
            "type": chart_type,
            "data": data,
            "title": title,
            "x_key": x_key,
            "y_key": y_key
        }))
        return self
    
    def table(self, data: List[Dict], columns: Optional[List[str]] = None,
              title: str = ""):
        """Add data table"""
        self.components.append(Component("table", {
            "data": data,
            "columns": columns or (list(data[0].keys()) if data else []),
            "title": title
        }))
        return self
    
    def progress(self, label: str, value: float, max_value: float = 100):
        """Add progress bar"""
        percentage = (value / max_value) * 100
        self.components.append(Component("progress", {
            "label": label,
            "value": value,
            "max_value": max_value,
            "percentage": percentage
        }))
        return self
    
    def divider(self):
        """Add horizontal divider"""
        self.components.append(Component("divider", {}))
        return self
    
    def _render_component(self, component: Component) -> str:
        """Render single component to HTML"""
        if component.type == "header":
            return f'''
            <div class="header">
                <h1>{component.props["title"]}</h1>
                {f"<p>{component.props['subtitle']}</p>" if component.props.get("subtitle") else ""}
            </div>
            '''
        
        elif component.type == "metric":
            value = component.props["value"]
            change = component.props.get("change")
            prefix = component.props.get("prefix", "")
            suffix = component.props.get("suffix", "")
            
            # Determine color class
            color_class = "neutral"
            if change is not None:
                positive_good = component.props.get("positive_is_good", True)
                if (change > 0 and positive_good) or (change < 0 and not positive_good):
                    color_class = "positive"
                else:
                    color_class = "negative"
            
            change_html = ""
            if change is not None:
                arrow = "↑" if change > 0 else "↓"
                change_html = f'<div class="change {color_class}">{arrow} {abs(change):.1f}%</div>'
            
            return f'''
            <div class="card">
                <h3>{component.props["label"]}</h3>
                <div class="metric {color_class}">{prefix}{value}{suffix}</div>
                {change_html}
            </div>
            '''
        
        elif component.type == "chart":
            chart_type = component.props["type"]
            data = component.props["data"]
            
            if chart_type == "bar":
                # Simple CSS bar chart
                max_val = max(d[component.props["y_key"]] for d in data) if data else 1
                bars = ""
                for d in data:
                    height = (d[component.props["y_key"]] / max_val) * 200
                    bars += f'''
                    <div style="display: inline-block; margin-right: 10px; text-align: center;">
                        <div style="height: {height}px; width: 40px; background: linear-gradient(180deg, #3b82f6, #8b5cf6); border-radius: 4px;"></div>
                        <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px;">{d[component.props["x_key"]]}</div>
                    </div>
                    '''
                
                return f'''
                <div class="chart-container">
                    <h3>{component.props["title"]}</h3>
                    <div style="display: flex; align-items: flex-end; height: 220px; padding: 20px 0;">
                        {bars}
                    </div>
                </div>
                '''
            
            elif chart_type == "line":
                # SVG line chart
                if not data:
                    return '<div class="chart-container"><h3>No data</h3></div>'
                
                x_key = component.props["x_key"]
                y_key = component.props["y_key"]
                
                values = [d[y_key] for d in data]
                min_val, max_val = min(values), max(values)
                val_range = max_val - min_val if max_val != min_val else 1
                
                points = []
                width, height = 600, 200
                for i, d in enumerate(data):
                    x = (i / (len(data) - 1)) * width if len(data) > 1 else width / 2
                    y = height - ((d[y_key] - min_val) / val_range) * height
                    points.append(f"{x},{y}")
                
                polyline = " ".join(points)
                
                return f'''
                <div class="chart-container">
                    <h3>{component.props["title"]}</h3>
                    <svg width="100%" height="220" viewBox="0 0 {width} {height}" style="overflow: visible;">
                        <polyline points="{polyline}" fill="none" stroke="#3b82f6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
                        {''.join(f'<circle cx="{p.split(",")[0]}" cy="{p.split(",")[1]}" r="4" fill="#8b5cf6"/>' for p in points)}
                    </svg>
                </div>
                '''
        
        elif component.type == "table":
            columns = component.props["columns"]
            data = component.props["data"]
            
            header_html = "".join(f"<th>{col}</th>" for col in columns)
            
            rows_html = ""
            for row in data:
                row_html = ""
                for col in columns:
                    value = row.get(col, "")
                    # Format badges
                    if isinstance(value, str) and value.lower() in ["active", "success", "completed"]:
                        value = f'<span class="badge success">{value}</span>'
                    elif isinstance(value, str) and value.lower() in ["pending", "warning"]:
                        value = f'<span class="badge warning">{value}</span>'
                    elif isinstance(value, str) and value.lower() in ["error", "failed"]:
                        value = f'<span class="badge error">{value}</span>'
                    row_html += f"<td>{value}</td>"
                rows_html += f"<tr>{row_html}</tr>"
            
            return f'''
            <div class="chart-container">
                <h3>{component.props["title"]}</h3>
                <table>
                    <thead><tr>{header_html}</tr></thead>
                    <tbody>{rows_html}</tbody>
                </table>
            </div>
            '''
        
        elif component.type == "progress":
            return f'''
            <div class="card">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>{component.props["label"]}</span>
                    <span style="color: #94a3b8;">{component.props["value"]}/{component.props["max_value"]}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {component.props["percentage"]}%"></div>
                </div>
            </div>
            '''
        
        elif component.type == "divider":
            return '<hr style="border: none; border-top: 1px solid #334155; margin: 24px 0;">'
        
        return ""
    
    def build(self) -> str:
        """Build complete HTML dashboard"""
        components_html = ""
        metrics_html = ""
        
        for comp in self.components:
            if comp.type == "metric":
                metrics_html += self._render_component(comp)
            else:
                components_html += self._render_component(comp)
        
        # Wrap metrics in grid
        if metrics_html:
            metrics_html = f'<div class="grid">{metrics_html}</div>'
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    <style>{self.css}</style>
</head>
<body>
    <div class="container">
        {metrics_html}
        {components_html}
    </div>
    <script>{self.js}</script>
</body>
</html>'''
        
        return html
    
    def save(self, filepath: str):
        """Save dashboard to file"""
        html = self.build()
        with open(filepath, 'w') as f:
            f.write(html)
        logger.info(f"Dashboard saved to {filepath}")

# === QUICK DASHBOARD FUNCTIONS ===
def create_metrics_dashboard(title: str, metrics: List[Dict], 
                            output_path: str = "/tmp/dashboard.html"):
    """Quick metrics dashboard"""
    db = DashboardBuilder(title)
    db.header(title, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    for m in metrics:
        db.metric(
            label=m.get("label", "Metric"),
            value=m.get("value", 0),
            change=m.get("change"),
            prefix=m.get("prefix", ""),
            suffix=m.get("suffix", "")
        )
    
    db.save(output_path)
    return output_path

def create_system_dashboard(output_path: str = "/tmp/system_dashboard.html"):
    """Quick system status dashboard"""
    import subprocess
    
    # Get system info
    try:
        disk = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
        disk_usage = disk.stdout.split('\n')[1].split()[4] if disk.returncode == 0 else "N/A"
    except:
        disk_usage = "N/A"
    
    try:
        mem = subprocess.run(['free', '-m'], capture_output=True, text=True)
        mem_lines = mem.stdout.split('\n')
        if len(mem_lines) > 1:
            mem_info = mem_lines[1].split()
            mem_used = int(mem_info[2])
            mem_total = int(mem_info[1])
            mem_pct = (mem_used / mem_total) * 100
        else:
            mem_pct = 0
    except:
        mem_pct = 0
    
    db = DashboardBuilder("System Dashboard")
    db.header("System Status", "Real-time system monitoring")
    
    db.metric("Disk Usage", disk_usage)
    db.metric("Memory Usage", f"{mem_pct:.1f}", suffix="%")
    db.metric("Active Processes", "Running")
    
    db.save(output_path)
    return output_path

# === TESTING ===
if __name__ == "__main__":
    print("📊 BaarliClaw Dashboard Builder - Testing")
    print("=" * 50)
    
    # Test full dashboard
    db = DashboardBuilder("NRJ Morgen Dashboard")
    
    db.header("NRJ Morgen", "Daily performance metrics")
    
    db.metric("Downloads", 16500, change=5.2, suffix="")
    db.metric("Ranking", 62, change=-3, positive_is_good=False)
    db.metric("Listeners", 69000, change=12.5, suffix="")
    
    db.divider()
    
    db.chart("line", [
        {"day": "Mon", "downloads": 15000},
        {"day": "Tue", "downloads": 15800},
        {"day": "Wed", "downloads": 16200},
        {"day": "Thu", "downloads": 16500},
        {"day": "Fri", "downloads": 16900},
    ], title="Weekly Downloads", x_key="day", y_key="downloads")
    
    db.table([
        {"episode": "#1", "title": "Premiere", "status": "Completed", "downloads": 25000},
        {"episode": "#2", "title": "Therapy Session", "status": "Active", "downloads": 18000},
        {"episode": "#3", "title": "Guest Special", "status": "Pending", "downloads": 0},
    ], title="Recent Episodes")
    
    db.progress("Storage", 75, 100)
    
    output = "/tmp/test_dashboard.html"
    db.save(output)
    
    print(f"\n✅ Dashboard created: {output}")
    print("Open in browser to view!")
