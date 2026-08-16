import { useParams, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "../api/base44Client";
import { Button } from "../components/ui/button";
import PageHeader from "../components/ui/PageHeader";
import EntryChecklist from "../components/trades/EntryChecklist";
import SetupQualityScorePanel from "../components/trades/SetupQualityScorePanel";
import { ArrowLeft, TrendingUp, TrendingDown } from "lucide-react";
import { cn } from "../lib/utils";
import { TradePlanStatusBadge } from "./TradePlans";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

function relativeTime(isoString) {
  if (!isoString) return null;
  const diff = Date.now() - new Date(isoString).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  return `${days}d ago`;
}

function formatMarketCap(value) {
  if (value == null) return "—";
  if (value >= 1e12) return `$${(value / 1e12).toFixed(1)}T`;
  if (value >= 1e9) return `$${(value / 1e9).toFixed(1)}B`;
  if (value >= 1e6) return `$${(value / 1e6).toFixed(1)}M`;
  return `$${value.toLocaleString()}`;
}

function stripUkSuffix(t) {
  return t?.endsWith(".L") ? t.slice(0, -2) : (t ?? "");
}

function currencySymbol(ticker) {
  return ticker?.endsWith(".L") ? "£" : "$";
}

function SignalBadge({ status }) {
  const cfg =
    {
      active: { label: "Active", cls: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30" },
      watch: { label: "Watch", cls: "bg-amber-500/20 text-amber-400 border-amber-500/30" },
      no_signal: { label: "No Signal", cls: "bg-slate-700/50 text-slate-600 dark:text-slate-400 border-slate-600/30" },
    }[status] || { label: status ?? "—", cls: "bg-slate-700/50 text-slate-600 dark:text-slate-400 border-slate-600/30" };
  return (
    <span className={cn("inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border whitespace-nowrap", cfg.cls)}>
      {cfg.label}
    </span>
  );
}

function HeatValue({ value, isError }) {
  if (isError) return <span className="text-slate-600 dark:text-slate-400 text-sm">N/A</span>;
  if (value == null) return <span className="text-slate-600 dark:text-slate-400 text-sm">—</span>;
  const pct = Number(value).toFixed(1);
  const cls = value > 25 ? "text-red-400" : value >= 15 ? "text-amber-400" : "text-emerald-400";
  return <span className={cn("text-xl font-semibold", cls)}>{pct}%</span>;
}

function Skeleton({ className }) {
  return <div className={cn("h-4 bg-slate-700/50 rounded animate-pulse", className)} />;
}

export default function Research() {
  const { ticker } = useParams();
  const navigate = useNavigate();

  const {
    data: researchData,
    isLoading: researchLoading,
    isError: researchError,
    refetch,
  } = useQuery({
    queryKey: ["research", ticker],
    queryFn: async () => {
      const r = await apiFetch(`${API_BASE}/research/${ticker}`);
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const j = await r.json();
      return j.data ?? j;
    },
    enabled: !!ticker,
    retry: 1,
  });

  const sigEntry = researchData?.signal?.entry_price ?? null;
  const sigStop = researchData?.signal?.stop_price ?? null;
  const canCalculateHeat = sigEntry !== null && sigStop !== null && sigEntry > sigStop;

  const { data: heatData, isError: heatError } = useQuery({
    queryKey: ["prospective-heat", ticker, sigEntry, sigStop],
    queryFn: async () => {
      const params = new URLSearchParams({ ticker, shares: 1, entry_price: sigEntry, stop_price: sigStop });
      const r = await apiFetch(`${API_BASE}/portfolio/prospective-heat?${params}`);
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const j = await r.json();
      return j.data ?? j;
    },
    enabled: !!ticker && canCalculateHeat,
    retry: 1,
  });
  const heatLoading = canCalculateHeat && !heatData && !heatError;

  const { data: tradePlansData, isLoading: plansLoading, isError: tradePlansError } = useQuery({
    queryKey: ["trade-plans-ticker", ticker],
    queryFn: async () => {
      const r = await apiFetch(`${API_BASE}/trade-plans?ticker=${ticker}`);
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const j = await r.json();
      return j.data ?? j;
    },
    enabled: !!ticker,
    retry: 1,
  });

  if (researchError) {
    const errorStatus = researchError?.message?.match(/HTTP (\d+)/)?.[1];
    const errorMessage =
      errorStatus === "404"
        ? `Ticker '${ticker}' was not found.`
        : errorStatus === "503"
        ? "Market data service is currently unavailable. Please try again later."
        : "Unable to load research data. Please try again.";
    return (
      <div className="space-y-6">
        <PageHeader
          title={ticker || "Research"}
          description="Pre-trade research"
          actions={
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate(-1)}
              className="text-slate-600 dark:text-slate-400 hover:text-white"
            >
              <ArrowLeft className="w-4 h-4 mr-1" />
              Back
            </Button>
          }
        />
        <div className="rounded-xl bg-red-500/10 border border-red-500/30 p-8 text-center">
          <p className="text-red-400 text-sm mb-4">{errorMessage}</p>
          <Button
            onClick={() => refetch()}
            className="bg-red-600 hover:bg-red-700 text-white text-xs"
          >
            Retry
          </Button>
        </div>
      </div>
    );
  }

  const r = researchData;
  const sym = currencySymbol(ticker);
  const priceChangePct = r?.price_change_pct;
  const priceChangePos = priceChangePct != null && priceChangePct >= 0;

  const plans = Array.isArray(tradePlansData) ? tradePlansData : [];
  // ST-14 (EPIC-03, BLG-FE-162, v8.8): extended from 3 to all 6 statuses —
  // previously research_pending/research_complete/closed plans matched none
  // of the .find() calls, so activePlan stayed null and the panel silently
  // fell back to the "No trade plan" CTA for those statuses (found via the
  // Playwright coverage this story added, not a design-time AC). Precedence
  // follows the plan lifecycle from most to least currently relevant.
  const activePlan =
    plans.find((p) => p.status === "active") ||
    plans.find((p) => p.status === "entry_conditions_set") ||
    plans.find((p) => p.status === "research_complete") ||
    plans.find((p) => p.status === "research_pending") ||
    plans.find((p) => p.status === "draft") ||
    plans.find((p) => p.status === "closed") ||
    null;

  const newsHeadlines = r?.news_headlines || [];

  return (
    <div className="space-y-6">
      <PageHeader
        title={ticker ? `${stripUkSuffix(ticker)} — Research` : "Research"}
        description={
          researchLoading
            ? "Loading…"
            : [r?.sector?.sector, r?.sector?.industry].filter(Boolean).join(" · ") || ""
        }
        actions={
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate(-1)}
            className="text-slate-600 dark:text-slate-400 hover:text-white"
          >
            <ArrowLeft className="w-4 h-4 mr-1" />
            Back
          </Button>
        }
      />

      {/* Header meta */}
      {!researchLoading && (
        <div className="flex flex-wrap gap-4 items-center text-xs">
          {r?.market_cap != null && (
            <span className="text-slate-600 dark:text-slate-400">
              Market cap:{" "}
              <span className="text-slate-200">{formatMarketCap(r.market_cap)}</span>
            </span>
          )}
          {r?.updated_at && (
            <span className="text-slate-600 dark:text-slate-400">Updated {relativeTime(r.updated_at)}</span>
          )}
        </div>
      )}

      {/* Price and Signal */}
      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-6">
        <h2 className="text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wider mb-4">
          Price &amp; Signal
        </h2>
        {researchLoading ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="space-y-2">
                <Skeleton className="w-16 h-3" />
                <Skeleton className="w-24 h-6" />
              </div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div>
              <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Current Price</p>
              <p className="text-xl font-semibold text-white">
                {r?.price != null ? `${sym}${Number(r.price).toFixed(2)}` : "—"}
              </p>
            </div>
            <div>
              <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Price Change</p>
              <p
                className={cn(
                  "text-sm font-medium flex items-center gap-1",
                  priceChangePct == null
                    ? "text-slate-600 dark:text-slate-400"
                    : priceChangePos
                    ? "text-emerald-400"
                    : "text-red-400"
                )}
              >
                {priceChangePct != null ? (
                  <>
                    {priceChangePos ? (
                      <TrendingUp className="w-4 h-4" />
                    ) : (
                      <TrendingDown className="w-4 h-4" />
                    )}
                    {priceChangePos ? "+" : ""}
                    {(priceChangePct * 100).toFixed(1)}%
                  </>
                ) : (
                  "—"
                )}
              </p>
            </div>
            <div>
              <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Momentum Signal</p>
              <SignalBadge status={r?.signal?.status} />
            </div>
            <div>
              <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Setup Type</p>
              <p className="text-sm text-slate-200">
                {r?.signal?.signal_type ?? "—"}
              </p>
            </div>
            <div>
              <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">ATR (14d)</p>
              <p className="text-sm text-slate-200">
                {r?.signal?.atr != null ? `${sym}${Number(r.signal.atr).toFixed(2)}` : "—"}
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Prospective Heat */}
      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-6">
        <h2 className="text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wider mb-4">
          Prospective heat at entry
        </h2>
        <div className="grid grid-cols-2 gap-6">
          <div>
            <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Current Portfolio Heat</p>
            {heatLoading ? (
              <Skeleton className="w-16 h-6" />
            ) : heatData?.valid && heatData.current_heat_percent != null ? (
              <HeatValue value={heatData.current_heat_percent} isError={false} />
            ) : (
              <HeatValue value={null} isError={true} />
            )}
          </div>
          <div>
            <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Prospective Heat (if entered)</p>
            {heatLoading ? (
              <Skeleton className="w-16 h-6" />
            ) : heatData?.valid && heatData.prospective_heat_percent != null ? (
              <HeatValue value={heatData.prospective_heat_percent} isError={false} />
            ) : (
              <HeatValue value={null} isError={true} />
            )}
          </div>
        </div>
      </div>

      {/* Setup Quality Score — ST-09 (v6.1) */}
      <SetupQualityScorePanel ticker={ticker} />

      {/* Trade Plan Context Panel */}
      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-6">
        <h2 className="text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wider mb-4">
          Trade Plan
        </h2>
        {plansLoading && !tradePlansError ? (
          <Skeleton className="w-full h-5" />
        ) : tradePlansError || !activePlan ? (
          <div className="flex items-center justify-between flex-wrap gap-3">
            <p className="text-sm text-slate-600 dark:text-slate-400">No trade plan for {ticker}.</p>
            <Button
              size="sm"
              onClick={() => navigate(`/TradePlan?ticker=${ticker}`)}
              className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 text-xs"
            >
              Create Trade Plan
            </Button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <TradePlanStatusBadge status={activePlan.status} />
              <button
                onClick={() => navigate(`/TradePlan?edit=${activePlan.id}&ticker=${ticker}`)}
                className="text-xs text-cyan-400 hover:text-cyan-300 underline"
              >
                View full plan
              </button>
            </div>
            {activePlan.stop_level != null && (
              <div>
                <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Stop Level</p>
                <p className="text-sm text-slate-200">{sym}{Number(activePlan.stop_level).toFixed(2)}</p>
              </div>
            )}
            {activePlan.risk_reward_notes && (
              <div>
                <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Notes</p>
                <p className="text-sm text-slate-600 dark:text-slate-400 italic">
                  {activePlan.risk_reward_notes.length > 100
                    ? `${activePlan.risk_reward_notes.slice(0, 100)}…`
                    : activePlan.risk_reward_notes}
                </p>
              </div>
            )}
            {activePlan.r_target != null && (
              <div>
                <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">R Target</p>
                <p className="text-sm text-slate-200">{activePlan.r_target}R</p>
              </div>
            )}
            {Array.isArray(activePlan.checklist_items) && activePlan.checklist_items.length > 0 && (
              <div>
                <p className="text-xs text-slate-600 dark:text-slate-400 mb-2">Pre-Entry Checklist</p>
                <EntryChecklist
                  items={activePlan.checklist_items}
                  ticker={ticker}
                  readOnly
                />
              </div>
            )}
          </div>
        )}
      </div>

      {/* Recent News */}
      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-6">
        <h2 className="text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wider mb-4">
          Recent News
        </h2>
        {researchLoading ? (
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <Skeleton key={i} className="w-full h-4" />
            ))}
          </div>
        ) : newsHeadlines.length > 0 ? (
          <ul className="space-y-3">
            {newsHeadlines.slice(0, 5).map((h, i) => (
              <li
                key={i}
                className="border-b border-slate-700/30 pb-3 last:border-0 last:pb-0"
              >
                {h.url ? (
                  <a href={h.url} target="_blank" rel="noopener noreferrer" className="text-sm text-slate-200 hover:text-blue-400 hover:underline">{h.headline || h.title}</a>
                ) : (
                  <p className="text-sm text-slate-200">{h.headline || h.title}</p>
                )}
                <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
                  {h.source ? `${h.source} · ` : ""}
                  {h.published_at ? relativeTime(h.published_at) : ""}
                </p>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-slate-600 dark:text-slate-400">No recent news available.</p>
        )}
      </div>
    </div>
  );
}
