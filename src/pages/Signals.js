import React, { useState, useMemo } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Signal, Position } from '../api/base44Client';
import { toast } from 'react-hot-toast';
import { TrendingUp, DollarSign, Activity, Globe } from 'lucide-react';

const Signals = () => {
  const queryClient = useQueryClient();
  
  // Filters
  const [marketFilter, setMarketFilter] = useState('all'); // all, US, UK
  const [sortBy, setSortBy] = useState('rank'); // rank, momentum, price
  const [showDismissed, setShowDismissed] = useState(false);
  const [showAlreadyHeld, setShowAlreadyHeld] = useState(false);

  // Fetch signals
  const { data: signals = [], isLoading } = useQuery({
    queryKey: ['signals'],
    queryFn: () => Signal.list(),
    refetchInterval: 60000 // Refresh every minute
  });

  // Create position mutation
  const createPositionMutation = useMutation({
    mutationFn: async (signal) => {
      const positionData = {
        ticker: signal.ticker,
        market: signal.market,
        entry_date: new Date().toISOString().split('T')[0],
        shares: signal.suggested_shares,
        entry_price: signal.current_price,
        atr_value: signal.atr_value,
        fx_rate: signal.market === 'US' ? signal.fx_rate : null
      };
      
      const result = await Position.create(positionData);
      
      // Update signal status to 'entered'
      await Signal.update(signal.id, { 
        status: 'entered',
        position_id: result.data.position_id 
      });
      
      return result;
    },
    onSuccess: () => {
      toast.success('✓ Position created successfully');
      queryClient.invalidateQueries(['signals']);
      queryClient.invalidateQueries(['positions']);
      queryClient.invalidateQueries(['portfolio']);
    },
    onError: (error) => {
      toast.error(`Failed to create position: ${error.message}`);
    }
  });

  // Dismiss signal mutation
  const dismissMutation = useMutation({
    mutationFn: (signalId) => Signal.update(signalId, { status: 'dismissed' }),
    onSuccess: () => {
      toast.success('Signal dismissed');
      queryClient.invalidateQueries(['signals']);
    }
  });

  // Filter and sort signals
  const filteredSignals = useMemo(() => {
    let filtered = signals.filter(s => {
      // Market filter
      if (marketFilter !== 'all' && s.market !== marketFilter) return false;
      
      // Show dismissed filter
      if (!showDismissed && s.status === 'dismissed') return false;
      
      // Show already held filter
      if (!showAlreadyHeld && s.status === 'already_held') return false;
      
      return true;
    });

    // Sort
    filtered.sort((a, b) => {
      if (sortBy === 'rank') return a.rank - b.rank;
      if (sortBy === 'momentum') return b.momentum_percent - a.momentum_percent;
      if (sortBy === 'price') return b.current_price - a.current_price;
      return 0;
    });

    return filtered;
  }, [signals, marketFilter, sortBy, showDismissed, showAlreadyHeld]);

  // Calculate summary stats
  const stats = useMemo(() => {
    const newSignals = signals.filter(s => s.status === 'new');
    const totalCapital = newSignals.reduce((sum, s) => sum + (s.allocation_gbp || 0), 0);
    const avgMomentum = newSignals.length > 0 
      ? newSignals.reduce((sum, s) => sum + s.momentum_percent, 0) / newSignals.length 
      : 0;
    const usSplit = newSignals.filter(s => s.market === 'US').length;
    const ukSplit = newSignals.filter(s => s.market === 'UK').length;
    
    return {
      total: newSignals.length,
      totalCapital,
      avgMomentum,
      usSplit,
      ukSplit
    };
  }, [signals]);

  // Get latest signal date
  const latestSignalDate = signals.length > 0 
    ? new Date(signals[0].signal_date).toLocaleDateString('en-GB', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    : 'No signals yet';

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
            Momentum Signals
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            Last updated: {latestSignalDate}
          </p>
          <p className="text-xs text-slate-400 dark:text-slate-500">
            Signals auto-generate daily at 4 PM UTC weekdays
          </p>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard
          icon={<TrendingUp className="w-5 h-5" />}
          label="New Signals"
          value={stats.total}
          color="blue"
        />
        <StatCard
          icon={<DollarSign className="w-5 h-5" />}
          label="Total Capital"
          value={`£${stats.totalCapital.toLocaleString()}`}
          color="green"
        />
        <StatCard
          icon={<Activity className="w-5 h-5" />}
          label="Avg Momentum"
          value={`${stats.avgMomentum.toFixed(1)}%`}
          color="purple"
        />
        <StatCard
          icon={<Globe className="w-5 h-5" />}
          label="US / UK Split"
          value={`${stats.usSplit} / ${stats.ukSplit}`}
          color="orange"
        />
      </div>

      {/* Filters */}
      <div className="flex flex-wrap items-center gap-4 bg-white dark:bg-slate-800 p-4 rounded-lg border border-slate-200 dark:border-slate-700">
        {/* Market Filter */}
        <div className="flex items-center gap-2">
          <label className="text-sm font-medium text-slate-700 dark:text-slate-300">
            Market:
          </label>
          <select
            value={marketFilter}
            onChange={(e) => setMarketFilter(e.target.value)}
            className="px-3 py-1.5 text-sm border border-slate-300 dark:border-slate-600 rounded-md bg-white dark:bg-slate-700 text-slate-900 dark:text-white"
          >
            <option value="all">All</option>
            <option value="US">US</option>
            <option value="UK">UK</option>
          </select>
        </div>

        {/* Sort */}
        <div className="flex items-center gap-2">
          <label className="text-sm font-medium text-slate-700 dark:text-slate-300">
            Sort by:
          </label>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-3 py-1.5 text-sm border border-slate-300 dark:border-slate-600 rounded-md bg-white dark:bg-slate-700 text-slate-900 dark:text-white"
          >
            <option value="rank">Rank</option>
            <option value="momentum">Momentum</option>
            <option value="price">Price</option>
          </select>
        </div>

        {/* Show Dismissed */}
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={showDismissed}
            onChange={(e) => setShowDismissed(e.target.checked)}
            className="w-4 h-4 text-blue-600 border-slate-300 rounded focus:ring-blue-500"
          />
          <span className="text-sm text-slate-700 dark:text-slate-300">
            Show dismissed
          </span>
        </label>

        {/* Show Already Held */}
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={showAlreadyHeld}
            onChange={(e) => setShowAlreadyHeld(e.target.checked)}
            className="w-4 h-4 text-blue-600 border-slate-300 rounded focus:ring-blue-500"
          />
          <span className="text-sm text-slate-700 dark:text-slate-300">
            Show already held
          </span>
        </label>

        <div className="ml-auto text-sm text-slate-500 dark:text-slate-400">
          {filteredSignals.length} signal{filteredSignals.length !== 1 ? 's' : ''}
        </div>
      </div>

      {/* Signals Grid */}
      {filteredSignals.length === 0 ? (
        <div className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 p-12 text-center">
          <p className="text-slate-500 dark:text-slate-400">
            No signals match your filters
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredSignals.map((signal) => (
            <SignalCard
              key={signal.id}
              signal={signal}
              onAddPosition={() => createPositionMutation.mutate(signal)}
              onDismiss={() => dismissMutation.mutate(signal.id)}
              isCreating={createPositionMutation.isPending}
            />
          ))}
        </div>
      )}
    </div>
  );
};

// Stat Card Component
const StatCard = ({ icon, label, value, color }) => {
  const colorClasses = {
    blue: 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400',
    green: 'bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400',
    purple: 'bg-purple-50 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400',
    orange: 'bg-orange-50 dark:bg-orange-900/20 text-orange-600 dark:text-orange-400'
  };

  return (
    <div className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 p-4">
      <div className="flex items-center gap-3">
        <div className={`p-2 rounded-lg ${colorClasses[color]}`}>
          {icon}
        </div>
        <div>
          <p className="text-xs text-slate-500 dark:text-slate-400">{label}</p>
          <p className="text-lg font-semibold text-slate-900 dark:text-white">
            {value}
          </p>
        </div>
      </div>
    </div>
  );
};

// Signal Card Component
const SignalCard = ({ signal, onAddPosition, onDismiss, isCreating }) => {
  const getStatusBadge = () => {
  // Priority order: entered > dismissed > already_held > new
  if (signal.status === 'entered') {
    return (
      <span className="px-2 py-1 text-xs font-medium bg-green-100 dark:bg-green-900/20 text-green-600 dark:text-green-400 rounded">
        ✓ Position Entered
      </span>
    );
  }
  
  if (signal.status === 'dismissed') {
    return (
      <span className="px-2 py-1 text-xs font-medium bg-red-100 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded">
        ✗ Dismissed
      </span>
    );
  }
  
  if (signal.status === 'already_held') {
    return (
      <span className="px-2 py-1 text-xs font-medium bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 rounded">
        ◉ Already Held
      </span>
    );
  }
  
  // Default: new signal
  return (
    <span className="px-2 py-1 text-xs font-medium bg-blue-100 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded">
      ★ New Signal
    </span>
  );
};
  
  const currencySymbol = signal.market === 'US' ? '$' : '£';
  const isActionable = signal.status === 'new';

  return (
    <div className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 p-4 hover:border-blue-400 dark:hover:border-blue-500 transition-colors">
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-lg font-bold text-slate-900 dark:text-white">
              {signal.ticker.replace('.L', '')}
            </h3>
            <span className="px-1.5 py-0.5 text-xs font-medium bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 rounded">
              #{signal.rank}
            </span>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            {signal.market === 'US' ? '🇺🇸 US Stock' : '🇬🇧 UK Stock'}
          </p>
        </div>
        {getStatusBadge()}
      </div>

      {/* Metrics */}
      <div className="space-y-2 mb-4">
        <div className="flex justify-between text-sm">
          <span className="text-slate-600 dark:text-slate-400">Momentum</span>
          <span className="font-semibold text-green-600 dark:text-green-400">
            +{signal.momentum_percent.toFixed(1)}%
          </span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-slate-600 dark:text-slate-400">Price</span>
          <span className="font-semibold text-slate-900 dark:text-white">
            {currencySymbol}{signal.current_price.toFixed(2)}
          </span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-slate-600 dark:text-slate-400">Stop</span>
          <span className="font-semibold text-red-600 dark:text-red-400">
            {currencySymbol}{signal.initial_stop.toFixed(2)}
          </span>
        </div>
        {isActionable && (
          <>
            <div className="flex justify-between text-sm">
              <span className="text-slate-600 dark:text-slate-400">Shares</span>
              <span className="font-semibold text-slate-900 dark:text-white">
                {signal.suggested_shares}
              </span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-600 dark:text-slate-400">Capital</span>
              <span className="font-semibold text-slate-900 dark:text-white">
                £{signal.allocation_gbp.toFixed(2)}
              </span>
            </div>
          </>
        )}
      </div>

      {/* Actions */}
      {isActionable && (
        <div className="flex gap-2">
          <button
            onClick={onAddPosition}
            disabled={isCreating}
            className="flex-1 px-3 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 rounded-md transition-colors"
          >
            {isCreating ? 'Creating...' : 'Add Position'}
          </button>
          <button
            onClick={onDismiss}
            className="px-3 py-2 text-sm font-medium text-slate-700 dark:text-slate-300 bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 dark:hover:bg-slate-600 rounded-md transition-colors"
          >
            Dismiss
          </button>
        </div>
      )}
    </div>
  );
};

export default Signals;
