import { useState, useEffect, useCallback } from "react";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Label } from "../../components/ui/label";
import { BellPlus, Edit2 } from "lucide-react";
import { cn } from "../../lib/utils";
import { apiFetch } from "../../api/base44Client";

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const TYPE_LABELS = {
  stop_loss_approach: "Stop Loss Approach",
  grace_period_warning: "Grace Period Warning",
  market_regime_change: "Market Regime Change",
  daily_portfolio_summary: "Daily Portfolio Summary",
};

const THRESHOLD_TYPES = ["stop_loss_approach"];

function validateThreshold(val) {
  if (val === "" || val === null || val === undefined) return null;
  const n = Number(val);
  if (isNaN(n)) return "Please enter a valid number.";
  if (n <= 0) return "Threshold must be greater than 0.";
  if (n > 50) return "Threshold cannot exceed 50%.";
  return null;
}

function ThresholdText({ rule }) {
  if (!THRESHOLD_TYPES.includes(rule.type)) return null;
  const val = rule.threshold_percent ?? 5.0;
  const isDefault = val === 5.0;
  return (
    <span className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
      Within {val}% of stop{isDefault ? " (default)" : ""}
    </span>
  );
}

function SkeletonRows() {
  return (
    <>
      {Array.from({ length: 4 }).map((_, i) => (
        <div key={i} className="flex items-center justify-between px-6 py-5">
          <div className="space-y-2">
            <div className="h-4 w-44 bg-slate-700 rounded animate-pulse" />
            <div className="h-3 w-32 bg-slate-800 rounded animate-pulse" />
          </div>
          <div className="h-7 w-14 bg-slate-700 rounded animate-pulse" />
        </div>
      ))}
    </>
  );
}

function CreateForm({ onSave, onCancel }) {
  const [alertType, setAlertType] = useState('stop_loss_approach');
  const [threshold, setThreshold] = useState('');
  const [validationError, setValidationError] = useState(null);
  const [saveError, setSaveError] = useState(null);
  const [saving, setSaving] = useState(false);

  const showThresholdField = THRESHOLD_TYPES.includes(alertType);

  const handleThresholdChange = (val) => {
    setThreshold(val);
    setValidationError(validateThreshold(val));
  };

  const handleSubmit = async () => {
    if (showThresholdField) {
      const err = validateThreshold(threshold);
      if (err) { setValidationError(err); return; }
    }
    setSaveError(null);
    setSaving(true);
    try {
      const body = {
        type: alertType,
        threshold_percent: showThresholdField && threshold !== '' ? parseFloat(threshold) : 5.0,
      };
      const res = await apiFetch(`${API_BASE_URL}/alerts/rules`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error();
      onSave();
    } catch {
      setSaveError('Failed to save alert rule. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="px-6 py-5 bg-slate-800/40 border-t border-slate-700/50 space-y-4">
      <div className="space-y-1">
        <Label className="text-slate-600 dark:text-slate-400 text-xs">Alert Type</Label>
        <select
          value={alertType}
          onChange={(e) => { setAlertType(e.target.value); setValidationError(null); }}
          className="bg-slate-800/50 border border-slate-700 text-white text-sm rounded px-3 py-2 w-full"
        >
          {Object.entries(TYPE_LABELS).map(([value, label]) => (
            <option key={value} value={value}>{label}</option>
          ))}
        </select>
      </div>

      {showThresholdField && (
        <div className="space-y-1.5">
          <Label className="text-slate-600 dark:text-slate-400 text-xs">
            Notify when within ___ % of stop
          </Label>
          <Input
            type="text"
            inputMode="decimal"
            value={threshold}
            onChange={(e) => handleThresholdChange(e.target.value)}
            placeholder="5"
            className={cn(
              'bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-600 dark:text-slate-400 h-9 w-40',
              validationError && '!border-rose-500/60'
            )}
          />
          {validationError ? (
            <p className="text-xs text-rose-700 dark:text-rose-400">{validationError}</p>
          ) : (
            <p className="text-xs text-slate-600 dark:text-slate-400">Leave blank to use the default (5%).</p>
          )}
        </div>
      )}

      {saveError && <p className="text-xs text-rose-700 dark:text-rose-400">{saveError}</p>}

      <div className="flex gap-2">
        <Button
          onClick={handleSubmit}
          disabled={saving || !!validationError}
          className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 h-8 text-xs"
        >
          {saving ? 'Saving…' : 'Save'}
        </Button>
        <Button
          variant="ghost"
          onClick={onCancel}
          className="text-slate-600 dark:text-slate-400 hover:text-white hover:bg-slate-800 h-8 text-xs"
        >
          Cancel
        </Button>
      </div>
    </div>
  );
}

function EditForm({ rule, onSave, onCancel }) {
  const [threshold, setThreshold] = useState(
    rule ? String(rule.threshold_percent ?? 5.0) : ""
  );
  const [validationError, setValidationError] = useState(null);
  const [saveError, setSaveError] = useState(null);
  const [saving, setSaving] = useState(false);

  const showThresholdField = THRESHOLD_TYPES.includes(rule?.type);

  const handleThresholdChange = (val) => {
    setThreshold(val);
    setValidationError(validateThreshold(val));
  };

  const handleSubmit = async () => {
    const err = validateThreshold(threshold);
    if (err) { setValidationError(err); return; }
    setSaveError(null);
    setSaving(true);
    try {
      const body = { threshold_percent: threshold === "" ? 5.0 : parseFloat(threshold) };
      const res = await apiFetch(`${API_BASE_URL}/alerts/rules/${rule.id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error();
      onSave();
    } catch {
      setSaveError("Failed to save alert rule. Please try again.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="px-6 py-5 bg-slate-800/40 border-t border-slate-700/50 space-y-4">
      {/* Alert type — display only when editing */}
      <div className="space-y-1">
        <Label className="text-slate-600 dark:text-slate-400 text-xs">Alert Type</Label>
        <p className="text-sm text-white font-medium">{TYPE_LABELS[rule?.type] ?? "—"}</p>
      </div>

      {/* Threshold field — only for stop_loss_approach */}
      {showThresholdField && (
        <div className="space-y-1.5">
          <Label className="text-slate-600 dark:text-slate-400 text-xs">
            Notify when within ___ % of stop
          </Label>
          <Input
            type="text"
            inputMode="decimal"
            value={threshold}
            onChange={(e) => handleThresholdChange(e.target.value)}
            placeholder="5"
            className={cn(
              "bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-600 dark:text-slate-400 h-9 w-40",
              validationError && "!border-rose-500/60"
            )}
          />
          {validationError ? (
            <p className="text-xs text-rose-700 dark:text-rose-400">{validationError}</p>
          ) : (
            <p className="text-xs text-slate-600 dark:text-slate-400">Leave blank to use the default (5%).</p>
          )}
        </div>
      )}

      {saveError && (
        <p className="text-xs text-rose-700 dark:text-rose-400">{saveError}</p>
      )}

      <div className="flex gap-2">
        <Button
          onClick={handleSubmit}
          disabled={saving || !!validationError}
          className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 h-8 text-xs"
        >
          {saving ? "Saving…" : "Save"}
        </Button>
        <Button
          variant="ghost"
          onClick={onCancel}
          className="text-slate-600 dark:text-slate-400 hover:text-white hover:bg-slate-800 h-8 text-xs"
        >
          Cancel
        </Button>
      </div>
    </div>
  );
}

export default function AlertThresholdsSection() {
  const [rules, setRules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(false);
  const [openEditId, setOpenEditId] = useState(null);
  const [showCreateForm, setShowCreateForm] = useState(false);

  const fetchRules = useCallback(async () => {
    setLoadError(false);
    try {
      const res = await apiFetch(`${API_BASE_URL}/alerts/rules`);
      if (!res.ok) throw new Error();
      const json = await res.json();
      setRules(json.data);
    } catch {
      setLoadError(true);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchRules(); }, [fetchRules]);

  const handleSaved = async () => {
    setOpenEditId(null);
    setLoading(true);
    await fetchRules();
  };

  return (
    <div className="space-y-4">
      {/* Section heading */}
      <div className="px-1">
        <h2 className="text-base font-semibold text-white">Alert Thresholds</h2>
        <p className="text-sm text-slate-600 dark:text-slate-400 mt-0.5">Configure trigger thresholds for individual alert rules.</p>
      </div>

      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 divide-y divide-slate-700/50 overflow-hidden">
        {loadError ? (
          <div className="p-6 text-rose-400 text-sm">
            Unable to load alert rules. Please refresh.
          </div>
        ) : loading ? (
          <SkeletonRows />
        ) : rules.length === 0 ? (
          <>
            <div className="flex flex-col items-center justify-center py-16 text-center px-6">
              <BellPlus className="w-10 h-10 text-slate-600 mb-3" />
              <h3 className="text-base font-semibold text-white mb-1">No alert rules configured.</h3>
              <p className="text-sm text-slate-600 dark:text-slate-400 mb-5">Add an alert rule to receive notifications.</p>
              {!showCreateForm && (
                <Button
                  onClick={() => setShowCreateForm(true)}
                  className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 h-8 text-xs"
                >
                  Add alert rule
                </Button>
              )}
            </div>
            {showCreateForm && (
              <CreateForm
                onSave={async () => { setShowCreateForm(false); setLoading(true); await fetchRules(); }}
                onCancel={() => setShowCreateForm(false)}
              />
            )}
          </>
        ) : (
          rules.map((rule) => (
            <div key={rule.id}>
              {/* Row */}
              <div className="flex items-center justify-between px-6 py-4">
                <div className="flex flex-col">
                  <span className="text-sm font-semibold text-white">
                    {TYPE_LABELS[rule.type] ?? rule.type}
                  </span>
                  <ThresholdText rule={rule} />
                </div>
                {THRESHOLD_TYPES.includes(rule.type) && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setOpenEditId(openEditId === rule.id ? null : rule.id)}
                    className="text-slate-600 dark:text-slate-400 hover:text-white hover:bg-slate-800 h-7 w-7 p-0"
                  >
                    <Edit2 className="w-3.5 h-3.5" />
                  </Button>
                )}
              </div>

              {/* Inline edit form */}
              {openEditId === rule.id && (
                <EditForm
                  rule={rule}
                  onSave={handleSaved}
                  onCancel={() => setOpenEditId(null)}
                />
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
