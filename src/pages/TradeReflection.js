import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { base44 } from "../api/base44Client";
import { Loader2, BookOpen, Search, TrendingUp, TrendingDown, Calendar } from "lucide-react";
import { cn } from "../lib/utils";
import { format } from "date-fns";
import PageHeader from "../components/ui/PageHeader";
import { Input } from "../components/ui/input";
import TradeReflectionModal from "../components/trades/TradeReflectionModal";

function exitReasonLabel(r) {
  const map = { stop_hit: "STOP", manual: "MANUAL", target: "TARGET", market_regime: "REGIME" };
  return map[r] || (r ? r.toUpperCase() : "—");
}

function exitReasonColor(r) {
  return {
    stop_hit:      "bg-rose-500/20 text-rose-400 border-rose-500/30",
    manual:        "bg-violet-500/20 text-violet-400 border-violet-500/30",
    target:        "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
    market_regime: "bg-amber-500/20 text-amber-400 border-amber-500/30",
  }[r] || "bg-slate-800 text-slate-400 border-slate-700";
}

export default function TradeReflection() {
  const [search, setSearch] = useState("");
  const [selectedTrade, setSelectedTrade] = useState(null);

  const { data: trades = [], isLoading } = useQuery({
    queryKey: ["trade-reflections-list"],
    queryFn: () => base44.entities.TradeReflection.list(),
  });

  const filtered = trades.filter((r) =>
    !search || r.ticker?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <PageHeader
        title="Trade Reflections"
        description="Review and revisit your structured post-trade reflections."
      />

      <div className="relative max-w-sm">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
        <Input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search by ticker…"
          className="bg-slate-800/50 border-slate-700 text-white pl-10"
        />
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-24">
          <Loader2 className="w-8 h-8 animate-spin text-slate-500" />
        </div>
      ) : filtered.length === 0 ? (
        <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-12 text-center">
          <BookOpen className="w-10 h-10 text-slate-600 mx-auto mb-3" />
          <p className="text-slate-500">No closed trades yet — close a trade to write your first reflection.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {filtered.map((r) => {
            const isProfit = (r.pnl ?? 0) >= 0;

            return (
              <button
                key={r.id}
                onClick={() => setSelectedTrade(r)}
                className="text-left rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-5 hover:border-cyan-500/40 hover:shadow-lg hover:shadow-cyan-500/5 transition-all group"
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <span className="text-lg font-bold text-white group-hover:text-cyan-400 transition-colors">
                      {r.ticker}
                    </span>
                    <span className="ml-2 text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                      {r.market || "—"}
                    </span>
                  </div>
                  <span className={cn(
                    "text-xs px-2.5 py-1 rounded-full border",
                    exitReasonColor(r.exit_reason)
                  )}>
                    {exitReasonLabel(r.exit_reason)}
                  </span>
                </div>

                <div className="grid grid-cols-3 gap-2 mb-3">
                  <div>
                    <div className="text-xs text-slate-500">P&L</div>
                    <div className={cn("text-sm font-semibold", isProfit ? "text-emerald-400" : "text-rose-400")}>
                      {isProfit ? "+" : ""}£{(r.pnl || 0).toFixed(2)}
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-slate-500">R-Multiple</div>
                    <div className={cn("text-sm font-semibold", r.r_multiple == null ? "text-slate-400" : r.r_multiple >= 0 ? "text-emerald-400" : "text-rose-400")}>
                      {r.r_multiple != null ? `${r.r_multiple >= 0 ? "+" : ""}${r.r_multiple.toFixed(2)}R` : "N/A"}
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-slate-500">Hold</div>
                    <div className="text-sm font-medium text-slate-300">
                      {r.hold_days != null ? `${r.hold_days}d` : "—"}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-1 mt-3 text-xs text-slate-600">
                  <Calendar className="w-3 h-3" />
                  {r.exit_date ? format(new Date(r.exit_date), "dd MMM yyyy") : "—"}
                </div>
              </button>
            );
          })}
        </div>
      )}

      {selectedTrade && (
        <TradeReflectionModal
          trade={selectedTrade}
          open={!!selectedTrade}
          onClose={() => setSelectedTrade(null)}
        />
      )}
    </div>
  );
}
