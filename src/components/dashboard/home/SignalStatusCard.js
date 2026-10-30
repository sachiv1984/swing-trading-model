import { useId } from "react";
import { useQuery } from "@tanstack/react-query";
import { format } from "date-fns";
import { api } from "../../../api/base44Client";
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from "../../ui/tooltip";
import { REGIME_RISK_ON, REGIME_UNKNOWN, regimeStatusOf, unknownRegimeExplanation } from "../../../lib/regime";
import DashboardCard from "./DashboardCard";

const REGION_BY_INDEX = { SPY: "US", FTSE: "UK" };
const BADGE = "text-xs font-semibold px-2 py-0.5 rounded-full";

function UnknownRegimeBadge({ market }) {
  const descriptionId = useId();
  const explanation = unknownRegimeExplanation(REGION_BY_INDEX[market]);
  return (
    <TooltipProvider delayDuration={200}>
      <Tooltip>
        <TooltipTrigger asChild>
          <span
            data-testid={`regime-unknown-${market}`}
            aria-describedby={descriptionId}
            className={`${BADGE} bg-slate-200 text-slate-800 dark:bg-slate-500/20 dark:text-slate-300`}
          >
            UNKNOWN ?
          </span>
        </TooltipTrigger>
        <TooltipContent className="max-w-xs text-left">{explanation}</TooltipContent>
      </Tooltip>
      <span id={descriptionId} className="sr-only">{explanation}</span>
    </TooltipProvider>
  );
}

function RegimeRow({ market, status }) {
  const isOn = status === REGIME_RISK_ON;
  return (
    <div className="flex items-center justify-between">
      <span className="text-sm text-slate-300">{market}</span>
      {status === REGIME_UNKNOWN ? (
        <UnknownRegimeBadge market={market} />
      ) : (
        <span className={`${BADGE} ${isOn ? "bg-emerald-500/20 text-emerald-400" : "bg-rose-500/20 text-rose-400"}`}>
          {isOn ? "RISK-ON ✓" : "RISK-OFF ✗"}
        </span>
      )}
    </div>
  );
}

export default function SignalStatusCard() {
  const today = format(new Date(), "yyyy-MM-dd");

  const marketQuery = useQuery({
    queryKey: ["home-market-status"],
    queryFn: () => api.market.getStatus(),
    retry: 1,
  });

  const signalsQuery = useQuery({
    queryKey: ["home-signals-today"],
    queryFn: () => api.signals.list(),
    retry: 1,
  });

  const isLoading = marketQuery.isLoading || signalsQuery.isLoading;
  // Only show error state if both queries failed (individual card error per spec §5)
  const error = marketQuery.error && signalsQuery.error ? marketQuery.error : null;

  // Normalise market status response: { spy: { regime_status, is_risk_on }, ftse: { ... } }
  const mktData = marketQuery.data?.data ?? marketQuery.data;
  const regimes = mktData?.regimes ?? [
    { market: "SPY", status: regimeStatusOf(mktData?.spy) },
    { market: "FTSE", status: regimeStatusOf(mktData?.ftse) },
  ];

  const usDescriptionId = useId();
  const ukDescriptionId = useId();
  const descriptionIds = { SPY: usDescriptionId, FTSE: ukDescriptionId };
  const descriptions = regimes
    .filter((r) => r.status === REGIME_UNKNOWN && descriptionIds[r.market])
    .map((r) => ({ id: descriptionIds[r.market], text: unknownRegimeExplanation(REGION_BY_INDEX[r.market]) }));

  const signals = Array.isArray(signalsQuery.data) ? signalsQuery.data : [];
  const todaySignals = signals.filter(s => s.signal_date === today || s.created_date?.startsWith(today));

  return (
    <DashboardCard title="Signal Status" to="/Signals" isLoading={isLoading} error={error} descriptions={descriptions}>
      <div className="space-y-2 mb-3">
        {regimes.map(r => <RegimeRow key={r.market} market={r.market} status={r.status} />)}
      </div>
      <p className="text-sm text-slate-600 dark:text-slate-400">
        {todaySignals.length > 0
          ? `${todaySignals.length} new signal${todaySignals.length !== 1 ? "s" : ""} today`
          : "No new signals today"}
      </p>
    </DashboardCard>
  );
}
