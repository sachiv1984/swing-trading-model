import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Tag, ChevronDown, ChevronUp, X } from "lucide-react";
import { api } from "../../api/base44Client";

// §14a Trade Plan Tag Filter — analytics.md v2.0 (ST-05, BLG-FEAT-52)
// Design source: docs/design/2026-07-08__release-v6.8/trade-tagging/ux_spec.md §3
//
// Operates on trade_plans.trade_tags — independent of the position/journal `tags`
// field used by the §14 TagPerformance table below it, which is unaffected.
export default function TradePlanTagFilter() {
  const [selectedTags, setSelectedTags] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);

  const { data: tagsResponse } = useQuery({
    queryKey: ["trade-plan-tags"],
    queryFn: () => api.tradePlans.tags(),
    staleTime: 60 * 1000,
  });
  // Defensive: tolerate non-array fallback mocks / unexpected envelope shapes
  // in existing test suites that stub unmocked endpoints with `{}`.
  const availableTags = Array.isArray(tagsResponse) ? tagsResponse : [];

  const { data: comparisonResponse, isLoading, isError } = useQuery({
    queryKey: ["tag-performance", selectedTags],
    queryFn: () => api.analytics.tagPerformance(selectedTags),
    enabled: selectedTags.length > 0,
    retry: 1,
  });
  const comparison = Array.isArray(comparisonResponse) ? comparisonResponse : [];

  const handleToggleTag = (tag) => {
    setSelectedTags((prev) =>
      prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]
    );
  };

  return (
    <div className="mb-4 space-y-3" data-testid="trade-plan-tag-filter">
      <div className="relative inline-block">
        <button
          type="button"
          data-testid="trade-plan-tag-filter-toggle"
          onClick={() => setShowDropdown(!showDropdown)}
          className="flex items-center gap-2 px-3 py-2 text-sm rounded-lg bg-slate-800/50 border border-slate-700 text-slate-300 hover:border-violet-500/50 transition-colors"
        >
          <Tag className="w-4 h-4 text-violet-400" />
          Filter by trade plan tag
          {showDropdown ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
        </button>

        {showDropdown && (
          <div className="absolute z-10 mt-1 w-56 max-h-56 overflow-y-auto rounded-lg bg-slate-800 border border-slate-700 shadow-lg">
            {availableTags.length === 0 ? (
              <div className="px-3 py-2 text-sm text-slate-600 dark:text-slate-400 italic">No trade plan tags yet</div>
            ) : (
              availableTags.map((tag) => (
                <button
                  type="button"
                  key={tag}
                  data-testid={`trade-plan-tag-filter-option-${tag}`}
                  onClick={() => handleToggleTag(tag)}
                  className={`flex items-center justify-between w-full text-left px-3 py-2 text-sm transition-colors ${
                    selectedTags.includes(tag) ? "bg-violet-500/20 text-violet-300" : "text-slate-300 hover:bg-slate-700"
                  }`}
                >
                  {tag}
                  {selectedTags.includes(tag) && <span>✓</span>}
                </button>
              ))
            )}
          </div>
        )}
      </div>

      {selectedTags.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {selectedTags.map((tag) => (
            <span
              key={tag}
              className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium bg-violet-500/20 text-violet-300 border border-violet-500/30"
            >
              {tag}
              <button
                type="button"
                onClick={() => handleToggleTag(tag)}
                className="hover:text-violet-200 transition-colors"
                aria-label={`Remove filter ${tag}`}
              >
                <X className="w-3 h-3" />
              </button>
            </span>
          ))}
        </div>
      )}

      {selectedTags.length > 0 && (
        <div data-testid="trade-plan-tag-comparison-row">
          {isLoading ? (
            <div className="h-12 rounded-lg bg-slate-800/50 border border-slate-700/50 animate-pulse" />
          ) : isError ? null : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
              {(comparison || []).map((row) => (
                <div
                  key={row.tag}
                  className="rounded-lg bg-slate-800/50 border border-slate-700/50 px-4 py-2"
                >
                  <div className="text-xs font-medium text-violet-300 mb-1">{row.tag}</div>
                  {row.trade_count === 0 ? (
                    <div className="text-xs text-slate-600 dark:text-slate-400">No closed trades for selected tag(s)</div>
                  ) : (
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-slate-300">{row.win_rate}% win rate</span>
                      <span className={row.avg_r_multiple >= 0 ? "text-emerald-400" : "text-rose-400"}>
                        {row.avg_r_multiple != null ? `${row.avg_r_multiple >= 0 ? "+" : ""}${row.avg_r_multiple}R` : "—"}
                      </span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
