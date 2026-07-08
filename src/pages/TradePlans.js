import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../api/base44Client";
import { Button } from "../components/ui/button";
import PageHeader from "../components/ui/PageHeader";
import DataState from "../components/ui/DataState";
import { Plus, FileText, Edit2, Trash2, AlertTriangle } from "lucide-react";
import { cn } from "../lib/utils";
import { formatDistanceToNow } from "date-fns";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

const STATUS_CONFIG = {
  draft:                 { label: "Draft",              bg: "bg-gray-500",    text: "text-white" },
  research_pending:      { label: "Research Pending",   bg: "bg-amber-600",   text: "text-white" },
  research_complete:     { label: "Research Complete",  bg: "bg-blue-600",    text: "text-white" },
  entry_conditions_set:  { label: "Entry Ready",        bg: "bg-violet-600",  text: "text-white" },
  active:                { label: "Active",             bg: "bg-green-700",   text: "text-white" },
  closed:                { label: "Closed",             bg: "bg-slate-500",   text: "text-white" },
  abandoned:             { label: "Abandoned",          bg: "bg-red-600",     text: "text-white" },
};

export function TradePlanStatusBadge({ status }) {
  const cfg = STATUS_CONFIG[status] || STATUS_CONFIG.draft;
  return (
    <span className={cn("inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold", cfg.bg, cfg.text)}>
      {cfg.label}
    </span>
  );
}

export default function TradePlans() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [deleteTarget, setDeleteTarget] = useState(null);

  const { data: plans = [], isLoading, isError, refetch } = useQuery({
    queryKey: ["tradePlans"],
    queryFn: async () => {
      const res = await apiFetch(`${API_BASE}/trade-plans`);
      const json = await res.json();
      return json.data || [];
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id) =>
      apiFetch(`${API_BASE}/trade-plans/${id}`, { method: "DELETE" }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tradePlans"] });
      setDeleteTarget(null);
    },
  });

  const sorted = [...plans].sort(
    (a, b) => new Date(b.updated_at || 0) - new Date(a.updated_at || 0)
  );

  return (
    <div className="space-y-6">
      <PageHeader
        title="Trade Plans"
        description={`${plans.length} plan${plans.length !== 1 ? "s" : ""}`}
        actions={
          <Button
            onClick={() => navigate("/TradePlan")}
            className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 shadow-lg shadow-violet-500/25"
          >
            <Plus className="w-4 h-4 mr-2" />
            New Trade Plan
          </Button>
        }
      />

      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 overflow-hidden">
        <DataState
          loading={isLoading}
          error={isError}
          onRetry={refetch}
          empty={!isLoading && !isError && plans.length === 0}
          emptyIcon={<FileText className="w-10 h-10 text-slate-600" />}
          emptyHeading="No trade plans yet."
          emptyBody="Create a trade plan before opening your next position."
          emptyAction={
            <Button
              onClick={() => navigate("/TradePlan")}
              className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0"
            >
              <Plus className="w-4 h-4 mr-2" />
              New Trade Plan
            </Button>
          }
        >
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-700/50">
                  {["Ticker", "Status", "R Target", "Notes", "Updated", "Actions"].map((h) => (
                    <th
                      key={h}
                      className="px-5 py-3.5 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider whitespace-nowrap"
                    >
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700/30">
                {sorted.map((plan) => (
                  <tr
                    key={plan.id}
                    className={cn("transition-colors", plan.status === "abandoned" && "opacity-70")}
                  >
                    <td className="px-5 py-4">
                      <span className="font-semibold text-white text-sm">{plan.ticker}</span>
                      {plan.market && (
                        <span className="ml-2 text-xs text-slate-400">{plan.market}</span>
                      )}
                    </td>
                    <td className="px-5 py-4">
                      <TradePlanStatusBadge status={plan.status} />
                    </td>
                    <td className="px-5 py-4 text-sm text-slate-300">
                      {plan.r_target != null ? `${plan.r_target}R` : "—"}
                    </td>
                    <td className="px-5 py-4 text-sm text-slate-400 max-w-xs truncate">
                      {plan.setup_thesis
                        ? plan.setup_thesis.slice(0, 60) + (plan.setup_thesis.length > 60 ? "…" : "")
                        : "—"}
                    </td>
                    <td className="px-5 py-4 text-sm text-slate-400 whitespace-nowrap">
                      {plan.updated_at
                        ? formatDistanceToNow(new Date(plan.updated_at), { addSuffix: true })
                        : "—"}
                    </td>
                    <td className="px-5 py-4">
                      <div className="flex items-center gap-2">
                        {plan.status !== "abandoned" && (
                          <Button
                            variant="ghost"
                            size="icon"
                            className="h-7 w-7 text-slate-400 hover:text-white hover:bg-slate-800"
                            onClick={() =>
                              navigate(
                                `/TradePlan?edit=${plan.id}&ticker=${plan.ticker}&market=${plan.market || "US"}`
                              )
                            }
                          >
                            <Edit2 className="w-4 h-4" />
                          </Button>
                        )}
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-7 w-7 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10"
                          onClick={() => setDeleteTarget(plan)}
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </DataState>
      </div>

      {/* Delete confirmation */}
      {deleteTarget && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
          <div className="w-full max-w-md rounded-2xl bg-slate-900 border border-slate-700 p-6 space-y-4 mx-4">
            <div className="flex items-center gap-3">
              <AlertTriangle className="w-5 h-5 text-rose-400 flex-shrink-0" />
              <h2 className="text-lg font-semibold text-white">
                Delete plan for {deleteTarget.ticker}?
              </h2>
            </div>
            <p className="text-sm text-slate-400">This action cannot be undone.</p>
            <div className="flex gap-3 justify-end">
              <Button variant="ghost" onClick={() => setDeleteTarget(null)} className="text-slate-400">
                Cancel
              </Button>
              <Button
                onClick={() => deleteMutation.mutate(deleteTarget.id)}
                disabled={deleteMutation.isPending}
                className="bg-rose-600 hover:bg-rose-500 text-white border-0"
              >
                {deleteMutation.isPending ? "Deleting…" : "Delete"}
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
