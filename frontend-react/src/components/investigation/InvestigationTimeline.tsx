// ============================================================
// MuleShield — InvestigationTimeline
// Shows the mule lifecycle stage as a horizontal timeline.
// ============================================================

import { memo } from "react";
import { MULE_STAGES } from "../../constants";
import { labelStage } from "../../utils/caseUtils";
import type { CaseItem } from "../../types";

interface InvestigationTimelineProps {
  currentStage: string;
  highlightedDimension: "profile" | "transaction" | "network" | null;
  item?: CaseItem;
}

export const InvestigationTimeline = memo(function InvestigationTimeline({
  currentStage,
  highlightedDimension,
  item,
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
      {item?.timeline?.length ? (
        <div className="event-timeline" aria-label="Investigation evidence events">
          {item.timeline.map((event, index) => (
            <div className="event-row" key={`${event.timestamp}-${event.label}`}>
              <div className={`event-marker event-${event.kind}`} aria-hidden="true" />
              <div className="event-copy">
                <div className="event-meta"><span className="font-mono">{event.timestamp}</span><span className="risk-delta">+{event.risk_delta} risk</span></div>
                <strong>{event.label}</strong><span>{event.detail}</span>
              </div>
              {index === item.timeline.length - 1 && <span className="event-decision">Review</span>}
            </div>
          ))}
        </div>
      ) : null}
    </div>
  );
});
