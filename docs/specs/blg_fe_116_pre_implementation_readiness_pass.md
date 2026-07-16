**Owner:** Data Model & Domain Schema Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-16
**Story:** ST-05 (BLG-SPEC-92, EPIC-03, v7.3)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# BLG-FE-116 Pre-Implementation Readiness Pass — Custom Price Alerts

## 1. Purpose

Close every pre-implementation information gap for `BLG-FE-116` (user-defined, per-ticker price-threshold alerts) before it can be scoped into a future sprint (candidate: v7.4). This is the highest-priority readiness gate this release (`RISK-03`) because it carries a `§13` human-in-the-loop boundary pre-check. This is a spec/scoping pass only — no code is written here. `BLG-FE-116` itself remains deferred (see `stage4_backlog_slice.md#Deferred-Items`).

## 2. AC-01 — Data Schema Pre-Design

**Finding: existing `alert_rules` table cannot represent this feature — a new table is required.** `alert_rules` (`docs/specs/data_model.md §8`) is a **singleton-per-type** table: `UNIQUE (portfolio_id, type)` — exactly one row per alert type per portfolio. Custom price alerts are fundamentally different: a user may define an arbitrary number of alerts, each scoped to an arbitrary ticker (not limited to open positions), each with its own condition and threshold. This requires a new, many-rows-per-portfolio table.

**Proposed schema (`price_alerts`):**

```sql
CREATE TABLE price_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    ticker VARCHAR(10) NOT NULL,
    condition VARCHAR(10) NOT NULL CHECK (condition IN ('above', 'below')),
    threshold_price NUMERIC(10, 4) NOT NULL CHECK (threshold_price > 0),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    triggered_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_price_alerts_portfolio_active ON price_alerts(portfolio_id, active);
```

| Field | Type | Nullable | Description |
|-------|------|----------|--------------|
| `ticker` | VARCHAR(10) | No | Not constrained to open positions or watchlist — any valid ticker, consistent with `utils.pricing.get_current_price(ticker)` accepting an arbitrary ticker string (see AC-02). |
| `condition` | VARCHAR(10) | No | `above` or `below` — direction of the threshold crossing. |
| `threshold_price` | NUMERIC(10,4) | No | Same precision as `positions.current_price` (`data_model.md` line 75) for consistency. |
| `active` | BOOLEAN | No | Set `false` once triggered (single-fire, not repeating) or by explicit user deactivation — see AC-06 false-positive note. |
| `triggered_at` | TIMESTAMPTZ | Yes | `null` until fired; distinguishes "not yet evaluated" from "evaluated, not yet triggered" only implicitly (both read as `null`) — sufficient for v1 since evaluation runs nightly and `active=false` is the authoritative fired-state signal. |

**Companion migration requirement flagged forward:** `notifications.alert_type` (`data_model.md §9`) has a `CHECK` constraint restricting values to the existing four type keys. `BLG-FE-116`'s implementation migration must extend this constraint to also permit `custom_price_alert`, in the same migration that creates `price_alerts` — otherwise `POST /alerts/evaluate` cannot log a triggered custom alert to `notifications`.

## 3. AC-02 — Background Alert-Evaluation Service Pattern

**Finding: the existing evaluation infrastructure extends cleanly — no duplicate scheduler needed.** `.github/workflows/alert-evaluation.yml` already runs a daily GitHub Actions cron (21:30 UTC weekdays) calling `POST /alerts/evaluate` (per `ST-03 Decision D` — external cron over Render's paid cron, per its own header comment). `BLG-FE-116` should add custom-price-alert evaluation **as a new step inside the existing `POST /alerts/evaluate` handler**, not as a second cron workflow — this reuses the already-scheduled trigger and avoids adding Render/GitHub Actions billing surface.

**Evaluation logic (for `BLG-FE-116` to implement):** for each `price_alerts` row with `active = true`: call `utils.pricing.get_current_price(ticker)` (the same arbitrary-ticker price utility already used by `portfolio_service.py`, `position_service.py`, and `compliance_recheck_service.py` — no new pricing integration required), compare against `threshold_price` per `condition`, and on trigger: write a `notifications` row (`alert_type: 'custom_price_alert'`), set `active = false`, `triggered_at = now()`.

**Health-check surfacing on `GET /health/scheduler` (AC-02's explicit requirement):** `backend/services/health_service.py`'s `get_scheduler_health()` currently only tracks three hardcoded job keys (`trailing_stop`, `rebalance_exit`, `inv_vol_sizing`) sourced from a different cron workflow (`daily-snapshot.yml`/nightly stop-update path), driven by the module-level `_nightly_job_status` dict and the `record_nightly_job(job_name, ...)` helper (which no-ops silently if `job_name` is not a pre-registered key — confirmed by reading the function body). `BLG-FE-116` must: (a) add a `custom_price_alerts` key to `_nightly_job_status`'s initial dict, (b) add a corresponding `"custom_price_alerts": "co-invoked by POST /alerts/evaluate"` entry to `get_scheduler_health()`'s `trigger_endpoints` block, and (c) call `record_nightly_job("custom_price_alerts", ...)` from within the new evaluation step. This makes custom-alert evaluation visible in `GET /health/scheduler` exactly as required, without introducing a second scheduler concept.

## 4. AC-03 — Auth/Rate-Limit Review

**Finding: no global rate limiting exists; a per-endpoint pattern exists and is reusable if needed.** `backend/main.py` has no rate-limiting middleware (only `CORSMiddleware` and the `X-API-Key` auth middleware, confirmed by direct read). `backend/services/rate_limiter.py` defines an `_ai_limiter` currently wired only to `POST /ai/daily-briefing` and `POST /ai/chat` (per `backend/routers/test.py`'s `rate_limit_scenarios()` comment, AC-05 of ST-03/BLG-OPS-81/EPIC-01/v6.3).

**Assessment:** The evaluation path (`POST /alerts/evaluate`) is internal-only, triggered solely by the GitHub Actions cron with the server's own `API_KEY` — no new external-facing rate-limit surface there (same trust boundary as the existing three alert types already evaluated by this endpoint). The **CRUD endpoints** for managing `price_alerts` (create/list/delete, to be added per AC-08) are user-facing and, unlike the four singleton `alert_rules`, are unbounded in count per user — a rate limit (or a hard per-portfolio row cap, e.g. 50 active alerts) is recommended to bound both abuse and the nightly evaluation job's runtime. Recommend reusing the `rate_limiter.py` pattern for `POST /price-alerts` (create) specifically; `GET`/`DELETE` do not need it (read-only / self-limiting by existing-row count). Final limit values are an implementation-time decision for `BLG-FE-116`, not fixed here.

## 5. AC-04 — Cost-Impact Pre-Assessment (Render Compute Trend)

**Finding: incremental, not structural — no new vendor integration.** The evaluation step reuses the already-scheduled cron (no new invocation) and the already-integrated pricing utility (`utils.pricing.get_current_price`, itself backed by yfinance per the pattern already used across `gap_risk_service.py`, `earnings_service.py`, `sector_service.py`). The only new compute cost is: one `get_current_price` call per active `price_alerts` row per evaluation run (once/weekday), plus one DB row read/write per alert. This is bounded by the per-portfolio active-alert cap recommended in AC-03 and is materially smaller than the existing per-position `get_current_price` calls already made for every open position during the same evaluation cycle (`stop_loss_approach` evaluation). No Render tier change or new external API vendor is implicated. Confirmed no-gap; no reference to `docs/ops/arc5_hosting_cost_projection.md` or a new cost-tracking doc is needed for a change of this size — flag for FinOps review only if the recommended alert cap is later removed or set very high.

## 6. AC-05 — §13 Pre-Check (RISK-03)

**PASS.** Confirmed against `claude/strategy/strategy_rules.md §13.1`/`§13.2` ("human-in-the-loop by design"; "not an automated trading bot"). Custom price alerts, per AC-02's design, **only write a `notifications` row and set `active = false`** — identical in kind to the existing `stop_loss_approach`/`grace_period_warning` alert types already evaluated by the same `POST /alerts/evaluate` endpoint, which are established precedent for passive, notification-only automation that does not cross the §13 boundary (no order placement, no position mutation, no automatic execution of any kind). The user must still manually act (e.g. open `TradeEntry.js` or exit a position) on any information the alert surfaces — the alert is advisory only, consistent with `strategy_rules.md` line 267's existing principle ("advisory panel must never prevent, gate, or auto-reject"). No named follow-up required; no decision escalation needed. `BLG-FE-116` does not require a fresh §13 review at its own future implementation time, since this pre-check already confirms the design stays within the existing, already-cleared advisory-notification boundary — re-confirm only if the implementation design deviates from what is scoped here (e.g. if a future revision proposed auto-creating a trade plan from a triggered alert, that would cross the boundary and require a new §13 review).

## 7. AC-06 — Trigger-Accuracy / False-Positive Metric

**Metric definition:** false-positive rate = (alerts triggered where the triggering price reading, on manual spot-check against a secondary source at the same timestamp, was not genuinely past threshold) / (total alerts triggered), tracked manually during the first post-launch review window (no automated ground-truth source exists to compute this continuously — `get_current_price` is itself the system's sole price source, so an automated self-check would be circular). Secondary signal: **repeat-trigger rate** — since `price_alerts` fires once and deactivates (AC-01), a legitimately high number of users immediately re-creating an identical alert after it fires is an indirect signal of a premature/noisy trigger (e.g. threshold too close to a volatile ticker's daily range) and should be tracked as a lightweight proxy metric via `created_at` clustering on `(portfolio_id, ticker, threshold_price)`.

## 8. AC-07 — Mock-Payload Strategy for Playwright Tests

Follow the existing project convention for price-dependent Playwright fixtures (consistent with other price/position-dependent E2E specs, e.g. `tests/e2e/v7.2-dashboard-tradeplan-ux-hardening.spec.js`'s use of fixed seeded data rather than live market calls): `BLG-FE-116`'s Playwright coverage should mock `GET /price-alerts` (list) responses with deterministic fixture rows spanning both `active=true`/`false` and both `condition` values, and mock the triggered-notification case via a fixture `notifications` row with `alert_type: 'custom_price_alert'` rather than depending on a live price crossing a live threshold during CI. No live `get_current_price`/yfinance calls should occur in Playwright coverage.

## 9. AC-08 — API Contract Stub

**No new `## METHOD /path` heading is added to `docs/specs/api_contracts/` in this pass**, per the same rationale established in `docs/specs/blg_fe_109_pre_implementation_readiness_pass.md §3` and `docs/specs/blg_fe_115_pre_implementation_readiness_pass.md §6`: no backend router implementation exists yet, and adding a contract heading without one would fail the OpenAPI Drift Detection gate (CLAUDE.md §2) for a path that isn't real yet.

**Pre-staged shape (for `BLG-FE-116` to apply, in the same commit as its `docs/reference/openapi.yaml` entry and `backend/routers/` implementation):**
- `GET /price-alerts` — list all `price_alerts` rows for the portfolio.
- `POST /price-alerts` — create one; body `{ ticker, condition, threshold_price }`; validates `condition ∈ {above, below}`, `threshold_price > 0`; recommend enforcing the AC-03 per-portfolio active-alert cap here with a `400` response.
- `DELETE /price-alerts/{id}` — remove or deactivate one; follow the `DELETE` response convention in `conventions.md §12` (`{ deleted: true, id }`).
- All three follow the standard `{ status, data }` / `{ status, message }` envelopes in `conventions.md §2`, and require `X-API-Key` per `conventions.md §1` (no new exemption).
- New route(s) must be registered in `backend/routers/test.py` and `SystemStatus.js`'s hardcoded fallback count updated, per CLAUDE.md's endpoint-test-suite rule, in the same commit as the implementation (not this pass).

## 10. AC-09 — `DataState` Empty-State Reuse

Confirmed reusable without a new variant. A "no alerts configured" list view is a standard full-page/table empty state — the existing default-sized `DataState` (`design_system.md` line 132: `loading → error → empty → children`, default `py-16`/`w-10 h-10` sizing) is a direct fit, unlike the command palette's compact-list context (`blg_fe_115_pre_implementation_readiness_pass.md §7`), which needed a new-variant decision. No `design_system.md` change required for this AC.

## 11. Scope Completeness Summary

All 9 acceptance criteria (AC-01 through AC-09) addressed: AC-01 (new `price_alerts` table designed, `notifications.alert_type` CHECK-constraint migration flagged forward), AC-02 (evaluation extends the existing `POST /alerts/evaluate` cron step; `GET /health/scheduler` surfacing designed against the actual `health_service.py` implementation), AC-03 (no global rate limiting exists; reusable per-endpoint pattern identified; per-portfolio alert cap recommended), AC-04 (incremental cost only, no new vendor, confirmed no-gap), AC-05 (§13 pre-check **PASS**, no follow-up, RISK-03 cleared), AC-06 (metric defined with an explicit note on why full automation isn't possible), AC-07 (mock-payload strategy specified, consistent with existing E2E fixture convention), AC-08 (contract stub pre-staged as prose, explicit no-heading rationale), AC-09 (confirmed no-gap). `BLG-FE-116`'s own acceptance criteria at its next sprint planning cycle should reference this readiness pass as its implementation baseline.

## 12. Known Deviations

None. This is a net-new readiness/confirmation artefact; no prior canonical spec governed this work.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-07-16 | 1.0 | Initial readiness pass (ST-05, EPIC-03, v7.3) — §13 pre-check PASS |
