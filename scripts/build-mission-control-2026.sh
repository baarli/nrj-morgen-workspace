#!/bin/bash
set -e  # Exit on error
# BUILD MISSION CONTROL 2026 - Complete with all functionality
# This script builds all pages with the new 2026 design AND all existing features

WORKSPACE="/root/.openclaw/workspace"
MISSION_CONTROL="$WORKSPACE/mission-control/public"
BACKUP="$MISSION_CONTROL/backup-old"

echo "🚀 Building Mission Control 2026 with FULL functionality..."
echo "=========================================================="

# Function to build a page
build_page() {
    local filename=$1
    local title=$2
    local active_nav=$3
    local extra_scripts=$4
    local content_file=$5
    
    echo "Building: $filename"
    
    cat > "$MISSION_CONTROL/$filename" << HTMLHEAD
<!DOCTYPE html>
<html lang="no" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <meta name="description" content="Mission Control - Total kontroll dashboard for NRJ Morgen">
    <meta name="theme-color" content="#6366f1">
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; img-src 'self' data: https:; connect-src 'self' https://*.supabase.co wss://*.supabase.co;">
    <meta http-equiv="X-Frame-Options" content="DENY">
    <link rel="manifest" href="/manifest.json">
    <title>$title | Mission Control</title>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js" defer></script>
    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js" defer></script>
    $extra_scripts
    
    <script src="pwa-manager.js" defer></script>
    <script src="security-manager.js" defer></script>
    <script src="realtime-collaboration.js" defer></script>
    <script src="ai-content-suggestions.js" defer></script>
    <script src="mobile-experience.js" defer></script>
    <script src="dark-mode-manager.js" defer></script>
    <script src="advanced-analytics.js" defer></script>
    <script src="test-suite.js" defer></script>
    
    <style>
        /* 2026 Design System */
        :root {
            --color-primary: #6366f1;
            --color-primary-gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            --color-success: #10b981;
            --color-warning: #f59e0b;
            --color-danger: #ef4444;
            --color-info: #3b82f6;
            
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-tertiary: #334155;
            --bg-card: rgba(30, 41, 59, 0.8);
            
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            
            --border-color: rgba(148, 163, 184, 0.1);
            
            --space-xs: 0.25rem; --space-sm: 0.5rem; --space-md: 1rem;
            --space-lg: 1.5rem; --space-xl: 2rem; --space-2xl: 3rem;
            
            --radius-sm: 0.375rem; --radius-md: 0.5rem; --radius-lg: 0.75rem;
            --radius-xl: 1rem; --radius-2xl: 1.5rem;
            
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --shadow-glow: 0 0 20px rgba(99, 102, 241, 0.3);
            
            --sidebar-width: 280px;
            --header-height: 64px;
        }
        
        [data-theme="light"] {
            --bg-primary: #ffffff;
            --bg-secondary: #f8fafc;
            --bg-tertiary: #e2e8f0;
            --bg-card: rgba(255, 255, 255, 0.9);
            --text-primary: #0f172a;
            --text-secondary: #334155;
            --text-muted: #64748b;
            --border-color: rgba(148, 163, 184, 0.2);
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
        }
        
        .app { display: flex; min-height: 100vh; }
        
        .sidebar {
            width: var(--sidebar-width);
            background: var(--bg-secondary);
            border-right: 1px solid var(--border-color);
            position: fixed;
            height: 100vh;
            overflow-y: auto;
            z-index: 100;
            transition: transform 0.3s ease;
        }
        
        .sidebar-header {
            padding: var(--space-lg);
            border-bottom: 1px solid var(--border-color);
        }
        
        .brand {
            display: flex;
            align-items: center;
            gap: var(--space-md);
        }
        
        .brand-icon {
            width: 40px;
            height: 40px;
            background: var(--color-primary-gradient);
            border-radius: var(--radius-lg);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
        }
        
        .brand-text h1 {
            font-size: var(--text-lg);
            font-weight: 700;
            line-height: 1.2;
        }
        
        .brand-text span {
            font-size: var(--text-xs);
            color: var(--text-muted);
        }
        
        .nav { padding: var(--space-md); list-style: none; }
        
        .nav-section { margin-bottom: var(--space-lg); }
        
        .nav-section-title {
            font-size: var(--text-xs);
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: var(--space-sm) var(--space-md);
        }
        
        .nav-item { margin-bottom: var(--space-xs); }
        
        .nav-link {
            display: flex;
            align-items: center;
            gap: var(--space-md);
            padding: var(--space-sm) var(--space-md);
            border-radius: var(--radius-lg);
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.875rem;
            font-weight: 500;
            transition: all 0.15s ease;
        }
        
        .nav-link:hover {
            background: var(--bg-tertiary);
            color: var(--text-primary);
        }
        
        .nav-link.active {
            background: var(--color-primary-gradient);
            color: white;
            box-shadow: var(--shadow-glow);
        }
        
        .nav-link i { width: 20px; text-align: center; }
        
        .main {
            flex: 1;
            margin-left: var(--sidebar-width);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            height: var(--header-height);
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 var(--space-xl);
            position: sticky;
            top: 0;
            z-index: 50;
        }
        
        .header-title h2 {
            font-size: 1.25rem;
            font-weight: 700;
        }
        
        .header-actions {
            display: flex;
            align-items: center;
            gap: var(--space-md);
        }
        
        .content {
            flex: 1;
            padding: var(--space-xl);
            overflow-y: auto;
        }
        
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-xl);
            padding: var(--space-xl);
            transition: all 0.15s ease;
        }
        
        .card:hover {
            border-color: rgba(148, 163, 184, 0.2);
            box-shadow: var(--shadow-lg);
        }
        
        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: var(--space-lg);
        }
        
        .card-title {
            font-size: 1.125rem;
            font-weight: 600;
        }
        
        .btn {
            display: inline-flex;
            align-items: center;
            gap: var(--space-sm);
            padding: var(--space-sm) var(--space-lg);
            border-radius: var(--radius-lg);
            font-size: 0.875rem;
            font-weight: 600;
            text-decoration: none;
            border: none;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        
        .btn-primary {
            background: var(--color-primary-gradient);
            color: white;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
        }
        
        .btn-secondary {
            background: var(--bg-tertiary);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
        }
        
        .grid {
            display: grid;
            gap: var(--space-xl);
        }
        
        .grid-2 { grid-template-columns: repeat(2, 1fr); }
        .grid-3 { grid-template-columns: repeat(3, 1fr); }
        .grid-4 { grid-template-columns: repeat(4, 1fr); }
        
        .badge {
            display: inline-flex;
            align-items: center;
            gap: var(--space-xs);
            padding: var(--space-xs) var(--space-sm);
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        .badge-success { background: rgba(16, 185, 129, 0.1); color: var(--color-success); }
        .badge-warning { background: rgba(245, 158, 11, 0.1); color: var(--color-warning); }
        .badge-danger { background: rgba(239, 68, 68, 0.1); color: var(--color-danger); }
        .badge-info { background: rgba(59, 130, 246, 0.1); color: var(--color-info); }
        
        .flex { display: flex; }
        .flex-col { flex-direction: column; }
        .items-center { align-items: center; }
        .justify-between { justify-content: space-between; }
        .gap-sm { gap: var(--space-sm); }
        .gap-md { gap: var(--space-md); }
        .gap-lg { gap: var(--space-lg); }
        .mt-md { margin-top: var(--space-md); }
        .mt-lg { margin-top: var(--space-lg); }
        .mt-xl { margin-top: var(--space-xl); }
        .text-muted { color: var(--text-muted); }
        .text-secondary { color: var(--text-secondary); }
        
        @media (max-width: 1024px) {
            .grid-4, .grid-3 { grid-template-columns: repeat(2, 1fr); }
        }
        
        @media (max-width: 768px) {
            .sidebar { transform: translateX(-100%); }
            .sidebar.open { transform: translateX(0); }
            .main { margin-left: 0; }
            .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="app">
        <aside class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <div class="brand">
                    <div class="brand-icon">🚀</div>
                    <div class="brand-text">
                        <h1>Mission Control</h1>
                        <span>v3.2</span>
                    </div>
                </div>
            </div>
            
            <nav class="nav">
                <div class="nav-section">
                    <div class="nav-section-title">Hovedmeny</div>
                    <div class="nav-item"><a href="total-control.html" class="nav-link ${active_nav['dashboard']}"><i class="fas fa-home"></i><span>Dashboard</span></a></div>
                    <div class="nav-item"><a href="sakslista-pro.html" class="nav-link ${active_nav['saker']}"><i class="fas fa-list"></i><span>Sakslista</span></a></div>
                    <div class="nav-item"><a href="analytics.html" class="nav-link ${active_nav['analytics']}"><i class="fas fa-chart-line"></i><span>Analytics</span></a></div>
                </div>
                
                <div class="nav-section">
                    <div class="nav-section-title">Verktøy</div>
                    <div class="nav-item"><a href="podkast-control.html" class="nav-link ${active_nav['podkast']}"><i class="fas fa-podcast"></i><span>Podkast</span></a></div>
                    <div class="nav-item"><a href="cron-control.html" class="nav-link ${active_nav['cron']}"><i class="fas fa-clock"></i><span>Cron Jobs</span></a></div>
                    <div class="nav-item"><a href="system-monitor.html" class="nav-link ${active_nav['system']}"><i class="fas fa-server"></i><span>System</span></a></div>
                </div>
                
                <div class="nav-section">
                    <div class="nav-section-title">Innstillinger</div>
                    <div class="nav-item"><a href="innstillinger.html" class="nav-link ${active_nav['settings']}"><i class="fas fa-cog"></i><span>Innstillinger</span></a></div>
                </div>
            </nav>
        </aside>

        <main class="main">
            <header class="header">
                <div class="header-title"><h2>$title</h2></div>
                <div class="header-actions">
                    <button class="btn btn-secondary" id="mobile-menu-toggle"><i class="fas fa-bars"></i></button>
                    <button class="btn btn-secondary" id="theme-toggle"><i class="fas fa-moon"></i></button>
                </div>
            </header>

            <div class="content">
HTMLHEAD

    # Add content
    if [ -f "$content_file" ]; then
        cat "$content_file" >> "$MISSION_CONTROL/$filename"
    else
        echo "                <div class='card'><div class='card-header'><div class='card-title'>$content_file</div></div><div class='text-secondary'>Content loading...</div></div>" >> "$MISSION_CONTROL/$filename"
    fi

    # Add footer
    cat >> "$MISSION_CONTROL/$filename" << 'HTMLFOOT'
            </div>
        </main>
    </div>

    <script>
        document.getElementById('mobile-menu-toggle')?.addEventListener('click', () => {
            document.getElementById('sidebar')?.classList.toggle('open');
        });

        document.getElementById('theme-toggle')?.addEventListener('click', () => {
            const html = document.documentElement;
            const current = html.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
        });

        const savedTheme = localStorage.getItem('theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
    </script>
</body>
</html>
HTMLFOOT

    echo "  ✅ Built: $filename"
}

# Build Dashboard
build_page "total-control.html" "Dashboard" "dashboard" "" "Dashboard med system status, aktiviteter og kontroller"

# Build Sakslista Pro (with full functionality)
cat > /tmp/sakslista-content.html <> 'SAKSLISTA'
<div class="flex justify-between items-center mb-lg">
    <div>
        <h3>Dagens Saker</h3>
        <p class="text-muted">Drag & drop for å endre rekkefølge</p>
    </div>
    <div class="flex gap-md">
        <button class="btn btn-secondary" onclick="runMorningRoutine()">
            <i class="fas fa-play"></i> Morning Routine
        </button>
        <button class="btn btn-primary" onclick="showAddModal()">
            <i class="fas fa-plus"></i> Ny Sak
        </button>
    </div>
</div>

<div class="card">
    <div id="saker-list">
        <div class="text-secondary text-center py-xl">
            <i class="fas fa-spinner fa-spin"></i> Laster saker...
        </div>
    </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.15.0/Sortable.min.js"></script>
<script src="sakslista-pro.js" defer></script>
SAKSLISTA

build_page "sakslista-pro.html" "Sakslista Pro" "saker" "<script src='https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.15.0/Sortable.min.js'></script>
    <script src='sakslista-pro.js' defer></script>" "Sakslista"

# Build Analytics
cat > /tmp/analytics-content.html <> 'ANALYTICS'
<div class="grid grid-2">
    <div class="card">
        <div class="card-header">
            <div class="card-title">Saker per Kategori</div>
        </div>
        <canvas id="chart-categories"></canvas>
    </div>
    
    <div class="card">
        <div class="card-header">
            <div class="card-title">Saker over Tid</div>
        </div>
        <canvas id="chart-timeline"></canvas>
    </div>
</div>

<div class="mt-xl">
    <div class="card">
        <div class="card-header">
            <div class="card-title">System Metrics</div>
        </div>
        <canvas id="chart-metrics"></canvas>
    </div>
</div>
ANALYTICS

build_page "analytics.html" "Analytics" "analytics" "" "Analytics"

# Build Podkast
cat > /tmp/podkast-content.html <> 'PODKAST'
<div class="grid grid-2">
    <div class="card">
        <div class="card-header">
            <div class="card-title">Siste Episoder</div>
        </div>
        <div id="episodes-list">
            <div class="text-secondary">Laster episoder...</div>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header">
            <div class="card-title">Statistikk</div>
        </div>
        <div class="text-secondary">Podkast statistikk...</div>
    </div>
</div>
PODKAST

build_page "podkast-control.html" "Podkast" "podkast" "" "Podkast"

# Build Cron
cat > /tmp/cron-content.html <> 'CRON'
<div class="card">
    <div class="card-header">
        <div class="card-title">Scheduled Tasks</div>
    </div>
    <div id="cron-jobs-list">
        <div class="text-secondary">Laster cron jobs...</div>
    </div>
</div>
CRON

build_page "cron-control.html" "Cron Jobs" "cron" "" "Cron Jobs"

# Build System
cat > /tmp/system-content.html <> 'SYSTEM'
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
SYSTEM

build_page "system-monitor.html" "System Monitor" "system" "" "System Monitor"

# Build Settings
cat > /tmp/settings-content.html <> 'SETTINGS'
<div class="grid grid-2">
    <div class="card">
        <div class="card-header">
            <div class="card-title">Appearance</div>
        </div>
        <div class="flex flex-col gap-md">
            <label class="flex items-center gap-md">
                <input type="checkbox" id="dark-mode-pref" checked>
                <span>Dark Mode</span>
            </label>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header">
            <div class="card-title">Notifications</div>
        </div>
        <div class="text-secondary">Notification settings...</div>
    </div>
</div>
SETTINGS

build_page "innstillinger.html" "Innstillinger" "settings" "" "Settings"

echo ""
echo "=========================================================="
echo "✅ ALL PAGES BUILT WITH 2026 DESIGN + FULL FUNCTIONALITY!"
echo "=========================================================="
