**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v3.5
**Cycle:** 2026-05-15__release-v3.5
**Last Updated:** 2026-05-15

---

# Release Plan — v3.5 Arc 3 Completion + Arc 4 Foundation

---

## Readiness

### §1.1 Backlog Age Advisory

Spec/documentation debt items aged 2+ cycles without story assignment:

| Item | Type | Cycles without ST | Advisory |
|------|------|------------------|---------|
| BLG-FE-26 — Research page UX review: regime lozenge and font consistency | Frontend / UX | 3 (Provisional-Target v3.3; deferred v3.3; deferred to design gate v3.4) | ⚠ 3 cycles unassigned — recommend decision: either assign ST in v3.5 spec/debt EPIC or formally re-park to Arc 4 design gate |

**Action (advisory):** BLG-FE-26 has been deferred since v3.3. P3 priority and design exploration nature make it low-risk to continue parking. Product Owner decision: not assigned a story in v3.5 (deferred again to Arc 4/5 design gate when design system investment is warranted). Recorded in run manifest as outstanding advisory.

### §1.2 Provisional-Target Advisory

Items carrying `Provisional-Target: v3.5` (horizon-planned for this release): 5 items.
- BLG-QA-19 — Research view regression test protocol
- BLG-SPEC-29 — Grace-period-alert ux_spec sessionStorage correction
- BLG-SPEC-30 — Stop-management-workflow ux_spec PATCH verb correction
- BLG-SPEC-31 — React Query v5 onSuccess codebase scan
- BLG-GOV-22 — sprint_planning_prompt.md shared execution_state.json ownership

Items horizon-planned for Arc 4 start (triggering condition met):
- BLG-GOV-21 — Arc 4 data requirements capture (Provisional-Target: "Before Arc 4 planning begins" — v3.5 is the Arc 4 start release per roadmap)

Items entering scope from roadmap (no Provisional-Target field):
- IT-06 — Alpaca Paper Trading Integration (Arc 3 remainder; §13 gate required)
- PO-01 — Plan vs Reality Analysis (Arc 4 first feature; requires PT-01 live ✅)

Items without matching Provisional-Target signal (no PT field or PT=other): BLG-OPS-13, BLG-FE-26, BLG-FE-27 — 3 items (not in v3.5 scope).

### §1.3 Design-Gate Language Scan

| Item | Flag | Note |
|------|------|------|
| IT-06 — Alpaca Paper Trading Integration | ⚠ Design dependency detected | §13 review required before any implementation; strategy decision by Strategy Rules & System Intent Owner |
| PO-01 — Plan vs Reality Analysis | ⚠ Design dependency detected | New Arc 4 surface (plan vs reality comparison view at trade close) requires UX spec before sprint planning seals EPIC-02 |

**Design dependency scan: 2 items flagged.** Surface at Pre-sprint Required Decisions checklist. Design gate (Phase 1.5) must produce: (a) §13 determination for IT-06; (b) UX spec for PO-01 comparison view before EPIC-02 sprint planning seals.

---

## Scope

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Arc 3 Completion — IT-06 Alpaca Paper Trading: §13 compliance review (prerequisite story) + backend sync service + frontend display. US market only. Scoped conditional on §13 PASS. |
| S2-02 | EPIC-02 | Arc 4 Foundation — BLG-GOV-21 Arc 4 data requirements capture (prerequisite doc) + PO-01 Plan vs Reality Analysis backend (calculation service, data model) + PO-01 frontend (comparison view at trade close). |
| S2-03 | EPIC-03 | Spec & QA Debt — BLG-SPEC-29 (grace-period sessionStorage correction), BLG-SPEC-30 (stop-management PATCH correction), BLG-SPEC-31 (React Query v5 onSuccess scan), BLG-QA-19 (research view regression protocol). |
| S2-04 | EPIC-04 | Governance Patches — BLG-GOV-22 (sprint_planning_prompt.md execution_state.json ownership + Positions.js merge guidance) + execution_prompt.md deviation-filing advisory patches (LL v3.4 items #3–#5) + sprint_close / LL formatting improvements (LL v3.4 items #6–#7). |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| IT-06 implementation (only) | Conditional: if §13 review determines non-compliant, implementation scope removed; §13 review story retained | Descoped in-sprint if §13 fails |
| PT-04 Setup Quality Score | Gate: 20+ closed trades — data volume not yet reached | Arc 4 later cycle |
| BLG-FE-26 Research page UX review | P3; 3 cycles deferred; no blocking workflow; defer to Arc 4/5 design gate | Arc 4/5 design gate |
| BLG-FE-27 Nav bar redesign exploration | Design exploration item; not urgent; not blocking any workflow | Arc 4/5 design gate |
| BLG-OPS-13 API performance baseline re-run | Requires live environment + human coordination; P3 | Next operational review |
| PO-02 Journal Pattern Recognition | Gate: 6+ months AI-summarised journal entries (BLG-FEAT-16 must be active) | Arc 4 later cycle |
| IT-06 (if §13 fails) | Full re-scope required if §13 review determines paper trading is outside §13 bounds | Post-§13 decision |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-05-15__release-v3.5

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Head of Engineering | RISK-01 | Sprint 1: §13 review ST first; implementation conditional on §13 PASS; design gate must deliver IT-06 UX spec |
| EPIC-02 | S2-02 | Head of Engineering | RISK-02 | Sprint 2; BLG-GOV-21 data requirements doc first (ST-04); PO-01 backend then frontend; design gate must deliver PO-01 UX spec |
| EPIC-03 | S2-03 | Head of Specs Team | None | Sprint 1; no dependencies; parallelisable with EPIC-04 |
| EPIC-04 | S2-04 | Head of Specs Team | None | Sprint 1; EPIC-04 first per governance patch convention |

**EPIC-01 note:** §13 review (ST-01) must be completed before any IT-06 implementation story begins. If §13 review yields FAIL (paper trading determined to be outside §13 bounds), EPIC-01 scope reduces to the §13 review story only. Backup scope: add BLG-GOV-21 and governance debt to Sprint 1 to maintain velocity.

**EPIC-02 note:** BLG-GOV-21 (data requirements capture) is a prerequisite for informed PO-01 planning. PO-01 is H effort — if capacity is tight after IT-06, PO-01 may be phased: backend in Sprint 2, frontend deferred to v3.6. Design gate must produce PO-01 UX spec before EPIC-02 sprint planning seals.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | §13 review may determine IT-06 paper trading is outside system bounds (connects to broker execution infrastructure) | High | §13 review as Sprint 1 ST-01 (before any implementation); if FAIL, EPIC-01 reduces to §13 doc only; Arc 4 backup scope absorbs capacity | null |
| RISK-02 | EPIC-02 | PO-01 (H effort) + IT-06 backend (M effort) in same release may exceed solo-dev capacity | Medium | Phase: IT-06 Sprint 1, PO-01 Sprint 2; PO-01 can split backend/frontend across v3.5/v3.6 if needed | null |
| RISK-03 | EPIC-02 | PO-01 depends on PT-01 data being populated (trade plans exist for comparison) — limited real data if user has few closed trades with plans | Low | Feature designed to gracefully degrade — "no trade plans with comparison data yet" empty state; no gate on data volume for feature implementation | null |

---

## Integrity Validation — 3.5 Local Model Integrity

### S2-ID → EPIC mapping
| S2-ID | EPIC | Status |
|-------|------|--------|
| S2-01 | EPIC-01 | ✅ Mapped |
| S2-02 | EPIC-02 | ✅ Mapped |
| S2-03 | EPIC-03 | ✅ Mapped |
| S2-04 | EPIC-04 | ✅ Mapped |

### EPIC → RISK mapping
| EPIC | RISK-IDs | Status |
|------|---------|--------|
| EPIC-01 | RISK-01 | ✅ Mapped |
| EPIC-02 | RISK-02, RISK-03 | ✅ Mapped |
| EPIC-03 | (none) | ✅ No high risks |
| EPIC-04 | (none) | ✅ No high risks |

### RISK → Risk Register
| RISK-ID | In Register | escalation_ref |
|---------|-------------|----------------|
| RISK-01 | ✅ | null |
| RISK-02 | ✅ | null |
| RISK-03 | ✅ | null |

**Result: PASS** — All S2 IDs mapped to EPICs; all RISK IDs referenced in EPIC table appear in Risk Register; no orphaned references.

**attributes.plan_executable:** true

---

## Capacity Check

### Effort Estimates

| EPIC | Stories (est.) | Effort estimate | Effort Band | Source |
|------|---------------|-----------------|-------------|--------|
| EPIC-01 | 3 stories | S (§13 review) + M + M = ~4–5 days | M | Inline estimate |
| EPIC-02 | 3 stories | S + M-H + M = ~6–8 days | H | Inline estimate |
| EPIC-03 | 4 stories | XS + XS + S + S = ~1.5–2 days | S | Inline estimate |
| EPIC-04 | 3 stories | S + S + S = ~1.5–2 days | S | Inline estimate |

**Total: ~13–17 days mid-point.** Standard release pacing: 2 sprints, ~8–10 days per sprint at solo-dev rate.

**Note on scored_initiatives.md:** 0 matching entries (file predates Arc 3/4). All estimates are inline.

**§13 contingency:** If RISK-01 fires (§13 FAIL), EPIC-01 shrinks from ~5 days to ~0.5 days. Net capacity freed: ~4–4.5 days. This capacity would be absorbed by pulling in backup scope (BLG-OPS-13, BLG-FE-26 if P3 acceptable, or pulling in Arc 4 PO-01 backend earlier).

**Outcome: WARN** — Total estimated effort (13–17 days) exceeds typical 2-sprint capacity (~10–12 days at solo-dev evenings pace). The §13 contingency (RISK-01) and PO-01 phasing (RISK-02) provide natural release valves.

---

## Integrity Validation — 5.5 Cross-Stage Integrity

### S2-ID → EPIC coverage

| S2-ID | EPIC referenced in stage4 | In Risk Register (if applicable) | Status |
|-------|--------------------------|----------------------------------|--------|
| S2-01 | EPIC-01 ✅ | RISK-01 ✅ | PASS |
| S2-02 | EPIC-02 ✅ | RISK-02, RISK-03 ✅ | PASS |
| S2-03 | EPIC-03 ✅ | (none) | PASS |
| S2-04 | EPIC-04 ✅ | (none) | PASS |

### EPIC IDs in stage4 vs stage3

EPICs in stage3 (Execution Plan): EPIC-01, EPIC-02, EPIC-03, EPIC-04.
EPICs in stage4 (stage4_backlog_slice.md): EPIC-01, EPIC-02, EPIC-03, EPIC-04.
**No orphaned EPICs. No missing EPICs.**

### RISK IDs cross-reference

RISK-IDs in EPIC table: RISK-01 (EPIC-01), RISK-02 (EPIC-02), RISK-03 (EPIC-02).
RISK-IDs in Risk Register: RISK-01 ✅, RISK-02 ✅, RISK-03 ✅.
**All RISK-IDs present in register.**

**5.5 result: PASS**

### 5.7 Decision Record Integrity

- `docs/product/decisions/decisions--2026-05-15__release-v3.5.md` — present ✅
- Mandatory template fields populated: Release, Cycle, Last Updated, scope decisions, sequencing decisions, accepted risks ✅
- Accepted risks section: "None" (no escalations raised) ✅
- No AR/SRB records referenced.

**5.7 result: PASS**

---

### Phasing Recommendation

- **Phase 1 (Sprint 1): EPIC-04 + EPIC-03 + EPIC-01 (ST-01 §13 review only)** — ~3–5 days. Front-load governance patches and spec debt. §13 review gates implementation.
- **Phase 2 (Sprint 2): EPIC-01 (IT-06 implementation, conditional) + EPIC-02 (PO-01)** — ~8–10 days. If §13 PASS: IT-06 backend + frontend. If §13 FAIL: full Sprint 2 capacity to EPIC-02 Arc 4. PO-01 backend first, frontend if capacity remains; otherwise PO-01 frontend deferred to v3.6.

**Ordering rationale:** Governance and spec debt first (EPIC-03/04 sprint 1) to clear quality debt and prevent recurrence; §13 review as early gate to de-risk EPIC-01; Arc 4 foundation in Sprint 2 (depends on data requirements capture first).
