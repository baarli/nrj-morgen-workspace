// Mission Control Service Worker
// Provides offline functionality and caching

const CACHE_NAME = 'mission-control-v3.1';
const STATIC_CACHE = 'mission-control-static-v3.1';
const DYNAMIC_CACHE = 'mission-control-dynamic-v3.1';

// Static assets to cache on install
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/total-control.html',
    '/sakslista-pro.html',
    '/analytics.html',
    '/ai-assistant.html',
    '/widget-dashboard.html',
    '/podkast-control.html',
    '/cron-control.html',
    '/agent-control.html',
    '/notifications.html',
    '/system-monitor.html',
    '/database-admin.html',
    '/git-control.html',
    '/api-docs.html',
    '/innstillinger.html',
    '/offline.html',
    '/manifest.json',
    '/pwa-manager.js',
    '/shared-navigation.js',
    '/auto-nav.js',
    '/realtime-collaboration.js',
    '/ai-content-suggestions.js',
    '/advanced-analytics.js',
    '/sakslista-pro.js',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
    'https://cdn.jsdelivr.net/npm/chart.js'
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
    console.log('[SW] Installing...');
    
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then((cache) => {
                console.log('[SW] Caching static assets');
                return cache.addAll(STATIC_ASSETS);
            })
            .catch((err) => {
                console.error('[SW] Cache failed:', err);
            })
    );
    
    // Activate immediately
    self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    console.log('[SW] Activating...');
    
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
                        console.log('[SW] Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    
    // Take control of all clients
    self.clients.claim();
});

// Fetch event - serve from cache or network
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Skip non-GET requests
    if (request.method !== 'GET') return;
    
    // Skip Supabase API calls
    if (url.hostname.includes('supabase.co')) return;
    
    // Skip WebSocket connections
    if (request.headers.get('upgrade') === 'websocket') return;
    
    event.respondWith(
        caches.match(request)
            .then((cachedResponse) => {
                // Return cached version if available
                if (cachedResponse) {
                    // Fetch update in background
                    fetch(request)
                        .then((networkResponse) => {
                            if (networkResponse.ok) {
                                caches.open(DYNAMIC_CACHE)
                                    .then((cache) => {
                                        cache.put(request, networkResponse);
                                    });
                            }
                        })
                        .catch(() => {
                            // Network failed, but we have cached version
                        });
                    
                    return cachedResponse;
                }
                
                // Not in cache, fetch from network
                return fetch(request)
                    .then((networkResponse) => {
                        if (!networkResponse.ok) {
                            throw new Error('Network response not ok');
                        }
                        
                        // Clone response before caching
                        const responseToCache = networkResponse.clone();
                        
                        caches.open(DYNAMIC_CACHE)
                            .then((cache) => {
                                cache.put(request, responseToCache);
                            });
                        
                        return networkResponse;
                    })
                    .catch((error) => {
                        console.error('[SW] Fetch failed:', error);
                        
                        // Return offline page for HTML requests
                        if (request.headers.get('accept').includes('text/html')) {
                            return caches.match('/offline.html');
                        }
                        
                        throw error;
                    });
            })
    );
});

// Background sync for offline form submissions
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-saker') {
        event.waitUntil(syncSakerData());
    }
});

// Sync saker data when back online
async function syncSakerData() {
    try {
        const db = await openDB('mission-control-db', 1);
        const pendingSaker = await db.getAll('pending-saker');
        
        for (const sak of pendingSaker) {
            try {
                const response = await fetch('/api/saker', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(sak)
                });
                
                if (response.ok) {
                    await db.delete('pending-saker', sak.id);
                }
            } catch (error) {
                console.error('[SW] Sync failed for sak:', sak.id, error);
            }
        }
    } catch (error) {
        console.error('[SW] Sync error:', error);
    }
}

// Push notification support
self.addEventListener('push', (event) => {
    if (!event.data) return;
    
    const data = event.data.json();
    const options = {
        body: data.body,
        icon: '/icons/icon-192x192.png',
        badge: '/icons/badge-72x72.png',
        tag: data.tag || 'mission-control',
        requireInteraction: data.requireInteraction || false,
        actions: data.actions || []
    };
    
    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    
    event.waitUntil(
        clients.matchAll({ type: 'window' })
            .then((clientList) => {
                if (clientList.length > 0) {
                    clientList[0].focus();
                } else {
                    clients.openWindow('/');
                }
            })
    );
});

// Message handler from main thread
self.addEventListener('message', (event) => {
    if (event.data === 'skipWaiting') {
        self.skipWaiting();
    }
});
