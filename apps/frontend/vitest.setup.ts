import "@testing-library/jest-dom";
import { vi } from "vitest";
import fs from "fs";
import path from "path";
import React from "react";

// make React available globally for tests using JSX without explicit import
(global as any).React = React;

// Load environment variables from .env.test
const envPath = path.resolve(__dirname, ".env.test");
if (fs.existsSync(envPath)) {
  const lines = fs.readFileSync(envPath, "utf-8").split(/\r?\n/).filter(Boolean);
  for (const line of lines) {
    const [key, ...rest] = line.split("=");
    if (key) process.env[key] = rest.join("=");
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
Object.defineProperty(window, "matchMedia", {
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

// Ensure layout-dependent libs get non-zero sizes
Object.defineProperty(HTMLElement.prototype, "offsetWidth", {
  configurable: true,
  value: 800,
});
Object.defineProperty(HTMLElement.prototype, "offsetHeight", {
  configurable: true,
  value: 600,
});

// Minimal canvas shim for libs like cytoscape/recharts
Object.defineProperty(HTMLCanvasElement.prototype, "getContext", {
  configurable: true,
  value: () => ({
    fillRect: () => {},
    clearRect: () => {},
    getImageData: () => ({ data: [] }),
    putImageData: () => {},
    createImageData: () => [],
    setTransform: () => {},
    drawImage: () => {},
    save: () => {},
    fillText: () => {},
    restore: () => {},
    beginPath: () => {},
    moveTo: () => {},
    lineTo: () => {},
    closePath: () => {},
    stroke: () => {},
    translate: () => {},
    scale: () => {},
    rotate: () => {},
    arc: () => {},
    fill: () => {},
    measureText: () => ({ width: 0 }),
    transform: () => {},
    rect: () => {},
    clip: () => {},
  }),
});

// Mock next/router
vi.mock("next/router", () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    prefetch: vi.fn(),
    query: {},
    pathname: "/",
    asPath: "/",
  }),
}));

// Mock next/link without enforcing single-child
vi.mock("next/link", () => {
  const React = require("react");
  return {
    default: ({ href, children, ...rest }: any) =>
      React.createElement("a", { href, ...rest }, children),
  };
});

// Mock next-auth
vi.mock("next-auth/react", () => ({
  useSession: () => ({ data: null, status: "unauthenticated" }),
  signIn: vi.fn(),
  signOut: vi.fn(),
}));

// Soft fetch mock
const fetchMock = vi.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({}),
    text: () => Promise.resolve(""),
  } as Response),
);
// @ts-ignore
global.fetch = fetchMock;

// Mock react-cytoscapejs to avoid canvas usage
vi.mock("react-cytoscapejs", () => {
  const React = require("react");
  return {
    __esModule: true,
    default: ({ cy }: any) => {
      React.useEffect(() => {
        if (cy) {
          const stub = {
            handler: undefined as any,
            on: (_evt: string, _sel: string, fn: any) => {
              stub.handler = fn;
            },
            $: (_sel: string) => ({
              emit: (evt: string) =>
                stub.handler && stub.handler({ target: { id: () => _sel.replace("#", "") } }),
            }),
          };
          cy(stub);
        }
      }, [cy]);
      return React.createElement("div");
    },
  };
});

// Mock lucide-react icons
vi.mock(
  "lucide-react",
  () =>
    new Proxy(
      {},
      {
        get: () => () => null,
      },
    ),
);

// --- Polyfills for JSDOM ---

// 1) ResizeObserver (für recharts, etc.)
class RO {
  observe() {}
  unobserve() {}
  disconnect() {}
}
if (typeof (globalThis as any).ResizeObserver === "undefined") {
  (globalThis as any).ResizeObserver = RO as any;
}

// 2) Canvas-Stub (für cytoscape & recharts)
if (typeof HTMLCanvasElement !== "undefined") {
  // Avoid "Could not create canvas of type 2d"
  (HTMLCanvasElement.prototype as any).getContext = function getContext() {
    return {
      // minimal 2D API surface
      canvas: this,
      fillRect() {},
      clearRect() {},
      getImageData() {
        return { data: new Uint8ClampedArray() };
      },
      putImageData() {},
      createImageData() {
        return new ImageData(1, 1);
      },
      setTransform() {},
      drawImage() {},
      save() {},
      restore() {},
      beginPath() {},
      moveTo() {},
      lineTo() {},
      closePath() {},
      stroke() {},
      translate() {},
      scale() {},
      rotate() {},
      arc() {},
      fill() {},
      measureText() {
        return { width: 0 };
      },
      transform() {},
      resetTransform() {},
      createLinearGradient() {
        return { addColorStop() {} };
      },
    };
  };

  // toDataURL is sometimes accessed
  if (!(HTMLCanvasElement.prototype as any).toDataURL) {
    (HTMLCanvasElement.prototype as any).toDataURL = () => "";
  }
}

// 3) matchMedia stub (falls Komponenten es erwarten)
if (typeof (window as any).matchMedia === "undefined") {
  (window as any).matchMedia = () => ({
    matches: false,
    media: "",
    onchange: null,
    addListener() {},
    removeListener() {},
    addEventListener() {},
    removeEventListener() {},
    dispatchEvent() {
      return false;
    },
  });
}
