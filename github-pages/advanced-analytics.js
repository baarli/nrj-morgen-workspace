// Advanced Analytics Dashboard for Mission Control
// Provides comprehensive analytics, trends and predictions

class AdvancedAnalytics {
    constructor() {
        this.charts = {};
        this.data = {};
        this.timeRange = '7d';
        this.refreshInterval = null;
    }

    init() {
        console.log('📊 Initializing Advanced Analytics...');
        this.loadData();
        this.renderDashboard();
        this.startAutoRefresh();
    }

    // Load data from APIs
    async loadData() {
        try {
            // Load sakslista data
            const saksResponse = await fetch('/api/saker/stats');
            this.data.saker = await saksResponse.json();
            
            // Load system metrics
            const metricsResponse = await fetch('/api/system/metrics');
            this.data.metrics = await metricsResponse.json();
            
            // Load cron job stats
            const cronResponse = await fetch('/api/cron/stats');
            this.data.cron = await cronResponse.json();
            
            this.updateCharts();
        } catch (error) {
            console.error('Error loading analytics data:', error);
            this.loadDemoData();
        }
    }

    // Load demo data if APIs fail
    loadDemoData() {
        this.data = {
            saker: {
                total: 156,
                byCategory: {
                    'Reality TV': 45,
                    'Kjendis': 38,
                    'Film & TV': 32,
                    'Musikk': 25,
                    'Internasjonalt': 16
                },
                byDay: this.generateDailyData(30)
            },
            metrics: {
                cpu: this.generateTimeSeriesData(24, 20, 80),
                memory: this.generateTimeSeriesData(24, 40, 90),
                disk: this.generateTimeSeriesData(24, 30, 70)
            },
            cron: {
                total: 23,
                success: 198,
                failed: 12,
                byHour: this.generateHourlyData()
            }
        };
    }

    // Generate daily data
    generateDailyData(days) {
        const data = {};
        for (let i = 0; i < days; i++) {
            const date = new Date();
            date.setDate(date.getDate() - i);
            data[date.toISOString().split('T')[0]] = Math.floor(Math.random() * 20) + 5;
        }
        return data;
    }

    // Generate time series data
    generateTimeSeriesData(points, min, max) {
        return Array.from({length: points}, () => 
            Math.floor(Math.random() * (max - min)) + min
        );
    }

    // Generate hourly data
    generateHourlyData() {
        return Array.from({length: 24}, () => Math.floor(Math.random() * 10));
    }

    // Render dashboard
    renderDashboard() {
        const container = document.getElementById('analytics-dashboard');
        if (!container) return;

        container.innerHTML = `
            <div class="analytics-header">
                <h2>📊 Advanced Analytics</h2>
                <div class="time-range-selector">
                    <button onclick="analytics.setTimeRange('24h')" class="${this.timeRange === '24h' ? 'active' : ''}">24t</button>
                    <button onclick="analytics.setTimeRange('7d')" class="${this.timeRange === '7d' ? 'active' : ''}">7d</button>
                    <button onclick="analytics.setTimeRange('30d')" class="${this.timeRange === '30d' ? 'active' : ''}">30d</button>
                </div>
            </div>
            
            <div class="analytics-grid">
                <div class="analytics-card">
                    <h3>Saker per Kategori</h3>
                    <canvas id="chart-categories"></canvas>
                </div>
                
                <div class="analytics-card">
                    <h3>Saker over Tid</h3>
                    <canvas id="chart-timeline"></canvas>
                </div>
                
                <div class="analytics-card">
                    <h3>System Metrics</h3>
                    <canvas id="chart-metrics"></canvas>
                </div>
                
                <div class="analytics-card">
                    <h3>Cron Job Success Rate</h3>
                    <div class="success-rate">
                        <div class="rate-circle">
                            <span class="rate-value">${this.calculateSuccessRate()}%</span>
                            <span class="rate-label">Success Rate</span>
                        </div>
                    </div>
                </div>
                
                <div class="analytics-card wide">
                    <h3>Prediksjoner</h3>
                    <div class="predictions">
                        <div class="prediction-item">
                            <span class="prediction-label">Forventede saker i morgen:</span>
                            <span class="prediction-value">${this.predictTomorrowSaker()}</span>
                        </div>
                        <div class="prediction-item">
                            <span class="prediction-label">Trend (7 dager):</span>
                            <span class="prediction-value ${this.getTrend() >= 0 ? 'positive' : 'negative'}">
                                ${this.getTrend() >= 0 ? '↑' : '↓'} ${Math.abs(this.getTrend()).toFixed(1)}%
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="analytics-actions">
                <button onclick="analytics.exportData('csv')" class="btn btn-primary">
                    <i class="fas fa-download"></i> Eksporter CSV
                </button>
                <button onclick="analytics.exportData('pdf')" class="btn btn-secondary">
                    <i class="fas fa-file-pdf"></i> Eksporter PDF
                </button>
                <button onclick="analytics.refreshData()" class="btn">
                    <i class="fas fa-sync"></i> Oppdater
                </button>
            </div>
        `;

        this.initCharts();
    }

    // Initialize Chart.js charts
    initCharts() {
        // Categories pie chart
        const ctxCategories = document.getElementById('chart-categories');
        if (ctxCategories) {
            this.charts.categories = new Chart(ctxCategories, {
                type: 'doughnut',
                data: {
                    labels: Object.keys(this.data.saker?.byCategory || {}),
                    datasets: [{
                        data: Object.values(this.data.saker?.byCategory || {}),
                        backgroundColor: [
                            '#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'bottom' }
                    }
                }
            });
        }

        // Timeline line chart
        const ctxTimeline = document.getElementById('chart-timeline');
        if (ctxTimeline) {
            const days = Object.keys(this.data.saker?.byDay || {}).slice(-7);
            const values = days.map(d => this.data.saker.byDay[d]);
            
            this.charts.timeline = new Chart(ctxTimeline, {
                type: 'line',
                data: {
                    labels: days.map(d => d.slice(5)),
                    datasets: [{
                        label: 'Saker',
                        data: values,
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }

        // Metrics chart
        const ctxMetrics = document.getElementById('chart-metrics');
        if (ctxMetrics) {
            this.charts.metrics = new Chart(ctxMetrics, {
                type: 'line',
                data: {
                    labels: Array.from({length: 24}, (_, i) => `${i}:00`),
                    datasets: [
                        {
                            label: 'CPU %',
                            data: this.data.metrics?.cpu || [],
                            borderColor: '#667eea',
                            tension: 0.4
                        },
                        {
                            label: 'Memory %',
                            data: this.data.metrics?.memory || [],
                            borderColor: '#f093fb',
                            tension: 0.4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true, max: 100 }
                    }
                }
            });
        }
    }

    // Update charts with new data
    updateCharts() {
        Object.values(this.charts).forEach(chart => chart.destroy());
        this.initCharts();
    }

    // Calculate success rate
    calculateSuccessRate() {
        const total = (this.data.cron?.success || 0) + (this.data.cron?.failed || 0);
        if (total === 0) return 0;
        return Math.round((this.data.cron.success / total) * 100);
    }

    // Predict tomorrow's saker count
    predictTomorrowSaker() {
        const values = Object.values(this.data.saker?.byDay || {});
        if (values.length === 0) return 0;
        
        const avg = values.reduce((a, b) => a + b, 0) / values.length;
        const trend = this.getTrend();
        
        return Math.round(avg * (1 + trend / 100));
    }

    // Calculate trend percentage
    getTrend() {
        const values = Object.values(this.data.saker?.byDay || {});
        if (values.length < 7) return 0;
        
        const recent = values.slice(-7).reduce((a, b) => a + b, 0) / 7;
        const previous = values.slice(-14, -7).reduce((a, b) => a + b, 0) / 7;
        
        if (previous === 0) return 0;
        return ((recent - previous) / previous) * 100;
    }

    // Set time range
    setTimeRange(range) {
        this.timeRange = range;
        this.loadData();
        this.renderDashboard();
    }

    // Export data
    exportData(format) {
        const data = {
            timestamp: new Date().toISOString(),
            saker: this.data.saker,
            metrics: this.data.metrics,
            cron: this.data.cron
        };

        if (format === 'csv') {
            this.downloadCSV(data);
        } else if (format === 'pdf') {
            this.downloadPDF(data);
        }
    }

    // Download as CSV
    downloadCSV(data) {
        let csv = 'Category,Count\n';
        Object.entries(data.saker.byCategory).forEach(([cat, count]) => {
            csv += `${cat},${count}\n`;
        });

        const blob = new Blob([csv], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `analytics-${new Date().toISOString().split('T')[0]}.csv`;
        a.click();
    }

    // Download as PDF (simplified)
    downloadPDF(data) {
        alert('PDF export would generate a report with all charts and data');
    }

    // Refresh data
    refreshData() {
        this.loadData();
        this.renderDashboard();
    }

    // Start auto refresh
    startAutoRefresh() {
        this.refreshInterval = setInterval(() => {
            this.loadData();
            this.updateCharts();
        }, 30000); // Every 30 seconds
    }

    // Stop auto refresh
    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }
    }
}

// Initialize when DOM is ready
let analytics;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        analytics = new AdvancedAnalytics();
        analytics.init();
    });
} else {
    analytics = new AdvancedAnalytics();
    analytics.init();
}

// Export
window.AdvancedAnalytics = AdvancedAnalytics;
window.analytics = analytics;
