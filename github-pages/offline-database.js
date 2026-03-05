// Offline Database Manager
// Handles local data storage with IndexedDB for offline functionality

class OfflineDatabase {
    constructor() {
        this.dbName = 'mission-control-db';
        this.dbVersion = 2;
        this.db = null;
        this.isInitialized = false;
    }

    // Initialize database
    async init() {
        if (this.isInitialized) return;

        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, this.dbVersion);

            request.onerror = () => {
                console.error('[OfflineDB] Failed to open database');
                reject(request.error);
            };

            request.onsuccess = () => {
                this.db = request.result;
                this.isInitialized = true;
                console.log('[OfflineDB] Database initialized');
                resolve(this.db);
            };

            request.onupgradeneeded = (event) => {
                const db = event.target.result;

                // Store for saker
                if (!db.objectStoreNames.contains('saker')) {
                    const sakerStore = db.createObjectStore('saker', { keyPath: 'id' });
                    sakerStore.createIndex('date', 'date', { unique: false });
                    sakerStore.createIndex('category', 'category', { unique: false });
                    sakerStore.createIndex('syncStatus', 'syncStatus', { unique: false });
                }

                // Store for podkast episoder
                if (!db.objectStoreNames.contains('podkast')) {
                    const podkastStore = db.createObjectStore('podkast', { keyPath: 'id' });
                    podkastStore.createIndex('date', 'date', { unique: false });
                    podkastStore.createIndex('syncStatus', 'syncStatus', { unique: false });
                }

                // Store for pending changes (offline queue)
                if (!db.objectStoreNames.contains('pending')) {
                    const pendingStore = db.createObjectStore('pending', { 
                        keyPath: 'id', 
                        autoIncrement: true 
                    });
                    pendingStore.createIndex('timestamp', 'timestamp', { unique: false });
                    pendingStore.createIndex('type', 'type', { unique: false });
                }

                // Store for cache metadata
                if (!db.objectStoreNames.contains('cache-meta')) {
                    const cacheStore = db.createObjectStore('cache-meta', { keyPath: 'key' });
                    cacheStore.createIndex('timestamp', 'timestamp', { unique: false });
                }

                // Store for user settings
                if (!db.objectStoreNames.contains('settings')) {
                    db.createObjectStore('settings', { keyPath: 'key' });
                }

                console.log('[OfflineDB] Database schema upgraded');
            };
        });
    }

    // Generic add/update method
    async put(storeName, data) {
        await this.init();
        
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readwrite');
            const store = transaction.objectStore(storeName);
            const request = store.put(data);

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    // Generic get method
    async get(storeName, key) {
        await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readonly');
            const store = transaction.objectStore(storeName);
            const request = store.get(key);

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    // Generic get all method
    async getAll(storeName) {
        await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readonly');
            const store = transaction.objectStore(storeName);
            const request = store.getAll();

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    // Generic delete method
    async delete(storeName, key) {
        await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readwrite');
            const store = transaction.objectStore(storeName);
            const request = store.delete(key);

            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
    }

    // Get by index
    async getByIndex(storeName, indexName, value) {
        await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readonly');
            const store = transaction.objectStore(storeName);
            const index = store.index(indexName);
            const request = index.getAll(value);

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    // Clear store
    async clear(storeName) {
        await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readwrite');
            const store = transaction.objectStore(storeName);
            const request = store.clear();

            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
    }

    // ===== SAKER SPECIFIC METHODS =====

    // Save saker to local database
    async saveSaker(saker) {
        const data = {
            ...saker,
            syncStatus: navigator.onLine ? 'synced' : 'pending',
            lastModified: Date.now()
        };
        await this.put('saker', data);
        console.log('[OfflineDB] Saker saved:', saker.id);
    }

    // Get all saker
    async getAllSaker() {
        return await this.getAll('saker');
    }

    // Get saker by category
    async getSakerByCategory(category) {
        return await this.getByIndex('saker', 'category', category);
    }

    // Get pending saker
    async getPendingSaker() {
        return await this.getByIndex('saker', 'syncStatus', 'pending');
    }

    // ===== PENDING QUEUE METHODS =====

    // Add to pending queue
    async addToPending(type, data) {
        const item = {
            type,
            data,
            timestamp: Date.now(),
            retryCount: 0
        };
        const id = await this.put('pending', item);
        console.log('[OfflineDB] Added to pending queue:', type, id);
        return id;
    }

    // Get all pending items
    async getPendingItems() {
        return await this.getAll('pending');
    }

    // Remove from pending queue
    async removeFromPending(id) {
        await this.delete('pending', id);
        console.log('[OfflineDB] Removed from pending queue:', id);
    }

    // ===== SETTINGS METHODS =====

    // Save setting
    async saveSetting(key, value) {
        await this.put('settings', { key, value, timestamp: Date.now() });
    }

    // Get setting
    async getSetting(key, defaultValue = null) {
        const result = await this.get('settings', key);
        return result ? result.value : defaultValue;
    }

    // ===== SYNC METHODS =====

    // Sync data with server when online
    async syncWithServer() {
        if (!navigator.onLine) {
            console.log('[OfflineDB] Cannot sync - offline');
            return { success: false, reason: 'offline' };
        }

        const pending = await this.getPendingItems();
        const results = { success: [], failed: [] };

        for (const item of pending) {
            try {
                // Process based on type
                switch (item.type) {
                    case 'create-sak':
                        await this.syncCreateSak(item);
                        break;
                    case 'update-sak':
                        await this.syncUpdateSak(item);
                        break;
                    case 'delete-sak':
                        await this.syncDeleteSak(item);
                        break;
                    default:
                        console.warn('[OfflineDB] Unknown pending type:', item.type);
                }

                await this.removeFromPending(item.id);
                results.success.push(item.id);
            } catch (error) {
                console.error('[OfflineDB] Sync failed for item:', item.id, error);
                results.failed.push({ id: item.id, error: error.message });
            }
        }

        console.log('[OfflineDB] Sync complete:', results);
        return results;
    }

    // Sync create sak
    async syncCreateSak(item) {
        // Implementation depends on your API
        console.log('[OfflineDB] Syncing create sak:', item.data);
    }

    // Sync update sak
    async syncUpdateSak(item) {
        console.log('[OfflineDB] Syncing update sak:', item.data);
    }

    // Sync delete sak
    async syncDeleteSak(item) {
        console.log('[OfflineDB] Syncing delete sak:', item.data);
    }

    // ===== UTILITY METHODS =====

    // Get database stats
    async getStats() {
        await this.init();

        const stats = {
            saker: 0,
            podkast: 0,
            pending: 0,
            settings: 0
        };

        for (const storeName of Object.keys(stats)) {
            const items = await this.getAll(storeName);
            stats[storeName] = items.length;
        }

        return stats;
    }

    // Export all data
    async exportData() {
        const data = {
            saker: await this.getAll('saker'),
            podkast: await this.getAll('podkast'),
            settings: await this.getAll('settings'),
            exportedAt: new Date().toISOString()
        };
        return data;
    }

    // Import data
    async importData(data) {
        if (data.saker) {
            for (const sak of data.saker) {
                await this.put('saker', sak);
            }
        }
        if (data.podkast) {
            for (const episode of data.podkast) {
                await this.put('podkast', episode);
            }
        }
        if (data.settings) {
            for (const setting of data.settings) {
                await this.put('settings', setting);
            }
        }
        console.log('[OfflineDB] Data imported successfully');
    }

    // Clear all data
    async clearAll() {
        await this.clear('saker');
        await this.clear('podkast');
        await this.clear('pending');
        await this.clear('cache-meta');
        console.log('[OfflineDB] All data cleared');
    }
}

// Create global instance
const offlineDB = new OfflineDatabase();

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        offlineDB.init().then(() => {
            console.log('✅ Offline Database ready');
        }).catch(err => {
            console.error('❌ Offline Database failed:', err);
        });
    });
} else {
    offlineDB.init().then(() => {
        console.log('✅ Offline Database ready');
    }).catch(err => {
        console.error('❌ Offline Database failed:', err);
    });
}

// Export
window.OfflineDatabase = OfflineDatabase;
window.offlineDB = offlineDB;
