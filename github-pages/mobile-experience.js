// Mobile Experience Manager for Mission Control
// Optimizes UI for mobile devices with touch-friendly interactions

class MobileExperience {
    constructor() {
        this.isMobile = window.innerWidth <= 768;
        this.isTouch = 'ontouchstart' in window;
        this.touchStartY = 0;
        this.touchEndY = 0;
    }

    // Initialize mobile experience
    init() {
        console.log('📱 Initializing Mobile Experience...');
        
        this.setupViewport();
        this.setupTouchTargets();
        this.setupMobileNavigation();
        this.setupSwipeGestures();
        this.setupPullToRefresh();
        this.optimizeForTouch();
        
        // Listen for resize
        window.addEventListener('resize', () => {
            this.isMobile = window.innerWidth <= 768;
            this.handleResize();
        });
    }

    // Setup viewport meta tag
    setupViewport() {
        let viewport = document.querySelector('meta[name="viewport"]');
        if (!viewport) {
            viewport = document.createElement('meta');
            viewport.name = 'viewport';
            document.head.appendChild(viewport);
        }
        viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes';
    }

    // Ensure all touch targets are at least 44px
    setupTouchTargets() {
        const touchElements = document.querySelectorAll('button, a, input, select, textarea, [role="button"]');
        
        touchElements.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.width < 44 || rect.height < 44) {
                el.style.minWidth = '44px';
                el.style.minHeight = '44px';
                el.style.padding = '12px';
            }
        });
    }

    // Setup mobile navigation
    setupMobileNavigation() {
        // Create mobile menu button if it doesn't exist
        if (!document.getElementById('mobile-menu-btn')) {
            const menuBtn = document.createElement('button');
            menuBtn.id = 'mobile-menu-btn';
            menuBtn.innerHTML = '<i class="fas fa-bars"></i>';
            menuBtn.setAttribute('aria-label', 'Åpne meny');
            menuBtn.style.cssText = `
                position: fixed;
                top: 16px;
                left: 16px;
                z-index: 1001;
                width: 48px;
                height: 48px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                border-radius: 12px;
                color: white;
                font-size: 20px;
                cursor: pointer;
                display: none;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            `;
            
            menuBtn.addEventListener('click', () => this.toggleMobileMenu());
            document.body.appendChild(menuBtn);
        }

        // Show menu button on mobile
        this.updateMenuButtonVisibility();

        // Create mobile overlay
        if (!document.getElementById('mobile-overlay')) {
            const overlay = document.createElement('div');
            overlay.id = 'mobile-overlay';
            overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.5);
                z-index: 99;
                display: none;
                opacity: 0;
                transition: opacity 0.3s;
            `;
            overlay.addEventListener('click', () => this.closeMobileMenu());
            document.body.appendChild(overlay);
        }

        // Make sidebar mobile-friendly
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.style.transition = 'transform 0.3s ease';
        }
    }

    // Toggle mobile menu
    toggleMobileMenu() {
        const sidebar = document.querySelector('.sidebar');
        const overlay = document.getElementById('mobile-overlay');
        
        if (sidebar.classList.contains('mobile-open')) {
            this.closeMobileMenu();
        } else {
            sidebar.classList.add('mobile-open');
            sidebar.style.transform = 'translateX(0)';
            overlay.style.display = 'block';
            setTimeout(() => overlay.style.opacity = '1', 10);
            document.body.style.overflow = 'hidden';
        }
    }

    // Close mobile menu
    closeMobileMenu() {
        const sidebar = document.querySelector('.sidebar');
        const overlay = document.getElementById('mobile-overlay');
        
        sidebar.classList.remove('mobile-open');
        sidebar.style.transform = 'translateX(-100%)';
        overlay.style.opacity = '0';
        setTimeout(() => {
            overlay.style.display = 'none';
            document.body.style.overflow = '';
        }, 300);
    }

    // Update menu button visibility
    updateMenuButtonVisibility() {
        const menuBtn = document.getElementById('mobile-menu-btn');
        if (menuBtn) {
            menuBtn.style.display = this.isMobile ? 'flex' : 'none';
        }
    }

    // Setup swipe gestures
    setupSwipeGestures() {
        let touchStartX = 0;
        let touchEndX = 0;

        document.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
            this.touchStartY = e.changedTouches[0].screenY;
        }, { passive: true });

        document.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            this.touchEndY = e.changedTouches[0].screenY;
            this.handleSwipe(touchStartX, touchEndX);
        }, { passive: true });
    }

    // Handle swipe gestures
    handleSwipe(startX, endX) {
        const swipeThreshold = 100;
        const diff = endX - startX;

        // Swipe right from edge opens menu
        if (diff > swipeThreshold && startX < 50) {
            this.toggleMobileMenu();
        }
        
        // Swipe left closes menu
        if (diff < -swipeThreshold) {
            this.closeMobileMenu();
        }
    }

    // Setup pull-to-refresh
    setupPullToRefresh() {
        let isPulling = false;
        let pullStartY = 0;
        const pullThreshold = 100;

        document.addEventListener('touchstart', (e) => {
            if (window.scrollY === 0) {
                isPulling = true;
                pullStartY = e.touches[0].clientY;
            }
        }, { passive: true });

        document.addEventListener('touchmove', (e) => {
            if (!isPulling) return;
            
            const pullDistance = e.touches[0].clientY - pullStartY;
            
            if (pullDistance > 0 && pullDistance < pullThreshold) {
                // Visual feedback could be added here
            }
            
            if (pullDistance > pullThreshold) {
                isPulling = false;
                this.refreshPage();
            }
        }, { passive: true });

        document.addEventListener('touchend', () => {
            isPulling = false;
        }, { passive: true });
    }

    // Refresh page
    refreshPage() {
        location.reload();
    }

    // Optimize for touch
    optimizeForTouch() {
        // Remove hover effects on touch devices
        if (this.isTouch) {
            document.body.classList.add('touch-device');
            
            const style = document.createElement('style');
            style.textContent = `
                .touch-device *:hover {
                    transform: none !important;
                }
                .touch-device button:active,
                .touch-device a:active {
                    opacity: 0.7;
                }
            `;
            document.head.appendChild(style);
        }

        // Prevent zoom on double tap
        let lastTouchEnd = 0;
        document.addEventListener('touchend', (e) => {
            const now = Date.now();
            if (now - lastTouchEnd <= 300) {
                e.preventDefault();
            }
            lastTouchEnd = now;
        }, { passive: false });
    }

    // Handle resize
    handleResize() {
        this.updateMenuButtonVisibility();
        
        if (!this.isMobile) {
            this.closeMobileMenu();
            // Reset sidebar
            const sidebar = document.querySelector('.sidebar');
            if (sidebar) {
                sidebar.style.transform = '';
            }
        }
    }

    // Add mobile-specific CSS
    addMobileCSS() {
        const css = `
            @media (max-width: 768px) {
                .sidebar {
                    position: fixed;
                    left: 0;
                    top: 0;
                    transform: translateX(-100%);
                    z-index: 100;
                    width: 280px;
                    height: 100vh;
                }
                
                .main {
                    margin-left: 0 !important;
                    padding: 80px 16px 16px !important;
                }
                
                .systems-grid {
                    grid-template-columns: 1fr !important;
                }
                
                .quick-actions {
                    grid-template-columns: repeat(2, 1fr) !important;
                }
                
                .header {
                    flex-direction: column;
                    gap: 16px;
                }
                
                .header h2 {
                    font-size: 24px;
                }
                
                .sak-item {
                    flex-direction: column;
                    align-items: flex-start !important;
                }
                
                .sak-actions {
                    width: 100%;
                    justify-content: flex-start;
                    margin-top: 12px;
                }
                
                .analytics-grid {
                    grid-template-columns: 1fr !important;
                }
                
                .modal {
                    width: 95% !important;
                    max-height: 90vh;
                }
                
                input, select, textarea {
                    font-size: 16px !important; /* Prevents zoom on iOS */
                }
            }
            
            @media (max-width: 480px) {
                .quick-actions {
                    grid-template-columns: 1fr !important;
                }
                
                .btn {
                    width: 100%;
                    justify-content: center;
                }
            }
        `;
        
        const style = document.createElement('style');
        style.textContent = css;
        document.head.appendChild(style);
    }
}

// Initialize when DOM is ready
let mobileExperience;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        mobileExperience = new MobileExperience();
        mobileExperience.init();
        mobileExperience.addMobileCSS();
    });
} else {
    mobileExperience = new MobileExperience();
    mobileExperience.init();
    mobileExperience.addMobileCSS();
}

// Export
window.MobileExperience = MobileExperience;
window.mobileExperience = mobileExperience;
