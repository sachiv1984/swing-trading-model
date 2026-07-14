**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-07-14
**Cycle:** 2026-07-14__release-v7.1
**Release:** v7.1
**Sprint Goal:** Eliminate the two P1 nightly-backtest data-integrity bugs feeding the Strategy Benchmark page (EPIC-01), bring the Table View RISK OFF badge into spec compliance (EPIC-02), and close out the four v7.0 post-ship hardening gaps (EPIC-03) — delivering all v7.1 mandatory anchors plus capacity-filling hardening in a single sprint.
**Backlog Slice Source:** original `stage4_backlog_slice.md`

## Merge Order

- **EPIC merge sequence:** EPIC-01 → EPIC-02 → EPIC-03
- **`execution_state.json` owner:** EPIC-01 (first in execution order — EPIC-02/EPIC-03 branches must check for existence and append rather than overwrite)
- **Shared files across EPICs:** None identified — see `sprint_planning_notes.md §Shared file ownership advisory` for the full per-EPIC file ownership breakdown

## Sprint Scope

### EPIC-01 — Nightly Backtest Data Integrity

**Maps to:** S2-01, S2-02
**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 5.5 days
**Risk IDs:** RISK-01, RISK-02
**Execution sequence:** 1

#### ST-01 — Gate nightly backtest ticker eligibility on ticker_universe.created_at

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 1.5 (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

*(The Execution Engine reads AC from `stage4_backlog_slice.md` directly via `spec_references`. Do not duplicate the full AC table here — the sprint backlog is a sequencing and ownership document.)*

**Dependencies:** None

**Notes:** Recommend landing before ST-02 (RISK-02 — both touch `production_strategy.py`'s core signal/simulation path).

**Staging-only ACs:** None — all ACs verifiable via backtest re-run comparison in CI/local test.

---

#### ST-02 — Fix nightly backtest total_pnl_gbp non-reproducibility

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 4.0 (L)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None (soft-coordinate with ST-01 per RISK-02)

**Notes:** RISK-01 — fix vehicle (persist/cache historical prices; append-only trade ledger; wire existing drift-check to an alert threshold) not yet selected. Backend Engineering Patterns Owner selects at kickoff/early execution; record the choice.

**Staging-only ACs:** Conditional on fix vehicle selected (RISK-01) — if option (a) or (b) is chosen and requires a live nightly GH Actions run to confirm reproducibility over consecutive real nights, flag "AC-02 (night-to-night reproducibility under production nightly schedule)" for human staging sign-off if not fully reproducible in a local/CI simulated re-run. Confirm at execution time.

---

### EPIC-02 — Table View Badge Spec Compliance

**Maps to:** S2-03
**Owner:** Head of Engineering / Head of UX & Design
**Estimated effort:** 0.5 days
**Risk IDs:** RISK-03
**Execution sequence:** 2

#### ST-03 — Table View RISK OFF badge colour/label spec compliance

**Owner:** Head of Engineering
**Estimated effort:** 0.5 (S)
**Delegation class:** autonomous (post-design-gate)

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None — Design Gate resolved (RISK-03, `design_gate.md` PASSED 2026-07-14, Option (a) selected: bring Table View into spec compliance — `#1E40AF`, "RISK OFF" label, drop unspecified `ShieldAlert` icon)

**Notes:** Fix `AlertsCell` and update `SC-RO-02`'s expected values in the same commit (per `design_gate.md` Notes). `DEV-EPIC01-ST05-01` closes on merge.

**Staging-only ACs:** None — AC-02/AC-03 are colour/label rendering claims requiring Playwright coverage (existing `SC-RO-02`/`SC-GVP-02` updated in place); no new staging-only evidence needed beyond existing CI coverage.

---

### EPIC-03 — v7.0 Post-Ship Hardening

**Maps to:** S2-04, S2-05, S2-06, S2-07
**Owner:** Backend Engineering Patterns Owner / QA & Testing Owner / Data Model & Domain Schema Owner / API Contracts & Documentation Owner
**Estimated effort:** 8.0 days
**Risk IDs:** RISK-04, RISK-05
**Execution sequence:** 3

#### ST-04 — Position review-cadence nudge: backend/data-integrity hardening pass

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 2.0 (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None — verifiable via code review + production data query.

---

#### ST-05 — Position review-cadence nudge: frontend/QA polish pass

**Owner:** QA & Testing Owner
**Estimated effort:** 2.0 (M)
**Delegation class:** autonomous (UX consistency sub-item routed through design gate, RISK-04)

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None — Design Gate resolved (RISK-04); `docs/design/2026-07-12__release-v7.0/position-review-cadence-nudge/ux_spec.md` (v1.0, Approved) reviewed and confirmed still current

**Notes:** AC-03 (UX consistency review) is substantively satisfied by the design gate sign-off itself (`design_gate.md` STEP 2.1 existing-artefact confirmation) — no further staging run needed at execution beyond confirming AC-01/AC-02/AC-04/AC-05.

**Staging-only ACs:** AC-03 (UX consistency review) — visual/design judgment call; satisfied via design gate sign-off recorded 2026-07-14 (see Notes). No outstanding staging-only evidence gap.

---

#### ST-06 — Realized/unrealized P&L split: spec & metrics hardening pass

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** 2.0 (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** `docs/specs/frontend/pages/reports.md` already updated v0.8→v0.9 during design gate (colour-convention sentence added to both Unrealised P&L Card sections) — AC-04's spec-text gap is closed; execution confirms implementation matches.

**Staging-only ACs:** AC-04 (visual treatment) — colour/layout claim; covered by AC-07's dedicated Playwright scenario (required same story). Flag for human staging sign-off only if AC-07's scenario cannot be delivered in CI.

---

#### ST-07 — Tax-year P&L CSV export: spec & test hardening pass

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 2.0 (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None — all ACs verifiable via code review, CI test, and documentation review.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~12-14 days |
| Total estimated effort (in-scope) | 14.0 days (midpoint); ~15.5 days pessimistic |
| Utilisation | ~100-117% |
| Over-allocation | Yes (accepted by PO) |

## Items Deferred This Sprint

None.

## Deferred Execution Blockers Accepted

*(section omitted — `deferred_execution_blockers` was empty)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Select `BLG-BE-60` fix vehicle (RISK-01) | Backend Engineering Patterns Owner | No |
| Install `pip-audit` in `backend/.venv` | Head of Engineering | No |
| Reconcile `lifecycle_schema.json` state names with actual `status` literals | Head of Specs Team | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — 2026-07-14
**Scope confirmed:** Confirmed — full scope (3 EPICs, 7 stories), 2026-07-14
**Capacity confirmed:** Confirmed — WARN acknowledged, full scope accepted, 2026-07-14
**Deferred execution blockers accepted (if any):** N/A — none present
**Signed off by:** Product Owner
**Date:** 2026-07-14
