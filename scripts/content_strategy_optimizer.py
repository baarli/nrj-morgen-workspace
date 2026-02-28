#!/usr/bin/env python3
"""
🎯 Content Strategy Optimizer - Optimize content for maximum engagement
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter

class ContentStrategyOptimizer:
    """Optimize NRJ Morgen content strategy"""
    
    def __init__(self):
        self.topics_file = Path('/root/.openclaw/workspace/brain/content-topics.json')
        self.performance_data = []
        
    def analyze_topic_performance(self, topics_with_engagement: List[Dict]) -> Dict:
        """Analyze which topics drive most engagement"""
        # Group by topic category
        by_category = {}
        
        for item in topics_with_engagement:
            category = item.get('category', 'unknown')
            engagement = item.get('engagement_score', 0)
            
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(engagement)
        
        # Calculate average engagement per category
        results = {}
        for category, scores in by_category.items():
            avg = sum(scores) / len(scores) if scores else 0
            results[category] = {
                'avg_engagement': round(avg, 2),
                'count': len(scores)
            }
        
        return results
    
    def generate_optimal_schedule(self) -> Dict:
        """Generate optimal content schedule based on listener patterns"""
        # Best times for different content types
        schedule = {
            '06:00-07:00': {
                'type': 'news_briefing',
                'description': 'Morning news roundup - quick hits',
                'duration': '10-15 min'
            },
            '07:00-08:00': {
                'type': 'main_show',
                'description': 'Peak time - main content, interviews, games',
                'duration': '60 min'
            },
            '08:00-09:00': {
                'type': 'deep_dive',
                'description': 'Longer interviews, stories, features',
                'duration': '60 min'
            },
            '09:00-10:00': {
                'type': 'wrap_up',
                'description': 'Recap, trending topics, listener interaction',
                'duration': '60 min'
            }
        }
        
        return schedule
    
    def identify_viral_opportunities(self, trending_topics: List[str]) -> List[Dict]:
        """Identify topics with viral potential"""
        opportunities = []
        
        viral_indicators = [
            'kjendis', 'brudd', 'skandale', 'konflikt', 'drama',
            'reality', 'paradise hotel', 'farmen', 'love island',
            'trending', 'viral', 'tiktoker', 'influencer'
        ]
        
        for topic in trending_topics:
            score = sum(1 for indicator in viral_indicators if indicator in topic.lower())
            if score > 0:
                opportunities.append({
                    'topic': topic,
                    'viral_score': score,
                    'recommendation': 'High priority - cover immediately'
                })
        
        # Sort by viral score
        opportunities.sort(key=lambda x: x['viral_score'], reverse=True)
        return opportunities[:10]
    
    def generate_content_ideas(self) -> List[Dict]:
        """Generate content ideas for upcoming shows"""
        ideas = [
            {
                'category': 'Interactive',
                'title': 'Lytterens Valg',
                'description': 'La lytterne stemme på dagens tema i real-time',
                'engagement_potential': 'High',
                'effort': 'Medium'
            },
            {
                'category': 'Celebrity',
                'title': 'Kjendis Radar',
                'description': 'Dypdykk i ukens kjendisnyheter med eksklusive vinklinger',
                'engagement_potential': 'High',
                'effort': 'Low'
            },
            {
                'category': 'Reality',
                'title': 'Reality Check',
                'description': 'Analyse og diskusjon av aktuelle reality-serier',
                'engagement_potential': 'Very High',
                'effort': 'Low'
            },
            {
                'category': 'Social Media',
                'title': 'TikTok Tirsdag',
                'description': 'Ukens viral TikTok-trend med lytterdeltakelse',
                'engagement_potential': 'High',
                'effort': 'Medium'
            },
            {
                'category': 'Music',
                'title': 'Norsk på Toppen',
                'description': 'Fremheve norske artister og deres suksesshistorier',
                'engagement_potential': 'Medium',
                'effort': 'Medium'
            },
            {
                'category': 'Games',
                'title': 'Morgenquizzen',
                'description': 'Daglig quiz med premier for lyttere',
                'engagement_potential': 'Very High',
                'effort': 'Low'
            }
        ]
        
        return ideas
    
    def create_weekly_plan(self) -> Dict:
        """Create optimized weekly content plan"""
        plan = {
            'mandag': {
                'theme': 'Ny uke, nye muligheter',
                'focus': 'Ukens agenda, trending topics',
                'special_segment': 'Morgenquizzen'
            },
            'tirsdag': {
                'theme': 'TikTok Tirsdag',
                'focus': 'Sosiale medier, viral content',
                'special_segment': 'TikTok Trend Report'
            },
            'onsdag': {
                'theme': 'Reality Check',
                'focus': 'Reality-TV, kjendisdrama',
                'special_segment': 'Reality Radar'
            },
            'torsdag': {
                'theme': 'Throwback Thursday',
                'focus': 'Nostalgi, gamle hits, retro',
                'special_segment': 'Nostalgi-minuttet'
            },
            'fredag': {
                'theme': 'Fredagsfeeling',
                'focus': 'Weekend-vibes, party-mood',
                'special_segment': 'Ukens Vinner'
            }
        }
        
        return plan
    
    def print_strategy(self):
        """Print complete content strategy"""
        print("\n" + "=" * 70)
        print("🎯 NRJ MORGEN CONTENT STRATEGY OPTIMIZER")
        print("=" * 70)
        
        # Optimal schedule
        print("\n📅 OPTIMAL CONTENT SCHEDULE:")
        schedule = self.generate_optimal_schedule()
        for time_slot, info in schedule.items():
            print(f"\n   {time_slot}: {info['type']}")
            print(f"   └─ {info['description']} ({info['duration']})")
        
        # Weekly plan
        print("\n\n📆 WEEKLY CONTENT PLAN:")
        weekly = self.create_weekly_plan()
        for day, info in weekly.items():
            print(f"\n   {day.upper()}: {info['theme']}")
            print(f"   └─ Focus: {info['focus']}")
            print(f"   └─ Special: {info['special_segment']}")
        
        # Content ideas
        print("\n\n💡 HIGH-IMPACT CONTENT IDEAS:")
        ideas = self.generate_content_ideas()
        for idea in ideas:
            potential = idea['engagement_potential']
            icon = '🔥' if potential == 'Very High' else '⭐' if potential == 'High' else '💡'
            print(f"\n   {icon} {idea['title']} ({idea['category']})")
            print(f"   └─ {idea['description']}")
            print(f"   └─ Engagement: {potential} | Effort: {idea['effort']}")
        
        print("\n" + "=" * 70)


if __name__ == '__main__':
    optimizer = ContentStrategyOptimizer()
    optimizer.print_strategy()
