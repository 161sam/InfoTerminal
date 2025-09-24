import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { vi } from "vitest";
import DemoPage from "../../pages/demo";

test("triggers loader and shows results", async () => {
  global.fetch = vi.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ ingested: [{ file: "demo1.pdf" }], skipped: [] }),
  }) as any;
  render(<DemoPage />);
  fireEvent.click(screen.getByText("Demo-Daten laden"));
  expect(screen.getByText("Loading...")).toBeInTheDocument();
  await waitFor(() => expect(global.fetch).toHaveBeenCalled());
  await waitFor(() => expect(screen.getByText("demo1.pdf")).toBeInTheDocument());
});
