**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-05-25
**Cycle:** 2026-05-25__scheduled

---

# Lessons Learnt — 2026-05-25__scheduled

**Invoking routine:** roadmap_prompt.md v6.5
**Cycle:** 2026-05-25__scheduled
**Phase:** Roadmap
**Prior cycle:** 2026-05-22__scheduled

## Summary

| Friction count | Deferred patches | Action-now items |
|---------------|-----------------|-----------------|
| 4 | 0 | 2 |

---

## Meta-Review

**rebalance_cycles_since_meta_review:** 3 — **META-REVIEW DUE.**

**Meta-review procedure** (per roadmap_prompt.md §11 — Type D pattern check):

The meta-review at cycle 3 reviews whether any recurring pattern across the last 3 rebalance cycles indicates a systemic issue requiring a governance prompt change.

**Cycles reviewed:** 2026-05-19__scheduled, 2026-05-22__scheduled, 2026-05-25__scheduled

**Pattern analysis:**

| Pattern | Frequency | Assessment |
|---------|-----------|-----------|
| Spec debt from shipped endpoints accumulates as backlog items | 2/3 cycles (v4.0 produced BLG-SPEC-38/39/40 retroactively, similar to v3.8/v3.9 producing BLG-SPEC-33/34) | **Systemic** — API contract same-sprint rule (BLG-GOV-55) directly addresses this. No prompt change required — BLG-GOV-55 is the fix. |
| Now horizon empty at rebalance | 3/3 cycles | Not a pattern issue — expected at post-ship scheduled rebalances. No action. |
| CPS tier discrepancy (run_manifest classifies tier before CPS is computed) | 1/3 cycles (this cycle only) | Isolated — CPS computation happens at STEP 2, after tier is recorded in STEP 1 run_manifest. Low frequency; deferred patch not warranted. Record as Friction #4. |
| Ideas with high rejection rate due to duplication | 2/3 cycles (4 duplicates this cycle, 2 in 2026-05-22) | Moderate — indicates idea pool is generating tracking-what-exists ideas rather than novel suggestions. Advisory only — not a prompt change candidate; monitor at next meta-review. |

**Meta-review outcome:** No systemic issues requiring governance prompt changes identified. Spec debt pattern is addressed by BLG-GOV-55 (action-now item). All other patterns are either expected or low frequency. Meta-review COMPLETE.

**rebalance_cycles_since_meta_review → reset to 0.**

---

## Recurrence Check (against 2026-05-22__scheduled lessons_learnt.md)

| Prior friction | Recurrence? | Status |
|---------------|-------------|--------|
| Friction #1: P1 spec debt from shipped features (BLG-SPEC-33/34) | Yes — 2nd recurrence (BLG-SPEC-38/39/40 this cycle) | **Recurrence confirmed.** BLG-GOV-55 (API contract same-sprint rule) directly addresses this. OA-01 this cycle. |
| Friction #2: SI-05 scope ambiguity | Resolved — SI-05 phased delivery formally scoped this cycle (BLG-GOV-54) | Not recurring. |

---

## Frictions

### Friction #1 (Type B — 2nd recurrence): API contract spec debt from shipped features

**Observed:** Three P1 spec debt items created this cycle (BLG-SPEC-38 Gemini thesis endpoint, BLG-SPEC-39 SI-02 data model gap, BLG-SPEC-40 Arc 5 analytics endpoint). Both BLG-SPEC-38 and BLG-SPEC-40 represent endpoints shipped in v4.0 without formal API contract documents — the same pattern as BLG-SPEC-33/34 from the prior cycle.

**Root cause:** No governance rule requires an API contract document in the same sprint as a new endpoint. CLAUDE.md §2 requires openapi.yaml entry in the same commit, but not a docs/specs/api_contracts/ document. Sprint planning does not enforce contract authoring as part of story acceptance criteria.

**Blast radius:** If uncaught: each sprint accumulates spec debt backlog items that must be addressed before the next sprint planning. At 2 per sprint, this generates 10+ retroactive spec debt items per Arc. Audit scores decline on spec completeness dimension.

**Recommendation:** BLG-GOV-55 (API contract same-sprint delivery rule) directly addresses this. Should be actioned before v4.1 sprint planning seals. This is OA-01 below.

**Owner:** Head of Specs Team

**Status:** Action-now — see OA-01.

---

### Friction #2 (Type C): Strategy Drift Alert triggered; CPS = 2.69

**Observed:** CPS computed at 2.69 — above the 2.5 absolute threshold. Strategy Rules & System Intent Owner acknowledged the alert and confirmed all SPS-4 initiatives remain within §13 bounds. No strategic deviation found — the elevated CPS reflects the correct arc sequence moving toward more complex AI-adjacent features.

**Root cause:** CPS naturally increases as the roadmap advances toward Arc 5/6 features, which have higher SPS scores due to §13 adjacency. This is expected, not a governance failure.

**Blast radius:** If unacknowledged: AI-adjacent features could enter sprint planning without Strategy Rules & System Intent Owner sign-off. The alert mechanism is functioning correctly.

**Recommendation:** No governance change required. Monitor CPS at each rebalance; document trend in next scored_initiatives.md refresh. CPS is expected to remain in the 2.5–3.0 range through Arc 5 completion.

**Owner:** Strategy Rules & System Intent Owner

**Status:** Resolved this cycle. Advisory carry-forward only.

---

### Friction #3 (Type A): Idea duplication rate elevated (4 of 44 rejected as duplicates)

**Observed:** 4 ideas rejected as not-strong duplicates: challenger-02 (duplicate BLG-GOV-33), head-of-engineering-02 (duplicate BLG-OPS-29), qa-lead-01 (duplicate BLG-QA-27), head-of-ux-01 (duplicate BLG-FE-42). All four referenced existing tracked backlog items. Similarly, 2 ideas were rejected as duplicates in the prior cycle.

**Root cause:** Agents submitting ideas do not have visibility into the current backlog before generating submissions. IW-20260525-01 window did not surface the existing BLG items as reference. No pre-window backlog summary was provided.

**Blast radius:** Wasted idea generation effort; STEP 5 debate queue could become inflated with well-intentioned but redundant ideas. At 4 duplicates per 44 ideas (9% rate), this is not yet a critical issue.

**Recommendation:** Advisory only. Consider including a "recent backlog adds" summary in the idea intake context at the next window opening. No prompt change warranted at this frequency.

**Owner:** PMO Lead

**Status:** Deferred — advisory. No prompt change. Monitor at next meta-review.

---

### Friction #4 (Type C): Run tier discrepancy — CPS computed after tier recorded in run_manifest

**Observed:** Run tier was recorded as "Standard" in run_manifest.md (written at STEP 1, before STEP 2 CPS computation). CPS computed at STEP 2 = 2.69, which satisfies the Extended tier condition (CPS ≥ 2.5 absolute). The run should have been classified Extended but was not retroactively updated.

**Root cause:** Tier is determined at STEP 0.C before STEP 2 SPS scoring. At STEP 0.C, the prior cycle CPS was not recorded in the 2026-05-22__scheduled cycle_record (it also lacked SPS/CPS scoring). The tier decision at STEP 0.C had no CPS to evaluate.

**Blast radius:** Low — all Extended-tier obligations were fulfilled in practice (full STEP 2.3 horizon review, full STEP 5 debate, full workforce economics). The discrepancy is documentary only, not a process failure.

**Recommendation:** Head of Specs Team should add guidance to roadmap_prompt.md STEP 0.C that if prior cycle CPS is unavailable, run a preliminary SPS assessment before finalising tier. Deferred (no immediate sprint impact).

**Owner:** Head of Specs Team

**Status:** Deferred — low blast radius; addressed as advisory. Patch deferred to BLG-GOV-56 scope consideration.

---

## Action-Now Items (STEP 11)

### OA-01: Action BLG-GOV-55 — API contract same-sprint delivery rule before v4.1 sprint planning

**Owner:** Head of Specs Team
**Due:** Before v4.1 sprint planning seals

BLG-GOV-55 (API contract same-sprint delivery rule — CLAUDE.md §2 amendment) is a P1 governance item directly addressing the 2nd-recurrence spec debt pattern. Must be actioned before v4.1 sprint planning to prevent BLG-SPEC-38/39/40-type debt from recurring in v4.1.

**Scope:**
- Add to CLAUDE.md §2: "Every new `## METHOD /path` endpoint added to a file in `backend/routers/` must have a corresponding API contract document in `docs/specs/api_contracts/` in the same sprint. This complements the same-commit openapi.yaml requirement."
- Per CLAUDE.md §6: bump CLAUDE.md version; verify OPERATIONAL_GUIDE.md §14 reference; append prompt_change_log.md if applicable.

**Head of Specs Team sign-off required before applying.**

---

### OA-02: Address spec debt BLG-SPEC-38 and BLG-SPEC-40 before v4.1 sprint planning

**Owner:** API Contracts Documentation Owner
**Due:** Before v4.1 sprint planning seals

BLG-SPEC-38 (Gemini thesis endpoint API contract) and BLG-SPEC-40 (Arc 5 analytics endpoint API contract) are P1 spec debt items from v4.0. SI-02 and future Arc 5 work will reference both endpoints; contracts must exist before sprint planning seals to prevent implementation confusion.

**Scope:**
- Author `docs/specs/api_contracts/gemini_thesis_generation.md` for `POST /trade-plans/{plan_id}/generate-thesis`
- Author `docs/specs/api_contracts/arc5_compliance_analytics.md` for `GET /analytics/arc5-compliance`
- Both must be registered in `docs/reference/openapi.yaml` per CLAUDE.md §2
- Gate for BLG-SPEC-38: BLG-SPEC-33 (SI-03 contract) must be closed first

---

## Deferred Patches

None. Friction items are addressed via backlog items or advisory only. No governance prompt changes applied this cycle.

---

## Carry-Forward Advisory (from this cycle)

| # | Item | Owner | Implication |
|---|------|-------|-------------|
| 1 | OA-01: BLG-GOV-55 (API contract same-sprint rule) | Head of Specs Team | P1 — must action before v4.1 sprint planning |
| 2 | OA-02: BLG-SPEC-38 + BLG-SPEC-40 spec debt | API Contracts Documentation Owner | P1 — must action before v4.1 sprint planning |
| 3 | CPS elevation (2.69) — §13 adjacency increasing | Strategy Rules & System Intent Owner | Advisory — monitor at each rebalance; §13 acknowledgement required at each run |
| 4 | Idea duplication rate 9% | PMO Lead | Advisory — consider backlog summary in next idea intake window |
| 5 | OA-01 from v4.0 closure (OA-04: pr_number null guard) | Head of Specs Team | Carry-forward from v4.0; BLG-GOV-40 tracks this |
| 6 | OA-02 from v4.0 closure (OA-03: sprint_close_reminder.yml) | PMO Lead | Carry-forward from v4.0; BLG-GOV-41 tracks this |
