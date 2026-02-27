#!/usr/bin/env python3
"""
🌐 BAARLICLAW WEB SCRAPER
Web-scraping og data-utvinning
"""

import os
import sys
import re
import json
import time
import random
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse
from datetime import datetime

# Legg til toolkit i path
sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging, validate_url

logger = setup_logging("WebScraper")

class SimpleScraper:
    """Simple scraper using only standard library"""
    
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.last_request = 0
        self.session_cookies = {}
        
    def _rate_limit(self):
        """Respect rate limits"""
        elapsed = time.time() - self.last_request
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request = time.time()
    
    def fetch(self, url: str, headers: Optional[Dict] = None) -> Optional[str]:
        """
        Fetch HTML from URL
        
        Args:
            url: Target URL
            headers: Optional custom headers
        """
        if not validate_url(url):
            logger.error(f"Invalid URL: {url}")
            return None
        
        self._rate_limit()
        
        try:
            import urllib.request
            
            default_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            if headers:
                default_headers.update(headers)
            
            req = urllib.request.Request(url, headers=default_headers)
            
            # Add cookies if we have them for this domain
            domain = urlparse(url).netloc
            if domain in self.session_cookies:
                cookie_str = '; '.join([f"{k}={v}" for k, v in self.session_cookies[domain].items()])
                req.add_header('Cookie', cookie_str)
            
            with urllib.request.urlopen(req, timeout=30) as response:
                html = response.read().decode('utf-8', errors='ignore')
                
                # Store cookies
                if 'Set-Cookie' in response.headers:
                    self._parse_cookies(response.headers['Set-Cookie'], domain)
                
                return html
                
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
    
    def _parse_cookies(self, cookie_header: str, domain: str):
        """Parse and store cookies"""
        if domain not in self.session_cookies:
            self.session_cookies[domain] = {}
        
        for cookie in cookie_header.split(','):
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                self.session_cookies[domain][key.strip()] = value.split(';')[0].strip()
    
    def extract_links(self, html: str, base_url: str) -> List[Dict]:
        """Extract all links from HTML"""
        links = []
        
        # Simple regex for href attributes
        pattern = r'href=["\'](.*?)["\']'
        matches = re.findall(pattern, html, re.IGNORECASE)
        
        for href in matches:
            full_url = urljoin(base_url, href)
            parsed = urlparse(full_url)
            
            links.append({
                'url': full_url,
                'text': '',  # Would need HTML parsing for text
                'is_external': parsed.netloc != urlparse(base_url).netloc,
                'path': parsed.path
            })
        
        return links
    
    def extract_emails(self, html: str) -> List[str]:
        """Extract email addresses from HTML"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return list(set(re.findall(pattern, html)))
    
    def extract_phones(self, html: str) -> List[str]:
        """Extract phone numbers from HTML"""
        # Norwegian phone patterns
        patterns = [
            r'\+47[\s]?[0-9]{8}',
            r'\b[0-9]{8}\b',
            r'\b[0-9]{3}[\s][0-9]{2}[\s][0-9]{3}\b'
        ]
        
        phones = []
        for pattern in patterns:
            phones.extend(re.findall(pattern, html))
        
        return list(set(phones))
    
    def extract_meta(self, html: str) -> Dict[str, str]:
        """Extract meta tags from HTML"""
        meta = {}
        
        # Title
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        if title_match:
            meta['title'] = title_match.group(1).strip()
        
        # Meta tags
        pattern = r'<meta[^>]+name=["\']([^"\']+)["\'][^>]+content=["\']([^"\']*)["\']'
        for name, content in re.findall(pattern, html, re.IGNORECASE):
            meta[name.lower()] = content
        
        # Open Graph
        og_pattern = r'<meta[^>]+property=["\']og:([^"\']+)["\'][^>]+content=["\']([^"\']*)["\']'
        for prop, content in re.findall(og_pattern, html, re.IGNORECASE):
            meta[f'og:{prop}'] = content
        
        return meta
    
    def extract_article(self, html: str) -> Dict[str, Any]:
        """
        Extract article content from HTML
        Simple version - looks for common patterns
        """
        article = {
            'title': '',
            'author': '',
            'date': '',
            'content': '',
            'excerpt': ''
        }
        
        # Try to extract from JSON-LD
        jsonld_pattern = r'\u003cscript type=["\']application/ld\+json["\'][^\u003e]*\u003e(.*?)\u003c/script\u003e'
        for json_str in re.findall(jsonld_pattern, html, re.DOTALL | re.IGNORECASE):
            try:
                data = json.loads(json_str)
                if isinstance(data, dict) and data.get('@type') in ['Article', 'NewsArticle']:
                    article['title'] = data.get('headline', '')
                    article['author'] = data.get('author', {}).get('name', '') if isinstance(data.get('author'), dict) else str(data.get('author', ''))
                    article['date'] = data.get('datePublished', '')
                    article['content'] = data.get('articleBody', '')
                    break
            except:
                pass
        
        # Fallback to meta tags
        if not article['title']:
            meta = self.extract_meta(html)
            article['title'] = meta.get('title', '')
            article['excerpt'] = meta.get('description', '')
        
        return article

class FeedReader:
    """Read RSS/Atom feeds"""
    
    def __init__(self):
        self.scraper = SimpleScraper(delay=0.5)
    
    def parse_feed(self, url: str) -> List[Dict]:
        """
        Parse RSS/Atom feed
        
        Returns list of items with:
        - title
        - link
        - description
        - published
        """
        html = self.scraper.fetch(url)
        if not html:
            return []
        
        items = []
        
        # Try RSS format
        if '<item>' in html:
            item_pattern = r'<item\u003e(.*?)\u003c/item\u003e'
            for item_xml in re.findall(item_pattern, html, re.DOTALL):
                item = self._parse_rss_item(item_xml)
                if item:
                    items.append(item)
        
        # Try Atom format
        elif '<entry>' in html:
            entry_pattern = r'<entry\u003e(.*?)\u003c/entry\u003e'
            for entry_xml in re.findall(entry_pattern, html, re.DOTALL):
                item = self._parse_atom_entry(entry_xml)
                if item:
                    items.append(item)
        
        return items
    
    def _parse_rss_item(self, xml: str) -> Optional[Dict]:
        """Parse RSS item"""
        def get_tag(tag: str) -> str:
            pattern = f'<{tag}[^\u003e]*\u003e(.*?)\u003c/{tag}\u003e'
            match = re.search(pattern, xml, re.DOTALL | re.IGNORECASE)
            return match.group(1).strip() if match else ''
        
        title = get_tag('title')
        link = get_tag('link')
        desc = get_tag('description')
        pub_date = get_tag('pubDate')
        
        if title and link:
            return {
                'title': re.sub(r'<[^\u003e]+>', '', title),  # Remove HTML
                'link': link,
                'description': re.sub(r'<[^\u003e]+>', '', desc),
                'published': pub_date
            }
        return None
    
    def _parse_atom_entry(self, xml: str) -> Optional[Dict]:
        """Parse Atom entry"""
        def get_tag(tag: str) -> str:
            pattern = f'<{tag}[^\u003e]*\u003e(.*?)\u003c/{tag}\u003e'
            match = re.search(pattern, xml, re.DOTALL | re.IGNORECASE)
            return match.group(1).strip() if match else ''
        
        title = get_tag('title')
        link_match = re.search(r'href=["\'](.*?)["\']', xml)
        link = link_match.group(1) if link_match else ''
        summary = get_tag('summary')
        updated = get_tag('updated')
        
        if title:
            return {
                'title': re.sub(r'<[^\u003e]+>', '', title),
                'link': link,
                'description': re.sub(r'<[^\u003e]+>', '', summary),
                'published': updated
            }
        return None

class SitemapParser:
    """Parse XML sitemaps"""
    
    def __init__(self):
        self.scraper = SimpleScraper(delay=0.5)
    
    def parse(self, url: str) -> List[Dict]:
        """
        Parse sitemap.xml
        
        Returns list of URLs with metadata
        """
        html = self.scraper.fetch(url)
        if not html:
            return []
        
        urls = []
        
        # URL pattern
        url_pattern = r'<url\u003e\s*<loc\u003e(.*?)\u003c/loc\u003e'
        for match in re.findall(url_pattern, html, re.DOTALL):
            url_data = {'url': match.strip()}
            
            # Try to find lastmod
            lastmod_pattern = r'<lastmod\u003e(.*?)\u003c/lastmod\u003e'
            lastmod_match = re.search(lastmod_pattern, html)
            if lastmod_match:
                url_data['lastmod'] = lastmod_match.group(1).strip()
            
            urls.append(url_data)
        
        return urls

# === CONVENIENCE FUNCTIONS ===
def quick_scrape(url: str) -> Optional[Dict]:
    """Quick scrape - get meta and article data"""
    scraper = SimpleScraper()
    html = scraper.fetch(url)
    
    if not html:
        return None
    
    return {
        'url': url,
        'meta': scraper.extract_meta(html),
        'article': scraper.extract_article(html),
        'emails': scraper.extract_emails(html),
        'links': len(scraper.extract_links(html, url))
    }

def fetch_feed(url: str) -> List[Dict]:
    """Quick feed fetch"""
    reader = FeedReader()
    return reader.parse_feed(url)

def extract_all_links(url: str) -> List[str]:
    """Extract all links from page"""
    scraper = SimpleScraper()
    html = scraper.fetch(url)
    
    if not html:
        return []
    
    links = scraper.extract_links(html, url)
    return [l['url'] for l in links if not l['is_external']]

# === TESTING ===
if __name__ == "__main__":
    print("🌐 BaarliClaw Web Scraper - Testing")
    print("=" * 50)
    
    scraper = SimpleScraper()
    
    # Test with a simple page
    test_url = "https://httpbin.org/html"
    print(f"\n🧪 Testing with: {test_url}")
    
    html = scraper.fetch(test_url)
    if html:
        print(f"✅ Fetched {len(html)} bytes")
        
        # Test meta extraction
        meta = scraper.extract_meta(html)
        print(f"📋 Meta: {meta}")
    else:
        print("⚠️ Could not fetch test page (might be network issue)")
    
    # Test feed parsing with a known feed
    print("\n📰 Feed Parser Test:")
    # Using a simple example
    sample_rss = """<?xml version="1.0"?>
    <rss>
        <channel>
            <item>
                <title>Test Article</title>
                <link>https://example.com/1</link>
                <description>Test description</description>
            </item>
        </channel>
    </rss>"""
    
    reader = FeedReader()
    items = reader.parse_feed("data:text/xml;base64," + 
        __import__('base64').b64encode(sample_rss.encode()).decode())
    print(f"✅ Parsed {len(items)} items from sample RSS")
    
    print("\n✅ Web Scraper ready!")
