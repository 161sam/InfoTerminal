"use client";
import { highlightText, Entity } from "@/lib/nlp";

export default function HighlightedText({
  text,
  entities,
}: {
  text: string;
  entities: Entity[];
}) {
  const parts = highlightText(text, entities);
  return (
    <p className="leading-relaxed">
      {parts.map((p, i) =>
        p.label ? (
          <mark key={i} title={p.label} className="rounded px-1">
            {p.t}
          </mark>
        ) : (
          <span key={i}>{p.t}</span>
        )
      )}
    </p>
  );
}
