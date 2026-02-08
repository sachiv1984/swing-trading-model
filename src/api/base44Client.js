// src/api/base44Client.js

// ---------- Config ----------
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const APP_ID = process.env.REACT_APP_APP_ID || 'local-app-id';
const DEV_FAKE_AUTH = String(process.env.REACT_APP_DEV_FAKE_AUTH || '').toLowerCase() === 'true';

// ---------- Token storage ----------
const TOKEN_KEY = 'app_token';

function getToken() {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
}
function setToken(token) {
  try {
    if (token) localStorage.setItem(TOKEN_KEY, token);
    else localStorage.removeItem(TOKEN_KEY);
  } catch {}
}

// Expose app params (backwards compatibility with your previous code)
export const appParams = {
  appId: APP_ID,
  token: getToken(),
};

// ---------- Fetch helpers ----------
async function doFetch(path, { method = 'GET', headers = {}, body, raw = false } = {}) {
  const token = getToken();
  const mergedHeaders = {
    ...(body ? { 'Content-Type': 'application/json' } : {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...headers,
  };

  const res = await fetch(
    path.startsWith('http') ? path : `${API_BASE_URL}${path}`,
    { method, headers: mergedHeaders, body }
  );

  let json;
  try {
    json = await res.json();
  } catch {
    // Non-JSON response
    if (!res.ok) {
      const text = await res.text();
      throw { status: res.status, data: text, message: text || 'Request failed' };
    }
    return null;
  }

  // If caller wants raw JSON (arrays, non-wrapped responses)
  if (raw) {
    if (!res.ok) {
      throw { status: res.status, data: json, message: json?.message || 'Request failed' };
    }
    return json;
  }

  // "Base44-like" envelope: { status, data }
  if (!res.ok || json?.status === 'error') {
    throw { status: res.status, data: json, message: json?.message || 'Request failed' };
  }

  // If server uses {status, data}, return data; else return json
  if (json && typeof json === 'object' && 'data' in json && 'status' in json) {
    return json.data;
  }
  return json;
}

// ---------- A tiny wrapper for your original handleResponse ----------
const handleResponse = async (response) => {
  const data = await response.json();
  if (data.status === 'error') throw new Error(data.message);
  return data.data;
};

// ---------- Public Apps API ----------
async function getPublicSettingsById(appId) {
  // Include X-App-Id header (if your backend requires it)
  return doFetch(`/apps/public/prod/public-settings/by-id/${appId}`, {
    headers: { 'X-App-Id': appId },
    raw: false, // expects {status, data}
  });
}

// ---------- Auth ----------
export const base44 = {
  auth: {
    /**
     * If you’re using an OAuth/OIDC provider, you’ll be redirected back with a token or a code.
     * This helper captures ?token= or ?access_token= from the URL and stores it.
     */
    initFromUrl() {
      if (typeof window === 'undefined') return;
      const url = new URL(window.location.href);
      const token = url.searchParams.get('token') || url.searchParams.get('access_token');
      if (token) {
        setToken(token);
        appParams.token = token;
        // Clean the URL
        url.searchParams.delete('token');
        url.searchParams.delete('access_token');
        window.history.replaceState({}, '', url.toString());
      }
    },

    /**
     * Returns the current user based on Authorization header.
     * Expects your backend to implement GET /auth/me
     *   -> envelope: {status, data: { id, email, name, ... }}  OR raw user object
     */
    async me() {
      if (DEV_FAKE_AUTH && !getToken()) {
        // Dev-only fake identity (no backend yet)
        return {
          id: 'dev-user',
          email: 'dev@example.com',
          name: 'Dev User',
          roles: ['admin'],
        };
      }
      // Prefer envelope; if your backend returns raw user, we still handle it.
      const result = await doFetch('/auth/me', { raw: true });
      if (result && typeof result === 'object' && 'data' in result && 'status' in result) {
        return result.data;
      }
      return result; // raw user object
    },

    /**
     * Starts a login redirect. Backend should begin OIDC/OAuth2 flow and
     * return to your app with ?token=... or ?code=... that you parse in initFromUrl().
     */
    redirectToLogin(redirectUri) {
      const target =
        redirectUri ||
        (typeof window !== 'undefined' ? window.location.href : '/');
      if (typeof window !== 'undefined') {
        window.location.assign(
          `${API_BASE_URL}/auth/login?redirect_uri=${encodeURIComponent(target)}`
        );
      }
    },

    /**
     * Clears token and optionally redirects via backend (to clear server session/cookies).
     */
    logout(redirectUri) {
      setToken(null);
      appParams.token = null;
      if (typeof window !== 'undefined' && redirectUri) {
        window.location.assign(
          `${API_BASE_URL}/auth/logout?redirect_uri=${encodeURIComponent(redirectUri)}`
        );
      }
    },

    /** If your IdP sends back a code (Authorization Code + PKCE), exchange it here. */
    async exchangeCodeForToken(params) {
      // Example: POST /auth/callback { code, state? } -> { token }
      const result = await doFetch('/auth/callback', {
        method: 'POST',
        body: JSON.stringify(params),
        raw: true,
      });
      const token = result?.token;
      if (token) {
        setToken(token);
        appParams.token = token;
      }
      return token;
    },

    getToken,
    setToken,
  },

  // Keep a public API namespace similar to Base44 if you want
  apps: {
    public: {
      getPublicSettingsById,
    },
  },

  // ---------- Your existing data APIs preserved ----------
  entities: {
    Portfolio: {
      list: async () => {
        const data = await api.portfolio.get();
        return [{ cash: data.cash, ...data }];
      },
      getHistory: async (days) => api.portfolio.getHistory(days),
      createSnapshot: async () => api.portfolio.createSnapshot(),
    },
    Position: {
      list: async () => api.positions.list(),
      filter: async (conditions, orderBy) => {
        const positions = await api.positions.list();

        // Filter by conditions
        let filtered = positions.filter((p) =>
          Object.entries(conditions).every(([key, value]) => {
            if (key === 'status') return p[key] === value;
            return p[key] === value;
          })
        );

        // Sort if orderBy provided
        if (orderBy) {
          const isDescending = orderBy.startsWith('-');
          const field = isDescending ? orderBy.slice(1) : orderBy;
          filtered.sort((a, b) => {
            const aVal = a[field];
            const bVal = b[field];
            const cmp = aVal > bVal ? 1 : aVal < bVal ? -1 : 0;
            return isDescending ? -cmp : cmp;
          });
        }

        return filtered;
      },
      create: async (positionData) => api.portfolio.addPosition(positionData),
      update: async (id, data) =>
        doFetch(`/positions/${id}`, {
          method: 'PATCH',
          body: JSON.stringify(data),
          raw: true, // backend returns raw json for this route
        }),
      // Exit supports both call shapes:
      //   exit(id, {exit_price, shares, ...})
      //   exit({position_id, exit_price, shares, ...})
      exit: async (idOrExitData, exitData) => {
        let positionId;
        let requestData;

        if (typeof idOrExitData === 'string' || typeof idOrExitData === 'number') {
          positionId = idOrExitData;
          requestData = exitData || {};
        } else if (typeof idOrExitData === 'object' && idOrExitData !== null) {
          positionId = idOrExitData.position_id;
          requestData = idOrExitData;
        } else {
          throw new Error('Invalid arguments to exit()');
        }

        if (!positionId) throw new Error('Position ID is required');

        const sharesValue = requestData.shares || requestData.exit_shares;
        const shares = parseFloat(sharesValue);
        if (isNaN(shares) || shares <= 0) {
          throw new Error('Number of shares to exit is required and must be > 0');
        }

        const exitPriceValue = requestData.exit_price || requestData.price;
        const exitPrice = parseFloat(exitPriceValue);
        if (isNaN(exitPrice) || exitPrice <= 0) {
          throw new Error('Exit price is required and must be > 0');
        }

        const body = {
          shares,
          exit_price: exitPrice,
          exit_date: requestData.exit_date || new Date().toISOString().split('T')[0],
          exit_reason: requestData.exit_reason || 'Manual Exit',
        };

        const fxRateValue = requestData.fx_rate || requestData.exit_fx_rate;
        const fxRate = parseFloat(fxRateValue);
        if (!isNaN(fxRate) && fxRate > 0) {
          body.exit_fx_rate = fxRate;
        }

        const result = await doFetch(`/positions/${positionId}/exit`, {
          method: 'POST',
          body: JSON.stringify(body),
          raw: true, // route returns {status,data} or raw; handle below
        });

        if (result?.status === 'error') {
          throw new Error(result?.message || 'Exit failed');
        }
        return result?.data ?? result;
      },
    },
    Settings: {
      list: async () => api.settings.list(),
      create: async (data) => api.settings.create(data),
      update: async (id, data) => api.settings.update(id, data),
    },
    MarketRegime: {
      list: async () => {
        try {
          const analysis = await api.positions.analyze();
          if (analysis && analysis.market_regime) {
            return [
              { market: 'US', status: analysis.market_regime.spy_risk_on ? 'risk_on' : 'risk_off' },
              { market: 'UK', status: analysis.market_regime.ftse_risk_on ? 'risk_on' : 'risk_off' },
            ];
          }
        } catch (e) {
          console.error('Failed to get market regime', e);
        }
        return [
          { market: 'US', status: 'risk_on' },
          { market: 'UK', status: 'risk_on' },
        ];
      },
    },
    CashTransaction: {
      list: async (orderBy = '-date') => {
        const isDescending = orderBy.startsWith('-');
        const order = isDescending ? 'DESC' : 'ASC';
        return api.cash.getTransactions(order);
      },
      create: async (tx) => api.cash.createTransaction(tx),
      getSummary: async () => api.cash.getSummary(),
    },
  },
};

// ---------- Your original api.* methods, now using doFetch ----------
export const api = {
  portfolio: {
    get: async () => doFetch('/portfolio'),
    getHistory: async (days = 30) => doFetch(`/portfolio/history?days=${days}`),
    createSnapshot: async () => doFetch('/portfolio/snapshot', { method: 'POST' }),
    addPosition: async (positionData) =>
      doFetch('/portfolio/position', {
        method: 'POST',
        body: JSON.stringify(positionData),
      }),
  },

  positions: {
    list: async () =>
      // IMPORTANT: /positions returns array directly (raw)
      doFetch('/positions', { raw: true }),
    analyze: async () => doFetch('/positions/analyze'),
  },

  trades: {
    list: async () => doFetch('/trades'),
  },

  settings: {
    list: async () => doFetch('/settings'),
    create: async (settingsData) =>
      doFetch('/settings', {
        method: 'POST',
        body: JSON.stringify(settingsData),
      }),
    update: async (id, settingsData) =>
      doFetch(`/settings/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(settingsData),
      }),
  },

  cash: {
    createTransaction: async (transactionData) =>
      doFetch('/cash/transaction', {
        method: 'POST',
        body: JSON.stringify(transactionData),
      }),
    getTransactions: async (order = 'DESC') =>
      doFetch(`/cash/transactions?order=${order}`),
    getSummary: async () => doFetch('/cash/summary'),
  },
};
Signal: {
      list: async (orderBy = '-signal_date') => {
        try {
          // Try to fetch from backend (when endpoint exists)
          return await doFetch('/signals', { raw: true });
        } catch (error) {
          // Fallback to mock data if endpoint doesn't exist
          console.warn('Signals endpoint not available, using mock data');
          return generateMockSignals();
        }
      },
      
      create: async (signalData) =>
        doFetch('/signals', {
          method: 'POST',
          body: JSON.stringify(signalData),
        }),
      
      update: async (id, data) =>
        doFetch(`/signals/${id}`, {
          method: 'PATCH',
          body: JSON.stringify(data),
        }),
      
      delete: async (id) =>
        doFetch(`/signals/${id}`, {
          method: 'DELETE',
        }),
    },
  },
};

// Helper function for mock signals (remove when backend is ready)
function generateMockSignals() {
  const today = new Date();
  const signalDate = new Date(today.getFullYear(), today.getMonth(), 1);
  const signalDateStr = signalDate.toISOString().split('T')[0];
  
  const mockTickers = [
    { ticker: 'NVDA', market: 'US', momentum: 12.3, price: 878.45, atr: 24.5 },
    { ticker: 'TSLA', market: 'US', momentum: 8.7, price: 245.67, atr: 18.2 },
    { ticker: 'FRES', market: 'UK', momentum: 15.2, price: 42.35, atr: 3.1 },
    { ticker: 'BARC', market: 'UK', momentum: 6.4, price: 238.50, atr: 8.7 },
    { ticker: 'AAPL', market: 'US', momentum: 5.9, price: 182.34, atr: 5.4 },
  ];

  const portfolioValue = 10000; // £10k default
  const riskPerTrade = 0.02; // 2% risk per trade

  const signals = mockTickers.map((stock, index) => {
    const riskAmount = portfolioValue * riskPerTrade;
    const stopDistance = stock.atr * 5; // 5x ATR wide stop
    const suggestedShares = Math.floor(riskAmount / stopDistance);
    
    // Calculate total cost in GBP
    let totalCost;
    if (stock.market === 'US') {
      // Convert USD to GBP (using 1.3611 rate)
      totalCost = (suggestedShares * stock.price) / 1.3611;
    } else {
      totalCost = suggestedShares * stock.price;
    }

    return {
      id: `signal-${index + 1}`,
      ticker: stock.ticker,
      market: stock.market,
      signal_date: signalDateStr,
      current_price: stock.price,
      momentum_percent: stock.momentum,
      atr_value: stock.atr,
      initial_stop: stock.price - (stock.atr * 5),
      suggested_shares: suggestedShares,
      total_cost: totalCost,
      rank: index + 1,
      status: 'new', // new, entered, dismissed, expired
    };
  });

  return signals;
}
``
