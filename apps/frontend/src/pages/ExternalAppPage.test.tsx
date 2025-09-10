import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { vi } from "vitest";
import ExternalAppPage from "./ExternalAppPage";
import * as routes from "../routes/appRoutes";

test("renders warning if URL not configured", () => {
  const spy = vi.spyOn(routes, "appRoutes", "get").mockReturnValue([
    { key: "aleph", label: "Aleph", path: "/apps/aleph", kind: "external", urlEnvVar: "VITE_APP_ALEPH_URL", enabled: true }
  ] as any);

  render(
    <MemoryRouter initialEntries={["/apps/aleph"]}>
      <Routes>
        <Route path="/apps/aleph" element={<ExternalAppPage />} />
      </Routes>
    </MemoryRouter>
  );

  expect(screen.getByText(/nicht konfiguriert/i)).toBeInTheDocument();
  spy.mockRestore();
});
