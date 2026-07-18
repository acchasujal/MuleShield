// ============================================================
// MuleShield — NetworkDiagram
// SVG-based network visualization showing linked accounts.
// Uses SVG lines for edges (Q4 decision: no heavy graph libraries).
// ============================================================

import { memo } from "react";
import { motion } from "framer-motion";
import { Network } from "lucide-react";
import type { CaseItem } from "../../types";

interface NetworkDiagramProps {
  subjectAccount: string;
  highlighted: boolean;
  item?: CaseItem;
}

// Fixed node positions for the static demo topology
const NODE_SUBJECT = { cx: 200, cy: 100 };
const NODE_N1 = { cx: 70, cy: 48 };
const NODE_N2 = { cx: 330, cy: 155 };

export const NetworkDiagram = memo(function NetworkDiagram({
  subjectAccount,
  highlighted,
  item,
}: NetworkDiagramProps) {
  const nodes = item?.network.nodes ?? [
    { id: subjectAccount, label: subjectAccount, role: "Subject account", risk: "subject" as const },
    { id: "...999", label: "...999", role: "Linked account", risk: "linked" as const },
    { id: "...980", label: "...980", role: "Settlement node", risk: "sink" as const },
  ];
  const edges = item?.network.edges ?? [];
  const positions = [{ x: 50, y: 50 }, { x: 18, y: 24 }, { x: 82, y: 72 }, { x: 80, y: 20 }, { x: 20, y: 78 }, { x: 50, y: 84 }];
  return (
    <div
      className={`network-diagram${highlighted ? " highlighted" : ""}`}
      aria-label="Network relationship diagram showing linked accounts"
    >
      {/* SVG edges */}
      <svg width="100%" height="190" viewBox="0 0 400 200" aria-hidden="true" style={{ position: "absolute", inset: 0 }}>
        <defs><marker id="flow-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="rgba(164,166,255,.65)" /></marker></defs>
        {edges.slice(0, 5).map((networkEdge, index) => {
          const from = positions[0]; const to = positions[(index % Math.max(1, nodes.length - 1)) + 1] || positions[1];
          return <motion.line key={`${networkEdge.from}-${networkEdge.to}-${index}`} x1={`${from.x}%`} y1={`${from.y}%`} x2={`${to.x}%`} y2={`${to.y}%`} stroke={networkEdge.direction === "inbound" ? "rgba(245,158,11,.65)" : "rgba(164,166,255,.52)"} strokeWidth="1.5" strokeDasharray="5 4" markerEnd="url(#flow-arrow)" initial={{ pathLength: 0, opacity: 0 }} animate={{ pathLength: 1, opacity: 1 }} transition={{ duration: .65, delay: index * .12 }} />;
        })}
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
      {nodes.slice(0, 6).map((networkNode, index) => <div key={networkNode.id} className={`network-node ${index === 0 ? "network-node-subject" : "network-node-secondary"}`} style={index === 0 ? undefined : { left: `${positions[index]?.x || 20}%`, top: `${positions[index]?.y || 24}%` }} title={`${networkNode.id} · ${networkNode.role}`} role="img" aria-label={`${networkNode.role} ${networkNode.id}`}>{index === 0 ? subjectAccount.slice(-4) : networkNode.id.slice(-4)}</div>)}

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
