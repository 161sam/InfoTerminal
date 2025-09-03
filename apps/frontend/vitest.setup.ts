import '@testing-library/jest-dom';
import { vi } from 'vitest';
import fs from 'fs';
import path from 'path';
import React from 'react';

// make React available globally for tests using JSX without explicit import
(global as any).React = React;

// Load environment variables from .env.test
const envPath = path.resolve(__dirname, '.env.test');
if (fs.existsSync(envPath)) {
  const lines = fs.readFileSync(envPath, 'utf-8').split(/\r?\n/).filter(Boolean);
  for (const line of lines) {
    const [key, ...rest] = line.split('=');
    if (key) process.env[key] = rest.join('=');
  }
}

// Polyfill ResizeObserver
class ResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
}
(global as any).ResizeObserver = ResizeObserver;

// Stub matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: (query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  }),
});

// Mock next/router
vi.mock('next/router', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    prefetch: vi.fn(),
    query: {},
    pathname: '/',
    asPath: '/',
  }),
}));

// Mock next/link
vi.mock('next/link', () => {
  const React = require('react');
  return {
    default: ({ href, children, ...rest }: any) =>
      React.cloneElement(React.Children.only(children), { href, ...rest }),
  };
});

// Mock next-auth
vi.mock('next-auth/react', () => ({
  useSession: () => ({ data: null, status: 'unauthenticated' }),
  signIn: vi.fn(),
  signOut: vi.fn(),
}));

// Soft fetch mock
const fetchMock = vi.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({}),
    text: () => Promise.resolve(''),
  } as Response),
);
// @ts-ignore
global.fetch = fetchMock;

// Mock lucide-react icons
vi.mock('lucide-react', () => new Proxy({}, {
  get: () => () => null,
}));
