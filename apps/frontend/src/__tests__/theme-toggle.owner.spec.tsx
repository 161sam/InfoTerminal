import React from "react";
import { render, fireEvent } from "@testing-library/react";
import { vi } from "vitest";
import { ThemeProvider, ThemeToggle } from "@/lib/theme-provider";

function setupMatchMedia() {
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: vi.fn().mockImplementation((query) => ({
      matches: false,
      media: query,
      onchange: null,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
    })),
  });
}

describe("Theme single authority", () => {
  beforeEach(() => {
    localStorage.clear();
    document.documentElement.classList.remove("dark");
    document.body.classList.remove("dark");
    setupMatchMedia();
  });

  it("toggles html.dark and never sets body.dark", () => {
    const { getByRole } = render(
      <ThemeProvider>
        <ThemeToggle />
      </ThemeProvider>
    );

    const btn = getByRole('button');
    const html = document.documentElement;
    const body = document.body;

    expect(body.classList.contains("dark")).toBe(false);

    fireEvent.click(btn); // light -> dark
    expect(html.classList.contains("dark")).toBe(true);
    expect(localStorage.getItem("ui.theme")).toBe("dark");
    expect(body.classList.contains("dark")).toBe(false);

    fireEvent.click(btn); // dark -> system
    expect(html.classList.contains("dark")).toBe(false);
    expect(localStorage.getItem("ui.theme")).toBe("system");
    expect(body.classList.contains("dark")).toBe(false);

    fireEvent.click(btn); // system -> light
    expect(html.classList.contains("dark")).toBe(false);
    expect(localStorage.getItem("ui.theme")).toBe("light");
    expect(body.classList.contains("dark")).toBe(false);
  });
});

