#!/usr/bin/env python3
"""
🎙️ NRJ MORGEN - MORNING ROUTINE (REFACTORED v3.0)
==================================================
Fullstendig refactored versjon med:
- ✅ Sikker credential-håndtering (ingen hardkodede verdier)
- ✅ Konsistent logging
- ✅ Retry-logikk med exponential backoff
- ✅ Standardisert error handling
- ✅ Execution summary

Author: Vev
Version: 3.0
Date: 2026-03-11
"""

import sys
import json
import concurrent.futures
import urllib.request
import urllib.parse
import urllib.error
import uuid
import base64
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
import time

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from base_script import (
    BaseScript, 
    retry_with_backoff, 
    APIError, 
    CredentialError,
    handle_error,
    truncate_text
)

class MorningRoutine(BaseScript):
    """
    NRJ Morgen Morning Routine - henter nyheter og genererer AI-bilder.
    """
    
    def __init__(self):
        super().__init__("morning-routine", log_to_file=True)
        
        # Load credentials securely
        self.logger.info("Loading credentials...")
        try:
            self.supabase_url = self.get_credential("SUPABASE_URL")
            self.supabase_key = self.get_credential("SUPABASE_SERVICE_KEY")
            self.brave_key = self.get_credential("BRAVE_API_KEY")
            self.openai_key = self.get_credential("OPENAI_API_KEY")
            self.tenant_id = self.get_credential("TENANT_ID")
            self.created_by = self.get_credential("USER_ID")
            self.bucket_name = "media-library"
            self.logger.info("✅ All credentials loaded successfully")
        except CredentialError as e:
            self.logger.error(f"Failed to load credentials: {e}")
            raise
        
        # Configuration
        self.target_article_count = 15
        self.search_queries = [
            "site:vg.no rampelys",
            "site:tv2.no underholdning",
            "site:nettavisen.no kjendis",
            "site:seher.no kjendis",
            "site:seher.no reality",
            "Farmen Kjendis 2026",
            "Paradise Hotel Norge",
            "Spillet TV 2",
            "Spellemannprisen 2026",
            "Eurovision Norge",
            "rød løper Norge",
            "norsk premiere"
        ]
    
    # =========================================================================
    # SEARCH FUNCTIONS
    # =========================================================================
    
    @retry_with_backoff(
        max_retries=3, 
        base_delay=2.0, 
        exceptions=(urllib.error.URLError, TimeoutError, ConnectionError)
    )
    def search_brave(self, query: str, count: int = 5) -> Optional[Dict]:
        """
        Søk med Brave API - med retry-logikk.
        
        Args:
            query: Søkestreng
            count: Antall resultater
        
        Returns:
            JSON respons eller None ved feil
        """
        encoded_query = urllib.parse.quote(query)
        url = (
            f"https://api.search.brave.com/res/v1/news/search"
            f"?q={encoded_query}&count={count}&search_lang=nb"
            f"&country=no&freshness=pd"
        )
        
        headers = {
            'X-Subscription-Token': self.brave_key,
            'Accept': 'application/json'
        }
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            self.logger.error(f"Brave API HTTP {e.code}: {e.reason}")
            if e.code == 429:  # Rate limited
                raise  # Trigger retry
            elif e.code >= 500:
                raise  # Server error, retry
            else:
                # Client error, don't retry
                raise APIError(
                    f"Brave API client error: {e.reason}", 
                    status_code=e.code
                )
    
    def search_all_queries(self) -> List[Dict]:
        """
        Kjør alle søk parallelt og samle resultater.
        
        Returns:
            Liste med artikler
        """
        self.logger.info(f"Starting {len(self.search_queries)} parallel searches...")
        all_articles = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            future_to_query = {
                executor.submit(self.search_brave, query, 5): query 
                for query in self.search_queries
            }
            
            completed = 0
            for future in concurrent.futures.as_completed(future_to_query):
                query = future_to_query[future]
                completed += 1
                
                try:
                    data = future.result()
                    if data and 'results' in data:
                        articles = self._process_search_results(data['results'])
                        all_articles.extend(articles)
                        self.logger.info(
                            f"✅ {completed}/{len(self.search_queries)}: "
                            f"{query[:30]}... ({len(articles)} articles)"
                        )
                except Exception as e:
                    self.record_error()
                    self.logger.warning(
                        f"⚠️  {completed}/{len(self.search_queries)}: "
                        f"{query[:30]}... failed: {e}"
                    )
        
        self.logger.info(f"Total articles found: {len(all_articles)}")
        return all_articles
    
    def _process_search_results(self, results: List[Dict]) -> List[Dict]:
        """Prosesser søkeresultater og filtrer uønskede."""
        articles = []
        
        for result in results:
            title = result.get('title', '').strip()
            desc = result.get('description', '').strip()
            url = result.get('url', '').strip()
            
            # Skip hard news
            if self._is_hard_news(title, desc):
                continue
            
            # Only approved sources
            approved_sources = ['vg.no', 'tv2.no', 'nettavisen.no', 'seher.no']
            if not any(src in url.lower() for src in approved_sources):
                continue
            
            articles.append({
                'title': self._create_short_title(title),
                'original_title': title,
                'description': desc,
                'url': url,
                'source': result.get('meta_url', {}).get('hostname', 'Unknown'),
                'score': self._calculate_score(title, desc)
            })
        
        return articles
    
    def _is_hard_news(self, title: str, description: str) -> bool:
        """Sjekk om det er hard nyhet som skal ekskluderes."""
        combined = (title + ' ' + description).lower()
        
        hard_keywords = [
            'krig', 'terror', 'angrep', 'drap', 'voldtekt', 'overgrep',
            'tragedie', 'ulykke', 'død', 'omkom', 'drept', 'skutt',
            'politi', 'pågripelse', 'fengsel', 'dom', 'rettssak',
            'regjering', 'storting', 'parti', 'politikk', 'lovforslag'
        ]
        
        return any(word in combined for word in hard_keywords)
    
    def _create_short_title(self, original_title: str) -> str:
        """Lag kort tittel - maks 6-7 ord."""
        words = original_title.split()
        
        if len(words) <= 7:
            return original_title
        
        key_words = []
        skip_words = {'den', 'det', 'som', 'for', 'med', 'til', 'av', 'på', 'om', 'er', 'å', 'en', 'et'}
        
        for word in words:
            if word.lower() not in skip_words and len(key_words) < 7:
                key_words.append(word)
        
        short_title = ' '.join(key_words)
        if len(words) > 7:
            short_title = short_title.rstrip('.') + '...'
        
        return short_title
    
    def _calculate_score(self, title: str, description: str) -> int:
        """Vurder underholdningsverdi (0-100)."""
        score = 50
        combined = (title + ' ' + description).lower()
        
        # Boost for ønskede temaer
        if any(x in combined for x in ['rød løper', 'premiere', 'galla', 'fest']):
            score += 20
        if any(x in combined for x in ['farmen', 'paradise hotel', 'spillet', 'kompani lauritzen']):
            score += 15
        if any(x in combined for x in ['spellemann', 'p3 gull', 'vg-lista', 'eurovision']):
            score += 15
        if any(x in combined for x in ['brudd', 'skandale', 'avsløring', 'ny kjæreste']):
            score += 10
        
        # Reduser for potensielt harde temaer
        if any(x in combined for x in ['kronprins', 'mette-marit', 'kongehus']):
            score -= 20
        
        return max(0, min(100, score))
    
    def deduplicate_and_sort(self, articles: List[Dict]) -> List[Dict]:
        """Fjern duplikater og sorter etter score."""
        seen_urls = set()
        seen_titles = set()
        unique = []
        
        for article in articles:
            url = article['url']
            title_key = article['title'][:25].lower()
            
            if url not in seen_urls and title_key not in seen_titles:
                seen_urls.add(url)
                seen_titles.add(title_key)
                unique.append(article)
        
        unique.sort(key=lambda x: x['score'], reverse=True)
        return unique[:self.target_article_count]
    
    # =========================================================================
    # IMAGE GENERATION
    # =========================================================================
    
    @retry_with_backoff(
        max_retries=2,
        base_delay=2.0,
        exceptions=(urllib.error.URLError, TimeoutError, ConnectionError, APIError)
    )
    def generate_image(self, title: str, description: str) -> Optional[bytes]:
        """
        Generer AI-bilde med OpenAI.
        
        Args:
            title: Artikkel tittel
            description: Artikkel beskrivelse
        
        Returns:
            Bilde data som bytes eller None
        """
        prompt = self._create_image_prompt(title, description)
        
        payload = {
            "model": "gpt-image-1",
            "prompt": prompt[:4000],
            "size": "1024x1024",
            "n": 1
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_key}"
        }
        
        req = urllib.request.Request(
            "https://api.openai.com/v1/images/generations",
            data=json.dumps(payload).encode('utf-8'),
            headers=headers
        )
        
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode())
                return base64.b64decode(data['data'][0]['b64_json'])
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if hasattr(e, 'read') else 'Unknown'
            self.logger.error(f"OpenAI API error: {e.code} - {error_body[:200]}")
            raise APIError(
                f"OpenAI image generation failed",
                status_code=e.code,
                response=error_body
            )
    
    def _create_image_prompt(self, title: str, description: str) -> str:
        """Lag prompt for AI-bildegenerering."""
        
        title_short = title[:100]
        desc_short = description[:150] if description else ""
        
        # Identifiser tema
        keywords = {
            'oscar': 'glamorous Oscar awards ceremony, red carpet, Hollywood lights',
            'eurovision': 'Eurovision Song Contest stage, colorful lights, music performance',
            'reality': 'reality TV show scene, dramatic lighting, television studio',
            'premiere': 'movie or show premiere, red carpet event, glamorous atmosphere',
            'brudd': 'emotional scene, relationship drama, soft lighting',
            'artist': 'music artist performance, concert vibes, creative setting'
        }
        
        style_hints = "professional news illustration, vibrant colors, modern composition"
        combined = (title_short + " " + desc_short).lower()
        
        for key, style in keywords.items():
            if key in combined:
                style_hints = style + ", " + style_hints
                break
        
        return f"""Create a professional news illustration for an entertainment news article.

Headline: "{title_short}"
Context: {desc_short}

Visual style: {style_hints}
Mood: Engaging, energetic, suitable for morning radio show audience 18-35
Composition: Clean, eye-catching, suitable as article header image
Important: No text in the image, no watermarks, professional photojournalism style

Create a compelling visual that captures the essence of this Norwegian entertainment news story."""
    
    @retry_with_backoff(
        max_retries=3,
        base_delay=1.0,
        exceptions=(urllib.error.URLError, TimeoutError)
    )
    def upload_image_to_supabase(self, image_data: bytes, filename: str) -> Optional[str]:
        """
        Last opp bilde til Supabase Storage.
        
        Args:
            image_data: Bilde som bytes
            filename: Filnavn
        
        Returns:
            Public URL eller None
        """
        upload_url = f"{self.supabase_url}/storage/v1/object/{self.bucket_name}/{filename}"
        
        headers = {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'image/png'
        }
        
        req = urllib.request.Request(
            upload_url,
            data=image_data,
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=60) as resp:
            if resp.status in [200, 201]:
                return f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{filename}"
            else:
                raise APIError(f"Upload failed with status {resp.status}", status_code=resp.status)
    
    def generate_all_images(self, articles: List[Dict]) -> Dict[int, Optional[str]]:
        """
        Generer bilder for alle artikler.
        
        Args:
            articles: Liste med artikler
        
        Returns:
            Dict med artikkel indeks -> bilde URL
        """
        self.logger.info(f"\n🎨 Generating images for {len(articles)} articles...")
        self.logger.info(f"   (Estimated time: ~{len(articles) * 2} seconds with rate limiting)\n")
        
        image_urls = {}
        last_call = 0
        MIN_DELAY = 2.0  # OpenAI rate limit
        
        for i, article in enumerate(articles, 1):
            title = article.get('title', '')
            description = article.get('description', '')
            
            self.logger.info(f"{i:2}. {truncate_text(title, 40)}... ", end="")
            
            # Rate limiting
            elapsed = time.time() - last_call
            if elapsed < MIN_DELAY:
                sleep_time = MIN_DELAY - elapsed
                time.sleep(sleep_time)
            
            try:
                # Generate image
                image_data = self.generate_image(title, description)
                
                # Create filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_title = "".join(c for c in title[:20] if c.isalnum()).replace(' ', '_')
                filename = f"nrj-news/{timestamp}_{safe_title}_{uuid.uuid4().hex[:6]}.png"
                
                # Upload
                image_url = self.upload_image_to_supabase(image_data, filename)
                
                image_urls[i] = image_url
                last_call = time.time()
                self.logger.info("✅")
                
            except Exception as e:
                self.record_error()
                handle_error(self.logger, e, {
                    'function': 'generate_all_images',
                    'article_index': i,
                    'article_title': title
                })
                image_urls[i] = None
                self.logger.info("❌")
        
        return image_urls
    
    # =========================================================================
    # DATABASE OPERATIONS
    # =========================================================================
    
    @retry_with_backoff(
        max_retries=3,
        base_delay=1.0,
        exceptions=(urllib.error.URLError, TimeoutError)
    )
    def _insert_article(self, payload: Dict) -> bool:
        """Internal insert med retry."""
        url = f"{self.supabase_url}/rest/v1/agenda_items"
        
        headers = {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers
        )
        
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status in [200, 201]
    
    def insert_articles(self, articles: List[Dict], image_urls: Dict[int, Optional[str]]) -> int:
        """
        Insert alle artikler til Supabase.
        
        Args:
            articles: Liste med artikler
            image_urls: Dict med bilde URLs
        
        Returns:
            Antall insertete artikler
        """
        self.logger.info(f"\n💾 Inserting {len(articles)} articles to Supabase...\n")
        
        today = datetime.now().strftime("%Y-%m-%d")
        inserted = 0
        
        for i, article in enumerate(articles, 1):
            title = article.get('title', '')
            
            self.logger.info(f"{i:2}. {truncate_text(title, 45)}... ", end="")
            
            # Create notes
            desc = article.get('description', '')
            score = article.get('score', 50)
            source = article.get('source', 'Unknown')
            notes = f"Score: {score}/100 | Source: {source}\n\n{desc[:150]}"
            
            payload = {
                'id': str(uuid.uuid4()),
                'tenant_id': self.tenant_id,
                'title': title,
                'description': desc,
                'notes': notes,
                'link_url': article.get('url', ''),
                'show_date': today,
                'category': 'TALK',
                'created_by': self.created_by,
                'is_pinned': False,
                'is_completed': False,
                'order_index': i
            }
            
            # Add image if available
            if image_urls.get(i):
                payload['link_metadata'] = {'image_url': image_urls[i]}
            
            try:
                if self._insert_article(payload):
                    self.logger.info("✅")
                    inserted += 1
                else:
                    self.logger.info("⚠️  Unexpected response")
                    self.record_error()
            except Exception as e:
                self.record_error()
                handle_error(self.logger, e, {
                    'function': 'insert_articles',
                    'article_index': i,
                    'article_title': title
                })
                self.logger.info("❌")
        
        return inserted
    
    # =========================================================================
    # MAIN EXECUTION
    # =========================================================================
    
    def run(self) -> int:
        """Hoved entry point."""
        try:
            self.logger.info("=" * 70)
            self.logger.info("🚀 NRJ MORGEN - MORNING ROUTINE v3.0")
            self.logger.info("=" * 70)
            
            # Validate credentials
            self.validate_required_credentials(
                "SUPABASE_URL",
                "SUPABASE_SERVICE_KEY", 
                "BRAVE_API_KEY",
                "OPENAI_API_KEY"
            )
            
            # Step 1: Search
            self.logger.info("\n📡 STEP 1: Searching for articles...")
            all_articles = self.search_all_queries()
            
            # Deduplicate and sort
            top_articles = self.deduplicate_and_sort(all_articles)
            self.logger.info(f"✅ Selected {len(top_articles)} unique articles")
            
            if len(top_articles) < 5:
                self.logger.warning(f"⚠️  Only {len(top_articles)} articles found, minimum is 5")
            
            # Step 2: Generate images
            image_urls = self.generate_all_images(top_articles)
            successful_images = sum(1 for v in image_urls.values() if v)
            self.logger.info(f"✅ Generated {successful_images}/{len(top_articles)} images")
            
            # Step 3: Insert to database
            inserted = self.insert_articles(top_articles, image_urls)
            
            # Summary
            self.log_summary(
                success=(inserted >= 5),
                details={
                    "articles_found": len(all_articles),
                    "articles_unique": len(top_articles),
                    "articles_inserted": inserted,
                    "images_generated": successful_images,
                    "target_count": self.target_article_count
                }
            )
            
            # Return appropriate exit code
            if inserted >= 5:
                self.logger.info("✅ Morning routine completed successfully")
                return 0
            else:
                self.logger.error(f"❌ Only {inserted} articles inserted, minimum is 5")
                return 1
                
        except CredentialError as e:
            handle_error(self.logger, e, {'function': 'run'})
            self.log_summary(success=False)
            return 2
        except Exception as e:
            handle_error(self.logger, e, {'function': 'run'})
            self.log_summary(success=False)
            return 1


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    script = MorningRoutine()
    sys.exit(script.run())
