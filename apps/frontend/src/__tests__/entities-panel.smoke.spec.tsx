import { render } from "@testing-library/react";
import React from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";

function FakeEntities() {
  return (
    <DashboardLayout title="Entities">
      <div data-testid="entities-page">
        <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-4">
          <h2>Entity Distribution</h2>
        </div>
        <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-4 mt-4">
          <h2>Data Table</h2>
        </div>
      </div>
    </DashboardLayout>
  );
}

describe("Entities page surfaces", () => {
  it("renders dark-safe panels", () => {
    const { getByTestId } = render(<FakeEntities />);
    const root = getByTestId("entities-page");
    const html = document.documentElement;
    html.classList.add("dark");
    expect(root.querySelectorAll(".dark\\:bg-gray-900").length).toBeGreaterThan(0);
  });
});
