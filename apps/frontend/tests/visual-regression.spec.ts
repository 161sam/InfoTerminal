import { test, expect, Page } from '@playwright/test';

/**
 * Visual Regression Tests for InfoTerminal Design System
 * 
 * Tests all components across different themes, states, and viewports
 * to ensure consistent visual appearance and detect regressions.
 */

const VIEWPORTS = [
  { name: 'mobile', width: 375, height: 667 },
  { name: 'tablet', width: 768, height: 1024 },  
  { name: 'desktop', width: 1440, height: 900 },
] as const;

const THEMES = ['light', 'dark'] as const;

// Component test URLs (assuming we have a showcase/storybook page)
const COMPONENT_ROUTES = {
  showcase: '/components/showcase',
  tabs: '/components/showcase?section=tabs',
  loading: '/components/showcase?section=loading',
  layouts: '/components/showcase?section=layouts',
  darkMode: '/components/showcase?section=dark-mode',
} as const;

test.describe('Visual Regression Tests', () => {
  
  // Tab Component Visual Tests
  test.describe('Tab Components', () => {
    for (const theme of THEMES) {
      for (const viewport of VIEWPORTS) {
        test(`tab-components-${theme}-${viewport.name}`, async ({ page }) => {
          await page.setViewportSize(viewport);
          await setTheme(page, theme);
          
          await page.goto(COMPONENT_ROUTES.showcase);
          
          // Navigate to components tab
          await page.click('[data-testid="tab-components"]');
          await page.waitForLoadState('networkidle');
          
          // Test all tab variants
          const tabVariants = [
            'default-tabs',
            'underline-tabs', 
            'pills-tabs',
            'card-tabs'
          ];
          
          for (const variant of tabVariants) {
            await page.locator(`[data-testid="${variant}"]`).scrollIntoViewIfNeeded();
            await expect(page.locator(`[data-testid="${variant}"]`)).toHaveScreenshot(
              `${variant}-${theme}-${viewport.name}.png`
            );
          }
        });
      }
    }
  });

  // Loading States Visual Tests
  test.describe('Loading States', () => {
    for (const theme of THEMES) {
      test(`loading-states-${theme}`, async ({ page }) => {
        await page.setViewportSize(VIEWPORTS[2]); // Desktop
        await setTheme(page, theme);
        
        await page.goto(COMPONENT_ROUTES.loading);
        await page.waitForLoadState('networkidle');
        
        // Test loading spinner variants
        const loadingVariants = [
          'spinner-inline',
          'spinner-block',
          'spinner-card',
          'skeleton-basic',
          'skeleton-table',
          'skeleton-graph',
          'error-state',
          'empty-state'
        ];
        
        for (const variant of loadingVariants) {
          const element = page.locator(`[data-testid="${variant}"]`);
          await element.scrollIntoViewIfNeeded();
          await expect(element).toHaveScreenshot(`${variant}-${theme}.png`);
        }
      });
    }
  });

  // Layout Component Visual Tests  
  test.describe('Layout Components', () => {
    for (const theme of THEMES) {
      for (const viewport of VIEWPORTS) {
        test(`layouts-${theme}-${viewport.name}`, async ({ page }) => {
          await page.setViewportSize(viewport);
          await setTheme(page, theme);
          
          await page.goto(COMPONENT_ROUTES.layouts);
          await page.waitForLoadState('networkidle');
          
          // Test layout variations
          const layouts = [
            'page-layout-basic',
            'page-layout-with-breadcrumbs',
            'tabbed-page-layout',
            'dashboard-layout',
            'panel-component'
          ];
          
          for (const layout of layouts) {
            const element = page.locator(`[data-testid="${layout}"]`);
            await element.scrollIntoViewIfNeeded();
            await expect(element).toHaveScreenshot(`${layout}-${theme}-${viewport.name}.png`);
          }
        });
      }
    }
  });

  // Mobile Navigation Visual Tests
  test.describe('Mobile Navigation', () => {
    test('mobile-navigation-states', async ({ page }) => {
      await page.setViewportSize(VIEWPORTS[0]); // Mobile
      
      for (const theme of THEMES) {
        await setTheme(page, theme);
        await page.goto('/');
        
        // Test mobile header
        await expect(page.locator('[data-testid="mobile-header"]')).toHaveScreenshot(
          `mobile-header-${theme}.png`
        );
        
        // Test mobile menu open
        await page.click('[data-testid="mobile-menu-button"]');
        await page.waitForSelector('[data-testid="mobile-menu"]');
        await expect(page.locator('[data-testid="mobile-menu"]')).toHaveScreenshot(
          `mobile-menu-open-${theme}.png`
        );
        
        // Test bottom navigation
        await expect(page.locator('[data-testid="bottom-navigation"]')).toHaveScreenshot(
          `bottom-navigation-${theme}.png`
        );
        
        await page.click('[data-testid="mobile-menu-close"]');
      }
    });
  });

  // Full Page Visual Tests (Key Pages)
  test.describe('Full Page Screenshots', () => {
    const keyPages = [
      { path: '/', name: 'dashboard' },
      { path: '/search', name: 'search' },
      { path: '/graphx', name: 'graph-analysis' },
      { path: '/nlp', name: 'nlp-analysis' },
      { path: '/agent', name: 'ai-agents' },
      { path: '/settings', name: 'settings' }
    ];
    
    for (const { path, name } of keyPages) {
      for (const theme of THEMES) {
        for (const viewport of VIEWPORTS) {
          test(`page-${name}-${theme}-${viewport.name}`, async ({ page }) => {
            await page.setViewportSize(viewport);
            await setTheme(page, theme);
            
            await page.goto(path);
            await page.waitForLoadState('networkidle');
            
            // Wait for any loading states to complete
            await page.waitForTimeout(1000);
            
            // Hide any dynamic elements that might cause flakiness
            await hideDynamicElements(page);
            
            await expect(page).toHaveScreenshot(`${name}-${theme}-${viewport.name}.png`, {
              fullPage: true,
              animations: 'disabled'
            });
          });
        }
      }
    }
  });

  // Interactive State Tests
  test.describe('Interactive States', () => {
    test('button-states', async ({ page }) => {
      await page.setViewportSize(VIEWPORTS[2]); // Desktop
      
      for (const theme of THEMES) {
        await setTheme(page, theme);
        await page.goto(COMPONENT_ROUTES.showcase);
        
        const buttonVariants = ['default', 'secondary', 'outline'];
        
        for (const variant of buttonVariants) {
          const button = page.locator(`[data-testid="button-${variant}"]`);
          
          // Normal state
          await expect(button).toHaveScreenshot(`button-${variant}-normal-${theme}.png`);
          
          // Hover state
          await button.hover();
          await expect(button).toHaveScreenshot(`button-${variant}-hover-${theme}.png`);
          
          // Focus state
          await button.focus();
          await expect(button).toHaveScreenshot(`button-${variant}-focus-${theme}.png`);
          
          // Disabled state
          await page.evaluate((variant) => {
            const btn = document.querySelector(`[data-testid="button-${variant}"]`) as HTMLButtonElement;
            if (btn) btn.disabled = true;
          }, variant);
          await expect(button).toHaveScreenshot(`button-${variant}-disabled-${theme}.png`);
        }
      }
    });

    test('tab-interaction-states', async ({ page }) => {
      await page.setViewportSize(VIEWPORTS[2]); // Desktop
      
      for (const theme of THEMES) {
        await setTheme(page, theme);
        await page.goto(COMPONENT_ROUTES.tabs);
        
        const tabContainer = page.locator('[data-testid="default-tabs"]');
        
        // Initial state
        await expect(tabContainer).toHaveScreenshot(`tabs-initial-${theme}.png`);
        
        // Click second tab
        await page.click('[data-testid="tab-trigger-active"]');
        await page.waitForTimeout(300); // Wait for transition
        await expect(tabContainer).toHaveScreenshot(`tabs-second-active-${theme}.png`);
        
        // Hover state on inactive tab
        await page.hover('[data-testid="tab-trigger-disabled"]');
        await expect(tabContainer).toHaveScreenshot(`tabs-hover-inactive-${theme}.png`);
      }
    });
  });

  // Cross-browser Tests (if needed)
  test.describe('Cross-browser Visual Tests', () => {
    ['chromium', 'firefox', 'webkit'].forEach(browserName => {
      test(`critical-components-${browserName}`, async ({ page }) => {
        // Test key components across browsers
        await page.setViewportSize(VIEWPORTS[2]);
        await setTheme(page, 'light');
        
        await page.goto(COMPONENT_ROUTES.showcase);
        
        // Test critical UI components that might render differently
        const criticalComponents = [
          'tab-navigation',
          'form-inputs', 
          'loading-spinners',
          'panels'
        ];
        
        for (const component of criticalComponents) {
          const element = page.locator(`[data-testid="${component}"]`);
          await element.scrollIntoViewIfNeeded();
          await expect(element).toHaveScreenshot(`${component}-${browserName}.png`);
        }
      });
    });
  });
});

// Helper Functions
async function setTheme(page: Page, theme: 'light' | 'dark') {
  await page.evaluate((theme) => {
    // Simulate theme switching - adjust based on your theme implementation
    document.documentElement.classList.remove('light', 'dark');
    document.documentElement.classList.add(theme);
    localStorage.setItem('theme', theme);
    
    // Trigger theme change event if needed
    window.dispatchEvent(new CustomEvent('theme-changed', { detail: theme }));
  }, theme);
  
  // Wait for theme to apply
  await page.waitForTimeout(500);
}

async function hideDynamicElements(page: Page) {
  await page.evaluate(() => {
    // Hide elements that might cause visual flakiness
    const dynamicElements = [
      '[data-testid="timestamp"]',
      '[data-testid="live-status"]',
      '[data-testid="loading-indicator"]',
      '.animate-spin',
      '.animate-pulse'
    ];
    
    dynamicElements.forEach(selector => {
      const elements = document.querySelectorAll(selector);
      elements.forEach(el => {
        (el as HTMLElement).style.visibility = 'hidden';
      });
    });
  });
}

// Component-specific test helpers
test.describe('Tab Navigation Edge Cases', () => {
  test('tab-overflow-behavior', async ({ page }) => {
    await page.setViewportSize({ width: 400, height: 600 }); // Narrow mobile
    await page.goto(COMPONENT_ROUTES.tabs);
    
    // Test how tabs behave when they don't fit
    const tabContainer = page.locator('[data-testid="tab-list-many-tabs"]');
    await expect(tabContainer).toHaveScreenshot('tabs-overflow-mobile.png');
  });
  
  test('tab-loading-states', async ({ page }) => {
    await page.goto(COMPONENT_ROUTES.tabs);
    
    // Simulate tab loading state
    await page.evaluate(() => {
      const tabContent = document.querySelector('[data-testid="tab-content"]');
      if (tabContent) {
        tabContent.innerHTML = '<div data-testid="tab-loading-skeleton">Loading...</div>';
      }
    });
    
    await expect(page.locator('[data-testid="tab-loading-skeleton"]')).toHaveScreenshot('tab-loading-state.png');
  });
});

// Accessibility Visual Tests
test.describe('Accessibility Visual Tests', () => {
  test('focus-indicators', async ({ page }) => {
    await page.goto(COMPONENT_ROUTES.showcase);
    
    // Test focus indicators on interactive elements
    const focusableElements = [
      '[data-testid="tab-trigger"]',
      '[data-testid="button-primary"]',
      '[data-testid="input-field"]',
      '[data-testid="select-field"]'
    ];
    
    for (const selector of focusableElements) {
      const element = page.locator(selector).first();
      await element.focus();
      await expect(element).toHaveScreenshot(`focus-${selector.replace(/[\[\]"=]/g, '')}.png`);
    }
  });
  
  test('high-contrast-mode', async ({ page }) => {
    // Test with forced-colors media query (Windows high contrast)
    await page.emulateMedia({ colorScheme: 'light', forcedColors: 'active' });
    await page.goto(COMPONENT_ROUTES.showcase);
    
    const criticalElements = [
      '[data-testid="tab-navigation"]',
      '[data-testid="button-group"]',
      '[data-testid="form-fields"]'
    ];
    
    for (const selector of criticalElements) {
      const element = page.locator(selector);
      await element.scrollIntoViewIfNeeded();
      await expect(element).toHaveScreenshot(`high-contrast-${selector.replace(/[\[\]"=]/g, '')}.png`);
    }
  });
});

// Performance Visual Tests
test.describe('Performance Impact Visual Tests', () => {
  test('large-dataset-rendering', async ({ page }) => {
    await page.goto('/graphx'); // Page with potentially large datasets
    
    // Simulate loading large dataset
    await page.evaluate(() => {
      // Mock large graph data
      window.mockLargeGraphData = true;
    });
    
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Test that layout doesn't break with large datasets
    await expect(page.locator('[data-testid="graph-container"]')).toHaveScreenshot('large-dataset-graph.png');
  });
  
  test('animation-performance', async ({ page }) => {
    await page.goto(COMPONENT_ROUTES.showcase);
    
    // Test animations don't cause layout shifts
    await page.click('[data-testid="tab-trigger"]');
    await page.waitForTimeout(150); // Mid-animation
    await expect(page.locator('[data-testid="tab-container"]')).toHaveScreenshot('tab-animation-mid.png');
    
    await page.waitForTimeout(200); // Animation complete
    await expect(page.locator('[data-testid="tab-container"]')).toHaveScreenshot('tab-animation-end.png');
  });
});
