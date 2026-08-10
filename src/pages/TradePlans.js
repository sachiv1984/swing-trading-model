import { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../api/base44Client";
import { Button } from "../components/ui/button";
import PageHeader from "../components/ui/PageHeader";
import DataState from "../components/ui/DataState";
import { Checkbox } from "../components/ui/checkbox";
import BulkActionToolbar from "../components/shared/BulkActionToolbar";
import { Plus, FileText, Edit2, Trash2, AlertTriangle, Rocket } from "lucide-react";
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

// ST-01 (EPIC-01, v7.3): a plan is eligible for "Start Trade from Plan" only
// while it has no position linked yet and isn't already terminal/active.
const NOT_STARTABLE_STATUSES = ["active", "closed", "abandoned"];
export function isStartTradeEligible(plan) {
  return !plan.position_id && !NOT_STARTABLE_STATUSES.includes(plan.status);
}

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
  const [selectedIds, setSelectedIds] = useState(new Set());
  const [tagOptions, setTagOptions] = useState([]);

  const { data: plans = [], isLoading, isError, refetch } = useQuery({
    queryKey: ["tradePlans"],
    queryFn: async () => {
      const res = await apiFetch(`${API_BASE}/trade-plans`);
      const json = await res.json();
      return json.data || [];
    },
  });

  useEffect(() => {
    apiFetch(`${API_BASE}/trade-plans/tags`)
      .then((r) => (r.ok ? r.json() : { data: [] }))
      .then((json) => setTagOptions(json.data || []))
      .catch(() => {});
  }, []);

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

  const toggleRow = (id) => {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  };

  const toggleAll = () => {
    setSelectedIds((prev) =>
      prev.size === sorted.length ? new Set() : new Set(sorted.map((p) => p.id))
    );
  };

  const selectedActiveCount = sorted.filter(
    (p) => selectedIds.has(p.id) && p.status === "active"
  ).length;

  const handleBulkResult = async (result) => {
    if (result.failed.length === 0) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(result.failed.map((f) => f.id)));
    }
    await queryClient.invalidateQueries({ queryKey: ["tradePlans"] });
  };

  const handleStartTrade = (plan) => {
    navigate("/TradeEntry", {
      state: {
        trade_plan_prefill: {
          id: plan.id,
          ticker: plan.ticker,
          market: plan.market || "US",
          entry_price: plan.planned_entry_price,
          stop_price: plan.planned_stop_price,
          quantity: plan.planned_quantity,
        },
      },
    });
  };

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

      <BulkActionToolbar
        selectedCount={selectedIds.size}
        onClear={() => setSelectedIds(new Set())}
        itemLabel="plans"
        excludedNote={
          selectedActiveCount > 0
            ? `${selectedActiveCount} active plan(s) excluded — cannot be archived.`
            : null
        }
        tagAction={{
          tagOptions,
          onSubmit: async (tags) => {
            const res = await apiFetch(`${API_BASE}/trade-plans/bulk-tag`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ ids: Array.from(selectedIds), tags }),
            });
            const json = await res.json();
            return json.data;
          },
        }}
        destructiveActions={[
          {
            key: "archive",
            label: "Bulk Archive",
            confirmText: `Archive ${selectedIds.size} selected trade plan(s)?`,
            onConfirm: async () => {
              const res = await apiFetch(`${API_BASE}/trade-plans/bulk-archive`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ids: Array.from(selectedIds) }),
              });
              const json = await res.json();
              return json.data;
            },
          },
          {
            key: "delete",
            label: "Bulk Delete",
            confirmText: `Delete ${selectedIds.size} selected trade plan(s)?`,
            onConfirm: async () => {
              const res = await apiFetch(`${API_BASE}/trade-plans/bulk`, {
                method: "DELETE",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ids: Array.from(selectedIds) }),
              });
              const json = await res.json();
              return json.data;
            },
          },
        ]}
        onResult={handleBulkResult}
      />

      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 overflow-hidden">
        <DataState
          loading={isLoading}
          error={isError}
          onRetry={refetch}
          empty={!isLoading && !isError && plans.length === 0}
          emptyIcon={<FileText className="w-10 h-10 text-slate-600" />}
          emptyHeading="No trade plans yet"
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
                  <th className="px-5 py-3.5 text-left w-8">
                    <Checkbox
                      checked={sorted.length > 0 && selectedIds.size === sorted.length}
                      onCheckedChange={toggleAll}
                      aria-label="Select all"
                    />
                  </th>
                  {["Ticker", "Status", "R Target", "Notes", "Updated", "Actions"].map((h) => (
                    <th
                      key={h}
                      className="px-5 py-3.5 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider whitespace-nowrap"
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
                    className={cn(
                      "transition-colors",
                      plan.status === "abandoned" && "opacity-70",
                      selectedIds.has(plan.id) && "bg-cyan-500/5"
                    )}
                  >
                    <td className="px-5 py-4">
                      <Checkbox
                        checked={selectedIds.has(plan.id)}
                        onCheckedChange={() => toggleRow(plan.id)}
                        aria-label={`Select ${plan.ticker}`}
                      />
                    </td>
                    <td className="px-5 py-4">
                      <span className="font-semibold text-white text-sm">{plan.ticker}</span>
                      {plan.market && (
                        <span className="ml-2 text-xs text-slate-600 dark:text-slate-400">{plan.market}</span>
                      )}
                    </td>
                    <td className="px-5 py-4">
                      <TradePlanStatusBadge status={plan.status} />
                    </td>
                    <td className="px-5 py-4 text-sm text-slate-300">
                      {plan.r_target != null ? `${plan.r_target}R` : "—"}
                    </td>
                    <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-400 max-w-xs truncate">
                      {plan.setup_thesis
                        ? plan.setup_thesis.slice(0, 60) + (plan.setup_thesis.length > 60 ? "…" : "")
                        : "—"}
                    </td>
                    <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-400 whitespace-nowrap">
                      {plan.updated_at
                        ? formatDistanceToNow(new Date(plan.updated_at), { addSuffix: true })
                        : "—"}
                    </td>
                    <td className="px-5 py-4">
                      <div className="flex items-center gap-2">
                        {isStartTradeEligible(plan) && (
                          <Button
                            variant="outline"
                            size="sm"
                            data-testid={`start-trade-from-plan-${plan.id}`}
                            className="h-7 border-emerald-500/40 text-emerald-400 hover:bg-emerald-500/10 hover:text-emerald-300"
                            onClick={() => handleStartTrade(plan)}
                          >
                            <Rocket className="w-3.5 h-3.5 mr-1.5" />
                            Start Trade
                          </Button>
                        )}
                        {plan.status !== "abandoned" && (
                          <Button
                            variant="ghost"
                            size="icon"
                            className="h-7 w-7 text-slate-600 dark:text-slate-400 hover:text-white hover:bg-slate-800"
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
                          className="h-7 w-7 text-slate-600 dark:text-slate-400 hover:text-rose-400 hover:bg-rose-500/10"
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
            <p className="text-sm text-slate-600 dark:text-slate-400">This action cannot be undone.</p>
            <div className="flex gap-3 justify-end">
              <Button variant="ghost" onClick={() => setDeleteTarget(null)} className="text-slate-600 dark:text-slate-400">
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
