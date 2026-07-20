import { useState } from "react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { X, AlertTriangle, ChevronDown, ChevronUp } from "lucide-react";
import { cn } from "../../lib/utils";

const TAG_MAX_LENGTH = 20;
const TAG_MAX_COUNT = 10;
const TAG_RE = /^[a-z0-9-]+$/;

function cleanTag(raw) {
  return (raw || "").trim().toLowerCase().replace(/\s+/g, "-");
}

/**
 * Generic bulk-action toolbar for row-multi-select tables (ST-03, BLG-FE-117,
 * EPIC-03, v7.5). Renders only when 1+ rows are selected — the toolbar's
 * presence is itself the selected-state indicator (no "0 selected" state,
 * per bulk-actions-toolbar/ux_spec.md §2.2 / readiness pass AC-05).
 *
 * `tagAction` and `destructiveActions[].onConfirm`/`tagAction.onSubmit` must
 * return a Promise<{succeeded: string[], failed: [{id, reason}]}> per the
 * readiness pass AC-01 response shape. This component only renders the
 * toolbar/confirm/toast UI — the parent owns selection state and list refresh
 * via the `onResult` callback.
 */
export default function BulkActionToolbar({
  selectedCount,
  onClear,
  itemLabel = "items",
  tagAction = null,
  destructiveActions = [],
  excludedNote = null,
  onResult,
}) {
  const [showTagForm, setShowTagForm] = useState(false);
  const [tagInput, setTagInput] = useState("");
  const [pendingTags, setPendingTags] = useState([]);
  const [confirmingKey, setConfirmingKey] = useState(null);
  const [submittingKey, setSubmittingKey] = useState(null);
  const [toast, setToast] = useState(null);
  const [showFailedDetail, setShowFailedDetail] = useState(false);

  // Toolbar body (selected-count/actions) is absent at zero-selected per
  // ux_spec.md §2.2 — but a just-shown result toast must survive the
  // selection being cleared after a successful bulk action, or the toast
  // would vanish before the user ever sees it.
  if (selectedCount === 0 && !toast) return null;

  const handleAddTag = () => {
    const clean = cleanTag(tagInput);
    if (!clean || pendingTags.length >= TAG_MAX_COUNT) return;
    if (clean.length > TAG_MAX_LENGTH || !TAG_RE.test(clean)) return;
    if (pendingTags.includes(clean)) return;
    setPendingTags((prev) => [...prev, clean]);
    setTagInput("");
  };

  const handleTagKeyDown = (e) => {
    if (e.key === "Enter" || e.key === ",") {
      e.preventDefault();
      handleAddTag();
    }
  };

  const buildToast = (result) => {
    const succeededCount = result.succeeded.length;
    const failedCount = result.failed.length;
    if (failedCount === 0) {
      return { message: `${succeededCount} ${itemLabel} updated.`, failed: [] };
    }
    return {
      message: `${succeededCount} succeeded, ${failedCount} failed.`,
      failed: result.failed,
    };
  };

  const handleTagSubmit = async () => {
    if (!tagAction || pendingTags.length === 0) return;
    setSubmittingKey("tag");
    try {
      const result = await tagAction.onSubmit(pendingTags);
      setToast(buildToast(result));
      setShowTagForm(false);
      setPendingTags([]);
      setTagInput("");
      onResult?.(result, "tag");
    } finally {
      setSubmittingKey(null);
    }
  };

  const handleDestructiveConfirm = async (action) => {
    setSubmittingKey(action.key);
    try {
      const result = await action.onConfirm();
      setToast(buildToast(result));
      setConfirmingKey(null);
      onResult?.(result, action.key);
    } finally {
      setSubmittingKey(null);
    }
  };

  const confirmingAction = destructiveActions.find((a) => a.key === confirmingKey);

  return (
    <div className="rounded-xl bg-gradient-to-r from-cyan-500/10 to-violet-500/10 border border-cyan-500/20 mb-4">
      {selectedCount > 0 && (
      <div className="flex items-center justify-between px-4 py-3 flex-wrap gap-2">
        <div className="flex items-center gap-3 flex-wrap">
          <span className="text-sm font-semibold text-white">{selectedCount} selected</span>

          {tagAction && (
            <Button
              size="sm"
              variant="outline"
              onClick={() => setShowTagForm((v) => !v)}
              className="h-7 bg-slate-800/50 border-slate-700 text-slate-300 hover:text-white text-xs"
            >
              Bulk Tag
            </Button>
          )}

          {destructiveActions.map((action) => (
            <Button
              key={action.key}
              size="sm"
              variant="outline"
              onClick={() => setConfirmingKey(action.key)}
              className="h-7 bg-slate-800/50 border-slate-700 text-rose-400 hover:text-rose-300 hover:bg-rose-500/10 text-xs"
            >
              {action.label}
            </Button>
          ))}

          {excludedNote && (
            <span className="text-xs text-amber-400">{excludedNote}</span>
          )}
        </div>

        <Button
          size="sm"
          variant="ghost"
          onClick={onClear}
          className="h-7 text-slate-600 dark:text-slate-400 hover:text-white text-xs"
        >
          Clear
        </Button>
      </div>
      )}

      {selectedCount > 0 && showTagForm && tagAction && (
        <div className="px-4 pb-4 space-y-2 border-t border-cyan-500/10 pt-3">
          <div className="flex flex-wrap gap-1.5">
            {pendingTags.map((tag) => (
              <span
                key={tag}
                className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-slate-700/60 text-xs text-slate-200"
              >
                {tag}
                <button onClick={() => setPendingTags((prev) => prev.filter((t) => t !== tag))}>
                  <X className="w-3 h-3" />
                </button>
              </span>
            ))}
          </div>
          <div className="flex gap-2 items-center">
            <Input
              value={tagInput}
              onChange={(e) => setTagInput(e.target.value)}
              onKeyDown={handleTagKeyDown}
              placeholder="Add a tag and press Enter"
              list={tagAction.tagOptions?.length ? "bulk-tag-options" : undefined}
              className="bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-600 dark:text-slate-400 h-8 text-sm max-w-xs"
            />
            {tagAction.tagOptions?.length > 0 && (
              <datalist id="bulk-tag-options">
                {tagAction.tagOptions.map((t) => (
                  <option key={t} value={t} />
                ))}
              </datalist>
            )}
            <Button
              size="sm"
              onClick={handleTagSubmit}
              disabled={pendingTags.length === 0 || submittingKey === "tag"}
              className="h-8 bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 text-xs"
            >
              {submittingKey === "tag" ? "Applying…" : "Apply Tags"}
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => { setShowTagForm(false); setPendingTags([]); setTagInput(""); }}
              className="h-8 text-slate-600 dark:text-slate-400 hover:text-white text-xs"
            >
              Cancel
            </Button>
          </div>
        </div>
      )}

      {confirmingAction && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
          <div className="w-full max-w-md rounded-2xl bg-slate-900 border border-slate-700 p-6 space-y-4 mx-4">
            <div className="flex items-center gap-3">
              <AlertTriangle className="w-5 h-5 text-rose-400 flex-shrink-0" />
              <h2 className="text-lg font-semibold text-white">{confirmingAction.confirmText}</h2>
            </div>
            <div className="flex gap-3 justify-end">
              <Button
                variant="ghost"
                onClick={() => setConfirmingKey(null)}
                className="text-slate-600 dark:text-slate-400"
              >
                Cancel
              </Button>
              <Button
                onClick={() => handleDestructiveConfirm(confirmingAction)}
                disabled={submittingKey === confirmingAction.key}
                className="bg-rose-600 hover:bg-rose-500 text-white border-0"
              >
                {submittingKey === confirmingAction.key ? "Working…" : confirmingAction.label}
              </Button>
            </div>
          </div>
        </div>
      )}

      {toast && (
        <div className="px-4 pb-3">
          <div className={cn(
            "rounded-lg px-3 py-2 text-xs flex flex-col gap-1",
            toast.failed.length > 0 ? "bg-amber-500/10 text-amber-300" : "bg-emerald-500/10 text-emerald-300"
          )}>
            <div className="flex items-center justify-between">
              <span>{toast.message}</span>
              <div className="flex items-center gap-2">
                {toast.failed.length > 0 && (
                  <button onClick={() => setShowFailedDetail((v) => !v)} className="flex items-center gap-0.5">
                    Details {showFailedDetail ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                  </button>
                )}
                <button onClick={() => { setToast(null); setShowFailedDetail(false); }}>
                  <X className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
            {showFailedDetail && toast.failed.length > 0 && (
              <ul className="mt-1 space-y-0.5">
                {toast.failed.map((f) => (
                  <li key={f.id}>{f.id}: {f.reason}</li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
