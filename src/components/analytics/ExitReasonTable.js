import { cn } from "../../lib/utils";

export default function ExitReasonTable({ exitReasonData }) {
  return (
    <div className="rounded-2xl bg-slate-800/50 border border-slate-700/50 p-6 backdrop-blur-sm">
      <h3 className="text-lg font-semibold text-white mb-6">Performance by Exit Reason</h3>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-700/50">
              <th className="text-left text-xs text-slate-400 font-medium py-3 px-4">Exit Reason</th>
              <th className="text-right text-xs text-slate-400 font-medium py-3 px-4">Count</th>
              <th className="text-right text-xs text-slate-400 font-medium py-3 px-4">Win Rate</th>
              <th className="text-right text-xs text-slate-400 font-medium py-3 px-4">Total P&L</th>
              <th className="text-right text-xs text-slate-400 font-medium py-3 px-4">Avg P&L</th>
              <th className="text-right text-xs text-slate-400 font-medium py-3 px-4">% of Trades</th>
            </tr>
          </thead>
          <tbody>
            {exitReasonData.map((row, idx) => (
              <tr key={idx} className="border-b border-slate-700/30 hover:bg-slate-800/30 transition-colors">
                <td className="py-3 px-4 text-sm text-white font-medium">{row.reason}</td>
                <td className="py-3 px-4 text-sm text-slate-300 text-right">{row.count}</td>
                <td className="py-3 px-4 text-sm text-slate-300 text-right">{row.winRate.toFixed(1)}%</td>
                <td className={cn(
                  "py-3 px-4 text-sm font-semibold text-right",
                  row.totalPnl >= 0 ? "text-emerald-400" : "text-rose-400"
                )}>
                  {row.totalPnl >= 0 ? "+" : ""}£{row.totalPnl.toFixed(2)}
                </td>
                <td className={cn(
                  "py-3 px-4 text-sm font-semibold text-right",
                  row.avgPnl >= 0 ? "text-emerald-400" : "text-rose-400"
                )}>
                  {row.avgPnl >= 0 ? "+" : ""}£{row.avgPnl.toFixed(2)}
                </td>
                <td className="py-3 px-4 text-sm text-slate-300 text-right">{row.percentage.toFixed(1)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
