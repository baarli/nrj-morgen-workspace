#!/usr/bin/env python3
"""
AI Research Module for NRJ Morgen Content Pipeline v3
Håndterer AI-drevet research og analyse av nyheter
"""

import os
import json
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger('ai-research')

@dataclass
class ResearchResult:
    """Resultat fra AI research"""
    query: str
    findings: List[Dict]
    analysis: str
    confidence: float
    timestamp: str

class AIResearchEngine:
    """AI-drevet research motor"""
    
    def __init__(self):
        self.brave_api_key = os.getenv('BRAVE_API_KEY', 'BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev')
    
    def search(self, query: str, freshness: str = "pd") -> ResearchResult:
        """Søk etter nyheter"""
        url = "https://api.search.brave.com/res/v1/news/search"
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.brave_api_key
        }
        params = {
            "q": query,
            "freshness": freshness,
            "count": 10
        }
        
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                findings = data.get('results', [])
                
                # Analyser resultater
                analysis = self._analyze_findings(findings)
                confidence = self._calculate_confidence(findings)
                
                return ResearchResult(
                    query=query,
                    findings=findings,
                    analysis=analysis,
                    confidence=confidence,
                    timestamp=datetime.now().isoformat()
                )
            else:
                logger.error(f"API error: {resp.status_code} - {resp.text[:200]}")
                return ResearchResult(query, [], f"Error: {resp.status_code}", 0.0, datetime.now().isoformat())
        except Exception as e:
            logger.error(f"Search error: {e}")
            return ResearchResult(query, [], f"Error: {str(e)}", 0.0, datetime.now().isoformat())
    
    def search_multi(self, queries: List[str], freshness: str = "pd") -> List[ResearchResult]:
        """Søk i flere kilder"""
        results = []
        for query in queries:
            result = self.search(query, freshness)
            results.append(result)
        return results
    
    def _analyze_findings(self, findings: List[Dict]) -> str:
        """Analyser funn og gi oppsummering"""
        if not findings:
            return "Ingen resultater funnet"
        
        # Tell kilder
        sources = {}
        for f in findings:
            domain = f.get('meta', {}).get('domain', 'unknown')
            sources[domain] = sources.get(domain, 0) + 1
        
        # Sjekk aktualitet
        ages = []
        for f in findings:
            age = f.get('age', '')
            if age and ('time' in str(age) or 'minutter' in str(age) or 'timer' in str(age)):
                ages.append('recent')
            elif age and ('dag' in str(age) or 'dager' in str(age)):
                ages.append('day')
            else:
                ages.append('older')
        
        analysis_parts = [
            f"Fant {len(findings)} resultater",
            f"Kilder: {', '.join(sources.keys())}",
            f"Aktualitet: {ages.count('recent')} nylige, {ages.count('day')} dag gamle"
        ]
        
        return " | ".join(analysis_parts)
    
    def _calculate_confidence(self, findings: List[Dict]) -> float:
        """Beregn konfidens-score"""
        if not findings:
            return 0.0
        
        score = 0.5
        
        # Flere kilder = høyere konfidens
        sources = set(f.get('meta', {}).get('domain') for f in findings)
        score += min(len(sources) * 0.1, 0.3)
        
        # Nylige resultater = høyere konfidens
        recent_count = sum(1 for f in findings if 'time' in str(f.get('age', '')))
        score += min(recent_count * 0.05, 0.2)
        
        return min(score, 1.0)
    
    def get_trending_topics(self) -> List[Dict]:
        """Hent trending topics"""
        trending_queries = [
            "Farmen",
            "Paradise Hotel",
            "Kjendisnytt"
        ]
        
        results = self.search_multi(trending_queries, freshness="pd")
        
        trending = []
        for result in results:
            for finding in result.findings[:3]:
                trending.append({
                    'title': finding.get('title'),
                    'url': finding.get('url'),
                    'source': finding.get('meta', {}).get('domain'),
                    'confidence': result.confidence
                })
        
        # Sorter etter konfidens
        trending.sort(key=lambda x: x['confidence'], reverse=True)
        return trending[:10]

def main():
    """Test AI Research Module"""
    print("🧠 Testing AI Research Module...")
    
    engine = AIResearchEngine()
    
    # Test multi-source search
    queries = [
        "Farmen",
        "Paradise Hotel",
        "Kjendisnytt"
    ]
    
    results = engine.search_multi(queries)
    
    print(f"\n📊 Found {len(results)} research results:")
    for r in results:
        print(f"\n  Query: {r.query}")
        print(f"  Analysis: {r.analysis}")
        print(f"  Confidence: {r.confidence:.2f}")
        print(f"  Items: {len(r.findings)}")
    
    # Test trending
    print("\n🔥 Trending topics:")
    trending = engine.get_trending_topics()
    for t in trending[:5]:
        print(f"  - {t['title'][:60]}... ({t['source']})")

if __name__ == "__main__":
    main()
