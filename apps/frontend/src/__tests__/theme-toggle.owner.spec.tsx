import React from "react";
import { render, fireEvent } from "@testing-library/react";
import { ThemeProvider, ThemeToggle } from "@/lib/theme-provider";

describe("Theme single authority", () => {
  beforeEach(() => {
    localStorage.clear();
    document.documentElement.classList.remove("dark");
    document.body.classList.remove("dark");
  });

  it("toggles html.dark and never sets body.dark", () => {
    const { getByTestId } = render(
      <ThemeProvider>
        <ThemeToggle />
      </ThemeProvider>
    );

    const btn = getByTestId("theme-toggle");
    const html = document.documentElement;
    const body = document.body;

    expect(body.classList.contains("dark")).toBe(false);

    fireEvent.click(btn); // system -> light (initial provider default)
    expect(html.classList.contains("dark")).toBe(false);
    expect(localStorage.getItem("ui.theme")).toBe("light");
    expect(body.classList.contains("dark")).toBe(false);

    fireEvent.click(btn); // light -> dark
    expect(html.classList.contains("dark")).toBe(true);
    expect(localStorage.getItem("ui.theme")).toBe("dark");
    expect(body.classList.contains("dark")).toBe(false);

    fireEvent.click(btn); // dark -> system
    expect(localStorage.getItem("ui.theme")).toBe("system");
    expect(body.classList.contains("dark")).toBe(false);
  });
});

