export const createPageUrl = (pageName) => {
  // Routes must match the keys in pages.config.js exactly
  const routes = {
    Dashboard: '/',
    DashboardHome: '/',
    Positions: '/Positions',
    Signals: '/Signals',  
    TradeEntry: '/TradeEntry',
    TradeHistory: '/TradeHistory',
    Reports: '/Reports',
    Settings: '/Settings',
    SystemStatus: '/SystemStatus',
    PerformanceAnalytics: '/PerformanceAnalytics',
    RiskDashboard: '/RiskDashboard',
    TradeReflection: '/TradeReflection',
    notifications: '/notifications',
    NotificationPreferences: '/notifications/preferences',
    Watchlist: '/Watchlist',
    WeeklyDigest: '/WeeklyDigest',
    Screener: '/Screener',
    TickerUniverse: '/TickerUniverse',
  };
  return routes[pageName] || '/';
};
