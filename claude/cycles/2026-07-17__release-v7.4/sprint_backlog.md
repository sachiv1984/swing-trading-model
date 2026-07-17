**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-07-17
**Cycle:** 2026-07-17__release-v7.4
**Release:** v7.4
**Sprint Goal:** Produce the consolidated v7.4 UI-feature readiness pass — dependency pre-flight (`cmdk`, `react-day-picker`), UX specs for the saved-filters empty state and bulk-actions confirmation/undo-window modal, a command-palette keyboard-navigation design review, a Playwright visual-regression baseline scope, a command-palette analytics event schema, and a regression-suite CI tagging scheme — so command palette, custom price alerts, bulk actions, and saved filters/calendar view (`BLG-FE-115/116/117/118`) can each clear a fresh Design Gate once real design artefacts exist.
**Backlog Slice Source:** amended `claude/cycles/2026-07-17__release-v7.4/amendments/AMD-20260717-01/amended_backlog_slice.md` (supersedes `stage4_backlog_slice.md` for sprint planning purposes; original 5-item slice removed ST-02/03/04/05 by `AMD-20260717-01` — see `sprint_planning_notes.md`)

Single-EPIC sprint — no merge order section required (§6.1 applies only when >1 EPIC is in scope).

## Sprint Scope

### EPIC-01 — v7.4 UI-heavy release readiness bundle

**Maps to:** S2-01
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design; Director of Quality
**Estimated effort:** 6.0 days
**Risk IDs:** RISK-01 (changed — no longer critical-path this sprint), RISK-02
**Execution sequence:** 1

#### ST-01 — Produce v7.4 readiness pass (dependencies, UX specs, design review, QA/analytics coverage)

**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design; Director of Quality
**Estimated effort:** 6.0 (L, ~5–7 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `amended_backlog_slice.md#ST-01` (7-item bullet list; informal AC-01…AC-07 mapping recorded in `sprint_planning_notes.md`)

*(The Execution Engine reads AC from the amended backlog slice directly via `spec_references`. Do not duplicate the full AC list here — the sprint backlog is a sequencing and ownership document.)*

**Dependencies:** None

**Notes:** Design gate cleared 2026-07-17 (second pass, `design_gate.md`) — classified Design Pre-Approved (documentation/spec-and-process pass only, no shippable UI). This story's acceptance criteria are unchanged from the original 5-item plan — the design/spec work it produces remains valid forward-looking preparation for whichever future release re-introduces EPIC-02/03/04/05, per the amendment's own note. RISK-02 (dependency install) still applies: verify `cmdk` and `react-day-picker` are both correctly added to `package.json` at EPIC-01 close, even though the consuming EPICs are deferred.

**Staging-only ACs:** None — documentation/spec/design-review pass, no UI to verify visually.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24–28 days |
| Total estimated effort (in-scope) | 6.0 days (midpoint) |
| Utilisation | ~21–25% of band |
| Over-allocation | No |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| ST-02 (`BLG-FE-115`) | EPIC-02 | Removed from cycle scope by `AMD-20260717-01` — Design Gate BLOCKED, no approved design artefact |
| ST-03 (`BLG-FE-116`) | EPIC-03 | Removed from cycle scope by `AMD-20260717-01` — Design Gate BLOCKED, no design artefact scheduled anywhere in v7.4 plan |
| ST-04 (`BLG-FE-117`) | EPIC-04 | Removed from cycle scope by `AMD-20260717-01` — Design Gate BLOCKED, no UX spec for confirmation/undo-window modal |
| ST-05 (`BLG-FE-118`) | EPIC-05 | Removed from cycle scope by `AMD-20260717-01` — Design Gate BLOCKED, no UX spec for empty state / no calendar-view design review |

## Deferred Execution Blockers Accepted

N/A — none present (`state.json deferred_execution_blockers` empty).

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Add 5 missing prompt-change-log rows (see `sprint_planning_notes.md`) | Head of Specs Team | No |
| Mirror `design_gate_status` from cycle-level `state.json` to root `.claude_current_state.json` pointer (file as backlog item) | Head of Specs Team | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed
**Scope confirmed:** Confirmed — 1 item, 1 EPIC, well within capacity (PASS, ~21–25% utilisation)
**Capacity confirmed:** Confirmed — PASS at 6.0d midpoint vs. ~24–28d band, matches DL-069 baseline verification (`BLG-GOV-249`)
**Deferred execution blockers accepted (if any):** N/A — none present
**Signed off by:** Product Owner
**Date:** 2026-07-17
