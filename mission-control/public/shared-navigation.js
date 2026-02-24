// Shared Navigation Component for Mission Control
// Injects consistent navigation into all pages

const NAV_CONFIG = {
    logo: {
        icon: '🚀',
        title: 'Mission Control'
    },
    items: [
        { href: 'total-control.html', icon: 'fas fa-home', label: 'Oversikt' },
        { href: 'sakslista-pro.html', icon: 'fas fa-list', label: 'Saker' },
        { href: 'analytics.html', icon: 'fas fa-chart-line', label: 'Analyse' },
        { href: 'ai-assistant.html', icon: 'fas fa-robot', label: 'AI Assistant' },
        { href: 'widget-dashboard.html', icon: 'fas fa-th-large', label: 'Widgets' },
        { href: 'podkast-control.html', icon: 'fas fa-podcast', label: 'Podkast' },
        { href: 'podkast-clip-studio.html', icon: 'fas fa-cut', label: 'Clip Studio' },
        { href: 'video-editor.html', icon: 'fas fa-film', label: 'Video Editor' },
        { href: 'thumbnail-generator.html', icon: 'fas fa-image', label: 'Thumbnails' },
        { href: 'clip-analytics.html', icon: 'fas fa-chart-bar', label: 'Clip Analytics' },
        { href: 'cron-control.html', icon: 'fas fa-clock', label: 'Cron' },
        { href: 'agent-control.html', icon: 'fas fa-robot', label: 'Agent' },
        { href: 'notifications.html', icon: 'fas fa-bell', label: 'Varsler' },
        { href: 'system-monitor.html', icon: 'fas fa-heartbeat', label: 'System' },
        { href: 'database-admin.html', icon: 'fas fa-database', label: 'Database' },
        { href: 'git-control.html', icon: 'fas fa-code-branch', label: 'Git' },
        { href: 'api-docs.html', icon: 'fas fa-book', label: 'API Docs' },
        { href: 'innstillinger.html', icon: 'fas fa-cog', label: 'Innstillinger' }
    ]
};

function injectNavigation() {
    // Find or create sidebar
    let sidebar = document.querySelector('.sidebar');
    
    if (!sidebar) {
        // Create sidebar if it doesn't exist
        sidebar = document.createElement('aside');
        sidebar.className = 'sidebar';
        document.body.insertBefore(sidebar, document.body.firstChild);
        
        // Add styles if not present
        if (!document.getElementById('shared-nav-styles')) {
            const styles = document.createElement('style');
            styles.id = 'shared-nav-styles';
            styles.textContent = `
                .sidebar {
                    width: 280px; background: rgba(30, 41, 59, 0.98); padding: 24px;
                    border-right: 1px solid rgba(255,255,255,0.1); position: fixed;
                    height: 100vh; overflow-y: auto; z-index: 100;
                }
                .logo { display: flex; align-items: center; gap: 12px; margin-bottom: 32px; padding-bottom: 24px; border-bottom: 1px solid rgba(255,255,255,0.1); }
                .logo-icon { width: 48px; height: 48px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px; }
                .nav { list-style: none; }
                .nav li { margin-bottom: 4px; }
                .nav a { display: flex; align-items: center; gap: 12px; padding: 10px 14px; border-radius: 8px; color: #94a3b8; text-decoration: none; transition: all 0.2s; font-size: 14px; }
                .nav a:hover, .nav a.active { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
                .nav a i { width: 20px; text-align: center; }
                .main { margin-left: 280px; }
                @media (max-width: 768px) { .sidebar { display: none; } .main { margin-left: 0; } }
            `;
            document.head.appendChild(styles);
        }
    }
    
    // Get current page
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    
    // Build navigation HTML
    const navHTML = `
        <div class="logo">
            <div class="logo-icon">${NAV_CONFIG.logo.icon}</div>
            <div>
                <h1 style="font-size: 18px; margin: 0;">${NAV_CONFIG.logo.title}</h1>
                <p style="font-size: 11px; color: #94a3b8; margin: 4px 0 0 0;">v3.0</p>
            </div>
        </div>
        <ul class="nav">
            ${NAV_CONFIG.items.map(item => {
                const isActive = currentPage === item.href || 
                                (currentPage === '' && item.href === 'total-control.html');
                return `
                    <li>
                        <a href="${item.href}" class="${isActive ? 'active' : ''}">
                            <i class="${item.icon}"></i>
                            ${item.label}
                        </a>
                    </li>
                `;
            }).join('')}
        </ul>
    `;
    
    sidebar.innerHTML = navHTML;
}

// Auto-inject on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectNavigation);
} else {
    injectNavigation();
}
