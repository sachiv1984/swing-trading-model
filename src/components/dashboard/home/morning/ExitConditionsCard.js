import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { api } from "../../../../api/base44Client";
import { getExitCondition } from "../../../../lib/exitCondition";

const MAX_ROWS = 5;

// ST-09 (BLG-FE-199, v9.10): dashboard.md §1A Exit Conditions Met Row.
// Display-only: lists positions meeting a §8 exit condition and links to the
// exit dialog; nothing is exited automatically. Renders nothing while loading,
// on error, or when no position qualifies.
export default function ExitConditionsCard() {
  const { data: positions, isLoading, error } = useQuery({
    queryKey: ["morning-positions"],
    queryFn: () => api.positions.list(),
    retry: 1,
  });

  if (isLoading || error || !Array.isArray(positions)) return null;
  const qualifying = positions
    .map((p) => ({ position: p, condition: getExitCondition(p) }))
    .filter(({ condition }) => condition.reason);
  if (qualifying.length === 0) return null;

  const shown = qualifying.slice(0, MAX_ROWS);
  const overflow = qualifying.length - shown.length;

  return (
    <div
      data-testid="exit-conditions-card"
      className="mb-4 rounded-2xl bg-slate-800/50 border border-slate-700/50 border-l-4 p-6"
      style={{ borderLeftColor: "#EA580C" }}
    >
      <p className="text-xs text-slate-600 dark:text-slate-400 uppercase tracking-wider mb-1">
        Exit Conditions Met <span data-testid="exit-conditions-count">({qualifying.length})</span>
      </p>
      <p className="text-sm text-slate-600 dark:text-slate-400 mb-3">
        These positions meet a strategy exit condition (§8). Nothing is exited automatically.
      </p>
      <ul className="space-y-2">
        {shown.map(({ position, condition }) => (
          <li
            key={position.id}
            data-testid={`exit-conditions-row-${position.id}`}
            className="flex items-center gap-3 text-sm"
          >
            <span className="font-semibold text-white">{position.ticker}</span>
            {condition.riskOff ? (
              <span
                className="inline-flex items-center text-xs px-1.5 py-0.5 rounded-full text-white font-medium"
                style={{ backgroundColor: "#1E40AF" }}
              >
                RISK OFF
              </span>
            ) : (
              <span className="inline-flex items-center text-xs px-1.5 py-0.5 rounded-full bg-orange-600 text-white font-medium">
                STOP REACHED
              </span>
            )}
            <Link
              to={`/Positions?exit=${encodeURIComponent(position.id)}`}
              aria-label={`Review exit for ${position.ticker}`}
              className="ml-auto text-cyan-400 hover:text-cyan-300 underline underline-offset-2"
            >
              Review exit
            </Link>
          </li>
        ))}
      </ul>
      {overflow > 0 && (
        <Link
          to="/Positions"
          data-testid="exit-conditions-overflow"
          className="mt-3 inline-block text-xs text-cyan-400 hover:text-cyan-300"
        >
          +{overflow} more
        </Link>
      )}
    </div>
  );
}
