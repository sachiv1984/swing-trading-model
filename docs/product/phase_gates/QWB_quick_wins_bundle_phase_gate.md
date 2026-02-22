# Phase Gate Document — Quick Wins Bundle

**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.2
**Created:** 2026-02-22
**Last Updated:** 2026-02-24
**Filed:** — (immutable on closure)

**Charter authority:** `docs/team_skills/pmo/processess/pre_alignment_run.md` v2.0

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

| Item | Description | Target page | Effort |
|------|-------------|-------------|--------|
| BLG-FEAT-01 | Current Drawdown Widget | Dashboard — stats row | ~30 min |
| BLG-FEAT-02 | R-Multiple Column in Trade History | Trade History table | ~1 hour |
| BLG-FEAT-04 | Best / Worst Trades Widget | Performance Analytics page | ~1 hour |
| BLG-FEAT-05 | Win Rate by Month Chart | Performance Analytics page | ~1 hour |
| BLG-FEAT-06 | Grace Period Indicator | Open Positions table | ~1 hour |
| BLG-FEAT-07 | CSV Export of Trade History | Trade History page | ~1 hour |

**Total estimated effort:** ~8–10.5 hours (implementation + spec authoring)

---

## Current Status

```
Current phase:    SPEC_DELIVERY
Gate passed:      Gate 1 — 2026-02-24
Next gate:        Gate 2 — all spec actions committed and verified
Who acts next:    API Contracts owner (A-S02, A-S03, A-S04 — sequential)
                  + Metrics Definitions owner (A-S01)
                  + Product Owner (A-S05)
                  + Frontend Spec owner (A-S07, A-S09 — can start now)
Deadline:         Parallel stream: 2026-02-25T17:00:00Z
                  Frontend spec stream: 2026-02-26T17:00:00Z
Blockers:         None
```

---

## Phase History

| Phase | Gate condition | Status | Date | Notes |
|-------|---------------|--------|------|-------|
| Phase 0 — Readiness Audit | Audit complete, Go/No-Go issued | ✅ Complete | 2026-02-22 | Gate R passed. All items confirmed. |
| Phase 1 — Pre-Alignment Meeting | All decisions closed, decisions record committed | ✅ Complete | 2026-02-24 | 13 decisions closed. Zero deferrals. Record committed. |
| Phase 2 — Parallel Spec Delivery | All spec actions complete and committed | 🟡 In progress | 2026-02-24 | 11 actions open across 3 owners. |
| Phase 3 — QA Review Gate | QA sign-off confirmed | ⬜ Not started | — | |
| Phase 4 — Scope Document | Scope document committed, implementation declared open | ⬜ Not started | — | |
| Implementation | Engineering builds against locked specs | ⬜ Not started | — | |
| Phase 5 — Verification | All criteria pass, Director of Quality final sign-off | ⬜ Not started | — | |
| Shipping Closure | Changelog, roadmap, supersession actions complete | ⬜ Not started | — | |

Status key: ⬜ Not started | 🟡 In progress | ✅ Complete | 🔴 Blocked

---

## Gate R — ✅ COMPLETE (2026-02-22)

All 6 gate items passed. Full evidence record in phase gate document v1.1.

---

## Gate 0 — ✅ COMPLETE (2026-02-23)

```
Gate 0.1 — All required attendees confirmed
  Evidence:             Meeting invitation QWB-PA-001 issued 2026-02-23. All 7 roles confirmed.
  Owner confirmation:   Yes — PMO Lead, 2026-02-23
  PMO validation:       Pass — PMO Lead, 2026-02-23

Gate 0.2 — Decisions list distributed
  Evidence:             D1–D12 + D2a full agenda distributed with invitation 2026-02-23
  Owner confirmation:   Yes — PMO Lead, 2026-02-23
  PMO validation:       Pass — PMO Lead, 2026-02-23
```

---

## Gate 1 — ✅ COMPLETE (2026-02-24)

```
Gate 1.1 — All decisions closed or explicitly deferred
  Evidence:             docs/product/decisions/QWB-quick-wins-bundle.md, 2026-02-24
                        13 decisions closed (D1–D12 + D2a). Zero deferrals. Zero open questions.
  Owner confirmation:   Yes — Product Owner, 2026-02-24
  PMO validation:       Pass — PMO Lead, 2026-02-24

Gate 1.2 — Decisions record committed
  Evidence:             docs/product/decisions/QWB-quick-wins-bundle.md committed 2026-02-24
  Owner confirmation:   Yes — Product Owner, 2026-02-24
  PMO validation:       Pass — PMO Lead, 2026-02-24

Gate 1.3 — Action list produced
  Evidence:             Spec Delivery Action Table below — 11 actions, owners, deadlines,
                        dependencies all assigned. Critical path identified.
  Owner confirmation:   Yes — PMO Lead, 2026-02-24
  PMO validation:       Pass — PMO Lead, 2026-02-24

Gate 1.4 — Critical path communicated
  Evidence:             All owners notified of first action and deadline 2026-02-24
  Owner confirmation:   Yes — PMO Lead, 2026-02-24
  PMO validation:       Pass — PMO Lead, 2026-02-24
```

---

## Gate 2 — 🟡 IN PROGRESS

```
Gate 2.1 — All spec actions confirmed complete
  Evidence:             [PENDING — A-S01 through A-S11 must all show ✅ Complete]
  PMO validation:       [PENDING]

Gate 2.2 — openapi.yaml committed in same PR as each API contract change
  Evidence:             [PENDING — A-S02, A-S03, A-S04 each require same-PR openapi.yaml]
  PMO validation:       [PENDING]

Gate 2.3 — Patch verification confirmed for all patched files
  Evidence:             [PENDING — each owner confirms specific changed text]
  PMO validation:       [PENDING]

Gate 2.4 — No open decisions
  Evidence:             [PENDING — confirm no new questions arose during spec delivery]
  PMO validation:       [PENDING]
```

---

## Spec Delivery Action Table

### Parallel stream — no dependencies, start immediately

| # | Action | Owner | Deadline | Status | Blocked on | Evidence |
|---|--------|-------|----------|--------|------------|---------|
| A-S01 | Add Current Drawdown section to `metrics_definitions.md` → v1.5.8. Include: formula, data sources (GET /portfolio fields), failure behaviour (0.0 when no history), relationship to days_underwater. | Metrics Definitions owner | 2026-02-25T17:00:00Z | 🟡 Not started | — | — |
| A-S02 | Add `current_drawdown_percent` (float, ≤0.0, default 0.0) and `peak_portfolio_value` (float, GBP, default 0.0) to GET /portfolio response in `portfolio_endpoints.md`. Update `openapi.yaml` in same PR. | API Contracts owner | 2026-02-25T17:00:00Z | 🟡 Not started | — | — |
| A-S03 | Add `grace_days_remaining` (integer \| null) to GET /positions response in `position_endpoints.md`. Formula: `max(0, 10 - holding_days)` when `grace_period = true`; null otherwise. Always present. Update `openapi.yaml` in same PR. | API Contracts owner | 2026-02-25T17:00:00Z | 🟡 Not started | GI-1: complete A-S02 first | — |
| A-S04 | Add `GET /trades/export/csv` section to `trade_endpoints.md`. 14 fields (see D5). Response: text/csv, attachment. No params. Update `openapi.yaml` in same PR. | API Contracts owner | 2026-02-25T17:00:00Z | 🟡 Not started | GI-1: complete A-S03 first | — |
| A-S05 | Update `docs/product/roadmap.md` — QWB effort estimate to ~8–10.5 hours; itemise spec authoring additions. | Product Owner | 2026-02-25T17:00:00Z | 🟡 Not started | — | — |
| A-S07 | Update trade history component spec — R-multiple column: formula `(exit-entry)/(entry-stop)`, `trades_for_charts` source, frontend-only calculation, colour threshold convention. | Frontend Spec owner | 2026-02-26T17:00:00Z | 🟡 Not started | — (no API dependency) | — |
| A-S09 | Update analytics page spec — Best/Worst Trades widget (R-multiple ranking, top 3/bottom 3, `trades_for_charts`) + Win Rate by month chart (`monthly_data[].win_rate`). | Frontend Spec owner | 2026-02-26T17:00:00Z | 🟡 Not started | — (no API dependency) | — |

### Blocked stream — waits for upstream commits

| # | Action | Owner | Deadline | Status | Blocked on | Evidence |
|---|--------|-------|----------|--------|------------|---------|
| A-S06 | Update dashboard stats frontend spec — drawdown widget: stats row placement, GET /portfolio data source (drawdown %), GET /analytics/metrics data source (days_underwater, max_drawdown), at-peak state, progress bar, colour threshold convention (impl detail). | Frontend Spec owner | 2026-02-26T17:00:00Z | ⛔ Blocked | A-S01 + A-S02 committed | — |
| A-S08 | Update positions table spec — `grace_days_remaining` column: display format "Day X of 10", null = not in grace (hide or dash). | Frontend Spec owner | 2026-02-26T17:00:00Z | ⛔ Blocked | A-S03 committed | — |
| A-S10 | Update trade history page spec — CSV export button: triggers GET /trades/export/csv, browser file download, button placement. | Frontend Spec owner | 2026-02-26T17:00:00Z | ⛔ Blocked | A-S04 committed | — |
| A-S11 | Update `api_dependencies.md` — add: Dashboard page → GET /portfolio new fields; Positions table → GET /positions new field; Trade History page → GET /trades/export/csv. | Frontend Spec owner | 2026-02-26T17:00:00Z | ⛔ Blocked | A-S02 + A-S03 + A-S04 committed | — |

### Critical path

```
2026-02-25T17:00:00Z target:
  A-S01 ─────────────────────────────────────────────────────┐
  A-S02 → A-S03 → A-S04 (sequential per GI-1) ──────────────┤
  A-S05 ─────────────────────────────────────────────────────┤ all complete
  A-S07 ─────────────────────────────────────────────────────┤
  A-S09 ─────────────────────────────────────────────────────┘

2026-02-26T17:00:00Z target:
  A-S06 (unblocked by A-S01 + A-S02) ───────────────────────┐
  A-S08 (unblocked by A-S03) ────────────────────────────────┤
  A-S10 (unblocked by A-S04) ────────────────────────────────┤ → Gate 2
  A-S11 (unblocked by A-S02 + A-S03 + A-S04) ───────────────┘
```

---

## Stakeholder Next Steps

**As of 2026-02-24:**

| Role | Action | By when |
|------|--------|---------|
| **Metrics Definitions owner** | A-S01 — add Current Drawdown section to `metrics_definitions.md` v1.5.8 | 2026-02-25T17:00:00Z |
| **API Contracts owner** | A-S02 — `portfolio_endpoints.md` + `openapi.yaml` | 2026-02-25T17:00:00Z |
| **API Contracts owner** | A-S03 — `position_endpoints.md` + `openapi.yaml` (after A-S02 complete) | 2026-02-25T17:00:00Z |
| **API Contracts owner** | A-S04 — `trade_endpoints.md` + `openapi.yaml` (after A-S03 complete) | 2026-02-25T17:00:00Z |
| **Product Owner** | A-S05 — roadmap effort estimate update | 2026-02-25T17:00:00Z |
| **Frontend Spec owner** | A-S07 — trade history spec (R-multiple column) — start now | 2026-02-26T17:00:00Z |
| **Frontend Spec owner** | A-S09 — analytics page spec (Best/Worst + Win Rate) — start now | 2026-02-26T17:00:00Z |
| **Frontend Spec owner** | A-S06, A-S08, A-S10, A-S11 — start when upstream commits confirmed | 2026-02-26T17:00:00Z |
| **Engineering** | No action. Discard `WidgetLibrary.jsx`. Note: prototype `days_underwater` calc and `dataSource` fallback logic to be removed when implementation begins. | Before implementation |
| **QA & Testing Owner** | No action until Gate 2 passes | — |

---

## Open Blockers

**No open blockers.**

---

## Decisions Record Reference

`docs/product/decisions/QWB-quick-wins-bundle.md` — committed 2026-02-24

| # | Decision | Summary |
|---|----------|---------|
| D1 | BLG-FEAT-01 formula + endpoint | `(peak-current)/peak×100` via GET /portfolio (2 new fields) |
| D2 | BLG-FEAT-02 R-multiple | Frontend-only, `metrics_definitions.md` v1.5.7 canonical, no spec change |
| D2a | stop_price in GET /trades | Absent — use `trades_for_charts` |
| D3 | BLG-FEAT-04 ranking | R-multiple, top 3 / bottom 3 |
| D4 | BLG-FEAT-06 grace field | New `grace_days_remaining` on GET /positions |
| D5 | BLG-FEAT-07 CSV export | GET /trades/export/csv, 14 fields confirmed |
| D6 | BLG-TECH-06 scope | Out of QWB — separate delivery |
| D7 | days_underwater source | GET /analytics/metrics trade-sequence (canonical) |
| D8 | Progress bar scope | In scope — `max_drawdown.percent` from GET /analytics/metrics |
| D9 | Colour thresholds | Implementation detail — Engineering owns |
| D10 | Fallback logic | No fallback — GET /portfolio always returns both fields |
| D11 | WidgetLibrary | Out of scope — roadmap deferral stands |
| D12 | New Peak! state | In scope — styling is implementation detail |

---

## Observations Register

| ID | Date | Summary | Status |
|----|------|---------|--------|
| OBS-QWB-01 | 2026-02-22 | Prototype code produced before spec lock. Six implicit decisions surfaced (D7–D12). | ✅ Resolved — all decisions closed at meeting 2026-02-24 |

---

## State Transition Log

| # | From | To | Date | Time (UTC) | Declared by | Gate passed |
|---|------|----|------|------------|-------------|-------------|
| 1 | PRE-LOGGED | READINESS_AUDIT | 2026-02-22 | 00:00:00Z | PMO Lead | — |
| 2 | READINESS_AUDIT | AWAITING_MEETING | 2026-02-22 | 23:59:00Z | PMO Lead | Gate R |
| 3 | AWAITING_MEETING | PRE_ALIGNMENT_MEETING | 2026-02-23 | 17:00:00Z | PMO Lead | Gate 0 |
| 4 | PRE_ALIGNMENT_MEETING | SPEC_DELIVERY | 2026-02-24 | 17:00:00Z | PMO Lead | Gate 1 |

---

## Shipping Closure Checklist

*Completed by PMO Lead once Director of Quality final sign-off is confirmed.*

- [ ] Changelog entry added (`docs/product/changelog.md`)
- [ ] Roadmap updated — all six items → ✅ Complete, version bumped, effort estimate updated
- [ ] Scope document status → Superseded
- [ ] Decisions record status → Superseded
- [ ] Head of Engineering notified
- [ ] Lessons learnt review scheduled
- [ ] This phase gate document status → Shipped, date filed
