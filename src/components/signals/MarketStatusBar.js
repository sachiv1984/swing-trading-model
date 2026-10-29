import { TrendingUp, TrendingDown, HelpCircle } from "lucide-react";
import { formatCurrency } from "../../lib/format";
import ExplainedMarker from "../ui/ExplainedMarker";
import { REGIME_RISK_ON, REGIME_RISK_OFF, REGIME_UNKNOWN, unknownRegimeExplanation } from "../../lib/regime";

function RegimeStatus({ status, region }) {
  if (status === REGIME_RISK_ON) {
    return (
      <>
        <TrendingUp className="w-5 h-5 text-emerald-400" />
        <span className="font-bold text-emerald-400">Risk On</span>
      </>
    );
  }
  if (status === REGIME_RISK_OFF) {
    return (
      <>
        <TrendingDown className="w-5 h-5 text-rose-400" />
        <span className="font-bold text-rose-400">Risk Off</span>
      </>
    );
  }
  if (status === REGIME_UNKNOWN) {
    return (
      <ExplainedMarker
        label={`${region} market regime unknown`}
        description={unknownRegimeExplanation(region)}
        testId={`signals-regime-unknown-${region}`}
        className="text-slate-700 dark:text-slate-300 ring-slate-500"
      >
        <HelpCircle className="w-5 h-5" aria-hidden="true" />
        <span className="font-bold">Unknown</span>
      </ExplainedMarker>
    );
  }
  return <span className="font-bold text-slate-600 dark:text-slate-400">—</span>;
}

function RegimeTile({ name, flag, region, index, currency }) {
  const measured = index?.status === REGIME_RISK_ON || index?.status === REGIME_RISK_OFF;
  return (
    <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/50" data-testid={`signals-regime-${region}`}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm text-slate-600 dark:text-slate-400">{name}</span>
        <span className="text-lg">{flag}</span>
      </div>
      <div className="flex items-center gap-2">
        <RegimeStatus status={index?.status} region={region} />
      </div>
      <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">
        {measured && index?.price != null
          ? `${formatCurrency(index.price, currency ? { currency } : undefined)} vs MA200`
          : index?.status === REGIME_UNKNOWN ? "Price unavailable" : "—"}
      </p>
    </div>
  );
}

export default function MarketStatusBar({ spyStatus, ftseStatus, fxRate, availableCash }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <RegimeTile name="SPY (US)" flag="🇺🇸" region="US" index={spyStatus} currency="USD" />
      <RegimeTile name="FTSE (UK)" flag="🇬🇧" region="UK" index={ftseStatus} />

      <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/50">
        <span className="text-sm text-slate-600 dark:text-slate-400 block mb-2">FX Rate</span>
        <p className="text-lg font-bold text-white">1 GBP = ${fxRate.toFixed(4)} USD</p>
      </div>

      <div className="p-4 rounded-xl bg-gradient-to-br from-cyan-500/10 to-violet-500/10 border border-cyan-500/30">
        <span className="text-sm text-slate-600 dark:text-slate-400 block mb-2">Available Cash</span>
        <p className="text-lg font-bold text-white">{formatCurrency(availableCash)}</p>
      </div>
    </div>
  );
}
