/**
 * MetricsStalenessIndicator — ST-02 (BLG-FEAT-09, v2.3)
 *
 * Displays data freshness on Analytics and Portfolio/Positions pages.
 * Fetches last_sync_at from GET /analytics/metrics and renders:
 *   - Fresh  (<4h): grey secondary text "Data as of N mins ago"
 *   - Stale (≥4h): amber badge "⚠ Data as of Nh ago — may be outdated"
 *   - Absent/null: renders nothing
 *
 * Hover tooltip shows absolute ISO timestamp in both states.
 *
 * Spec: docs/specs/frontend/pages/analytics.md §Metrics Staleness Indicator
 * UX:   docs/design/2026-03-24__release-v2.3/staleness-indicator/ux_spec.md
 */

import { useQuery } from "@tanstack/react-query";
import { AlertTriangle, Clock } from "lucide-react";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "../ui/tooltip";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";
const STALE_THRESHOLD_MS = 4 * 60 * 60 * 1000; // 4 hours

/**
 * Compute human-readable relative time string from a UTC ISO timestamp.
 * Rules per UX spec:
 *   < 1 min  → "just now"
 *   1–59 min → "N mins ago"
 *   1–23 h   → "Nh ago"
 *   ≥ 24 h   → "N days ago"
 */
function formatRelativeTime(isoString) {
  const syncTime = new Date(isoString);
  const nowMs = Date.now();
  const diffMs = nowMs - syncTime.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMs < 60000) return "just now";
  if (diffMins < 60) return `${diffMins} mins ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  return `${diffDays} days ago`;
}

/**
 * Format absolute ISO timestamp for tooltip display.
 * Output: "Updated: 2026-03-24 09:41 UTC"
 */
function formatAbsoluteTime(isoString) {
  const d = new Date(isoString);
  const year = d.getUTCFullYear();
  const month = String(d.getUTCMonth() + 1).padStart(2, "0");
  const day = String(d.getUTCDate()).padStart(2, "0");
  const hours = String(d.getUTCHours()).padStart(2, "0");
  const mins = String(d.getUTCMinutes()).padStart(2, "0");
  return `Updated: ${year}-${month}-${day} ${hours}:${mins} UTC`;
}

export default function MetricsStalenessIndicator() {
  const { data: lastSyncAt } = useQuery({
    queryKey: ["analyticsLastSyncAt"],
    queryFn: async () => {
      try {
        const response = await fetch(`${API_URL}/analytics/metrics`, {
          credentials: "include",
        });
        if (!response.ok) return null;
        const result = await response.json();
        return result?.data?.last_sync_at ?? null;
      } catch {
        return null;
      }
    },
    staleTime: 5 * 60 * 1000,
    retry: false,
  });

  if (!lastSyncAt) return null;

  const diffMs = Date.now() - new Date(lastSyncAt).getTime();
  const isStale = diffMs >= STALE_THRESHOLD_MS;
  const relativeTime = formatRelativeTime(lastSyncAt);
  const absoluteTime = formatAbsoluteTime(lastSyncAt);

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          {isStale ? (
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-amber-500/15 border border-amber-500/30 text-amber-400 text-xs font-medium cursor-default select-none">
              <AlertTriangle className="w-3 h-3 shrink-0" />
              Data as of {relativeTime} — may be outdated
            </span>
          ) : (
            <span className="inline-flex items-center gap-1.5 text-slate-400 text-xs cursor-default select-none">
              <Clock className="w-3 h-3 shrink-0 text-slate-500" />
              Data as of {relativeTime}
            </span>
          )}
        </TooltipTrigger>
        <TooltipContent
          side="bottom"
          className="bg-slate-800 border-slate-700 text-slate-200 text-xs"
        >
          {absoluteTime}
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
