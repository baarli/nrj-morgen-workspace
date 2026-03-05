#!/usr/bin/env python3
"""
🔧 Cron Error Fixer - Automatisk fiks av cron job errors
"""

import json
from pathlib import Path

# Les jobs.json
jobs_file = Path('/root/.openclaw/cron/jobs.json')

with open(jobs_file, 'r') as f:
    data = json.load(f)

fixed_count = 0

for job in data.get('jobs', []):
    # Sjekk om jobben har error
    state = job.get('state', {})
    
    if state.get('lastStatus') == 'error' and 'whatsapp' in str(state.get('lastError', '')).lower():
        # Reset error state
        state['lastStatus'] = 'ok'
        state['consecutiveErrors'] = 0
        if 'lastError' in state:
            del state['lastError']
        
        # Sørg for delivery.mode er none
        if 'delivery' not in job:
            job['delivery'] = {}
        job['delivery']['mode'] = 'none'
        
        fixed_count += 1
        print(f"✅ Fixed: {job.get('name', 'Unknown')}")

# Lagre tilbake
with open(jobs_file, 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n🔧 Fixed {fixed_count} cron jobs")
