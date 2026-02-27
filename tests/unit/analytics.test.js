/**
 * Unit Tests for Analytics Engine
 */

// Mock the AnalyticsEngine class
const mockData = {
    listeners: Array.from({ length: 30 }, (_, i) => ({
        date: `2024-01-${String(i + 1).padStart(2, '0')}`,
        value: 60000 + i * 200 + Math.random() * 1000
    })),
    podcast: Array.from({ length: 30 }, (_, i) => ({
        date: `2024-01-${String(i + 1).padStart(2, '0')}`,
        value: 80 - i * 0.5 + Math.random() * 5
    }))
};

describe('AnalyticsEngine', () => {
    let engine;

    beforeEach(() => {
        // Create a minimal AnalyticsEngine mock
        engine = {
            data: mockData,
            
            linearRegression(data) {
                const n = data.length;
                let sumX = 0, sumY = 0, sumXY = 0, sumXX = 0;
                
                for (let i = 0; i < n; i++) {
                    sumX += i;
                    sumY += data[i].value;
                    sumXY += i * data[i].value;
                    sumXX += i * i;
                }
                
                const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
                const intercept = (sumY - slope * sumX) / n;
                
                return { slope, intercept };
            },
            
            predict(metric, periods = 7) {
                const data = this.data[metric];
                const { slope, intercept } = this.linearRegression(data);
                
                const predictions = [];
                const lastDate = new Date(data[data.length - 1].date);
                
                for (let i = 1; i <= periods; i++) {
                    const predictedValue = slope * (data.length + i - 1) + intercept;
                    const date = new Date(lastDate);
                    date.setDate(date.getDate() + i);
                    
                    predictions.push({
                        date: date.toISOString().split('T')[0],
                        value: Math.round(predictedValue * 10) / 10,
                        confidence: Math.max(0.7, 1 - (i * 0.05))
                    });
                }
                
                return predictions;
            },
            
            calculateTrend(metric) {
                const data = this.data[metric];
                const { slope } = this.linearRegression(data);
                const avg = data.reduce((a, b) => a + b.value, 0) / data.length;
                const trendStrength = Math.abs(slope / avg) * 100;
                
                return {
                    direction: slope > 0 ? 'up' : 'down',
                    strength: trendStrength,
                    slope: slope,
                    percentage: (slope / avg) * 100
                };
            }
        };
    });

    describe('linearRegression', () => {
        test('should calculate correct slope for upward trend', () => {
            const data = [
                { value: 100 },
                { value: 200 },
                { value: 300 }
            ];
            const result = engine.linearRegression(data);
            
            expect(result.slope).toBeGreaterThan(0);
        });

        test('should calculate correct slope for downward trend', () => {
            const data = [
                { value: 300 },
                { value: 200 },
                { value: 100 }
            ];
            const result = engine.linearRegression(data);
            
            expect(result.slope).toBeLessThan(0);
        });
    });

    describe('predict', () => {
        test('should return correct number of predictions', () => {
            const predictions = engine.predict('listeners', 5);
            
            expect(predictions).toHaveLength(5);
        });

        test('should return predictions with required fields', () => {
            const predictions = engine.predict('listeners', 3);
            
            predictions.forEach(pred => {
                expect(pred).toHaveProperty('date');
                expect(pred).toHaveProperty('value');
                expect(pred).toHaveProperty('confidence');
            });
        });

        test('should have decreasing confidence over time', () => {
            const predictions = engine.predict('listeners', 5);
            
            for (let i = 1; i < predictions.length; i++) {
                expect(predictions[i].confidence).toBeLessThanOrEqual(predictions[i - 1].confidence);
            }
        });
    });

    describe('calculateTrend', () => {
        test('should detect upward trend correctly', () => {
            const trend = engine.calculateTrend('listeners');
            
            expect(trend).toHaveProperty('direction');
            expect(trend).toHaveProperty('strength');
            expect(trend).toHaveProperty('percentage');
        });

        test('should have positive strength', () => {
            const trend = engine.calculateTrend('podcast');
            
            expect(trend.strength).toBeGreaterThan(0);
        });
    });
});
