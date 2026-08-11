// src/api/base44Client.js

// ---------- Config ----------
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
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
  const API_KEY = process.env.REACT_APP_API_KEY || '';
  const mergedHeaders = {
    ...(body ? { 'Content-Type': 'application/json' } : {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(API_KEY ? { 'X-API-Key': API_KEY } : {}),
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
  baseUrl: API_BASE_URL,
  auth: {
    /**
     * If you're using an OAuth/OIDC provider, you'll be redirected back with a token or a code.
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
      // Always return fake user (no backend auth)
      return {
        id: 'dev-user',
        email: 'dev@example.com',
        name: 'Dev User',
        role: 'admin',
      };
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

      // ✅ NEW: Update position note
      updateNote: async (positionId, entryNote) =>
        doFetch(`/positions/${positionId}/note`, {
          method: 'PATCH',
          body: JSON.stringify({ entry_note: entryNote }),
        }),

      // ✅ NEW: Update position tags
      updateTags: async (positionId, tags) =>
        doFetch(`/positions/${positionId}/tags`, {
          method: 'PATCH',
          body: JSON.stringify({ tags }),
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

        // ✅ FIXED: Include exit_note if provided
        if (requestData.exit_note) {
          body.exit_note = requestData.exit_note;
        }

        console.log('Exit request body:', body); // Debug log

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
    Signal: {
      list: async (orderBy = '-signal_date') => {
        return await doFetch('/signals', { raw: true });
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

      generate: async () =>
        doFetch('/signals/generate', {
          method: 'POST',
        }),
    },

    // TradeReflection: lists closed trades (for browsing page); filter loads per-trade reflection
    TradeReflection: {
      list: async () => {
        const result = await doFetch('/trades');
        const trades = result?.trades || [];
        return trades.map((t) => ({
          id: t.id,
          trade_id: t.id,
          ticker: t.ticker,
          market: t.market,
          entry_price: t.entry_price,
          exit_price: t.exit_price,
          exit_reason: t.exit_reason,
          exit_date: t.exit_date,
          hold_days: t.holding_days,
          r_multiple: t.net_r_multiple ?? null,
          pnl: t.pnl,
        }));
      },
      filter: async ({ trade_id }) => {
        try {
          const data = await doFetch(`/trades/${trade_id}/reflection`);
          return data ? [{ ...data, id: trade_id }] : [];
        } catch {
          return [];
        }
      },
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
    // ST-02 (BLG-FEAT-46, v6.0): Morning Briefing — red flag journal summary
    redFlagJournal: async (params = {}) => {
      const qs = Object.entries(params).filter(([, v]) => v !== undefined && v !== null).map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`).join('&');
      return doFetch(`/portfolio/red-flag-journal${qs ? '?' + qs : ''}`);
    },
    // Added for Position Sizing Calculator (roadmap 3.2)
    size: async (sizeData) =>
      doFetch('/portfolio/size', {
        method: 'POST',
        body: JSON.stringify(sizeData),
      }),
    prospectiveHeat: async (ticker, shares, entry_price, stop_price) =>
      doFetch(
        `/portfolio/prospective-heat?ticker=${encodeURIComponent(ticker)}&shares=${shares}&entry_price=${entry_price}&stop_price=${stop_price}`
      ),
    // ST-06 (v6.1): Sector concentration heat map
    sectorWeights: async () => doFetch('/portfolio/sector-weights'),
    // ST-07 (v6.1): Trade gate proximity indicator
    gateMetrics: async () => doFetch('/portfolio/gate-metrics'),
    // ST-02 (EPIC-02, v7.9, BLG-FEAT-67): sector/regime exposure trend
    sectorRegimeTrend: async (weeks = 12) => doFetch(`/portfolio/sector-regime-trend?weeks=${weeks}`),
  },

  positions: {
    list: async () =>
      // IMPORTANT: /positions returns array directly (raw)
      doFetch('/positions', { raw: true }),
    analyze: async () => doFetch('/positions/analyze'),
    // ST-01 (BLG-FEAT-11, v2.3): ATR-based per-position compliance flags
    positionCompliance: async () => doFetch('/positions/compliance'),
    // ST-02 (BLG-FEAT-46, v6.0): Morning Briefing — positions in exit zone
    gracePeriodAlerts: async () => doFetch('/positions/grace-period-alerts'),
  },

  trades: {
    list: async () => doFetch('/trades'),
    getReflection: async (tradeId) => doFetch(`/trades/${tradeId}/reflection`),
    saveReflection: async (tradeId, data) => doFetch(`/trades/${tradeId}/reflection`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    updateCosts: async (tradeId, costs) => doFetch(`/trades/${tradeId}/costs`, {
      method: 'PATCH',
      body: JSON.stringify(costs),
    }),
  },

  analytics: {
    metrics: async (period = 'all_time') =>
      doFetch(`/analytics/metrics?period=${encodeURIComponent(period)}`),
    cohort: async (period = 'month') =>
      doFetch(`/analytics/cohort?period=${encodeURIComponent(period)}`),
    rMultipleDistribution: async () =>
      doFetch('/analytics/r-multiple-distribution'),
    complianceMetrics: async () =>
      doFetch('/analytics/compliance-metrics'),
    marketCorrelation: async () =>
      doFetch('/analytics/market-correlation'),
    arc5Compliance: async (period = '7d') =>
      doFetch(`/analytics/arc5-compliance?period=${encodeURIComponent(period)}`),
    // ST-05 (v8.2, EPIC-01, BLG-FEAT-86): SI-02 insufficient_data streak metric
    behaviouralDrift: async () =>
      doFetch('/analytics/behavioural-drift'),
    // ST-05 (v6.8, BLG-FEAT-52): trade-plan tag performance comparison
    tagPerformance: async (tags) =>
      doFetch(`/analytics/tag-performance?tags=${encodeURIComponent(tags.join(','))}`),
    // ST-01 (v8.6, BLG-FEAT-32): trade plan completion rate (analytics.md §21)
    tradePlanCompletionRate: async () =>
      doFetch('/analytics/trade-plan-completion-rate'),
  },

  market: {
    getStatus: async () => doFetch('/market/status'),
  },

  signals: {
    list: async () => doFetch('/signals', { raw: true }),
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

  tradePlans: {
    // ST-08/09 (v6.1): Setup Quality Score
    setupQualityScore: async (ticker) =>
      doFetch(`/trade-plans/setup-quality-score?ticker=${encodeURIComponent(ticker)}`),
    // ST-05 (v6.8, BLG-FEAT-52): trade-plan tag autocomplete source
    tags: async () => doFetch('/trade-plans/tags'),
    // ST-02 (v8.6, BLG-FEAT-56): fetch a single plan by id — used by the
    // TradeEntry Setup Thesis Digest panel (trade_plan.md §10.5).
    getById: async (planId) => doFetch(`/trade-plans/${encodeURIComponent(planId)}`),
  },

  // ST-06/ST-08 (v6.2 EPIC-02): AI advisory endpoints — display-only, SRB-v1.7
  ai: {
    dailyBriefing: async () =>
      doFetch('/ai/daily-briefing', { method: 'POST', body: JSON.stringify({}) }),
    chat: async (question, context = null) =>
      doFetch('/ai/chat', {
        method: 'POST',
        body: JSON.stringify({ question, ...(context ? { context } : {}) }),
      }),
    // ST-07 (EPIC-07, v7.6, BLG-FEAT-77): Settings §6 AI Usage & Costs
    monthlyCost: async () => doFetch('/ai/monthly-cost'),
    // ST-06 (v7.8 EPIC-06, BLG-FEAT-82): AI spend trend chart
    spendTrend: async () => doFetch('/ai/spend-trend'),
  },

  // ST-11 (v6.3 EPIC-03): Strategy Benchmark — backtest vs live comparison
  strategyBenchmark: {
    getSummary: async ({ year, market } = {}) => {
      const params = new URLSearchParams();
      if (year != null) params.set('year', year);
      if (market && market !== 'ALL') params.set('market', market);
      const qs = params.toString();
      return doFetch(`/strategy/benchmark/summary${qs ? '?' + qs : ''}`);
    },
    getTrades: async ({ year, market } = {}) => {
      const params = new URLSearchParams();
      if (year != null) params.set('year', year);
      if (market && market !== 'ALL') params.set('market', market);
      const qs = params.toString();
      return doFetch(`/strategy/benchmark/trades${qs ? '?' + qs : ''}`);
    },
    getOpenPositions: async ({ market } = {}) => {
      const params = new URLSearchParams();
      if (market && market !== 'ALL') params.set('market', market);
      const qs = params.toString();
      return doFetch(`/strategy/benchmark/open-positions${qs ? '?' + qs : ''}`);
    },
    importData: async (payload) =>
      doFetch('/strategy/benchmark/import', {
        method: 'POST',
        body: JSON.stringify(payload),
      }),
  },

  // ST-01 (v7.7 EPIC-01, BLG-FEAT-75): SI-04 strategy version performance comparison
  strategyVersionComparison: {
    compare: async ({ versionFrom, versionTo, dateRange } = {}) => {
      const params = new URLSearchParams();
      params.set('version_from', versionFrom);
      params.set('version_to', versionTo);
      if (dateRange) params.set('date_range', dateRange);
      return doFetch(`/analytics/strategy-version-comparison?${params.toString()}`);
    },
  },

  // ST-01 (v7.8 EPIC-01, BLG-FE-128): in-app "What's New" panel
  changelog: {
    latest: async () => doFetch('/changelog/latest'),
  },
};

export const Signal = base44.entities.Signal;
export const Position = base44.entities.Position;

// ---------- apiFetch — raw fetch() with X-API-Key header ----------
// Use this instead of raw fetch() in pages/components so that the API key
// is forwarded automatically, matching the behaviour of doFetch / api.*.
export async function apiFetch(url, options = {}) {
  const API_KEY = process.env.REACT_APP_API_KEY || '';
  const headers = {
    ...(options.headers || {}),
    ...(API_KEY ? { 'X-API-Key': API_KEY } : {}),
  };
  return fetch(url, { ...options, headers });
}