// Canonical page labels — the single label source for the sidebar, the page
// heading, the command palette and the browser-tab title.
// Source of truth: docs/reference/glossary.md §UI Labels (v1.3, ST-08); rule:
// docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md §3.1.
// ST-11 (BLG-FE-248, EPIC-02, v9.15). A deliberate difference between surfaces
// is recorded in the glossary's "Deliberate difference" column, never here.
// Keys are the route page keys (pages.config.js PAGES, plus the routes App.js
// declares by hand).

export const PAGE_LABELS = {
  DashboardHome: "Dashboard",
  notifications: "Notifications",
  NotificationsHistory: "Notification History",
  NotificationPreferences: "Notification Preferences",
  Positions: "Positions",
  TradeEntry: "Trade Entry",
  RiskDashboard: "Risk Dashboard",
  Signals: "Signals",
  Screener: "Screener",
  Watchlist: "Watchlist",
  Research: "Research",
  TradePlans: "Trade Plans",
  TradePlan: "Trade Plan",
  TickerUniverse: "Ticker Universe",
  TradeHistory: "Trade History",
  PerformanceAnalytics: "Analytics",
  Reports: "Reports",
  StrategyBenchmark: "Strategy Benchmark",
  Replay: "Replay",
  TradeReflection: "Trade Reflections",
  RedFlagJournal: "Red Flag Journal",
  WeeklyDigest: "Weekly Digest",
  Settings: "Settings",
  SystemStatus: "System Status",
};

// Pages with a command-palette entry (glossary §UI Labels "Palette" column).
// Detail pages without a palette entry (Notification History, Notification
// Preferences) are left out. Research follows once its /Research landing
// exists (BLG-FE-250); until then the palette reaches it through Your Data.
export const PALETTE_PAGE_KEYS = [
  "DashboardHome",
  "notifications",
  "Positions",
  "TradeEntry",
  "RiskDashboard",
  "Signals",
  "Screener",
  "Watchlist",
  "TradePlans",
  "TradePlan",
  "TickerUniverse",
  "TradeHistory",
  "PerformanceAnalytics",
  "Reports",
  "StrategyBenchmark",
  "Replay",
  "TradeReflection",
  "RedFlagJournal",
  "WeeklyDigest",
  "Settings",
  "SystemStatus",
];

export function pageLabel(key) {
  return PAGE_LABELS[key];
}
