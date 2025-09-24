import { render, screen } from "@testing-library/react";
import EntityHighlighter from "@/components/docs/EntityHighlighter";
import { Entity } from "@/types/docs";

test("renders marks and graph links", () => {
  process.env.NEXT_PUBLIC_GRAPH_DEEPLINK_BASE = "/graphx?focus=";
  const text = "Hello Barack Obama";
  const entities: Entity[] = [
    { text: "Barack Obama", start: 6, end: 18, label: "PERSON", node_id: "123" },
  ];
  render(<EntityHighlighter text={text} entities={entities} />);
  const mark = screen.getByText("Barack Obama");
  expect(mark.tagName).toBe("MARK");
  const link = screen.getByRole("link", { name: /im graph anzeigen/i });
  expect(link).toHaveAttribute("href", "/graphx?focus=123");
});
