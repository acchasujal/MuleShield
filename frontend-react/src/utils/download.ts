// ============================================================
// MuleShield — Download Utilities
// ============================================================

/**
 * Triggers a browser download of a text string as a file.
 */
export function downloadText(content: string, filename: string): void {
  const blob = new Blob([content], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(url);
}
