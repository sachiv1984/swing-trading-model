import { cn } from "../../lib/utils";
import { formatCurrency, formatPercent } from "../../lib/format";

export default function ExitReasonTable({ exitReasonData }) {
  return (
    <div className="rounded-2xl bg-app-raised border border-app-line p-6 backdrop-blur-sm">
      <h3 className="text-lg font-semibold text-app-fg mb-6">Performance by Exit Reason</h3>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-app-line">
              <th className="text-left text-xs text-slate-600 dark:text-slate-400 font-medium py-3 px-4">Exit Reason</th>
              <th className="text-right text-xs text-slate-600 dark:text-slate-400 font-medium py-3 px-4">Count</th>
              <th className="text-right text-xs text-slate-600 dark:text-slate-400 font-medium py-3 px-4">Win Rate</th>
              <th className="text-right text-xs text-slate-600 dark:text-slate-400 font-medium py-3 px-4">Total P&L</th>
              <th className="text-right text-xs text-slate-600 dark:text-slate-400 font-medium py-3 px-4">Avg P&L</th>
              <th className="text-right text-xs text-slate-600 dark:text-slate-400 font-medium py-3 px-4">% of Trades</th>
            </tr>
          </thead>
          <tbody>
            {exitReasonData.map((row, idx) => (
              <tr key={idx} className="border-b border-slate-200 dark:border-slate-700/30 hover:bg-slate-100 dark:hover:bg-slate-800/30 transition-colors">
                <td className="py-3 px-4 text-sm text-app-fg font-medium">{row.reason}</td>
                <td className="py-3 px-4 text-sm text-slate-700 dark:text-slate-300 text-right">{row.count}</td>
                <td className="py-3 px-4 text-sm text-slate-700 dark:text-slate-300 text-right">{formatPercent(row.winRate)}</td>
                <td className={cn(
                  "py-3 px-4 text-sm font-semibold text-right",
                  row.totalPnl > 0 ? "text-app-positive" : row.totalPnl < 0 ? "text-app-negative" : "text-slate-700 dark:text-slate-300"
                )}>
                  {formatCurrency(row.totalPnl, { signed: true })}
                </td>
                <td className={cn(
                  "py-3 px-4 text-sm font-semibold text-right",
                  row.avgPnl > 0 ? "text-app-positive" : row.avgPnl < 0 ? "text-app-negative" : "text-slate-700 dark:text-slate-300"
                )}>
                  {formatCurrency(row.avgPnl, { signed: true })}
                </td>
                <td className="py-3 px-4 text-sm text-slate-700 dark:text-slate-300 text-right">{formatPercent(row.percentage)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
