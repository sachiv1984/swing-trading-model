import { AlertCircle, Loader2 } from "lucide-react";
import { Link } from "react-router-dom";
import { cn } from "../../../lib/utils";
import DataState from "../../ui/DataState";

export default function DashboardCard({
  title,
  to,
  isLoading,
  error,
  empty,
  emptyIcon,
  emptyHeading,
  emptyBody,
  children,
  className,
  descriptions = [],
}) {
  // ST-09 (BLG-FE-264, EPIC-03, v9.16): shell on the semantic colour tokens
  // (design_system.md v1.25 §Semantic Colour Tokens rule 5). The hover fill
  // keeps an explicit pair because tokens take no opacity modifier (rule 2).
  const content = (
    <div className={cn(
      "relative rounded-2xl bg-app-raised border border-app-line backdrop-blur-sm p-6 transition-all hover:border-slate-300 hover:bg-slate-50 dark:hover:border-slate-600/70 dark:hover:bg-slate-800/70 cursor-pointer h-full",
      className
    )}>
      <p className="text-xs text-app-fg uppercase tracking-wider mb-3">{title}</p>

      {isLoading && (
        <div className="flex justify-center py-4">
          <Loader2 className="w-5 h-5 animate-spin text-slate-500" />
        </div>
      )}

      {!isLoading && error && (
        <div className="flex items-center gap-2 text-app-negative">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span className="text-sm">Unable to load</span>
        </div>
      )}

      {!isLoading && !error && empty && (
        <DataState
          compact
          empty
          emptyIcon={emptyIcon}
          emptyHeading={emptyHeading}
          emptyBody={emptyBody}
        />
      )}

      {!isLoading && !error && !empty && children}
      {descriptions.map(({ id, text }) => (
        <span key={id} id={id} className="sr-only">{text}</span>
      ))}
    </div>
  );

  const describedBy = descriptions.map(({ id }) => id).join(" ") || undefined;
  return to ? <Link to={to} className="block h-full" aria-describedby={describedBy}>{content}</Link> : content;
}
