import { useState, useRef } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { base44, apiFetch, api } from "../api/base44Client";
import { motion } from "framer-motion";
import { Button } from "../components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import PageHeader from "../components/ui/PageHeader";
import SignalCard from "../components/signals/SignalCard";
import MarketStatusBar from "../components/signals/MarketStatusBar";
import { Zap, RefreshCw, Filter, TrendingUp, DollarSign, Target } from "lucide-react";
import { toast } from "sonner";
import { cn } from "../lib/utils";
import AiChatWidget from "../components/AiChatWidget";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

const TOP_N_DEFAULT = 5;
const LOOKBACK_DAYS_DEFAULT = 252;

export default function SignalsPage() {
  const queryClient = useQueryClient();
  const [marketFilter, setMarketFilter] = useState("all");
  const [sortBy, setSortBy] = useState("rank");
  const [showDismissed, setShowDismissed] = useState(false);
  const [showRecentOnly, setShowRecentOnly] = useState(true);
  const [addingToWatchlistId, setAddingToWatchlistId] = useState(null);

  // top_n and lookback_days controls with debounce
  const [topNInput, setTopNInput] = useState(String(TOP_N_DEFAULT));
  const [lookbackDaysInput, setLookbackDaysInput] = useState(String(LOOKBACK_DAYS_DEFAULT));
  const [topN, setTopN] = useState(TOP_N_DEFAULT);
  const [lookbackDays, setLookbackDays] = useState(LOOKBACK_DAYS_DEFAULT);
  const topNTimer = useRef(null);
  const lookbackTimer = useRef(null);

  const handleTopNChange = (val) => {
    setTopNInput(val);
    clearTimeout(topNTimer.current);
    topNTimer.current = setTimeout(() => {
      const parsed = parseInt(val, 10);
      if (!isNaN(parsed) && parsed >= 1) {
        setTopN(parsed);
      } else {
        setTopNInput(String(TOP_N_DEFAULT));
        setTopN(TOP_N_DEFAULT);
      }
    }, 500);
  };

  const handleLookbackDaysChange = (val) => {
    setLookbackDaysInput(val);
    clearTimeout(lookbackTimer.current);
    lookbackTimer.current = setTimeout(() => {
      const parsed = parseInt(val, 10);
      if (!isNaN(parsed) && parsed >= 1) {
        setLookbackDays(parsed);
      } else {
        setLookbackDaysInput(String(LOOKBACK_DAYS_DEFAULT));
        setLookbackDays(LOOKBACK_DAYS_DEFAULT);
      }
    }, 500);
  };

  // Fetch signals directly from GET /signals?top_n=N&lookback_days=N
  const { data: signals = [], isLoading } = useQuery({
    queryKey: ["signals", topN, lookbackDays],
    queryFn: async () => {
      const response = await apiFetch(
        `${base44.baseUrl}/signals?top_n=${topN}&lookback_days=${lookbackDays}`
      );
      const result = await response.json();
      return Array.isArray(result) ? result : (result.data || []);
    },
    refetchInterval: 60000 // Auto-refresh every 60 seconds
  });

  const { data: positions = [] } = useQuery({
    queryKey: ["positions"],
    queryFn: () => base44.entities.Position.filter({ status: "open" }),
  });

  // ST-03: Cash balance sourced from GET /cash/summary (authoritative backend source)
  const { data: cashSummary } = useQuery({
    queryKey: ["cashSummary"],
    queryFn: () => api.cash.getSummary(),
  });

  // Fetch live market status
  const { data: marketStatus } = useQuery({
    queryKey: ["marketStatus"],
    queryFn: async () => {
      const response = await apiFetch(`${base44.baseUrl}/market/status`);
      const result = await response.json();
      return result.data;
    },
    refetchInterval: 300000, // Refresh every 5 minutes
    initialData: {
      spy: { price: 0, ma200: 0, is_risk_on: false },
      ftse: { price: 0, ma200: 0, is_risk_on: false },
      fx_rate: 1.3611
    }
  });

  const dismissMutation = useMutation({
    mutationFn: (signalId) => base44.entities.Signal.update(signalId, { status: "dismissed" }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["signals"] });
      toast.success("Signal dismissed");
    },
  });

  const handleAddToWatchlist = async (signal) => {
    setAddingToWatchlistId(signal.id);
    try {
      const res = await apiFetch(`${API_BASE}/watchlist`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ticker: signal.ticker,
          market: signal.market,
          initial_stop_price: signal.initial_stop ?? null,
        }),
      });
      if (res.status === 409) {
        toast.info("Already on your watchlist");
      } else if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Failed to add to watchlist");
      }
    } catch (e) {
      toast.error(e.message || "Failed to add to watchlist");
      setAddingToWatchlistId(null);
      return;
    }
    try {
      await base44.entities.Signal.update(signal.id, { status: "watchlisted" });
      queryClient.invalidateQueries({ queryKey: ["signals"] });
    } catch (e) {
      toast.error("Added to watchlist but failed to update signal status");
    } finally {
      setAddingToWatchlistId(null);
    }
  };

  // Mark signals with correct status based on positions
  const signalsWithStatus = signals.map(signal => {
    const hasPosition = positions.some(p => p.ticker === signal.ticker && p.status === "open");
    if (hasPosition && signal.status === "new") {
      return { ...signal, status: "already_held" };
    }
    return signal;
  });

  // Filter signals
  let filteredSignals = signalsWithStatus;

  if (marketFilter !== "all") {
    filteredSignals = filteredSignals.filter(s => s.market === marketFilter);
  }

  if (!showDismissed) {
    filteredSignals = filteredSignals.filter(s => s.status !== "dismissed");
  }

  // ST-08 (BLG-FE-25): Default to most recent trading day's signals
  const mostRecentDate = signals
    .map(s => s.signal_date)
    .filter(Boolean)
    .sort()
    .at(-1);

  if (showRecentOnly && mostRecentDate) {
    filteredSignals = filteredSignals.filter(s => s.signal_date === mostRecentDate);
  }

  // Sort signals
  filteredSignals.sort((a, b) => {
    if (sortBy === "rank") return a.rank - b.rank;
    if (sortBy === "momentum") return b.momentum_percent - a.momentum_percent;
    if (sortBy === "price") return b.current_price - a.current_price;
    return 0;
  });

  // Enforce top_n limit after all filters and sorting
  filteredSignals = filteredSignals.slice(0, topN);

  // Calculate stats only for NEW signals
  const newSignals = filteredSignals.filter(s => s.status === "new");
  const totalCapital = newSignals.reduce((sum, s) => sum + (s.total_cost || 0), 0);
  const avgMomentum = filteredSignals.length > 0
    ? filteredSignals.reduce((sum, s) => sum + s.momentum_percent, 0) / filteredSignals.length
    : 0;
  const usCount = filteredSignals.filter(s => s.market === "US").length;
  const ukCount = filteredSignals.filter(s => s.market === "UK").length;

  const availableCashBalance = cashSummary?.current_cash ?? 0;
  const currentMonth = new Date().toLocaleDateString("en-US", { month: "long", year: "numeric" });

  // Format date properly
  const latestSignalDate = signals.length > 0 && signals[0].signal_date
    ? new Date(signals[0].signal_date).toLocaleString("en-GB", {
        weekday: "short",
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        hour12: false
      })
    : "No signals yet";

  return (
    <div>
      <PageHeader
        title="Monthly Signals"
        description={
          <div>
            <div>Signals for {currentMonth}</div>
            <div className="text-xs text-slate-600 dark:text-slate-400 mt-1">
              Last updated: {latestSignalDate} • Auto-refreshes every minute
            </div>
          </div>
        }
        actions={
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              queryClient.invalidateQueries({ queryKey: ["signals"] });
              queryClient.invalidateQueries({ queryKey: ["marketStatus"] });
            }}
            className="border-slate-700 text-slate-600 dark:text-slate-400 hover:text-white hover:bg-slate-800"
          >
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </Button>
        }
      />

      {/* Use live market status */}
      <MarketStatusBar
        spyStatus={{
          isRiskOn: marketStatus?.spy?.is_risk_on,
          price: marketStatus?.spy?.price || 0
        }}
        ftseStatus={{
          isRiskOn: marketStatus?.ftse?.is_risk_on,
          price: marketStatus?.ftse?.price || 0
        }}
        fxRate={marketStatus?.fx_rate || 1.3611}
        availableCash={availableCashBalance}
      />

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="p-4 rounded-xl bg-gradient-to-br from-cyan-500/10 to-violet-500/10 border border-cyan-500/30"
        >
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-cyan-500/20 flex items-center justify-center">
              <Zap className="w-5 h-5 text-cyan-400" />
            </div>
            <div>
              <p className="text-sm text-slate-600 dark:text-slate-400">New Signals</p>
              <p className="text-2xl font-bold text-white">{newSignals.length}</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/50"
        >
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-violet-500/20 flex items-center justify-center">
              <DollarSign className="w-5 h-5 text-violet-400" />
            </div>
            <div>
              <p className="text-sm text-slate-600 dark:text-slate-400">Total Capital</p>
              <p className="text-2xl font-bold text-white">£{totalCapital.toLocaleString()}</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/50"
        >
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-500/20 flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-emerald-400" />
            </div>
            <div>
              <p className="text-sm text-slate-600 dark:text-slate-400">Avg Momentum</p>
              <p className="text-2xl font-bold text-white">{avgMomentum.toFixed(1)}%</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/50"
        >
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-fuchsia-500/20 flex items-center justify-center">
              <Target className="w-5 h-5 text-fuchsia-400" />
            </div>
            <div>
              <p className="text-sm text-slate-600 dark:text-slate-400">Distribution</p>
              <p className="text-2xl font-bold text-white">{usCount} US, {ukCount} UK</p>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap items-center gap-4 mb-6">
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-slate-400" />
          <Select value={marketFilter} onValueChange={setMarketFilter}>
            <SelectTrigger className="w-32 bg-slate-800/50 border-slate-700 text-white h-9">
              <SelectValue />
            </SelectTrigger>
            <SelectContent className="bg-slate-800 border-slate-700">
              <SelectItem value="all">All Markets</SelectItem>
              <SelectItem value="US">US Only</SelectItem>
              <SelectItem value="UK">UK Only</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <Select value={sortBy} onValueChange={setSortBy}>
          <SelectTrigger className="w-40 bg-slate-800/50 border-slate-700 text-white h-9">
            <SelectValue />
          </SelectTrigger>
          <SelectContent className="bg-slate-800 border-slate-700">
            <SelectItem value="rank">Sort by Rank</SelectItem>
            <SelectItem value="momentum">Sort by Momentum</SelectItem>
            <SelectItem value="price">Sort by Price</SelectItem>
          </SelectContent>
        </Select>

        <div className="flex items-center gap-2">
          <label className="text-sm text-slate-600 dark:text-slate-400 whitespace-nowrap">Top N</label>
          <input
            type="number"
            min="1"
            value={topNInput}
            onChange={(e) => handleTopNChange(e.target.value)}
            className="w-20 h-9 bg-slate-800/50 border border-slate-700 rounded-md text-white text-sm px-2 focus:outline-none focus:border-cyan-500"
          />
        </div>

        <div className="flex items-center gap-2">
          <label className="text-sm text-slate-600 dark:text-slate-400 whitespace-nowrap">Lookback Days</label>
          <input
            type="number"
            min="1"
            value={lookbackDaysInput}
            onChange={(e) => handleLookbackDaysChange(e.target.value)}
            className="w-24 h-9 bg-slate-800/50 border border-slate-700 rounded-md text-white text-sm px-2 focus:outline-none focus:border-cyan-500"
          />
        </div>

        <Button
          variant="outline"
          size="sm"
          onClick={() => setShowDismissed(!showDismissed)}
          className={cn(
            "border-slate-700 h-9",
            showDismissed ? "bg-slate-700 text-white" : "text-slate-600 dark:text-slate-400 hover:text-white hover:bg-slate-800"
          )}
        >
          {showDismissed ? "Hide" : "Show"} Dismissed
        </Button>

        <Button
          variant="outline"
          size="sm"
          onClick={() => setShowRecentOnly(!showRecentOnly)}
          className={cn(
            "border-slate-700 h-9",
            showRecentOnly ? "bg-slate-700 text-white" : "text-slate-600 dark:text-slate-400 hover:text-white hover:bg-slate-800"
          )}
        >
          {showRecentOnly ? "Most Recent Day" : "All Days"}
        </Button>
      </div>

      {/* Signals Grid */}
      {isLoading ? (
        <div className="text-center py-12">
          <RefreshCw className="w-8 h-8 text-slate-400 animate-spin mx-auto mb-4" />
          <p className="text-slate-600 dark:text-slate-400">Loading signals...</p>
        </div>
      ) : filteredSignals.length === 0 ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center py-12 px-6 rounded-xl bg-slate-800/50 border border-slate-700/50"
        >
          <Zap className="w-12 h-12 text-slate-600 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">No signals found for the selected parameters.</h3>
          <p className="text-slate-600 dark:text-slate-400 mb-4">
            Signals are generated daily at 4 PM UTC weekdays
          </p>
          <p className="text-sm text-slate-600 dark:text-slate-400">Last update: {latestSignalDate}</p>
        </motion.div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {filteredSignals.map((signal, index) => (
            <motion.div
              key={signal.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
            >
              <SignalCard
                signal={signal}
                onAddToWatchlist={handleAddToWatchlist}
                onDismiss={(id) => dismissMutation.mutate(id)}
                isAddingToWatchlist={addingToWatchlistId === signal.id}
              />
            </motion.div>
          ))}
        </div>
      )}

      {/* ST-09 (EPIC-02, v6.2): AI Trade Advisor — fixed floating widget, display-only advisory */}
      <AiChatWidget />
    </div>
  );
}
