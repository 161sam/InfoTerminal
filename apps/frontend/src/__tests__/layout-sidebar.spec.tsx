import { render, screen, fireEvent } from "@testing-library/react";
import React from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";

function LayoutFixture() {
  return (
    <DashboardLayout title="Test Title" subtitle="Sub">
      <div>Content</div>
    </DashboardLayout>
  );
}

describe("DashboardLayout accessibility and sidebar", () => {
  it("renders structural landmark roles", () => {
    render(<LayoutFixture />);
    expect(screen.getByRole("banner")).toBeInTheDocument();
    expect(screen.getAllByRole("navigation").length).toBeGreaterThan(0);
    expect(screen.getByRole("main")).toBeInTheDocument();
  });

  it("opens and closes the mobile sidebar with proper ARIA", () => {
    render(<LayoutFixture />);
    const toggle = screen.getByRole("button", { name: /open sidebar/i });
    expect(toggle).toHaveAttribute("aria-controls", "mobile-sidebar");
    expect(toggle).toHaveAttribute("aria-expanded", "false");

    fireEvent.click(toggle);
    expect(toggle).toHaveAttribute("aria-expanded", "true");
    const drawer = screen.getByRole("dialog", { name: /sidebar/i });
    expect(drawer).toHaveAttribute("id", "mobile-sidebar");

    // click overlay to close: find by backdrop via click on element behind dialog
    const overlay = document.querySelector('[aria-hidden="true"]') as HTMLElement | null;
    if (overlay) fireEvent.click(overlay);

    // aria-expanded should go back to false
    expect(toggle).toHaveAttribute("aria-expanded", "false");
  });
});
