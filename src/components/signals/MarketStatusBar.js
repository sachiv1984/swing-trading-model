import { TrendingUp, TrendingDown } from "lucide-react";
import { cn } from "@/lib/utils";

export default function MarketStatusBar({ spyStatus, ftseStatus, fxRate, availableCash }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/50">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-slate-400">SPY (US)</span>
          <span className="text-lg">🇺🇸</span>
        </div>
        <div className="flex items-center gap-2">
          {spyStatus?.isRiskOn ? (
            <>
              <TrendingUp className="w-5 h-5 text-emerald-400" />
              <span className="font-bold text-emerald-400">Risk On</span>
            </>
          ) : (
            <>
              <TrendingDown className="w-5 h-5 text-rose-400" />
              <span className="font-bold text-rose-400">Risk Off</span>
            </>
          )}
        </div>
        <p className="text-xs text-slate-500 mt-1">
          ${spyStatus?.price.toFixed(2)} vs MA200
        </p>
      </div>

      <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/50">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-slate-400">FTSE (UK)</span>
          <span className="text-lg">🇬🇧</span>
        </div>
        <div className="flex items-center gap-2">
          {ftseStatus?.isRiskOn ? (
            <>
              <TrendingUp className="w-5 h-5 text-emerald-400" />
              <span className="font-bold text-emerald-400">Risk On</span>
            </>
          ) : (
            <>
              <TrendingDown className="w-5 h-5 text-rose-400" />
              <span className="font-bold text-rose-400">Risk Off</span>
            </>
          )}
        </div>
        <p className="text-xs text-slate-500 mt-1">
          £{ftseStatus?.price.toFixed(2)} vs MA200
        </p>
      </div>

      <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/50">
        <span className="text-sm text-slate-400 block mb-2">FX Rate</span>
        <p className="text-lg font-bold text-white">1 GBP = ${fxRate.toFixed(4)} USD</p>
      </div>

      <div className="p-4 rounded-xl bg-gradient-to-br from-cyan-500/10 to-violet-500/10 border border-cyan-500/30">
        <span className="text-sm text-slate-400 block mb-2">Available Cash</span>
        <p className="text-lg font-bold text-white">£{availableCash.toLocaleString()}</p>
      </div>
    </div>
  );
}
