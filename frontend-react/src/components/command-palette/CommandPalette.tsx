// ============================================================
// MuleShield — Command Palette
//
// Raycast/Linear-style command palette:
// - Centered modal with backdrop blur
// - Full keyboard navigation (↑↓ Enter Escape shortcuts)
// - Search with instant filtering
// - Categorized commands
// - Recent actions
// - Focus trap
// - Accessible (role=dialog, aria-modal, listbox)
// ============================================================

import React, { memo, useEffect, useRef } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Search } from "lucide-react";
import type { Command } from "../../hooks/useCommandPalette";

interface CommandItemProps {
  command: Command;
  isFocused: boolean;
  onClick: () => void;
  onMouseEnter: () => void;
}

const CommandItem = memo(function CommandItem({
  command,
  isFocused,
  onClick,
  onMouseEnter,
}: CommandItemProps) {
  const ref = useRef<HTMLButtonElement>(null);
  const Icon = command.icon;

  // Scroll focused item into view
  useEffect(() => {
    if (isFocused) {
      ref.current?.scrollIntoView({ block: "nearest" });
    }
  }, [isFocused]);

  return (
    <button
      ref={ref}
      role="option"
      aria-selected={isFocused}
      className={`cmd-item${isFocused ? " focused" : ""}`}
      onClick={onClick}
      onMouseEnter={onMouseEnter}
      tabIndex={-1}
    >
      <span className="cmd-item-icon" aria-hidden="true">
        <Icon size={14} />
      </span>
      <span className="cmd-item-label">{command.label}</span>
      {command.shortcut && (
        <span className="cmd-item-shortcut" aria-hidden="true">
          {command.shortcut.map((key) => (
            <kbd key={key}>{key}</kbd>
          ))}
        </span>
      )}
    </button>
  );
});

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  query: string;
  onQueryChange: (q: string) => void;
  filteredCommands: Command[];
  allCommands: Command[];
  focusedIndex: number;
  setFocusedIndex: (i: number) => void;
  onExecute: (cmd: Command) => void;
  recentIds: string[];
  onKeyDown: (e: React.KeyboardEvent) => void;
  searchRef: React.RefObject<HTMLInputElement | null>;
}

export const CommandPalette = memo(function CommandPalette({
  isOpen,
  onClose,
  query,
  onQueryChange,
  filteredCommands,
  allCommands,
  focusedIndex,
  setFocusedIndex,
  onExecute,
  recentIds,
  onKeyDown,
  searchRef,
}: CommandPaletteProps) {
  // Group commands by category
  const grouped = filteredCommands.reduce<Record<string, Command[]>>(
    (acc, cmd) => {
      if (!acc[cmd.category]) acc[cmd.category] = [];
      acc[cmd.category].push(cmd);
      return acc;
    },
    {}
  );

  // Recent commands (only show if no active query)
  const recentCommands = !query
    ? recentIds
        .map((id) => allCommands.find((c) => c.id === id))
        .filter(Boolean as unknown as <T>(v: T | undefined) => v is T)
    : [];

  // Build a flat ordered index for keyboard nav
  let globalIndex = 0;
  const categoryOrder = Object.keys(grouped);

  return (
    <AnimatePresence>
      {isOpen && (
        <div
          className="modal-overlay"
          onClick={onClose}
          aria-hidden="true"
        >
          <motion.div
            role="dialog"
            aria-modal="true"
            aria-label="Command palette"
            className="cmd-palette-box"
            initial={{ opacity: 0, scale: 0.96, y: -8 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.96, y: -8 }}
            transition={{ duration: 0.15, ease: [0.16, 1, 0.3, 1] }}
            onClick={(e) => e.stopPropagation()}
            onKeyDown={onKeyDown}
          >
            {/* Search */}
            <div className="cmd-search-row">
              <Search size={16} color="var(--color-text-subtle)" aria-hidden="true" />
              <input
                ref={searchRef as React.RefObject<HTMLInputElement>}
                className="cmd-search-input"
                placeholder="Search commands..."
                value={query}
                onChange={(e) => onQueryChange(e.target.value)}
                aria-label="Search commands"
                aria-autocomplete="list"
                aria-controls="cmd-listbox"
                autoComplete="off"
                spellCheck={false}
              />
              <kbd>Esc</kbd>
            </div>

            {/* List */}
            <div
              className="cmd-body"
              id="cmd-listbox"
              role="listbox"
              aria-label="Available commands"
            >
              {/* Recent */}
              {recentCommands.length > 0 && (
                <>
                  <p className="cmd-category">Recent</p>
                  {recentCommands.map((cmd) => {
                    const gi = globalIndex++;
                    return (
                      <CommandItem
                        key={cmd.id}
                        command={cmd}
                        isFocused={focusedIndex === gi}
                        onClick={() => onExecute(cmd)}
                        onMouseEnter={() => setFocusedIndex(gi)}
                      />
                    );
                  })}
                  {categoryOrder.length > 0 && (
                    <div className="cmd-divider" aria-hidden="true" />
                  )}
                </>
              )}

              {/* Grouped */}
              {categoryOrder.map((category, catIdx) => (
                <div key={category}>
                  {catIdx > 0 && (
                    <div className="cmd-divider" aria-hidden="true" />
                  )}
                  <p className="cmd-category">{category}</p>
                  {grouped[category].map((cmd) => {
                    const gi = globalIndex++;
                    return (
                      <CommandItem
                        key={cmd.id}
                        command={cmd}
                        isFocused={focusedIndex === gi}
                        onClick={() => onExecute(cmd)}
                        onMouseEnter={() => setFocusedIndex(gi)}
                      />
                    );
                  })}
                </div>
              ))}

              {filteredCommands.length === 0 && (
                <p
                  style={{
                    padding: "var(--space-6) var(--space-5)",
                    color: "var(--color-text-muted)",
                    fontSize: "var(--text-sm)",
                    textAlign: "center",
                  }}
                >
                  No commands match "{query}"
                </p>
              )}
            </div>

            {/* Footer hints */}
            <div className="cmd-footer" aria-hidden="true">
              <span className="cmd-footer-hint">
                <kbd>↑↓</kbd> Navigate
              </span>
              <span className="cmd-footer-hint">
                <kbd>↵</kbd> Select
              </span>
              <span className="cmd-footer-hint">
                <kbd>Esc</kbd> Close
              </span>
              <span
                className="cmd-footer-hint"
                style={{ marginLeft: "auto" }}
              >
                <kbd>⌃K</kbd> Toggle
              </span>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
});
