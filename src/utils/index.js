export const createPageUrl = (pageName) => {
  const routes = {
    Dashboard: '/',
    Positions: '/positions',
    TradeEntry: '/trade-entry',
    TradeHistory: '/trade-history',
    Reports: '/reports',
    Settings: '/settings',
  };
  return routes[pageName] || '/';
};
