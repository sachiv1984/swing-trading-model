**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v2.1
**Cycle:** 2026-03-18__release-v2.1
**Last Updated:** 2026-03-18

---

# Release Plan — v2.1 Alerts, Watchlists & Enhancements

---

## Readiness

**Release Validation — STEP 1**

| Check | Status | Note |
|-------|--------|------|
| v2.1 on roadmap | ✅ | §4 Priority 2 + §8 Release Summary |
| Prior cycle closed | ✅ | 2026-03-17__release-v2.0 — Closed, post_ship_complete=true |
| BLG-TECH-08 (ADR) status | ⚠ Open | Required before EPIC-02 stories can be specced or implemented; included as EPIC-01 ST-01 |
| 4.2 Watchlists — data model pre-work | ⚠ Gap | data_model.md must be updated before implementation begins (part of EPIC-03 scope) |
| CHART-IX — frontend-only scope confirmed | ✅ | No new backend indicators; UX improvement only |
| BLG-FR-01/02 — reports endpoint exists | ✅ | GET /reports/tax-year exists; format param extension only |
| BLG-FEAT-03 — fill price capture pre-work | ⚠ Gate | data_model.md must define Fill Price field before implementation; gated within story |

**Backlog Age Advisory (STEP 1.1):** No spec/documentation debt items have been in the backlog 2+ cycles without story assignment. All v2.1-targeted items were added in 2026-03-17__release-v2.0 (1 cycle only). No advisory.

**Readiness verdict:** CONDITIONAL — release may proceed under standard mode. EPIC-02 (Alerts) is gated on EPIC-01 (BLG-TECH-08 ADR complete + sprint planning seal check). All other scope items proceed independently.

---

## Scope

**STEP 2 — Scope Extraction**

### Items in scope

| S2-ID | Epic | Description | Source |
|-------|------|-------------|--------|
| S2-01 | EPIC-01 | Notification delivery ADR — BLG-TECH-08: sync vs async architecture decision | Backlog P2 — v2.1 prerequisite |
| S2-02 | EPIC-02 | 3.5 Alerts & Notifications — full implementation: alert rules engine, email delivery, notification preferences, in-app feed | Roadmap §3 (Now horizon, deferred from v2.0); gated on S2-01 complete |
| S2-03 | EPIC-03 | 4.2 Watchlists & Screening — monitor tickers, entry signals, quick-add to position entry | Roadmap §4 Priority 2 |
| S2-04 | EPIC-04 | Chart Interactivity Enhancements (CHART-IX) — hover tooltips, zoom, drill-down on 3 analytics charts | Roadmap §4 Priority 2 |
| S2-05 | EPIC-05 | Financial Reporting Exports + Feature Enhancements — PDF export, CSV export, slippage tracking, PR preview environments | Backlog P2 — v2.1 target (BLG-FR-01/02, BLG-FEAT-03, BLG-OPS-03) |
| S2-06 | EPIC-06 | Spec Debt & QA Coverage — bulk lifecycle headers, spec maintenance, test scenario documents, process compliance check | Backlog P2/P3 — v2.1 target |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-TECH-05 Prometheus metrics | P3, below v2.1 priority threshold given 3-sprint scope | v2.2 (or multi-user need) |
| BLG-GOV-03/04/05/06 | v2.2 governance process improvements — not product scope | v2.2 |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*
Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-03-18__release-v2.1

---

## Execution Plan

**STEP 3 — Execution Plan + Decisions Record**

### EPIC Table

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Head of Engineering + Backend Engineering Patterns Owner | RISK-01 (ADR decision affects entire EPIC-02 spec) | None — must start early; completion unlocks EPIC-02 |
| EPIC-02 | S2-02 | Head of Engineering + Base44 Frontend + Director of Quality | RISK-02 (EPIC-01 gate; high combined effort) | **Conditional** — EPIC-01 (ST-01) must be Complete and Sprint Planning Engine verified before any EPIC-02 story seals |
| EPIC-03 | S2-03 | Head of Engineering + Base44 Frontend + Data Model & Domain Schema Owner | RISK-03 (data model pre-work gate) | Spec + data model (ST-08) must gate implementation (ST-09/10); EPIC-02 dependency: none |
| EPIC-04 | S2-04 | Base44 Frontend | RISK-04 (scope boundary — no new indicators) | Independent; can run parallel to any EPIC |
| EPIC-05 | S2-05 | Head of Engineering + Base44 Frontend + Financial Reporting & Records Owner + Infrastructure & Operations Owner | RISK-05 (BLG-FEAT-03 data model gate) | BLG-FR-01 (ST-12) backend before frontend component; BLG-FEAT-03 (ST-14) data model spec must precede implementation |
| EPIC-06 | S2-06 | Head of Specs Team + QA & Testing Owner + PMO Lead | None | Independent; can run as parallel track alongside Sprint 1/2 |

**EPIC-02 note:** The 6 Alerts stories (ST-02–ST-07) are the same scope as v2.0 ST-06–ST-11 (deferred). Sprint Planning Engine STEP -1 must confirm BLG-TECH-08 (ST-01) is Complete with Head of Engineering sign-off before any EPIC-02 story can be sealed in the sprint backlog.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | BLG-TECH-08 ADR not yet authored — EPIC-02 cannot be specced without the decision on sync vs async notification delivery | High | EPIC-01 ST-01 is first story; EPIC-02 gates on its completion; must resolve before sprint planning seals EPIC-02 items | null |
| RISK-02 | EPIC-02 | EPIC-02 has 6 deferred stories with ~47 hrs mid effort — largest single EPIC in this release; combined with EPIC-03/05 pushes release to 3 sprints | High | Phasing recommendation in Capacity Check (STEP 4.5); sprint planning team to adopt phase plan | null |
| RISK-03 | EPIC-03 | 4.2 Watchlists requires new data model tables — implementation blocked until data_model.md spec is authored | Medium | ST-08 (spec + data model) is first EPIC-03 story and gates ST-09/10 | null |
| RISK-04 | EPIC-04 | Chart Interactivity must not introduce client-side re-derivation of values — all values must remain consistent with canonical backend response | Medium | Scope constraint documented in roadmap entry; enforced at code review and DoQ sign-off | null |
| RISK-05 | EPIC-05 | BLG-FEAT-03 Slippage Tracking requires new Fill Price field in data model — data model spec must be authored before any implementation | Medium | ST-14 scoped as spec + implementation; data_model.md spec gate enforced within story AC | null |

---

## Integrity Validation — 3.5 Local Model Integrity

**STEP 3.5 — Local Model Integrity Check**

| Check | Result |
|-------|--------|
| All S2 items map to exactly one EPIC | ✅ S2-01→EPIC-01, S2-02→EPIC-02, S2-03→EPIC-03, S2-04→EPIC-04, S2-05→EPIC-05, S2-06→EPIC-06 |
| All EPICs declare Maps-to S2-IDs | ✅ (see EPIC table above) |
| All RISK-IDs reference a valid EPIC | ✅ RISK-01→EPIC-01, RISK-02→EPIC-02, RISK-03→EPIC-03, RISK-04→EPIC-04, RISK-05→EPIC-05 |
| No scope changes from roadmap | ✅ Roadmap §4 initiatives unchanged; backlog items added per v2.1 target in backlog.md |
| Strategy boundary check (CHART-IX) | ✅ No new indicators — confirmed strategy_rules.md §13 boundary maintained |
| EPIC-02 conditional status documented | ✅ RISK-01/02 filed; pre-sprint required decision captured in cycle_summary.md |
| Plan executable without EPIC-02? | ✅ EPIC-01/03/04/05/06 are all viable standalone scope |

**Local model integrity: PASS**

---

## Capacity Check

**STEP 4.5 — Capacity Feasibility Sense Check**

**Result: WARN** — total scope mid-estimate (~129 hrs) requires 3 sprints at standard capacity.

| EPIC | Stories | Low hrs | High hrs | Mid hrs |
|------|---------|---------|---------|---------|
| EPIC-01 (Notification ADR) | ST-01 | 3 | 6 | 4 |
| EPIC-02 (Alerts — gated) | ST-02–ST-07 | 34 | 60 | 47 |
| EPIC-03 (Watchlists) | ST-08–ST-10 | 20 | 36 | 28 |
| EPIC-04 (Chart Interactivity) | ST-11 | 5 | 10 | 7 |
| EPIC-05 (Financial + Enhancements) | ST-12–ST-15 | 18 | 32 | 25 |
| EPIC-06 (Spec Debt + QA) | ST-16–ST-19 | 13 | 23 | 18 |
| **Total** | **19 stories** | **93** | **167** | **129** |

*Capacity baseline (solo dev, evenings): ~40 hrs/sprint.*

### Phasing Recommendation

**Sprint 1 (~38 hrs mid):** EPIC-01 (ADR) + EPIC-04 (Chart) + EPIC-06 (Spec Debt + QA) + EPIC-05 partial (FR exports)
- ST-01 (BLG-TECH-08 ADR): ~4 hrs — must be item 1; completion unlocks EPIC-02
- ST-11 (Chart Interactivity): ~7 hrs
- ST-16 (Bulk spec headers): ~8 hrs
- ST-17 (Spec maintenance batch): ~4 hrs
- ST-18 (Test scenario docs): ~4 hrs
- ST-19 (Process compliance check): ~2 hrs
- ST-12 (PDF Export): ~10 hrs — Sprint 1 backend work (within capacity)
- *Sprint 1 total: ~39 hrs mid — at capacity*

**Sprint 2 (~42 hrs mid):** EPIC-02 (Alerts Phase 1) + EPIC-05 remainder
- ST-02 (Alerts spec): ~8 hrs
- ST-03 (Alert rules engine): ~14 hrs
- ST-13 (CSV Export): ~4 hrs — small, complete EPIC-05
- ST-15 (PR preview environments): ~3 hrs
- ST-14 (Slippage Tracking): ~8 hrs
- *Sprint 2 total: ~37 hrs mid — within capacity. ST-04/05 begin if bandwidth allows (stretch)*

**Sprint 3 (~46 hrs mid):** EPIC-02 (Alerts Phase 2) + EPIC-03 (Watchlists)
- ST-04 (Notification delivery email): ~10 hrs
- ST-05 (Notification preferences frontend): ~6 hrs
- ST-06 (In-app notification feed): ~6 hrs
- ST-07 (QA notification scenarios): ~3 hrs
- ST-08 (Watchlist spec + data model): ~6 hrs
- ST-09 (Watchlist backend): ~12 hrs
- *Sprint 3 core: ~43 hrs mid — WARN; ST-10 (Watchlist frontend, ~10 hrs) as stretch or Sprint 4*

**Ordering rationale:** EPIC-01 first (unlocks EPIC-02). EPIC-04 + EPIC-06 early (quick wins, low risk). EPIC-02 spans Sprint 2–3 (high priority but large). EPIC-03 in Sprint 3 (Next horizon, lower than Now/Alerts). EPIC-05 distributed across Sprint 1–2.

**Sprint planning recommendation:** This is a 3-sprint release (minimum). Sprint planning team must confirm actual available hours against these estimates. EPIC-03 ST-10 (watchlist frontend, ~10 hrs) may slip to Sprint 4 if Sprint 3 runs long.

---

## Integrity Validation — 5.5 Cross-Stage Integrity

**STEP 5.5 — Cross-Stage Integrity Validation**

| Check | Result |
|-------|--------|
| All S2 IDs reference at least one EPIC in stage4_backlog_slice.md | ✅ S2-01→EPIC-01, S2-02→EPIC-02, S2-03→EPIC-03, S2-04→EPIC-04, S2-05→EPIC-05, S2-06→EPIC-06 |
| All EPICs in stage4_backlog_slice.md declared in release_plan.md EPIC table | ✅ EPIC-01 through EPIC-06 all present |
| All ST items in issue manifest match stories in stage4_backlog_slice.md | ✅ ST-01 through ST-19 — 19 stories |
| RISK-IDs reference valid EPICs | ✅ RISK-01→EPIC-01, RISK-02→EPIC-02, RISK-03→EPIC-03, RISK-04→EPIC-04, RISK-05→EPIC-05 |
| No scope items exist in stage4 without a corresponding S2 ID | ✅ All EPICs map to S2 items |
| Conditional flag on EPIC-02 stories consistent with RISK-01/02 | ✅ ST-02–ST-07 all marked conditional in backlog slice |
| Capacity check outcome recorded | ✅ WARN — 3-sprint phasing recommendation provided |
| Decisions record `decisions--2026-03-18__release-v2.1.md` created | ✅ Present |
| Scope document `scope--2026-03-18__release-v2.1-alerts-watchlists.md` created | ✅ Present |
| Backlog lock released | ✅ Released after STEP 4 commit |
| Roadmap lock released | ✅ Released after STEP 5 commit |

**Cross-stage integrity: PASS**

---

## Integrity Validation — 5.7 Decision Record Integrity

**STEP 5.7 — Decision Record Integrity Validation**

| Check | Result |
|-------|--------|
| `decisions--2026-03-18__release-v2.1.md` exists | ✅ Present at `docs/product/decisions/` |
| Scope decisions section present | ✅ 4 entries |
| Sequencing decisions section present | ✅ 3 entries |
| Accepted risks section present | ✅ "None" (no escalations raised) |
| Supersession note present (deferred) | ✅ |
| open_escalations empty | ✅ — no escalations raised in this cycle |
| No Open escalations in escalations.md | ✅ — escalations.md not created (no escalations required) |

**Decision record integrity: PASS** (not_applicable path — no ESC entries; decisions record present and complete)
