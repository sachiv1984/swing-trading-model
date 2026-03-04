**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Submitted
**Submitted by:** Head of Specs Team
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-head-of-specs-20260304-01

---

# Idea: Canonical Terms Glossary

## 1. Problem Statement

Key system terms — "portfolio value", "P&L", "stop", "ATR", "R-Multiple", "value" — are each defined within their respective specs but there is no single authoritative glossary document. New spec owners must read five or more documents to build a mental model of core concepts. Worse, there is active risk of semantic drift: a term used in `metrics_definitions.md` may carry a subtly different meaning from the same term in `data_model.md`, and without a canonical glossary that drift is invisible until it causes a defect. This is a systemic coherence gap.

## 2. Strategic Alignment

Section reference: §14 — Authority statement ("this document is the single source of truth for production strategy behaviour")

Alignment rationale: The governance model depends on every spec being authoritative within its domain and coherent with all other specs. The Head of Specs Team is responsible for ensuring "core concepts have a single source of truth and consistent meaning across specs." A canonical glossary is the structural mechanism for delivering this. Without it, coherence is aspirational rather than enforced.

## 3. Proposed Solution

Create `docs/specs/canonical_glossary.md` — a Class 1 canonical document defining all key system terms with: (1) the authoritative definition, (2) cross-references to the spec sections that govern the concept, and (3) explicitly noted exclusions (what this term does not mean). All spec owners are required to reference the glossary for shared terms rather than redefining them locally. The glossary is updated whenever a new term is introduced or an existing definition is revised.

## 4. Expected Value

Reduces onboarding time for new spec owners from approximately 4–6 hours of cross-document reading to 30 minutes. Makes semantic drift detectable: any divergence between a spec's local usage and the glossary definition becomes visible in PR review. Target outcome: zero undetected semantic drift instances per release cycle after the glossary is adopted.

## 5. Effort Estimate

- [x] Small — days to 1 week

Constraints or dependencies: Requires input from all domain spec owners to validate their terms. Should be done as a workshop rather than solo authorship.

## 6. Reversibility

- [x] Fully reversible — no lasting effects

Reasoning: The glossary is a standalone reference document; removing it reverts to the current distributed state with no loss of existing functionality.

## 7. What Would You Stop?

If this is prioritised, I would suggest deferring any further individual spec authorship until the glossary is in place — adding more specs without a shared vocabulary compounds the coherence problem.

## 8. Submitter Recommendation

- [x] Now — should be in the next roadmap cycle

Reasoning: Every new spec authored without a canonical glossary adds to the semantic drift risk. The cost of retrofitting a glossary grows with each new spec; the cost of doing it now is low.

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
