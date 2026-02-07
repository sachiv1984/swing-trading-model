// base44Client.js - API Client for Momentum Trading Assistant

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class Base44Client {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || `API Error: ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error(`API Request failed: ${endpoint}`, error);
      throw error;
    }
  }

  // Portfolio endpoints
  portfolio = {
    get: () => this.request('/portfolio'),
    addPosition: (positionData) => this.request('/portfolio/position', {
      method: 'POST',
      body: JSON.stringify(positionData),
    }),
    snapshot: () => this.request('/portfolio/snapshot', {
      method: 'POST',
    }),
    history: (days = 30) => this.request(`/portfolio/history?days=${days}`),
  };

  // Position endpoints
  positions = {
    list: () => this.request('/positions'),
    get: (ticker) => this.request(`/positions/${encodeURIComponent(ticker)}`),
    analyze: () => this.request('/positions/analyze'),
    
    // FIXED: Exit endpoint with proper parameter handling
    exit: async (exitData) => {
      console.log('Exit API call received:', exitData);
      
      // Validate required fields
      if (!exitData.position_id) {
        throw new Error('Position ID is required');
      }
      
      // Parse and validate shares
      const shares = parseFloat(exitData.shares);
      if (isNaN(shares) || shares <= 0) {
        console.error('Invalid shares value:', exitData.shares, 'parsed:', shares);
        throw new Error('Number of shares to exit is required and must be greater than 0');
      }
      
      // Parse and validate exit price
      const exitPrice = parseFloat(exitData.exit_price);
      if (isNaN(exitPrice) || exitPrice <= 0) {
        console.error('Invalid exit_price value:', exitData.exit_price, 'parsed:', exitPrice);
        throw new Error('Exit price is required and must be greater than 0');
      }
      
      // Build the request payload
      const payload = {
        shares,
        exit_price: exitPrice,
        exit_date: exitData.exit_date || new Date().toISOString().split('T')[0],
        exit_reason: exitData.exit_reason || 'Manual Exit',
      };
      
      // Add FX rate if provided (for US stocks)
      if (exitData.fx_rate !== undefined && exitData.fx_rate !== null) {
        const fxRate = parseFloat(exitData.fx_rate);
        if (!isNaN(fxRate) && fxRate > 0) {
          payload.fx_rate = fxRate;
        }
      }
      
      console.log('Exit API payload being sent:', payload);
      console.log('Exit API endpoint:', `/positions/${exitData.position_id}/exit`);
      
      return this.request(`/positions/${exitData.position_id}/exit`, {
        method: 'POST',
        body: JSON.stringify(payload),
      });
    },
  };

  // Cash endpoints
  cash = {
    transaction: (transactionData) => this.request('/cash/transaction', {
      method: 'POST',
      body: JSON.stringify(transactionData),
    }),
    transactions: (order = 'DESC') => this.request(`/cash/transactions?order=${order}`),
    summary: () => this.request('/cash/summary'),
  };

  // Trade history endpoints
  trades = {
    list: () => this.request('/trades'),
  };

  // Settings endpoints - FIXED to match your Settings entity structure
  entities = {
    Settings: {
      list: async () => {
        const response = await this.request('/settings');
        // The API returns { status: "ok", data: [...] }
        return response.data || response;
      },
    },
  };
}

// Export singleton instance
export const base44 = new Base44Client(API_BASE_URL);

// Also export the class for testing
export { Base44Client };
