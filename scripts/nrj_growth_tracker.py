#!/usr/bin/env python3
"""
📈 NRJ Growth Tracker - Track and analyze growth metrics
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

class NRJGrowthTracker:
    """Track NRJ Morgen growth metrics over time"""
    
    def __init__(self):
        self.data_dir = Path('/root/.openclaw/workspace/brain/nrj-growth')
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.metrics_file = self.data_dir / 'growth-metrics.json'
        
    def load_historical_data(self) -> List[Dict]:
        """Load historical growth data"""
        if self.metrics_file.exists():
            with open(self.metrics_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_metrics(self, metrics: Dict):
        """Save growth metrics"""
        data = self.load_historical_data()
        data.append(metrics)
        
        # Keep only last 90 days
        cutoff = datetime.now() - timedelta(days=90)
        data = [d for d in data if datetime.fromisoformat(d['date']) > cutoff]
        
        with open(self.metrics_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def track_nielsen(self, listeners: int, week: int):
        """Track Nielsen radio metrics"""
        metrics = {
            'date': datetime.now().isoformat(),
            'source': 'nielsen',
            'listeners': listeners,
            'week': week
        }
        self.save_metrics(metrics)
        
    def track_podtoppen(self, rank: int, listeners: int):
        """Track Podtoppen podcast metrics"""
        metrics = {
            'date': datetime.now().isoformat(),
            'source': 'podtoppen',
            'rank': rank,
            'listeners': listeners
        }
        self.save_metrics(metrics)
    
    def track_social_media(self, platform: str, followers: int, engagement: float):
        """Track social media growth"""
        metrics = {
            'date': datetime.now().isoformat(),
            'source': f'social_{platform}',
            'followers': followers,
            'engagement': engagement
        }
        self.save_metrics(metrics)
    
    def calculate_growth_rate(self, metric_type: str, days: int = 30) -> Optional[float]:
        """Calculate growth rate for a metric"""
        data = self.load_historical_data()
        
        # Filter by metric type
        filtered = [d for d in data if d.get('source') == metric_type]
        
        if len(filtered) < 2:
            return None
        
        # Sort by date
        filtered.sort(key=lambda x: x['date'])
        
        # Get first and last
        first = filtered[0]
        last = filtered[-1]
        
        # Calculate growth
        if metric_type == 'nielsen':
            first_val = first.get('listeners', 0)
            last_val = last.get('listeners', 0)
        elif metric_type == 'podtoppen':
            first_val = first.get('listeners', 0)
            last_val = last.get('listeners', 0)
        else:
            return None
        
        if first_val == 0:
            return 0
        
        return ((last_val - first_val) / first_val) * 100
    
    def generate_report(self) -> Dict:
        """Generate growth report"""
        data = self.load_historical_data()
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_data_points': len(data),
            'nielsen_growth': self.calculate_growth_rate('nielsen', 30),
            'podtoppen_growth': self.calculate_growth_rate('podtoppen', 30),
            'latest_metrics': {}
        }
        
        # Get latest for each source
        sources = set(d.get('source') for d in data)
        for source in sources:
            source_data = [d for d in data if d.get('source') == source]
            if source_data:
                source_data.sort(key=lambda x: x['date'], reverse=True)
                report['latest_metrics'][source] = source_data[0]
        
        return report
    
    def print_report(self):
        """Print growth report"""
        report = self.generate_report()
        
        print("\n" + "=" * 60)
        print("📈 NRJ MORGEN GROWTH TRACKER")
        print("=" * 60)
        
        print(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"Data points: {report['total_data_points']}")
        
        # Nielsen
        nielsen_growth = report.get('nielsen_growth')
        if nielsen_growth is not None:
            trend = "📈" if nielsen_growth > 0 else "📉" if nielsen_growth < 0 else "➡️"
            print(f"\n{trend} Nielsen (30d): {nielsen_growth:+.1f}%")
        
        # Podtoppen
        podtoppen_growth = report.get('podtoppen_growth')
        if podtoppen_growth is not None:
            trend = "📈" if podtoppen_growth > 0 else "📉" if podtoppen_growth < 0 else "➡️"
            print(f"{trend} Podtoppen (30d): {podtoppen_growth:+.1f}%")
        
        # Latest metrics
        print("\n📊 Latest Metrics:")
        for source, metrics in report['latest_metrics'].items():
            if source == 'nielsen':
                print(f"   Nielsen: {metrics.get('listeners', 'N/A'):,} listeners (Week {metrics.get('week', 'N/A')})")
            elif source == 'podtoppen':
                print(f"   Podtoppen: #{metrics.get('rank', 'N/A')} ({metrics.get('listeners', 'N/A'):,} listeners)")
        
        print("=" * 60)


if __name__ == '__main__':
    tracker = NRJGrowthTracker()
    tracker.print_report()
