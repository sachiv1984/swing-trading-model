const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const handleResponse = async (response) => {
  const data = await response.json();
  
  if (data.status === 'error') {
    throw new Error(data.message);
  }
  
  return data.data;
};

export const api = {
  dashboard: {
    get: async () => {
      const response = await fetch(`${API_BASE_URL}/dashboard`);
      return handleResponse(response);
    }
  },
  
  portfolio: {
    get: async () => {
      const response = await fetch(`${API_BASE_URL}/portfolio`);
      return handleResponse(response);
    },
    
    addPosition: async (positionData) => {
      const response = await fetch(`${API_BASE_URL}/portfolio/position`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(positionData)
      });
      return handleResponse(response);
    }
  },
  
  positions: {
    analyze: async () => {
      const response = await fetch(`${API_BASE_URL}/positions/analyze`);
      return handleResponse(response);
    }
  },
  
  trades: {
    list: async () => {
      const response = await fetch(`${API_BASE_URL}/trades`);
      return handleResponse(response);
    }
  }
};

// Keep compatibility with old base44 structure
export const base44 = {
  entities: {
    Portfolio: {
      list: () => api.portfolio.get().then(data => [{ ...data }])
    },
    Position: {
      list: () => api.portfolio.get().then(data => data.positions),
      filter: (conditions) => api.portfolio.get().then(data => 
        data.positions.filter(p => 
          Object.entries(conditions).every(([key, value]) => p[key] === value)
        )
      )
    },
    Settings: {
      list: () => Promise.resolve([])
    },
    MarketRegime: {
      list: () => api.dashboard.get().then(data => [
        { market: 'US', status: data.market_status.spy.risk_on ? 'risk_on' : 'risk_off' },
        { market: 'UK', status: data.market_status.ftse.risk_on ? 'risk_on' : 'risk_off' }
      ])
    }
  }
};
