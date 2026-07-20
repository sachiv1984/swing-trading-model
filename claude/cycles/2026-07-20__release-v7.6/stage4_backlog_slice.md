**Owner:** Head of Specs Team
**Status:** Active
**Release:** v7.6
**Cycle:** 2026-07-20__release-v7.6
**Last Updated:** 2026-07-20
**Amendment note:** Extended same-day 2026-07-20 (PO-directed capacity-fill reopen, DL-073 — see `decision_log.md`). EPIC-03 through EPIC-08 added post-publish, out-of-band (this cycle's release plan had already reached `Published` before this extension — see the "PO-Directed Post-Publish Scope Expansion" note in `release_plan.md`).

---

# Stage 4 Backlog Slice — v7.6

<!-- release-plan-marker: RP:v7.6:2026-07-20__release-v7.6 -->

EPIC-01/ST-01 and EPIC-07/ST-07 are **conditional**, not firm — see `release_plan.md` RISK-01. Sprint Planning may not seal either story until `run design-gate --cycle 2026-07-20__release-v7.6` PASSes for the relevant item(s). All other items (EPIC-02 through EPIC-06, EPIC-08) have no Design Gate dependency — no observable UI acceptance criteria.

## EPIC-01 — PDF / print-friendly export
**Maps to:** S2-01
**Backlog source:** `BLG-FE-119`
**Sequencing:** Conditional on Design Gate PASS (RISK-01); standalone, no dependencies

### ST-01 — Add print/PDF export action to WeeklyDigest and TradePlan
**Acceptance Criteria:**
- A "Print / Export PDF" action is available on both `WeeklyDigest.js` and `TradePlan.js`
- Output is legible and correctly formatted without app chrome (nav/sidebar)

---

## EPIC-02 — Regression suite baseline update
**Maps to:** S2-02
**Backlog source:** `BLG-QA-112`
**Sequencing:** Gate-triggered companion to EPIC-01 (gate fired: `BLG-FE-119` entered release scope); no independent Design Gate dependency (documentation-only, no observable UI)

### ST-02 — Update regression suite baseline for BLG-FE-115-119 interaction surfaces
**Acceptance Criteria:**
- Regression baseline document updated with new scenario entries for the shipped item(s) (`BLG-FE-115`–`BLG-FE-118`, already shipped v7.4/v7.5, plus `BLG-FE-119` this cycle)
- Cross-referenced against the corresponding Playwright spec file(s)

---

## EPIC-03 — P&L export audit trail reconciliation
**Maps to:** S2-03
**Backlog source:** `BLG-FEAT-79`
**Sequencing:** Standalone, no dependencies; no Design Gate dependency (no UI)

### ST-03 — Reconcile realised P&L export against trade_plan closes
**Acceptance Criteria:**
- Reconciliation logic specified comparing `trade_history` realised P&L rows against corresponding `trade_plans` closure data
- Run once against production data with results recorded (pass, or specific mismatches filed as follow-up items)

---

## EPIC-04 — Backend error-response envelope standardisation
**Maps to:** S2-04
**Backlog source:** `BLG-BE-65`
**Sequencing:** Standalone, no dependencies; no Design Gate dependency (no UI)

### ST-04 — Standardise error-response envelope across all routers
**Acceptance Criteria:**
- Audit of current error-response shapes across all `backend/routers/` files complete
- Canonical envelope documented in `backend_engineering_patterns.md`
- Any non-conforming endpoints filed as follow-up items

---

## EPIC-05 — OpenAPI-derived Playwright fixture library
**Maps to:** S2-05
**Backlog source:** `BLG-QA-114`
**Sequencing:** Standalone, no dependencies; no Design Gate dependency (no UI)

### ST-05 — Build shared mock payload fixture library from openapi.yaml
**Acceptance Criteria:**
- Fixture library exists for at least the endpoints touched by `BLG-SPEC-95`'s scope
- Documented as the preferred pattern for new Playwright tests

---

## EPIC-06 — Nightly batch-job idempotency audit
**Maps to:** S2-06
**Backlog source:** `BLG-BE-62`
**Sequencing:** Standalone, no dependencies; no Design Gate dependency (no UI)

### ST-06 — Audit nightly batch jobs for idempotency risk
**Acceptance Criteria:**
- `daily-snapshot.yml`'s three jobs (position analysis, portfolio snapshot, signal generation) plus the nightly backtest import audited for idempotency
- Findings documented per job; any additional non-idempotency risks filed as follow-up items
- Explicitly cross-references `BLG-BE-59`/`BLG-BE-60` as the confirmed instance of this pattern

---

## EPIC-07 — Consolidated monthly AI cost view
**Maps to:** S2-07
**Backlog source:** `BLG-FEAT-77`
**Sequencing:** Standalone, no dependencies; **conditional on Design Gate PASS (RISK-01)** — observable UI (new consolidated view)

### ST-07 — Add consolidated Gemini + Claude monthly cost summary
**Acceptance Criteria:**
- Consolidated view shows both providers' costs and a combined total for the current month, added to an existing settings/reports surface
- Combined total matches the sum of the two existing per-provider sources

---

## EPIC-08 — Ticker/market input sanitisation regression suite
**Maps to:** S2-08
**Backlog source:** `BLG-QA-69`
**Sequencing:** Standalone, no dependencies; no Design Gate dependency (no UI)

### ST-08 — Add standing regression suite for ticker/market input sanitisation
**Acceptance Criteria:**
- Regression suite covers all 4 previously-vulnerable paths (`create_signal`, `create_rebalance_exit_signal`, `update_signal`, AI chat `context_opts.ticker`)
- Suite runs in CI on every PR touching `backend/services/signal_service.py`, `database.py`, or `ai_service.py`
- Director of Quality sign-off

---

// ARTEFACT_STATUS
```json
{
  "cycle_id": "2026-07-20__release-v7.6",
  "phase": "Release",
  "status": "present",
  "generated_utc": "2026-07-20T16:15:00Z",
  "amended_utc": "2026-07-20T17:15:00Z",
  "amendment_note": "PO-directed capacity-fill reopen, DL-073 — EPIC-03 through EPIC-08 added post-publish"
}
```
