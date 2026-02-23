# Phase Gate Document — Quick Wins Bundle

**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.3
**Created:** 2026-02-22
**Last Updated:** 2026-02-27
**Filed:** — (immutable on closure)

**Charter authority:** `docs/team_skills/pmo/processess/pre_alignment_run.md` v2.0

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.3 | 2026-02-27 | Gate 2 closed. All 11 spec actions confirmed complete with specific content evidence. State transitioned SPEC_DELIVERY → QA_REVIEW. QA & Testing Owner notified with full spec list. |
| 1.2 | 2026-02-24 | Gate 1 closed. Decisions record committed. 11 spec delivery actions opened across 4 owners. |
| 1.1 | 2026-02-23 | Gate 0 closed. Pre-alignment meeting held. |
| 1.0 | 2026-02-22 | Document created. Gate R passed. |

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
Current phase:    QA_REVIEW
Gate passed:      Gate 2 — 2026-02-27
Next gate:        Gate 3 — QA sign-off confirmed
Who acts next:    QA & Testing Owner
What they do:     Review all committed canonical specs and confirm acceptance
                  criteria are fully derivable. Produce written verdict.
Deadline:         2026-02-27T17:00:00Z
Blockers:         None
```

---

## Phase History

| Phase | Gate condition | Status | Date | Notes |
|-------|---------------|--------|------|-------|
| Phase 0 — Readiness Audit | Audit complete, Go/No-Go issued | ✅ Complete | 2026-02-22 | Gate R passed. All items confirmed. |
| Phase 1 — Pre-Alignment Meeting | All decisions closed, decisions record committed | ✅ Complete | 2026-02-24 | 13 decisions closed. Zero deferrals. Record committed. |
| Phase 2 — Parallel Spec Delivery | All spec actions complete and committed | ✅ Complete | 2026-02-27 | All 11 actions confirmed complete. Gate 2 passed. |
| Phase 3 — QA Review Gate | QA sign-off confirmed | 🟡 In progress | 2026-02-27 | QA & Testing Owner notified. Specs list delivered. |
| Phase 4 — Scope Document | Scope document committed, implementation declared open | ⬜ Not started | — | |
| Implementation | Engineering builds against locked specs | ⬜ Not started | — | |
| Phase 5 — Verification | All criteria pass, Director of Quality final sign-off | ⬜ Not started | — | |
| Shipping Closure | Changelog, roadmap, supersession actions complete | ⬜ Not started | — | |

Status key: ⬜ Not started | 🟡 In progress | ✅ Complete | 🔴 Blocked

---

## Gate R — ✅ COMPLETE (2026-02-22)

All 6 gate items passed. Full evidence on record.

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
  Evidence:             Spec Delivery Action Table — 11 actions, owners, deadlines,
                        dependencies all assigned. Critical path identified.
  Owner confirmation:   Yes — PMO Lead, 2026-02-24
  PMO validation:       Pass — PMO Lead, 2026-02-24

Gate 1.4 — Critical path communicated
  Evidence:             All owners notified of first action and deadline 2026-02-24
  Owner confirmation:   Yes — PMO Lead, 2026-02-24
  PMO validation:       Pass — PMO Lead, 2026-02-24
```

---

## Gate 2 — ✅ COMPLETE (2026-02-27)

```
Gate 2.1 — All spec actions confirmed complete
  Evidence:
    A-S01  metrics_definitions.md → v1.5.8
           Added: Current Drawdown section (formula, data requirements, API data sources,
           failure behaviour, validation note, implementation note). No other sections modified.
           Owner confirmation: Yes — Metrics Definitions owner, 2026-02-25

    A-S02  portfolio_endpoints.md → v1.8.2 + openapi.yaml (same PR)
           Added: current_drawdown_percent and peak_portfolio_value to GET /portfolio
           example JSON and field notes table. openapi.yaml PortfolioOverview schema updated
           in same PR.
           Owner confirmation: Yes — API Contracts owner, 2026-02-25

    A-S03  position_endpoints.md → v1.8.3 + openapi.yaml (same PR)
           Added: grace_days_remaining to GET /positions example JSON and field notes table
           (formula, null rule, display format, always-present rule). openapi.yaml
           PositionDetail and PositionSummary schemas updated in same PR.
           Owner confirmation: Yes — API Contracts owner, 2026-02-25

    A-S04  trade_endpoints.md → v1.8.4 + openapi.yaml (same PR)
           Added: GET /trades/export/csv section (purpose, response headers, 14-column
           table in canonical order, serialisation rules, empty-history behaviour, error
           shape). openapi.yaml GET /trades/export/csv path and TradeExportCsv component
           added in same PR.
           Owner confirmation: Yes — API Contracts owner, 2026-02-25

    A-S05  roadmap.md
           Updated: QWB effort estimate from ~6–8 hours to ~8–10.5 hours. Itemised
           breakdown updated to include spec authoring overhead.
           Owner confirmation: Yes — Product Owner, 2026-02-25

    A-S06  dashboard.md → v1.1
           Added: Current Drawdown Widget section (stats row placement, data sources,
           3 display states, progress bar rules, no-fallback rule per D10, colour
           thresholds as Engineering implementation detail).
           Owner confirmation: Yes — Frontend Spec owner, 2026-02-26

    A-S07  trade_history.md → v1.1
           Added: R-Multiple column section (formula, trades_for_charts source,
           frontend-only calculation, display format, null handling, sort behaviour).
           Owner confirmation: Yes — Frontend Spec owner, 2026-02-25

    A-S08  positions.md → v1.2
           Added: grace_days_remaining column section (display format "Day X of 10",
           null = dash or hidden).
           Owner confirmation: Yes — Frontend Spec owner, 2026-02-26

    A-S09  analytics.md → v1.2
           Added: Component 11 Best/Worst Trades (R-multiple ranking, top 3/bottom 3,
           trades_for_charts source, card contents, empty/partial states).
           Added: Component 12 Win Rate by Month chart (monthly_data source, fixed
           0–100 Y-axis, 50% reference line, colour coding, tooltip with trade_count,
           empty state).
           Owner confirmation: Yes — Frontend Spec owner, 2026-02-25

    A-S10  trade_history.md → v1.1 (additive to A-S07)
           Added: CSV Export Button section (placement, GET /trades/export/csv trigger,
           browser download, server-side only per D5).
           Owner confirmation: Yes — Frontend Spec owner, 2026-02-26

    A-S11  api_dependencies.md → v1.2
           Added: Dashboard → GET /portfolio new fields; Dashboard → GET /analytics/metrics
           new fields; Positions table → GET /positions new field; Trade History →
           GET /trades/export/csv new endpoint.
           Owner confirmation: Yes — Frontend Spec owner, 2026-02-26

  PMO validation:       Pass — PMO Lead, 2026-02-27
                        All 11 actions show owner confirmation with specific content
                        evidence per GI-3. No action confirmed as "done" without
                        specific changed text.

Gate 2.2 — openapi.yaml committed in same PR as each API contract change
  Evidence:             A-S02: portfolio_endpoints.md + openapi.yaml — same PR confirmed
                          by API Contracts owner, 2026-02-25
                        A-S03: position_endpoints.md + openapi.yaml — same PR confirmed
                          by API Contracts owner, 2026-02-25
                        A-S04: trade_endpoints.md + openapi.yaml — same PR confirmed
                          by API Contracts owner, 2026-02-25
  Owner confirmation:   Yes — API Contracts owner, 2026-02-25 (all three PRs)
  PMO validation:       Pass — PMO Lead, 2026-02-27

Gate 2.3 — Patch verification confirmed for all patched files
  Evidence:             Each of the 11 action confirmations above includes the specific
                        content change (section added, field added, formula confirmed,
                        rule documented). No owner confirmed with "it's done" alone.
                        Patch verification satisfied for all 11 actions.
  Owner confirmation:   Yes — all four owners on record (dates above)
  PMO validation:       Pass — PMO Lead, 2026-02-27

Gate 2.4 — No open decisions
  Evidence:             Confirmed by all four spec owners: no new decisions or questions
                        arose during spec delivery. All 11 actions executed against the
                        locked decisions record (D1–D12 + D2a). Zero deviations.
  Owner confirmation:   Yes — Metrics Definitions owner, 2026-02-25
                        Yes — API Contracts owner, 2026-02-25
                        Yes — Product Owner, 2026-02-25
                        Yes — Frontend Spec owner, 2026-02-26
  PMO validation:       Pass — PMO Lead, 2026-02-27
```

**✅ ALL GATE 2 ITEMS PASS — State transitions SPEC_DELIVERY → QA_REVIEW**

---

## Gate 3 — 🟡 IN PROGRESS

```
Gate 3.1 — QA verdict recorded as Pass
  Evidence:             [PENDING — awaiting written verdict from QA & Testing Owner]
  Owner confirmation:   [PENDING]
  PMO validation:       [PENDING]

Gate 3.2 — All Conditional Pass issues resolved (if applicable)
  Evidence:             [PENDING — n/a if clean pass; issues to be logged here if raised]
  Owner confirmation:   [PENDING]
  PMO validation:       [PENDING]

Gate 3.3 — No outstanding spec questions
  Evidence:             [PENDING]
  Owner confirmation:   [PENDING]
  PMO validation:       [PENDING]
```

---

## Spec Delivery Action Table — ✅ ALL COMPLETE

### Parallel stream

| # | Action | Owner | Deadline | Status | Evidence |
|---|--------|-------|----------|--------|----------|
| A-S01 | Add Current Drawdown section to `metrics_definitions.md` → v1.5.8 | Metrics Definitions owner | 2026-02-25T17:00:00Z | ✅ Complete | Confirmed by owner 2026-02-25 — section content detailed above |
| A-S02 | Add drawdown fields to `portfolio_endpoints.md` v1.8.2 + `openapi.yaml` | API Contracts owner | 2026-02-25T17:00:00Z | ✅ Complete | Confirmed by owner 2026-02-25 — same-PR confirmed |
| A-S03 | Add `grace_days_remaining` to `position_endpoints.md` v1.8.3 + `openapi.yaml` | API Contracts owner | 2026-02-25T17:00:00Z | ✅ Complete | Confirmed by owner 2026-02-25 — same-PR confirmed |
| A-S04 | Add `GET /trades/export/csv` to `trade_endpoints.md` v1.8.4 + `openapi.yaml` | API Contracts owner | 2026-02-25T17:00:00Z | ✅ Complete | Confirmed by owner 2026-02-25 — same-PR confirmed |
| A-S05 | Update `roadmap.md` effort estimate to ~8–10.5 hours | Product Owner | 2026-02-25T17:00:00Z | ✅ Complete | Confirmed by owner 2026-02-25 |
| A-S07 | Update `trade_history.md` v1.1 — R-multiple column | Frontend Spec owner | 2026-02-26T17:00:00Z | ✅ Complete | Confirmed by owner 2026-02-25 |
| A-S09 | Update `analytics.md` v1.2 — Best/Worst Trades + Win Rate by Month | Frontend Spec owner | 2026-02-26T17:00:00Z | ✅ Complete | Confirmed by owner 2026-02-25 |

### Blocked stream (unblocked and completed)

| # | Action | Owner | Deadline | Status | Evidence |
|---|--------|-------|----------|--------|----------|
| A-S06 | Update `dashboard.md` v1.1 — Current Drawdown Widget | Frontend Spec owner | 2026-02-26T17:00:00Z | ✅ Complete | Confirmed by owner 2026-02-26 |
| A-S08 | Update `positions.md` v1.2 — grace_days_remaining column | Frontend Spec owner | 2026-02-26T17:00:00Z | ✅ Complete | Confirmed by owner 2026-02-26 |
| A-S10 | Update `trade_history.md` v1.1 — CSV export button | Frontend Spec owner | 2026-02-26T17:00:00Z | ✅ Complete | Confirmed by owner 2026-02-26 |
| A-S11 | Update `api_dependencies.md` v1.2 | Frontend Spec owner | 2026-02-26T17:00:00Z | ✅ Complete | Confirmed by owner 2026-02-26 |

---

## Locked Canonical Specs (for QA Review)

The following specs are committed and locked. QA & Testing Owner reviews these for Gate 3.

| Spec | Version | Changed in this bundle |
|------|---------|----------------------|
| `docs/specs/metrics_definitions.md` | v1.5.8 | ✅ New section: Current Drawdown |
| `docs/specs/api_contracts/portfolio_endpoints.md` | v1.8.2 | ✅ New fields: current_drawdown_percent, peak_portfolio_value |
| `docs/specs/api_contracts/position_endpoints.md` | v1.8.3 | ✅ New field: grace_days_remaining |
| `docs/specs/api_contracts/trade_endpoints.md` | v1.8.4 | ✅ New endpoint: GET /trades/export/csv |
| `docs/specs/api_contracts/analytics_endpoints.md` | v1.8.1 | No change — existing fields consumed |
| `docs/specs/data_model.md` | v1.7 | No change — no migration required |
| `docs/specs/frontend/pages/dashboard.md` | v1.1 | ✅ New widget: Current Drawdown |
| `docs/specs/frontend/pages/trade_history.md` | v1.1 | ✅ New column: R-multiple; new button: CSV export |
| `docs/specs/frontend/pages/analytics.md` | v1.2 | ✅ New components: Best/Worst Trades, Win Rate by Month |
| `docs/specs/frontend/pages/positions.md` | v1.2 | ✅ New column: grace_days_remaining |
| `docs/specs/api_dependencies.md` | v1.2 | ✅ New dependencies added |
| `docs/reference/openapi.yaml` | current | ✅ Updated with A-S02, A-S03, A-S04 |

---

## Stakeholder Next Steps

**As of 2026-02-27:**

| Role | Action | By when |
|------|--------|---------|
| **QA & Testing Owner** | QA review — read all committed specs above, confirm acceptance criteria are fully derivable from them, produce written verdict (Pass / Conditional Pass / Fail) with any issues identified | 2026-02-27T17:00:00Z |
| **All spec owners** | Standby — QA review may raise issues requiring spec fixes. No other action until verdict received. | — |
| **Product Owner** | No action until Gate 3 passes | — |
| **Head of Engineering** | No action until Gate 4 passes | — |

---

## Open Actions

| # | Action | Owner | Status | Due |
|---|--------|-------|--------|-----|
| A-QA-01 | QA review of all locked specs — produce written verdict | QA & Testing Owner | 🟡 In progress | 2026-02-27T17:00:00Z |

---

## Open Blockers

**No open blockers.**

---

## Decisions Record Reference

`docs/product/decisions/QWB-quick-wins-bundle.md` — committed 2026-02-24

| # | Decision | Summary |
|---|----------|---------|
| D1 | BLG-FEAT-01 formula + endpoint | `(peak−current)/peak×100` via GET /portfolio (2 new fields) |
| D2 | BLG-FEAT-02 R-multiple | Frontend-only, `metrics_definitions.md` v1.5.8 canonical |
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
| OBS-QWB-02 | 2026-02-27 | Test scenario document authored during SPEC_DELIVERY state, before QA review gate. Sequencing premature per testing_guide.md. Content is spec-derived and complete. QA & Testing Owner to re-confirm document after Gate 3 passes. Process gap identified: Gate 4 has no checklist item requiring test scenario document. A-PROC-01 raised. | 🟡 Open — re-confirmation pending Gate 3 |

---

## Process Improvement Actions

| # | Action | Owner | Status |
|---|--------|-------|--------|
| A-PROC-01 | Add Gate 4.6 checklist item to `pre_alignment_run.md`: "Test scenario document committed at `docs/testing/{id}-{slug}-test-scenarios.md`. Evidence: file path + QA & Testing Owner confirmation." Prevents recurrence of A-TS-01 sequencing issue. | Head of Specs Team | 🟡 Open |

---

## State Transition Log

| # | From | To | Date | Time (UTC) | Declared by | Gate passed |
|---|------|----|------|------------|-------------|-------------|
| 1 | PRE-LOGGED | READINESS_AUDIT | 2026-02-22 | 00:00:00Z | PMO Lead | — |
| 2 | READINESS_AUDIT | AWAITING_MEETING | 2026-02-22 | 23:59:00Z | PMO Lead | Gate R |
| 3 | AWAITING_MEETING | PRE_ALIGNMENT_MEETING | 2026-02-23 | 17:00:00Z | PMO Lead | Gate 0 |
| 4 | PRE_ALIGNMENT_MEETING | SPEC_DELIVERY | 2026-02-24 | 17:00:00Z | PMO Lead | Gate 1 |
| 5 | SPEC_DELIVERY | QA_REVIEW | 2026-02-27 | 09:30:00Z | PMO Lead | Gate 2 |

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
