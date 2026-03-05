#!/usr/bin/env python3
"""
📊 BAARLICLAW CHART TOOLKIT
Avanserte grafer og visualiseringer
"""

import os
import sys
import math
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("ChartToolkit")

@dataclass
class DataPoint:
    """Single data point"""
    x: Any
    y: float
    label: Optional[str] = None

class SVGChart:
    """Generate SVG charts"""
    
    def __init__(self, width: int = 800, height: int = 400):
        self.width = width
        self.height = height
        self.margin = {'top': 40, 'right': 40, 'bottom': 60, 'left': 60}
    
    def _get_chart_area(self) -> Tuple[int, int, int, int]:
        """Get chart drawing area"""
        x = self.margin['left']
        y = self.margin['top']
        w = self.width - self.margin['left'] - self.margin['right']
        h = self.height - self.margin['top'] - self.margin['bottom']
        return x, y, w, h
    
    def line_chart(self, data: List[DataPoint], 
                   title: str = "",
                   color: str = "#3b82f6") -> str:
        """Generate line chart"""
        if not data:
            return ""
        
        cx, cy, cw, ch = self._get_chart_area()
        
        # Calculate scales
        x_values = [d.x for d in data]
        y_values = [d.y for d in data]
        
        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)
        
        y_range = y_max - y_min if y_max != y_min else 1
        
        # Generate points
        points = []
        for d in data:
            px = cx + ((d.x - x_min) / (x_max - x_min)) * cw if x_max != x_min else cx + cw/2
            py = cy + ch - ((d.y - y_min) / y_range) * ch
            points.append(f"{px},{py}")
        
        points_str = " ".join(points)
        
        # Build SVG
        svg = f'''<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="lineGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:{color};stop-opacity:0.3" />
                    <stop offset="100%" style="stop-color:{color};stop-opacity:0" />
                </linearGradient>
            </defs>
            
            {f'<text x="{self.width/2}" y="25" text-anchor="middle" font-size="18" font-weight="bold">{title}</text>' if title else ''}
            
            <rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="#f8f9fa" stroke="#e9ecef" />
            
            <polyline points="{points_str}" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
            
            {''.join(f'<circle cx="{p.split(",")[0]}" cy="{p.split(",")[1]}" r="5" fill="{color}" stroke="white" stroke-width="2" />' for p in points)}
            
            <text x="{cx}" y="{cy + ch + 20}" font-size="12" fill="#666">{self._format_value(x_min)}</text>
            <text x="{cx + cw}" y="{cy + ch + 20}" font-size="12" fill="#666" text-anchor="end">{self._format_value(x_max)}</text>
            
            <text x="{cx - 10}" y="{cy + ch}" font-size="12" fill="#666" text-anchor="end">{self._format_value(y_min)}</text>
            <text x="{cx - 10}" y="{cy + 10}" font-size="12" fill="#666" text-anchor="end">{self._format_value(y_max)}</text>
        </svg>'''
        
        return svg
    
    def bar_chart(self, data: List[DataPoint], 
                  title: str = "",
                  color: str = "#3b82f6") -> str:
        """Generate bar chart"""
        if not data:
            return ""
        
        cx, cy, cw, ch = self._get_chart_area()
        
        y_max = max(d.y for d in data)
        bar_width = cw / len(data) * 0.8
        bar_spacing = cw / len(data) * 0.2
        
        bars = []
        for i, d in enumerate(data):
            bar_height = (d.y / y_max) * ch if y_max > 0 else 0
            x = cx + i * (bar_width + bar_spacing) + bar_spacing / 2
            y = cy + ch - bar_height
            
            bars.append(f'''
                <rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" 
                        fill="{color}" rx="4" />
                <text x="{x + bar_width/2}" y="{cy + ch + 15}" 
                      font-size="11" fill="#666" text-anchor="middle">{d.label or str(d.x)}</text>
            ''')
        
        svg = f'''<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">
            {f'<text x="{self.width/2}" y="25" text-anchor="middle" font-size="18" font-weight="bold">{title}</text>' if title else ''}
            
            <rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="#f8f9fa" stroke="#e9ecef" />
            
            {''.join(bars)}
        </svg>'''
        
        return svg
    
    def pie_chart(self, data: List[DataPoint], 
                  title: str = "",
                  colors: Optional[List[str]] = None) -> str:
        """Generate pie chart"""
        if not data:
            return ""
        
        colors = colors or ["#3b82f6", "#ef4444", "#22c55e", "#f59e0b", "#8b5cf6", "#ec4899"]
        
        total = sum(d.y for d in data)
        if total == 0:
            return ""
        
        cx, cy = self.width / 2, self.height / 2
        radius = min(self.width, self.height) / 2 - 60
        
        slices = []
        legend = []
        start_angle = 0
        
        for i, d in enumerate(data):
            angle = (d.y / total) * 360
            end_angle = start_angle + angle
            
            # Calculate path
            x1 = cx + radius * math.cos(math.radians(start_angle))
            y1 = cy + radius * math.sin(math.radians(start_angle))
            x2 = cx + radius * math.cos(math.radians(end_angle))
            y2 = cy + radius * math.sin(math.radians(end_angle))
            
            large_arc = 1 if angle > 180 else 0
            
            path = f"M {cx} {cy} L {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2} Z"
            
            color = colors[i % len(colors)]
            slices.append(f'<path d="{path}" fill="{color}" stroke="white" stroke-width="2" />')
            
            # Legend
            legend_y = 60 + i * 25
            legend.append(f'''
                <rect x="{self.width - 150}" y="{legend_y}" width="15" height="15" fill="{color}" />
                <text x="{self.width - 130}" y="{legend_y + 12}" font-size="12" fill="#333">{d.label or str(d.x)} ({d.y})</text>
            ''')
            
            start_angle = end_angle
        
        svg = f'''<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">
            {f'<text x="{self.width/2}" y="25" text-anchor="middle" font-size="18" font-weight="bold">{title}</text>' if title else ''}
            
            {''.join(slices)}
            {''.join(legend)}
        </svg>'''
        
        return svg
    
    def _format_value(self, value: float) -> str:
        """Format value for display"""
        if value >= 1000000:
            return f"{value/1000000:.1f}M"
        elif value >= 1000:
            return f"{value/1000:.1f}K"
        elif value == int(value):
            return str(int(value))
        return f"{value:.2f}"

class ASCIIChart:
    """Generate ASCII charts for terminal"""
    
    @staticmethod
    def bar(data: List[float], labels: Optional[List[str]] = None,
            width: int = 40, height: int = 10) -> str:
        """Generate ASCII bar chart"""
        if not data:
            return "No data"
        
        max_val = max(data)
        if max_val == 0:
            max_val = 1
        
        lines = []
        
        for i, value in enumerate(data):
            bar_len = int((value / max_val) * width)
            bar = '█' * bar_len
            label = labels[i] if labels and i < len(labels) else str(i)
            lines.append(f"{label:10} │{bar} {value}")
        
        return '\n'.join(lines)
    
    @staticmethod
    def sparkline(data: List[float]) -> str:
        """Generate sparkline"""
        if not data:
            return ""
        
        blocks = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
        
        min_val = min(data)
        max_val = max(data)
        val_range = max_val - min_val if max_val != min_val else 1
        
        result = ""
        for value in data:
            idx = int(((value - min_val) / val_range) * (len(blocks) - 1))
            result += blocks[idx]
        
        return result

# === CONVENIENCE FUNCTIONS ===
def quick_line_chart(data: List[Tuple[Any, float]], title: str = "") -> str:
    """Quick line chart"""
    points = [DataPoint(x=x, y=y) for x, y in data]
    chart = SVGChart()
    return chart.line_chart(points, title)

def quick_bar_chart(data: List[Tuple[str, float]], title: str = "") -> str:
    """Quick bar chart"""
    points = [DataPoint(x=i, y=y, label=label) for i, (label, y) in enumerate(data)]
    chart = SVGChart()
    return chart.bar_chart(points, title)

def quick_sparkline(data: List[float]) -> str:
    """Quick sparkline"""
    return ASCIIChart.sparkline(data)

# === TESTING ===
if __name__ == "__main__":
    print("📊 BaarliClaw Chart Toolkit - Testing")
    print("=" * 50)
    
    # Test SVG charts
    print("\n🧪 Testing SVG Charts")
    chart = SVGChart(width=600, height=300)
    
    # Line chart
    line_data = [
        DataPoint(x=i, y=val) 
        for i, val in enumerate([10, 25, 15, 40, 30, 55, 45])
    ]
    svg = chart.line_chart(line_data, "Weekly Sales", "#3b82f6")
    print(f"✅ Line chart: {len(svg)} chars")
    
    # Bar chart
    bar_data = [
        DataPoint(x=i, y=val, label=label)
        for i, (label, val) in enumerate([
            ("Mon", 20), ("Tue", 35), ("Wed", 25), 
            ("Thu", 45), ("Fri", 40)
        ])
    ]
    svg = chart.bar_chart(bar_data, "Daily Visitors", "#22c55e")
    print(f"✅ Bar chart: {len(svg)} chars")
    
    # Pie chart
    pie_data = [
        DataPoint(x="A", y=30, label="Product A"),
        DataPoint(x="B", y=45, label="Product B"),
        DataPoint(x="C", y=25, label="Product C"),
    ]
    svg = chart.pie_chart(pie_data, "Market Share")
    print(f"✅ Pie chart: {len(svg)} chars")
    
    # Test ASCII charts
    print("\n🧪 Testing ASCII Charts")
    
    ascii_data = [30, 50, 25, 80, 45]
    ascii_labels = ["A", "B", "C", "D", "E"]
    ascii_chart = ASCIIChart.bar(ascii_data, ascii_labels)
    print("✅ ASCII Bar Chart:")
    print(ascii_chart)
    
    sparkline_data = [1, 4, 2, 8, 5, 7, 3, 9, 6, 8]
    spark = ASCIIChart.sparkline(sparkline_data)
    print(f"\n✅ Sparkline: {spark}")
    
    print("\n✅ Chart Toolkit ready!")
