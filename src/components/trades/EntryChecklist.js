import { Link } from "react-router-dom";
import { ExternalLink } from "lucide-react";
import { format } from "date-fns";
import { cn } from "../../lib/utils";
import {
  SIZE_ITEM_LABEL,
  judgementItems,
  positionSizeText,
  stopLevel,
  stopText,
} from "../../lib/checklistStatus";

export const DEFAULT_CHECKLIST_ITEMS = [
  { id: "signal_confirmed", label: "Strategy signal confirmed", checked: false },
  // trade_plan.md v1.30 §6.2 (ST-12): was "Position size within heat limits";
  // strategy_rules.md has no heat limit (Product Owner decision 2026-11-18).
  { id: "heat_limit_checked", label: SIZE_ITEM_LABEL, checked: false },
  { id: "stop_defined", label: "Stop level defined", checked: false },
  { id: "research_reviewed", label: "Pre-trade research reviewed", checked: false },
];

function CheckItem({ item, onToggle, readOnly }) {
  const handleKeyDown = (e) => {
    if (readOnly) return;
    if (e.key === " " || e.key === "Enter") {
      e.preventDefault();
      onToggle();
    }
  };

  return (
    <div
      role="checkbox"
      aria-checked={item.checked}
      tabIndex={readOnly ? -1 : 0}
      data-testid={`entry-checklist-item-${item.id}`}
      className={cn(
        "flex items-center gap-3 px-3 py-2 rounded-lg transition-colors",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
        !readOnly && "hover:bg-slate-100 dark:hover:bg-slate-700/30 cursor-pointer"
      )}
      onClick={!readOnly ? onToggle : undefined}
      onKeyDown={handleKeyDown}
    >
      <div
        className={cn(
          "flex-shrink-0 w-4 h-4 rounded border-2 flex items-center justify-center transition-colors",
          item.checked
            ? "bg-cyan-500 border-cyan-500"
            : "border-slate-300 dark:border-slate-600 bg-transparent"
        )}
      >
        {item.checked && (
          <svg className="w-2.5 h-2.5 text-white" viewBox="0 0 10 10" fill="none">
            <path d="M1.5 5L4 7.5L8.5 2.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        )}
      </div>
      <span className={cn("text-sm select-none", item.checked ? "text-slate-700 dark:text-slate-300 line-through decoration-slate-500" : "text-slate-700 dark:text-slate-300")}>
        {item.label}
      </span>
    </div>
  );
}

const STATUS_CLASS = {
  pass: "text-app-positive",
  warn: "text-app-warning",
  fail: "text-app-negative",
  none: "text-app-muted",
};

// A system-checked row (trade_plan.md v1.30 §6.2): plain text, not focusable,
// cannot be ticked; the glyph and word always accompany the colour.
function StatusRow({ id, label, text, tone }) {
  return (
    <div className="flex items-center justify-between gap-3 px-3 py-2" data-testid={`entry-checklist-status-${id}`}>
      <span className="text-sm text-slate-700 dark:text-slate-300">{label}</span>
      <span className={cn("text-sm font-medium", STATUS_CLASS[tone])} data-testid={`entry-checklist-status-${id}-text`}>
        {text}
      </span>
    </div>
  );
}

function capturedCaption(savedAt) {
  if (!savedAt) return null;
  const d = new Date(savedAt);
  return Number.isNaN(d.getTime()) ? null : `As checked when the plan was saved, ${format(d, "d MMM HH:mm")}`;
}

// trade_plan.md v1.30 §6 (ST-12, BLG-UX-19): two groups. "Checked by the
// system" shows Position size checks (the worst of the cash, sector and sizing
// pre-entry checks: `sizeStatus`) and Stop level defined (`stopValue`) as
// status. "Your judgement" keeps the two tickable items. Read-only (the plan
// detail on Research) reads the plan's stored snapshot and stop: `savedAt` is
// the snapshot's captured_at.
export default function EntryChecklist({ items, ticker, onToggle, readOnly = false, sizeStatus = null, stopValue = null, market = "US", savedAt = null }) {
  const judged = judgementItems(items);
  const checkedCount = judged.filter(({ item }) => item.checked).length;
  const allChecked = judged.length > 0 && checkedCount === judged.length;
  const stopSet = stopLevel(stopValue) !== null;
  const caption = readOnly ? capturedCaption(savedAt) : null;

  return (
    <div className="space-y-3">
      <div data-testid="checklist-system" className="space-y-0.5">
        <p className="text-xs font-medium text-slate-600 dark:text-slate-400">Checked by the system</p>
        <StatusRow
          id="heat_limit_checked"
          label={SIZE_ITEM_LABEL}
          text={positionSizeText(sizeStatus, { readOnly })}
          tone={sizeStatus || "none"}
        />
        {/* The caption dates the stored check result, so it sits under the size
            row only; the stop row reads the plan's current Stop Level. */}
        {caption && (
          <p className="px-3 text-xs text-slate-600 dark:text-slate-400" data-testid="checklist-captured-at">{caption}</p>
        )}
        <StatusRow
          id="stop_defined"
          label="Stop level defined"
          text={stopText(stopValue, market)}
          tone={stopSet ? "pass" : "fail"}
        />
      </div>

      <div data-testid="checklist-human" className="space-y-1">
        <div className="flex items-center justify-between mb-2">
          <p className="text-xs font-medium text-slate-600 dark:text-slate-400">Your judgement</p>
          <span className="text-xs text-slate-600 dark:text-slate-400" data-testid="checklist-counter">
            {allChecked ? (
              <span className="font-medium text-app-positive">{judged.length === 2 ? "Both confirmed" : "All confirmed"}</span>
            ) : (
              `${checkedCount} / ${judged.length} confirmed`
            )}
          </span>
        </div>

        <div className="space-y-0.5">
          {judged.map(({ item, index }) => (
            <CheckItem
              key={item.id}
              item={item}
              readOnly={readOnly}
              onToggle={!readOnly ? () => onToggle(index) : undefined}
            />
          ))}
        </div>
      </div>

      {ticker && (
        <div className="pl-3">
          <Link
            to={`/research/${ticker}`}
            className="inline-flex items-center gap-1.5 text-xs text-cyan-700 dark:text-cyan-400 hover:text-cyan-800 dark:hover:text-cyan-300 transition-colors"
          >
            <ExternalLink className="w-3 h-3" />
            Review research for {ticker}
          </Link>
        </div>
      )}
    </div>
  );
}
