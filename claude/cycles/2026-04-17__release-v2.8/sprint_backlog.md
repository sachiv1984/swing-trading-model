**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-04-18
**Cycle:** 2026-04-17__release-v2.8
**Release:** v2.8
**Sprint Goal:** Deliver v2.8 in full: complete the v2.7 deferred market correlation frontend, fill the CORR/SIG-IND test scenario gaps, apply three governance hardening patches, and ship AI journal summarisation (backend + frontend) within the §13 compliance boundary.
**Backlog Slice Source:** original `claude/cycles/2026-04-17__release-v2.8/stage4_backlog_slice.md`

---

## Sprint Scope

---

### Sprint 1

---

#### EPIC-02 — Test Scenario Coverage

**Maps to:** S2-02 (BLG-QA-13)
**Owner:** QA & Testing Owner
**Estimated effort:** 16 hrs (~2 days total)
**Risk IDs:** RISK-02
**Execution sequence:** 2 (Sprint 1; independent)

##### ST-02 — Market Correlation Endpoint Scenarios

**Owner:** QA & Testing Owner
**Estimated effort:** S–M (~0.5–1 day; ~8 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** All new scenarios must reference `analytics_endpoints.md v2.1.0` exactly. Do not modify existing analytics_scenarios.md content.

---

##### ST-03 — Supplementary Indicator Field Scenarios

**Owner:** QA & Testing Owner
**Estimated effort:** S (~0.5 day; ~8 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** All new scenarios must reference `signal_endpoints.md v1.1` exactly. Do not modify existing signals_scenarios.md content.

---

#### EPIC-03 — Governance Process Hardening

**Maps to:** S2-03 (CF-1), S2-04 (CF-2), S2-05 (BLG-GOV-13)
**Owner:** Head of Specs Team + PMO Lead
**Estimated effort:** 8 hrs (~1 day total)
**Risk IDs:** RISK-03
**Execution sequence:** 1 (Sprint 1; run first — reduces governance drift risk during execution)

##### ST-04 — DoQ Date Field Reminder Patch

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day; ~4 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** CLAUDE.md §6 checklist is mandatory (version bump, OPERATIONAL_GUIDE update, prompt_change_log entry). Self-referential: this story's own DoQ sign-off Date field is evidence the patch works.

---

##### ST-05 — Sprint Close Terminology Clarification

**Owner:** PMO Lead
**Estimated effort:** S (~0.5 day; ~2 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** If the fix touches a governed prompt, apply CLAUDE.md §6 checklist. If fix is in a non-governed template file only, checklist not required (per AC).

---

##### ST-06 — Backlog Archive Deduplication

**Owner:** PMO Lead
**Estimated effort:** S (~0.5 day; ~2 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** PO confirmation of deduplication approach (retain most recent per ID; remove earlier copies) — to be confirmed at sprint planning sign-off

**Notes:** PO confirmation is the first AC bullet. Do not execute deduplication until confirmed.

---

### Sprint 2

---

#### EPIC-01 — Market Correlation Frontend

**Maps to:** S2-01 (BLG-FE-14)
**Owner:** Frontend Specifications & UX Owner
**Estimated effort:** 12 hrs (~1.5 days)
**Risk IDs:** RISK-01
**Execution sequence:** 5 (Sprint 2; independent — can run parallel with ST-07)

##### ST-01 — Market Correlation View

**Owner:** Frontend Specifications & UX Owner
**Estimated effort:** M (~1–2 days; ~12 hrs)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (UX placement resolved by design gate — Analytics page §18)

**Notes:** Design spec locked at `docs/design/2026-04-17__release-v2.8/market-correlation/ux_spec.md`. Frontend spec locked at `docs/specs/frontend/pages/analytics.md v1.7`. Severity colours: high=Rose-500, moderate=Amber-500, low=Emerald-500, null=Slate-500. Sort severity descending; null rows to bottom.
**Test scenarios gap:** QA & Testing Owner to author SC-CORR frontend scenario tests before next sprint on this domain (see sprint_planning_notes.md).

---

#### EPIC-04 — AI Journal Summarisation

**Maps to:** S2-06 (BLG-FEAT-16)
**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Estimated effort:** 16 hrs (~2 days total)
**Risk IDs:** RISK-04
**Execution sequence:** 3 and 4 (Sprint 2; ST-07 before ST-08)

**§13 Status:** CONDITIONALLY COMPLIANT — SRB-v1.7 (2026-03-02). Mandatory AC conditions appear verbatim in ST-07 and ST-08.

##### ST-07 — AI Journal Summary Backend

**Owner:** Head of Engineering
**Estimated effort:** M (~1–2 days; ~8 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** External LLM API key set in env var (pre-execution requirement)

**Notes:** openapi.yaml must be updated in the same commit as the contract. `## POST /ai/journal-summary` heading in API contract spec must be at `##` level (not `###`). AI output must NOT feed into any signal, scoring, or recommendation system.

---

##### ST-08 — AI Journal Summary Frontend

**Owner:** Frontend Specifications & UX Owner
**Estimated effort:** M (~1–2 days; ~8 hrs)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** ST-07 (backend endpoint `POST /ai/journal-summary` must be live)

**Notes:** Design spec locked at `docs/design/2026-04-17__release-v2.8/ai-journal-summary/ux_spec.md`. Trade History spec at `docs/specs/frontend/pages/trade_history.md v1.7`. Disclaimer label must be visible and non-dismissible. Collapsed by default. No auto-generation on page load. **Strategy Rules owner sign-off is an explicit AC and merge pre-condition** — do not merge PR without recorded sign-off in DoQ block.
**Test scenarios gap:** QA & Testing Owner to author AI Journal Summary frontend scenario tests before next sprint on this domain (see sprint_planning_notes.md).

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~52 hrs (across 2 sprints) |
| Total estimated effort (in-scope) | ~52 hrs |
| Utilisation | ~100% |
| Over-allocation | No |

| Sprint | Capacity | Effort | EPICs |
|--------|----------|--------|-------|
| Sprint 1 | ~24 hrs | ~24 hrs | EPIC-02 (ST-02, ST-03), EPIC-03 (ST-04, ST-05, ST-06) |
| Sprint 2 | ~28 hrs | ~28 hrs | EPIC-01 (ST-01), EPIC-04 (ST-07, ST-08) |

## Items Deferred This Sprint

None — all backlog slice items included.

## Deferred Execution Blockers Accepted

N/A — `deferred_execution_blockers` was empty in `state.json`.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? | Resolution |
|--------|-------|---------|------------|
| PO to confirm: design gate RISK-04 classification (Strategy Rules sign-off as merge AC) satisfies cycle_summary "before sprint planning seal" requirement | Product Owner | **Yes** | **RESOLVED 2026-04-18** — PO confirmed: merge-AC classification satisfies requirement. Strategy Rules sign-off as AC in ST-08 is a hard merge blocker and satisfies the intent (boundary compliance before any AI journal work ships). |
| PO to confirm ST-06 deduplication approach: retain most recent entry per duplicate ID; remove earlier copies | Product Owner | Yes (can confirm at sprint sign-off) | **RESOLVED 2026-04-18** — PO confirmed: retain most recent entry per duplicate ID; remove earlier copies. |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Yes
**Scope confirmed:** Yes — all 8 stories in scope; delegation classes correct; execution sequence approved
**Capacity confirmed:** Yes — ~52 hrs estimated, ~52 hrs available; 100% utilisation accepted
**Deferred execution blockers accepted (if any):** N/A
**Signed off by:** Product Owner
**Date:** 2026-04-18
