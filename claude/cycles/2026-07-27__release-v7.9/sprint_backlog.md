**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-07-27
**Cycle:** 2026-07-27__release-v7.9
**Release:** v7.9
**Sprint Goal:** Ship all 15 v7.9 EPICs — the two P1 UX anchors and the 13 capacity-fill engineering-hardening items — with every acceptance criterion met and QA sign-off recorded for each EPIC. (See `sprint_goal.md`.)
**Backlog Slice Source:** Original — `stage4_backlog_slice.md`

# Sprint Backlog — 2026-07-27__release-v7.9

## Merge Order

**EPIC merge sequence:** EPIC-03 → EPIC-11 → EPIC-13 → EPIC-14 → EPIC-15 → EPIC-09 → EPIC-10 → EPIC-07 → EPIC-08 → EPIC-12 → EPIC-06 → EPIC-04 → EPIC-01 → EPIC-02 → EPIC-05

**`execution_state.json` owner:** EPIC-03 (first in merge sequence). Every other EPIC branch must check for `execution_state.json` before creating its own — if present, append rather than overwrite.

**Shared files across EPICs** (full detail: `sprint_planning_notes.md ## Multi-EPIC Execution Notes`):

| Shared file | Owning EPIC | Must rebase after |
|---|---|---|
| `docs/data_model.md` | EPIC-03 | EPIC-06 |
| `docs/reference/openapi.yaml`, `docs/specs/api_contracts/*.md`, `backend/routers/test.py`, `src/pages/SystemStatus.js`, `tests/e2e/system-status.spec.js` | EPIC-02 | Any EPIC found at kickoff to add a new endpoint (EPIC-06/EPIC-12 unconfirmed — see Outstanding Actions) |
| `render.yaml` | EPIC-12 | — (sole owner this sprint) |

---

## Sprint Scope

### EPIC-01 — Watchlist staleness and decay review

**Maps to:** S2-01
**Owner:** Head of UX & Design; Product Owner
**Estimated effort:** 1.0 days (S)
**Risk IDs:** RISK-01 (resolved — Design Gate Passed)
**Execution sequence:** 13

#### ST-01 — Add staleness tracking and Keep/Remove review action to Watchlist

**Owner:** Head of UX & Design; Product Owner
**Estimated effort:** 1.0
**Delegation class:** autonomous — new section/component against a locked frontend spec (`docs/design/2026-07-27__release-v7.9/watchlist-staleness-review/ux_spec.md`, `docs/specs/frontend/pages/watchlist.md` v0.5), Playwright feasibility expected, per BLG-GOV-72 fast-path (c)

**Acceptance Criteria:** see `stage4_backlog_slice.md#EPIC-01`

**Dependencies:** None

**Notes:** Reuses the existing `PATCH /watchlist/{entry_id}` (timestamp reset for "Keep") and `DELETE /watchlist/{entry_id}` (for "Remove") endpoints confirmed present in `backend/routers/watchlist.py` — not expected to require a new endpoint or same-commit API contract entry. Confirm this at kickoff before assuming no contract change is needed.

**Staging-only ACs:** AC-02 (visual staleness flag) and AC-03 (Keep/Remove interaction) are observable UI — Playwright coverage or recorded staging sign-off required before PR opens (CLAUDE.md §2); confirm feasibility at kickoff.

---

### EPIC-02 — Historical sector/regime exposure trend

**Maps to:** S2-02
**Owner:** Metrics Definitions & Analytics Owner; Head of UX & Design
**Estimated effort:** 2.0 days (M)
**Risk IDs:** RISK-01 (resolved — Design Gate Passed)
**Execution sequence:** 14

#### ST-02 — Add sector concentration / regime exposure trend chart to Risk Dashboard

**Owner:** Metrics Definitions & Analytics Owner; Head of UX & Design
**Estimated effort:** 2.0
**Delegation class:** autonomous — new chart against a locked frontend spec (`docs/design/2026-07-27__release-v7.9/sector-regime-exposure-trend/ux_spec.md`, `docs/specs/frontend/pages/risk_dashboard.md` v0.1.10 §8b — placement corrected at Design Gate from Positions/Reports to Risk Dashboard), no new inputs (aggregates existing `portfolio_history` + sector/regime data)

**Acceptance Criteria:** see `stage4_backlog_slice.md#EPIC-02`

**Dependencies:** None (independent of the EPIC-03/EPIC-06 `data_model.md` cluster)

**Notes:** No existing sector/regime **history** endpoint was found in `backend/routers/portfolio_risk.py` (only current-snapshot endpoints: `sector-weights`, `concentration-status`, `drawdown-status`, `gate-metrics`) — this EPIC will very likely add a new aggregation endpoint. Same-commit API contract entry (`docs/reference/openapi.yaml` + `docs/specs/api_contracts/*.md`) required per CLAUDE.md §2, and `backend/routers/test.py` + `SystemStatus.js` fallback count + `SC-SS-01b` must update in the same commit as the new route. This EPIC owns the shared-file cluster this sprint (see Merge Order).

**Staging-only ACs:** AC-01 (sector concentration trend chart) and AC-02 (regime status trend) are chart-rendering observable UI; AC-03 (insufficient-history graceful state) is an observable UI state — Playwright coverage or recorded staging sign-off required before PR opens (CLAUDE.md §2); confirm feasibility at kickoff.

---

### EPIC-03 — Formalise trade_plan-to-position FK linkage schema

**Maps to:** S2-03
**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** 2.5 days (M)
**Risk IDs:** None
**Execution sequence:** 1

#### ST-03 — Document canonical trade_plan↔position linkage schema in data_model.md

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** 2.5
**Delegation class:** autonomous — documentation-only, no UI, no ambiguous scope

**Acceptance Criteria:** see `stage4_backlog_slice.md#EPIC-03`

**Dependencies:** None (first to touch `data_model.md` this sprint — owns it for the cluster)

**Notes:** No Design Gate dependency (Design Not Applicable). AC-03 requires cross-referencing from the SI-02 gate note in `current_roadmap.md` — a roadmap document touch, not a governance-file edit restricted by write scope (confirm with Head of Specs Team if any ambiguity arises).

**Staging-only ACs:** None — documentation artefact, verifiable by review.

---

### EPIC-04 — Monthly P&L CSV export: tax-lot cost-basis reconciliation

**Maps to:** S2-04
**Owner:** Financial Reporting & Records Owner
**Estimated effort:** 2.5 days (M)
**Risk IDs:** None
**Execution sequence:** 12

#### ST-04 — Add cost-basis method disclosure/reconciliation column to Monthly P&L CSV export

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** 2.5
**Delegation class:** autonomous — extends the existing v7.8 Monthly P&L CSV export (`BLG-FEAT-81`, `backend/routers/trades_export.py`) with an additional disclosure column; no new endpoint expected

**Acceptance Criteria:** see `stage4_backlog_slice.md#EPIC-04`

**Dependencies:** None (hard); sequencing preference after EPIC-06 per `release_plan.md ## Execution Plan` (shared audit-trail/reporting domain — not a hard dependency)

**Notes:** No Design Gate dependency (Design Not Applicable — CSV export column, no in-app UI rendering).

**Staging-only ACs:** None — export column and reconciliation-against-manually-verified-sample AC are verifiable via unit/integration test with fixture trade data.

---

### EPIC-05 — "Why is my stop moving" explainer tooltip on the trailing-stop UI

**Maps to:** S2-05
**Owner:** Head of Engineering; Head of UX & Design
**Estimated effort:** 1.5 days (S)
**Risk IDs:** RISK-01 (resolved — Design Gate Passed)
**Execution sequence:** 15

#### ST-05 — Add trailing-stop rule explainer tooltip to position/trade view

**Owner:** Head of Engineering; Head of UX & Design
**Estimated effort:** 1.5
**Delegation class:** autonomous — new UI element against a locked frontend spec (`docs/design/2026-07-27__release-v7.9/trailing-stop-explainer-tooltip/ux_spec.md`, `docs/specs/frontend/pages/positions.md` v2.5), tooltip text sourced directly from `strategy_rules.md §7`

**Acceptance Criteria:** see `stage4_backlog_slice.md#EPIC-05`

**Dependencies:** None

**Notes:** AC-02 requires the tooltip text to be reviewed against `strategy_rules.md §7` for accuracy — treat as a content-review step, not a strategy-rule change. No new endpoint expected (display-only, reads existing trailing-stop state).

**Staging-only ACs:** AC-01 (tooltip rendering/interaction) is observable UI — Playwright coverage or recorded staging sign-off required before PR opens (CLAUDE.md §2); confirm feasibility at kickoff.

---

### EPIC-06 — Audit trail for manual position overrides

**Maps to:** S2-06
**Owner:** Financial Reporting & Records Owner
**Estimated effort:** 2.5 days (M)
**Risk IDs:** None
**Execution sequence:** 11

#### ST-06 — Add audit-log entries for manual position edits (who, when, before/after)

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** 2.5
**Delegation class:** delegated_decision — no existing "manual position edit" API endpoint was found in `backend/routers/` at planning time; the actual write path to instrument (an existing internal service call vs. a new endpoint) is not fully specified in the backlog item and must be confirmed with Financial Reporting & Records Owner before implementation begins

**Acceptance Criteria:** see `stage4_backlog_slice.md#EPIC-06`

**Dependencies:** ST-03 (shared file: `docs/data_model.md` — rebase after EPIC-03 merges)

**Notes:** No Design Gate dependency (Design Not Applicable — backend audit logging, no UI). Distinct from `BLG-SEC-14`'s AI-journal-generation audit trail (different write path). If the confirmed write path turns out to require a new endpoint, apply the same-commit `openapi.yaml`/`api_contracts`/`backend/routers/test.py`/`SystemStatus.js`/`SC-SS-01b` requirements (CLAUDE.md §2) and rebase onto `main` after EPIC-02 merges.

**Staging-only ACs:** None expected — audit-log entry creation is verifiable via unit/integration test asserting before/after values are recorded; reconfirm once the write path is settled at kickoff.

---

### EPIC-07 — Nightly backtest data-integrity smoke test as a standing CI gate

**Maps to:** S2-07
**Owner:** Head of Engineering
**Estimated effort:** 2.5 days (M)
**Risk IDs:** RISK-02
**Execution sequence:** 8

#### ST-07 — Add permanent data-integrity smoke test to the nightly backtest CI job

**Owner:** Head of Engineering
**Estimated effort:** 2.5
**Delegation class:** autonomous — CI/backend tooling, checks the same invariant class as three prior one-off audits (`BLG-BE-59/60`, `BLG-BE-63`)

**Acceptance Criteria:** see `stage4_backlog_slice.md#EPIC-07`

**Dependencies:** None

**Notes:** RISK-02 — a newly-surfaced data-integrity defect during this build should be filed as its own backlog item, not treated as blocking this story's own AC (per `stage4_backlog_slice.md` Notes).

**Staging-only ACs:** None — CI smoke test behaviour (added, passes on current data) is fully verifiable in CI.

---

### EPIC-08 — Provision a staging credential for SI-02 live gate re-checks

**Maps to:** S2-08
**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 1.5 days (S)
**Risk IDs:** None
**Execution sequence:** 9

#### ST-08 — Provision and document a read-only staging/scoped-production credential

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 1.5
**Delegation class:** delegated_decision — obtaining a genuine external API credential requires human action (account/console access); the execution engine can prepare storage/documentation but cannot generate the actual secret

**Acceptance Criteria:** see `stage4_backlog_slice.md#EPIC-08`

**Dependencies:** External — real credential provisioning (see `sprint_planning_notes.md ## Dependency Map`)

**Notes:** No Design Gate dependency (Design Not Applicable — infra/credential provisioning, no UI). AC-02 ("next scheduled roadmap rebalance can perform a genuine live SI-02 re-check") is only verifiable at the next rebalance, after this sprint closes — flag this to Director of Quality as a delayed-verification AC.

**Staging-only ACs:** AC-01/AC-03 (provisioning + sign-off) are verifiable by documentation review; AC-02 is inherently deferred past this sprint's close — not a CI-verifiable AC, and not a staging-UI AC either. Record as `None` for CI-verifiability purposes but note the delayed-verification caveat above.

---

### EPIC-09 — Shared cross-EPIC smoke-test tagging for parallel-branch merges

**Maps to:** S2-09
**Owner:** QA Lead
**Estimated effort:** 2.5 days (M)
**Risk IDs:** None
**Execution sequence:** 6

#### ST-09 — Define a common regression smoke-test tag/suite for EPIC-branch merges

**Owner:** QA Lead
**Estimated effort:** 2.5
**Delegation class:** autonomous — CI/process tooling extending `shared_standards.md §12`, no UI change

**Acceptance Criteria:** see `stage4_backlog_slice.md#EPIC-09`

**Dependencies:** None

**Notes:** No Design Gate dependency (Design Not Applicable). Directly relevant to this sprint's own 15-EPIC merge sequence — consider dogfooding the new tag on this sprint's own later merges if ready in time (not a hard requirement).

**Staging-only ACs:** None — tag/suite definition and its documentation in `shared_standards.md §12` are verifiable by review and CI run.

---

### EPIC-10 — Pre-commit hook automating the `backend/routers/test.py` registration check

**Maps to:** S2-10
**Owner:** QA & Testing Owner
**Estimated effort:** 1.5 days (S)
**Risk IDs:** None
**Execution sequence:** 7

#### ST-10 — Add pre-commit hook blocking commits with unregistered new routes

**Owner:** QA & Testing Owner
**Estimated effort:** 1.5
**Delegation class:** autonomous — tooling only, no UI change, mechanical grep-based check

**Acceptance Criteria:** see `stage4_backlog_slice.md#EPIC-10`

**Dependencies:** None

**Notes:** No Design Gate dependency (Design Not Applicable). Must be tested against a deliberately-missing case per AC-02.

**Staging-only ACs:** None — hook behaviour (including the negative test) is fully verifiable via local pre-commit run / CI.

---

### EPIC-11 — WCAG contrast checklist addendum for chart colour palettes

**Maps to:** S2-11
**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.0 days (S)
**Risk IDs:** None
**Execution sequence:** 2

#### ST-11 — Add chart-specific contrast checklist item to design_system.md Accessibility section

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.0
**Delegation class:** autonomous — documentation addendum, no shipped UI change

**Acceptance Criteria:** see `stage4_backlog_slice.md#EPIC-11`

**Dependencies:** None

**Notes:** No Design Gate dependency (Design Not Applicable). Sole owner of `design_system.md` this sprint — no other EPIC touches it.

**Staging-only ACs:** None — documentation artefact, verifiable by review.

---

### EPIC-12 — Cost-tag cloud infrastructure spend by EPIC

**Maps to:** S2-12
**Owner:** FinOps & Resource Architect
**Estimated effort:** 2.5 days (M)
**Risk IDs:** None
**Execution sequence:** 10

#### ST-12 — Add EPIC-level cost tags to cloud resources and produce a per-EPIC spend summary

**Owner:** FinOps & Resource Architect
**Estimated effort:** 2.5
**Delegation class:** autonomous — `render.yaml` supports config-level tagging in-repo; spend summary is a generated report, not in-app UI

**Acceptance Criteria:** see `stage4_backlog_slice.md#EPIC-12`

**Dependencies:** None

**Notes:** No Design Gate dependency (Design Not Applicable — infra tagging/reporting, no in-app UI). If Render's actual tagging support requires console/dashboard action beyond `render.yaml`, flag as an external dependency at kickoff (same class of gap as EPIC-08). Distinct domain from the existing `/ai/monthly-cost` / `/ai/spend-trend` endpoints (AI token spend, not cloud infra spend) — confirm no overlap/duplication with those at kickoff.

**Staging-only ACs:** None — cost tags and the summary report are verifiable by config/artefact review.

---

### EPIC-13 — Dark-mode acceptance-criteria checklist addendum for Base44 prompt drafts

**Maps to:** S2-13
**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** 1.0 days (S)
**Risk IDs:** None
**Execution sequence:** 3

#### ST-13 — Add dark-mode AC checklist item to the Base44 prompt template

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** 1.0
**Delegation class:** autonomous — process template edit, no shipped UI change

**Acceptance Criteria:** see `stage4_backlog_slice.md#EPIC-13`

**Dependencies:** None

**Notes:** No Design Gate dependency (Design Not Applicable). Follows on from the v7.8 dark-mode contrast audit (`BLG-FE-125`) that found issues after the fact.

**Staging-only ACs:** None — template edit, verifiable by review.

---

### EPIC-14 — Displacement debt register — track unused named displacement candidates

**Maps to:** S2-14
**Owner:** Challenger; Head of Specs Team
**Estimated effort:** 1.0 days (S)
**Risk IDs:** None
**Execution sequence:** 4

#### ST-14 — Add rolling log of named displacement candidates and their disposition

**Owner:** Challenger; Head of Specs Team
**Estimated effort:** 1.0
**Delegation class:** autonomous — governance process artefact, no UI

**Acceptance Criteria:** see `stage4_backlog_slice.md#EPIC-14`

**Dependencies:** None

**Notes:** No Design Gate dependency (Design Not Applicable). Format decision is self-contained; no external stakeholder input required beyond Head of Specs Team sign-off.

**Staging-only ACs:** None — log format and documentation, verifiable by review.

---

### EPIC-15 — Defined visual-regression baseline refresh cadence for Grid View components

**Maps to:** S2-15
**Owner:** Head of UX & Design
**Estimated effort:** 1.0 days (S)
**Risk IDs:** None
**Execution sequence:** 5

#### ST-15 — Define refresh cadence for Grid View visual-regression baselines

**Owner:** Head of UX & Design
**Estimated effort:** 1.0
**Delegation class:** autonomous — cadence definition/process, no shipped UI change

**Acceptance Criteria:** see `stage4_backlog_slice.md#EPIC-15`

**Dependencies:** None

**Notes:** No Design Gate dependency (Design Not Applicable). Builds on `BLG-QA-81`'s initial visual-regression baselines. Requires both Head of UX & Design and Director of Quality sign-off per AC-02.

**Staging-only ACs:** None — cadence documentation, verifiable by review.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24-28 working-day-equivalent |
| Total estimated effort (in-scope) | ~26.5 days |
| Utilisation | ~95-110% |
| Over-allocation | No |

## Items Deferred This Sprint

None — all 15 EPICs / ST items are in scope.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Confirm the manual-position-edit write path for EPIC-06 before implementation begins | Financial Reporting & Records Owner | No |
| Provision the real staging/scoped-production credential for EPIC-08 | Infrastructure & Operations Owner | No |
| Escalate to Head of Specs Team if the `execution_state.json` cross-EPIC merge conflict recurs a 3rd consecutive time this sprint | Sprint Execution / Head of Specs Team | No |
| Prompt change log gaps across 7 files (advisory, pre-existing — not introduced this session; see `sprint_planning_notes.md`) | Head of Specs Team | No |
| Confirm Playwright feasibility / arrange staging sign-off for EPIC-01/02/05 observable ACs at kickoff | Director of Quality | No |
| Confirm at kickoff whether EPIC-02 (and possibly EPIC-06/EPIC-12) require a new backend endpoint and apply same-commit contract/test-suite requirements accordingly | Head of Engineering | No |

No outstanding action is marked `Blocker? Yes`.

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — 2026-07-27 (see `sprint_goal.md`)
**Scope confirmed:** Confirmed — all 15 EPICs / ST items, no deferrals, no over-allocation
**Capacity confirmed:** Confirmed — ~26.5 days vs ~24-28 day ceiling, no WARN (deliberately at top of band per explicit user "use the full capacity" instruction, RISK-03 accepted)
**Deferred execution blockers accepted (if any):** N/A — `deferred_execution_blockers` empty in `state.json`
**Signed off by:** Product Owner
**Date:** 2026-07-27
