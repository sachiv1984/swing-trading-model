**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-06-19
**Cycle:** 2026-06-19__release-v6.0
**Release:** v6.0
**Sprint Goal:** Ship the P0 signal correctness fix and deliver the Trader's Morning Briefing and net-of-costs features to resolve the Product Value Alert, complete Screener data quality telemetry, and advance SI-05 effectiveness reviews as within-sprint gates clear.
**Backlog Slice Source:** original — `claude/cycles/2026-06-19__release-v6.0/stage4_backlog_slice.md`

---

# Sprint Backlog — 2026-06-19__release-v6.0

---

## Merge Order (Multi-EPIC Sprint)

**EPIC merge sequence:** EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04

**execution_state.json owner:** EPIC-01 branch. All other EPIC branches must check for `execution_state.json` before creating their own — if found, append rather than overwrite.

**Shared file advisory:**
- `docs/specs/api_contracts/` and `docs/reference/openapi.yaml`: EPIC-02 and EPIC-03 both modify these. EPIC-03 branch must rebase onto `main` after EPIC-02 merges before finalising contract changes.
- `data_model.md`: EPIC-02 owns (trade cost fields). EPIC-03 and EPIC-04 must not modify without rebasing onto main after EPIC-02 merges.

---

## Sprint Scope

---

### EPIC-01 — Signal Correctness Fast-Track

**Maps to:** S2-01
**Owner:** Strategy Rules & System Intent Owner; Head of Engineering
**Estimated effort:** S (~0.5 day)
**Risk IDs:** RISK-01
**Execution sequence:** 1st — P0 correctness fast-track; no dependencies

---

#### ST-01 — Align signal_service suggested_shares to risk-based sizing model

**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (Strategy Rules & System Intent Owner confirmation is AC-01 — scoped within the story)

**Notes:** P0 correctness fast-track. RISK-01: sign-off required as AC-01 before implementation proceeds. Execution Engine must record sign-off in QA evidence before proceeding to AC-02 onwards.

**Staging-only ACs:** None

---

### EPIC-02 — User Intelligence Features

**Maps to:** S2-02, S2-03
**Owner:** Head of UX & Design; Financial Reporting & Records Owner
**Estimated effort:** M (~5 days total)
**Risk IDs:** RISK-02, RISK-03
**Execution sequence:** 2nd — after EPIC-01; addresses Product Value Alert commitment

---

#### ST-02 — Trader's Morning Briefing dashboard

**Owner:** Head of UX & Design; Base44 Frontend Prompt Owner
**Estimated effort:** M (~2.5 days)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None (all 5 composing endpoints confirmed live)

**Notes:** Frontend composition from existing endpoints (GET /portfolio/grace-period-alerts, GET /positions, GET /portfolio/red-flag-journal, GET /earnings/{ticker}, GET /analytics/arc5-compliance). No new backend required. RISK-02: if any endpoint contract has changed since release planning, surface as execution blocker immediately. Playwright coverage required (AC-09).

**Staging-only ACs:** None

---

#### ST-03 — Net-of-costs performance tracking

**Owner:** Financial Reporting & Records Owner; Head of Engineering
**Estimated effort:** M (~2.5 days)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** Additive data model + backend + frontend. RISK-03: optional fields only — existing R-multiple unaffected where cost data absent. EPIC-02 owns `data_model.md` and `docs/specs/api_contracts/` for trade history endpoints. EPIC-03 must rebase after EPIC-02 merges.

**Staging-only ACs:** None

---

### EPIC-03 — Screener Quality & Ops Closure

**Maps to:** S2-04, S2-05
**Owner:** Head of UX & Design; Infrastructure & Operations Owner
**Estimated effort:** S/XS (~1.1 days)
**Risk IDs:** RISK-04
**Execution sequence:** 3rd (after EPIC-01; parallel with EPIC-02 possible)

---

#### ST-04 — Screener data quality telemetry

**Owner:** Head of UX & Design; Head of Backend Engineering
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** New GET /screener/results response fields required (AC-01). Spec contract update required (AC-01 references "docs/specs/api_contracts/ (screener results contract — update required)"). Must add `## GET /screener/results` to screener contract file and update `docs/reference/openapi.yaml` in the same commit (CLAUDE.md §2). EPIC-03 branch must rebase onto main after EPIC-02 merges before finalising openapi.yaml changes. Playwright coverage required (AC-07).

**Staging-only ACs:** None

---

#### ST-05 — SI-05 deep link AC-04 staging confirmation

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** XS (<1 hour)
**Delegation class:** autonomous
**Status at sprint open: conditional — gate ~2026-06-23**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** SI-05 Telegram digest delivery after 2026-06-17 FRONTEND_URL set

**Notes:** RISK-04. Do not begin until digest delivery confirmed (~2026-06-23). All ACs are staging-only (require live Telegram digest). Backlog filing required before PR opens if staging sign-off is deferred post-merge. BLG-OPS-70 5th carry-forward.

**Staging-only ACs:** AC-01 (SI-05 Telegram digest received after FRONTEND_URL applied), AC-02 (deep links resolve to correct frontend pages), AC-03 (Infrastructure & Operations Owner confirmation recorded)

---

### EPIC-04 — SI-05 Effectiveness Reviews & RFJ Design (Conditional)

**Maps to:** S2-06, S2-07, S2-08, S2-09, S2-10, S2-11
**Owner:** PMO Lead; Product Owner; Head of UX & Design; Infrastructure & Operations Owner
**Estimated effort:** ~4.35 days (if all activate)
**Risk IDs:** RISK-05
**Execution sequence:** 4th — conditional; activates cluster by cluster as gates clear

**EPIC-04 cluster structure:**
- Cluster A (gate 2026-06-21): ST-06, ST-07 — activates if SI-03 Red Flag Journal live ≥ 30 days
- Cluster B (gate 2026-07-04): ST-08, ST-09, ST-10, ST-11 — activates after SI-05 Phase 1 effectiveness review

If any cluster gate is not met by sprint close, affected items return to backlog.

---

#### ST-06 — RFJ design review pre-brief

**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_decision
**Status at sprint open: conditional — gate 2026-06-21**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** Gate confirmed: SI-03 Red Flag Journal live ≥ 30 days (on or after 2026-06-21)

**Notes:** RISK-05 HIGH. 6th consecutive carry-forward (v5.3–v5.9 deferrals). Gate 2026-06-21 is 2 days from sprint open — schedule promptly on gate confirmation to avoid 7th deferral. Perennial-return advisory: this item should be prioritised immediately when gate clears. ST-07 depends on this story. delegated_decision — Head of UX & Design to produce design review brief under delegation.

**Staging-only ACs:** None

---

#### ST-07 — Red Flag Journal visual design review

**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Estimated effort:** M (~1.5 days)
**Delegation class:** delegated_decision
**Status at sprint open: conditional — gate 2026-06-21**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** ST-06 (BLG-FE-64 pre-brief) must complete first; gate 2026-06-21

**Notes:** RISK-05 HIGH. Depends on ST-06 brief. delegated_decision — Head of UX & Design conducts design review. If redesign recommended, UX spec produced and implementation backlog item filed (AC-03).

**Staging-only ACs:** None

---

#### ST-08 — SI-05 digest weekly cadence review

**Owner:** Product Owner; Director of Quality
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_decision
**Status at sprint open: conditional — gate 2026-07-04**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** 2026-07-04 SI-05 effectiveness review (BLG-GOV-96) complete; review outputs available

**Notes:** 3rd consecutive carry-forward (v5.5, v5.7, v5.8). delegated_decision — PO product review. Gate is a scheduled event. Cluster B item — activates only after effectiveness review complete. Independent within Cluster B.

**Staging-only ACs:** None

---

#### ST-09 — SI-05 digest actionability metric definition

**Owner:** Metrics Definitions & Analytics Owner; Infrastructure & Operations Owner
**Estimated effort:** S (~0.75 day)
**Delegation class:** autonomous
**Status at sprint open: conditional — gate 2026-07-04**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** BLG-GOV-113 (SI-05 effectiveness review protocol) complete — i.e., 2026-07-04 review conducted

**Notes:** 3rd consecutive carry-forward (v5.5, v5.7, v5.8). autonomous — metrics definition document. Feeds ST-08 (cadence review) and BLG-GOV-96 (effectiveness criteria). Independent within Cluster B.

**Staging-only ACs:** None

---

#### ST-10 — SI-05 Phase 2 activation decision scope

**Owner:** Product Owner; PMO Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_decision
**Status at sprint open: conditional — gate 2026-07-04**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** 2026-07-04 effectiveness review outputs available; BLG-GOV-121 §13 pre-clearance status available

**Notes:** delegated_decision — PO formal Phase 2 activation decision document. Document filed as Class 3 Operational Record in `docs/product/decisions/` (AC-05). Independent within Cluster B.

**Staging-only ACs:** None

---

#### ST-11 — SI-05 service production p99 latency baseline review

**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Status at sprint open: conditional — gate 2026-07-04**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** ≥4 weeks of POST /digest/si05/send production operation (SI-05 live 2026-06-04 → gate 2026-07-04)

**Notes:** 3rd consecutive carry-forward (v5.5, v5.7, v5.8). autonomous — ops measurement + doc. All ACs require live production Render log data (staging-only). Backlog filing required before PR opens if staging sign-off deferred post-merge. Independent within Cluster B.

**Staging-only ACs:** AC-01 (p99 latency extracted from Render logs), AC-02 (comparison against pre-launch baseline), AC-03 (PASS recorded or investigation item filed), AC-04 (Infrastructure & Operations Owner sign-off)

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~12–14 working days |
| Firm scope effort | 6.5 days |
| Conditional scope effort (if all activate) | 4.35 days |
| Total if all activate | ~10.85 days |
| Firm utilisation | 50% (PASS) |
| All-scope utilisation | ~79–86% (WARN — within ceiling) |
| Over-allocation | No |

---

## Items Deferred This Sprint

No items from the authoritative backlog slice (ST-01 through ST-11) are deferred. All 11 items are included (4 firm + 7 conditional). PT-04 (BLG-FEAT-25) and SI-02 frontend were excluded at release planning and are not in the backlog slice.

---

## Deferred Execution Blockers Accepted

*(Section omitted — `deferred_execution_blockers` was empty at release planning.)*

---

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? | Resolution |
|--------|-------|---------|------------|
| Design gate bypass authority/reason (IMP-04, IMP-30) | Head of UX & Design + Product Owner | No | Resolved — design gate ran and Passed 2026-06-19; bypass audit skipped per §STEP -1.3 (entered from Design_Gate_Passed) |
| Product Owner acknowledge capacity WARN (IMP-41) | Product Owner | No | Resolved — PO confirmed 2026-06-19 (see Sign-Off section) |
| Product Owner confirm sprint goal | Product Owner | No | Resolved — sprint_goal.md confirmed 2026-06-19 |
| Product Owner sign off sprint scope | Product Owner | No | Resolved — full sign-off 2026-06-19 |
| Staging-only ACs for ST-05 (AC-01/02/03) — backlog items to be filed before PR opens if staging deferred post-merge | Infrastructure & Operations Owner | Yes (before PR) | Execution-phase requirement — not a sprint seal blocker |
| Staging-only ACs for ST-11 (AC-01/02/03/04) — backlog items to be filed before PR opens if staging deferred post-merge | Infrastructure & Operations Owner; Head of Engineering | Yes (before PR) | Execution-phase requirement — not a sprint seal blocker |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — 2026-06-19
**Scope confirmed:** Confirmed — 4 firm + 7 conditional stories; PT-04/SI-02 exclusion accepted — 2026-06-19
**Capacity WARN acknowledged (IMP-41):** Confirmed — 10.85-day all-conditional scenario accepted; phased gate-cluster structure is the risk management mechanism — 2026-06-19
**Deferred execution blockers accepted (if any):** N/A
**Signed off by:** Product Owner
**Date:** 2026-06-19 (sealed 2026-06-19 after design gate Passed; all planning-phase blockers resolved)
