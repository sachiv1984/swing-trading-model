import { useQuery } from "@tanstack/react-query";
import { Sparkles } from "lucide-react";
import { api } from "../../../api/base44Client";
import DataState from "../../ui/DataState";

const MAX_BULLETS = 8;

/**
 * In-app "What's New" panel (ST-01, EPIC-01, v7.8, BLG-FE-128).
 *
 * Full-width secondary-tier card below the Gate Progress Indicator strip
 * (dashboard.md §6A). Shows the most recent release's changelog entries,
 * parsed server-side by GET /changelog/latest — no hardcoded copy, so a
 * new release is picked up automatically with no manual wiring.
 *
 * Display-only: no dismiss/collapse, no click-through, no navigation.
 */
export default function WhatsNewCard() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["home-whats-new"],
    queryFn: () => api.changelog.latest(),
    retry: 1,
  });

  // api.changelog.latest() -> doFetch() already unwraps the {status, data}
  // envelope, so `data` here IS the {version, changes} payload directly
  // (or null) -- not a further-nested `data.data`.
  const entry = data;
  const changes = entry?.changes || [];
  const visible = changes.slice(0, MAX_BULLETS);
  const overflowCount = changes.length - MAX_BULLETS;

  return (
    <div
      className="rounded-2xl bg-slate-800/50 border border-slate-700/50 backdrop-blur-sm p-6"
      data-testid="whats-new-card"
    >
      <div className="flex items-center gap-2 mb-4">
        <Sparkles className="w-4 h-4 text-slate-500" />
        <h2 className="text-sm font-semibold text-white">
          {entry ? `What's New — ${entry.version}` : "What's New"}
        </h2>
      </div>

      <DataState
        loading={isLoading}
        error={!!error}
        errorHeading="Unable to load release notes"
        empty={!isLoading && !error && changes.length === 0}
        emptyHeading="Nothing to show"
        emptyBody="Check back after the next release."
      >
        <ul className="space-y-2">
          {visible.map((description, i) => (
            <li key={i} className="flex gap-2 text-sm text-slate-600 dark:text-slate-400">
              <span className="text-slate-600 dark:text-slate-400 shrink-0">•</span>
              <span>{description}</span>
            </li>
          ))}
          {overflowCount > 0 && (
            <li className="text-xs text-slate-600 dark:text-slate-400 pl-4">+{overflowCount} more</li>
          )}
        </ul>
      </DataState>
    </div>
  );
}
