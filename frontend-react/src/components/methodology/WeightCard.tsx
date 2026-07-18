// ============================================================
// MuleShield — WeightCard (Methodology page)
// ============================================================

import { memo } from "react";
import type { LucideIcon } from "lucide-react";

interface WeightCardProps {
  value: string;
  label: string;
  text: string;
  icon: LucideIcon;
}

export const WeightCard = memo(function WeightCard({
  value,
  label,
  text,
  icon: Icon,
}: WeightCardProps) {
  return (
    <div className="card" aria-label={`${label}: ${value} weight`}>
      <Icon size={20} aria-hidden={true} />
      <div className="weight-value" aria-label={`${value} weighting`}>
        {value}
      </div>
      <h3>{label}</h3>
      <p
        className="text-muted text-sm"
        style={{ lineHeight: "var(--leading-relaxed)", marginTop: "var(--space-2)" }}
      >
        {text}
      </p>
    </div>
  );
});
