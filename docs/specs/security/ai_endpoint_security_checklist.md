**Owner:** Cybersecurity & Trust Lead
**Class:** Governance (Class 3)
**Status:** Published
**Version:** 1.0
**Last Updated:** 2026-07-30
**Story:** ST-05 (BLG-SEC-23, EPIC-02, v8.0)

---

# Mandatory Security Review Checklist — New AI-Calling Endpoints

## Purpose

This is a short, mandatory security review, distinct from `docs/specs/api_contracts/ai_advisory_contract_checklist.md`'s contract-completeness checklist. That checklist confirms the endpoint's *contract documentation* is complete (rate limit numbers stated, §13 boundary fields present, openapi.yaml updated); this checklist confirms the *security posture* itself was actually reviewed before the endpoint's design is approved — rate limiting, cost gating, and prompt-injection awareness. Both are required; neither substitutes for the other.

Referenced from the design gate process (`claude/system/design_gate_prompt.md` §2.2) — any sprint item introducing a new endpoint that calls an LLM (Claude or any other model provider) must complete this checklist before its design artefact is approved.

---

## Checklist

For each new AI-calling endpoint, confirm all three items below. Mark: **PASS** / **FAIL** / **N/A** (N/A requires a stated reason).

### 1. Rate Limiting

| Check | Requirement |
|-------|-------------|
| Per-IP or per-user rate limit defined | A concrete requests/minute figure is chosen before implementation (see `services/rate_limiter.py` for the existing limiter pattern used by `/ai/daily-briefing` (10/min) and `/ai/chat` (30/min)) |
| HTTP 429 response documented | The endpoint's contract entry in `docs/specs/api_contracts/` states the 429 response shape and `Retry-After` header, matching `ai_advisory_contract_checklist.md` CC-01 |

**Why it matters:** an LLM-calling endpoint is the most expensive and most abusable request shape in the API — an unbounded endpoint is a direct cost-exhaustion and DoS vector.

### 2. Cost Gating

| Check | Requirement |
|-------|-------------|
| Token usage is logged | Every call logs to `claude_audit_log` via `create_claude_audit_entry` (matching `ai_advisory_contract_checklist.md` CC-02) — this is the data source for cost monitoring, not a separate mechanism |
| A cost ceiling or circuit-breaker exists, or the absence of one is an explicit accepted risk | Either (a) a per-user/per-day call cap or spend ceiling is enforced, or (b) the reviewer explicitly records why the existing rate limit alone is judged sufficient for this endpoint's risk profile (e.g. low request volume, low per-call token cost) |

**Why it matters:** rate limiting bounds request *frequency*; it does not bound *cost* if a single request can be made arbitrarily expensive (e.g. an unbounded input length driving up token count). This item forces an explicit decision rather than a silent gap.

### 3. Prompt-Injection Awareness

| Check | Requirement |
|-------|-------------|
| Every external input reaching the prompt is inventoried | List each input (user-supplied field, database value, external API response) that is interpolated into the prompt, and its insertion point (user-role message vs. system-prompt string) — system-prompt interpolation of unsanitized input is materially higher risk than user-role placement (see `docs/specs/security/ai_injection_risk_assessment.md` Input 2 for the concrete precedent this checklist item exists to catch) |
| SRB-v1.7 display-only constraint confirmed | The endpoint's response is display-only and does not feed into signals, scoring, compliance checks, or trade execution — this is the primary harm limiter and must be true for every new AI-calling endpoint per `strategy_rules.md` §13 |

**Why it matters:** `docs/specs/security/ai_injection_risk_assessment.md` found that unsanitized input interpolated directly into a system-prompt f-string (rather than passed via the API's user-role message) has a materially higher injection-success probability. This item exists so that distinction is checked at design time, before the pattern is repeated.

---

## Disposition

Record the outcome as a short sign-off block at the end of the endpoint's design artefact or contract section:

```
**AI Endpoint Security Checklist (docs/specs/security/ai_endpoint_security_checklist.md v1.0):**
- Rate limiting: PASS/FAIL/N/A — <one line>
- Cost gating: PASS/FAIL/N/A — <one line>
- Prompt-injection awareness: PASS/FAIL/N/A — <one line>
- Signed off by: Cybersecurity & Trust Lead
- Date: <date>
```

A **FAIL** on any item blocks the design gate from marking the item's design artefact approved until resolved or explicitly accepted as a documented risk (matching the accepted-risk pattern already used in `ai_injection_risk_assessment.md`'s Open Risk Summary).

---

## Relationship to Existing Documents

- `docs/specs/api_contracts/ai_advisory_contract_checklist.md` — contract-completeness checklist (§13 boundary + documentation checks); this document does not replace it. Both apply.
- `docs/specs/security/ai_injection_risk_assessment.md` — the original deep-dive risk assessment for the two existing AI endpoints (`/ai/daily-briefing`, `/ai/chat`); this checklist generalises its input-inventory method into a reusable, forward-looking design-time step for future endpoints, rather than re-deriving the same analysis from scratch each time.

---

## Sign-Off

| Role | Decision | Date |
|------|----------|------|
| Cybersecurity & Trust Lead | Approved — checklist adopted as a mandatory design-gate step for all future AI-calling endpoints | 2026-07-30 |

*Sign-off completed by Sprint Execution Engine under agent-mediated governance protocol — ST-05 AC.*
