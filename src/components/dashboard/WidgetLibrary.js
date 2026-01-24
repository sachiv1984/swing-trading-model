import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "../ui/dialog";
import { Button } from "../ui/button";
import { motion } from "framer-motion";
import { 
  Wallet, 
  TrendingUp, 
  Briefcase, 
  PieChart, 
  BarChart3, 
  LineChart,
  Activity,
  Target,
  Zap,
  Globe,
  Clock,
  Award
} from "lucide-react";
import { cn } from "../../lib/utils";

const WIDGET_CATALOG = [
  {
    category: "Stats Cards",
    widgets: [
      { id: "portfolio_value", name: "Portfolio Value", icon: Wallet, description: "Total portfolio value", size: "small" },
      { id: "cash_balance", name: "Cash Balance", icon: Briefcase, description: "Available cash", size: "small" },
      { id: "open_positions", name: "Open Positions", icon: PieChart, description: "Current positions value", size: "small" },
      { id: "total_pnl", name: "Total P&L", icon: TrendingUp, description: "Profit and loss", size: "small" },
      { id: "win_rate", name: "Win Rate", icon: Award, description: "Trading win percentage", size: "small" },
      { id: "avg_hold_time", name: "Avg Hold Time", icon: Clock, description: "Average position duration", size: "small" },
    ]
  },
  {
    category: "Charts",
    widgets: [
      { id: "portfolio_chart", name: "Portfolio Chart", icon: LineChart, description: "Performance over time", size: "large" },
      { id: "allocation_chart", name: "Allocation Chart", icon: PieChart, description: "Position allocation pie", size: "medium" },
      { id: "pnl_chart", name: "P&L Bar Chart", icon: BarChart3, description: "Trade P&L breakdown", size: "large" },
      { id: "win_rate_chart", name: "Win Rate Chart", icon: Target, description: "Win/loss visualization", size: "medium" },
    ]
  },
  {
    category: "Market Info",
    widgets: [
      { id: "market_regime_us", name: "US Market Regime", icon: Globe, description: "US market status", size: "medium" },
      { id: "market_regime_uk", name: "UK Market Regime", icon: Globe, description: "UK market status", size: "medium" },
    ]
  },
  {
    category: "Actions",
    widgets: [
      { id: "quick_actions", name: "Quick Actions", icon: Zap, description: "Shortcuts to common tasks", size: "large" },
      { id: "recent_trades", name: "Recent Trades", icon: Activity, description: "Latest trade activity", size: "large" },
    ]
  }
];

export default function WidgetLibrary({ open, onClose, onAddWidget, activeWidgets }) {
  const [selectedCategory, setSelectedCategory] = useState("Stats Cards");

  const isWidgetActive = (widgetId) => activeWidgets.some(w => w.id === widgetId);

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="bg-slate-900 border-slate-700 text-white max-w-2xl max-h-[80vh] overflow-hidden flex flex-col">
        <DialogHeader>
          <DialogTitle className="text-xl font-bold text-white">Widget Library</DialogTitle>
          <DialogDescription className="text-slate-400">
            Add widgets to customize your dashboard
          </DialogDescription>
        </DialogHeader>

        {/* Category Tabs */}
        <div className="flex gap-2 overflow-x-auto pb-2 border-b border-slate-700/50">
          {WIDGET_CATALOG.map((cat) => (
            <button
              key={cat.category}
              onClick={() => setSelectedCategory(cat.category)}
              className={cn(
                "px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-all",
                selectedCategory === cat.category
                  ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 text-cyan-400 border border-cyan-500/30"
                  : "text-slate-400 hover:text-white hover:bg-slate-800/50"
              )}
            >
              {cat.category}
            </button>
          ))}
        </div>

        {/* Widget Grid */}
        <div className="flex-1 overflow-y-auto py-4">
          <div className="grid grid-cols-2 gap-3">
            {WIDGET_CATALOG.find(c => c.category === selectedCategory)?.widgets.map((widget) => {
              const Icon = widget.icon;
              const isActive = isWidgetActive(widget.id);
              
              return (
                <motion.button
                  key={widget.id}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => !isActive && onAddWidget(widget)}
                  disabled={isActive}
                  className={cn(
                    "flex items-start gap-3 p-4 rounded-xl text-left transition-all",
                    isActive
                      ? "bg-slate-800/30 border border-slate-700/30 opacity-50 cursor-not-allowed"
                      : "bg-slate-800/50 border border-slate-700/50 hover:border-cyan-500/50 hover:bg-slate-800"
                  )}
                >
                  <div className={cn(
                    "p-2.5 rounded-xl",
                    isActive ? "bg-slate-700/50 text-slate-500" : "bg-gradient-to-br from-cyan-500/20 to-violet-500/20 text-cyan-400"
                  )}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className={cn("font-medium", isActive ? "text-slate-500" : "text-white")}>
                      {widget.name}
                    </p>
                    <p className="text-xs text-slate-500 mt-0.5">{widget.description}</p>
                    <div className="flex items-center gap-2 mt-2">
                      <span className={cn(
                        "text-xs px-2 py-0.5 rounded-full",
                        widget.size === "small" && "bg-emerald-500/20 text-emerald-400",
                        widget.size === "medium" && "bg-amber-500/20 text-amber-400",
                        widget.size === "large" && "bg-violet-500/20 text-violet-400"
                      )}>
                        {widget.size}
                      </span>
                      {isActive && (
                        <span className="text-xs text-slate-500">Already added</span>
                      )}
                    </div>
                  </div>
                </motion.button>
              );
            })}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}

export { WIDGET_CATALOG };
