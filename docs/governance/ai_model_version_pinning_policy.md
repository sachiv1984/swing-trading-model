**Owner:** AI Compliance & Governance Officer; Head of Specs Team
**Class:** Governance Document (Class 1)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-28
**Cycle:** 2026-05-27__release-v4.2 (ST-02, BLG-GOV-64)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# AI Model Version Pinning Policy

## 1. Purpose

This policy governs how Claude (Anthropic) model versions are selected and managed for all Claude-backed features in the Momentum Trading Assistant. It ensures that model version changes are deliberate, governed, and auditable — preventing silent capability drift from version promotions.

**Scope note:** This policy applies to all backend service modules that call the Anthropic API, regardless of filename. This includes `backend/services/gemini_service.py` (legacy filename — implements Claude API thesis generation) and `backend/services/ai_service.py` (Claude API journal summary).

---

## 2. Pinning Rule

**All Claude-backed features must pin to a specific, explicit model ID. The use of alias, "latest" identifiers, or runtime environment variable overrides for model selection is prohibited in production code.**

| Requirement | Rule |
|-------------|------|
| Model identifier format | Must be the full versioned model ID (e.g. `claude-haiku-4-5`, `claude-haiku-4-5-20251001`) |
| "Latest" alias | Prohibited in production — aliases resolve to different models over time without a deliberate decision |
| Runtime env-var override | Prohibited — `os.getenv("AI_MODEL", default)` or similar patterns bypass governance and are not permitted |
| Model ID location | Defined as a `MODEL_VERSION` named constant in the service module |
| Code review gate | Any change to a `MODEL_VERSION` constant requires AI Compliance Officer sign-off before merge |

---

## 3. Current Implementation Status

| Feature | Endpoint | Current Model ID | Service Module | Constant Name | Status |
|---------|----------|-----------------|----------------|---------------|--------|
| Trade plan thesis generation | `POST /trade-plans/{plan_id}/generate-thesis` | `claude-haiku-4-5` | `backend/services/gemini_service.py:21` | `MODEL_VERSION` | ✅ Pinned |
| Full plan generation | `POST /trade-plans/generate-plan` | `claude-haiku-4-5` | `backend/services/gemini_service.py:21` | `MODEL_VERSION` | ✅ Pinned |
| Journal summary | `POST /ai/journal-summary` | `claude-haiku-4-5-20251001` | `backend/services/ai_service.py` | `MODEL_VERSION` | ✅ Pinned (v4.2 ST-02 — removed prior `AI_MODEL` env-var override) |

**Verification:** Both service modules declare a `MODEL_VERSION` constant and pass it directly to `client.messages.create(model=MODEL_VERSION, ...)`. No alias or runtime env-var override is used as of v4.2.

**Note on model IDs:** `gemini_service.py` uses `claude-haiku-4-5` and `ai_service.py` uses `claude-haiku-4-5-20251001`. These are distinct versioned identifiers from Anthropic. Both are valid pinned IDs. Any future alignment to a single canonical ID requires this policy's change management procedure (§4).

---

## 4. Change Management Procedure

A model version update is a **governed change** that requires:

### 4.1 Trigger Conditions

A model version update may only be initiated when one or more of the following conditions are met:

- The current pinned model is deprecated or end-of-life by Anthropic
- A QA-verified performance improvement justifies the upgrade (must be measurable and documented)
- A security advisory requires immediate version rotation
- AI Compliance Officer recommends an upgrade based on capability assessment

### 4.2 Change Process

| Step | Action | Owner |
|------|--------|-------|
| 1 | File a backlog item describing the proposed model version change with rationale | AI Compliance & Governance Officer |
| 2 | Conduct QA re-test of all Claude-backed features against the new model version | Director of Quality |
| 3 | AI Compliance Officer sign-off: approve the change | AI Compliance & Governance Officer |
| 4 | Update `MODEL_VERSION` constant(s) in the relevant service file(s) | Head of Engineering |
| 5 | Update this document's §3 table with the new model ID and effective date | Head of Specs Team |
| 6 | Update `docs/ops/gemini_cost_tracking.md` (legacy filename for Claude cost tracking) with new model pricing | FinOps & Resource Architect |
| 7 | Merge via standard PR with `[EPIC-xx][ST-xx]` commit format | Product Owner + Director of Quality |

### 4.3 Emergency Version Rotation

If a security advisory requires immediate model version rotation:

1. AI Compliance Officer and Cybersecurity & Trust Lead jointly review and approve the emergency rotation in writing before the commit is made
2. Change is committed using `[GOVERNANCE] Emergency model version rotation: <old>→<new>` commit format
3. QA re-test must be completed within 48 hours of the emergency rotation
4. This document must be updated within the same sprint
5. Even emergency rotations must not be merged without the joint written approval in step 1 — no unreviewed direct-to-main pushes are permitted under any circumstance

---

## 5. Non-Compliance Consequences

Any production deployment with an unpinned model identifier (alias, "latest", or runtime env-var override) is a P1 governance deviation:

- Must be remediated in the current sprint
- Must be documented in `qa_evidence_EPIC-xx.md` and backlog
- PR merge is blocked until the pinned model ID is confirmed and the runtime override is removed

---

## 6. Review Schedule

This policy is reviewed:
- At each major Anthropic SDK version upgrade
- Annually by the AI Compliance & Governance Officer
- Whenever a new Claude-backed feature is added to the system

---

## 7. Sign-Off

| Role | Status | Date |
|------|--------|------|
| AI Compliance & Governance Officer | Approved (agent-mediated) | 2026-05-28 |
| Head of Specs Team | Approved (agent-mediated) | 2026-05-28 |
