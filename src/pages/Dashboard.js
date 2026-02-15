import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import CashManagementModal from "../components/cash/CashManagementModal";
import { base44 } from "../api/base44Client";
import { Loader2, Settings2, Plus, RotateCcw, Check } from "lucide-react";
import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd";
import { Button } from "../components/ui/button";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "../lib/utils";

import PageHeader from "../components/ui/PageHeader";
import DashboardWidget from "../components/dashboard/DashboardWidget";
import WidgetLibrary from "../components/dashboard/WidgetLibrary";
import MonitorModal from "../components/monitor/MonitorModal";
import { useDashboardLayout } from "../components/dashboard/useDashboardLayout";

// Widget components
import { 
  PortfolioValueWidget, 
  CashBalanceWidget, 
  OpenPositionsWidget, 
  TotalPnLWidget,
  WinRateWidget,
  AvgHoldTimeWidget
} from "../components/dashboard/widgets/StatsWidgets";
import CurrentDrawdownWidget from "../components/dashboard/widgets/CurrentDrawdownWidget";
import PortfolioChart from "../components/charts/PortfolioChart";
import AllocationChart from "../components/charts/AllocationChart";
import PnLBarChart from "../components/charts/PnLBarChart";
import WinRateChart from "../components/charts/WinRateChart";
import MarketRegimeCard from "../components/dashboard/MarketRegimeCard";
import QuickActions from "../components/dashboard/QuickActions";
import RecentTradesWidget from "../components/dashboard/widgets/RecentTradesWidget";

export default function Dashboard() {
  const [monitorOpen, setMonitorOpen] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [libraryOpen, setLibraryOpen] = useState(false);
  const [cashModalOpen, setCashModalOpen] = useState(false);
  
  const { widgets, addWidget, removeWidget, reorderWidgets, resetToDefault, isLoaded } = useDashboardLayout();

  // ✅ Get API URL from environment variable (production-safe)
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const { data: portfolios, isLoading: loadingPortfolio } = useQuery({
    queryKey: ["portfolios"],
    queryFn: () => base44.entities.Portfolio.list(),
  });

  const { data: positions, isLoading: loadingPositions } = useQuery({
    queryKey: ["positions"],
    queryFn: () => base44.entities.Position.filter({ status: "open" }),
  });

  const { data: allPositions } = useQuery({
    queryKey: ["allPositions"],
    queryFn: () => base44.entities.Position.list(),
  });

  const { data: marketRegimes, isLoading: loadingRegimes } = useQuery({
    queryKey: ["marketRegimes"],
    queryFn: () => base44.entities.MarketRegime.list(),
  });

  const { data: cashTransactions } = useQuery({
    queryKey: ["cashTransactions"],
    queryFn: () => base44.entities.CashTransaction.list("-date"),
  });

  // ✅ CRITICAL: Fetch portfolio history for accurate peak calculation
  const { data: portfolioHistory, isLoading: loadingHistory } = useQuery({
    queryKey: ["portfolioHistory"],
    queryFn: async () => {
      try {
        const response = await fetch(`${API_URL}/portfolio/history?days=365`);
        if (!response.ok) {
          console.warn('Portfolio history not available:', response.status);
          return [];
        }
        const result = await response.json();
        return result.data || [];
      } catch (error) {
        console.error('Failed to load portfolio history:', error);
        return [];
      }
    },
    initialData: [],
    // Refetch every 5 minutes to stay current
    refetchInterval: 5 * 60 * 1000,
    // Stale after 1 minute
    staleTime: 60 * 1000,
  });

  const portfolio = portfolios?.[0];
  const openPositions = positions || [];
  const closedPositions = allPositions?.filter(p => p.status === "closed") || [];
  
  // ✅ Use values directly from portfolio endpoint (already calculated correctly)
  const totalPositionsValue = portfolio?.open_positions_value || openPositions.reduce((sum, p) => {
    return sum + (p.current_price || p.entry_price) * p.shares;
  }, 0);

  const totalPnL = portfolio?.total_pnl || 0;  // ✅ Use portfolio's pre-calculated P&L

  const isLoading = loadingPortfolio || loadingPositions || loadingRegimes || !isLoaded;

  const handleExitPositions = async (positionsToExit) => {
    for (const position of positionsToExit) {
      await base44.entities.Position.update(position.id, {
        status: "closed",
        exit_date: new Date().toISOString().split("T")[0],
        exit_price: position.current_price,
        exit_reason: "market_regime",
        pnl: (position.current_price - position.entry_price) * position.shares,
        pnl_percent: ((position.current_price - position.entry_price) / position.entry_price) * 100
      });
    }
    setMonitorOpen(false);
  };

  const handleDragEnd = (result) => {
    if (!result.destination) return;
    
    const items = Array.from(widgets);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);
    
    reorderWidgets(items.map(w => w.id));
  };

  const renderWidget = (widgetId, dragHandleProps) => {
    // ✅ PERFECT: Calculate drawdown metrics with comprehensive error handling
    const currentEquity = (portfolio?.cash_balance || 0) + totalPositionsValue;
    
    /**
     * Calculate accurate drawdown metrics from portfolio history
     * @returns {Object} Drawdown metrics with peak, date, and max DD
     */
    const calculateDrawdownMetrics = () => {
      // Method 1: Portfolio History (BEST - Most Accurate)
      if (portfolioHistory && portfolioHistory.length > 0) {
        try {
          // ✅ Step 1: Find all-time peak from historical data
          const historicalValues = portfolioHistory.map(h => {
            const value = parseFloat(h.total_value);
            // Validate data integrity
            if (!value || isNaN(value) || value < 0) {
              console.warn('Invalid portfolio value in history:', h);
              return 0;
            }
            return value;
          });
          
          // Include current equity in peak calculation (handles new peaks)
          const allValues = [...historicalValues, currentEquity];
          const historicalPeak = Math.max(...allValues);
          
          // ✅ Step 2: Find when peak occurred
          let peakSnapshot = portfolioHistory.find(h => 
            Math.abs(parseFloat(h.total_value) - historicalPeak) < 0.01
          );
          
          // If current equity is peak, use today's date
          let peakDate;
          if (Math.abs(currentEquity - historicalPeak) < 0.01) {
            peakDate = new Date().toISOString().split('T')[0];
          } else {
            peakDate = peakSnapshot?.snapshot_date || new Date().toISOString().split('T')[0];
          }
          
          // ✅ Step 3: Calculate max historical drawdown
          // This is the largest peak-to-trough decline ever experienced
          let maxDD = 0;
          let runningPeak = 0;
          
          // Sort by date ascending for chronological peak tracking
          const sortedHistory = [...portfolioHistory]
            .filter(h => h.snapshot_date && h.total_value) // Filter invalid entries
            .sort((a, b) => new Date(a.snapshot_date) - new Date(b.snapshot_date));
          
          // Track running peak and calculate drawdowns
          sortedHistory.forEach(snapshot => {
            const value = parseFloat(snapshot.total_value);
            
            // Update running peak
            if (value > runningPeak) {
              runningPeak = value;
            }
            
            // Calculate drawdown from peak
            if (runningPeak > 0) {
              const drawdown = ((value - runningPeak) / runningPeak) * 100;
              
              // Track maximum drawdown (most negative)
              if (drawdown < maxDD) {
                maxDD = drawdown;
              }
            }
          });
          
          // ✅ Step 4: Include current drawdown in max calculation
          if (historicalPeak > 0) {
            const currentDD = ((currentEquity - historicalPeak) / historicalPeak) * 100;
            if (currentDD < maxDD) {
              maxDD = currentDD;
            }
          }
          
          // ✅ Validation: Ensure values are sensible
          if (historicalPeak <= 0) {
            console.warn('Invalid historical peak:', historicalPeak);
            return fallbackCalculation();
          }
          
          return {
            currentEquity,
            peakEquity: historicalPeak,
            peakDate,
            maxHistoricalDrawdown: maxDD,
            dataSource: 'portfolio_history',
            dataPoints: sortedHistory.length
          };
          
        } catch (error) {
          console.error('Error calculating drawdown from history:', error);
          return fallbackCalculation();
        }
      }
      
      // Method 2: Fallback Estimation (GOOD - When No History Available)
      return fallbackCalculation();
    };
    
    /**
     * Fallback calculation when portfolio history unavailable
     * Estimates peak from closed trades and current state
     */
    const fallbackCalculation = () => {
      try {
        // ✅ Calculate realized P&L from closed positions
        const realizedPnL = closedPositions.reduce((sum, p) => {
          const pnl = p.pnl || 0;
          // Validate data
          if (isNaN(pnl)) {
            console.warn('Invalid P&L in closed position:', p);
            return sum;
          }
          return sum + pnl;
        }, 0);
        
        // ✅ Calculate unrealized P&L from open positions
        const unrealizedPnL = openPositions.reduce((sum, p) => {
          const pnl = p.pnl || 0;
          if (isNaN(pnl)) {
            console.warn('Invalid P&L in open position:', p);
            return sum;
          }
          return sum + pnl;
        }, 0);
        
        // ✅ Estimate peak: If we've taken losses, peak was higher
        let estimatedPeak;
        if (realizedPnL < 0) {
          // Add back realized losses to estimate peak
          estimatedPeak = currentEquity - realizedPnL;
        } else {
          // Peak is at least current equity
          estimatedPeak = currentEquity;
        }
        
        // Ensure peak is at least current (handles new peak case)
        estimatedPeak = Math.max(estimatedPeak, currentEquity);
        
        // ✅ Estimate max drawdown from worst single trade
        let maxDD = 0;
        if (closedPositions.length > 0) {
          const worstTrade = Math.min(
            ...closedPositions.map(p => p.pnl_percent || 0)
          );
          maxDD = Math.min(worstTrade, 0);
        }
        
        // ✅ Include current drawdown if worse
        if (estimatedPeak > 0) {
          const currentDD = ((currentEquity - estimatedPeak) / estimatedPeak) * 100;
          maxDD = Math.min(maxDD, currentDD);
        }
        
        return {
          currentEquity,
          peakEquity: estimatedPeak,
          peakDate: new Date().toISOString().split('T')[0],
          maxHistoricalDrawdown: maxDD,
          dataSource: 'estimated',
          dataPoints: closedPositions.length
        };
        
      } catch (error) {
        console.error('Error in fallback calculation:', error);
        // Ultimate fallback: safe defaults
        return {
          currentEquity: currentEquity || 0,
          peakEquity: currentEquity || 0,
          peakDate: new Date().toISOString().split('T')[0],
          maxHistoricalDrawdown: 0,
          dataSource: 'default',
          dataPoints: 0
        };
      }
    };

    const drawdownMetrics = calculateDrawdownMetrics();
    
    // ✅ Log for debugging (can be removed in production)
    if (process.env.NODE_ENV === 'development') {
      console.debug('Drawdown Metrics:', {
        source: drawdownMetrics.dataSource,
        points: drawdownMetrics.dataPoints,
        current: drawdownMetrics.currentEquity.toFixed(2),
        peak: drawdownMetrics.peakEquity.toFixed(2),
        maxDD: drawdownMetrics.maxHistoricalDrawdown.toFixed(2)
      });
    }

    const widgetProps = {
      portfolio,
      totalPositionsValue,
      totalPnL,
      openPositions,
      closedPositions,
      allPositions,
      marketRegimes,
      positionsCount: openPositions.length,
      onRunMonitor: () => setMonitorOpen(true)
    };

    switch (widgetId) {
      case "portfolio_value":
        return <PortfolioValueWidget {...widgetProps} />;
      case "cash_balance":
        return <CashBalanceWidget {...widgetProps} onManageCash={() => setCashModalOpen(true)} />;
      case "open_positions":
        return <OpenPositionsWidget {...widgetProps} />;
      case "total_pnl":
        return <TotalPnLWidget {...widgetProps} />;
      case "win_rate":
        return <WinRateWidget {...widgetProps} />;
      case "avg_hold_time":
        return <AvgHoldTimeWidget {...widgetProps} />;
      case "current_drawdown":
        return <CurrentDrawdownWidget 
          currentEquity={drawdownMetrics.currentEquity}
          peakEquity={drawdownMetrics.peakEquity}
          peakDate={drawdownMetrics.peakDate}
          maxHistoricalDrawdown={drawdownMetrics.maxHistoricalDrawdown}
          dataSource={drawdownMetrics.dataSource}
        />;
      case "portfolio_chart":
        return <PortfolioChart />;
      case "allocation_chart":
        return <AllocationChart positions={openPositions} />;
      case "pnl_chart":
        return <PnLBarChart trades={closedPositions} />;
      case "win_rate_chart":
        return <WinRateChart trades={closedPositions} />;
      case "market_regime_us":
        return (
          <MarketRegimeCard
            market="US"
            status={marketRegimes?.find(r => r.market === "US")?.status || "risk_on"}
            index="SPY"
          />
        );
      case "market_regime_uk":
        return (
          <MarketRegimeCard
            market="UK"
            status={marketRegimes?.find(r => r.market === "UK")?.status || "risk_on"}
            index="FTSE 100"
          />
        );
      case "quick_actions":
        return <QuickActions onRunMonitor={() => setMonitorOpen(true)} />;
      case "recent_trades":
        return <RecentTradesWidget positions={allPositions} />;
      default:
        return null;
    }
  };

  const getWidgetSize = (widgetId) => {
    const smallWidgets = ["portfolio_value", "cash_balance", "open_positions", "total_pnl", "win_rate", "avg_hold_time", "current_drawdown"];
    const mediumWidgets = ["allocation_chart", "market_regime_us", "market_regime_uk", "win_rate_chart"];
    const largeWidgets = ["portfolio_chart", "pnl_chart", "quick_actions", "recent_trades"];
    
    if (smallWidgets.includes(widgetId)) return "small";
    if (mediumWidgets.includes(widgetId)) return "medium";
    if (largeWidgets.includes(widgetId)) return "large";
    return "medium";
  };

  // Group widgets by size for layout
  const smallWidgets = widgets.filter(w => getWidgetSize(w.id) === "small");
  const otherWidgets = widgets.filter(w => getWidgetSize(w.id) !== "small");

  return (
    <div className="space-y-6">
      <PageHeader
        title="Dashboard"
        description="Portfolio overview and quick actions"
        actions={
          <div className="flex items-center gap-2">
            {isEditing && (
              <>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setLibraryOpen(true)}
                  className="bg-slate-800/50 border-slate-700 text-slate-300 hover:bg-slate-700 hover:text-white"
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Add Widget
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={resetToDefault}
                  className="bg-slate-800/50 border-slate-700 text-slate-300 hover:bg-slate-700 hover:text-white"
                >
                  <RotateCcw className="w-4 h-4 mr-2" />
                  Reset
                </Button>
              </>
            )}
            <Button
              variant={isEditing ? "default" : "outline"}
              size="sm"
              onClick={() => setIsEditing(!isEditing)}
              className={cn(
                isEditing 
                  ? "bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-600 hover:to-violet-600 text-white"
                  : "bg-slate-800/50 border-slate-700 text-slate-300 hover:bg-slate-700 hover:text-white"
              )}
            >
              {isEditing ? (
                <>
                  <Check className="w-4 h-4 mr-2" />
                  Done
                </>
              ) : (
                <>
                  <Settings2 className="w-4 h-4 mr-2" />
                  Customize
                </>
              )}
            </Button>
          </div>
        }
      />

      {isLoading ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="w-8 h-8 animate-spin text-slate-500" />
        </div>
      ) : (
        <DragDropContext onDragEnd={handleDragEnd}>
          <Droppable droppableId="dashboard" direction="vertical">
            {(provided) => (
              <div
                ref={provided.innerRef}
                {...provided.droppableProps}
                className="space-y-6"
              >
                {/* Small Widgets Grid */}
                {smallWidgets.length > 0 && (
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    {smallWidgets.map((widget, index) => (
                      <Draggable 
                        key={widget.id} 
                        draggableId={widget.id} 
                        index={widgets.findIndex(w => w.id === widget.id)}
                        isDragDisabled={!isEditing}
                      >
                        {(provided, snapshot) => (
                          <div
                            ref={provided.innerRef}
                            {...provided.draggableProps}
                            className={cn(snapshot.isDragging && "z-50")}
                          >
                            <DashboardWidget
                              id={widget.id}
                              isEditing={isEditing}
                              onRemove={removeWidget}
                              dragHandleProps={provided.dragHandleProps}
                            >
                              {renderWidget(widget.id)}
                            </DashboardWidget>
                          </div>
                        )}
                      </Draggable>
                    ))}
                  </div>
                )}

                {/* Other Widgets */}
                {otherWidgets.map((widget, index) => {
                  const size = getWidgetSize(widget.id);
                  
                  return (
                    <Draggable 
                      key={widget.id} 
                      draggableId={widget.id} 
                      index={widgets.findIndex(w => w.id === widget.id)}
                      isDragDisabled={!isEditing}
                    >
                      {(provided, snapshot) => (
                        <div
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          className={cn(
                            snapshot.isDragging && "z-50",
                            size === "large" && "col-span-full",
                            size === "medium" && "lg:col-span-1"
                          )}
                        >
                          <DashboardWidget
                            id={widget.id}
                            isEditing={isEditing}
                            onRemove={removeWidget}
                            size={size}
                            dragHandleProps={provided.dragHandleProps}
                          >
                            {renderWidget(widget.id)}
                          </DashboardWidget>
                        </div>
                      )}
                    </Draggable>
                  );
                })}
                {provided.placeholder}
              </div>
            )}
          </Droppable>
        </DragDropContext>
      )}

      <WidgetLibrary
        open={libraryOpen}
        onClose={() => setLibraryOpen(false)}
        onAddWidget={(widget) => {
          addWidget(widget);
          setLibraryOpen(false);
        }}
        activeWidgets={widgets}
      />

      <MonitorModal
        open={monitorOpen}
        onClose={() => setMonitorOpen(false)}
        positions={openPositions}
        marketRegimes={marketRegimes}
        isLoading={loadingPositions}
        onConfirmExits={handleExitPositions}
      />

      <CashManagementModal
        open={cashModalOpen}
        onClose={() => setCashModalOpen(false)}
        portfolio={portfolio}
        transactions={cashTransactions}
      />
    </div>
  );
}
