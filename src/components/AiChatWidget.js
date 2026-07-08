'use strict';

import { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Send } from 'lucide-react';
import { api } from '../api/base44Client';

export default function AiChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

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
      setMessages(prev => [...prev, { role: 'ai', text: data.response }]);
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
              <span className="text-xs font-bold px-1.5 py-0.5 rounded bg-amber-600 text-white">
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
                <div
                  className={`max-w-[80%] rounded-lg px-3 py-2 text-sm ${
                    msg.role === 'user'
                      ? 'bg-blue-700 text-white'
                      : 'bg-slate-700 text-slate-200'
                  }`}
                >
                  {msg.text}
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
          <div className="px-3 pb-2">
            <p className="text-xs text-slate-600 dark:text-slate-400 italic text-center" data-testid="ai-chat-advisory-footer">
              AI responses are advisory only. All trade decisions require human confirmation.
            </p>
          </div>
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
