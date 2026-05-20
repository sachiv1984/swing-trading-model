import { useState, useEffect, useRef } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "../api/base44Client";
import { Button } from "../components/ui/button";
import PageHeader from "../components/ui/PageHeader";
import DataState from "../components/ui/DataState";
import EntryChecklist, { DEFAULT_CHECKLIST_ITEMS } from "../components/trades/EntryChecklist";
import SignalContextPanel, { buildSignalPrePopulation } from "../components/trades/SignalContextPanel";
import { BookOpen, Save, ArrowLeft, AlertTriangle, ChevronDown, ChevronUp, Newspaper, Sparkles, X as XIcon } from "lucide-react";
import { TradePlanStatusBadge } from "./TradePlans";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

const SETUP_TYPES = [
  { value: "", label: "— Select setup type —" },
  { value: "Breakout", label: "Breakout" },
  { value: "Pullback to MA", label: "Pullback to MA" },
  { value: "Momentum Continuation", label: "Momentum Continuation" },
  { value: "Mean Reversion", label: "Mean Reversion" },
  { value: "Catalyst-driven", label: "Catalyst-driven" },
  { value: "Other", label: "Other" },
];

const STATUSES = [
  "draft",
  "research_pending",
  "research_complete",
  "entry_conditions_set",
  "active",
  "closed",
];

const STATUS_LABELS = {
  draft: "Draft",
  research_pending: "Research Pending",
  research_complete: "Research Complete",
  entry_conditions_set: "Entry Ready",
  active: "Active",
  closed: "Closed",
};

function relativeAge(isoString) {
  if (!isoString) return "";
  const diff = Date.now() - new Date(isoString).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}

function NewsContextPanel({ ticker, market }) {
  const storageKey = `news-collapsed-${ticker}`;
  const [collapsed, setCollapsed] = useState(() => {
    try { return localStorage.getItem(storageKey) === "true"; } catch { return false; }
  });

  const { data: headlines = [], isFetched } = useQuery({
    queryKey: ["plan-news", ticker],
    queryFn: async () => {
      const res = await apiFetch(`${API_BASE}/news/${ticker}?limit=5`);
      const json = await res.json();
      return Array.isArray(json.data) ? json.data : [];
    },
    enabled: !!ticker && market === "US",
    staleTime: 5 * 60 * 1000,
  });

  if (market !== "US" || !ticker) return null;
  if (isFetched && headlines.length === 0) return null;

  const toggle = () => {
    const next = !collapsed;
    setCollapsed(next);
    try { localStorage.setItem(storageKey, String(next)); } catch {}
  };

  return (
    <div data-testid="news-context-panel" className="rounded-xl border border-slate-700/50 bg-slate-800/30 overflow-hidden">
      <button
        type="button"
        onClick={toggle}
        className="w-full flex items-center justify-between px-4 py-2.5 text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-700/30 transition-colors"
        data-testid="news-panel-toggle"
      >
        <div className="flex items-center gap-2">
          <Newspaper size={14} className="text-slate-400" />
          <span>News Context</span>
          {headlines.length > 0 && (
            <span className="text-xs text-slate-500">{headlines.length} headlines</span>
          )}
        </div>
        {collapsed ? <ChevronDown size={14} className="text-slate-500" /> : <ChevronUp size={14} className="text-slate-500" />}
      </button>
      {!collapsed && headlines.length > 0 && (
        <ul className="divide-y divide-slate-700/30 px-4 pb-3" data-testid="news-headline-list">
          {headlines.map((item, i) => (
            <li key={i} className="py-2 space-y-0.5">
              <p className="text-sm text-slate-200 leading-snug">{item.title || item.headline}</p>
              <div className="flex items-center gap-2 text-xs text-slate-500">
                {(item.source || item.author) && <span>{item.source || item.author}</span>}
                <span>{relativeAge(item.created_at || item.updated_at)}</span>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

const HAS_GEMINI = !!process.env.REACT_APP_GEMINI_API_KEY;

function generateThesisTemplate({ setupType, ticker, market, signal, headlines }) {
  const parts = [];
  const setupLabel = setupType || "Technical";
  parts.push(`**${setupLabel} setup on ${ticker} (${market})**`);

  if (signal) {
    const score = signal.signal_score != null ? ` Signal score ${(signal.signal_score * 100).toFixed(0)}%.` : "";
    const atr = signal.atr != null ? ` ATR ${signal.atr.toFixed(2)}.` : "";
    parts.push(`Signal metrics:${score}${atr}`);
  }

  if (setupType === "Momentum Continuation") {
    parts.push("Price is extending a trend from a prior base. Looking for continuation on volume expansion.");
  } else if (setupType === "Breakout") {
    parts.push("Price is breaking above a key resistance level. Seeking confirmation of volume and follow-through.");
  } else if (setupType === "Pullback to MA") {
    parts.push("Price has pulled back to a moving average in a broader uptrend. Watching for reversal candle.");
  } else if (setupType === "Mean Reversion") {
    parts.push("Price has extended from the mean. Expecting reversion with defined risk at extremes.");
  } else if (setupType === "Catalyst-driven") {
    parts.push("A specific catalyst is the thesis driver. Entry contingent on catalyst confirmation.");
  }

  if (headlines && headlines.length > 0) {
    const topTwo = headlines.slice(0, 2).map((h) => `"${(h.title || h.headline || "").slice(0, 80)}"`).join("; ");
    parts.push(`Recent news: ${topTwo}.`);
  }

  parts.push("[Edit this draft to add your specific entry trigger and risk parameters.]");
  return parts.join("\n\n");
}

function buildPrePopulatedItems(plan) {
  return DEFAULT_CHECKLIST_ITEMS.map((item) => ({
    ...item,
    checked:
      (item.id === "stop_defined" && !!plan.early_exit_conditions) ||
      (item.id === "research_reviewed" && plan.r_target != null),
  }));
}

const EMPTY_FORM = {
  ticker: "",
  market: "US",
  position_id: null,
  setup_type: null,
  setup_thesis: "",
  entry_rationale: "",
  regime_context_at_entry: "",
  r_target: "",
  early_exit_conditions: "",
  confirmation_criteria: "",
  checklist_completed: false,
  checklist_items: DEFAULT_CHECKLIST_ITEMS.map((i) => ({ ...i })),
  status: "draft",
};

function Field({ label, children }) {
  return (
    <div className="space-y-1">
      <label className="text-xs font-medium text-slate-400 uppercase tracking-wide">{label}</label>
      {children}
    </div>
  );
}

function TextArea({ value, onChange, placeholder, rows = 3 }) {
  return (
    <textarea
      className="w-full px-3 py-2 text-sm bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 resize-none"
      rows={rows}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
    />
  );
}

function TextInput({ value, onChange, placeholder, type = "text" }) {
  return (
    <input
      type={type}
      className="w-full px-3 py-2 text-sm bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
      value={value}
      onChange={onChange}
      placeholder={placeholder}
    />
  );
}

export default function TradePlan() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const positionId = searchParams.get("position_id");
  const ticker = searchParams.get("ticker") || "";
  const market = searchParams.get("market") || "US";
  const editId = searchParams.get("edit");

  const [form, setForm] = useState({
    ...EMPTY_FORM,
    ticker,
    market,
    position_id: positionId || null,
  });
  const [saved, setSaved] = useState(false);
  const [isAiDraft, setIsAiDraft] = useState(false);
  const [showAbandonModal, setShowAbandonModal] = useState(false);
  const [abandonReason, setAbandonReason] = useState("");
  const [abandonReasonTouched, setAbandonReasonTouched] = useState(false);

  const { data: healthData } = useQuery({
    queryKey: ["market-status"],
    queryFn: () =>
      apiFetch(`${API_BASE}/market/status`).then((r) => r.json()),
    staleTime: 60000,
  });

  const regimeFromHealth =
    healthData?.data?.regime_status || healthData?.regime_status || "";

  const { data: existingPlan, isLoading: loadingExisting } = useQuery({
    queryKey: ["tradePlan", editId],
    queryFn: () =>
      apiFetch(`${API_BASE}/trade-plans/${editId}`).then((r) => r.json()).then((res) => res.data),
    enabled: !!editId,
  });

  useEffect(() => {
    if (existingPlan) {
      const existingItems = Array.isArray(existingPlan.checklist_items) ? existingPlan.checklist_items : [];
      const hasUserState = existingItems.some((i) => i.checked);
      const checklistItems = hasUserState
        ? existingItems
        : buildPrePopulatedItems(existingPlan);
      setForm({
        ticker: existingPlan.ticker || ticker,
        market: existingPlan.market || market,
        position_id: existingPlan.position_id || positionId || null,
        setup_type: existingPlan.setup_type || null,
        setup_thesis: existingPlan.setup_thesis || "",
        entry_rationale: existingPlan.entry_rationale || "",
        regime_context_at_entry: existingPlan.regime_context_at_entry || "",
        r_target: existingPlan.r_target != null ? String(existingPlan.r_target) : "",
        early_exit_conditions: existingPlan.early_exit_conditions || "",
        confirmation_criteria: existingPlan.confirmation_criteria || "",
        checklist_items: checklistItems,
        checklist_completed: checklistItems.every((i) => i.checked),
        status: existingPlan.status || "draft",
      });
    }
  }, [existingPlan]); // eslint-disable-line react-hooks/exhaustive-deps

  const { data: newsForGenerator = [] } = useQuery({
    queryKey: ["plan-news", form.ticker],
    queryFn: async () => {
      const res = await apiFetch(`${API_BASE}/news/${form.ticker}?limit=5`);
      const json = await res.json();
      return Array.isArray(json.data) ? json.data : [];
    },
    enabled: !!form.ticker && form.market === "US",
    staleTime: 5 * 60 * 1000,
  });

  const { data: watchlistedSignals = [] } = useQuery({
    queryKey: ["signals-watchlisted"],
    queryFn: () =>
      apiFetch(`${API_BASE}/signals?status=watchlisted`)
        .then((r) => r.json())
        .then((res) => (Array.isArray(res.data) ? res.data : [])),
    enabled: !!form.ticker && !editId,
    staleTime: 30000,
  });

  const linkedSignal = watchlistedSignals.find(
    (s) => s.ticker === form.ticker || s.ticker === form.ticker + ".L" || s.ticker.replace(/\.L$/, "") === form.ticker
  ) || null;

  const prePopApplied = useRef(false);
  useEffect(() => {
    if (!editId && linkedSignal && !prePopApplied.current) {
      prePopApplied.current = true;
      const { setupThesis, entryRationale, confirmationCriteria } = buildSignalPrePopulation(linkedSignal, form.market);
      setForm((prev) => ({
        ...prev,
        setup_type: prev.setup_type || "Momentum Continuation",
        setup_thesis: prev.setup_thesis || setupThesis,
        entry_rationale: prev.entry_rationale || entryRationale,
        confirmation_criteria: prev.confirmation_criteria || confirmationCriteria,
      }));
    }
  }, [linkedSignal]); // eslint-disable-line react-hooks/exhaustive-deps

  const { data: existingByPosition } = useQuery({
    queryKey: ["tradePlanByPosition", positionId],
    queryFn: () =>
      apiFetch(`${API_BASE}/trade-plans/by-position/${positionId}`)
        .then((r) => r.json())
        .then((res) => res.data?.[0] || null),
    enabled: !!positionId && !editId,
  });

  const createMutation = useMutation({
    mutationFn: (data) =>
      apiFetch(`${API_BASE}/trade-plans`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      }).then((r) => r.json()),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tradePlans"] });
      setSaved(true);
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }) =>
      apiFetch(`${API_BASE}/trade-plans/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      }).then((r) => r.json()),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tradePlans"] });
      setSaved(true);
    },
  });

  const abandonMutation = useMutation({
    mutationFn: ({ id, reason }) =>
      apiFetch(`${API_BASE}/trade-plans/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: "abandoned", abandonment_reason: reason }),
      }).then((r) => r.json()),
    onSuccess: (res) => {
      queryClient.invalidateQueries({ queryKey: ["tradePlans"] });
      setShowAbandonModal(false);
      setAbandonReason("");
      if (res.data) {
        setForm((prev) => ({ ...prev, status: "abandoned" }));
      }
    },
  });

  const set = (field) => (e) =>
    setForm((prev) => ({ ...prev, [field]: e.target.value }));

  const handleChecklistToggle = (idx) => {
    setForm((prev) => {
      const items = prev.checklist_items.map((item, i) =>
        i === idx ? { ...item, checked: !item.checked } : item
      );
      return { ...prev, checklist_items: items, checklist_completed: items.every((i) => i.checked) };
    });
  };

  const handleSubmit = () => {
    const payload = {
      ...form,
      regime_context_at_entry: form.regime_context_at_entry || regimeFromHealth || null,
      r_target: form.r_target !== "" ? parseFloat(form.r_target) : null,
    };
    if (editId) {
      updateMutation.mutate({ id: editId, data: payload });
    } else {
      createMutation.mutate(payload);
    }
  };

  const isPending = createMutation.isPending || updateMutation.isPending;
  // Derive abandonment state from the fetched plan OR form state (onSuccess removed in RQ v5)
  const isAbandoned = existingPlan?.status === "abandoned" || form.status === "abandoned";
  const abandonReasonValid = abandonReason.trim().length >= 10;

  return (
    <div className="space-y-6">
      <PageHeader
        title="Trade Plan"
        description={
          <div className="flex items-center gap-2 flex-wrap">
            <span>{form.ticker ? `${form.ticker} — ${form.market}` : "Document your pre-trade reasoning"}</span>
            {(existingPlan?.status || form.status) && (
              <TradePlanStatusBadge status={existingPlan?.status || form.status} />
            )}
          </div>
        }
        actions={
          <div className="flex items-center gap-2">
            {editId && !isAbandoned && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowAbandonModal(true)}
                className="border-amber-500/50 text-amber-400 hover:bg-amber-500/10 hover:text-amber-300"
              >
                <AlertTriangle className="w-4 h-4 mr-1" />
                Abandon Plan
              </Button>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate(-1)}
              className="text-slate-400 hover:text-white"
            >
              <ArrowLeft className="w-4 h-4 mr-1" />
              Back
            </Button>
          </div>
        }
      />

      {positionId && existingByPosition && !editId && (
        <div className="rounded-xl bg-amber-500/10 border border-amber-500/30 px-4 py-3 text-sm text-amber-300">
          An existing trade plan was found for this position.{" "}
          <button
            className="underline hover:text-amber-200"
            onClick={() =>
              navigate(`/TradePlan?edit=${existingByPosition.id}&position_id=${positionId}&ticker=${form.ticker}&market=${form.market}`)
            }
          >
            Edit it instead
          </button>
        </div>
      )}

      {saved && (
        <div className="rounded-xl bg-emerald-500/10 border border-emerald-500/30 px-4 py-3 text-sm text-emerald-300">
          Trade plan saved successfully.
        </div>
      )}

      {isAbandoned && (existingPlan?.abandonment_reason || form.abandonment_reason) && (
        <div className="rounded-xl bg-red-500/10 border border-red-500/30 px-4 py-3 text-sm text-red-300">
          <span className="font-medium">Reason for abandoning: </span>
          {existingPlan?.abandonment_reason || form.abandonment_reason}
        </div>
      )}

      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-6 space-y-6">

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Field label="Ticker">
            <TextInput value={form.ticker} onChange={set("ticker")} placeholder="e.g. AAPL" />
          </Field>
          <Field label="Market">
            <select
              className="w-full px-3 py-2 text-sm bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-cyan-500"
              value={form.market}
              onChange={set("market")}
            >
              <option value="US">US</option>
              <option value="UK">UK</option>
            </select>
          </Field>
          <Field label="Status">
            <select
              className="w-full px-3 py-2 text-sm bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-cyan-500 disabled:opacity-50"
              value={form.status}
              onChange={set("status")}
              disabled={isAbandoned}
            >
              {STATUSES.map((s) => (
                <option key={s} value={s}>{STATUS_LABELS[s] || s}</option>
              ))}
              {isAbandoned && <option value="abandoned">Abandoned</option>}
            </select>
          </Field>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Field label="R Target">
            <TextInput
              type="number"
              value={form.r_target}
              onChange={set("r_target")}
              placeholder="e.g. 2.5"
            />
          </Field>
          <Field label="Regime Context at Entry">
            <TextInput
              value={form.regime_context_at_entry || regimeFromHealth}
              onChange={set("regime_context_at_entry")}
              placeholder={regimeFromHealth || "e.g. risk_on"}
            />
          </Field>
        </div>

        {!editId && <SignalContextPanel signal={linkedSignal} market={form.market} />}

        <Field label="Setup Type">
          <select
            data-testid="setup-type-select"
            className="w-full px-3 py-2 text-sm bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-cyan-500"
            value={form.setup_type || ""}
            onChange={(e) => setForm((prev) => ({ ...prev, setup_type: e.target.value || null }))}
          >
            {SETUP_TYPES.map((t) => (
              <option key={t.value} value={t.value}>{t.label}</option>
            ))}
          </select>
        </Field>

        <NewsContextPanel ticker={form.ticker} market={form.market} />

        <div className="space-y-1">
          <div className="flex items-center justify-between">
            <label className="text-xs font-medium text-slate-400 uppercase tracking-wide">Setup Thesis</label>
            <div className="flex items-center gap-2">
              {isAiDraft && (
                <span data-testid="ai-draft-badge" className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs bg-violet-500/20 text-violet-300 border border-violet-500/30">
                  <Sparkles size={10} />
                  AI draft
                </span>
              )}
              <button
                type="button"
                data-testid="generate-thesis-btn"
                onClick={() => {
                  const draft = generateThesisTemplate({
                    setupType: form.setup_type,
                    ticker: form.ticker,
                    market: form.market,
                    signal: linkedSignal,
                    headlines: newsForGenerator,
                  });
                  setForm((prev) => ({ ...prev, setup_thesis: draft }));
                  setIsAiDraft(true);
                }}
                className="flex items-center gap-1 text-xs text-violet-400 hover:text-violet-300 transition-colors"
                title="Generate thesis from setup type and signal data"
              >
                <Sparkles size={12} />
                Generate thesis
              </button>
              {HAS_GEMINI && (
                <button
                  type="button"
                  data-testid="improve-with-ai-btn"
                  className="flex items-center gap-1 text-xs text-cyan-400 hover:text-cyan-300 transition-colors"
                >
                  <Sparkles size={12} />
                  Improve with AI
                </button>
              )}
            </div>
          </div>
          <textarea
            data-testid="setup-thesis-textarea"
            className="w-full px-3 py-2 text-sm bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 resize-none"
            rows={3}
            value={form.setup_thesis}
            onChange={(e) => {
              setForm((prev) => ({ ...prev, setup_thesis: e.target.value }));
              if (isAiDraft) setIsAiDraft(false);
            }}
            placeholder="Describe the setup — what technical or fundamental condition makes this a candidate?"
          />
        </div>

        <Field label="Entry Rationale">
          <TextArea
            rows={3}
            value={form.entry_rationale}
            onChange={set("entry_rationale")}
            placeholder="Why enter now? What specific trigger confirms the thesis?"
          />
        </Field>

        <Field label="Confirmation Criteria">
          <TextArea
            rows={2}
            value={form.confirmation_criteria}
            onChange={set("confirmation_criteria")}
            placeholder="What must be true before pressing the button? (e.g. volume > 1.5× avg, no earnings within 5 days)"
          />
        </Field>

        <Field label="Early Exit Conditions">
          <TextArea
            rows={2}
            value={form.early_exit_conditions}
            onChange={set("early_exit_conditions")}
            placeholder="Under what conditions would you exit before the stop is hit?"
          />
        </Field>

        <Field label="Pre-Entry Checklist">
          <EntryChecklist
            items={form.checklist_items}
            ticker={form.ticker}
            onToggle={handleChecklistToggle}
          />
        </Field>

        {!isAbandoned && (
          <div className="flex justify-end">
            <Button
              onClick={handleSubmit}
              disabled={isPending || !form.ticker}
              className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0"
            >
              <Save className="w-4 h-4 mr-2" />
              {isPending ? "Saving…" : editId ? "Update Plan" : "Save Plan"}
            </Button>
          </div>
        )}
      </div>

      {/* Abandon modal */}
      {showAbandonModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
          <div className="w-full max-w-md rounded-2xl bg-slate-900 border border-slate-700 p-6 space-y-4 mx-4">
            <div className="flex items-center gap-3">
              <AlertTriangle className="w-5 h-5 text-amber-400 flex-shrink-0" />
              <h2 className="text-lg font-semibold text-white">
                Abandon trade plan for {form.ticker}?
              </h2>
            </div>
            <p className="text-sm text-slate-400">
              This plan will be marked as abandoned. You will not be prompted to enter this position again based on this plan.
            </p>
            <div className="space-y-1">
              <label className="text-xs font-medium text-slate-400 uppercase tracking-wide">
                Reason for abandoning <span className="text-rose-400">*</span>
              </label>
              <textarea
                rows={3}
                className="w-full px-3 py-2 text-sm bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-amber-500 resize-none"
                placeholder="Describe why you're abandoning this plan (min 10 characters)"
                value={abandonReason}
                onChange={(e) => setAbandonReason(e.target.value)}
                onBlur={() => setAbandonReasonTouched(true)}
              />
              {abandonReasonTouched && !abandonReasonValid && (
                <p className="text-xs text-rose-400">Reason must be at least 10 characters.</p>
              )}
            </div>
            <div className="flex gap-3 justify-end">
              <Button
                variant="ghost"
                onClick={() => { setShowAbandonModal(false); setAbandonReason(""); setAbandonReasonTouched(false); }}
                className="text-slate-400"
              >
                Cancel
              </Button>
              <Button
                disabled={!abandonReasonValid || abandonMutation.isPending}
                onClick={() => abandonMutation.mutate({ id: editId, reason: abandonReason.trim() })}
                className="bg-amber-600 hover:bg-amber-500 text-white border-0"
              >
                {abandonMutation.isPending ? "Abandoning…" : "Abandon Plan"}
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
