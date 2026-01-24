import { motion } from "framer-motion";
import { cn } from "../../lib";

export default function StatsCard({ 
  title, 
  value, 
  subtitle, 
  icon: Icon, 
  trend, 
  trendValue,
  gradient,
  className 
}) {
  const isPositive = trend === "up";
  const isNegative = trend === "down";

  const gradients = {
    cyan: "from-cyan-500/20 to-cyan-500/5 border-cyan-500/30",
    violet: "from-violet-500/20 to-violet-500/5 border-violet-500/30",
    fuchsia: "from-fuchsia-500/20 to-fuchsia-500/5 border-fuchsia-500/30",
    emerald: "from-emerald-500/20 to-emerald-500/5 border-emerald-500/30",
    amber: "from-amber-500/20 to-amber-500/5 border-amber-500/30",
    rose: "from-rose-500/20 to-rose-500/5 border-rose-500/30",
  };

  const iconColors = {
    cyan: "text-cyan-400 bg-cyan-500/20",
    violet: "text-violet-400 bg-violet-500/20",
    fuchsia: "text-fuchsia-400 bg-fuchsia-500/20",
    emerald: "text-emerald-400 bg-emerald-500/20",
    amber: "text-amber-400 bg-amber-500/20",
    rose: "text-rose-400 bg-rose-500/20",
  };

  const selectedGradient = gradient || "cyan";

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn(
        "relative overflow-hidden rounded-2xl border p-6",
        "bg-gradient-to-br",
        gradients[selectedGradient],
        "backdrop-blur-sm",
        className
      )}
    >
      <div className="flex items-start justify-between">
        <div className="space-y-2">
          <p className="text-sm font-medium text-slate-600 dark:text-slate-400">{title}</p>
          <p className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">{value}</p>
          {subtitle && (
            <p className="text-xs text-slate-500 dark:text-slate-500">{subtitle}</p>
          )}
          {trendValue && (
            <div className={cn(
              "inline-flex items-center gap-1 text-xs font-medium px-2.5 py-1 rounded-full",
              isPositive && "bg-emerald-500/20 text-emerald-400",
              isNegative && "bg-rose-500/20 text-rose-400",
              !isPositive && !isNegative && "bg-slate-800 text-slate-400"
            )}>
              {isPositive && "↑"}
              {isNegative && "↓"}
              {trendValue}
            </div>
          )}
        </div>
        {Icon && (
          <div className={cn("p-3 rounded-xl", iconColors[selectedGradient])}>
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>
      
      {/* Glow effect */}
      <div className="absolute -bottom-8 -right-8 w-32 h-32 bg-gradient-to-br from-white/5 to-transparent rounded-full blur-2xl" />
    </motion.div>
  );
}
