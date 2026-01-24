import { cn } from "@/lib/utils";

export default function StatusBadge({ status, className }) {
  const statusConfig = {
    risk_on: {
      label: "Risk On",
      className: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30"
    },
    risk_off: {
      label: "Risk Off",
      className: "bg-rose-500/20 text-rose-400 border-rose-500/30"
    },
    open: {
      label: "Open",
      className: "bg-cyan-500/20 text-cyan-400 border-cyan-500/30"
    },
    closed: {
      label: "Closed",
      className: "bg-slate-500/20 text-slate-400 border-slate-500/30"
    },
    hold: {
      label: "Hold",
      className: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30"
    },
    exit: {
      label: "Exit",
      className: "bg-amber-500/20 text-amber-400 border-amber-500/30"
    }
  };

  const config = statusConfig[status] || statusConfig.open;

  return (
    <span className={cn(
      "inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border",
      config.className,
      className
    )}>
      <span className="w-1.5 h-1.5 rounded-full bg-current mr-2" />
      {config.label}
    </span>
  );
}
