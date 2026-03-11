// Dark Mode Manager for Mission Control
// Provides enhanced dark mode with toggle and preferences

class DarkModeManager {
    constructor() {
        this.isDarkMode = this.getStoredPreference() ?? true;
        this.systemPreference = window.matchMedia('(prefers-color-scheme: dark)');
    }

    // Initialize dark mode
    init() {
        console.log('🌙 Initializing Dark Mode Manager...');
        
        this.applyTheme();
        this.createToggleButton();
        this.listenToSystemChanges();
        this.enhanceContrast();
    }

    // Get stored preference
    getStoredPreference() {
        const stored = localStorage.getItem('darkMode');
        return stored === null ? null : stored === 'true';
    }

    // Store preference
    storePreference(isDark) {
        localStorage.setItem('darkMode', isDark);
    }

    // Apply theme
    applyTheme() {
        if (this.isDarkMode) {
            document.documentElement.setAttribute('data-theme', 'dark');
            document.body.classList.add('dark-mode');
            document.body.classList.remove('light-mode');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            document.body.classList.add('light-mode');
            document.body.classList.remove('dark-mode');
        }
        
        this.updateToggleButton();
    }

    // Toggle dark mode
    toggle() {
        this.isDarkMode = !this.isDarkMode;
        this.applyTheme();
        this.storePreference(this.isDarkMode);
        
        // Dispatch event for other components
        window.dispatchEvent(new CustomEvent('themeChanged', {
            detail: { isDarkMode: this.isDarkMode }
        }));
    }

    // Create toggle button
    createToggleButton() {
        // Check if button already exists
        if (document.getElementById('dark-mode-toggle')) return;

        const button = document.createElement('button');
        button.id = 'dark-mode-toggle';
        button.className = 'dark-mode-toggle';
        button.setAttribute('aria-label', 'Toggle dark mode');
        button.innerHTML = `
            <span class="toggle-icon">${this.isDarkMode ? '🌙' : '☀️'}</span>
            <span class="toggle-text">${this.isDarkMode ? 'Dark' : 'Light'}</span>
        `;
        
        button.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: ${this.isDarkMode ? 'rgba(102, 126, 234, 0.2)' : 'rgba(255, 255, 255, 0.9)'};
            border: 2px solid ${this.isDarkMode ? '#667eea' : '#e2e8f0'};
            border-radius: 50px;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        `;

        button.addEventListener('click', () => this.toggle());
        
        // Hover effects
        button.addEventListener('mouseenter', () => {
            button.style.transform = 'scale(1.05)';
            button.style.boxShadow = '0 6px 20px rgba(0,0,0,0.15)';
        });
        
        button.addEventListener('mouseleave', () => {
            button.style.transform = 'scale(1)';
            button.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
        });

        document.body.appendChild(button);
    }

    // Update toggle button appearance
    updateToggleButton() {
        const button = document.getElementById('dark-mode-toggle');
        if (!button) return;

        const icon = button.querySelector('.toggle-icon');
        const text = button.querySelector('.toggle-text');

        if (icon) icon.textContent = this.isDarkMode ? '🌙' : '☀️';
        if (text) text.textContent = this.isDarkMode ? 'Dark' : 'Light';

        button.style.background = this.isDarkMode 
            ? 'rgba(102, 126, 234, 0.2)' 
            : 'rgba(255, 255, 255, 0.9)';
        button.style.borderColor = this.isDarkMode ? '#667eea' : '#e2e8f0';
        button.style.color = this.isDarkMode ? '#e2e8f0' : '#1e293b';
    }

    // Listen to system preference changes
    listenToSystemChanges() {
        this.systemPreference.addEventListener('change', (e) => {
            // Only auto-switch if user hasn't set a preference
            if (localStorage.getItem('darkMode') === null) {
                this.isDarkMode = e.matches;
                this.applyTheme();
            }
        });
    }

    // Enhance contrast for better accessibility
    enhanceContrast() {
        // Add CSS for better contrast
        const css = `
            /* Enhanced Dark Mode Contrast */
            [data-theme="dark"] {
                --text-primary: #f8fafc;
                --text-secondary: #e2e8f0;
                --text-muted: #94a3b8;
                --bg-primary: #0f172a;
                --bg-secondary: #1e293b;
                --bg-tertiary: #334155;
                --border-color: rgba(255,255,255,0.15);
                --accent-primary: #667eea;
                --accent-secondary: #764ba2;
            }

            [data-theme="light"] {
                --text-primary: #0f172a;
                --text-secondary: #1e293b;
                --text-muted: #64748b;
                --bg-primary: #ffffff;
                --bg-secondary: #f8fafc;
                --bg-tertiary: #e2e8f0;
                --border-color: rgba(0,0,0,0.1);
                --accent-primary: #667eea;
                --accent-secondary: #764ba2;
            }

            /* Apply variables */
            body {
                color: var(--text-primary);
                background: var(--bg-primary);
                transition: color 0.3s ease, background 0.3s ease;
            }

            /* Enhanced contrast for cards */
            .card, .system-card, .sak-item, .analytics-card {
                background: var(--bg-secondary);
                border: 1px solid var(--border-color);
            }

            /* Better text contrast */
            h1, h2, h3, h4 {
                color: var(--text-primary);
            }

            p, span, div {
                color: var(--text-secondary);
            }

            .text-muted {
                color: var(--text-muted);
            }

            /* Enhanced buttons */
            .btn {
                background: var(--accent-primary);
                color: white;
                transition: all 0.3s ease;
            }

            .btn:hover {
                background: var(--accent-secondary);
                transform: translateY(-2px);
            }

            /* Form elements */
            input, select, textarea {
                background: var(--bg-tertiary);
                border: 1px solid var(--border-color);
                color: var(--text-primary);
            }

            input:focus, select:focus, textarea:focus {
                border-color: var(--accent-primary);
                outline: none;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
            }

            /* Sidebar */
            .sidebar {
                background: var(--bg-secondary);
                border-right: 1px solid var(--border-color);
            }

            /* Navigation */
            .nav a {
                color: var(--text-muted);
            }

            .nav a:hover, .nav a.active {
                background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
                color: white;
            }

            /* Smooth transitions */
            * {
                transition: background-color 0.3s ease, 
                            border-color 0.3s ease, 
                            color 0.3s ease;
            }
        `;

        const style = document.createElement('style');
        style.textContent = css;
        document.head.appendChild(style);
    }

    // Get current theme
    getCurrentTheme() {
        return this.isDarkMode ? 'dark' : 'light';
    }

    // Set specific theme
    setTheme(theme) {
        this.isDarkMode = theme === 'dark';
        this.applyTheme();
        this.storePreference(this.isDarkMode);
    }

    // Reset to system preference
    resetToSystem() {
        localStorage.removeItem('darkMode');
        this.isDarkMode = this.systemPreference.matches;
        this.applyTheme();
    }
}

// Initialize when DOM is ready
let darkModeManager;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        darkModeManager = new DarkModeManager();
        darkModeManager.init();
    });
} else {
    darkModeManager = new DarkModeManager();
    darkModeManager.init();
}

// Export
window.DarkModeManager = DarkModeManager;
window.darkModeManager = darkModeManager;
