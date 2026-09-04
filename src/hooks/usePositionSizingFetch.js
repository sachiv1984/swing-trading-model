import { useState, useEffect } from "react";
import { api } from "../api/base44Client";

/**
 * Shared position-sizing debounced-fetch/session-storage boilerplate
 * (ST-06, BLG-TECH-14, v9.1 EPIC-01). Extracted from PositionSizingWidget.js
 * and WhatIfSizingPreview.js, which had independently hand-duplicated both
 * pieces below. Structural extraction only — no behaviour change to either
 * consumer (existing Playwright coverage for both components must pass
 * unchanged, per this story's acceptance criteria).
 */

/**
 * sessionStorage-backed risk-percent state. On mount, reads the last-used
 * session value first; falls back to `defaultRiskPercent` only when no
 * session value exists yet. Once the user has overridden it in-session, a
 * later `defaultRiskPercent` change (e.g. settings reload) does not
 * overwrite it. Cleared automatically when the browser tab is closed.
 *
 * @param {string} sessionKey - sessionStorage key (each caller uses its own
 *   key, e.g. "widget_risk_percent" vs "what_if_preview_risk_percent", so
 *   the two panels' risk % values don't cross-couple — see WhatIfSizingPreview.js).
 * @param {number} [defaultRiskPercent]
 */
export function useSessionRiskPercent(sessionKey, defaultRiskPercent) {
  const [riskPercent, setRiskPercent] = useState(() => {
    const stored = sessionStorage.getItem(sessionKey);
    return stored !== null ? parseFloat(stored) : (defaultRiskPercent ?? 1.0);
  });

  useEffect(() => {
    sessionStorage.setItem(sessionKey, String(riskPercent));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [riskPercent]);

  useEffect(() => {
    if (defaultRiskPercent != null && sessionStorage.getItem(sessionKey) === null) {
      setRiskPercent(defaultRiskPercent);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [defaultRiskPercent]);

  return [riskPercent, setRiskPercent];
}

/**
 * Debounced (300ms) POST /portfolio/size call. `isReady()` and
 * `buildRequest()` are supplied by the caller since "is there enough valid
 * input yet" and "what does the request body look like" differ between the
 * two consumers; only the setTimeout/fetch/loading-state/cleanup skeleton
 * is shared.
 *
 * `checkBeforeDebounce` preserves each caller's existing timing exactly:
 * - PositionSizingWidget.js (`checkBeforeDebounce: false`, the default):
 *   sizingLoading flips true immediately, and the readiness check happens
 *   300ms later inside the debounce callback — an invalid/empty input
 *   briefly shows the loading spinner before clearing.
 * - WhatIfSizingPreview.js (`checkBeforeDebounce: true`): the readiness
 *   check happens synchronously before the debounce timer starts — an
 *   invalid input clears immediately with no loading flash.
 * These were already two different (pre-existing, unrelated to this story)
 * timing behaviours before consolidation; this flag keeps both unchanged
 * rather than silently harmonising them.
 *
 * `onResult(result)` is called with the resolved response (or `null`) only
 * on the success path, after `sizingResult` is set — for
 * PositionSizingWidget.js's auto-fill-shares / usedSuggestion side effects.
 *
 * @param {() => boolean} isReady
 * @param {() => object} buildRequest
 * @param {any[]} deps - effect dependency array
 * @param {{ checkBeforeDebounce?: boolean, onResult?: (result: object|null) => void }} [options]
 */
export function useDebouncedSizing(isReady, buildRequest, deps, options = {}) {
  const { checkBeforeDebounce = false, onResult } = options;
  const [sizingResult, setSizingResult] = useState(null);
  const [sizingLoading, setSizingLoading] = useState(false);

  useEffect(() => {
    if (checkBeforeDebounce && !isReady()) {
      setSizingResult(null);
      setSizingLoading(false);
      return;
    }

    setSizingLoading(true);

    const timer = setTimeout(async () => {
      if (!checkBeforeDebounce && !isReady()) {
        setSizingResult(null);
        setSizingLoading(false);
        return;
      }

      try {
        // doFetch unwraps the {status, data} envelope — response IS the
        // data object directly (not {status, data}).
        const response = await api.portfolio.size(buildRequest());
        const result = response ?? null;
        setSizingResult(result);
        if (result != null && onResult) {
          onResult(result);
        }
      } catch {
        setSizingResult(null);
      } finally {
        setSizingLoading(false);
      }
    }, 300);

    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return { sizingResult, sizingLoading };
}
