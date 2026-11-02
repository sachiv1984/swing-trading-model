/**
 * Realised P&L by exit condition card for the Monthly P&L report — ST-24 (EPIC-04, v9.14, BLG-FEAT-99).
 *
 * Spec: docs/specs/frontend/pages/reports.md §Exit Condition Breakdown, v0.26
 * Design: docs/design/2026-10-29__release-v9.14/monthly-pnl-exit-condition-breakdown/decision_record.md
 *
 * Display only: each month's §8 categories come from the API's by_exit_condition
 * (the browser never maps exit_reason itself), and the Total column is the
 * month's realised_pnl_gbp / trade_count, the Monthly Financial Table's figures.
 */
import { formatCurrency } from "../../lib/format";

const MONTH_NAMES = [
  "", "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December",
];

// Column headers name the §8 condition (metrics_definitions.md §Exit Condition Category).
const CATEGORIES = [
  { key: "stop_loss", label: "Stop-loss (§8.1)" },
  { key: "risk_off", label: "Risk-off (§8.2)" },
  { key: "manual", label: "Manual (§8.3)" },
];

const toPennies = (value) => Math.round((value ?? 0) * 100);

// The Monthly Financial Table's P&L tone rule: green, red, neutral at exactly zero.
function pnlTone(pnl) {
  if (pnl > 0) return "text-emerald-700 dark:text-emerald-400";
  if (pnl < 0) return "text-rose-700 dark:text-rose-400";
  return "text-slate-600 dark:text-slate-400";
}

// A category with no trades shows "—" and no trade line (Avg P&L/Trade convention).
function PnlCell({ pnl, count, testId, strong = false }) {
  if (!count) {
    return (
      <td data-testid={testId} className="px-4 py-3 text-right text-slate-600 dark:text-slate-400">
        —
      </td>
    );
  }
  return (
    <td data-testid={testId} className="px-4 py-3 text-right whitespace-nowrap">
      <span data-testid={`${testId}-pnl`} className={`block ${strong ? "font-semibold" : "font-medium"} ${pnlTone(pnl)}`}>
        {formatCurrency(pnl)}
      </span>
      <span data-testid={`${testId}-trades`} className="block text-xs text-slate-600 dark:text-slate-400">
        {count} {count === 1 ? "trade" : "trades"}
      </span>
    </td>
  );
}

export default function ExitConditionBreakdownCard({ rows }) {
  // by_exit_condition is present on every month or on none (reports_endpoints.md v0.19).
  const available = rows.length > 0 && rows.every((row) => row.by_exit_condition);

  // Sum in pennies so the footer is exact for the 2 dp figures the API returns.
  const footer = { total: { pennies: 0, count: 0 } };
  CATEGORIES.forEach(({ key }) => { footer[key] = { pennies: 0, count: 0 }; });
  if (available) {
    rows.forEach((row) => {
      footer.total.pennies += toPennies(row.realised_pnl_gbp);
      footer.total.count += row.trade_count ?? 0;
      CATEGORIES.forEach(({ key }) => {
        const cat = row.by_exit_condition[key] ?? {};
        footer[key].pennies += toPennies(cat.realised_pnl_gbp);
        footer[key].count += cat.trade_count ?? 0;
      });
    });
  }

  const thClass = "px-4 py-3 text-right text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider whitespace-nowrap";
  // Sticky Month column keeps the card surface behind it while the table scrolls.
  const stickyClass = "sticky left-0 bg-white dark:bg-slate-800";

  return (
    <div
      data-testid="monthly-exit-condition-card"
      className="bg-white dark:bg-slate-800/50 rounded-lg border border-slate-200 dark:border-slate-700/50 overflow-hidden"
    >
      <div className="px-6 py-4 border-b border-slate-200 dark:border-slate-700/50">
        <h3 className="text-sm font-semibold text-slate-900 dark:text-white">Realised P&L by exit condition</h3>
      </div>
      {!available ? (
        <p data-testid="monthly-exit-condition-unavailable" className="px-6 py-4 text-sm text-slate-600 dark:text-slate-400">
          Exit-condition breakdown unavailable.
        </p>
      ) : (
        <>
          <div className="overflow-x-auto">
            <table data-testid="monthly-exit-condition-table" className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-200 dark:border-slate-700/50">
                  <th className={`${stickyClass} px-4 py-3 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider`}>Month</th>
                  {CATEGORIES.map(({ key, label }) => (
                    <th key={key} data-testid={`monthly-exit-condition-header-${key}`} className={thClass}>{label}</th>
                  ))}
                  <th className={thClass}>Total</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 dark:divide-slate-700/30">
                {rows.map((row) => {
                  const monthKey = `${row.year}-${row.month}`;
                  return (
                    <tr key={monthKey} data-testid="monthly-exit-condition-row">
                      <td className={`${stickyClass} px-4 py-3 text-slate-900 dark:text-white whitespace-nowrap`}>
                        {MONTH_NAMES[row.month]} {row.year}
                      </td>
                      {CATEGORIES.map(({ key }) => (
                        <PnlCell
                          key={key}
                          testId={`monthly-exit-condition-${key}`}
                          pnl={row.by_exit_condition[key]?.realised_pnl_gbp ?? 0}
                          count={row.by_exit_condition[key]?.trade_count ?? 0}
                        />
                      ))}
                      <PnlCell
                        testId="monthly-exit-condition-total"
                        pnl={row.realised_pnl_gbp ?? 0}
                        count={row.trade_count ?? 0}
                      />
                    </tr>
                  );
                })}
              </tbody>
              <tfoot>
                <tr data-testid="monthly-exit-condition-footer" className="border-t border-slate-200 dark:border-slate-700/50">
                  <th scope="row" className={`${stickyClass} px-4 py-3 text-left font-semibold text-slate-900 dark:text-white whitespace-nowrap`}>
                    Tax year total
                  </th>
                  {CATEGORIES.map(({ key }) => (
                    <PnlCell
                      key={key}
                      strong
                      testId={`monthly-exit-condition-footer-${key}`}
                      pnl={footer[key].pennies / 100}
                      count={footer[key].count}
                    />
                  ))}
                  <PnlCell
                    strong
                    testId="monthly-exit-condition-footer-total"
                    pnl={footer.total.pennies / 100}
                    count={footer.total.count}
                  />
                </tr>
              </tfoot>
            </table>
          </div>
          {/* Removed when a §8.4 exit reason is added (BLG-SPEC-206). */}
          <p data-testid="monthly-exit-condition-caption" className="px-6 py-3 text-xs text-slate-600 dark:text-slate-400 border-t border-slate-200 dark:border-slate-700/30">
            Month-end rebalance exits (§8.4) are recorded as Manual Exit and counted under Manual until a separate exit reason exists.
          </p>
        </>
      )}
    </div>
  );
}
