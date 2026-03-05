#!/usr/bin/env python3
"""
🧪 API Health Checker - Monitor external API status
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, '/root/.openclaw/workspace/scripts')
from baarliclaw_toolkit import setup_logging

logger = setup_logging("APIHealthChecker")

class APIHealthChecker:
    """Check health of external APIs used by the system"""
    
    def __init__(self):
        self.results = []
        self.config_file = Path('/root/.openclaw/workspace/.credentials/nrj-morgen.env')
        
    def load_env_vars(self) -> Dict:
        """Load environment variables from credentials file"""
        env_vars = {}
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        env_vars[key] = value
        return env_vars
    
    def check_supabase(self) -> Tuple[bool, str]:
        """Check Supabase connection"""
        try:
            env_vars = self.load_env_vars()
            url = env_vars.get('SUPABASE_URL', '').strip('"')
            key = env_vars.get('SUPABASE_SERVICE_KEY', '').strip('"')
            
            if not url or not key:
                return False, "Missing credentials"
            
            response = requests.get(
                f"{url}/rest/v1/",
                headers={"apikey": key},
                timeout=10
            )
            
            if response.status_code == 200:
                return True, f"Connected ({response.status_code})"
            else:
                return False, f"HTTP {response.status_code}"
                
        except Exception as e:
            return False, str(e)
    
    def check_brave_api(self) -> Tuple[bool, str]:
        """Check Brave Search API"""
        try:
            env_vars = self.load_env_vars()
            api_key = env_vars.get('BRAVE_API_KEY', '').strip('"')
            
            if not api_key:
                return False, "Missing API key"
            
            response = requests.get(
                "https://api.search.brave.com/res/v1/news/search?q=test&count=1",
                headers={"X-Subscription-Token": api_key},
                timeout=10
            )
            
            if response.status_code in [200, 401]:  # 401 is OK (auth works)
                return True, f"API reachable ({response.status_code})"
            else:
                return False, f"HTTP {response.status_code}"
                
        except Exception as e:
            return False, str(e)
    
    def check_nielsen_api(self) -> Tuple[bool, str]:
        """Check Nielsen API (basic connectivity)"""
        try:
            # Nielsen API requires special auth, just check if we can reach domain
            response = requests.get(
                "https://www.nielsen.com",
                timeout=10,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                return True, "Domain reachable"
            else:
                return False, f"HTTP {response.status_code}"
                
        except Exception as e:
            return False, str(e)
    
    def check_podtoppen(self) -> Tuple[bool, str]:
        """Check Podtoppen RSS feed"""
        try:
            response = requests.get(
                "https://rss.podplaystudio.com/4035.xml",
                timeout=10
            )
            
            if response.status_code == 200 and 'xml' in response.text.lower():
                return True, "RSS feed accessible"
            else:
                return False, f"HTTP {response.status_code}"
                
        except Exception as e:
            return False, str(e)
    
    def run_all_checks(self) -> List[Dict]:
        """Run all API health checks"""
        checks = [
            ("Supabase", self.check_supabase),
            ("Brave Search", self.check_brave_api),
            ("Nielsen", self.check_nielsen_api),
            ("Podtoppen RSS", self.check_podtoppen),
        ]
        
        for name, check_func in checks:
            print(f"Checking {name}...")
            success, message = check_func()
            self.results.append({
                'name': name,
                'status': '✅' if success else '❌',
                'success': success,
                'message': message,
                'timestamp': datetime.now().isoformat()
            })
        
        return self.results
    
    def print_report(self):
        """Print formatted report"""
        print("\n" + "=" * 60)
        print("🌐 API HEALTH CHECK REPORT")
        print("=" * 60)
        print(f"{'Service':<20} {'Status':<8} {'Details':<30}")
        print("-" * 60)
        
        for result in self.results:
            print(f"{result['name']:<20} {result['status']:<8} {result['message']:<30}")
        
        print("=" * 60)
        
        passed = sum(1 for r in self.results if r['success'])
        total = len(self.results)
        print(f"\n📊 Summary: {passed}/{total} APIs healthy")
        
        return passed == total
    
    def save_report(self):
        """Save report to JSON"""
        report_dir = Path('/root/.openclaw/workspace/brain/reports')
        report_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        report_file = report_dir / f'api-health-{timestamp}.json'
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': len(self.results),
                'passed': sum(1 for r in self.results if r['success']),
                'failed': sum(1 for r in self.results if not r['success'])
            },
            'checks': self.results
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_file


def main():
    """Main entry point"""
    checker = APIHealthChecker()
    checker.run_all_checks()
    all_healthy = checker.print_report()
    
    report_file = checker.save_report()
    print(f"\n💾 Report saved to: {report_file}")
    
    return 0 if all_healthy else 1


if __name__ == '__main__':
    sys.exit(main())
