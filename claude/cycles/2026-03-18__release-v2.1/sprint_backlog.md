**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-03-18
**Cycle:** 2026-03-18__release-v2.1
**Release:** v2.1
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Sprint Goal:** Deliver v2.1 Alerts, Watchlists & Enhancements: author the notification delivery architecture decision, implement the full alerts and notification system, add watchlist monitoring capability, enhance chart interactivity and financial reporting exports, and close all spec debt and QA coverage gaps — across three planned sprints.
**Backlog Slice Source:** claude/cycles/2026-03-18__release-v2.1/stage4_backlog_slice.md (original; no amendment)

---

# Sprint Backlog — v2.1 Alerts, Watchlists & Enhancements

---

## Sprint 1 — Foundation & Quick Wins

**Sprint 1 goal:** Deliver the notification delivery architecture ADR (unlocking EPIC-02), chart interactivity enhancements, PDF export, and all spec debt and QA coverage items.
**Sprint 1 target capacity:** ~40 hrs | **Estimated effort:** ~39 hrs mid

---

### EPIC-01 — Notification Architecture

**Maps to:** S2-01
**Owner:** Head of Engineering + Backend Engineering Patterns Owner
**Estimated effort:** S (~4 hrs mid)
**Risk IDs:** RISK-01
**Execution sequence:** 1 (must be first; completion unlocks EPIC-02 — hard gate)

#### ST-01 — Author async notification delivery ADR (BLG-TECH-08)

**Owner:** Head of Engineering + Backend Engineering Patterns Owner
**Estimated effort:** S (~4 hrs mid)
**Delegation class:** delegated_decision
**Acceptance Criteria:** see `stage4_backlog_slice.md § ST-01`
**Dependencies:** None — must start immediately; Sprint 2 EPIC-02 is blocked until this is Complete
**Seal condition:** Head of Engineering sign-off required. Sprint Planning Engine (STEP -1.10 / RISK-01 gate) must verify Complete before any EPIC-02 story is sealed.
**Notes:** RISK-01. Decision directly controls how ST-02 (Alerts spec) is written. If sync decided: simpler path. If async decided: PoC required in staging.

---

### EPIC-04 — Chart Interactivity Enhancements

**Maps to:** S2-04
**Owner:** Base44 Frontend
**Estimated effort:** S–M (~7 hrs mid)
**Risk IDs:** RISK-04 (no client-side re-derivation)
**Execution sequence:** 2 (independent; can run parallel to EPIC-01)

#### ST-11 — Implement chart interactivity (CHART-IX)

**Owner:** Base44 Frontend
**Estimated effort:** S–M (~7 hrs mid)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md § ST-11`
**Spec locked:** `docs/specs/frontend/pages/analytics.md` v1.5
**Design source:** `docs/design/2026-03-18__release-v2.1/chart-interactivity/ux_spec.md`
**Dependencies:** None (analytics.md v1.5 already updated by design gate)
**Notes:** RISK-04 — scope boundary enforced: no new indicators, no client-side re-derivation. DoQ evidence method must name whether verification is by code review, local run, or staging. Test scenarios gap flagged — QA & Testing Owner to author chart_interactivity_scenarios.md before Sprint 1 close on this EPIC.

---

### EPIC-05 — Financial Reporting Exports & Feature Enhancements (Sprint 1 portion)

**Maps to:** S2-05
**Owner:** Head of Engineering + Base44 Frontend + Financial Reporting & Records Owner + Infrastructure & Operations Owner
**Sprint 1 items:** ST-12 only
**Execution sequence:** 3

#### ST-12 — BLG-FR-01: Tax Year P&L PDF Export

**Owner:** Head of Engineering + Base44 Frontend + Financial Reporting & Records Owner
**Estimated effort:** M (~10 hrs mid)
**Delegation class:** delegated_backend (primary) + delegated_frontend (download button UX)
**Acceptance Criteria:** see `stage4_backlog_slice.md § ST-12`
**Spec locked:** `docs/specs/frontend/pages/reports.md` v0.2
**Design source:** `docs/design/2026-03-18__release-v2.1/pdf-export/ux_spec.md`
**Dependencies:** None (independent)
**Notes:** `openapi.yaml` must be updated in same commit as endpoint. Financial Reporting & Records Owner sign-off required. Test scenarios gap — PDF export UI verification to be included in EPIC-05 QA scenarios.

---

### EPIC-06 — Spec Debt & QA Coverage

**Maps to:** S2-06
**Owner:** Head of Specs Team + QA & Testing Owner + PMO Lead
**Estimated effort:** S–M (~18 hrs mid for all 4 items)
**Execution sequence:** 4 (parallel track; independent)

#### ST-16 — BLG-SPEC-D12: Bulk lifecycle header remediation

**Owner:** Head of Specs Team
**Estimated effort:** S–M (~8 hrs mid)
**Delegation class:** delegated_decision
**Acceptance Criteria:** see `stage4_backlog_slice.md § ST-16`
**Dependencies:** None
**Notes:** Header-only changes to 28 documents. No content modifications. Head of Specs Team sign-off required.

#### ST-17 — Spec maintenance batch (BLG-SPEC-D13 + BLG-SPEC-G6 + BLG-SPEC-D10 + BLG-SPEC-D11)

**Owner:** Head of Specs Team + Metrics Definitions & Analytics Canonical Owner + Head of Engineering
**Estimated effort:** S (~4 hrs mid)
**Delegation class:** delegated_decision
**Acceptance Criteria:** see `stage4_backlog_slice.md § ST-17`
**Dependencies:** None
**Notes:** BLG-SPEC-G6 requires `openapi.yaml` update in same commit as backend change. Head of Specs Team sign-off on spec changes; Head of Engineering sign-off on BLG-SPEC-G6 implementation.

#### ST-18 — Author missing test scenario documents (TEST-GAP-SIG-01 + TEST-GAP-TAX-01)

**Owner:** QA & Testing Owner
**Estimated effort:** S (~4 hrs mid)
**Delegation class:** delegated_qa
**Acceptance Criteria:** see `stage4_backlog_slice.md § ST-18`
**Dependencies:** None
**Notes:** Covers signals and reports scenarios. Does not cover chart interactivity, watchlist, slippage, or PDF export scenarios — those are separate gap flags (see sprint_planning_notes.md).

#### ST-19 — BLG-PROC-01: Cross-EPIC branch process compliance check

**Owner:** PMO Lead
**Estimated effort:** S (~2 hrs mid)
**Delegation class:** delegated_decision
**Acceptance Criteria:** see `stage4_backlog_slice.md § ST-19`
**Dependencies:** None (review conducted at Sprint 1 close — PMO Lead reviews commit history)
**Notes:** PMO Lead must review commit history at Sprint 1 close for cross-EPIC violations. Outcome recorded in qa_evidence log.

---

## Sprint 2 — Alerts Foundation + EPIC-05 Completion

**Sprint 2 goal:** Complete the alerts spec and backend, finish EPIC-05 (CSV, slippage, PR environments). EPIC-02 is conditional on ST-01 Complete with Head of Engineering sign-off.
**Sprint 2 target capacity:** ~40 hrs | **Estimated effort:** ~37 hrs mid (+ stretch ST-04/05 if bandwidth)

**⚠ SPRINT 2 GATE:** Before any EPIC-02 story in Sprint 2 is sealed, PMO Lead must confirm ST-01 is marked Complete with Head of Engineering sign-off. This is the RISK-01 resolution gate.

---

### EPIC-02 — Alerts & Notifications (Sprint 2 portion)

**Maps to:** S2-02
**Owner:** Head of Engineering + Base44 Frontend + Director of Quality
**Sprint 2 items:** ST-02, ST-03 (+ ST-04/05 as stretch)
**Condition:** ST-01 (BLG-TECH-08 ADR) must be Complete + HoE sign-off before any item below is sealed
**Risk IDs:** RISK-01, RISK-02
**Execution sequence:** 1 (Sprint 2)

#### ST-02 — Spec: alerts endpoint + notification preference model

**Owner:** Head of Specs Team + Head of Engineering
**Estimated effort:** M (~8 hrs mid)
**Delegation class:** delegated_decision
**Acceptance Criteria:** see `stage4_backlog_slice.md § ST-02`
**Dependencies:** ST-01 Complete (hard gate)
**Seal condition:** ⚠ CONDITIONAL — ST-01 must be Complete with Head of Engineering sign-off. Do not seal until confirmed.
**Notes:** Architecture mode (sync/async per ADR) must be reflected in the spec. `openapi.yaml` updated in same commit.

#### ST-03 — Backend: alert rules engine

**Owner:** Head of Engineering
**Estimated effort:** M–H (~14 hrs mid)
**Delegation class:** delegated_backend
**Acceptance Criteria:** see `stage4_backlog_slice.md § ST-03`
**Dependencies:** ST-02 (spec signed off)
**Seal condition:** ⚠ CONDITIONAL — ST-01 must be Complete. ST-02 must be signed off.
**Notes:** All 4 alert types required. Engine must be testable in isolation. Unit tests required.

#### ST-04 — Backend: notification delivery (email) [Sprint 2 stretch / Sprint 3]

**Owner:** Head of Engineering
**Estimated effort:** M (~10 hrs mid)
**Delegation class:** delegated_backend
**Acceptance Criteria:** see `stage4_backlog_slice.md § ST-04`
**Dependencies:** ST-01 (architecture decision), ST-02 (spec)
**Seal condition:** ⚠ CONDITIONAL — ST-01 Complete. ST-02 signed off.
**Notes:** Stretch item for Sprint 2. Primary target: Sprint 3. Delivery in Sprint 2 only if bandwidth permits after ST-02 and ST-03.

#### ST-05 — Frontend: notification preferences page [Sprint 2 stretch / Sprint 3]

**Owner:** Base44 Frontend
**Estimated effort:** S–M (~6 hrs mid)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md § ST-05`
**Spec locked:** `docs/specs/frontend/pages/notifications.md` v0.1
**Design source:** `docs/design/2026-03-18__release-v2.1/notification-preferences/ux_spec.md`
**Dependencies:** ST-02 (preference model defined)
**Seal condition:** ⚠ CONDITIONAL — ST-01 Complete. ST-02 signed off.
**Notes:** Stretch item for Sprint 2. Primary target: Sprint 3. Test scenarios gap: ST-07 covers this feature.

---

### EPIC-05 — Financial Reporting Exports & Feature Enhancements (Sprint 2 portion)

**Maps to:** S2-05
**Sprint 2 items:** ST-13, ST-14, ST-15
**Execution sequence:** 2 (Sprint 2; parallel to EPIC-02)

#### ST-13 — BLG-FR-02: Tax Year P&L CSV Export

**Owner:** Head of Engineering
**Estimated effort:** S (~4 hrs mid)
**Delegation class:** delegated_backend
**Acceptance Criteria:** see `stage4_backlog_slice.md § ST-13`
**Dependencies:** None (independent backend; completes EPIC-05 reporting export pair with ST-12)
**Notes:** `openapi.yaml` updated in same commit. No schema migration required.

#### ST-14 — BLG-FEAT-03: Slippage Tracking

**Owner:** Head of Engineering + Data Model & Domain Schema Owner + Base44 Frontend
**Estimated effort:** S–M (~8 hrs mid)
**Delegation class:** delegated_backend (primary) + delegated_decision (data model gate)
**Acceptance Criteria:** see `stage4_backlog_slice.md § ST-14`
**Spec locked (display):** `docs/specs/frontend/pages/trade_history.md` v1.2
**Design source:** `docs/design/2026-03-18__release-v2.1/slippage-tracking/ux_spec.md`
**Dependencies:** data_model.md Fill Price field spec (Data Model Owner + Head of Specs Team sign-off required before implementation begins — embedded gate within story)
**Notes:** RISK-05. data_model.md must define Fill Price before code implementation. Test scenarios gap — QA & Testing Owner to cover slippage display in EPIC-05 scenarios.

#### ST-15 — BLG-OPS-03: Render PR Preview Environments

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~3 hrs mid)
**Delegation class:** delegated_decision
**Acceptance Criteria:** see `stage4_backlog_slice.md § ST-15`
**Dependencies:** None
**Notes:** Configuration in Render dashboard (infrastructure action, not code). `OPERATIONAL_GUIDE.md §8` update required. DoQ sign-off checklist update required.

---

## Sprint 3 — Alerts Completion + Watchlists

**Sprint 3 goal:** Complete the full alerts implementation (email delivery, frontend pages, QA scenarios), deliver the watchlist backend and frontend.
**Sprint 3 target capacity:** ~40 hrs | **Estimated effort:** ~43 hrs core / ~53 hrs with ST-10 stretch

**⚠ SPRINT 3 GATE:** Before EPIC-02 frontend items (ST-05 if not done in Sprint 2, ST-06) and remaining backend (ST-04 if not done in Sprint 2) are sealed, ST-02 must be signed off by Head of Specs Team.

---

### EPIC-02 — Alerts & Notifications (Sprint 3 portion)

**Sprint 3 items:** ST-04 (if not Sprint 2), ST-05 (if not Sprint 2), ST-06, ST-07

#### ST-06 — Frontend: in-app notification feed

**Owner:** Base44 Frontend
**Estimated effort:** S–M (~6 hrs mid)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md § ST-06`
**Spec locked:** `docs/specs/frontend/pages/notifications.md` v0.1
**Design source:** `docs/design/2026-03-18__release-v2.1/notification-feed/ux_spec.md`
**Dependencies:** ST-02 (notification feed schema), ST-04 (backend must be functional for integration)
**Seal condition:** ⚠ CONDITIONAL — ST-01 Complete. ST-02 signed off. ST-04 complete (staging confirmation required).
**Notes:** Test scenarios: ST-07 covers this feature.

#### ST-07 — QA: notification delivery test scenarios

**Owner:** QA & Testing Owner + Director of Quality
**Estimated effort:** S (~3 hrs mid)
**Delegation class:** delegated_qa
**Acceptance Criteria:** see `stage4_backlog_slice.md § ST-07`
**Dependencies:** ST-03, ST-04, ST-05, ST-06 (all implementation stories should be at minimum in-progress before scenario authoring is complete)
**Seal condition:** ⚠ CONDITIONAL — ST-01 Complete.
**Notes:** This is the vehicle to close the EPIC-02 test scenario gap flag. Director of Quality review required.

---

### EPIC-03 — Watchlists & Screening

**Maps to:** S2-03
**Owner:** Head of Engineering + Base44 Frontend + Data Model & Domain Schema Owner
**Estimated effort:** M (~28 hrs mid; ~38 hrs with ST-10)
**Risk IDs:** RISK-03
**Execution sequence:** Can start parallel to EPIC-02 Sprint 3 frontend items

#### ST-08 — Spec: watchlist data model + API endpoints

**Owner:** Head of Specs Team + Data Model & Domain Schema Owner
**Estimated effort:** S–M (~6 hrs mid)
**Delegation class:** delegated_decision
**Acceptance Criteria:** see `stage4_backlog_slice.md § ST-08`
**Dependencies:** None (can start Sprint 3 immediately)
**Notes:** RISK-03. Must gate ST-09 and ST-10. `openapi.yaml` updated in same commit.

#### ST-09 — Backend: watchlist implementation

**Owner:** Head of Engineering
**Estimated effort:** M (~12 hrs mid)
**Delegation class:** delegated_backend
**Acceptance Criteria:** see `stage4_backlog_slice.md § ST-09`
**Dependencies:** ST-08 (spec + data model signed off)
**Notes:** Database migration required. Signal status integration. Integration tests required.

#### ST-10 — Frontend: watchlist UI [STRETCH — Sprint 3 / Sprint 4]

**Owner:** Base44 Frontend
**Estimated effort:** M (~10 hrs mid)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md § ST-10`
**Spec locked:** `docs/specs/frontend/pages/watchlist.md` v0.1
**Design source:** `docs/design/2026-03-18__release-v2.1/watchlist/ux_spec.md`
**Dependencies:** ST-08 (spec), ST-09 (backend live in staging)
**Seal condition:** Conditional on ST-09 complete and staging deployment confirmed.
**Notes:** ⚠ STRETCH — if Sprint 3 runs long, defer to Sprint 4. Product Owner accepts. ST-09 backend is the release-blocker for watchlist feature; ST-10 frontend completion is required for feature acceptance. Test scenarios gap: QA & Testing Owner to author watchlist_scenarios.md before Sprint 3 closes on EPIC-03.

---

## Capacity Summary

| Metric | Sprint 1 | Sprint 2 | Sprint 3 core | Release total |
|--------|----------|----------|---------------|---------------|
| Total confirmed capacity | ~40 hrs | ~40 hrs | ~40 hrs | ~120 hrs |
| Total estimated effort (mid) | ~39 hrs | ~37 hrs | ~43 hrs | ~119–129 hrs |
| Utilisation | ~98% | ~93% | ~108% (WARN) | ~99–108% |
| Over-allocation | No | No | Yes (ST-10 stretch mitigates) | WARN — acknowledged |

## Items Deferred This Sprint

None. All items included across 3 sprint phases. ST-10 carried as stretch.

## Deferred Execution Blockers Accepted

N/A — `deferred_execution_blockers` field was empty in cycle state.json.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| RISK-01: ST-01 must be Complete (Head of Engineering sign-off) before any EPIC-02 story seals | Head of Engineering | Yes — EPIC-02 seal gate |
| pip-audit install before first exec branch commit | Head of Engineering | No |
| EPIC-04 test scenarios (chart_interactivity_scenarios.md) | QA & Testing Owner | Yes — Sprint 1 EPIC-04 close |
| EPIC-03 test scenarios (watchlist_scenarios.md) | QA & Testing Owner | Yes — Sprint 3 EPIC-03 close |
| EPIC-05 slippage + PDF export test scenarios | QA & Testing Owner | Yes — Sprint 2/3 EPIC-05 close |
| ST-14: data_model.md Fill Price spec sign-off before implementation | Data Model & Domain Schema Owner + Head of Specs Team | Yes — ST-14 implementation gate |
| ST-19: PMO Lead to review commit history at Sprint 1 close | PMO Lead | Yes — ST-19 acceptance |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** confirmed — 2026-03-18
**Scope confirmed:** confirmed — all 19 stories included across 3 sprint phases; ST-10 stretch acknowledged
**Capacity confirmed:** confirmed — WARN acknowledged; 3-sprint phasing accepted; Sprint 3 ST-10 stretch accepted
**Deferred execution blockers accepted:** N/A — none present
**EPIC-02 conditional seal accepted:** confirmed — EPIC-02 stories (ST-02–ST-07) carry conditional seal status pending ST-01 Complete with Head of Engineering sign-off; Product Owner explicitly accepts this structure
**Signed off by:** Product Owner
**Date:** 2026-03-18
