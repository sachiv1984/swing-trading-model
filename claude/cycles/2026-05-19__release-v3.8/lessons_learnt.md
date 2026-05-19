**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-05-19__release-v3.8
**Release:** v3.8
**Generated:** 2026-05-19

---

# Release Planning Lessons Learnt — v3.8

---

## What Went Well

1. **Scored initiatives alignment** — scored_initiatives.md (BLG-GOV-23, v3.7 ST-11) provided clear prioritisation signal for v3.8 scope selection. SI-01 was the obvious primary choice (SPS=4, highest unshipped item). No scoring disputes.

2. **Provisional-Target tracking** — 5 backlog items already carried `Provisional-Target: v3.8` (added in 2026-05-19 session by user). Release planning consumed them directly without needing to re-evaluate scope from scratch.

3. **Carry-forward closure** — v3.7 lessons_learnt_closure.md carry-forward items were properly surfaced in the run manifest advisory. PT-04 gate decision (carry-forward item #1) converted to Pre-sprint Planning Required Decision with clear deadline.

4. **§13 gate pattern established** — the delegated_decision gate story pattern (established v3.5 IT-06; encoded in execution_prompt.md v3.22) is well-understood and applied cleanly for SI-01 in EPIC-01.

---

## Improvement Areas

1. **PT-04 third conditional include** — this is the third consecutive release carrying PT-04 as conditional scope (v3.6, v3.7, v3.8). If gate is not confirmed by 2026-05-22, Product Owner should park PT-04 formally rather than carrying it a fourth time — it creates noise in planning and sprint planning pre-checks.

2. **BLG-FEAT-22/23/24/BLG-FE-36 arrived mid-session** — four of the ten stories were backlog items added by the user in the same session as release planning. Future consideration: if ideas are ready to add to the backlog, adding them before running `plan release` allows the advisory checks (Provisional-Target, design dependency) to operate on a stable set of candidates.

---

## Action Items

| # | Action | Type | Owner | Target cycle |
|---|--------|------|-------|-------------|
| 1 | If PT-04 gate not met by 2026-05-22: formally park PT-04 as "pending gate" in backlog.md with park rationale — do not carry as conditional a fourth time | Decision | Product Owner | v3.8 sprint planning |
| 2 | Review smoke-tests.yml timeout if CI timeout recurs on any v3.8 PR | Advisory (if triggered) | QA & Testing Owner | v3.8 execution |

---

// ARTEFACT_STATUS
{
  "phase": "Release",
  "cycle_id": "2026-05-19__release-v3.8",
  "status": "complete",
  "generated_utc": "2026-05-19T08:20:00Z"
}
