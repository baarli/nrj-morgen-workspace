/**
 * Test Setup File
 * Runs before each test file
 */

// Mock localStorage
global.localStorage = {
    store: {},
    getItem(key) {
        return this.store[key] || null;
    },
    setItem(key, value) {
        this.store[key] = value;
    },
    removeItem(key) {
        delete this.store[key];
    },
    clear() {
        this.store = {};
    }
};

// Mock sessionStorage
global.sessionStorage = {
    store: {},
    getItem(key) {
        return this.store[key] || null;
    },
    setItem(key, value) {
        this.store[key] = value;
    },
    removeItem(key) {
        delete this.store[key];
    },
    clear() {
        this.store = {};
    }
};

// Mock fetch
global.fetch = jest.fn(() =>
    Promise.resolve({
        ok: true,
        json: () => Promise.resolve({}),
        text: () => Promise.resolve(''),
        blob: () => Promise.resolve(new Blob())
    })
);

// Mock Chart.js
global.Chart = jest.fn(() => ({
    destroy: jest.fn(),
    update: jest.fn(),
    data: { datasets: [] }
}));

// Mock performance API if not available
if (!global.performance) {
    global.performance = {
        now: () => Date.now(),
        mark: () => {},
        measure: () => {},
        getEntriesByName: () => [],
        memory: {
            usedJSHeapSize: 0,
            totalJSHeapSize: 0,
            jsHeapSizeLimit: 0
        }
    };
}

// Reset mocks before each test
beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
    sessionStorage.clear();
});

// Suppress console errors during tests (optional)
// global.console.error = jest.fn();
// global.console.warn = jest.fn();
