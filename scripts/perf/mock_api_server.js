#!/usr/bin/env node
/**
 * Mock API server for Lighthouse CI (ST-06, BLG-QA-271, EPIC-01, v9.18).
 *
 * Serves populated, deterministic JSON on http://localhost:<port> so the four
 * measured pages (Dashboard, Positions, Trade Plan, Performance) render real
 * content instead of empty states. The E2E build points REACT_APP_API_URL at
 * http://localhost:8000, so this listens there by default.
 *
 * The app's Content-Security-Policy (public/index.html) allows connect-src 'self'
 * and https: only, so a mock on another http port is blocked in a real browser.
 * With --static <build dir> this server also serves the build (SPA fallback to
 * index.html) on the same origin, and the API under --api-prefix (default /api):
 * build with REACT_APP_API_URL=http://localhost:<port>/api.
 *
 * Shapes follow the e2e fixtures (tests/e2e/fixtures/routed-pages-populated.js,
 * tests/e2e/accessibility-axe-scan.spec.js), which follow the backend writers.
 * Every other path gets the generic {status: "ok", data: []} envelope, as the
 * e2e catch-all does. Responses are immediate: Lighthouse measures the
 * front end's own rendering cost, not API latency (performance_budget.md §2).
 *
 * Usage: node scripts/perf/mock_api_server.js [--port 8000] [--static build] [--api-prefix /api]
 */

'use strict';

const fs = require('fs');
const http = require('http');
const path = require('path');
const zlib = require('zlib');
// Shared e2e fixtures, so the measured pages keep the shapes the e2e suite keeps current.
const { makePosition } = require('../../tests/e2e/fixtures/positions-table');
const { ANALYTICS_METRICS } = require('../../tests/e2e/fixtures/analytics-metrics');

const arg = (name, fallback) => {
  const i = process.argv.indexOf(`--${name}`);
  return i > -1 ? process.argv[i + 1] : fallback;
};
const PORT = Number(arg('port', '8000'));
const STATIC_DIR = arg('static', null);
const API_PREFIX = STATIC_DIR ? arg('api-prefix', '/api') : '';

const MIME = {
  '.html': 'text/html; charset=utf-8', '.js': 'application/javascript', '.css': 'text/css',
  '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.ico': 'image/x-icon',
  '.woff2': 'font/woff2', '.woff': 'font/woff', '.map': 'application/json', '.txt': 'text/plain',
};

// Text assets are gzipped when the client accepts it, as GitHub Pages serves them.
// Without this, Lighthouse's simulated slow 4G downloads the raw 2 MB bundle instead
// of ~548 KB and the mobile baseline is inflated by several seconds (EPIC-01 PR review).
const GZIP_TYPES = new Set(['.html', '.js', '.css', '.json', '.svg', '.map', '.txt']);

function serveStatic(req, pathname, res) {
  const root = path.resolve(STATIC_DIR);
  let file = path.resolve(root, `.${decodeURIComponent(pathname)}`);
  if (!file.startsWith(root) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
    file = path.join(root, 'index.html'); // SPA fallback
  }
  const ext = path.extname(file);
  const headers = { 'Content-Type': MIME[ext] || 'application/octet-stream', Vary: 'Accept-Encoding' };
  if (GZIP_TYPES.has(ext) && /\bgzip\b/.test(req.headers['accept-encoding'] || '')) {
    res.writeHead(200, { ...headers, 'Content-Encoding': 'gzip' });
    fs.createReadStream(file).pipe(zlib.createGzip({ level: 9 })).pipe(res);
    return;
  }
  res.writeHead(200, headers);
  fs.createReadStream(file).pipe(res);
}

const DAY = 24 * 3600 * 1000;
const NOW = Date.UTC(2026, 10, 18, 12, 0, 0);
const dateDaysAgo = (n) => new Date(NOW - n * DAY).toISOString().slice(0, 10);

const POSITIONS = [
  makePosition({
    id: 'pos-us', ticker: 'WDC', market: 'US', entry_price: 100.0, fill_price: 127.0, current_price: 92.31,
    current_price_native: 120.0, initial_stop: 80.0, current_trailing_stop: 76.92, current_trailing_stop_native: 100.0,
    stop_price: 76.92, stop_price_native: 100.0, fx_rate: 1.27, live_fx_rate: 1.3, pnl: 153.85, pnl_percent: 20.0,
    holding_days: 15, entry_date: dateDaysAgo(15),
  }),
  makePosition({
    id: 'pos-uk', ticker: 'VOD.L', market: 'UK', entry_price: 120.0, fill_price: 120.0, current_price: 100.0,
    current_price_native: 100.0, initial_stop: 95.0, current_trailing_stop: 95.0, current_trailing_stop_native: 95.0,
    stop_price: 95.0, stop_price_native: 95.0, fx_rate: 1, live_fx_rate: 1, pnl: -200.0, pnl_percent: -16.67,
    holding_days: 3, grace_days_remaining: 2, entry_date: dateDaysAgo(3), lifecycle_state: 'GRACE', position_state: 'GRACE',
  }),
];

const TRADES = Array.from({ length: 24 }, (_, i) => {
  const win = i % 3 !== 0;
  return {
    id: `t-${i}`, ticker: ['AAPL', 'MSFT', 'BARC.L'][i % 3], market: i % 3 === 2 ? 'UK' : 'US',
    entry_date: dateDaysAgo(40 + i * 3), exit_date: dateDaysAgo(20 + i * 3), shares: 10,
    entry_price: 100, exit_price: win ? 110 : 95, pnl: win ? 78.74 : -39.37,
    pnl_pct: win ? 10 : -5, pnl_percent: win ? 10 : -5,
    exit_reason: win ? 'Target Reached' : 'Stop Loss', tags: [], holding_days: 19, fees: 1.5,
  };
});

const ok = (data) => ({ status: 'ok', data });

function route(path) {
  if (/^\/positions\/?$/.test(path)) return POSITIONS; // bare array, as GET /positions returns
  if (path.startsWith('/positions/compliance')) return ok([]);
  if (path.startsWith('/market/status')) {
    return ok({ spy: { price: 521.0, ma200: 480.0, is_risk_on: true }, ftse: { is_risk_on: false }, fx_rate: 1.3 });
  }
  if (path.startsWith('/settings')) return ok([{ id: 'settings-1', default_risk_percent: 1.0, min_hold_days: 10 }]);
  if (/^\/portfolio\/?$/.test(path)) {
    return ok({ id: 'pf-1', cash: 15000, initial_cash: 20000, total_value: 17280.5, portfolio_heat_percent: 3.2, positions: POSITIONS });
  }
  if (/^\/trades\/?$/.test(path)) {
    return { status: 'ok', trades: TRADES, total_trades: TRADES.length, win_rate: 66.7, total_pnl: 944.88 };
  }
  if (path.startsWith('/analytics/metrics')) {
    return { ...ANALYTICS_METRICS, data: { ...ANALYTICS_METRICS.data, trades_for_charts: TRADES } };
  }
  if (/^\/signals\/?$/.test(path)) return [{ id: 'sig-1', ticker: 'MSFT', market: 'US', status: 'new', signal_date: dateDaysAgo(0) }];
  if (/^\/trade-plans\/?$/.test(path)) {
    return ok([{ id: 'tp-1', ticker: 'NVDA', market: 'US', status: 'entry_conditions_set', r_target: 2, setup_thesis: 'Breakout over 50-day high', created_at: new Date(NOW - 5 * DAY).toISOString(), updated_at: new Date(NOW - DAY).toISOString() }]);
  }
  return ok([]);
}

const server = http.createServer((req, res) => {
  // Echo the requested headers: the CORS "*" wildcard does not cover Authorization,
  // so a "*" preflight answer fails every authenticated fetch.
  const headers = {
    'Access-Control-Allow-Origin': req.headers.origin || '*',
    'Access-Control-Allow-Headers': req.headers['access-control-request-headers'] || '*',
    'Access-Control-Allow-Methods': 'GET,POST,PUT,PATCH,DELETE,OPTIONS',
    'Access-Control-Allow-Credentials': 'true',
  };
  if (req.method === 'OPTIONS') {
    res.writeHead(204, headers);
    res.end();
    return;
  }
  const pathname = new URL(req.url, `http://localhost:${PORT}`).pathname;
  if (STATIC_DIR && !pathname.startsWith(`${API_PREFIX}/`)) {
    serveStatic(req, pathname, res);
    return;
  }
  res.writeHead(200, { ...headers, 'Content-Type': 'application/json' });
  res.end(JSON.stringify(route(pathname.slice(API_PREFIX.length))));
});

server.listen(PORT, () => {
  console.log(`mock API listening on http://localhost:${PORT}${API_PREFIX}${STATIC_DIR ? ` (static: ${STATIC_DIR})` : ''}`);
});
