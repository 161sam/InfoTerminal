import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import GlobalHealth from "@/components/health/GlobalHealth";
import { vi } from "vitest";

describe("GlobalHealth", () => {
  it("shows green when all ok and opens popover", async () => {
    const mock = {
      timestamp: new Date().toISOString(),
      services: {
        search: { state: "ok", latencyMs: 10 },
        graph: { state: "ok", latencyMs: 12 },
        docentities: { state: "ok", latencyMs: 8 },
        nlp: { state: "ok", latencyMs: 9 },
      },
    };
    global.fetch = vi.fn().mockResolvedValue({ ok: true, json: async () => mock });
    render(<GlobalHealth pollIntervalMs={100000} />);
    await waitFor(() => expect(global.fetch).toHaveBeenCalled());
    const btn = screen.getByLabelText("service-health");
    const dot = btn.querySelector("span span");
    expect(dot?.className).toContain("bg-green-500");
    await fireEvent.click(btn);
    expect(screen.getByText(/search/i)).toBeInTheDocument();
    expect(screen.getByText(/graph/i)).toBeInTheDocument();
    expect(screen.getByText(/docentities/i)).toBeInTheDocument();
    expect(screen.getByText(/nlp/i)).toBeInTheDocument();
  });
});
