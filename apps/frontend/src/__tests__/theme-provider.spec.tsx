import { render, screen, fireEvent, act } from "@testing-library/react";
import React from "react";
import { ThemeProvider, ThemeToggle } from "@/lib/theme-provider";

function setupMatchMedia(matches: boolean) {
  const mql: any = {
    matches,
    media: "(prefers-color-scheme: dark)",
    onchange: null,
    addEventListener: function (_: string, cb: any) {
      this._cb = cb;
    },
    removeEventListener: function () {
      this._cb = null;
    },
    dispatch: function (matchesNext: boolean) {
      this.matches = matchesNext;
      this._cb?.({ matches: matchesNext });
    },
  };
  // @ts-ignore
  window.matchMedia = vi.fn().mockImplementation(() => mql);
  return mql;
}

describe("ThemeProvider and ThemeToggle", () => {
  beforeEach(() => {
    localStorage.clear();
    document.documentElement.classList.remove("dark");
  });

  it("rotates light -> dark -> system -> light and persists ui.theme", () => {
    setupMatchMedia(false);
    render(
      <ThemeProvider>
        <ThemeToggle />
      </ThemeProvider>,
    );

    const btn = screen.getByRole("button");

    // Initial: light (default, no dark unless system matches)
    expect(localStorage.getItem("ui.theme")).toBeNull();
    expect(document.documentElement.classList.contains("dark")).toBe(false);

    // Click -> dark
    fireEvent.click(btn);
    expect(localStorage.getItem("ui.theme")).toBe("dark");
    expect(document.documentElement.classList.contains("dark")).toBe(true);

    // Click -> system
    fireEvent.click(btn);
    expect(localStorage.getItem("ui.theme")).toBe("system");
    // system is currently light
    expect(document.documentElement.classList.contains("dark")).toBe(false);

    // Click -> light
    fireEvent.click(btn);
    expect(localStorage.getItem("ui.theme")).toBe("light");
    expect(document.documentElement.classList.contains("dark")).toBe(false);
  });

  it.skip("follows system preference changes live in system mode", () => {
    const mql = setupMatchMedia(false);
    render(
      <ThemeProvider>
        <ThemeToggle />
      </ThemeProvider>,
    );

    const btn = screen.getByRole("button");
    // move to system
    fireEvent.click(btn); // dark
    fireEvent.click(btn); // system
    expect(localStorage.getItem("ui.theme")).toBe("system");
    expect(document.documentElement.classList.contains("dark")).toBe(false);

    // Flip system to dark
    act(() => {
      mql.dispatch(true);
    });
    expect(document.documentElement.classList.contains("dark")).toBe(true);

    // Flip back to light
    act(() => {
      mql.dispatch(false);
    });
    expect(document.documentElement.classList.contains("dark")).toBe(false);
  });
});
