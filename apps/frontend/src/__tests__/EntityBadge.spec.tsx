import { fireEvent, render } from "@testing-library/react";
import EntityBadge from "@/components/entities/EntityBadge";
import { describe, it, expect, vi } from "vitest";

describe("EntityBadge", () => {
  it("renders label", () => {
    const { getByText } = render(<EntityBadge label="Person" />);
    expect(getByText("Person")).toBeInTheDocument();
  });

  it("calls onClick when clicked", () => {
    const onClick = vi.fn();
    const { getByRole } = render(<EntityBadge label="Organization" clickable onClick={onClick} />);
    fireEvent.click(getByRole("button"));
    expect(onClick).toHaveBeenCalled();
  });

  it("renders as link when href provided", () => {
    const { container } = render(<EntityBadge label="Location" href="/search" />);
    const a = container.querySelector("a");
    expect(a).toHaveAttribute("href", "/search");
  });
});
