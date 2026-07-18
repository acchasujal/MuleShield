// ============================================================
// MuleShield — NetworkDiagram
// SVG-based network visualization showing linked accounts.
// Uses SVG lines for edges (Q4 decision: no heavy graph libraries).
// ============================================================

import { memo } from "react";
import { Network } from "lucide-react";

interface NetworkDiagramProps {
  subjectAccount: string;
  highlighted: boolean;
}

// Fixed node positions for the static demo topology
const NODE_SUBJECT = { cx: 200, cy: 100 };
const NODE_N1 = { cx: 70, cy: 48 };
const NODE_N2 = { cx: 330, cy: 155 };

export const NetworkDiagram = memo(function NetworkDiagram({
  subjectAccount,
  highlighted,
}: NetworkDiagramProps) {
  return (
    <div
      className={`network-diagram${highlighted ? " highlighted" : ""}`}
      aria-label="Network relationship diagram showing linked accounts"
    >
      {/* SVG edges */}
      <svg
        width="100%"
        height="160"
        viewBox="0 0 400 200"
        aria-hidden="true"
        style={{ position: "absolute", inset: 0 }}
      >
        {/* Subject ↔ N1 */}
        <line
          x1={NODE_SUBJECT.cx}
          y1={NODE_SUBJECT.cy}
          x2={NODE_N1.cx}
          y2={NODE_N1.cy}
          stroke="rgba(164,166,255,0.35)"
          strokeWidth="1"
          strokeDasharray="4 3"
        />
        {/* Subject ↔ N2 */}
        <line
          x1={NODE_SUBJECT.cx}
          y1={NODE_SUBJECT.cy}
          x2={NODE_N2.cx}
          y2={NODE_N2.cy}
          stroke="rgba(164,166,255,0.35)"
          strokeWidth="1"
          strokeDasharray="4 3"
        />
        {/* Flow arrow midpoints */}
        <circle
          cx={(NODE_SUBJECT.cx + NODE_N1.cx) / 2}
          cy={(NODE_SUBJECT.cy + NODE_N1.cy) / 2}
          r="2.5"
          fill="rgba(91,95,239,0.7)"
        />
        <circle
          cx={(NODE_SUBJECT.cx + NODE_N2.cx) / 2}
          cy={(NODE_SUBJECT.cy + NODE_N2.cy) / 2}
          r="2.5"
          fill="rgba(91,95,239,0.7)"
        />
      </svg>

      {/* Nodes as absolutely positioned DOM elements */}
      <div
        className="network-node network-node-subject"
        title={subjectAccount}
        role="img"
        aria-label={`Subject account ${subjectAccount}`}
      >
        {subjectAccount.slice(-4)}
      </div>
      <div
        className="network-node network-node-secondary network-node-n1"
        title="Linked account ACC...999"
        role="img"
        aria-label="Linked account"
      >
        ...999
      </div>
      <div
        className="network-node network-node-secondary network-node-n2"
        title="Linked account ACC...980"
        role="img"
        aria-label="Linked account"
      >
        ...980
      </div>

      <p
        className="text-muted text-xs"
        style={{
          position: "absolute",
          bottom: "var(--space-3)",
          left: "var(--space-3)",
          right: "var(--space-3)",
          display: "flex",
          alignItems: "center",
          gap: "var(--space-1)",
          lineHeight: "var(--leading-snug)",
        }}
      >
        <Network size={12} aria-hidden="true" />
        Simulated offline network enrichment. Fallback targets configured.
      </p>
    </div>
  );
});
