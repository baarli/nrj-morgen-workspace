#!/usr/bin/env python3
"""
Mission Control 2026 - UI Regenerator
Regenerates all HTML files with the new 2026 design
"""

import os
import re

WORKSPACE = "/root/.openclaw/workspace"
MISSION_CONTROL = f"{WORKSPACE}/mission-control/public"
TEMPLATE_FILE = f"{MISSION_CONTROL}/TEMPLATE-2026.html"

def load_template():
    """Load the 2026 template"""
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def generate_page(template, page_config):
    """Generate a page from template and config"""
    html = template
    
    # Replace all placeholders
    for key, value in page_config.items():
        placeholder = '{{' + key + '}}'
        html = html.replace(placeholder, value)
    
    return html

def get_page_configs():
    """Get configuration for all pages"""
    return {
        'total-control.html': {
            'PAGE_TITLE': 'Dashboard',
            'PAGE_SCRIPT': 'dashboard.js',
            'PAGE_STYLES': '',
            'PAGE_CONTENT': '''
                <div class="grid grid-4">
                    <div class="card">
                        <div class="card-header">
                            <div>
                                <div class="card-title">System Status</div>
                                <div class="card-subtitle">All systems operational</div>
                            </div>
                            <span class="badge badge-success">● Online</span>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <div>
                                <div class="card-title">Active Projects</div>
                                <div class="card-subtitle">Currently in progress</div>
                            </div>
                            <span class="badge badge-info">9 Total</span>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <div>
                                <div class="card-title">Cron Jobs</div>
                                <div class="card-subtitle">Scheduled tasks</div>
                            </div>
                            <span class="badge badge-success">23 Active</span>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <div>
                                <div class="card-title">Last Deploy</div>
                                <div class="card-subtitle">Production environment</div>
                            </div>
                            <span class="badge badge-success">Just now</span>
                        </div>
                    </div>
                </div>
                
                <div class="mt-xl">
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">Recent Activity</div>
                        </div>
                        <div class="text-secondary">
                            <p>✅ Automated Testing Suite deployed</p>
                            <p>✅ Security Hardening completed</p>
                            <p>✅ Dark Mode Enhancement deployed</p>
                            <p>✅ Mobile App Experience implemented</p>
                        </div>
                    </div>
                </div>
            ''',
            'PAGE_SCRIPTS': '',
            'ACTIVE_DASHBOARD': 'active',
            'ACTIVE_SAKER': '',
            'ACTIVE_ANALYTICS': '',
            'ACTIVE_PODKAST': '',
            'ACTIVE_CRON': '',
            'ACTIVE_SYSTEM': '',
            'ACTIVE_SETTINGS': ''
        },
        'sakslista-pro.html': {
            'PAGE_TITLE': 'Sakslista',
            'PAGE_SCRIPT': 'sakslista.js',
            'PAGE_STYLES': '',
            'PAGE_CONTENT': '''
                <div class="flex justify-between items-center mb-lg">
                    <h3>Dagens Saker</h3>
                    <button class="btn btn-primary">
                        <i class="fas fa-plus"></i>
                        Ny Sak
                    </button>
                </div>
                
                <div class="card">
                    <div class="text-secondary">
                        <p>Sakslista vil vises her...</p>
                    </div>
                </div>
            ''',
            'PAGE_SCRIPTS': '',
            'ACTIVE_DASHBOARD': '',
            'ACTIVE_SAKER': 'active',
            'ACTIVE_ANALYTICS': '',
            'ACTIVE_PODKAST': '',
            'ACTIVE_CRON': '',
            'ACTIVE_SYSTEM': '',
            'ACTIVE_SETTINGS': ''
        },
        'analytics.html': {
            'PAGE_TITLE': 'Analytics',
            'PAGE_SCRIPT': 'analytics.js',
            'PAGE_STYLES': '',
            'PAGE_CONTENT': '''
                <div class="grid grid-2">
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">Traffic Overview</div>
                        </div>
                        <div class="text-secondary">Analytics charts will appear here...</div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">User Statistics</div>
                        </div>
                        <div class="text-secondary">Statistics will appear here...</div>
                    </div>
                </div>
            ''',
            'PAGE_SCRIPTS': '',
            'ACTIVE_DASHBOARD': '',
            'ACTIVE_SAKER': '',
            'ACTIVE_ANALYTICS': 'active',
            'ACTIVE_PODKAST': '',
            'ACTIVE_CRON': '',
            'ACTIVE_SYSTEM': '',
            'ACTIVE_SETTINGS': ''
        },
        'podkast-control.html': {
            'PAGE_TITLE': 'Podkast',
            'PAGE_SCRIPT': 'podkast.js',
            'PAGE_STYLES': '',
            'PAGE_CONTENT': '''
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">Podkast Episoder</div>
                    </div>
                    <div class="text-secondary">Podkast content will appear here...</div>
                </div>
            ''',
            'PAGE_SCRIPTS': '',
            'ACTIVE_DASHBOARD': '',
            'ACTIVE_SAKER': '',
            'ACTIVE_ANALYTICS': '',
            'ACTIVE_PODKAST': 'active',
            'ACTIVE_CRON': '',
            'ACTIVE_SYSTEM': '',
            'ACTIVE_SETTINGS': ''
        },
        'cron-control.html': {
            'PAGE_TITLE': 'Cron Jobs',
            'PAGE_SCRIPT': 'cron.js',
            'PAGE_STYLES': '',
            'PAGE_CONTENT': '''
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">Scheduled Tasks</div>
                    </div>
                    <div class="text-secondary">Cron jobs will be listed here...</div>
                </div>
            ''',
            'PAGE_SCRIPTS': '',
            'ACTIVE_DASHBOARD': '',
            'ACTIVE_SAKER': '',
            'ACTIVE_ANALYTICS': '',
            'ACTIVE_PODKAST': '',
            'ACTIVE_CRON': 'active',
            'ACTIVE_SYSTEM': '',
            'ACTIVE_SETTINGS': ''
        },
        'system-monitor.html': {
            'PAGE_TITLE': 'System Monitor',
            'PAGE_SCRIPT': 'system.js',
            'PAGE_STYLES': '',
            'PAGE_CONTENT': '''
                <div class="grid grid-3">
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">CPU Usage</div>
                        </div>
                        <div class="text-secondary">CPU metrics...</div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">Memory</div>
                        </div>
                        <div class="text-secondary">Memory metrics...</div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">Disk</div>
                        </div>
                        <div class="text-secondary">Disk metrics...</div>
                    </div>
                </div>
            ''',
            'PAGE_SCRIPTS': '',
            'ACTIVE_DASHBOARD': '',
            'ACTIVE_SAKER': '',
            'ACTIVE_ANALYTICS': '',
            'ACTIVE_PODKAST': '',
            'ACTIVE_CRON': '',
            'ACTIVE_SYSTEM': 'active',
            'ACTIVE_SETTINGS': ''
        },
        'innstillinger.html': {
            'PAGE_TITLE': 'Innstillinger',
            'PAGE_SCRIPT': 'settings.js',
            'PAGE_STYLES': '',
            'PAGE_CONTENT': '''
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">System Settings</div>
                    </div>
                    <div class="text-secondary">Settings will appear here...</div>
                </div>
            ''',
            'PAGE_SCRIPTS': '',
            'ACTIVE_DASHBOARD': '',
            'ACTIVE_SAKER': '',
            'ACTIVE_ANALYTICS': '',
            'ACTIVE_PODKAST': '',
            'ACTIVE_CRON': '',
            'ACTIVE_SYSTEM': '',
            'ACTIVE_SETTINGS': 'active'
        }
    }

def regenerate_all_pages():
    """Regenerate all HTML pages from template"""
    print("🎨 Regenerating all Mission Control pages with 2026 design...")
    
    template = load_template()
    configs = get_page_configs()
    
    for filename, config in configs.items():
        filepath = os.path.join(MISSION_CONTROL, filename)
        
        # Backup existing file
        if os.path.exists(filepath):
            backup_path = filepath + '.old'
            os.rename(filepath, backup_path)
            print(f"  📦 Backed up: {filename}")
        
        # Generate new file
        html = generate_page(template, config)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"  ✅ Generated: {filename}")
    
    print(f"\n✅ All {len(configs)} pages regenerated with 2026 design!")

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Mission Control 2026 - UI Regenerator")
    print("=" * 60)
    
    regenerate_all_pages()
    
    print("\n" + "=" * 60)
    print("✅ ALL PAGES REGENERATED WITH MODERN 2026 DESIGN!")
    print("=" * 60)
