Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v3.7
Cycle: 2026-05-18__release-v3.7
Last Updated: 2026-05-18

---

# Release Plan — v3.7 Signal-to-Watchlist Workflow + Arc 2 Completion + Governance Hardening

## Readiness

**Prior cycle:** 2026-05-16__release-v3.6 — Closed_with_actions (verified 2026-05-17)
**Next release preconditions:** post_ship_complete=true ✅ next_cycle_unblocked=true ✅

**Arc status at planning:**
- Arc 1 (Stock Discovery): ✅ Complete (v3.1)
- Arc 2 (Pre-Trade Research): PT-01/02/03/05 complete; PT-04 (Setup Quality Score) deferred from v3.6 — gate: 20+ closed trades (Product Owner must confirm)
- Arc 3 (In-Trade Risk Management): ✅ Complete (v3.3–v3.5)
- Arc 4 (Post-Trade Intelligence): PO-01 complete (v3.5–v3.6); PO-02/03/04 gated on data density — PO-02 requires 6+ months of AI-summarised journal entries (AI Journal live ~1 month since v2.8 2026-04-20 — gate NOT met)
- Arc 5/6: Horizon

**Deferred patches carried from v3.6:** 5 items (3 execution_prompt.md + 1 qa_evidence_template.md + 1 PMO enforcement) — all included in S2-03/S2-04 scope.

**Backlog age advisory:** BLG-FE-27 (nav bar redesign, 3+ cycles without story) — not included, Provisional-Target: Arc 3.
**Provisional-Target advisory:** 4 items carry `Provisional-Target: v3.7` — all in scope.
**Design dependency scan:** 3 items flagged (BLG-FE-33, BLG-FE-34, PT-04) — design gate required.

## Scope

| S2-ID | Description | Source items | Priority |
|-------|-------------|--------------|----------|
| S2-01 | Signals-to-Watchlist workflow improvement — replace Add Position CTA with Add to Watchlist on signal cards; trade plan form signal context panel | BLG-FE-33, BLG-FE-34 | P1 |
| S2-02 | Arc 2 Completion — PT-04 Setup Quality Score (conditional: 20+ closed trades gate) | PT-04 | P2 (conditional) |
| S2-03 | Governance hardening patches (deferred from v3.6 lessons) — execution_prompt.md ×3 + qa_evidence_template.md ×1 | LL-v3.6 items 1/2/4/5 | P1 (process) |
| S2-04 | Technical debt clearance — database stub conftest, pycache git hygiene, Research page font staging, scored_initiatives.md refresh | BLG-QA-20, BLG-OPS-16, BLG-FE-35, BLG-GOV-23 | P2–P3 |

**Items explicitly deferred:**
- BLG-FE-27 (nav bar redesign): P3 design exploration, no blocking workflow — deferred to Arc 3/4 context
- PO-02/03/04 (Arc 4 pattern recognition / behavioural taxonomy / reflection correlation): Data density gates not met — PO-02 requires 6+ months AI journal (1 month available); deferred to v3.8+
- BLG-FEAT-20 (net-of-costs performance): Arc 3/4 data model context — deferred
- BLG-OPS-13 (API performance baseline re-run): Requires live staging environment — deferred
- S2-02 EPIC-02 conditional defer: If Product Owner does not confirm 20+ closed trades at design gate, EPIC-02 defers to v3.8

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Head of Engineering | RISK-02 (BLG-FE-34 depends on BLG-FE-33) | None — independent |
| EPIC-02 | S2-02 | Head of Specs Team + Head of Engineering | RISK-01 (PT-04 gate not confirmed) | Gate check required before sprint planning seals |
| EPIC-03 | S2-03 | Head of Specs Team + Director of Quality | RISK-03 (prompt_change_log gaps) | None — independent |
| EPIC-04 | S2-04 | Head of Engineering + QA & Testing Owner + Facilitator | None | Smallest EPIC — merge first |

**EPIC-01 note:** BLG-FE-34 (signal context panel in trade plan form) depends on BLG-FE-33 (signals → watchlist) because the signal → watchlist linkage is required to pass signal data through to the trade plan form. BLG-FE-33 backend (ST-01) + frontend (ST-02) must complete before BLG-FE-34 (ST-03) begins within the same EPIC.

**EPIC-02 note:** Product Owner must confirm 20+ closed trades before sprint planning seals. If not confirmed at design gate, EPIC-02 defers to v3.8 and sprint scope shrinks to 8 stories across EPICs 01/03/04.

**Merge order:** EPIC-04 → EPIC-03 → EPIC-01 → EPIC-02

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-02 | PT-04 gate (20+ closed trades) not confirmed before sprint planning seals — entire EPIC-02 defers to v3.8 | High | Product Owner gate confirmation at design gate; pre-sprint required decision | null |
| RISK-02 | EPIC-01 | BLG-FE-34 depends on BLG-FE-33 completing first — sequential dependency within EPIC creates delivery risk if BLG-FE-33 has unexpected complexity | Medium | BLG-FE-33 split into backend (ST-01) and frontend (ST-02) stories to allow parallel spec work; BLG-FE-34 starts only after ST-02 merged | null |
| RISK-03 | EPIC-03 | Prompt change log gaps (v3.18→v3.22 execution_prompt.md + 2 others) need retroactive entries — scope risk if entries require authority sign-off per missing records | Low | Retroactive entries are advisory-only additions; no authority gate for historical documentation | null |

## Capacity Check

**Estimation (Tier 3 inline inference — no scored_initiatives.md rows for v3.7 items):**

| EPIC | Stories | Effort estimate | Hours (mid) |
|------|---------|----------------|-------------|
| EPIC-01 | ST-01 (M), ST-02 (M), ST-03 (M) | 3 × M | ~6 days |
| EPIC-02 | ST-04 (XS), ST-05 (M), ST-06 (M) | 1 × XS + 2 × M | ~4 days (conditional) |
| EPIC-03 | ST-07 (S), ST-08 (S) | 2 × S | ~1 day |
| EPIC-04 | ST-09 (S), ST-10 (XS+XS), ST-11 (S) | 2 × S + 2 × XS | ~1.5 days |

**Without EPIC-02:** ~8.5 days (~1.5 sprints)
**With EPIC-02:** ~12.5 days (~2.5 sprints)

**Assumption:** Standard solo-dev capacity (~5 days/sprint).

### Phasing Recommendation

**WARN:** Total estimated effort with EPIC-02 (~12.5 days) exceeds 2-sprint capacity (~10 days). Recommended phasing:

- **Sprint 1:** EPIC-04 (1.5 days) + EPIC-03 (1 day) + EPIC-01 (6 days) = ~8.5 days — fits comfortably
- **Sprint 2:** EPIC-02 (4 days conditional) — fits with margin if gate confirmed; omit if gate not met

This phasing matches the merge order (EPIC-04 → EPIC-03 → EPIC-01 → EPIC-02) and front-loads the high-value P1 user-facing work.

**Capacity check outcome:** WARN (total with EPIC-02 slightly over 2 sprints; standard mode — may proceed with phasing recommendation)

## Integrity Validation — 3.5 Local Model Integrity

**S2 → EPIC mapping check:**
- S2-01 → EPIC-01 ✅
- S2-02 → EPIC-02 ✅
- S2-03 → EPIC-03 ✅
- S2-04 → EPIC-04 ✅

**EPIC → Risk mapping:**
- EPIC-01 → RISK-02 ✅
- EPIC-02 → RISK-01 ✅
- EPIC-03 → RISK-03 ✅
- EPIC-04 → no risk (low-complexity debt items) ✅

**Dependency check:**
- BLG-FE-34 dependency on BLG-FE-33 captured in EPIC-01 note and RISK-02 ✅
- EPIC-02 gate dependency captured in RISK-01 and Pre-sprint Required Decisions ✅

**Model integrity result:** ✅ Pass — all S2 items map to EPICs, all EPIC risks registered, dependency chain complete.
