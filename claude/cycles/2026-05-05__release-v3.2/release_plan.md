**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v3.2
**Cycle:** 2026-05-05__release-v3.2
**Last Updated:** 2026-05-05
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Release Plan — v3.2 Arc 2 Pre-Trade Research & Planning

---

## Readiness

### Roadmap alignment
v3.2 is the planned continuation of Arc 2 (Pre-Trade Research & Planning). The roadmap explicitly sequences PT-02 frontend as the primary v3.2 deliverable following PT-01 (shipped v3.1) and PT-02 backend (also shipped v3.1). PT-03 and PT-05 are both deferred v3.2 items.

### Prerequisite status
| Prerequisite | Status |
|--------------|--------|
| PT-01 Trade Plan Object (data model, CRUD, frontend) | ✅ Shipped v3.1 |
| PT-02 backend GET /research/{ticker} | ✅ Shipped v3.1 |
| GET /portfolio/prospective-heat (PT-03 backend) | ✅ Shipped v2.0 |
| post_ship_complete (v3.1) | ✅ True |
| next_cycle_unblocked (v3.1) | ✅ True |

### Advisories
- ⚠ **Backlog Age:** BLG-GOV-11 (Cycle artefact inventory) deferred 3 consecutive cycles (v3.0, v3.1, and carries into v3.2 candidate pool). In-scope for v3.2 as ST-17.
- ℹ **Provisional-Target:** 7 items carry `Provisional-Target: v3.2`. 6 in scope. 1 deferred (BLG-FEAT-13 → v3.3). 3 items have no Provisional-Target signal.
- ℹ **Design dependency scan:** 1 item flagged — BLG-FE-22 (Screener morning routine UX spec) is explicitly marked "before v3.2 sprint planning" and is a prerequisite input for PT-02 UX story authoring. Design gate required for v3.2.

---

## Scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Pre-Trade Research View frontend (PT-02) — fetch and render research data from existing GET /research/{ticker} endpoint; ticker fundamentals, news, and momentum signals |
| S2-02 | EPIC-01 | Prospective Heat at Entry integration (PT-03) — surface GET /portfolio/prospective-heat result within the research view; frontend integration only, backend shipped |
| S2-03 | EPIC-02 | Pre-Trade Entry Checklist (PT-05) — checklist component embedded in Trade Plan form flow; schema, UI, pre-population from trade plan data, and persistence |
| S2-04 | EPIC-03 | Governance & process prompt hardening — D-01 through D-04 from v3.1 lessons_learnt deferred actions (OA-02 to OA-05); sprint_planning_prompt.md branch check, execution_prompt.md deviations_filed and test_scenarios patches, Playwright waitFor pattern |
| S2-05 | EPIC-03 | Test scenario gap remediation — TEST-GAP-EPIC-01 (Trade Plan domain) and TEST-GAP-EPIC-03 (Earnings Calendar + UK screener) from v3.1 delivery verification |
| S2-06 | EPIC-04 | Documentation & security quick wins — BLG-FE-16 (React component inventory), BLG-FE-21 (design system document), BLG-SEC-05 (Alpaca credential audit and rotation policy), BLG-GOV-18 (external API dependency register), BLG-GOV-11 (cycle artefact inventory — 3rd deferral, mandatory) |

### Explicitly deferred
| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-13 (gated feature rollout) | P3 capacity trade-off; Arc 2 EPIC-01/02 are the primary user-value deliverables. 2nd consecutive deferral; will be mandatory in v3.3 | v3.3 |
| BLG-FEAT-20 (net-of-costs tracking) | Provisional-Target changed to Arc 3/4 context — not a standalone sprint item; sequence alongside Arc 3/4 data model work | Arc 3/4 |
| BLG-FE-22 (Screener morning routine UX spec) | Treated as design gate prerequisite deliverable, not a sprint story — must be delivered before sprint planning seals | Design gate |

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01, S2-02 | Frontend Specs & UX Documentation Owner | RISK-01 | BLG-FE-22 UX spec must be complete (design gate); after EPIC-03 governance stories |
| EPIC-02 | S2-03 | Frontend Specs & UX Documentation Owner | RISK-02 | After EPIC-01 (PT-05 depends on PT-02 being live) |
| EPIC-03 | S2-04, S2-05 | Head of Specs Team | RISK-03 | Sprint 1; no external dependency |
| EPIC-04 | S2-06 | PMO Lead + Cybersecurity & Trust Lead | — | Sprint 2; no dependency on EPIC-01/02 |

**EPIC-01 note:** PT-02 frontend is the largest single deliverable. BLG-FE-22 must be completed in the design gate phase and its navigation model adopted into story acceptance criteria before sprint planning seals.

**EPIC-02 note:** PT-05 (Entry Checklist) is embedded in the Trade Plan form. Depends on PT-02 research view being available for context linking. Sequence in Sprint 2 after EPIC-01 merges.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | BLG-FE-22 UX spec not completed before sprint planning seals — PT-02 UX stories authored without navigation model, leading to rework or fragmented design | High | Design gate required before sprint planning; BLG-FE-22 is a mandatory design gate deliverable; Sprint Planning Engine STEP -1 must consume this checklist | null |
| RISK-02 | EPIC-02 | PT-02 frontend not merged before EPIC-02 begins — PT-05 checklist has no research context to link to | Medium | Sprint 2 sequencing enforces ordering; EPIC-02 may not start until EPIC-01 PR merges | null |
| RISK-03 | EPIC-03 | Governance prompt patches (ST-07 to ST-10) require CLAUDE.md §6 compliance checklist (version bump, OPERATIONAL_GUIDE update, prompt_change_log entry) — all four changes in same sprint creates coordination overhead | Medium | EPIC-03 stories must be committed per §6 checklist; QA evidence log must confirm checklist compliance before PR opens | null |

---

## Integrity Validation — 3.5 Local Model Integrity

- All 6 scope items have S2-IDs ✅
- All 4 EPICs have EPIC-IDs ✅
- All EPICs declare `Maps to:` S2 items ✅
  - EPIC-01 → S2-01, S2-02
  - EPIC-02 → S2-03
  - EPIC-03 → S2-04, S2-05
  - EPIC-04 → S2-06
- All 3 risks have RISK-IDs and Relates to fields ✅
- No orphan S2 items (all 6 mapped to EPICs) ✅
- No orphan EPICs (all 4 have S2 coverage) ✅
- `escalation_ref` populated on all risks (null = no escalation raised) ✅

**Result: ✅ Pass**

---

## Capacity Check

### Effort estimates (inline — no scored_initiatives.md match)

| EPIC | Stories | Effort estimate | Skill domain |
|------|---------|-----------------|--------------|
| EPIC-01 | 4 (ST-01 to ST-04) | M–M–S–S → ~5–8 days | Frontend + UX |
| EPIC-02 | 2 (ST-05, ST-06) | M–M → ~2–3 days | Frontend + Backend |
| EPIC-03 | 6 (ST-07 to ST-12) | XS–XS–XS–XS–S–S → ~2–3 days | Governance + QA |
| EPIC-04 | 5 (ST-13 to ST-17) | M–M–S–S–M → ~3–5 days | Documentation + Security |
| **Total** | **17** | **~12–19 days** | Mixed |

Available capacity (2 sprints, solo developer evenings): ~10–12 days.

**Outcome: ⚠ WARN** — Total estimated effort exceeds available capacity at mid-point (~15 days vs ~11 days available).

**Mitigating factors:** EPIC-03 stories (ST-07 to ST-10) are prompt file edits estimated at 30–60 minutes each; EPIC-04 stories are documentation tasks estimated at 1–2 days each. Actual EPIC-01/02 risk is the primary capacity driver. Historical velocity = 1.00 across last 6 cycles at similar scopes (v3.0: 16 stories, v3.1: 14 stories).

### Phasing Recommendation

| Phase | Sprint | EPICs | Est. hours | Rationale |
|-------|--------|-------|------------|-----------|
| Phase 1 | Sprint 1 | EPIC-01 + EPIC-03 | ~7–11 days | PT-02 frontend (core user value); governance patches (lightweight, clear the OA backlog) |
| Phase 2 | Sprint 2 | EPIC-02 + EPIC-04 | ~5–8 days | PT-05 (depends on PT-02 live); documentation and security items (time-insensitive) |

Ordering rationale: EPIC-01 delivers the primary Arc 2 feature and blocks EPIC-02. EPIC-03 governance patches are lightweight and clear 4 outstanding OAs from v3.1 — high governance value at low effort. EPIC-04 items are independent and suitable for Sprint 2 alongside EPIC-02.

---

## Integrity Validation — 5.5 Cross-Stage Integrity

| Check | Result |
|-------|--------|
| All S2-IDs traced to EPICs | ✅ S2-01→EPIC-01, S2-02→EPIC-01, S2-03→EPIC-02, S2-04→EPIC-03, S2-05→EPIC-03, S2-06→EPIC-04 |
| All EPIC-IDs present in stage4_backlog_slice.md | ✅ EPIC-01, EPIC-02, EPIC-03, EPIC-04 |
| All ST-IDs in backlog slice reference an EPIC | ✅ ST-01 to ST-17 all assigned to EPICs |
| ST count matches: 17 declared, 17 in slice | ✅ |
| Scope document present | ✅ docs/product/scope/scope--2026-05-05__release-v3.2-arc-2-pre-trade-research.md |
| Decisions record present | ✅ docs/product/decisions/decisions--2026-05-05__release-v3.2.md |
| No orphan backlog items | ✅ |
| No scope drift from STEP 2 | ✅ |

**Result: ✅ Pass**

---

## Integrity Validation — 5.7 Decision Record Integrity

No escalations raised in this cycle. No AR or SRB decision records created. `stage5_7_decision_record_integrity` = not_applicable.

**Result: ✅ Not Applicable**
