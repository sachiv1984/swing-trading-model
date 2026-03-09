import { useQuery } from "@tanstack/react-query";
import { Loader2 } from "lucide-react";
import PageHeader from "@/components/ui/PageHeader";
import HeatGauge from "@/components/risk/HeatGauge";
import DrawdownSummary from "@/components/risk/DrawdownSummary";
import GracePeriodPanel from "@/components/risk/GracePeriodPanel";
import PositionRiskTable from "@/components/risk/PositionRiskTable";
import ProspectiveHeatPanel from "@/components/risk/ProspectiveHeatPanel";

export default function RiskDashboard() {
  const {
    data: portfolioData,
    isLoading,
    error: portfolioError,
    refetch,
  } = useQuery({
    queryKey: ["riskPortfolio"],
    queryFn: async () => {
      const res = await fetch("/api/portfolio");
      if (!res.ok) throw new Error(`Portfolio API error ${res.status}`);
      return res.json();
    },
    retry: 1,
  });

  const positions = portfolioData?.positions ?? [];

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
              heatPercent={portfolioData?.portfolio_heat_percent ?? null}
              positionRisks={portfolioData?.position_risks ?? []}
              error={portfolioError}
              onRetry={refetch}
            />
            <DrawdownSummary
              drawdownPercent={portfolioData?.current_drawdown_percent ?? null}
              peakValue={portfolioData?.peak_portfolio_value ?? null}
              error={portfolioError}
            />
          </div>

          {/* Grace Period Panel */}
          <GracePeriodPanel positions={positions} error={portfolioError} />

          {/* Position Risk Table */}
          <PositionRiskTable positions={positions} error={portfolioError} />

          {/* Prospective Heat Calculator — manages its own error state */}
          <ProspectiveHeatPanel currentHeat={portfolioData?.portfolio_heat_percent ?? null} />
        </div>
      )}
    </div>
  );
}
