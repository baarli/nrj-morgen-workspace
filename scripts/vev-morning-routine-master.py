#!/usr/bin/env python3
"""
VEV MORNING ROUTINE MASTER v3.0
Konsolidert versjon som erstatter alle tidligere varianter
"""

import sys
import os
import json
import uuid
import time
import base64
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, '/root/.openclaw/workspace/scripts')

# Import error handling and config modules
from error_handler import retry_on_error, safe_execute, setup_logging
from config_manager import credentials, SUPABASE_URL, SUPABASE_SERVICE_KEY, TENANT_ID, CREATED_BY

# Setup logging
logger = setup_logging('morning-routine-master')

class MorningRoutineMaster:
    """Master class for NRJ Morgen Morning Routine"""
    
    def __init__(self):
        self.stats = {
            'articles_found': 0,
            'articles_inserted': 0,
            'images_generated': 0,
            'errors': []
        }
        self.today = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
    @retry_on_error(max_retries=3, base_delay=5)
    def search_brave(self, query: str, count: int = 5) -> list:
        """Search Brave News API with retry"""
        brave_key = credentials.brave_api_key
        if not brave_key:
            raise ValueError("BRAVE_API_KEY not found")
            
        encoded_query = urllib.parse.quote(query)
        url = f"https://api.search.brave.com/res/v1/news/search?q={encoded_query}&count={count}&search_lang=nb&country=no&freshness=pd"
        
        headers = {
            'X-Subscription-Token': brave_key,
            'Accept': 'application/json'
        }
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data.get('results', [])
    
    @retry_on_error(max_retries=3, base_delay=2)
    def generate_ai_image(self, title: str, description: str, article_id: str) -> str:
        """Generate AI image with retry"""
        openai_key = credentials.openai_api_key
        if not openai_key:
            return None
            
        prompt = f"News illustration: {title}. Professional, vibrant, no text."
        
        payload = {
            "model": "gpt-image-1",
            "prompt": prompt[:1000],
            "size": "1024x1024",
            "n": 1
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_key}"
        }
        
        req = urllib.request.Request(
            "https://api.openai.com/v1/images/generations",
            data=json.dumps(payload).encode('utf-8'),
            headers=headers
        )
        
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode())
            image_data = base64.b64decode(data['data'][0]['b64_json'])
        
        # Upload to Supabase
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c for c in title[:15] if c.isalnum()).replace(' ', '_')
        filename = f"nrj-news/{timestamp}_{safe_title}_{article_id[:6]}.png"
        
        upload_url = f"{SUPABASE_URL}/storage/v1/object/media-library/{filename}"
        upload_headers = {
            'apikey': SUPABASE_SERVICE_KEY,
            'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
            'Content-Type': 'image/png'
        }
        
        req = urllib.request.Request(upload_url, data=image_data, headers=upload_headers, method='POST')
        with urllib.request.urlopen(req, timeout=60) as resp:
            if resp.status in [200, 201]:
                return f"{SUPABASE_URL}/storage/v1/object/public/media-library/{filename}"
        return None
    
    def insert_to_supabase(self, articles: list) -> int:
        """Insert articles to Supabase"""
        inserted = 0
        
        for i, article in enumerate(articles, 1):
            try:
                title = article['title']
                url = article['url']
                description = article.get('description', '')
                source = article.get('source', 'Ukjent')
                score = article.get('score', 50)
                
                # Generate image for top 3
                image_url = None
                if i <= 3:
                    try:
                        article_id = str(uuid.uuid4())
                        image_url = self.generate_ai_image(title, description, article_id)
                        if image_url:
                            self.stats['images_generated'] += 1
                            time.sleep(2)  # Rate limiting
                    except Exception as e:
                        logger.warning(f"Image generation failed: {e}")
                
                # Prepare payload
                notes = f"Score: {score}/100 | Kilde: {source}\n\n{description[:150]}"
                payload = {
                    'id': str(uuid.uuid4()),
                    'tenant_id': TENANT_ID,
                    'title': title,
                    'description': description,
                    'notes': notes,
                    'link_url': url,
                    'show_date': self.today,
                    'category': 'TALK',
                    'created_by': CREATED_BY,
                    'is_pinned': False,
                    'is_completed': False,
                    'order_index': i
                }
                
                if image_url:
                    payload['link_metadata'] = {'image_url': image_url}
                
                # Insert to Supabase
                req = urllib.request.Request(
                    f"{SUPABASE_URL}/rest/v1/agenda_items",
                    data=json.dumps(payload).encode('utf-8'),
                    headers={
                        'apikey': SUPABASE_SERVICE_KEY,
                        'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
                        'Content-Type': 'application/json'
                    }
                )
                
                with urllib.request.urlopen(req, timeout=15) as resp:
                    if resp.status in [200, 201]:
                        inserted += 1
                        
            except Exception as e:
                logger.error(f"Insert failed: {e}")
                self.stats['errors'].append(str(e))
        
        return inserted
    
    def run(self):
        """Execute full morning routine"""
        logger.info("=" * 70)
        logger.info("🚀 NRJ MORGEN - MORNING ROUTINE MASTER v3.0")
        logger.info("=" * 70)
        
        try:
            # Search queries
            queries = [
                "site:vg.no rampelys", "site:tv2.no underholdning",
                "site:nettavisen.no kjendis", "site:seher.no kjendis",
                "Farmen Kjendis", "Paradise Hotel", "Spillet TV 2",
                "Spellemannprisen", "Eurovision", "rød løper"
            ]
            
            # Search for articles
            all_articles = []
            for query in queries:
                try:
                    results = self.search_brave(query, 5)
                    all_articles.extend(results)
                except Exception as e:
                    logger.warning(f"Search failed for {query}: {e}")
            
            self.stats['articles_found'] = len(all_articles)
            logger.info(f"📰 {len(all_articles)} articles found")
            
            # Deduplicate and score
            seen = set()
            unique = []
            for article in all_articles:
                key = article.get('title', '')[:30].lower()
                if key and key not in seen:
                    seen.add(key)
                    unique.append({
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'url': article.get('url', ''),
                        'source': article.get('meta_url', {}).get('hostname', 'Ukjent'),
                        'score': 50
                    })
            
            # Sort and select top 15
            unique.sort(key=lambda x: x['score'], reverse=True)
            top_15 = unique[:15]
            
            # Insert to Supabase
            inserted = self.insert_to_supabase(top_15)
            self.stats['articles_inserted'] = inserted
            
            # Report success
            logger.info("=" * 70)
            logger.info(f"✅ Completed: {inserted}/15 articles inserted")
            logger.info(f"🎨 {self.stats['images_generated']} images generated")
            logger.info("=" * 70)
            
            return True
            
        except Exception as e:
            logger.error(f"Morning routine failed: {e}")
            raise

if __name__ == '__main__':
    routine = MorningRoutineMaster()
    routine.run()
