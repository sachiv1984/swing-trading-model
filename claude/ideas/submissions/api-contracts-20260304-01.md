**Owner:** API Contracts & Documentation Owner
**Class:** Planning Document (Class 4)
**Status:** Advancing
**Submitted by:** API Contracts & Documentation Owner
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-api-contracts-20260304-01

---

# Idea: Running API Changelog Document

## 1. Problem Statement

There is no centralised changelog tracking what changed in the API between releases. Consumers of the API — the frontend, the CI validation endpoint, and any future integrations — must compare API contract markdown files across git commits to understand what changed and why. The v1.7 EPIC-06 work updated three endpoint specs (analytics, portfolio, and trade) to versions 1.9.0 — but there is no single document where a consumer can read "in v1.9.0 of portfolio_endpoints, field X was added and field Y's description was corrected." The API versioning decision record (created in v1.7) specifies a 60-day deprecation timeline for breaking changes — but consumers can only observe the deprecation timeline if they know a deprecation has been announced.

## 2. Strategic Alignment

Section reference: docs/product/decisions/api-versioning-v1.7.md — "60-day deprecation timeline; consumers must be notified of deprecations"

Alignment rationale: The API versioning policy requires that consumers are notified of breaking changes with a 60-day window. A changelog is the notification mechanism. Without it, the 60-day policy exists on paper but is unenforceable — consumers have no channel through which to receive deprecation notices. The changelog directly enables the policy to function as designed.

## 3. Proposed Solution

Create `docs/specs/api_contracts/API_CHANGELOG.md` — a Class 2 supporting document updated with every API contract change. Each entry contains: version, date, endpoints affected, change type (Added field, Modified field, Deprecated field, Breaking change), and a brief description. Breaking changes are flagged with the deprecation deadline. The API Contracts owner updates the changelog as part of every PR that modifies an endpoint spec. The Head of Specs Team enforces this as a mandatory companion to any contract update.

## 4. Expected Value

Enables consumers to track breaking changes without scanning git diffs. Supports the 60-day deprecation window by providing a clear deprecation announcement channel. Measurable as: proportion of API changes that appear in the changelog within 24 hours of the PR merge (target: 100%).

## 5. Effort Estimate

- [x] Small — days to 1 week

Constraints or dependencies: Requires retroactively documenting changes made in v1.7 to bootstrap the changelog with a starting entry. Ongoing maintenance requires discipline in the PR review process.

## 6. Reversibility

- [x] Fully reversible — no lasting effects

Reasoning: A document can be archived; removing it does not affect API function.

## 7. What Would You Stop?

No view — leave to debate.

## 8. Submitter Recommendation

- [x] Now — should be in the next roadmap cycle

Reasoning: The API versioning policy (EPIC-05) was completed in v1.7 but the changelog — the enabling mechanism of the policy — was not created. Without it, the policy is incomplete.

---

## Intake Review

*Completed by the roadmap rebalance engine (STEP 4). Do not fill in this section.*

| Field | Value |
|-------|-------|
| STEP 4 classification | ✅ Advancing |
| Classification date | 2026-03-04 |
| Classified by | Product Owner |
| STEP 5 outcome | ✅ Advance — promoted to backlog (operational prerequisite for versioning policy) |
| Outcome date | 2026-03-04 |
| Notes | |
