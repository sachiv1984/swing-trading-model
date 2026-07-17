**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-07-17
**Cycle:** 2026-07-17__release-v7.5
**Release:** v7.5
**Sprint Goal:** Ship all four v7.5 UI feature expansions — global command palette, user-defined price alerts, bulk actions, and saved filters/calendar view — each fully wired to its now-locked design artefact and observable in the running app.
**Backlog Slice Source:** original `stage4_backlog_slice.md`

- **EPIC merge sequence:** EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04
- **`execution_state.json` owner:** EPIC-01 (first in execution order — EPIC-02/EPIC-03/EPIC-04 branches must check for existence and append rather than overwrite)
- **Shared files across EPICs:** None identified — see `sprint_planning_notes.md §Multi-EPIC Execution Notes` for the full per-EPIC file ownership breakdown (Design Gate placement decisions resolved the one plausible overlap between EPIC-03 and EPIC-04)

## Sprint Scope

### EPIC-01 — Global command palette / cross-page search

**Maps to:** S2-01
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Estimated effort:** 1.5 days
**Risk IDs:** RISK-01 (resolved), RISK-02
**Execution sequence:** 1

#### ST-01 — Wire global Cmd/Ctrl-K command palette

**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Estimated effort:** 1.5 (M)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

*(The Execution Engine reads AC from `stage4_backlog_slice.md` directly via `spec_references`. Do not duplicate the full AC table here — the sprint backlog is a sequencing and ownership document.)*

**Dependencies:** None

**Spec references:** `docs/design/2026-07-17__release-v7.5/command-palette/ux_spec.md`; `docs/specs/frontend/pages/navigation.md` v1.3; existing `src/components/ui/command.js` (shadcn Command primitive, currently unwired)

**Notes:** Design gate cleared 2026-07-17 (`design_gate.md`) — classified Design Required, artefact produced as a Design Gate precursor step (not in-sprint work). Simplest of the 4 EPICs — sequenced first and designated `execution_state.json` owner.

**Staging-only ACs:** None — all 3 ACs (palette open, cross-entity search + navigate, page-name navigate) are pure client-side interaction/rendering behaviour against existing app data, fully reproducible in a Playwright test in CI. Per `CLAUDE.md`, Playwright coverage or recorded human staging sign-off is still required for each observable AC at execution time — this field specifically flags ACs CI *cannot* reach, which is none here.

---

### EPIC-02 — User-defined custom price alerts

**Maps to:** S2-02
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner; Backend Engineering Patterns Owner
**Estimated effort:** 4.0 days
**Risk IDs:** RISK-01 (resolved), RISK-02, RISK-03
**Execution sequence:** 2

#### ST-02 — Add user-created price-alert data model, UI, and delivery integration

**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner; Backend Engineering Patterns Owner
**Estimated effort:** 4.0 (L)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Spec references:** `docs/design/2026-07-17__release-v7.5/custom-price-alerts/ux_spec.md`; `docs/specs/frontend/pages/notifications.md` v0.4; backend data model, evaluation-pipeline extension, and health-check surfacing pre-scoped in `docs/specs/blg_fe_116_pre_implementation_readiness_pass.md` (§13 PASS, filed 2026-07-16)

**Notes:** Largest-effort, only item with backend scope (RISK-03) — sequenced 2nd (not last) to preserve runway if backend integration surfaces an issue during implementation, despite pre-scoping. Design Gate placement decision: new "Custom Price Alerts" section on the existing Notifications Preferences page (`notifications.md`), below the fixed-type Alert Thresholds section — not a new top-level page. Also requires backend implementation work (data model + notification-pipeline integration per RISK-03) alongside the frontend CRUD UI — the single `delegated_frontend` classification reflects where the user-facing design decisions live; the backend piece is implementation against an already-fully-scoped spec, not a fresh design decision.

**Staging-only ACs:** AC "Alert fires via the existing notification delivery channel when its condition is met" — requires live delivery-channel firing behaviour that CI cannot reproduce (same class as the canonical `shared_standards.md §16.11` staging-only example). If staging sign-off for this AC is deferred to post-merge, a backlog item must be filed before the PR opens per `CLAUDE.md` §2. The remaining 2 ACs (create alert from UI; view/edit/delete active alerts) are pure CRUD UI, fully Playwright-testable in CI.

---

### EPIC-03 — Bulk actions on list/table views

**Maps to:** S2-03
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Estimated effort:** 1.5 days
**Risk IDs:** RISK-01 (resolved), RISK-02
**Execution sequence:** 3

#### ST-03 — Add multi-select and bulk-action toolbar to Watchlist/TradePlans

**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Estimated effort:** 1.5 (M)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Spec references:** `docs/design/2026-07-17__release-v7.5/bulk-actions-toolbar/ux_spec.md`; `docs/specs/frontend/pages/watchlist.md` v0.4; `docs/specs/frontend/pages/trade_plan.md` v1.1

**Notes:** Design gate cleared 2026-07-17 — classified Design Required (new multi-select interaction pattern, new bulk-action toolbar component, applied to two pages). No cross-EPIC file overlap with EPIC-04 (see `sprint_planning_notes.md`).

**Staging-only ACs:** None — multi-select, toolbar appearance, and bulk tag/archive/remove are all client-side interaction/rendering behaviour, fully Playwright-testable in CI against seeded rows.

---

### EPIC-04 — Saved filter views and calendar view

**Maps to:** S2-04
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Estimated effort:** 4.0 days
**Risk IDs:** RISK-01 (resolved), RISK-02
**Execution sequence:** 4

#### ST-04 — Add named saved filter presets and a calendar view

**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Estimated effort:** 4.0 (L)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Spec references:** `docs/design/2026-07-17__release-v7.5/saved-filters-calendar-view/ux_spec.md`; `docs/specs/frontend/pages/trade_history.md` v1.11

**Notes:** Design Gate placement decision: both saved filter presets and the calendar view placed on Trade History only (not split across Screener/TradeHistory/Watchlist as the original backlog scope wording suggested) — grounded in Trade History having the richest existing filter set and the calendar's date-sourcing being built on `trade_history.exit_date`. This placement decision resolves the only plausible cross-EPIC file overlap with EPIC-03 (see `sprint_planning_notes.md`). Sequenced last — largest single-EPIC effort alongside EPIC-02, but no backend scope and no runway concern.

**Staging-only ACs:** None — saved-filter persistence (reapply in a later session) and calendar rendering/month navigation are both testable in CI (persistence via integration test against the backend/localStorage; rendering via Playwright against seeded trade-plan/key-date data, no external date source).

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24–28 days |
| Total estimated effort (in-scope) | 11.0 days (midpoint) |
| Utilisation | ~39–46% of band |
| Over-allocation | No (outcome: PASS) |

## Items Deferred This Sprint

None — all 4 backlog-slice items are in scope.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Add missing `sprint_planning_prompt.md` v3.13 prompt-change-log row | Head of Specs Team | No |
| Clear stale top-level `.claude_current_state.json amended_backlog_slice_path` (v7.4 leftover) | PMO Lead / Head of Specs Team | No |
| Apply `CLAUDE.md` §8 procedure proactively if concurrent EPIC PRs report `CONFLICTING/DIRTY` | PMO Lead | No |
| File a backlog item before PR opens if ST-02's staging-only AC (alert delivery firing) sign-off is deferred to post-merge | Director of Quality / Base44 Frontend Prompt Owner | No (execution-time conditional, per `CLAUDE.md` §2) |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — see `sprint_goal.md`
**Scope confirmed:** Confirmed — 4 items, 4 EPICs, all `include`, within capacity (PASS)
**Capacity confirmed:** Confirmed — PASS at 11.0d midpoint vs. ~24–28d band, ~39–46% utilisation, no WARN, no phasing action required
**Deferred execution blockers accepted (if any):** N/A — none present (`state.json deferred_execution_blockers` empty)
**Signed off by:** Product Owner
**Date:** 2026-07-17
