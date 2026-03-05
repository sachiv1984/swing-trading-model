import { useQuery } from "@tanstack/react-query";
import { base44, api } from "../api/base44Client";
import { Loader2, AlertCircle } from "lucide-react";
import PageHeader from "../components/ui/PageHeader";
import HeatGauge from "../components/risk/HeatGauge";
import DrawdownSummary from "../components/risk/DrawdownSummary";
import GracePeriodPanel from "../components/risk/GracePeriodPanel";
import PositionRiskTable from "../components/risk/PositionRiskTable";
import ProspectiveHeatPanel from "../components/risk/ProspectiveHeatPanel";

function ErrorCard({ message }) {
  return (
    <div className="rounded-2xl bg-rose-900/20 border border-rose-500/30 p-6 flex items-center gap-3">
      <AlertCircle className="w-5 h-5 text-rose-400 flex-shrink-0" />
      <p className="text-sm text-rose-300">{message}</p>
    </div>
  );
}

export default function RiskDashboard() {
  const {
    data: portfolioData,
    isLoading: loadingPortfolio,
    error: portfolioError,
  } = useQuery({
    queryKey: ["riskPortfolio"],
    queryFn: () => api.portfolio.get(),
    retry: 1,
  });

  // Fallback: if the /api/portfolio endpoint isn't available yet,
  // read from the entity store so the page is useful immediately.
  const {
    data: entityPositions,
    isLoading: loadingEntityPositions,
  } = useQuery({
    queryKey: ["riskEntityPositions"],
    queryFn: () => base44.entities.Position.filter({ status: "open" }),
    enabled: !!portfolioError, // only if api fails
  });

  const {
    data: entityPortfolio,
    isLoading: loadingEntityPortfolio,
  } = useQuery({
    queryKey: ["riskEntityPortfolio"],
    queryFn: () => base44.entities.Portfolio.list(),
    enabled: !!portfolioError,
  });

  const usingEntityFallback = !!portfolioError;

  // Resolve which data to use
  const heatPercent = portfolioData?.portfolio_heat_percent ?? null;
  const drawdownPercent = portfolioData?.current_drawdown_percent ?? null;
  const peakValue = portfolioData?.peak_portfolio_value ?? entityPortfolio?.[0]?.total_value ?? null;

  // Positions: prefer API response, fallback to entity store
  const positions = portfolioData?.positions ?? entityPositions ?? [];

  const isLoading = loadingPortfolio || (usingEntityFallback && (loadingEntityPositions || loadingEntityPortfolio));

  return (
    <div className="space-y-6">
      <PageHeader
        title="Risk Dashboard"
        description="Daily portfolio risk snapshot — review before making trading decisions."
      />

      {isLoading ? (
        <div className="flex items-center justify-center py-24">
          <Loader2 className="w-8 h-8 animate-spin text-slate-500" />
        </div>
      ) : (
        <div className="space-y-6">
          {/* Top row: Heat Gauge + Drawdown Summary */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Heat Gauge */}
            <div className="rounded-2xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700/50 backdrop-blur-sm p-6 flex flex-col items-center justify-center">
              {portfolioError && heatPercent === null ? (
                <ErrorCard message="Could not load portfolio heat. Check API connection." />
              ) : (
                <>
                  <HeatGauge heatPercent={heatPercent ?? 0} />
                  {usingEntityFallback && (
                    <p className="mt-2 text-xs text-amber-400">Live heat unavailable — showing entity data fallback.</p>
                  )}
                </>
              )}
            </div>

            {/* Drawdown Summary */}
            {portfolioError && drawdownPercent === null ? (
              <ErrorCard message="Could not load drawdown data. Check API connection." />
            ) : (
              <DrawdownSummary
                drawdownPercent={drawdownPercent}
                peakValue={peakValue}
              />
            )}
          </div>

          {/* Grace Period Panel */}
          <GracePeriodPanel positions={positions} />

          {/* Position Risk Table */}
          <PositionRiskTable positions={positions} />

          {/* Prospective Heat Calculator */}
          <ProspectiveHeatPanel currentHeat={heatPercent} />
        </div>
      )}
    </div>
  );
}
