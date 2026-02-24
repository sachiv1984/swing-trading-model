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

  // B1 / F1 — BLG-FEAT-01: Analytics metrics for drawdown widget secondary fields.
  // Provides: advanced_metrics.days_underwater, advanced_metrics.max_drawdown.percent
  // Spec: dashboard.md v1.1; decisions D7, D8
  // This query is non-blocking — widget degrades gracefully if it fails.
  const { data: analyticsMetrics } = useQuery({
    queryKey: ["analyticsMetrics"],
    queryFn: async () => {
      try {
        const response = await fetch(`${API_URL}/analytics/metrics`);
        if (!response.ok) {
          console.warn('Analytics metrics not available:', response.status);
          return null;
        }
        const result = await response.json();
        return result.data || null;
      } catch (error) {
        console.error('Failed to load analytics metrics:', error);
        return null;
      }
    },
    // Stale after 5 minutes — this data changes slowly
    staleTime: 5 * 60 * 1000,
    // Do not throw on error — widget handles null gracefully
    retry: false,
  });

  const portfolio = portfolios?.[0];
  const openPositions = positions || [];
  const closedPositions = allPositions?.filter(p => p.status === "closed") || [];
  
  const totalPositionsValue = portfolio?.open_positions_value || openPositions.reduce((sum, p) => {
    return sum + (p.current_price || p.entry_price) * p.shares;
  }, 0);

  const totalPnL = portfolio?.total_pnl || 0;

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

  const renderWidget = (widgetId) => {
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

      // B1 / F1 — BLG-FEAT-01: Current Drawdown Widget
      // Data sourced directly from API fields per decisions D1, D7, D8, D10.
      // No client-side peak/drawdown calculation. No fallback logic.
      // - currentDrawdownPercent: GET /portfolio → data.current_drawdown_percent
      // - peakPortfolioValue:     GET /portfolio → data.peak_portfolio_value
      // - daysUnderwater:         GET /analytics/metrics → advanced_metrics.days_underwater
      // - maxDrawdownPercent:     GET /analytics/metrics → advanced_metrics.max_drawdown.percent
      case "current_drawdown":
        return (
          <CurrentDrawdownWidget
            currentDrawdownPercent={portfolio?.current_drawdown_percent ?? 0}
            peakPortfolioValue={portfolio?.peak_portfolio_value ?? 0}
            daysUnderwater={analyticsMetrics?.advanced_metrics?.days_underwater ?? 0}
            maxDrawdownPercent={analyticsMetrics?.advanced_metrics?.max_drawdown?.percent ?? 0}
          />
        );

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
                    {smallWidgets.map((widget) => (
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
                {otherWidgets.map((widget) => {
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
