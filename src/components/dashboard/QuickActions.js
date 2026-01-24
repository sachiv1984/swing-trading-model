import { motion } from "framer-motion";
import { Button } from "../components/ui/button";
import { Plus, BarChart3, Play, ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";
import { createPageUrl } from "@/utils";
import { cn } from "@/lib/utils";

export default function QuickActions({ onRunMonitor }) {
  const actions = [
    {
      label: "New Position",
      description: "Enter a new trade",
      icon: Plus,
      href: createPageUrl("TradeEntry"),
      gradient: "from-cyan-500/20 to-cyan-500/5",
      iconBg: "bg-cyan-500/20 text-cyan-400",
      borderColor: "border-cyan-500/30",
      hoverBorder: "hover:border-cyan-500/50"
    },
    {
      label: "View Positions",
      description: "See all open positions",
      icon: BarChart3,
      href: createPageUrl("Positions"),
      gradient: "from-violet-500/20 to-violet-500/5",
      iconBg: "bg-violet-500/20 text-violet-400",
      borderColor: "border-violet-500/30",
      hoverBorder: "hover:border-violet-500/50"
    },
    {
      label: "Daily Monitor",
      description: "Run position checks",
      icon: Play,
      onClick: onRunMonitor,
      gradient: "from-fuchsia-500/20 to-fuchsia-500/5",
      iconBg: "bg-fuchsia-500/20 text-fuchsia-400",
      borderColor: "border-fuchsia-500/30",
      hoverBorder: "hover:border-fuchsia-500/50"
    }
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="grid grid-cols-1 sm:grid-cols-3 gap-4"
    >
      {actions.map((action, index) => {
        const Icon = action.icon;
        const content = (
          <div
            className={cn(
              "group relative overflow-hidden rounded-2xl border p-5 transition-all cursor-pointer",
              "bg-gradient-to-br backdrop-blur-sm",
              action.gradient,
              action.borderColor,
              action.hoverBorder
            )}
          >
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-4">
                <div className={cn("p-3 rounded-xl", action.iconBg)}>
                  <Icon className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-semibold text-white">{action.label}</h3>
                  <p className="text-sm text-slate-400 mt-0.5">{action.description}</p>
                </div>
              </div>
              <ArrowRight className="w-5 h-5 text-slate-600 group-hover:text-slate-400 group-hover:translate-x-1 transition-all" />
            </div>
          </div>
        );

        if (action.href) {
          return (
            <Link key={index} to={action.href}>
              {content}
            </Link>
          );
        }

        return (
          <div key={index} onClick={action.onClick}>
            {content}
          </div>
        );
      })}
    </motion.div>
  );
}
