'use strict';

import { useState, useEffect, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { api } from '../api/base44Client';
import { BarChart2, RefreshCw, Upload, ChevronDown, ChevronUp, Play, Loader2 } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import PageHeader from '../components/ui/PageHeader';

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const MARKETS = ['ALL', 'US', 'UK'];

// SI-04 (ST-01, v7.7 EPIC-01): must stay in sync with backend/strategy_version_registry.py,
// which is itself sourced from claude/strategy/strategy_rules.md's Change Log table.
const STRATEGY_VERSIONS = ['1.0', '1.1', '1.2', '1.3', '1.4'];

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
  if (val == null) return 'text-slate-600 dark:text-slate-400';
  return Number(val) >= 0 ? 'text-green-400' : 'text-red-400';
}

// Panel 0 (Open Positions) uses emerald/rose per ux_spec.md, distinct from the
// green-400/red-400 used by the realized-trade panels above — reinforces that
// unrealized figures are visually separate from realized ones (AC-02).
function unrealizedPnlClass(val) {
  if (val == null) return 'text-slate-600 dark:text-slate-400';
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
  if (!config) return <span className="text-xs text-slate-600 dark:text-slate-400">{reason || '—'}</span>;
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
        <p className="text-sm text-slate-600 dark:text-slate-400" data-testid="benchmark-open-positions-error">
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
            <tr className="text-xs text-slate-600 dark:text-slate-400 border-b border-slate-700">
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
                <td className="py-2 pr-3 text-slate-600 dark:text-slate-400">{fmtDateLong(pos.entry_date)}</td>
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
      <p className="text-xs text-slate-600 dark:text-slate-400 mb-2">{label}</p>
      <div className="flex items-end justify-between gap-2">
        <div>
          <p className="text-xs text-slate-600 dark:text-slate-400 mb-0.5">Backtest</p>
          <p className="text-base font-semibold text-white">{backtest}</p>
        </div>
        <div className="text-right">
          <p className="text-xs text-slate-600 dark:text-slate-400 mb-0.5">Actual</p>
          <p className="text-base font-semibold text-slate-600 dark:text-slate-400">{actual}</p>
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
          <span className="text-xs text-slate-600 dark:text-slate-400">
            Last updated {new Date(lastImportedAt).toLocaleDateString('en-GB')}
          </span>
        )}
      </div>

      {!backtest ? (
        <p className="text-sm text-slate-600 dark:text-slate-400 italic" data-testid="benchmark-no-data">
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
        <p className="text-sm text-slate-600 dark:text-slate-400 italic">No yearly data available.</p>
      </section>
    );
  }

  return (
    <section data-testid="benchmark-panel-2">
      <h2 className="text-sm font-semibold text-white mb-3">Yearly Breakdown</h2>
      <div className="overflow-x-auto">
        <table className="w-full text-sm" data-testid="benchmark-yearly-table">
          <thead>
            <tr className="text-xs text-slate-600 dark:text-slate-400 border-b border-slate-700">
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
          <span className={`ml-1.5 text-xs px-1 py-0.5 rounded ${source === 'backtest' ? 'bg-slate-700 text-slate-600 dark:text-slate-400' : 'bg-blue-900 text-blue-300'}`}>
            {source === 'backtest' ? 'BT' : 'Live'}
          </span>
        )}
      </td>
      <td className="py-2 pr-3 text-slate-600 dark:text-slate-400">{trade.entry_date || '—'}</td>
      <td className="py-2 pr-3 text-slate-600 dark:text-slate-400">{trade.exit_date || '—'}</td>
      <td className="py-2 pr-3 text-slate-600 dark:text-slate-400">{trade.holding_days != null ? `${trade.holding_days}d` : '—'}</td>
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
                  : 'border-slate-700 text-slate-600 dark:text-slate-400 hover:text-slate-300 hover:bg-slate-800'
              }`}
              data-testid={`benchmark-mode-${mode}`}
            >
              {TOGGLE_LABELS[mode]}
            </button>
          ))}
        </div>
      </div>

      {rows.length === 0 ? (
        <p className="text-sm text-slate-600 dark:text-slate-400 italic" data-testid="benchmark-trades-empty">
          No trades for the selected filter.
        </p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm" data-testid="benchmark-trade-table">
            <thead>
              <tr className="text-xs text-slate-600 dark:text-slate-400 border-b border-slate-700">
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
// Version Comparison Tab (v0.4 — ST-01, EPIC-01, BLG-FEAT-75, v7.7)
// ---------------------------------------------------------------------------

function fmtR(val) {
  if (val == null) return '—';
  const n = Number(val);
  return (n >= 0 ? '+' : '') + n.toFixed(2) + 'R';
}

function fmtDelta(val, suffix = '') {
  if (val == null) return '—';
  const n = Number(val);
  return (n >= 0 ? '+' : '') + n.toFixed(2) + suffix;
}

function deltaClass(val) {
  if (val == null) return 'text-slate-600 dark:text-slate-400';
  return Number(val) >= 0 ? 'text-emerald-400' : 'text-rose-400';
}

const ASSESSMENT_BADGE = {
  Improved: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
  Degraded: 'bg-rose-500/20 text-rose-400 border-rose-500/30',
  'Insufficient data': 'bg-slate-500/20 text-slate-400 border-slate-500/30',
};

function VersionComparisonTab() {
  const [versionFrom, setVersionFrom] = useState(STRATEGY_VERSIONS[0]);
  const [versionTo, setVersionTo] = useState(STRATEGY_VERSIONS[STRATEGY_VERSIONS.length - 1]);
  const [state, setState] = useState('idle'); // idle | loading | loaded | error
  const [result, setResult] = useState(null);
  const [fieldError, setFieldError] = useState(null); // { field: 'from'|'to', message }
  const [generalError, setGeneralError] = useState(null);

  const handleCompare = useCallback(async () => {
    setState('loading');
    setFieldError(null);
    setGeneralError(null);
    setResult(null);
    try {
      const data = await api.strategyVersionComparison.compare({ versionFrom, versionTo });
      setResult(data);
      setState('loaded');
    } catch (err) {
      // ST-08 (EPIC-02, v8.3, BLG-BE-69): backend error body is now the canonical
      // flat {status, code, message, ...} envelope at the top level of err.data —
      // no longer nested under a "detail" key (FastAPI's old default envelope).
      const detail = err?.data;
      const code = detail?.code;
      if (code === 'insufficient_data') {
        setGeneralError(
          `Not enough trades to compare — ${detail.version} has ${detail.trade_count} trades (minimum ${detail.min_trades_required} required).`
        );
      } else if (code === 'version_not_found') {
        setFieldError({
          field: detail.missing_version === versionFrom ? 'from' : 'to',
          message: 'Version not found.',
        });
      } else if (code === 'version_order_error') {
        setFieldError({ field: 'to', message: "Must be chronologically after the 'From' version." });
      } else {
        setGeneralError('Unable to load comparison. Please try again.');
      }
      setState('error');
    }
  }, [versionFrom, versionTo]);

  return (
    <section data-testid="version-comparison-tab">
      {/* Controls row */}
      <div className="flex flex-wrap items-end gap-3 mb-4">
        <div className="flex items-center gap-2">
          <label className="text-xs text-slate-600 dark:text-slate-400 shrink-0">From</label>
          <select
            value={versionFrom}
            onChange={e => setVersionFrom(e.target.value)}
            className="appearance-none bg-slate-800 border border-slate-600 rounded-md px-3 py-1.5 text-xs text-slate-300 focus:outline-none focus:border-slate-400"
            data-testid="version-from-select"
          >
            {STRATEGY_VERSIONS.map(v => (
              <option key={v} value={v}>{v}</option>
            ))}
          </select>
          {fieldError?.field === 'from' && (
            <span className="text-xs text-rose-700 dark:text-rose-400" data-testid="version-from-error">{fieldError.message}</span>
          )}
        </div>

        <div className="flex items-center gap-2">
          <label className="text-xs text-slate-600 dark:text-slate-400 shrink-0">To</label>
          <select
            value={versionTo}
            onChange={e => setVersionTo(e.target.value)}
            className="appearance-none bg-slate-800 border border-slate-600 rounded-md px-3 py-1.5 text-xs text-slate-300 focus:outline-none focus:border-slate-400"
            data-testid="version-to-select"
          >
            {STRATEGY_VERSIONS.map(v => (
              <option key={v} value={v}>{v}</option>
            ))}
          </select>
          {fieldError?.field === 'to' && (
            <span className="text-xs text-rose-700 dark:text-rose-400" data-testid="version-to-error">{fieldError.message}</span>
          )}
        </div>

        <button
          onClick={handleCompare}
          disabled={state === 'loading'}
          className="text-xs px-3 py-1.5 rounded-md border border-slate-400 bg-slate-700 text-white hover:bg-slate-600 disabled:opacity-50"
          data-testid="version-compare-btn"
        >
          Compare
        </button>
      </div>

      {/* States */}
      {state === 'idle' && (
        <p className="text-sm text-slate-600 dark:text-slate-400 italic" data-testid="version-comparison-idle">
          Select two strategy versions to compare.
        </p>
      )}

      {state === 'loading' && (
        <div className="space-y-2 animate-pulse" data-testid="version-comparison-loading">
          {[1, 2, 3, 4].map(i => <div key={i} className="h-8 bg-slate-800 rounded-md" />)}
        </div>
      )}

      {state === 'error' && generalError && (
        <div className="rounded-lg border border-red-800 bg-red-900/20 p-4" data-testid="version-comparison-error">
          <p className="text-sm text-red-400">{generalError}</p>
        </div>
      )}

      {state === 'loaded' && result && (
        <div data-testid="version-comparison-result">
          <div className="overflow-x-auto">
            <table className="w-full text-sm" data-testid="version-comparison-table">
              <thead>
                <tr className="text-xs text-slate-600 dark:text-slate-400 border-b border-slate-700">
                  <th scope="col" className="text-left py-2 pr-3">Metric</th>
                  <th scope="col" className="text-right py-2 pr-3">{result.version_from}</th>
                  <th scope="col" className="text-right py-2">{result.version_to}</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-slate-800">
                  <td className="py-2 pr-3 text-slate-300">Trades Compared</td>
                  <td className="py-2 pr-3 text-right text-white">{fmtNum(result.version_from_metrics.trade_count)}</td>
                  <td className="py-2 text-right text-white">{fmtNum(result.version_to_metrics.trade_count)}</td>
                </tr>
                <tr className="border-b border-slate-800">
                  <td className="py-2 pr-3 text-slate-300">Win Rate</td>
                  <td className="py-2 pr-3 text-right text-white">{fmtPct(result.version_from_metrics.win_rate * 100)}</td>
                  <td className="py-2 text-right text-white">{fmtPct(result.version_to_metrics.win_rate * 100)}</td>
                </tr>
                <tr className="border-b border-slate-800">
                  <td className="py-2 pr-3 text-slate-300">Average R</td>
                  <td className="py-2 pr-3 text-right text-white">{fmtR(result.version_from_metrics.avg_R)}</td>
                  <td className="py-2 text-right text-white">{fmtR(result.version_to_metrics.avg_R)}</td>
                </tr>
                <tr>
                  <td className="py-2 pr-3 text-slate-300">
                    Compliance Rate
                    {(result.version_from_metrics.compliance_rate == null || result.version_to_metrics.compliance_rate == null) && (
                      <span className="ml-1 text-slate-600 dark:text-slate-400" title="Not yet available">ⓘ</span>
                    )}
                  </td>
                  <td className="py-2 pr-3 text-right text-white">
                    {result.version_from_metrics.compliance_rate != null
                      ? fmtPct(result.version_from_metrics.compliance_rate * 100)
                      : <span title="Not yet available">—</span>}
                  </td>
                  <td className="py-2 text-right text-white">
                    {result.version_to_metrics.compliance_rate != null
                      ? fmtPct(result.version_to_metrics.compliance_rate * 100)
                      : <span title="Not yet available">—</span>}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* Comparison Summary strip */}
          <div className="mt-4 flex flex-wrap items-center gap-4 rounded-lg border border-slate-700 bg-slate-800/50 p-3" data-testid="version-comparison-summary">
            <span className={`text-sm font-medium ${deltaClass(result.comparison_summary.win_rate_delta)}`}>
              Win Rate {fmtDelta(result.comparison_summary.win_rate_delta * 100, '%')}
            </span>
            <span className={`text-sm font-medium ${deltaClass(result.comparison_summary.avg_R_delta)}`}>
              Avg R {fmtDelta(result.comparison_summary.avg_R_delta, 'R')}
            </span>
            <span className="text-sm font-medium text-slate-300">
              Trades {fmtDelta(result.comparison_summary.trade_count_delta)}
            </span>
            <span
              className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${ASSESSMENT_BADGE[result.comparison_summary.assessment] || ASSESSMENT_BADGE['Insufficient data']}`}
              data-testid="version-comparison-assessment"
            >
              {result.comparison_summary.assessment}
            </span>
          </div>
        </div>
      )}
    </section>
  );
}

// ---------------------------------------------------------------------------
// Backtest Rule Change tab (ST-07, v8.9 EPIC-02, BLG-FEAT-89)
// Design source: docs/design/2026-08-17__release-v8.9/in-app-backtesting-engine/ux_spec.md
// ---------------------------------------------------------------------------

// Structured candidate parameter form (design_record.md §2.1 leaves raw-diff
// vs. structured-form open; resolved to structured here — a safe, bounded
// set of fields mirroring strategy_rules.md's actual tunable parameters,
// rather than free-form text with no deterministic parse path).
const CANDIDATE_FIELDS = [
  { key: 'lookback', label: 'Lookback (days)', type: 'number', step: '1' },
  { key: 'top_n', label: 'Top N', type: 'number', step: '1' },
  { key: 'atr_mult', label: 'ATR Multiplier', type: 'number', step: '0.1' },
  { key: 'min_hold_days', label: 'Min Hold Days', type: 'number', step: '1' },
  { key: 'initial_atr_mult', label: 'Initial ATR Multiplier', type: 'number', step: '0.1' },
  { key: 'profit_atr_mult', label: 'Profit-Lock ATR Multiplier', type: 'number', step: '0.1' },
  { key: 'min_position_pct', label: 'Min Position %', type: 'number', step: '0.01' },
  { key: 'max_position_pct', label: 'Max Position %', type: 'number', step: '0.01' },
];

function BacktestComparisonRow({ label, candidate, live, format }) {
  return (
    <tr className="border-b border-slate-800">
      <td className="py-2 pr-3 text-slate-300">{label}</td>
      <td className="py-2 pr-3 text-right text-white">{format(candidate)}</td>
      <td className="py-2 text-right text-white">{format(live)}</td>
    </tr>
  );
}

function RMultipleComparisonChart({ candidateBuckets, liveBuckets }) {
  const merged = (candidateBuckets || []).map((b, i) => ({
    range: b.label,
    Candidate: b.count,
    Live: liveBuckets?.[i]?.count ?? 0,
  }));
  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={merged} margin={{ top: 8, right: 8, left: 0, bottom: 40 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.3} />
        <XAxis dataKey="range" stroke="#64748b" tick={{ fill: '#94a3b8', fontSize: 11 }} angle={-40} textAnchor="end" height={60} />
        <YAxis stroke="#64748b" tick={{ fill: '#94a3b8', fontSize: 12 }} allowDecimals={false}
          label={{ value: 'Trades', angle: -90, position: 'insideLeft', fill: '#64748b', fontSize: 11 }} />
        <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
          labelStyle={{ color: '#e2e8f0' }} itemStyle={{ fontSize: 12 }} />
        <Legend wrapperStyle={{ fontSize: 12 }} />
        <Bar dataKey="Candidate" fill="#22d3ee" radius={[4, 4, 0, 0]} data-testid="backtest-rmultiple-candidate-bar" />
        <Bar dataKey="Live" fill="#64748b" radius={[4, 4, 0, 0]} data-testid="backtest-rmultiple-live-bar" />
      </BarChart>
    </ResponsiveContainer>
  );
}

function BacktestRunHistoryItem({ run }) {
  const [expanded, setExpanded] = useState(false);
  return (
    <div className="rounded-lg border border-slate-700/50 bg-slate-800/30" data-testid="backtest-run-history-item">
      <button
        type="button"
        onClick={() => setExpanded((e) => !e)}
        className="w-full flex items-center justify-between px-3 py-2 text-left"
        data-testid="backtest-run-history-toggle"
      >
        <div className="text-xs text-slate-300">
          <span className="text-slate-600 dark:text-slate-400">{new Date(run.created_at).toLocaleString()}</span>
          {' — '}
          <span>{run.rule_diff_summary}</span>
        </div>
        {expanded ? <ChevronUp className="w-3.5 h-3.5 text-slate-500" /> : <ChevronDown className="w-3.5 h-3.5 text-slate-500" />}
      </button>
      {expanded && (
        <div className="px-3 pb-3 text-xs text-slate-400 space-y-1">
          <div>By: {run.initiated_by || '—'}</div>
          <div>Universe: {run.universe_size} tickers, {run.universe_start_date} to {run.universe_end_date}</div>
          <div>Win Rate — Candidate {fmtPct(run.candidate_result?.win_rate_pct)} vs Live {fmtPct(run.live_result?.win_rate_pct)}</div>
          <div>Max DD — Candidate {fmtPct(run.candidate_result?.max_drawdown_pct)} vs Live {fmtPct(run.live_result?.max_drawdown_pct)}</div>
          <div>Median R — Candidate {fmtR(run.candidate_result?.median_r)} vs Live {fmtR(run.live_result?.median_r)}</div>
        </div>
      )}
    </div>
  );
}

function BacktestRuleChangeTab() {
  const [inputs, setInputs] = useState({});
  const [runState, setRunState] = useState('idle'); // idle | loading | loaded | error
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState(null);
  const [historyExpanded, setHistoryExpanded] = useState(false);

  const loadHistory = useCallback(async () => {
    try {
      const data = await api.backtestRuleChange.getRuns({ limit: 20 });
      setHistory(data);
    } catch {
      setHistory([]);
    }
  }, []);

  useEffect(() => {
    if (historyExpanded && history === null) {
      loadHistory();
    }
  }, [historyExpanded, history, loadHistory]);

  const handleFieldChange = (key, value) => {
    setInputs((prev) => ({ ...prev, [key]: value }));
  };

  const handleRun = useCallback(async () => {
    setRunState('loading');
    setError(null);
    try {
      const overrides = {};
      for (const { key } of CANDIDATE_FIELDS) {
        const raw = inputs[key];
        if (raw !== undefined && raw !== '') overrides[key] = parseFloat(raw);
      }
      const data = await api.backtestRuleChange.run(overrides);
      setResult(data);
      setRunState('loaded');
      // Refresh history so the just-completed run appears without a manual reload.
      if (historyExpanded) loadHistory();
    } catch (err) {
      setError('Backtest failed to complete. Please try again.');
      setRunState('error');
    }
  }, [inputs, historyExpanded, loadHistory]);

  return (
    <section data-testid="backtest-rule-change-tab">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Left panel — Candidate Rule Input */}
        <div className="rounded-xl border border-slate-700 bg-slate-900 p-4">
          <h3 className="text-sm font-medium text-slate-300 mb-3">Candidate Rule Change</h3>
          <p className="text-xs text-slate-600 dark:text-slate-400 mb-3">
            Leave a field blank to use the live strategy_rules.md value.
          </p>
          <div className="grid grid-cols-2 gap-3">
            {CANDIDATE_FIELDS.map(({ key, label, type, step }) => (
              <div key={key} className="space-y-1">
                <label className="text-xs text-slate-600 dark:text-slate-400">{label}</label>
                <input
                  type={type}
                  step={step}
                  value={inputs[key] ?? ''}
                  onChange={(e) => handleFieldChange(key, e.target.value)}
                  data-testid={`backtest-input-${key}`}
                  className="w-full bg-slate-800 border border-slate-700 rounded-md px-2 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-slate-400"
                />
              </div>
            ))}
          </div>
          <button
            onClick={handleRun}
            disabled={runState === 'loading'}
            data-testid="backtest-run-btn"
            className="mt-4 flex items-center gap-2 text-xs px-3 py-2 rounded-md border border-slate-400 bg-slate-700 text-white hover:bg-slate-600 disabled:opacity-50"
          >
            {runState === 'loading' ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                Running backtest…
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5" />
                Run Backtest
              </>
            )}
          </button>
          {runState === 'error' && (
            <p className="mt-2 text-xs text-rose-400" data-testid="backtest-run-error">{error}</p>
          )}
        </div>

        {/* Right panel — Results */}
        <div className="rounded-xl border border-slate-700 bg-slate-900 p-4">
          <h3 className="text-sm font-medium text-slate-300 mb-3">Results</h3>
          {runState === 'idle' && (
            <p className="text-sm text-slate-600 dark:text-slate-400 italic" data-testid="backtest-results-empty">
              Set parameter overrides and run a backtest to compare it against your live strategy.
            </p>
          )}
          {runState === 'loading' && (
            <div className="space-y-2 animate-pulse" data-testid="backtest-results-loading">
              {[1, 2, 3].map((i) => <div key={i} className="h-8 bg-slate-800 rounded-md" />)}
            </div>
          )}
          {runState === 'loaded' && result && (
            <div data-testid="backtest-results-loaded">
              <div className="overflow-x-auto mb-4">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-xs text-slate-600 dark:text-slate-400 border-b border-slate-700">
                      <th scope="col" className="text-left py-2 pr-3">Metric</th>
                      <th scope="col" className="text-right py-2 pr-3">Candidate</th>
                      <th scope="col" className="text-right py-2">Live</th>
                    </tr>
                  </thead>
                  <tbody>
                    <BacktestComparisonRow label="Trades" candidate={result.candidate_result.trade_count} live={result.live_result.trade_count} format={fmtNum} />
                    <BacktestComparisonRow label="Win Rate" candidate={result.candidate_result.win_rate_pct} live={result.live_result.win_rate_pct} format={fmtPct} />
                    <BacktestComparisonRow label="Median R" candidate={result.candidate_result.median_r} live={result.live_result.median_r} format={fmtR} />
                    <BacktestComparisonRow label="Max Drawdown" candidate={result.candidate_result.max_drawdown_pct} live={result.live_result.max_drawdown_pct} format={fmtPct} />
                  </tbody>
                </table>
              </div>

              <RMultipleComparisonChart
                candidateBuckets={result.candidate_result.r_multiple_buckets}
                liveBuckets={result.live_result.r_multiple_buckets}
              />

              <div className="mt-4 text-xs text-slate-600 dark:text-slate-400 space-y-1" data-testid="backtest-run-metadata">
                <div>{new Date(result.created_at).toLocaleString()} — by {result.initiated_by || '—'}</div>
                <div>{result.rule_diff_summary}</div>
                <div>Universe: {result.universe_tickers.length} tickers, {result.universe_start_date} to {result.universe_end_date}</div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Run History (AC-03) */}
      <div className="mt-4 rounded-xl border border-slate-700 bg-slate-900 p-4">
        <button
          type="button"
          onClick={() => setHistoryExpanded((e) => !e)}
          className="w-full flex items-center justify-between"
          data-testid="backtest-run-history-toggle-panel"
        >
          <h3 className="text-sm font-medium text-slate-300">Run History</h3>
          {historyExpanded ? <ChevronUp className="w-4 h-4 text-slate-500" /> : <ChevronDown className="w-4 h-4 text-slate-500" />}
        </button>
        {historyExpanded && (
          <div className="mt-3 space-y-2" data-testid="backtest-run-history-list">
            {history === null && <p className="text-xs text-slate-600 dark:text-slate-400">Loading…</p>}
            {history?.length === 0 && <p className="text-xs text-slate-600 dark:text-slate-400">No runs yet.</p>}
            {history?.map((run) => <BacktestRunHistoryItem key={run.id} run={run} />)}
          </div>
        )}
      </div>
    </section>
  );
}

// ---------------------------------------------------------------------------
// Main page
// ---------------------------------------------------------------------------

export default function StrategyBenchmark() {
  const [searchParams, setSearchParams] = useSearchParams();
  const tabParam = searchParams.get('tab');
  const activeTab =
    tabParam === 'version-comparison' ? 'version-comparison' :
    tabParam === 'backtest-rule-change' ? 'backtest-rule-change' :
    'benchmark';
  const setActiveTab = (tab) => {
    const next = new URLSearchParams(searchParams);
    if (tab === 'version-comparison' || tab === 'backtest-rule-change') next.set('tab', tab);
    else next.delete('tab');
    setSearchParams(next, { replace: true });
  };

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

      {/* Page header — ST-19 (EPIC-05, v7.10, BLG-FE-106): consolidated onto the
          shared PageHeader component (strategy_benchmark.md §2). BarChart2 icon
          and the "Benchmark data as of" last-updated line are preserved as
          adjacent elements — PageHeader has no icon/subtitle-line prop. */}
      <div className="flex items-start gap-3">
        <BarChart2 className="w-5 h-5 text-slate-400 mt-1.5 shrink-0" data-testid="benchmark-header-icon" />
        <div className="flex-1">
          <PageHeader
            title="Strategy Benchmark"
            description="Compare live trading vs backtest"
            actions={
              <button
                onClick={fetchData}
                disabled={loading}
                className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-md border border-slate-600 text-slate-300 hover:bg-slate-800 disabled:opacity-50"
                data-testid="benchmark-refresh-btn"
              >
                <RefreshCw className={`w-3 h-3 ${loading ? 'animate-spin' : ''}`} />
                Refresh
              </button>
            }
          />
          {summary?.last_imported_at && (
            <p className="text-xs text-slate-600 dark:text-slate-400 -mt-6" data-testid="benchmark-last-imported">
              Benchmark data as of {fmtDateLong(summary.last_imported_at)}
            </p>
          )}
        </div>
      </div>

      {/* Sub-navigation (v0.4 — ST-01, EPIC-01, v7.7) */}
      <div className="flex gap-1 border-b border-slate-700" role="tablist" data-testid="benchmark-subnav">
        <button
          role="tab"
          aria-selected={activeTab === 'benchmark'}
          onClick={() => setActiveTab('benchmark')}
          className={`text-sm px-3 py-2 border-b-2 transition-colors ${
            activeTab === 'benchmark'
              ? 'border-slate-400 text-slate-900 dark:text-white font-medium'
              : 'border-transparent text-slate-600 dark:text-slate-400 hover:text-slate-300'
          }`}
          data-testid="benchmark-tab-benchmark"
        >
          Benchmark
        </button>
        <button
          role="tab"
          aria-selected={activeTab === 'version-comparison'}
          onClick={() => setActiveTab('version-comparison')}
          className={`text-sm px-3 py-2 border-b-2 transition-colors ${
            activeTab === 'version-comparison'
              ? 'border-slate-400 text-slate-900 dark:text-white font-medium'
              : 'border-transparent text-slate-600 dark:text-slate-400 hover:text-slate-300'
          }`}
          data-testid="benchmark-tab-version-comparison"
        >
          Version Comparison
        </button>
        <button
          role="tab"
          aria-selected={activeTab === 'backtest-rule-change'}
          onClick={() => setActiveTab('backtest-rule-change')}
          className={`text-sm px-3 py-2 border-b-2 transition-colors ${
            activeTab === 'backtest-rule-change'
              ? 'border-slate-400 text-slate-900 dark:text-white font-medium'
              : 'border-transparent text-slate-600 dark:text-slate-400 hover:text-slate-300'
          }`}
          data-testid="benchmark-tab-backtest-rule-change"
        >
          Backtest Rule Change
        </button>
      </div>

      {activeTab === 'version-comparison' ? (
        <div className="rounded-xl border border-slate-700 bg-slate-900 p-4">
          <VersionComparisonTab />
        </div>
      ) : activeTab === 'backtest-rule-change' ? (
        <BacktestRuleChangeTab />
      ) : (
      <>
      {/* Sticky filters */}
      <div
        className="sticky top-0 z-10 bg-slate-900/95 backdrop-blur-sm border border-slate-700 rounded-lg p-3 flex flex-wrap gap-3 items-center"
        data-testid="benchmark-filters"
      >
        {/* Year filter */}
        <div className="flex items-center gap-2">
          <label className="text-xs text-slate-600 dark:text-slate-400 shrink-0">Year</label>
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
          <label className="text-xs text-slate-600 dark:text-slate-400 shrink-0">Market</label>
          <div className="flex gap-1">
            {MARKETS.map(m => (
              <button
                key={m}
                onClick={() => setMarket(m)}
                className={`text-xs px-2.5 py-1 rounded-md border transition-colors ${
                  market === m
                    ? 'border-slate-400 bg-slate-700 text-white'
                    : 'border-slate-700 text-slate-600 dark:text-slate-400 hover:text-slate-300 hover:bg-slate-800'
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
      </>
      )}
    </div>
  );
}
