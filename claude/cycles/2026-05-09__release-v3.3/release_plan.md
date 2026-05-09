**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v3.3
**Cycle:** 2026-05-09__release-v3.3
**Last Updated:** 2026-05-09

---

# Release Plan — v3.3 Arc 3 In-Trade Risk Management

---

## Readiness

**Release:** v3.3
**Planned theme:** Arc 3 start — In-Trade Risk Management (IT-01, IT-02, IT-03) + Research View Spec Closure + Governance Patches

### Prior cycle confirmation

| Item | Status |
|------|--------|
| v3.2 post-ship closure | ✅ Complete (Closed_with_actions 2026-05-07) |
| v3.2 delivery verification | ✅ Verified |
| next_cycle_unblocked | ✅ true |
| Carry-forward items reviewed | ✅ 3 items (CF-01, CF-02, CF-03) — all addressed in EPIC-04 |

### Backlog readiness

- 10 backlog items carry `Provisional-Target: v3.3`
- 6 items carry `Provisional-Target: Before v3.3 sprint planning` — included as Sprint 1 spec/QA stories
- Arc 3 roadmap items (IT-01 through IT-05) have no gate conditions blocking v3.3 entry (IT-06 needs §13 review — deferred)
- BLG-FEAT-13 mandatory: 3rd consecutive deferral; roadmap annotation states "mandatory for v3.3"
- PT-04 (Setup Quality Score) gate not met (20+ closed trades required) — deferred to v3.4+

### Outstanding actions (v3.2 carry-forward)

| OA | Status | v3.3 scope action |
|----|--------|-------------------|
| OA-01 (CF-01) | Open | EPIC-04 ST-13 — execution_prompt sealed-file integrity check |
| OA-02 (CF-02) | Open | EPIC-04 ST-13 — mock payload API shape advisory |
| OA-03 | Open | EPIC-04 ST-14 — backlog deferral policy doc + BLG-FEAT-13 in scope |
| OA-04 | Ongoing | PMO Lead monitoring |
| OA-05 | Open | EPIC-04 ST-14 — sprint_planning design gate check |
| OA-06 | Ongoing | Covered by BLG-OPS-15 (EPIC-03 ST-12) + BLG-OPS-13 (deferred) |

### Advisory checks

- ⚠ Backlog age: 0 spec/doc items aged 2+ cycles without story assignment.
- ℹ Provisional-Target: 10 items `v3.3`, 6 items `Before v3.3 sprint planning`.
- ℹ Design-gate language scan: 6 items flagged ("before sprint planning" prerequisite language). Surface at Pre-Sprint Required Decisions checklist.

---

## Scope

### S2 Scope Items

| S2-ID | Description | Backlog refs | Priority |
|-------|-------------|-------------|----------|
| S2-01 | Position Lifecycle Manager (IT-01) — backend state machine + frontend state display | IT-01 | P1 |
| S2-02 | Grace Period Decision Support (IT-02) + Stop Management Workflow (IT-03) | IT-02, IT-03 | P1 |
| S2-03 | Research view specification & QA closure | BLG-SPEC-24/25/26, BLG-FE-28, BLG-QA-14/15/16/17, BLG-OPS-15, BLG-SEC-06, BLG-GOV-20 | P1/P2 |
| S2-04 | Governance patches + mandatory quick wins | OA-01/02/03/05, CF-01/02/03, BLG-GOV-19, BLG-FEAT-13, BLG-FEAT-21, BLG-FE-23/24/25/29/30 | P1/P2/P3 |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| IT-04 Drawdown-Triggered Review Prompt | Sequenced after Arc 3 foundation established; defer to next Arc 3 release | v3.4 |
| IT-05 Position Concentration Limits | Sequenced with IT-04 | v3.4 |
| IT-06 Alpaca Paper Trading Integration | §13 review required before pre-alignment (paper trading touches execution infrastructure) | v3.4+ with §13 review |
| PT-04 Setup Quality Score | Gate not met: requires 20+ closed trades; depends on PT-01 | v3.4+ (gate-dependent) |
| BLG-FE-26 Research page UX review | P3; no blocking workflow; defer | v3.4 |
| BLG-FE-27 Nav bar redesign | P3 design exploration; not urgent | Arc 3 (design only) |
| BLG-AI-03 AI Journal quarterly review | Define process before v3.4 | v3.4 |
| BLG-OPS-13 API performance baseline re-run | Requires live environment; deferred to standalone ops task | Before next perf review |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-05-09__release-v3.3

---

## Execution Plan

### EPIC Table

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Head of Engineering | RISK-01 | Must complete before EPIC-02 (IT-01 is Arc 3 data foundation) |
| EPIC-02 | S2-02 | Head of Engineering | RISK-02 | After EPIC-01 (uses position state infrastructure) |
| EPIC-03 | S2-03 | Head of Specs Team | RISK-03 | Sprint 1; parallel with EPIC-01; "before sprint planning" items complete before EPIC-02 designs finalise |
| EPIC-04 | S2-04 | PMO Lead + Head of Specs Team | RISK-04 | Sprint 1 (governance); Sprint 2 (quick wins); BLG-FEAT-13 after feature flag infra ready |

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Position state machine complexity — open positions need state assigned retroactively; migration edge cases | High | Back-fill logic with explicit "unknown" initial state; migration tested on staging before prod deploy | null |
| RISK-02 | EPIC-02 | Stop Management (IT-03) — ATR trail calculation depends on existing stop price join (shipped v2.4); calculation may surface edge cases with missing stop values | Medium | Verify stop price join in staging; null stop handled gracefully (disable trail UI if no current stop) | null |
| RISK-03 | EPIC-03 | Spec authoring dependency — BLG-SPEC-24/FE-28 must be complete before EPIC-02 frontend stories can be designed; delay propagates to Sprint 2 | Medium | EPIC-03 Sprint 1 priority; spec authoring starts day 1 of sprint | null |
| RISK-04 | EPIC-04 | BLG-FEAT-13 feature flag rollout — new platform capability with no existing infrastructure; scope must be tightly controlled to avoid creep | Medium | Strict scope: env-var/config-file only (no external service); one proof-of-concept gate on an Arc 3 UI feature | null |
| RISK-05 | Release | Design gate required — v3.3 has frontend-visible changes (EPIC-01 position state display, EPIC-02 grace period + stop management UIs); design gate must pass before sprint planning seals | High | Design gate initiated immediately after plan release; UX specs for IT-01/02/03 produced before sprint planning | null |

---

## Integrity Validation — 3.5 Local Model Integrity

**Classification:** Conditional Gate

| Check | Result | Notes |
|-------|--------|-------|
| All S2 items have IDs | ✅ Pass | S2-01 through S2-04 |
| All EPICs have IDs and Maps-to | ✅ Pass | EPIC-01→S2-01, EPIC-02→S2-02, EPIC-03→S2-03, EPIC-04→S2-04 |
| All risks have IDs and relates-to | ✅ Pass | RISK-01 through RISK-05 |
| No scope changes from roadmap | ✅ Pass | IT-01/02/03 from roadmap Priority 3 §5; BLG items from active backlog |
| IT-06 §13 gate respected | ✅ Pass | IT-06 deferred; §13 review noted as gate |
| PT-04 gate respected | ✅ Pass | Deferred — gate not met |
| BLG-FEAT-13 mandatory addressed | ✅ Pass | Included in S2-04 / EPIC-04 |

**Result:** ✅ Pass — model is structured and executable.

---

## Capacity Check

**Effort bands (from inline estimates — scored_initiatives.md has no Arc 3 items):**

| EPIC | Stories | Effort estimate | Sprint |
|------|---------|----------------|--------|
| EPIC-01 | 3 stories (1×data model/migration, 1×backend service, 1×frontend display) | ~3–5 days | Sprint 1 |
| EPIC-02 | 4 stories (2×backend, 2×frontend) | ~4–6 days | Sprint 2 |
| EPIC-03 | 5 stories (spec, QA, governance docs) | ~4–6 days | Sprint 1 |
| EPIC-04 | 5 stories (governance patches, feature, quick wins) | ~3–5 days | Sprint 1–2 |
| **Total** | **17 stories** | **~14–22 days mid-point ~18 days** | **2 sprints** |

**Solo-dev evening/weekend capacity (standard assumption):** ~8–12 days per sprint; ~16–24 days for 2-sprint cycle.

**Mid-point total effort (18 days) vs available capacity (20 days mid-point):** borderline — WARN.

### Phasing Recommendation

The 17-story plan is feasible with careful sprint phasing. Estimated effort (18 days) sits near the top of available capacity (20 days mid-point).

- **Sprint 1 (10 stories):** EPIC-01 (3) + EPIC-03 (5) + EPIC-04 ST-13/14/15 (3) — ~9–13 days estimated
  - EPIC-01 data model + backend + frontend state display (foundation work — must complete early)
  - EPIC-03 spec/QA closure (parallel track, mostly doc/test work — lighter effort per story)
  - EPIC-04 governance patches + BLG-GOV-19 §13 review (autonomous-class governance stories)

- **Sprint 2 (7 stories):** EPIC-02 (4) + EPIC-04 ST-16/17 (2) + EPIC-04 BLG-FEAT-13 (1) — ~7–10 days estimated
  - EPIC-02 grace period + stop management (depends on EPIC-01 complete)
  - EPIC-04 BLG-FEAT-13 mandatory feature flag + quick wins + BLG-FEAT-21/FE-30

**Note:** If Sprint 1 capacity is exceeded, EPIC-04 ST-15 (BLG-GOV-19 §13 review — XS effort) and ST-16 (BLG-FEAT-13 — M effort) can be moved to Sprint 2 without impacting EPIC-01 or EPIC-02 sequencing.

**Capacity gate outcome:** ⚠ WARN — plan is within capacity but tight. Sprint phasing recommendation above must be adopted in sprint planning. Mode = standard: WARN allowed, publish eligible.

---

## Integrity Validation — 5.5 Cross-Stage Integrity

| Check | Result |
|-------|--------|
| Every S2 item has at least one EPIC | ✅ Pass |
| Every EPIC references S2 items | ✅ Pass |
| Every EPIC appears in stage4_backlog_slice.md | ✅ Pass |
| Every RISK has relates-to | ✅ Pass |
| No orphan backlog items (items referenced but not in active backlog) | ✅ Pass |
| IT-01/02/03 roadmap items present as backlog items | ✅ Pass (via Priority 3 roadmap section) |
| BLG-FEAT-13 mandatory flag cross-checked | ✅ Pass — roadmap "mandatory for v3.3" note confirmed |
| "Before v3.3 sprint planning" items in scope | ✅ Pass — all 6 items in EPIC-03 S2-03 |

**Result:** ✅ Pass

---

## Integrity Validation — 5.7 Decision Record Integrity

No Accepted Risk escalations in this cycle. No AR or SRB decision records required.

**Result:** not_applicable ✅
