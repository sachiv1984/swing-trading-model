/**
 * Notifications Mock Data — Acceptance Tests
 * ST-09 (v2.2): SC-NOTIF-02 through SC-NOTIF-08
 *
 * Response shapes match backend/routers/alerts.py:
 *   GET  /notifications       → {status, data: {notifications, has_more}}
 *   GET  /notifications/preferences → {status, data: {preferences}}
 *   PATCH /notifications/{id} → {status, data: {...}}
 *   POST  /notifications/mark-all-read → {status, data: {}}
 *
 * Usage: import in Playwright tests, pass to page.route() mock handler.
 */

'use strict';

// ---------------------------------------------------------------------------
// Single unread notification (stop_loss_approach)
// alert_type matches the DB field name used by NotificationRow component
// ---------------------------------------------------------------------------
const NOTIF_STOP_LOSS_UNREAD = {
  id: 'notif-1',
  alert_type: 'stop_loss_approach',
  title: 'Stop Loss Approach Alert',
  message: 'AAPL is approaching its stop loss at $210.00.',
  read: false,
  created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(), // 2 hours ago
  portfolio_id: 'portfolio-test-001',
};

// ---------------------------------------------------------------------------
// One read notification (daily_portfolio_summary)
// ---------------------------------------------------------------------------
const NOTIF_DAILY_READ = {
  id: 'notif-2',
  alert_type: 'daily_portfolio_summary',
  title: 'Daily Portfolio Summary',
  message: 'Your portfolio has 3 open positions.',
  read: true,
  created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(), // yesterday
  portfolio_id: 'portfolio-test-001',
};

// ---------------------------------------------------------------------------
// TD-NOTIF-A: One unread notification  (SC-NOTIF-02, SC-NOTIF-03)
// ---------------------------------------------------------------------------
const TD_NOTIF_A = {
  status: 'ok',
  data: {
    notifications: [NOTIF_STOP_LOSS_UNREAD],
    has_more: false,
  },
};

// ---------------------------------------------------------------------------
// TD-NOTIF-B: Mixed — one unread + one read  (SC-NOTIF-02)
// ---------------------------------------------------------------------------
const TD_NOTIF_B = {
  status: 'ok',
  data: {
    notifications: [NOTIF_STOP_LOSS_UNREAD, NOTIF_DAILY_READ],
    has_more: false,
  },
};

// ---------------------------------------------------------------------------
// TD-NOTIF-C: Two unread notifications  (SC-NOTIF-04)
// ---------------------------------------------------------------------------
const TD_NOTIF_C = {
  status: 'ok',
  data: {
    notifications: [
      NOTIF_STOP_LOSS_UNREAD,
      {
        id: 'notif-3',
        alert_type: 'grace_period_warning',
        title: 'Grace Period Warning',
        message: 'TSLA has 2 days remaining in its grace period.',
        read: false,
        created_at: new Date(Date.now() - 60 * 60 * 1000).toISOString(),
        portfolio_id: 'portfolio-test-001',
      },
    ],
    has_more: false,
  },
};

// ---------------------------------------------------------------------------
// custom_price_alert notification with context (ST-09, BLG-BE-84, EPIC-02,
// v8.8) — carries context.ticker / context.price_alert_id, used by
// NotificationRow's "Create Trade Plan" CTA.
// ---------------------------------------------------------------------------
const NOTIF_PRICE_ALERT_WITH_CONTEXT = {
  id: 'notif-4',
  alert_type: 'custom_price_alert',
  title: 'Price Alert — TSLA above 250.00',
  message: 'TSLA crossed above your threshold of 250.00 (current: 251.30).',
  read: false,
  created_at: new Date(Date.now() - 10 * 60 * 1000).toISOString(),
  portfolio_id: 'portfolio-test-001',
  context: {
    ticker: 'TSLA',
    condition: 'above',
    threshold_price: 250.0,
    current_price: 251.3,
    price_alert_id: 'pa-42',
  },
};

const TD_NOTIF_PRICE_ALERT = {
  status: 'ok',
  data: {
    notifications: [NOTIF_PRICE_ALERT_WITH_CONTEXT],
    has_more: false,
  },
};

// ---------------------------------------------------------------------------
// TD-NOTIF-EMPTY: No notifications  (SC-NOTIF-05)
// ---------------------------------------------------------------------------
const TD_NOTIF_EMPTY = {
  status: 'ok',
  data: {
    notifications: [],
    has_more: false,
  },
};

// ---------------------------------------------------------------------------
// TD-PREFS-ALL-ON: All 4 alert types enabled  (SC-NOTIF-06, SC-NOTIF-07, SC-NOTIF-08)
// ---------------------------------------------------------------------------
const TD_PREFS_ALL_ON = {
  status: 'ok',
  data: {
    preferences: [
      { alert_type: 'stop_loss_approach',      email_enabled: true },
      { alert_type: 'grace_period_warning',    email_enabled: true },
      { alert_type: 'market_regime_change',    email_enabled: true },
      { alert_type: 'daily_portfolio_summary', email_enabled: true },
    ],
  },
};

// ---------------------------------------------------------------------------
// Standard success responses for write operations
// ---------------------------------------------------------------------------
const MARK_READ_OK    = { status: 'ok', data: {} };
const MARK_ALL_OK     = { status: 'ok', data: {} };
const PREF_UPDATE_OK  = { status: 'ok', data: {} };

// ---------------------------------------------------------------------------
// Alert rules mock (for AlertThresholdsSection on preferences page)
// ---------------------------------------------------------------------------
// data is the array directly — matches GET /alerts/rules response schema (alerts_endpoints.md §data schema)
const TD_ALERT_RULES = {
  status: 'ok',
  data: [
    { id: 'rule-1', type: 'stop_loss_approach',      enabled: true, threshold_percent: 5.0  },
    { id: 'rule-2', type: 'grace_period_warning',    enabled: true, threshold_percent: null },
    { id: 'rule-3', type: 'market_regime_change',    enabled: true, threshold_percent: null },
    { id: 'rule-4', type: 'daily_portfolio_summary', enabled: true, threshold_percent: null },
  ],
};

module.exports = {
  TD_NOTIF_A,
  TD_NOTIF_B,
  TD_NOTIF_C,
  TD_NOTIF_EMPTY,
  TD_NOTIF_PRICE_ALERT,
  TD_PREFS_ALL_ON,
  MARK_READ_OK,
  MARK_ALL_OK,
  PREF_UPDATE_OK,
  TD_ALERT_RULES,
  NOTIF_STOP_LOSS_UNREAD,
  NOTIF_PRICE_ALERT_WITH_CONTEXT,
};
