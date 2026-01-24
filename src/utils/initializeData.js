export const initializeDefaultData = () => {
  // Check if portfolio exists, if not create default
  const portfolios = localStorage.getItem('portfolio_data');
  if (!portfolios || JSON.parse(portfolios).length === 0) {
    localStorage.setItem('portfolio_data', JSON.stringify([
      {
        id: '1',
        name: 'Main Portfolio',
        total_value: 10000,
        cash_balance: 5000,
        open_positions_value: 5000,
        total_pnl: 0,
        currency: 'GBP'
      }
    ]));
  }

  // Initialize empty arrays for other entities if needed
  if (!localStorage.getItem('position_data')) {
    localStorage.setItem('position_data', JSON.stringify([]));
  }
  
  if (!localStorage.getItem('settings_data')) {
    localStorage.setItem('settings_data', JSON.stringify([]));
  }
  
  if (!localStorage.getItem('marketregime_data')) {
    localStorage.setItem('marketregime_data', JSON.stringify([
      { id: '1', market: 'US', status: 'risk_on' },
      { id: '2', market: 'UK', status: 'risk_on' }
    ]));
  }
};
