**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Submitted
**Submitted by:** Head of Specs Team
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-head-of-specs-20260304-02

---

# Idea: Spec Coverage Inventory

## 1. Problem Statement

It is currently unknown which product features have canonical specifications and which are undocumented. The v1.7 EPIC-06 work surfaced spec debt in analytics, portfolio, and trade endpoints — but only because we happened to look. There is no systematic map of coverage. Features implemented without specs create technical debt that accumulates silently: the system behaves in a way that was never intentionally specified, and when something changes, there is no baseline to verify against. We are flying partially blind.

## 2. Strategic Alignment

Section reference: §14 — Authority statement ("if a behaviour can affect trading outcomes, it must be specified here")

Alignment rationale: The Head of Specs Team is responsible for ensuring "the specification ecosystem is coherent, authoritative, owned, and evolvable." A coverage inventory is the prerequisite for all four properties — you cannot ensure a spec ecosystem is authoritative if you do not know what it covers. Making coverage visible is the first step toward closing every gap.

## 3. Proposed Solution

Create `docs/specs/spec_coverage_inventory.md` — a Class 2 supporting document listing all product features (endpoints, UI components, calculation behaviours) and for each: whether a canonical spec exists, which spec covers it, the spec version, and the date last reviewed. Features with no spec are flagged as "unspecified." The inventory is reviewed and updated at the start of each release cycle.

## 4. Expected Value

Makes spec debt visible and actionable. Enables systematic prioritisation of spec work rather than reactive gap-filling. Target: every feature rated "unspecified" in the first inventory becomes a backlog item. Expected to reveal 5–15 unspecified or under-specified features in the first pass, given the v1.7 spec debt findings.

## 5. Effort Estimate

- [x] Small — days to 1 week

Constraints or dependencies: Requires collaboration with all spec domain owners to self-report coverage. Should be run as a structured survey rather than a solo audit.

## 6. Reversibility

- [x] Fully reversible — no lasting effects

Reasoning: The inventory is a reference document; removing it does not affect system behaviour.

## 7. What Would You Stop?

No view — leave to debate. The inventory is a low-effort input to roadmap prioritisation; it does not compete directly with delivery work.

## 8. Submitter Recommendation

- [x] Now — should be in the next roadmap cycle

Reasoning: Every cycle we run without a coverage map, new features may be delivered without specs. The inventory pays for itself in the first cycle where it prevents an unspecified feature from reaching production.

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
