import { useState, useEffect, useCallback } from "react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select";
import { X } from "lucide-react";
import { apiFetch } from "../../api/base44Client";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

/**
 * Named, server-side Trade History filter presets (ST-04, BLG-FE-118, EPIC-04,
 * v7.5). Distinct from the page's ephemeral active-filter localStorage
 * envelope — these persist across devices/sessions until deleted.
 */
export default function SavedFiltersControl({ hasActiveFilters, currentFilterState, onApply }) {
  const [presets, setPresets] = useState([]);
  const [showNameInput, setShowNameInput] = useState(false);
  const [nameInput, setNameInput] = useState("");
  const [saveError, setSaveError] = useState(null);
  const [saving, setSaving] = useState(false);
  const [confirmingDeleteId, setConfirmingDeleteId] = useState(null);
  const [deleting, setDeleting] = useState(false);

  const fetchPresets = useCallback(async () => {
    try {
      const res = await apiFetch(`${API_BASE_URL}/saved-filters`);
      if (!res.ok) throw new Error();
      const json = await res.json();
      setPresets(Array.isArray(json.data) ? json.data : []);
    } catch {
      // silent — dropdown just shows "No saved filters"
    }
  }, []);

  useEffect(() => { fetchPresets(); }, [fetchPresets]);

  const handleSave = async () => {
    const name = nameInput.trim();
    if (!name) return;
    setSaveError(null);
    setSaving(true);
    try {
      const res = await apiFetch(`${API_BASE_URL}/saved-filters`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, filter_state: currentFilterState }),
      });
      if (res.status === 400) {
        setSaveError(`A preset named '${name}' already exists.`);
        setSaving(false);
        return;
      }
      if (!res.ok) throw new Error();
      setNameInput("");
      setShowNameInput(false);
      await fetchPresets();
    } catch {
      setSaveError("Failed to save preset. Please try again.");
    } finally {
      setSaving(false);
    }
  };

  const handleApply = (presetId) => {
    const preset = presets.find((p) => p.id === presetId);
    if (preset) onApply(preset.filter_state);
  };

  const handleDelete = async (preset) => {
    setDeleting(true);
    try {
      const res = await apiFetch(`${API_BASE_URL}/saved-filters/${preset.id}`, { method: "DELETE" });
      if (!res.ok) throw new Error();
      setConfirmingDeleteId(null);
      await fetchPresets();
    } finally {
      setDeleting(false);
    }
  };

  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center gap-3 flex-wrap">
        {hasActiveFilters && !showNameInput && (
          <button
            onClick={() => setShowNameInput(true)}
            className="text-sm text-cyan-400 hover:text-cyan-300 transition-colors"
          >
            Save current filters as…
          </button>
        )}

        {showNameInput && (
          <div className="flex items-center gap-2">
            <Input
              value={nameInput}
              onChange={(e) => { setNameInput(e.target.value); setSaveError(null); }}
              placeholder="Preset name"
              maxLength={100}
              className="bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-600 dark:text-slate-400 h-8 text-sm max-w-xs"
            />
            <Button
              size="sm"
              onClick={handleSave}
              disabled={saving || !nameInput.trim()}
              className="h-8 bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 text-xs"
            >
              {saving ? "Saving…" : "Save"}
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => { setShowNameInput(false); setNameInput(""); setSaveError(null); }}
              className="h-8 text-slate-600 dark:text-slate-400 hover:text-white text-xs"
            >
              Cancel
            </Button>
          </div>
        )}

        <div className="flex items-center gap-1">
          <Select onValueChange={handleApply}>
            <SelectTrigger className="bg-slate-800/50 border-slate-700 text-white h-8 text-sm w-48">
              <SelectValue placeholder={presets.length === 0 ? "No saved filters" : "Saved filters"} />
            </SelectTrigger>
            <SelectContent className="bg-slate-800 border-slate-700">
              {presets.length === 0 ? (
                <div className="px-3 py-2 text-xs text-slate-600 dark:text-slate-400">No saved filters</div>
              ) : (
                presets.map((p) => (
                  <div key={p.id} className="flex items-center justify-between pr-1">
                    <SelectItem value={p.id} className="flex-1">{p.name}</SelectItem>
                    <button
                      onClick={(e) => { e.stopPropagation(); setConfirmingDeleteId(p.id); }}
                      className="p-1 text-slate-600 dark:text-slate-400 hover:text-rose-400"
                      aria-label={`Delete preset ${p.name}`}
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </div>
                ))
              )}
            </SelectContent>
          </Select>
        </div>
      </div>

      {saveError && <p className="text-xs text-rose-700 dark:text-rose-400">{saveError}</p>}

      {confirmingDeleteId && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
          <div className="w-full max-w-md rounded-2xl bg-slate-900 border border-slate-700 p-6 space-y-4 mx-4">
            <h2 className="text-lg font-semibold text-white">
              Delete preset '{presets.find((p) => p.id === confirmingDeleteId)?.name}'?
            </h2>
            <div className="flex gap-3 justify-end">
              <Button variant="ghost" onClick={() => setConfirmingDeleteId(null)} className="text-slate-600 dark:text-slate-400">
                Cancel
              </Button>
              <Button
                onClick={() => handleDelete(presets.find((p) => p.id === confirmingDeleteId))}
                disabled={deleting}
                className="bg-rose-600 hover:bg-rose-500 text-white border-0"
              >
                {deleting ? "Deleting…" : "Delete"}
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
