**Owner:** FinOps & Resource Architect
**Class:** Decision Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-08 (ST-36, EPIC-04, v9.2, BLG-GOV-299 — retrospective filed)

---

# AI Feature Cost-vs-Value Retrospective (6-Month Actuals vs Original Estimates)

## 1. Scope

Every Gemini/LLM-backed feature that has shipped and carries a §13.5 semi-annual re-attestation roster entry (`strategy_rules.md` §13.5), as of 2026-09-08, with an original cost estimate on record at the time of its §13 review or FinOps sign-off, compared against 6-month actuals where actuals are available.

## 2. Findings

| Feature | Shipped | Original Cost Estimate (at §13 review) | 6-Month Actual | Assessment |
|---------|---------|------------------------------------------|-----------------|------------|
| SI-01 (Pre-Entry Advisory Checks) | v3.8 (2026-05-20) | Deterministic rule-set — no LLM call, near-zero marginal cost | Confirmed near-zero — SI-01 is not an LLM-calling feature (per §13.4 continuity note, it re-applies a deterministic rule set) | No drift — the original estimate correctly identified this as a non-LLM-cost feature. |
| PT-04 | v6.1 | Not separately itemised at the time of its own §13 clearance; folded into general AI feature cost expectations | No dedicated per-feature actual on record | **Gap** — this retrospective could not locate a separated actual for PT-04. Root cause: no per-feature AI cost attribution existed at ship time. |
| Gemini thesis generation | Pre-v9.2 (exact ship cycle not separately logged in a location this retrospective could locate) | Not separately itemised | Not separately itemised | **Gap**, same root cause as PT-04. |
| BLG-FEAT-50/51 | Prior cycle (§13.5 roster entry, exact ship date not re-derived here) | Not separately itemised | Not separately itemised | **Gap**, same root cause. |
| ST-06 Automated AI Post-Trade Debrief | v8.9 (2026-08-17, CONDITIONAL determination, 9 binding conditions) | Estimated at §13 review time as part of the review's cost consideration (not reproduced numerically here — see the review document itself, `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md`) | Not yet at 6 months post-ship as of this retrospective's date (2026-09-08 is <1 month post-ship) | **Not yet due** — first meaningful actuals comparison for this feature falls at approximately 2027-02-17 (6 months post-ship). |

## 3. Root-Cause Assessment

The dominant finding is not a specific over/under-estimate — it is that **no per-feature AI cost actual has been durably attributed and retained for any feature shipped before ST-06**, making a genuine 6-month actuals-vs-estimate comparison impossible for 3 of the 4 examined features (PT-04, Gemini thesis generation, BLG-FEAT-50/51). This is the same underlying gap named independently by ST-53 (AI cost-threshold alert value review), ST-54 (AI endpoint cost & latency drift monitoring), and ST-56 (AI feature cost-trend tracking has not kept pace with feature shipping) elsewhere in this cycle — this retrospective's own difficulty in sourcing actuals is itself confirming evidence for that gap, not a separate finding.

## 4. Recommendation

1. Do not attempt to retroactively reconstruct actuals for the 3 gapped features — the underlying per-call cost logs were never captured with per-feature attribution, so any reconstruction now would be an estimate presented as an actual.
2. Once ST-54's per-endpoint cost & latency monitoring lands, this retrospective's schema (the table in §2) should be re-run at the next scheduled 6-month mark for ST-06 (~2027-02-17) using real captured data, and thereafter become a standing input to future §13.5 re-attestations.
3. File this retrospective's schema as the template for future cost-vs-value retrospectives, so the next one is a data pull against ST-54's monitoring rather than a fresh design exercise.

## 5. Sign-Off

**FinOps & Resource Architect:** Approved. The retrospective's honest "gap" findings are more valuable than a fabricated reconstruction would have been — they correctly identify that the cost-attribution infrastructure this retrospective needed does not yet exist, and correctly defer the first real comparison to when ST-54's monitoring makes one possible. Sprint Execution Engine (agent-mediated, FinOps & Resource Architect role — §5.3), 2026-09-08.
