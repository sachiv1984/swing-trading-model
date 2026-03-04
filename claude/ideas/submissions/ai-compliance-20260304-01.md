**Owner:** AI Compliance & Governance Officer
**Class:** Planning Document (Class 4)
**Status:** Submitted
**Submitted by:** AI Compliance & Governance Officer
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-ai-compliance-20260304-01

---

# Idea: AI-Assisted Workflow Governance Policy

## 1. Problem Statement

Claude Code and equivalent AI tools are actively used in this governance workflow to generate specs, write code, commit to branches, create PRs, and make architectural decisions. There is no formal document defining what AI tools are authorised to do versus what requires explicit human review. The current practice is governed by the CLAUDE.md system anchor and governance prompts, but these define the process — not the policy on AI authority boundaries. An AI agent that commits a strategy rule change, modifies a canonical spec, or merges a PR without the required human gates would violate the governance model. The policy for preventing this is implicit, not explicit.

## 2. Strategic Alignment

Section reference: AI Compliance §4.1 — "define where and how AI may be used; establish prohibited and constrained AI behaviors; prevent silent expansion of AI authority"

Alignment rationale: The AI Compliance mandate requires an explicit AI usage policy. The current governance model relies on prompt-based constraints that are session-scoped and version-controlled, but there is no canonical document that a human reviewer can consult to verify whether AI behaviour in a given session was within authorised bounds. The policy is the mechanism for making AI authority boundaries auditable.

## 3. Proposed Solution

Create `docs/governance/ai_usage_policy.md` — a Class 1 canonical document defining: (1) authorised AI actions (file creation within write scope, commit preparation, spec draft generation, analysis and calculation), (2) prohibited AI actions (autonomous merges, strategy rule changes without human review, modification of sealed artefacts), (3) required human review steps for AI-generated artefacts (spec changes, strategy changes, any commit to main), and (4) the process for auditing AI actions after the fact.

## 4. Expected Value

Makes AI authority boundaries explicit and auditable. Provides a reference that human reviewers can use to assess whether AI behaviour in a given session was within policy. Prevents silent expansion of AI authority as capabilities grow. Required foundation for any future external audit of the governance process.

## 5. Effort Estimate

- [x] Small — days to 1 week

Constraints or dependencies: Requires input from the Head of Specs Team (what counts as a canonical artefact change), the PMO Lead (what actions require human gate), and the Product Owner (what decisions require human sign-off).

## 6. Reversibility

- [x] Fully reversible — no lasting effects

Reasoning: A policy document can be revised; it does not change system behaviour.

## 7. What Would You Stop?

No view — leave to debate.

## 8. Submitter Recommendation

- [x] Now — should be in the next roadmap cycle

Reasoning: AI tool usage in this workflow is growing. The longer the policy is absent, the larger the gap between what AI has been doing and what is formally authorised.

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
