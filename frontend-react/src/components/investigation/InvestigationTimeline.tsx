// ============================================================
// MuleShield — InvestigationTimeline
// Shows the mule lifecycle stage as a horizontal timeline.
// ============================================================

import { memo } from "react";
import { MULE_STAGES } from "../../constants";
import { labelStage } from "../../utils/caseUtils";

interface InvestigationTimelineProps {
  currentStage: string;
  highlightedDimension: "profile" | "transaction" | "network" | null;
}

export const InvestigationTimeline = memo(function InvestigationTimeline({
  currentStage,
  highlightedDimension,
}: InvestigationTimelineProps) {
  const currentIndex = Math.max(0, MULE_STAGES.indexOf(currentStage as typeof MULE_STAGES[number]));

  return (
    <div>
      <div className="section-head">
        <h3>Investigation timeline</h3>
        <span className="text-muted text-xs">Lifecycle context</span>
      </div>
      <ol
        className="timeline"
        aria-label="Mule lifecycle stages"
        role="list"
      >
        {MULE_STAGES.map((stage, index) => {
          const isDone = index < currentIndex;
          const isCurrent = index === currentIndex;
          const isHighlighted =
            highlightedDimension === "profile" && index === 0;

          return (
            <li
              key={stage}
              className={[
                "timeline-item",
                isDone ? "done" : "",
                isCurrent ? "current" : "",
                isHighlighted ? "highlighted-timeline" : "",
              ]
                .filter(Boolean)
                .join(" ")}
              aria-current={isCurrent ? "step" : undefined}
            >
              <div
                className="timeline-dot"
                aria-hidden="true"
              />
              <div className="timeline-label">{labelStage(stage)}</div>
            </li>
          );
        })}
      </ol>
    </div>
  );
});
