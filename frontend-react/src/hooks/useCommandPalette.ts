// ============================================================
// MuleShield — Command Palette Hook
//
// Handles open/close state, keyboard navigation, search,
// command execution, and recent-action tracking.
// ============================================================

import { useCallback, useEffect, useRef, useState } from "react";
import type { LucideIcon } from "lucide-react";

export interface Command {
  id: string;
  label: string;
  category: string;
  icon: LucideIcon;
  shortcut?: string[];
  action: () => void;
}

const RECENT_KEY = "ms_recent_cmds";
const MAX_RECENT = 3;

function loadRecent(): string[] {
  try {
    const raw = sessionStorage.getItem(RECENT_KEY);
    return raw ? (JSON.parse(raw) as string[]) : [];
  } catch {
    return [];
  }
}

function saveRecent(ids: string[]): void {
  try {
    sessionStorage.setItem(RECENT_KEY, JSON.stringify(ids));
  } catch {
    /* ignore */
  }
}

export function useCommandPalette(commands: Command[]) {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [focusedIndex, setFocusedIndex] = useState(0);
  const [recentIds, setRecentIds] = useState<string[]>(loadRecent);
  const searchRef = useRef<HTMLInputElement>(null);

  // ── Filtered commands ─────────────────────────────────────
  const filtered = query.trim()
    ? commands.filter((c) =>
        `${c.label} ${c.category}`.toLowerCase().includes(query.toLowerCase())
      )
    : commands;

  // ── Open / close ──────────────────────────────────────────
  const open = useCallback(() => {
    setIsOpen(true);
    setQuery("");
    setFocusedIndex(0);
  }, []);

  const close = useCallback(() => {
    setIsOpen(false);
    setQuery("");
    setFocusedIndex(0);
  }, []);

  const toggle = useCallback(() => {
    setIsOpen((prev) => {
      if (!prev) {
        setQuery("");
        setFocusedIndex(0);
      }
      return !prev;
    });
  }, []);

  // ── Execute a command ─────────────────────────────────────
  const execute = useCallback(
    (cmd: Command) => {
      // Track recent
      const next = [
        cmd.id,
        ...recentIds.filter((id) => id !== cmd.id),
      ].slice(0, MAX_RECENT);
      setRecentIds(next);
      saveRecent(next);
      // Run
      cmd.action();
      close();
    },
    [recentIds, close]
  );

  // ── Focus search on open ──────────────────────────────────
  useEffect(() => {
    if (isOpen) {
      const raf = requestAnimationFrame(() => searchRef.current?.focus());
      return () => cancelAnimationFrame(raf);
    }
  }, [isOpen]);

  // ── Keyboard handler (Ctrl+K global) ─────────────────────
  useEffect(() => {
    const handleGlobal = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        toggle();
      }
    };
    window.addEventListener("keydown", handleGlobal);
    return () => window.removeEventListener("keydown", handleGlobal);
  }, [toggle]);

  // ── Keyboard handler (inside palette) ────────────────────
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      switch (e.key) {
        case "Escape":
          e.preventDefault();
          close();
          break;
        case "ArrowDown":
          e.preventDefault();
          setFocusedIndex((i) => Math.min(i + 1, filtered.length - 1));
          break;
        case "ArrowUp":
          e.preventDefault();
          setFocusedIndex((i) => Math.max(i - 1, 0));
          break;
        case "Enter":
          e.preventDefault();
          if (filtered[focusedIndex]) execute(filtered[focusedIndex]);
          break;
        default:
          // Number shortcuts: 1-4 → navigate
          if (!query && /^[1-4]$/.test(e.key)) {
            const idx = parseInt(e.key) - 1;
            if (filtered[idx]) execute(filtered[idx]);
          }
          // Letter shortcuts
          const keyLower = e.key.toLowerCase();
          if (!query && keyLower === "g") {
            const cmd = commands.find((c) => c.id === "guided");
            if (cmd) execute(cmd);
          }
          if (!query && keyLower === "r") {
            const cmd = commands.find((c) => c.id === "reset");
            if (cmd) execute(cmd);
          }
          if (!query && keyLower === "o") {
            const cmd = commands.find((c) => c.id === "toggle-mode");
            if (cmd) execute(cmd);
          }
      }
    },
    [filtered, focusedIndex, query, commands, execute, close]
  );

  return {
    isOpen,
    open,
    close,
    toggle,
    query,
    setQuery,
    filtered,
    focusedIndex,
    setFocusedIndex,
    execute,
    recentIds,
    handleKeyDown,
    searchRef,
  };
}
