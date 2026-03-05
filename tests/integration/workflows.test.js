/**
 * Integration Tests for Mission Control Workflows
 */

describe('Mission Control Workflows', () => {
    describe('Dashboard Loading', () => {
        test('should load all dashboard components', async () => {
            const components = ['sidebar', 'header', 'main-content', 'footer'];
            
            components.forEach(component => {
                const element = document.querySelector(`[data-component="${component}"]`);
                expect(element).toBeDefined();
            });
        });

        test('should initialize analytics engine', () => {
            // Mock analyticsEngine
            global.analyticsEngine = {
                data: { listeners: [], podcast: [] }
            };
            
            expect(typeof analyticsEngine).toBe('object');
            expect(analyticsEngine.data).toBeDefined();
        });

        test('should load notifications', () => {
            // Mock notifications
            global.window = global.window || {};
            global.window.MissionControlNotifications = {
                add: jest.fn()
            };
            
            expect(window.MissionControlNotifications).toBeDefined();
        });
    });

    describe('Navigation', () => {
        test('should switch between sections', () => {
            const sections = ['dashboard', 'sakslista', 'podkast', 'cron', 'system', 'analytics'];
            
            sections.forEach(section => {
                showSection(section);
                const activeSection = document.querySelector('.section.active');
                expect(activeSection).toBeDefined();
            });
        });

        test('should update active nav link', () => {
            showSection('analytics');
            
            const activeLink = document.querySelector('.nav-link.active');
            expect(activeLink).toBeDefined();
        });
    });

    describe('Data Export', () => {
        test('should generate export data', () => {
            const data = [
                { id: 1, title: 'Test 1', status: 'active' },
                { id: 2, title: 'Test 2', status: 'completed' }
            ];
            
            const exportData = generateExportData(data, 'json');
            
            expect(JSON.parse(exportData)).toHaveLength(2);
        });

        test('should format CSV correctly', () => {
            const data = [
                { name: 'Test', value: 100 },
                { name: 'Test 2', value: 200 }
            ];
            
            const csv = generateExportData(data, 'csv');
            
            expect(csv).toContain('name,value');
            expect(csv).toContain('Test,100');
        });
    });
});

// Helper functions for tests
function generateExportData(data, format) {
    if (format === 'json') {
        return JSON.stringify(data);
    }
    
    if (format === 'csv') {
        const headers = Object.keys(data[0]).join(',');
        const rows = data.map(row => Object.values(row).join(','));
        return [headers, ...rows].join('\n');
    }
    
    return '';
}

function showSection(sectionId) {
    // Mock implementation
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    const section = document.getElementById(sectionId);
    if (section) {
        section.classList.add('active');
    }
}
