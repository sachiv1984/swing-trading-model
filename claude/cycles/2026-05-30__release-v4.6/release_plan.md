**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v4.6
**Cycle:** 2026-05-30__release-v4.6
**Published:** 2026-05-30

---

# Release Plan — v4.6 SI-02 Behavioural Drift Detection & Arc 5 Completion

---

## Readiness

**Prior cycle:** 2026-05-30__release-v4.5 — Closed (Verified, Closed_with_actions, completed_cycle_count=31)
**Post-ship complete:** true | **Next cycle unblocked:** true
**Audit status:** AUD-2026-05-30 (2026-05-30) — Overall 74; no unresolved Tier 1 items; AUDIT DUE at cycle 33
**Outstanding actions from v4.5:** 2 (OA-01: System_status_report.md stale — PMO Lead; OA-02: roadmap_prompt.md advisory — Head of Specs Team)

**Readiness advisories:**
- ⚠ Advisory: v4.6 not present as explicit roadmap section. Annotation approach applied (established pattern — v4.4 and v4.5 both proceeded via annotation; per v4.5 lessons_learnt carry-forward "annotation is acceptable"). v4.6 will be added to roadmap at STEP 5.
- ℹ OA-01 (System_status_report.md v4.4 stale status) and OA-02 (roadmap_prompt.md advisory) both resolved in EPIC-04.
- ℹ Carry-forward item from v4.5: OA-02 roadmap_prompt.md next_release advisory — addressed in EPIC-04 ST-22.
- ℹ 1 item with `Provisional-Target: v4.1` still open (BLG-OPS-28) — included in scope assessment; deferred.
- ℹ Design dependency scan: 0 items flagged.
- ℹ scored_initiatives.md: no matching SI-02 or governance items — using STEP 4 inline estimates.
- ℹ Backlog age advisory: BLG-GOV-33 (PT-04 closed trade count audit, Provisional-Target v4.0 release planning) and BLG-GOV-34 (Arc 4 trajectory, Provisional-Target v4.0) have each been in the backlog for 6+ cycles without story assignment. Both promoted to firm scope in EPIC-04.
- ℹ SI-02 pre-planning complete: §13 PASS (9 binding conditions, v4.5 EPIC-03 ST-06), drift score metric definition (si02_drift_score.md v1.0), data schema pre-definition (si02_data_schema.md v1.0), all four pre-design documents shipped (v4.4: BLG-BE-17/18/20/23, BLG-FE-52/53, BLG-QA-31). SI-02 is ready for implementation.
- ℹ Data density gate: SI-02 sprint planning must verify ≥20 closed trades with linked trade_plans. BLG-GOV-33 (ST-16) performs this check in Sprint 1; if gate not met, EPIC-02 is deferred and cycle closes with Sprint 1 only.
- ⚠ Advisory: BLG-GOV-67 (SI-05 Phase 1) gate clears 2026-06-21 (SI-01 + SI-03 live ≥30 days). Included as conditional EPIC-03 item.

---

## Scope

### S2-01 — SI-02 Behavioural Drift Detection: Backend Implementation
**Source:** Arc 5 roadmap; si02_drift_score.md v1.0; si02_data_schema.md v1.0; §13 PASS (decisions--2026-05-30__release-v4.5--SI-02-section13-review.md)
**Items:** SI-02 DS-07 migration, drift detection service (4 metrics), GET /analytics/behavioural-drift endpoint, POST /trade-plans capture updates, unit tests
**Owner:** Head of Backend Engineering; Data Model & Domain Schema Owner
**Rationale:** All SI-02 pre-planning is complete. §13 PASS confirmed. Data schema pre-defined. The DS-07 migration and drift detection service are the primary implementation work unlocking Arc 5 completion.

### S2-02 — SI-02 Behavioural Drift Detection: Frontend Implementation
**Source:** Arc 5 roadmap; BLG-FE-52/53 component pre-design (v4.4); BLG-QA-31 Playwright pre-design (v4.4)
**Items:** BehaviouralDriftPanel component, PerformanceAnalytics integration, Playwright tests
**Owner:** Base44 Frontend; QA Lead
**Sequencing:** After S2-01 backend (depends on GET /analytics/behavioural-drift endpoint)
**Gate:** Data density verification (ST-16 in Sprint 1 confirms ≥20 trades); if gate not met, S2-02 deferred

### S2-03 — Arc 5 Enablers: Gate-Cleared Items
**Source:** BLG-BE-16, BLG-OPS-40, BLG-FE-42, BLG-FE-47
**Items:** red_flag_events severity field (gate cleared: SI-02 sprint planning imminent), Arc 5 hosting cost projection (gate cleared: SI-02 sprint planning), Arc 5 nav cohesion review (gate cleared), Red Flag Journal design review scope doc
**Owner:** Head of Backend Engineering; Infrastructure & Operations Owner; Head of UX & Design; Frontend Specs & UX Documentation Owner
**Rationale:** All four items have gates that clear with SI-02 sprint planning becoming imminent. Delivering alongside SI-02 maximises gate efficiency.
**Conditional item:** BLG-GOV-67 SI-05 Phase 1 (gate: SI-01 + SI-03 live ≥30 days = 2026-06-21)

### S2-04 — Governance, Spec Debt & OA Resolution
**Source:** v4.5 OA-01/OA-02; BLG-GOV-32/33/34/41/43/45/52; BLG-SPEC-32
**Items:** System status fix (OA-01), release planning prompt gate scan + data density checkpoint (BLG-GOV-32/43), trade count audit (BLG-GOV-33), Arc 4 data density trajectory (BLG-GOV-34), Arc 6 Monte Carlo §13 pre-assessment (BLG-GOV-45), trade plan schema audit (BLG-GOV-52), sprint close automation investigation (BLG-GOV-41), external API spec template (BLG-SPEC-32), roadmap_prompt advisory (OA-02)
**Owner:** PMO Lead; Head of Specs Team; Product Owner; Strategy Rules & System Intent Owner; QA Lead
**Rationale:** OA-01/OA-02 must be resolved per v4.5 closure. BLG-GOV-32 explicitly deferred to v4.6 from v4.5 planning. BLG-GOV-33/34 aged 6+ cycles without story. BLG-SPEC-32 gate cleared (3 external APIs now: Alpaca, Yahoo Finance, Anthropic).

### Items Explicitly Deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-25 (PT-04 Setup Quality Score) | Gate: 20+ closed trades — trade count audit (ST-16) will confirm; if unmet, defer | TBD (gate-conditional) |
| BLG-GOV-62 (SI-04 §13 pre-assessment) | Gate: SI-04 sprint planning imminent — SI-04 planned after SI-02 ships | v4.7+ |
| BLG-SPEC-35 (PO-02 §13 review) | Gate: PO-02 sprint planning imminent — Arc 4 data density gates not met | TBD |
| BLG-OPS-28 (staging deploy live verification) | Requires live Render environment with deploy hook; bounded ops task; defer if not blocking | v4.7 |
| BLG-FE-43 (SI-05 frontend spec) | Gate: SI-05 sprint planning imminent — phase after SI-05 Phase 1 gate clears | v4.7 |
| BLG-QA-26 (Arc 5 QA protocol) | Gate: all 5 Arc 5 features shipped — SI-02 not yet live | Post-v4.6 |
| BLG-GOV-30/31/55 | Already resolved per prompt_change_log.md (grooming outstanding — archive in next groom backlog) | Archive |

---

## Execution Plan

### EPIC Table

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Head of Backend Engineering; Data Model & Domain Schema Owner | RISK-01, RISK-02 | Sprint 1; before EPIC-02 |
| EPIC-02 | S2-02 | Base44 Frontend; QA Lead | RISK-03 | Sprint 2; after EPIC-01 merged; data density gate (ST-16) must pass |
| EPIC-03 | S2-03 | Head of UX & Design; Head of Backend Engineering; Infra & Ops Owner | RISK-04 | Sprint 2; parallel to EPIC-02; SI-05 conditional on 2026-06-21 gate |
| EPIC-04 | S2-04 | Head of Specs Team; PMO Lead; Product Owner | RISK-05 | Sprint 1; parallel to EPIC-01; no dependencies on SI-02 |

**EPIC-01 notes:** DS-07 migration uses `CREATE INDEX CONCURRENTLY` — requires two separate migration files (ALTER TABLE in transaction; index CONCURRENTLY outside transaction). POST /trade-plans handler updates must be backward-compatible (nullable columns, no backfill). New endpoint GET /analytics/behavioural-drift must be added to openapi.yaml and docs/specs/api_contracts/ in the same commit per CLAUDE.md §2.

**EPIC-02 notes:** Depends on EPIC-01 merged to main before Sprint 2 opens. Data density gate (ST-16 result) must be confirmed by Product Owner before EPIC-02 sprint planning seals. BehaviouralDriftPanel design informed by BLG-FE-52/53 pre-design (v4.4); si02_fe_component_predesign.md is the authoritative frontend spec.

**EPIC-03 notes:** BLG-BE-16 adds severity field to red_flag_events; openapi.yaml must be updated for the new severity filter parameter on GET /portfolio/red-flag-journal. SI-05 Phase 1 (BLG-GOV-67) is conditional — if gate (2026-06-21) does not clear before Sprint 2 seals, it is deferred and Sprint 2 closes with EPIC-03 stories ST-09–ST-12 only.

**EPIC-04 notes:** BLG-GOV-32 and BLG-GOV-43 both modify release_planning_prompt.md — grouped into single story ST-15 to reduce version bump overhead; §6 governance checklist applied once. OA-02 (ST-22) modifies roadmap_prompt.md; §6 checklist applied separately.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | DS-07 migration uses CONCURRENTLY index — requires two separate migration files; migration runner must handle correctly | Medium | Schema doc §6 specifies split; backend engineer verifies migration runner supports this pattern before ST-01 commits | null |
| RISK-02 | EPIC-01/02 | SI-02 data density gate (≥20 closed trades with linked trade_plans) may not be met — if unmet, EPIC-02 cannot produce meaningful data | Medium | BLG-GOV-33 (ST-16) runs in Sprint 1 and confirms count; if < 20, EPIC-02 is deferred; release closes with Sprint 1 only | null |
| RISK-03 | EPIC-02 | BehaviouralDriftPanel pre-design (BLG-FE-52/53, v4.4) may require updates now that full metric formulas are published in si02_drift_score.md | Low | si02_fe_component_predesign.md v1.0 incorporates metric format decisions; review at Sprint 2 planning before committing | null |
| RISK-04 | EPIC-03 | SI-05 Phase 1 gate (2026-06-21) may not be confirmed before Sprint 2 seal; deferred if gate not cleared | Low | EPIC-03 ST-13 marked conditional; Sprint 2 closes with ST-09–ST-12 if gate not met | null |
| RISK-05 | EPIC-04 | BLG-GOV-32 + BLG-GOV-43 both modify release_planning_prompt.md; OA-02 modifies roadmap_prompt.md — three §6 governance checklist applications in one EPIC | Low | Grouped BLG-GOV-32/43 into single story (ST-15); two §6 applications total (ST-15 + ST-22). Clear version bump order documented in EPIC-04 description | null |

---

## Integrity Validation — 3.5 Local Model Integrity

| Check | Result | Notes |
|-------|--------|-------|
| All S2 IDs map to EPICs | PASS | S2-01→EPIC-01, S2-02→EPIC-02, S2-03→EPIC-03, S2-04→EPIC-04 |
| All EPICs declare Maps to | PASS | See EPIC table above |
| All RISK IDs referenced in EPIC table appear in Risk Register | PASS | RISK-01/02/03/04/05 all present |
| No orphaned references | PASS | No free-text epics; all IDs stable |
| Conditional EPICs declared | PASS | EPIC-02 data density gate; EPIC-03 SI-05 conditional item; both documented |
| SI-02 §13 gate status | PASS | §13 PASS documented in decisions--2026-05-30__release-v4.5--SI-02-section13-review.md |
| SI-02 pre-planning completeness | PASS | si02_drift_score.md v1.0, si02_data_schema.md v1.0, BLG-FE-52/53, BLG-QA-31 all present |

---

## Capacity Check

**Capacity assumptions:** double (~24–28 days/sprint; 2× the standard 12–14 day solo-dev baseline from workforce_capacity.md 2026-05-27 revision)
**Timebox:** 2 sprints (~48–56 days total capacity)

| EPIC | Stories | Effort estimate | Source |
|------|---------|-----------------|--------|
| EPIC-01 | 5 | DS-07 migration M + POST handler M + drift service H + endpoint M + unit tests M = ~1.5–2 days | STEP 4 inline; si02_data_schema.md §9 |
| EPIC-02 | 3 | BehaviouralDriftPanel H + integration S + Playwright S = ~1–1.5 days | STEP 4 inline; BLG-FE-52/53 pre-design |
| EPIC-03 | 4 firm + 1 conditional | severity field M + hosting cost S + nav review M + RFJ scope S = ~0.75–1 day firm; SI-05 Phase 1 M conditional | STEP 4 inline |
| EPIC-04 | 9 | XS + S + XS + S + S + S + S + S + XS = ~1.5–2 days | STEP 4 inline |

**Sprint 1 firm:** EPIC-01 (~1.5–2 days) + EPIC-04 (~1.5–2 days) = **~3–4 days** vs 24–28 day capacity → well within
**Sprint 2 firm:** EPIC-02 (~1–1.5 days) + EPIC-03 firm (~0.75–1 day) = **~1.75–2.5 days** vs 24–28 day capacity → well within
**Sprint 2 conditional:** +EPIC-03 ST-13 SI-05 Phase 1 M (~1.5–2 days) if gate met
**Total (both sprints):** ~5–7 days of effort vs 48–56 days capacity → **~10–15% utilisation**

**Capacity verdict:** PASS — total estimated effort well within doubled capacity. Note: scope is constrained by available actionable backlog items rather than capacity. Capacity is deliberately doubled to accommodate the H-effort SI-02 implementation; actual utilisation is moderate at ~10–15%.

### Phasing Recommendation

- **Sprint 1:** EPIC-04 (governance/OA, fast deliverables) + EPIC-01 (SI-02 backend, H effort core work) — parallel EPICs; merge order EPIC-04 first, then EPIC-01
- **Sprint 2:** EPIC-03 (Arc 5 enablers, gate-cleared) + EPIC-02 (SI-02 frontend, depends on EPIC-01) — merge order EPIC-03 first, then EPIC-02 (data density gate must be confirmed before EPIC-02 sprint planning seals)

Sprint 1 data density audit (ST-16) is the decision gate for Sprint 2 EPIC-02. If closed trade count < 20, Sprint 2 proceeds with EPIC-03 only and EPIC-02 is deferred.
