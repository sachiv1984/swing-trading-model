/**
 * Market Correlation Mock Data — EPIC-01 Playwright acceptance tests
 * SC-CORR-FE-01 through SC-CORR-FE-06
 *
 * Response shape: GET /analytics/market-correlation
 *   { status, data: { correlations: [...], portfolio_correlation: {...}, data_source } }
 *
 * Dataset design:
 *   - 3 positions with valid correlation (high / moderate / low) + 1 null-correlation row
 *   - Null row (HSBA) has severity:null — sorts to bottom per SEVERITY_ORDER
 *   - portfolio_correlation uses equal_weighted_average of the 3 non-null values
 *     (0.85 + 0.52 + 0.18) / 3 ≈ 0.52 → rounded to moderate
 */

'use strict';

const CORRELATION_RESPONSE = {
  status: 'ok',
  data: {
    correlations: [
      {
        ticker: 'LGEN',
        correlation: 0.85,
        severity: 'high',
        benchmark: 'FTSE 100',
        data_points: 90,
        cached: false,
      },
      {
        ticker: 'BARC',
        correlation: 0.52,
        severity: 'moderate',
        benchmark: 'FTSE 100',
        data_points: 85,
        cached: false,
      },
      {
        ticker: 'SHEL',
        correlation: 0.18,
        severity: 'low',
        benchmark: 'FTSE 100',
        data_points: 88,
        cached: false,
      },
      {
        ticker: 'HSBA',
        correlation: null,
        severity: null,
        benchmark: null,
        data_points: 0,
        cached: false,
      },
    ],
    portfolio_correlation: {
      value: 0.52,
      severity: 'moderate',
      method: 'equal_weighted_average',
    },
    data_source: 'Yahoo Finance',
  },
};

const CORRELATION_ERROR_RESPONSE = {
  status: 'error',
  message: 'Yahoo Finance unavailable',
};

const CORRELATION_EMPTY_RESPONSE = {
  status: 'ok',
  data: {
    correlations: [],
    portfolio_correlation: null,
    data_source: 'Yahoo Finance',
  },
};

module.exports = {
  CORRELATION_RESPONSE,
  CORRELATION_ERROR_RESPONSE,
  CORRELATION_EMPTY_RESPONSE,
};
