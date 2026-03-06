# Lessons Learnt — Release Planning v1.9

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-03-06__release-v1.9
**Release:** v1.9
**Last Updated:** 2026-03-06

---

## LL-v1.9-01 — Spec debt accumulation risk

**Observation:** 10 spec/documentation debt items (S2-21–S2-30) were included in scope, with 3 items (G1, G2, G5) open since 2026-02-21 — three release cycles. In each prior release, these items were noted but not assigned a sprint story.

**Impact:** Items not assigned story IDs do not enter sprint planning. They remain advisory forever until explicitly storied.

**Recommendation:** In future release planning cycles, any spec debt item aged >2 cycles should be automatically promoted to a sprint story (as was done here with ST-16–ST-19). The release planning engine should check backlog item age and flag items that have been in the backlog for 2+ prior release cycles without a story assignment.

**Action:** Head of Specs Team to add a backlog age check to the release planning STEP 1 advisory checklist in the next prompt version. Target: prompt v2.9.

---

## LL-v1.9-02 — Capacity advisory should include phasing recommendation

**Observation:** Stage 4.5 produced a WARN (capacity advisory) noting ~90 hours of estimated work vs ~10–15 hrs/week available. The advisory was correct but the WARN outcome does not trigger a concrete action — it only informs.

**Impact:** Without an explicit phasing recommendation in the backlog slice, sprint planning may attempt all 6 EPICs simultaneously and underestimate the risk.

**Recommendation:** When Stage 4.5 issues a WARN, the cycle summary should include an explicit phasing recommendation (e.g., "Phase 1: EPIC-04 + EPIC-05; Phase 2: EPIC-01 + EPIC-02 + EPIC-03 + EPIC-06"). This recommendation was included informally in cycle_summary.md §6 but not as a formal advisory in stage4_5_capacity_check.md.

**Action:** PMO Lead to add a "Phasing Recommendation" section to stage4_5_capacity_check.md template in the next prompt version when WARN condition is triggered.

---

## LL-v1.9-03 — RISK-06 (drawdown spec alignment) is a sprint planning gate, not a release planning gate

**Observation:** RISK-06 (ST-06: drawdown data source) was correctly classified as High priority but not escalated (standard mode advisory). However, this risk has a concrete "must resolve before sprint planning seal" requirement that is easy to lose track of.

**Recommendation:** Add a "Pre-sprint planning required decisions" section to cycle_summary.md for any High-priority risk that has a "must resolve before sprint planning seal" disposition. This creates an explicit checklist for the sprint planning engine to consume at its preflight step.

**Action:** PMO Lead to add this section to cycle_summary.md template. Applicable here: ST-06 must resolve before sprint plan seals.

---

## LL-v1.9-04 — S2-12 and ST-06 alignment: spec-only story items improve traceability

**Observation:** ST-06 (drawdown data source alignment) is a documentation-only story item with no code change. Including it as a numbered story item (rather than an EPIC pre-condition note) meant it got an acceptance criterion, an owner, a clear definition of done, and a place in the sprint sequence.

**Positive lesson:** Giving documentation decisions a story ID improves traceability and reduces the risk of them being skipped at sprint time.

**Recommendation:** Reinforce in sprint planning prompt: spec alignment / documentation decisions that are prerequisites to verification should always have a story item, not just an EPIC note.

---

## Summary

| LL ID | Theme | Actionable? | Owner | Target |
|-------|-------|------------|-------|--------|
| LL-v1.9-01 | Backlog age check for spec debt | Yes | Head of Specs Team | Prompt v2.9 |
| LL-v1.9-02 | Capacity WARN phasing recommendation | Yes | PMO Lead | Next prompt version |
| LL-v1.9-03 | High-risk pre-sprint decisions checklist | Yes | PMO Lead | cycle_summary.md template |
| LL-v1.9-04 | Spec alignment items as story items | Positive reinforcement | — | Keep pattern |
