import { Loader2, AlertCircle } from "lucide-react";
import { Button } from "./button";
import { Skeleton } from "./skeleton";

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
 *
 * Pass `errorHeading`/`errorBody` to override the default "Something went
 * wrong" / "Unable to load data. Please try again." copy for a context where
 * a more specific message is warranted (e.g. "Unable to load release notes",
 * ST-01/EPIC-01/v7.8). Both default to the original strings, so existing
 * call sites are unaffected.
 *
 * Pass `loadingVariant="skeleton"` (default remains `"spinner"`, unchanged)
 * plus a `loadingSkeleton` node to render a content-shaped placeholder
 * instead of the centered spinner for card-shaped async regions (v1.7,
 * ST-13, EPIC-03, v8.3, BLG-FE-126 — design_system.md §Shared UI Components
 * → Data States → Skeleton loading variant). If `loadingSkeleton` is
 * omitted, a default 3-bar composition renders (title + 2 body lines) — a
 * starting point, not a mandate; compose your own bars from the shared
 * `Skeleton` primitive (`src/components/ui/skeleton.js`) for a different
 * shape. Not retrofitted to any existing card this cycle — adoption is
 * per-consumer, going forward.
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
  errorHeading = "Something went wrong",
  errorBody = "Unable to load data. Please try again.",
  loadingVariant = "spinner",
  loadingSkeleton = null,
}) {
  if (loading) {
    if (loadingVariant === "skeleton") {
      return (
        <div className={`${compact ? "py-4" : "py-6"} ${className}`} data-testid="data-state-skeleton">
          {loadingSkeleton || (
            <div className="space-y-2">
              <Skeleton className="h-4 w-3/5 bg-slate-300/60 dark:bg-slate-700/60" />
              <Skeleton className="h-3 w-full bg-slate-300/60 dark:bg-slate-700/60" />
              <Skeleton className="h-3 w-4/5 bg-slate-300/60 dark:bg-slate-700/60" />
            </div>
          )}
        </div>
      );
    }
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
          <p className="text-sm font-semibold text-white mb-1">{errorHeading}</p>
          <p className="text-xs text-slate-600 dark:text-slate-400">
            {errorBody}
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
