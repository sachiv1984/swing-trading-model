import { useQuery } from "@tanstack/react-query";
import { Flame } from "lucide-react";
import { cn } from "../../../lib/utils";
import { api } from "../../../api/base44Client";
import DashboardCard from "./DashboardCard";
import { formatPercent } from "../../../lib/format";

function heatColor(pct) {
  if (pct == null) return "text-white";
  if (pct < 15) return "text-emerald-400";
  if (pct <= 25) return "text-amber-400";
  return "text-rose-400";
}

export default function PortfolioHeatCard() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["home-portfolio-heat"],
    queryFn: () => api.portfolio.get(),
    retry: 1,
  });

  const portfolio = data?.portfolio ?? data?.data ?? data;
  const heat = portfolio?.portfolio_heat_percent;
  // ST-10 (EPIC-02, v9.11, BLG-BE-154): count positions whose live price fetch failed.
  const staleCount = (portfolio?.positions ?? []).filter((p) => p?.price_is_stale === true).length;

  return (
    <DashboardCard
      title="Portfolio Heat"
      to="/RiskDashboard"
      isLoading={isLoading}
      error={error}
      empty={heat == null}
      emptyIcon={<Flame className="w-8 h-8 text-slate-600" />}
      emptyHeading="No portfolio heat data"
      emptyBody="Heat will show here once you're holding a position."
    >
      <p className={cn("text-4xl font-bold mb-2", heatColor(heat))}>
        {heat != null ? formatPercent(heat) : ""}
      </p>
      <p className="text-sm text-slate-600 dark:text-slate-400">
        {heat != null && (heat < 15 ? "Heat within safe range" : heat <= 25 ? "Heat elevated — monitor closely" : "Heat critical — review positions")}
      </p>
      {staleCount > 0 && (
        <p
          className="text-xs text-amber-400 mt-1"
          data-testid="dashboard-price-stale-notice"
          title="Live price unavailable. Showing the last stored price converted at today's FX rate."
        >
          ⚠ {staleCount} position price{staleCount === 1 ? "" : "s"} stale
        </p>
      )}
    </DashboardCard>
  );
}
