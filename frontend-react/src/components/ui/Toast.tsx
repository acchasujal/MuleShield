// ============================================================
// MuleShield — Toast Notification
// ============================================================

import { AnimatePresence, motion } from "framer-motion";
import { memo } from "react";

interface ToastProps {
  message: string;
}

export const Toast = memo(function Toast({ message }: ToastProps) {
  return (
    <AnimatePresence>
      {message && (
        <motion.div
          role="status"
          aria-live="polite"
          aria-atomic="true"
          className="toast"
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 12 }}
          transition={{ duration: 0.18, ease: [0.16, 1, 0.3, 1] }}
        >
          {message}
        </motion.div>
      )}
    </AnimatePresence>
  );
});
