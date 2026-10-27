'use strict';

import { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Send, ThumbsUp, ThumbsDown } from 'lucide-react';
import { api } from '../api/base44Client';
import AiDisclaimer from './shared/AiDisclaimer';

// ST-22 (EPIC-03, v9.13, BLG-FE-208): useful / not-useful rating under each
// model answer. Design: docs/design/2026-10-16__release-v9.13/chat-answer-rating/decision_record.md
// (positions.md §AI Trade Advisor Widget §Answer Rating). The panel is a fixed
// dark surface in both themes, so single dark tokens apply.
const RATING_OPTIONS = [
  { value: 'useful', label: 'Useful', Icon: ThumbsUp, testId: 'chat-rating-useful', selected: 'text-emerald-400' },
  { value: 'not_useful', label: 'Not useful', Icon: ThumbsDown, testId: 'chat-rating-not-useful', selected: 'text-rose-400' },
];

function AnswerRating({ msg, onRate }) {
  const locked = msg.ratingState === 'saving' || msg.ratingState === 'rated';
  return (
    <div className="mt-1">
      <div className="flex gap-3" role="group" aria-label="Rate this answer" data-testid="chat-rating">
        {RATING_OPTIONS.map(({ value, label, Icon, testId, selected }) => {
          const isSelected = msg.rating === value;
          return (
            <button
              key={value}
              type="button"
              aria-pressed={isSelected}
              disabled={locked}
              onClick={() => onRate(value)}
              className={`flex items-center gap-1 text-xs ${
                isSelected ? selected : `text-slate-400${locked ? '' : ' hover:text-slate-200'}`
              } disabled:cursor-default`}
              data-testid={testId}
            >
              <Icon className="w-3 h-3" />
              {label}
            </button>
          );
        })}
        {msg.thanks && (
          <span className="text-xs text-slate-400" data-testid="chat-rating-thanks">Thanks — recorded.</span>
        )}
      </div>
      {msg.ratingState === 'failed' && (
        <p className="text-xs text-rose-400 mt-1" role="status" data-testid="chat-rating-error">
          Couldn't save your rating. Try again.
        </p>
      )}
    </div>
  );
}

export default function AiChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const thanksTimers = useRef([]);

  useEffect(() => () => thanksTimers.current.forEach(clearTimeout), []);

  const updateMessage = (index, patch) =>
    setMessages(prev => prev.map((m, i) => (i === index ? { ...m, ...patch } : m)));

  const handleRate = async (index, answerId, rating) => {
    updateMessage(index, { rating, ratingState: 'saving' });
    try {
      const saved = await api.ai.rateChatAnswer(answerId, rating);
      updateMessage(index, { rating: saved?.rating || rating, ratingState: 'rated', thanks: true });
      thanksTimers.current.push(setTimeout(() => updateMessage(index, { thanks: false }), 3000));
    } catch (err) {
      const stored = err?.status === 409 ? err?.data?.data?.rating : null;
      if (stored) {
        updateMessage(index, { rating: stored, ratingState: 'rated' });
      } else {
        updateMessage(index, { rating: null, ratingState: 'failed' });
      }
    }
  };

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, loading]);

  const handleOpen = () => {
    setOpen(true);
    setError(null);
  };

  const handleClose = () => {
    setOpen(false);
    setMessages([]);
    setInput('');
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const question = input.trim();
    if (!question || loading) return;

    setInput('');
    setError(null);
    setMessages(prev => [...prev, { role: 'user', text: question }]);
    setLoading(true);

    try {
      const data = await api.ai.chat(question);
      setMessages(prev => [...prev, { role: 'ai', text: data.response, answerId: data.answer_id || null, rating: null, ratingState: 'unrated' }]);
    } catch {
      setError('Unable to get a response. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{ position: 'fixed', bottom: 24, right: 24, zIndex: 100 }}
      data-testid="ai-chat-widget"
    >
      {open ? (
        /* Expanded panel */
        <div
          className="flex flex-col rounded-xl border border-slate-700 bg-slate-900 shadow-2xl"
          style={{ width: 350, height: 480 }}
          data-testid="ai-chat-panel"
        >
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-slate-700">
            <div className="flex items-center gap-2">
              <span className="text-sm font-semibold text-white">AI Trade Advisor</span>
              <span className="text-xs font-bold px-1.5 py-0.5 rounded bg-amber-700 text-white">
                Advisory
              </span>
            </div>
            <button
              onClick={handleClose}
              className="text-slate-600 dark:text-slate-400 hover:text-white"
              data-testid="ai-chat-close"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-3 space-y-2" data-testid="ai-chat-messages">
            {messages.length === 0 && !loading && !error && (
              <p className="text-xs text-slate-600 dark:text-slate-400 text-center mt-4" data-testid="ai-chat-empty">
                Ask about your portfolio, positions, or signals.
              </p>
            )}

            {messages.map((msg, i) => (
              <div
                key={i}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className="max-w-[80%]">
                  <div
                    className={`rounded-lg px-3 py-2 text-sm ${
                      msg.role === 'user'
                        ? 'bg-blue-700 text-white'
                        : 'bg-slate-700 text-slate-200'
                    }`}
                    data-testid={msg.role === 'ai' ? 'ai-chat-answer' : undefined}
                  >
                    {msg.text}
                  </div>
                  {msg.role === 'ai' && msg.answerId && (
                    <AnswerRating msg={msg} onRate={rating => handleRate(i, msg.answerId, rating)} />
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex justify-start" data-testid="ai-chat-loading">
                <div className="bg-slate-700 rounded-lg px-3 py-2">
                  <span className="flex gap-1 items-center text-slate-600 dark:text-slate-400 text-xs">
                    <span className="animate-bounce" style={{ animationDelay: '0ms' }}>•</span>
                    <span className="animate-bounce" style={{ animationDelay: '150ms' }}>•</span>
                    <span className="animate-bounce" style={{ animationDelay: '300ms' }}>•</span>
                  </span>
                </div>
              </div>
            )}

            {error && (
              <div className="flex justify-start" data-testid="ai-chat-error">
                <div className="bg-rose-900/40 border border-rose-700/50 rounded-lg px-3 py-2 text-sm text-rose-300">
                  {error}
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <form
            onSubmit={handleSubmit}
            className="flex items-center gap-2 px-3 py-2 border-t border-slate-700"
          >
            <input
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              disabled={loading}
              placeholder="Ask about your portfolio…"
              className="flex-1 bg-slate-800 border border-slate-600 rounded-md px-3 py-1.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 disabled:opacity-50"
              data-testid="ai-chat-input"
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="p-1.5 rounded-md bg-blue-700 hover:bg-blue-600 text-white disabled:opacity-50 disabled:cursor-not-allowed"
              data-testid="ai-chat-submit"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>

          {/* Advisory footer — non-dismissible */}
          <AiDisclaimer variant="footer" testId="ai-chat-advisory-footer" />
        </div>
      ) : (
        /* Collapsed pill button */
        <button
          onClick={handleOpen}
          className="flex items-center gap-2 px-4 py-2.5 rounded-full bg-blue-700 hover:bg-blue-800 text-white text-sm font-medium shadow-lg"
          data-testid="ai-chat-open-btn"
        >
          <MessageCircle className="w-4 h-4" />
          Ask Advisor
        </button>
      )}
    </div>
  );
}
