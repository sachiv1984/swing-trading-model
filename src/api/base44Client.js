const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const handleResponse = async (response) => {
  const data = await response.json();
  
  if (data.status === 'error') {
    throw new Error(data.message);
  }
  
  return data.data;
};

export const api = {
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

// Backwards compatibility with base44 structure
export const base44 = {
  entities: {
    Portfolio: {
      list: async () => {
        const data = await api.portfolio.get();
        return [{ cash: data.cash, ...data }];
      }
    },
    Position: {
      list: async () => {
        const data = await api.portfolio.get();
        return data.positions || [];
      },
      filter: async (conditions) => {
        const data = await api.portfolio.get();
        const positions = data.positions || [];
        return positions.filter(p => 
          Object.entries(conditions).every(([key, value]) => p[key] === value)
        );
      },
      create: async (positionData) => {
        return api.portfolio.addPosition(positionData);
      }
    },
    Settings: {
      list: async () => Promise.resolve([])
    },
    MarketRegime: {
      list: async () => {
        // Try to get from analysis endpoint
        try {
          const analysis = await api.positions.analyze();
          if (analysis && analysis.market_regime) {
            return [
              { market: 'US', status: analysis.market_regime.spy_risk_on ? 'risk_on' : 'risk_off' },
              { market: 'UK', status: analysis.market_regime.ftse_risk_on ? 'risk_on' : 'risk_off' }
            ];
          }
        } catch (error) {
          console.error('Failed to get market regime:', error);
        }
        // Fallback
        return [
          { market: 'US', status: 'risk_on' },
          { market: 'UK', status: 'risk_on' }
        ];
      }
    }
  }
};
