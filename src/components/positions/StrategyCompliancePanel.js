/**
 * StrategyCompliancePanel — ST-01 (BLG-FEAT-11, v2.3)
 *
 * Collapsible ATR-based strategy compliance panel, rendered below Table View only.
 * Display-only — §13.3 constraint: no automated notification, alert, or action.
 *
 * Spec: docs/specs/frontend/pages/positions.md §Strategy Compliance Panel
 * UX:   docs/design/2026-03-24__release-v2.3/compliance-panel/ux_spec.md
 */

import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { ChevronDown, ChevronUp, Loader2, ShieldCheck, ShieldAlert, ShieldX } from "lucide-react";
import { apiFetch } from "../../api/base44Client";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

// ---------------------------------------------------------------------------
// Status config
// ---------------------------------------------------------------------------
const STATUS_CONFIG = {
  Compliant: {
    label: "Compliant",
    badgeClass: "bg-emerald-500/15 text-emerald-400 border border-emerald-500/30",
    Icon: ShieldCheck,
    iconClass: "text-emerald-400",
  },
  "Needs Attention": {
    label: "Needs Attention",
    badgeClass: "bg-amber-500/15 text-amber-400 border border-amber-500/30",
    Icon: ShieldAlert,
    iconClass: "text-amber-400",
  },
  "Review Required": {
    label: "Review Required",
    badgeClass: "bg-rose-500/15 text-rose-400 border border-rose-500/30",
    Icon: ShieldX,
    iconClass: "text-rose-400",
  },
};

// ---------------------------------------------------------------------------
// Cell renderers
// ---------------------------------------------------------------------------
function ComplianceFlag({ value }) {
  if (value === null || value === undefined) {
    return <span className="text-slate-600">—</span>;
  }
  return value ? (
    <span className="text-emerald-400" title="Compliant">✅</span>
  ) : (
    <span className="text-amber-400" title="Non-compliant">⚠️</span>
  );
}

function StopAge({ days }) {
  if (days === null || days === undefined) {
    return <span className="text-slate-600 dark:text-slate-400 italic">Not set</span>;
  }
  return <span className="text-slate-300">{days} {days === 1 ? "day" : "days"}</span>;
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------
export default function StrategyCompliancePanel() {
  const [isExpanded, setIsExpanded] = useState(false);
  const [defaultSet, setDefaultSet] = useState(false);

  const { data, isLoading, isError } = useQuery({
    queryKey: ["positionsCompliance"],
    queryFn: async () => {
      const response = await apiFetch(`${API_URL}/positions/compliance`);
      if (!response.ok) return null;
      const result = await response.json();
      return result?.data ?? null;
    },
    staleTime: 2 * 60 * 1000,
    retry: false,
  });

  // Set default expand/collapse once data arrives
  useEffect(() => {
    if (data && !defaultSet) {
      const hasNonCompliant = data.positions?.some(
        (p) =>
          p.stop_compliant === false ||
          p.size_compliant === false
      );
      setIsExpanded(!!hasNonCompliant);
      setDefaultSet(true);
    }
  }, [data, defaultSet]);

  // Hide panel on error or if no positions
  if (isError) return null;
  if (!isLoading && (!data || data.total_count === 0)) return null;

  const status = data?.overall_status ?? "Compliant";
  const config = STATUS_CONFIG[status] ?? STATUS_CONFIG["Compliant"];
  const { Icon } = config;

  return (
    <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 overflow-hidden">
      {/* Header — always visible */}
      <button
        type="button"
        onClick={() => setIsExpanded((v) => !v)}
        className="w-full flex items-center justify-between px-5 py-3 cursor-pointer hover:bg-slate-700/20 transition-colors"
        aria-expanded={isExpanded}
      >
        <div className="flex items-center gap-3">
          {isLoading ? (
            <Loader2 className="w-4 h-4 animate-spin text-slate-500" />
          ) : (
            <Icon className={`w-4 h-4 ${config.iconClass}`} />
          )}
          <span className="text-sm font-medium text-slate-300">
            Strategy Compliance
          </span>
          {!isLoading && data && (
            <span
              className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${config.badgeClass}`}
            >
              {config.label}
            </span>
          )}
        </div>

        <div className="flex items-center gap-3">
          {!isLoading && data && (
            <span className="text-xs text-slate-600 dark:text-slate-400">
              {data.compliant_count} of {data.total_count}{" "}
              {data.total_count === 1 ? "position" : "positions"} fully compliant
            </span>
          )}
          {isLoading ? null : isExpanded ? (
            <ChevronUp className="w-4 h-4 text-slate-500" />
          ) : (
            <ChevronDown className="w-4 h-4 text-slate-500" />
          )}
        </div>
      </button>

      {/* Collapsible body */}
      <div
        style={{
          maxHeight: isExpanded && !isLoading && data ? "600px" : "0px",
          overflow: "hidden",
          transition: "max-height 0.25s ease",
        }}
      >
        {data && data.positions && data.positions.length > 0 && (
          <div className="px-5 pb-4">
            <div className="border-t border-slate-700/50 pt-3">
              <table className="w-full text-xs">
                <thead>
                  <tr className="text-slate-600 dark:text-slate-400 border-b border-slate-700/40">
                    <th className="text-left pb-2 font-medium">Ticker</th>
                    <th className="text-center pb-2 font-medium">Stop Compliance</th>
                    <th className="text-center pb-2 font-medium">Stop Age</th>
                    <th className="text-center pb-2 font-medium">Size Compliance</th>
                  </tr>
                </thead>
                <tbody>
                  {data.positions.map((pos) => (
                    <tr
                      key={pos.position_id}
                      className="border-b border-slate-700/20 last:border-0"
                    >
                      <td className="py-2">
                        <div className="flex items-center gap-1.5">
                          <span className="font-semibold text-white">{pos.ticker}</span>
                          <span className="text-xs px-1.5 py-0.5 rounded bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-700">
                            {pos.market}
                          </span>
                        </div>
                      </td>
                      <td className="py-2 text-center">
                        <ComplianceFlag value={pos.stop_compliant} />
                      </td>
                      <td className="py-2 text-center">
                        <StopAge days={pos.stop_age_days} />
                      </td>
                      <td className="py-2 text-center">
                        <ComplianceFlag value={pos.size_compliant} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
