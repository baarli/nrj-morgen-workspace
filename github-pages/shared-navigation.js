// Shared Navigation Component for Mission Control
// Injects consistent navigation into all pages

// Dark Mode Manager
const DarkModeManager = {
    STORAGE_KEY: 'mission-control-dark-mode',
    
    init() {
        // Check saved preference or system preference
        const saved = localStorage.getItem(this.STORAGE_KEY);
        if (saved !== null) {
            this.set(saved === 'true');
        } else {
            this.set(window.matchMedia('(prefers-color-scheme: dark)').matches);
        }
        
        // Listen for system changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
            if (localStorage.getItem(this.STORAGE_KEY) === null) {
                this.set(e.matches);
            }
        });
    },
    
    toggle() {
        const isDark = !document.body.classList.contains('dark-mode');
        this.set(isDark);
        localStorage.setItem(this.STORAGE_KEY, isDark);
    },
    
    set(isDark) {
        if (isDark) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
        this.updateToggleIcon();
    },
    
    updateToggleIcon() {
        const btn = document.getElementById('dark-mode-toggle');
        if (btn) {
            const isDark = document.body.classList.contains('dark-mode');
            btn.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
            btn.title = isDark ? 'Bytt til lys modus' : 'Bytt til mørk modus';
        }
    }
};

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
    // Initialize dark mode first
    DarkModeManager.init();
    
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
                .dark-mode-toggle { position: fixed; top: 20px; right: 20px; width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; color: white; font-size: 18px; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4); transition: all 0.3s ease; z-index: 1000; }
                .dark-mode-toggle:hover { transform: scale(1.1); box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6); }
                .main { margin-left: 280px; }
                @media (max-width: 768px) { .sidebar { display: none; } .main { margin-left: 0; } .dark-mode-toggle { top: 10px; right: 10px; width: 40px; height: 40px; } }
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
    
    // Add dark mode toggle button
    const toggleBtn = document.createElement('button');
    toggleBtn.id = 'dark-mode-toggle';
    toggleBtn.className = 'dark-mode-toggle';
    toggleBtn.onclick = () => DarkModeManager.toggle();
    document.body.appendChild(toggleBtn);
    DarkModeManager.updateToggleIcon();
}

// Auto-inject on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectNavigation);
} else {
    injectNavigation();
}
