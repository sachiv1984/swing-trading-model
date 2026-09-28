/**
 * PaperAccountPanel — Alpaca paper account positions display
 *
 * §13 compliance: display-only; no automated order execution.
 * Conditionally rendered: hidden when ALPACA_PAPER_API_KEY not configured
 * (backend returns {"paper_tracking_enabled": false}).
 *
 * Spec: docs/ux_specs/paper-trading/ux_spec.md v1.0
 * ST-03, EPIC-01, v3.5
 */
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "../../api/base44Client";
import { ChevronDown, ChevronRight } from "lucide-react";
import { cn } from "../../lib/utils";
import { formatCurrency, formatPercent } from "../../lib/format";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

function PnlCell({ value, kind = "currency" }) {
  if (value == null) return <span className="text-slate-600 dark:text-slate-400">—</span>;
  return (
    <span className={cn("font-semibold", value > 0 ? "text-emerald-400" : value < 0 ? "text-rose-400" : "text-slate-300")}>
      {kind === "percent" ? formatPercent(value, { signed: true }) : formatCurrency(value, { currency: "USD", signed: true })}
    </span>
  );
}

function formatDate(iso) {
  if (!iso) return "—";
  try {
    return new Date(iso).toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
  } catch {
    return iso;
  }
}

export default function PaperAccountPanel() {
  const [expanded, setExpanded] = useState(true);

  const { data, isError } = useQuery({
    queryKey: ["paperPositions"],
    queryFn: async () => {
      const res = await apiFetch(`${API_URL}/portfolio/paper-positions`);
      if (!res.ok) return null;
      const json = await res.json();
      return json;
    },
    retry: false,
    staleTime: 60_000,
  });

  // Hidden when not enabled or data unavailable
  if (!data || !data.paper_tracking_enabled) return null;

  const positions = data.positions || [];
  const hasPositions = positions.length > 0;

  // Collapsed by default when no positions (per ux_spec.md §3.1)
  const defaultExpanded = hasPositions;

  return (
    <div className="mt-4 w-full rounded-xl border border-slate-700/50 bg-slate-800/40 overflow-hidden">
      {/* Header */}
      <button
        className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-slate-700/30 transition-colors"
        onClick={() => setExpanded((v) => !v)}
        aria-expanded={expanded}
        data-testid="paper-account-panel"
      >
        <div>
          <span className="text-sm font-semibold text-slate-200">Paper Account</span>
          <span className="ml-2 text-xs text-slate-600 dark:text-slate-400">Hypothetical tracking — US market positions only. Not real capital.</span>
        </div>
        {expanded ? (
          <ChevronDown className="w-4 h-4 text-slate-400 flex-shrink-0" />
        ) : (
          <ChevronRight className="w-4 h-4 text-slate-400 flex-shrink-0" />
        )}
      </button>

      {/* Body */}
      {expanded && (
        <div className="px-4 pb-4">
          {isError ? (
            <p className="text-xs text-slate-600 dark:text-slate-400 py-2">Paper tracking temporarily unavailable.</p>
          ) : !hasPositions ? (
            <p className="text-xs text-slate-600 dark:text-slate-400 py-2">
              No paper positions tracked. Open a US market position to begin tracking.
            </p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-xs" data-testid="paper-positions-table">
                <thead>
                  <tr className="text-slate-600 dark:text-slate-400 border-b border-slate-700/50">
                    <th className="text-left py-2 pr-4 font-medium">Ticker</th>
                    <th className="text-right py-2 pr-4 font-medium">Paper Entry</th>
                    <th className="text-right py-2 pr-4 font-medium">Current</th>
                    <th className="text-right py-2 pr-4 font-medium">P&amp;L ($)</th>
                    <th className="text-right py-2 pr-4 font-medium">P&amp;L (%)</th>
                    <th className="text-right py-2 pr-4 font-medium">Date Opened</th>
                    <th className="text-right py-2 font-medium">Size</th>
                  </tr>
                </thead>
                <tbody>
                  {positions.map((pos) => (
                    <tr key={pos.ticker} className="border-b border-slate-700/20 last:border-0">
                      <td className="py-2 pr-4 font-semibold text-slate-200">{pos.ticker}</td>
                      <td className="py-2 pr-4 text-right text-slate-300">
                        {formatCurrency(pos.paper_entry_price, { currency: "USD" })}
                      </td>
                      <td className="py-2 pr-4 text-right text-slate-300">
                        {formatCurrency(pos.current_market_price, { currency: "USD" })}
                      </td>
                      <td className="py-2 pr-4 text-right">
                        <PnlCell value={pos.paper_pnl_usd} kind="currency" />
                      </td>
                      <td className="py-2 pr-4 text-right">
                        <PnlCell value={pos.paper_pnl_pct} kind="percent" />
                      </td>
                      <td className="py-2 pr-4 text-right text-slate-600 dark:text-slate-400">
                        {formatDate(pos.date_opened)}
                      </td>
                      <td className="py-2 text-right text-slate-300">
                        {pos.position_size != null ? pos.position_size : "—"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
