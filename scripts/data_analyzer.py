#!/usr/bin/env python3
"""
📊 BAARLICLAW DATA ANALYZER
Dataanalyse, trend-deteksjon og visualisering
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from collections import Counter
import statistics

# Legg til toolkit i path
sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("DataAnalyzer")

class TrendAnalyzer:
    """Analyze trends in data over time"""
    
    def __init__(self):
        self.data_points = []
        
    def add_point(self, value: float, timestamp: Optional[datetime] = None):
        """Add a data point"""
        if timestamp is None:
            timestamp = datetime.now()
        self.data_points.append({'value': value, 'timestamp': timestamp})
    
    def load_from_list(self, data: List[Dict]):
        """Load data from list of dicts with 'value' and 'timestamp'"""
        self.data_points = sorted(data, key=lambda x: x['timestamp'])
    
    def calculate_moving_average(self, window: int = 7) -> List[float]:
        """Calculate moving average"""
        if len(self.data_points) < window:
            return [p['value'] for p in self.data_points]
        
        values = [p['value'] for p in self.data_points]
        moving_avgs = []
        
        for i in range(len(values)):
            if i < window - 1:
                moving_avgs.append(sum(values[:i+1]) / (i+1))
            else:
                moving_avgs.append(sum(values[i-window+1:i+1]) / window)
        
        return moving_avgs
    
    def detect_trend(self) -> Dict[str, Any]:
        """
        Detect overall trend in data
        
        Returns:
            {
                'direction': 'up' | 'down' | 'stable',
                'strength': float (0-1),
                'change_percent': float,
                'avg_change': float
            }
        """
        if len(self.data_points) < 2:
            return {'direction': 'stable', 'strength': 0, 'change_percent': 0}
        
        values = [p['value'] for p in self.data_points]
        first_value = values[0]
        last_value = values[-1]
        
        # Calculate overall change
        change = last_value - first_value
        change_percent = (change / first_value * 100) if first_value != 0 else 0
        
        # Calculate trend strength using linear regression
        n = len(values)
        x_values = list(range(n))
        
        x_mean = sum(x_values) / n
        y_mean = sum(values) / n
        
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, values))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
        
        # Determine direction and strength
        if abs(slope) < 0.01:
            direction = 'stable'
            strength = 0
        elif slope > 0:
            direction = 'up'
            strength = min(abs(slope) / (y_mean * 0.1), 1.0) if y_mean != 0 else 0.5
        else:
            direction = 'down'
            strength = min(abs(slope) / (y_mean * 0.1), 1.0) if y_mean != 0 else 0.5
        
        return {
            'direction': direction,
            'strength': round(strength, 2),
            'change_percent': round(change_percent, 2),
            'avg_change': round(change / (n - 1), 2) if n > 1 else 0,
            'slope': round(slope, 4)
        }
    
    def find_anomalies(self, threshold: float = 2.0) -> List[Dict]:
        """
        Find anomalous data points using standard deviation
        
        Args:
            threshold: Number of standard deviations from mean
        """
        if len(self.data_points) < 3:
            return []
        
        values = [p['value'] for p in self.data_points]
        mean = statistics.mean(values)
        std_dev = statistics.stdev(values)
        
        anomalies = []
        for point in self.data_points:
            z_score = abs(point['value'] - mean) / std_dev if std_dev > 0 else 0
            if z_score > threshold:
                anomalies.append({
                    **point,
                    'z_score': round(z_score, 2),
                    'deviation': round(point['value'] - mean, 2)
                })
        
        return anomalies
    
    def predict_next(self, method: str = 'linear') -> Optional[float]:
        """
        Predict next value
        
        Methods: linear, average
        """
        if len(self.data_points) < 2:
            return None
        
        values = [p['value'] for p in self.data_points]
        
        if method == 'average':
            return statistics.mean(values[-5:])  # Last 5 average
        
        elif method == 'linear':
            # Simple linear extrapolation
            n = len(values)
            x_values = list(range(n))
            
            x_mean = sum(x_values) / n
            y_mean = sum(values) / n
            
            numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, values))
            denominator = sum((x - x_mean) ** 2 for x in x_values)
            
            if denominator == 0:
                return y_mean
            
            slope = numerator / denominator
            intercept = y_mean - slope * x_mean
            
            # Predict next value (x = n)
            return slope * n + intercept
        
        return None
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics"""
        if not self.data_points:
            return {}
        
        values = [p['value'] for p in self.data_points]
        
        return {
            'count': len(values),
            'min': min(values),
            'max': max(values),
            'mean': round(statistics.mean(values), 2),
            'median': round(statistics.median(values), 2),
            'stdev': round(statistics.stdev(values), 2) if len(values) > 1 else 0,
            'trend': self.detect_trend()
        }

class TextAnalyzer:
    """Analyze text data"""
    
    def __init__(self):
        self.stop_words = {'og', 'i', 'jeg', 'det', 'at', 'en', 'den', 'til', 
                          'er', 'som', 'på', 'de', 'med', 'han', 'av', 'ikke', 
                          'der', 'så', 'var', 'meg', 'seg', 'men', 'ett', 'har', 
                          'om', 'vi', 'min', 'ha', 'hadde', 'hun', 'nå', 'over', 
                          'da', 'ved', 'fra', 'du', 'ut', 'sin', 'dem', 'oss', 
                          'opp', 'man', 'kan', 'hans', 'hvor', 'eller', 'hva', 
                          'skal', 'selv', 'sjøl', 'bare', 'noe', 'noen', 'deres', 
                          'vil', 'dere', 'kunne', 'bli', 'ble', 'blitt', 'the', 
                          'and', 'for', 'are', 'this', 'that', 'with', 'have'}
    
    def extract_keywords(self, texts: List[str], top_n: int = 10) -> List[Tuple[str, int]]:
        """Extract most common keywords from texts"""
        all_words = []
        
        for text in texts:
            # Simple tokenization
            words = text.lower().split()
            # Remove punctuation and filter
            words = [''.join(c for c in w if c.isalnum()) for w in words]
            words = [w for w in words if len(w) > 2 and w not in self.stop_words]
            all_words.extend(words)
        
        return Counter(all_words).most_common(top_n)
    
    def analyze_sentiment_simple(self, text: str) -> Dict[str, float]:
        """
        Simple sentiment analysis (Norwegian + English)
        
        Returns: {'positive': float, 'negative': float, 'neutral': float}
        """
        positive_words = {'bra', 'god', 'flott', 'fantastisk', 'glad', 'positiv', 
                         'suksess', 'vakkert', 'elsker', 'best', 'good', 'great', 
                         'excellent', 'happy', 'love', 'best', 'amazing'}
        
        negative_words = {'dårlig', 'vondt', 'trist', 'negativ', 'problem', 'feil', 
                         'katastrofe', 'hater', 'verst', 'bad', 'terrible', 'sad', 
                         'hate', 'worst', 'awful', 'problem'}
        
        words = text.lower().split()
        words = [''.join(c for c in w if c.isalnum()) for w in words]
        
        pos_count = sum(1 for w in words if w in positive_words)
        neg_count = sum(1 for w in words if w in negative_words)
        total = len(words)
        
        if total == 0:
            return {'positive': 0, 'negative': 0, 'neutral': 1}
        
        return {
            'positive': round(pos_count / total, 2),
            'negative': round(neg_count / total, 2),
            'neutral': round((total - pos_count - neg_count) / total, 2)
        }
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities (simple version)
        
        Returns: {'persons': [], 'organizations': [], 'locations': []}
        """
        # Simple capitalized word detection
        words = text.split()
        entities = []
        current_entity = []
        
        for word in words:
            clean = ''.join(c for c in word if c.isalnum())
            if clean and clean[0].isupper() and len(clean) > 1:
                current_entity.append(clean)
            else:
                if current_entity:
                    entities.append(' '.join(current_entity))
                    current_entity = []
        
        if current_entity:
            entities.append(' '.join(current_entity))
        
        # Simple classification (very basic)
        persons = []
        orgs = []
        locations = []
        
        for entity in entities:
            # Heuristics
            if any(x in entity.lower() for x in ['as', 'asa', 'ltd', 'inc', 'corp']):
                orgs.append(entity)
            elif any(x in entity.lower() for x in ['norge', 'oslo', 'bergen', 'norway']):
                locations.append(entity)
            else:
                persons.append(entity)
        
        return {
            'persons': list(set(persons)),
            'organizations': list(set(orgs)),
            'locations': list(set(locations))
        }

class DataVisualizer:
    """Create visualizations from data"""
    
    def __init__(self):
        self.output_dir = "/tmp/visualizations"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_ascii_chart(self, values: List[float], width: int = 50, 
                          height: int = 10, title: str = "") -> str:
        """Create ASCII art chart"""
        if not values:
            return "No data"
        
        min_val = min(values)
        max_val = max(values)
        val_range = max_val - min_val if max_val != min_val else 1
        
        lines = []
        if title:
            lines.append(f"📊 {title}")
            lines.append("=" * width)
        
        for row in range(height, 0, -1):
            threshold = min_val + (val_range * (row - 1) / height)
            line = ""
            for val in values[:width]:
                if val >= threshold:
                    line += "█"
                else:
                    line += " "
            lines.append(line)
        
        lines.append("-" * min(width, len(values)))
        lines.append(f"Min: {min_val:.1f} | Max: {max_val:.1f} | Avg: {sum(values)/len(values):.1f}")
        
        return "\n".join(lines)
    
    def create_summary_table(self, data: Dict[str, Any]) -> str:
        """Create formatted text table"""
        lines = []
        lines.append("┌" + "─" * 38 + "┐")
        lines.append("│" + " SUMMARY ".center(36) + "│")
        lines.append("├" + "─" * 38 + "┤")
        
        for key, value in data.items():
            if isinstance(value, float):
                value_str = f"{value:.2f}"
            else:
                value_str = str(value)
            
            key_str = key.replace('_', ' ').title()[:15]
            lines.append(f"│ {key_str:15} │ {value_str:18} │")
        
        lines.append("└" + "─" * 38 + "┘")
        
        return "\n".join(lines)

# === CONVENIENCE FUNCTIONS ===
def analyze_numbers(values: List[float]) -> Dict[str, Any]:
    """Quick analysis of number list"""
    analyzer = TrendAnalyzer()
    for v in values:
        analyzer.add_point(v)
    return analyzer.get_summary()

def find_trend(values: List[float]) -> str:
    """Quick trend detection"""
    analyzer = TrendAnalyzer()
    for v in values:
        analyzer.add_point(v)
    trend = analyzer.detect_trend()
    
    arrows = {'up': '📈', 'down': '📉', 'stable': '➡️'}
    return f"{arrows.get(trend['direction'], '➡️')} {trend['direction'].upper()} ({trend['change_percent']:.1f}%)"

def quick_chart(values: List[float], title: str = "") -> str:
    """Quick ASCII chart"""
    viz = DataVisualizer()
    return viz.create_ascii_chart(values, title=title)

# === TESTING ===
if __name__ == "__main__":
    print("📊 BaarliClaw Data Analyzer - Testing")
    print("=" * 50)
    
    # Test trend analysis
    print("\n📈 Trend Analysis Test:")
    trend = TrendAnalyzer()
    
    # Simulate daily downloads
    downloads = [100, 105, 110, 108, 115, 120, 125, 130, 128, 135]
    for d in downloads:
        trend.add_point(d)
    
    summary = trend.get_summary()
    print(f"  Count: {summary['count']}")
    print(f"  Mean: {summary['mean']}")
    print(f"  Trend: {summary['trend']}")
    
    # Test text analysis
    print("\n📝 Text Analysis Test:")
    text_analyzer = TextAnalyzer()
    
    texts = [
        "Farmen Kjendis er en populær realityserie på TV2",
        "Paradise Hotel har mange seere",
        "Kjendisene i Farmen er veldig underholdende"
    ]
    
    keywords = text_analyzer.extract_keywords(texts, 5)
    print(f"  Top keywords: {keywords}")
    
    # Test visualization
    print("\n📊 Visualization Test:")
    viz = DataVisualizer()
    chart = viz.create_ascii_chart(downloads, title="Downloads")
    print(chart)
    
    print("\n✅ Data Analyzer ready!")
