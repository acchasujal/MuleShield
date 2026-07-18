// ============================================================
// MuleShield — useUpload Hook
// Handles CSV file upload with API fallback to guided demo.
// ============================================================

import { useCallback } from "react";
import { uploadBatch } from "../services/api";
import type { CaseItem } from "../types";

interface UseUploadOptions {
  onSuccess: (cases: CaseItem[], firstId: string) => void;
  onFallback: () => void;
  notify: (message: string) => void;
}

/**
 * Returns an upload handler that calls the API and falls back
 * to the guided demo if the backend is unavailable.
 */
export function useUpload({
  onSuccess,
  onFallback,
  notify,
}: UseUploadOptions) {
  const handleUpload = useCallback(
    async (file: File) => {
      try {
        const { cases } = await uploadBatch(file);
        if (cases.length > 0) {
          onSuccess(cases, cases[0].account);
          notify("Transaction batch analyzed.");
        } else {
          notify("No alerts in uploaded batch.");
        }
      } catch {
        notify("Backend unavailable — showing offline guided case instead.");
        onFallback();
      }
    },
    [onSuccess, onFallback, notify]
  );

  return handleUpload;
}
