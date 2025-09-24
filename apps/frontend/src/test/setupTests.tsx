import "@testing-library/jest-dom";
import { vi } from "vitest";

// -------------------- Polyfills --------------------

// ResizeObserver (für Recharts & Co.)
class RO {
  observe() {}
  unobserve() {}
  disconnect() {}
}
(globalThis as any).ResizeObserver = (globalThis as any).ResizeObserver ?? RO;

// Canvas-API (jsdom hat kein echtes Canvas)
if (!(HTMLCanvasElement.prototype as any).getContext) {
  (HTMLCanvasElement.prototype as any).getContext = vi.fn(() => {
    // Minimal-Stub – genug für libs, die nur Präsenz prüfen
    return {
      canvas: document.createElement("canvas"),
      // no-op Methods:
      save() {},
      restore() {},
      beginPath() {},
      closePath() {},
      moveTo() {},
      lineTo() {},
      stroke() {},
      fill() {},
      rect() {},
      clearRect() {},
      fillRect() {},
      drawImage() {},
      putImageData() {},
      getImageData: () => ({ data: [] }),
      createImageData: () => ({}),
      setTransform() {},
      resetTransform() {},
      translate() {},
      scale() {},
      rotate() {},
      arc() {},
      measureText: () => ({ width: 0 }),
      fillText() {},
    };
  });
}

// getBoundingClientRect – einige Layout-basierte Komponenten erwarten Maße
if (!HTMLElement.prototype.getBoundingClientRect) {
  HTMLElement.prototype.getBoundingClientRect = function () {
    return {
      x: 0,
      y: 0,
      top: 0,
      left: 0,
      bottom: 0,
      right: 0,
      width: (this as HTMLElement).offsetWidth || 300,
      height: (this as HTMLElement).offsetHeight || 150,
      toJSON() {},
    } as DOMRect;
  };
}

// -------------------- Library-Mocks --------------------
// Next.js router mock for components using useRouter in tests
vi.mock("next/router", () => {
  return {
    __esModule: true,
    useRouter: () => ({
      pathname: "/",
      push: vi.fn(),
      prefetch: vi.fn(),
      replace: vi.fn(),
      query: {},
    }),
  };
});

// react-cytoscapejs: Fake-Implementierung ohne Canvas. Ruft die "cy"-Callback-Prop auf
// und erlaubt das Auslösen eines "tap"-Events auf einen Node mit id 'a' über einen Button.
vi.mock("react-cytoscapejs", () => {
  const React = require("react");

  const CytoscapeStub = ({ cy }: any) => {
    const handlers: Record<string, (evt: any) => void> = {};

    const fakeCy = {
      on: (event: string, selector: string, handler: (evt: any) => void) => {
        handlers[`${event}:${selector}`] = handler;
      },
      destroy: () => {},
    } as const;

    if (typeof cy === "function") {
      cy(fakeCy);
    }

    return (
      <button
        data-testid="fire-tap-a"
        onClick={() => handlers["tap:node"]?.({ target: { id: () => "a" } })}
      >
        fire tap a
      </button>
    );
  };

  return {
    __esModule: true,
    default: CytoscapeStub,
    CytoscapeComponent: CytoscapeStub,
  };
});

// useFileUpload mocken: nach "Upload" sofort Erfolg + doc_id liefern,
// damit Tests den Link "Zum Dokument" finden
vi.mock("@/hooks/useFileUpload", () => {
  const React = require("react");

  type Upload = {
    id: string;
    fileName: string;
    status: "pending" | "uploading" | "success" | "error";
    progress: number;
    message?: string;
    doc_id?: string;
  };

  return {
    __esModule: true,
    default: () => {
      const [uploads, setUploads] = React.useState([]) as [
        Upload[],
        React.Dispatch<React.SetStateAction<Upload[]>>,
      ];

      const startUpload = async (files: File[]) => {
        const newUploads = files.map((f, i) => ({
          id: String(Date.now() + i),
          fileName: f.name,
          status: "success" as const,
          progress: 100,
          doc_id: "demo-doc-1",
        }));
        setUploads(newUploads);
        return newUploads.map((u) => ({ ok: true, id: u.doc_id }));
      };

      const cancelUpload = () => {};
      const retryUpload = () => {};

      return { uploads, startUpload, cancelUpload, retryUpload };
    },
  };
});
