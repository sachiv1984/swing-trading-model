// Core-loop events (ST-17, v9.18, BLG-FEAT-103): POST /digest/events
// (digest_endpoints.md v0.8). A failed write never changes the page. The
// returned promise always resolves (never rejects), so a caller may wait for
// the write to settle (the Weekly Digest does, so its counts include it) or
// ignore it (the Today list does: navigation never waits).
import { apiFetch } from "./base44Client";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export function recordLoopEvent(eventType) {
  try {
    return apiFetch(`${API_BASE_URL}/digest/events`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ event_type: eventType }),
      keepalive: true,
    }).then(() => undefined, () => undefined);
  } catch {
    return Promise.resolve();
  }
}
