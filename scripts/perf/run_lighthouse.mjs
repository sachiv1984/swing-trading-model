#!/usr/bin/env node
/**
 * Lighthouse lab run for the performance budget (ST-06, BLG-QA-271, EPIC-01, v9.18).
 *
 * Measures Dashboard, Positions, Trade Plan and Performance on the mobile profile
 * (Lighthouse default: Moto G Power emulation, simulated slow 4G and 4x CPU) and the
 * desktop profile, against a production build served locally with the mock API
 * (scripts/perf/mock_api_server.js). Each page/profile is run --runs times and the
 * median of each metric is reported.
 *
 * Reports, it does not gate (docs/specs/frontend/performance_budget.md §3.5): the
 * markdown table marks each value against the Core Web Vitals targets.
 * Lab runs cannot measure INP (it needs real interactions); Total Blocking Time is
 * the lab proxy reported in its place, against Lighthouse's own "good" TBT
 * thresholds (200 ms mobile, 150 ms desktop).
 *
 * Usage:
 *   node scripts/perf/run_lighthouse.mjs --base http://localhost:3000 \
 *     [--runs 3] [--out perf-results] [--summary $GITHUB_STEP_SUMMARY]
 * Needs the `lighthouse` package (CI installs lighthouse@13.6.0 with --no-save)
 * and Chrome (CHROME_PATH, or the one chrome-launcher finds).
 */

import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import lighthouse from 'lighthouse';
import desktopConfig from 'lighthouse/core/config/desktop-config.js';
import * as chromeLauncher from 'chrome-launcher';

const args = process.argv.slice(2);
const opt = (name, fallback) => {
  const i = args.indexOf(`--${name}`);
  return i > -1 ? args[i + 1] : fallback;
};
const BASE = opt('base', 'http://localhost:3000').replace(/\/$/, '');
const RUNS = Number(opt('runs', '3'));
const OUT = opt('out', 'perf-results');
const SUMMARY = opt('summary', null);

export const PAGES = [
  ['Dashboard', '/#/DashboardHome'],
  ['Positions', '/#/Positions'],
  ['Trade Plan', '/#/TradePlan'],
  ['Performance', '/#/Performance'],
];
const PROFILES = [
  ['mobile', undefined],
  ['desktop', desktopConfig],
];

// performance_budget.md §3.1 (Core Web Vitals "good" thresholds; TBT as the lab INP
// proxy, with Lighthouse's own "good" TBT per profile: 200 ms mobile, 150 ms desktop).
export const TARGETS = { lcp: 2500, cls: 0.1, tbt: { mobile: 200, desktop: 150 } };

const median = (xs) => {
  const s = [...xs].sort((a, b) => a - b);
  return s.length % 2 ? s[(s.length - 1) / 2] : (s[s.length / 2 - 1] + s[s.length / 2]) / 2;
};

const AUDITS = {
  fcp: 'first-contentful-paint',
  lcp: 'largest-contentful-paint',
  cls: 'cumulative-layout-shift',
  tbt: 'total-blocking-time',
  si: 'speed-index',
};

// A metric Lighthouse could not compute (e.g. NO_LCP on an error page) fails the run
// rather than becoming NaN in the table.
export function metrics(lhr) {
  const out = { score: Math.round((lhr.categories.performance.score ?? 0) * 100) };
  for (const [key, id] of Object.entries(AUDITS)) {
    const audit = lhr.audits[id];
    const v = audit?.numericValue;
    if (!Number.isFinite(v)) {
      throw new Error(`${lhr.finalDisplayedUrl}: ${id} has no value (${audit?.errorMessage || 'missing audit'})`);
    }
    out[key] = v;
  }
  return out;
}

export function formatRow(page, profile, m) {
  const mark = (ok) => (ok ? '✅' : '⚠️');
  return `| ${page} | ${profile} | ${m.score} | ${Math.round(m.fcp)} | ${Math.round(m.lcp)} ${mark(m.lcp <= TARGETS.lcp)} | ${m.cls.toFixed(3)} ${mark(m.cls <= TARGETS.cls)} | ${Math.round(m.tbt)} ${mark(m.tbt <= TARGETS.tbt[profile])} | ${Math.round(m.si)} |`;
}

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const chrome = await chromeLauncher.launch({
    chromePath: process.env.CHROME_PATH || undefined,
    chromeFlags: ['--headless=new', '--no-sandbox', '--disable-gpu'],
  });
  const results = [];
  try {
    for (const [profile, config] of PROFILES) {
      for (const [page, hash] of PAGES) {
        const runs = [];
        for (let i = 0; i < RUNS; i += 1) {
          const r = await lighthouse(`${BASE}${hash}`, {
            port: chrome.port,
            output: 'json',
            onlyCategories: ['performance'],
            logLevel: 'error',
          }, config);
          if (r.lhr.runtimeError) throw new Error(`${page} ${profile}: ${r.lhr.runtimeError.message}`);
          runs.push(metrics(r.lhr));
          if (i === 0) {
            fs.writeFileSync(path.join(OUT, `${page.replace(/\s/g, '_')}-${profile}.json`), r.report);
          }
        }
        const m = Object.fromEntries(Object.keys(runs[0]).map((k) => [k, median(runs.map((x) => x[k]))]));
        results.push({ page, profile, runs: RUNS, ...m });
        console.log(formatRow(page, profile, m));
      }
    }
  } finally {
    await chrome.kill();
  }

  fs.writeFileSync(path.join(OUT, 'lighthouse-summary.json'), JSON.stringify({ base: BASE, runs: RUNS, results }, null, 2));
  const lines = [
    `### Lighthouse (median of ${RUNS} run(s); lab, mocked API)`,
    '',
    `Targets: LCP ≤ ${TARGETS.lcp} ms, CLS ≤ ${TARGETS.cls}, TBT ≤ ${TARGETS.tbt.mobile} ms mobile / ${TARGETS.tbt.desktop} ms desktop (lab proxy for INP ≤ 200 ms). Report only; see docs/specs/frontend/performance_budget.md.`,
    '',
    '| Page | Profile | Score | FCP ms | LCP ms | CLS | TBT ms | Speed Index ms |',
    '|------|---------|-------|--------|--------|-----|--------|----------------|',
    ...results.map((r) => formatRow(r.page, r.profile, r)),
    '',
  ];
  fs.writeFileSync(path.join(OUT, 'lighthouse-summary.md'), lines.join('\n'));
  if (SUMMARY) fs.appendFileSync(SUMMARY, `${lines.join('\n')}\n`);
}

// Run main() only when executed directly. pathToFileURL + realpath matches
// import.meta.url for paths with spaces and through symlinks (e.g. macOS /var).
if (process.argv[1] && import.meta.url === pathToFileURL(fs.realpathSync(process.argv[1])).href) {
  main().catch((e) => {
    console.error(e);
    process.exit(1);
  });
}
