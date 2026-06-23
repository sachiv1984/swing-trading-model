import { useQuery } from "@tanstack/react-query";
import { base44, api } from "../api/base44Client";
import { Loader2 } from "lucide-react";
import PageHeader from "../components/ui/PageHeader";
import HeatGauge from "../components/risk/HeatGauge";
import DrawdownSummary from "../components/risk/DrawdownSummary";
import GracePeriodPanel from "../components/risk/GracePeriodPanel";
import PositionRiskTable from "../components/risk/PositionRiskTable";
import SectorHeatMap from "../components/risk/SectorHeatMap";
import ProspectiveHeatPanel from "../components/risk/ProspectiveHeatPanel";

export default function RiskDashboard() {
  const {
    data: portfolioData,
    isLoading: loadingPortfolio,
    error: portfolioError,
    refetch,
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
    enabled: !!portfolioError,
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

  // Only surface position error when entity fallback is not providing data
  const positionError = usingEntityFallback ? null : portfolioError;

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
            <HeatGauge
              heatPercent={heatPercent}
              positionRisks={portfolioData?.position_risks ?? []}
              error={portfolioError}
              onRetry={refetch}
            />
            <DrawdownSummary
              drawdownPercent={drawdownPercent}
              peakValue={peakValue}
              error={portfolioError}
            />
          </div>

          {usingEntityFallback && (
            <p className="text-xs text-amber-400">Live heat unavailable — showing entity data fallback.</p>
          )}

          {/* Grace Period Panel */}
          <GracePeriodPanel positions={positions} error={positionError} />

          {/* Position Risk Table */}
          <PositionRiskTable positions={positions} error={positionError} />

          {/* Sector Concentration Heat Map — manages its own query */}
          <SectorHeatMap />

          {/* Prospective Heat Calculator — manages its own error state */}
          <ProspectiveHeatPanel currentHeat={heatPercent} />
        </div>
      )}
    </div>
  );
}
