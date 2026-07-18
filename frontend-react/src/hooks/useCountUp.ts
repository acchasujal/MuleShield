// ============================================================
// MuleShield — useCountUp Hook
// Animates a number from its current value to a target value.
// ============================================================

import { useEffect, useRef, useState } from "react";

/**
 * Smoothly animates a counter from its previous value to `target`.
 * Uses requestAnimationFrame with easeOut timing.
 */
export function useCountUp(target: number, duration = 500): number {
  const [value, setValue] = useState(0);
  const previousTarget = useRef(0);

  useEffect(() => {
    const start = previousTarget.current;
    previousTarget.current = target;

    if (start === target) return;

    const startTime = performance.now();
    let frame: number;

    const tick = (now: number) => {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = progress * (2 - progress); // easeOut quad
      setValue(Math.round(start + (target - start) * eased));
      if (progress < 1) {
        frame = requestAnimationFrame(tick);
      }
    };

    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [target, duration]);

  return value;
}
