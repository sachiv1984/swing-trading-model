import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
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
import CashManagementModal from "../components/cash/CashManagementModal";
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

  const portfolio = portfolios?.[0];
  const openPositions = positions || [];
  const closedPositions = allPositions?.filter(p => p.status === "closed") || [];
  
  // FIXED: Use value_gbp if available, otherwise calculate
  const totalPositionsValue = openPositions.reduce((sum, p) => {
    // Backend now provides value_gbp (already calculated and converted)
    if (p.value_gbp !== undefined) {
      return sum + p.value_gbp;
    }
    // Fallback for backward compatibility
    return sum + (p.current_price || p.entry_price) * p.shares;
  }, 0);
  
  // Total P&L is already in GBP from API
  const totalPnL = openPositions.reduce((sum, p) => {
    return sum + (p.pnl || 0);
  }, 0);

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
    const smallWidgets = ["portfolio_value", "cash_balance", "open_positions", "total_pnl", "win_rate", "avg_hold_time"];
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
