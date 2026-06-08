**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v5.2
**Cycle:** 2026-06-08__release-v5.2
**Last Updated:** 2026-06-08

---

# Release Plan — v5.2 Governance Debt, SI-05 Ops & Spec Compliance

## Readiness

**Lifecycle guard:** status = Closed ✅  
**Post-ship preconditions:** post_ship_complete = true, next_cycle_unblocked = true ✅  
**Design gate:** Not required (0 frontend-visible stories; confirmed by design dependency scan)  
**Gate-conditional items:** BLG-FE-64 gate clears 2026-06-21 (13 days); included as conditional in EPIC-04  
**Outstanding advisory:** delivery_verification_prompt.md v3.0 log entry unconfirmed — PMO Lead to verify before sprint planning seals

---

## Scope

### S2 Scope Items — Firm (17)

| S2-ID | Description | Backlog ID | Priority | Effort |
|-------|-------------|------------|----------|--------|
| S2-01 | OA-01: release_planning_prompt.md §-1.2 STEP 8.1 Option(b) accommodation patch | OA-01 (v5.1 D-1) | P1/OA | S |
| S2-02 | OA-02: execution_prompt.md §3.1.A test-authoring spec_references guidance | OA-02 (v5.1 D-2) | P1/OA | S |
| S2-03 | BLG-SPEC-47: Align SI-05 pass_rate computation with BLG-GOV-86 §5.2 | BLG-SPEC-47 | P3* | S |
| S2-04 | BLG-SPEC-48: POST /digest/si05/send API contract gap check and authoring | BLG-SPEC-48 | P1 | XS-S |
| S2-05 | BLG-BE-32: SI-05 Telegram delivery retry and failure handling | BLG-BE-32 | P2 | S |
| S2-06 | BLG-BE-33: SI-05 digest delivery log table (si05_digest_log) | BLG-BE-33 | P2 | S |
| S2-07 | BLG-OPS-55: Deployment runbook update for SI-05 operational environment | BLG-OPS-55 | P2 | XS |
| S2-08 | BLG-OPS-56: SI-05 service scheduled run health check procedure | BLG-OPS-56 | P2 | XS |
| S2-09 | BLG-GOV-97: Claude API model deprecation compliance check | BLG-GOV-97 | P1 | XS |
| S2-10 | BLG-GOV-98: Telegram bot token minimal-permission security review | BLG-GOV-98 | P2 | S |
| S2-11 | BLG-GOV-99: SI-05 digest endpoint authentication review | BLG-GOV-99 | P2 | S |
| S2-12 | BLG-GOV-100: Backend endpoint documentation coverage audit post-v5.1 | BLG-GOV-100 | P2 | S |
| S2-13 | BLG-QA-46: SI-05 digest service edge case test gap analysis | BLG-QA-46 | P2 | XS |
| S2-14 | BLG-QA-47: SI-05 Phase 1 acceptance test protocol | BLG-QA-47 | P2 | S |
| S2-15 | BLG-QA-48: Regression test suite baseline refresh post-v5.1 | BLG-QA-48 | P2 | XS |
| S2-16 | BLG-GOV-94: SI-05 Phase 1 delivery verification protocol | BLG-GOV-94 | P2 | S |
| S2-17 | BLG-GOV-96: SI-05 Phase 1 effectiveness measurement criteria | BLG-GOV-96 | P2 | S |

*BLG-SPEC-47 is P3 severity but must resolve before next SI-05 feature increment (dev deviation DEV-v51-EPIC01-01)

### S2 Scope Items — Conditional (1)

| S2-ID | Description | Backlog ID | Gate | Effort |
|-------|-------------|------------|------|--------|
| S2-18 | BLG-FE-64: BLG-FE-41 Red Flag Journal visual design review pre-brief | BLG-FE-64 | SI-03 live ≥ 30d (2026-06-21) | S |

### Explicitly Deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-GOV-92 (SI-05 Phase 2 activation criteria) | Gate: SI-02 frontend sprint planning ~Nov 2026 | ~Nov 2026 |
| BLG-QA-49 (Arc 5 test scenario completeness) | No active gate; lower priority than v5.2 QA items | Unscheduled |
| BLG-GOV-101 (Governance model complexity assessment) | P2 but requires post-audit analysis; BLG-GOV-79–83 must resolve first | Unscheduled |
| BLG-QA-45 (Arc 5 QA completion criteria definition) | Gate: before BLG-QA-26 sprint planning; not imminent | Unscheduled |
| BLG-FE-65 (SI-05 Telegram-to-app journey map) | P3; no gate condition; lower priority | Unscheduled |
| BLG-GOV-93 (OA-01/02 resolution check procedure) | Absorbed: OA-01 and OA-02 are both firm stories in EPIC-01; procedural check satisfied by their completion | n/a (absorbed) |

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing |
|---------|-------------|-------|----------|-----------|
| EPIC-01 | S2-01, S2-02, S2-03, S2-04 | Head of Specs Team; API Contracts Owner | RISK-01 | Merge last — prompt patches affect engine for subsequent runs |
| EPIC-02 | S2-05, S2-06, S2-07, S2-08 | Backend Engineering Patterns Owner; I&O Owner | RISK-02 | Merge 2nd — BLG-BE-33 migration before OPS-56 health check |
| EPIC-03 | S2-09, S2-10, S2-11, S2-12 | AI Compliance Officer; Cybersecurity Lead; Head of Engineering | RISK-03 | Merge 1st — security reviews must not block other EPICs |
| EPIC-04 | S2-13, S2-14, S2-15, S2-16, S2-17 (+ S2-18 conditional) | Director of Quality; QA & Testing Owner; Product Owner; Head of UX & Design | RISK-04 | Merge 3rd — conditional S2-18 gate must clear before sprint planning seals |

**Merge order:** EPIC-03 → EPIC-02 → EPIC-04 → EPIC-01

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Governance prompt patches affect current engine invocations; any error in prompt text will affect the next governed routine | High | All prompt changes must follow CLAUDE.md §6 checklist (version bump, OPERATIONAL_GUIDE §14 update, prompt_change_log.md entry); Head of Specs Team sign-off required | null |
| RISK-02 | EPIC-02 | BLG-BE-33 introduces a new DB table (si05_digest_log); migration must apply cleanly in both staging and production | Medium | DB migration to be authored with `IF NOT EXISTS` guard; verified in staging before merge; Infrastructure & Operations Owner confirms | null |
| RISK-03 | EPIC-03 | BLG-GOV-99 auth review may identify an authentication gap in POST /digest/si05/send; if unauthenticated, a P2 fix story would be needed | Medium | Auth review produces a finding document first; if gap found, file P2 backlog item and schedule as separate story (not blocking v5.2 merge); Cybersecurity Lead signs off | null |
| RISK-04 | EPIC-04 | BLG-FE-64 conditional story gate clears 2026-06-21; if sprint planning begins before that date, the story may not be scoped | Low | Sprint planning to confirm gate status; if not cleared at planning seal, defer to v5.3; no other EPIC-04 items are gate-conditional | null |

---

## Capacity Check

**Effort Band Lookup (scored_initiatives.md):** No matching items in scored_initiatives.md for v5.2 scope — all items are governance debt or SI-05 ops/security work. Falling back to inline estimates (Tier 3 — no advisory required).

**Per-EPIC effort estimates:**

| EPIC | Stories | Effort estimate (mid-point) |
|------|---------|---------------------------|
| EPIC-01 | 4 | ~2.5 days (1×S OA-01, 1×S OA-02, 1×S BLG-SPEC-47, 1×XS-S BLG-SPEC-48) |
| EPIC-02 | 4 | ~2.5 days (2×S backend + 2×XS ops) |
| EPIC-03 | 4 | ~2.0 days (1×XS + 3×S security/audit reviews) |
| EPIC-04 | 5–6 | ~3.0–3.5 days (1×XS, 3×S, 1×S + 1×S conditional) |
| **Total** | 17–18 | **~10–11 days mid-point** |

**Capacity assessment:** Available capacity is estimated at ~1.5 weeks (7–10 business days) for a standard solo-dev sprint. The 10–11 day mid-point exceeds a single tight sprint. However:
- Many items are documentation/assessment work (not blocked on CI pipelines or external APIs)
- EPIC-04 items (BLG-QA-47, BLG-GOV-94, BLG-GOV-96) are planning documents produceable in parallel with other EPICs
- BLG-GOV-97 (model deprecation check) is XS (~30 min)
- Several items can be batched efficiently (e.g., BLG-OPS-55 + BLG-OPS-56 together)

**Outcome:** WARN — total estimated effort slightly exceeds tight capacity; feasible within 2-week sprint window.

### Phasing Recommendation

| Phase | EPICs | Estimated effort |
|-------|-------|-----------------|
| Sprint 1 (primary) | EPIC-03, EPIC-02, EPIC-04, EPIC-01 | ~10–11 days — single sprint if 2-week window |
| No Sprint 2 required | — | — |

All EPICs are scoped to fit within a standard sprint. The WARN reflects the upper end of estimates; if any EPIC-04 items slip, they can defer to v5.3 without blocking the mandatory P1 items (OA-01, OA-02, BLG-GOV-97, BLG-SPEC-48) which are light XS-S effort.

---

## Integrity Validation — 3.5 Local Model Integrity

| Check | Result | Notes |
|-------|--------|-------|
| All S2 IDs have assigned EPIC | PASS | S2-01→04: EPIC-01; S2-05→08: EPIC-02; S2-09→12: EPIC-03; S2-13→17: EPIC-04; S2-18: EPIC-04 (conditional) |
| EPIC IDs sequential and non-overlapping | PASS | EPIC-01 through EPIC-04 |
| All RISK IDs referenced in table | PASS | RISK-01 through RISK-04 each referenced under EPIC and in risk register |
| Conditional item clearly marked | PASS | S2-18 / EPIC-04 conditional with explicit gate condition |
| No S2 item appears in multiple EPICs | PASS | Each S2 item mapped to exactly one EPIC |
| Deferred items listed | PASS | 6 items explicitly deferred with rationale |
| Release is v5.2 and is on roadmap Now horizon | PASS | RA:v5.2 section present in current_roadmap.md §3 |

**Model integrity: PASS**

---

## Cross-Stage Integrity — 5.5

| Check | Result | Notes |
|-------|--------|-------|
| All S2 IDs in scope section map to EPICs in execution plan | PASS | S2-01→18 all mapped |
| All EPIC IDs in backlog slice match stage3 execution plan | PASS | EPIC-01 through EPIC-04 consistent |
| All RISK IDs referenced in EPIC table appear in Risk Register | PASS | RISK-01 through RISK-04 all in register |
| No orphaned references | PASS | |
| Decisions record present | PASS | docs/product/decisions/decisions--2026-06-08__release-v5.2.md |
| All AR/SRB records exist | PASS | No escalations in this cycle |
| Scope document present | PASS | docs/product/scope/scope--2026-06-08__release-v5.2-govdebt-si05ops.md |

**Cross-stage integrity: PASS**
**Decision record integrity: PASS (no escalations; decisions record present)**
