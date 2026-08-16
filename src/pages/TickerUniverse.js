import { useState, useCallback, useEffect, useMemo } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "../api/base44Client";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import PageHeader from "../components/ui/PageHeader";
import DataState from "../components/ui/DataState";
import { cn } from "../lib/utils";
import { Plus, Trash2, ToggleLeft, ToggleRight, Loader2, X } from "lucide-react";

// ST-15 (EPIC-03, BLG-FE-163, v8.8): search-input debounce, matching the
// project-wide search-input debounce convention (not a new timing parameter
// per design_gate_prompt.md §6 — see decision record).
const SEARCH_DEBOUNCE_MS = 200;

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function displayTicker(ticker) {
  return ticker.endsWith(".L") ? ticker.slice(0, -2) : ticker;
}

function MarketBadge({ market }) {
  const cls =
    market === "UK"
      ? "bg-blue-500/20 text-blue-400 border-blue-500/30"
      : "bg-violet-500/20 text-violet-400 border-violet-500/30";
  return (
    <span className={cn("inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border", cls)}>
      {market}
    </span>
  );
}

function ActiveBadge({ active }) {
  return active ? (
    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
      Active
    </span>
  ) : (
    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-slate-700/50 text-slate-600 dark:text-slate-400 border border-slate-600/30">
      Inactive
    </span>
  );
}

// ---------------------------------------------------------------------------
// Add Ticker Form
// ---------------------------------------------------------------------------

const EMPTY_FORM = { ticker: "", market: "US", sector: "", industry: "" };

function AddTickerForm({ onAdded, onCancel }) {
  const [form, setForm] = useState(EMPTY_FORM);
  const [error, setError] = useState(null);

  const mutation = useMutation({
    mutationFn: async (payload) => {
      const res = await apiFetch(`${API_BASE}/ticker-universe`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        // ST-08 (EPIC-02, v8.3, BLG-BE-69): canonical error envelope uses "message", not "detail".
        throw new Error(body.message || `HTTP ${res.status}`);
      }
      return res.json();
    },
    onSuccess: (data) => {
      onAdded(data.data);
    },
    onError: (err) => setError(err.message),
  });

  function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    const ticker = form.ticker.trim().toUpperCase();
    if (!ticker) { setError("Ticker is required"); return; }
    mutation.mutate({
      ticker,
      market: form.market,
      sector: form.sector.trim() || null,
      industry: form.industry.trim() || null,
    });
  }

  const inputCls = "w-full px-3 py-2 text-sm bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-cyan-500";
  const labelCls = "block text-xs text-slate-600 dark:text-slate-400 mb-1";

  return (
    <form onSubmit={handleSubmit} data-testid="add-ticker-form" className="bg-slate-800/50 border border-slate-700 rounded-xl p-4 mb-4">
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm font-medium text-slate-200">Add Ticker</span>
        <button type="button" onClick={onCancel} className="text-slate-600 dark:text-slate-400 hover:text-slate-300">
          <X size={16} />
        </button>
      </div>
      {error && (
        <p className="text-red-400 text-xs mb-3 bg-red-900/20 border border-red-800/30 rounded px-3 py-2">
          {error}
        </p>
      )}
      <div className="grid grid-cols-2 gap-3 mb-3">
        <div>
          <label className={labelCls}>Ticker *</label>
          <input
            className={inputCls}
            placeholder="e.g. AAPL"
            value={form.ticker}
            onChange={(e) => setForm((f) => ({ ...f, ticker: e.target.value.toUpperCase() }))}
            aria-label="Ticker symbol"
            autoFocus
          />
        </div>
        <div>
          <label className={labelCls}>Market *</label>
          <select
            className={inputCls}
            value={form.market}
            onChange={(e) => setForm((f) => ({ ...f, market: e.target.value }))}
            aria-label="Market"
          >
            <option value="US">US</option>
            <option value="UK">UK</option>
          </select>
        </div>
        <div>
          <label className={labelCls}>Sector</label>
          <input
            className={inputCls}
            placeholder="e.g. Technology"
            value={form.sector}
            onChange={(e) => setForm((f) => ({ ...f, sector: e.target.value }))}
            aria-label="Sector"
          />
        </div>
        <div>
          <label className={labelCls}>Industry</label>
          <input
            className={inputCls}
            placeholder="e.g. Software"
            value={form.industry}
            onChange={(e) => setForm((f) => ({ ...f, industry: e.target.value }))}
            aria-label="Industry"
          />
        </div>
      </div>
      <div className="flex gap-2 justify-end">
        <Button type="button" variant="ghost" size="sm" onClick={onCancel} disabled={mutation.isPending}>
          Cancel
        </Button>
        <Button type="submit" size="sm" disabled={mutation.isPending}>
          {mutation.isPending ? <Loader2 size={14} className="animate-spin mr-1" /> : null}
          Add Ticker
        </Button>
      </div>
    </form>
  );
}

// ---------------------------------------------------------------------------
// Main Page
// ---------------------------------------------------------------------------

export default function TickerUniverse() {
  const queryClient = useQueryClient();
  const [showForm, setShowForm] = useState(false);
  const [marketFilter, setMarketFilter] = useState("all");
  const [activeFilter, setActiveFilter] = useState("all");
  const [pendingAction, setPendingAction] = useState({}); // { [ticker]: true }

  // ST-15 (EPIC-03, BLG-FE-163, v8.8): search/sector/industry filters —
  // docs/specs/frontend/pages/ticker_universe.md §10.
  const [searchInput, setSearchInput] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [sectorFilter, setSectorFilter] = useState("all");
  const [industryFilter, setIndustryFilter] = useState("all");

  useEffect(() => {
    const t = setTimeout(() => setDebouncedSearch(searchInput.trim().toLowerCase()), SEARCH_DEBOUNCE_MS);
    return () => clearTimeout(t);
  }, [searchInput]);

  // Fetch all tickers (active and inactive)
  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["ticker-universe"],
    queryFn: async () => {
      const res = await apiFetch(`${API_BASE}/ticker-universe?active_only=false`);
      const json = await res.json();
      return json.data || [];
    },
    staleTime: 30 * 1000,
  });

  const tickers = data || [];

  // ST-15: Sector/Industry <select> options — derived dynamically from the
  // loaded ticker list, no new endpoint (ticker_universe.md §10).
  const sectorOptions = useMemo(
    () => Array.from(new Set(tickers.map((t) => t.sector).filter(Boolean))).sort(),
    [tickers]
  );
  const industryOptions = useMemo(
    () => Array.from(new Set(tickers.map((t) => t.industry).filter(Boolean))).sort(),
    [tickers]
  );

  // Filter — all 5 controls AND-combine (Market, Active, Search, Sector, Industry).
  const filtered = tickers.filter((t) => {
    if (marketFilter !== "all" && t.market !== marketFilter) return false;
    if (activeFilter === "active" && !t.active) return false;
    if (activeFilter === "inactive" && t.active) return false;
    if (sectorFilter !== "all" && t.sector !== sectorFilter) return false;
    if (industryFilter !== "all" && t.industry !== industryFilter) return false;
    if (debouncedSearch) {
      const haystack = `${t.ticker} ${t.company_name || ""}`.toLowerCase();
      if (!haystack.includes(debouncedSearch)) return false;
    }
    return true;
  });

  const hasActiveFilters =
    marketFilter !== "all" ||
    activeFilter !== "all" ||
    sectorFilter !== "all" ||
    industryFilter !== "all" ||
    searchInput.trim() !== "";

  function handleClearFilters() {
    setMarketFilter("all");
    setActiveFilter("all");
    setSectorFilter("all");
    setIndustryFilter("all");
    setSearchInput("");
    setDebouncedSearch("");
  }

  // Deactivate (soft delete) mutation
  const deactivateMutation = useMutation({
    mutationFn: async (ticker) => {
      const res = await apiFetch(`${API_BASE}/ticker-universe/${ticker}`, { method: "DELETE" });
      if (!res.ok && res.status !== 404) throw new Error(`HTTP ${res.status}`);
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["ticker-universe"] }),
    onSettled: (_, __, ticker) => setPendingAction((p) => { const n = { ...p }; delete n[ticker]; return n; }),
  });

  // Reactivate (POST with conflict re-activate logic)
  const reactivateMutation = useMutation({
    mutationFn: async ({ ticker, market, sector, industry }) => {
      const res = await apiFetch(`${API_BASE}/ticker-universe`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ticker, market, sector: sector || null, industry: industry || null }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["ticker-universe"] }),
    onSettled: (_, __, { ticker }) => setPendingAction((p) => { const n = { ...p }; delete n[ticker]; return n; }),
  });

  const handleToggle = useCallback((row) => {
    setPendingAction((p) => ({ ...p, [row.ticker]: true }));
    if (row.active) {
      deactivateMutation.mutate(row.ticker);
    } else {
      reactivateMutation.mutate(row);
    }
  }, [deactivateMutation, reactivateMutation]);

  const handleDelete = useCallback((row) => {
    if (!window.confirm(`Permanently deactivate ${row.ticker}? (It can be re-added later.)`)) return;
    setPendingAction((p) => ({ ...p, [row.ticker]: true }));
    deactivateMutation.mutate(row.ticker);
  }, [deactivateMutation]);

  function handleAdded() {
    setShowForm(false);
    queryClient.invalidateQueries({ queryKey: ["ticker-universe"] });
  }

  const filterBtnCls = (active) =>
    cn(
      "px-3 py-1.5 text-xs rounded-lg border transition-colors",
      active
        ? "bg-cyan-600 border-cyan-500 text-white"
        : "bg-slate-800 border-slate-700 text-slate-600 dark:text-slate-400 hover:text-slate-200"
    );

  return (
    <div className="p-4 md:p-6 max-w-5xl mx-auto">
      <PageHeader
        title="Ticker Universe"
        description={`${tickers.filter((t) => t.active).length} active tickers`}
        actions={
          <Button size="sm" onClick={() => setShowForm((v) => !v)} data-testid="add-ticker-btn">
            <Plus size={14} className="mr-1" />
            Add Ticker
          </Button>
        }
      />

      {showForm && (
        <AddTickerForm onAdded={handleAdded} onCancel={() => setShowForm(false)} />
      )}

      {/* Filters */}
      <div className="flex flex-wrap gap-2 mb-4 items-center" data-testid="filter-bar">
        <input
          type="text"
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          placeholder="Search ticker or company…"
          aria-label="Search ticker or company"
          data-testid="ticker-search-input"
          className="flex-1 min-w-[220px] px-3 py-1.5 text-xs bg-slate-800 border border-slate-700 rounded-lg text-white placeholder:text-slate-600 dark:placeholder:text-slate-400 focus:outline-none focus:border-cyan-500"
        />
        <select
          value={sectorFilter}
          onChange={(e) => setSectorFilter(e.target.value)}
          aria-label="Filter by sector"
          data-testid="sector-filter"
          className="px-3 py-1.5 text-xs bg-slate-800 border border-slate-700 rounded-lg text-slate-200 focus:outline-none focus:border-cyan-500"
        >
          <option value="all">All Sectors</option>
          {sectorOptions.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
        <select
          value={industryFilter}
          onChange={(e) => setIndustryFilter(e.target.value)}
          aria-label="Filter by industry"
          data-testid="industry-filter"
          className="px-3 py-1.5 text-xs bg-slate-800 border border-slate-700 rounded-lg text-slate-200 focus:outline-none focus:border-cyan-500"
        >
          <option value="all">All Industries</option>
          {industryOptions.map((i) => (
            <option key={i} value={i}>{i}</option>
          ))}
        </select>
        <div className="flex items-center gap-1">
          <span className="text-xs text-slate-600 dark:text-slate-400 mr-1">Market:</span>
          {["all", "US", "UK"].map((m) => (
            <button key={m} className={filterBtnCls(marketFilter === m)} onClick={() => setMarketFilter(m)} aria-label={`Filter market ${m}`}>
              {m === "all" ? "All" : m}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-1">
          <span className="text-xs text-slate-600 dark:text-slate-400 mr-1">Status:</span>
          {[["all", "All"], ["active", "Active"], ["inactive", "Inactive"]].map(([val, label]) => (
            <button key={val} className={filterBtnCls(activeFilter === val)} onClick={() => setActiveFilter(val)} aria-label={`Filter status ${val}`}>
              {label}
            </button>
          ))}
        </div>
        {hasActiveFilters && (
          <Badge
            variant="secondary"
            role="button"
            tabIndex={0}
            onClick={handleClearFilters}
            onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); handleClearFilters(); } }}
            data-testid="clear-filters-badge"
            className="cursor-pointer"
          >
            Clear filters ×
          </Badge>
        )}
      </div>

      {/* Table */}
      {isLoading ? (
        <DataState type="loading" />
      ) : isError ? (
        <DataState type="error" message="Failed to load ticker universe" onRetry={refetch} />
      ) : filtered.length === 0 ? (
        <DataState
          type="empty"
          message={tickers.length === 0 ? "No tickers in the universe yet. Add the first one." : "No tickers match the current filters."}
        />
      ) : (
        <div className="bg-slate-800/50 border border-slate-700 rounded-xl overflow-hidden">
          <table className="w-full text-sm" data-testid="ticker-table">
            <thead>
              <tr className="border-b border-slate-700 text-left">
                <th className="px-4 py-3 text-xs font-medium text-slate-600 dark:text-slate-400">Ticker</th>
                <th className="px-4 py-3 text-xs font-medium text-slate-600 dark:text-slate-400 hidden sm:table-cell">Company Name</th>
                <th className="px-4 py-3 text-xs font-medium text-slate-600 dark:text-slate-400">Market</th>
                <th className="px-4 py-3 text-xs font-medium text-slate-600 dark:text-slate-400">Status</th>
                <th className="px-4 py-3 text-xs font-medium text-slate-600 dark:text-slate-400 text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((row) => {
                const busy = !!pendingAction[row.ticker];
                return (
                  <tr key={row.ticker} className="border-b border-slate-700/50 last:border-0 hover:bg-slate-700/20 transition-colors" data-testid={`ticker-row-${row.ticker}`}>
                    <td className="px-4 py-3 font-mono font-semibold text-slate-100">{displayTicker(row.ticker)}</td>
                    <td className="px-4 py-3 text-slate-300 hidden sm:table-cell" data-testid={`company-name-${row.ticker}`}>{row.company_name || ""}</td>
                    <td className="px-4 py-3"><MarketBadge market={row.market} /></td>
                    <td className="px-4 py-3"><ActiveBadge active={row.active} /></td>
                    <td className="px-4 py-3">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleToggle(row)}
                          disabled={busy}
                          title={row.active ? "Deactivate" : "Reactivate"}
                          aria-label={row.active ? `Deactivate ${row.ticker}` : `Reactivate ${row.ticker}`}
                          data-testid={`toggle-${row.ticker}`}
                          className="text-slate-600 dark:text-slate-400 hover:text-amber-400 disabled:opacity-40 transition-colors"
                        >
                          {busy ? (
                            <Loader2 size={16} className="animate-spin" />
                          ) : row.active ? (
                            <ToggleRight size={16} className="text-emerald-400" />
                          ) : (
                            <ToggleLeft size={16} />
                          )}
                        </button>
                        <button
                          onClick={() => handleDelete(row)}
                          disabled={busy}
                          title={`Delete ${row.ticker}`}
                          aria-label={`Delete ${row.ticker}`}
                          data-testid={`delete-${row.ticker}`}
                          className="text-slate-600 dark:text-slate-400 hover:text-red-400 disabled:opacity-40 transition-colors"
                        >
                          <Trash2 size={16} />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          <div className="px-4 py-2 border-t border-slate-700 text-xs text-slate-600 dark:text-slate-400">
            Showing {filtered.length} of {tickers.length} tickers
          </div>
        </div>
      )}
    </div>
  );
}
