**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Published
**Cycle:** 2026-06-16__release-v5.7
**Last Updated:** 2026-06-16

---

# Release Plan — v5.7

**Theme:** Staging Verification Completion, SI-05 Effectiveness Review & Engineering/Governance Patches

---

## Readiness

**Lifecycle status:** Closed (post-ship complete, next_cycle_unblocked: true)
**Prior cycle:** 2026-06-16__release-v5.6 — 10/10 stories, zero deviations
**Next release declared:** v5.7 (roadmap header + state.json `next_release`)

**§-1.2 note:** v5.7 cleared via post-ship closure `next_release: "v5.7"` and roadmap "Next planned release: v5.7" (equivalent to STEP 8.1 Option(a) declaration; formal Now section to be added at next scheduled rebalance).

**Carry-forwards addressed:** 5 of 6 from v5.6 lessons_learnt_closure.md (see run_manifest.md).

**Gate proximity:**
- BLG-FE-64: gate 2026-06-21 (5 days) — within Sprint 1 window
- BLG-GOV-112/115 + BLG-OPS-59: gate 2026-07-04 (18 days) — Sprint 2 conditional
- PT-04: 13 closed trades, trajectory accelerating — not in scope this cycle; monitor

---

## Scope

| S2-ID | Item | Source | Priority | Effort | Sprint |
|-------|------|--------|----------|--------|--------|
| S2-01 | Staging Verification Suite (v5.6 deferred production measurements) | BLG-OPS-66/67/68/69 + BLG-FE-75 | P2–P3 | XS–S | 1 |
| S2-02 | Arc 5 Playwright Coverage Gaps | BLG-QA-56/57/58 | P3 | XS×3 | 1 |
| S2-03 | Governance & Engineering Patches | BLG-FE-64 (cond.), lazy-import doc, execution_prompt dual sign-off | P2–P3 | XS–S | 1 |
| S2-04 | SI-05 Effectiveness Review & Post-Deploy Metrics | BLG-GOV-112 + BLG-GOV-115 + BLG-OPS-59 | P2 | S×3 | 2 (cond.) |

**Items explicitly deferred from this cycle:**
- PT-04 Setup Quality Score — gate NOT MET (13/20 closed trades); monitor closely
- SI-02 frontend — gate NOT MET (need 20+ closed trades with linked trade_plans)
- BLG-GOV-74 (AI quarterly review) — gate 2026-08-29
- All Arc 4/6 items — data density gates not met

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01, S2-02 | Infrastructure & Operations Owner; Director of Quality | RISK-01 (staging env access) | None — independent |
| EPIC-02 | S2-03 | Head of Specs Team; Head of Backend Engineering | RISK-02 (BLG-FE-64 gate) | None — independent |
| EPIC-03 | S2-04 | Product Owner; Infrastructure & Operations Owner | RISK-03 (2026-07-04 gate) | After Sprint 1 close; gate must clear before Sprint 2 planning |

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | BLG-OPS-66–69 require production environment access for latency measurement; environment availability not guaranteed | Medium | Batch all 4 measurement runs into a single staging session to minimise coordination overhead | null |
| RISK-02 | EPIC-02 | BLG-FE-64 gate (2026-06-21) falls within Sprint 1; if sprint closes before gate date, item returns to backlog (4th deferral) | Low | Gate is calendar-based and unambiguous; sprint window should easily accommodate; PO disposition confirmed | null |
| RISK-03 | EPIC-03 | Sprint 2 conditional on 2026-07-04 SI-05 effectiveness review; sprint 2 EPICs may be skipped if gate not actionable | Low | All 3 Sprint 2 items have the same gate date; if gate clears mid-sprint-2, all proceed together | null |

---

## Capacity Check

**Sprint 1 — EPIC-01 (8 stories, XS–S):**
- ST-01/02/03/05: 4 × XS staging verifications = ~2–4 hrs total
- ST-04: 1 × S staging verification = ~2–3 hrs
- ST-06/07/08: 3 × XS Playwright additions = ~1–2 hrs
- EPIC-01 subtotal: ~5–9 hrs

**Sprint 1 — EPIC-02 (3 stories, XS–S):**
- ST-09: XS conditional (gate 2026-06-21) = ~1 hr
- ST-10: S backend engineering doc = ~1–2 hrs
- ST-11: S governance patch verification = ~1 hr
- EPIC-02 subtotal: ~3–4 hrs

**Sprint 1 total: ~8–13 hrs. Well within solo-dev sprint capacity.**

**Sprint 2 — EPIC-03 (3 stories, S, conditional):**
- ST-12/13/14: 3 × S effectiveness review items = ~3–4.5 hrs total
- EPIC-03 subtotal: ~3–4.5 hrs (conditional — only if gate 2026-07-04 clears)

**Overall capacity verdict: PASS** — no phasing required.

### Phasing Recommendation
Not required (PASS verdict). Sprint 1 and Sprint 2 naturally partitioned by gate dates. Sprint 1 is fully within solo-dev capacity at ~8–13 hrs. Sprint 2 conditional block adds ≤4.5 hrs if gate clears.

---

## Integrity Validation — 3.5 Local Model Integrity

- All S2 IDs map to EPICs: S2-01→EPIC-01, S2-02→EPIC-01, S2-03→EPIC-02, S2-04→EPIC-03 ✓
- All EPIC IDs declared with Maps-to ✓
- All RISK IDs appear in risk register ✓
- No orphaned references ✓
- All scope items are from active backlog (verified) or lesson-learnt actions (carry-forward authority) ✓
- EPIC-03 conditional flag documented ✓

**Result: PASS**

---

## Cross-Stage Integrity (STEP 5.5)

- All S2 IDs map to EPICs: ✓
- All EPIC IDs in stage4_backlog_slice.md match stage3: ✓
- All RISK IDs in EPIC table appear in Risk Register: ✓
- No orphaned references: ✓
- Decisions record: N/A (no High-priority risks requiring decision records this cycle)

**Result: PASS**
