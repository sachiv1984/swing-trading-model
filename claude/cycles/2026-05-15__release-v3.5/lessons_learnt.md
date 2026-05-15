**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Release:** v3.5
**Cycle:** 2026-05-15__release-v3.5
**Last Updated:** 2026-05-15

---

# Lessons Learnt — Release Planning v3.5

## Planning Phase Observations

### 1. §13 gate as Sprint 1 prerequisite story (first occurrence — new pattern)

**Observation:** For the first time, a formal §13 compliance review is scoped as a Sprint 1 story (ST-01) rather than as a pre-planning gate. Previous cycles either (a) skipped §13 review (features were clearly compliant) or (b) deferred the feature entirely until the gate cleared. Scoping the review as an in-sprint story allows IT-06 to progress without blocking the entire release, while still enforcing the gate before implementation begins.

**Recommendation:** This pattern (§13 review as a Sprint 1 story, gating implementation stories in Sprint 2) should be documented in the execution_prompt.md §13 guidance as the canonical approach for gated arc features. Consider formalising as a "gate story" pattern.

**Action:** Defer — capture in v3.5 lessons_learnt_closure if pattern proves effective. Not an action-now.

### 2. Arc 4 data requirements capture as a prerequisite story (first occurrence)

**Observation:** BLG-GOV-21 (Arc 4 data requirements capture) was promoted from backlog to Sprint 2 ST-04 as a prerequisite for PO-01 implementation. This creates a story that is purely preparatory documentation — not a feature. This is deliberate Arc 4 planning: starting a new arc with a data requirements capture before any implementation reduces mid-arc data model gaps.

**Recommendation:** Document this pattern in roadmap_prompt.md or release_planning_prompt.md for future arcs: "When an arc begins, a data requirements capture story should precede the first implementation story if the arc introduces new data model requirements."

**Action:** Defer to next roadmap rebalance observation. Not an action-now.

### 3. Carry-forward items from v3.4 LL fully scoped (positive observation)

**Observation:** All 7 deferred actions from v3.4 lessons_learnt_closure.md were scoped as explicit stories (ST-11, ST-12, ST-13) in EPIC-04. No carry-forward item was overlooked or parked again. The STEP 0 carry-forward advisory mechanism worked as intended.

**Recommendation:** No change needed — pattern working.

### 4. scored_initiatives.md staleness advisory

**Observation:** `scored_initiatives.md` was last updated 2026-03-31 (8 cycles ago). It contains no entries for Arc 3/4 features (IT-06, PO-01). Effort bands defaulted to inline estimates for all EPICs this cycle.

**Recommendation:** Consider a periodic refresh of `scored_initiatives.md` at each roadmap rebalance (or at each new arc start) to ensure effort band data remains relevant for release planning.

**Action:** File as backlog item at v3.5 post-ship closure if still relevant. Not an action-now.

---

## Action Summary

### Immediate Actions Applied: 0

None.

### Deferred Actions: 1

| # | Action | Source | Owner | Target |
|---|--------|--------|-------|--------|
| 1 | Consider formalising §13 gate pattern as "gate story" in execution_prompt.md or release_planning_prompt.md | LL item #1 above | Head of Specs Team | v3.5 post-ship (if pattern confirmed effective) |

---

## Carry-Forward (for v3.6 Release Planning)

| # | Description | Target | Owner | Notes |
|---|-------------|--------|-------|-------|
| 1 | §13 gate story pattern formalisation (if ST-01 pattern proves effective) | v3.6 release planning or post-ship v3.5 | Head of Specs Team | Conditional on ST-01 outcome |
| 2 | scored_initiatives.md refresh — Arc 3/4 items absent | Next roadmap rebalance | Facilitator | Advisory — no delivery impact |

---

// ARTEFACT_STATUS
```json
{
  "phase": "Release",
  "cycle_id": "2026-05-15__release-v3.5",
  "release": "v3.5",
  "status": "complete",
  "generated_utc": "2026-05-15T00:30:00Z",
  "action_now_count": 0,
  "deferred_count": 1,
  "carry_forward_count": 2
}
```
