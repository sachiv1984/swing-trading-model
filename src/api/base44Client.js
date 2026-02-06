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
    
    getHistory: async (days = 30) => {
      const response = await fetch(`${API_BASE_URL}/portfolio/history?days=${days}`);
      return handleResponse(response);
    },
    
    createSnapshot: async () => {
      const response = await fetch(`${API_BASE_URL}/portfolio/snapshot`, {
        method: 'POST'
      });
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
    list: async () => {
      const response = await fetch(`${API_BASE_URL}/positions`);
      // IMPORTANT: /positions returns array directly, not wrapped in {status, data}
      return response.json();
    },
    
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
  },
  
  settings: {
    list: async () => {
      const response = await fetch(`${API_BASE_URL}/settings`);
      return handleResponse(response);
    },
    
    create: async (settingsData) => {
      const response = await fetch(`${API_BASE_URL}/settings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settingsData)
      });
      return handleResponse(response);
    },
    
    update: async (id, settingsData) => {
      const response = await fetch(`${API_BASE_URL}/settings/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settingsData)
      });
      return handleResponse(response);
    }
  },
  
  cash: {
    createTransaction: async (transactionData) => {
      const response = await fetch(`${API_BASE_URL}/cash/transaction`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(transactionData)
      });
      return handleResponse(response);
    },
    
    getTransactions: async (order = 'DESC') => {
      const response = await fetch(`${API_BASE_URL}/cash/transactions?order=${order}`);
      return handleResponse(response);
    },
    
    getSummary: async () => {
      const response = await fetch(`${API_BASE_URL}/cash/summary`);
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
      },
      getHistory: async (days) => {
        return api.portfolio.getHistory(days);
      },
      createSnapshot: async () => {
        return api.portfolio.createSnapshot();
      }
    },
    Position: {
      list: async () => {
        return api.positions.list();
      },
      filter: async (conditions, orderBy) => {
        // Fetch all positions from /positions endpoint
        const positions = await api.positions.list();
        
        console.log('Fetched positions:', positions.length);
        
        // Filter by conditions (e.g., {status: "open"})
        let filtered = positions.filter(p => {
          return Object.entries(conditions).every(([key, value]) => {
            // Handle status filtering
            if (key === 'status') {
              // Backend returns "open" in status field
              return p[key] === value;
            }
            return p[key] === value;
          });
        });
        
        console.log('Filtered positions:', filtered.length, 'for conditions:', conditions);
        
        // Sort if orderBy is provided
        if (orderBy) {
          const isDescending = orderBy.startsWith('-');
          const field = isDescending ? orderBy.slice(1) : orderBy;
          filtered.sort((a, b) => {
            const aVal = a[field];
            const bVal = b[field];
            const comparison = aVal > bVal ? 1 : aVal < bVal ? -1 : 0;
            return isDescending ? -comparison : comparison;
          });
        }
        
        return filtered;
      },
      create: async (positionData) => {
        return api.portfolio.addPosition(positionData);
      },
      update: async (id, data) => {
        const response = await fetch(`${API_BASE_URL}/positions/${id}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        return response.json();
      },
      exit: async (id, exitData = {}) => {
    console.log('Calling exit endpoint for position:', id);
    console.log('Exit data:', exitData);
    
    // Validate required fields
    if (!exitData.exit_price || exitData.exit_price <= 0) {
      throw new Error('Exit price is required and must be greater than 0');
    }
    
    if (!exitData.shares || exitData.shares <= 0) {
      throw new Error('Number of shares to exit is required and must be greater than 0');
    }
    
    // Prepare request body with all new fields
    const requestBody = {
      shares: parseFloat(exitData.shares),
      exit_price: parseFloat(exitData.exit_price),
      exit_date: exitData.exit_date || new Date().toISOString().split('T')[0],
      exit_reason: exitData.exit_reason || 'Manual Exit'
    };
    
    // Add FX rate for US stocks (required)
    if (exitData.exit_fx_rate) {
      requestBody.exit_fx_rate = parseFloat(exitData.exit_fx_rate);
    }
    
    console.log('Request body:', requestBody);
    
    const response = await fetch(`${API_BASE_URL}/positions/${id}/exit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestBody)
    });
    
    const data = await response.json();
    
    console.log('Exit response:', data);
    
    if (data.status === 'error') {
      throw new Error(data.message);
    }
    
    return data.data;
  }
}
    },
    Settings: {
      list: async () => {
        return api.settings.list();
      },
      create: async (data) => {
        return api.settings.create(data);
      },
      update: async (id, data) => {
        return api.settings.update(id, data);
      }
    },
    MarketRegime: {
      list: async () => {
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
        return [
          { market: 'US', status: 'risk_on' },
          { market: 'UK', status: 'risk_on' }
        ];
      }
    },
    CashTransaction: {
      list: async (orderBy = '-date') => {
        const isDescending = orderBy.startsWith('-');
        const order = isDescending ? 'DESC' : 'ASC';
        return api.cash.getTransactions(order);
      },
      create: async (transactionData) => {
        return api.cash.createTransaction(transactionData);
      },
      getSummary: async () => {
        return api.cash.getSummary();
      }
    }
  }
};
