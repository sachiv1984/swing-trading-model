'use strict';

/**
 * Shared AI advisory disclaimer (BLG-FE-81).
 *
 * Consolidates the two disclaimer renderings that were previously
 * hand-duplicated in AiDailyBriefing.js ("badge" variant) and
 * AiChatWidget.js ("footer" variant). Each site independently fixed
 * disclaimer contrast in v6.4 (BLG-UX-01 / BLG-UX-02) — the slate values
 * below are those WCAG-AA-passing values, carried over unchanged. This is
 * a structural extraction only; no visual change to either consumer.
 *
 * @param {"badge"|"footer"} variant - which rendered shape to produce
 * @param {string} [testId] - data-testid applied to the disclaimer text node
 */
export default function AiDisclaimer({ variant = 'footer', testId }) {
  if (variant === 'badge') {
    return (
      <div className="flex items-center gap-2">
        <span className="text-xs font-semibold px-2 py-0.5 rounded bg-amber-700 text-white">
          AI Advisory
        </span>
        <span
          className="text-xs text-slate-700 dark:text-slate-300 italic"
          data-testid={testId}
        >
          All actions require your confirmation
        </span>
      </div>
    );
  }

  return (
    <div className="px-3 pb-2">
      <p
        className="text-xs text-slate-600 dark:text-slate-400 italic text-center"
        data-testid={testId}
      >
        AI responses are advisory only. All trade decisions require human confirmation.
      </p>
    </div>
  );
}
