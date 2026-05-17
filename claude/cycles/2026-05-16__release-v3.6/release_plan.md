Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v3.6
Cycle: 2026-05-16__release-v3.6
Last Updated: 2026-05-16

---

# Release Plan — v3.6 Arc 4 Data Integrity + Arc 2 Quality Score + Debt Clearance

## Readiness

**Release:** v3.6
**Cycle:** 2026-05-16__release-v3.6
**Prior release:** v3.5 — Closed ✅
**Lifecycle guard:** status = Closed, post_ship_complete = true, next_cycle_unblocked = true ✅

### Readiness checks

| Check | Result | Notes |
|-------|--------|-------|
| Prior cycle closed | ✅ Pass | 2026-05-15__release-v3.5 Closed_with_actions |
| v3.6 on roadmap | ✅ Pass | Listed as Next planned release |
| Backlog available | ✅ Pass | Active backlog has 7+ items |
| No active amendment | ✅ Pass | status = Closed, not Amendment_In_Progress |
| No stale backlog lock | ✅ Pass | No claude/backlog/.lock present |

### Backlog age advisory

⚠ Advisory: 2 spec/documentation debt items aged 2+ cycles without story assignment:
- BLG-FE-26 (Provisional-Target: v3.3 — 3+ cycles): Research page UX review
- BLG-SPEC-27 (Provisional-Target: v3.4 — 2+ cycles): Research endpoint error codes

Both promoted to sprint story scope in this release (S2-03). Recommendation satisfied.

### Provisional-Target advisory

ℹ 1 item carries `Provisional-Target: v3.6` — BLG-FE-32 (SC-RV-18/19 Playwright coverage). 6 items have no matching v3.6 Provisional-Target signal (deferred or TBD).

### Design-gate language scan

Design dependency scan: 1 item flagged — PT-04 Setup Quality Score has implicit spec authoring dependency (no canonical spec exists; scoring algorithm requires Product Owner definition before implementation). Surfaced at Pre-sprint Required Decisions checklist.

---

## Scope

### S2-01 — Arc 4 Data Capture Foundation

**Rationale:** PO-01 (Plan vs Reality Analysis) shipped v3.5 but `entry_delta_pct` was deferred because `planned_entry_price` is not captured at trade entry. Every trade entry without this snapshot is Arc 4 data lost. Priority fix to ensure the data pipeline is complete before more trades accumulate.

**Backlog source:** v3.5 PO-01 delivery note (arc4_data_requirements.md §3.1 deferral)

**Scope:** Backend — capture `planned_entry_price` from linked trade plan at position creation; update plan-vs-reality service to compute and return `entry_delta_pct`. Frontend — update PlanVsReality component to display entry delta when available.

---

### S2-02 — Arc 2 Completion: PT-04 Setup Quality Score

**Rationale:** PT-04 is the only remaining Arc 2 feature. Gate: 20+ closed trades (system has been live since v1.5; gate likely met but PO must confirm before sprint planning seals). Spec authoring required before implementation — no canonical spec exists for the scoring algorithm.

**Backlog source:** Roadmap §4 Arc 2 — PT-04 Setup Quality Score (M effort)

**Scope:** Spec authoring (delegated_decision sprint 1 story); backend scoring endpoint; frontend display in Pre-Trade Research View.

**Gate condition:** Product Owner must confirm 20+ closed trades before sprint planning seals. If gate not met: EPIC-02 defers to v3.7.

---

### S2-03 — QA, Spec & UX Debt Clearance

**Rationale:** Three aged backlog items now blocking UX quality and test completeness. BLG-FE-32 + TEST-GAP-EPIC-03-v33 have been deferred 2+ cycles; BLG-SPEC-27 deferred 2+ cycles; BLG-FE-26 deferred 3+ cycles.

**Backlog sources:** BLG-FE-32 (SC-RV-18/19 Playwright), TEST-GAP-EPIC-03-v33 (research view null state test scenarios), BLG-SPEC-27 (research endpoint HTTP error differentiation), BLG-FE-26 (research page UX: regime lozenge + font consistency)

**Scope:** Playwright tests for SC-RV-18/19; backend error code differentiation; UX review and fix.

---

### S2-04 — Governance Maintenance

**Rationale:** Four execution_prompt.md patches deferred from v3.5 lessons learnt closure. Also: 4 prompt versions unrecorded in prompt_change_log.md (OA-RP-01–04). Pattern from v3.5: governance patches bundled into EPIC-04 clear LL debt efficiently within one cycle.

**Backlog sources:** v3.5 lessons_learnt_closure.md deferred actions 1–4; OA-RP-01–04 (run manifest)

**Scope:** execution_prompt.md §13 gate story pattern formalisation; deviations_filed + sprint_close three-field block + Phase 3 section reference patches; prompt_change_log.md missing entries (OA-RP-01–04).

---

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| PO-02 Journal Pattern Recognition | Gate: 6+ months AI-summarised journal data (AI Journal Summarisation shipped 2026-04-20 — ~1 month ago, gate not met) | v3.7+ |
| PO-03 Behavioural Error Taxonomy | Depends on PO-02; gate not met | v3.7+ |
| PO-04 Reflection ↔ Outcome Correlation | Depends on PO-02; gate: 50+ trades with plans | v3.8+ |
| PO-05 Lightweight Replay Mode | VH effort; depends on IT-06 + data accumulation | v3.8+ |
| BLG-FEAT-20 Net-of-costs tracking | M effort; deferred to Arc 4 data model work — not standalone | v3.7+ |
| BLG-FE-27 Nav bar redesign | P3 Low; non-blocking design exploration | TBD |
| BLG-OPS-13 API performance baseline | Requires live environment + human coordination; not automatable | TBD |

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Head of Engineering | RISK-01 | Before EPIC-02 (data model first) |
| EPIC-02 | S2-02 | Head of Specs Team + Head of Engineering | RISK-02 | After EPIC-01; gate confirmation before seal |
| EPIC-03 | S2-03 | QA & Testing Owner + API Contracts Owner | RISK-03 | Parallel with EPIC-01 |
| EPIC-04 | S2-04 | Head of Specs Team | — | Sprint 1 priority (governance debt) |

**EPIC-01 note:** ST-01 (backend) must precede ST-02 (frontend). Data model migration required — planned_entry_price field addition to trades table. Existing PlanVsReality display degrades gracefully when field absent (historical trades).

**EPIC-02 note:** Sprint 1 story = spec authoring (delegated_decision, gating Sprint 2 implementation). Gate confirmation (20+ closed trades) must be obtained from Product Owner before sprint planning seals. If gate not met, EPIC-02 defers entirely.

**EPIC-04 note:** §13 carry-forward advisory: when any arc feature requires a §13 review, the pattern is to scope the review as a Sprint 1 story (delegated_decision) gating implementation in Sprint 2. No §13 review required in v3.6 scope; pattern documentation target is EPIC-04 ST-08.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | planned_entry_price schema migration may affect existing trade records with null values; PlanVsReality must handle null gracefully | Medium | Nullable field + conditional display; test with existing null data | null |
| RISK-02 | EPIC-02 | PT-04 gate (20+ closed trades) not confirmed; no canonical spec for scoring algorithm | High | Sprint 1 delegated_decision story: PO confirms gate + authors spec before implementation stories seal | null |
| RISK-03 | EPIC-03 | BLG-SPEC-27 HTTP error differentiation may require openapi.yaml changes; potential regression in research endpoint callers | Low | Scope backend only; update openapi.yaml in same commit per CLAUDE.md §2 | null |

### Pre-sprint Planning Required Decisions

The following High-priority decisions must be resolved before sprint planning seals (before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-02] PT-04 gate confirmation — Product Owner must confirm 20+ closed trades before sprint planning seals. If confirmed: EPIC-02 proceeds in Sprint 2. If not confirmed: EPIC-02 defers to v3.7. — Owner: Product Owner

---

## Integrity Validation — 3.5 Local Model Integrity

| Check | Result | Notes |
|-------|--------|-------|
| All S2 IDs present | ✅ Pass | S2-01 through S2-04 defined |
| All EPICs have Maps-to | ✅ Pass | EPIC-01→S2-01, EPIC-02→S2-02, EPIC-03→S2-03, EPIC-04→S2-04 |
| All RISK IDs referenced | ✅ Pass | RISK-01 (EPIC-01), RISK-02 (EPIC-02), RISK-03 (EPIC-03) |
| Scope items match EPICs | ✅ Pass | 4 scope items, 4 EPICs |
| Deferred items documented | ✅ Pass | 7 items explicitly deferred with rationale |
| No orphaned EPIC references | ✅ Pass | All EPICs trace to scope items |

**Model integrity: PASS** — plan is internally consistent and executable.

---

## Capacity Check

**Mode:** standard (WARN permitted)
**Capacity:** solo-dev (single developer, evening hours + occasional full days)
**Timebox:** 2 sprints (~2 weeks estimated)
**scored_initiatives.md:** Not present for Arc 4/Arc 2 items — Tier 3 estimates used throughout.

| EPIC | Scope | Effort estimate | Sprint |
|------|-------|----------------|--------|
| EPIC-04 Governance Patches | S2-04 | XS–S (~0.5 day: 2 stories, autonomous) | Sprint 1 |
| EPIC-03 QA, Spec & UX | S2-03 | S (~1 day: 3 stories, autonomous/QA) | Sprint 1 |
| EPIC-01 Arc 4 Data Capture | S2-01 | M (~1.5–2 days: 2 stories, backend + frontend) | Sprint 1–2 |
| EPIC-02 PT-04 Quality Score | S2-02 | M–L (~2–3 days: 3 stories, spec + backend + frontend) | Sprint 2 (gated) |

**Totals (without EPIC-02):** ~3–3.5 days estimated effort against solo-dev evening capacity (2–3 hrs/day). Within 2-sprint capacity.
**Totals (with EPIC-02):** ~5–6.5 days. Feasible across 2 sprints with phased delivery.

### Phasing Recommendation

Sprint 1 (days 1–3): EPIC-04 (governance patches), EPIC-03 (QA/spec/UX), EPIC-01 ST-01 (backend data capture) — estimated 2–2.5 days. Gate check: EPIC-02 PT-04 gate confirmation obtained by Sprint 1 close.

Sprint 2 (days 4–7): EPIC-01 ST-02 (frontend PlanVsReality update), EPIC-02 (PT-04 full, if gate confirmed) — estimated 2–3 days.

**Outcome:** WARN — total with EPIC-02 approaches solo-dev capacity limit for 2 sprints. Phasing recommendation distributes workload. Sprint Planning Engine to verify sprint-level utilisation at plan seal.

---

## Integrity Validation — 5.5 Cross-Stage Integrity

| Check | Result | Notes |
|-------|--------|-------|
| All S2 IDs map to EPICs | ✅ Pass | S2-01→EPIC-01, S2-02→EPIC-02, S2-03→EPIC-03, S2-04→EPIC-04 |
| All EPIC IDs in backlog slice match stage3 | ✅ Pass | EPIC-01/02/03/04 confirmed in both |
| All RISK IDs in EPIC table appear in Risk Register | ✅ Pass | RISK-01/02/03 all present |
| No orphaned references | ✅ Pass | All IDs traceable |
| Decisions record present | ✅ Pass | decisions--2026-05-16__release-v3.6.md created |
| Scope document present | ✅ Pass | scope--2026-05-16__release-v3.6-arc-4-data-integrity.md created |

**Cross-stage integrity: PASS**

### 5.7 Decision Record Integrity

| Check | Result | Notes |
|-------|--------|-------|
| Decisions document present | ✅ Pass | docs/product/decisions/decisions--2026-05-16__release-v3.6.md |
| All mandatory template fields populated | ✅ Pass | Scope decisions, sequencing decisions, accepted risks all populated |
| No AR/SRB records referenced in escalations | ✅ N/A | No escalations raised this cycle |

**Decision record integrity: PASS (no escalations)**
