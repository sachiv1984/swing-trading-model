export const createPageUrl = (pageName) => {
  // Routes must match the keys in pages.config.js exactly
  const routes = {
    Dashboard: '/',
    Positions: '/Positions',
    Signals: '/Signals',  
    TradeEntry: '/TradeEntry',
    TradeHistory: '/TradeHistory',
    Reports: '/Reports',
    Settings: '/Settings',
    SystemStatus: '/SystemStatus',
    PerformanceAnalytics: '/PerformanceAnalytics',
  };
  return routes[pageName] || '/';
};
