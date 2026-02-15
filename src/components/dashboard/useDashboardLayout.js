import { useState, useEffect } from "react";

const DEFAULT_LAYOUT = [
  { id: "portfolio_value", order: 0 },
  { id: "cash_balance", order: 1 },
  { id: "open_positions", order: 2 },
  { id: "total_pnl", order: 3 },
  { id: "win_rate", order: 4 },
  { id: "avg_hold_time", order: 5 },
  { id: "current_drawdown", order: 6 },
  { id: "recent_trades", order: 7 },
  { id: "portfolio_chart", order: 8 },
  { id: "allocation_chart", order: 9 },
  { id: "market_regime_us", order: 10 },
  { id: "market_regime_uk", order: 11 },
  { id: "quick_actions", order: 12 },
];

const STORAGE_KEY = "dashboard_layout";

export function useDashboardLayout() {
  const [widgets, setWidgets] = useState([]);
  const [isLoaded, setIsLoaded] = useState(false);

  // Load layout from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        setWidgets(JSON.parse(saved));
      } catch {
        setWidgets(DEFAULT_LAYOUT);
      }
    } else {
      setWidgets(DEFAULT_LAYOUT);
    }
    setIsLoaded(true);
  }, []);

  // Save layout to localStorage whenever it changes
  useEffect(() => {
    if (isLoaded && widgets.length > 0) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(widgets));
    }
  }, [widgets, isLoaded]);

  const addWidget = (widget) => {
    setWidgets(prev => [...prev, { id: widget.id, order: prev.length }]);
  };

  const removeWidget = (widgetId) => {
    setWidgets(prev => prev.filter(w => w.id !== widgetId).map((w, idx) => ({ ...w, order: idx })));
  };

  const reorderWidgets = (newOrder) => {
    setWidgets(newOrder.map((id, idx) => ({ id, order: idx })));
  };

  const resetToDefault = () => {
    setWidgets(DEFAULT_LAYOUT);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(DEFAULT_LAYOUT));
  };

  const saveLayout = () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(widgets));
  };

  return {
    widgets: widgets.sort((a, b) => a.order - b.order),
    addWidget,
    removeWidget,
    reorderWidgets,
    resetToDefault,
    saveLayout,
    isLoaded
  };
}

export { DEFAULT_LAYOUT };
