#!/usr/bin/env python3
"""
Supabase Integration Module for Content Pipeline v3
Håndterer publisering til Supabase database
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

logger = logging.getLogger('supabase-integration')

class SupabasePublisher:
    """Publiserer innhold til Supabase"""
    
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL', 'https://kvniauxokdtmpvjtfnej.supabase.co')
        self.supabase_key = os.getenv('SUPABASE_SERVICE_KEY', '')
        self.tenant_id = os.getenv('TENANT_ID', 'a0000000-0000-0000-0000-000000000001')
        self.user_id = '10aa1508-6d52-490c-8ae5-fa3da9a152c4'  # BaarliClaw
        
        if not self.supabase_key:
            # Load from credentials file
            try:
                with open('/root/.openclaw/workspace/.credentials/nrj-morgen.env', 'r') as f:
                    for line in f:
                        if line.startswith('SUPABASE_SERVICE_KEY='):
                            self.supabase_key = line.split('=', 1)[1].strip()
                        elif line.startswith('SUPABASE_URL='):
                            self.supabase_url = line.split('=', 1)[1].strip()
                        elif line.startswith('TENANT_ID='):
                            self.tenant_id = line.split('=', 1)[1].strip()
            except Exception as e:
                logger.error(f"Could not load credentials: {e}")
    
    def _get_headers(self) -> Dict:
        """Get Supabase API headers"""
        return {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
    
    def publish_content(self, content_item: Dict) -> bool:
        """Publiser et innholdselement til Supabase"""
        url = f"{self.supabase_url}/rest/v1/agenda_items"
        
        # Prepare data
        data = {
            'tenant_id': self.tenant_id,
            'title': content_item.get('title', ''),
            'description': content_item.get('summary', ''),
            'link_url': content_item.get('source_url', ''),
            'link_metadata': json.dumps({
                'image_url': content_item.get('image_url'),
                'source_name': content_item.get('source_name'),
                'category': content_item.get('category'),
                'engagement_score': content_item.get('engagement_score', 0)
            }),
            'notes': f"Kilde: {content_item.get('source_name', 'Unknown')}\nKategori: {content_item.get('category', '')}",
            'created_by': self.user_id,
            'status': 'active',
            'is_pinned': False,
            'scheduled_time': (datetime.now() + timedelta(days=1)).isoformat()
        }
        
        try:
            resp = requests.post(url, headers=self._get_headers(), json=data, timeout=10)
            if resp.status_code in [200, 201]:
                logger.info(f"Published: {content_item.get('title', '')[:50]}...")
                return True
            else:
                logger.error(f"Publish error: {resp.status_code} - {resp.text[:200]}")
                return False
        except Exception as e:
            logger.error(f"Publish exception: {e}")
            return False
    
    def publish_batch(self, content_items: List[Dict]) -> Dict:
        """Publiser flere innholdselementer"""
        results = {
            'success': 0,
            'failed': 0,
            'items': []
        }
        
        for item in content_items:
            if self.publish_content(item):
                results['success'] += 1
                results['items'].append({'title': item.get('title'), 'status': 'published'})
            else:
                results['failed'] += 1
                results['items'].append({'title': item.get('title'), 'status': 'failed'})
        
        return results
    
    def get_existing_items(self, date: str = None) -> List[Dict]:
        """Hent eksisterende items for en dato"""
        url = f"{self.supabase_url}/rest/v1/agenda_items"
        headers = self._get_headers()
        params = {
            'tenant_id': f'eq.{self.tenant_id}',
            'select': '*',
            'limit': 10
        }
        
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            print(f"Debug - Status: {resp.status_code}")
            if resp.status_code == 200:
                return resp.json()
            else:
                print(f"Debug - Error: {resp.text[:500]}")
                logger.error(f"Fetch error: {resp.status_code}")
                return []
        except Exception as e:
            logger.error(f"Fetch exception: {e}")
            return []

def main():
    """Test Supabase integration"""
    print("🔗 Testing Supabase Integration...")
    
    publisher = SupabasePublisher()
    
    # Test get existing items
    print("\n📋 Checking existing items for tomorrow...")
    existing = publisher.get_existing_items()
    print(f"Found {len(existing)} existing items")
    
    # Test publish (commented out for safety)
    # test_item = {
    #     'title': 'Test Item from Pipeline v3',
    #     'summary': 'This is a test item from the new content pipeline',
    #     'source_url': 'https://example.com/test',
    #     'source_name': 'Test Source',
    #     'category': 'test',
    #     'engagement_score': 0.8
    # }
    # 
    # print("\n📝 Publishing test item...")
    # success = publisher.publish_content(test_item)
    # print(f"Publish result: {'Success' if success else 'Failed'}")

if __name__ == "__main__":
    main()
