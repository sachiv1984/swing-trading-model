/**
 * Shared number/currency formatting helper — unit tests (ST-06, EPIC-01, v9.6, BLG-FE-182)
 *
 * Design source: docs/design/2026-09-21__release-v9.6/number-format-convention/decision_record.md §2.1, §5
 * Spec: docs/specs/frontend/design_system.md v1.21 §Number and Currency Formatting
 *
 * Browser-free: src/lib/format.js is plain functions with no imports, so it is loaded here by
 * stripping the `export` keywords (the repo has no Jest suite; these run in the Playwright job).
 *
 *   SC-NF-01  Money, unsigned: symbol + en-GB grouping + 2 dp, GBP and USD
 *   SC-NF-02  Money, signed: explicit + on gains, typographic minus before the symbol, zero unsigned
 *   SC-NF-03  Negative sign is U+2212 placed BEFORE the currency symbol; never an ASCII hyphen
 *   SC-NF-04  Percentage: 1 dp default, 2 dp cost metrics, signed variants, rounds-to-zero is unsigned
 *   SC-NF-05  R-multiple: computed is signed 2 dp; a user target is as entered, trimmed, unsigned
 *   SC-NF-06  Missing values (null / undefined / NaN / '' / non-numeric) are an em dash
 *   SC-NF-07  Numeric strings are accepted; the helper never converts currency
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { test, expect } = require('@playwright/test');

const src = fs.readFileSync(path.join(__dirname, '..', '..', 'src', 'lib', 'format.js'), 'utf8')
  .replace(/^export /gm, '');
const { formatCurrency, formatPercent, formatR, currencyForMarket, MINUS, MISSING } =
  new Function(`${src}\nreturn { formatCurrency, formatPercent, formatR, currencyForMarket, MINUS, MISSING };`)();

const EM = '—';
const M = '−';

test('SC-NF-01: unsigned money — symbol, en-GB grouping, 2 dp, both currencies', () => {
  expect(formatCurrency(1234.5)).toBe('£1,234.50');
  expect(formatCurrency(48.2, { currency: 'USD' })).toBe('$48.20');
  expect(formatCurrency(0)).toBe('£0.00');
  expect(formatCurrency(999.999)).toBe('£1,000.00');           // rounds, then groups
  expect(formatCurrency(1234567.891)).toBe('£1,234,567.89');
  expect(formatCurrency(12345.6, { currency: 'USD' })).toBe('$12,345.60');
  expect(formatCurrency(150)).toBe('£150.00');                 // no sign on a positive unsigned amount
});

test('SC-NF-02: signed money — explicit +, typographic −, zero unsigned', () => {
  expect(formatCurrency(150, { signed: true })).toBe('+£150.00');
  expect(formatCurrency(-80, { signed: true })).toBe(`${M}£80.00`);
  expect(formatCurrency(0, { signed: true })).toBe('£0.00');
  expect(formatCurrency(-0, { signed: true })).toBe('£0.00');
  expect(formatCurrency(0.004, { signed: true })).toBe('£0.00');    // rounds to zero -> unsigned
  expect(formatCurrency(-0.004, { signed: true })).toBe('£0.00');
  expect(formatCurrency(1234.5, { signed: true, currency: 'USD' })).toBe('+$1,234.50');
});

test('SC-NF-03: negative sign is U+2212 before the currency symbol — never an ASCII hyphen', () => {
  for (const s of [formatCurrency(-80), formatCurrency(-80, { signed: true }), formatPercent(-1.8), formatR(-0.5)]) {
    expect(s).toContain(M);
    expect(s).not.toContain('-');
  }
  expect(formatCurrency(-1234.5)).toBe(`${M}£1,234.50`);           // unsigned amounts still carry the minus
  expect(formatCurrency(-1234.5, { currency: 'USD' })).toBe(`${M}$1,234.50`);
  expect(MINUS).toBe(M);
  expect(MISSING).toBe(EM);
});

test('SC-NF-04: percentages — 1 dp default, 2 dp for cost metrics, signed variants', () => {
  expect(formatPercent(12.5)).toBe('12.5%');
  expect(formatPercent(12.54)).toBe('12.5%');
  expect(formatPercent(4.2, { signed: true })).toBe('+4.2%');
  expect(formatPercent(-1.8, { signed: true })).toBe(`${M}1.8%`);
  expect(formatPercent(-1.8)).toBe(`${M}1.8%`);
  expect(formatPercent(0.35, { signed: true, dp: 2 })).toBe('+0.35%');
  expect(formatPercent(-0.35, { signed: true, dp: 2 })).toBe(`${M}0.35%`);
  expect(formatPercent(0, { signed: true })).toBe('0.0%');
  expect(formatPercent(0.04, { signed: true })).toBe('0.0%');       // rounds to zero at 1 dp -> unsigned
  expect(formatPercent(0.04, { signed: true, dp: 2 })).toBe('+0.04%');
});

test('SC-NF-05: R-multiples — computed is signed 2 dp; a user target is as entered, trimmed, unsigned', () => {
  expect(formatR(1.25)).toBe('+1.25R');
  expect(formatR(-0.5)).toBe(`${M}0.50R`);
  expect(formatR(0)).toBe('0.00R');
  expect(formatR(1.5)).toBe('+1.50R');                               // 1 dp source -> 2 dp
  expect(formatR(2.5, { target: true })).toBe('2.5R');
  expect(formatR(3, { target: true })).toBe('3R');
  expect(formatR(2.25, { target: true })).toBe('2.25R');
  expect(formatR(2.50, { target: true })).toBe('2.5R');              // trailing zero trimmed
  expect(formatR(2.5, { target: true })).not.toContain('+');
});

test('SC-NF-06: missing values render an em dash', () => {
  for (const v of [null, undefined, NaN, '', '   ', 'abc', Infinity]) {
    expect(formatCurrency(v)).toBe(EM);
    expect(formatCurrency(v, { signed: true })).toBe(EM);
    expect(formatPercent(v)).toBe(EM);
    expect(formatR(v)).toBe(EM);
    expect(formatR(v, { target: true })).toBe(EM);
  }
});

test('SC-NF-07: numeric strings are accepted; currency comes from the caller and is never converted', () => {
  expect(formatCurrency('1234.5')).toBe('£1,234.50');
  expect(formatPercent('4.2', { signed: true })).toBe('+4.2%');
  expect(formatR('1.25')).toBe('+1.25R');
  // same number, different currency argument -> same digits, different symbol (no FX)
  expect(formatCurrency(100, { currency: 'GBP' })).toBe('£100.00');
  expect(formatCurrency(100, { currency: 'USD' })).toBe('$100.00');
  expect(currencyForMarket('UK')).toBe('GBP');
  expect(currencyForMarket('US')).toBe('USD');
});
