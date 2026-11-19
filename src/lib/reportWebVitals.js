// ST-06 (BLG-QA-271, EPIC-01, v9.18): Core Web Vitals reporting
// (docs/specs/frontend/performance_budget.md §4.3).
//
// Every metric is kept on window.__WEB_VITALS__ (latest value per metric name)
// so a developer, a Playwright test or a Lighthouse run can read the field
// values. In development each metric is also logged to the console. No network
// call: there is no analytics endpoint, and none is wanted (a single-user app).
import { onCLS, onFCP, onINP, onLCP, onTTFB } from "web-vitals";

export function recordMetric(metric, { store = typeof window !== "undefined" ? window : null, log = null } = {}) {
  if (!metric || typeof metric.name !== "string") return;
  if (store) {
    store.__WEB_VITALS__ = { ...(store.__WEB_VITALS__ || {}), [metric.name]: { value: metric.value, rating: metric.rating } };
  }
  if (log) {
    const shown = metric.name === "CLS" ? Number(metric.value).toFixed(3) : `${Math.round(metric.value)} ms`;
    log(`[web-vitals] ${metric.name} ${shown} (${metric.rating})`);
  }
}

export default function reportWebVitals() {
  const log = process.env.NODE_ENV === "development" ? console.info : null; // eslint-disable-line no-console
  const handler = (metric) => recordMetric(metric, { log });
  // reportAllChanges: without it web-vitals reports CLS and INP only when the tab is
  // hidden, and LCP only after the first input, so window.__WEB_VITALS__ would lack
  // them while the page is open.
  const opts = { reportAllChanges: true };
  onCLS(handler, opts);
  onFCP(handler, opts);
  onINP(handler, opts);
  onLCP(handler, opts);
  onTTFB(handler, opts);
}
