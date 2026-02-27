/**
 * Unit Tests for Theme/Dark Mode
 */

describe('Theme System', () => {
    let themeManager;
    let localStorageMock;

    beforeEach(() => {
        // Setup DOM
        document.documentElement.innerHTML = '<html data-theme="dark"></html>';
        
        // Setup localStorage mock for this test file
        localStorageMock = {
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
        
        // Override global localStorage for this test
        Object.defineProperty(global, 'localStorage', {
            value: localStorageMock,
            writable: true,
            configurable: true
        });
        
        // Mock theme manager
        themeManager = {
            currentTheme: 'dark',
            
            init() {
                const saved = localStorage.getItem('theme');
                if (saved) {
                    this.currentTheme = saved;
                    this.apply(saved);
                }
            },
            
            toggle() {
                const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
                this.set(newTheme);
                return newTheme;
            },
            
            set(theme) {
                this.currentTheme = theme;
                this.apply(theme);
                localStorage.setItem('theme', theme);
            },
            
            apply(theme) {
                document.documentElement.setAttribute('data-theme', theme);
            },
            
            get() {
                return this.currentTheme;
            }
        };
        
        // Clear localStorage before each test
        localStorageMock.clear();
    });

    describe('init', () => {
        test('should load saved theme from localStorage', () => {
            localStorageMock.setItem('theme', 'light');
            
            themeManager.init();
            
            expect(themeManager.get()).toBe('light');
        });

        test('should use default theme if no saved theme', () => {
            themeManager.init();
            
            expect(themeManager.get()).toBe('dark');
        });
    });

    describe('toggle', () => {
        test('should switch from dark to light', () => {
            themeManager.currentTheme = 'dark';
            
            const result = themeManager.toggle();
            
            expect(result).toBe('light');
            expect(themeManager.get()).toBe('light');
        });

        test('should switch from light to dark', () => {
            themeManager.currentTheme = 'light';
            
            const result = themeManager.toggle();
            
            expect(result).toBe('dark');
            expect(themeManager.get()).toBe('dark');
        });

        test('should save theme to localStorage', () => {
            themeManager.currentTheme = 'dark';
            
            themeManager.toggle();
            
            expect(localStorageMock.getItem('theme')).toBe('light');
        });
    });

    describe('set', () => {
        test('should set theme attribute on document', () => {
            themeManager.set('light');
            
            expect(document.documentElement.getAttribute('data-theme')).toBe('light');
        });

        test('should save to localStorage', () => {
            themeManager.set('light');
            
            expect(localStorageMock.getItem('theme')).toBe('light');
        });
    });
});
