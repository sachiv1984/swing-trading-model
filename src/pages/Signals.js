import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { base44 } from "../api/base44Client";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Button } from "../components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import PageHeader from "../components/ui/PageHeader";
import SignalCard from "../components/signals/SignalCard";
import MarketStatusBar from "../components/signals/MarketStatusBar";
import { Zap, RefreshCw, Filter, TrendingUp, DollarSign, Target } from "lucide-react";
import { toast } from "sonner";
import { cn } from "../lib/utils";

export default function SignalsPage() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [marketFilter, setMarketFilter] = useState("all");
  const [sortBy, setSortBy] = useState("rank");
  const [showDismissed, setShowDismissed] = useState(false);
  const [showAlreadyHeld, setShowAlreadyHeld] = useState(true);

  // Fetch signals from backend
  const { data: signals = [], isLoading } = useQuery({
    queryKey: ["signals"],
    queryFn: () => base44.entities.Signal.list(),
  });

  // Fetch positions to cross-check
  const { data: positions = [] } = useQuery({
    queryKey: ["positions"],
    queryFn: () => base44.entities.Position.filter({ status: "open" }),
  });

  // Fetch portfolio for cash balance
  const { data: portfolios = [] } = useQuery({
    queryKey: ["portfolios"],
    queryFn: () => base44.entities.Portfolio.list(),
  });

  // Generate signals mutation (STEP 5)
  const generateMutation = useMutation({
    mutationFn: () => base44.entities.Signal.generate(),
    onSuccess: (result) => {
      queryClient.invalidateQueries({ queryKey: ["signals"] });
      const data = result?.data || result;
      toast.success(
        `Generated ${data.signals_generated || 0} signals (${data.new_signals || 0} new, ${data.already_held || 0} already held)`
      );
    },
    onError: (error) => {
      toast.error(error.message || "Failed to generate signals");
    },
  });

  // Dismiss signal mutation
  const dismissMutation = useMutation({
    mutationFn: (signalId) => base44.entities.Signal.update(signalId, { status: "dismissed" }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["signals"] });
      toast.success("Signal dismissed");
    },
  });

  // Create position from signal (STEP 6 - includes signal refresh after position creation)
  const createPositionMutation = useMutation({
    mutationFn: async ({ signal, positionData }) => {
      // Create the position
      const position = await base44.entities.Position.create(positionData);
      
      // Update signal status to 'entered' and link position_id
      await base44.entities.Signal.update(signal.id, { 
        status: "entered",
        position_id: position.id 
      });
      
      return position;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["positions"] });
      queryClient.invalidateQueries({ queryKey: ["signals"] });
      queryClient.invalidateQueries({ queryKey: ["portfolios"] });
      toast.success("Position added successfully");
    },
    onError: (error) => {
      toast.error(error.message || "Failed to add position");
    },
  });

  const handleAddPosition = async (signal) => {
    // Get live FX rate for US stocks
    const fxRate = signal.market === "US" ? 1.3611 : 1.0;
    
    const positionData = {
      ticker: signal.ticker,
      market: signal.market,
      entry_date: new Date().toISOString().split("T")[0],
      entry_price: signal.current_price,
      shares: signal.suggested_shares,
      atr_value: signal.atr_value || 0,
      fx_rate: fxRate,
      status: "open"
    };

    await createPositionMutation.mutateAsync({ signal, positionData });
  };

  // Mark entered signals based on open positions
  const signalsWithStatus = signals.map(signal => {
    const hasPosition = positions.some(p => {
      // Remove .L suffix for comparison
      const signalTicker = signal.ticker.replace('.L', '');
      const posTicker = p.ticker.replace('.L', '');
      return signalTicker === posTicker && p.status === "open";
    });
    
    // If position exists but signal status is still 'new', update to 'already_held'
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

  if (!showAlreadyHeld) {
    filteredSignals = filteredSignals.filter(s => s.status !== "already_held");
  }

  // Sort signals
  filteredSignals.sort((a, b) => {
    if (sortBy === "rank") return a.rank - b.rank;
    if (sortBy === "momentum") return b.momentum_percent - a.momentum_percent;
    if (sortBy === "price") return b.current_price - a.current_price;
    return 0;
  });

  // Calculate summary stats
  const totalCapital = filteredSignals
    .filter(s => s.status === "new")
    .reduce((sum, s) => sum + (s.total_cost || 0), 0);
  const avgMomentum = filteredSignals.length > 0
    ? filteredSignals.reduce((sum, s) => sum + s.momentum_percent, 0) / filteredSignals.length
    : 0;
  const usCount = filteredSignals.filter(s => s.market === "US").length;
  const ukCount = filteredSignals.filter(s => s.market === "UK").length;
  const newCount = filteredSignals.filter(s => s.status === "new").length;

  const portfolio = portfolios[0] || { cash_balance: 0 };
  const currentMonth = new Date().toLocaleDateString("en-US", { month: "long", year: "numeric" });

  // Get latest signal date from signals
  const latestSignalDate = signals.length > 0 
    ? new Date(Math.max(...signals.map(s => new Date(s.signal_date)))).toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })
    : "Never";

  // Mock market status (will be replaced by real data from generate endpoint)
  const marketStatus = {
    spy: { isRiskOn: true, price: 598.43 },
    ftse: { isRiskOn: false, price: 8534.20 }
  };

  return (
    <div>
      <PageHeader
        title="Monthly Signals"
        description={`Signals for ${currentMonth} • Last updated: ${latestSignalDate}`}
        actions={
          <Button
            variant="outline"
            size="sm"
            onClick={() => generateMutation.mutate()}
            disabled={generateMutation.isPending}
            className="border-slate-700 text-slate-400 hover:text-white hover:bg-slate-800"
          >
            {generateMutation.isPending ? (
              <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
            ) : (
              <RefreshCw className="w-4 h-4 mr-2" />
            )}
            {generateMutation.isPending ? "Generating..." : "Refresh Signals"}
          </Button>
        }
      />

      <MarketStatusBar
        spyStatus={marketStatus.spy}
        ftseStatus={marketStatus.ftse}
        fxRate={1.3611}
        availableCash={portfolio.cash_balance}
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
              <p className="text-sm text-slate-400">Total Signals</p>
              <p className="text-2xl font-bold text-white">{filteredSignals.length}</p>
              <p className="text-xs text-slate-500">{newCount} new</p>
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
              <p className="text-sm text-slate-400">Total Capital</p>
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
              <p className="text-sm text-slate-400">Avg Momentum</p>
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
              <p className="text-sm text-slate-400">Distribution</p>
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

        <Button
          variant="outline"
          size="sm"
          onClick={() => setShowDismissed(!showDismissed)}
          className={cn(
            "border-slate-700 h-9",
            showDismissed ? "bg-slate-700 text-white" : "text-slate-400 hover:text-white hover:bg-slate-800"
          )}
        >
          {showDismissed ? "Hide" : "Show"} Dismissed
        </Button>

        <Button
          variant="outline"
          size="sm"
          onClick={() => setShowAlreadyHeld(!showAlreadyHeld)}
          className={cn(
            "border-slate-700 h-9",
            showAlreadyHeld ? "bg-slate-700 text-white" : "text-slate-400 hover:text-white hover:bg-slate-800"
          )}
        >
          {showAlreadyHeld ? "Hide" : "Show"} Already Held
        </Button>
      </div>

      {/* Signals Grid */}
      {isLoading || generateMutation.isPending ? (
        <div className="text-center py-12">
          <RefreshCw className="w-8 h-8 text-slate-400 animate-spin mx-auto mb-4" />
          <p className="text-slate-400">
            {generateMutation.isPending ? "Generating signals..." : "Loading signals..."}
          </p>
        </div>
      ) : filteredSignals.length === 0 ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center py-12 px-6 rounded-xl bg-slate-800/50 border border-slate-700/50"
        >
          <Zap className="w-12 h-12 text-slate-600 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">No signals available</h3>
          <p className="text-slate-400 mb-4">
            Click "Refresh Signals" to generate new momentum signals
          </p>
          <Button
            onClick={() => generateMutation.mutate()}
            className="bg-gradient-to-r from-cyan-600 to-violet-600 hover:from-cyan-500 hover:to-violet-500"
          >
            <RefreshCw className="w-4 h-4 mr-2" />
            Generate Signals
          </Button>
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
                onAddPosition={handleAddPosition}
                onDismiss={(id) => dismissMutation.mutate(id)}
                isLoading={createPositionMutation.isPending}
              />
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
