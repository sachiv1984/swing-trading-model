/**
 * Shared OpenAPI-derived Playwright mock fixture library.
 *
 * ST-05 (EPIC-05, v7.6, BLG-QA-114). Preferred pattern for new Playwright
 * tests — read this file's factories instead of hand-rolling inline mock
 * JSON literals per spec file. Shapes are derived directly from
 * docs/reference/openapi.yaml component schemas, so a contract change is
 * one place to update rather than N specs. Per shared_standards.md §18
 * (Mock payload advisory): mocks must match the canonical response shape,
 * nested objects must not be flattened — every factory below returns the
 * full envelope, never a flattened `data` field.
 *
 * Scope: the endpoints touched by BLG-SPEC-95's v7.4 UI-heavy release
 * readiness bundle (command palette / custom price alerts / bulk actions /
 * saved filters). Command palette introduces no backend endpoint (v1 is
 * client-side only per that readiness pass), so it has no fixtures here.
 *
 *   GET/POST /saved-filters, DELETE /saved-filters/{id}   -> SavedFilter
 *   GET/POST /price-alerts, DELETE /price-alerts/{id}     -> PriceAlert
 *   POST .../bulk-tag, PUT .../bulk-archive, DELETE .../bulk -> BulkActionResult
 *
 * Usage:
 *   const { apiOk, savedFilter, savedFiltersListOk, priceAlert,
 *           priceAlertsListOk, bulkActionResultOk } = require('./fixtures/api-mocks');
 *
 *   await page.route(/\/saved-filters$/, (route) => {
 *     if (route.request().method() === 'GET') {
 *       route.fulfill({ status: 200, contentType: 'application/json',
 *         body: JSON.stringify(savedFiltersListOk([savedFilter({ name: 'My Filter' })])) });
 *     } else {
 *       route.continue();
 *     }
 *   });
 */

// ---------------------------------------------------------------------------
// Generic envelope helpers (conventions.md §2.1/§13.1)
// ---------------------------------------------------------------------------

function apiOk(data) {
  return { status: 'ok', data };
}

function apiError(message) {
  return { status: 'error', message };
}

// ---------------------------------------------------------------------------
// SavedFilter (openapi.yaml components/schemas/SavedFilter)
// ---------------------------------------------------------------------------

function savedFilter(overrides = {}) {
  return {
    id: 'sf-1',
    name: 'My Filter',
    filter_state: {},
    created_at: '2026-07-17T12:00:00Z',
    updated_at: '2026-07-17T12:00:00Z',
    ...overrides,
  };
}

function savedFiltersListOk(filters = []) {
  return apiOk(filters);
}

function savedFilterCreatedOk(overrides = {}) {
  return apiOk(savedFilter(overrides));
}

function savedFilterDeletedOk(id = 'sf-1') {
  return apiOk({ deleted: true, id });
}

// ---------------------------------------------------------------------------
// PriceAlert (openapi.yaml components/schemas/PriceAlert)
// ---------------------------------------------------------------------------

function priceAlert(overrides = {}) {
  return {
    id: 'pa-1',
    ticker: 'AAPL',
    condition: 'above',
    threshold_price: 150.0,
    active: true,
    triggered_at: null,
    created_at: '2026-07-17T12:00:00Z',
    updated_at: '2026-07-17T12:00:00Z',
    ...overrides,
  };
}

function priceAlertsListOk(alerts = []) {
  return apiOk(alerts);
}

function priceAlertCreatedOk(overrides = {}) {
  return apiOk(priceAlert(overrides));
}

function priceAlertDeletedOk(id = 'pa-1') {
  return apiOk({ deleted: true, id });
}

// ---------------------------------------------------------------------------
// BulkActionResult (openapi.yaml components/schemas/BulkActionResult)
// Shared by /watchlist/bulk-tag, /watchlist/bulk, /trade-plans/bulk-tag,
// /trade-plans/bulk-archive, /trade-plans/bulk.
// ---------------------------------------------------------------------------

function bulkActionResultOk(succeeded = [], failed = []) {
  return apiOk({ succeeded, failed });
}

function bulkActionFailure(id, reason) {
  return { id, reason };
}

module.exports = {
  apiOk,
  apiError,
  savedFilter,
  savedFiltersListOk,
  savedFilterCreatedOk,
  savedFilterDeletedOk,
  priceAlert,
  priceAlertsListOk,
  priceAlertCreatedOk,
  priceAlertDeletedOk,
  bulkActionResultOk,
  bulkActionFailure,
};
