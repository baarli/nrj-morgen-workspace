import { test, expect } from '@playwright/test';

/**
 * E2E Tests for Mission Control
 */

test.describe('Mission Control E2E', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('https://creative-muffin-dcf3a0.netlify.app');
    });

    test('should load dashboard', async ({ page }) => {
        await expect(page).toHaveTitle(/Mission Control/);
        
        // Check main elements
        await expect(page.locator('.sidebar')).toBeVisible();
        await expect(page.locator('.header')).toBeVisible();
        await expect(page.locator('.main')).toBeVisible();
    });

    test('should navigate to analytics section', async ({ page }) => {
        // Click analytics nav link
        await page.click('text=Analytics');
        
        // Check analytics section is visible
        await expect(page.locator('#analytics')).toBeVisible();
        
        // Check analytics cards
        await expect(page.locator('.analytics-card')).toHaveCount(4);
    });

    test('should toggle theme', async ({ page }) => {
        // Get initial theme
        const initialTheme = await page.getAttribute('html', 'data-theme');
        
        // Click theme toggle
        await page.click('[data-theme-toggle]');
        
        // Check theme changed
        const newTheme = await page.getAttribute('html', 'data-theme');
        expect(newTheme).not.toBe(initialTheme);
    });

    test('should show notifications', async ({ page }) => {
        // Click notification button
        await page.click('.notification-btn');
        
        // Check dropdown is visible
        await expect(page.locator('.notification-dropdown')).toBeVisible();
    });

    test('should search', async ({ page }) => {
        // Click search button
        await page.click('.search-btn');
        
        // Type in search
        await page.fill('.search-input', 'test');
        
        // Check search results appear
        await expect(page.locator('.search-results')).toBeVisible();
    });

    test('should generate analytics report', async ({ page }) => {
        // Navigate to analytics
        await page.click('text=Analytics');
        
        // Click generate report button
        await page.click('text=Generer Rapport');
        
        // Wait for download
        const download = await page.waitForEvent('download');
        expect(download.suggestedFilename()).toContain('analytics-report');
    });
});
