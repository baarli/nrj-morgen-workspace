// Test Suite for Mission Control
// Provides automated testing for all features

class TestSuite {
    constructor() {
        this.tests = [];
        this.results = [];
        this.isRunning = false;
    }

    // Initialize test suite
    init() {
        console.log('🧪 Initializing Test Suite...');
        this.registerTests();
        this.createTestUI();
    }

    // Register all tests
    registerTests() {
        // Navigation tests
        this.addTest('Navigation', 'Sidebar renders correctly', () => {
            const sidebar = document.querySelector('.sidebar');
            return sidebar !== null;
        });

        this.addTest('Navigation', 'All menu items exist', () => {
            const menuItems = document.querySelectorAll('.nav a');
            return menuItems.length >= 10;
        });

        // Dark mode tests
        this.addTest('Dark Mode', 'Toggle button exists', () => {
            const toggle = document.getElementById('dark-mode-toggle');
            return toggle !== null;
        });

        this.addTest('Dark Mode', 'Theme changes on toggle', () => {
            const before = document.documentElement.getAttribute('data-theme');
            if (window.darkModeManager) {
                window.darkModeManager.toggle();
                const after = document.documentElement.getAttribute('data-theme');
                window.darkModeManager.toggle(); // Reset
                return before !== after;
            }
            return false;
        });

        // PWA tests
        this.addTest('PWA', 'Service worker registered', async () => {
            if ('serviceWorker' in navigator) {
                const registration = await navigator.serviceWorker.ready;
                return registration !== null;
            }
            return false;
        });

        this.addTest('PWA', 'Manifest exists', () => {
            const manifest = document.querySelector('link[rel="manifest"]');
            return manifest !== null;
        });

        // Mobile tests
        this.addTest('Mobile', 'Viewport meta tag exists', () => {
            const viewport = document.querySelector('meta[name="viewport"]');
            return viewport !== null;
        });

        this.addTest('Mobile', 'Touch targets are adequate', () => {
            const buttons = document.querySelectorAll('button, a');
            let allAdequate = true;
            buttons.forEach(btn => {
                const rect = btn.getBoundingClientRect();
                if (rect.width < 44 || rect.height < 44) {
                    allAdequate = false;
                }
            });
            return allAdequate;
        });

        // Security tests
        this.addTest('Security', 'Security manager loaded', () => {
            return typeof window.securityManager !== 'undefined';
        });

        this.addTest('Security', 'Input validation works', () => {
            const input = document.createElement('input');
            input.value = '<script>alert("xss")</script>';
            if (window.securityManager) {
                return !window.securityManager.validateInput(input);
            }
            return false;
        });

        // Analytics tests
        this.addTest('Analytics', 'Analytics manager loaded', () => {
            return typeof window.analytics !== 'undefined';
        });

        // Real-time tests
        this.addTest('Real-time', 'Collaboration manager loaded', () => {
            return typeof window.collaboration !== 'undefined';
        });

        // AI tests
        this.addTest('AI', 'AI suggestions manager loaded', () => {
            return typeof window.aiSuggester !== 'undefined';
        });
    }

    // Add a test
    addTest(category, name, testFn) {
        this.tests.push({
            category,
            name,
            testFn,
            id: `${category}_${name}`.replace(/\s+/g, '_').toLowerCase()
        });
    }

    // Create test UI
    createTestUI() {
        // Check if test panel already exists
        if (document.getElementById('test-panel')) return;

        const panel = document.createElement('div');
        panel.id = 'test-panel';
        panel.innerHTML = `
            <div class="test-panel-header">
                <h3>🧪 Test Suite</h3>
                <button onclick="testSuite.runAllTests()">Kjør alle tester</button>
            </div>
            <div class="test-results" id="test-results"></div>
        `;
        
        panel.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 400px;
            max-height: 500px;
            background: rgba(30, 41, 59, 0.98);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 20px;
            z-index: 10000;
            overflow-y: auto;
            display: none;
        `;

        // Add toggle button
        const toggleBtn = document.createElement('button');
        toggleBtn.id = 'test-toggle-btn';
        toggleBtn.innerHTML = '🧪';
        toggleBtn.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            border: none;
            border-radius: 50%;
            color: white;
            font-size: 20px;
            cursor: pointer;
            z-index: 10001;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
        `;
        
        toggleBtn.addEventListener('click', () => {
            panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
        });

        document.body.appendChild(panel);
        document.body.appendChild(toggleBtn);
    }

    // Run all tests
    async runAllTests() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.results = [];
        
        console.log('🧪 Running all tests...');
        
        const resultsContainer = document.getElementById('test-results');
        resultsContainer.innerHTML = '<p>Kjører tester...</p>';

        for (const test of this.tests) {
            const result = await this.runTest(test);
            this.results.push(result);
        }

        this.displayResults();
        this.isRunning = false;
    }

    // Run single test
    async runTest(test) {
        console.log(`🧪 Testing: ${test.category} - ${test.name}`);
        
        const startTime = performance.now();
        
        try {
            const result = await test.testFn();
            const endTime = performance.now();
            
            return {
                ...test,
                passed: result === true,
                error: result === false ? 'Test returned false' : null,
                duration: endTime - startTime
            };
        } catch (error) {
            const endTime = performance.now();
            
            return {
                ...test,
                passed: false,
                error: error.message,
                duration: endTime - startTime
            };
        }
    }

    // Display test results
    displayResults() {
        const container = document.getElementById('test-results');
        
        const passed = this.results.filter(r => r.passed).length;
        const failed = this.results.filter(r => !r.passed).length;
        const total = this.results.length;
        
        let html = `
            <div class="test-summary">
                <div class="test-stats">
                    <span class="passed">✅ ${passed} passed</span>
                    <span class="failed">❌ ${failed} failed</span>
                    <span class="total">📊 ${total} total</span>
                </div>
                <div class="test-progress">
                    <div class="progress-bar" style="width: ${(passed/total)*100}%"></div>
                </div>
            </div>
        `;

        // Group by category
        const categories = {};
        this.results.forEach(result => {
            if (!categories[result.category]) {
                categories[result.category] = [];
            }
            categories[result.category].push(result);
        });

        // Display by category
        Object.entries(categories).forEach(([category, tests]) => {
            html += `<div class="test-category"><h4>${category}</h4>`;
            
            tests.forEach(test => {
                const icon = test.passed ? '✅' : '❌';
                const duration = test.duration.toFixed(2);
                html += `
                    <div class="test-item ${test.passed ? 'passed' : 'failed'}">
                        <span class="test-icon">${icon}</span>
                        <span class="test-name">${test.name}</span>
                        <span class="test-duration">${duration}ms</span>
                        ${test.error ? `<div class="test-error">${test.error}</div>` : ''}
                    </div>
                `;
            });
            
            html += '</div>';
        });

        container.innerHTML = html;
    }

    // Get test report
    getTestReport() {
        return {
            total: this.results.length,
            passed: this.results.filter(r => r.passed).length,
            failed: this.results.filter(r => !r.passed).length,
            results: this.results,
            timestamp: new Date().toISOString()
        };
    }

    // Export results
    exportResults() {
        const report = this.getTestReport();
        const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `test-report-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
    }
}

// Initialize when DOM is ready
let testSuite;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        testSuite = new TestSuite();
        testSuite.init();
    });
} else {
    testSuite = new TestSuite();
    testSuite.init();
}

// Export
window.TestSuite = TestSuite;
window.testSuite = testSuite;
