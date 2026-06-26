**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-06-26__scheduled
**Last Updated:** 2026-06-26

---

# Lessons Learnt — Roadmap Rebalance 2026-06-26__scheduled

---

## Friction Items

### FI-1 — velocity_metrics.md path discrepancy persists across two rebalance cycles

**Observed:** The deferred patch from 2026-06-24__scheduled specified creating `claude/roadmap/velocity_metrics.md`. The post-ship closure (2026-06-25) created the file at `claude/cycles/velocity_metrics.md` instead — a path deviation from the specification. This discrepancy was still present at this rebalance (2 cycles after filing).

**Impact:** The roadmap_prompt.md STEP 1.1 reads velocity metrics from `claude/roadmap/velocity_metrics.md`. The actual data is at `claude/cycles/velocity_metrics.md`. Every future roadmap run must handle this discrepancy manually, or the velocity data may be inaccessible.

**Resolution required:** Move `claude/cycles/velocity_metrics.md` to `claude/roadmap/velocity_metrics.md` and update any references. This is a Class 3 operational record — move requires no governance approval (non-sealed, non-canonical spec file).

**Action:** Deferred patch — resolve at next `run post-ship` closure or as a standalone governance commit before v6.3 planning.
- **Owner:** Infrastructure & Operations Owner
- **Target:** Before `plan release v6.3`
- **Action type:** Deferred patch (carry-forward)

---

### FI-2 — 44-idea intake window with 22 agents produces decision load that compresses STEP 5 debate quality

**Observed:** IW-20260626-01 had 44 submissions from 22 agents (vs 9 agents in prior window). Processing 44 ideas through STEP 4.1 classification and 14 advancing ideas through STEP 5 structured debate is feasible but produces a compressed debate record — each debate is necessarily shorter than in lower-volume windows.

**Impact:** Advisory only. The structured debate still covers the key PO required case, Challenger counter-argument, and outcome for each advancing idea. However, edge cases and secondary considerations receive less analysis time.

**Recommendation:** No change to intake window scope at this time. If STEP 5 debate quality degrades further in future windows (e.g., 25+ advancing ideas), consider raising the Advance threshold or adding a pre-STEP 5 filtering step.

- **Owner:** PMO Lead
- **Target:** Advisory only — monitor over next 2 rebalances
- **Action type:** Advisory observation (no action required)

---

## Carry-Forward from Prior Cycles

### FI-P3-01 — Playwright strict mode advisory to Base44 prompt draft §6 (from v6.2 closure)
- **Owner:** Director of Quality
- **Target:** v6.3
- **Status:** Carry-forward — not yet actioned

### FI-P3-02 — Frontend testing gate clarification (code review vs staging for wording-only ACs) (from v6.2 closure)
- **Owner:** Head of Specs Team
- **Target:** v6.3
- **Status:** Carry-forward — not yet actioned

### FI-P4-01 — CI/infra spec_references convention to execution_prompt.md §3.1.A (from v6.2 closure)
- **Owner:** Head of Specs Team
- **Target:** v6.3
- **Status:** Carry-forward — not yet actioned

**Note:** FI-P3-01, FI-P3-02, FI-P4-01 are advisory pre-planning items for v6.3. They should be addressed at `plan release v6.3` and `run design-gate v6.3` as applicable.

---

## STEP 11.4 — Meta-Review

**Trigger:** 3rd cycle since last meta-review (2026-06-17__scheduled). Threshold reached per DL-056 note ("incremented to 3 in state → due at next rebalance"). Meta-review IS due this run.

**Meta-review period:** 2026-06-17__scheduled → 2026-06-26__scheduled (3 rebalance cycles reviewed)

**Cycles reviewed:**
1. 2026-06-17__scheduled (DL-053 — Standard, 13 ideas, 1 net initiative change)
2. 2026-06-22__scheduled (DL-054/055 — Standard, 9 ideas, 0 net roadmap changes)
3. 2026-06-24__scheduled (DL-056 — Standard, 8 ideas terminal cycle; 4 backlog additions; Skill-Silo + PVR alerts)
4. 2026-06-26__scheduled (this run — DL-057 — Standard, 44 ideas; 25 backlog additions)

---

### Meta-Review Findings

**MRF-1 — Product Value Ratio trend is improving but pattern of D/G sprint work is structural**

Over the 3-cycle review period, the PVR improved significantly: 0.136 → 0.209 → 0.37. The trajectory is correct. However, all three "Alert" or "Advisory" signals occurred because G+D+P work was systematically included in sprints rather than being incrementally prioritised alongside U work. The v6.2 sprint (9/13 U stories) demonstrates the discipline is achievable. The root pattern: governance debt (prompt patches, CI improvements, QA scaffolding) accumulates between cycles and then gets included in bundles when the signal fires. No structural change recommended — the PVR mechanism is working as designed.

**Rating:** No action required. Advisory monitoring continues.

---

**MRF-2 — Skill-Silo alert recovery is tracking to target**

Skill-Silo metric (G+D+P%) over the 3-cycle review period: 72.7% (v6.0) → 55.6% (v6.1) → 30.8% (v6.2). Rolling 3-cycle average at this meta-review: 51.5% (still above 40% ceiling but tracking downward). The mechanism is working. v6.2's strong U-story emphasis pulled the ratio down significantly. v6.3 will need similar U-emphasis to clear the ceiling.

**Rating:** No action required. Skill-Silo alert remains active; trajectory is correct.

---

### FI-META-01 — roadmap_prompt.md: velocity_metrics.md canonical path not enforced at STEP 1.1

**Identified during meta-review:** The roadmap_prompt.md STEP 1.1 instruction reads "read `claude/roadmap/velocity_metrics.md`" but the file was created at `claude/cycles/velocity_metrics.md` at post-ship closure. The prompt does not include a fallback path search — if the file is not at the canonical location, no error is surfaced; the engine proceeds without velocity data.

**Proposed change:** Add to roadmap_prompt.md STEP 1.1: "If `claude/roadmap/velocity_metrics.md` does not exist, also check `claude/cycles/velocity_metrics.md`. If found at the alternative path, record a path-deviation warning in the run_manifest and flag the discrepancy as a friction item."

**Owner:** Head of Specs Team
**Target:** v6.3 (as a §6 governance checklist prompt patch)
**Action type:** Deferred prompt patch

---

### FI-META-02 — ideas_intake_prompt.md: full-window expansion (22 agents) produces large STEP 5 debate load

**Identified during meta-review:** STEP -1.6 inline trigger in roadmap_prompt.md opens an intake window when `open_ideas_count < 20`. When the trigger fires after a large-scale intake (22 agents), the resulting 44-idea pool creates a significantly larger STEP 4 and STEP 5 workload than the 9-agent windows that preceded it. The STEP -1.6 trigger has no mechanism to anticipate the expanded window scope.

**Proposed change:** None structural — the expanded window provides genuine idea diversity value. However, roadmap_prompt.md STEP -1.6 should include a note: "When the inline window produces >30 submissions, budget additional context depth for STEPs 4 and 5. If advancing idea count exceeds 15, prioritise advancing only the highest-scoring ideas (per STEP 6 criteria) and park the remainder."

**Owner:** PMO Lead
**Target:** v6.3 (as a §6 governance checklist prompt patch)
**Action type:** Deferred prompt patch

---

## Meta-Review Reset

**Meta-review cycle count reset to 0.** Next meta-review due after 3 further rebalances.
