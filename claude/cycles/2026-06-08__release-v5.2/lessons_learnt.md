**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Release:** v5.2
**Cycle:** 2026-06-08__release-v5.2
**Filed:** 2026-06-08

---

# Lessons Learnt — Release Planning v5.2

**Phase:** Release
**Invoking routine:** release_planning_prompt.md v2.33
**Prior cycle carry-forwards:** 2 (from 2026-06-21__release-v5.1 — both addressed in scope)

---

## Carry-Forward Resolution

| Carry-Forward Item | Status | How Resolved |
|-------------------|--------|-------------|
| CF-1: STEP 8.1 Option(b) §-1.2 ambiguity (LL-RP-v5.1-01) | RESOLVED IN SCOPE | OA-01 (ST-01, EPIC-01) explicitly included as firm story; Head of Specs Team will patch §-1.2 in this sprint |
| CF-2: Test-authoring spec_references guidance (v5.1 D-2) | RESOLVED IN SCOPE | OA-02 (ST-02, EPIC-01) explicitly included as firm story; guidance will be added to execution_prompt.md §3.1.A |

Both carry-forwards from v5.1 are now assigned story IDs and scoped into EPIC-01. The carry-forward pattern is working as designed.

---

## Release Planning Phase Observations

### Scope assembly was efficient
The 2026-06-07 roadmap rebalance (DL-039) pre-populated 25 new backlog items specifically targeting v5.2. This significantly accelerated scope identification — most of the 17 firm stories were directly from that rebalance, requiring only sequencing decisions at release planning time. The Provisional-Target field pattern is working well.

### BLG-GOV-93 absorption avoids redundancy
BLG-GOV-93 (OA-01/02 enforcement procedure) was appropriately absorbed into the EPIC-01 scope rather than creating a separate story. When the OAs themselves are sprint stories, the "check procedure" is redundant. This absorption pattern may be useful in future cycles when OA-tracking backlog items collide with the OA-execution stories themselves.

### Prompt change log advisory recurred
STEP -1.7 flagged delivery_verification_prompt.md v3.0 as potentially missing a prompt_change_log.md entry (from v5.1 ST-03). This is the same class of issue that BLG-GOV-79 and BLG-GOV-80 were designed to prevent. The execution_prompt.md v3.36 structural check (BLG-GOV-80) should have auto-added this entry during v5.1 execution. PMO Lead should verify before sprint planning seals. If confirmed missing, patch in same commit as OA-01/OA-02 work in EPIC-01.

### Capacity WARN is expected for governance debt sprints
v5.2 has 17 firm stories but most are XS-S effort governance documents, assessments, and security reviews. The WARN outcome (10–11 day mid-point vs ~7–10 day tight capacity) is appropriate to flag but does not require phasing — many items can be produced in parallel as they are documentation-only. This is a known characteristic of governance debt sprints.

---

## Items for Deferred Action

| # | Item | File | Section | Change | Owner | Target |
|---|------|------|---------|--------|-------|--------|
| D-1 | Verify delivery_verification_prompt.md v3.0 entry in prompt_change_log.md; patch in ST-01 or ST-02 commit if missing | prompt_change_log.md | — | Append v2.9→v3.0 entry if absent | PMO Lead + Head of Specs Team | v5.2 EPIC-01 (before sprint planning seals) |

---

// ARTEFACT_STATUS
{
  "phase": "Release",
  "cycle_id": "2026-06-08__release-v5.2",
  "release": "v5.2",
  "status": "Published",
  "scope_items": 18,
  "scope_items_firm": 17,
  "scope_items_conditional": 1,
  "epics": ["EPIC-01", "EPIC-02", "EPIC-03", "EPIC-04"],
  "design_gate_required": false,
  "capacity_check": "warn",
  "open_escalations": 0,
  "publish_utc": "2026-06-08T00:10:00Z"
}
