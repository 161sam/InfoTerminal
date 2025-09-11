import { defineConfig } from 'vitest/config';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [tsconfigPaths()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/setupTests.ts'],
    css: false,
    // nur Unit-/Component-Tests
    include: ['src/__tests__/**/*.{test,spec}.{ts,tsx}'],
    // E2E / Playwright ausklammern:
    exclude: [
      '**/node_modules/**',
      '**/dist/**',
      '**/build/**',
      '**/e2e/**',
    ],
  },
  resolve: {
    // Fallback – normalerweise reicht das Plugin, aber doppelt hält besser
    alias: {
      '@': '/apps/frontend/src',
    },
  },
});
