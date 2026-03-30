import { AlertCircle, Loader2 } from "lucide-react";
import { Link } from "react-router-dom";
import { cn } from "../../../lib/utils";

export default function DashboardCard({ title, to, isLoading, error, children, className }) {
  const content = (
    <div className={cn(
      "relative rounded-2xl bg-slate-800/50 border border-slate-700/50 backdrop-blur-sm p-6 transition-all hover:border-slate-600/70 hover:bg-slate-800/70 cursor-pointer h-full",
      className
    )}>
      <p className="text-xs text-slate-400 uppercase tracking-wider mb-3">{title}</p>

      {isLoading && (
        <div className="flex justify-center py-4">
          <Loader2 className="w-5 h-5 animate-spin text-slate-500" />
        </div>
      )}

      {!isLoading && error && (
        <div className="flex items-center gap-2 text-rose-400">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span className="text-sm">Unable to load</span>
        </div>
      )}

      {!isLoading && !error && children}
    </div>
  );

  return to ? <Link to={to} className="block h-full">{content}</Link> : content;
}
