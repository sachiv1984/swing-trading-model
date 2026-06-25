'use strict';

import { useState } from 'react';
import { api } from '../../../api/base44Client';
import { RefreshCw, AlertTriangle } from 'lucide-react';

const TYPE_COLOURS = {
  EXIT: 'bg-red-600 text-white',
  ENTER: 'bg-green-700 text-white',
  MONITOR: 'bg-amber-600 text-white',
  HOLD: 'bg-slate-600 text-white',
};

export default function AiDailyBriefing() {
  const [briefing, setBriefing] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const regenerate = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.ai.dailyBriefing();
      if (!data.advisory) {
        setError('Unable to generate briefing. Try regenerating.');
        return;
      }
      if (data.error && !data.summary) {
        setError(data.error || 'Unable to generate briefing. Try regenerating.');
        return;
      }
      setBriefing(data);
    } catch {
      setError('Unable to generate briefing. Try regenerating.');
    } finally {
      setLoading(false);
    }
  };

  const generatedTime = briefing?.generated_at
    ? new Date(briefing.generated_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    : null;

  return (
    <div
      className="rounded-xl border border-slate-700 bg-slate-900 p-4 space-y-3"
      data-testid="ai-daily-briefing-card"
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <span className="text-sm font-semibold text-white">Today's Briefing</span>
        <div className="flex items-center gap-3">
          {generatedTime && (
            <span className="text-xs text-slate-500">Generated {generatedTime}</span>
          )}
          <button
            onClick={regenerate}
            disabled={loading}
            className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-md border border-slate-600 text-slate-300 hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed"
            data-testid="regenerate-briefing-btn"
          >
            <RefreshCw className={`w-3 h-3 ${loading ? 'animate-spin' : ''}`} />
            Regenerate
          </button>
        </div>
      </div>

      {/* Advisory label — non-dismissible */}
      <div className="flex items-center gap-2">
        <span className="text-xs font-semibold px-2 py-0.5 rounded bg-amber-600 text-white">
          AI Advisory
        </span>
        <span className="text-xs text-slate-500 italic">All actions require your confirmation</span>
      </div>

      {/* Body */}
      {loading && (
        <div className="space-y-2 animate-pulse" data-testid="briefing-loading">
          <div className="h-3 bg-slate-700 rounded w-full" />
          <div className="h-3 bg-slate-700 rounded w-5/6" />
          <div className="mt-3 space-y-2">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-4 bg-slate-700 rounded w-4/5" />
            ))}
          </div>
        </div>
      )}

      {!loading && error && (
        <p className="text-sm text-rose-400" data-testid="briefing-error">{error}</p>
      )}

      {!loading && !error && !briefing && (
        <p className="text-sm text-slate-500" data-testid="briefing-empty">
          No briefing for today. Click Regenerate to generate your daily summary.
        </p>
      )}

      {!loading && !error && briefing && (
        <div className="space-y-3" data-testid="briefing-content">
          {briefing.summary && (
            <p className="text-sm text-slate-300 leading-relaxed">{briefing.summary}</p>
          )}

          {briefing.actions && briefing.actions.length > 0 ? (
            <ol className="space-y-1.5" data-testid="briefing-actions">
              {briefing.actions.map((action, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                  <span
                    className={`mt-0.5 shrink-0 text-xs font-bold px-1.5 py-0.5 rounded ${TYPE_COLOURS[action.type] || 'bg-slate-600 text-white'}`}
                  >
                    {action.type}
                  </span>
                  <span>
                    <span className="font-semibold text-white">{action.ticker}</span>
                    {' — '}
                    {action.description}
                  </span>
                </li>
              ))}
            </ol>
          ) : (
            <p className="text-xs text-slate-500 italic" data-testid="briefing-no-actions">
              No specific actions required today.
            </p>
          )}
        </div>
      )}
    </div>
  );
}
