import { Info } from "lucide-react";
import { motion } from "framer-motion";
import { cn } from "../../lib/utils";

export default function StatsCard({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  trendValue,
  gradient,
  className,
  tooltip,
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
        "relative rounded-2xl border bg-gradient-to-br backdrop-blur-sm",
        "p-4 xl:p-6",
        gradients[selectedGradient],
        className
      )}
    >
      <div className="flex items-center justify-between gap-3">
        {/* Text content */}
        <div className="min-w-0 space-y-1 xl:space-y-2">
          <p className="text-xs xl:text-sm font-medium text-slate-400 flex items-center gap-1 truncate">
            {title}
            {tooltip && (
              <span className="relative group/tooltip inline-flex flex-shrink-0">
                <Info className="w-3 h-3 text-slate-500 hover:text-slate-300 transition-colors cursor-default" />
                <span className="pointer-events-none absolute bottom-full right-0 mb-1.5 w-56 rounded bg-slate-800 px-2 py-1.5 text-xs text-slate-200 opacity-0 group-hover/tooltip:opacity-100 transition-opacity z-50 shadow-lg">
                  {tooltip}
                </span>
              </span>
            )}
          </p>
          <p className="text-xl xl:text-2xl font-bold text-white tracking-tight truncate">{value}</p>
          {subtitle && (
            <p className="text-xs text-slate-500 hidden xl:block">{subtitle}</p>
          )}
          {trendValue && (
            <div className={cn(
              "inline-flex items-center gap-1 text-xs font-medium px-2 py-0.5 rounded-full",
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

        {/* Decorative icon — scaled down at md, full size at xl */}
        {Icon && (
          <div className={cn(
            "flex-shrink-0 rounded-xl",
            "p-2 xl:p-3",
            iconColors[selectedGradient]
          )}>
            <Icon className="w-4 h-4 xl:w-5 xl:h-5" />
          </div>
        )}
      </div>
    </motion.div>
  );
}
