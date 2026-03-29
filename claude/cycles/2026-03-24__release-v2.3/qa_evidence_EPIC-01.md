**Owner:** QA Lead + Strategy Rules & System Intent Owner
**Class:** QA Evidence Log (Class 3)
**Status:** In Progress
**Cycle:** 2026-03-24__release-v2.3
**EPIC:** EPIC-01

---

# QA Evidence — EPIC-01: User Features: Compliance & Metrics

---

## ST-01 — BLG-FEAT-11: Strategy Compliance Score (Display-Only)

**Status:** Done
**Commit:** `b6b6958`
**Completed UTC:** 2026-03-29T11:30:00Z
**Delegation class:** autonomous (engine — reclassified per 2026-03-26 frontend delegation decision)

### Spec References

- `docs/specs/frontend/pages/positions.md#Strategy Compliance Panel`
- `docs/design/2026-03-24__release-v2.3/compliance-panel/ux_spec.md`
- `docs/specs/api_contracts/position_endpoints.md#GET /positions/compliance`

### What Was Built

New `GET /positions/compliance` backend endpoint (`compliance_service.py`) computing per-position ATR-based flags: `stop_compliant` (stop_distance/ATR ≤ 2.5), `stop_age_days` (holding_days proxy), and `size_compliant` (entry risk vs risk_percent × portfolio_value). New `StrategyCompliancePanel` React component rendered below the Table View only — collapsible, display-only, §13.3 constraint enforced at every layer. `position_endpoints.md` bumped to v2.0.0; `openapi.yaml` bumped to v2.2.0. `positions.md` API Dependencies table updated.

### Acceptance Criteria Verification

| AC | Criterion | Result | Method |
|----|-----------|--------|--------|
| 1 | Compliance panel visible on positions page | ✅ Pass | Code review — `StrategyCompliancePanel` imported and rendered in `Positions.js` line 372; gated on `viewMode === "table" && openPositions.length > 0` |
| 2 | Per-position: ATR-based stop compliance, stop age, size compliance | ✅ Pass | Code review — `compliance_service.py` computes all three flags per position |
| 3 | No automated notification, alert, or action | ✅ Pass | Code review + agent-mediated sign-off — §13.3 enforced at service, router, OpenAPI, frontend component, and spec layers |
| 4 | Strategy Rules & System Intent Owner DoQ sign-off (SPS=4) | ✅ Pass | Agent-mediated sign-off cleared 2026-03-29 — all §5 quality bar criteria passed |
| 5 | §13.3 scope constraint documented and reflected in implementation | ✅ Pass | Code review — constraint documented in compliance_service.py header, main.py docstring, openapi.yaml, positions.md, ux_spec.md, and component file comment |
| 6 | openapi.yaml updated in same commit | ✅ Pass | Code review — `GET /positions/compliance` added to openapi.yaml v2.2.0 in commit `b6b6958` |

### Strategy Rules & System Intent Owner Sign-Off

**Method:** Agent-mediated (§5.3)
**Decision:** Approved
**Findings applied:** 1 (positions.md API Dependencies table updated — non-blocking)
**Cleared UTC:** 2026-03-29T11:30:00Z

### DoQ Sign-Off Block

**Verification method:** Code review + agent-mediated sign-off
**Unverified AC (post-merge actions):** Visual rendering of compliance panel (expand/collapse states, amber/green/red badge colours) requires staging verification. Logic verified by code review and agent sign-off.
**Post-merge action:** Product Owner to verify panel renders in Table View on staging at next deployment.

---

## ST-02 — BLG-FEAT-09: Metrics Staleness Indicator

**Status:** Done
**Commit:** `07bb1b1`
**Completed UTC:** 2026-03-29T00:00:00Z
**Delegation class:** autonomous (engine — reclassified per 2026-03-26 frontend delegation decision)

### Acceptance Criteria Verification

| AC | Criterion | Result | Method |
|----|-----------|--------|--------|
| 1 | Data freshness indicator visible on analytics and portfolio pages | ✅ Pass | Staging verification (commit `825a546`) — indicator confirmed visible on both Analytics and Positions pages |
| 2 | Shows relative time (e.g. "Updated 2h ago") and absolute time on hover | ✅ Pass | Staging verification — "Data as of just now" renders in grey with clock icon; hover tooltip shows absolute UTC timestamp |
| 3 | Visual warning (amber) if data is stale beyond a configurable threshold | ✅ Pass | Code review — `STALE_THRESHOLD_MS = 4 * 60 * 60 * 1000`; amber badge with `AlertTriangle` icon rendered when `isStale === true`. Amber rendering not staging-verified (requires 4h wait or forced override); logic verified by code review. |
| 4 | openapi.yaml updated if new field added to response schema | ✅ Pass | Code review — `AnalyticsMetricsResponse` description updated in `openapi.yaml`; `analytics_endpoints.md` bumped to v2.0.0 with `last_sync_at` field doc |

### Staging Verification Record

**Commit verified:** `825a546`
**Verified by:** Product Owner
**Date:** 2026-03-29

| Visual item | Result |
|-------------|--------|
| Grey text (fresh state) | ✅ Pass |
| Clock icon | ✅ Pass |
| Hover tooltip (absolute UTC) | ✅ Pass |
| Positions page presence | ✅ Pass |
| Amber stale badge | — Not staging-verified (requires 4h elapsed or forced override) — logic pass by code review |

### DoQ Sign-Off Block

**Verification method:** Code review + staging run (commit `825a546`)
**Unverified AC (post-merge actions):** AC 3 amber rendering — acceptable; conditional logic is deterministic and verified by code review. No post-merge action required.

**Sign-off:** Granted.
**Signed by:** Product Owner (staging verification) + Engine (code review)
**Date:** 2026-03-29
