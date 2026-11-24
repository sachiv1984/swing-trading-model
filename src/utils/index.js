export const createPageUrl = (pageName) => {
  // Routes must match the keys in pages.config.js exactly
  const routes = {
    Dashboard: '/',
    DashboardHome: '/',
    Positions: '/Positions',
    Signals: '/Signals',  
    TradeEntry: '/TradeEntry',
    TradeHistory: '/TradeHistory',
    Settings: '/Settings',
    SystemStatus: '/SystemStatus',
    Performance: '/Performance',
    RiskDashboard: '/RiskDashboard',
    notifications: '/notifications',
    NotificationPreferences: '/notifications/preferences',
    Watchlist: '/Watchlist',
    WeeklyDigest: '/WeeklyDigest',
    Screener: '/Screener',
    // navigation.md v2.5 (ST-08, BLG-FE-323, v9.18): Ticker Universe is a
    // Settings detail page; Strategy Benchmark is Performance's
    // "Strategy vs backtest" section.
    TickerUniverse: '/settings/ticker-universe',
    Journal: '/Journal',
    StrategyVsBacktest: '/Performance?section=strategy-vs-backtest',
    Replay: '/Replay',
    TradePlan: '/TradePlan',
    TradePlans: '/TradePlans',
    Research: '/Research',
  };
  return routes[pageName] || '/';
};
