// ============================================================
// MuleShield — Highlight
// Renders text with search query matches highlighted.
// ============================================================

import { memo } from "react";

interface HighlightProps {
  text: string;
  query: string;
}

export const Highlight = memo(function Highlight({
  text,
  query,
}: HighlightProps) {
  if (!query.trim()) return <span>{text}</span>;

  const escaped = query.replace(/[-/\\^$*+?.()|[\]{}]/g, "\\$&");
  const parts = text.split(new RegExp(`(${escaped})`, "gi"));

  return (
    <span>
      {parts.map((part, i) =>
        part.toLowerCase() === query.toLowerCase() ? (
          <mark key={i} className="search-highlight">
            {part}
          </mark>
        ) : (
          <span key={i}>{part}</span>
        )
      )}
    </span>
  );
});
