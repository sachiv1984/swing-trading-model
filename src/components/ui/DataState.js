import { Loader2, AlertCircle } from "lucide-react";
import { Button } from "./button";

/**
 * DataState — canonical three-state wrapper for API-backed components.
 *
 * States (evaluated in priority order):
 *   1. loading — centered spinner, no skeleton
 *   2. error   — error icon + "Something went wrong" + retry button
 *   3. empty   — neutral icon + descriptive heading + body + optional CTA
 *   4. (else)  — render children
 *
 * Usage:
 *   <DataState
 *     loading={isLoading}
 *     error={isError}
 *     onRetry={refetch}
 *     empty={data.length === 0}
 *     emptyIcon={<InboxIcon className="w-10 h-10 text-slate-600" />}
 *     emptyHeading="No positions open"
 *     emptyBody="Open a position to see it here."
 *     emptyAction={<Button>Add trade</Button>}
 *   >
 *     {children}
 *   </DataState>
 *
 * Pass `compact` for smaller contexts (e.g. a dashboard grid tile) where the
 * default py-16 empty-state padding would exaggerate tile height — reduces
 * padding/icon size while keeping the same state logic and visual language.
 *
 * Pass `inline` for a compact-list context (e.g. inside a command palette or
 * other single-line result list) where even `compact`'s icon+heading+body
 * stack is too tall — renders `emptyHeading` (or `emptyBody`) alone as a
 * single centered text line, no icon. `loading`/`error` are unaffected.
 */
export default function DataState({
  loading,
  error,
  onRetry,
  empty,
  emptyIcon,
  emptyHeading,
  emptyBody,
  emptyAction,
  children,
  className = "",
  compact = false,
  inline = false,
}) {
  if (loading) {
    return (
      <div className={`flex items-center justify-center ${compact ? "py-4" : "py-16"} ${className}`}>
        <Loader2 className={`${compact ? "w-5 h-5" : "w-8 h-8"} animate-spin text-slate-500`} />
      </div>
    );
  }

  if (error) {
    return (
      <div className={`flex flex-col items-center justify-center ${compact ? "py-4 gap-2" : "py-16 gap-4"} text-center px-6 ${className}`}>
        <AlertCircle className={`${compact ? "w-6 h-6" : "w-10 h-10"} text-rose-400`} />
        <div>
          <p className="text-sm font-semibold text-white mb-1">Something went wrong</p>
          <p className="text-xs text-slate-600 dark:text-slate-400">
            Unable to load data. Please try again.
          </p>
        </div>
        {onRetry && (
          <Button
            variant="outline"
            size="sm"
            onClick={onRetry}
            className="bg-slate-800/50 border-slate-700 text-slate-300 hover:text-white"
          >
            Try again
          </Button>
        )}
      </div>
    );
  }

  if (empty) {
    if (inline) {
      return (
        <p className={`text-sm text-slate-600 dark:text-slate-400 text-center py-6 ${className}`}>
          {emptyHeading || emptyBody}
        </p>
      );
    }
    return (
      <div className={`flex flex-col items-center justify-center ${compact ? "py-4 gap-2" : "py-16 gap-3"} text-center px-6 ${className}`}>
        {emptyIcon && <div className="mb-1">{emptyIcon}</div>}
        {emptyHeading && (
          <p className="text-sm font-semibold text-white">{emptyHeading}</p>
        )}
        {emptyBody && (
          <p className="text-xs text-slate-600 dark:text-slate-400">{emptyBody}</p>
        )}
        {emptyAction && <div className="mt-2">{emptyAction}</div>}
      </div>
    );
  }

  return children;
}
