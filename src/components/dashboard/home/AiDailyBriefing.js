'use strict';

import { useState } from 'react';
import { api } from '../../../api/base44Client';
import { RefreshCw, ChevronDown, ChevronRight, Send, MessageSquare } from 'lucide-react';
import DataState from '../../ui/DataState';
import AiDisclaimer from '../../shared/AiDisclaimer';

const STORAGE_KEY = 'ai-briefing-collapsed-sections-v1';

const TYPE_COLOURS = {
  EXIT: 'bg-red-600 text-white',
  ENTER: 'bg-green-700 text-white',
  MONITOR: 'bg-amber-600 text-white',
  HOLD: 'bg-slate-600 text-white',
};

function loadCollapsed() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

function saveCollapsed(state) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch {}
}

function Section({ label, sectionKey, collapsed, onToggle, children }) {
  return (
    <div className="border border-slate-200 dark:border-slate-700 rounded-lg overflow-hidden">
      <button
        onClick={() => onToggle(sectionKey)}
        className="w-full flex items-center justify-between px-3 py-2 text-xs font-semibold text-slate-600 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        aria-expanded={!collapsed}
        data-testid={`section-toggle-${sectionKey}`}
      >
        <span>{label}</span>
        {collapsed
          ? <ChevronRight className="w-3.5 h-3.5 shrink-0" />
          : <ChevronDown className="w-3.5 h-3.5 shrink-0" />}
      </button>
      {!collapsed && (
        <div className="px-3 pb-3" data-testid={`section-content-${sectionKey}`}>
          {children}
        </div>
      )}
    </div>
  );
}

export default function AiDailyBriefing() {
  const [briefing, setBriefing] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [collapsed, setCollapsed] = useState(() => loadCollapsed());
  const [chatQuestion, setChatQuestion] = useState('');
  const [chatResponse, setChatResponse] = useState(null);
  const [chatLoading, setChatLoading] = useState(false);
  const [chatError, setChatError] = useState(null);

  const toggleSection = (key) => {
    setCollapsed(prev => {
      const next = { ...prev, [key]: !prev[key] };
      saveCollapsed(next);
      return next;
    });
  };

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

  const sendChat = async () => {
    if (!chatQuestion.trim()) return;
    setChatLoading(true);
    setChatError(null);
    setChatResponse(null);
    try {
      const data = await api.ai.chat(chatQuestion.trim(), briefing?.summary || null);
      setChatResponse(data.response);
    } catch {
      setChatError('Unable to get a response. Try again.');
    } finally {
      setChatLoading(false);
    }
  };

  const generatedTime = briefing?.generated_at
    ? new Date(briefing.generated_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    : null;

  return (
    <div
      className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 p-4 space-y-3"
      data-testid="ai-daily-briefing-card"
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <span className="text-sm font-semibold text-slate-900 dark:text-white">Today's Briefing</span>
        <div className="flex items-center gap-3">
          {generatedTime && (
            <span className="text-xs text-slate-600 dark:text-slate-400">Generated {generatedTime}</span>
          )}
          <button
            onClick={regenerate}
            disabled={loading}
            className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-md border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed"
            data-testid="regenerate-briefing-btn"
          >
            <RefreshCw className={`w-3 h-3 ${loading ? 'animate-spin' : ''}`} />
            Regenerate
          </button>
        </div>
      </div>

      {/* Advisory label — non-dismissible */}
      <AiDisclaimer variant="badge" />

      {/* Body */}
      {loading && (
        <div className="space-y-2 animate-pulse" data-testid="briefing-loading">
          <div className="h-3 bg-slate-200 dark:bg-slate-700 rounded w-full" />
          <div className="h-3 bg-slate-200 dark:bg-slate-700 rounded w-5/6" />
          <div className="mt-3 space-y-2">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-4/5" />
            ))}
          </div>
        </div>
      )}

      {!loading && error && (
        <p className="text-sm text-rose-400" data-testid="briefing-error">{error}</p>
      )}

      {!loading && !error && !briefing && (
        <div data-testid="briefing-empty">
          <DataState
            compact
            empty
            emptyIcon={<MessageSquare className="w-8 h-8 text-slate-600 dark:text-slate-400" />}
            emptyHeading="No briefing for today"
            emptyBody="Click Regenerate to generate your daily summary."
          />
        </div>
      )}

      {!loading && !error && briefing && (
        <div className="space-y-2" data-testid="briefing-content">

          {/* Market Context */}
          <Section
            label="Market Context"
            sectionKey="market_context"
            collapsed={!!collapsed.market_context}
            onToggle={toggleSection}
          >
            {briefing.summary
              ? <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed pt-2">{briefing.summary}</p>
              : <p className="text-xs text-slate-600 dark:text-slate-400 italic pt-2">No market context available.</p>}
          </Section>

          {/* Signals */}
          <Section
            label="Signals"
            sectionKey="signals"
            collapsed={!!collapsed.signals}
            onToggle={toggleSection}
          >
            {briefing.actions && briefing.actions.length > 0 ? (
              <ol className="space-y-1.5 pt-2" data-testid="briefing-actions">
                {briefing.actions.map((action, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-slate-700 dark:text-slate-300">
                    <span
                      className={`mt-0.5 shrink-0 text-xs font-bold px-1.5 py-0.5 rounded ${TYPE_COLOURS[action.type] || 'bg-slate-600 text-white'}`}
                    >
                      {action.type}
                    </span>
                    <span>
                      <span className="font-semibold text-slate-900 dark:text-white">{action.ticker}</span>
                      {' — '}
                      {action.description}
                    </span>
                  </li>
                ))}
              </ol>
            ) : (
              <p className="text-xs text-slate-600 dark:text-slate-400 italic pt-2" data-testid="briefing-no-actions">
                No specific actions required today.
              </p>
            )}
          </Section>

          {/* Chat Prompt */}
          <Section
            label="Ask the AI"
            sectionKey="chat_prompt"
            collapsed={!!collapsed.chat_prompt}
            onToggle={toggleSection}
          >
            <div className="pt-2 space-y-2">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={chatQuestion}
                  onChange={e => setChatQuestion(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && !chatLoading && sendChat()}
                  placeholder="Ask about today's briefing…"
                  className="flex-1 text-sm bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-md px-3 py-1.5 text-slate-900 dark:text-slate-300 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-slate-400"
                  disabled={chatLoading}
                  data-testid="briefing-chat-input"
                />
                <button
                  onClick={sendChat}
                  disabled={chatLoading || !chatQuestion.trim()}
                  className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-md border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed"
                  data-testid="briefing-chat-send"
                >
                  <Send className="w-3 h-3" />
                </button>
              </div>
              {chatError && (
                <p className="text-xs text-rose-400" data-testid="briefing-chat-error">{chatError}</p>
              )}
              {chatResponse && (
                <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed" data-testid="briefing-chat-response">
                  {chatResponse}
                </p>
              )}
            </div>
          </Section>

        </div>
      )}
    </div>
  );
}
