import { Link } from "react-router-dom";
import { ExternalLink } from "lucide-react";
import { cn } from "../../lib/utils";

export const DEFAULT_CHECKLIST_ITEMS = [
  { id: "signal_confirmed", label: "Strategy signal confirmed", checked: false },
  { id: "heat_limit_checked", label: "Position size within heat limits", checked: false },
  { id: "stop_defined", label: "Stop level defined", checked: false },
  { id: "research_reviewed", label: "Pre-trade research reviewed", checked: false },
];

function CheckItem({ item, onToggle, readOnly }) {
  return (
    <div
      className={cn(
        "flex items-center gap-3 px-3 py-2 rounded-lg transition-colors",
        !readOnly && "hover:bg-slate-700/30 cursor-pointer"
      )}
      onClick={!readOnly ? onToggle : undefined}
    >
      <div
        className={cn(
          "flex-shrink-0 w-4 h-4 rounded border-2 flex items-center justify-center transition-colors",
          item.checked
            ? "bg-cyan-500 border-cyan-500"
            : "border-slate-600 bg-transparent"
        )}
      >
        {item.checked && (
          <svg className="w-2.5 h-2.5 text-white" viewBox="0 0 10 10" fill="none">
            <path d="M1.5 5L4 7.5L8.5 2.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        )}
      </div>
      <span className={cn("text-sm select-none", item.checked ? "text-slate-300 line-through decoration-slate-500" : "text-slate-300")}>
        {item.label}
      </span>
    </div>
  );
}

export default function EntryChecklist({ items, ticker, onToggle, readOnly = false }) {
  const checkedCount = items.filter((i) => i.checked).length;
  const allChecked = items.length > 0 && checkedCount === items.length;

  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs text-slate-600 dark:text-slate-400">
          {checkedCount} / {items.length} complete
        </span>
        {allChecked && (
          <span className="text-xs font-medium text-emerald-400">All complete</span>
        )}
      </div>

      <div className="space-y-0.5">
        {items.map((item, idx) => (
          <CheckItem
            key={item.id}
            item={item}
            readOnly={readOnly}
            onToggle={!readOnly ? () => onToggle(idx) : undefined}
          />
        ))}
      </div>

      {ticker && (
        <div className="pt-2 pl-3">
          <Link
            to={`/research/${ticker}`}
            className="inline-flex items-center gap-1.5 text-xs text-cyan-400 hover:text-cyan-300 transition-colors"
          >
            <ExternalLink className="w-3 h-3" />
            Review research for {ticker}
          </Link>
        </div>
      )}
    </div>
  );
}
