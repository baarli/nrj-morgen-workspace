#!/usr/bin/env python3
"""
NRJ Morgen Content Pipeline v3 - Full Integration
Kombinerer research, approval og publisering til Supabase
"""

import os
import sys
import json
import time
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/content-pipeline-v3.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('content-pipeline')

# Load credentials
def load_credentials():
    """Load credentials from env file"""
    creds = {}
    try:
        with open('/root/.openclaw/workspace/.credentials/nrj-morgen.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, val = line.strip().split('=', 1)
                    creds[key] = val
    except Exception as e:
        logger.error(f"Could not load credentials: {e}")
    return creds

CREDS = load_credentials()

@dataclass
class ContentItem:
    """Representerer et innholdselement"""
    id: str
    title: str
    summary: str
    source_url: str
    source_name: str
    category: str
    image_url: Optional[str] = None
    status: str = "draft"
    created_at: str = ""
    published_at: Optional[str] = None
    engagement_score: float = 0.0
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

class AIResearchModule:
    """AI-drevet research modul for nyheter"""
    
    def __init__(self):
        self.brave_api_key = CREDS.get('BRAVE_API_KEY', 'BSAt0WSIpXP0Hp6sPvNwaaGuLoyewev')
        self.categories = {
            'reality_tv': ['Farmen', 'Paradise Hotel', 'Kompani Lauritzen', 'Love Island'],
            'celebrity_drama': ['brudd', 'raser', 'avsløringer', 'skandale'],
            'film_tv': ['premiere', 'rød løper', 'Netflix', 'HBO'],
            'music': ['Spellemannprisen', 'VG-lista', 'P3 Gull', 'artist'],
            'international': ['Daily Mail', 'TMZ', 'E! Online', 'People']
        }
    
    def search_news(self, query: str, freshness: str = "pd") -> List[Dict]:
        """Søk etter nyheter via Brave API"""
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
                return data.get('results', [])
            else:
                logger.error(f"Brave API error: {resp.status_code}")
                return []
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    def research_all_categories(self) -> List[ContentItem]:
        """Research alle kategorier og returner funn"""
        all_items = []
        
        for category, keywords in self.categories.items():
            logger.info(f"Researching category: {category}")
            
            for keyword in keywords[:2]:  # Max 2 keywords per category
                try:
                    results = self.search_news(keyword)
                    
                    for result in results[:3]:  # Max 3 results per keyword
                        item = ContentItem(
                            id=f"{category}_{int(time.time())}_{len(all_items)}",
                            title=result.get('title', ''),
                            summary=result.get('description', '')[:200] + '...' if result.get('description') else '',
                            source_url=result.get('url', ''),
                            source_name=result.get('meta', {}).get('domain', 'Unknown'),
                            category=category,
                            image_url=result.get('meta', {}).get('image', {}).get('url') if result.get('meta', {}).get('image') else None
                        )
                        all_items.append(item)
                    
                    time.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    logger.error(f"Error researching {keyword}: {e}")
        
        return all_items

class ContentApprovalWorkflow:
    """Content approval workflow system"""
    
    def __init__(self):
        self.approval_queue = []
        self.approved_content = []
        self.rejected_content = []
    
    def submit_for_approval(self, item: ContentItem) -> bool:
        """Send innhold til godkjenning"""
        item.status = "pending_approval"
        self.approval_queue.append(item)
        logger.info(f"Submitted for approval: {item.title}")
        return True
    
    def auto_approve(self, item: ContentItem) -> bool:
        """Auto-godkjenn basert på regler"""
        rules = [
            len(item.title) > 10 and len(item.title) < 100,
            len(item.summary) > 50,
            item.source_url.startswith('http'),
            item.engagement_score > 0.3
        ]
        
        if all(rules):
            item.status = "approved"
            self.approved_content.append(item)
            logger.info(f"Auto-approved: {item.title}")
            return True
        
        return False
    
    def reject(self, item: ContentItem, reason: str):
        """Avvis innhold"""
        item.status = "rejected"
        self.rejected_content.append({
            'item': asdict(item),
            'reason': reason,
            'rejected_at': datetime.now().isoformat()
        })
        logger.info(f"Rejected: {item.title} - {reason}")

class SupabasePublisher:
    """Publiserer innhold til Supabase"""
    
    def __init__(self):
        self.supabase_url = CREDS.get('SUPABASE_URL', 'https://kvniauxokdtmpvjtfnej.supabase.co')
        self.supabase_key = CREDS.get('SUPABASE_SERVICE_KEY', '')
        self.tenant_id = CREDS.get('TENANT_ID', 'a0000000-0000-0000-0000-000000000001')
        self.user_id = '10aa1508-6d52-490c-8ae5-fa3da9a152c4'
    
    def _get_headers(self) -> Dict:
        return {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
    
    def publish_content(self, content_item: ContentItem) -> bool:
        """Publiser et innholdselement til Supabase"""
        url = f"{self.supabase_url}/rest/v1/agenda_items"
        
        data = {
            'tenant_id': self.tenant_id,
            'title': content_item.title,
            'description': content_item.summary,
            'link_url': content_item.source_url,
            'link_metadata': json.dumps({
                'image_url': content_item.image_url,
                'source_name': content_item.source_name,
                'category': content_item.category,
                'engagement_score': content_item.engagement_score
            }),
            'notes': f"Kilde: {content_item.source_name}\nKategori: {content_item.category}",
            'created_by': self.user_id,
            'is_pinned': False,
            'scheduled_time': datetime.now().strftime('%H:%M:%S')
        }
        
        try:
            resp = requests.post(url, headers=self._get_headers(), json=data, timeout=10)
            if resp.status_code in [200, 201]:
                logger.info(f"Published: {content_item.title[:50]}...")
                return True
            else:
                logger.error(f"Publish error: {resp.status_code} - {resp.text[:200]}")
                return False
        except Exception as e:
            logger.error(f"Publish exception: {e}")
            return False
    
    def publish_batch(self, content_items: List[ContentItem]) -> Dict:
        """Publiser flere innholdselementer"""
        results = {
            'success': 0,
            'failed': 0,
            'items': []
        }
        
        for item in content_items:
            if self.publish_content(item):
                results['success'] += 1
                results['items'].append({'title': item.title, 'status': 'published'})
            else:
                results['failed'] += 1
                results['items'].append({'title': item.title, 'status': 'failed'})
        
        return results

class ContentPipeline:
    """Hoved pipeline klasse"""
    
    def __init__(self):
        self.research_module = AIResearchModule()
        self.approval_workflow = ContentApprovalWorkflow()
        self.publisher = SupabasePublisher()
        self.content_items = []
    
    def run_pipeline(self, publish: bool = False):
        """Kjør hele pipelinen"""
        logger.info("🚀 Starting Content Pipeline v3")
        
        # 1. Research
        logger.info("📚 Phase 1: Researching news...")
        items = self.research_module.research_all_categories()
        logger.info(f"Found {len(items)} potential items")
        
        # 2. Score and filter
        logger.info("📊 Phase 2: Scoring items...")
        for item in items:
            item.engagement_score = self._calculate_engagement_score(item)
        
        items.sort(key=lambda x: x.engagement_score, reverse=True)
        
        # 3. Approval workflow
        logger.info("✅ Phase 3: Approval workflow...")
        for item in items[:15]:  # Top 15 items
            if not self.approval_workflow.auto_approve(item):
                self.approval_workflow.submit_for_approval(item)
        
        # 4. Publish to Supabase (optional)
        if publish:
            logger.info("🌐 Phase 4: Publishing to Supabase...")
            publish_results = self.publisher.publish_batch(
                self.approval_workflow.approved_content[:5]  # Max 5 items
            )
        else:
            publish_results = {'success': 0, 'failed': 0}
        
        # 5. Save results
        logger.info("💾 Phase 5: Saving results...")
        self._save_results()
        
        logger.info("✅ Pipeline complete!")
        return {
            'total_found': len(items),
            'approved': len(self.approval_workflow.approved_content),
            'pending': len(self.approval_workflow.approval_queue),
            'published': publish_results['success'],
            'publish_failed': publish_results['failed']
        }
    
    def _calculate_engagement_score(self, item: ContentItem) -> float:
        """Beregn engagement score for et item"""
        score = 0.5
        
        if len(item.title) > 20 and len(item.title) < 80:
            score += 0.1
        
        if item.image_url:
            score += 0.15
        
        quality_sources = ['vg.no', 'dagbladet.no', 'tv2.no', 'nrk.no', 'nettavisen.no']
        if any(source in item.source_url.lower() for source in quality_sources):
            score += 0.15
        
        category_scores = {
            'reality_tv': 0.1,
            'celebrity_drama': 0.1,
            'film_tv': 0.05,
            'music': 0.05,
            'international': 0.05
        }
        score += category_scores.get(item.category, 0)
        
        return min(score, 1.0)
    
    def _save_results(self):
        """Lagre resultater til fil"""
        output = {
            'timestamp': datetime.now().isoformat(),
            'approved': [asdict(item) for item in self.approval_workflow.approved_content],
            'pending': [asdict(item) for item in self.approval_workflow.approval_queue],
            'rejected': self.approval_workflow.rejected_content
        }
        
        output_file = f"/tmp/content-pipeline-results-{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        logger.info(f"Results saved to: {output_file}")

def main():
    """Hovedfunksjon"""
    import argparse
    parser = argparse.ArgumentParser(description='NRJ Morgen Content Pipeline v3')
    parser.add_argument('--publish', action='store_true', help='Publish to Supabase')
    args = parser.parse_args()
    
    pipeline = ContentPipeline()
    results = pipeline.run_pipeline(publish=args.publish)
    
    print("\n" + "="*50)
    print("CONTENT PIPELINE v3 RESULTS")
    print("="*50)
    print(f"Total items found: {results['total_found']}")
    print(f"Auto-approved: {results['approved']}")
    print(f"Pending approval: {results['pending']}")
    if args.publish:
        print(f"Published: {results['published']}")
        print(f"Publish failed: {results['publish_failed']}")
    print("="*50)

if __name__ == "__main__":
    main()
