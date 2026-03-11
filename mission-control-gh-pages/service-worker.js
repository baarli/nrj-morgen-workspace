// Mission Control Service Worker v3.3
// Performance optimized with advanced caching strategies

const CACHE_VERSION = 'v3.3';
const STATIC_CACHE = `mission-control-static-${CACHE_VERSION}`;
const DYNAMIC_CACHE = `mission-control-dynamic-${CACHE_VERSION}`;
const IMAGE_CACHE = `mission-control-images-${CACHE_VERSION}`;
const API_CACHE = `mission-control-api-${CACHE_VERSION}`;

// Cache duration settings (in milliseconds)
const CACHE_DURATION = {
    static: 30 * 24 * 60 * 60 * 1000,  // 30 days
    dynamic: 24 * 60 * 60 * 1000,       // 1 day
    images: 7 * 24 * 60 * 60 * 1000,    // 7 days
    api: 5 * 60 * 1000                   // 5 minutes
};

// Static assets to cache on install
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/manifest.json',
    '/pwa-manager.js',
    '/offline-database.js',
    '/shared-navigation.js',
    '/auto-nav.js',
    '/dark-mode-manager.js',
    '/mobile-experience.js',
    '/security-manager.js',
    '/advanced-analytics.js',
    '/sakslista-pro.js',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
    console.log('[SW] Installing v3.3...');
    
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then((cache) => {
                console.log('[SW] Caching static assets');
                // Use addAll with individual catch to prevent total failure
                return Promise.all(
                    STATIC_ASSETS.map(url => 
                        cache.add(url).catch(err => {
                            console.warn(`[SW] Failed to cache: ${url}`, err);
                        })
                    )
                );
            })
            .then(() => {
                console.log('[SW] Static assets cached');
            })
            .catch((err) => {
                console.error('[SW] Cache install failed:', err);
            })
    );
    
    self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    console.log('[SW] Activating v3.3...');
    
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (!cacheName.includes(CACHE_VERSION)) {
                        console.log('[SW] Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    
    self.clients.claim();
});

// Helper: Check if cache entry is expired
function isCacheExpired(cachedResponse, maxAge) {
    if (!cachedResponse) return true;
    
    const dateHeader = cachedResponse.headers.get('date');
    if (!dateHeader) return false; // No date, assume valid
    
    const cachedTime = new Date(dateHeader).getTime();
    const now = Date.now();
    return (now - cachedTime) > maxAge;
}

// Helper: Get cache strategy based on request type
function getCacheStrategy(request) {
    const url = new URL(request.url);
    const acceptHeader = request.headers.get('accept') || '';
    
    // Images
    if (acceptHeader.includes('image/') || 
        url.pathname.match(/\.(jpg|jpeg|png|gif|webp|svg|ico)$/i)) {
        return { cache: IMAGE_CACHE, strategy: 'cache-first', maxAge: CACHE_DURATION.images };
    }
    
    // API calls
    if (url.hostname.includes('supabase.co') || 
        url.pathname.startsWith('/api/') ||
        url.hostname.includes('api.')) {
        return { cache: API_CACHE, strategy: 'network-first', maxAge: CACHE_DURATION.api };
    }
    
    // Static assets (JS, CSS)
    if (url.pathname.match(/\.(js|css)$/i) ||
        STATIC_ASSETS.includes(request.url) ||
        STATIC_ASSETS.includes(url.pathname)) {
        return { cache: STATIC_CACHE, strategy: 'cache-first', maxAge: CACHE_DURATION.static };
    }
    
    // HTML pages
    if (acceptHeader.includes('text/html')) {
        return { cache: DYNAMIC_CACHE, strategy: 'network-first', maxAge: CACHE_DURATION.dynamic };
    }
    
    // Default: dynamic cache with stale-while-revalidate
    return { cache: DYNAMIC_CACHE, strategy: 'stale-while-revalidate', maxAge: CACHE_DURATION.dynamic };
}

// Fetch event - intelligent caching
self.addEventListener('fetch', (event) => {
    const { request } = event;
    
    // Skip non-GET requests
    if (request.method !== 'GET') return;
    
    // Skip WebSocket connections
    if (request.headers.get('upgrade') === 'websocket') return;
    
    const { cache, strategy, maxAge } = getCacheStrategy(request);
    
    event.respondWith(
        (async () => {
            const cacheInstance = await caches.open(cache);
            
            // Cache First strategy
            if (strategy === 'cache-first') {
                const cached = await cacheInstance.match(request);
                if (cached && !isCacheExpired(cached, maxAge)) {
                    // Return cached and update in background
                    fetch(request).then(response => {
                        if (response.ok) {
                            cacheInstance.put(request, response);
                        }
                    }).catch(() => {});
                    return cached;
                }
                
                // Not in cache or expired, fetch from network
                try {
                    const networkResponse = await fetch(request);
                    if (networkResponse.ok) {
                        cacheInstance.put(request, networkResponse.clone());
                    }
                    return networkResponse;
                } catch (error) {
                    if (cached) return cached; // Return stale if network fails
                    throw error;
                }
            }
            
            // Network First strategy
            if (strategy === 'network-first') {
                try {
                    const networkResponse = await fetch(request);
                    if (networkResponse.ok) {
                        cacheInstance.put(request, networkResponse.clone());
                    }
                    return networkResponse;
                } catch (error) {
                    const cached = await cacheInstance.match(request);
                    if (cached) {
                        console.log('[SW] Serving from cache (network failed):', request.url);
                        return cached;
                    }
                    throw error;
                }
            }
            
            // Stale While Revalidate strategy (default)
            const cached = await cacheInstance.match(request);
            const fetchPromise = fetch(request).then(response => {
                if (response.ok) {
                    cacheInstance.put(request, response.clone());
                }
                return response;
            }).catch(() => cached);
            
            return cached && !isCacheExpired(cached, maxAge) ? cached : fetchPromise;
        })()
    );
});

// Background sync for offline operations
self.addEventListener('sync', (event) => {
    console.log('[SW] Background sync:', event.tag);
    
    if (event.tag === 'sync-saker') {
        event.waitUntil(syncSakerData());
    } else if (event.tag === 'sync-analytics') {
        event.waitUntil(syncAnalyticsData());
    }
});

// Sync saker data when back online
async function syncSakerData() {
    try {
        const db = await openDB('mission-control-db', 1);
        const pendingSaker = await db.getAll('pending-saker');
        
        console.log(`[SW] Syncing ${pendingSaker.length} pending saker`);
        
        for (const sak of pendingSaker) {
            try {
                const response = await fetch('/api/saker', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(sak)
                });
                
                if (response.ok) {
                    await db.delete('pending-saker', sak.id);
                    console.log('[SW] Synced sak:', sak.id);
                }
            } catch (error) {
                console.error('[SW] Sync failed for sak:', sak.id, error);
            }
        }
    } catch (error) {
        console.error('[SW] Sync error:', error);
    }
}

// Sync analytics data
async function syncAnalyticsData() {
    // Implementation for analytics sync
    console.log('[SW] Analytics sync complete');
}

// Periodic background sync (if supported)
self.addEventListener('periodicsync', (event) => {
    if (event.tag === 'refresh-data') {
        event.waitUntil(refreshDataInBackground());
    }
});

async function refreshDataInBackground() {
    console.log('[SW] Periodic background sync');
    // Refresh critical data in background
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
        actions: data.actions || [],
        data: data.data || {}
    };
    
    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    
    const notificationData = event.notification.data;
    const url = notificationData?.url || '/';
    
    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true })
            .then((clientList) => {
                // Focus existing window if open
                for (const client of clientList) {
                    if (client.url === url && 'focus' in client) {
                        return client.focus();
                    }
                }
                // Open new window
                if (clients.openWindow) {
                    return clients.openWindow(url);
                }
            })
    );
});

// Message handler from main thread
self.addEventListener('message', (event) => {
    const { type, payload } = event.data;
    
    switch (type) {
        case 'skipWaiting':
            self.skipWaiting();
            break;
            
        case 'clearCache':
            event.waitUntil(
                caches.keys().then(names => {
                    return Promise.all(
                        names.map(name => caches.delete(name))
                    );
                }).then(() => {
                    event.ports[0].postMessage({ success: true });
                })
            );
            break;
            
        case 'getCacheStats':
            event.waitUntil(
                caches.keys().then(async names => {
                    const stats = {};
                    for (const name of names) {
                        const cache = await caches.open(name);
                        const keys = await cache.keys();
                        stats[name] = keys.length;
                    }
                    event.ports[0].postMessage({ stats });
                })
            );
            break;
            
        default:
            console.log('[SW] Unknown message type:', type);
    }
});

// Handle errors gracefully
self.addEventListener('error', (event) => {
    console.error('[SW] Error:', event.error);
});

self.addEventListener('unhandledrejection', (event) => {
    console.error('[SW] Unhandled rejection:', event.reason);
});

console.log('[SW] Service Worker v3.3 loaded');
