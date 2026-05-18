**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-05-18
**Cycle:** 2026-05-18__release-v3.7
**Release:** v3.7
**Sprint Goal:** Ship the signal-to-watchlist workflow (Add to Watchlist CTA on signal cards + signal context panel in trade plan form) and deliver the four governance hardening patches deferred from v3.6.
**Backlog Slice Source:** original — claude/cycles/2026-05-18__release-v3.7/stage4_backlog_slice.md

---

# Sprint Backlog — 2026-05-18__release-v3.7

## Sprint Scope

### Merge Order

**Merge sequence:** EPIC-04 → EPIC-03 → EPIC-01

**execution_state.json owner:** EPIC-04 (first in execution order). EPIC-03 and EPIC-01 branches must check for `claude/cycles/2026-05-18__release-v3.7/execution_state.json` existence before creating their section — if found, read and append; do not overwrite.

**Shared file advisory:**
- `backend/routers/test.py`: modified by EPIC-04 (ST-09 conftest) and EPIC-01 (ST-01 new route test). EPIC-04 owns conftest changes. EPIC-01 must rebase onto `origin/main` after EPIC-04 merges before finalising test.py changes.
- All other modified files (`execution_prompt.md`, `prompt_change_log.md`, `openapi.yaml`, `data_model.md`) are owned by a single EPIC — no cross-EPIC conflict expected.

**EPIC-02 deferred to v3.8:** Product Owner confirmed < 20 closed trades (2026-05-18). ST-04, ST-05, ST-06 not in sprint scope.

---

### EPIC-04 — Technical Debt Clearance

**Maps to:** S2-04
**Owner:** Head of Engineering + QA & Testing Owner + Facilitator (ST-11)
**Estimated effort:** ~1.5 days
**Risk IDs:** None
**Execution sequence:** 1 (first to merge)
**Sprint:** 1

#### ST-09 — BLG-QA-20: Database stub conftest consolidation

**Owner:** QA & Testing Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** Closes BLG-QA-20. Creates `tests/conftest.py` session-scoped fixture. All four stub test files must drop their inline `types.ModuleType("database")` blocks. CI must stay green (69+ tests collected).

---

#### ST-10 — BLG-OPS-16 + BLG-FE-35: Pycache git hygiene + Research page font staging

**Owner:** Head of Engineering (BLG-OPS-16) + Head of UX & Design (BLG-FE-35)
**Estimated effort:** XS + XS (~0.5 day combined)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** BLG-OPS-16 (autonomous sub-task): untrack `backend/__pycache__/`, add `__pycache__/` and `*.pyc` to `.gitignore`. BLG-FE-35 (delegated_decision): Head of UX & Design must perform staging run of Research page against design system typography scale — date must be recorded in DoQ sign-off block. No design artefact pre-exists; staging run IS the artefact. Advisory per LL-v2.2-SP-01.

---

#### ST-11 — BLG-GOV-23: scored_initiatives.md comprehensive refresh

**Owner:** Facilitator
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** Resolves OA-RP-05 (open 2+ consecutive cycles). Facilitator to schedule refresh session before execution begins. Advisory per LL-v2.2-SP-01 — no pre-existing design session artefact required for this item.

---

### EPIC-03 — Governance Hardening Patches

**Maps to:** S2-03
**Owner:** Head of Specs Team + Director of Quality
**Estimated effort:** ~1 day
**Risk IDs:** RISK-03
**Execution sequence:** 2 (merges after EPIC-04)
**Sprint:** 1

#### ST-07 — execution_prompt.md patches ×3 (deviations_filed + backlog verify + spec_references verify)

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** Three sub-patches: (a) sub-step 10a atomic write of `deviations_filed`; (b) backlog verify guidance for deferred staging ACs; (c) spec_references path verify guidance. Also includes retroactive `prompt_change_log.md` entries for execution_prompt.md v3.18→v3.22, sprint_planning_prompt.md v3.0→v3.2, backlog_management_prompt.md v1.6→v1.7 (per cycle_summary advisory). CLAUDE.md §6 four-step checklist mandatory (version bump + OPERATIONAL_GUIDE §14 + phase section header + prompt_change_log.md entry). RISK-03 mitigation: retroactive log entries are advisory-only additions; no authority gate required.

---

#### ST-08 — qa_evidence_template.md: BLG-GOV-19 criterion 3 fail-path

**Owner:** Director of Quality
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** Adds explicit criterion 3 fail-path to BLG-GOV-19 section of qa_evidence_template.md. Resolves LL-v3.6 carry-forward item 2. If file is Class 6 governance: CLAUDE.md §6 checklist applies (version bump + OPERATIONAL_GUIDE §14 + prompt_change_log.md entry).

---

### EPIC-01 — Signals-to-Watchlist Workflow

**Maps to:** S2-01
**Owner:** Head of Engineering
**Estimated effort:** ~6 days
**Risk IDs:** RISK-02
**Execution sequence:** 3 (merges after EPIC-03)
**Sprint:** 1

#### ST-01 — BLG-FE-33: Signals page backend — watchlisted status support

**Owner:** Head of Engineering
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Notes:** `watchlisted` added to signals table CHECK constraint. `PATCH /signals/{id}` updated to accept `status: "watchlisted"`. signal_endpoints.md and data_model.md updated in same commit (per CLAUDE.md §2 — OpenAPI and endpoint contract rules). Backend test for PATCH `/signals/{id}` in `backend/routers/test.py`. Rebase onto `origin/main` after EPIC-03 merges before opening PR.

---

#### ST-02 — BLG-FE-33: Signals page frontend — Add to Watchlist CTA

**Owner:** Head of Engineering
**Estimated effort:** M (~1–2 days)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** ST-01 (PATCH /signals/{id} watchlisted support must be merged first)

**Notes:** New user-facing control — classification upgraded from `standard` to `delegated_frontend` at planning time. Playwright scenario SC-SIG-01 (or equivalent) is a mandatory AC — Playwright coverage satisfies CLAUDE.md §2 observable AC requirement. No additional human staging sign-off required if Playwright tests pass in CI. RISK-02: BLG-FE-34 (ST-03) depends on this story completing — sequential delivery required.

---

#### ST-03 — BLG-FE-34: Trade plan form signal context panel

**Owner:** Head of Engineering
**Estimated effort:** M (~1–2 days)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** ST-01, ST-02 (signal → watchlist linkage required to pass signal data to trade plan form)

**Notes:** New read-only Signal Context panel — classification upgraded from `standard` to `delegated_frontend` at planning time. Playwright scenario covering panel presence/absence is a mandatory AC. UX spec artefact: `docs/design/2026-05-18__release-v3.7/signal-context-panel/ux_spec.md`. Frontend spec: `docs/specs/frontend/pages/trade_plan.md` (v0.6 — Signal Context section pre-added at design gate).

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity (1 sprint) | ~5 days |
| Total estimated effort (8 in-scope stories) | ~8.5 days |
| Utilisation | ~170% |
| Over-allocation | Yes — accepted by Product Owner (2026-05-18) |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| ST-04 — PT-04 spec authoring + gate confirmation | EPIC-02 | EPIC-02 gate not met: < 20 closed trades confirmed by PO (2026-05-18) |
| ST-05 — PT-04 backend: quality score endpoint | EPIC-02 | EPIC-02 gate not met |
| ST-06 — PT-04 frontend: quality score display | EPIC-02 | EPIC-02 gate not met |

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Capture additional prompt_change_log.md gaps (v3.22→v3.23, v2.2→v2.3, v2.8→v2.9, v2.28→v2.29) | Head of Specs Team | No |
| Facilitator to schedule scored_initiatives.md refresh before ST-11 execution | Facilitator | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — 2026-05-18
**Scope confirmed:** Confirmed — 8 stories (EPIC-04/03/01); EPIC-02 deferred to v3.8 (gate not met)
**Capacity confirmed:** Confirmed — over-capacity acknowledged; phasing accepted
**Deferred execution blockers accepted (if any):** N/A — no deferred_execution_blockers in release plan
**Signed off by:** Product Owner
**Date:** 2026-05-18
