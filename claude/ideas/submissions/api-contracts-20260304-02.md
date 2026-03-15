**Owner:** API Contracts & Documentation Owner
**Class:** Planning Document (Class 4)
**Status:** Promoted-Added
**Submitted by:** API Contracts & Documentation Owner
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-api-contracts-20260304-02

---

# Idea: Automated OpenAPI Drift Detection in CI

## 1. Problem Statement

The Head of Specs Team has mandated (in the head_of_specs_team.md charter §5) that the openapi.yaml file and the canonical markdown API contracts must be reviewed simultaneously in any PR that changes API behaviour. However, there is no automated enforcement of this requirement. A PR that updates a canonical markdown contract but not the openapi.yaml will pass CI without detection. Similarly, a PR that updates the openapi.yaml without a corresponding canonical contract update is equally undetected. The mandate exists; the enforcement mechanism does not.

## 2. Strategic Alignment

Section reference: Head of Specs Team §5 — "Mandatory Enforcement: API Contracts & OpenAPI Alignment — when canonical API contracts change, the API Contracts owner must review both the canonical Markdown contracts and the openapi.yaml inline, in the same pull request"

Alignment rationale: The API Contracts owner's mandate is to ensure the openapi.yaml remains aligned with the canonical markdown contracts. Automated detection closes the gap between the Head of Specs Team's mandated policy and what is actually enforced. Without it, the policy relies entirely on reviewer discipline — which is insufficient for a canonical spec alignment requirement.

## 3. Proposed Solution

Add a CI step that: (1) identifies any PR that modifies files in `docs/specs/api_contracts/*.md`, (2) checks whether the same PR also modifies `docs/reference/openapi.yaml`, and (3) if the markdown contract changed but the OpenAPI spec did not, adds a blocking label ("openapi-review-required") and posts a PR comment requesting the OpenAPI review. The step does not enforce content alignment (which requires human review) — it enforces the procedural requirement that both files are reviewed in the same PR.

## 4. Expected Value

Eliminates silent OpenAPI drift caused by PRs that update canonical contracts without reviewing the OpenAPI spec. Enforces the Head of Specs Team's mandatory requirement automatically, removing reliance on reviewer discipline. Measurable as: proportion of contract-changing PRs where the OpenAPI review is completed in the same PR (target: 100%).

## 5. Effort Estimate

- [x] Small — days to 1 week

Constraints or dependencies: Requires a simple CI script (a git diff check is sufficient) and GitHub label configuration. No infrastructure changes needed.

## 6. Reversibility

- [x] Fully reversible — no lasting effects

Reasoning: A CI script can be disabled or removed trivially.

## 7. What Would You Stop?

No view — leave to debate.

## 8. Submitter Recommendation

- [x] Now — should be in the next roadmap cycle

Reasoning: The mandate exists but is unenforced. Every PR since the mandate was written that changed a contract without the OpenAPI review is a retroactive compliance gap. The fix is trivial.

---

## Intake Review

*Completed by the roadmap rebalance engine (STEP 4). Do not fill in this section.*

| Field | Value |
|-------|-------|
| STEP 4 classification | ✅ Advancing |
| Classification date | 2026-03-04 |
| Classified by | Product Owner |
| STEP 5 outcome | ✅ Advance — promoted to backlog (interim enforcement; long-term: auto-generation) |
| Outcome date | 2026-03-04 |
| Notes | |
