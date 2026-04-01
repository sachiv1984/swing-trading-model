**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v2.4
**Cycle:** 2026-03-31__release-v2.4
**Last Updated:** 2026-03-31

---

# Release Plan — v2.4 Correctness, Insight & Governance Hardening

---

## Readiness

**Lifecycle guard:** `.claude_current_state.json` status = `Closed` — valid from-state for release planning. ✅

**Backlog Age Advisory (STEP 1.1):**
Spec/documentation debt items in v2.4 scope checked for 2+ cycles without story assignment:
- BLG-SPEC-D15 (portfolios table): Added 2026-03-25 (v2.3 sprint). First cycle without story assignment. No advisory.
- BLG-SPEC-D16 (trade_history table): Added 2026-03-25 (v2.3 sprint). First cycle without story assignment. No advisory.

No spec/documentation debt items found with 2+ cycles without story assignment. ✅

**Provisional-Target Advisory (STEP 1.2):**
- 14 items carry `Provisional-Target: v2.4` — horizon-planned for this release
- 0 items have no Provisional-Target signal (all active backlog items carry explicit targets)

ℹ 14 item(s) carry `Provisional-Target: v2.4`. Scope selection proceeds at STEP 2.

---

## Scope

### Items in Scope

| S2-ID | Epic | Description | Backlog ref(s) |
|-------|------|-------------|----------------|
| S2-01 | EPIC-01 | Backend correctness & alert reliability — ATR conversion fix, alert notification deduplication, R-Multiple stop price | BLG-BE-05, BLG-BE-06, BLG-BE-04 |
| S2-02 | EPIC-02 | Frontend & UX polish — P&L (GBP) column fix, error message mapping layer | BLG-FE-06, BLG-FE-03 |
| S2-03 | EPIC-03 | Spec debt resolution — portfolios and trade_history table schema reconciliation | BLG-SPEC-D15, BLG-SPEC-D16 |
| S2-04 | EPIC-04 | Weekly trading digest — backend endpoint and frontend component | BLG-FEAT-14 |
| S2-05 | EPIC-05 | Operational readiness — Render tier review, API baseline, slippage test scenarios, cycle velocity metric | BLG-OPS-10, BLG-OPS-05, TEST-GAP-EPIC-05-SLIP, BLG-GOV-09 |
| S2-06 | EPIC-06 | Governance engine maintenance — action-now execution_prompt patches, deviation compliance patch, delegation model update, sealing simplification | LL-v2.2-EX-01/02/04, v2.3 Friction Item 1, v2.3 Friction Item 2, BLG-GOV-03 |

### Items Explicitly Deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-GOV-08 — Engine prompt compression (roadmap_prompt + release_planning_prompt) | L effort (~3–5 days); exceeds available sprint bandwidth given backend capacity ceiling and action-now governance items. Requires dedicated standalone sprint. | v2.5 |
| BLG-FEAT-13 — Gated feature rollout capability | Provisional-Target v2.5; not horizon-planned for v2.4 | v2.5 |
| BLG-TECH-05 — Prometheus metrics endpoint | P3; deferred until multi-user scale or explicit operational need | v2.x (conditional) |

### Supersession Note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-03-31__release-v2.4

---

## Execution Plan

### EPIC Table

| EPIC-ID | Maps to | Scope items | Owner | Key risk | Sequencing constraint |
|---------|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | ST-01, ST-02, ST-03 | Head of Engineering + Backend Engineering Patterns Owner | RISK-01 (BE capacity) | Sprint 2; ST-01 first (unblocks integration tests) |
| EPIC-02 | S2-02 | ST-04, ST-05 | Frontend Specs & UX Documentation Owner | RISK-01 (FE bandwidth) | Sprint 2; no EPIC-01 dependency |
| EPIC-03 | S2-03 | ST-06, ST-07 | API Contracts & Documentation Owner | RISK-03 (live DB access) | Sprint 1; foundational — informs EPIC-01 ST-03 |
| EPIC-04 | S2-04 | ST-08, ST-09 | Backend Engineering Patterns Owner + Frontend Specs & UX Documentation Owner | RISK-04 (scope boundary) | Sprint 3; ST-08 before ST-09 |
| EPIC-05 | S2-05 | ST-10, ST-11, ST-12, ST-13 | Infrastructure & Operations Owner + PMO Lead + QA & Testing Owner | RISK-01 (low) | Sprint 1 (ST-10, ST-12, ST-13) + Sprint 2 (ST-11) |
| EPIC-06 | S2-06 | ST-14, ST-15, ST-16, ST-17 | Head of Specs Team | RISK-02 (third recurrence) | Sprint 1; action-now priority — must not defer |

*EPIC-06 note: ST-14/15/16 carry second-recurrence status from v2.3 closure carry-forward. The governance rules require these to be scheduled in Sprint 1 to prevent a third recurrence. The sprint planning engine MUST NOT deprioritise or defer EPIC-06 stories.*

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01, EPIC-02, EPIC-04 | Backend engineering is capacity ceiling for v2.4 (identified in roadmap rebalance 2026-03-31). EPIC-01 (3 BE stories) and EPIC-04 (1 BE story) cannot be in the same sprint without stress. | Medium | Sequence EPIC-01 in Sprint 2 and EPIC-04 in Sprint 3; no overlap of BE-heavy epics | null |
| RISK-02 | EPIC-06 | Three second-recurrence execution_prompt.md patches (LL-v2.2-EX-01/02/04) — if deferred to a third cycle, constitutes a pattern of governance non-compliance. Governance carry-forward CF-1 explicitly flags this risk. | High | Schedule EPIC-06 in Sprint 1 as non-negotiable; sprint planning must not move EPIC-06 stories to Sprint 2+ | null |
| RISK-03 | EPIC-03 | Spec debt reconciliation (BLG-SPEC-D15/16) requires live staging DB inspection (`\d portfolios`, `\d trade_history`). If staging DB is inaccessible, spec-only update with assumption note is acceptable fallback. | Medium | Run DB inspection command early in Sprint 1; document result in story acceptance. If unavailable: proceed with best-evidence spec update and note assumption | null |
| RISK-04 | EPIC-04 | Weekly digest scope boundary: BLG-FEAT-14 Challenger debate in v2.3 rebalance accepted constraint — raw data only, no generated text or interpretive commentary. Any response field containing AI-generated text violates this constraint. | Low | AC explicitly states "no generated text"; DoQ sign-off must verify this AC via code review of response builder | null |

---

## Integrity Validation — 3.5 Local Model Integrity

**Classification:** Conditional Gate

**S2-ID completeness:** All 6 S2 items have IDs (S2-01 through S2-06). ✅

**EPIC-ID completeness:** All 6 EPICs have IDs (EPIC-01 through EPIC-06). ✅

**EPIC→S2 mapping:** Every EPIC declares a `Maps to` field referencing its S2 item. ✅
- EPIC-01 → S2-01 ✅
- EPIC-02 → S2-02 ✅
- EPIC-03 → S2-03 ✅
- EPIC-04 → S2-04 ✅
- EPIC-05 → S2-05 ✅
- EPIC-06 → S2-06 ✅

**RISK-ID completeness:** All 4 risks have IDs (RISK-01 through RISK-04). ✅

**RISK→EPIC mapping:** Every RISK declares a `Relates to` field. ✅

**Backlog references:** All S2 items reference specific BLG-xxx or governance IDs as source. ✅

**Deferred items:** All 3 deferred items have a target release (v2.5 or conditional). ✅

**Model integrity:** PASS — no orphan IDs, no missing maps-to fields, no free-text epics, no missing risk entries.

artifacts.stage3_5_model_integrity = pass ✅
attributes.plan_executable = true ✅

---

## Capacity Check

**Classification:** Conditional Gate

### Effort Estimates

| EPIC-ID | Stories | Effort (mid) | Effort Band Source |
|---------|---------|-------------|-------------------|
| EPIC-01 | ST-01 (XS), ST-02 (M), ST-03 (S) | ~2.25d | Backlog + scored_initiatives.md (BLG-BE-06 M) |
| EPIC-02 | ST-04 (S), ST-05 (S-M) | ~1.5d | Backlog |
| EPIC-03 | ST-06 (XS), ST-07 (S) | ~0.75d | Backlog |
| EPIC-04 | ST-08 (M), ST-09 (M) | ~3.0d | scored_initiatives.md (BLG-FEAT-14 M × 2 stories) |
| EPIC-05 | ST-10 (XS), ST-11 (S), ST-12 (S), ST-13 (S) | ~2.0d | Backlog + scored_initiatives.md (BLG-OPS-10 XS, BLG-GOV-09 S) |
| EPIC-06 | ST-14 (S), ST-15 (S), ST-16 (S), ST-17 (S) | ~2.0d | Backlog (governance patches) |

**Total estimated effort:** ~11.5 days (mid-point) | Range: 9–14 days

**Available capacity:** Solo autonomous developer — 3 sprints × ~5d = ~15d

**Outcome:** PASS — estimated effort (11.5d) is within 3-sprint capacity (15d) with ~24% buffer.

*Note: Backend engineering as capacity ceiling (identified rebalance 2026-03-31): BE workload per this plan = ~3.5d total (ST-01, ST-02, ST-03, ST-08). Distributed across Sprints 1–3. Within ceiling constraints.*

### Phasing Recommendation

**Sprint 1 (~4.75d):**
- EPIC-06: ST-14, ST-15, ST-16, ST-17 (~2.0d) — governance action-now; non-deferrable
- EPIC-03: ST-06, ST-07 (~0.75d) — spec debt; foundational
- EPIC-05 partial: ST-10, ST-12, ST-13 (~1.25d) — quick ops + QA wins
- *Rationale: Governance patches must land in Sprint 1 per carry-forward CF-1. Spec debt items are XS/S and unblock EPIC-01 ST-03.*

**Sprint 2 (~4.75d):**
- EPIC-01: ST-01, ST-02, ST-03 (~2.25d) — backend correctness
- EPIC-02: ST-04, ST-05 (~1.5d) — frontend fixes
- EPIC-05 partial: ST-11 (~0.75d) — API baseline (follows spec debt resolution)
- *Rationale: Backend-heavy sprint with parallel FE work. Backend ceiling managed by separating BE from EPIC-04.*

**Sprint 3 (~3.0d):**
- EPIC-04: ST-08, ST-09 (~3.0d) — weekly digest
- Any spillover from Sprint 2
- *Rationale: New feature sprint isolated from correctness work; lowest risk of blocking prior stories.*

artifacts.stage4_5_capacity_check = pass ✅
attributes.capacity_feasible = pass ✅

---

## Integrity Validation — 5.5 Cross-Stage Integrity

**Classification:** Hard Gate

**S2-ID coverage in EPIC table:** All 6 S2 items (S2-01 through S2-06) are referenced in the EPIC table. ✅

**EPIC-ID coverage in backlog slice:** All 6 EPIC-IDs used in `release_plan.md` also appear in `stage4_backlog_slice.md`. ✅

**ST-IDs consistent:** ST-01 through ST-17 referenced in `stage4_backlog_slice.md` match the story list above. ✅

**RISK-IDs in risk register:** RISK-01 through RISK-04 — all present in register, all with `Relates to`. ✅

**Backlog marker present:** `<!-- release-plan-marker: RP:v2.4:2026-03-31__release-v2.4 -->` confirmed in `claude/backlog/backlog.md §12 Active Release Slice`. ✅

**Deferred items not in backlog slice:** BLG-GOV-08, BLG-FEAT-13, BLG-TECH-05 — none appear in `stage4_backlog_slice.md`. ✅

**Cross-stage integrity:** PASS

artifacts.stage5_5_cross_stage_integrity = pass ✅
attributes.cross_stage_integrity = pass ✅

---

## Integrity Validation — 5.7 Decision Record Integrity

**Classification:** Hard Gate (triggered only if Accepted Risk escalations exist)

No Accepted Risk (AR) escalations were raised during this cycle. No SRB escalations raised.

*Trigger condition not met — no decision records required.*

artifacts.stage5_7_decision_record_integrity = not_applicable ✅
attributes.decisions_validated = not_applicable ✅
