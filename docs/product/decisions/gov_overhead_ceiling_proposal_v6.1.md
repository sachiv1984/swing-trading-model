---
**Owner:** PMO Lead; Head of Specs Team
**Class:** Decision Support Document (Class 4)
**Status:** Proposal — Awaiting Head of Specs Team and PMO Lead Review
**Version:** 0.1
**Date:** 2026-06-23
**Story:** ST-03 (EPIC-01, v6.1) — BLG-GOV-131
**Spec references:** `claude/system/roadmap_prompt.md` STEP 2.4, STEP 7.1
---

# Governance Overhead Ceiling Metric — Proposal v6.1

## 1. Context and Motivation

The roadmap process already tracks governance overhead in two places:

1. **STEP 2.4** (`user_value_ratio`): looks back at 5 cycles and classifies stories as U / G / D / P. Fires a Product Value Alert when `user_value_ratio < 0.30` (< 30% user-facing stories).

2. **STEP 7.1** (`Skill-Silo Alert`): looks back at 3 cycles. Fires at > 40% G+D+P stories. Scope is capacity planning, not accountability.

**Gap:** Neither mechanism provides a governance-specific ceiling with a clear accountability owner, a consistent 5-cycle window, and a threshold calibrated to the observed pattern where governance overhead creeps up gradually across multiple cycles without triggering a single-cycle gate.

The v6.1 sprint planning notes flagged EPIC-01 Sprint 2 as "G+D+P%: 75% — above Skill-Silo ceiling (structural; see sprint_planning_notes.md)". This was treated as structural and noted without an accountable response required. This proposal adds the missing accountability layer.

---

## 2. Proposed Metric Definition

**Name:** Governance Overhead Percentage (G+D+P%)

**Formula:**
```
G+D+P% = (G + D + P stories) ÷ total stories delivered × 100
          — computed over a rolling 5-cycle window (matching STEP 2.4 window)
```

**Story classifications** (reuse STEP 2.4 taxonomy):
- **U** — User-facing feature or visible UX improvement
- **G** — Governance / prompt / process work
- **D** — Debt clearance (spec, QA, ops baseline, audit, pre-planning)
- **P** — Pre-work for a future feature (pre-design, pre-planning, pre-spec)

Note: G+D+P% = (1 − user_value_ratio) × 100. These are complementary views of the same data — user_value_ratio measures what users gained; G+D+P% measures the overhead cost.

**Window:** Rolling 5 completed cycles (same as STEP 2.4). Excludes cycles where ≤ 2 stories were shipped (micro-cycles with forced returns distort the percentage).

---

## 3. Proposed Alert Threshold

**Alert threshold: G+D+P% ≥ 60% over the rolling 5-cycle window.**

Rationale:
- The STEP 7.1 > 40% ceiling applies to a 3-cycle window and is already active. A 5-cycle window naturally smooths more, so the threshold should be higher than 40%.
- 60% means ≥ 3 in 5 stories are non-user-facing — a pattern that indicates systemic tilt away from product delivery.
- 50% would be the mathematical midpoint but would duplicate the STEP 2.4 Product Value Alert (user_value_ratio < 0.50) without adding new signal.
- 70%+ is too permissive given the observed 81.8% baseline (see §4).

---

## 4. Prior 5-Cycle Baseline Data (AC-04)

The following table is derived from `docs/product/changelog.md` for the 5 most recently completed cycles. Stories returned to backlog are excluded; only shipped stories are counted.

| Cycle | Release | Stories Shipped | U | G | D | P | G+D+P | G+D+P% |
|-------|---------|----------------|---|---|---|---|-------|--------|
| 2026-06-10__release-v5.5 | v5.5 | 10 | 2 | 3 | 5 | 0 | 8 | 80.0% |
| 2026-06-16__release-v5.6 | v5.6 | 10 | 2 | 1 | 7 | 0 | 8 | 80.0% |
| 2026-06-17__release-v5.7 | v5.7 | 10 | 0 | 1 | 9 | 0 | 10 | 100.0% |
| 2026-06-17__release-v5.8 | v5.8 | 2 | 1 | 1 | 0 | 0 | 1 | 50.0% |
| 2026-06-18__release-v5.9 | v5.9 | 11 | 1 | 8 | 2 | 0 | 10 | 90.9% |
| **5-cycle total** | — | **43** | **6** | **14** | **23** | **0** | **37** | **86.0%** |

> Note: v5.8 shipped 2 stories (3 were returned); included per methodology since > 2 stories shipped.

**Status vs proposed threshold:** 86.0% >> 60% ceiling. **Alert would fire.**

### v6.0 Context (cycle completed but outside 5-cycle window)

| Cycle | Release | Stories Shipped | U | G | D | P | G+D+P | G+D+P% |
|-------|---------|----------------|---|---|---|---|-------|--------|
| 2026-06-22__release-v6.0 | v6.0 | 11 | 4 | 3 | 2 | 2 | 7 | 63.6% |

v6.0 shows the overhead ratio declining as user-facing features (Morning Briefing, net-of-costs, Screener quality panel) were delivered. The 5-cycle window as of v6.1 planning (cycles v5.6–v6.0) would yield **~78%** — still above the proposed 60% ceiling.

---

## 5. Proposed Accountability Mechanism

When G+D+P% ≥ 60% in the rolling 5-cycle window, the following actions are mandatory:

1. **STEP 2.4 addition:** Facilitator computes and records G+D+P% alongside user_value_ratio in the `run_manifest.md` Product Value Ratio Diagnostic table.

2. **Alert label:** "Governance Overhead Alert" — recorded in the STEP 2.4 section of `cycle_record.md` and surfaced at STEP 8.

3. **Mandatory response:** PO must provide a written rationale explaining why the overhead level is acceptable for the next cycle. One of:
   - **Planned reduction:** "Next cycle contains ≥ N U-classified items" (name them)
   - **Structural justification:** "Overhead is temporary due to [named debt clearance or arc transition]"
   - Vague rationale ("catching up", "expected") is not valid — the overhead narrative must name the specific items driving it.

4. **Backlog pull-forward obligation:** If PO cannot provide a structural justification, a user-facing item from the Now horizon must be added to the current cycle scope before STEP 8 concludes (same mechanism as STEP 7.1 Skill-Silo Alert pull-forward).

5. **STEP 7.1 coordination:** The existing Skill-Silo Alert (3-cycle, > 40%) continues to operate independently. If both alerts fire, the pull-forward obligation becomes double-weighted: two user-facing items must be identified (though only one needs to be added to current scope if capacity is constrained).

---

## 6. Draft Amendment to roadmap_prompt.md STEP 2.4

> **Implementation note:** Per CLAUDE.md §6, any modification to files in `claude/system/` requires Head of Specs Team sign-off. The following is a draft proposal only — no changes to `roadmap_prompt.md` should be committed until sign-off is obtained.

### Current STEP 2.4 text (extract)

> Compute: `user_value_ratio = U stories ÷ total stories` across the 5 cycles (one decimal, e.g. 0.42).
>
> | Ratio | Status | Action |
> |-------|--------|--------|
> | ≥ 0.50 | Healthy | Record and continue |
> | 0.30–0.49 | Advisory | Facilitator surfaces in STEP 8 before final decisions |
> | < 0.30 | **Product Value Alert** | Challenger must treat this as equivalent weight to a §13 concern — requires explicit PO written response before STEP 8 concludes; pull-forward of a user-facing backlog item is mandatory unless PO provides written rationale |

### Proposed Addition (to be inserted after the user_value_ratio table)

```markdown
**Governance Overhead Percentage (G+D+P%):**

Compute: `G+D+P% = (G + D + P stories) ÷ total stories × 100` across the same 5 cycles.
Record the 5-cycle breakdown table (cycle, U, G, D, P, G+D+P%) in `run_manifest.md` under
`## Product Value Ratio Diagnostic`.

| G+D+P% | Status | Action |
|--------|--------|--------|
| < 60% | Healthy | Record and continue |
| ≥ 60% | **Governance Overhead Alert** | Facilitator surfaces at STEP 8. PO must provide written rationale (planned reduction naming specific U items, or structural justification naming the debt/arc transition). Vague rationale is invalid. If no structural justification: pull-forward of ≥ 1 user-facing Now-horizon item is mandatory (same rule as STEP 7.1 Skill-Silo Alert). |

Note: G+D+P% = (1 − user_value_ratio) × 100. If both alerts fire (Product Value Alert and
Governance Overhead Alert), the obligations are cumulative: PO must address both in writing and
identify ≥ 1 pull-forward candidate.
```

### Rationale for placement in STEP 2.4 (not STEP 7.1)

STEP 7.1 already has a 3-cycle, > 40% Skill-Silo check. Adding the 5-cycle G+D+P% alert to STEP 2.4 means:
- It runs at the same time as user_value_ratio (same data, same window)
- It is recorded in `run_manifest.md` alongside the existing ratio table (consistent documentation)
- It surfaces at STEP 8 via the same path as the Product Value Alert (PO accountability)

---

## 7. Questions for Head of Specs Team and PMO Lead Review

1. **Threshold:** Is 60% the right ceiling, or should it be calibrated to the observed historical range (80–100%) with a more permissive threshold for the first 2–3 cycles post-adoption?

2. **v5.8 micro-cycle:** v5.8 shipped only 2 stories (5 were returned). Should micro-cycles (≤ 3 shipped stories) be excluded from the window calculation to avoid distortion?

3. **Double-obligation clause:** Is the double pull-forward obligation (when both Skill-Silo Alert and Governance Overhead Alert fire) appropriate, or does it duplicate existing STEP 7.1 incentives?

4. **Adoption date:** Should this amendment apply retroactively from the current cycle, or from the next planning cycle after sign-off?

---

## 8. Next Steps

- **Head of Specs Team + PMO Lead:** Review this proposal and provide written response on the 3 questions in §7.
- **If approved:** Sprint Execution Engine to implement the STEP 2.4 draft amendment in `claude/system/roadmap_prompt.md` per CLAUDE.md §6 governance edit checklist (version bump, OPERATIONAL_GUIDE update, prompt_change_log.md entry).
- **If amendment rejected or modified:** PMO Lead to document decision rationale and file updated proposal.

**This document is a proposal. No prompt files have been modified.**
