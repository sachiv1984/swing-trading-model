import { useQuery } from "@tanstack/react-query";
import { format } from "date-fns";
import { api } from "../../../api/base44Client";
import DashboardCard from "./DashboardCard";

function RegimeRow({ market, status }) {
  const isOn = status === "risk_on";
  return (
    <div className="flex items-center justify-between">
      <span className="text-sm text-slate-300">{market}</span>
      <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${isOn ? "bg-emerald-500/20 text-emerald-400" : "bg-rose-500/20 text-rose-400"}`}>
        {isOn ? "RISK-ON ✓" : "RISK-OFF ✗"}
      </span>
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

  // Normalise market status response: { spy: { is_risk_on }, ftse: { is_risk_on } }
  const mktData = marketQuery.data;
  const regimes = mktData?.regimes ?? [
    { market: "SPY", status: mktData?.spy?.is_risk_on ? "risk_on" : (mktData?.spy?.is_risk_on === false ? "risk_off" : "unknown") },
    { market: "FTSE", status: mktData?.ftse?.is_risk_on ? "risk_on" : (mktData?.ftse?.is_risk_on === false ? "risk_off" : "unknown") },
  ];

  const signals = Array.isArray(signalsQuery.data) ? signalsQuery.data : [];
  const todaySignals = signals.filter(s => s.signal_date === today || s.created_date?.startsWith(today));

  return (
    <DashboardCard title="Signal Status" to="/Signals" isLoading={isLoading} error={error}>
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
