**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v2.0
**Cycle:** 2026-03-17__release-v2.0
**Last Updated:** 2026-03-17

---

# Release Plan — v2.0 Reporting & Alerts

---

## Readiness

**Release Validation — STEP 1**

| Check | Status | Note |
|-------|--------|------|
| v2.0 on roadmap | ✅ | §3 Delivery Plan — Horizon: Now |
| strategy_rules.md version | ✅ v1.3 | PoG POG-20260304-01 valid for 4.3 |
| 4.3 backend support | ✅ | signal_endpoints.md: top_n + lookback_days documented as query params |
| 4.3 frontend spec | ⚠ Gap | No signals page spec exists — must be authored (ST-01) |
| 4.1b endpoint spec | ⚠ Gap | No tax-year P&L endpoint spec — must be authored (ST-03) |
| 3.5 endpoint spec | ⚠ Gap | No alerts/notification spec — QA gate also pending |
| 3.5 QA gate (gate 3) | ⚠ Pending | QA planning session for notification delivery not yet completed |
| BLG-BE-01 (P1) | ⚠ Open | GET /portfolio missing 4 fields — P1 defect from v1.10 QA |

**Backlog Age Advisory (STEP 1.1):** No spec/documentation debt items have been in the backlog 2+ cycles without story assignment. TEST-GAP-EPIC-02 (1 cycle) and BLG-NEW-13 (1 cycle) are approaching threshold — promoted to sprint stories in STEP 4.

**Readiness verdict:** CONDITIONAL — release may proceed under standard mode. EPIC-03 (3.5 Alerts) is conditional on QA gate clearance before sprint planning seals. All other scope items are proceeding.

---

## Scope

**STEP 2 — Scope Extraction**

### Items in scope

| S2-ID | Epic | Description | Source |
|-------|------|-------------|--------|
| S2-01 | EPIC-03 | 3.5 Alerts & Notifications — email/SMS alerts, in-app feed, notification preferences | Roadmap §3 (conditional — QA gate 3 pending) |
| S2-02 | EPIC-02 | 4.1b Tax-Year P&L Statement — server-side GBP-adjusted tax-year report, realised/unrealised distinction | Roadmap §3 |
| S2-03 | EPIC-01 | 4.3 Signal Exposure Enhancement — top_n + lookback_days as user-facing controls on signals page | Roadmap §3 (PoG POG-20260304-01) |
| S2-04 | EPIC-04 | BLG-BE-01 P1 fix — GET /portfolio missing 4 fields + BLG-BE-02 prospective-heat endpoint (stretch) | Backlog P1/P3 — v2.0 target |
| S2-05 | EPIC-05 | Documentation Pack — production runbook, positions data dictionary, migration governance, spec coverage inventory | Backlog P2 — v2.0 target |
| S2-06 | EPIC-06 | Governance Tooling — roadmap stage document consolidation (BLG-GOV-01), ideas register (BLG-GOV-02) | Backlog P2 — v2.0 governance prep |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| 4.2 Watchlists & Screening | Roadmap Priority 2 — do not pull forward | post-v2.0 |
| Chart Interactivity Enhancements | Roadmap Priority 2 | post-v2.0 |
| TEST-GAP-EPIC-02 | P3, promoted to ST-20 as stretch | EPIC-05 stretch |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*
Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-03-17__release-v2.0

---

## Execution Plan

**STEP 3 — Execution Plan + Decisions Record**

### EPIC Table

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-03 | Base44 Frontend + Head of Specs Team | RISK-03 (no signals page spec) | None — start any time; spec (ST-01) gates implementation (ST-02) |
| EPIC-02 | S2-02 | Head of Specs Team + Head of Engineering + Base44 Frontend | RISK-02 (no tax-year spec) | Spec (ST-03) gates backend (ST-04) and frontend (ST-05); DB migration governance (EPIC-05) should precede any schema change |
| EPIC-03 | S2-01 | Head of Engineering + Base44 Frontend + Director of Quality | RISK-01 (QA gate pending) | **Conditional** — must not enter sprint execution until QA gate 3 cleared; see Pre-sprint Required Decisions |
| EPIC-04 | S2-04 | Head of Engineering | RISK-04 (P1 open defect) | ST-12 (BLG-BE-01) is P1 — must be Sprint 1 item 1. ST-13 (BLG-BE-02) is P3 stretch. |
| EPIC-05 | S2-05 | Infrastructure & Operations Owner + Data Model Owner + Backend Engineering Patterns Owner + Head of Specs Team | None | Independent parallel track; ST-16 (migration governance) should precede EPIC-02 schema work |
| EPIC-06 | S2-06 | Head of Specs Team | RISK-05 (prompt rewrites) | Can run parallel; changes take effect next roadmap cycle |

**EPIC-03 note:** If QA gate 3 (DL-003) is not cleared before sprint planning seals, EPIC-03 is deferred to v2.1. The auto-advance trigger (DL-003) activates when the QA planning session is documented: test types, notification delivery modes, expected test infrastructure. EPIC-01, EPIC-02, EPIC-04, EPIC-05, EPIC-06 proceed regardless.

**EPIC-02 note:** Realised vs Unrealised P&L labelling (BLG-NEW-06, merged into 4.1b) is pre-work scope per roadmap annotation. Must be covered in the tax-year spec (ST-03).

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-03 | QA gate 3 (notification delivery QA session) not cleared — 3.5 Alerts cannot enter sprint execution | High | EPIC-03 conditional: sprint planning seal check required; defer to v2.1 if uncleared | null |
| RISK-02 | EPIC-02 | No tax-year P&L endpoint spec exists — implementation blocked until spec authored | High | ST-03 (spec authoring) is first EPIC-02 story; must pass Head of Specs Team sign-off before ST-04 proceeds | null |
| RISK-03 | EPIC-01 | No frontend signals page spec exists — implementation blocked until spec authored | Medium | ST-01 (spec authoring) gates ST-02; frontend spec is S effort (< 1 day) | null |
| RISK-04 | EPIC-04 | BLG-BE-01 is open P1 defect — GET /portfolio missing 4 fields already in spec | High | ST-12 guaranteed Sprint 1 item 1; not a risk to close — must ship in v2.0 Sprint 1 | null |
| RISK-05 | EPIC-06 | BLG-GOV-01 (roadmap_prompt.md rewrite) is a 2-3 day governance prompt change — high blast radius if defects introduced | Low | Governance prompt changes require Head of Specs Team sign-off and full CLAUDE.md §6 edit checklist; test by running next roadmap cycle after v2.0 ships | null |

---

## Integrity Validation — 3.5 Local Model Integrity

**STEP 3.5 — Local Model Integrity Check**

| Check | Result |
|-------|--------|
| All S2 items map to exactly one EPIC | ✅ S2-01→EPIC-03, S2-02→EPIC-02, S2-03→EPIC-01, S2-04→EPIC-04, S2-05→EPIC-05, S2-06→EPIC-06 |
| All EPICs declare Maps-to S2-IDs | ✅ (see EPIC table above) |
| All RISK-IDs reference a valid EPIC | ✅ RISK-01→EPIC-03, RISK-02→EPIC-02, RISK-03→EPIC-01, RISK-04→EPIC-04, RISK-05→EPIC-06 |
| No scope changes from roadmap | ✅ Roadmap §3 initiatives unchanged; backlog items added per v2.0 target in backlog.md |
| Strategy boundary check (4.3 PoG) | ✅ strategy_rules.md v1.3 unchanged; POG-20260304-01 valid |
| EPIC-03 conditional status documented | ✅ RISK-01 filed; pre-sprint required decision captured in cycle_summary.md |
| Plan executable without EPIC-03? | ✅ EPIC-01/02/04/05/06 are all viable standalone scope |

**Local model integrity: PASS**

---

## Capacity Check

**STEP 4.5 — Capacity Feasibility Sense Check**

**Result: WARN** — total scope mid-estimate exceeds a 2-sprint capacity baseline; phasing required.

| Group | Stories | Low hrs | High hrs | Mid hrs |
|-------|---------|---------|---------|---------|
| EPIC-01 (4.3 Signal Exposure) | ST-01, ST-02 | 3 | 5 | 4 |
| EPIC-02 (4.1b Tax-Year P&L) | ST-03–ST-05 | 9 | 17 | 13 |
| EPIC-04 (Backend Completeness) | ST-12, ST-13 stretch | 6 | 12 | 9 |
| EPIC-05 (Documentation Pack) | ST-14–ST-17, ST-20 stretch | 11 | 21 | 16 |
| EPIC-06 (Governance Tooling) | ST-18–ST-19 | 32 | 48 | 40 |
| **Subtotal (non-conditional, non-governance)** | **EPIC-01+02+04+05** | **29** | **55** | **42** |
| EPIC-03 (3.5 Alerts — conditional) | ST-06–ST-11 | 21 | 38 | 30 |
| **Total with EPIC-03** | | **50** | **93** | **72** |
| **Total with EPIC-03 + EPIC-06** | | **82** | **141** | **112** |

*Capacity baseline (solo dev, evenings): ~40 hrs/sprint × 2 sprints = ~80 hrs.*

**Capacity findings:**
- EPIC-01 + EPIC-02 + EPIC-04 + EPIC-05 (core product): ~42 hrs mid — within 2 sprints ✅
- Adding EPIC-03 (if QA gate clears): ~72 hrs mid — WARN, over Sprint 1 but fits 2 sprints with phasing
- Adding EPIC-06 (governance): ~112 hrs mid — exceeds 2-sprint capacity; must run as parallel track outside sprint execution

### Phasing Recommendation

**Sprint 1 (~38 hrs mid):** EPIC-04 P1 first, EPIC-01, EPIC-05 documentation stories, EPIC-02 spec
- ST-12 (P1 GET /portfolio fix) — Sprint 1 item 1, ~3 hrs
- ST-01, ST-02 (4.3 signal exposure spec + implementation) — ~4 hrs
- ST-14, ST-15, ST-16 (runbook, data dictionary, migration governance) — ~3 hrs
- ST-03 (4.1b tax-year P&L spec) — ~3 hrs
- ST-11 (QA notification planning — DL-003 gate clearance, enables EPIC-03) — ~1 hr
- ST-13 (BLG-BE-02 stretch), ST-20 (CohortAnalysis stretch) — ~6 hrs stretch
- **Sprint 1 total (excl stretch): ~14 hrs mid — light sprint; allows parallel EPIC-06 work**

**Sprint 2 (~40 hrs mid):** EPIC-02 implementation, EPIC-05 spec inventory, EPIC-03 if gate cleared
- ST-04, ST-05 (4.1b backend + frontend) — ~13 hrs
- ST-17 (Spec Coverage Inventory) — ~12 hrs
- ST-06–ST-10 (EPIC-03 alerts — if DL-003 cleared in Sprint 1) — ~25 hrs
- **Sprint 2 total (with EPIC-03): ~50 hrs mid — WARN, may require Sprint 3 if EPIC-03 enters**

**EPIC-06 (ST-18 + ST-19): Parallel track** — run alongside Sprint 1 and Sprint 2 as governance work; does not block product delivery; ~40 hrs mid distributed over the release window.

**Sprint planning recommendation:** If EPIC-03 enters Sprint 2, consider a 3-sprint plan. Sprint planning team should assess against actual available hours before sealing.

---

## Integrity Validation — 5.5 Cross-Stage Integrity

**STEP 5.5 — Cross-Stage Integrity Validation**

| Check | Result |
|-------|--------|
| All S2 IDs reference at least one EPIC in stage4_backlog_slice.md | ✅ S2-01→EPIC-03, S2-02→EPIC-02, S2-03→EPIC-01, S2-04→EPIC-04, S2-05→EPIC-05, S2-06→EPIC-06 |
| All EPICs in stage4_backlog_slice.md declared in release_plan.md EPIC table | ✅ EPIC-01 through EPIC-06 all present |
| All ST items in issue manifest match stories in stage4_backlog_slice.md | ✅ ST-01 through ST-20 (excl. ST-11 gap closed) — 20 stories |
| RISK IDs reference valid EPICs | ✅ RISK-01→EPIC-03, RISK-02→EPIC-02, RISK-03→EPIC-01, RISK-04→EPIC-04, RISK-05→EPIC-06 |
| No scope items exist in stage4 without a corresponding S2 ID | ✅ All EPICs map to S2 items |
| Conditional flag on EPIC-03 stories consistent with RISK-01 | ✅ ST-06–ST-11 all marked conditional in backlog slice |
| Capacity check outcome recorded | ✅ WARN — phasing recommendation provided |
| Decisions record `decisions--2026-03-17__release-v2.0.md` created | ✅ Present |
| Scope document `scope--2026-03-17__release-v2.0-reporting-alerts.md` created | ✅ Present |
| Backlog lock released | ✅ Released after STEP 4 commit |
| Roadmap lock released | ✅ Released after STEP 5 commit |

**Cross-stage integrity: PASS**

---

## Integrity Validation — 5.7 Decision Record Integrity

**STEP 5.7 — Decision Record Integrity Validation**

| Check | Result |
|-------|--------|
| `decisions--2026-03-17__release-v2.0.md` exists | ✅ Present at `docs/product/decisions/` |
| Scope decisions section present | ✅ 4 entries |
| Sequencing decisions section present | ✅ 4 entries |
| Accepted risks section present | ✅ "None" (no escalations raised) |
| Supersession note present (deferred) | ✅ |
| open_escalations empty | ✅ — no escalations raised in this cycle |
| No Open escalations in escalations.md | ✅ — escalations.md not created (no escalations required) |

**Decision record integrity: PASS** (not_applicable path — no ESC entries; decisions record present and complete)
