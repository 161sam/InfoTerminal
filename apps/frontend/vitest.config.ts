import { defineConfig } from 'vitest/config';

export default defineConfig(async () => ({
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/setupTests.ts'],
    css: false,
    exclude: ['**/e2e/**', '**/node_modules/**'],
  },
  plugins: [(await import('vite-tsconfig-paths')).default()],
}));
