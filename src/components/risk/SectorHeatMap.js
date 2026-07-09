import { useQuery } from "@tanstack/react-query";
import { api } from "../../api/base44Client";

function tileClass(exposurePct) {
  if (exposurePct >= 40) return "border border-amber-400 bg-amber-400/10";
  if (exposurePct >= 20) return "border border-amber-400/60";
  return "border border-slate-700";
}

function SectorTile({ sector_name, position_count, exposure_pct }) {
  return (
    <div
      data-testid="sector-tile"
      data-sector={sector_name}
      className={`rounded-lg p-3 flex flex-col gap-1 min-w-0 ${tileClass(exposure_pct)}`}
    >
      <span className="text-xs text-slate-600 dark:text-slate-400 truncate" title={sector_name}>
        {sector_name}
      </span>
      <span className="text-lg font-semibold text-white leading-tight">
        {exposure_pct.toFixed(1)}%
      </span>
      <span className="text-xs text-slate-600 dark:text-slate-400">
        {position_count} {position_count === 1 ? "position" : "positions"}
      </span>
    </div>
  );
}

export default function SectorHeatMap() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["sector-weights"],
    queryFn: api.portfolio.sectorWeights,
    staleTime: 60_000,
  });

  if (isLoading) {
    return (
      <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
        <h3 className="text-sm font-medium text-slate-300 mb-3">Sector Concentration</h3>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-20 rounded-lg bg-slate-800 animate-pulse" />
          ))}
        </div>
      </div>
    );
  }

  if (isError) {
    return null;
  }

  const sectors = data?.sectors ?? [];
  const concentrationAlert = data?.concentration_alert ?? false;

  if (sectors.length === 0) {
    return (
      <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
        <h3 className="text-sm font-medium text-slate-300 mb-2">Sector Concentration</h3>
        <p className="text-sm text-slate-600 dark:text-slate-400">No open positions.</p>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-medium text-slate-300">Sector Concentration</h3>
        {concentrationAlert && (
          <span className="text-xs font-medium text-amber-400 bg-amber-400/10 border border-amber-400/30 rounded px-2 py-0.5">
            Concentration Alert
          </span>
        )}
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
        {sectors.map((s) => (
          <SectorTile key={s.sector_name} {...s} />
        ))}
      </div>
    </div>
  );
}
