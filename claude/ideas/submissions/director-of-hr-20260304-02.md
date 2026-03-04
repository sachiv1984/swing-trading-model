**Owner:** Director of HR
**Class:** Planning Document (Class 4)
**Status:** Submitted
**Submitted by:** Director of HR
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-director-of-hr-20260304-02

---

# Idea: Role Accountability Matrix (RACI)

## 1. Problem Statement

While individual role charters define each role's responsibilities, there is no consolidated view showing which role is accountable for which decision type when multiple roles are involved. In governance processes such as the roadmap engine, idea intake, and sprint execution, the same decision (e.g., "should this spec be classified as Class 1?") may involve the Head of Specs Team, the relevant domain owner, and the Product Owner — with no single document clearly stating who has the final call. This ambiguity is resolved ad hoc by reading multiple charters during live decision-making, which is inefficient and error-prone under time pressure.

## 2. Strategic Alignment

Section reference: claude/charter/team_charter.md — authority model

Alignment rationale: The RACI matrix is the operational implementation of the team charter's authority model. Where the charter defines individual roles, the RACI defines how those roles interact on cross-role decisions. Without it, the authority model is only legible to someone who has read all 23 role charters — which is not a reasonable expectation. The RACI makes the authority model legible in a single reference.

## 3. Proposed Solution

Create `docs/governance/raci_matrix.md` — a Class 4 planning document (reviewed annually or when role charters change) mapping key decision types to Accountable, Responsible, Consulted, and Informed roles. Decision types to cover: (1) canonical spec authorship and change, (2) strategy rule change, (3) roadmap add/remove, (4) production deployment, (5) data model schema change, (6) CI gate change, (7) agent role addition, (8) governance process change. For each decision type, one role is Accountable (final call) and others are Responsible, Consulted, or Informed.

## 4. Expected Value

Reduces time to resolve cross-role conflicts from "read all relevant charters" to "consult one row of the RACI matrix." Makes the authority model legible to any role owner without charter archaeology. Measurable as: reduction in time spent resolving authority boundary disputes during governance routines.

## 5. Effort Estimate

- [x] Small — days to 1 week

Constraints or dependencies: Requires validation by all role owners that the matrix correctly reflects their charter. Should be ratified by the Head of Specs Team as canonical.

## 6. Reversibility

- [x] Fully reversible — no lasting effects

Reasoning: A reference matrix can be revised; it creates no structural or technical commitments.

## 7. What Would You Stop?

No view — leave to debate.

## 8. Submitter Recommendation

- [x] Soon — worth debating in the next 2–3 cycles

Reasoning: Important for governance clarity but requires careful validation with all 23 role owners. Should be prioritised in the cycle immediately following the onboarding guide, which establishes the authority model as the primary reference point.

---

## Intake Review

*Completed by the roadmap rebalance engine (STEP 4). Do not fill in this section.*

| Field | Value |
|-------|-------|
| STEP 4 classification | |
| Classification date | |
| Classified by | Product Owner |
| STEP 5 outcome | |
| Outcome date | |
| Notes | |
