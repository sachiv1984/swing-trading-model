'use strict';

import { useState, useEffect, useCallback } from 'react';
import { api } from '../api/base44Client';
import { BarChart2, RefreshCw, Upload, ChevronDown } from 'lucide-react';

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const MARKETS = ['ALL', 'US', 'UK'];

// Exit reason → badge config
const EXIT_REASON_BADGE = {
  Stop:             { label: 'Stop',      cls: 'bg-red-600 text-white' },
  stop:             { label: 'Stop',      cls: 'bg-red-600 text-white' },
  trailing_stop:    { label: 'Stop',      cls: 'bg-red-600 text-white' },
  'Risk-Off':       { label: 'Risk-Off',  cls: 'bg-amber-600 text-white' },
  risk_off:         { label: 'Risk-Off',  cls: 'bg-amber-600 text-white' },
  Rebalance:        { label: 'Rebalance', cls: 'bg-teal-600 text-white' },
  exit_rebalance:   { label: 'Rebalance', cls: 'bg-teal-600 text-white' },
};

const TOGGLE_MODES = ['backtest', 'actual', 'side-by-side'];
const TOGGLE_LABELS = {
  backtest:      'Backtest Only',
  actual:        'Actual Only',
  'side-by-side':'Side by Side',
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function fmtPct(val) {
  if (val == null) return '—';
  return `${Number(val).toFixed(1)}%`;
}

function fmtGbp(val) {
  if (val == null) return '—';
  const n = Number(val);
  return (n < 0 ? '-£' : '£') + Math.abs(n).toLocaleString('en-GB', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
}

function fmtDays(val) {
  if (val == null) return '—';
  return `${Number(val).toFixed(1)}d`;
}

function fmtNum(val) {
  if (val == null) return '—';
  return String(Number(val));
}

function pnlClass(val) {
  if (val == null) return 'text-slate-400';
  return Number(val) >= 0 ? 'text-green-400' : 'text-red-400';
}

// Panel 0 (Open Positions) uses emerald/rose per ux_spec.md, distinct from the
// green-400/red-400 used by the realized-trade panels above — reinforces that
// unrealized figures are visually separate from realized ones (AC-02).
function unrealizedPnlClass(val) {
  if (val == null) return 'text-slate-400';
  return Number(val) >= 0 ? 'text-emerald-400' : 'text-rose-400';
}

function fmtGbpSigned(val, decimals = 0) {
  if (val == null) return '—';
  const n = Number(val);
  const sign = n >= 0 ? '+' : '-';
  return sign + '£' + Math.abs(n).toLocaleString('en-GB', { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
}

function fmtGbpPrice(val) {
  if (val == null) return '—';
  return '£' + Number(val).toLocaleString('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function fmtPctSigned(val) {
  if (val == null) return '—';
  const n = Number(val);
  return (n >= 0 ? '+' : '') + n.toFixed(1) + '%';
}

function fmtDateLong(val) {
  if (!val) return '—';
  const d = new Date(val);
  if (Number.isNaN(d.getTime())) return '—';
  return d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
}

function MarketBadge({ market }) {
  const cls =
    market === 'UK'
      ? 'bg-blue-500/20 text-blue-400 border-blue-500/30'
      : 'bg-violet-500/20 text-violet-400 border-violet-500/30';
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${cls}`}>
      {market}
    </span>
  );
}

function ExitBadge({ reason }) {
  const config = EXIT_REASON_BADGE[reason] || null;
  if (!config) return <span className="text-xs text-slate-400">{reason || '—'}</span>;
  return (
    <span className={`text-xs font-bold px-1.5 py-0.5 rounded ${config.cls}`}>
      {config.label}
    </span>
  );
}

// ---------------------------------------------------------------------------
// Panel 0 — Open Positions
// ---------------------------------------------------------------------------

function Panel0({ openPositions, loading, error, showMarketBadge }) {
  // Error state: header + muted inline message only — does not break rest of page (AC per ux_spec.md "States").
  if (error) {
    return (
      <section data-testid="benchmark-panel-0">
        <h2 className="text-sm font-semibold text-white mb-3">Open Positions</h2>
        <p className="text-sm text-slate-400" data-testid="benchmark-open-positions-error">
          Open positions temporarily unavailable.
        </p>
      </section>
    );
  }

  if (loading) {
    return (
      <section data-testid="benchmark-panel-0">
        <h2 className="text-sm font-semibold text-white mb-3">Open Positions</h2>
        <div className="space-y-2 animate-pulse" data-testid="benchmark-open-positions-loading">
          {[1, 2, 3].map(i => <div key={i} className="h-8 bg-slate-800 rounded-md" />)}
        </div>
      </section>
    );
  }

  const positions = openPositions?.open_positions || [];
  const summary = openPositions?.summary;

  // Zero open positions: panel omitted entirely — no empty-state card (ux_spec.md "Conditional Rendering").
  if (positions.length === 0) return null;

  const count = summary?.count ?? positions.length;
  const total = summary?.total_unrealized_pnl_gbp;
  const summaryColour = total != null && Number(total) < 0 ? 'text-rose-400' : 'text-emerald-400';

  return (
    <section data-testid="benchmark-panel-0">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-sm font-semibold text-white">Open Positions</h2>
      </div>
      <p className={`text-sm mb-3 ${summaryColour}`} data-testid="benchmark-open-positions-summary">
        {count} open position{count === 1 ? '' : 's'} · {fmtGbpSigned(total)} unrealized
      </p>
      <div className="overflow-x-auto">
        <table className="w-full text-sm" data-testid="benchmark-open-positions-table">
          <thead>
            <tr className="text-xs text-slate-400 border-b border-slate-700">
              <th scope="col" className="text-left py-2 pr-3">Ticker</th>
              <th scope="col" className="text-left py-2 pr-3">Entry</th>
              <th scope="col" className="text-right py-2 pr-3">Entry £</th>
              <th scope="col" className="text-right py-2 pr-3">Current £</th>
              <th scope="col" className="text-right py-2 pr-3">P&L £</th>
              <th scope="col" className="text-right py-2 pr-3">P&L %</th>
              <th scope="col" className="text-right py-2">Days</th>
            </tr>
          </thead>
          <tbody>
            {positions.map(pos => (
              <tr
                key={`${pos.ticker}-${pos.entry_date}`}
                className="border-b border-slate-800 hover:bg-slate-800/40"
                data-testid={`benchmark-open-position-${pos.ticker}`}
              >
                <td className="py-2 pr-3">
                  <span className="font-semibold text-white">{pos.ticker}</span>
                  {showMarketBadge && (
                    <span className="ml-1.5 inline-block align-middle">
                      <MarketBadge market={pos.market} />
                    </span>
                  )}
                </td>
                <td className="py-2 pr-3 text-slate-400">{fmtDateLong(pos.entry_date)}</td>
                <td className="py-2 pr-3 text-right text-slate-300">{fmtGbpPrice(pos.entry_price)}</td>
                <td className="py-2 pr-3 text-right text-slate-300">{fmtGbpPrice(pos.current_price)}</td>
                <td className={`py-2 pr-3 text-right ${unrealizedPnlClass(pos.unrealized_pnl_gbp)}`}>{fmtGbpSigned(pos.unrealized_pnl_gbp, 2)}</td>
                <td className={`py-2 pr-3 text-right ${unrealizedPnlClass(pos.unrealized_pnl_pct)}`}>{fmtPctSigned(pos.unrealized_pnl_pct)}</td>
                <td className="py-2 text-right text-slate-300">{pos.days_held ?? '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

// ---------------------------------------------------------------------------
// Panel 1 — Performance Parity stat cards
// ---------------------------------------------------------------------------

function StatCard({ label, backtest, actual }) {
  return (
    <div className="bg-slate-800 rounded-lg p-3 border border-slate-700">
      <p className="text-xs text-slate-400 mb-2">{label}</p>
      <div className="flex items-end justify-between gap-2">
        <div>
          <p className="text-xs text-slate-400 mb-0.5">Backtest</p>
          <p className="text-base font-semibold text-white">{backtest}</p>
        </div>
        <div className="text-right">
          <p className="text-xs text-slate-400 mb-0.5">Actual</p>
          <p className="text-base font-semibold text-slate-400">{actual}</p>
        </div>
      </div>
    </div>
  );
}

function Panel1({ backtest, actual, lastImportedAt }) {
  const bt = backtest || {};
  const ac = actual;

  const fmtActual = (fn, key) => ac ? fn(ac[key]) : '—';

  return (
    <section data-testid="benchmark-panel-1">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-sm font-semibold text-white">Performance Parity</h2>
        {lastImportedAt && (
          <span className="text-xs text-slate-400">
            Last updated {new Date(lastImportedAt).toLocaleDateString('en-GB')}
          </span>
        )}
      </div>

      {!backtest ? (
        <p className="text-sm text-slate-400 italic" data-testid="benchmark-no-data">
          No backtest data imported yet. Run{' '}
          <code className="text-xs bg-slate-800 px-1 py-0.5 rounded">python import_backtest.py</code>{' '}
          to import production_strategy.py results.
        </p>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3" data-testid="benchmark-stat-cards">
          <StatCard
            label="Total Trades"
            backtest={fmtNum(bt.total_trades)}
            actual={fmtActual(fmtNum, 'total_trades')}
          />
          <StatCard
            label="Win Rate"
            backtest={fmtPct(bt.win_rate_pct)}
            actual={fmtActual(fmtPct, 'win_rate_pct')}
          />
          <StatCard
            label="Avg P&L"
            backtest={fmtGbp(bt.avg_pnl_gbp)}
            actual={fmtActual(fmtGbp, 'avg_pnl_gbp')}
          />
          <StatCard
            label="Total P&L"
            backtest={fmtGbp(bt.total_pnl_gbp)}
            actual={fmtActual(fmtGbp, 'total_pnl_gbp')}
          />
          <StatCard
            label="Avg Hold"
            backtest={fmtDays(bt.avg_hold_days)}
            actual={fmtActual(fmtDays, 'avg_hold_days')}
          />
        </div>
      )}
    </section>
  );
}

// ---------------------------------------------------------------------------
// Panel 2 — Yearly Breakdown table
// ---------------------------------------------------------------------------

function Panel2({ rows }) {
  if (!rows || rows.length === 0) {
    return (
      <section data-testid="benchmark-panel-2">
        <h2 className="text-sm font-semibold text-white mb-3">Yearly Breakdown</h2>
        <p className="text-sm text-slate-400 italic">No yearly data available.</p>
      </section>
    );
  }

  return (
    <section data-testid="benchmark-panel-2">
      <h2 className="text-sm font-semibold text-white mb-3">Yearly Breakdown</h2>
      <div className="overflow-x-auto">
        <table className="w-full text-sm" data-testid="benchmark-yearly-table">
          <thead>
            <tr className="text-xs text-slate-400 border-b border-slate-700">
              <th className="text-left py-2 pr-4">Year</th>
              <th className="text-right py-2 pr-4">Trades</th>
              <th className="text-right py-2 pr-4">Win Rate</th>
              <th className="text-right py-2 pr-4">Avg P&L</th>
              <th className="text-right py-2 pr-4">Total P&L</th>
              <th className="text-right py-2">Avg Hold</th>
            </tr>
          </thead>
          <tbody>
            {rows.map(row => (
              <tr
                key={row.entry_year}
                className="border-b border-slate-800 hover:bg-slate-800/40"
                data-testid={`benchmark-year-row-${row.entry_year}`}
              >
                <td className="py-2 pr-4 font-medium text-white">{row.entry_year}</td>
                <td className="py-2 pr-4 text-right text-slate-300">{fmtNum(row.num_trades)}</td>
                <td className="py-2 pr-4 text-right text-slate-300">{fmtPct(row.win_rate_pct)}</td>
                <td className={`py-2 pr-4 text-right ${pnlClass(row.avg_pnl_gbp)}`}>{fmtGbp(row.avg_pnl_gbp)}</td>
                <td className={`py-2 pr-4 text-right ${pnlClass(row.total_pnl_gbp)}`}>{fmtGbp(row.total_pnl_gbp)}</td>
                <td className="py-2 text-right text-slate-300">{fmtDays(row.avg_hold_days)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

// ---------------------------------------------------------------------------
// Panel 3 — Trade Log
// ---------------------------------------------------------------------------

function TradeRow({ trade, source }) {
  return (
    <tr className="border-b border-slate-800 hover:bg-slate-800/40 text-sm">
      <td className="py-2 pr-3">
        <span className="font-semibold text-white">{trade.ticker}</span>
        {source && (
          <span className={`ml-1.5 text-xs px-1 py-0.5 rounded ${source === 'backtest' ? 'bg-slate-700 text-slate-400' : 'bg-blue-900 text-blue-300'}`}>
            {source === 'backtest' ? 'BT' : 'Live'}
          </span>
        )}
      </td>
      <td className="py-2 pr-3 text-slate-400">{trade.entry_date || '—'}</td>
      <td className="py-2 pr-3 text-slate-400">{trade.exit_date || '—'}</td>
      <td className="py-2 pr-3 text-slate-400">{trade.holding_days != null ? `${trade.holding_days}d` : '—'}</td>
      <td className="py-2 pr-3">
        <ExitBadge reason={trade.exit_reason} />
      </td>
      <td className={`py-2 pr-3 text-right ${pnlClass(trade.pnl_gbp)}`}>{fmtGbp(trade.pnl_gbp)}</td>
      <td className={`py-2 text-right ${pnlClass(trade.pnl_pct)}`}>{fmtPct(trade.pnl_pct)}</td>
    </tr>
  );
}

function Panel3({ backtestTrades, actualTrades, toggleMode, onToggleMode }) {
  const showBacktest = toggleMode === 'backtest' || toggleMode === 'side-by-side';
  const showActual = toggleMode === 'actual' || toggleMode === 'side-by-side';
  const sideBySide = toggleMode === 'side-by-side';

  let rows = [];
  if (sideBySide) {
    const btRows = (backtestTrades || []).map(t => ({ ...t, _src: 'backtest' }));
    const acRows = (actualTrades || []).map(t => ({ ...t, _src: 'actual' }));
    rows = [...btRows, ...acRows].sort((a, b) =>
      (a.entry_date || '').localeCompare(b.entry_date || '')
    );
  } else if (showBacktest) {
    rows = (backtestTrades || []).map(t => ({ ...t, _src: null }));
  } else {
    rows = (actualTrades || []).map(t => ({ ...t, _src: null }));
  }

  return (
    <section data-testid="benchmark-panel-3">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-sm font-semibold text-white">Trade Log</h2>
        <div className="flex gap-1" data-testid="benchmark-toggle-modes">
          {TOGGLE_MODES.map(mode => (
            <button
              key={mode}
              onClick={() => onToggleMode(mode)}
              className={`text-xs px-2.5 py-1 rounded-md border transition-colors ${
                toggleMode === mode
                  ? 'border-slate-400 bg-slate-700 text-white'
                  : 'border-slate-700 text-slate-400 hover:text-slate-300 hover:bg-slate-800'
              }`}
              data-testid={`benchmark-mode-${mode}`}
            >
              {TOGGLE_LABELS[mode]}
            </button>
          ))}
        </div>
      </div>

      {rows.length === 0 ? (
        <p className="text-sm text-slate-400 italic" data-testid="benchmark-trades-empty">
          No trades for the selected filter.
        </p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm" data-testid="benchmark-trade-table">
            <thead>
              <tr className="text-xs text-slate-400 border-b border-slate-700">
                <th className="text-left py-2 pr-3">Ticker</th>
                <th className="text-left py-2 pr-3">Entry</th>
                <th className="text-left py-2 pr-3">Exit</th>
                <th className="text-left py-2 pr-3">Hold</th>
                <th className="text-left py-2 pr-3">Reason</th>
                <th className="text-right py-2 pr-3">P&L (£)</th>
                <th className="text-right py-2">P&L %</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((trade, i) => (
                <TradeRow key={`${trade.ticker}-${trade.entry_date}-${i}`} trade={trade} source={trade._src} />
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

// ---------------------------------------------------------------------------
// Main page
// ---------------------------------------------------------------------------

export default function StrategyBenchmark() {
  const [year, setYear] = useState(null);
  const [market, setMarket] = useState('ALL');
  const [toggleMode, setToggleMode] = useState('backtest');

  const [summary, setSummary] = useState(null);
  const [trades, setTrades] = useState(null);
  const [openPositions, setOpenPositions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [openPositionsLoading, setOpenPositionsLoading] = useState(false);
  const [openPositionsError, setOpenPositionsError] = useState(false);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    setOpenPositionsLoading(true);
    setOpenPositionsError(false);

    // Open Positions (Panel 0) is fetched independently of summary/trades — an
    // API error here must not take down the rest of the page (ux_spec.md
    // "States"). No year param: open positions are current-state, not
    // historical-per-year (see Filter Interaction in the spec).
    const [mainResult, openPositionsResult] = await Promise.allSettled([
      Promise.all([
        api.strategyBenchmark.getSummary({ year, market }),
        api.strategyBenchmark.getTrades({ year, market }),
      ]),
      api.strategyBenchmark.getOpenPositions({ market }),
    ]);

    if (mainResult.status === 'fulfilled') {
      const [s, t] = mainResult.value;
      setSummary(s);
      setTrades(t);
    } else {
      setError('Failed to load benchmark data. Check the API is running.');
    }
    setLoading(false);

    if (openPositionsResult.status === 'fulfilled') {
      setOpenPositions(openPositionsResult.value);
    } else {
      setOpenPositionsError(true);
    }
    setOpenPositionsLoading(false);
  }, [year, market]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const availableYears = summary?.available_years || [];

  return (
    <div className="p-4 md:p-6 space-y-6 max-w-7xl mx-auto" data-testid="strategy-benchmark-page">

      {/* Page header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <BarChart2 className="w-5 h-5 text-slate-400" />
          <div>
            <h1 className="text-lg font-semibold text-white">Strategy Benchmark</h1>
            <p className="text-xs text-slate-400">Compare live trades against production backtest results</p>
          </div>
        </div>
        <button
          onClick={fetchData}
          disabled={loading}
          className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-md border border-slate-600 text-slate-300 hover:bg-slate-800 disabled:opacity-50"
          data-testid="benchmark-refresh-btn"
        >
          <RefreshCw className={`w-3 h-3 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      {/* Sticky filters */}
      <div
        className="sticky top-0 z-10 bg-slate-900/95 backdrop-blur-sm border border-slate-700 rounded-lg p-3 flex flex-wrap gap-3 items-center"
        data-testid="benchmark-filters"
      >
        {/* Year filter */}
        <div className="flex items-center gap-2">
          <label className="text-xs text-slate-400 shrink-0">Year</label>
          <div className="relative">
            <select
              value={year == null ? 'all' : String(year)}
              onChange={e => setYear(e.target.value === 'all' ? null : Number(e.target.value))}
              className="appearance-none bg-slate-800 border border-slate-600 rounded-md pl-3 pr-7 py-1.5 text-xs text-slate-300 focus:outline-none focus:border-slate-400"
              data-testid="benchmark-year-filter"
            >
              <option value="all">All Years</option>
              {availableYears.map(y => (
                <option key={y} value={String(y)}>{y}</option>
              ))}
            </select>
            <ChevronDown className="absolute right-2 top-1/2 -translate-y-1/2 w-3 h-3 text-slate-500 pointer-events-none" />
          </div>
        </div>

        {/* Market filter */}
        <div className="flex items-center gap-2">
          <label className="text-xs text-slate-400 shrink-0">Market</label>
          <div className="flex gap-1">
            {MARKETS.map(m => (
              <button
                key={m}
                onClick={() => setMarket(m)}
                className={`text-xs px-2.5 py-1 rounded-md border transition-colors ${
                  market === m
                    ? 'border-slate-400 bg-slate-700 text-white'
                    : 'border-slate-700 text-slate-400 hover:text-slate-300 hover:bg-slate-800'
                }`}
                data-testid={`benchmark-market-${m.toLowerCase()}`}
              >
                {m}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Panel 0 — Open Positions (independent loading/error state; renders even if
          Panel 1-3's fetch fails, per ux_spec.md "does not break rest of page") */}
      {(openPositionsLoading || openPositionsError || (openPositions?.open_positions?.length > 0)) && (
        <div className="rounded-xl border border-slate-700 bg-slate-900 p-4">
          <Panel0
            openPositions={openPositions}
            loading={openPositionsLoading}
            error={openPositionsError}
            showMarketBadge={market === 'ALL'}
          />
        </div>
      )}

      {/* Error state */}
      {error && (
        <div className="rounded-lg border border-red-800 bg-red-900/20 p-4">
          <p className="text-sm text-red-400" data-testid="benchmark-error">{error}</p>
        </div>
      )}

      {/* Loading skeleton */}
      {loading && (
        <div className="space-y-4 animate-pulse" data-testid="benchmark-loading">
          <div className="grid grid-cols-5 gap-3">
            {[1,2,3,4,5].map(i => <div key={i} className="h-20 bg-slate-800 rounded-lg" />)}
          </div>
          <div className="h-40 bg-slate-800 rounded-lg" />
          <div className="h-60 bg-slate-800 rounded-lg" />
        </div>
      )}

      {!loading && !error && (
        <div className="space-y-6">
          {/* Panel 1 */}
          <div className="rounded-xl border border-slate-700 bg-slate-900 p-4">
            <Panel1
              backtest={summary?.backtest_stats}
              actual={summary?.actual_stats}
              lastImportedAt={summary?.last_imported_at}
            />
          </div>

          {/* Panel 2 */}
          <div className="rounded-xl border border-slate-700 bg-slate-900 p-4">
            <Panel2 rows={summary?.yearly_breakdown || []} />
          </div>

          {/* Panel 3 */}
          <div className="rounded-xl border border-slate-700 bg-slate-900 p-4">
            <Panel3
              backtestTrades={trades?.backtest_trades || []}
              actualTrades={trades?.actual_trades || []}
              toggleMode={toggleMode}
              onToggleMode={setToggleMode}
            />
          </div>
        </div>
      )}
    </div>
  );
}
