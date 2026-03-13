import { useQuery } from "@tanstack/react-query";
import { format } from "date-fns";
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
    queryFn: async () => {
      const res = await fetch("/api/market/status");
      if (!res.ok) throw new Error(`API error ${res.status}`);
      return res.json();
    },
    retry: 1,
  });

  const signalsQuery = useQuery({
    queryKey: ["home-signals-today"],
    queryFn: async () => {
      const res = await fetch(`/api/signals?date=${today}`);
      if (!res.ok) throw new Error(`API error ${res.status}`);
      return res.json();
    },
    retry: 1,
  });

  const isLoading = marketQuery.isLoading || signalsQuery.isLoading;
  const error = marketQuery.error && signalsQuery.error ? marketQuery.error : null;

  const regimes = marketQuery.data?.regimes ?? marketQuery.data?.data ?? [];
  const signals = Array.isArray(signalsQuery.data) ? signalsQuery.data : (signalsQuery.data?.signals ?? signalsQuery.data?.data ?? []);
  const todaySignals = signals.filter(s => s.signal_date === today || s.created_date?.startsWith(today));

  return (
    <DashboardCard title="Signal Status" to="/Signals" isLoading={isLoading} error={error}>
      <div className="space-y-2 mb-3">
        {regimes.length > 0
          ? regimes.map(r => <RegimeRow key={r.market} market={r.market} status={r.status} />)
          : (
            <>
              <RegimeRow market="SPY" status={marketQuery.data?.spy_status ?? marketQuery.data?.us_status ?? "unknown"} />
              <RegimeRow market="FTSE" status={marketQuery.data?.ftse_status ?? marketQuery.data?.uk_status ?? "unknown"} />
            </>
          )
        }
      </div>
      <p className="text-sm text-slate-400">
        {todaySignals.length > 0
          ? `${todaySignals.length} new signal${todaySignals.length !== 1 ? "s" : ""} today`
          : "No new signals today"}
      </p>
    </DashboardCard>
  );
}
