import { motion } from "framer-motion";
import { TrendingUp, TrendingDown, Globe, HelpCircle } from "lucide-react";
import { cn } from "../../lib/utils";
import ExplainedMarker from "../ui/ExplainedMarker";
import { REGIME_RISK_ON, REGIME_UNKNOWN, unknownRegimeExplanation } from "../../lib/regime";

const TONES = {
  on: {
    card: "bg-gradient-to-br from-emerald-500/10 to-emerald-500/5 border-emerald-500/30",
    iconBg: "bg-emerald-500/20",
    icon: "text-emerald-400",
    pill: "bg-emerald-500/20 text-emerald-400",
    glow: "bg-emerald-500",
  },
  off: {
    card: "bg-gradient-to-br from-rose-500/10 to-rose-500/5 border-rose-500/30",
    iconBg: "bg-rose-500/20",
    icon: "text-rose-400",
    pill: "bg-rose-500/20 text-rose-400",
    glow: "bg-rose-500",
  },
  unknown: {
    card: "bg-gradient-to-br from-slate-500/10 to-slate-500/5 border-slate-500/30",
    iconBg: "bg-slate-500/20",
    icon: "text-slate-700 dark:text-slate-300",
    pill: "bg-slate-200 text-slate-800 dark:bg-slate-500/20 dark:text-slate-300",
    glow: "bg-slate-500",
  },
};

function RegimePill({ market, isUnknown, isRiskOn, tone }) {
  const pillClass = cn("flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium", tone.pill);
  if (isUnknown) {
    return (
      <ExplainedMarker
        label={`${market} market regime unknown`}
        description={unknownRegimeExplanation(market)}
        testId={`regime-widget-unknown-${market}`}
        className={cn(pillClass, "ring-slate-500")}
      >
        <HelpCircle className="w-4 h-4" aria-hidden="true" />
        Unknown
      </ExplainedMarker>
    );
  }
  return (
    <div className={pillClass}>
      {isRiskOn ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
      {isRiskOn ? "Risk On" : "Risk Off"}
    </div>
  );
}

export default function MarketRegimeCard({ market, status, index }) {
  const isUnknown = status === REGIME_UNKNOWN;
  const isRiskOn = status === REGIME_RISK_ON;
  const tone = TONES[isUnknown ? "unknown" : isRiskOn ? "on" : "off"];

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className={cn(
        "relative overflow-hidden rounded-2xl p-5 border backdrop-blur-sm",
        tone.card
      )}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className={cn("p-3 rounded-xl", tone.iconBg)}>
            <Globe className={cn("w-5 h-5", tone.icon)} />
          </div>
          <div>
            <p className="text-base font-semibold text-white">{market} Market</p>
            <p className="text-sm text-slate-600 dark:text-slate-400">{index}</p>
          </div>
        </div>
        <RegimePill market={market} isUnknown={isUnknown} isRiskOn={isRiskOn} tone={tone} />
      </div>

      <div className={cn(
        "absolute -bottom-10 -right-10 w-32 h-32 rounded-full blur-3xl opacity-30",
        tone.glow
      )} />
    </motion.div>
  );
}
