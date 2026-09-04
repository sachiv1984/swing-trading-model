import { useState, useEffect, useRef } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "../api/base44Client";
import { Button } from "../components/ui/button";
import { Dialog, DialogContent, DialogTitle } from "../components/ui/dialog";
import PageHeader from "../components/ui/PageHeader";
import DataState from "../components/ui/DataState";
import EntryChecklist, { DEFAULT_CHECKLIST_ITEMS } from "../components/trades/EntryChecklist";
import SignalContextPanel, { buildSignalPrePopulation } from "../components/trades/SignalContextPanel";
import SetupQualityScorePanel from "../components/trades/SetupQualityScorePanel";
import WhatIfSizingPreview from "../components/trades/WhatIfSizingPreview";
import { BookOpen, Save, ArrowLeft, AlertTriangle, ChevronDown, ChevronUp, Newspaper, Sparkles, X as XIcon, ShieldCheck, ThumbsUp, ThumbsDown, Tag as TagIcon, Rocket, Printer } from "lucide-react";
import { TradePlanStatusBadge, isStartTradeEligible } from "./TradePlans";

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
            <span className="text-xs text-slate-600 dark:text-slate-400">{headlines.length} headlines</span>
          )}
        </div>
        {collapsed ? <ChevronDown size={14} className="text-slate-500" /> : <ChevronUp size={14} className="text-slate-500" />}
      </button>
      {!collapsed && headlines.length > 0 && (
        <ul className="divide-y divide-slate-700/30 px-4 pb-3" data-testid="news-headline-list">
          {headlines.map((item, i) => (
            <li key={i} className="py-2 space-y-0.5">
              <p className="text-sm text-slate-200 leading-snug">{item.title || item.headline}</p>
              <div className="flex items-center gap-2 text-xs text-slate-600 dark:text-slate-400">
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

const HAS_AI = !!process.env.REACT_APP_ANTHROPIC_API_KEY;

const RULE_LABELS = {
  regime_gate: "Regime Gate",
  cash_constraint: "Cash Constraint",
  sector_concentration: "Sector Concentration",
  earnings_proximity: "Earnings Proximity",
  sizing_validity: "Sizing Validity",
};

function PreEntryValidationPanel({ ticker, market, quantity, entryPrice, stopPrice, overrideAcknowledged, onOverrideChange }) {
  const [collapsed, setCollapsed] = useState(false);

  const { data, isLoading, isError } = useQuery({
    queryKey: ["pre-entry-validation", ticker, market, quantity, entryPrice, stopPrice],
    queryFn: async () => {
      const paramObj = { ticker, quantity, market };
      const ep = parseFloat(entryPrice);
      const sp = parseFloat(stopPrice);
      if (!isNaN(ep) && ep > 0) paramObj.entry_price = ep;
      if (!isNaN(sp) && sp > 0) paramObj.stop_price = sp;
      const params = new URLSearchParams(paramObj);
      const r = await apiFetch(`${API_BASE}/portfolio/pre-entry-validation?${params}`);
      const j = await r.json();
      return j.data;
    },
    enabled: !!ticker && !!quantity && Number(quantity) > 0,
    staleTime: 60000,
  });

  if (!ticker || !quantity || Number(quantity) <= 0) return null;

  const advisory = data?.advisory_status;
  const checks = data?.checks || [];
  const hasWarnings = checks.some((c) => c.status === "warn" || c.status === "fail");
  const warnCount = checks.filter((c) => c.status === "warn").length;
  const failCount = checks.filter((c) => c.status === "fail").length;

  const STATUS_ICON = { pass: "✓", warn: "⚠", fail: "✗", skipped: "—" };
  const STATUS_COLOR = {
    pass: "text-emerald-400",
    warn: "text-amber-400",
    fail: "text-red-400",
    skipped: "text-slate-600 dark:text-slate-400",
  };
  const ADVISORY_BADGE = {
    pass: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
    warn: "bg-amber-500/20 text-amber-400 border-amber-500/30",
    fail: "bg-red-500/20 text-red-400 border-red-500/30",
  };

  return (
    <div data-testid="pre-entry-checks-panel" className="rounded-xl border border-slate-700/50 bg-slate-800/30 overflow-hidden">
      <button
        type="button"
        data-testid="pre-entry-panel-toggle"
        className="w-full flex items-center justify-between px-4 py-3"
        onClick={() => setCollapsed((c) => !c)}
      >
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-3.5 h-3.5 text-slate-400" />
          <span className="text-xs font-medium text-slate-300 uppercase tracking-wide">Pre-Entry Checks</span>
          {advisory && (
            <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${ADVISORY_BADGE[advisory] || ADVISORY_BADGE.warn}`}>
              {advisory === "pass" ? "Pass" : advisory === "warn" ? "Warn" : "Fail"}
            </span>
          )}
          {collapsed && (advisory === "warn" || advisory === "fail") && (
            <span data-testid="pre-entry-issue-count" className="text-xs text-slate-600 dark:text-slate-400">
              {[failCount > 0 && `${failCount} fail`, warnCount > 0 && `${warnCount} warn`].filter(Boolean).join(", ")}
            </span>
          )}
          {isLoading && <span className="text-xs text-slate-600 dark:text-slate-400">Checking…</span>}
        </div>
        {collapsed ? <ChevronDown className="w-4 h-4 text-slate-500" /> : <ChevronUp className="w-4 h-4 text-slate-500" />}
      </button>
      {!collapsed && (
        <div className="px-4 pb-4 space-y-2 border-t border-slate-700/50 pt-3">
          {isError && <p className="text-xs text-slate-600 dark:text-slate-400">Validation unavailable — proceed with manual checks</p>}
          {!isLoading && !isError && checks.length === 0 && (
            <p className="text-xs text-slate-600 dark:text-slate-400">No checks available</p>
          )}
          {!isLoading && !isError && checks.map((check) => (
            <div key={check.rule} className="flex items-start gap-2 text-xs">
              <span className={`mt-0.5 font-mono w-3 shrink-0 ${STATUS_COLOR[check.status] || "text-slate-600 dark:text-slate-400"}`}>
                {STATUS_ICON[check.status] || "?"}
              </span>
              <div className="flex-1 min-w-0">
                <span className="text-slate-300">{RULE_LABELS[check.rule] || check.rule}</span>
                {check.detail && (
                  <span className="text-slate-600 dark:text-slate-400"> — {check.detail}</span>
                )}
              </div>
            </div>
          ))}
          {hasWarnings && (
            <label className="flex items-center gap-2 mt-3 cursor-pointer">
              <input
                type="checkbox"
                data-testid="override-acknowledgement-checkbox"
                checked={overrideAcknowledged || false}
                onChange={(e) => onOverrideChange(e.target.checked)}
                className="w-4 h-4 rounded border-slate-600 bg-slate-800 text-amber-500 focus:ring-amber-500/30"
              />
              <span className="text-xs text-amber-400">I acknowledge the advisory warnings</span>
            </label>
          )}
        </div>
      )}
    </div>
  );
}

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
  invalidation_condition: "",
  checklist_completed: false,
  checklist_items: DEFAULT_CHECKLIST_ITEMS.map((i) => ({ ...i })),
  status: "draft",
  pre_entry_override_acknowledged: false,
  thesis_feedback: null,
  planned_quantity: "",
  planned_entry_price: "",
  planned_stop_price: "",
  trade_tags: [],
  // ST-07 (BLG-FE-143, EPIC-03, v8.5): populated only from the real Claude
  // "Improve with AI" response (POST /trade-plans/generate-plan) -- never
  // from generateThesisTemplate(), which is a local, deterministic string
  // builder, not an AI call. Cleared on any manual edit to a narrative
  // field (setNarrativeField below) so a saved plan's version fields only
  // ever reflect content that was directly AI-generated, never edited.
  thesis_model_version: null,
  thesis_prompt_version: null,
  // ST-09 (BLG-BE-84, EPIC-02, v8.8): set only via the alert-notification-
  // to-trade-plan UI path (NotificationRow.js "Create Trade Plan" CTA);
  // null for plans created any other way. Ignored server-side on PUT
  // (TradePlanUpdate has no such field) so it's harmless to leave in the
  // update payload too.
  triggered_by_price_alert_id: null,
};

// ST-05 (BLG-FEAT-52): Tag Rules per journal_components.md §3/§4, reused for trade_tags
const TRADE_TAG_MAX_LENGTH = 20;
const TRADE_TAG_MAX_COUNT = 10;

function Field({ label, children }) {
  return (
    <div className="space-y-1">
      <label className="text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wide">{label}</label>
      {children}
    </div>
  );
}

function TextArea({ value, onChange, placeholder, rows = 3 }) {
  return (
    <textarea
      className="w-full px-3 py-2 text-sm bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring resize-none"
      rows={rows}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
    />
  );
}

function TextInput({ value, onChange, placeholder, type = "text", ...rest }) {
  return (
    <input
      type={type}
      className="w-full px-3 py-2 text-sm bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      {...rest}
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
  const priceAlertId = searchParams.get("price_alert_id"); // ST-09, BLG-BE-84, EPIC-02, v8.8

  const [form, setForm] = useState({
    ...EMPTY_FORM,
    ticker,
    market,
    position_id: positionId || null,
    triggered_by_price_alert_id: priceAlertId || null,
  });
  const [saved, setSaved] = useState(false);
  const [isAiDraft, setIsAiDraft] = useState(false);
  // isClaudeDraft: true only for "Improve with AI" (Claude Haiku 4.5) output — the
  // pre-existing "Generate thesis" button is a client-side template fill (isAiDraft
  // also true there) with no model call, so it must never trigger the feedback
  // control (ux_spec.md "Trigger Condition" note, ST-07/BLG-FE-46, v6.5).
  const [isClaudeDraft, setIsClaudeDraft] = useState(false);
  const [feedbackJustGiven, setFeedbackJustGiven] = useState(false);
  const hasUnsavedAiChanges = useRef(false);
  const [isAiLoading, setIsAiLoading] = useState(false);
  const [showAbandonModal, setShowAbandonModal] = useState(false);
  const [abandonReason, setAbandonReason] = useState("");
  const [abandonReasonTouched, setAbandonReasonTouched] = useState(false);
  const abandonTriggerRef = useRef(null);

  const { data: healthData } = useQuery({
    queryKey: ["market-status"],
    queryFn: () =>
      apiFetch(`${API_BASE}/market/status`).then((r) => r.json()),
    staleTime: 60000,
  });

  const regimeFromHealth = (() => {
    if (healthData?.data?.regime_status) return healthData.data.regime_status;
    if (healthData?.regime_status) return healthData.regime_status;
    const isUK = (form.market || "US").toUpperCase() === "UK";
    const indicator = isUK ? healthData?.data?.ftse : healthData?.data?.spy;
    if (indicator != null) return indicator.is_risk_on ? "risk_on" : "risk_off";
    return "";
  })();

  const { data: existingPlan, isLoading: loadingExisting } = useQuery({
    queryKey: ["tradePlan", editId],
    queryFn: () =>
      apiFetch(`${API_BASE}/trade-plans/${editId}`).then((r) => r.json()).then((res) => res.data),
    enabled: !!editId,
  });

  // ST-05 (BLG-FEAT-91): defaultRiskPercent for WhatIfSizingPreview — same
  // settings source as PositionSizingWidget (TradeEntry.js).
  const { data: settingsData } = useQuery({
    queryKey: ["settings"],
    queryFn: () =>
      apiFetch(`${API_BASE}/settings`).then((r) => r.json()).then((res) => res.data),
  });
  const defaultRiskPercent = settingsData?.[0]?.default_risk_percent ?? 1.0;

  useEffect(() => {
    if (existingPlan && !hasUnsavedAiChanges.current) {
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
        planned_quantity: existingPlan.planned_quantity != null ? String(existingPlan.planned_quantity) : "",
        planned_entry_price: existingPlan.planned_entry_price != null ? String(existingPlan.planned_entry_price) : "",
        planned_stop_price: existingPlan.planned_stop_price != null ? String(existingPlan.planned_stop_price) : "",
        early_exit_conditions: existingPlan.early_exit_conditions || "",
        confirmation_criteria: existingPlan.confirmation_criteria || "",
        invalidation_condition: existingPlan.invalidation_condition || "",
        checklist_items: checklistItems,
        checklist_completed: checklistItems.every((i) => i.checked),
        status: existingPlan.status || "draft",
        thesis_feedback: existingPlan.thesis_feedback || null,
        trade_tags: Array.isArray(existingPlan.trade_tags) ? existingPlan.trade_tags : [],
        // ST-07: carry the persisted values forward so re-saving an
        // already-AI-generated, unedited plan doesn't lose them.
        thesis_model_version: existingPlan.thesis_model_version || null,
        thesis_prompt_version: existingPlan.thesis_prompt_version || null,
      });
      setIsClaudeDraft(!!existingPlan.is_ai_draft);
    }
  }, [existingPlan]); // eslint-disable-line react-hooks/exhaustive-deps

  // ST-05 (BLG-FEAT-52): trade-plan tag autocomplete source
  const [tagInput, setTagInput] = useState("");
  const [showTagSuggestions, setShowTagSuggestions] = useState(false);
  const { data: existingTradeTags = [] } = useQuery({
    queryKey: ["trade-plan-tags"],
    queryFn: async () => {
      const res = await apiFetch(`${API_BASE}/trade-plans/tags`);
      const json = await res.json();
      return Array.isArray(json.data) ? json.data : [];
    },
    staleTime: 60 * 1000,
  });

  const handleAddTradeTag = (rawTag) => {
    if (form.trade_tags.length >= TRADE_TAG_MAX_COUNT) return;
    const clean = rawTag.trim().toLowerCase().replace(/\s+/g, "-");
    if (!clean || clean.length > TRADE_TAG_MAX_LENGTH || !/^[a-z0-9-]+$/.test(clean)) return;
    if (form.trade_tags.includes(clean)) return;
    setForm((prev) => ({ ...prev, trade_tags: [...prev.trade_tags, clean] }));
    setTagInput("");
    setShowTagSuggestions(false);
  };

  const handleRemoveTradeTag = (tagToRemove) => {
    setForm((prev) => ({ ...prev, trade_tags: prev.trade_tags.filter((t) => t !== tagToRemove) }));
  };

  const handleTradeTagInputKeyDown = (e) => {
    if (e.key === "Enter" && tagInput.trim()) {
      e.preventDefault();
      handleAddTradeTag(tagInput.trim());
    }
  };

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
      hasUnsavedAiChanges.current = false;
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

  // ST-07 (BLG-FE-143, EPIC-03, v8.5): narrative fields are the ones
  // generate-plan populates with AI content (setup_thesis, entry_rationale,
  // confirmation_criteria, early_exit_conditions). A manual edit to any of
  // them means the saved content is no longer purely AI-generated, so the
  // thesis_model_version/thesis_prompt_version must be cleared -- same
  // signal setup_thesis's own onChange already used for isAiDraft/
  // isClaudeDraft (below), extended to also clear the version fields.
  const setNarrativeField = (field) => (e) => {
    setForm((prev) => ({
      ...prev,
      [field]: e.target.value,
      thesis_model_version: null,
      thesis_prompt_version: null,
    }));
    if (isAiDraft) setIsAiDraft(false);
    if (isClaudeDraft) setIsClaudeDraft(false);
  };

  const handleChecklistToggle = (idx) => {
    setForm((prev) => {
      const items = prev.checklist_items.map((item, i) =>
        i === idx ? { ...item, checked: !item.checked } : item
      );
      return { ...prev, checklist_items: items, checklist_completed: items.every((i) => i.checked) };
    });
  };

  const handleSubmit = () => {
    const toNum = (v, parse) => (v === "" || v == null ? null : (n => isNaN(n) ? null : n)(parse(v)));
    const payload = {
      ...form,
      regime_context_at_entry: form.regime_context_at_entry || regimeFromHealth || null,
      r_target: toNum(form.r_target, parseFloat),
      planned_quantity: toNum(form.planned_quantity, v => parseInt(v, 10)),
      planned_entry_price: toNum(form.planned_entry_price, parseFloat),
      planned_stop_price: toNum(form.planned_stop_price, parseFloat),
      is_ai_draft: isClaudeDraft,
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
            {editId && existingPlan && isStartTradeEligible(existingPlan) && (
              <Button
                variant="outline"
                size="sm"
                data-testid="start-trade-from-plan-btn"
                onClick={() =>
                  navigate("/TradeEntry", {
                    state: {
                      trade_plan_prefill: {
                        id: existingPlan.id,
                        ticker: existingPlan.ticker,
                        market: existingPlan.market || "US",
                        entry_price: existingPlan.planned_entry_price,
                        stop_price: existingPlan.planned_stop_price,
                        quantity: existingPlan.planned_quantity,
                      },
                    },
                  })
                }
                className="border-emerald-500/40 text-emerald-400 hover:bg-emerald-500/10 hover:text-emerald-300"
              >
                <Rocket className="w-4 h-4 mr-1" />
                Start Trade from Plan
              </Button>
            )}
            {editId && !isAbandoned && (
              <Button
                ref={abandonTriggerRef}
                variant="outline"
                size="sm"
                onClick={() => setShowAbandonModal(true)}
                className="border-amber-500/50 text-amber-400 hover:bg-amber-500/10 hover:text-amber-300"
              >
                <AlertTriangle className="w-4 h-4 mr-1" />
                Abandon Plan
              </Button>
            )}
            {editId && existingPlan && (
              <Button
                variant="outline"
                size="sm"
                data-testid="print-export-pdf-btn"
                onClick={() => window.print()}
                className="border-slate-700 text-slate-300 hover:bg-slate-800"
              >
                <Printer className="w-4 h-4 mr-1" />
                Print / Export PDF
              </Button>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate(-1)}
              className="text-slate-600 dark:text-slate-400 hover:text-white"
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
              aria-label="Market"
              className="w-full px-3 py-2 text-sm bg-slate-800 border border-slate-700 rounded-lg text-white focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
              value={form.market}
              onChange={set("market")}
            >
              <option value="US">US</option>
              <option value="UK">UK</option>
            </select>
          </Field>
          <Field label="Status">
            <select
              aria-label="Status"
              className="w-full px-3 py-2 text-sm bg-slate-800 border border-slate-700 rounded-lg text-white focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:opacity-50"
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
          <Field label="Regime at Entry">
            <div className="px-3 py-2 text-sm bg-slate-800/50 border border-slate-700 rounded-lg text-slate-300 min-h-[38px] flex items-center">
              {form.regime_context_at_entry || regimeFromHealth || <span className="text-slate-600 dark:text-slate-400 italic">loading…</span>}
            </div>
          </Field>
        </div>

        {/* Trade Plan Tags — ST-05 (v6.8, BLG-FEAT-52). Independent from position/journal
            tags (journal_components.md); data-only field on trade_plans.trade_tags. */}
        <Field label={`Tags (${form.trade_tags.length}/${TRADE_TAG_MAX_COUNT})`}>
          <div className="space-y-2" data-testid="trade-plan-tags">
            {form.trade_tags.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {form.trade_tags.map((tag) => (
                  <span
                    key={tag}
                    className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium bg-cyan-500/20 text-cyan-400 border border-cyan-500/30"
                  >
                    {tag}
                    {!isAbandoned && (
                      <button
                        type="button"
                        data-testid={`trade-plan-tag-remove-${tag}`}
                        onClick={() => handleRemoveTradeTag(tag)}
                        className="hover:text-cyan-300 transition-colors"
                        aria-label={`Remove tag ${tag}`}
                      >
                        <XIcon className="w-3 h-3" />
                      </button>
                    )}
                  </span>
                ))}
              </div>
            ) : (
              <p className="text-sm text-slate-600 dark:text-slate-400 italic">No tags</p>
            )}

            {!isAbandoned && form.trade_tags.length < TRADE_TAG_MAX_COUNT && (
              <div className="relative">
                <div className="relative">
                  <TagIcon className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    data-testid="trade-plan-tag-input"
                    type="text"
                    value={tagInput}
                    onChange={(e) => {
                      setTagInput(e.target.value);
                      setShowTagSuggestions(e.target.value.length > 0);
                    }}
                    onFocus={() => setShowTagSuggestions(tagInput.length > 0)}
                    onBlur={() => setTimeout(() => setShowTagSuggestions(false), 200)}
                    onKeyDown={handleTradeTagInputKeyDown}
                    placeholder="Type to add tags…"
                    className="w-full pl-9 pr-3 py-2 text-sm bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                  />
                </div>
                {showTagSuggestions && (
                  <div className="absolute z-10 mt-1 w-full max-h-40 overflow-y-auto rounded-lg bg-slate-800 border border-slate-700 shadow-lg">
                    {existingTradeTags
                      .filter((t) => t.toLowerCase().includes(tagInput.toLowerCase()) && !form.trade_tags.includes(t))
                      .map((t) => (
                        <button
                          type="button"
                          key={t}
                          onClick={() => handleAddTradeTag(t)}
                          className="block w-full text-left px-3 py-2 text-sm text-slate-300 hover:bg-slate-700"
                        >
                          {t}
                        </button>
                      ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </Field>

        {!editId && <SignalContextPanel signal={linkedSignal} market={form.market} />}

        <Field label="Setup Type">
          <select
            data-testid="setup-type-select"
            aria-label="Setup Type"
            className="w-full px-3 py-2 text-sm bg-slate-800 border border-slate-700 rounded-lg text-white focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
            value={form.setup_type || ""}
            onChange={(e) => setForm((prev) => ({ ...prev, setup_type: e.target.value || null }))}
          >
            {SETUP_TYPES.map((t) => (
              <option key={t.value} value={t.value}>{t.label}</option>
            ))}
          </select>
        </Field>

        {/* Setup Quality Score — ST-09 (v6.1) */}
        <SetupQualityScorePanel ticker={form.ticker} />

        <NewsContextPanel ticker={form.ticker} market={form.market} />

        {/* Pre-Entry Validation — ST-03 / ST-16 */}
        <Field label="Planned Shares (for pre-entry checks)">
          <TextInput
            type="number"
            value={form.planned_quantity}
            onChange={set("planned_quantity")}
            placeholder="e.g. 50"
          />
        </Field>
        <div className="grid grid-cols-2 gap-3">
          <Field label="Planned Entry Price (optional)">
            <TextInput
              type="number"
              data-testid="planned-entry-price-input"
              value={form.planned_entry_price}
              onChange={set("planned_entry_price")}
              placeholder="e.g. 150.00"
            />
          </Field>
          <Field label="Planned Stop Price (optional)">
            <TextInput
              type="number"
              data-testid="planned-stop-price-input"
              value={form.planned_stop_price}
              onChange={set("planned_stop_price")}
              placeholder="e.g. 142.00"
            />
          </Field>
        </div>
        <PreEntryValidationPanel
          ticker={form.ticker}
          market={form.market}
          quantity={form.planned_quantity}
          entryPrice={form.planned_entry_price}
          stopPrice={form.planned_stop_price}
          overrideAcknowledged={form.pre_entry_override_acknowledged}
          onOverrideChange={(val) => setForm((prev) => ({ ...prev, pre_entry_override_acknowledged: val }))}
        />

        <div className="space-y-1">
          <div className="flex items-center justify-between">
            <label className="text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wide">Setup Thesis</label>
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
                  // ST-07: this is a client-side template fill, not a Claude
                  // call -- clear any prior thesis_model_version/
                  // thesis_prompt_version so a save after this never records
                  // AI-generation metadata for content Claude didn't produce.
                  setForm((prev) => ({
                    ...prev,
                    setup_thesis: draft,
                    thesis_feedback: null,
                    thesis_model_version: null,
                    thesis_prompt_version: null,
                  }));
                  setIsAiDraft(true);
                  setIsClaudeDraft(false);
                }}
                className="flex items-center gap-1 text-xs text-violet-400 hover:text-violet-300 transition-colors"
                title="Generate thesis from setup type and signal data"
              >
                <Sparkles size={12} />
                Generate thesis
              </button>
              {HAS_AI && form.ticker && (
                <button
                  type="button"
                  data-testid="improve-with-ai-btn"
                  disabled={isAiLoading}
                  className="flex items-center gap-1 text-xs text-cyan-400 hover:text-cyan-300 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  onClick={async () => {
                    setIsAiLoading(true);
                    try {
                      const res = await apiFetch(`${API_BASE}/trade-plans/generate-plan`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                          ticker: form.ticker,
                          market: form.market,
                          setup_type: form.setup_type,
                          signal_data: linkedSignal || null,
                          planned_entry_price: form.planned_entry_price !== "" ? parseFloat(form.planned_entry_price) : null,
                          planned_stop_price: form.planned_stop_price !== "" ? parseFloat(form.planned_stop_price) : null,
                          planned_quantity: form.planned_quantity !== "" ? parseInt(form.planned_quantity, 10) : null,
                          r_target: form.r_target !== "" ? parseFloat(form.r_target) : null,
                        }),
                      });
                      const json = await res.json();
                      const d = json?.data;
                      if (d?.available && d?.fields) {
                        const f = d.fields;
                        setForm((prev) => {
                          const updatedChecklist = linkedSignal
                            ? prev.checklist_items.map((item) =>
                                item.id === "signal_confirmed" ? { ...item, checked: true } : item
                              )
                            : prev.checklist_items;
                          return {
                            ...prev,
                            ...(f.setup_thesis ? { setup_thesis: f.setup_thesis } : {}),
                            ...(f.entry_rationale ? { entry_rationale: f.entry_rationale } : {}),
                            ...(f.confirmation_criteria ? { confirmation_criteria: f.confirmation_criteria } : {}),
                            ...(f.early_exit_conditions ? { early_exit_conditions: f.early_exit_conditions } : {}),
                            ...(f.regime_context_at_entry ? { regime_context_at_entry: f.regime_context_at_entry } : {}),
                            ...(f.r_target != null ? { r_target: f.r_target } : {}),
                            checklist_items: updatedChecklist,
                            thesis_feedback: null,
                            // ST-07 (BLG-FE-143): this IS the real Claude
                            // path -- record what generated it so a save
                            // right after this (no further manual edits)
                            // persists genuine AI-generation provenance.
                            thesis_model_version: d.model_version || null,
                            thesis_prompt_version: d.prompt_version || null,
                          };
                        });
                        setIsAiDraft(true);
                        setIsClaudeDraft(true);
                        setFeedbackJustGiven(false);
                        hasUnsavedAiChanges.current = true;
                      }
                    } catch (_) {}
                    setIsAiLoading(false);
                  }}
                >
                  <Sparkles size={12} />
                  {isAiLoading ? "Generating…" : "Improve with AI"}
                </button>
              )}
            </div>
          </div>
          {isClaudeDraft && (
            <div className="flex items-center gap-3" data-testid="thesis-feedback-control">
              {form.thesis_feedback && feedbackJustGiven ? (
                <span className="text-xs text-slate-600 dark:text-slate-400" data-testid="thesis-feedback-confirmation">
                  Thanks — feedback recorded.
                </span>
              ) : (
                <>
                  <button
                    type="button"
                    data-testid="thesis-feedback-useful"
                    disabled={!!form.thesis_feedback}
                    aria-pressed={form.thesis_feedback === "useful"}
                    onClick={() => {
                      setForm((prev) => ({ ...prev, thesis_feedback: "useful" }));
                      setFeedbackJustGiven(true);
                      setTimeout(() => setFeedbackJustGiven(false), 2000);
                    }}
                    className={`flex items-center gap-1 text-xs transition-colors disabled:cursor-not-allowed ${
                      form.thesis_feedback === "useful" ? "text-emerald-400" : "text-slate-600 dark:text-slate-400 hover:text-slate-600 dark:text-slate-400"
                    }`}
                  >
                    <ThumbsUp size={12} />
                    Useful
                  </button>
                  <button
                    type="button"
                    data-testid="thesis-feedback-not-useful"
                    disabled={!!form.thesis_feedback}
                    aria-pressed={form.thesis_feedback === "not_useful"}
                    onClick={() => {
                      setForm((prev) => ({ ...prev, thesis_feedback: "not_useful" }));
                      setFeedbackJustGiven(true);
                      setTimeout(() => setFeedbackJustGiven(false), 2000);
                    }}
                    className={`flex items-center gap-1 text-xs transition-colors disabled:cursor-not-allowed ${
                      form.thesis_feedback === "not_useful" ? "text-rose-400" : "text-slate-600 dark:text-slate-400 hover:text-slate-600 dark:text-slate-400"
                    }`}
                  >
                    <ThumbsDown size={12} />
                    Not useful
                  </button>
                </>
              )}
            </div>
          )}
          <textarea
            data-testid="setup-thesis-textarea"
            className="w-full px-3 py-2 text-sm bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring resize-none"
            rows={3}
            value={form.setup_thesis}
            onChange={setNarrativeField("setup_thesis")}
            placeholder="Describe the setup — what technical or fundamental condition makes this a candidate?"
          />
        </div>

        <Field label="Entry Rationale">
          <TextArea
            rows={3}
            value={form.entry_rationale}
            onChange={setNarrativeField("entry_rationale")}
            placeholder="Why enter now? What specific trigger confirms the thesis?"
          />
        </Field>

        <Field label="Confirmation Criteria">
          <TextArea
            rows={2}
            value={form.confirmation_criteria}
            onChange={setNarrativeField("confirmation_criteria")}
            placeholder="What must be true before pressing the button? (e.g. volume > 1.5× avg, no earnings within 5 days)"
          />
        </Field>

        <Field label="Early Exit Conditions">
          <TextArea
            rows={2}
            value={form.early_exit_conditions}
            onChange={setNarrativeField("early_exit_conditions")}
            placeholder="Under what conditions would you exit before the stop is hit?"
          />
        </Field>

        <Field label="Invalidation Condition">
          <TextArea
            rows={2}
            data-testid="invalidation-condition-input"
            value={form.invalidation_condition}
            onChange={set("invalidation_condition")}
            placeholder="What would prove this thesis wrong? (optional)"
          />
        </Field>

        {/* What-If Sizing Preview — ST-05 (v8.9, BLG-FEAT-91), trade_plan.md §5d */}
        <WhatIfSizingPreview
          ticker={form.ticker}
          market={form.market}
          stopLevel={form.planned_stop_price}
          defaultRiskPercent={defaultRiskPercent}
        />

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

      {/* Abandon modal — Radix Dialog primitive for focus trap/restoration (ST-07, BLG-FE-136, EPIC-02, v8.0) */}
      <Dialog
        open={showAbandonModal}
        onOpenChange={(open) => {
          if (!open && !abandonMutation.isPending) {
            setShowAbandonModal(false);
            setAbandonReason("");
            setAbandonReasonTouched(false);
          }
        }}
      >
        <DialogContent
          className="w-full max-w-md !rounded-2xl bg-slate-900 border border-slate-700 p-6 space-y-4 mx-4"
          onCloseAutoFocus={(e) => {
            // Radix's default onCloseAutoFocus focuses context.triggerRef, which is only
            // populated by <DialogTrigger> — this modal is opened via a plain Button (not
            // DialogTrigger) so that ref is never set. Focus the actual trigger button
            // directly instead, per the decision record's focus-restoration requirement.
            e.preventDefault();
            abandonTriggerRef.current?.focus();
          }}
        >
          <div className="flex items-center gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-400 flex-shrink-0" />
            <DialogTitle className="text-lg font-semibold text-white">
              Abandon trade plan for {form.ticker}?
            </DialogTitle>
          </div>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            This plan will be marked as abandoned. You will not be prompted to enter this position again based on this plan.
          </p>
          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-600 dark:text-slate-400 uppercase tracking-wide">
              Reason for abandoning <span className="text-rose-400">*</span>
            </label>
            <textarea
              rows={3}
              className="w-full px-3 py-2 text-sm bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring resize-none"
              placeholder="Describe why you're abandoning this plan (min 10 characters)"
              value={abandonReason}
              onChange={(e) => setAbandonReason(e.target.value)}
              onBlur={() => setAbandonReasonTouched(true)}
            />
            {abandonReasonTouched && !abandonReasonValid && (
              <p className="text-xs text-rose-700 dark:text-rose-400">Reason must be at least 10 characters.</p>
            )}
          </div>
          <div className="flex gap-3 justify-end">
            <Button
              variant="ghost"
              onClick={() => { setShowAbandonModal(false); setAbandonReason(""); setAbandonReasonTouched(false); }}
              className="text-slate-600 dark:text-slate-400"
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
        </DialogContent>
      </Dialog>
    </div>
  );
}
