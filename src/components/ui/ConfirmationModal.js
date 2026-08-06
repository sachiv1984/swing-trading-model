'use strict';

/**
 * Shared modal-confirmation component (ST-12, BLG-FE-121, EPIC-03, v8.3).
 *
 * Decision record: docs/design/2026-08-05__release-v8.3/shared-confirmation-modal-undo-window/decision_record.md
 * Template library entry: docs/specs/frontend/base44_prompt_template_library.md §10
 *
 * Two variants, selected via `undoWindow.enabled`:
 *
 *  - Standard (default, undoWindow.enabled = false): the modal opens, Confirm
 *    executes `onConfirm` and closes the modal, Cancel dismisses without
 *    action. This formalises the existing shipped confirmation-modal
 *    precedent (positions.md §Exit action, watchlist.md §Remove Confirmation
 *    Prompt) — no new interaction here.
 *
 *  - Undo-window (undoWindow.enabled = true): Confirm closes the modal
 *    immediately and runs `onConfirm` optimistically. A toast then shows
 *    `actionText` (the action's past-tense confirmation line, e.g.
 *    "3 positions removed.") alongside a live "Undo (Ns)" countdown button.
 *    Clicking Undo before the window expires calls `onUndo` and replaces the
 *    toast with a brief "Undone." confirmation; letting the window expire
 *    dismisses the toast silently and the action is final.
 *
 * `actionText`/`onUndo` are the implementation-level props the decision
 * record's props table doesn't spell out by name (it only documents
 * `undoWindow.enabled`/`durationSeconds`) — they exist to realise §4's
 * described interaction and may be refined once a real consumer
 * (BLG-FE-116/BLG-FE-117) lands; no consumer references this component yet.
 */

import { useEffect, useState } from "react";
import { toast } from "sonner";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "./dialog";
import { Button } from "./button";

export default function ConfirmationModal({
  open,
  onOpenChange,
  message,
  confirmLabel = "Confirm",
  cancelLabel = "Cancel",
  destructive = false,
  undoWindow = { enabled: false },
  onConfirm,
  onUndo,
  actionText,
  undoneMessage = "Undone.",
}) {
  const handleCancel = () => onOpenChange(false);

  const handleConfirm = () => {
    onOpenChange(false);
    onConfirm?.();

    if (undoWindow.enabled) {
      const durationSeconds = undoWindow.durationSeconds ?? 5;
      toast.custom(
        (t) => (
          <UndoToastBody
            toastId={t}
            durationSeconds={durationSeconds}
            actionText={actionText}
            onUndo={onUndo}
            undoneMessage={undoneMessage}
          />
        ),
        { duration: durationSeconds * 1000 }
      );
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="w-full max-w-sm bg-slate-900 border-slate-700 text-white">
        <DialogHeader>
          <DialogTitle className="text-base font-semibold text-white" data-testid="confirmation-modal-message">
            {message}
          </DialogTitle>
        </DialogHeader>
        <DialogFooter>
          <Button
            variant="ghost"
            onClick={handleCancel}
            className="text-slate-600 dark:text-slate-400"
            data-testid="confirmation-modal-cancel"
          >
            {cancelLabel}
          </Button>
          <Button
            variant={destructive ? "destructive" : "default"}
            onClick={handleConfirm}
            data-testid="confirmation-modal-confirm"
          >
            {confirmLabel}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

function UndoToastBody({ toastId, durationSeconds, actionText, onUndo, undoneMessage }) {
  const [remaining, setRemaining] = useState(durationSeconds);

  useEffect(() => {
    if (remaining <= 0) return undefined;
    const timer = setTimeout(() => setRemaining((r) => r - 1), 1000);
    return () => clearTimeout(timer);
  }, [remaining]);

  const handleUndo = () => {
    toast.dismiss(toastId);
    onUndo?.();
    toast.success(undoneMessage);
  };

  return (
    <div
      className="flex items-center gap-3 bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-sm text-white shadow-lg"
      data-testid="undo-toast"
    >
      {actionText && <span className="flex-1">{actionText}</span>}
      <button
        onClick={handleUndo}
        className="shrink-0 text-xs font-semibold px-3 py-1.5 rounded-md border border-slate-600 text-slate-200 hover:bg-slate-700"
        data-testid="undo-toast-button"
      >
        {`Undo (${remaining}s)`}
      </button>
    </div>
  );
}
