// PWA Registration and Install Handler
// Manages service worker registration and install prompt

class PWAManager {
    constructor() {
        this.deferredPrompt = null;
        this.isInstalled = false;
        this.isOnline = navigator.onLine;
    }

    // Initialize PWA
    init() {
        console.log('📱 Initializing PWA...');
        
        this.registerServiceWorker();
        this.setupInstallPrompt();
        this.setupNetworkStatus();
        this.createInstallButton();
    }

    // Register service worker
    registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/service-worker.js')
                .then((registration) => {
                    console.log('[PWA] Service Worker registered:', registration.scope);
                    
                    // Check for updates
                    registration.addEventListener('updatefound', () => {
                        const newWorker = registration.installing;
                        newWorker.addEventListener('statechange', () => {
                            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                                // New version available
                                this.showUpdateNotification();
                            }
                        });
                    });
                })
                .catch((error) => {
                    console.error('[PWA] Service Worker registration failed:', error);
                });
            
            // Listen for messages from service worker
            navigator.serviceWorker.addEventListener('message', (event) => {
                if (event.data === 'update-available') {
                    this.showUpdateNotification();
                }
            });
        } else {
            console.log('[PWA] Service Worker not supported');
        }
    }

    // Setup install prompt
    setupInstallPrompt() {
        window.addEventListener('beforeinstallprompt', (event) => {
            // Prevent default install prompt
            event.preventDefault();
            
            // Store the event for later use
            this.deferredPrompt = event;
            
            // Show install button
            this.showInstallButton();
            
            console.log('[PWA] Install prompt available');
        });

        // Check if already installed
        window.addEventListener('appinstalled', () => {
            console.log('[PWA] App installed');
            this.isInstalled = true;
            this.hideInstallButton();
            this.deferredPrompt = null;
        });

        // Check display mode
        if (window.matchMedia('(display-mode: standalone)').matches) {
            this.isInstalled = true;
            console.log('[PWA] Running in standalone mode');
        }
    }

    // Setup network status monitoring
    setupNetworkStatus() {
        window.addEventListener('online', () => {
            console.log('[PWA] Back online');
            this.isOnline = true;
            this.hideOfflineIndicator();
            this.syncData();
        });

        window.addEventListener('offline', () => {
            console.log('[PWA] Gone offline');
            this.isOnline = false;
            this.showOfflineIndicator();
        });
    }

    // Create install button
    createInstallButton() {
        const button = document.createElement('button');
        button.id = 'pwa-install-btn';
        button.className = 'pwa-install-btn';
        button.innerHTML = '<i class="fas fa-download"></i> Installer App';
        button.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            z-index: 1000;
            display: none;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            transition: transform 0.2s, box-shadow 0.2s;
        `;
        
        button.addEventListener('click', () => this.installApp());
        button.addEventListener('mouseenter', () => {
            button.style.transform = 'translateY(-2px)';
            button.style.boxShadow = '0 6px 16px rgba(102, 126, 234, 0.5)';
        });
        button.addEventListener('mouseleave', () => {
            button.style.transform = 'translateY(0)';
            button.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.4)';
        });
        
        document.body.appendChild(button);
    }

    // Show install button
    showInstallButton() {
        const button = document.getElementById('pwa-install-btn');
        if (button && !this.isInstalled) {
            button.style.display = 'flex';
        }
    }

    // Hide install button
    hideInstallButton() {
        const button = document.getElementById('pwa-install-btn');
        if (button) {
            button.style.display = 'none';
        }
    }

    // Install app
    async installApp() {
        if (!this.deferredPrompt) return;
        
        // Show install prompt
        this.deferredPrompt.prompt();
        
        // Wait for user choice
        const { outcome } = await this.deferredPrompt.userChoice;
        
        if (outcome === 'accepted') {
            console.log('[PWA] User accepted install');
            this.hideInstallButton();
        } else {
            console.log('[PWA] User dismissed install');
        }
        
        // Clear deferred prompt
        this.deferredPrompt = null;
    }

    // Show offline indicator
    showOfflineIndicator() {
        let indicator = document.getElementById('offline-indicator');
        
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'offline-indicator';
            indicator.innerHTML = '<i class="fas fa-wifi-slash"></i> Du er offline';
            indicator.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: #ef4444;
                color: white;
                text-align: center;
                padding: 12px;
                z-index: 10000;
                font-weight: 600;
            `;
            document.body.appendChild(indicator);
        }
        
        indicator.style.display = 'block';
    }

    // Hide offline indicator
    hideOfflineIndicator() {
        const indicator = document.getElementById('offline-indicator');
        if (indicator) {
            indicator.style.display = 'none';
        }
    }

    // Show update notification
    showUpdateNotification() {
        const notification = document.createElement('div');
        notification.className = 'pwa-update-notification';
        notification.innerHTML = `
            <span>🔄 Ny versjon tilgjengelig!</span>
            <button onclick="pwaManager.updateApp()">Oppdater nå</button>
        `;
        notification.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(30, 41, 59, 0.98);
            border: 1px solid rgba(102, 126, 234, 0.5);
            border-radius: 12px;
            padding: 16px 20px;
            display: flex;
            align-items: center;
            gap: 16px;
            z-index: 10000;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        `;
        
        document.body.appendChild(notification);
    }

    // Update app
    updateApp() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.ready.then((registration) => {
                registration.waiting?.postMessage('skipWaiting');
                window.location.reload();
            });
        }
    }

    // Sync data when back online
    async syncData() {
        if ('serviceWorker' in navigator && 'SyncManager' in window) {
            try {
                const registration = await navigator.serviceWorker.ready;
                await registration.sync.register('sync-saker');
                console.log('[PWA] Background sync registered');
            } catch (error) {
                console.error('[PWA] Background sync failed:', error);
            }
        }
    }

    // Check for updates
    async checkForUpdates() {
        if ('serviceWorker' in navigator) {
            const registration = await navigator.serviceWorker.ready;
            await registration.update();
        }
    }
}

// Initialize when DOM is ready
let pwaManager;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        pwaManager = new PWAManager();
        pwaManager.init();
    });
} else {
    pwaManager = new PWAManager();
    pwaManager.init();
}

// Export
window.PWAManager = PWAManager;
window.pwaManager = pwaManager;
