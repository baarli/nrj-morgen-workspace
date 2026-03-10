#!/usr/bin/env python3
"""
VEV DASHBOARD UPDATER MASTER v2.0
Konsolidert versjon for NRJ Dashboard
Henter data fra Nielsen Radio og Podtoppen
"""

import sys
import json
import csv
import io
import urllib.request
from datetime import datetime

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from error_handler import retry_on_error, setup_logging
from config_manager import credentials, SUPABASE_URL, SUPABASE_SERVICE_KEY, TENANT_ID

logger = setup_logging('dashboard-updater-master')

class DashboardUpdaterMaster:
    """Master class for NRJ Dashboard updates"""
    
    PANEL_ID = "0b1f6b6b-3fde-434b-b7c8-dcf306beea72"
    
    def __init__(self):
        self.stats = {
            'nielsen_fetched': False,
            'podtoppen_fetched': False,
            'updated': False
        }
    
    @retry_on_error(max_retries=3, base_delay=5)
    def fetch_nielsen(self) -> dict:
        """Fetch Nielsen Radio data"""
        url = "https://eu-iport.nielsen-iwatch.com/api/Chart?dataid=8eb6daca-1266-4af8-8e8f-f39107dc63fb&publish_key=bd551853-f42b-4b86-813a-79faf3a718e9"
        
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; NRJ Dashboard Bot)'
        })
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            
        # Extract NRJ data
        for item in data.get('chart_data', []):
            if item.get('station_name') == 'NRJ':
                return {
                    'week_number': data.get('week_number'),
                    'year': data.get('year'),
                    'daily_reach': item.get('daily_reach'),
                    'weekly_reach': item.get('weekly_reach'),
                    'market_share': item.get('market_share_percent')
                }
        return None
    
    @retry_on_error(max_retries=3, base_delay=5)
    def fetch_podtoppen(self) -> dict:
        """Fetch Podtoppen podcast data"""
        url = "https://podtoppen.tnslistene.no/export.php"
        
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; NRJ Dashboard Bot)'
        })
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read().decode('latin-1')
        
        # Parse CSV
        reader = csv.DictReader(io.StringIO(content), delimiter=';')
        
        for row in reader:
            if 'NRJ Morgen' in row.get('Podkast', ''):
                return {
                    'week_number': row.get('Uke'),
                    'year': row.get('År'),
                    'rank': int(row.get('Rank', 0)),
                    'unique_listeners': int(row.get('Unike lyttere', 0).replace(' ', '') or 0),
                    'downloads': int(row.get('Nedlastinger', 0).replace(' ', '') or 0)
                }
        return None
    
    def update_supabase(self, nielsen_data: dict, podtoppen_data: dict) -> bool:
        """Update Supabase dashboard panel"""
        try:
            # Build content
            content = f"""# 📻 NRJ MORGEN - STATISTIKK

## Radio (Nielsen)
- **Uke:** {nielsen_data.get('week_number', 'N/A')} {nielsen_data.get('year', '')}
- **Daglige lyttere:** {nielsen_data.get('daily_reach', 0):,}
- **Ukentlig rekkevidde:** {nielsen_data.get('weekly_reach', 0):,}
- **Markedsandel:** {nielsen_data.get('market_share', 0)}%

## Podcast (Podtoppen)
- **Rangering:** #{podtoppen_data.get('rank', 'N/A')}
- **Unike lyttere:** {podtoppen_data.get('unique_listeners', 0):,}
- **Nedlastinger:** {podtoppen_data.get('downloads', 0):,}

Oppdatert: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
            
            # Prepare payload
            payload = {
                'id': self.PANEL_ID,
                'tenant_id': TENANT_ID,
                'title': '📊 NRJ Statistikk',
                'content': content,
                'category': 'STATS',
                'is_pinned': True,
                'link_metadata': {
                    'nielsen': nielsen_data,
                    'podtoppen': podtoppen_data
                }
            }
            
            # Update Supabase
            req = urllib.request.Request(
                f"{SUPABASE_URL}/rest/v1/agenda_items?id=eq.{self.PANEL_ID}",
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    'apikey': SUPABASE_SERVICE_KEY,
                    'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
                    'Content-Type': 'application/json'
                },
                method='PATCH'
            )
            
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.status in [200, 201, 204]
                
        except Exception as e:
            logger.error(f"Update failed: {e}")
            return False
    
    def run(self):
        """Execute full dashboard update"""
        logger.info("=" * 70)
        logger.info("📊 NRJ DASHBOARD UPDATER MASTER v2.0")
        logger.info("=" * 70)
        
        try:
            # Fetch Nielsen data
            logger.info("📡 Fetching Nielsen Radio data...")
            nielsen = self.fetch_nielsen()
            if nielsen:
                self.stats['nielsen_fetched'] = True
                logger.info(f"✅ Nielsen: {nielsen.get('daily_reach', 0):,} daily reach")
            else:
                logger.warning("❌ Nielsen data not found")
            
            # Fetch Podtoppen data
            logger.info("🎧 Fetching Podtoppen data...")
            podtoppen = self.fetch_podtoppen()
            if podtoppen:
                self.stats['podtoppen_fetched'] = True
                logger.info(f"✅ Podtoppen: #{podtoppen.get('rank')} rank")
            else:
                logger.warning("❌ Podtoppen data not found")
            
            # Update Supabase
            if nielsen or podtoppen:
                logger.info("💾 Updating Supabase...")
                success = self.update_supabase(nielsen or {}, podtoppen or {})
                self.stats['updated'] = success
                
                if success:
                    logger.info("✅ Dashboard updated successfully")
                else:
                    logger.error("❌ Dashboard update failed")
            else:
                logger.error("❌ No data available to update")
            
            logger.info("=" * 70)
            return self.stats['updated']
            
        except Exception as e:
            logger.error(f"Dashboard updater failed: {e}")
            raise

if __name__ == '__main__':
    updater = DashboardUpdaterMaster()
    updater.run()
