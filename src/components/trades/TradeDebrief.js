/**
 * TradeDebrief — Automated AI Post-Trade Debrief section for Trade Journal
 *
 * Renders inside the Trade History expandable row, after Plan vs Reality.
 * Lazy-fetches GET /trades/{id}/debrief only when mounted (row expanded).
 * Offers an on-demand "Generate Debrief" action (POST) when none exists yet
 * — this feature does not hook into the live trade-close event path (§13
 * review's own accepted fallback: "real-time generation, or on-demand if
 * real-time isn't feasible").
 *
 * §13 review (CONDITIONAL): docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md
 * Condition 4: no action affordances beyond Generate/Regenerate — no button,
 * link, or prompt here may auto-adjust strategy parameters, create a trade
 * plan, or modify any record based on debrief content.
 *
 * Spec: docs/specs/api_contracts/trade_endpoints.md#GET /trades/{trade_id}/debrief
 * ST-06, EPIC-02, v8.9
 */
import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Sparkles } from "lucide-react";
import { apiFetch } from "../../api/base44Client";
import { Button } from "../ui/button";
import { cn } from "../../lib/utils";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

function Skeleton() {
  return (
    <div className="space-y-2 animate-pulse" data-testid="debrief-skeleton">
      <div className="h-3 bg-slate-700 rounded w-2/3" />
      <div className="h-3 bg-slate-700 rounded w-1/2" />
    </div>
  );
}

const STATUS_LABEL = {
  ai_unavailable: "AI generation unavailable — showing the factual summary only.",
  fallback_no_focus_area: "The AI-generated focus area didn't pass its automated compliance check, so only the factual summary is shown.",
};

export default function TradeDebrief({ tradeId }) {
  const queryClient = useQueryClient();
  const [justGenerated, setJustGenerated] = useState(false);

  const { data, isLoading, isFetching } = useQuery({
    queryKey: ["tradeDebrief", tradeId],
    queryFn: async () => {
      const res = await apiFetch(`${API_URL}/trades/${tradeId}/debrief`);
      if (res.status === 404) return { status: "not_found" };
      if (!res.ok) return { status: "error" };
      const json = await res.json();
      return { status: "found", data: json.data };
    },
    retry: false,
    staleTime: 60_000,
  });

  const generateMutation = useMutation({
    mutationFn: async () => {
      const res = await apiFetch(`${API_URL}/trades/${tradeId}/debrief`, { method: "POST" });
      const json = await res.json();
      return json.data;
    },
    onSuccess: () => {
      setJustGenerated(true);
      queryClient.invalidateQueries({ queryKey: ["tradeDebrief", tradeId] });
    },
  });

  if (isLoading) {
    return (
      <div className="space-y-2.5">
        <div className="flex items-center gap-2">
          <Sparkles className="w-3.5 h-3.5 text-violet-400" />
          <h4 className="text-xs font-semibold uppercase tracking-wider text-violet-400">Post-Trade Debrief</h4>
        </div>
        <div className="w-full bg-slate-800/50 rounded-xl p-4 border border-violet-600/20 shadow-lg">
          <Skeleton />
        </div>
      </div>
    );
  }

  const notFound = data?.status === "not_found";
  const debrief = data?.status === "found" ? data.data : (justGenerated ? generateMutation.data : null);

  return (
    <div className="space-y-2.5" data-testid="trade-debrief-section">
      <div className="flex items-center gap-2">
        <Sparkles className="w-3.5 h-3.5 text-violet-400" />
        <h4 className="text-xs font-semibold uppercase tracking-wider text-violet-400">Post-Trade Debrief</h4>
        <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-violet-500/20 text-violet-300 border border-violet-500/30">AI-generated</span>
      </div>

      <div className="w-full bg-slate-800/50 rounded-xl border-l-4 border-l-violet-500 border border-slate-700/30 shadow-lg p-4 space-y-3">
        {!debrief && (notFound || !!generateMutation.error) && (
          <div className="space-y-2.5" data-testid="debrief-empty-state">
            <p className="text-xs text-slate-600 dark:text-slate-400">No debrief generated yet for this trade.</p>
            <Button
              size="sm"
              variant="outline"
              data-testid="generate-debrief-btn"
              disabled={generateMutation.isPending}
              onClick={() => generateMutation.mutate()}
              className="text-xs"
            >
              {generateMutation.isPending ? "Generating…" : "Generate Debrief"}
            </Button>
            {generateMutation.error && (
              <p className="text-xs text-rose-400">Could not generate a debrief right now. Try again shortly.</p>
            )}
          </div>
        )}

        {debrief && (
          <div className="space-y-3" data-testid="debrief-content">
            <p className="text-sm text-slate-300 leading-relaxed">{debrief.summary_text}</p>

            {debrief.focus_area_text && (
              <div className="pt-2 border-t border-slate-700/30">
                <span className="text-[10px] uppercase tracking-wider text-violet-400 font-semibold">Focus area</span>
                <p className="text-sm text-slate-300 leading-relaxed italic mt-1">{debrief.focus_area_text}</p>
              </div>
            )}

            {!debrief.focus_area_text && STATUS_LABEL[debrief.generation_status] && (
              <p className="text-xs text-slate-600 dark:text-slate-400 italic pt-2 border-t border-slate-700/30">
                {STATUS_LABEL[debrief.generation_status]}
              </p>
            )}

            <div className="pt-1">
              <Button
                size="sm"
                variant="ghost"
                data-testid="regenerate-debrief-btn"
                disabled={generateMutation.isPending || isFetching}
                onClick={() => generateMutation.mutate()}
                className={cn("text-xs text-slate-600 dark:text-slate-400 hover:text-slate-300")}
              >
                {generateMutation.isPending ? "Regenerating…" : "Regenerate"}
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
