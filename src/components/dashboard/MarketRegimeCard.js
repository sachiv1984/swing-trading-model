import { motion } from "framer-motion";
import { TrendingUp, TrendingDown, Globe } from "lucide-react";
import { cn } from "../../lib/utils";

export default function MarketRegimeCard({ market, status, index }) {
  const isRiskOn = status === "risk_on";

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className={cn(
        "relative overflow-hidden rounded-2xl p-5 border backdrop-blur-sm",
        isRiskOn 
          ? "bg-gradient-to-br from-emerald-500/10 to-emerald-500/5 border-emerald-500/30" 
          : "bg-gradient-to-br from-rose-500/10 to-rose-500/5 border-rose-500/30"
      )}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className={cn(
            "p-3 rounded-xl",
            isRiskOn ? "bg-emerald-500/20" : "bg-rose-500/20"
          )}>
            <Globe className={cn(
              "w-5 h-5",
              isRiskOn ? "text-emerald-400" : "text-rose-400"
            )} />
          </div>
          <div>
            <p className="text-base font-semibold text-white">{market} Market</p>
            <p className="text-sm text-slate-400">{index}</p>
          </div>
        </div>
        <div className={cn(
          "flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium",
          isRiskOn 
            ? "bg-emerald-500/20 text-emerald-400" 
            : "bg-rose-500/20 text-rose-400"
        )}>
          {isRiskOn ? (
            <TrendingUp className="w-4 h-4" />
          ) : (
            <TrendingDown className="w-4 h-4" />
          )}
          {isRiskOn ? "Risk On" : "Risk Off"}
        </div>
      </div>
      
      {/* Glow effect */}
      <div className={cn(
        "absolute -bottom-10 -right-10 w-32 h-32 rounded-full blur-3xl opacity-30",
        isRiskOn ? "bg-emerald-500" : "bg-rose-500"
      )} />
    </motion.div>
  );
}
