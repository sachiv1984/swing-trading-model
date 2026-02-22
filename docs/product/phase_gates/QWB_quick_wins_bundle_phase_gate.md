# Phase Gate Document — Quick Wins Bundle

**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Created:** 2026-02-22
**Filed:** — (immutable on closure)

**Charter authority:** `docs/team_skills/pmo/processess/pre_alignment_run.md`

---

## Feature Summary

| Field | Value |
|-------|-------|
| Feature | Quick Wins Bundle — BLG-FEAT-01, 02, 04, 05, 06, 07 |
| Roadmap entry | `docs/product/roadmap.md` — v1.6.1 Quick Wins Bundle |
| Target release | v1.6.1 |
| PMO Lead | PMO Lead |
| Date opened | 2026-02-22 |
| Date shipped | — |

---

## Bundle Items

| Item | Description | Effort |
|------|-------------|--------|
| BLG-FEAT-01 | Current Drawdown Widget | ~30 min |
| BLG-FEAT-02 | R-Multiple Column in Trade History | ~1 hour |
| BLG-FEAT-04 | Best / Worst Trades Widget | ~1 hour |
| BLG-FEAT-05 | Win Rate by Month Chart | ~1 hour |
| BLG-FEAT-06 | Grace Period Indicator | ~1 hour |
| BLG-FEAT-07 | CSV Export of Trade History | ~1 hour |

**Total estimated effort (implementation only):** ~6–8 hours
**Spec authoring effort:** TBD at pre-alignment meeting

---

## Current Status
```
Current phase:    Phase 0 — Readiness Audit
Gate passed:      —
Next gate:        Gate R — all readiness items cleared → AWAITING_MEETING
Who acts next:    Metrics Definitions owner (A-PRE-01, A-PRE-02); API Contracts owner (A-PRE-03); PMO Lead (A-PRE-04)
What they do:     Provide written formula confirmations and field exposure confirmation
Deadline:         As soon as possible — meeting cannot be scheduled until complete
Blockers:         A-PRE-01 and A-PRE-02 (roadmap-stated pre-alignment gates — blocking)
```

---

## Phase History

| Phase | Gate condition | Status | Date | Notes |
|-------|---------------|--------|------|-------|
| Phase 0 — Readiness Audit | Audit complete, Go/No-Go issued | 🟡 In progress | 2026-02-22 | Conditional Go issued. Pre-meeting actions block meeting scheduling. |
| Phase 1 — Pre-Alignment Meeting | All decisions closed, decisions record committed | ⬜ Not started | — | |
| Phase 2 — Parallel Spec Delivery | All spec actions complete and committed | ⬜ Not started | — | |
| Phase 3 — QA Review Gate | QA sign-off confirmed | ⬜ Not started | — | |
| Phase 4 — Scope Document | Scope document committed, implementation declared open | ⬜ Not started | — | |
| Implementation | Engineering builds against locked specs | ⬜ Not started | — | |
| Phase 5 — Verification | All criteria pass, Director of Quality final sign-off | ⬜ Not started | — | |
| Shipping Closure | Changelog, roadmap, supersession actions complete | ⬜ Not started | — | |

Status key: ⬜ Not started | 🟡 In progress | ✅ Complete | 🔴 Blocked

---

## Gate R — READINESS_AUDIT → AWAITING_MEETING

### Gate R.1 — Data model readiness confirmed
```
Gate item:  All fields the bundle reads or writes exist in data_model.md,
            or are pre-designed with type, constraint, default, and migration documented.

Evidence required:
  BLG-FEAT-01: drawdown formula confirmation from Metrics Definitions owner
  BLG-FEAT-02: R-multiple formula confirmation from Metrics Definitions owner
  BLG-FEAT-05: monthly_data field confirmed present in GET /analytics/metrics — existing
  BLG-FEAT-06: grace days field confirmed in GET /positions response
  BLG-FEAT-07: no schema changes required — confirmed by audit

#### R.1 — BLG-FEAT-01: Drawdown formula confirmed

 Evidence:         `docs/specs/metrics_definitions.md` [MISSING: version number after update]
                    Formula confirmed: [MISSING: exact formula e.g. "(peak_equity - current_equity) / peak_equity"]
                    Data source confirmed: [MISSING: existing GET /analytics/metrics field name OR new endpoint required]
                    Display format confirmed: [MISSING: e.g. "Drawdown: -8.2%, 12 days underwater"]
 Owner confirmation: [MISSING: Yes/No] — Metrics Definitions owner, [MISSING: date]
 PMO validation:   [MISSING: Pass/Fail] — PMO Lead, [MISSING: date]

#### R.1 — BLG-FEAT-02: R-multiple formula confirmed

 Evidence:         `docs/specs/metrics_definitions.md` [MISSING: version number after update]
                    Formula confirmed: [MISSING: e.g. "(exit_price - entry_price) / (entry_price - stop_price)"]
                    Calculation location: [MISSING: server-side (new endpoint field) OR frontend-only derivation]
                    If server-side: endpoint and field name: [MISSING]
 Owner confirmation: [MISSING: Yes/No] — Metrics Definitions owner, [MISSING: date]
 PMO validation:   [MISSING: Pass/Fail] — PMO Lead, [MISSING: date]

```
### Gate R.1a — Settings table dependency

```
Gate item:  No bundle item reads from or writes to the settings table.

- Evidence:         Audit confirmed no settings dependency across all six items.
- Owner confirmation: Yes — PMO Lead, 2026-02-22
- PMO validation:   Pass — PMO Lead, 2026-02-22

```
### Gate R.2 — API contract readiness confirmed

```
Gate item:  All required endpoints documented, or API Contracts owner briefed.

Evidence required:
  BLG-FEAT-07: new CSV export endpoint — API Contracts owner not yet briefed
  BLG-FEAT-06: grace days field exposure in GET /positions — confirmation outstanding
  BLG-FEAT-02: server-side vs frontend decision open — determines whether endpoint change needed

#### R.2 — BLG-FEAT-06: Grace days field confirmed in GET /positions

 Evidence:         `docs/specs/api_contracts/` [MISSING: exact file name and version]
                    Field confirmed present: [MISSING: Yes — field name e.g. "grace_days_remaining" /
                    No — endpoint update required, field name and type to be added]
                    If absent: contract update scope: [MISSING: field name, type, example value]
 Owner confirmation: [MISSING: Yes/No] — API Contracts owner, [MISSING: date]
 PMO validation:   [MISSING: Pass/Fail] — PMO Lead, [MISSING: date]

#### R.2 — BLG-FEAT-07: CSV export endpoint briefing confirmed

 Evidence:          API Contracts owner briefed by PMO Lead: [MISSING: date of briefing]
                    Endpoint path agreed: [MISSING: e.g. "GET /trades/export/csv"]
                    Fields confirmed: [MISSING: list of fields to include in CSV]
                    Scope: [MISSING: full history / filtered by date range / other]
                    Contract document to be authored: `docs/specs/api_contracts/` [MISSING: file name]
 Owner confirmation: [MISSING: Yes/No] — API Contracts owner, [MISSING: date]
 PMO validation:   [MISSING: Pass/Fail] — PMO Lead, [MISSING: date]

```

### Gate R.3 — Frontend spec readiness confirmed

```
Gate item:  Relevant component/page specs current, or UX decisions pre-resolved.

Evidence required:
  Confirm which page/component spec each item targets (positions table, trade history,
  analytics page). Frontend Spec owner must be briefed before meeting.

 Evidence:         Written briefing confirmation from Frontend Spec owner.
                    Page/component targets confirmed per item:
                    BLG-FEAT-01 (Drawdown Widget): [MISSING: target page/component]
                    BLG-FEAT-02 (R-Multiple Column): [MISSING: target page/component — likely trade history table]
                    BLG-FEAT-04 (Best/Worst Widget): [MISSING: target page/component]
                    BLG-FEAT-05 (Win Rate by Month): [MISSING: target page/component — likely analytics page]
                    BLG-FEAT-06 (Grace Period Indicator): [MISSING: target page/component — likely positions table]
                    BLG-FEAT-07 (CSV Export): [MISSING: target page/component — likely trade history]
                    Spec currency: [MISSING: confirm relevant component spec is current or note gaps]
 Owner confirmation: [MISSING: Yes/No] — Frontend Spec owner, [MISSING: date]
 PMO validation:   [MISSING: Pass/Fail] — PMO Lead, [MISSING: date]

```

### Gate R.4 — Strategy rules readiness confirmed

```
Gate item:  No bundle item requires changes to strategy_rules.md.
            Grace period lifecycle is already defined there.

- Evidence:         Audit confirmed. No strategy_rules.md changes required.
- Owner confirmation: Yes — PMO Lead, 2026-02-22
- PMO validation:   Pass — PMO Lead, 2026-02-22

```

### Gate R.5 — Effort estimate reviewed

```
Gate item:  Roadmap estimate accounts for all spec, backend, and frontend work.

Note:       Current estimate (~6–8 hours) covers implementation only.
            Spec authoring for BLG-FEAT-07 (new endpoint) and BLG-FEAT-02
            (if server-side) is additional. Estimate must be revised at meeting.

 Evidence:         Product Owner revised estimate confirmed.
                    Implementation effort: ~6–8 hours (unchanged)
                    Spec authoring — BLG-FEAT-07 new endpoint: [MISSING: estimated hours]
                    Spec authoring — BLG-FEAT-02 if server-side: [MISSING: estimated hours or N/A]
                    Revised total estimate: [MISSING: X hours]
                    Roadmap entry updated: [MISSING: Yes/No — docs/product/roadmap.md commit hash]
 Owner confirmation: [MISSING: Yes/No] — Product Owner, [MISSING: date]
 PMO validation:   [MISSING: Pass/Fail] — PMO Lead, [MISSING: date]

```

### Gate R.6 — Decisions inventory produced

```
Gate item:  Preliminary decisions list produced and agreed as meeting agenda.

- Evidence:         Readiness audit produced 6 open decisions (D1–D6). Filed in this document.
- Owner confirmation: Yes — PMO Lead, 2026-02-22
- PMO validation:   Pass — PMO Lead, 2026-02-22
```

**Gate R overall status: 🔴 FAIL — R.1, R.2, R.3, R.5 outstanding. Meeting may not be scheduled.**

---

## Action Register

| # | Action | Owner | Deadline | Status | Blocked on |
|---|--------|-------|----------|--------|------------|
| A-PRE-01 | Provide written confirmation of drawdown formula for BLG-FEAT-01 — apply to Gate R.1 patch | Metrics Definitions owner | 2026-02-23T17:00:00Z (PROPOSED) | 🔴 OPEN | — |
| A-PRE-02 | Provide written confirmation of R-multiple formula + server-side vs frontend decision — apply to Gate R.1 patch | Metrics Definitions owner | 2026-02-23T17:00:00Z (PROPOSED) | 🔴 OPEN | — |
| A-PRE-03 | Confirm grace days field in GET /positions — apply to Gate R.2 patch | API Contracts owner | 2026-02-23T17:00:00Z (PROPOSED) | 🔴 OPEN | — |
| A-PRE-04 | Confirm CSV export endpoint scope after PMO briefing — apply to Gate R.2 patch | API Contracts owner | 2026-02-23T17:00:00Z (PROPOSED) | 🔴 OPEN | A-PRE-04 briefing by PMO Lead |
| A-PRE-05 | Confirm briefing received + page/component targets for all six items — apply to Gate R.3 patch | Frontend Spec owner | 2026-02-23T17:00:00Z (PROPOSED) | 🔴 OPEN | PMO Lead briefing |
| A-PRE-06 | Confirm revised total effort estimate including spec authoring — apply to Gate R.5 patch | Product Owner | 2026-02-24T12:00:00Z (PROPOSED) | 🔴 OPEN | A-PRE-02 (server-side decision) |
| A-PRE-07 | Confirm or replace all PROPOSED deadlines above with actual UTC deadlines | Product Owner | 2026-02-23T12:00:00Z (PROPOSED) | 🔴 OPEN | — |


> GI-2 compliant: All deadlines are either UTC-dated (PROPOSED) or [MISSING] with A-PRE-07 covering resolution.
> PROPOSED deadlines become binding when confirmed by Product Owner via A-PRE-07.

---

## Preliminary Decisions List (Meeting Agenda)

| # | Decision | Owner | Pre-condition |
|---|----------|-------|---------------|
| D1 | BLG-FEAT-01: Drawdown formula and data source (existing endpoint or new?) | Metrics Definitions owner | A-PRE-01 must be complete first |
| D2 | BLG-FEAT-02: R-multiple formula confirmed; server-side or frontend-only? | Metrics Definitions owner + API Contracts owner | A-PRE-02 must be complete first |
| D3 | BLG-FEAT-04: Best/Worst Trades — ranked by R-multiple or P&L? | Product Owner | D2 must be closed first |
| D4 | BLG-FEAT-06: Grace days field confirmed in GET /positions; if absent, scope endpoint addition | API Contracts owner | A-PRE-03 |
| D5 | BLG-FEAT-07: CSV endpoint path, fields, filtered vs full history | API Contracts owner | A-PRE-04 |
| D6 | BLG-TECH-06: In scope for this bundle or tracked separately? | Product Owner + API Contracts owner | — |

---

## Open Blockers

| # | Blocker | Affects | Owner | Raised | Status |
|---|---------|---------|-------|--------|--------|
| B-01 | Metrics Definitions owner formula confirmations not received (A-PRE-01, A-PRE-02) | Gate R.1 — meeting scheduling | Metrics Definitions owner | 2026-02-22 | 🔴 Open |
| B-02 | API Contracts owner not yet briefed on CSV endpoint (A-PRE-04) | Gate R.2 | PMO Lead | 2026-02-22 | 🔴 Open |
| B-03 | Frontend Spec owner not yet briefed (A-PRE-05) | Gate R.3 | PMO Lead | 2026-02-22 | 🔴 Open |

---

## State Transition Log

| # | From | To | Date | Time (UTC) | Declared by | Gate passed |
|---|------|----|------|------------|-------------|-------------|
| 1 | PRE-LOGGED | READINESS_AUDIT | 2026-02-22 | 00:00:00Z | PMO Lead | — (Product Owner nomination received) |

---

## Decisions Record Reference

Pre-alignment decisions: `docs/product/decisions/QWB-quick-wins-bundle.md`
*(to be created at Phase 1)*

---

## Shipping Closure Checklist

- [ ] Changelog entry added (`docs/product/changelog.md`)
- [ ] Roadmap updated — all six items → ✅ Complete, version bumped
- [ ] Scope document status → Superseded
- [ ] Decisions record status → Superseded
- [ ] Head of Engineering notified
- [ ] Lessons learnt review scheduled
- [ ] This phase gate document status → Shipped, date filed
