// Auto-inject consistent navigation into all pages
(function() {
    'use strict';
    
    // Wait for DOM to be ready
    function init() {
        // Only run if sidebar doesn't already have our nav
        const existingNav = document.querySelector('.nav');
        if (existingNav && existingNav.querySelector('a[href="ai-assistant.html"]')) {
            return; // Navigation already updated
        }
        
        const currentPage = window.location.pathname.split('/').pop() || 'total-control.html';
        
        const navItems = [
            { href: 'total-control.html', icon: 'fas fa-home', label: 'Oversikt' },
            { href: 'sakslista-pro.html', icon: 'fas fa-list', label: 'Saker' },
            { href: 'analytics.html', icon: 'fas fa-chart-line', label: 'Analyse' },
            { href: 'ai-assistant.html', icon: 'fas fa-robot', label: 'AI Assistant' },
            { href: 'widget-dashboard.html', icon: 'fas fa-th-large', label: 'Widgets' },
            { href: 'podkast-control.html', icon: 'fas fa-podcast', label: 'Podkast' },
            { href: 'cron-control.html', icon: 'fas fa-clock', label: 'Cron' },
            { href: 'agent-control.html', icon: 'fas fa-robot', label: 'Agent' },
            { href: 'notifications.html', icon: 'fas fa-bell', label: 'Varsler' },
            { href: 'system-monitor.html', icon: 'fas fa-heartbeat', label: 'System' },
            { href: 'database-admin.html', icon: 'fas fa-database', label: 'Database' },
            { href: 'git-control.html', icon: 'fas fa-code-branch', label: 'Git' },
            { href: 'api-docs.html', icon: 'fas fa-book', label: 'API Docs' },
            { href: 'innstillinger.html', icon: 'fas fa-cog', label: 'Innstillinger' }
        ];
        
        // Find sidebar
        let sidebar = document.querySelector('.sidebar');
        if (!sidebar) return;
        
        // Build nav HTML
        const navHTML = `
            <div class="logo">
                <div class="logo-icon">🚀</div>
                <div>
                    <h1 style="font-size: 18px; margin: 0;">Mission Control</h1>
                    <p style="font-size: 11px; color: #94a3b8; margin: 4px 0 0 0;">v3.0</p>
                </div>
            </div>
            <ul class="nav">
                ${navItems.map(item => {
                    const isActive = currentPage === item.href || 
                                    (currentPage === '' && item.href === 'total-control.html') ||
                                    (currentPage === 'index.html' && item.href === 'total-control.html');
                    return `
                        <li>
                            <a href="${item.href}" class="${isActive ? 'active' : ''}">
                                <i class="${item.icon}"></i> ${item.label}
                            </a>
                        </li>
                    `;
                }).join('')}
            </ul>
        `;
        
        // Replace sidebar content
        sidebar.innerHTML = navHTML;
        
        // Adjust main content margin
        const main = document.querySelector('.main, .content, [class*="main"]');
        if (main) {
            main.style.marginLeft = '280px';
        }
    }
    
    // Run immediately if DOM is ready, otherwise wait
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();