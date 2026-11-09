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
// Preferences) are left out. Research opens its /Research landing (ST-01,
// BLG-FE-250, v9.16).
export const PALETTE_PAGE_KEYS = [
  "DashboardHome",
  "notifications",
  "Positions",
  "TradeEntry",
  "RiskDashboard",
  "Signals",
  "Screener",
  "Watchlist",
  "Research",
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

// Browser-tab title (navigation.md §Browser Tab Title; ST-13, BLG-FE-249, v9.15):
// "{page label} · Position Manager", Research pages "{TICKER} · Research ·
// Position Manager", unknown routes "Page not found · Position Manager".
// Other detail views (a trade plan, a replayed trade) use the page label alone,
// so no per-record data is fetched. Set once by Layout.js on route change;
// PageNotFound (rendered outside Layout) sets the not-found title. No page sets
// document.title itself.
export const APP_TITLE = "Position Manager";
export const TITLE_SEPARATOR = " · ";
export const NOT_FOUND_TITLE = `Page not found${TITLE_SEPARATOR}${APP_TITLE}`;

// Some routes render under another page's Layout key (App.js): the pathname
// tells them apart.
function pageKeyForPath(pageName, pathname) {
  const path = (pathname || "").toLowerCase();
  if (path === "/notifications/history") return "NotificationsHistory";
  if (path === "/notifications/preferences" || path === "/notificationpreferences") return "NotificationPreferences";
  return pageName;
}

export function documentTitle(pageName, pathname) {
  const key = pageKeyForPath(pageName, pathname);
  if (key === "Research") {
    const match = /^\/research\/([^/]+)/i.exec(pathname || "");
    if (match) {
      // Same ticker form as the Research heading (UK ".L" suffix dropped).
      // BLG-FE-273: a malformed percent-escape makes decodeURIComponent throw,
      // which would crash Layout's title effect and blank the app. Fall back to
      // the raw path segment instead.
      let segment = match[1];
      try {
        segment = decodeURIComponent(segment);
      } catch {
        // keep the raw segment
      }
      const ticker = segment.toUpperCase().replace(/\.L$/, "");
      return [ticker, PAGE_LABELS.Research, APP_TITLE].join(TITLE_SEPARATOR);
    }
  }
  const label = PAGE_LABELS[key];
  return label ? `${label}${TITLE_SEPARATOR}${APP_TITLE}` : NOT_FOUND_TITLE;
}
