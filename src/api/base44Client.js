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
      // FIXED: Exit function now handles both calling patterns
      exit: async (idOrExitData, exitData) => {
        console.log('=== EXIT FUNCTION CALLED ===');
        console.log('Argument 1 (idOrExitData):', idOrExitData);
        console.log('Argument 2 (exitData):', exitData);
        
        let positionId;
        let requestData;
        
        // Handle two calling patterns:
        // 1. exit(id, {exit_price, shares, ...}) - old pattern
        // 2. exit({position_id, exit_price, shares, ...}) - new pattern from ExitModal
        
        if (typeof idOrExitData === 'string' || typeof idOrExitData === 'number') {
          // Pattern 1: exit(id, exitData)
          positionId = idOrExitData;
          requestData = exitData || {};
        } else if (typeof idOrExitData === 'object' && idOrExitData !== null) {
          // Pattern 2: exit({position_id, ...})
          positionId = idOrExitData.position_id;
          requestData = idOrExitData;
        } else {
          throw new Error('Invalid arguments to exit function');
        }
        
        console.log('Position ID:', positionId);
        console.log('Request data:', requestData);
        
        // Validate position ID
        if (!positionId) {
          throw new Error('Position ID is required');
        }
        
        // Parse and validate shares - CHECK THE ACTUAL FIELD NAME
        const sharesValue = requestData.shares || requestData.exit_shares;
        const shares = parseFloat(sharesValue);
        
        console.log('Shares field value:', sharesValue);
        console.log('Parsed shares:', shares);
        
        if (isNaN(shares) || shares <= 0) {
          console.error('VALIDATION FAILED - Invalid shares');
          console.error('  Original value:', sharesValue);
          console.error('  Parsed value:', shares);
          console.error('  Full requestData:', requestData);
          throw new Error('Number of shares to exit is required and must be greater than 0');
        }
        
        // Parse and validate exit price
        const exitPriceValue = requestData.exit_price || requestData.price;
        const exitPrice = parseFloat(exitPriceValue);
        
        console.log('Exit price field value:', exitPriceValue);
        console.log('Parsed exit price:', exitPrice);
        
        if (isNaN(exitPrice) || exitPrice <= 0) {
          console.error('VALIDATION FAILED - Invalid exit price');
          console.error('  Original value:', exitPriceValue);
          console.error('  Parsed value:', exitPrice);
          throw new Error('Exit price is required and must be greater than 0');
        }
        
        // Prepare request body with all fields
        const requestBody = {
          shares: shares,
          exit_price: exitPrice,
          exit_date: requestData.exit_date || new Date().toISOString().split('T')[0],
          exit_reason: requestData.exit_reason || 'Manual Exit'
        };
        
        // Add FX rate for US stocks if provided
        if (requestData.fx_rate || requestData.exit_fx_rate) {
          const fxRateValue = requestData.fx_rate || requestData.exit_fx_rate;
          const fxRate = parseFloat(fxRateValue);
          if (!isNaN(fxRate) && fxRate > 0) {
            requestBody.fx_rate = fxRate;
          }
        }
        
        console.log('Final request body:', requestBody);
        console.log('Making POST to:', `${API_BASE_URL}/positions/${positionId}/exit`);
        
        const response = await fetch(`${API_BASE_URL}/positions/${positionId}/exit`, {
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
