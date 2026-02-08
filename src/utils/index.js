export const createPageUrl = (pageName) => {
  // Routes must match the keys in pages.config.js exactly
  const routes = {
    Dashboard: '/',
    Positions: '/Positions',
    Signals: '/Signals',  
    TradeEntry: '/TradeEntry',  // Changed from /trade-entry
    TradeHistory: '/TradeHistory',  // Changed from /trade-history
    Reports: '/Reports',
    Settings: '/Settings',
  };
  return routes[pageName] || '/';
};
