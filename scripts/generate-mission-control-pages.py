#!/usr/bin/env python3
"""
Mission Control HTML Generator
Regenerates all HTML files from master template to ensure consistency
"""

import os
import re
from datetime import datetime

WORKSPACE = "/root/.openclaw/workspace"
MISSION_CONTROL = f"{WORKSPACE}/mission-control/public"
TEMPLATE_FILE = f"{MISSION_CONTROL}/TEMPLATE.html"

def load_template():
    """Load the master template"""
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
            'PAGE_TITLE': 'Oversikt',
            'PAGE_SCRIPTS': '<script src="total-control.js" defer></script>',
            'PAGE_CSS': '',
            'PAGE_CONTENT': '''
                <div class="header">
                    <h2>Total Control</h2>
                    <span class="status-badge status-ok" id="system-status-badge">🟢 Alle systemer operative</span>
                </div>
                
                <!-- Systems Grid -->
                <div class="systems-grid" id="systems-grid">
                    <!-- Populated by JavaScript -->
                </div>
                
                <!-- Quick Actions -->
                <div class="quick-actions">
                    <button class="action-btn" onclick="runMorningRoutine()">
                        <i class="fas fa-play"></i> Morning Routine
                    </button>
                    <button class="action-btn" onclick="deployAll()">
                        <i class="fas fa-rocket"></i> Deploy Alt
                    </button>
                    <button class="action-btn" onclick="restartAgent()">
                        <i class="fas fa-sync"></i> Restart Agent
                    </button>
                    <button class="action-btn" onclick="showLogs()">
                        <i class="fas fa-file-alt"></i> Vis Logger
                    </button>
                </div>
                
                <!-- Activity Log -->
                <div class="activity-log">
                    <h3><i class="fas fa-list"></i> Aktivitetslogg</h3>
                    <div class="log-container" id="activity-container"></div>
                </div>
            ''',
            'PAGE_JS': '''
                // Total Control specific code
                console.log('Total Control loaded');
            ''',
            'ACTIVE_OVERSIKT': 'active',
            'ACTIVE_SAKER': '',
            'ACTIVE_ANALYSE': '',
            'ACTIVE_AI': '',
            'ACTIVE_WIDGETS': '',
            'ACTIVE_PODKAST': '',
            'ACTIVE_CRON': '',
            'ACTIVE_AGENT': '',
            'ACTIVE_VARSLER': '',
            'ACTIVE_SYSTEM': '',
            'ACTIVE_DATABASE': '',
            'ACTIVE_GIT': '',
            'ACTIVE_API': '',
            'ACTIVE_INSTILLINGER': ''
        },
        'sakslista-pro.html': {
            'PAGE_TITLE': 'Sakslista Pro',
            'PAGE_SCRIPTS': '''
                <script src="https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.15.0/Sortable.min.js"></script>
                <script src="sakslista-pro.js" defer></script>
            ''',
            'PAGE_CSS': '''
                .sak-item { display: flex; align-items: center; gap: 12px; padding: 16px; background: var(--bg-card); border-radius: 8px; margin-bottom: 8px; }
                .sak-actions { display: flex; gap: 4px; }
                .sak-actions button { background: none; border: none; color: var(--text-muted); cursor: pointer; padding: 8px; border-radius: 6px; }
                .sak-actions button:hover { background: rgba(255,255,255,0.1); color: white; }
                .ai-suggest { background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%) !important; color: var(--primary) !important; }
            ''',
            'PAGE_CONTENT': '''
                <div class="header">
                    <h2>Sakslista Pro</h2>
                    <div class="header-actions">
                        <button class="btn btn-primary" onclick="runMorningRoutine()">
                            <i class="fas fa-play"></i> Morning Routine
                        </button>
                        <button class="btn" onclick="showAddModal()">
                            <i class="fas fa-plus"></i> Ny Sak
                        </button>
                    </div>
                </div>
                
                <div id="saker-list"></div>
            ''',
            'PAGE_JS': '''
                // Sakslista Pro specific code
                console.log('Sakslista Pro loaded');
            ''',
            'ACTIVE_OVERSIKT': '',
            'ACTIVE_SAKER': 'active',
            'ACTIVE_ANALYSE': '',
            'ACTIVE_AI': '',
            'ACTIVE_WIDGETS': '',
            'ACTIVE_PODKAST': '',
            'ACTIVE_CRON': '',
            'ACTIVE_AGENT': '',
            'ACTIVE_VARSLER': '',
            'ACTIVE_SYSTEM': '',
            'ACTIVE_DATABASE': '',
            'ACTIVE_GIT': '',
            'ACTIVE_API': '',
            'ACTIVE_INSTILLINGER': ''
        },
        # Add more pages as needed
    }

def regenerate_all_pages():
    """Regenerate all HTML pages from template"""
    print("🔄 Regenerating all Mission Control pages...")
    
    template = load_template()
    configs = get_page_configs()
    
    for filename, config in configs.items():
        filepath = os.path.join(MISSION_CONTROL, filename)
        
        # Backup existing file
        if os.path.exists(filepath):
            backup_path = filepath + '.backup'
            os.rename(filepath, backup_path)
            print(f"  📦 Backed up: {filename}")
        
        # Generate new file
        html = generate_page(template, config)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"  ✅ Generated: {filename}")
    
    print(f"\n✅ All {len(configs)} pages regenerated!")
    print("📋 Backup files created with .backup extension")

def sync_shared_components():
    """Sync shared components across all existing pages"""
    print("\n🔄 Syncing shared components...")
    
    # Files that must be included on every page
    required_scripts = [
        'realtime-collaboration.js',
        'ai-content-suggestions.js',
        'shared-navigation.js',
        'auto-nav.js'
    ]
    
    html_files = [f for f in os.listdir(MISSION_CONTROL) if f.endswith('.html')]
    
    for filename in html_files:
        filepath = os.path.join(MISSION_CONTROL, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for required scripts
        modified = False
        for script in required_scripts:
            if script not in content:
                # Add before closing </head> or </body>
                if '</head>' in content:
                    content = content.replace(
                        '</head>',
                        f'    <script src="{script}" defer></script>\n</head>'
                    )
                    modified = True
                    print(f"  ➕ Added {script} to {filename}")
        
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
    
    print(f"  ✅ Synced {len(html_files)} files")

def verify_consistency():
    """Verify all pages have consistent elements"""
    print("\n🔍 Verifying consistency...")
    
    html_files = [f for f in os.listdir(MISSION_CONTROL) if f.endswith('.html')]
    
    checks = {
        'Mission Control v3.1': 0,
        'realtime-collaboration.js': 0,
        'ai-content-suggestions.js': 0,
        'active-project-widget': 0
    }
    
    for filename in html_files:
        filepath = os.path.join(MISSION_CONTROL, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for check in checks:
            if check in content:
                checks[check] += 1
    
    print("  Consistency Report:")
    for check, count in checks.items():
        status = "✅" if count == len(html_files) else "⚠️"
        print(f"    {status} {check}: {count}/{len(html_files)} pages")
    
    return all(count == len(html_files) for count in checks.values())

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Mission Control HTML Generator")
    print("=" * 60)
    
    # Regenerate all pages
    regenerate_all_pages()
    
    # Sync shared components
    sync_shared_components()
    
    # Verify consistency
    is_consistent = verify_consistency()
    
    print("\n" + "=" * 60)
    if is_consistent:
        print("✅ ALL PAGES ARE CONSISTENT!")
    else:
        print("⚠️  SOME PAGES NEED ATTENTION")
    print("=" * 60)
